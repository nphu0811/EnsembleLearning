"""Pure P21 RQ5 sampling rules; never reads dataset, scores or TEST."""
from __future__ import annotations
import numpy as np

ARMS = ("NONE", "BALANCED", "FIT_ONLY_RANDOM_OVERSAMPLE")

def prepare_arm(fit_indices, labels, *, arm: str, seed: int,
                forbidden_validation_indices=(), max_rows: int = 16000):
    """Return source row indices for FIT-only training and class_weight.
    
    Inputs are positional IDs from the *already frozen* group-disjoint FIT pool.
    Never supply test/validation source rows. Duplicate source IDs are allowed
    only for oversampling. No model is fitted by this helper.
    """
    if arm not in ARMS:
        raise ValueError("Unknown predeclared RQ5 treatment")
    fit = np.asarray(fit_indices, dtype=np.int64)
    y = np.asarray(labels)
    banned = np.asarray(forbidden_validation_indices, dtype=np.int64)
    if fit.ndim != 1 or y.ndim != 1 or len(fit) != len(y):
        raise ValueError("FIT indices / labels mismatch")
    if not len(fit) or np.unique(fit).size != len(fit):
        raise ValueError("FIT source indices must be nonempty and unique")
    if np.intersect1d(fit, banned).size:
        raise ValueError("Validation contamination detected")
    classes, counts = np.unique(y, return_counts=True)
    if classes.tolist() != [0, 1]:
        raise ValueError("Expected exactly labels 0 and 1")
    if len(fit) > max_rows:
        raise ValueError("FIT sample above resource cap")
    selected = fit.copy()
    if arm == "FIT_ONLY_RANDOM_OVERSAMPLE":
        minority = classes[np.argmin(counts)]
        deficit = int(counts.max() - counts.min())
        if len(selected) + deficit > max_rows:
            raise ValueError("Oversampling would exceed row safety cap")
        minority_ids = fit[y == minority]
        rng = np.random.default_rng(seed)
        selected = np.concatenate((fit, rng.choice(minority_ids, size=deficit, replace=True)))
    if not set(selected.tolist()).issubset(set(fit.tolist())):
        raise AssertionError("Sampling leaked out of FIT")
    if np.intersect1d(selected, banned).size:
        raise AssertionError("Sampling leaked into validation")
    weights = "balanced" if arm == "BALANCED" else None
    return selected, weights

def arm_metadata(fit_indices, fit_labels, chosen_indices, *, arm: str):
    """Aggregate counts only; do not serialize indices or per-row predictions."""
    fit = np.asarray(fit_indices)
    y = np.asarray(fit_labels)
    lookup = dict(zip(fit.tolist(), y.tolist()))
    before = {str(c): int((y == c).sum()) for c in (0, 1)}
    after = {str(c): int(sum(lookup[int(i)] == c for i in chosen_indices)) for c in (0, 1)}
    return {"arm": arm, "before": before, "after": after, "fit_rows": len(fit),
            "fitted_rows": len(chosen_indices), "scientific_metrics_calculated": False}
