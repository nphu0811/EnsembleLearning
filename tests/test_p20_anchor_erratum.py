"""Regression tests: a single immutable Reviewer A evidence-header typo is NOT a true literal PASS."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p20_review_validator", ROOT / "tools/p20_validate_pre_review.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class ReviewAnchorErratumTests(TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.orig = self.root / MOD.CSV_EVIDENCE
        self.orig.parent.mkdir(parents=True)
        self.orig.write_text("split,label,class_name,count,percentage\nTrain,0,Normal,56000,31.9\n", encoding="utf-8")
        self.packet = self.root / "packet_copy.csv"
        self.packet.write_bytes(self.orig.read_bytes())
        self.erratum = self.root / "documented_erratum.md"
        self.erratum.write_text(MOD.ORIGINAL_A_Q11_HEADER + " -> " + MOD.ACTUAL_CSV_HEADER, encoding="utf-8")
        self.item = {"path": MOD.CSV_EVIDENCE, "locator": "header", "anchor": MOD.ORIGINAL_A_Q11_HEADER}
        self.root_patch = patch.object(MOD, "ROOT", self.root)
        self.erratum_patch = patch.object(MOD, "ERRATUM", self.erratum)
        self.root_patch.start()
        self.erratum_patch.start()

    def tearDown(self):
        self.erratum_patch.stop()
        self.root_patch.stop()
        self.temp.cleanup()

    def test_exact_frozen_A_Q11_known_header_typo(self):
        self.assertTrue(MOD.is_frozen_A_Q11_header_erratum("A-Q11", 1, self.item, self.packet))
        self.assertNotIn(MOD.normalized(self.item["anchor"]), MOD.normalized(self.packet.read_text(encoding="utf-8")))

    def test_wrong_reviewer_question_index_or_anchor_cannot_be_accepted(self):
        for prefix, index in [("B-Q11", 1), ("A-Q11", 0), ("A-Q12", 1)]:
            self.assertFalse(MOD.is_frozen_A_Q11_header_erratum(prefix, index, self.item, self.packet))
        self.assertFalse(MOD.is_frozen_A_Q11_header_erratum("A-Q11", 1, {**self.item, "anchor": "wrong"}, self.packet))
        self.assertFalse(MOD.is_frozen_A_Q11_header_erratum("A-Q11", 1, {**self.item, "path": "unrelated.csv"}, self.packet))

    def test_changed_modelled_csv_or_copy_is_not_an_acceptable_erratum(self):
        self.packet.write_text("split,incorrect,columns\n", encoding="utf-8")
        self.assertFalse(MOD.is_frozen_A_Q11_header_erratum("A-Q11", 1, self.item, self.packet))
        self.packet.write_bytes(self.orig.read_bytes())
        self.orig.write_text("split,edited\n", encoding="utf-8")
        self.assertFalse(MOD.is_frozen_A_Q11_header_erratum("A-Q11", 1, self.item, self.packet))

    def test_missing_erratum_file_is_not_acceptable(self):
        self.erratum.unlink()
        self.assertFalse(MOD.is_frozen_A_Q11_header_erratum("A-Q11", 1, self.item, self.packet))


if __name__ == "__main__":
    main()
