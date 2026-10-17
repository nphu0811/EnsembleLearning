"""P21 selector safety fixtures: no TRAIN/TEST or sklearn required in this job."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from p21_pilot_guards import (
    safe_new_selector_output, validate_selector_worker_scope,
)
from p21_selector_pilot_supervisor import (
    CONSENT, acceptable_worker, pilot_timeout_ok,
)


class P21SelectorSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "results/controlled_extensions").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_fresh_direct_selector_output_only(self):
        rel = Path("results/controlled_extensions/p21_train_only_pilot_selector17_01")
        self.assertEqual(safe_new_selector_output(self.root, rel), self.root / rel)
        with self.assertRaises(ValueError):
            safe_new_selector_output(
                self.root, Path("results/controlled_extensions/p21_train_only_pilot_rf42_01"))
        with self.assertRaises((ValueError, OSError)):
            safe_new_selector_output(
                self.root, Path("results/controlled_extensions/../p21_train_only_pilot_selector17_escape"))
        (self.root / rel).mkdir()
        with self.assertRaises(ValueError):
            safe_new_selector_output(self.root, rel)

    def test_worker_path_enforces_selector_only(self):
        rel = "results/controlled_extensions/p21_train_only_pilot_selector17_02"
        worker = self.root / rel / "worker"
        worker.mkdir(parents=True)
        validate_selector_worker_scope(worker, self.root)
        other = self.root / "results/controlled_extensions/p21_train_only_pilot_rf42_01/worker"
        other.mkdir(parents=True)
        with self.assertRaises(PermissionError):
            validate_selector_worker_scope(other, self.root)

    def test_authorization_distinct_and_time_bounded(self):
        self.assertEqual(CONSENT, "I_AUTHORIZE_TRAIN_ONLY_P21_SELECTOR17_PILOT")
        self.assertTrue(pilot_timeout_ok(20))
        self.assertFalse(pilot_timeout_ok(21))
        self.assertFalse(pilot_timeout_ok(0))

    def test_fabricated_worker_outcome_guard(self):
        result = {
            "passed": True,
            "scope": "P21_SELECTOR17_FIT_ONLY_RESOURCE_PILOT; no scientific RQ feature selection",
            "pilot_component": "TRAIN_SUBSET_STABLE_TOP17_RESOURCE_PROBE",
            "source_sha256": "t",
            "pilot_fit_rows": 8000,
            "selection": {
                "original_feature_count": 42,
                "selected_feature_count": 17,
                "selection_sample_rows_per_seed": 4667,
                "selector_fit_calls": 15,
                "selection_seeds": [11, 23, 42, 71, 101],
                "methods": ["filter", "l1", "extra_trees"],
                "no_validation_rows_used": True,
                "validated_fit_index_exclusivity": True,
                "pilot_subset_not_for_scientific_comparison": True,
                "pilot_feature_names_saved": False,
                "pilot_selection_digest_sha256": "0" * 64,
            },
            "split": {
                "group_disjoint": True, "row_disjoint": True,
                "validation_evaluation_performed": False,
            },
            "validation_predicted": False,
            "scientific_metrics_calculated": False,
            "model_artifact_saved": False,
            "official_test_opened": False,
        }
        self.assertTrue(acceptable_worker(result, 8000, "t"))
        for section, key, val in [
            ("selection", "selected_feature_count", 18),
            ("selection", "selector_fit_calls", 14),
            ("selection", "no_validation_rows_used", False),
            ("selection", "pilot_feature_names_saved", True),
            ("split", "group_disjoint", False),
            ("top", "official_test_opened", True),
            ("top", "validation_predicted", True),
            ("top", "scientific_metrics_calculated", True),
        ]:
            other = {**result, "selection": dict(result["selection"]),
                     "split": dict(result["split"])}
            if section == "top":
                other[key] = val
            else:
                other[section][key] = val
            with self.subTest(key=key):
                self.assertFalse(acceptable_worker(other, 8000, "t"))


if __name__ == "__main__":
    unittest.main()
