"""Synthetic-only verification of P21 RQ5 fit sampler."""
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from p21_rq5_sampling import prepare_arm, arm_metadata

class TestRQ5Sampler(unittest.TestCase):
    def setUp(self):
        self.ids = np.arange(100, 110)
        self.labels = np.array([0]*7 + [1]*3)

    def test_none_and_balanced_same_rows(self):
        n, w = prepare_arm(self.ids, self.labels, arm="NONE", seed=42, forbidden_validation_indices=[10])
        b, wb = prepare_arm(self.ids, self.labels, arm="BALANCED", seed=42)
        np.testing.assert_array_equal(n, b)
        self.assertIsNone(w)
        self.assertEqual(wb, "balanced")

    def test_oversample_only_fit_minority(self):
        a, w = prepare_arm(self.ids, self.labels, arm="FIT_ONLY_RANDOM_OVERSAMPLE", seed=42,
                           forbidden_validation_indices=[999])
        self.assertIsNone(w)
        self.assertEqual(len(a), 14)
        self.assertTrue(set(a[10:]).issubset({107, 108, 109}))
        m = arm_metadata(self.ids, self.labels, a, arm="FIT_ONLY_RANDOM_OVERSAMPLE")
        self.assertEqual(m["after"], {"0": 7, "1": 7})

    def test_minor_class_reversed(self):
        a, _ = prepare_arm(self.ids, 1-self.labels, arm="FIT_ONLY_RANDOM_OVERSAMPLE", seed=42)
        self.assertTrue(set(a[10:]).issubset({107, 108, 109}))

    def test_validation_overlap_rejected(self):
        with self.assertRaises(ValueError):
            prepare_arm(self.ids, self.labels, arm="NONE", seed=42, forbidden_validation_indices=[105])

    def test_source_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            prepare_arm([1, 1, 2], [0, 1, 1], arm="NONE", seed=42)

    def test_unexpected_class_rejected(self):
        with self.assertRaises(ValueError):
            prepare_arm([1, 2], [0, 2], arm="NONE", seed=42)

    def test_arm_or_cap_violation(self):
        with self.assertRaises(ValueError):
            prepare_arm(self.ids, self.labels, arm="UNLISTED", seed=42)
        with self.assertRaises(ValueError):
            prepare_arm(self.ids, self.labels, arm="FIT_ONLY_RANDOM_OVERSAMPLE", seed=42, max_rows=12)

    def test_reproducible(self):
        a, _ = prepare_arm(self.ids, self.labels, arm="FIT_ONLY_RANDOM_OVERSAMPLE", seed=101)
        b, _ = prepare_arm(self.ids, self.labels, arm="FIT_ONLY_RANDOM_OVERSAMPLE", seed=101)
        np.testing.assert_array_equal(a, b)

if __name__ == "__main__":
    unittest.main()
