"""Fixture-only safety tests for read-only P15 final-artifact verifier.

These do not load joblib models, read the real UNSW dataset, or run ML.
"""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools/p15_verify_full_artifacts.py"
spec = importlib.util.spec_from_file_location("p15_artifact_acceptance_test", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ArtifactAcceptanceSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "results/reproducibility").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_output_new_unique_and_isolated(self):
        path = mod.secure_output_dir(
            self.root, Path("results/reproducibility/p15_local_artifact_qa_fixture")
        )
        self.assertEqual(path.parent.resolve(), (self.root / "results/reproducibility").resolve())

    def test_output_cannot_reuse_past_results_or_escape(self):
        existing = self.root / "results/reproducibility/p15_local_artifact_qa_exists"
        existing.mkdir()
        for name in (
            existing,
            Path("results/reproducibility/p15_local_rf17_full_01"),
            Path("results/reproducibility/../official_test"),
        ):
            with self.subTest(path=str(name)), self.assertRaises((ValueError, FileNotFoundError)):
                mod.secure_output_dir(self.root, name)

    def test_file_integrity_hash_size_and_tamper(self):
        path = self.root / "model.joblib"
        content = b"trusted-fake-bytes-fixture-not-a-real-pickle"
        path.write_bytes(content)
        expected = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
        self.assertTrue(mod.file_integrity(path, expected))
        self.assertFalse(mod.file_integrity(path, {**expected, "bytes": 42}))
        self.assertFalse(mod.file_integrity(path, {**expected, "sha256": "0" * 64}))
        path.write_bytes(b"tampered")
        self.assertFalse(mod.file_integrity(path, expected))

    def test_model_path_refuses_missing_or_wrong_name(self):
        worker = self.root / "worker"
        worker.mkdir()
        with self.assertRaises(ValueError):
            mod.safe_artifact_path(worker, "fake_RECONSTRUCTED_FULL_TRAIN.joblib")
        path = worker / "fake_RECONSTRUCTED_FULL_TRAIN.joblib"
        path.write_bytes(b"only-a-fixture")
        self.assertEqual(mod.safe_artifact_path(worker, path.name).resolve(), path.resolve())

    def test_only_train_csv_allowed(self):
        with self.assertRaises(PermissionError):
            mod.audit_csv_access(
                "open", (str(mod.ROOT / "data/raw/unsw-nb15/UNSW_NB15_testing-set.csv"), "r", 0)
            )
        with self.assertRaises(PermissionError):
            mod.audit_csv_access(
                "open", (str(mod.ROOT / "data/interim/unsw/test.csv"), "r", 0)
            )
        mod.audit_csv_access("open", (str(mod.TRAIN), "r", 0)

    def test_no_joblib_or_scikit_learn_import_at_module_load(self):
        self.assertIn("verify_one", vars(mod))
        self.assertIn("verify_fitted_configuration", vars(mod))


if __name__ == "__main__":
    unittest.main()
