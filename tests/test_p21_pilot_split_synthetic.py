"""P21 feature-vector group split tests on fabricated rows only.

These tests install pandas/numpy/scikit-learn in a separate CI job. There is no
access to UNSW-NB15 raw TRAIN or TEST and no model fitting.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from p21_pilot_worker import fingerprint_and_split


def fake_42_feature_dataset(groups: int = 300, copies: int = 3):
    rows = []
    for g in range(groups):
        features = {f"n{i}": float(g * 0.1 + (i % 5)) for i in range(39)}
        features.update({
            "proto": ["tcp", "udp"][g % 2],
            "service": ["http", "dns"][g % 2],
            "state": ["FIN", "INT"][g % 2],
        })
        for _ in range(copies):
            rows.append({**features, "label": g % 2})
    frame = pd.DataFrame(rows)
    selected = [c for c in frame.columns if c != "label"]
    assert len(selected) == 42
    return frame, selected


class P21GroupSplitSyntheticTests(TestCase):
    def test_exact_duplicate_vectors_are_group_disjoint(self):
        frame, features = fake_42_feature_dataset()
        fit, val, report = fingerprint_and_split(frame, features, 20261018)
        self.assertTrue(report["row_disjoint"])
        self.assertTrue(report["group_disjoint"])
        self.assertFalse(report["validation_evaluation_performed"])
        self.assertEqual(len(fit) + len(val), len(frame))
        self.assertTrue(0.18 <= len(val) / len(frame) <= 0.22)
        self.assertLessEqual(abs((frame.label.iloc[val] == 0).mean() - (frame.label == 0).mean()), 0.02)
        fit_keys = set(map(tuple, frame.iloc[fit][features].to_numpy().tolist()))
        val_keys = set(map(tuple, frame.iloc[val][features].to_numpy().tolist()))
        self.assertFalse(fit_keys & val_keys)

    def test_injected_hash_collision_is_rejected(self):
        frame, features = fake_42_feature_dataset(groups=100)
        with patch("pandas.util.hash_pandas_object",
                   return_value=pd.Series(np.zeros(len(frame), dtype=np.uint64))):
            with self.assertRaisesRegex(ValueError, "Hash collision"):
                fingerprint_and_split(frame, features, 20261018)

    def test_missing_predictor_is_rejected_before_split(self):
        frame, features = fake_42_feature_dataset(groups=100)
        frame.loc[0, features[0]] = np.nan
        with self.assertRaisesRegex(ValueError, "Missing/duplicate"):
            fingerprint_and_split(frame, features, 20261018)


if __name__ == "__main__":
    main()
