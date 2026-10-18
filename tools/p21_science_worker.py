"""P21 scientific seed worker: five predeclared arms, TRAIN-derived validation ONLY.

Launch solely via tools/p21_science_supervisor.py after author opt-in.
Never opens official TEST, frozen P9 model outputs, or report PDFs.
All features / preprocessing / over-sampling / OOF folds are FIT-only.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import threading
import time

from p21_pilot_guards import ROOT, TRAIN, TRAIN_REL, audit_file_open, sha256_stream
from p21_pilot_worker import fingerprint_and_split, heartbeat_watch


def worker_scope(out: Path, seed: int) -> None:
    base = (ROOT / "results" / "controlled_extensions").resolve(strict=True)
    path = out.resolve(strict=True)
    if (out.is_symlink() or path.name != "worker" or
            path.parent.parent != base or
            path.parent.name != f"p21_train_only_science_seed_{seed}"):
        raise PermissionError("Worker scope must be dedicated sealed science seed directory")
    if out.parent.is_symlink():
        raise PermissionError("Symlink seed directory forbidden")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("P21_SCIENCE_WATCHED") != "1":
        raise SystemExit("Scientific seed worker must be supervised")
    out = args.out_dir.resolve(strict=True)
    worker_scope(out, args.seed)
    gate = out.parent / "go.signal"
    for _ in range(200):
        if gate.is_file() and gate.read_text(encoding="utf-8").strip() == "P21_TRAIN_ONLY_SCIENCE_SEED":
            break
        time.sleep(0.1)
    else:
        raise SystemExit("No supervised authorization gate")
    heartbeat = out.parent / "heartbeat"
    if not heartbeat.is_file():
        raise SystemExit("No supervisor heartbeat")
    done = threading.Event()
    threading.Thread(target=heartbeat_watch, args=(heartbeat, done), daemon=True).start()
    sys.dont_write_bytecode = True
    sys.addaudithook(audit_file_open)

    import numpy as np
    import pandas as pd
    import psutil
    from sklearn.model_selection import train_test_split
    from threadpoolctl import threadpool_limits
    from p21_science_core import (
        ARM_IDS, binary_metrics, fit_ids_digest, inner_group_folds,
        make_rf, make_stacking,
    )
    from p21_selector_core import fit_only_stable17
    from p21_rq5_sampling import prepare_arm, arm_metadata

    config_path = ROOT / "config" / "p21_train_only_protocol_2026_10_18.json"
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if (cfg["training_authorized"] is not False or
            cfg["first_experiment_executed"] is not False or
            cfg["source"]["raw_train"] != TRAIN_REL or
            cfg["model"]["decision_threshold"] != 0.5 or
            cfg["runtime"]["worker_concurrency"] != 1 or
            cfg["replication"]["fit_rows_per_replication"] != 60000 or
            cfg["feature_selector"]["subsample_rows_per_selector_seed"] != 35000 or
            cfg["replication"]["seeds"] != [1103, 2207, 3301, 4409, 5501] or
            args.seed not in cfg["replication"]["seeds"] or
            [a["id"] for a in cfg["arms"]] != list(ARM_IDS)):
        raise RuntimeError("P21 protocol altered: abort before fitting")
    sha = cfg["source"]["sha256"]
    if sha256_stream(TRAIN) != sha:
        raise RuntimeError("Official TRAIN SHA mismatch")
    cpus = psutil.Process().cpu_affinity()
    if len(cpus) != 1:
        raise RuntimeError("Worker must be pinned to one logical CPU")

    frame = pd.read_csv(TRAIN, low_memory=False)
    features = [c for c in frame.columns if c not in cfg["source"]["excluded_predictors"]]
    if (len(frame) != cfg["source"]["expected_rows"] or len(features) != 42 or
            set(frame["label"].unique()) != {0, 1} or
            frame.loc[:, features].isna().any().any()):
        raise RuntimeError("Unexpected official TRAIN schema")
    fit_pool_idx, val_idx, split = fingerprint_and_split(frame, features, cfg["split"]["seed"])
    fit_idx, _ = train_test_split(
        fit_pool_idx, train_size=60000,
        stratify=frame.iloc[fit_pool_idx]["label"],
        random_state=args.seed,
    )
    if (len(fit_idx) != 60000 or
            set(fit_idx.tolist()) & set(val_idx.tolist())):
        raise RuntimeError("FIT / validation overlap")
    fit_digest = fit_ids_digest(fit_idx)
    fit_frame = frame.iloc[fit_idx]
    X_val = frame.iloc[val_idx].loc[:, features]
    y_val = frame.iloc[val_idx]["label"].to_numpy(dtype=int)
    y_fit = fit_frame["label"].to_numpy(dtype=int)

    # RQ2: the selector is fit anew within THIS replicated 60k fit subset.
    sel_start = time.monotonic()
    with threadpool_limits(limits=1):
        selection = fit_only_stable17(
            fit_frame, features, allowed_fit_indices=fit_idx,
            forbidden_validation_indices=val_idx, pilot_sample_rows=35000,
        )
    selector_seconds = round(time.monotonic() - sel_start, 3)
    chosen17 = selection["feature_names"]
    if len(chosen17) != 17 or len(set(chosen17)) != 17 or not selection["no_validation_rows_used"]:
        raise RuntimeError("Fit-only selection invariant broken")
    # Amendment: strictly group-disjoint OOF inner CV on full 42-source predictor vectors.
    inner_folds = inner_group_folds(fit_frame.loc[:, features], y_fit, seed=137)
    arms = []
    for arm in ARM_IDS:
        if arm == "A1_RF17_NONE":
            train_ids = fit_idx
            columns = chosen17
            weighting = None
        elif arm == "A2_RF42_BALANCED":
            train_ids, weighting = prepare_arm(
                fit_idx, y_fit, arm="BALANCED", seed=args.seed,
                forbidden_validation_indices=val_idx, max_rows=120000)
            columns = features
        elif arm == "A3_RF42_OVERSAMPLE":
            train_ids, weighting = prepare_arm(
                fit_idx, y_fit, arm="FIT_ONLY_RANDOM_OVERSAMPLE", seed=args.seed,
                forbidden_validation_indices=val_idx, max_rows=120000)
            columns = features
        else:
            train_ids, weighting = prepare_arm(
                fit_idx, y_fit, arm="NONE", seed=args.seed,
                forbidden_validation_indices=val_idx, max_rows=120000)
            columns = features
        if not set(int(x) for x in train_ids).issubset(set(int(x) for x in fit_idx)):
            raise RuntimeError("Arm sample includes non-FIT indices")
        if arm == "A4_STACK42_NONE":
            model = make_stacking(features, cfg, args.seed, inner_folds)
        else:
            model = make_rf(columns, cfg, args.seed, weighting=weighting)
        start = time.monotonic()
        with threadpool_limits(limits=1):
            model.fit(frame.iloc[train_ids].loc[:, columns],
                      frame.iloc[train_ids]["label"].to_numpy(dtype=int))
        train_seconds = round(time.monotonic() - start, 3)
        if list(model.classes_) != [0, 1]:
            raise RuntimeError("Wrong estimator binary class order")
        start = time.monotonic()
        with threadpool_limits(limits=1):
            proba = model.predict_proba(X_val.loc[:, columns])[:, 1]
        predict_seconds = round(time.monotonic() - start, 3)
        metrics = binary_metrics(y_val, proba)
        arms.append({
            "arm": arm,
            "fit_row_ids_sha256": fit_digest,
            "fit_source_rows": 60000,
            "actual_model_fit_rows": len(train_ids),
            "original_feature_count": len(columns),
            "class_weight": weighting,
            "fit_seconds": train_seconds,
            "predict_seconds": predict_seconds,
            "metrics": metrics,
        })
        del model, proba
        (out.parent / "progress.json").write_text(
            json.dumps({
                "scope": "PROGRESS_NOT_SCIENTIFIC_RESULT",
                "seed": args.seed, "completed_arm_ids": [a["arm"] for a in arms],
                "official_test_opened": False,
            }, indent=2) + "\n", encoding="utf-8")
    if [a["arm"] for a in arms] != list(ARM_IDS):
        raise RuntimeError("Incomplete five-arm design")
    if any(a["fit_row_ids_sha256"] != fit_digest for a in arms):
        raise RuntimeError("Unmatched arm FIT identity")
    if sha256_stream(TRAIN) != sha:
        raise RuntimeError("TRAIN source changed during experiment")

    out_result = {
        "passed": True,
        "scope": "P21_TRAIN_REUSED_POST_HOC_SCIENCE_INTERNAL_VALIDATION_ONLY",
        "source_path": TRAIN_REL, "source_sha256": sha,
        "protocol_sha256": sha256_stream(config_path),
        "seed": args.seed, "train_rows": len(frame),
        "fit_pool_rows": len(fit_pool_idx), "fit_subset_rows": len(fit_idx),
        "fit_row_ids_sha256": fit_digest,
        "validation_rows": len(val_idx), "split": split,
        "selector": {
            "feature_names": chosen17,
            "feature_names_sha256": selection["feature_names_sha256"],
            "eligible_stable_count": selection["eligible_stable_count"],
            "forced_top17_count": selection["forced_top17_count"],
            "selector_fit_calls": selection["selector_fit_calls"],
            "sample_rows_per_selection_seed": 35000,
            "fit_seconds": selector_seconds,
            "validation_used": False,
        },
        "stack_inner_cv": {
            "type": "StratifiedGroupKFold",
            "n_splits": 3, "seed": 137,
            "exact_vector_group_disjoint": True,
            "amendment": "P21_PRE_FULL_SCIENCE_INNER_GROUP_SPLIT_2026-10-18",
        },
        "arm_ids": list(ARM_IDS), "arms": arms,
        "official_test_opened": False, "historical_p9_modified": False,
        "validation_used_for_tuning": False, "model_artifacts_saved": False,
        "versions": {name: importlib.metadata.version(name)
                     for name in ("numpy", "pandas", "scikit-learn", "scipy", "psutil")},
    }
    (out / "worker_result.json").write_text(
        json.dumps(out_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    done.set()
    print(json.dumps({
        "passed": True, "seed": args.seed,
        "arm_count": len(arms),
        "validation_rows": len(val_idx),
        "official_test_opened": False,
    }), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
