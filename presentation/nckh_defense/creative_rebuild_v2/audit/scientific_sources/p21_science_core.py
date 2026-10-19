"""P21 scientific TRAIN-derived contrasts: deterministic helpers, no data reads."""
from __future__ import annotations

import hashlib
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, matthews_corrcoef, precision_score, recall_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

ARM_IDS = ("A0_RF42_NONE", "A1_RF17_NONE", "A2_RF42_BALANCED",
           "A3_RF42_OVERSAMPLE", "A4_STACK42_NONE")


def make_preprocess(features, categorical):
    """Preprocessing fitted strictly inside each learner's training fold."""
    cat = [c for c in categorical if c in features]
    nums = [f for f in features if f not in cat]
    if len(set(features)) != len(features) or not nums:
        raise ValueError("Duplicate/empty numeric predictor set")
    return ColumnTransformer([
        ("num", "passthrough", nums),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
    ], remainder="drop")


def make_rf(features, cfg, seed, *, weighting=None):
    r = cfg["model"]["common_rf"]
    return Pipeline([
        ("preprocess", make_preprocess(features, cfg["source"]["categorical_predictors"])),
        ("model", RandomForestClassifier(
            n_estimators=r["n_estimators"], min_samples_leaf=r["min_samples_leaf"],
            max_features=r["max_features"], bootstrap=r["bootstrap"],
            class_weight=weighting, n_jobs=1, random_state=int(seed)
        )),
    ])


def inner_group_folds(X_fit, y_fit, *, seed=137):
    """Group exact full 42-predictor row vectors for unbiased inner OOF training.

    This is the explicit PRE-FULL-P21 safety amendment to the originally
    proposed stratified-only inner CV. A seed's outer validation rows never
    enter X_fit/y_fit. No validation labels used for group CV.
    """
    groups = pd.util.hash_pandas_object(X_fit, index=False).to_numpy(dtype=np.uint64)
    if len(groups) != len(X_fit):
        raise ValueError("Broken inner group fingerprints")
    # Hash collisions fail closed even for rare adversarial/typed collisions.
    duplicates = pd.Series(groups).duplicated(keep=False).to_numpy()
    if duplicates.any():
        dup = X_fit.iloc[np.flatnonzero(duplicates)].copy()
        dup["_group"] = groups[duplicates]
        if dup.groupby("_group", dropna=False, sort=False)[list(X_fit.columns)].nunique(dropna=False).gt(1).any(axis=1).any():
            raise ValueError("Fingerprint collision in inner CV")
    cv = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=seed)
    folds = list(cv.split(np.zeros((len(X_fit), 1)), y_fit, groups))
    check = np.zeros(len(X_fit), dtype=np.int8)
    for train_idx, validation_idx in folds:
        if (set(groups[train_idx]) & set(groups[validation_idx]) or
                set(np.unique(y_fit[train_idx])) != {0, 1} or
                set(np.unique(y_fit[validation_idx])) != {0, 1}):
            raise ValueError("Unacceptable class support or exact-vector leakage in inner folds")
        check[validation_idx] += 1
    if np.any(check != 1):
        raise ValueError("Inner group CV is not a complete nonoverlapping partition")
    return folds


def make_stacking(features, cfg, seed, folds):
    s = cfg["model"]["stacking_lite"]
    if (s["inner_cv"] != 3 or s["inner_cv_seed"] != 137 or
            s["stack_method"] != "predict_proba" or s["passthrough"] is not False):
        raise ValueError("Unexpected frozen stacking configuration")
    cat = cfg["source"]["categorical_predictors"]
    base = [
        ("lr", Pipeline([
            ("preprocess", make_preprocess(features, cat)),
            ("scale", StandardScaler(with_mean=False)),
            ("model", LogisticRegression(
                C=s["base_lr"]["C"], solver=s["base_lr"]["solver"],
                max_iter=1000, random_state=seed))
        ])),
        ("dt", Pipeline([
            ("preprocess", make_preprocess(features, cat)),
            ("model", DecisionTreeClassifier(
                min_samples_leaf=s["base_dt"]["min_samples_leaf"],
                random_state=seed))
        ])),
        ("rf", make_rf(features, cfg, seed)),
    ]
    return StackingClassifier(
        estimators=base,
        final_estimator=LogisticRegression(
            C=s["meta_lr"]["C"], solver=s["meta_lr"]["solver"],
            class_weight=s["meta_lr"]["class_weight"], random_state=seed,
            max_iter=1000),
        cv=folds, stack_method="predict_proba", passthrough=False, n_jobs=1,
    )


def binary_metrics(y_true, probabilities):
    """Return locked threshold metrics, never tune based on held-out scores."""
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    if (y.ndim != 1 or p.shape != y.shape or len(y) == 0 or
            set(np.unique(y)) != {0, 1} or
            not np.isfinite(p).all() or np.any(p < 0) or np.any(p > 1)):
        raise ValueError("Binary evaluation shape, probability or support invalid")
    pred = (p >= 0.5).astype(int)
    tn, fp, fn, tp = [int(x) for x in confusion_matrix(y, pred, labels=[0, 1]).ravel()]
    return {
        "macro_f1": float(f1_score(y, pred, average="macro", zero_division=0)),
        "mcc": float(matthews_corrcoef(y, pred)),
        "attack_precision": float(precision_score(y, pred, pos_label=1, zero_division=0)),
        "attack_recall": float(recall_score(y, pred, pos_label=1, zero_division=0)),
        "fpr": fp / (fp + tn), "fnr": fn / (fn + tp),
        "tn": tn, "fp": fp, "fn": fn, "tp": tp, "validation_rows": len(y),
        "threshold": 0.5,
    }


def fit_ids_digest(indices):
    """Fingerprint SORTED FIT ids for row-identity pairing verification."""
    unique = sorted(int(x) for x in indices)
    if len(unique) != len(set(unique)):
        raise ValueError("FIT IDs must be unique before resampling")
    return hashlib.sha256(json.dumps(unique, separators=(",", ":")).encode()).hexdigest()
