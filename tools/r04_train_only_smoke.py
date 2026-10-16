"""Isolated fit/serialize/reload smoke; only official TRAIN, no research metrics."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TRAIN=ROOT/'data/raw/unsw-nb15/UNSW_NB15_training-set.csv'
SOURCE=ROOT/'src/models/run_unsw_phase9_final_holdout.py'
FREEZE=ROOT/'results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json'
SUBSETS=ROOT/'results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_frame(frame,features,categorical):
    import numpy as np
    import pandas as pd
    if frame.empty:raise ValueError('Input has no rows')
    if frame.columns.duplicated().any():raise ValueError('Duplicate columns')
    missing=set(features)-set(frame.columns)
    extra=set(frame.columns)-set(features)
    if missing or extra:raise ValueError('Schema mismatch: missing='+repr(sorted(missing))+' extra='+repr(sorted(extra)))
    if frame.isna().any().any():raise ValueError('Missing input values')
    for name in features:
        if name in categorical:
            if not frame[name].map(lambda x:isinstance(x,str)).all():raise ValueError('Non-string categorical value: '+name)
        else:
            if not pd.api.types.is_numeric_dtype(frame[name]):raise ValueError('Non-numeric input: '+name)
            if not np.isfinite(frame[name].to_numpy(dtype=float)).all():raise ValueError('Non-finite input: '+name)
    return frame.loc[:,features]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',required=True,type=Path)
    args=parser.parse_args()
    out=args.out_dir.resolve()
    out.relative_to(ROOT/'results/reproducibility')
    out.mkdir(parents=True,exist_ok=False)
    dataset_reads=[]
    def audit(event,values):
        if event!='open' or not isinstance(values[0],(str,bytes)):return
        try:p=Path(values[0]).resolve()
        except (ValueError,TypeError):return
        if p.suffix.lower()=='.csv' and (ROOT/'data') in p.parents:
            if p!=TRAIN:raise PermissionError('Smoke contract forbids reading other dataset CSV: '+str(p))
            dataset_reads.append(p.relative_to(ROOT).as_posix())
    sys.addaudithook(audit)
    import numpy as np
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from threadpoolctl import threadpool_limits
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('historical_builders_for_smoke',SOURCE)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    manifest=json.loads(FREEZE.read_text(encoding='utf-8'))
    module.validate_freeze_manifest(manifest)
    frame=pd.read_csv(TRAIN,low_memory=False)
    tracks=module.load_feature_tracks(frame)
    features=tracks['all_features']
    pool,_=train_test_split(np.arange(len(frame)),train_size=2500,stratify=frame['label'],random_state=42)
    train_index,validation_index=train_test_split(pool,train_size=2000,stratify=frame.iloc[pool]['label'],random_state=137)
    xtrain=frame.iloc[train_index][features]
    xvalid=frame.iloc[validation_index][features]
    ytrain=frame.iloc[train_index]['label']
    checks=dict(train_rows_2000=len(train_index)==2000,validation_rows_500=len(validation_index)==500,indices_disjoint=not bool(set(train_index)&set(validation_index)),labels_0_1=set(ytrain)=={0,1},features_42=len(features)==42,features_17=len(tracks['stable_17_features'])==17,excluded_identifiers=not bool(set(features)&{'id','label','attack_cat'}),isolated_environment=sys.prefix!=sys.base_prefix)
    if not all(checks.values()):raise ValueError('Preflight failed: '+repr(checks))
    candidates=module.build_frozen_models(tracks,manifest)
    details={}
    schema={}
    (out/'smoke_models').mkdir()
    for name,item in candidates.items():
        model=item['model']; selected=item['features']
        valid=validate_frame(xvalid[selected],selected,module.CATEGORICAL_COLS)
        start=time.perf_counter()
        with threadpool_limits(limits=2):model.fit(xtrain[selected],ytrain)
        fit_seconds=time.perf_counter()-start
        proba=model.predict_proba(valid)
        checks[name+'_proba_contract']=bool(proba.shape==(500,2) and np.isfinite(proba).all() and (proba>=0).all() and (proba<=1).all() and np.allclose(proba.sum(axis=1),1))
        checks[name+'_classes']=model.classes_.tolist()==[0,1]
        path=out/'smoke_models'/(name+'_SMOKE_ONLY.joblib')
        joblib.dump(model,path,compress=3)
        loaded=joblib.load(path)
        again=loaded.predict_proba(valid)
        checks[name+'_roundtrip_numeric']=bool(np.allclose(proba,again,rtol=1e-12,atol=1e-12))
        checks[name+'_roundtrip_labels_exact']=bool(np.array_equal(proba[:,1]>=item['threshold'],again[:,1]>=item['threshold']))
        schemas=dict(features=selected,categorical=[f for f in selected if f in module.CATEGORICAL_COLS],threshold=item['threshold'],scope='SMOKE_ONLY_TRAIN_SUBSET; not a final demo model')
        schema[name]=schemas
        details[name]=dict(fit_seconds=fit_seconds,sha256=digest(path),bytes=path.stat().st_size,threshold=item['threshold'],train_rows=2000,validation_rows=500,feature_count=len(selected),roundtrip_bitwise=bool(np.array_equal(proba,again)),roundtrip_max_abs=float(np.max(np.abs(proba-again))),probability_tolerance=dict(rtol=1e-12,atol=1e-12),scope='software smoke; no scientific performance metrics')
        # Negative input contracts exercise real inference preconditions.
        numeric=next(f for f in selected if f not in module.CATEGORICAL_COLS)
        bad={
          'missing_column':valid.drop(columns=[selected[0]]),
          'target_leak_extra':valid.assign(label=1),
          'non_numeric':valid.assign(**{numeric:'invalid'}),
          'infinity':valid.assign(**{numeric:np.inf}),
          'missing_value':valid.assign(**{numeric:np.nan}),
          'empty':valid.iloc[:0],
          'duplicate_column':pd.concat([valid,valid[[selected[0]]]],axis=1),
        }
        for case,data in bad.items():
            try:validate_frame(data,selected,module.CATEGORICAL_COLS)
            except ValueError:checks[name+'_reject_'+case]=True
            else:checks[name+'_reject_'+case]=False
        unknown=valid.iloc[:2].copy()
        cat=schemas['categorical'][0]
        unknown[cat]='__R04_UNSEEN_CATEGORY__'
        unknown=validate_frame(unknown,selected,module.CATEGORICAL_COLS)
        checks[name+'_unknown_category_handled']=bool(np.isfinite(loaded.predict_proba(unknown)).all())
        print(name+': fit/serialize/reload/schema checks finished',flush=True)
    checks['only_TRAIN_dataset_read']=bool(dataset_reads) and set(dataset_reads)=={TRAIN.relative_to(ROOT).as_posix()}
    metadata=dict(timestamp=datetime.now(timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),executable=sys.executable,environment_original='UNKNOWN; this is a new smoke environment',versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','scikit-learn','scipy','joblib','threadpoolctl']},input_sha256={p.relative_to(ROOT).as_posix():digest(p) for p in [TRAIN,SOURCE,FREEZE,SUBSETS]},sampling=dict(seed_pool=42,seed_split=137,train_index_sha256=hashlib.sha256(np.asarray(train_index,dtype='<i8').tobytes()).hexdigest(),validation_index_sha256=hashlib.sha256(np.asarray(validation_index,dtype='<i8').tobytes()).hexdigest(),validation_source='official TRAIN only'),dataset_csv_reads=sorted(set(dataset_reads)),models=details,scope='SMOKE_ONLY; no official TEST evaluation, no tuning, no final model reproduction')
    (out/'schema.json').write_text(json.dumps(schema,indent=2),encoding='utf-8')
    (out/'run_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    (out/'validation.json').write_text(json.dumps(dict(checks=checks,passed=all(checks.values()),scope=metadata['scope']),indent=2),encoding='utf-8')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),scope='SMOKE_ONLY_TRAIN_SUBSET')))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
