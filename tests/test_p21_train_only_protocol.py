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

    def test_hash_verifier_accepts_exact_lf_and_crlf(self):
        import hashlib

        lf = b'{"stable_features": 17}\n{"seed": 42}\n'
        crlf = lf.replace(b"\n", b"\r\n")
        git_hash = hashlib.sha256(lf).hexdigest()
        author_hash = hashlib.sha256(crlf).hexdigest()
        self.assertTrue(MOD.verify_dual_eol_bytes(lf, git_hash, author_hash))
        self.assertTrue(MOD.verify_dual_eol_bytes(crlf, git_hash, author_hash))

    def test_hash_verifier_rejects_changes_mixed_eol_and_stray_cr(self):
        import hashlib

        lf = b'{"stable_features": 17}\n{"seed": 42}\n'
        crlf = lf.replace(b"\n", b"\r\n")
        git_hash = hashlib.sha256(lf).hexdigest()
        author_hash = hashlib.sha256(crlf).hexdigest()
        altered = lf.replace(b"17", b"18")
        mixed = b'{"stable_features": 17}\r\n{"seed": 42}\n'
        stray_cr = b'{"stable_features": 17}\r{"seed": 42}\n'
        for bad in (altered, mixed, stray_cr, b"", lf + b" "):
            with self.subTest(bad=bad):
                self.assertFalse(MOD.verify_dual_eol_bytes(bad, git_hash, author_hash))

    def test_hash_verifier_rejects_one_incorrect_expected_digest(self):
        import hashlib

        lf = b'{"stable_features": 17}\n'
        crlf = lf.replace(b"\n", b"\r\n")
        git_hash = hashlib.sha256(lf).hexdigest()
        author_hash = hashlib.sha256(crlf).hexdigest()
        self.assertFalse(MOD.verify_dual_eol_bytes(lf, "0" * 64, author_hash))
        self.assertFalse(MOD.verify_dual_eol_bytes(crlf, git_hash, "0" * 64))

    def test_actual_tracked_json_accepts_windows_byte_representation(self):
        for rel, git_hash in MOD.EXPECTED_GIT_LF.items():
            with self.subTest(file=rel):
                # A Windows checkout may already contain CRLF. Build each
                # exact representation from LF, avoiding accidental CRCRLF.
                lf_data = (ROOT / rel).read_bytes().replace(b"\r\n", b"\n")
                self.assertTrue(
                    MOD.verify_dual_eol_bytes(
                        lf_data, git_hash, MOD.EXPECTED_FROZEN[rel]
                    )
                )
                windows_bytes = lf_data.replace(b"\n", b"\r\n")
                self.assertTrue(
                    MOD.verify_dual_eol_bytes(
                        windows_bytes, git_hash, MOD.EXPECTED_FROZEN[rel]
                    )
                )

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
