"""
PHASE 7.1 — UNSW-NB15 OOF Base-Learner Diversity Analysis
==========================================================

Goal
----
Measure whether candidate base learners make complementary errors BEFORE
constructing Voting/Stacking ensembles.

This is TRAIN-only development analysis.

Models
------
1. Logistic Regression
2. Decision Tree
3. Random Forest
4. AdaBoost

Feature tracks
--------------
1. all_features        — all 42 model features
2. stable_17_features  — Stage-2 stable >=2-method subset

Protocol
--------
- 3-fold Stratified CV on the official training split.
- Each row receives an Out-Of-Fold (OOF) prediction from a model that was
  NOT trained on that row.
- Preprocessing is fitted inside each training fold only.
- Official test data is NEVER loaded.

Diversity metrics
-----------------
For each model pair:
- Disagreement Rate
- Double-Fault Rate
- Pairwise Oracle Accuracy = 1 - Double-Fault
- Q-statistic
- Error Correlation
- Probability Correlation

Interpretation
--------------
Diversity alone is NOT sufficient. A weak random model can be highly diverse.
Useful ensemble candidates should combine:
    individual predictive strength + complementary errors.

Outputs
-------
results/ensemble/unsw_nb15/phase7_1_diversity/
"""

from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
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


RANDOM_STATE = 42
CV_SPLITS = 3

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"

CATEGORICAL_COLS = ["proto", "service", "state"]
FEATURE_TRACKS = ["all_features", "stable_17_features"]

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
    / "phase7_1_diversity"
)

TABLE_DIR = OUT_DIR / "tables"
OOF_DIR = OUT_DIR / "oof"


def make_ohe():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=True)


def load_train() -> pd.DataFrame:
    if not TRAIN_FILE.exists():
        raise FileNotFoundError(TRAIN_FILE)

    df = pd.read_csv(TRAIN_FILE, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def load_feature_tracks(train: pd.DataFrame) -> dict[str, list[str]]:
    all_features = [
        c for c in train.columns
        if c not in {ID_COL, TARGET_COL, ATTACK_COL}
    ]

    if not STAGE2_SUBSETS_FILE.exists():
        raise FileNotFoundError(STAGE2_SUBSETS_FILE)

    stage2 = json.loads(
        STAGE2_SUBSETS_FILE.read_text(encoding="utf-8")
    )
    stable = stage2.get("stable_2plus_methods", [])

    if not stable:
        raise ValueError("stable_2plus_methods is missing/empty.")

    return {
        "all_features": all_features,
        "stable_17_features": stable,
    }


def build_preprocessor(features: list[str], scale_numeric: bool):
    categorical = [c for c in CATEGORICAL_COLS if c in features]
    numeric = [c for c in features if c not in categorical]

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
            ("cat", make_ohe(), categorical)
        )

    return ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=True,
    )


def model_registry():
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
        "adaboost": {
            "estimator": AdaBoostClassifier(
                estimator=DecisionTreeClassifier(
                    max_depth=2,
                    min_samples_leaf=2,
                    random_state=RANDOM_STATE,
                ),
                n_estimators=100,
                learning_rate=0.5,
                random_state=RANDOM_STATE,
            ),
            "scale_numeric": False,
        },
    }


def predict_score(pipe: Pipeline, X: pd.DataFrame) -> np.ndarray:
    if hasattr(pipe, "predict_proba"):
        return pipe.predict_proba(X)[:, 1]
    if hasattr(pipe, "decision_function"):
        return np.asarray(pipe.decision_function(X), dtype=float)
    return pipe.predict(X).astype(float)


def classification_metrics(y_true, y_pred, y_score):
    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[0, 1]
    ).ravel()

    fpr = fp / (fp + tn) if (fp + tn) else np.nan
    fnr = fn / (fn + tp) if (fn + tp) else np.nan

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall_detection_rate": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "roc_auc": float(roc_auc_score(y_true, y_score)),
        "pr_auc": float(average_precision_score(y_true, y_score)),
        "false_positive_rate": float(fpr),
        "false_negative_rate": float(fnr),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def safe_corr(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def pairwise_diversity(y_true, pred_a, pred_b, prob_a, prob_b):
    correct_a = pred_a == y_true
    correct_b = pred_b == y_true

    error_a = (~correct_a).astype(int)
    error_b = (~correct_b).astype(int)

    n11 = int(np.sum(correct_a & correct_b))
    n00 = int(np.sum((~correct_a) & (~correct_b)))
    n10 = int(np.sum(correct_a & (~correct_b)))
    n01 = int(np.sum((~correct_a) & correct_b))

    total = len(y_true)

    disagreement = (n10 + n01) / total
    double_fault = n00 / total

    denominator = n11 * n00 + n10 * n01
    q_statistic = (
        np.nan if denominator == 0
        else (n11 * n00 - n10 * n01) / denominator
    )

    return {
        "n_both_correct": n11,
        "n_both_wrong": n00,
        "n_a_correct_b_wrong": n10,
        "n_a_wrong_b_correct": n01,
        "disagreement_rate": float(disagreement),
        "double_fault_rate": float(double_fault),
        "pairwise_oracle_accuracy": float(1.0 - double_fault),
        "q_statistic": float(q_statistic) if not np.isnan(q_statistic) else np.nan,
        "error_correlation": safe_corr(error_a, error_b),
        "probability_correlation": safe_corr(prob_a, prob_b),
    }


def generate_oof(train, features, track_name):
    X = train[features]
    y = train[TARGET_COL].to_numpy()

    cv = StratifiedKFold(
        n_splits=CV_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    models = model_registry()

    oof = pd.DataFrame({
        "row_index": np.arange(len(train)),
        "id": train[ID_COL].to_numpy(),
        "attack_cat": train[ATTACK_COL].astype(str).to_numpy(),
        "y_true": y,
        "fold": np.zeros(len(train), dtype=int),
    })

    for model_name in models:
        oof[f"{model_name}_pred"] = -1
        oof[f"{model_name}_prob"] = np.nan

    runtime_rows = []

    print(
        f"\n[TRACK] {track_name} "
        f"({len(features)} original features)"
    )

    for fold, (train_idx, valid_idx) in enumerate(
        cv.split(X, y),
        start=1,
    ):
        oof.loc[valid_idx, "fold"] = fold

        X_train = X.iloc[train_idx]
        X_valid = X.iloc[valid_idx]
        y_train = y[train_idx]

        print(
            f"  [FOLD {fold}/{CV_SPLITS}] "
            f"train={len(train_idx):,}, valid={len(valid_idx):,}"
        )

        for model_name, cfg in models.items():
            prep = build_preprocessor(
                features,
                scale_numeric=cfg["scale_numeric"],
            )

            pipe = Pipeline([
                ("preprocess", prep),
                ("model", clone(cfg["estimator"])),
            ])

            fit_start = time.perf_counter()
            pipe.fit(X_train, y_train)
            fit_seconds = time.perf_counter() - fit_start

            pred_start = time.perf_counter()
            pred = pipe.predict(X_valid)
            prob = predict_score(pipe, X_valid)
            pred_seconds = time.perf_counter() - pred_start

            oof.loc[valid_idx, f"{model_name}_pred"] = pred.astype(int)
            oof.loc[valid_idx, f"{model_name}_prob"] = prob.astype(float)

            runtime_rows.append({
                "feature_track": track_name,
                "fold": fold,
                "model": model_name,
                "train_rows": len(train_idx),
                "validation_rows": len(valid_idx),
                "train_time_seconds": fit_seconds,
                "inference_time_seconds": pred_seconds,
                "inference_ms_per_sample": (
                    pred_seconds / len(valid_idx) * 1000
                ),
            })

            print(
                f"    {model_name}: "
                f"train={fit_seconds:.2f}s, infer={pred_seconds:.2f}s"
            )

    return oof, pd.DataFrame(runtime_rows)


def summarize_individual_models(oof, runtime, track_name):
    rows = []

    for model_name in model_registry():
        pred = oof[f"{model_name}_pred"].to_numpy(dtype=int)
        prob = oof[f"{model_name}_prob"].to_numpy(dtype=float)
        y = oof["y_true"].to_numpy(dtype=int)

        metrics = classification_metrics(y, pred, prob)
        rt = runtime[runtime["model"] == model_name]

        rows.append({
            "feature_track": track_name,
            "model": model_name,
            **metrics,
            "mean_train_time_seconds": float(rt["train_time_seconds"].mean()),
            "total_cv_train_time_seconds": float(rt["train_time_seconds"].sum()),
            "mean_inference_ms_per_sample": float(
                rt["inference_ms_per_sample"].mean()
            ),
        })

    return pd.DataFrame(rows)


def summarize_diversity(oof, track_name):
    rows = []
    models = list(model_registry().keys())
    y = oof["y_true"].to_numpy(dtype=int)

    for model_a, model_b in combinations(models, 2):
        values = pairwise_diversity(
            y,
            oof[f"{model_a}_pred"].to_numpy(dtype=int),
            oof[f"{model_b}_pred"].to_numpy(dtype=int),
            oof[f"{model_a}_prob"].to_numpy(dtype=float),
            oof[f"{model_b}_prob"].to_numpy(dtype=float),
        )

        rows.append({
            "feature_track": track_name,
            "model_a": model_a,
            "model_b": model_b,
            **values,
        })

    return pd.DataFrame(rows)


def build_attack_error_profile(oof, track_name):
    attacks = oof[oof["y_true"] == 1].copy()
    rows = []

    for attack, group in attacks.groupby("attack_cat"):
        row = {
            "feature_track": track_name,
            "attack_cat": attack,
            "attack_rows": len(group),
        }

        for model_name in model_registry():
            false_negatives = int(
                (group[f"{model_name}_pred"] == 0).sum()
            )

            row[f"{model_name}_false_negatives"] = false_negatives
            row[f"{model_name}_miss_rate"] = (
                false_negatives / len(group)
                if len(group)
                else np.nan
            )

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    OOF_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("PHASE 7.1 — OOF BASE-LEARNER DIVERSITY ANALYSIS")
    print("TRAIN ONLY — OFFICIAL TEST IS NOT LOADED")
    print("=" * 80)

    train = load_train()
    tracks = load_feature_tracks(train)

    all_individual = []
    all_diversity = []
    all_runtime = []
    all_attack_profiles = []

    for track_name in FEATURE_TRACKS:
        features = tracks[track_name]

        oof, runtime = generate_oof(
            train,
            features,
            track_name,
        )

        individual = summarize_individual_models(
            oof,
            runtime,
            track_name,
        )

        diversity = summarize_diversity(
            oof,
            track_name,
        )

        attack_profile = build_attack_error_profile(
            oof,
            track_name,
        )

        oof.to_csv(
            OOF_DIR / f"{track_name}_oof_predictions.csv",
            index=False,
        )

        all_individual.append(individual)
        all_diversity.append(diversity)
        all_runtime.append(runtime)
        all_attack_profiles.append(attack_profile)

    individual_df = pd.concat(all_individual, ignore_index=True)
    diversity_df = pd.concat(all_diversity, ignore_index=True)
    runtime_df = pd.concat(all_runtime, ignore_index=True)
    attack_df = pd.concat(all_attack_profiles, ignore_index=True)

    individual_df.to_csv(
        TABLE_DIR / "individual_oof_metrics.csv",
        index=False,
    )
    diversity_df.to_csv(
        TABLE_DIR / "pairwise_diversity.csv",
        index=False,
    )
    runtime_df.to_csv(
        TABLE_DIR / "fold_runtime.csv",
        index=False,
    )
    attack_df.to_csv(
        TABLE_DIR / "attack_category_miss_profile.csv",
        index=False,
    )

    metadata = {
        "phase": "7.1",
        "dataset": "UNSW-NB15",
        "official_test_loaded": False,
        "cv_splits": CV_SPLITS,
        "random_state": RANDOM_STATE,
        "models": list(model_registry().keys()),
        "feature_tracks": {
            name: {
                "count": len(features),
                "features": features,
            }
            for name, features in tracks.items()
        },
        "note": (
            "Diversity is interpreted together with model strength and cost."
        ),
    }

    (OUT_DIR / "experiment_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "PHASE 7.1 — OOF DIVERSITY SUMMARY",
        "=" * 80,
        "",
        "IMPORTANT:",
        "- Official TEST was not loaded.",
        "- Each OOF prediction comes from a model that did not train on that row.",
        "- Diversity alone is not enough to select an ensemble member.",
        "",
        "INDIVIDUAL OOF PERFORMANCE",
    ]

    for _, row in individual_df.sort_values(
        ["feature_track", "macro_f1"],
        ascending=[True, False],
    ).iterrows():
        lines.append(
            f"- {row['feature_track']} / {row['model']}: "
            f"Macro-F1={row['macro_f1']:.4f}, "
            f"MCC={row['mcc']:.4f}, "
            f"FPR={row['false_positive_rate']:.4f}, "
            f"FNR={row['false_negative_rate']:.4f}"
        )

    lines.extend(["", "PAIRWISE DIVERSITY"])

    for _, row in diversity_df.sort_values(
        ["feature_track", "double_fault_rate", "disagreement_rate"],
        ascending=[True, True, False],
    ).iterrows():
        lines.append(
            f"- {row['feature_track']} / "
            f"{row['model_a']} + {row['model_b']}: "
            f"disagree={row['disagreement_rate']:.4f}, "
            f"double-fault={row['double_fault_rate']:.4f}, "
            f"oracle={row['pairwise_oracle_accuracy']:.4f}, "
            f"Q={row['q_statistic']:.4f}, "
            f"error-corr={row['error_correlation']:.4f}"
        )

    lines.extend([
        "",
        "NEXT:",
        "Use strength + diversity + cost together to define justified",
        "Voting/Stacking configurations for Phase 7.2.",
    ])

    report = "\n".join(lines)

    (OUT_DIR / "phase7_1_summary.txt").write_text(
        report,
        encoding="utf-8",
    )

    print()
    print(report)
    print()
    print(f"[OUTPUT] {OUT_DIR}")
    print("[DONE] Phase 7.1 diversity analysis completed.")


if __name__ == "__main__":
    main()
