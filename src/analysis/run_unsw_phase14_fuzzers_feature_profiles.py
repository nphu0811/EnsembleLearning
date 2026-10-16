#!/usr/bin/env python3
"""Canonical Phase 14 / Step 4: descriptive Fuzzers false-negative analysis.

Reads the frozen Phase-9 sample predictions and ORIGINAL official UNSW-NB15 test CSV.
Joins on unique `id` and verifies labels, attack categories, confusion matrices and
Fuzzers paired outcomes before computing aggregate subgroup profiles.

No model training, probability recalibration, threshold tuning, feature selection,
or editing of existing artifacts. Outputs are aggregated; NO sample-level rows.

From NCKH project root:
    py src/analysis/run_unsw_phase14_fuzzers_feature_profiles.py
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

RF_COL = "random_forest_42_pred"
STACK_COL = "stacking_42_pred"
PRED_COLUMNS = ["id", "label", "attack_cat", RF_COL, STACK_COL]
TEST_COLUMNS = [
    "id", "label", "attack_cat", "state", "proto", "sttl", "dload", "ct_state_ttl"
]
GROUPS = [
    "both_caught",
    "rf_caught_stack_missed",
    "rf_missed_stack_caught",
    "both_missed",
]
EXPECTED = {
    "all": 82332, "normal": 37000, "attack": 45332,
    "rf": {"tn": 26997, "fp": 10003, "fn": 734, "tp": 44598},
    "stack": {"tn": 27139, "fp": 9861, "fn": 852, "tp": 44480},
    "fuzzers": {
        "total": 6062,
        "both_caught": 5261,
        "rf_caught_stack_missed": 180,
        "rf_missed_stack_caught": 47,
        "both_missed": 574,
        "rf_fn": 621,
        "stack_fn": 754,
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--predictions", type=Path,
        default=Path(
            "results/final_evaluation/unsw_nb15/phase9_holdout/"
            "tables/official_test_predictions.csv"
        ),
        help="Saved sample-level frozen Phase-9 official test predictions",
    )
    parser.add_argument(
        "--test", type=Path,
        default=Path("data/raw/unsw-nb15/UNSW_NB15_testing-set.csv"),
        help="Original official UNSW-NB15 testing CSV (read only)",
    )
    parser.add_argument(
        "--out", type=Path,
        default=Path(
            "results/final_analysis/unsw_nb15/phase14_error_analysis_step4"
        ),
        help="New separate output folder; raw inputs are not changed",
    )
    return parser.parse_args()


def load_csv(path: Path, need: list[str], name: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {name}: {path}")
    headers = pd.read_csv(path, nrows=0)
    hmap = {str(c).strip(): c for c in headers.columns}
    missing = sorted(set(need) - set(hmap))
    if missing:
        raise ValueError(f"{name} missing columns: {missing}")
    df = pd.read_csv(path, usecols=[hmap[c] for c in need], low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    if len(df) != EXPECTED["all"]:
        raise ValueError(f"Unexpected number of {name} rows: {len(df)}")
    if df["id"].isna().any() or not df["id"].is_unique:
        raise ValueError(f"Missing/duplicate IDs in {name}; cannot join safely")
    if df["label"].isna().any() or not set(df["label"].unique()).issubset({0, 1}):
        raise ValueError(f"{name}.label must be 0 or 1 only")
    return df


def counts(y: pd.Series, p: pd.Series) -> dict[str, int]:
    return {
        "tn": int(((y == 0) & (p == 0)).sum()),
        "fp": int(((y == 0) & (p == 1)).sum()),
        "fn": int(((y == 1) & (p == 0)).sum()),
        "tp": int(((y == 1) & (p == 1)).sum()),
    }


def load_and_check(pred_path: Path, test_path: Path) -> pd.DataFrame:
    pred = load_csv(pred_path, PRED_COLUMNS, "frozen predictions")
    test = load_csv(test_path, TEST_COLUMNS, "official test")
    for col in (RF_COL, STACK_COL):
        if pred[col].isna().any() or not set(pred[col].unique()).issubset({0, 1}):
            raise ValueError(f"{col} is not binary 0/1")

    merged = pred.merge(
        test, on="id", validate="one_to_one", how="inner", sort=False,
        suffixes=("_saved", "_raw"),
    )
    if len(merged) != EXPECTED["all"]:
        raise ValueError("ID mismatch: saved predictions and official test differ")
    if not (merged["label_saved"].to_numpy() == merged["label_raw"].to_numpy()).all():
        raise ValueError("Label mismatch by ID: wrong test file/version?")

    for suffix in ("saved", "raw"):
        col = f"attack_cat_{suffix}"
        merged[col] = merged[col].astype("string").str.strip().fillna("<MISSING>")
    if not (merged["attack_cat_saved"].to_numpy() == merged["attack_cat_raw"].to_numpy()).all():
        raise ValueError("attack_cat mismatch by ID: wrong test file/version?")

    y = merged["label_saved"]
    if int((y == 0).sum()) != EXPECTED["normal"] or int((y == 1).sum()) != EXPECTED["attack"]:
        raise ValueError("Normal/Attack support mismatch")
    for name, col in (("rf", RF_COL), ("stack", STACK_COL)):
        actual = counts(y, merged[col])
        if actual != EXPECTED[name]:
            raise ValueError(f"{name} confusion counts mismatch: {actual}")
    return merged


def fuzzers_subgroups(merged: pd.DataFrame) -> pd.DataFrame:
    fuzz = merged.loc[merged["attack_cat_saved"].str.casefold().eq("fuzzers")].copy()
    if len(fuzz) != EXPECTED["fuzzers"]["total"]:
        raise ValueError(f"Fuzzers support mismatch: {len(fuzz)}")
    if not (fuzz["label_saved"] == 1).all():
        raise ValueError("Fuzzers should all be labeled Attack (=1)")

    rf_caught = fuzz[RF_COL].eq(1)
    stack_caught = fuzz[STACK_COL].eq(1)
    fuzz["error_group"] = "both_missed"
    fuzz.loc[rf_caught & stack_caught, "error_group"] = "both_caught"
    fuzz.loc[rf_caught & ~stack_caught, "error_group"] = "rf_caught_stack_missed"
    fuzz.loc[~rf_caught & stack_caught, "error_group"] = "rf_missed_stack_caught"
    actual = fuzz["error_group"].value_counts().to_dict()
    for group in GROUPS:
        if actual.get(group, 0) != EXPECTED["fuzzers"][group]:
            raise ValueError(f"Fuzzers group mismatch {group}: {actual}")
    if int((~rf_caught).sum()) != EXPECTED["fuzzers"]["rf_fn"]:
        raise ValueError("RF Fuzzers FN count mismatch")
    if int((~stack_caught).sum()) != EXPECTED["fuzzers"]["stack_fn"]:
        raise ValueError("Stacking Fuzzers FN count mismatch")
    return fuzz


def group_table(fuzz: pd.DataFrame) -> pd.DataFrame:
    counts_ = fuzz["error_group"].value_counts()
    return pd.DataFrame([
        {"error_group": g, "n": int(counts_.get(g, 0)),
         "share_of_all_fuzzers": float(counts_.get(g, 0) / len(fuzz))}
        for g in GROUPS
    ])


def categorical_profile(fuzz: pd.DataFrame, feature: str):
    values = fuzz[feature].astype("string").str.strip().fillna("<MISSING>")
    ct = pd.crosstab(values, fuzz["error_group"])
    for g in GROUPS:
        if g not in ct.columns:
            ct[g] = 0
    ct = ct[GROUPS].astype(int)
    ct.index.name = feature
    support = ct.sum(axis=1)
    group_totals = ct.sum(axis=0)

    by_value = ct.reset_index()
    by_value.insert(1, "fuzzers_support", support.to_numpy())
    by_value["rf_false_negatives"] = (
        ct["rf_missed_stack_caught"] + ct["both_missed"]
    ).to_numpy()
    by_value["stacking_false_negatives"] = (
        ct["rf_caught_stack_missed"] + ct["both_missed"]
    ).to_numpy()
    by_value["stacking_minus_rf_fn"] = (
        by_value["stacking_false_negatives"] - by_value["rf_false_negatives"]
    )
    by_value["rf_fnr_given_fuzzers_and_value"] = (
        by_value["rf_false_negatives"] / by_value["fuzzers_support"]
    )
    by_value["stacking_fnr_given_fuzzers_and_value"] = (
        by_value["stacking_false_negatives"] / by_value["fuzzers_support"]
    )
    by_value = by_value.sort_values(["fuzzers_support", feature], ascending=[False, True]).reset_index(drop=True)

    comp = ct.reset_index().melt(id_vars=feature, var_name="error_group", value_name="n")
    comp["pct_value_within_error_group"] = comp.apply(
        lambda row: row["n"] / group_totals[row["error_group"]], axis=1
    )
    comp = comp.sort_values(["error_group", "n"], ascending=[True, False]).reset_index(drop=True)

    if int(by_value["fuzzers_support"].sum()) != EXPECTED["fuzzers"]["total"]:
        raise ValueError(f"{feature} profile total mismatch")
    for g in GROUPS:
        if int(by_value[g].sum()) != EXPECTED["fuzzers"][g]:
            raise ValueError(f"{feature} {g} count mismatch")
    return by_value, comp


def numeric_summaries(fuzz: pd.DataFrame, feature: str) -> pd.DataFrame:
    numeric = pd.to_numeric(fuzz[feature], errors="coerce")
    if numeric.isna().any() or not numeric.map(lambda x: float("-inf") < x < float("inf")).all():
        raise ValueError(f"{feature} contains missing/invalid values; stop and audit")
    work = pd.DataFrame({"error_group": fuzz["error_group"], feature: numeric})
    results = []
    for group in ["ALL_FUZZERS"] + GROUPS:
        arr = work[feature] if group == "ALL_FUZZERS" else work.loc[work.error_group.eq(group), feature]
        q = arr.quantile([0.25, 0.5, 0.75, 0.9])
        results.append({
            "error_group": group,
            "support": len(arr),
            "min": float(arr.min()),
            "q1": float(q.loc[0.25]),
            "median": float(q.loc[0.5]),
            "q3": float(q.loc[0.75]),
            "p90": float(q.loc[0.9]),
            "max": float(arr.max()),
            "pct_equal_zero": float(arr.eq(0).mean()),
        })
    return pd.DataFrame(results)


def summary_text(gtable: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> str:
    head = [
        "# Canonical Phase 14 — Step 4: Fuzzers feature analysis",
        "",
        "**Status:** descriptive error analysis on frozen official TEST predictions.",
        "",
        "## Integrity checks",
        "- 82,332 unique IDs aligned one-to-one with official test: PASS.",
        "- Binary labels and attack categories matched for every ID: PASS.",
        "- RF-42 / Stacking-42 confusion counts match frozen results: PASS.",
        "- Fuzzers support 6,062 and four paired error groups verified: PASS.",
        "",
        "## Fuzzers paired groups",
        "```",
        gtable.to_string(index=False),
        "```",
        "",
        "- Stacking fixes 47 Fuzzers false negatives of RF but creates 180 new ones.",
        "- Net difference: +133 FNs (Stacking minus RF).",
        "- Both models miss the same 574 Fuzzers flows.",
        "",
        "## How to read the CSV outputs",
        "- `*_by_value.csv`: conditional FNR P(model misses | actual Fuzzers, feature=value).",
        "- `*_group_composition.csv`: distribution P(feature=value | paired error group).",
        "- `*_numeric_summary.csv`: quantiles within paired groups, not causal effects.",
        "- Do NOT reverse conditional probabilities or infer general accuracy from selected disagreements.",
        "- Low-support values are exploratory and should not be ranked as reliable deployment rules.",
        "",
    ]
    for feature in ["state", "proto", "sttl"]:
        sub = tables[feature].head(8)
        head += [
            f"## Most frequent {feature} values among Fuzzers",
            "```",
            sub[[feature, "fuzzers_support", "rf_caught_stack_missed", "rf_missed_stack_caught", "rf_fnr_given_fuzzers_and_value", "stacking_fnr_given_fuzzers_and_value"]].to_string(index=False),
            "```",
            "",
        ]
    head += [
        "## Scientific interpretation boundary",
        "- These subgroup associations do NOT establish that a feature causes a false negative.",
        "- No model, threshold, feature subset or hyperparameter was modified after the official holdout.",
        "- This analysis is an explanation of existing errors, not a new performance estimate.",
        "- This binary detector's per-attack-category miss profile is NOT multiclass classification.",
        "",
        "## Next",
        "Send this output directory for independent verification and guided interpretation.",
    ]
    return "\n".join(head) + "\n"


def main():
    args = parse_args()
    # Validate all data and locked evidence BEFORE creating an output directory.
    merged = load_and_check(args.predictions, args.test)
    fuzz = fuzzers_subgroups(merged)
    gtable = group_table(fuzz)
    tables = {}
    outputs = {"fuzzers_pairwise_groups.csv": gtable}
    for feature in ["state", "proto", "sttl"]:
        by_val, comp = categorical_profile(fuzz, feature)
        outputs[f"{feature}_by_value.csv"] = by_val
        outputs[f"{feature}_group_composition.csv"] = comp
        tables[feature] = by_val
    for feature in ["sttl", "dload", "ct_state_ttl"]:
        outputs[f"{feature}_numeric_summary.csv"] = numeric_summaries(fuzz, feature)

    args.out.mkdir(parents=True, exist_ok=True)
    for filename, df in outputs.items():
        df.to_csv(args.out / filename, index=False, encoding="utf-8")
    (args.out / "PHASE14_STEP4_SUMMARY.md").write_text(
        summary_text(gtable, tables), encoding="utf-8"
    )
    print("PASS — 82,332 IDs matched; frozen confusion counts and Fuzzers outcomes verified")
    print("Fuzzers: both caught=5,261; RF caught/Stack missed=180; RF missed/Stack caught=47; both missed=574")
    print("Net Stacking minus RF Fuzzers FN: +133")
    print("READ ONLY inputs. No model training or modifications.")
    print("OUTPUT:", args.out)


if __name__ == "__main__":
    main()
