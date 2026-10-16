"""Child for P15 resource-supervised TRAIN-only pilot/full reconstruction.

Not a standalone entry point. Only P15_SUPERVISED launcher supplies go.signal and
heartbeat. Never invokes the historical Phase-9 main(), never opens official TEST.
"""
from __future__ import annotations
import argparse
import gc
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import sys
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/models/run_unsw_phase9_final_holdout.py'
TRAIN=ROOT/'data/raw/unsw-nb15/UNSW_NB15_training-set.csv'
FREEZE=ROOT/'results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json'
SUBSETS=ROOT/'results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json'
FROZEN={'random_forest_17','random_forest_42','stacking_42'}
EXPECTED_HASHES={
 'data/raw/unsw-nb15/UNSW_NB15_training-set.csv':'bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa',
 'src/models/run_unsw_phase9_final_holdout.py':'3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480',
 'results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json':'cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6',
 'results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json':'5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be',
}


def stream_hash(path):
    h=hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def audit_csv(event,args):
    if event != 'open' or not args or not isinstance(args[0], (str,bytes,os.PathLike)): return
    try:p=Path(args[0]).resolve()
    except (OSError,ValueError,TypeError):return
    # Defense in depth: disallow all raw/interim/processed CSV reads except official TRAIN.
    if p.suffix.lower()=='.csv':
        if p.name.lower() == 'unsw_nb15_testing-set.csv'.lower():
            raise PermissionError('P15 worker forbids official TEST')
        if (ROOT/'data') in p.parents and p!=TRAIN:
            raise PermissionError('P15 worker forbids non-TRAIN dataset CSV: '+str(p))


def validate_frame(frame,features,categorical):
    import numpy as np
    import pandas as pd
    if frame.empty or frame.columns.duplicated().any() or list(frame.columns)!=list(features):
        raise ValueError('Invalid ordered nonempty feature schema')
    if frame.isna().any().any():raise ValueError('Missing values')
    for feature in features:
        if feature in categorical:
            if not frame[feature].map(lambda x:isinstance(x,str)).all():raise ValueError('Non-string category '+feature)
        else:
            if not pd.api.types.is_numeric_dtype(frame[feature]):raise ValueError('Non-numeric '+feature)
            if not np.isfinite(frame[feature].to_numpy(dtype=float)).all():raise ValueError('Non-finite '+feature)
    return frame


def heartbeat_thread(heartbeat,stop):
    while not stop.wait(1):
        try:
            if time.time()-heartbeat.stat().st_mtime>20:
                os._exit(91)  # Parent died/stalled: child fails closed, no runaway training.
        except OSError:
            os._exit(92)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',required=True,choices=sorted(FROZEN))
    parser.add_argument('--mode',required=True,choices=('pilot','full'))
    parser.add_argument('--pilot-rows',required=True,type=int)
    parser.add_argument('--cpu-cores',required=True,type=int)
    parser.add_argument('--out-dir',required=True,type=Path)
    args=parser.parse_args()
    if os.environ.get('P15_WATCHED')!='1':raise SystemExit('Refuse: start via p15_local_supervisor.py')
    out=args.out_dir.resolve(strict=True)
    if out.name!='worker' or not out.parent.name.startswith('p15_local_'):
        raise SystemExit('Unsafe output directory')
    if out.parent.parent!=(ROOT/'results/reproducibility').resolve():
        raise SystemExit('Output outside reproducibility')
    start=out.parent/'go.signal'
    # No TRAIN/ML import prior to supervisor admitting the child and fixing CPU affinity.
    for _ in range(200):
        if start.exists():break
        time.sleep(0.1)
    else:raise SystemExit('No watchdog start authorization within 20 s')
    heartbeat=out.parent/'heartbeat'
    if not heartbeat.exists():raise SystemExit('Watchdog heartbeat missing')
    stop=threading.Event()
    thread=threading.Thread(target=heartbeat_thread,args=(heartbeat,stop),daemon=True)
    thread.start()
    sys.dont_write_bytecode=True
    sys.addaudithook(audit_csv)
    import psutil
    affinity=psutil.Process().cpu_affinity()
    if not affinity or len(affinity)>args.cpu_cores:raise RuntimeError('CPU affinity not enforced')
    # Locked input hashes checked immediately before fit, after supervisor checks.
    for rel,expected in EXPECTED_HASHES.items():
        if stream_hash(ROOT/rel)!=expected:raise ValueError('Frozen provenance changed: '+rel)
    import numpy as np
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from threadpoolctl import threadpool_limits
    spec=importlib.util.spec_from_file_location('p15_frozen_builder_isolated',SOURCE)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module) # module main() only runs when __name__=='__main__'
    frozen=json.loads(FREEZE.read_text(encoding='utf-8'))
    module.validate_freeze_manifest(frozen)
    frame=pd.read_csv(TRAIN,low_memory=False)
    if len(frame)!=175341 or set(frame.label.unique())!={0,1} or int((frame.label==0).sum())!=56000:
        raise ValueError('Unexpected official TRAIN rows or labels')
    tracks=module.load_feature_tracks(frame)
    models=module.build_frozen_models(tracks,frozen)
    conf=models[args.candidate]
    features=conf['features']
    if len(features) != (17 if args.candidate=='random_forest_17' else 42):
        raise ValueError('Frozen feature count mismatch')
    if args.mode=='pilot':
        idx,_=train_test_split(np.arange(len(frame)),train_size=args.pilot_rows,
                               stratify=frame['label'],random_state=42)
        train=frame.iloc[idx].copy()
    else:
        train=frame
    X=train.loc[:,features]
    y=train.label.to_numpy(dtype=int)
    # Validation is TRAIN-sourced software roundtrip, never benchmark/holdout quality.
    probe=validate_frame(X.iloc[:min(16,len(X))].copy(),features,module.CATEGORICAL_COLS)
    fit_start=time.monotonic()
    model=conf['model']
    with threadpool_limits(limits=1):
        model.fit(X,y)
    fit_seconds=time.monotonic()-fit_start
    probabilities=model.predict_proba(probe)
    if not (probabilities.shape==(len(probe),2) and np.isfinite(probabilities).all()
            and np.all((probabilities>=0)&(probabilities<=1))
            and np.allclose(probabilities.sum(axis=1),1)):
        raise RuntimeError('Probability contract failed')
    if model.classes_.tolist()!=[0,1] or float(conf['threshold'])!=0.5:
        raise RuntimeError('Class mapping / frozen threshold violation')
    # Explicitly reject missing/extra/invalid inputs before recording model validity.
    numeric=next(c for c in features if c not in module.CATEGORICAL_COLS)
    bad_inputs={
      'missing_column':probe.drop(columns=[features[0]]),
      'extra_target_column':probe.assign(label=1),
      'non_numeric':probe.assign(**{numeric:'invalid'}),
      'non_finite':probe.assign(**{numeric:np.inf}),
      'missing_value':probe.assign(**{numeric:np.nan}),
      'empty_frame':probe.iloc[:0],
    }
    for label,bad in bad_inputs.items():
        try:validate_frame(bad,features,module.CATEGORICAL_COLS)
        except ValueError:pass
        else:raise RuntimeError('Negative schema contract failed: '+label)
    checks={'passed':True,'mode':args.mode,'candidate':args.candidate,
       'train_rows':len(train),'feature_count':len(features),'classes':model.classes_.tolist(),
       'threshold':0.5,'fit_seconds':round(fit_seconds,4),
       'eval':'TRAIN-derived sample for roundtrip ONLY; no generalization metric'}
    if args.mode=='full':
        # Compress final artifact separately; do not retain two full model copies during reload.
        temp=out/(args.candidate+'.joblib.tmp')
        final=out/(args.candidate+'_RECONSTRUCTED_FULL_TRAIN.joblib')
        joblib.dump(model,temp,compress=3)
        del model
        gc.collect()
        restored=joblib.load(temp)  # Only load the object just written by this run.
        after=restored.predict_proba(probe)
        if not np.allclose(probabilities,after,rtol=1e-12,atol=1e-12):
            raise RuntimeError('Serialize/reload roundtrip numerical mismatch')
        if not np.array_equal(probabilities[:,1]>=0.5,after[:,1]>=0.5):
            raise RuntimeError('Serialize/reload roundtrip labels mismatch')
        del restored
        gc.collect()
        temp.rename(final)
        checks['artifact']={'filename':final.name,'sha256':stream_hash(final),'bytes':final.stat().st_size,
                            'scope':'RECONSTRUCTED_FULL_TRAIN; NOT original trained artifact'}
        checks['roundtrip_numeric_atol_rtol']=1e-12
    # Never serialize pilot models as final artifacts.
    for rel,expected in EXPECTED_HASHES.items():
        if stream_hash(ROOT/rel)!=expected:raise ValueError('Frozen provenance modified during run: '+rel)
    checks['package_versions']={n:importlib.metadata.version(n) for n in
       ('numpy','pandas','scikit-learn','scipy','joblib','threadpoolctl','psutil')}
    checks['ordered_features']=list(features)
    checks['input_sha256']=EXPECTED_HASHES
    checks['python']=sys.version
    checks['cpu_affinity']=affinity
    checks['leakage_guard']='only official TRAIN CSV permitted inside project data/'
    checks['no_test_evaluation']=True
    (out/'worker_result.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False),encoding='utf-8')
    stop.set()
    print(json.dumps({'candidate':args.candidate,'mode':args.mode,'passed':True,
                     'train_rows':len(train),'fit_seconds':fit_seconds}),flush=True)

if __name__=='__main__':main()
