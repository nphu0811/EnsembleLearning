"""Read-only acceptance checks for a P21 RF42 *resource smoke*, NOT RQ1/2/5 science.

Uses only committed compact JSON: no raw TRAIN/TEST or ML libraries, no
model load, no predictions and no filesystem changes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "controlled_extensions"
TRAIN_HASH = "bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa"
GIB = 1024 ** 3
CAP = 2 * GIB
FLOOR = int(1.5 * GIB)


def valid_pilot_path(relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Absolute/parent-traversal pilot paths prohibited")
    parent = BASE.resolve(strict=True)
    target = (ROOT / path).resolve(strict=True)
    if (target.parent != parent or
            not target.name.startswith("p21_train_only_pilot_rf42_") or
            (ROOT / path).is_symlink()):
        raise ValueError("Pilot must be direct new P21 RF42 folder")
    return target


def same_bytes_hash_for_git_or_windows(path: Path, expected: str) -> bool:
    data = path.read_bytes()
    return (hashlib.sha256(data).hexdigest() == expected or
            hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest() == expected)


def checks_for_reports(start: dict, report: dict, worker: dict, contract: dict) -> list[dict]:
    checks: list[dict] = []

    def check(label: str, cond) -> None:
        checks.append({"check": label, "passed": bool(cond)})

    expected_hash = contract["source"]["sha256"]
    split = worker.get("split", {})
    cfg = worker.get("model_config", {})
    budget = report.get("budget", {})
    classes = worker.get("pilot_fit_class_counts", {})

    check("official TRAIN source exact", expected_hash == TRAIN_HASH and
          report.get("train_sha256") == expected_hash and
          worker.get("source_sha256") == expected_hash and
          worker.get("source_path") == contract["source"]["raw_train"])
    check("pilot only and not full RQ results",
          report.get("phase") == "P21" and
          report.get("scope") == "TRAIN_ONLY_RF42_SMOKE_PILOT" and
          worker.get("scope") == "P21_RF42_ANCHOR_PILOT_ONLY; no RQ result" and
          report.get("status") == "PASS_RESOURCE_SMOKE_ONLY" and
          worker.get("passed") is True and
          report.get("full_P21_training_authorized") is False and
          contract.get("training_authorized") is False)
    check("start/run provenance and state consistent",
          start.get("status") == "INCOMPLETE" and
          start.get("stop_reason") == "NOT_STARTED" and
          start.get("scope") == report.get("scope") and
          start.get("created_at_utc") == report.get("created_at_utc") and
          start.get("protocol_sha256") == report.get("protocol_sha256") and
          start.get("train_sha256") == report.get("train_sha256") and
          start.get("pilot_rows") == report.get("pilot_rows") and
          start.get("versions") == report.get("versions") and
          start.get("python_executable") == report.get("python_executable") and
          start.get("full_P21_training_authorized") is False)
    check("worker nested report equals separate result", report.get("worker_checks") == worker)
    check("completed without watchdog failure",
          report.get("exit_code") == 0 and report.get("stop_reason") is None and
          report.get("resource_samples", 0) > 0 and
          0 < report.get("wall_seconds", 0) <= report.get("timeout_minutes", 0) * 60)
    check("startup budget verified",
          budget.get("passed") is True and
          budget.get("system_available_bytes", 0) >= 4 * GIB and
          budget.get("disk_free_bytes", 0) >= 10 * GIB and
          budget.get("process_tree_rss_cap_bytes") == CAP and
          budget.get("system_available_floor_bytes") == FLOOR)
    check("observed watchdog headroom",
          0 < report.get("peak_tree_rss_bytes", 0) < CAP and
          report.get("minimum_system_available_bytes", 0) >= FLOOR)
    check("pilot row scope and class counts",
          1000 <= report.get("pilot_rows", -1) <= 20000 and
          report.get("pilot_rows") == worker.get("pilot_fit_rows") and
          worker.get("train_file_rows") == contract["source"]["expected_rows"] and
          set(classes) == {"0", "1"} and
          all(isinstance(x, int) and x > 0 for x in classes.values()) and
          sum(classes.values()) == worker.get("pilot_fit_rows"))
    check("fixed 42-feature RF configuration",
          worker.get("pilot_component") == "A0_RF42_NONE" and
          worker.get("feature_count") == 42 and
          cfg == {
              "n_estimators": 150,
              "min_samples_leaf": 2,
              "max_features": 0.5,
              "class_weight": None,
              "random_state": contract["replication"]["seeds"][0],
              "decision_threshold": 0.5,
          })
    normal_fraction = 56000 / 175341
    check("TRAIN-only group-disjoint single split",
          split.get("method") == "StratifiedGroupKFold" and
          split.get("seed") == contract["split"]["seed"] and
          split.get("validation_fold") == 0 and
          split.get("group_disjoint") is True and split.get("row_disjoint") is True and
          split.get("fit_rows", 0) + split.get("validation_rows", 0) == 175341 and
          0.18 <= split.get("validation_ratio", -1) <= 0.22 and
          abs(split.get("validation_normal_fraction", 100) - normal_fraction) <= 0.02 and
          split.get("validation_evaluation_performed") is False)
    check("NO official TEST, validation prediction or scientific metrics",
          report.get("official_test_opened") is False and
          worker.get("official_test_opened") is False and
          worker.get("validation_predicted") is False and
          worker.get("scientific_metrics_calculated") is False and
          report.get("scientific_metrics_calculated") is False and
          report.get("model_artifact_saved") is False and
          worker.get("model_artifact_saved") is False and
          worker.get("train_probe_samples") == 16)
    check("positive fit timing within wall clock",
          0 < worker.get("fit_and_train_probe_seconds", -1) < report.get("wall_seconds", 0))
    check("scikit-learn package provenance",
          worker.get("versions", {}).get("scikit-learn") ==
          report.get("versions", {}).get("scikit-learn") == "1.9.0")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-dir",
                        default="results/controlled_extensions/p21_train_only_pilot_rf42_01")
    args = parser.parse_args()
    pilot = valid_pilot_path(args.pilot_dir)
    start = json.loads((pilot / "start.json").read_text(encoding="utf-8"))
    report = json.loads((pilot / "run_report.json").read_text(encoding="utf-8"))
    worker = json.loads((pilot / "worker" / "worker_result.json").read_text(encoding="utf-8"))
    contract_path = ROOT / "config" / "p21_train_only_protocol_2026_10_18.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    checks = checks_for_reports(start, report, worker, contract)
    checks.append({"check": "frozen protocol digest from author host",
                   "passed": same_bytes_hash_for_git_or_windows(
                       contract_path, report.get("protocol_sha256", ""))})
    stats = {
        "audit": "P21_RF42_PILOT_REPORTED_EVIDENCE_ONLY",
        "checks_passed": sum(c["passed"] for c in checks),
        "checks_failed": sum(not c["passed"] for c in checks),
        "failed_checks": [c["check"] for c in checks if not c["passed"]],
        "limit": "No independent review of author-host process telemetry/raw TRAIN; no RQ model comparison.",
    }
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0 if stats["checks_failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
