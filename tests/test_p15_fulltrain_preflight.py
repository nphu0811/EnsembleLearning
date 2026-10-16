"""Fixture-only tests; never access official TEST or run any model."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "p15_fulltrain_preflight.py"
spec = importlib.util.spec_from_file_location("p15_preflight", MODULE)
p15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p15)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        train_path = self.root / "data/raw/unsw-nb15/UNSW_NB15_training-set.csv"
        freeze_path = self.root / "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json"
        subset_path = self.root / "results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json"
        source_path = self.root / "src/models/run_unsw_phase9_final_holdout.py"
        self.files = [train_path, freeze_path, subset_path, source_path]
        for path in self.files:
            path.parent.mkdir(parents=True, exist_ok=True)
        self.features = [f"feature_{i}" for i in range(42)]
        train_path.write_text("id," + ",".join(self.features) + ",attack_cat,label\n" +
                              "1," + ",".join("0" for _ in self.features) + ",Normal,0\n" +
                              "2," + ",".join("1" for _ in self.features) + ",Fuzzers,1\n", encoding="utf-8")
        freeze_path.write_text(json.dumps({key: {"decision_threshold": 0.5}
                                           for key in p15.EXPECTED_CANDIDATES}), encoding="utf-8")
        subset_path.write_text(json.dumps({"stable_2plus_methods": self.features[:17]}), encoding="utf-8")
        source_path.write_text("# synthetic fixture, no training\n", encoding="utf-8")
        self.hashes = {str(path.relative_to(self.root)).replace("\\", "/"):
                       hashlib.sha256(path.read_bytes()).hexdigest() for path in self.files}

    def tearDown(self):
        self.tmp.cleanup()

    def check(self):
        return p15.audit(self.root, expected_hashes=self.hashes,
                         expected_train_rows=2, expected_normal=1, expected_attack=1,
                         ram_bytes=10 * 1024**3, disk_bytes=12 * 1024**3,
                         check_git=False, expected_python=tuple(__import__("sys").version_info[:2]))

    def test_valid_fixture_passes_but_never_authorizes_training(self):
        r = self.check()
        self.assertTrue(r["preflight_checks_pass"])
        self.assertFalse(r["training_authorized"])
        self.assertEqual(r["reconstruction_status"], "NOT_RUN")

    def test_modifying_frozen_manifest_breaks_hash(self):
        p = self.files[1]
        p.write_text(p.read_text() + " ", encoding="utf-8")
        self.assertFalse(self.check()["preflight_checks_pass"])

    def test_changed_threshold_is_rejected_even_with_new_hash(self):
        p = self.files[1]
        p.write_text(json.dumps({key: {"decision_threshold": 0.4}
                                 for key in p15.EXPECTED_CANDIDATES}), encoding="utf-8")
        self.hashes[str(p.relative_to(self.root)).replace("\\", "/")] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertFalse(self.check()["checks"]["frozen_candidates_threshold"]["pass"])

    def test_low_ram_is_no_go(self):
        r = p15.audit(self.root, expected_hashes=self.hashes, expected_train_rows=2,
                      expected_normal=1, expected_attack=1, ram_bytes=1024,
                      disk_bytes=12 * 1024**3, check_git=False,
                      expected_python=tuple(__import__("sys").version_info[:2]))
        self.assertFalse(r["checks"]["available_ram_ge_9gib"]["pass"])
        self.assertFalse(r["training_authorized"])

    def test_modified_train_fails_before_any_fit(self):
        self.files[0].write_text(self.files[0].read_text() + "3," + ",".join("0" for _ in self.features) + ",Normal,0\n")
        r = self.check()
        self.assertFalse(r["checks"]["train_counts"]["pass"])
        self.assertFalse(r["checks"]["sha256:data/raw/unsw-nb15/UNSW_NB15_training-set.csv"]["pass"])

    def test_subset_unknown_feature_rejected(self):
        p = self.files[2]
        p.write_text(json.dumps({"stable_2plus_methods": self.features[:16] + ["missing"]}), encoding="utf-8")
        self.assertFalse(self.check()["checks"]["stable_17_subset"]["pass"])


if __name__ == "__main__":
    unittest.main()
