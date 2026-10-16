"""
PHASE 4 — UNSW-NB15 Exploratory Data Analysis
==============================================

Purpose
-------
Create a small set of scientifically useful EDA outputs for UNSW-NB15.

Important methodological rules
------------------------------
1. Raw files are NEVER modified.
2. Target-related exploratory analysis is performed on TRAIN only.
3. TEST is used only for descriptive class-distribution comparison.
4. EDA does NOT perform feature selection.
5. No model is trained here.

Expected project structure
--------------------------
NCKH/
├── data/
│   ├── raw/unsw-nb15/
│   │   ├── UNSW_NB15_training-set.csv
│   │   └── UNSW_NB15_testing-set.csv
│   └── interim/unsw-nb15/
│       └── test_unseen_vectors.csv
├── results/
└── src/data/
    └── eda_unsw_nb15.py

Outputs
-------
results/eda/unsw_nb15/
    tables/
    figures/
    eda_summary.txt
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "unsw-nb15"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "unsw-nb15"

TRAIN_FILE = RAW_DIR / "UNSW_NB15_training-set.csv"
TEST_FILE = RAW_DIR / "UNSW_NB15_testing-set.csv"
NOVEL_TEST_FILE = INTERIM_DIR / "test_unseen_vectors.csv"

OUT_DIR = PROJECT_ROOT / "results" / "eda" / "unsw_nb15"
TABLE_DIR = OUT_DIR / "tables"
FIG_DIR = OUT_DIR / "figures"

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"
CATEGORICAL_EXPECTED = ["proto", "service", "state"]

# Correlation/report thresholds are descriptive flags only.
HIGH_CORRELATION_THRESHOLD = 0.90
TOP_N_CORR_FEATURES = 15
TOP_N_EFFECT_FEATURES = 15


# ---------------------------------------------------------------------
# Figure defaults
# ---------------------------------------------------------------------

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "font.size": 9,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})


def save_figure(fig: plt.Figure, stem: str) -> None:
    """
    Save a single-panel EDA figure.
    Publication-grade QA is intentionally deferred to Phase 16.
    """
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def require(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def read_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    return df


# ---------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------

def build_class_distribution(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, df in [("Train", train), ("Test", test)]:
        counts = df[TARGET_COL].value_counts().sort_index()
        for value, count in counts.items():
            rows.append({
                "split": split,
                "label": int(value),
                "class_name": "Normal" if int(value) == 0 else "Attack",
                "count": int(count),
                "percentage": float(count / len(df) * 100),
            })
    return pd.DataFrame(rows)


def build_attack_distribution(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    categories = sorted(
        set(train[ATTACK_COL].astype(str).unique())
        | set(test[ATTACK_COL].astype(str).unique())
    )

    for category in categories:
        for split, df in [("Train", train), ("Test", test)]:
            count = int((df[ATTACK_COL].astype(str) == category).sum())
            rows.append({
                "attack_category": category,
                "split": split,
                "count": count,
                "percentage": float(count / len(df) * 100),
            })
    return pd.DataFrame(rows)


def numeric_feature_columns(train: pd.DataFrame) -> list[str]:
    cols = train.select_dtypes(include=[np.number]).columns.tolist()
    return [c for c in cols if c not in {ID_COL, TARGET_COL}]


def build_numeric_summary(train: pd.DataFrame) -> pd.DataFrame:
    cols = numeric_feature_columns(train)
    records = []

    for col in cols:
        s = train[col]
        records.append({
            "feature": col,
            "count": int(s.count()),
            "mean": float(s.mean()),
            "std": float(s.std()),
            "min": float(s.min()),
            "q01": float(s.quantile(0.01)),
            "q25": float(s.quantile(0.25)),
            "median": float(s.median()),
            "q75": float(s.quantile(0.75)),
            "q99": float(s.quantile(0.99)),
            "max": float(s.max()),
            "zero_pct": float((s == 0).mean() * 100),
            "skew": float(s.skew()),
        })

    return pd.DataFrame(records)


def build_categorical_summary(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for col in CATEGORICAL_EXPECTED:
        if col not in train.columns:
            continue

        train_values = set(train[col].astype(str).unique())
        test_values = set(test[col].astype(str).unique())

        rows.append({
            "feature": col,
            "train_unique": len(train_values),
            "test_unique": len(test_values),
            "unseen_in_train_count": len(test_values - train_values),
            "unseen_in_train_values": " | ".join(sorted(test_values - train_values)),
        })

    return pd.DataFrame(rows)


def build_high_corr_pairs(train: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    numeric_cols = numeric_feature_columns(train)

    corr = train[numeric_cols].corr(method="spearman")

    records = []
    for i, col_a in enumerate(numeric_cols):
        for j in range(i + 1, len(numeric_cols)):
            col_b = numeric_cols[j]
            value = corr.loc[col_a, col_b]

            if pd.notna(value) and abs(value) >= HIGH_CORRELATION_THRESHOLD:
                records.append({
                    "feature_a": col_a,
                    "feature_b": col_b,
                    "spearman_rho": float(value),
                    "abs_rho": float(abs(value)),
                })

    pairs = pd.DataFrame(records)
    if not pairs.empty:
        pairs = pairs.sort_values("abs_rho", ascending=False)

    return corr, pairs


def build_target_association(train: pd.DataFrame) -> pd.DataFrame:
    """
    Descriptive association only.
    This table is NOT a feature-selection result.

    For each numeric feature:
      - Spearman correlation with binary label
      - standardized mean difference between Attack and Normal
    """
    numeric_cols = numeric_feature_columns(train)
    rows = []

    y = train[TARGET_COL]

    for col in numeric_cols:
        x = train[col]

        rho = x.corr(y, method="spearman")

        normal = x[y == 0]
        attack = x[y == 1]

        mean_normal = float(normal.mean())
        mean_attack = float(attack.mean())
        var_normal = float(normal.var(ddof=1))
        var_attack = float(attack.var(ddof=1))

        pooled_sd = np.sqrt((var_normal + var_attack) / 2)

        if pooled_sd == 0 or np.isnan(pooled_sd):
            smd = np.nan
        else:
            smd = (mean_attack - mean_normal) / pooled_sd

        rows.append({
            "feature": col,
            "spearman_with_label": float(rho) if pd.notna(rho) else np.nan,
            "abs_spearman_with_label": float(abs(rho)) if pd.notna(rho) else np.nan,
            "mean_normal": mean_normal,
            "mean_attack": mean_attack,
            "standardized_mean_difference": float(smd) if pd.notna(smd) else np.nan,
            "abs_standardized_mean_difference": (
                float(abs(smd)) if pd.notna(smd) else np.nan
            ),
        })

    return pd.DataFrame(rows)


def build_attack_rate_by_category(train: pd.DataFrame) -> pd.DataFrame:
    """
    Describe target rate for categorical inputs using TRAIN only.
    """
    outputs = []

    for col in CATEGORICAL_EXPECTED:
        if col not in train.columns:
            continue

        table = (
            train.groupby(col, dropna=False)[TARGET_COL]
            .agg(["count", "mean"])
            .reset_index()
            .rename(columns={"mean": "attack_rate"})
        )
        table.insert(0, "feature", col)
        table = table.rename(columns={col: "value"})
        outputs.append(table)

    if not outputs:
        return pd.DataFrame(
            columns=["feature", "value", "count", "attack_rate"]
        )

    return pd.concat(outputs, ignore_index=True)


# ---------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------

def plot_binary_distribution(class_dist: pd.DataFrame) -> None:
    pivot = class_dist.pivot(
        index="class_name",
        columns="split",
        values="count",
    ).fillna(0)

    order = [x for x in ["Normal", "Attack"] if x in pivot.index]
    pivot = pivot.loc[order]

    x = np.arange(len(pivot.index))
    width = 0.36

    fig, ax = plt.subplots(figsize=(5.6, 3.8))

    train_vals = pivot["Train"].to_numpy() if "Train" in pivot.columns else np.zeros(len(x))
    test_vals = pivot["Test"].to_numpy() if "Test" in pivot.columns else np.zeros(len(x))

    ax.bar(x - width / 2, train_vals, width, label="Train")
    ax.bar(x + width / 2, test_vals, width, label="Test")

    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index)
    ax.set_ylabel("Number of records")
    ax.set_title("UNSW-NB15 binary class distribution")
    ax.legend()

    for xpos, vals in [(x - width / 2, train_vals), (x + width / 2, test_vals)]:
        for xi, value in zip(xpos, vals):
            ax.text(
                xi,
                value,
                f"{int(value):,}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    fig.tight_layout()
    save_figure(fig, "fig01_binary_class_distribution")


def plot_attack_distribution(attack_dist: pd.DataFrame) -> None:
    pivot = attack_dist.pivot(
        index="attack_category",
        columns="split",
        values="count",
    ).fillna(0)

    sort_col = "Train" if "Train" in pivot.columns else pivot.columns[0]
    pivot = pivot.sort_values(sort_col, ascending=False)

    x = np.arange(len(pivot.index))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    train_vals = pivot["Train"].to_numpy() if "Train" in pivot.columns else np.zeros(len(x))
    test_vals = pivot["Test"].to_numpy() if "Test" in pivot.columns else np.zeros(len(x))

    ax.bar(x - width / 2, train_vals, width, label="Train")
    ax.bar(x + width / 2, test_vals, width, label="Test")

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=45, ha="right")
    ax.set_ylabel("Number of records (log scale)")
    ax.set_title("Attack-category distribution reveals strong multiclass imbalance")
    ax.legend()

    fig.tight_layout()
    save_figure(fig, "fig02_attack_category_distribution")


def plot_target_association(target_assoc: pd.DataFrame) -> None:
    plot_df = (
        target_assoc
        .dropna(subset=["abs_standardized_mean_difference"])
        .nlargest(TOP_N_EFFECT_FEATURES, "abs_standardized_mean_difference")
        .sort_values("abs_standardized_mean_difference", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(6.5, 5.2))

    ax.barh(
        plot_df["feature"],
        plot_df["abs_standardized_mean_difference"],
    )
    ax.set_xlabel("Absolute standardized mean difference")
    ax.set_ylabel("Feature")
    ax.set_title(
        "Numeric features with strongest Normal–Attack separation\n"
        "(descriptive TRAIN-only EDA; not feature selection)"
    )

    fig.tight_layout()
    save_figure(fig, "fig03_numeric_class_separation")


def plot_correlation_heatmap(
    corr: pd.DataFrame,
    target_assoc: pd.DataFrame,
) -> None:
    ranked = (
        target_assoc
        .dropna(subset=["abs_spearman_with_label"])
        .nlargest(TOP_N_CORR_FEATURES, "abs_spearman_with_label")
        ["feature"]
        .tolist()
    )

    if len(ranked) < 2:
        return

    matrix = corr.loc[ranked, ranked]

    fig, ax = plt.subplots(figsize=(7.2, 6.3))
    image = ax.imshow(matrix.to_numpy(), vmin=-1, vmax=1, aspect="auto")

    ax.set_xticks(np.arange(len(ranked)))
    ax.set_yticks(np.arange(len(ranked)))
    ax.set_xticklabels(ranked, rotation=90)
    ax.set_yticklabels(ranked)

    ax.set_title(
        "Spearman correlation among target-associated numeric features\n"
        "(TRAIN only)"
    )

    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("Spearman rho")

    fig.tight_layout()
    save_figure(fig, "fig04_numeric_correlation_heatmap")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    require(TRAIN_FILE)
    require(TEST_FILE)

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("PHASE 4 — UNSW-NB15 EDA")
    print("No training, feature selection, resampling, or raw-data modification.")
    print("=" * 72)

    train = read_dataset(TRAIN_FILE)
    test = read_dataset(TEST_FILE)

    print(f"[LOAD] Train: {train.shape[0]:,} rows x {train.shape[1]} columns")
    print(f"[LOAD] Test : {test.shape[0]:,} rows x {test.shape[1]} columns")

    class_dist = build_class_distribution(train, test)
    attack_dist = build_attack_distribution(train, test)
    numeric_summary = build_numeric_summary(train)
    categorical_summary = build_categorical_summary(train, test)
    corr, high_corr_pairs = build_high_corr_pairs(train)
    target_assoc = build_target_association(train)
    categorical_rates = build_attack_rate_by_category(train)

    class_dist.to_csv(TABLE_DIR / "binary_class_distribution.csv", index=False)
    attack_dist.to_csv(TABLE_DIR / "attack_category_distribution.csv", index=False)
    numeric_summary.to_csv(TABLE_DIR / "numeric_feature_summary_train.csv", index=False)
    categorical_summary.to_csv(TABLE_DIR / "categorical_summary.csv", index=False)
    high_corr_pairs.to_csv(TABLE_DIR / "high_correlation_pairs_train.csv", index=False)
    target_assoc.to_csv(TABLE_DIR / "numeric_target_association_train.csv", index=False)
    categorical_rates.to_csv(TABLE_DIR / "categorical_attack_rates_train.csv", index=False)

    plot_binary_distribution(class_dist)
    plot_attack_distribution(attack_dist)
    plot_target_association(target_assoc)
    plot_correlation_heatmap(corr, target_assoc)

    novel_status = "not found"
    novel_rows = None
    if NOVEL_TEST_FILE.exists():
        novel = read_dataset(NOVEL_TEST_FILE)
        novel_status = "found"
        novel_rows = int(len(novel))

    strongest_effects = (
        target_assoc
        .dropna(subset=["abs_standardized_mean_difference"])
        .nlargest(10, "abs_standardized_mean_difference")
        [["feature", "standardized_mean_difference"]]
    )

    strongest_corr_pairs = (
        high_corr_pairs.head(10)
        if not high_corr_pairs.empty
        else pd.DataFrame()
    )

    summary_lines = [
        "PHASE 4 — UNSW-NB15 EDA SUMMARY",
        "=" * 72,
        "",
        f"Train rows: {len(train):,}",
        f"Test rows : {len(test):,}",
        f"Novel-vector test: {novel_status}"
        + (f" ({novel_rows:,} rows)" if novel_rows is not None else ""),
        "",
        "Binary class proportions:",
    ]

    for _, row in class_dist.iterrows():
        summary_lines.append(
            f"- {row['split']} / {row['class_name']}: "
            f"{int(row['count']):,} ({row['percentage']:.2f}%)"
        )

    summary_lines.extend([
        "",
        f"Attack categories in train: {train[ATTACK_COL].nunique()}",
        f"Attack categories in test : {test[ATTACK_COL].nunique()}",
        "",
        f"Numeric features inspected: {len(numeric_feature_columns(train))}",
        f"High-correlation numeric pairs "
        f"(|Spearman rho| >= {HIGH_CORRELATION_THRESHOLD}): "
        f"{len(high_corr_pairs)}",
        "",
        "Top numeric Normal–Attack separation (TRAIN only):",
    ])

    for _, row in strongest_effects.iterrows():
        summary_lines.append(
            f"- {row['feature']}: SMD={row['standardized_mean_difference']:.4f}"
        )

    if not strongest_corr_pairs.empty:
        summary_lines.extend([
            "",
            "Strongest correlated numeric feature pairs (TRAIN only):",
        ])
        for _, row in strongest_corr_pairs.iterrows():
            summary_lines.append(
                f"- {row['feature_a']} ↔ {row['feature_b']}: "
                f"rho={row['spearman_rho']:.4f}"
            )

    summary_lines.extend([
        "",
        "IMPORTANT INTERPRETATION RULES",
        "- These are descriptive EDA findings, not feature-selection decisions.",
        "- Test data was not used to rank/select features.",
        "- Correlation does not prove redundancy or causation.",
        "- Rare attack categories require per-class analysis later.",
        "",
        "NEXT PHASE",
        "Phase 5 — formal feature selection performed inside TRAIN/CV only.",
    ])

    report = "\n".join(summary_lines)
    (OUT_DIR / "eda_summary.txt").write_text(report, encoding="utf-8")

    print()
    print(report)
    print()
    print(f"[OUTPUT] {OUT_DIR}")
    print("[DONE] Phase-4 EDA artifacts generated.")


if __name__ == "__main__":
    main()
