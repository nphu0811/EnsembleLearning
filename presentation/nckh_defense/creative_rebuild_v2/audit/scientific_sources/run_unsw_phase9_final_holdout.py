"""
PHASE 9 — UNSW-NB15 Final Holdout Evaluation
==============================================

Purpose
-------
Evaluate exactly the predeclared/frozen Phase-8 candidates on the untouched
official UNSW-NB15 TEST split.

This is the FIRST phase allowed to load the official test set.

Frozen candidates
-----------------
1. random_forest_42
2. stacking_42
3. random_forest_17

Rules
-----
- No hyperparameter search.
- No feature selection.
- No threshold tuning.
- No candidate addition/removal after seeing test results.
- Threshold remains exactly the value stored in the freeze manifest (0.5).

Evaluation views
----------------
1. official_test      — full official test split
2. novel_vector_test  — official test rows whose feature vector did not occur
                        in the official training split

Outputs
-------
results/final_evaluation/unsw_nb15/phase9_holdout/
"""

from __future__ import annotations

import json
import pickle
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------------------------
# Frozen-design constants
# ---------------------------------------------------------------------

RANDOM_STATE = 42
STACKING_INNER_RANDOM_STATE = 137

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"
CATEGORICAL_COLS = ["proto", "service", "state"]

EXPECTED_CANDIDATES = {
    "random_forest_42",
    "stacking_42",
    "random_forest_17",
}


def default_threshold() -> float:
    return 0.5


def validate_freeze_manifest(manifest: dict) -> None:
    keys = set(manifest)

    if keys != EXPECTED_CANDIDATES:
        missing = sorted(
            EXPECTED_CANDIDATES - keys
        )
        extra = sorted(
            keys - EXPECTED_CANDIDATES
        )
        raise ValueError(
            "Freeze manifest candidate mismatch. "
            f"Missing={missing}; extra={extra}"
        )

    for name, cfg in manifest.items():
        threshold = cfg.get(
            "decision_threshold",
            default_threshold(),
        )

        if not np.isclose(
            float(threshold),
            default_threshold(),
        ):
            raise ValueError(
                f"{name}: Phase 9 requires frozen "
                f"threshold=0.5, found {threshold}"
            )


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

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "unsw-nb15"
    / "UNSW_NB15_testing-set.csv"
)

NOVEL_VIEW_FILE = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "unsw-nb15"
    / "test_unseen_vectors.csv"
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

FREEZE_FILE = (
    PROJECT_ROOT
    / "results"
    / "tuning"
    / "unsw_nb15"
    / "phase8_controlled"
    / "freeze_candidates.json"
)

OUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "final_evaluation"
    / "unsw_nb15"
    / "phase9_holdout"
)

TABLE_DIR = OUT_DIR / "tables"


# ---------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------

def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )


def load_csv(path: Path) -> pd.DataFrame:
    require_file(path)
    df = pd.read_csv(
        path,
        low_memory=False,
    )
    df.columns = [
        str(c).strip()
        for c in df.columns
    ]
    return df


def load_manifest() -> dict:
    require_file(FREEZE_FILE)

    manifest = json.loads(
        FREEZE_FILE.read_text(
            encoding="utf-8"
        )
    )

    validate_freeze_manifest(
        manifest
    )
    return manifest


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

    require_file(
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
        set(stable)
        - set(all_features)
    )
    if unknown:
        raise ValueError(
            f"Unknown stable features: {unknown}"
        )

    return {
        "all_features": all_features,
        "stable_17_features": stable,
    }


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
# Frozen model builders
# ---------------------------------------------------------------------

def make_lr_pipeline(
    features: list[str],
    C: float = 1.0,
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
                C=float(C),
                max_iter=1500,
                random_state=RANDOM_STATE,
            ),
        ),
    ])


def make_dt_pipeline(
    features: list[str],
    min_samples_leaf: int = 2,
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
                min_samples_leaf=int(
                    min_samples_leaf
                ),
                random_state=RANDOM_STATE,
            ),
        ),
    ])


def make_rf_pipeline(
    features: list[str],
    params: dict,
) -> Pipeline:
    rf_params = dict(
        params
    )

    rf_params.update({
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
    })

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
                **rf_params
            ),
        ),
    ])


def make_stacking_42(
    features: list[str],
    cfg: dict,
) -> StackingClassifier:
    base_cfg = cfg[
        "base_learners"
    ]

    lr_cfg = base_cfg[
        "logistic_regression"
    ]
    dt_cfg = base_cfg[
        "decision_tree"
    ]
    rf_cfg = base_cfg[
        "random_forest"
    ]

    meta_cfg = cfg[
        "meta_learner"
    ]

    estimators = [
        (
            "lr",
            make_lr_pipeline(
                features,
                C=float(
                    lr_cfg.get(
                        "C",
                        1.0,
                    )
                ),
            ),
        ),
        (
            "dt",
            make_dt_pipeline(
                features,
                min_samples_leaf=int(
                    dt_cfg.get(
                        "min_samples_leaf",
                        2,
                    )
                ),
            ),
        ),
        (
            "rf",
            make_rf_pipeline(
                features,
                params=rf_cfg,
            ),
        ),
    ]

    inner_cv = StratifiedKFold(
        n_splits=int(
            cfg.get(
                "inner_cv",
                3,
            )
        ),
        shuffle=True,
        random_state=(
            STACKING_INNER_RANDOM_STATE
        ),
    )

    final_estimator = (
        LogisticRegression(
            solver=meta_cfg.get(
                "solver",
                "liblinear",
            ),
            C=float(
                meta_cfg.get(
                    "C",
                    1.0,
                )
            ),
            class_weight=(
                meta_cfg.get(
                    "class_weight",
                    None,
                )
            ),
            max_iter=1500,
            random_state=RANDOM_STATE,
        )
    )

    return StackingClassifier(
        estimators=estimators,
        final_estimator=final_estimator,
        cv=inner_cv,
        stack_method="predict_proba",
        passthrough=False,
        n_jobs=1,
    )


def build_frozen_models(
    tracks: dict[str, list[str]],
    manifest: dict,
):
    return {
        "random_forest_42": {
            "features": tracks[
                "all_features"
            ],
            "threshold": float(
                manifest[
                    "random_forest_42"
                ][
                    "decision_threshold"
                ]
            ),
            "model": make_rf_pipeline(
                tracks[
                    "all_features"
                ],
                manifest[
                    "random_forest_42"
                ][
                    "hyperparameters"
                ],
            ),
        },
        "stacking_42": {
            "features": tracks[
                "all_features"
            ],
            "threshold": float(
                manifest[
                    "stacking_42"
                ][
                    "decision_threshold"
                ]
            ),
            "model": make_stacking_42(
                tracks[
                    "all_features"
                ],
                manifest[
                    "stacking_42"
                ],
            ),
        },
        "random_forest_17": {
            "features": tracks[
                "stable_17_features"
            ],
            "threshold": float(
                manifest[
                    "random_forest_17"
                ][
                    "decision_threshold"
                ]
            ),
            "model": make_rf_pipeline(
                tracks[
                    "stable_17_features"
                ],
                manifest[
                    "random_forest_17"
                ][
                    "hyperparameters"
                ],
            ),
        },
    }


# ---------------------------------------------------------------------
# Novel-vector mask
# ---------------------------------------------------------------------

def novel_mask_from_saved_view(
    test: pd.DataFrame,
) -> np.ndarray | None:
    if not NOVEL_VIEW_FILE.exists():
        return None

    novel = pd.read_csv(
        NOVEL_VIEW_FILE,
        low_memory=False,
    )
    novel.columns = [
        str(c).strip()
        for c in novel.columns
    ]

    if ID_COL in novel.columns:
        novel_ids = set(
            novel[
                ID_COL
            ].tolist()
        )

        return test[
            ID_COL
        ].isin(
            novel_ids
        ).to_numpy(
            dtype=bool
        )

    return None


def novel_mask_by_feature_hash(
    train: pd.DataFrame,
    test: pd.DataFrame,
    all_features: list[str],
) -> np.ndarray:
    """
    Deterministic fallback when the saved novel-view file is unavailable.

    Hashes are used only as a fast membership representation of complete
    42-feature vectors. The mask itself does not use labels.
    """
    train_hash = pd.util.hash_pandas_object(
        train[
            all_features
        ],
        index=False,
    ).to_numpy()

    test_hash = pd.util.hash_pandas_object(
        test[
            all_features
        ],
        index=False,
    ).to_numpy()

    seen = set(
        train_hash.tolist()
    )

    return np.fromiter(
        (
            h not in seen
            for h in test_hash
        ),
        dtype=bool,
        count=len(test_hash),
    )


# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------

def model_size_mb(
    model,
) -> float:
    payload = pickle.dumps(
        model,
        protocol=pickle.HIGHEST_PROTOCOL,
    )
    return (
        len(payload)
        / (1024 ** 2)
    )


def classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
) -> dict:
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    fpr = (
        fp / (fp + tn)
        if fp + tn
        else np.nan
    )

    fnr = (
        fn / (fn + tp)
        if fn + tp
        else np.nan
    )

    return {
        "n_rows": int(
            len(y_true)
        ),
        "accuracy": float(
            accuracy_score(
                y_true,
                y_pred,
            )
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(
                y_true,
                y_pred,
            )
        ),
        "precision": float(
            precision_score(
                y_true,
                y_pred,
                zero_division=0,
            )
        ),
        "recall_detection_rate": float(
            recall_score(
                y_true,
                y_pred,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                y_true,
                y_pred,
                zero_division=0,
            )
        ),
        "macro_f1": float(
            f1_score(
                y_true,
                y_pred,
                average="macro",
                zero_division=0,
            )
        ),
        "mcc": float(
            matthews_corrcoef(
                y_true,
                y_pred,
            )
        ),
        "roc_auc": float(
            roc_auc_score(
                y_true,
                y_prob,
            )
        ),
        "pr_auc": float(
            average_precision_score(
                y_true,
                y_prob,
            )
        ),
        "false_positive_rate": float(
            fpr
        ),
        "false_negative_rate": float(
            fnr
        ),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def attack_miss_profile(
    test_with_predictions: pd.DataFrame,
    model_names: list[str],
    eval_view: str,
    mask: np.ndarray,
) -> pd.DataFrame:
    frame = test_with_predictions.loc[
        mask
    ].copy()

    frame = frame[
        frame[
            TARGET_COL
        ] == 1
    ]

    rows = []

    for attack, group in frame.groupby(
        ATTACK_COL
    ):
        row = {
            "eval_view": eval_view,
            "attack_cat": str(
                attack
            ),
            "attack_rows": int(
                len(group)
            ),
        }

        for name in model_names:
            pred = group[
                f"{name}_pred"
            ]

            fn = int(
                (pred == 0).sum()
            )

            row[
                f"{name}_false_negatives"
            ] = fn

            row[
                f"{name}_miss_rate"
            ] = (
                fn / len(group)
                if len(group)
                else np.nan
            )

        rows.append(
            row
        )

    return pd.DataFrame(
        rows
    )


def pairwise_error_counts(
    prediction_frame: pd.DataFrame,
    model_names: list[str],
    mask: np.ndarray,
    eval_view: str,
) -> pd.DataFrame:
    frame = prediction_frame.loc[
        mask
    ]

    truth = frame[
        TARGET_COL
    ].to_numpy(
        dtype=int
    )

    rows = []

    for a, b in combinations(
        model_names,
        2,
    ):
        err_a = (
            frame[
                f"{a}_pred"
            ].to_numpy(
                dtype=int
            )
            != truth
        )

        err_b = (
            frame[
                f"{b}_pred"
            ].to_numpy(
                dtype=int
            )
            != truth
        )

        rows.append({
            "eval_view": eval_view,
            "model_a": a,
            "model_b": b,
            "both_correct": int(
                np.sum(
                    (~err_a)
                    & (~err_b)
                )
            ),
            "a_wrong_b_correct": int(
                np.sum(
                    err_a
                    & (~err_b)
                )
            ),
            "a_correct_b_wrong": int(
                np.sum(
                    (~err_a)
                    & err_b
                )
            ),
            "both_wrong": int(
                np.sum(
                    err_a
                    & err_b
                )
            ),
        })

    return pd.DataFrame(
        rows
    )


# ---------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------

def main():
    TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 84)
    print(
        "PHASE 9 — FINAL HOLDOUT EVALUATION"
    )
    print(
        "OFFICIAL TEST IS NOW OPENED "
        "FOR FROZEN PIPELINES ONLY"
    )
    print("=" * 84)

    train = load_csv(
        TRAIN_FILE
    )

    # FIRST official-test load in the study.
    test = load_csv(
        TEST_FILE
    )

    tracks = load_feature_tracks(
        train
    )

    manifest = load_manifest()

    print(
        f"[DATA] train: "
        f"{len(train):,} rows"
    )
    print(
        f"[DATA] official test: "
        f"{len(test):,} rows"
    )

    novel_mask = (
        novel_mask_from_saved_view(
            test
        )
    )

    novel_source = (
        "saved_view"
    )

    if novel_mask is None:
        novel_mask = (
            novel_mask_by_feature_hash(
                train,
                test,
                tracks[
                    "all_features"
                ],
            )
        )
        novel_source = (
            "recomputed_from_feature_vectors"
        )

    official_mask = np.ones(
        len(test),
        dtype=bool,
    )

    print(
        f"[DATA] novel-vector test: "
        f"{int(novel_mask.sum()):,} rows "
        f"({novel_source})"
    )

    frozen = build_frozen_models(
        tracks,
        manifest,
    )

    y_train = train[
        TARGET_COL
    ].to_numpy(
        dtype=int
    )

    y_test = test[
        TARGET_COL
    ].to_numpy(
        dtype=int
    )

    prediction_frame = test[
        [
            ID_COL,
            ATTACK_COL,
            TARGET_COL,
        ]
    ].copy()

    prediction_frame[
        "is_novel_vector"
    ] = novel_mask

    metric_rows = []
    cost_rows = []

    for name in [
        "random_forest_42",
        "stacking_42",
        "random_forest_17",
    ]:
        cfg = frozen[
            name
        ]
        features = cfg[
            "features"
        ]
        threshold = cfg[
            "threshold"
        ]
        model = cfg[
            "model"
        ]

        print(
            f"\n[FINAL] {name}"
        )
        print(
            f"  features={len(features)}; "
            f"threshold={threshold}"
        )

        fit_start = (
            time.perf_counter()
        )

        model.fit(
            train[
                features
            ],
            y_train,
        )

        train_seconds = (
            time.perf_counter()
            - fit_start
        )

        predict_start = (
            time.perf_counter()
        )

        probability = (
            model.predict_proba(
                test[
                    features
                ]
            )[:, 1]
        )

        prediction = (
            probability
            >= threshold
        ).astype(int)

        inference_seconds = (
            time.perf_counter()
            - predict_start
        )

        size_mb = model_size_mb(
            model
        )

        prediction_frame[
            f"{name}_prob"
        ] = probability

        prediction_frame[
            f"{name}_pred"
        ] = prediction

        for view_name, mask in [
            (
                "official_test",
                official_mask,
            ),
            (
                "novel_vector_test",
                novel_mask,
            ),
        ]:
            metrics = (
                classification_metrics(
                    y_test[
                        mask
                    ],
                    prediction[
                        mask
                    ],
                    probability[
                        mask
                    ],
                )
            )

            metric_rows.append({
                "pipeline": name,
                "eval_view": view_name,
                "original_feature_count": (
                    len(features)
                ),
                "decision_threshold": (
                    threshold
                ),
                **metrics,
            })

            print(
                f"  [{view_name}] "
                f"Macro-F1="
                f"{metrics['macro_f1']:.4f} | "
                f"MCC={metrics['mcc']:.4f} | "
                f"FPR="
                f"{metrics['false_positive_rate']:.4f} | "
                f"FNR="
                f"{metrics['false_negative_rate']:.4f}"
            )

        cost_rows.append({
            "pipeline": name,
            "original_feature_count": (
                len(features)
            ),
            "train_time_seconds": (
                train_seconds
            ),
            "inference_time_seconds": (
                inference_seconds
            ),
            "inference_ms_per_sample": (
                inference_seconds
                / len(test)
                * 1000
            ),
            "serialized_model_size_mb": (
                size_mb
            ),
        })

        print(
            f"  fit={train_seconds:.2f}s; "
            f"inference="
            f"{inference_seconds:.2f}s; "
            f"size={size_mb:.2f} MB"
        )

    model_names = [
        "random_forest_42",
        "stacking_42",
        "random_forest_17",
    ]

    metrics_df = pd.DataFrame(
        metric_rows
    )

    cost_df = pd.DataFrame(
        cost_rows
    )

    attack_profiles = pd.concat(
        [
            attack_miss_profile(
                prediction_frame,
                model_names,
                "official_test",
                official_mask,
            ),
            attack_miss_profile(
                prediction_frame,
                model_names,
                "novel_vector_test",
                novel_mask,
            ),
        ],
        ignore_index=True,
    )

    pairwise_df = pd.concat(
        [
            pairwise_error_counts(
                prediction_frame,
                model_names,
                official_mask,
                "official_test",
            ),
            pairwise_error_counts(
                prediction_frame,
                model_names,
                novel_mask,
                "novel_vector_test",
            ),
        ],
        ignore_index=True,
    )

    metrics_df.to_csv(
        TABLE_DIR
        / "final_metrics.csv",
        index=False,
    )

    cost_df.to_csv(
        TABLE_DIR
        / "cost_metrics.csv",
        index=False,
    )

    attack_profiles.to_csv(
        TABLE_DIR
        / "attack_category_miss_profile.csv",
        index=False,
    )

    pairwise_df.to_csv(
        TABLE_DIR
        / "pairwise_error_counts.csv",
        index=False,
    )

    prediction_frame.to_csv(
        TABLE_DIR
        / "official_test_predictions.csv",
        index=False,
    )

    metadata = {
        "phase": 9,
        "dataset": "UNSW-NB15",
        "official_test_opened": True,
        "train_rows": int(
            len(train)
        ),
        "official_test_rows": int(
            len(test)
        ),
        "novel_vector_rows": int(
            novel_mask.sum()
        ),
        "novel_vector_source": (
            novel_source
        ),
        "frozen_candidates": (
            manifest
        ),
        "rules": [
            "No hyperparameter tuning on TEST.",
            "No feature selection on TEST.",
            "No threshold tuning on TEST.",
            "No candidate addition after TEST inspection.",
        ],
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

    official = metrics_df[
        metrics_df[
            "eval_view"
        ] == "official_test"
    ].copy()

    lines = [
        "PHASE 9 — FINAL HOLDOUT SUMMARY",
        "=" * 84,
        "",
        "IMPORTANT:",
        "- This is the first use of the official UNSW-NB15 TEST split.",
        "- All pipelines were frozen before the test was opened.",
        "- No tuning, feature selection, or threshold selection used TEST.",
        "",
        f"Train rows: {len(train):,}",
        f"Official test rows: {len(test):,}",
        (
            f"Novel-vector test rows: "
            f"{int(novel_mask.sum()):,}"
        ),
        "",
        "OFFICIAL TEST",
    ]

    for _, row in official.sort_values(
        [
            "macro_f1",
            "mcc",
        ],
        ascending=[
            False,
            False,
        ],
    ).iterrows():
        lines.append(
            f"- {row['pipeline']}: "
            f"Macro-F1={row['macro_f1']:.4f}, "
            f"MCC={row['mcc']:.4f}, "
            f"FPR={row['false_positive_rate']:.4f}, "
            f"FNR={row['false_negative_rate']:.4f}, "
            f"ROC-AUC={row['roc_auc']:.4f}, "
            f"PR-AUC={row['pr_auc']:.4f}"
        )

    lines.extend([
        "",
        "POST-TEST RULE:",
        "Do not alter the frozen pipelines because of these test results.",
        "Next phase performs statistical/error analysis on the saved predictions.",
    ])

    report = "\n".join(
        lines
    )

    (
        OUT_DIR
        / "phase9_summary.txt"
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
        "[DONE] Final holdout evaluation completed."
    )


if __name__ == "__main__":
    main()
