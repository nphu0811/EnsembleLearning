"""Diagnose serialized RF prediction scheduling without refitting or TEST."""
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    import joblib
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    sys.dont_write_bytecode=True
    out=ROOT/'results/reproducibility/r04_smoke_roundtrip_diagnosis'
    out.mkdir(exist_ok=False)
    train=ROOT/'data/raw/unsw-nb15/UNSW_NB15_training-set.csv'
    frame=pd.read_csv(train,low_memory=False)
    pool,_=train_test_split(np.arange(len(frame)),train_size=2500,stratify=frame['label'],random_state=42)
    _,valid=train_test_split(pool,train_size=2000,stratify=frame.iloc[pool]['label'],random_state=137)
    schema=json.loads((ROOT/'results/reproducibility/r04_ml_smoke/schema.json').read_text())
    name='random_forest_17'
    x=frame.iloc[valid][schema[name]['features']]
    path=ROOT/'results/reproducibility/r04_ml_smoke/smoke_models/random_forest_17_SMOKE_ONLY.joblib'
    model=joblib.load(path)
    baseline=model.predict_proba(x)
    parallel=[model.predict_proba(x) for _ in range(5)]
    parallel_diffs=[float(np.max(np.abs(baseline-p))) for p in parallel]
    # Scheduling only: do not change fitted trees, configs, or saved artifact.
    model.set_params(model__n_jobs=1)
    serial=model.predict_proba(x)
    serial_runs=[model.predict_proba(x) for _ in range(5)]
    reload=joblib.load(path)
    reload.set_params(model__n_jobs=1)
    other=reload.predict_proba(x)
    result=dict(hypothesis='Parallel tree probability summation order produces tiny floating point differences, not model serialization corruption',model_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),parallel_max_abs_diffs=parallel_diffs,serial_exact_repeats=[bool(np.array_equal(serial,p)) for p in serial_runs],serial_reload_exact=bool(np.array_equal(serial,other)),parallel_vs_serial_max_abs=float(np.max(np.abs(baseline-serial))),parallel_serial_labels_identical=bool(np.array_equal(baseline[:,1]>=0.5,serial[:,1]>=0.5)),probability_tolerance=dict(rtol=1e-12,atol=1e-12),parallel_within_tolerance=all(bool(np.allclose(baseline,p,rtol=1e-12,atol=1e-12)) for p in parallel),scope='Diagnostic using saved SMOKE model and same TRAIN validation subset only; no refit, no TEST, no scientific metric')
    result['hypothesis_supported']=bool(any(d>0 for d in parallel_diffs) and all(result['serial_exact_repeats']) and result['serial_reload_exact'] and result['parallel_within_tolerance'] and result['parallel_serial_labels_identical'])
    (out/'diagnosis.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
