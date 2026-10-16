"""
PHASE 8 — UNSW-NB15 Controlled Tuning
=====================================

Purpose
-------
Tune only a small, predeclared set of development candidates while keeping the
official UNSW-NB15 TEST split completely locked.

Candidates
----------
1. Random Forest — all 42 modeling features
2. Stacking      — all 42 modeling features
3. Random Forest — 17 stable features

Stacking base learners:
- Logistic Regression
- Decision Tree
- tuned Random Forest

Stacking meta learner:
- Logistic Regression

Design
------
A. Tune RF-42 and RF-17 with the SAME compact 3-fold CV grid.
B. Generate TRAIN-only OOF probabilities for LR + DT + tuned RF-42.
C. Tune the Logistic meta learner on those OOF probabilities.
D. Produce threshold-sensitivity diagnostics, but DO NOT automatically tune
   the deployment threshold. Default threshold remains 0.5 until explicitly
   frozen.
E. Save exactly three predeclared freeze candidates.

Important
---------
- Official TEST file is never loaded.
- Hyperparameter selection uses TRAIN only.
- Phase-8 CV scores are development/model-selection evidence, not final
  generalization estimates.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    matthews_corrcoef,
    precision_score,
    recall_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_predict,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

RANDOM_STATE = 42
RF_CV_SPLITS = 3
OOF_CV_SPLITS = 3
META_CV_SPLITS = 5

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"

CATEGORICAL_COLS = ["proto", "service", "state"]


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[2]

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "unsw-nb15"
    / "UNSW_NB15_training-set.csv"
)

STAGE2_SUBSETS_FILE = (
    PROJECT_ROOT
    / "results"
    / "feature_selection"
    / "unsw_nb15"
    / "stage2"
    / "subsets"
    / "stage2_candidate_subsets.json"
)

OUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "tuning"
    / "unsw_nb15"
    / "phase8_controlled"
)

TABLE_DIR = OUT_DIR / "tables"


# ---------------------------------------------------------------------
# Public design helpers (also used by tests)
# ---------------------------------------------------------------------

def rf_param_grid() -> dict:
    """
    Deliberately compact RF grid.

    2 * 3 * 2 = 12 candidates, each evaluated with 3-fold CV.
    """
    return {
        "model__n_estimators": [150, 300],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", 0.5],
    }


def meta_param_grid() -> dict:
    """
    Cheap meta-level tuning on three OOF probability features.
    """
    return {
        "C": [0.1, 0.5, 1.0, 2.0, 10.0],
        "class_weight": [None, "balanced"],
    }


def build_freeze_candidates(
    rf42: dict,
    rf17: dict,
    meta: dict,
) -> dict:
    """
    Save only the three predeclared candidates.

    No TEST-driven candidate can enter here.
    """
    return {
        "random_forest_42": {
            "feature_track": "all_features",
            "model": "RandomForestClassifier",
            "hyperparameters": rf42,
            "decision_threshold": 0.5,
        },
        "stacking_42": {
            "feature_track": "all_features",
            "model": "StackingClassifier",
            "base_learners": {
                "logistic_regression": {
                    "C": 1.0,
                    "solver": "liblinear",
                },
                "decision_tree": {
                    "min_samples_leaf": 2,
                },
                "random_forest": rf42,
            },
            "meta_learner": {
                "model": "LogisticRegression",
                **meta,
                "solver": "liblinear",
            },
            "inner_cv": 3,
            "decision_threshold": 0.5,
        },
        "random_forest_17": {
            "feature_track": "stable_17_features",
            "model": "RandomForestClassifier",
            "hyperparameters": rf17,
            "decision_threshold": 0.5,
        },
    }


# ---------------------------------------------------------------------
# Data / preprocessing
# ---------------------------------------------------------------------

def make_ohe():
    try:
        return OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=True,
        )
    except TypeError:
        return OneHotEncoder(
            handle_unknown="ignore",
            sparse=True,
        )


def load_train() -> pd.DataFrame:
    if not TRAIN_FILE.exists():
        raise FileNotFoundError(TRAIN_FILE)

    df = pd.read_csv(
        TRAIN_FILE,
        low_memory=False,
    )
    df.columns = [
        str(c).strip()
        for c in df.columns
    ]
    return df


def load_feature_tracks(
    train: pd.DataFrame,
) -> dict[str, list[str]]:
    all_features = [
        c
        for c in train.columns
        if c not in {
            ID_COL,
            TARGET_COL,
            ATTACK_COL,
        }
    ]

    if not STAGE2_SUBSETS_FILE.exists():
        raise FileNotFoundError(
            STAGE2_SUBSETS_FILE
        )

    stage2 = json.loads(
        STAGE2_SUBSETS_FILE.read_text(
            encoding="utf-8"
        )
    )

    stable = stage2.get(
        "stable_2plus_methods",
        [],
    )

    if not stable:
        raise ValueError(
            "stable_2plus_methods is missing/empty."
        )

    unknown = sorted(
        set(stable) - set(all_features)
    )
    if unknown:
        raise ValueError(
            f"Unknown stable features: {unknown}"
        )

    return {
        "all_features": all_features,
        "stable_17_features": stable,
    }


def build_preprocessor(
    features: list[str],
    scale_numeric: bool,
) -> ColumnTransformer:
    categorical = [
        c
        for c in CATEGORICAL_COLS
        if c in features
    ]

    numeric = [
        c
        for c in features
        if c not in categorical
    ]

    transformers = []

    if numeric:
        transformers.append(
            (
                "num",
                StandardScaler()
                if scale_numeric
                else "passthrough",
                numeric,
            )
        )

    if categorical:
        transformers.append(
            (
                "cat",
                make_ohe(),
                categorical,
            )
        )

    return ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=True,
    )


# ---------------------------------------------------------------------
# Model builders
# ---------------------------------------------------------------------

def make_lr_pipeline(
    features: list[str],
) -> Pipeline:
    return Pipeline([
        (
            "preprocess",
            build_preprocessor(
                features,
                scale_numeric=True,
            ),
        ),
        (
            "model",
            LogisticRegression(
                solver="liblinear",
                C=1.0,
                max_iter=1500,
                random_state=RANDOM_STATE,
            ),
        ),
    ])


def make_dt_pipeline(
    features: list[str],
) -> Pipeline:
    return Pipeline([
        (
            "preprocess",
            build_preprocessor(
                features,
                scale_numeric=False,
            ),
        ),
        (
            "model",
            DecisionTreeClassifier(
                min_samples_leaf=2,
                random_state=RANDOM_STATE,
            ),
        ),
    ])


def make_rf_pipeline(
    features: list[str],
    fixed_params: dict | None = None,
) -> Pipeline:
    params = {
        "n_estimators": 150,
        "min_samples_leaf": 2,
        "max_features": "sqrt",
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
    }

    if fixed_params:
        params.update(
            fixed_params
        )

    return Pipeline([
        (
            "preprocess",
            build_preprocessor(
                features,
                scale_numeric=False,
            ),
        ),
        (
            "model",
            RandomForestClassifier(
                **params
            ),
        ),
    ])


# ---------------------------------------------------------------------
# Scoring / tuning
# ---------------------------------------------------------------------

def scoring_dict() -> dict:
    return {
        "macro_f1": make_scorer(
            f1_score,
            average="macro",
            zero_division=0,
        ),
        "mcc": make_scorer(
            matthews_corrcoef,
        ),
        "balanced_accuracy": make_scorer(
            balanced_accuracy_score,
        ),
        "attack_recall": make_scorer(
            recall_score,
            zero_division=0,
        ),
    }


def strip_model_prefix(
    params: dict,
) -> dict:
    out = {}

    for key, value in params.items():
        if key.startswith(
            "model__"
        ):
            key = key[
                len("model__"):
            ]
        out[key] = value

    return out


def tune_random_forest(
    train: pd.DataFrame,
    features: list[str],
    track_name: str,
) -> tuple[dict, pd.DataFrame, float]:
    X = train[
        features
    ]
    y = train[
        TARGET_COL
    ].to_numpy(
        dtype=int
    )

    cv = StratifiedKFold(
        n_splits=RF_CV_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    search = GridSearchCV(
        estimator=make_rf_pipeline(
            features
        ),
        param_grid=rf_param_grid(),
        scoring=scoring_dict(),
        refit="macro_f1",
        cv=cv,
        n_jobs=1,
        return_train_score=False,
        verbose=1,
    )

    start = time.perf_counter()
    search.fit(
        X,
        y,
    )
    elapsed = (
        time.perf_counter()
        - start
    )

    results = pd.DataFrame(
        search.cv_results_
    )

    keep = [
        c
        for c in results.columns
        if (
            c.startswith("param_")
            or c.startswith("mean_test_")
            or c.startswith("std_test_")
            or c == "rank_test_macro_f1"
            or c == "mean_fit_time"
            or c == "std_fit_time"
        )
    ]

    compact = (
        results[
            keep
        ]
        .sort_values(
            [
                "rank_test_macro_f1",
                "mean_test_mcc",
            ],
            ascending=[
                True,
                False,
            ],
        )
        .reset_index(
            drop=True
        )
    )

    best_params = strip_model_prefix(
        search.best_params_
    )

    print(
        f"[RF TUNING] {track_name}: "
        f"best Macro-F1="
        f"{search.best_score_:.6f}; "
        f"params={best_params}; "
        f"time={elapsed:.1f}s"
    )

    return (
        best_params,
        compact,
        elapsed,
    )


# ---------------------------------------------------------------------
# Base OOF probabilities for meta learner
# ---------------------------------------------------------------------

def generate_meta_features(
    train: pd.DataFrame,
    features: list[str],
    tuned_rf_params: dict,
) -> pd.DataFrame:
    X = train[
        features
    ]
    y = train[
        TARGET_COL
    ].to_numpy(
        dtype=int
    )

    cv = StratifiedKFold(
        n_splits=OOF_CV_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    # Materialize once so every base learner sees identical folds.
    splits = list(
        cv.split(
            X,
            y,
        )
    )

    models = {
        "lr_prob": make_lr_pipeline(
            features
        ),
        "dt_prob": make_dt_pipeline(
            features
        ),
        "rf_prob": make_rf_pipeline(
            features,
            fixed_params=tuned_rf_params,
        ),
    }

    out = pd.DataFrame({
        "row_index": np.arange(
            len(train)
        ),
        "y_true": y,
    })

    for name, estimator in models.items():
        print(
            f"[OOF] generating {name}..."
        )

        prob = cross_val_predict(
            estimator,
            X,
            y,
            cv=splits,
            method="predict_proba",
            n_jobs=1,
        )[:, 1]

        out[
            name
        ] = prob

    return out


def tune_meta_learner(
    meta_features: pd.DataFrame,
) -> tuple[dict, pd.DataFrame]:
    feature_cols = [
        "lr_prob",
        "dt_prob",
        "rf_prob",
    ]

    X_meta = meta_features[
        feature_cols
    ].to_numpy()

    y = meta_features[
        "y_true"
    ].to_numpy(
        dtype=int
    )

    cv = StratifiedKFold(
        n_splits=META_CV_SPLITS,
        shuffle=True,
        random_state=271,
    )

    estimator = LogisticRegression(
        solver="liblinear",
        max_iter=1500,
        random_state=RANDOM_STATE,
    )

    search = GridSearchCV(
        estimator=estimator,
        param_grid=meta_param_grid(),
        scoring=scoring_dict(),
        refit="macro_f1",
        cv=cv,
        n_jobs=-1,
        return_train_score=False,
    )

    search.fit(
        X_meta,
        y,
    )

    results = pd.DataFrame(
        search.cv_results_
    )

    keep = [
        c
        for c in results.columns
        if (
            c.startswith("param_")
            or c.startswith("mean_test_")
            or c.startswith("std_test_")
            or c == "rank_test_macro_f1"
            or c == "mean_fit_time"
        )
    ]

    compact = (
        results[
            keep
        ]
        .sort_values(
            [
                "rank_test_macro_f1",
                "mean_test_mcc",
            ],
            ascending=[
                True,
                False,
            ],
        )
        .reset_index(
            drop=True
        )
    )

    best = {
        "C": float(
            search.best_params_[
                "C"
            ]
        ),
        "class_weight": (
            search.best_params_[
                "class_weight"
            ]
        ),
    }

    print(
        "[META TUNING] "
        f"best Macro-F1="
        f"{search.best_score_:.6f}; "
        f"params={best}"
    )

    return (
        best,
        compact,
    )


# ---------------------------------------------------------------------
# Threshold sensitivity
# ---------------------------------------------------------------------

def metrics_at_threshold(
    y_true: np.ndarray,
    probability: np.ndarray,
    threshold: float,
) -> dict:
    pred = (
        probability >= threshold
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        pred,
        labels=[0, 1],
    ).ravel()

    return {
        "threshold": float(
            threshold
        ),
        "accuracy": float(
            accuracy_score(
                y_true,
                pred,
            )
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(
                y_true,
                pred,
            )
        ),
        "precision": float(
            precision_score(
                y_true,
                pred,
                zero_division=0,
            )
        ),
        "recall_detection_rate": float(
            recall_score(
                y_true,
                pred,
                zero_division=0,
            )
        ),
        "macro_f1": float(
            f1_score(
                y_true,
                pred,
                average="macro",
                zero_division=0,
            )
        ),
        "mcc": float(
            matthews_corrcoef(
                y_true,
                pred,
            )
        ),
        "false_positive_rate": float(
            fp / (fp + tn)
            if (fp + tn)
            else np.nan
        ),
        "false_negative_rate": float(
            fn / (fn + tp)
            if (fn + tp)
            else np.nan
        ),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def threshold_sensitivity_meta(
    meta_features: pd.DataFrame,
    meta_params: dict,
) -> pd.DataFrame:
    X = meta_features[
        [
            "lr_prob",
            "dt_prob",
            "rf_prob",
        ]
    ].to_numpy()

    y = meta_features[
        "y_true"
    ].to_numpy(
        dtype=int
    )

    model = LogisticRegression(
        solver="liblinear",
        max_iter=1500,
        random_state=RANDOM_STATE,
        C=meta_params[
            "C"
        ],
        class_weight=meta_params[
            "class_weight"
        ],
    )

    cv = StratifiedKFold(
        n_splits=META_CV_SPLITS,
        shuffle=True,
        random_state=271,
    )

    oof_prob = cross_val_predict(
        model,
        X,
        y,
        cv=cv,
        method="predict_proba",
        n_jobs=-1,
    )[:, 1]

    thresholds = np.round(
        np.arange(
            0.30,
            0.701,
            0.02,
        ),
        2,
    )

    rows = [
        metrics_at_threshold(
            y,
            oof_prob,
            float(t),
        )
        for t in thresholds
    ]

    return pd.DataFrame(
        rows
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 82)
    print(
        "PHASE 8 — CONTROLLED TUNING"
    )
    print(
        "TRAIN ONLY — OFFICIAL TEST IS NOT LOADED"
    )
    print("=" * 82)

    train = load_train()
    tracks = load_feature_tracks(
        train
    )

    print(
        f"[DATA] training rows: "
        f"{len(train):,}"
    )
    print(
        f"[DATA] all features: "
        f"{len(tracks['all_features'])}"
    )
    print(
        f"[DATA] stable features: "
        f"{len(tracks['stable_17_features'])}"
    )

    # --------------------------------------------------------------
    # RF-42
    # --------------------------------------------------------------
    print(
        "\n[1/4] Tuning Random Forest — 42 features..."
    )

    rf42, rf42_results, rf42_seconds = (
        tune_random_forest(
            train,
            tracks[
                "all_features"
            ],
            "all_features",
        )
    )

    rf42_results.to_csv(
        TABLE_DIR
        / "rf42_grid_results.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # RF-17
    # --------------------------------------------------------------
    print(
        "\n[2/4] Tuning Random Forest — 17 stable features..."
    )

    rf17, rf17_results, rf17_seconds = (
        tune_random_forest(
            train,
            tracks[
                "stable_17_features"
            ],
            "stable_17_features",
        )
    )

    rf17_results.to_csv(
        TABLE_DIR
        / "rf17_grid_results.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # OOF base probabilities for Stacking
    # --------------------------------------------------------------
    print(
        "\n[3/4] Generating 42-feature OOF base probabilities..."
    )

    meta_features = generate_meta_features(
        train,
        tracks[
            "all_features"
        ],
        rf42,
    )

    meta_features.to_csv(
        TABLE_DIR
        / "stacking42_base_oof_probabilities.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # Meta tuning
    # --------------------------------------------------------------
    print(
        "\n[4/4] Tuning Stacking meta learner..."
    )

    meta_params, meta_results = (
        tune_meta_learner(
            meta_features
        )
    )

    meta_results.to_csv(
        TABLE_DIR
        / "stacking42_meta_grid_results.csv",
        index=False,
    )

    threshold_df = (
        threshold_sensitivity_meta(
            meta_features,
            meta_params,
        )
    )

    threshold_df.to_csv(
        TABLE_DIR
        / "stacking42_threshold_sensitivity.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # Freeze candidate manifest
    # --------------------------------------------------------------
    candidates = build_freeze_candidates(
        rf42=rf42,
        rf17=rf17,
        meta=meta_params,
    )

    (
        OUT_DIR
        / "freeze_candidates.json"
    ).write_text(
        json.dumps(
            candidates,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    metadata = {
        "phase": 8,
        "dataset": "UNSW-NB15",
        "official_test_loaded": False,
        "selection_metric": "Macro-F1",
        "rf_cv_splits": RF_CV_SPLITS,
        "base_oof_cv_splits": OOF_CV_SPLITS,
        "meta_cv_splits": META_CV_SPLITS,
        "rf_grid_candidate_count": 12,
        "meta_grid_candidate_count": 10,
        "rf42_tuning_seconds": rf42_seconds,
        "rf17_tuning_seconds": rf17_seconds,
        "threshold_policy": (
            "Threshold sweep is diagnostic only. "
            "No threshold is auto-selected; candidates remain at 0.5."
        ),
        "interpretation_warning": (
            "This phase performs model selection on the official training "
            "split. CV scores may be optimistic after tuning and are not "
            "final test performance."
        ),
    }

    (
        OUT_DIR
        / "experiment_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    best_threshold_row = (
        threshold_df.sort_values(
            [
                "macro_f1",
                "mcc",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .iloc[0]
    )

    threshold_05 = threshold_df.loc[
        np.isclose(
            threshold_df[
                "threshold"
            ],
            0.5,
        )
    ].iloc[0]

    lines = [
        "PHASE 8 — CONTROLLED TUNING SUMMARY",
        "=" * 82,
        "",
        "IMPORTANT:",
        "- Official TEST was not loaded.",
        "- Hyperparameter selection used TRAIN only.",
        "- Threshold sweep is diagnostic; deployment threshold remains 0.5.",
        "",
        "TUNED RANDOM FOREST — 42 FEATURES",
        json.dumps(
            rf42,
            ensure_ascii=False,
        ),
        "",
        "TUNED RANDOM FOREST — 17 FEATURES",
        json.dumps(
            rf17,
            ensure_ascii=False,
        ),
        "",
        "TUNED STACKING META LEARNER — 42 FEATURES",
        json.dumps(
            meta_params,
            ensure_ascii=False,
        ),
        "",
        "STACKING META THRESHOLD DIAGNOSTIC",
        (
            f"At threshold 0.50: "
            f"Macro-F1={threshold_05['macro_f1']:.4f}, "
            f"FPR={threshold_05['false_positive_rate']:.4f}, "
            f"FNR={threshold_05['false_negative_rate']:.4f}"
        ),
        (
            f"Highest development Macro-F1 in sweep occurs near "
            f"threshold={best_threshold_row['threshold']:.2f}: "
            f"Macro-F1={best_threshold_row['macro_f1']:.4f}, "
            f"FPR={best_threshold_row['false_positive_rate']:.4f}, "
            f"FNR={best_threshold_row['false_negative_rate']:.4f}"
        ),
        "",
        "PREDECLARED FREEZE CANDIDATES",
        "- random_forest_42",
        "- stacking_42",
        "- random_forest_17",
        "",
        "NEXT:",
        "Review tuning stability and threshold trade-offs before freezing.",
        "Do not open the official test until the freeze decision is documented.",
    ]

    report = "\n".join(
        lines
    )

    (
        OUT_DIR
        / "phase8_summary.txt"
    ).write_text(
        report,
        encoding="utf-8",
    )

    print()
    print(report)
    print()
    print(
        f"[OUTPUT] {OUT_DIR}"
    )
    print(
        "[DONE] Phase 8 controlled tuning completed."
    )


if __name__ == "__main__":
    main()
