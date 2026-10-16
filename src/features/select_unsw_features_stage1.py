"""
PHASE 5.1 — UNSW-NB15 Feature Selection Candidate Generation
==============================================================

Goal
----
Generate leakage-safe *candidate* feature rankings using TRAIN ONLY.

Methods
-------
1. Filter: Mutual Information + redundancy pruning by Spearman correlation
2. Embedded: L1 Logistic Regression
3. Embedded: Extra Trees feature importance
4. Consensus: agreement among the three methods

Important
---------
- This script DOES NOT use the official test set.
- This script DOES NOT declare any subset "best".
- Final subset validation must happen later inside CV / validation pipelines.
- Wrapper/RFECV is deliberately deferred to Phase 5.2 because running it
  blindly on all one-hot-expanded features is computationally expensive.

Expected project layout
-----------------------
NCKH/
├── data/
│   └── raw/
│       └── unsw-nb15/
│           └── UNSW_NB15_training-set.csv
├── results/
└── src/
    └── features/
        └── select_unsw_features_stage1.py

Outputs
-------
results/feature_selection/unsw_nb15/stage1/
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

RANDOM_STATE = 42

SELECTION_SAMPLE_SIZE = 100_000
TOP_K = 20
CORRELATION_THRESHOLD = 0.95

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

OUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "feature_selection"
    / "unsw_nb15"
    / "stage1"
)

TABLE_DIR = OUT_DIR / "tables"
SUBSET_DIR = OUT_DIR / "subsets"


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def save_json(data, path: Path) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def read_train() -> pd.DataFrame:
    require_file(TRAIN_FILE)

    df = pd.read_csv(TRAIN_FILE, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]

    required = {ID_COL, TARGET_COL, ATTACK_COL, *CATEGORICAL_COLS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {sorted(missing)}")

    return df


def get_model_features(df: pd.DataFrame) -> list[str]:
    return [
        c
        for c in df.columns
        if c not in {ID_COL, TARGET_COL, ATTACK_COL}
    ]


def stratified_selection_sample(df: pd.DataFrame) -> pd.DataFrame:
    """
    Use a fixed, stratified TRAIN-only sample for feature-selection ranking.

    The official TEST set is never loaded.
    """
    if len(df) <= SELECTION_SAMPLE_SIZE:
        return df.copy()

    sample, _ = train_test_split(
        df,
        train_size=SELECTION_SAMPLE_SIZE,
        stratify=df[TARGET_COL],
        random_state=RANDOM_STATE,
    )

    return sample.reset_index(drop=True)


def normalize_scores(series: pd.Series) -> pd.Series:
    s = series.astype(float)

    min_v = s.min()
    max_v = s.max()

    if np.isclose(max_v, min_v):
        return pd.Series(np.zeros(len(s)), index=s.index)

    return (s - min_v) / (max_v - min_v)


# ---------------------------------------------------------------------
# 1. Filter — Mutual Information
# ---------------------------------------------------------------------

def prepare_mi_matrix(
    df: pd.DataFrame,
    feature_cols: list[str],
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Keep one column per ORIGINAL feature.

    Categorical variables are factorized to integer category IDs and marked
    discrete for mutual_info_classif. Numeric variables remain numeric.
    """
    X = df[feature_cols].copy()

    discrete_mask = []

    for col in feature_cols:
        if col in CATEGORICAL_COLS:
            codes, _ = pd.factorize(X[col].astype("string"), sort=True)
            X[col] = codes.astype(np.int32)
            discrete_mask.append(True)
        else:
            X[col] = pd.to_numeric(X[col], errors="raise")
            discrete_mask.append(False)

    return X, np.array(discrete_mask, dtype=bool)


def mutual_information_ranking(
    sample: pd.DataFrame,
    feature_cols: list[str],
) -> pd.DataFrame:
    X_mi, discrete_mask = prepare_mi_matrix(sample, feature_cols)
    y = sample[TARGET_COL].to_numpy()

    scores = mutual_info_classif(
        X_mi,
        y,
        discrete_features=discrete_mask,
        random_state=RANDOM_STATE,
    )

    result = pd.DataFrame({
        "feature": feature_cols,
        "mutual_information": scores,
        "is_categorical": [c in CATEGORICAL_COLS for c in feature_cols],
    })

    result["mi_normalized"] = normalize_scores(
        result["mutual_information"]
    )

    result = result.sort_values(
        "mutual_information",
        ascending=False,
    ).reset_index(drop=True)

    result["mi_rank"] = np.arange(1, len(result) + 1)

    return result


def redundancy_pruned_filter_subset(
    sample: pd.DataFrame,
    mi_ranking: pd.DataFrame,
    top_k: int,
) -> tuple[list[str], pd.DataFrame]:
    """
    Greedy redundancy pruning.

    Start from highest-MI feature. For numeric features, reject a candidate
    when it is highly Spearman-correlated with an already selected numeric
    feature.

    Categorical variables are not pruned using numeric Spearman correlation.
    """
    selected: list[str] = []
    decisions = []

    numeric_cols = [
        c
        for c in mi_ranking["feature"].tolist()
        if c not in CATEGORICAL_COLS
    ]

    numeric_corr = sample[numeric_cols].corr(method="spearman")

    for feature in mi_ranking["feature"]:
        if len(selected) >= top_k:
            break

        reason = "selected"
        blocked_by = None
        rho = None

        if feature not in CATEGORICAL_COLS:
            selected_numeric = [
                s for s in selected
                if s not in CATEGORICAL_COLS
            ]

            for already in selected_numeric:
                value = numeric_corr.loc[feature, already]

                if (
                    pd.notna(value)
                    and abs(float(value)) >= CORRELATION_THRESHOLD
                ):
                    reason = "rejected_high_redundancy"
                    blocked_by = already
                    rho = float(value)
                    break

        decisions.append({
            "feature": feature,
            "decision": reason,
            "blocked_by": blocked_by,
            "spearman_rho": rho,
        })

        if reason == "selected":
            selected.append(feature)

    return selected, pd.DataFrame(decisions)


# ---------------------------------------------------------------------
# Helpers for one-hot methods
# ---------------------------------------------------------------------

def build_onehot_preprocessor(
    numeric_cols: list[str],
    categorical_cols: list[str],
    scale_numeric: bool,
) -> ColumnTransformer:
    numeric_transformer = (
        StandardScaler()
        if scale_numeric
        else "passthrough"
    )

    categorical_transformer = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=True,
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


def original_feature_from_transformed(
    transformed_name: str,
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> str:
    """
    Map ColumnTransformer output names back to original UNSW-NB15 features.

    Examples:
      num__dur -> dur
      cat__proto_tcp -> proto
      cat__service_http -> service
    """
    if transformed_name.startswith("num__"):
        return transformed_name[len("num__"):]

    if transformed_name.startswith("cat__"):
        rest = transformed_name[len("cat__"):]

        # Match longest original categorical feature name first.
        for col in sorted(categorical_cols, key=len, reverse=True):
            prefix = f"{col}_"
            if rest == col or rest.startswith(prefix):
                return col

    raise ValueError(
        f"Could not map transformed feature back to original: "
        f"{transformed_name}"
    )


def aggregate_transformed_scores(
    transformed_names: np.ndarray,
    scores: np.ndarray,
    numeric_cols: list[str],
    categorical_cols: list[str],
    score_name: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    transformed = pd.DataFrame({
        "transformed_feature": transformed_names,
        score_name: scores,
    })

    transformed["original_feature"] = transformed[
        "transformed_feature"
    ].map(
        lambda name: original_feature_from_transformed(
            name,
            numeric_cols,
            categorical_cols,
        )
    )

    grouped = (
        transformed.groupby("original_feature", as_index=False)
        .agg(
            aggregate_score=(score_name, "sum"),
            max_component_score=(score_name, "max"),
            transformed_component_count=(
                "transformed_feature",
                "count",
            ),
        )
        .sort_values("aggregate_score", ascending=False)
        .reset_index(drop=True)
    )

    grouped["normalized_score"] = normalize_scores(
        grouped["aggregate_score"]
    )
    grouped["rank"] = np.arange(1, len(grouped) + 1)

    return transformed, grouped


# ---------------------------------------------------------------------
# 2. Embedded — L1 Logistic Regression
# ---------------------------------------------------------------------

def l1_ranking(
    sample: pd.DataFrame,
    feature_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    categorical_cols = [
        c for c in CATEGORICAL_COLS if c in feature_cols
    ]
    numeric_cols = [
        c for c in feature_cols if c not in categorical_cols
    ]

    preprocessor = build_onehot_preprocessor(
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        scale_numeric=True,
    )

    X = sample[feature_cols]
    y = sample[TARGET_COL]

    X_transformed = preprocessor.fit_transform(X)

    model = LogisticRegression(
        penalty="l1",
        solver="liblinear",
        C=0.1,
        max_iter=1000,
        random_state=RANDOM_STATE,
    )

    model.fit(X_transformed, y)

    names = preprocessor.get_feature_names_out()
    abs_coef = np.abs(model.coef_.ravel())

    transformed, grouped = aggregate_transformed_scores(
        transformed_names=names,
        scores=abs_coef,
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        score_name="abs_l1_coefficient",
    )

    return transformed, grouped


# ---------------------------------------------------------------------
# 3. Embedded — Extra Trees
# ---------------------------------------------------------------------

def extra_trees_ranking(
    sample: pd.DataFrame,
    feature_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    categorical_cols = [
        c for c in CATEGORICAL_COLS if c in feature_cols
    ]
    numeric_cols = [
        c for c in feature_cols if c not in categorical_cols
    ]

    preprocessor = build_onehot_preprocessor(
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        scale_numeric=False,
    )

    X = sample[feature_cols]
    y = sample[TARGET_COL]

    X_transformed = preprocessor.fit_transform(X)

    model = ExtraTreesClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        min_samples_leaf=2,
    )

    model.fit(X_transformed, y)

    names = preprocessor.get_feature_names_out()
    importance = model.feature_importances_

    transformed, grouped = aggregate_transformed_scores(
        transformed_names=names,
        scores=importance,
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        score_name="extra_trees_importance",
    )

    return transformed, grouped


# ---------------------------------------------------------------------
# 4. Consensus
# ---------------------------------------------------------------------

def build_consensus(
    all_features: list[str],
    mi_ranking: pd.DataFrame,
    filter_selected: list[str],
    l1_grouped: pd.DataFrame,
    et_grouped: pd.DataFrame,
) -> pd.DataFrame:
    table = pd.DataFrame({"feature": all_features})

    mi_map = mi_ranking.set_index("feature")
    l1_map = l1_grouped.set_index("original_feature")
    et_map = et_grouped.set_index("original_feature")

    table["mi_rank"] = table["feature"].map(mi_map["mi_rank"])
    table["mi_score"] = table["feature"].map(
        mi_map["mi_normalized"]
    )

    table["l1_rank"] = table["feature"].map(l1_map["rank"])
    table["l1_score"] = table["feature"].map(
        l1_map["normalized_score"]
    )

    table["et_rank"] = table["feature"].map(et_map["rank"])
    table["et_score"] = table["feature"].map(
        et_map["normalized_score"]
    )

    top_filter = set(filter_selected[:TOP_K])
    top_l1 = set(
        l1_grouped.head(TOP_K)["original_feature"]
    )
    top_et = set(
        et_grouped.head(TOP_K)["original_feature"]
    )

    table["filter_topk"] = table["feature"].isin(top_filter)
    table["l1_topk"] = table["feature"].isin(top_l1)
    table["extra_trees_topk"] = table["feature"].isin(top_et)

    table["topk_votes"] = (
        table[
            ["filter_topk", "l1_topk", "extra_trees_topk"]
        ]
        .astype(int)
        .sum(axis=1)
    )

    table["mean_normalized_score"] = (
        table[["mi_score", "l1_score", "et_score"]]
        .fillna(0)
        .mean(axis=1)
    )

    table = table.sort_values(
        ["topk_votes", "mean_normalized_score"],
        ascending=[False, False],
    ).reset_index(drop=True)

    table["consensus_rank"] = np.arange(
        1,
        len(table) + 1,
    )

    return table


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    SUBSET_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 76)
    print("PHASE 5.1 — UNSW-NB15 FEATURE SELECTION CANDIDATES")
    print("TRAIN ONLY — OFFICIAL TEST IS NOT LOADED")
    print("=" * 76)

    train = read_train()
    feature_cols = get_model_features(train)

    categorical_cols = [
        c for c in CATEGORICAL_COLS
        if c in feature_cols
    ]
    numeric_cols = [
        c for c in feature_cols
        if c not in categorical_cols
    ]

    print(f"[DATA] Train rows          : {len(train):,}")
    print(f"[DATA] Original features   : {len(feature_cols)}")
    print(f"[DATA] Numeric features    : {len(numeric_cols)}")
    print(f"[DATA] Categorical features: {categorical_cols}")

    sample = stratified_selection_sample(train)

    print(
        f"[DATA] Selection sample    : "
        f"{len(sample):,} rows (stratified, seed={RANDOM_STATE})"
    )

    # --------------------------------------------------------------
    # Filter
    # --------------------------------------------------------------
    print("\n[1/4] Mutual Information ranking...")

    mi = mutual_information_ranking(
        sample,
        feature_cols,
    )

    mi.to_csv(
        TABLE_DIR / "mutual_information_ranking.csv",
        index=False,
    )

    filter_selected, redundancy_decisions = (
        redundancy_pruned_filter_subset(
            sample=sample,
            mi_ranking=mi,
            top_k=TOP_K,
        )
    )

    redundancy_decisions.to_csv(
        TABLE_DIR / "filter_redundancy_decisions.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # L1
    # --------------------------------------------------------------
    print("[2/4] L1 Logistic Regression ranking...")

    l1_transformed, l1_grouped = l1_ranking(
        sample,
        feature_cols,
    )

    l1_transformed.to_csv(
        TABLE_DIR / "l1_transformed_feature_scores.csv",
        index=False,
    )

    l1_grouped.to_csv(
        TABLE_DIR / "l1_original_feature_ranking.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # Extra Trees
    # --------------------------------------------------------------
    print("[3/4] Extra Trees ranking...")

    et_transformed, et_grouped = extra_trees_ranking(
        sample,
        feature_cols,
    )

    et_transformed.to_csv(
        TABLE_DIR / "extra_trees_transformed_feature_scores.csv",
        index=False,
    )

    et_grouped.to_csv(
        TABLE_DIR / "extra_trees_original_feature_ranking.csv",
        index=False,
    )

    # --------------------------------------------------------------
    # Consensus
    # --------------------------------------------------------------
    print("[4/4] Building consensus...")

    consensus = build_consensus(
        all_features=feature_cols,
        mi_ranking=mi,
        filter_selected=filter_selected,
        l1_grouped=l1_grouped,
        et_grouped=et_grouped,
    )

    consensus.to_csv(
        TABLE_DIR / "consensus_feature_ranking.csv",
        index=False,
    )

    filter_top20 = filter_selected[:TOP_K]
    l1_top20 = (
        l1_grouped.head(TOP_K)["original_feature"].tolist()
    )
    et_top20 = (
        et_grouped.head(TOP_K)["original_feature"].tolist()
    )

    consensus_2plus = consensus.loc[
        consensus["topk_votes"] >= 2,
        "feature",
    ].tolist()

    union_top20 = consensus.loc[
        consensus["topk_votes"] >= 1,
        "feature",
    ].tolist()

    subsets = {
        "all_features": feature_cols,
        "filter_mi_redundancy_top20": filter_top20,
        "l1_top20": l1_top20,
        "extra_trees_top20": et_top20,
        "consensus_2plus_votes": consensus_2plus,
        "union_of_all_top20": union_top20,
    }

    save_json(
        subsets,
        SUBSET_DIR / "candidate_feature_subsets.json",
    )

    metadata = {
        "phase": "5.1",
        "dataset": "UNSW-NB15",
        "source": "official predefined training split only",
        "official_test_loaded": False,
        "train_rows": int(len(train)),
        "selection_sample_rows": int(len(sample)),
        "selection_sample_strategy": (
            "stratified random sample from official training split"
        ),
        "random_state": RANDOM_STATE,
        "original_feature_count": len(feature_cols),
        "top_k": TOP_K,
        "correlation_threshold": CORRELATION_THRESHOLD,
        "methods": [
            "Mutual Information + Spearman redundancy pruning",
            "L1 Logistic Regression",
            "Extra Trees feature importance",
            "Consensus voting across methods",
        ],
        "note": (
            "Candidate generation only. No subset is declared best. "
            "Final evaluation must occur in later CV/validation."
        ),
    }

    save_json(
        metadata,
        OUT_DIR / "stage1_metadata.json",
    )

    top_consensus = consensus.head(20)

    lines = [
        "PHASE 5.1 — FEATURE SELECTION STAGE-1 SUMMARY",
        "=" * 76,
        "",
        "IMPORTANT:",
        "- Official TEST set was not loaded.",
        "- No feature subset is declared 'best' yet.",
        "- These are candidate rankings for later validation.",
        "",
        f"Official training rows: {len(train):,}",
        f"Selection sample rows : {len(sample):,}",
        f"Original model features: {len(feature_cols)}",
        "",
        f"Filter subset size: {len(filter_top20)}",
        f"L1 top-K size      : {len(l1_top20)}",
        f"ExtraTrees top-K   : {len(et_top20)}",
        f"Consensus >=2 votes: {len(consensus_2plus)}",
        f"Union of top-K     : {len(union_top20)}",
        "",
        "TOP CONSENSUS FEATURES",
    ]

    for _, row in top_consensus.iterrows():
        lines.append(
            f"- {row['feature']}: "
            f"votes={int(row['topk_votes'])}, "
            f"MI-rank={int(row['mi_rank'])}, "
            f"L1-rank={int(row['l1_rank'])}, "
            f"ET-rank={int(row['et_rank'])}"
        )

    lines.extend([
        "",
        "NEXT:",
        "Phase 5.2 will test stability and wrapper/RFECV on a reduced candidate",
        "space, then Phase 6 baselines will compare candidate subsets using",
        "the same validation protocol.",
    ])

    report = "\n".join(lines)

    (OUT_DIR / "stage1_summary.txt").write_text(
        report,
        encoding="utf-8",
    )

    print()
    print(report)
    print()
    print(f"[OUTPUT] {OUT_DIR}")
    print("[DONE] Stage-1 candidate generation completed.")


if __name__ == "__main__":
    main()
