"""P21 resource pilot tests. Pure stdlib fixtures; NO dataset read or model fit."""
from __future__ import annotations
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from p21_pilot_guards import (
    GIB, safe_new_pilot_output, guard_dataset_read,
    audit_file_open, validate_worker_scope, within_resource_budget,
    within_pilot_size,
)
from p21_pilot_supervisor import (
    CONSENT, acceptable_worker, pilot_timeout_ok,
)


class P21PilotSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "results" / "controlled_extensions").mkdir(parents=True)
        (self.root / "data" / "raw" / "unsw-nb15").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_allow_only_new_direct_pilot_output(self):
        name = "results/controlled_extensions/p21_train_only_pilot_rf42_01"
        expected = self.root / name
        self.assertEqual(safe_new_pilot_output(self.root, Path(name)), expected)
        expected.mkdir()
        with self.assertRaises(ValueError):
            safe_new_pilot_output(self.root, Path(name))
        with self.assertRaises(ValueError):
            safe_new_pilot_output(
                self.root, Path("results/controlled_extensions/p21_train_only_rf42_full_01"))
        with self.assertRaises((ValueError, OSError)):
            safe_new_pilot_output(
                self.root, Path("results/controlled_extensions/../p21_train_only_pilot_rf42_escape"))

    def test_worker_write_boundary(self):
        pilot = self.root / "results/controlled_extensions/p21_train_only_pilot_rf42_02"
        worker = pilot / "worker"
        worker.mkdir(parents=True)
        validate_worker_scope(worker, self.root)
        with self.assertRaises(PermissionError):
            validate_worker_scope(self.root / "data/raw/unsw-nb15", self.root)

    def test_only_official_train_file_is_readable_from_data(self):
        train = self.root / "data/raw/unsw-nb15/UNSW_NB15_training-set.csv"
        guard_dataset_read(train, self.root)
        audit_file_open("open", (str(train), "r", 0), self.root)
        for bad in (
            self.root / "data/raw/unsw-nb15/UNSW_NB15_testing-set.csv",
            self.root / "data/raw/unsw-nb15/another.csv",
            self.root / "data/processed/feature_predictions.csv",
            self.root / "data/raw/unsw-nb15/UNSW_NB15_testing-set.csv",
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(PermissionError):
                    guard_dataset_read(bad, self.root)
                with self.assertRaises(PermissionError):
                    audit_file_open("open", (str(bad), "r", 0), self.root)

    def test_non_open_audit_event_is_ignored(self):
        audit_file_open("irrelevant", (str(self.root / "data/raw/unsw-nb15/UNSW_NB15_testing-set.csv"),), self.root)

    def test_resource_guards_and_timeout(self):
        self.assertTrue(within_resource_budget(5 * GIB, 20 * GIB, 2 * GIB))
        self.assertFalse(within_resource_budget(3 * GIB, 20 * GIB, 2 * GIB))
        self.assertFalse(within_resource_budget(5 * GIB, 9 * GIB, 2 * GIB))
        self.assertFalse(within_resource_budget(5 * GIB, 20 * GIB, 3 * GIB))
        self.assertTrue(within_pilot_size(8000))
        self.assertFalse(within_pilot_size(25000))
        self.assertTrue(pilot_timeout_ok(20))
        self.assertFalse(pilot_timeout_ok(0))
        self.assertFalse(pilot_timeout_ok(35))

    def test_reject_forged_worker_success_or_scientific_metrics(self):
        report = {
            "passed": True, "scope": "P21_RF42_ANCHOR_PILOT_ONLY; no RQ result",
            "pilot_component": "A0_RF42_NONE", "source_sha256": "x",
            "pilot_fit_rows": 8000, "feature_count": 42,
            "model_config": {"decision_threshold": 0.5, "n_estimators": 150},
            "split": {"group_disjoint": True, "validation_evaluation_performed": False},
            "validation_predicted": False, "scientific_metrics_calculated": False,
            "model_artifact_saved": False, "official_test_opened": False,
        }
        self.assertTrue(acceptable_worker(report, 8000, "x"))
        for component, key, value in (
            ("top", "official_test_opened", True),
            ("top", "validation_predicted", True),
            ("top", "scientific_metrics_calculated", True),
            ("top", "model_artifact_saved", True),
            ("top", "pilot_fit_rows", 25000),
            ("model", "n_estimators", 300),
            ("split", "validation_evaluation_performed", True),
        ):
            with self.subTest(key=key):
                other = {**report, "model_config": {**report["model_config"]},
                         "split": {**report["split"]}}
                if component == "model":
                    other["model_config"][key] = value
                elif component == "split":
                    other["split"][key] = value
                else:
                    other[key] = value
                self.assertFalse(acceptable_worker(other, 8000, "x"))

    def test_consent_token_is_distinct_and_nonempty(self):
        self.assertEqual(CONSENT, "I_AUTHORIZE_TRAIN_ONLY_P21_RF42_PILOT")


if __name__ == "__main__":
    unittest.main()
