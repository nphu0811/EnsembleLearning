"""Fixture-only P21 protocol tests. Never read raw TRAIN/TEST or fit models."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p21_validation", ROOT / "tools/p21_protocol_validator.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
SOURCE = json.loads(
    (ROOT / "config/p21_train_only_protocol_2026_10_18.json")
    .read_text(encoding="utf-8")
)


def failures(protocol):
    return [c["id"] for c in MOD.validate_contract(protocol) if not c["pass"]]


class P21TrainOnlyContractTests(unittest.TestCase):
    def test_current_protocol_is_design_only_valid(self):
        self.assertEqual(failures(copy.deepcopy(SOURCE)), [])

    def test_reject_train_to_test_path_switch(self):
        p = copy.deepcopy(SOURCE)
        p["source"]["raw_train"] = "data/raw/unsw-nb15/UNSW_NB15_testing-set.csv"
        self.assertIn("only official TRAIN path", failures(p))

    def test_reject_training_without_explicit_opt_in(self):
        p = copy.deepcopy(SOURCE)
        p["training_authorized"] = True
        self.assertIn("design-only and not authorized", failures(p))

    def test_reject_reused_global_stable17(self):
        p = copy.deepcopy(SOURCE)
        p["feature_selector"]["never_reuse_historical_full_train_stable17_for_primary"] = False
        self.assertIn("selector training-only fresh for each replicate", failures(p))

    def test_reject_split_and_group_leakage_policy_weakening(self):
        p = copy.deepcopy(SOURCE)
        p["split"]["require_no_row_or_group_overlap"] = False
        self.assertIn("group-disjoint 5-fold validation", failures(p))
        p = copy.deepcopy(SOURCE)
        p["split"]["allow_auto_fallback"] = True
        self.assertIn("no automatic split fallback", failures(p))

    def test_reject_mismatched_rq2_hyperparameter(self):
        p = copy.deepcopy(SOURCE)
        p["model"]["common_rf"]["n_estimators"] = 300
        self.assertIn("matched common RF + threshold", failures(p))

    def test_reject_unbalanced_resampling_on_validation_context(self):
        p = copy.deepcopy(SOURCE)
        p["arms"][3]["resampling"] = "oversample_all_train_validation"
        self.assertIn("RQ5 oversampling only on fit minority", failures(p))

    def test_reject_resource_watcher_disable(self):
        p = copy.deepcopy(SOURCE)
        p["runtime"]["worker_concurrency"] = 4
        self.assertIn("no automatic training or excessive resources", failures(p))

    def test_reject_retarget_original_report_output(self):
        p = copy.deepcopy(SOURCE)
        p["governance"]["new_output_prefix"] = "report/"
        self.assertIn("forbidden TEST/read and write boundaries", failures(p))

    def test_reject_hidden_prospective_claim(self):
        p = copy.deepcopy(SOURCE)
        p["new_experiment_is_post_hoc_relative_to_historical_test"] = False
        self.assertIn("post-hoc / prior TRAIN context disclosed", failures(p))


if __name__ == "__main__":
    unittest.main()
