"""P21 feature-selector leakage tests on fabricated rows only (never UNSW TRAIN/TEST)."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from p21_selector_core import (
    METHODS, SELECTION_SEEDS,
    require_fit_only, rank_stable_features, fit_only_stable17,
)


def dummy_frame(n=260):
    rng = np.random.default_rng(1624)
    label = np.asarray([0, 1] * (n // 2) + ([0] if n % 2 else []))
    columns = {
        f"measure_{i}": rng.normal(size=n) + label * (0.1 if i % 2 == 0 else 0.0)
        for i in range(39)
    }
    columns.update({
        "proto": np.where(np.arange(n) % 2 == 0, "tcp", "udp"),
        "service": np.where(np.arange(n) % 3 == 0, "http", "dns"),
        "state": np.where(np.arange(n) % 5 == 0, "FIN", "INT"),
        "label": label,
    })
    frame = pd.DataFrame(columns)
    features = [k for k in columns if k != "label"]
    assert len(features) == 42
    return frame, features


class P21SelectorSyntheticTests(unittest.TestCase):
    def test_fit_row_guard_rejects_all_validation_leakage(self):
        frame, features = dummy_frame()
        fit = frame.iloc[:200]
        allowed = list(fit.index)
        validation = list(frame.index[200:])
        require_fit_only(fit, features, allowed, validation)
        with self.assertRaises(PermissionError):
            require_fit_only(frame, features, allowed, validation)
        with self.assertRaises(PermissionError):
            require_fit_only(fit, features, allowed + [200], validation)
        with self.assertRaises(ValueError):
            require_fit_only(fit, features + ["label"], allowed, validation)

    def test_five_seed_sampling_only_fit_rows_with_mock_selectors(self):
        frame, features = dummy_frame()
        fit = frame.iloc[:200]
        valid = list(frame.index[200:])
        observed = []
        def mock_select(sample, candidate_features, seed, k):
            self.assertEqual(k, 20)
            self.assertEqual(len(sample), 110)
            self.assertFalse(set(sample.index) & set(valid))
            self.assertTrue(set(sample.index).issubset(set(fit.index)))
            self.assertEqual(set(candidate_features), set(features))
            observed.append(seed)
            return candidate_features[:20]
        with patch("p21_selector_core.filter_select", side_effect=mock_select), \
             patch("p21_selector_core.l1_select", side_effect=mock_select), \
             patch("p21_selector_core.extra_trees_select", side_effect=mock_select):
            result = fit_only_stable17(
                fit, features, allowed_fit_indices=fit.index,
                forbidden_validation_indices=valid, pilot_sample_rows=110)
        self.assertEqual(result["selector_fit_calls"], 15)
        self.assertEqual(len(observed), 15)
        self.assertEqual(set(observed), set(SELECTION_SEEDS))
        self.assertEqual(result["feature_count"], 17)
        self.assertTrue(result["no_validation_rows_used"])

    def test_stable_ranking_and_fallback_tiebreak(self):
        features = [f"f{i:02d}" for i in range(42)]
        seed_sets = {method: {seed: set(features[:20]) for seed in SELECTION_SEEDS}
                     for method in METHODS}
        result = rank_stable_features(seed_sets, features)
        self.assertEqual(result["feature_names"], sorted(features[:20])[:17])
        self.assertEqual(result["forced_top17_count"], 0)
        for method in METHODS:
            for seed in SELECTION_SEEDS:
                seed_sets[method][seed] = set(features[:5])
        result = rank_stable_features(seed_sets, features)
        self.assertEqual(result["eligible_stable_count"], 5)
        self.assertEqual(result["forced_top17_count"], 12)
        self.assertEqual(result["feature_count"], 17)

    def test_all_three_real_methods_finish_on_synthetic_data(self):
        frame, features = dummy_frame()
        fit, valid = frame.iloc[:200], frame.index[200:].tolist()
        result = fit_only_stable17(
            fit, features, allowed_fit_indices=fit.index,
            forbidden_validation_indices=valid, pilot_sample_rows=115)
        self.assertEqual(result["feature_count"], 17)
        self.assertEqual(result["selector_fit_calls"], 15)
        self.assertEqual(result["selection_methods"], list(METHODS))
        self.assertEqual(len(result["feature_names_sha256"]), 64)
        self.assertTrue(set(result["feature_names"]).issubset(set(features)))
        self.assertFalse(result["validation_scored"])


if __name__ == "__main__":
    unittest.main()
