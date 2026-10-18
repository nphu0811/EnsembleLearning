"""Read-only P21 five-seed scientific evidence audit (stdlib only).

Validates actual compact seed run reports, metrics, matched arm source IDs and
the precomputed descriptive aggregate before allowing PDF V3 compilation.
Does not load TRAIN, official TEST, models, predictions or external networks.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics

from p21_science_acceptance import (
    ARM_IDS, SEEDS, acceptable_science_worker
)
from p21_science_aggregate import PAIRS, MEASURES

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "controlled_extensions"
SOURCE_SHA = "bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa"
PROTOCOL_FILE = ROOT / "config" / "p21_train_only_protocol_2026_10_18.json"
SUMMARY = BASE / "p21_train_only_science_summary_20261019_022655" / "aggregate.json"


def near(a, b) -> bool:
    try:
        return (
            isinstance(a, (float, int)) and not isinstance(a, bool)
            and isinstance(b, (float, int)) and not isinstance(b, bool)
            and math.isfinite(a) and math.isfinite(b)
            and math.isclose(a, b, abs_tol=1e-10, rel_tol=0)
        )
    except (ValueError, OverflowError, TypeError):
        return False


def check_summary(aggregate: dict, rows: dict[int, dict]) -> list[str]:
    failures = []
    if aggregate.get("completed_seed_count") != 5 or aggregate.get("seeds") != list(SEEDS):
        failures.append("aggregate seed identity")
    if (aggregate.get("source_sha256") != SOURCE_SHA or
            aggregate.get("official_test_read") is not False or
            aggregate.get("seeds_are_independent_external_tests") is not False or
            aggregate.get("novel_external_validation_performed") is not False or
            aggregate.get("grouped_stack_inner_cv_pre_full_amendment") is not True):
        failures.append("aggregate scope/source")
    per_seed = aggregate.get("per_seed", {})
    for seed, w in rows.items():
        x = per_seed.get(str(seed), {})
        if x.get("fit_ids_sha256") != w["fit_row_ids_sha256"]:
            failures.append(f"aggregate FIT identity seed {seed}")
        if x.get("selected_features_sha256") != w["selector"]["feature_names_sha256"]:
            failures.append(f"aggregate selector seed {seed}")
        for arm in w["arms"]:
            published = x.get("metrics_by_arm", {}).get(arm["arm"], {})
            for key in ["macro_f1", "mcc", "attack_precision", "attack_recall", "fpr", "fnr"]:
                if not near(published.get(key), arm["metrics"][key]):
                    failures.append(f"aggregate {seed}/{arm['arm']}/{key}")
            for key in ["tn", "fp", "fn", "tp"]:
                if published.get(key) != arm["metrics"][key]:
                    failures.append(f"aggregate {seed}/{arm['arm']}/{key}")
    means = aggregate.get("arm_summary", {})
    contrasts = aggregate.get("contrasts", {})
    for arm in ARM_IDS:
        if arm not in means:
            failures.append(f"missing aggregate arm {arm}")
            continue
        for metric in (*MEASURES, "fit_seconds"):
            values = [
                next(a for a in rows[seed]["arms"] if a["arm"] == arm)
                for seed in SEEDS
            ]
            original = [
                v["fit_seconds"] if metric == "fit_seconds" else v["metrics"][metric]
                for v in values
            ]
            got = means[arm].get(metric, {})
            if (not near(got.get("mean"), statistics.mean(original))
                    or not near(got.get("sample_std"), statistics.stdev(original))
                    or not all(near(x, y) for x, y in zip(
                        got.get("values_by_seed", []), original, strict=False))
                    or len(got.get("values_by_seed", [])) != 5):
                failures.append(f"summary mean/std {arm}/{metric}")
    for key, (a, b) in PAIRS.items():
        if key not in contrasts:
            failures.append(f"missing paired contrast {key}")
            continue
        for metric in MEASURES:
            differences = []
            for seed in SEEDS:
                by_id = {x["arm"]: x for x in rows[seed]["arms"]}
                differences.append(
                    by_id[a]["metrics"][metric] - by_id[b]["metrics"][metric])
            got = contrasts[key].get(metric, {})
            if (not near(got.get("mean"), statistics.mean(differences))
                    or not near(got.get("sample_std"), statistics.stdev(differences))
                    or not all(near(x, y) for x, y in zip(
                        got.get("values_by_seed", []), differences, strict=False))
                    or len(got.get("values_by_seed", [])) != 5):
                failures.append(f"paired mean/std {key}/{metric}")
    return failures


def audit(path: Path) -> dict:
    failures = []
    cfg = json.loads(PROTOCOL_FILE.read_text(encoding="utf-8"))
    if (cfg["source"]["sha256"] != SOURCE_SHA or
            cfg["replication"]["seeds"] != list(SEEDS)):
        failures.append("frozen protocol source/seeds")
    rows = {}
    for seed in SEEDS:
        base = BASE / f"p21_train_only_science_seed_{seed}_01"
        report_path = base / "run_report.json"
        worker_path = base / "worker" / "worker_result.json"
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            worker = json.loads(worker_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            failures.append(f"missing/unreadable seed {seed} {type(exc).__name__}")
            continue
        if (report.get("status") != "PASS_INTERNAL_TRAIN_VALIDATION_SEED_ONLY"
                or report.get("seed") != seed or report.get("exit_code") != 0
                or report.get("stop_reason") is not None or
                report.get("official_test_opened") is not False or
                report.get("results_are_independent_external_test") is not False):
            failures.append(f"failed or invalid supervisor seed {seed}")
        budget = report.get("resource_policy", {})
        if (budget.get("full_training_has_wall_timeout") is not False
                or not 0 < report.get("peak_tree_rss_bytes", 0) < budget.get(
                    "peak_tree_rss_cap_bytes", 0)):
            failures.append(f"resource gate seed {seed}")
        # Protocol hash comes from worker and supervisor; physical TRAIN SHA also
        # verified at runtime. We do not re-open raw TRAIN here.
        if (report.get("source_sha256") != SOURCE_SHA or
                worker.get("source_sha256") != SOURCE_SHA or
                report.get("protocol_sha256") != worker.get("protocol_sha256")):
            failures.append(f"source identity seed {seed}")
        if not acceptable_science_worker(
            worker, seed, SOURCE_SHA, report.get("protocol_sha256")):
            failures.append(f"confusion matrix / arm fit checks seed {seed}")
        # To avoid circular logic, build baseline support from actual per-arm
        # confusion matrices and verify the same class support across all arms.
        if isinstance(worker.get("arms"), list) and len(worker["arms"]) == 5:
            supports = {
                (a["metrics"]["tn"] + a["metrics"]["fp"],
                 a["metrics"]["tp"] + a["metrics"]["fn"])
                for a in worker["arms"]
            }
            if supports != {(11200, 23869)}:
                failures.append(f"true label support differs seed {seed}")
        rows[seed] = worker
    if set(rows) == set(SEEDS):
        aggregate = json.loads(path.read_text(encoding="utf-8"))
        failures += check_summary(aggregate, rows)
    else:
        failures.append("incomplete five-seed input")
    return {
        "status": "PASS_FIVE_SEED_READ_ONLY_AUDIT" if not failures else "FAIL",
        "completed_seeds_verified": len(rows),
        "arms_claimed": len(rows) * 5,
        "official_test_opened_by_this_audit": False,
        "metrics_recomputed_from_existing_counts": True,
        "independent_external_validation": False,
        "failures": failures,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--summary", type=Path, default=SUMMARY)
    a = p.parse_args()
    if a.summary != SUMMARY:
        p.error("Only the canonical first completed five-seed aggregate is accepted")
    result = audit(a.summary)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not result["failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
