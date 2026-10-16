#!/usr/bin/env python3
"""Read-only NCKH P15-04 reproducibility-protocol audit (stdlib only).

Uses the source-code SHA256 snapshot from P15-01 and compares saved manifests.
This does NOT train models, read the raw CSV data, or prove absence of leakage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REFERENCE_SOURCES = {
    "src/features/select_unsw_features_stage1.py": "05a5914ade807c32049effa580e5fd862a5ec15a45ce00844c4e6f61505762d1",
    "src/features/select_unsw_features_stage2.py": "4c04d4a15e51e3d79487d089ee30bcccecbfcd7969eeaa8b0eedeb8cc249521e",
    "src/models/run_unsw_baseline_development.py": "463f0948d77d75ff18220d499c6a643263ce5d693e6b02af7b3d197a614f1ccf",
    "src/models/run_unsw_diversity_oof.py": "69b779fe95c78b204f8dc55d5dd1c208d5cb7492711273ef3feee066b596660d",
    "src/models/run_unsw_ensemble_phase7_2.py": "d2f22ea57172053c6b21dab4eda182bd2fcba23ce1182e725197ea43a826e1fb",
    "src/models/run_unsw_phase8_controlled_tuning.py": "76b11692154bff6004fac2153a80626779ef6468578aecfeb7f46102327f4bce",
    "src/models/run_unsw_phase9_final_holdout.py": "3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480",
}

METADATA_PATHS = {
    "stage2": "results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json",
    "phase8": "results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json",
    "freeze": "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json",
    "phase9": "results/final_evaluation/unsw_nb15/phase9_holdout/experiment_metadata.json",
}
EXPECTED_MODELS = {"random_forest_42", "stacking_42", "random_forest_17"}

# Line references are valid only when the file SHA-256 equals the audited source.
CODE_EVIDENCE = [
    {"topic": "CV seed", "path": "src/models/run_unsw_phase9_final_holdout.py", "lines": "72-73", "finding": "RANDOM_STATE=42; STACKING_INNER_RANDOM_STATE=137"},
    {"topic": "Feature inputs", "path": "src/models/run_unsw_phase9_final_holdout.py", "lines": "222-232", "finding": "Drops id, label, attack_cat from model features"},
    {"topic": "Preprocessing", "path": "src/models/run_unsw_phase9_final_holdout.py", "lines": "270-325,332-403", "finding": "Unknown categories ignored; preprocessing occurs inside sklearn Pipeline"},
    {"topic": "Stacking internal CV", "path": "src/models/run_unsw_phase9_final_holdout.py", "lines": "466-509", "finding": "StratifiedKFold inner CV; StackingClassifier predict_proba; passthrough=False"},
    {"topic": "Frozen official evaluation", "path": "src/models/run_unsw_phase9_final_holdout.py", "lines": "932-943,991-1073", "finding": "Loads official train/test, frozen manifest; fits frozen models only on train"},
    {"topic": "RF and meta tuning", "path": "src/models/run_unsw_phase8_controlled_tuning.py", "lines": "462-483,603-610,638-662", "finding": "Training-only GridSearchCV, base OOF predictions via cross_val_predict, meta-model tuning"},
    {"topic": "Ensemble validation", "path": "src/models/run_unsw_ensemble_phase7_2.py", "lines": "428-449,675-725,1113-1127", "finding": "Outer StratifiedKFold and nested internal StackingClassifier CV"},
    {"topic": "Feature selection timing", "path": "src/features/select_unsw_features_stage2.py", "lines": "793-804,901-913", "finding": "Stage2 features selected using full official TRAIN before development CV"},
    {"topic": "Feature selection seed", "path": "src/features/select_unsw_features_stage2.py", "lines": "53-62", "finding": "Stability seeds 11,23,42,71,101"},
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def evaluate(project_root: Path) -> dict:
    root = project_root.resolve()
    files = {}
    for rel, original_hash in REFERENCE_SOURCES.items():
        p = root / rel
        if not p.is_file():
            files[rel] = {"status": "MISSING", "expected_sha256": original_hash}
        else:
            digest = _sha256(p)
            files[rel] = {
                "status": "MATCH" if digest == original_hash else "CHANGED_REVIEW_NEEDED",
                "expected_sha256": original_hash,
                "observed_sha256": digest,
            }
    metadata = {}
    errors = []
    for key, rel in METADATA_PATHS.items():
        try:
            obj = _json(root / rel)
            if not isinstance(obj, dict):
                raise TypeError("JSON root must be an object")
            metadata[key] = {"status": "LOADED", "relative_path": rel, "sha256": _sha256(root / rel)}
            metadata[key]["obj"] = obj  # removed from serialized report below
        except (OSError, ValueError, TypeError) as exc:
            metadata[key] = {"status": "UNAVAILABLE", "relative_path": rel, "reason": str(exc)}
            errors.append(f"Cannot load {key}: {exc}")

    checks = {}
    def record(name: str, ok: bool, details: str):
        checks[name] = {"status": "PASS" if ok else "REVIEW", "detail": details}

    if all(metadata.get(k, {}).get("status") == "LOADED" for k in METADATA_PATHS):
        stage2, ph8, freeze, ph9 = [metadata[k]["obj"] for k in ("stage2", "phase8", "freeze", "phase9")]
        stable = stage2.get("stable_2plus_methods", None)
        record("feature_subset_17", isinstance(stable, list) and len(stable) == 17 and len(set(stable)) == 17,
               f"stable_2plus_methods count={len(stable) if isinstance(stable,list) else 'missing'}")
        record("phase8_official_test_not_loaded", ph8.get("official_test_loaded") is False,
               f"Phase 8 metadata official_test_loaded={ph8.get('official_test_loaded')!r}")
        record("phase9_official_test_evaluated", ph9.get("official_test_opened") is True,
               f"Phase 9 metadata official_test_opened={ph9.get('official_test_opened')!r}")
        record("official_split_sizes", ph9.get("train_rows") == 175341 and ph9.get("official_test_rows") == 82332,
               f"train={ph9.get('train_rows')}; test={ph9.get('official_test_rows')}")
        record("three_frozen_models", set(freeze) == EXPECTED_MODELS,
               f"models={sorted(freeze)}")
        record("manifest_unchanged_in_phase9", freeze == ph9.get("frozen_candidates"),
               "Phase 8 freeze_candidates JSON compared with Phase 9 experiment_metadata frozen_candidates")
        record("frozen_thresholds_0_5", set(freeze) == EXPECTED_MODELS and all(
            isinstance(cfg, dict) and cfg.get("decision_threshold") == 0.5 for cfg in freeze.values()),
            "All three final-model thresholds must equal 0.5")
        record("dataset_label", ph8.get("dataset") == "UNSW-NB15" and ph9.get("dataset") == "UNSW-NB15",
               "Both saved metadata records identify UNSW-NB15")
    else:
        record("metadata_set", False, "One or more required JSON input files are missing or invalid")

    code_ok = all(item["status"] == "MATCH" for item in files.values())
    record("source_matches_historical_audit", code_ok,
           "Seven critical script SHA-256 digests compared with audit snapshot; exact line evidence requires MATCH")
    flags = [
        "Historical original-training Python and package versions UNKNOWN; current reference venv is not proof of original environment.",
        "Feature selection is done on the entire official TRAIN before development CV; development scores can be optimistic (selection outside CV folds).",
        "Stratified shuffled CV is not a time/session-group split. Original official train/test may have feature-vector overlap; do not claim independent temporal validation.",
        "Static source checks plus metadata do NOT prove the original scripts executed exactly as currently stored, or that every data-leakage mode was excluded.",
        "Meta learner tuning reuses saved base OOF features from the full training set; do not call this a completely nested unbiased CV estimate.",
    ]
    status = "STATIC_PROTOCOL_EVIDENCE_MATCH_WITH_CAVEATS" if code_ok and all(x["status"] == "PASS" for x in checks.values()) else "REVIEW_NEEDED"
    # Exclude raw loaded JSON to keep output limited to provenance facts.
    metadata_public = {k: {a:b for a,b in v.items() if a != "obj"} for k,v in metadata.items()}
    return {
        "check_id": "P15-04",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "scope": "Read-only code hashes + saved protocol manifests; no CSV data read; no model fit/predict",
        "source_files": files,
        "metadata": metadata_public,
        "checks": checks,
        "code_evidence": CODE_EVIDENCE if code_ok else [],
        "known_limitations": flags,
        "status": status,
        "errors": errors,
        "note": "PASS of check items means static recorded protocol consistency; NOT independent end-to-end reproducibility or no-leakage certification."
    }


def markdown_report(report: dict) -> str:
    lines = ["# P15-04 — Split, Seeds & Leakage Safeguards (read-only)", "",
             f"Status: **{report['status']}**", "",
             "This is static source/metadata verification, not an executed training replay.", "",
             "## Checks", "", "| Check | Status | Evidence |", "|---|---|---|"]
    for k, val in report["checks"].items():
        lines.append(f"| `{k}` | {val['status']} | {val['detail'].replace('|','/')} |")
    lines.extend(["", "## Audited source evidence (only if all hashes match)", ""])
    for ev in report["code_evidence"]:
        lines.append(f"- `{ev['path']}:{ev['lines']}` — {ev['finding']}")
    lines.extend(["", "## Caveats / research limitations", ""])
    for flag in report["known_limitations"]:
        lines.append(f"- {flag}")
    lines.append("\nDo not use official TEST to adjust features, threshold or model configuration.\n")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--out-dir", default="results/reproducibility/p15_04_protocol")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    report = evaluate(root)
    out = Path(args.out_dir)
    if not out.is_absolute():
        out = root / out
    out.mkdir(parents=True, exist_ok=True)
    json_out = out / "p15_04_protocol_integrity.json"
    md_out = out / "P15_04_PROTOCOL_REPORT.md"
    if json_out.exists() or md_out.exists():
        raise SystemExit("REFUSE_OVERWRITE_EXISTING_AUDIT: choose a new --out-dir to preserve earlier evidence.")
    json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md_out.write_text(markdown_report(report), encoding="utf-8")
    for k, val in report["checks"].items():
        print(f"{k}: {val['status']}")
    print(report["status"])
    print("Report:", json_out)
    print("No model training/evaluation, dataset access, or input file modifications performed.")

if __name__ == "__main__":
    main()
