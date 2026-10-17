"""P21 selector17 pilot worker: 15 train-fit-only selector passes, NO scientific evaluation.

Only launched by the P21 selector resource supervisor after explicit author opt-in.
Never loads the official TEST, never calls historical Stage2 main(), never
uses the global historical stable17, never predicts on validation or writes a
serialized model. Output is aggregate safety/resource evidence only.
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

from p21_pilot_guards import (
    ROOT, TRAIN, TRAIN_REL, audit_file_open, sha256_stream,
    validate_selector_worker_scope,
)
from p21_pilot_worker import fingerprint_and_split, heartbeat_watch


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--pilot-rows", type=int, required=True)
    args = parser.parse_args()

    if os.environ.get("P21_SELECTOR_WATCHED") != "1":
        raise SystemExit("Selector pilot must run under its own watched supervisor")
    if not (1000 <= args.pilot_rows <= 20000):
        raise SystemExit("Selector pilot FIT sample must be 1000..20000")
    out = args.out_dir.resolve(strict=True)
    validate_selector_worker_scope(out)
    gate = out.parent / "go.signal"
    for _ in range(200):
        if gate.is_file() and gate.read_text(encoding="utf-8").strip() == "P21_SELECTOR_PILOT_ONLY":
            break
        time.sleep(0.1)
    else:
        raise SystemExit("No dedicated selector supervisor approval")
    heartbeat = out.parent / "heartbeat"
    if not heartbeat.is_file():
        raise SystemExit("Missing selector supervisor heartbeat")
    done = threading.Event()
    threading.Thread(target=heartbeat_watch, args=(heartbeat, done), daemon=True).start()
    sys.dont_write_bytecode = True
    sys.addaudithook(audit_file_open)

    import numpy as np
    import pandas as pd
    import psutil
    from sklearn.model_selection import train_test_split
    from threadpoolctl import threadpool_limits
    from p21_selector_core import fit_only_stable17, SELECTION_SEEDS, METHODS

    config_path = ROOT / "config/p21_train_only_protocol_2026_10_18.json"
    contract = json.loads(config_path.read_text(encoding="utf-8"))
    selector_cfg = contract["feature_selector"]
    if (
        contract["training_authorized"] is not False
        or contract["first_experiment_executed"] is not False
        or contract["source"]["raw_train"] != TRAIN_REL
        or contract["runtime"]["pilot_required"] is not True
        or selector_cfg["output_k"] != 17
        or selector_cfg["top_k_per_method"] != 20
        or selector_cfg["selection_seeds"] != list(SELECTION_SEEDS)
        or selector_cfg["selectors"] != [
            "mutual_information_filter_redundancy", "l1_logistic", "extra_trees"
        ]
    ):
        raise RuntimeError("Selector pilot contract changed; refuse pilot")
    expected_sha = contract["source"]["sha256"]
    if sha256_stream(TRAIN) != expected_sha:
        raise RuntimeError("official TRAIN checksum mismatch")
    if len(psutil.Process().cpu_affinity()) != 1:
        raise RuntimeError("Selector pilot requires one CPU affinity set by supervisor")

    # Split on all original 42 predictors FIRST; none of the held-out labels
    # or feature vectors are passed to a selector or score function.
    frame = pd.read_csv(TRAIN, low_memory=False)
    features = [c for c in frame.columns if c not in contract["source"]["excluded_predictors"]]
    if len(frame) != 175341 or len(features) != 42 or set(frame["label"].unique()) != {0, 1}:
        raise ValueError("Unexpected official TRAIN schema")
    if frame[features].isna().any().any():
        raise ValueError("Missing predictors; stop rather than alter cleaning policy")
    fit_pool_indices, validation_indices, split_meta = fingerprint_and_split(
        frame, features, contract["split"]["seed"])

    # FIT pool only. Preserve original row indices to assert no overlap.
    fit_rows, _ = train_test_split(
        fit_pool_indices,
        train_size=args.pilot_rows,
        stratify=frame.iloc[fit_pool_indices]["label"],
        random_state=contract["replication"]["seeds"][0],
    )
    pilot = frame.iloc[fit_rows]
    # Pilot scaled to 35k selector rows /60k scientific FIT rows. This
    # resource approximation is never used as the final stable17 result.
    per_selection = max(100, int(round(args.pilot_rows *
                                       selector_cfg["subsample_rows_per_selector_seed"] /
                                       contract["replication"]["fit_rows_per_replication"])))
    if per_selection >= len(pilot):
        raise RuntimeError("Selector pilot sample must be smaller than pilot FIT subset")
    start = time.monotonic()
    with threadpool_limits(limits=1):
        selection = fit_only_stable17(
            pilot, features,
            allowed_fit_indices=fit_rows,
            forbidden_validation_indices=validation_indices,
            pilot_sample_rows=per_selection,
            seeds=SELECTION_SEEDS,
        )
    fit_seconds = round(time.monotonic() - start, 3)
    if (selection["feature_count"] != 17
            or selection["selector_fit_calls"] != 15
            or not selection["no_validation_rows_used"]
            or selection["selection_seeds"] != list(SELECTION_SEEDS)
            or selection["selection_methods"] != list(METHODS)):
        raise RuntimeError("Selector pilot selection invariants violated")
    if sha256_stream(TRAIN) != expected_sha:
        raise RuntimeError("TRAIN changed while selector pilot was running")

    # Deliberately do NOT serialize the selected pilot feature names or model,
    # because the pilot subset is not the 60k RQ2 feature-selection result.
    result = {
        "passed": True,
        "scope": "P21_SELECTOR17_FIT_ONLY_RESOURCE_PILOT; no scientific RQ feature selection",
        "source_path": TRAIN_REL,
        "source_sha256": expected_sha,
        "train_file_rows": len(frame),
        "pilot_fit_rows": len(pilot),
        "pilot_fit_class_counts": {
            str(int(k)): int(v) for k, v in zip(*np.unique(pilot["label"], return_counts=True))
        },
        "split": split_meta,
        "pilot_component": "TRAIN_SUBSET_STABLE_TOP17_RESOURCE_PROBE",
        "selection": {
            "original_feature_count": len(features),
            "selected_feature_count": selection["feature_count"],
            "pilot_selection_digest_sha256": selection["feature_names_sha256"],
            "eligible_stable_count": selection["eligible_stable_count"],
            "forced_top17_count": selection["forced_top17_count"],
            "selection_sample_rows_per_seed": per_selection,
            "selector_fit_calls": selection["selector_fit_calls"],
            "selection_seeds": list(SELECTION_SEEDS),
            "methods": list(METHODS),
            "no_validation_rows_used": True,
            "validated_fit_index_exclusivity": True,
            "pilot_subset_not_for_scientific_comparison": True,
            "pilot_feature_names_saved": False,
        },
        "fit_selector_seconds": fit_seconds,
        "official_test_opened": False,
        "validation_predicted": False,
        "scientific_metrics_calculated": False,
        "model_artifact_saved": False,
        "versions": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "pandas", "scikit-learn", "scipy", "psutil")
        },
    }
    (out / "worker_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    done.set()
    print(json.dumps({
        "passed": True, "pilot_rows": len(pilot),
        "selection_sample_rows": per_selection,
        "fit_selector_seconds": fit_seconds,
        "validation_scored": False,
    }), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
