"""P21 child: one RF42-LITE resource smoke fit on official TRAIN only.

NOT a scientific validation. The held-out internal fold is never passed to
preprocessor.fit, model.fit, predict, or any quality metric. The pilot checks
split feasibility, run time, memory, fit-only model construction and schema.
Run ONLY when admitted by tools/p21_pilot_supervisor.py, NEVER standalone.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import threading
import time

from p21_pilot_guards import ROOT, TRAIN, TRAIN_REL, audit_file_open, sha256_stream


def heartbeat_watch(path: Path, stop: threading.Event):
    while not stop.wait(1):
        try:
            if time.time() - path.stat().st_mtime > 20:
                os._exit(91)
        except OSError:
            os._exit(92)


def fingerprint_and_split(frame, features, seed):
    """Full TRAIN group disjointness before any model fit; collision fail-closed."""
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import StratifiedGroupKFold

    X = frame.loc[:, features]
    if X.isna().any().any() or X.columns.duplicated().any():
        raise ValueError("Missing/duplicate feature columns; no grouping permitted")
    hashes = pd.util.hash_pandas_object(X, index=False).astype("uint64")
    duplicate = hashes.duplicated(keep=False)
    if duplicate.any():
        # Check a 64-bit hash never merges two different vectors.
        dup = X.loc[duplicate].copy()
        dup["_p21_group_hash"] = hashes.loc[duplicate].to_numpy()
        if (dup.groupby("_p21_group_hash", sort=False, dropna=False)[features]
                .nunique(dropna=False).gt(1).any(axis=1).any()):
            raise ValueError("Hash collision: different vectors mapped to same group")
    y = frame["label"].to_numpy(dtype=int)
    skf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
    fit_idx, val_idx = next(skf.split(X=np.zeros((len(frame), 1)), y=y, groups=hashes))
    fit_hash = set(hashes.iloc[fit_idx].tolist())
    val_hash = set(hashes.iloc[val_idx].tolist())
    if fit_hash & val_hash or set(fit_idx.tolist()) & set(val_idx.tolist()):
        raise ValueError("TRAIN/validation row or vector group overlap")
    ratio = len(val_idx) / len(frame)
    original_normal = float((y == 0).mean())
    val_normal = float((y[val_idx] == 0).mean())
    if (ratio < 0.18 or ratio > 0.22 or
            abs(val_normal - original_normal) > 0.02 or
            set(y[fit_idx].tolist()) != {0, 1} or
            set(y[val_idx].tolist()) != {0, 1}):
        raise ValueError(f"Predetermined group split QA failed: val_ratio={ratio:.6f}; normal_diff={abs(val_normal-original_normal):.6f}")
    return fit_idx, val_idx, {
        "method": "StratifiedGroupKFold", "seed": seed,
        "validation_fold": 0, "fit_rows": int(len(fit_idx)),
        "validation_rows": int(len(val_idx)),
        "validation_ratio": round(ratio, 6),
        "validation_normal_fraction": round(val_normal, 6),
        "fit_normal_fraction": round(float((y[fit_idx] == 0).mean()), 6),
        "group_disjoint": True, "row_disjoint": True,
        "validation_evaluation_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--pilot-rows", required=True, type=int)
    args = parser.parse_args()
    if os.environ.get("P21_STACK_WATCHED") != "1":
        raise SystemExit("P21 child cannot run without resource supervisor")
    if not (1000 <= args.pilot_rows <= 20000):
        raise SystemExit("Pilot size must be 1000..20000")
    out = args.out_dir.resolve(strict=True)
    if out.name != 'worker' or not out.parent.name.startswith('p21_train_only_pilot_stacklite_') or out.parent.parent != (ROOT / 'results/controlled_extensions').resolve():
        raise PermissionError('Wrong supervised RQ5 directory')
    gate = out.parent / "go.signal"
    for _ in range(200):
        if gate.is_file() and gate.read_text(encoding="utf-8").strip() == "P21_STACK_LITE_PILOT_ONLY":
            break
        time.sleep(0.1)
    else:
        raise SystemExit("No supervisor approval signal")
    heartbeat = out.parent / "heartbeat"
    if not heartbeat.is_file():
        raise SystemExit("Missing supervisor heartbeat")
    done = threading.Event()
    threading.Thread(target=heartbeat_watch, args=(heartbeat, done), daemon=True).start()
    sys.dont_write_bytecode = True
    sys.addaudithook(audit_file_open)

    import numpy as np
    import pandas as pd
    import psutil
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    from threadpoolctl import threadpool_limits

    config = json.loads((ROOT / "config/p21_train_only_protocol_2026_10_18.json").read_text(encoding="utf-8"))
    if (config["training_authorized"] is not False or
            config["source"]["raw_train"] != TRAIN_REL or
            config["model"]["decision_threshold"] != 0.5 or
            config["runtime"]["worker_concurrency"] != 1):
        raise ValueError("P21 design contract changed; abort")
    expected_sha = config["source"]["sha256"]
    if sha256_stream(TRAIN) != expected_sha:
        raise ValueError("official TRAIN checksum changed")
    affinity = psutil.Process().cpu_affinity()
    if not affinity or len(affinity) != 1:
        raise RuntimeError("Supervisor has not restricted worker to one logical CPU")
    frame = pd.read_csv(TRAIN, low_memory=False)
    features = [x for x in frame.columns if x not in config["source"]["excluded_predictors"]]
    if len(frame) != 175341 or len(features) != 42 or set(frame.label.unique()) != {0, 1}:
        raise ValueError("Unexpected dataset shape / feature schema / label")
    if frame[features].isna().any().any():
        raise ValueError("Raw features have nulls; pilot refuses to infer handling")
    fitting, held_out, split_meta = fingerprint_and_split(frame, features, config["split"]["seed"])
    # Pilot sample is drawn ONLY from fit pool. Held-out rows are never fitted or predicted.
    fit_rows, _ = train_test_split(fitting, train_size=args.pilot_rows,
                                   stratify=frame.iloc[fitting]["label"],
                                   random_state=config["replication"]["seeds"][0])
    pilot = frame.iloc[fit_rows]
    y = pilot.label.to_numpy(dtype=int)
    X = pilot.loc[:, features]
    categoricals = [c for c in config["source"]["categorical_predictors"] if c in features]
    numeric = [c for c in features if c not in categoricals]
    preprocessor = ColumnTransformer(transformers=[
        ("num", "passthrough", numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categoricals)
    ], remainder="drop")
    rfcfg = config["model"]["common_rf"]
    from sklearn.ensemble import StackingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import StratifiedKFold
    scfg = config["model"]["stacking_lite"]
    if (scfg["inner_cv"] != 3 or scfg["inner_cv_seed"] != 137 or
        scfg["base_learners"] != ["logistic_regression","decision_tree","random_forest"] or
        scfg["stack_method"] != "predict_proba" or scfg["passthrough"] is not False):
        raise ValueError("Stacking preset changed; abort")
    seed = config["replication"]["seeds"][0]
    def make_preprocessor():
        return ColumnTransformer([
            ("num","passthrough",numeric),
            ("cat",OneHotEncoder(handle_unknown="ignore"),categoricals)
        ], remainder="drop")
    estimators = [
        ("lr", Pipeline([
            ("preprocess", make_preprocessor()),
            ("scale", StandardScaler(with_mean=False)),
            ("model", LogisticRegression(
                C=scfg["base_lr"]["C"],solver=scfg["base_lr"]["solver"],
                max_iter=1000,random_state=seed))
        ])),
        ("dt", Pipeline([
            ("preprocess",make_preprocessor()),
            ("model",DecisionTreeClassifier(
                min_samples_leaf=scfg["base_dt"]["min_samples_leaf"],
                random_state=seed))
        ])),
        ("rf", Pipeline([
            ("preprocess",make_preprocessor()),
            ("model",RandomForestClassifier(
                n_estimators=rfcfg["n_estimators"],
                min_samples_leaf=rfcfg["min_samples_leaf"],
                max_features=rfcfg["max_features"],
                bootstrap=rfcfg["bootstrap"],class_weight=None,
                random_state=seed,n_jobs=1))
        ]))
    ]
    model = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(
            C=scfg["meta_lr"]["C"],solver=scfg["meta_lr"]["solver"],
            class_weight=None,random_state=seed,max_iter=1000),
        cv=StratifiedKFold(n_splits=3,shuffle=True,random_state=137),
        stack_method="predict_proba",passthrough=False,n_jobs=1
    )
    started=time.monotonic()
    with threadpool_limits(limits=1):
        model.fit(X,y)
    seconds=round(time.monotonic()-started,3)
    if list(model.classes_) != [0,1]:
        raise RuntimeError("Stacking class schema mismatch")
    del model
    if sha256_stream(TRAIN) != expected_sha:
        raise ValueError("Official TRAIN file changed during smoke test")
    result = {
        "passed": True,
        "scope": "P21_STACK_LITE_FIT_ONLY_RESOURCE_PILOT; no RQ result",
        "source_path":TRAIN_REL,"source_sha256":expected_sha,
        "train_file_rows":len(frame),"pilot_fit_rows":len(pilot),
        "pilot_fit_class_counts":{str(int(k)):int(v) for k,v in zip(*np.unique(y,return_counts=True))},
        "feature_count":len(features),"split":split_meta,
        "pilot_component":"A4_STACK42_LITE",
        "inner_cv_folds":3,"inner_cv_seed":137,"fit_seconds":seconds,
        "official_test_opened":False,"validation_predicted":False,
        "scientific_metrics_calculated":False,"model_artifact_saved":False,
        "versions":{name:importlib.metadata.version(name)
                    for name in ("numpy","pandas","scikit-learn","scipy","psutil")}
    }
    (out / "worker_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    done.set()
    print(json.dumps({"passed":True,"fit_seconds":seconds,"validation_scored":False}),flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
