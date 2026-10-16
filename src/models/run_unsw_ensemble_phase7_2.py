"""
PHASE 7.2 — UNSW-NB15 Voting / Stacking Development Comparison
================================================================

Purpose
-------
Compare justified heterogeneous ensembles against strong ensemble references
using the SAME outer cross-validation folds on the OFFICIAL TRAINING split.

This is DEVELOPMENT evaluation only.
The official test split is NEVER loaded.

Configurations
--------------
References:
1. Random Forest      — bagging reference
2. AdaBoost           — boosting reference

Heterogeneous ensembles:
3. Hard Voting        — Logistic Regression + Decision Tree + Random Forest
4. Soft Voting        — Logistic Regression + Decision Tree + Random Forest
5. Stacking           — LR + DT + RF -> Logistic Regression meta-learner

Feature tracks
--------------
1. all_features        — all 42 modeling features
2. stable_17_features  — Stage-2 stable >=2-method subset

Leakage control
---------------
Outer 3-fold Stratified CV:
    outer train -> fit complete model/ensemble
    outer valid -> evaluate

For Stacking, sklearn's StackingClassifier generates internal out-of-fold
predictions using INNER CV on the outer-training fold before fitting the
meta-learner. Therefore the outer validation fold is never used to train
either the base learners or the meta-learner.

Outputs
-------
results/ensemble/unsw_nb15/phase7_2_ensemble_cv/
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
    StackingClassifier,
    VotingClassifier,
)
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
# Configuration
# ---------------------------------------------------------------------

RANDOM_STATE = 42
OUTER_CV_SPLITS = 3
STACKING_INNER_CV_SPLITS = 3

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"

CATEGORICAL_COLS = ["proto", "service", "state"]

FEATURE_TRACKS = [
    "all_features",
    "stable_17_features",
]

CONFIGURATIONS = [
    "random_forest",
    "adaboost",
    "hard_voting_lrdtrf",
    "soft_voting_lrdtrf",
    "stacking_lrdtrf",
]


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
    / "ensemble"
    / "unsw_nb15"
    / "phase7_2_ensemble_cv"
)

TABLE_DIR = OUT_DIR / "tables"
OOF_DIR = OUT_DIR / "oof"


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


def make_adaboost():
    tree = DecisionTreeClassifier(
        max_depth=2,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
    )

    # Compatibility with old/new sklearn.
    try:
        return AdaBoostClassifier(
            estimator=tree,
            n_estimators=100,
            learning_rate=0.5,
            random_state=RANDOM_STATE,
        )
    except TypeError:
        return AdaBoostClassifier(
            base_estimator=tree,
            n_estimators=100,
            learning_rate=0.5,
            random_state=RANDOM_STATE,
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
# Base pipelines
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
                random_state=RANDOM_STATE,
                min_samples_leaf=2,
            ),
        ),
    ])


def make_rf_pipeline(
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
            RandomForestClassifier(
                n_estimators=150,
                min_samples_leaf=2,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        ),
    ])


def make_adaboost_pipeline(
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
            make_adaboost(),
        ),
    ])


# ---------------------------------------------------------------------
# Ensemble builders
# ---------------------------------------------------------------------

def base_estimators(
    features: list[str],
):
    return [
        ("lr", make_lr_pipeline(features)),
        ("dt", make_dt_pipeline(features)),
        ("rf", make_rf_pipeline(features)),
    ]


def build_configuration(
    name: str,
    features: list[str],
):
    if name == "random_forest":
        return make_rf_pipeline(features)

    if name == "adaboost":
        return make_adaboost_pipeline(
            features
        )

    if name == "hard_voting_lrdtrf":
        return VotingClassifier(
            estimators=base_estimators(
                features
            ),
            voting="hard",
            n_jobs=1,  # avoid nested parallelism with RF
        )

    if name == "soft_voting_lrdtrf":
        return VotingClassifier(
            estimators=base_estimators(
                features
            ),
            voting="soft",
            n_jobs=1,
        )

    if name == "stacking_lrdtrf":
        inner_cv = StratifiedKFold(
            n_splits=STACKING_INNER_CV_SPLITS,
            shuffle=True,
            random_state=137,
        )

        return StackingClassifier(
            estimators=base_estimators(
                features
            ),
            final_estimator=LogisticRegression(
                solver="liblinear",
                C=1.0,
                max_iter=1500,
                random_state=RANDOM_STATE,
            ),
            cv=inner_cv,
            stack_method="predict_proba",
            passthrough=False,
            n_jobs=1,  # RF itself already uses all cores
        )

    raise ValueError(
        f"Unknown configuration: {name}"
    )


# ---------------------------------------------------------------------
# Prediction / metrics
# ---------------------------------------------------------------------

def hard_vote_fraction(
    fitted_voter: VotingClassifier,
    X: pd.DataFrame,
) -> np.ndarray:
    """
    Continuous-ish score for Hard Voting:
    fraction of fitted base learners voting Attack.
    Values for 3 models are {0, 1/3, 2/3, 1}.
    """
    votes = np.column_stack(
        [
            estimator.predict(X)
            for estimator
            in fitted_voter.estimators_
        ]
    )

    return votes.mean(axis=1)


def prediction_score(
    config_name: str,
    fitted_model,
    X: pd.DataFrame,
) -> np.ndarray:
    if config_name == "hard_voting_lrdtrf":
        return hard_vote_fraction(
            fitted_model,
            X,
        )

    if hasattr(
        fitted_model,
        "predict_proba",
    ):
        return fitted_model.predict_proba(
            X
        )[:, 1]

    if hasattr(
        fitted_model,
        "decision_function",
    ):
        return np.asarray(
            fitted_model.decision_function(
                X
            ),
            dtype=float,
        )

    return fitted_model.predict(
        X
    ).astype(float)


def model_size_mb(
    fitted_model,
) -> float:
    try:
        payload = pickle.dumps(
            fitted_model,
            protocol=pickle.HIGHEST_PROTOCOL,
        )
        return (
            len(payload)
            / (1024 ** 2)
        )
    except Exception:
        return np.nan


def classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray,
) -> dict:
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    fpr = (
        fp / (fp + tn)
        if (fp + tn)
        else np.nan
    )

    fnr = (
        fn / (fn + tp)
        if (fn + tp)
        else np.nan
    )

    return {
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
                y_score,
            )
        ),
        "pr_auc": float(
            average_precision_score(
                y_true,
                y_score,
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


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def run_track(
    train: pd.DataFrame,
    features: list[str],
    track_name: str,
    splits,
):
    X = train[features]
    y = train[
        TARGET_COL
    ].to_numpy(dtype=int)

    oof = pd.DataFrame({
        "row_index": np.arange(
            len(train)
        ),
        "id": train[
            ID_COL
        ].to_numpy(),
        "attack_cat": train[
            ATTACK_COL
        ].astype(str).to_numpy(),
        "y_true": y,
        "fold": np.zeros(
            len(train),
            dtype=int,
        ),
    })

    for config_name in CONFIGURATIONS:
        oof[
            f"{config_name}_pred"
        ] = -1

        oof[
            f"{config_name}_score"
        ] = np.nan

    fold_rows = []

    print(
        f"\n[TRACK] {track_name}: "
        f"{len(features)} original features"
    )

    for fold, (
        train_idx,
        valid_idx,
    ) in enumerate(
        splits,
        start=1,
    ):
        X_train = X.iloc[
            train_idx
        ]
        X_valid = X.iloc[
            valid_idx
        ]

        y_train = y[
            train_idx
        ]
        y_valid = y[
            valid_idx
        ]

        oof.loc[
            valid_idx,
            "fold",
        ] = fold

        print(
            f"  [OUTER FOLD {fold}/"
            f"{OUTER_CV_SPLITS}] "
            f"train={len(train_idx):,}, "
            f"valid={len(valid_idx):,}"
        )

        for config_name in CONFIGURATIONS:
            print(
                f"    [MODEL] "
                f"{config_name}"
            )

            model = build_configuration(
                config_name,
                features,
            )

            fit_start = (
                time.perf_counter()
            )
            model.fit(
                X_train,
                y_train,
            )
            fit_seconds = (
                time.perf_counter()
                - fit_start
            )

            pred_start = (
                time.perf_counter()
            )

            y_pred = model.predict(
                X_valid
            ).astype(int)

            y_score = (
                prediction_score(
                    config_name,
                    model,
                    X_valid,
                )
            )

            inference_seconds = (
                time.perf_counter()
                - pred_start
            )

            metrics = (
                classification_metrics(
                    y_valid,
                    y_pred,
                    y_score,
                )
            )

            size_mb = model_size_mb(
                model
            )

            oof.loc[
                valid_idx,
                f"{config_name}_pred",
            ] = y_pred

            oof.loc[
                valid_idx,
                f"{config_name}_score",
            ] = y_score

            fold_rows.append({
                "feature_track": track_name,
                "original_feature_count": len(
                    features
                ),
                "configuration": config_name,
                "fold": fold,
                "train_rows": len(
                    train_idx
                ),
                "validation_rows": len(
                    valid_idx
                ),
                "train_time_seconds": fit_seconds,
                "inference_time_seconds": (
                    inference_seconds
                ),
                "inference_ms_per_sample": (
                    inference_seconds
                    / len(valid_idx)
                    * 1000
                ),
                "serialized_model_size_mb": size_mb,
                **metrics,
            })

            print(
                f"      Macro-F1="
                f"{metrics['macro_f1']:.4f} | "
                f"MCC={metrics['mcc']:.4f} | "
                f"FPR={metrics['false_positive_rate']:.4f} | "
                f"FNR={metrics['false_negative_rate']:.4f} | "
                f"fit={fit_seconds:.2f}s"
            )

    # Integrity checks.
    for config_name in CONFIGURATIONS:
        if (
            oof[
                f"{config_name}_pred"
            ] < 0
        ).any():
            raise RuntimeError(
                f"Missing OOF predictions: "
                f"{track_name}/"
                f"{config_name}"
            )

        if (
            oof[
                f"{config_name}_score"
            ].isna().any()
        ):
            raise RuntimeError(
                f"Missing OOF scores: "
                f"{track_name}/"
                f"{config_name}"
            )

    return (
        oof,
        pd.DataFrame(
            fold_rows
        ),
    )


# ---------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------

def aggregate_fold_metrics(
    fold_df: pd.DataFrame,
) -> pd.DataFrame:
    metric_cols = [
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall_detection_rate",
        "f1",
        "macro_f1",
        "mcc",
        "roc_auc",
        "pr_auc",
        "false_positive_rate",
        "false_negative_rate",
        "train_time_seconds",
        "inference_time_seconds",
        "inference_ms_per_sample",
        "serialized_model_size_mb",
    ]

    rows = []

    for (
        track,
        config,
    ), group in fold_df.groupby(
        [
            "feature_track",
            "configuration",
        ],
        sort=False,
    ):
        row = {
            "feature_track": track,
            "configuration": config,
            "original_feature_count": int(
                group[
                    "original_feature_count"
                ].iloc[0]
            ),
            "cv_folds": len(
                group
            ),
        }

        for metric in metric_cols:
            row[
                f"{metric}_mean"
            ] = float(
                group[
                    metric
                ].mean()
            )

            row[
                f"{metric}_std"
            ] = float(
                group[
                    metric
                ].std(
                    ddof=1
                )
            )

        rows.append(
            row
        )

    return pd.DataFrame(
        rows
    )


def pooled_oof_metrics(
    oof: pd.DataFrame,
    track_name: str,
) -> pd.DataFrame:
    y = oof[
        "y_true"
    ].to_numpy(
        dtype=int
    )

    rows = []

    for config_name in CONFIGURATIONS:
        pred = oof[
            f"{config_name}_pred"
        ].to_numpy(
            dtype=int
        )

        score = oof[
            f"{config_name}_score"
        ].to_numpy(
            dtype=float
        )

        metrics = (
            classification_metrics(
                y,
                pred,
                score,
            )
        )

        rows.append({
            "feature_track": track_name,
            "configuration": config_name,
            **metrics,
        })

    return pd.DataFrame(
        rows
    )


def comparison_vs_rf(
    pooled: pd.DataFrame,
    aggregate: pd.DataFrame,
) -> pd.DataFrame:
    merged = pooled.merge(
        aggregate[
            [
                "feature_track",
                "configuration",
                "train_time_seconds_mean",
                "inference_ms_per_sample_mean",
                "serialized_model_size_mb_mean",
            ]
        ],
        on=[
            "feature_track",
            "configuration",
        ],
        how="left",
    )

    rows = []

    for track, group in merged.groupby(
        "feature_track"
    ):
        ref = group[
            group[
                "configuration"
            ] == "random_forest"
        ]

        if ref.empty:
            continue

        ref = ref.iloc[0]

        for _, row in group.iterrows():
            if (
                row[
                    "configuration"
                ]
                == "random_forest"
            ):
                continue

            rows.append({
                "feature_track": track,
                "configuration": row[
                    "configuration"
                ],
                "delta_macro_f1_vs_rf": (
                    row[
                        "macro_f1"
                    ]
                    - ref[
                        "macro_f1"
                    ]
                ),
                "delta_mcc_vs_rf": (
                    row[
                        "mcc"
                    ]
                    - ref[
                        "mcc"
                    ]
                ),
                "delta_fpr_vs_rf": (
                    row[
                        "false_positive_rate"
                    ]
                    - ref[
                        "false_positive_rate"
                    ]
                ),
                "delta_fnr_vs_rf": (
                    row[
                        "false_negative_rate"
                    ]
                    - ref[
                        "false_negative_rate"
                    ]
                ),
                "train_time_ratio_vs_rf": (
                    row[
                        "train_time_seconds_mean"
                    ]
                    / ref[
                        "train_time_seconds_mean"
                    ]
                ),
                "inference_time_ratio_vs_rf": (
                    row[
                        "inference_ms_per_sample_mean"
                    ]
                    / ref[
                        "inference_ms_per_sample_mean"
                    ]
                ),
                "model_size_ratio_vs_rf": (
                    row[
                        "serialized_model_size_mb_mean"
                    ]
                    / ref[
                        "serialized_model_size_mb_mean"
                    ]
                ),
            })

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

    OOF_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 82)
    print(
        "PHASE 7.2 — VOTING / "
        "STACKING DEVELOPMENT COMPARISON"
    )
    print(
        "OFFICIAL TEST IS NOT LOADED"
    )
    print("=" * 82)

    train = load_train()
    tracks = load_feature_tracks(
        train
    )

    y = train[
        TARGET_COL
    ].to_numpy(
        dtype=int
    )

    outer_cv = StratifiedKFold(
        n_splits=OUTER_CV_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    # Materialize once so every configuration uses
    # exactly the same outer folds.
    splits = list(
        outer_cv.split(
            np.zeros(
                len(y)
            ),
            y,
        )
    )

    all_fold_metrics = []
    all_pooled = []

    for track_name in FEATURE_TRACKS:
        features = tracks[
            track_name
        ]

        oof, fold_metrics = run_track(
            train,
            features,
            track_name,
            splits,
        )

        pooled = pooled_oof_metrics(
            oof,
            track_name,
        )

        oof.to_csv(
            OOF_DIR
            / f"{track_name}_ensemble_oof.csv",
            index=False,
        )

        all_fold_metrics.append(
            fold_metrics
        )
        all_pooled.append(
            pooled
        )

    fold_df = pd.concat(
        all_fold_metrics,
        ignore_index=True,
    )

    pooled_df = pd.concat(
        all_pooled,
        ignore_index=True,
    )

    aggregate_df = (
        aggregate_fold_metrics(
            fold_df
        )
    )

    delta_df = comparison_vs_rf(
        pooled_df,
        aggregate_df,
    )

    fold_df.to_csv(
        TABLE_DIR
        / "fold_metrics.csv",
        index=False,
    )

    aggregate_df.to_csv(
        TABLE_DIR
        / "aggregate_metrics.csv",
        index=False,
    )

    pooled_df.to_csv(
        TABLE_DIR
        / "pooled_oof_metrics.csv",
        index=False,
    )

    delta_df.to_csv(
        TABLE_DIR
        / "comparison_vs_random_forest.csv",
        index=False,
    )

    metadata = {
        "phase": "7.2",
        "dataset": "UNSW-NB15",
        "official_test_loaded": False,
        "outer_cv": {
            "type": "StratifiedKFold",
            "n_splits": OUTER_CV_SPLITS,
            "shuffle": True,
            "random_state": RANDOM_STATE,
        },
        "stacking_inner_cv": {
            "type": "StratifiedKFold",
            "n_splits": STACKING_INNER_CV_SPLITS,
            "shuffle": True,
            "random_state": 137,
        },
        "configurations": {
            "random_forest": (
                "bagging reference"
            ),
            "adaboost": (
                "boosting reference"
            ),
            "hard_voting_lrdtrf": (
                "equal hard vote: LR + DT + RF"
            ),
            "soft_voting_lrdtrf": (
                "equal probability average: LR + DT + RF"
            ),
            "stacking_lrdtrf": (
                "LR + DT + RF base learners; "
                "Logistic Regression meta-learner"
            ),
        },
        "feature_tracks": {
            name: {
                "count": len(
                    features
                ),
                "features": features,
            }
            for (
                name,
                features,
            ) in tracks.items()
        },
        "interpretation_warning": (
            "Development CV only. No final "
            "generalization claim may be made "
            "until the official test is opened "
            "after configuration freezing."
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

    lines = [
        "PHASE 7.2 — ENSEMBLE DEVELOPMENT SUMMARY",
        "=" * 82,
        "",
        "IMPORTANT:",
        "- Official TEST was not loaded.",
        "- All configurations used identical outer folds.",
        "- Stacking meta-model was trained only from INNER-CV predictions",
        "  generated inside each outer-training fold.",
        "",
        "POOLED OOF PERFORMANCE",
    ]

    for track in FEATURE_TRACKS:
        lines.append(
            f"\n[{track}]"
        )

        block = (
            pooled_df[
                pooled_df[
                    "feature_track"
                ] == track
            ]
            .sort_values(
                [
                    "macro_f1",
                    "mcc",
                ],
                ascending=[
                    False,
                    False,
                ],
            )
        )

        for _, row in block.iterrows():
            lines.append(
                f"- {row['configuration']}: "
                f"Macro-F1={row['macro_f1']:.4f}, "
                f"MCC={row['mcc']:.4f}, "
                f"FPR={row['false_positive_rate']:.4f}, "
                f"FNR={row['false_negative_rate']:.4f}, "
                f"ROC-AUC={row['roc_auc']:.4f}"
            )

    lines.extend([
        "",
        "COST",
    ])

    for _, row in (
        aggregate_df
        .sort_values(
            [
                "feature_track",
                "train_time_seconds_mean",
            ]
        )
        .iterrows()
    ):
        lines.append(
            f"- {row['feature_track']} / "
            f"{row['configuration']}: "
            f"fit={row['train_time_seconds_mean']:.2f}s/fold, "
            f"inference={row['inference_ms_per_sample_mean']:.6f} ms/sample, "
            f"size={row['serialized_model_size_mb_mean']:.2f} MB"
        )

    lines.extend([
        "",
        "NEXT:",
        "Use performance + FPR/FNR + cost to freeze a very small number",
        "of candidate pipelines. Do NOT open the official test until the",
        "configuration decision is documented.",
    ])

    report = "\n".join(
        lines
    )

    (
        OUT_DIR
        / "phase7_2_summary.txt"
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
        "[DONE] Phase 7.2 "
        "development comparison completed."
    )


if __name__ == "__main__":
    main()
