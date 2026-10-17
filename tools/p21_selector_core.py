"""P21 train-fit-only, deterministic stable-top17 selection.

The statistical selectors mirror src/features/select_unsw_features_stage2.py:
MI + 0.95 Spearman redundancy filter; L1-logistic C=0.1/liblinear;
ExtraTrees 200/min_leaf2. New P21 makes ExtraTrees strictly n_jobs=1,
stable tie breaking by feature name, and *never* calls legacy main() or reads
legacy full-TRAIN chosen subsets.

The function requires exactly the caller-declared FIT indices and rejects
any intersection with forbidden validation indices. It cannot read external
files, load models, or compute held-out metrics.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL = ("proto", "service", "state")
EXCLUDED = frozenset(("id", "attack_cat", "label"))
METHODS = ("filter", "l1", "extra_trees")
SELECTION_SEEDS = (11, 23, 42, 71, 101)


def require_fit_only(frame: pd.DataFrame, features: list[str],
                     allowed_fit_indices, forbidden_validation_indices) -> None:
    """Fail closed if a caller tries to include one validation observation."""
    if frame.empty or not frame.index.is_unique:
        raise ValueError("Selector requires a nonempty dataframe with unique FIT row indices")
    eligible = set(int(x) for x in allowed_fit_indices)
    forbidden = set(int(x) for x in forbidden_validation_indices)
    actual = set(int(x) for x in frame.index.tolist())
    if eligible != actual or actual & forbidden or eligible & forbidden:
        raise PermissionError("Feature selection may only use declared FIT rows, never validation")
    if "label" not in frame or set(frame["label"].dropna().unique().tolist()) != {0, 1}:
        raise ValueError("Binary labels required on FIT only")
    if len(features) < 17 or len(features) != len(set(features)) or EXCLUDED & set(features):
        raise ValueError("Feature schema invalid or target/identity leakage")
    if any(x not in frame.columns for x in features):
        raise ValueError("Missing predictor")
    if frame[features].isna().any().any():
        raise ValueError("Missing predictors need a separately locked preprocessing policy")


def original_importance(names, values, numeric, categoricals) -> dict[str, float]:
    scores = {f: 0.0 for f in list(numeric) + list(categoricals)}
    for name, v in zip(names, values):
        name = str(name)
        if name.startswith("num__"):
            feature = name[len("num__"):]
        elif name.startswith("cat__"):
            rest = name[len("cat__"):]
            feature = next((c for c in sorted(categoricals, key=len, reverse=True)
                            if rest == c or rest.startswith(c + "_")), None)
        else:
            feature = None
        if feature not in scores:
            raise ValueError("Unknown transformed feature: " + name)
        scores[feature] += float(v)
    return scores


def top_k(scores: dict[str, float], k: int) -> list[str]:
    if not all(np.isfinite(x) for x in scores.values()):
        raise ValueError("Nonfinite selector importance")
    return [name for name, score in
            sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:k]]


def filter_select(sample: pd.DataFrame, features: list[str], seed: int,
                  k: int, threshold: float = 0.95) -> list[str]:
    X = sample.loc[:, features].copy()
    discrete = []
    for col in features:
        if col in CATEGORICAL:
            codes, _ = pd.factorize(X[col].astype("string"), sort=True)
            X[col] = codes.astype(np.int32)
            discrete.append(True)
        else:
            X[col] = pd.to_numeric(X[col], errors="raise")
            discrete.append(False)
    scores = mutual_info_classif(
        X, sample["label"].to_numpy(), discrete_features=np.asarray(discrete, dtype=bool),
        random_state=seed)
    ordered = top_k(dict(zip(features, scores)), len(features))
    numeric = [f for f in features if f not in CATEGORICAL]
    corr = sample[numeric].corr(method="spearman")
    result: list[str] = []
    for feature in ordered:
        if len(result) == k:
            break
        if feature not in CATEGORICAL:
            if any(
                f not in CATEGORICAL and pd.notna(corr.loc[feature, f]) and
                abs(float(corr.loc[feature, f])) >= threshold
                for f in result
            ):
                continue
        result.append(feature)
    return result


def make_preprocessor(features: list[str], scale: bool) -> ColumnTransformer:
    cat = [f for f in CATEGORICAL if f in features]
    numeric = [f for f in features if f not in cat]
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler() if scale else "passthrough", numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


def l1_select(sample: pd.DataFrame, features: list[str], seed: int, k: int) -> list[str]:
    cat = [f for f in CATEGORICAL if f in features]
    numeric = [f for f in features if f not in cat]
    prep = make_preprocessor(features, scale=True)
    X = prep.fit_transform(sample.loc[:, features])
    clf = LogisticRegression(penalty="l1", solver="liblinear", C=0.1,
                             max_iter=1500, random_state=seed)
    clf.fit(X, sample["label"])
    scores = original_importance(
        prep.get_feature_names_out(), np.abs(clf.coef_.ravel()), numeric, cat)
    return top_k(scores, k)


def extra_trees_select(sample: pd.DataFrame, features: list[str], seed: int, k: int) -> list[str]:
    cat = [f for f in CATEGORICAL if f in features]
    numeric = [f for f in features if f not in cat]
    prep = make_preprocessor(features, scale=False)
    X = prep.fit_transform(sample.loc[:, features])
    clf = ExtraTreesClassifier(n_estimators=200, min_samples_leaf=2,
                               n_jobs=1, random_state=seed)
    clf.fit(X, sample["label"])
    scores = original_importance(
        prep.get_feature_names_out(), clf.feature_importances_, numeric, cat)
    return top_k(scores, k)


def rank_stable_features(method_seed_sets: dict[str, dict[int, set[str]]],
                         features: list[str], seeds=SELECTION_SEEDS,
                         k: int = 17) -> dict:
    if set(method_seed_sets) != set(METHODS) or len(seeds) != 5:
        raise ValueError("Expected 3 methods with five predeclared seeds")
    freq = {}
    for method in METHODS:
        if set(method_seed_sets[method]) != set(seeds):
            raise ValueError("Incomplete selector seed matrix")
        for seed in seeds:
            extra = method_seed_sets[method][seed] - set(features)
            if extra:
                raise ValueError("Selector returned unknown features")
        freq[method] = {f: sum(f in method_seed_sets[method][seed] for seed in seeds)
                        / len(seeds) for f in features}
    table = []
    for feature in features:
        votes = sum(freq[m][feature] >= 0.6 for m in METHODS)
        mean = sum(freq[m][feature] for m in METHODS) / len(METHODS)
        table.append((feature, int(votes), float(mean)))
    table.sort(key=lambda p: (-p[1], -p[2], p[0]))
    selected = [p[0] for p in table[:k]]
    stable_at_least_two = sum(p[1] >= 2 for p in table)
    if len(selected) != k:
        raise ValueError("Cannot form exactly 17 original features")
    return {
        "feature_names": selected,
        "feature_names_sha256": sha256(json.dumps(selected, separators=(",", ":")).encode()).hexdigest(),
        "eligible_stable_count": stable_at_least_two,
        "forced_top17_count": max(0, k - stable_at_least_two),
        "selected_method_votes": [p[1] for p in table[:k]],
        "feature_count": k,
        "selection_method_count": len(METHODS),
        "selection_seed_count": len(seeds),
    }


def fit_only_stable17(fit_frame: pd.DataFrame, features: list[str], *,
                      allowed_fit_indices, forbidden_validation_indices,
                      pilot_sample_rows: int,
                      seeds=SELECTION_SEEDS) -> dict:
    """Select with fit-only labels; never accepts or evaluates validation data."""
    require_fit_only(fit_frame, features, allowed_fit_indices, forbidden_validation_indices)
    if tuple(seeds) != SELECTION_SEEDS:
        raise ValueError("The full 5-seed selector design is locked")
    if not 100 <= pilot_sample_rows < len(fit_frame):
        raise ValueError("Pilot selector sample must be strictly inside FIT subset")
    sets: dict[str, dict[int, set[str]]] = {m: {} for m in METHODS}
    for seed in seeds:
        sample, _ = train_test_split(
            fit_frame, train_size=pilot_sample_rows,
            stratify=fit_frame["label"], random_state=seed)
        if set(sample.index) - set(fit_frame.index):
            raise PermissionError("Selector sample includes rows outside FIT")
        selectors = {
            "filter": filter_select(sample, features, seed, 20),
            "l1": l1_select(sample, features, seed, 20),
            "extra_trees": extra_trees_select(sample, features, seed, 20),
        }
        for method, names in selectors.items():
            sets[method][seed] = set(names)
    result = rank_stable_features(sets, features, seeds=seeds, k=17)
    result.update({
        "source": "P21_TRAIN_FIT_ONLY_PILOT",
        "pilot_only_not_scientific_feature_subset": True,
        "selection_sample_rows_per_seed": pilot_sample_rows,
        "selection_methods": list(METHODS),
        "selection_seeds": list(seeds),
        "no_validation_rows_used": True,
        "validation_scored": False,
        "selector_fit_calls": 15,
    })
    return result
