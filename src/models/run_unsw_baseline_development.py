"""
PHASE 6 — UNSW-NB15 Baseline + Feature-Subset Development Screening
====================================================================

Purpose
-------
Compare candidate feature subsets using matched baseline models on the
OFFICIAL TRAINING SPLIT ONLY.

This is DEVELOPMENT CV, not final test evaluation.

Models
------
1. Logistic Regression      — simple linear baseline
2. Decision Tree            — simple nonlinear single-tree baseline
3. Random Forest            — strong conventional tree-ensemble reference

Why Random Forest here?
-----------------------
Random Forest is technically an ensemble (bagging). We keep it as a strong
standard reference model, but it is NOT the proposed heterogeneous ensemble.
Voting/Stacking/Boosting comparisons belong to Phase 7.

Feature subsets
---------------
- all_features
- stable_2plus_methods
- rfecv_selected_original
- stable_and_rfecv
- stable_all_3_methods

Important
---------
- Official TEST is NEVER loaded.
- `attack_cat` and `id` are NEVER used as model inputs.
- Preprocessing is FIT INSIDE each CV training fold only.
- Categorical encoder uses handle_unknown='ignore'.
- These CV scores are for model/subset DEVELOPMENT and selection.
- Because candidate subsets were discovered from the training split, do not
  present these CV numbers as unbiased final performance. The untouched
  official test is reserved for later final evaluation.

Outputs
-------
results/baselines/unsw_nb15/development_cv/
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
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
CV_SPLITS = 3

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"

CATEGORICAL_COLS = ["proto", "service", "state"]

SUBSETS_TO_COMPARE = [
    "all_features",
    "stable_2plus_methods",
    "rfecv_selected_original",
    "stable_and_rfecv",
    "stable_all_3_methods",
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
    / "baselines"
    / "unsw_nb15"
    / "development_cv"
)

TABLE_DIR = OUT_DIR / "tables"


# ---------------------------------------------------------------------
# Utilities
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

    df = pd.read_csv(TRAIN_FILE, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]

    return df


def load_subsets(train: pd.DataFrame) -> dict[str, list[str]]:
    if not STAGE2_SUBSETS_FILE.exists():
        raise FileNotFoundError(STAGE2_SUBSETS_FILE)

    stage2 = json.loads(
        STAGE2_SUBSETS_FILE.read_text(encoding="utf-8")
    )

    all_features = [
        c
        for c in train.columns
        if c not in {ID_COL, TARGET_COL, ATTACK_COL}
    ]

    subsets = {
        "all_features": all_features,
        "stable_2plus_methods": stage2["stable_2plus_methods"],
        "rfecv_selected_original": stage2["rfecv_selected_original"],
        "stable_and_rfecv": stage2["stable_and_rfecv"],
        "stable_all_3_methods": stage2["stable_all_3_methods"],
    }

    for name, features in subsets.items():
        missing = sorted(set(features) - set(all_features))
        if missing:
            raise ValueError(
                f"Subset {name} contains missing features: {missing}"
            )

    return subsets


def build_preprocessor(
    features: list[str],
    scale_numeric: bool,
) -> ColumnTransformer:
    categorical = [
        c for c in CATEGORICAL_COLS
        if c in features
    ]
    numeric = [
        c for c in features
        if c not in categorical
    ]

    transformers = []

    if numeric:
        transformers.append(
            (
                "num",
                StandardScaler() if scale_numeric else "passthrough",
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


def build_models() -> dict[str, dict]:
    return {
        "logistic_regression": {
            "estimator": LogisticRegression(
                solver="liblinear",
                C=1.0,
                max_iter=1500,
                random_state=RANDOM_STATE,
            ),
            "scale_numeric": True,
        },
        "decision_tree": {
            "estimator": DecisionTreeClassifier(
                random_state=RANDOM_STATE,
                min_samples_leaf=2,
            ),
            "scale_numeric": False,
        },
        "random_forest": {
            "estimator": RandomForestClassifier(
                n_estimators=150,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                min_samples_leaf=2,
            ),
            "scale_numeric": False,
        },
    }


def safe_probability(pipe: Pipeline, X_valid: pd.DataFrame):
    if hasattr(pipe, "predict_proba"):
        return pipe.predict_proba(X_valid)[:, 1]

    if hasattr(pipe, "decision_function"):
        scores = pipe.decision_function(X_valid)
        # AUC metrics only need ranking, but average precision also accepts scores.
        return scores

    return None


def pipeline_size_mb(pipe: Pipeline) -> float:
    payload = pickle.dumps(
        pipe,
        protocol=pickle.HIGHEST_PROTOCOL,
    )
    return len(payload) / (1024 ** 2)


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score,
) -> dict:
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    fpr = fp / (fp + tn) if (fp + tn) else np.nan
    fnr = fn / (fn + tp) if (fn + tp) else np.nan

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(
            y_true,
            y_pred,
        ),
        "precision": precision_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "recall_detection_rate": recall_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "f1": f1_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "false_positive_rate": fpr,
        "false_negative_rate": fnr,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }

    if y_score is not None:
        metrics["roc_auc"] = roc_auc_score(
            y_true,
            y_score,
        )
        metrics["pr_auc"] = average_precision_score(
            y_true,
            y_score,
        )
    else:
        metrics["roc_auc"] = np.nan
        metrics["pr_auc"] = np.nan

    return metrics


def transformed_feature_count(
    pipe: Pipeline,
) -> int:
    prep = pipe.named_steps["preprocess"]

    try:
        return len(prep.get_feature_names_out())
    except Exception:
        return -1


# ---------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------

def run_development_cv(
    train: pd.DataFrame,
    subsets: dict[str, list[str]],
) -> pd.DataFrame:
    y = train[TARGET_COL].to_numpy()

    cv = StratifiedKFold(
        n_splits=CV_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    models = build_models()
    records = []

    for subset_name in SUBSETS_TO_COMPARE:
        features = subsets[subset_name]
        X = train[features]

        print()
        print(
            f"[SUBSET] {subset_name} "
            f"({len(features)} original features)"
        )

        for model_name, cfg in models.items():
            print(f"  [MODEL] {model_name}")

            for fold, (train_idx, valid_idx) in enumerate(
                cv.split(X, y),
                start=1,
            ):
                X_train = X.iloc[train_idx]
                X_valid = X.iloc[valid_idx]

                y_train = y[train_idx]
                y_valid = y[valid_idx]

                prep = build_preprocessor(
                    features,
                    scale_numeric=cfg["scale_numeric"],
                )

                pipe = Pipeline(
                    steps=[
                        ("preprocess", prep),
                        ("model", clone(cfg["estimator"])),
                    ]
                )

                fit_start = time.perf_counter()
                pipe.fit(X_train, y_train)
                train_seconds = (
                    time.perf_counter() - fit_start
                )

                pred_start = time.perf_counter()
                y_pred = pipe.predict(X_valid)
                inference_seconds = (
                    time.perf_counter() - pred_start
                )

                y_score = safe_probability(
                    pipe,
                    X_valid,
                )

                metrics = compute_metrics(
                    y_valid,
                    y_pred,
                    y_score,
                )

                record = {
                    "subset": subset_name,
                    "original_feature_count": len(features),
                    "model": model_name,
                    "fold": fold,
                    "train_rows": len(train_idx),
                    "validation_rows": len(valid_idx),
                    "transformed_feature_count": (
                        transformed_feature_count(pipe)
                    ),
                    "train_time_seconds": train_seconds,
                    "inference_time_seconds": inference_seconds,
                    "inference_ms_per_sample": (
                        inference_seconds
                        / len(valid_idx)
                        * 1000
                    ),
                    "serialized_pipeline_size_mb": (
                        pipeline_size_mb(pipe)
                    ),
                    **metrics,
                }

                records.append(record)

                print(
                    f"    fold={fold} "
                    f"macro_f1={metrics['macro_f1']:.4f} "
                    f"mcc={metrics['mcc']:.4f} "
                    f"train={train_seconds:.2f}s"
                )

    return pd.DataFrame(records)


def aggregate_results(
    folds: pd.DataFrame,
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
        "serialized_pipeline_size_mb",
        "transformed_feature_count",
    ]

    rows = []

    for (subset, model), group in folds.groupby(
        ["subset", "model"],
        sort=False,
    ):
        row = {
            "subset": subset,
            "model": model,
            "original_feature_count": int(
                group["original_feature_count"].iloc[0]
            ),
            "cv_folds": len(group),
        }

        for col in metric_cols:
            row[f"{col}_mean"] = float(group[col].mean())
            row[f"{col}_std"] = float(
                group[col].std(ddof=1)
            )

        rows.append(row)

    out = pd.DataFrame(rows)

    out = out.sort_values(
        ["macro_f1_mean", "mcc_mean"],
        ascending=[False, False],
    ).reset_index(drop=True)

    return out


def build_subset_cost_summary(
    aggregate: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarize each subset across the three baseline perspectives.

    This is descriptive only — not a final winner ranking.
    """
    rows = []

    for subset, group in aggregate.groupby("subset"):
        rows.append({
            "subset": subset,
            "original_feature_count": int(
                group["original_feature_count"].iloc[0]
            ),
            "mean_macro_f1_across_models": float(
                group["macro_f1_mean"].mean()
            ),
            "min_macro_f1_across_models": float(
                group["macro_f1_mean"].min()
            ),
            "mean_mcc_across_models": float(
                group["mcc_mean"].mean()
            ),
            "mean_train_time_seconds": float(
                group["train_time_seconds_mean"].mean()
            ),
            "mean_inference_ms_per_sample": float(
                group["inference_ms_per_sample_mean"].mean()
            ),
        })

    return (
        pd.DataFrame(rows)
        .sort_values(
            "mean_macro_f1_across_models",
            ascending=False,
        )
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("PHASE 6 — BASELINE + FEATURE-SUBSET DEVELOPMENT CV")
    print("OFFICIAL TEST IS NOT LOADED")
    print("=" * 78)

    train = load_train()
    subsets = load_subsets(train)

    metadata = {
        "phase": 6,
        "dataset": "UNSW-NB15",
        "data_source": "official predefined training split",
        "official_test_loaded": False,
        "cv": {
            "type": "StratifiedKFold",
            "n_splits": CV_SPLITS,
            "shuffle": True,
            "random_state": RANDOM_STATE,
        },
        "models": [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest (strong conventional ensemble reference)",
        ],
        "subsets": {
            name: {
                "feature_count": len(features),
                "features": features,
            }
            for name, features in subsets.items()
            if name in SUBSETS_TO_COMPARE
        },
        "interpretation_warning": (
            "Development CV only. Candidate feature subsets were discovered "
            "from the training split; final generalization claims are reserved "
            "for the untouched official test."
        ),
    }

    (
        OUT_DIR / "experiment_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    folds = run_development_cv(
        train,
        subsets,
    )

    aggregate = aggregate_results(folds)
    subset_cost = build_subset_cost_summary(
        aggregate,
    )

    folds.to_csv(
        TABLE_DIR / "fold_metrics.csv",
        index=False,
    )

    aggregate.to_csv(
        TABLE_DIR / "aggregate_metrics.csv",
        index=False,
    )

    subset_cost.to_csv(
        TABLE_DIR / "subset_tradeoff_summary.csv",
        index=False,
    )

    lines = [
        "PHASE 6 — DEVELOPMENT BASELINE SUMMARY",
        "=" * 78,
        "",
        "IMPORTANT:",
        "- Official TEST was never loaded.",
        "- Preprocessing was fitted inside each CV training fold.",
        "- These numbers are DEVELOPMENT evidence, not final test claims.",
        "",
        f"Training records: {len(train):,}",
        f"CV: {CV_SPLITS}-fold StratifiedKFold",
        "",
        "MODELS",
        "- Logistic Regression: simple linear baseline",
        "- Decision Tree: simple nonlinear single-tree baseline",
        "- Random Forest: strong conventional tree-ensemble reference",
        "",
        "FEATURE SUBSETS",
    ]

    for name in SUBSETS_TO_COMPARE:
        lines.append(
            f"- {name}: {len(subsets[name])} original features"
        )

    lines.extend([
        "",
        "TOP DEVELOPMENT RESULTS BY MACRO-F1",
    ])

    for _, row in aggregate.head(10).iterrows():
        lines.append(
            f"- {row['model']} + {row['subset']}: "
            f"Macro-F1={row['macro_f1_mean']:.4f}±"
            f"{row['macro_f1_std']:.4f}, "
            f"MCC={row['mcc_mean']:.4f}, "
            f"train={row['train_time_seconds_mean']:.2f}s, "
            f"features={int(row['original_feature_count'])}"
        )

    lines.extend([
        "",
        "NEXT DECISION",
        "Use this development evidence to narrow the feature-set candidates.",
        "Do not open the official test yet. Phase 7 will build Voting/Stacking/",
        "Boosting against the same development protocol before final freezing.",
    ])

    report = "\n".join(lines)

    (OUT_DIR / "phase6_summary.txt").write_text(
        report,
        encoding="utf-8",
    )

    print()
    print(report)
    print()
    print(f"[OUTPUT] {OUT_DIR}")
    print("[DONE] Phase 6 development screening completed.")


if __name__ == "__main__":
    main()
