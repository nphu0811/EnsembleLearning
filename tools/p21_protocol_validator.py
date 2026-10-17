"""P21 static, TRAIN-safe pre-execution protocol audit.

This command NEVER imports sklearn/pandas, reads a raw dataset, fits models,
runs inference, invokes Phase 9, or computes scientific scores.

Optional --verify-local-train-sha reads the TRAIN CSV as opaque BYTES only.
It never reads any official TEST path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config/p21_train_only_protocol_2026_10_18.json"
TRAIN_SHA256 = "bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa"
EXPECTED_FROZEN = {
    "src/models/run_unsw_phase9_final_holdout.py": "3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480",
    "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json": "cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6",
    "results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json": "5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be",
}
EXPECTED_GIT_LF = {
    "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json":
        "7e9b99b39c455379871af93e447c80e375232ad66d9aae4075c105059dd1f6e7",
    "results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json":
        "1066e0791b13f681f72426636ca0713bb6c3316aacebf09d2f9b3b34121125e1",
}
EXPECTED_ARMS = {
    "A0_RF42_NONE", "A1_RF17_NONE", "A2_RF42_BALANCED",
    "A3_RF42_OVERSAMPLE", "A4_STACK42_NONE",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_contract(config: dict) -> list[dict]:
    checks = []

    def ok(name: str, condition) -> None:
        checks.append({"id": name, "pass": bool(condition)})

    src = config["source"]
    split = config["split"]
    rep = config["replication"]
    sel = config["feature_selector"]
    m = config["model"]
    runtime = config["runtime"]
    gov = config["governance"]
    arms = {arm["id"]: arm for arm in config["arms"]}

    ok("design-only and not authorized",
       config["status"].startswith("DESIGN_ONLY") and
       config["training_authorized"] is False and
       config["first_experiment_executed"] is False)
    ok("post-hoc / prior TRAIN context disclosed",
       config["new_experiment_is_post_hoc_relative_to_historical_test"] is True and
       "TRAIN_REUSED_POST_HOC" in config["scope"])
    ok("only official TRAIN path",
       src["raw_train"] == "data/raw/unsw-nb15/UNSW_NB15_training-set.csv" and
       src["sha256"] == TRAIN_SHA256 and src["expected_rows"] == 175341)
    ok("exclude identity and target from predictors",
       src["expected_original_features"] == 42 and
       src["label"] == "label" and src["positive_label"] == 1 and
       set(src["excluded_predictors"]) == {"id", "attack_cat", "label"})
    ok("all historical file identity checks declared",
       src["historical_read_only_hashes"] == EXPECTED_FROZEN)
    ok("repository LF to author Windows CRLF provenance declared",
       src["tracked_git_lf_sha256"] == EXPECTED_GIT_LF and
       src["historical_json_worktree_line_endings"] ==
       "CRLF_on_author_Windows; LF_in_Git_index; conversion_verified_without_content_changes")

    ok("group-disjoint 5-fold validation",
       split["group_by"] == "exact_original_42_predictor_vector_only" and
       split["cv"] == "StratifiedGroupKFold" and
       split["n_splits"] == 5 and split["fold_for_validation"] == 0 and
       split["shuffle"] is True and split["seed"] == 20261018 and
       split["require_no_row_or_group_overlap"] is True)
    ok("no automatic split fallback",
       split["allow_auto_fallback"] is False and
       split["valid_fraction_bounds"] == [0.18, 0.22] and
       split["class_proportion_max_deviation_percentage_points"] == 2)
    ok("5 fixed paired fit subsets",
       rep["seeds"] == [1103, 2207, 3301, 4409, 5501] and
       rep["fit_rows_per_replication"] == 60000 and
       rep["sample_method"] == "stratified_without_replacement_from_fit_pool" and
       rep["same_fit_rows_across_all_arms_within_seed"] is True and
       rep["shared_validation_across_seeds"] is True and
       rep["completed_seeds_required_for_full_results"] == 5)

    ok("selector training-only fresh for each replicate",
       sel["never_reuse_historical_full_train_stable17_for_primary"] is True and
       sel["refit_within_each_replication_fit_only"] is True and
       sel["reuse_only_within_same_seed"] is True and
       sel["primary_track"] == "train_subset_stable_top17")
    ok("selector five-seed, ranking & exact 17 size",
       sel["selection_seeds"] == [11, 23, 42, 71, 101] and
       sel["subsample_rows_per_selector_seed"] == 35000 and
       sel["top_k_per_method"] == 20 and
       sel["stable_frequency_min"] == 0.6 and
       sel["method_vote_threshold_for_stable"] == 2 and
       sel["output_k"] == 17 and
       sel["ranking_tie_breaker"] == [
           "stable_method_votes_desc", "mean_selection_frequency_desc",
           "feature_name_asc"])
    ok("selector components match historical 3 methods",
       set(sel["selectors"]) == {
           "mutual_information_filter_redundancy", "l1_logistic", "extra_trees"
       })

    ok("matched common RF + threshold",
       m["decision_threshold"] == 0.5 and
       m["common_rf"] == {
           "n_estimators": 150, "min_samples_leaf": 2,
           "max_features": 0.5, "bootstrap": True, "n_jobs": 1
       })
    ok("inner stacking / lower-cost meta config predeclared",
       m["stacking_lite"]["base_rf_matches_common_rf"] is True and
       m["stacking_lite"]["inner_cv"] == 3 and
       m["stacking_lite"]["inner_cv_seed"] == 137 and
       m["stacking_lite"]["n_jobs"] == 1 and
       m["stacking_lite"]["meta_lr"] == {
           "C": 0.5, "solver": "liblinear", "class_weight": None
       })
    ok("all and only 5 balanced matched arm IDs",
       set(arms) == EXPECTED_ARMS and len(config["arms"]) == 5)
    ok("RQ1 RF baseline reused and same full 42 feature track",
       arms["A0_RF42_NONE"]["role"] == ["RQ1", "RQ2", "RQ5"] and
       arms["A0_RF42_NONE"]["learner"] == "rf" and
       arms["A0_RF42_NONE"]["track"] == "all42" and
       arms["A4_STACK42_NONE"]["learner"] == "stacking_lite" and
       arms["A4_STACK42_NONE"]["track"] == "all42")
    ok("RQ2 only feature track differs",
       arms["A1_RF17_NONE"]["track"] == "train_subset_stable_top17" and
       arms["A1_RF17_NONE"]["learner"] == arms["A0_RF42_NONE"]["learner"] and
       arms["A1_RF17_NONE"]["resampling"] == arms["A0_RF42_NONE"]["resampling"] == "none" and
       arms["A1_RF17_NONE"]["class_weight"] is arms["A0_RF42_NONE"]["class_weight"] is None)
    ok("RQ5 balanced weight arm otherwise matched",
       arms["A2_RF42_BALANCED"]["learner"] == "rf" and
       arms["A2_RF42_BALANCED"]["track"] == "all42" and
       arms["A2_RF42_BALANCED"]["class_weight"] == "balanced" and
       arms["A2_RF42_BALANCED"]["resampling"] == "none")
    ok("RQ5 oversampling only on fit minority",
       arms["A3_RF42_OVERSAMPLE"]["learner"] == "rf" and
       arms["A3_RF42_OVERSAMPLE"]["track"] == "all42" and
       arms["A3_RF42_OVERSAMPLE"]["class_weight"] is None and
       arms["A3_RF42_OVERSAMPLE"]["resampling"] ==
       "train_minority_random_oversample_to_majority")
    ok("no unregistered arm resampling/weights",
       all(arm["resampling"] == "none" and arm["class_weight"] is None
           for k, arm in arms.items() if k in {"A0_RF42_NONE", "A1_RF17_NONE", "A4_STACK42_NONE"}))
    ok("no automatic training or excessive resources",
       runtime["pilot_required"] is True and
       runtime["author_explicit_opt_in_required"] is True and
       runtime["worker_concurrency"] == 1 and
       runtime["n_jobs"] == 1 and runtime["blas_threads"] == 1 and
       runtime["process_tree_rss_cap_gib"] == 2 and
       runtime["system_available_floor_gib"] == 1.5 and
       runtime["min_available_ram_at_start_gib"] == 4 and
       runtime["min_free_disk_gib"] >= 10 and
       runtime["automatic_retry"] is False)
    ok("frozen output protections",
       gov["freeze_original_p15_and_pdf_v2"] is True and
       gov["publish_full_data_or_model_binaries"] is False and
       gov["output_dir_must_not_preexist"] is True and
       gov["only_request_pdf_v3_after_author_review"] is True and
       gov["forbid_original_p9_main"] is True and
       gov["forbid_original_stage2_main"] is True)
    ok("forbidden TEST/read and write boundaries",
       all(token in gov["forbid_paths_containing"]
           for token in ("UNSW_NB15_testing-set.csv", "phase9_holdout",
                         "phase10_statistics", "final_evaluation")) and
       all(x in gov["forbid_writing_under"]
           for x in ("report", "results/final_evaluation", "data/raw")) and
       gov["new_output_prefix"] == "results/controlled_extensions/p21_train_only_")
    ok("claims not based on independent seed tests",
       config["outcomes"]["RQ1"]["interpretation"] ==
       "paired_seed_variability_with_common_validation_not_independent_external_test")
    ok("RQ2 paired same algorithm",
       config["outcomes"]["RQ2"]["comparison"] ==
       ["A1_RF17_NONE", "A0_RF42_NONE"])
    ok("RQ5 predeclared paired interventions",
       config["outcomes"]["RQ5"]["comparisons"] ==
       [["A2_RF42_BALANCED", "A0_RF42_NONE"],
        ["A3_RF42_OVERSAMPLE", "A0_RF42_NONE"]])
    return checks


def static_audit(verify_train: bool = False) -> dict:
    config = json.loads(CONTRACT.read_text(encoding="utf-8"))
    checks = validate_contract(config)
    for rel, expected in EXPECTED_FROZEN.items():
        path = ROOT / rel
        if rel in EXPECTED_GIT_LF and path.is_file():
            # Git stores LF; the author-host provenance record was created
            # from the Windows CRLF worktree. Require BOTH exact hashes.
            data = path.read_bytes()
            repo_hash = hashlib.sha256(data).hexdigest()
            crlf_data = data.replace(b"\\r\\n", b"\\n").replace(b"\\n", b"\\r\\n")
            crlf_hash = hashlib.sha256(crlf_data).hexdigest()
            valid = (repo_hash == EXPECTED_GIT_LF[rel] and
                     crlf_hash == expected and b"\\r\\n" not in data)
            checks.append({"id": "frozen_git_lf_and_author_crlf_sha256:" + rel,
                           "pass": valid})
        else:
            checks.append({"id": "frozen_sha256:" + rel,
                           "pass": path.is_file() and sha256(path) == expected})
    train_file = ROOT / config["source"]["raw_train"]
    if verify_train:
        checks.append({"id": "explicit_train_sha256",
                       "pass": train_file.is_file() and sha256(train_file) == TRAIN_SHA256})
    return {
        "protocol": config["protocol_id"],
        "status": "STATIC_PREEXECUTION_AUDIT_ONLY",
        "passed": sum(x["pass"] for x in checks),
        "failed": sum(not x["pass"] for x in checks),
        "checks": checks,
        "raw_train_read": verify_train,
        "official_test_read": False,
        "training_performed": False,
        "metrics_calculated": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verify-local-train-sha", action="store_true",
                   help="Read ONLY the official TRAIN file as opaque bytes on author host.")
    args = p.parse_args()
    result = static_audit(verify_train=args.verify_local_train_sha)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
