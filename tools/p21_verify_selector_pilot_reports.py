"""Read-only acceptance for author's P21 selector17 resource pilot report.

This verifies consistency of the three committed JSON files against the
frozen P21 protocol; it does not independently replay author-host execution,
load raw TRAIN/TEST, calculate RQ metrics or fit any model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "controlled_extensions"
CONTRACT_FILE = ROOT / "config" / "p21_train_only_protocol_2026_10_18.json"
TRAIN_HASH = "bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa"
GIB = 1024 ** 3


def safe_pilot_dir(arg: str) -> Path:
    raw = Path(arg)
    if raw.is_absolute() or ".." in raw.parts:
        raise ValueError("Only relative P21 selector pilot paths are allowed")
    path = (ROOT / raw).resolve(strict=True)
    base = BASE.resolve(strict=True)
    if (path.parent != base or
            not path.name.startswith("p21_train_only_pilot_selector17_") or
            (ROOT / raw).is_symlink()):
        raise ValueError("Expected a direct P21 selector17 pilot output directory")
    return path


def protocol_sha_matches(path: Path, expected: str) -> bool:
    """Accept untouched author Windows CRLF or Git LF bytes for this contract."""
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    windows_data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    return expected in (digest, hashlib.sha256(windows_data).hexdigest())


def verify_reports(start: dict, run: dict, worker: dict, contract: dict) -> list[dict]:
    checks = []

    def add(name: str, passed) -> None:
        checks.append({"check": name, "passed": bool(passed)})

    budget = run.get("budget", {})
    selection = worker.get("selection", {})
    split = worker.get("split", {})
    classes = worker.get("pilot_fit_class_counts", {})
    source = contract.get("source", {})
    protocol_selector = contract.get("feature_selector", {})
    pilot_rows = run.get("pilot_rows", 0)
    expected_selector_rows = max(
        100, int(round(pilot_rows * 35000 / 60000))
    ) if isinstance(pilot_rows, int) else -1

    add("exact official TRAIN identity",
        run.get("train_sha256") == TRAIN_HASH
        and worker.get("source_sha256") == TRAIN_HASH
        and source.get("sha256") == TRAIN_HASH
        and worker.get("source_path") == source.get("raw_train"))

    add("resource-only success not a scientific outcome",
        run.get("phase") == "P21"
        and run.get("status") == "PASS_SELECTOR_RESOURCE_SMOKE_ONLY"
        and run.get("scope") == "TRAIN_ONLY_SELECTOR17_SMOKE_PILOT"
        and worker.get("scope") ==
        "P21_SELECTOR17_FIT_ONLY_RESOURCE_PILOT; no scientific RQ feature selection"
        and worker.get("passed") is True
        and worker.get("pilot_component") == "TRAIN_SUBSET_STABLE_TOP17_RESOURCE_PROBE"
        and contract.get("training_authorized") is False
        and run.get("full_P21_training_authorized") is False)

    add("start JSON is immutable pre-run snapshot",
        start.get("status") == "INCOMPLETE"
        and start.get("stop_reason") == "NOT_STARTED"
        and start.get("exit_code") is None
        and start.get("scope") == run.get("scope")
        and start.get("created_at_utc") == run.get("created_at_utc")
        and start.get("protocol_sha256") == run.get("protocol_sha256")
        and start.get("train_sha256") == run.get("train_sha256")
        and start.get("pilot_rows") == run.get("pilot_rows")
        and start.get("timeout_minutes") == run.get("timeout_minutes")
        and start.get("versions") == run.get("versions")
        and start.get("budget") == run.get("budget"))

    add("separate worker JSON matches nested worker evidence",
        run.get("worker_checks") == worker)

    add("wall time and successful watchdog termination",
        run.get("exit_code") == 0
        and run.get("stop_reason") is None
        and isinstance(run.get("resource_samples"), int)
        and run.get("resource_samples") > 0
        and 0 < run.get("wall_seconds", 0) <
        run.get("timeout_minutes", 0) * 60
        and run.get("timeout_minutes") == 20)

    add("startup RAM and disk gate",
        budget.get("passed") is True
        and budget.get("system_available_bytes", 0) >= 4 * GIB
        and budget.get("disk_free_bytes", 0) >= 10 * GIB
        and budget.get("process_tree_rss_cap_bytes") == 2 * GIB
        and budget.get("system_available_floor_bytes") == int(1.5 * GIB))

    add("observed RSS/free system RAM safe",
        0 < run.get("peak_tree_rss_bytes", 0) < 2 * GIB
        and run.get("minimum_system_available_bytes", 0) >= int(1.5 * GIB))

    add("fit-only sampling scope and class supports",
        isinstance(pilot_rows, int)
        and 1000 <= pilot_rows <= 20000
        and worker.get("pilot_fit_rows") == pilot_rows
        and worker.get("train_file_rows") == 175341
        and set(classes) == {"0", "1"}
        and all(isinstance(v, int) and v > 0 for v in classes.values())
        and sum(classes.values()) == pilot_rows)

    add("exact-vector split consistent with original TRAIN",
        split.get("method") == "StratifiedGroupKFold"
        and split.get("seed") == contract.get("split", {}).get("seed") == 20261018
        and split.get("validation_fold") == 0
        and split.get("fit_rows", 0) + split.get("validation_rows", 0) == 175341
        and 0.18 <= split.get("validation_ratio", 0) <= 0.22
        and abs(split.get("validation_normal_fraction", 5) - 56000 / 175341) <= 0.02
        and split.get("group_disjoint") is True
        and split.get("row_disjoint") is True
        and split.get("validation_evaluation_performed") is False)

    add("exact 5 x 3 selection methods and FIT-only selector sample size",
        selection.get("selection_seeds") == [11, 23, 42, 71, 101]
        and selection.get("methods") == ["filter", "l1", "extra_trees"]
        and selection.get("selector_fit_calls") == 15
        and selection.get("selection_sample_rows_per_seed") == expected_selector_rows
        and protocol_selector.get("selection_seeds") == selection.get("selection_seeds"))

    add("exact stable feature count and provenance",
        selection.get("original_feature_count") == 42
        and selection.get("selected_feature_count") == 17
        and isinstance(selection.get("eligible_stable_count"), int)
        and 0 <= selection.get("eligible_stable_count", -1) <= 42
        and selection.get("forced_top17_count") ==
            max(0, 17 - selection.get("eligible_stable_count", -1))
        and isinstance(selection.get("pilot_selection_digest_sha256"), str)
        and len(selection.get("pilot_selection_digest_sha256", "")) == 64
        and all(c in "0123456789abcdef"
                for c in selection.get("pilot_selection_digest_sha256", "")))

    add("strict fit-only/validation/test/pilot outputs",
        selection.get("no_validation_rows_used") is True
        and selection.get("validated_fit_index_exclusivity") is True
        and selection.get("pilot_subset_not_for_scientific_comparison") is True
        and selection.get("pilot_feature_names_saved") is False
        and worker.get("validation_predicted") is False
        and run.get("official_test_opened") is False
        and worker.get("official_test_opened") is False
        and run.get("scientific_metrics_calculated") is False
        and worker.get("scientific_metrics_calculated") is False
        and run.get("model_artifact_saved") is False
        and worker.get("model_artifact_saved") is False)

    add("measured selector time is within the wall clock",
        0 < worker.get("fit_selector_seconds", 0) < run.get("wall_seconds", 0))

    add("matching package versions",
        worker.get("versions", {}).get("scikit-learn") ==
        run.get("versions", {}).get("scikit-learn") == "1.9.0"
        and worker.get("versions", {}).get("pandas") ==
        run.get("versions", {}).get("pandas") == "3.0.5")

    return checks


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--pilot-dir",
        default="results/controlled_extensions/p21_train_only_pilot_selector17_01",
    )
    args = p.parse_args()
    root = safe_pilot_dir(args.pilot_dir)
    start = json.loads((root / "start.json").read_text(encoding="utf-8"))
    run = json.loads((root / "run_report.json").read_text(encoding="utf-8"))
    worker = json.loads((root / "worker/worker_result.json").read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
    checks = verify_reports(start, run, worker, contract)
    checks.append({
        "check": "frozen P21 protocol SHA256",
        "passed": protocol_sha_matches(CONTRACT_FILE, run.get("protocol_sha256", "")),
    })
    result = {
        "audit": "P21_AUTHOR_REPORTED_SELECTOR_RESOURCE_PILOT_ONLY",
        "passed": sum(x["passed"] for x in checks),
        "failed": sum(not x["passed"] for x in checks),
        "failed_checks": [x["check"] for x in checks if not x["passed"]],
        "limitation": "Recorded JSON consistency; not independent observation of user-host execution or RQ2 metric evaluation",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
