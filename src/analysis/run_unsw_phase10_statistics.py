"""
PHASE 10 — UNSW-NB15 Statistical + Final Error Analysis
========================================================

Purpose
-------
Analyze the already-saved Phase-9 official-test predictions.

NO model is trained in this phase.
NO hyperparameter, feature, threshold, or candidate is changed.

Inputs
------
results/final_evaluation/unsw_nb15/phase9_holdout/tables/
    official_test_predictions.csv
    cost_metrics.csv

Analyses
--------
1. Stratified paired bootstrap confidence intervals:
   - Macro-F1
   - MCC
   - FPR
   - FNR
2. Paired bootstrap differences between frozen pipelines.
3. Exact McNemar tests on paired correctness.
4. Holm correction across the three pairwise McNemar tests per evaluation view.
5. Wilson confidence intervals for per-attack miss rates.
6. Descriptive official-test vs novel-vector degradation.
7. Performance-cost trade-off table.

Statistical scope
-----------------
Bootstrap intervals quantify uncertainty conditional on the benchmark rows.
They do not prove independence of network flows and should not be interpreted
as population-level guarantees beyond the benchmark distribution.

McNemar tests overall paired correctness (error rate), NOT Macro-F1 or MCC.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

RANDOM_SEED = 20260928
N_BOOTSTRAP = 10_000
ALPHA = 0.05

TARGET_COL = "label"
ATTACK_COL = "attack_cat"
NOVEL_COL = "is_novel_vector"

# Order chosen so the first key comparison is Stacking - RF42.
MODEL_NAMES = [
    "stacking_42",
    "random_forest_42",
    "random_forest_17",
]

EVAL_VIEWS = [
    "official_test",
    "novel_vector_test",
]

BOOT_METRICS = [
    "macro_f1",
    "mcc",
    "false_positive_rate",
    "false_negative_rate",
]


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[2]

PHASE9_DIR = (
    PROJECT_ROOT
    / "results"
    / "final_evaluation"
    / "unsw_nb15"
    / "phase9_holdout"
)

PRED_FILE = (
    PHASE9_DIR
    / "tables"
    / "official_test_predictions.csv"
)

COST_FILE = (
    PHASE9_DIR
    / "tables"
    / "cost_metrics.csv"
)

OUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "final_analysis"
    / "unsw_nb15"
    / "phase10_statistics"
)

TABLE_DIR = OUT_DIR / "tables"


# ---------------------------------------------------------------------
# Core statistical helpers
# ---------------------------------------------------------------------

def safe_div(
    numerator,
    denominator,
):
    numerator = np.asarray(
        numerator,
        dtype=float,
    )
    denominator = np.asarray(
        denominator,
        dtype=float,
    )

    return np.divide(
        numerator,
        denominator,
        out=np.full_like(
            numerator,
            np.nan,
            dtype=float,
        ),
        where=denominator != 0,
    )


def binary_metrics_from_counts(
    tn,
    fp,
    fn,
    tp,
) -> dict:
    """
    Binary metrics from confusion counts.

    Works with scalars or numpy arrays.
    """
    tn = np.asarray(tn, dtype=float)
    fp = np.asarray(fp, dtype=float)
    fn = np.asarray(fn, dtype=float)
    tp = np.asarray(tp, dtype=float)

    total = tn + fp + fn + tp

    accuracy = safe_div(
        tn + tp,
        total,
    )

    recall_pos = safe_div(
        tp,
        tp + fn,
    )
    recall_neg = safe_div(
        tn,
        tn + fp,
    )

    balanced_accuracy = (
        recall_pos + recall_neg
    ) / 2.0

    precision = safe_div(
        tp,
        tp + fp,
    )

    f1_pos = safe_div(
        2 * tp,
        2 * tp + fp + fn,
    )

    f1_neg = safe_div(
        2 * tn,
        2 * tn + fp + fn,
    )

    macro_f1 = (
        f1_pos + f1_neg
    ) / 2.0

    mcc_den = np.sqrt(
        (tp + fp)
        * (tp + fn)
        * (tn + fp)
        * (tn + fn)
    )

    mcc = safe_div(
        tp * tn - fp * fn,
        mcc_den,
    )

    fpr = safe_div(
        fp,
        fp + tn,
    )

    fnr = safe_div(
        fn,
        fn + tp,
    )

    values = {
        "accuracy": accuracy,
        "balanced_accuracy": balanced_accuracy,
        "precision": precision,
        "recall_detection_rate": recall_pos,
        "f1": f1_pos,
        "macro_f1": macro_f1,
        "mcc": mcc,
        "false_positive_rate": fpr,
        "false_negative_rate": fnr,
    }

    # Return ordinary floats for scalar inputs.
    return {
        k: (
            float(v)
            if np.ndim(v) == 0
            else v
        )
        for k, v in values.items()
    }


def mcnemar_exact(
    a_wrong_b_correct: int,
    a_correct_b_wrong: int,
) -> float:
    """
    Exact two-sided McNemar p-value using the binomial formulation.
    """
    b = int(
        a_wrong_b_correct
    )
    c = int(
        a_correct_b_wrong
    )

    n = b + c

    if n == 0:
        return 1.0

    return float(
        binomtest(
            k=min(b, c),
            n=n,
            p=0.5,
            alternative="two-sided",
        ).pvalue
    )


def holm_adjust(
    p_values,
) -> np.ndarray:
    """
    Holm step-down family-wise error correction.
    """
    p = np.asarray(
        p_values,
        dtype=float,
    )

    m = len(p)

    if m == 0:
        return np.array(
            [],
            dtype=float,
        )

    order = np.argsort(p)
    sorted_p = p[order]

    adjusted_sorted = np.empty(
        m,
        dtype=float,
    )

    running_max = 0.0

    for i, value in enumerate(
        sorted_p
    ):
        multiplier = m - i
        raw = min(
            1.0,
            multiplier * value,
        )
        running_max = max(
            running_max,
            raw,
        )
        adjusted_sorted[i] = (
            running_max
        )

    adjusted = np.empty(
        m,
        dtype=float,
    )

    adjusted[order] = (
        adjusted_sorted
    )

    return adjusted


def wilson_interval(
    successes: int,
    total: int,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    """
    Wilson score interval for a binomial proportion.
    """
    if total <= 0:
        return (
            np.nan,
            np.nan,
        )

    p = successes / total
    z2 = z ** 2

    denom = (
        1.0 + z2 / total
    )

    center = (
        p
        + z2
        / (2.0 * total)
    ) / denom

    half = (
        z
        * np.sqrt(
            (
                p * (1.0 - p)
                + z2 / (4.0 * total)
            )
            / total
        )
        / denom
    )

    return (
        float(
            max(
                0.0,
                center - half,
            )
        ),
        float(
            min(
                1.0,
                center + half,
            )
        ),
    )


# ---------------------------------------------------------------------
# Loading / validation
# ---------------------------------------------------------------------

def require_file(
    path: Path,
):
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )


def load_predictions() -> pd.DataFrame:
    require_file(
        PRED_FILE
    )

    df = pd.read_csv(
        PRED_FILE,
        low_memory=False,
    )

    required = {
        TARGET_COL,
        ATTACK_COL,
        NOVEL_COL,
    }

    for model in MODEL_NAMES:
        required.add(
            f"{model}_pred"
        )
        required.add(
            f"{model}_prob"
        )

    missing = sorted(
        required - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Prediction file missing columns: {missing}"
        )

    return df


def get_view_mask(
    df: pd.DataFrame,
    eval_view: str,
) -> np.ndarray:
    if eval_view == "official_test":
        return np.ones(
            len(df),
            dtype=bool,
        )

    if eval_view == "novel_vector_test":
        return df[
            NOVEL_COL
        ].astype(
            bool
        ).to_numpy()

    raise ValueError(
        f"Unknown eval view: {eval_view}"
    )


# ---------------------------------------------------------------------
# Confusion counts / point metrics
# ---------------------------------------------------------------------

def confusion_counts(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> tuple[int, int, int, int]:
    y_true = np.asarray(
        y_true,
        dtype=int,
    )
    y_pred = np.asarray(
        y_pred,
        dtype=int,
    )

    tn = int(
        np.sum(
            (y_true == 0)
            & (y_pred == 0)
        )
    )
    fp = int(
        np.sum(
            (y_true == 0)
            & (y_pred == 1)
        )
    )
    fn = int(
        np.sum(
            (y_true == 1)
            & (y_pred == 0)
        )
    )
    tp = int(
        np.sum(
            (y_true == 1)
            & (y_pred == 1)
        )
    )

    return (
        tn,
        fp,
        fn,
        tp,
    )


def point_metric_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for view in EVAL_VIEWS:
        mask = get_view_mask(
            df,
            view,
        )

        y = df.loc[
            mask,
            TARGET_COL,
        ].to_numpy(
            dtype=int
        )

        for model in MODEL_NAMES:
            pred = df.loc[
                mask,
                f"{model}_pred",
            ].to_numpy(
                dtype=int
            )

            tn, fp, fn, tp = (
                confusion_counts(
                    y,
                    pred,
                )
            )

            metrics = (
                binary_metrics_from_counts(
                    tn,
                    fp,
                    fn,
                    tp,
                )
            )

            rows.append({
                "eval_view": view,
                "pipeline": model,
                "n_rows": int(
                    len(y)
                ),
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
                **metrics,
            })

    return pd.DataFrame(
        rows
    )


# ---------------------------------------------------------------------
# Efficient stratified paired bootstrap
# ---------------------------------------------------------------------

def _prediction_pattern_counts(
    frame: pd.DataFrame,
    true_label: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    int,
]:
    """
    Count the joint three-model prediction patterns within one true-label stratum.

    There are at most 2^3 = 8 patterns, making 10,000 paired bootstrap
    replicates very cheap.
    """
    sub = frame[
        frame[
            TARGET_COL
        ] == true_label
    ]

    pred_cols = [
        f"{m}_pred"
        for m in MODEL_NAMES
    ]

    grouped = (
        sub.groupby(
            pred_cols,
            dropna=False,
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    patterns = grouped[
        pred_cols
    ].to_numpy(
        dtype=int
    )

    counts = grouped[
        "count"
    ].to_numpy(
        dtype=int
    )

    total = int(
        counts.sum()
    )

    probabilities = (
        counts / total
    )

    return (
        patterns,
        probabilities,
        total,
    )


def bootstrap_metric_arrays(
    frame: pd.DataFrame,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> dict[str, dict[str, np.ndarray]]:
    """
    Stratified paired bootstrap conditional on observed Normal/Attack counts.

    The same resampled joint prediction patterns are used for every model,
    preserving pairwise dependence among model outputs.
    """
    (
        patterns0,
        probs0,
        n0,
    ) = _prediction_pattern_counts(
        frame,
        0,
    )

    (
        patterns1,
        probs1,
        n1,
    ) = _prediction_pattern_counts(
        frame,
        1,
    )

    draw0 = rng.multinomial(
        n=n0,
        pvals=probs0,
        size=n_bootstrap,
    )

    draw1 = rng.multinomial(
        n=n1,
        pvals=probs1,
        size=n_bootstrap,
    )

    out = {}

    for j, model in enumerate(
        MODEL_NAMES
    ):
        pred0 = patterns0[
            :,
            j,
        ]
        pred1 = patterns1[
            :,
            j,
        ]

        tn = draw0[
            :,
            pred0 == 0,
        ].sum(
            axis=1
        )
        fp = draw0[
            :,
            pred0 == 1,
        ].sum(
            axis=1
        )
        fn = draw1[
            :,
            pred1 == 0,
        ].sum(
            axis=1
        )
        tp = draw1[
            :,
            pred1 == 1,
        ].sum(
            axis=1
        )

        out[
            model
        ] = binary_metrics_from_counts(
            tn,
            fp,
            fn,
            tp,
        )

    return out


def percentile_ci(
    values: np.ndarray,
    alpha: float = ALPHA,
) -> tuple[float, float]:
    low = 100.0 * (
        alpha / 2.0
    )
    high = 100.0 * (
        1.0
        - alpha / 2.0
    )

    return (
        float(
            np.nanpercentile(
                values,
                low,
            )
        ),
        float(
            np.nanpercentile(
                values,
                high,
            )
        ),
    )


def bootstrap_tables(
    df: pd.DataFrame,
    point_df: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
]:
    ci_rows = []
    delta_rows = []

    for view_idx, view in enumerate(
        EVAL_VIEWS
    ):
        mask = get_view_mask(
            df,
            view,
        )

        frame = df.loc[
            mask
        ].copy()

        rng = np.random.default_rng(
            RANDOM_SEED
            + view_idx
        )

        boot = bootstrap_metric_arrays(
            frame,
            n_bootstrap=N_BOOTSTRAP,
            rng=rng,
        )

        # Individual model CIs.
        for model in MODEL_NAMES:
            point_row = point_df[
                (
                    point_df[
                        "eval_view"
                    ] == view
                )
                & (
                    point_df[
                        "pipeline"
                    ] == model
                )
            ].iloc[0]

            for metric in BOOT_METRICS:
                values = boot[
                    model
                ][
                    metric
                ]

                lo, hi = percentile_ci(
                    values
                )

                ci_rows.append({
                    "eval_view": view,
                    "pipeline": model,
                    "metric": metric,
                    "point_estimate": float(
                        point_row[
                            metric
                        ]
                    ),
                    "ci_level": (
                        1.0 - ALPHA
                    ),
                    "ci_lower": lo,
                    "ci_upper": hi,
                    "bootstrap_replicates": (
                        N_BOOTSTRAP
                    ),
                    "bootstrap_type": (
                        "stratified paired multinomial "
                        "bootstrap over joint prediction patterns"
                    ),
                })

        # Pairwise metric-difference CIs.
        for model_a, model_b in combinations(
            MODEL_NAMES,
            2,
        ):
            point_a = point_df[
                (
                    point_df[
                        "eval_view"
                    ] == view
                )
                & (
                    point_df[
                        "pipeline"
                    ] == model_a
                )
            ].iloc[0]

            point_b = point_df[
                (
                    point_df[
                        "eval_view"
                    ] == view
                )
                & (
                    point_df[
                        "pipeline"
                    ] == model_b
                )
            ].iloc[0]

            for metric in BOOT_METRICS:
                diff = (
                    boot[
                        model_a
                    ][
                        metric
                    ]
                    - boot[
                        model_b
                    ][
                        metric
                    ]
                )

                lo, hi = percentile_ci(
                    diff
                )

                point_delta = float(
                    point_a[
                        metric
                    ]
                    - point_b[
                        metric
                    ]
                )

                delta_rows.append({
                    "eval_view": view,
                    "model_a": model_a,
                    "model_b": model_b,
                    "metric": metric,
                    "delta_a_minus_b": (
                        point_delta
                    ),
                    "ci_level": (
                        1.0 - ALPHA
                    ),
                    "ci_lower": lo,
                    "ci_upper": hi,
                    "ci_excludes_zero": bool(
                        (
                            lo > 0
                        )
                        or (
                            hi < 0
                        )
                    ),
                    "bootstrap_replicates": (
                        N_BOOTSTRAP
                    ),
                })

    return (
        pd.DataFrame(
            ci_rows
        ),
        pd.DataFrame(
            delta_rows
        ),
    )


# ---------------------------------------------------------------------
# McNemar + Holm
# ---------------------------------------------------------------------

def mcnemar_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    all_rows = []

    for view in EVAL_VIEWS:
        mask = get_view_mask(
            df,
            view,
        )

        frame = df.loc[
            mask
        ]

        y = frame[
            TARGET_COL
        ].to_numpy(
            dtype=int
        )

        rows = []

        for model_a, model_b in combinations(
            MODEL_NAMES,
            2,
        ):
            pred_a = frame[
                f"{model_a}_pred"
            ].to_numpy(
                dtype=int
            )

            pred_b = frame[
                f"{model_b}_pred"
            ].to_numpy(
                dtype=int
            )

            err_a = (
                pred_a != y
            )
            err_b = (
                pred_b != y
            )

            a_wrong_b_correct = int(
                np.sum(
                    err_a
                    & (~err_b)
                )
            )

            a_correct_b_wrong = int(
                np.sum(
                    (~err_a)
                    & err_b
                )
            )

            p = mcnemar_exact(
                a_wrong_b_correct,
                a_correct_b_wrong,
            )

            rows.append({
                "eval_view": view,
                "model_a": model_a,
                "model_b": model_b,
                "a_wrong_b_correct": (
                    a_wrong_b_correct
                ),
                "a_correct_b_wrong": (
                    a_correct_b_wrong
                ),
                "discordant_total": (
                    a_wrong_b_correct
                    + a_correct_b_wrong
                ),
                "p_exact_raw": p,
            })

        adjusted = holm_adjust(
            [
                row[
                    "p_exact_raw"
                ]
                for row in rows
            ]
        )

        for row, p_adj in zip(
            rows,
            adjusted,
        ):
            row[
                "p_holm"
            ] = float(
                p_adj
            )

            row[
                "reject_h0_alpha_0_05"
            ] = bool(
                p_adj < ALPHA
            )

            row[
                "test_scope"
            ] = (
                "paired overall correctness / error rate"
            )

        all_rows.extend(
            rows
        )

    return pd.DataFrame(
        all_rows
    )


# ---------------------------------------------------------------------
# Attack-family miss-rate uncertainty
# ---------------------------------------------------------------------

def attack_family_table(
    df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for view in EVAL_VIEWS:
        mask = get_view_mask(
            df,
            view,
        )

        frame = df.loc[
            mask
        ]

        attacks = frame[
            frame[
                TARGET_COL
            ] == 1
        ]

        for (
            attack_cat,
            group,
        ) in attacks.groupby(
            ATTACK_COL
        ):
            n = int(
                len(group)
            )

            for model in MODEL_NAMES:
                misses = int(
                    (
                        group[
                            f"{model}_pred"
                        ] == 0
                    ).sum()
                )

                rate = (
                    misses / n
                    if n
                    else np.nan
                )

                lo, hi = wilson_interval(
                    misses,
                    n,
                )

                rows.append({
                    "eval_view": view,
                    "attack_cat": str(
                        attack_cat
                    ),
                    "pipeline": model,
                    "attack_rows": n,
                    "false_negatives": (
                        misses
                    ),
                    "miss_rate": float(
                        rate
                    ),
                    "wilson_95_lower": (
                        lo
                    ),
                    "wilson_95_upper": (
                        hi
                    ),
                })

    return pd.DataFrame(
        rows
    )


# ---------------------------------------------------------------------
# Descriptive view degradation and cost trade-off
# ---------------------------------------------------------------------

def view_degradation_table(
    point_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    metrics = [
        "macro_f1",
        "mcc",
        "false_positive_rate",
        "false_negative_rate",
    ]

    for model in MODEL_NAMES:
        official = point_df[
            (
                point_df[
                    "eval_view"
                ] == "official_test"
            )
            & (
                point_df[
                    "pipeline"
                ] == model
            )
        ].iloc[0]

        novel = point_df[
            (
                point_df[
                    "eval_view"
                ] == "novel_vector_test"
            )
            & (
                point_df[
                    "pipeline"
                ] == model
            )
        ].iloc[0]

        row = {
            "pipeline": model,
            "official_rows": int(
                official[
                    "n_rows"
                ]
            ),
            "novel_rows": int(
                novel[
                    "n_rows"
                ]
            ),
        }

        for metric in metrics:
            row[
                f"official_{metric}"
            ] = float(
                official[
                    metric
                ]
            )

            row[
                f"novel_{metric}"
            ] = float(
                novel[
                    metric
                ]
            )

            row[
                f"delta_novel_minus_official_{metric}"
            ] = float(
                novel[
                    metric
                ]
                - official[
                    metric
                ]
            )

        rows.append(
            row
        )

    return pd.DataFrame(
        rows
    )


def performance_cost_table(
    point_df: pd.DataFrame,
) -> pd.DataFrame:
    require_file(
        COST_FILE
    )

    cost = pd.read_csv(
        COST_FILE
    )

    official = point_df[
        point_df[
            "eval_view"
        ] == "official_test"
    ][
        [
            "pipeline",
            "macro_f1",
            "mcc",
            "false_positive_rate",
            "false_negative_rate",
        ]
    ]

    return official.merge(
        cost,
        on="pipeline",
        how="left",
        validate="one_to_one",
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 86)
    print(
        "PHASE 10 — STATISTICAL + FINAL ERROR ANALYSIS"
    )
    print(
        "NO MODEL TRAINING — SAVED PHASE-9 PREDICTIONS ONLY"
    )
    print("=" * 86)

    df = load_predictions()

    print(
        f"[INPUT] official-test prediction rows: "
        f"{len(df):,}"
    )

    print(
        f"[INPUT] novel-vector rows: "
        f"{int(df[NOVEL_COL].astype(bool).sum()):,}"
    )

    point_df = point_metric_table(
        df
    )

    print(
        f"[BOOTSTRAP] {N_BOOTSTRAP:,} "
        "paired stratified replicates per view..."
    )

    ci_df, delta_df = (
        bootstrap_tables(
            df,
            point_df,
        )
    )

    print(
        "[MCNEMAR] exact paired tests + Holm correction..."
    )

    mcnemar_df = (
        mcnemar_table(
            df
        )
    )

    attack_df = (
        attack_family_table(
            df
        )
    )

    degradation_df = (
        view_degradation_table(
            point_df
        )
    )

    tradeoff_df = (
        performance_cost_table(
            point_df
        )
    )

    # --------------------------------------------------------------
    # Save tables
    # --------------------------------------------------------------

    point_df.to_csv(
        TABLE_DIR
        / "recomputed_point_metrics.csv",
        index=False,
    )

    ci_df.to_csv(
        TABLE_DIR
        / "bootstrap_metric_ci.csv",
        index=False,
    )

    delta_df.to_csv(
        TABLE_DIR
        / "paired_bootstrap_differences.csv",
        index=False,
    )

    mcnemar_df.to_csv(
        TABLE_DIR
        / "mcnemar_holm.csv",
        index=False,
    )

    attack_df.to_csv(
        TABLE_DIR
        / "attack_family_miss_rate_ci.csv",
        index=False,
    )

    degradation_df.to_csv(
        TABLE_DIR
        / "official_vs_novel_degradation.csv",
        index=False,
    )

    tradeoff_df.to_csv(
        TABLE_DIR
        / "performance_cost_tradeoff.csv",
        index=False,
    )

    metadata = {
        "phase": 10,
        "dataset": "UNSW-NB15",
        "model_training_performed": False,
        "source_predictions": str(
            PRED_FILE
        ),
        "models": MODEL_NAMES,
        "evaluation_views": (
            EVAL_VIEWS
        ),
        "bootstrap": {
            "replicates": N_BOOTSTRAP,
            "random_seed": RANDOM_SEED,
            "confidence_level": (
                1.0 - ALPHA
            ),
            "type": (
                "stratified paired multinomial bootstrap "
                "over joint prediction patterns"
            ),
            "metrics": (
                BOOT_METRICS
            ),
            "interpretation": (
                "Uncertainty conditional on benchmark rows; "
                "does not establish independent network-flow sampling."
            ),
        },
        "mcnemar": {
            "variant": (
                "exact two-sided binomial"
            ),
            "familywise_correction": (
                "Holm"
            ),
            "alpha": ALPHA,
            "scope": (
                "overall paired correctness/error rate only"
            ),
        },
        "attack_family_ci": (
            "Wilson 95% interval for miss rate"
        ),
        "post_test_rule": (
            "No model, feature, threshold, or hyperparameter "
            "changes are permitted based on Phase-10 findings."
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

    # --------------------------------------------------------------
    # Human-readable summary
    # --------------------------------------------------------------

    key_pair = delta_df[
        (
            delta_df[
                "eval_view"
            ] == "official_test"
        )
        & (
            delta_df[
                "model_a"
            ] == "stacking_42"
        )
        & (
            delta_df[
                "model_b"
            ] == "random_forest_42"
        )
    ]

    key_mcnemar = mcnemar_df[
        (
            mcnemar_df[
                "eval_view"
            ] == "official_test"
        )
        & (
            mcnemar_df[
                "model_a"
            ] == "stacking_42"
        )
        & (
            mcnemar_df[
                "model_b"
            ] == "random_forest_42"
        )
    ].iloc[0]

    lines = [
        "PHASE 10 — STATISTICAL + FINAL ERROR ANALYSIS",
        "=" * 86,
        "",
        "IMPORTANT:",
        "- No model training was performed.",
        "- All analyses use the frozen Phase-9 predictions.",
        "- McNemar evaluates paired correctness, not Macro-F1/MCC.",
        "- Bootstrap CIs quantify benchmark-sample uncertainty and do not",
        "  eliminate possible dependence among network flows.",
        "",
        "KEY OFFICIAL-TEST COMPARISON: STACKING-42 MINUS RF-42",
    ]

    for _, row in key_pair.iterrows():
        lines.append(
            f"- {row['metric']}: "
            f"delta={row['delta_a_minus_b']:+.6f}, "
            f"95% CI=[{row['ci_lower']:+.6f}, "
            f"{row['ci_upper']:+.6f}]"
        )

    lines.extend([
        "",
        "MCNEMAR: STACKING-42 VS RF-42",
        (
            f"- Stacking wrong / RF correct: "
            f"{int(key_mcnemar['a_wrong_b_correct']):,}"
        ),
        (
            f"- Stacking correct / RF wrong: "
            f"{int(key_mcnemar['a_correct_b_wrong']):,}"
        ),
        (
            f"- Exact raw p="
            f"{key_mcnemar['p_exact_raw']:.6g}"
        ),
        (
            f"- Holm-adjusted p="
            f"{key_mcnemar['p_holm']:.6g}"
        ),
        (
            "- Reject equal-error-rate null at alpha=.05: "
            f"{bool(key_mcnemar['reject_h0_alpha_0_05'])}"
        ),
        "",
        "OUTPUT TABLES:",
        "- recomputed_point_metrics.csv",
        "- bootstrap_metric_ci.csv",
        "- paired_bootstrap_differences.csv",
        "- mcnemar_holm.csv",
        "- attack_family_miss_rate_ci.csv",
        "- official_vs_novel_degradation.csv",
        "- performance_cost_tradeoff.csv",
        "",
        "NEXT:",
        "Interpret these statistical estimates together with Phase-9 cost and",
        "attack-family evidence, then answer the frozen research questions.",
    ])

    report = "\n".join(
        lines
    )

    (
        OUT_DIR
        / "phase10_summary.txt"
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
        "[DONE] Phase 10 statistical analysis completed."
    )


if __name__ == "__main__":
    main()
