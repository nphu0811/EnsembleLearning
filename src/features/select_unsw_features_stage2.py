"""
PHASE 5.2 — UNSW-NB15 Feature Selection Stability + Wrapper Validation
======================================================================

Goals
-----
A. Stability analysis:
   Repeat the Stage-1 feature-ranking procedures across multiple TRAIN-only
   stratified samples / random seeds.

B. Wrapper analysis:
   Run RFECV on the Stage-1 consensus candidate space using TRAIN only.

Important
---------
- Official test set is NEVER loaded.
- This script does NOT declare a final "best" subset.
- The wrapper is model-dependent (Logistic Regression).
- One-hot encoded categorical levels selected by RFECV are mapped back to
  their original UNSW-NB15 feature names for interpretation.

Expected input
--------------
data/raw/unsw-nb15/UNSW_NB15_training-set.csv
results/feature_selection/unsw_nb15/stage1/subsets/candidate_feature_subsets.json

Outputs
-------
results/feature_selection/unsw_nb15/stage2/
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFECV, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

SEEDS = [11, 23, 42, 71, 101]

STABILITY_SAMPLE_SIZE = 60_000
WRAPPER_SAMPLE_SIZE = 50_000

TOP_K = 20
CORRELATION_THRESHOLD = 0.95

# A feature is "stable within a method" if selected in Top-K in >= 3/5 runs.
STABILITY_MIN_FREQUENCY = 0.60

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

STAGE1_SUBSETS_FILE = (
    PROJECT_ROOT
    / "results"
    / "feature_selection"
    / "unsw_nb15"
    / "stage1"
    / "subsets"
    / "candidate_feature_subsets.json"
)

OUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "feature_selection"
    / "unsw_nb15"
    / "stage2"
)

TABLE_DIR = OUT_DIR / "tables"
SUBSET_DIR = OUT_DIR / "subsets"


# ---------------------------------------------------------------------
# Basic utilities
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
    return df


def load_stage1_subsets() -> dict:
    require_file(STAGE1_SUBSETS_FILE)
    return json.loads(STAGE1_SUBSETS_FILE.read_text(encoding="utf-8"))


def model_features(df: pd.DataFrame) -> list[str]:
    return [
        c
        for c in df.columns
        if c not in {ID_COL, TARGET_COL, ATTACK_COL}
    ]


def stratified_sample(
    df: pd.DataFrame,
    size: int,
    seed: int,
) -> pd.DataFrame:
    if len(df) <= size:
        return df.sample(frac=1, random_state=seed).reset_index(drop=True)

    sample, _ = train_test_split(
        df,
        train_size=size,
        stratify=df[TARGET_COL],
        random_state=seed,
    )
    return sample.reset_index(drop=True)


def normalize_scores(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    lo = float(s.min())
    hi = float(s.max())

    if np.isclose(lo, hi):
        return pd.Series(np.zeros(len(s)), index=s.index)

    return (s - lo) / (hi - lo)


def make_ohe():
    """
    scikit-learn compatibility helper.
    """
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


# ---------------------------------------------------------------------
# Stage-1 methods repeated for stability
# ---------------------------------------------------------------------

def prepare_mi_matrix(
    df: pd.DataFrame,
    features: list[str],
) -> tuple[pd.DataFrame, np.ndarray]:
    X = df[features].copy()
    discrete = []

    for col in features:
        if col in CATEGORICAL_COLS:
            codes, _ = pd.factorize(
                X[col].astype("string"),
                sort=True,
            )
            X[col] = codes.astype(np.int32)
            discrete.append(True)
        else:
            X[col] = pd.to_numeric(X[col], errors="raise")
            discrete.append(False)

    return X, np.asarray(discrete, dtype=bool)


def mi_ranking(
    sample: pd.DataFrame,
    features: list[str],
    seed: int,
) -> pd.DataFrame:
    X, discrete = prepare_mi_matrix(sample, features)
    y = sample[TARGET_COL].to_numpy()

    scores = mutual_info_classif(
        X,
        y,
        discrete_features=discrete,
        random_state=seed,
    )

    out = pd.DataFrame({
        "feature": features,
        "score": scores,
    }).sort_values("score", ascending=False).reset_index(drop=True)

    out["rank"] = np.arange(1, len(out) + 1)
    return out


def filter_topk_with_redundancy(
    sample: pd.DataFrame,
    ranking: pd.DataFrame,
    top_k: int,
) -> list[str]:
    ordered = ranking["feature"].tolist()

    numeric = [
        f for f in ordered
        if f not in CATEGORICAL_COLS
    ]

    corr = sample[numeric].corr(method="spearman")

    selected: list[str] = []

    for feature in ordered:
        if len(selected) >= top_k:
            break

        blocked = False

        if feature not in CATEGORICAL_COLS:
            for other in selected:
                if other in CATEGORICAL_COLS:
                    continue

                rho = corr.loc[feature, other]
                if pd.notna(rho) and abs(float(rho)) >= CORRELATION_THRESHOLD:
                    blocked = True
                    break

        if not blocked:
            selected.append(feature)

    return selected


def build_preprocessor(
    numeric_cols: list[str],
    categorical_cols: list[str],
    scale: bool,
) -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler() if scale else "passthrough",
                numeric_cols,
            ),
            (
                "cat",
                make_ohe(),
                categorical_cols,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


def original_feature_name(
    transformed_name: str,
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> str:
    if transformed_name.startswith("num__"):
        return transformed_name[len("num__"):]

    if transformed_name.startswith("cat__"):
        rest = transformed_name[len("cat__"):]
        for col in sorted(
            categorical_cols,
            key=len,
            reverse=True,
        ):
            if rest == col or rest.startswith(f"{col}_"):
                return col

    raise ValueError(
        f"Could not map transformed feature: {transformed_name}"
    )


def aggregate_scores_to_original(
    transformed_names: np.ndarray,
    scores: np.ndarray,
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> pd.DataFrame:
    temp = pd.DataFrame({
        "transformed": transformed_names,
        "score": scores,
    })

    temp["feature"] = temp["transformed"].map(
        lambda x: original_feature_name(
            x,
            numeric_cols,
            categorical_cols,
        )
    )

    grouped = (
        temp.groupby("feature", as_index=False)
        .agg(
            score=("score", "sum"),
            max_component=("score", "max"),
            transformed_components=("transformed", "count"),
        )
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
    )

    grouped["rank"] = np.arange(1, len(grouped) + 1)
    return grouped


def l1_ranking(
    sample: pd.DataFrame,
    features: list[str],
    seed: int,
) -> pd.DataFrame:
    categorical = [
        c for c in CATEGORICAL_COLS
        if c in features
    ]
    numeric = [
        c for c in features
        if c not in categorical
    ]

    prep = build_preprocessor(
        numeric,
        categorical,
        scale=True,
    )

    X = prep.fit_transform(sample[features])
    y = sample[TARGET_COL]

    model = LogisticRegression(
        penalty="l1",
        solver="liblinear",
        C=0.1,
        max_iter=1500,
        random_state=seed,
    )
    model.fit(X, y)

    names = prep.get_feature_names_out()
    scores = np.abs(model.coef_.ravel())

    return aggregate_scores_to_original(
        names,
        scores,
        numeric,
        categorical,
    )


def extra_trees_ranking(
    sample: pd.DataFrame,
    features: list[str],
    seed: int,
) -> pd.DataFrame:
    categorical = [
        c for c in CATEGORICAL_COLS
        if c in features
    ]
    numeric = [
        c for c in features
        if c not in categorical
    ]

    prep = build_preprocessor(
        numeric,
        categorical,
        scale=False,
    )

    X = prep.fit_transform(sample[features])
    y = sample[TARGET_COL]

    model = ExtraTreesClassifier(
        n_estimators=200,
        min_samples_leaf=2,
        n_jobs=-1,
        random_state=seed,
    )
    model.fit(X, y)

    names = prep.get_feature_names_out()

    return aggregate_scores_to_original(
        names,
        model.feature_importances_,
        numeric,
        categorical,
    )


# ---------------------------------------------------------------------
# Stability
# ---------------------------------------------------------------------

def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def run_stability(
    train: pd.DataFrame,
    features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    records = []
    method_sets: dict[str, dict[int, set[str]]] = {
        "filter": {},
        "l1": {},
        "extra_trees": {},
    }

    for seed in SEEDS:
        print(f"  [stability] seed={seed}")

        sample = stratified_sample(
            train,
            STABILITY_SAMPLE_SIZE,
            seed,
        )

        mi = mi_ranking(sample, features, seed)
        filter_set = set(
            filter_topk_with_redundancy(
                sample,
                mi,
                TOP_K,
            )
        )

        l1 = l1_ranking(sample, features, seed)
        l1_set = set(
            l1.head(TOP_K)["feature"].tolist()
        )

        et = extra_trees_ranking(sample, features, seed)
        et_set = set(
            et.head(TOP_K)["feature"].tolist()
        )

        method_sets["filter"][seed] = filter_set
        method_sets["l1"][seed] = l1_set
        method_sets["extra_trees"][seed] = et_set

        for method, selected in [
            ("filter", filter_set),
            ("l1", l1_set),
            ("extra_trees", et_set),
        ]:
            for feature in features:
                records.append({
                    "seed": seed,
                    "method": method,
                    "feature": feature,
                    "selected_topk": feature in selected,
                })

    selections = pd.DataFrame(records)

    freq = (
        selections.groupby(["method", "feature"])["selected_topk"]
        .agg(["sum", "mean"])
        .reset_index()
        .rename(
            columns={
                "sum": "selected_runs",
                "mean": "selection_frequency",
            }
        )
    )

    wide = freq.pivot(
        index="feature",
        columns="method",
        values="selection_frequency",
    ).reset_index()

    wide.columns.name = None

    for expected in ["filter", "l1", "extra_trees"]:
        if expected not in wide.columns:
            wide[expected] = 0.0

    wide["stable_filter"] = (
        wide["filter"] >= STABILITY_MIN_FREQUENCY
    )
    wide["stable_l1"] = (
        wide["l1"] >= STABILITY_MIN_FREQUENCY
    )
    wide["stable_extra_trees"] = (
        wide["extra_trees"] >= STABILITY_MIN_FREQUENCY
    )

    stable_cols = [
        "stable_filter",
        "stable_l1",
        "stable_extra_trees",
    ]

    wide["stable_method_votes"] = (
        wide[stable_cols]
        .astype(int)
        .sum(axis=1)
    )

    wide["mean_selection_frequency"] = (
        wide[["filter", "l1", "extra_trees"]]
        .mean(axis=1)
    )

    wide = wide.sort_values(
        ["stable_method_votes", "mean_selection_frequency"],
        ascending=[False, False],
    ).reset_index(drop=True)

    # Pairwise Jaccard per method.
    jac_rows = []

    for method, seed_map in method_sets.items():
        for seed_a, seed_b in combinations(SEEDS, 2):
            score = jaccard(
                seed_map[seed_a],
                seed_map[seed_b],
            )

            jac_rows.append({
                "method": method,
                "seed_a": seed_a,
                "seed_b": seed_b,
                "jaccard": score,
            })

    jaccard_df = pd.DataFrame(jac_rows)

    stability_summary = {}

    for method in method_sets:
        values = jaccard_df.loc[
            jaccard_df["method"] == method,
            "jaccard",
        ]

        stability_summary[method] = {
            "mean_pairwise_jaccard": float(values.mean()),
            "min_pairwise_jaccard": float(values.min()),
            "max_pairwise_jaccard": float(values.max()),
        }

    return wide, jaccard_df, stability_summary


# ---------------------------------------------------------------------
# RFECV wrapper
# ---------------------------------------------------------------------

def run_rfecv(
    train: pd.DataFrame,
    candidate_features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    seed = 42

    sample = stratified_sample(
        train,
        WRAPPER_SAMPLE_SIZE,
        seed,
    )

    categorical = [
        c for c in CATEGORICAL_COLS
        if c in candidate_features
    ]

    numeric = [
        c for c in candidate_features
        if c not in categorical
    ]

    prep = build_preprocessor(
        numeric,
        categorical,
        scale=True,
    )

    X = prep.fit_transform(sample[candidate_features])
    y = sample[TARGET_COL]

    transformed_names = prep.get_feature_names_out()

    estimator = LogisticRegression(
        penalty="l2",
        solver="liblinear",
        C=1.0,
        max_iter=1500,
        random_state=seed,
    )

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=seed,
    )

    selector = RFECV(
        estimator=estimator,
        step=0.10,
        min_features_to_select=10,
        cv=cv,
        scoring="f1_macro",
        n_jobs=-1,
    )

    selector.fit(X, y)

    selected_transformed = pd.DataFrame({
        "transformed_feature": transformed_names,
        "selected": selector.support_,
        "rfecv_rank": selector.ranking_,
    })

    selected_transformed["original_feature"] = (
        selected_transformed["transformed_feature"]
        .map(
            lambda x: original_feature_name(
                x,
                numeric,
                categorical,
            )
        )
    )

    original_summary = (
        selected_transformed
        .groupby("original_feature", as_index=False)
        .agg(
            transformed_component_count=(
                "transformed_feature",
                "count",
            ),
            selected_component_count=(
                "selected",
                "sum",
            ),
            best_rfecv_rank=(
                "rfecv_rank",
                "min",
            ),
        )
    )

    original_summary["selected_any_component"] = (
        original_summary["selected_component_count"] > 0
    )

    original_summary["selected_fraction"] = (
        original_summary["selected_component_count"]
        / original_summary["transformed_component_count"]
    )

    original_summary = original_summary.sort_values(
        [
            "selected_any_component",
            "selected_fraction",
            "selected_component_count",
        ],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    # Newer scikit-learn versions may include 2-D arrays in cv_results_
    # (for example per-step support/ranking matrices). Passing the whole
    # dictionary directly to pd.DataFrame therefore raises:
    #   ValueError: Per-column arrays must each be 1-dimensional
    #
    # We only need the 1-D CV curve fields for this experiment.
    preferred = [
        "n_features",
        "mean_test_score",
        "std_test_score",
        "split0_test_score",
        "split1_test_score",
        "split2_test_score",
    ]

    curve_data = {}
    for key in preferred:
        if key not in selector.cv_results_:
            continue

        values = np.asarray(selector.cv_results_[key])

        if values.ndim == 1:
            curve_data[key] = values

    curve = pd.DataFrame(curve_data)

    selected_original = (
        original_summary.loc[
            original_summary["selected_any_component"],
            "original_feature",
        ]
        .tolist()
    )

    metadata = {
        "sample_rows": int(len(sample)),
        "candidate_original_feature_count": len(candidate_features),
        "transformed_feature_count": int(len(transformed_names)),
        "selected_transformed_feature_count": int(selector.n_features_),
        "selected_original_feature_count": len(selected_original),
        "selected_original_features": selected_original,
        "best_cv_macro_f1": float(
            np.max(selector.cv_results_["mean_test_score"])
        ),
        "cv_splits": 3,
        "scoring": "f1_macro",
        "step": 0.10,
        "min_features_to_select": 10,
        "estimator": "LogisticRegression(L2, liblinear)",
        "note": (
            "Wrapper result is estimator-dependent. "
            "Categorical dummy levels are mapped back to original features."
        ),
    }

    return (
        selected_transformed,
        original_summary,
        curve,
        metadata,
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    SUBSET_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("PHASE 5.2 — FEATURE STABILITY + RFECV WRAPPER")
    print("TRAIN ONLY — OFFICIAL TEST IS NOT LOADED")
    print("=" * 78)

    train = read_train()
    stage1 = load_stage1_subsets()

    features = model_features(train)

    stage1_consensus = stage1.get(
        "consensus_2plus_votes",
        [],
    )

    if not stage1_consensus:
        raise ValueError(
            "Stage-1 consensus subset is missing or empty."
        )

    print(
        f"[DATA] Train rows: {len(train):,}; "
        f"model features: {len(features)}"
    )
    print(
        f"[DATA] Stage-1 consensus candidate count: "
        f"{len(stage1_consensus)}"
    )

    # --------------------------------------------------------------
    # Stability
    # --------------------------------------------------------------
    print("\n[1/2] Repeating selectors across random seeds...")

    stability, jac, stab_summary = run_stability(
        train,
        features,
    )

    stability.to_csv(
        TABLE_DIR / "selection_stability.csv",
        index=False,
    )

    jac.to_csv(
        TABLE_DIR / "pairwise_jaccard.csv",
        index=False,
    )

    save_json(
        stab_summary,
        OUT_DIR / "stability_summary.json",
    )

    stable_2plus = stability.loc[
        stability["stable_method_votes"] >= 2,
        "feature",
    ].tolist()

    stable_all3 = stability.loc[
        stability["stable_method_votes"] == 3,
        "feature",
    ].tolist()

    # --------------------------------------------------------------
    # RFECV
    # --------------------------------------------------------------
    print("\n[2/2] Running RFECV wrapper on Stage-1 consensus space...")

    (
        rfecv_transformed,
        rfecv_original,
        rfecv_curve,
        rfecv_meta,
    ) = run_rfecv(
        train,
        stage1_consensus,
    )

    rfecv_transformed.to_csv(
        TABLE_DIR / "rfecv_transformed_selection.csv",
        index=False,
    )

    rfecv_original.to_csv(
        TABLE_DIR / "rfecv_original_feature_summary.csv",
        index=False,
    )

    rfecv_curve.to_csv(
        TABLE_DIR / "rfecv_cv_curve.csv",
        index=False,
    )

    save_json(
        rfecv_meta,
        OUT_DIR / "rfecv_metadata.json",
    )

    rfecv_selected = rfecv_meta[
        "selected_original_features"
    ]

    stable_and_wrapper = [
        f for f in stable_2plus
        if f in set(rfecv_selected)
    ]

    stage1_and_stable = [
        f for f in stage1_consensus
        if f in set(stable_2plus)
    ]

    candidate_sets = {
        "stage1_consensus_2plus": stage1_consensus,
        "stable_2plus_methods": stable_2plus,
        "stable_all_3_methods": stable_all3,
        "rfecv_selected_original": rfecv_selected,
        "stage1_consensus_and_stable": stage1_and_stable,
        "stable_and_rfecv": stable_and_wrapper,
    }

    save_json(
        candidate_sets,
        SUBSET_DIR / "stage2_candidate_subsets.json",
    )

    # --------------------------------------------------------------
    # Human-readable summary
    # --------------------------------------------------------------
    lines = [
        "PHASE 5.2 — FEATURE SELECTION STABILITY + WRAPPER SUMMARY",
        "=" * 78,
        "",
        "IMPORTANT:",
        "- Official TEST set was never loaded.",
        "- No subset is declared final/best yet.",
        "- RFECV is model-dependent.",
        "",
        "STABILITY",
        f"Seeds: {SEEDS}",
        f"Rows per stability sample: {STABILITY_SAMPLE_SIZE:,}",
        f"Top-K per method: {TOP_K}",
        f"Stable threshold: >= {STABILITY_MIN_FREQUENCY:.0%} of runs",
        "",
    ]

    for method, values in stab_summary.items():
        lines.append(
            f"- {method}: mean pairwise Jaccard="
            f"{values['mean_pairwise_jaccard']:.3f}, "
            f"range="
            f"{values['min_pairwise_jaccard']:.3f}–"
            f"{values['max_pairwise_jaccard']:.3f}"
        )

    lines.extend([
        "",
        f"Features stable in >=2/3 methods: {len(stable_2plus)}",
        ", ".join(stable_2plus) if stable_2plus else "(none)",
        "",
        f"Features stable in all 3 methods: {len(stable_all3)}",
        ", ".join(stable_all3) if stable_all3 else "(none)",
        "",
        "RFECV WRAPPER",
        f"Wrapper sample rows: {rfecv_meta['sample_rows']:,}",
        f"Input original candidates: "
        f"{rfecv_meta['candidate_original_feature_count']}",
        f"One-hot transformed features: "
        f"{rfecv_meta['transformed_feature_count']}",
        f"Selected transformed features: "
        f"{rfecv_meta['selected_transformed_feature_count']}",
        f"Selected original features: "
        f"{rfecv_meta['selected_original_feature_count']}",
        f"Best CV Macro-F1 during RFECV: "
        f"{rfecv_meta['best_cv_macro_f1']:.6f}",
        "",
        "RFECV-selected original features:",
        ", ".join(rfecv_selected),
        "",
        "Stable >=2 methods AND selected by RFECV:",
        ", ".join(stable_and_wrapper)
        if stable_and_wrapper
        else "(none)",
        "",
        "NEXT:",
        "Phase 6 will compare ALL FEATURES vs candidate subsets using matched",
        "baseline models and validation. Only predictive/cost evidence can tell",
        "us whether reducing the feature set is actually worthwhile.",
    ])

    report = "\n".join(lines)

    (OUT_DIR / "stage2_summary.txt").write_text(
        report,
        encoding="utf-8",
    )

    print()
    print(report)
    print()
    print(f"[OUTPUT] {OUT_DIR}")
    print("[DONE] Phase 5.2 completed.")


if __name__ == "__main__":
    main()
