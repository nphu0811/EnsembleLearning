#!/usr/bin/env python3
"""Canonical Phase 14 — Step 3: descriptive Normal-traffic error profiles.

Reads the frozen Phase-9 saved prediction table and the OFFICIAL testing CSV.
Joins one-to-one on 'id'; checks labels, prediction counts and row totals.
Analyzes state, proto and sttl for 4 paired RF-42/Stacking-42 outcomes.

NO training / scoring / threshold changes / post-test model selection.
Outputs contain aggregate statistics only, not sample-level traffic records.

Run from NCKH root:
    py src/analysis/run_unsw_phase14_normal_feature_profiles.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

RF_COL = "random_forest_42_pred"
STACK_COL = "stacking_42_pred"
CORE_PRED_COLS = ["id", "label", "attack_cat", RF_COL, STACK_COL]
DATA_COLS = ["id", "label", "attack_cat", "state", "proto", "sttl"]

EXPECTED = {
    "rows": 82332, "normal": 37000, "attack": 45332,
    "rf": {"tn": 26997, "fp": 10003, "fn": 734, "tp": 44598},
    "stack": {"tn": 27139, "fp": 9861, "fn": 852, "tp": 44480},
    "normal_groups": {
        "both_correct": 26719,
        "stack_correct_rf_wrong": 420,
        "rf_correct_stack_wrong": 278,
        "both_wrong": 9583,
    },
}

GROUPS = [
    "both_correct",
    "stack_correct_rf_wrong",
    "rf_correct_stack_wrong",
    "both_wrong",
]
GROUP_DESCRIPTIONS = {
    "both_correct": "RF and Stacking both predict Normal correctly",
    "stack_correct_rf_wrong": "Stacking correct; RF false positive",
    "rf_correct_stack_wrong": "RF correct; Stacking false positive",
    "both_wrong": "RF and Stacking both predict Attack incorrectly",
}


def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--predictions", type=Path,
        default=Path("results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv"),
    )
    parser.add_argument(
        "--test", type=Path,
        default=Path("data/raw/unsw-nb15/UNSW_NB15_testing-set.csv"),
    )
    parser.add_argument(
        "--out", type=Path,
        default=Path("results/final_analysis/unsw_nb15/phase14_error_analysis_step3"),
    )
    return parser.parse_args()


def read_checked_csv(path: Path, columns: list[str], name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Cannot find {name}: {path}")
    header = pd.read_csv(path, nrows=0)
    col_map = {str(c).strip(): c for c in header.columns}
    missing = sorted(set(columns) - set(col_map))
    if missing:
        raise ValueError(f"{name} missing columns {missing}. Found: {list(col_map)}")
    df = pd.read_csv(path, usecols=[col_map[k] for k in columns], low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    if len(df) != EXPECTED["rows"]:
        raise ValueError(f"{name}: expected {EXPECTED['rows']} rows, found {len(df)}")
    if df["id"].isna().any() or not df["id"].is_unique:
        raise ValueError(f"{name}: id must be complete and unique for safe joining")
    if df["label"].isna().any() or not set(df["label"].unique()).issubset({0, 1}):
        raise ValueError(f"{name}: label must be exactly binary 0/1")
    return df


def confusion(y: pd.Series, p: pd.Series) -> dict[str, int]:
    return {
        "tn": int(((y == 0) & (p == 0)).sum()),
        "fp": int(((y == 0) & (p == 1)).sum()),
        "fn": int(((y == 1) & (p == 0)).sum()),
        "tp": int(((y == 1) & (p == 1)).sum()),
    }


def validated_join(predictions: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    for col in (RF_COL, STACK_COL):
        if predictions[col].isna().any() or not set(predictions[col].unique()).issubset({0, 1}):
            raise ValueError(f"Invalid binary predictions in {col}")

    both = predictions.merge(
        test, on="id", how="inner", validate="one_to_one",
        suffixes=("_saved", "_raw"), sort=False,
    )
    if len(both) != EXPECTED["rows"]:
        raise ValueError("Prediction and testing CSV IDs do not match one-to-one")
    if not both["label_saved"].equals(both["label_raw"]):
        raise ValueError("LABEL MISMATCH by id! Do not analyze — check dataset versions")

    attack_saved = both["attack_cat_saved"].astype("string").str.strip().fillna("<NULL>")
    attack_raw = both["attack_cat_raw"].astype("string").str.strip().fillna("<NULL>")
    if not attack_saved.equals(attack_raw):
        raise ValueError("attack_cat MISMATCH by id! Check file versions")

    y = both["label_saved"]
    if int((y == 0).sum()) != EXPECTED["normal"] or int((y == 1).sum()) != EXPECTED["attack"]:
        raise ValueError("Binary support differs from locked Phase 9/11")
    for key, col in (("rf", RF_COL), ("stack", STACK_COL)):
        actual = confusion(y, both[col])
        if actual != EXPECTED[key]:
            raise ValueError(f"{key} counts differ from frozen evidence: {actual}")

    return both


def profile_by_category(norm: pd.DataFrame, feature: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Two directions: P(feature value | error group) and per-value FP rates."""
    values = norm[feature].astype("string").str.strip().fillna("<MISSING>")
    work = pd.DataFrame({"value": values, "group": norm["error_group"]})
    ctab = pd.crosstab(work["value"], work["group"])
    for group in GROUPS:
        if group not in ctab.columns:
            ctab[group] = 0
    ctab = ctab[GROUPS].astype(int)
    total = ctab.sum(axis=1)
    groupsize = ctab.sum(axis=0)
    total_n = int(total.sum())
    if total_n != EXPECTED["normal"]:
        raise ValueError("Categorical counts failed Normal support verification")

    per_value = pd.DataFrame({
        feature: ctab.index.astype(str),
        "normal_support": total.to_numpy(),
        "normal_share": (total / total_n).to_numpy(),
        "stack_correct_rf_wrong": ctab["stack_correct_rf_wrong"].to_numpy(),
        "rf_correct_stack_wrong": ctab["rf_correct_stack_wrong"].to_numpy(),
        "both_correct": ctab["both_correct"].to_numpy(),
        "both_wrong": ctab["both_wrong"].to_numpy(),
        "rf_fp": (ctab["stack_correct_rf_wrong"] + ctab["both_wrong"]).to_numpy(),
        "stack_fp": (ctab["rf_correct_stack_wrong"] + ctab["both_wrong"]).to_numpy(),
    })
    per_value["stack_minus_rf_fp"] = per_value["stack_fp"] - per_value["rf_fp"]
    per_value["rf_fp_rate_given_normal_and_value"] = per_value["rf_fp"] / per_value["normal_support"]
    per_value["stack_fp_rate_given_normal_and_value"] = per_value["stack_fp"] / per_value["normal_support"]
    per_value["stack_correct_rate_given_normal_and_value"] = 1 - per_value["stack_fp_rate_given_normal_and_value"]
    per_value = per_value.sort_values("normal_support", ascending=False).reset_index(drop=True)

    long = ctab.reset_index().melt(id_vars="value", var_name="error_group", value_name="n")
    long["pct_feature_value_within_error_group"] = long.apply(
        lambda r: r["n"] / groupsize[r["error_group"]], axis=1
    )
    long = long.rename(columns={"value": feature}).sort_values(
        ["error_group", "n"], ascending=[True, False]
    ).reset_index(drop=True)
    return per_value, long


def sttl_groups(norm: pd.DataFrame) -> pd.DataFrame:
    vals = pd.to_numeric(norm["sttl"], errors="coerce")
    if vals.isna().any():
        raise ValueError("sttl has missing/non-numeric values. Audit before proceeding")
    raw = pd.DataFrame({"group": norm["error_group"], "sttl": vals})
    rows = []
    for name in ["ALL_NORMAL"] + GROUPS:
        sub = raw if name == "ALL_NORMAL" else raw[raw["group"] == name]
        q = sub["sttl"].quantile([0.25, 0.5, 0.75])
        rows.append({
            "group": name, "support": len(sub),
            "sttl_min": float(sub["sttl"].min()),
            "sttl_q1": float(q.loc[0.25]),
            "sttl_median": float(q.loc[0.5]),
            "sttl_q3": float(q.loc[0.75]),
            "sttl_max": float(sub["sttl"].max()),
        })
    return pd.DataFrame(rows)


def write_summary(path: Path, state: pd.DataFrame, proto: pd.DataFrame,
                  sttl: pd.DataFrame, sttl_exact: pd.DataFrame) -> None:
    lines = [
        "# Phase 14 — Step 3: Normal-error feature profiles",
        "",
        "Status: DESCRIPTIVE diagnostic on frozen predictions, not causal inference.",
        "",
        "## Controls checked",
        "- Official test / prediction join by unique `id`: PASS.",
        "- `label` and `attack_cat` agree on every matched id: PASS.",
        "- Both models' confusion matrices exactly match locked Phase 9/11: PASS.",
        "- Normal error groups: 26,719 both correct; 420 Stacking-only correct;",
        "  278 RF-only correct; 9,583 both wrong.",
        "",
        "## How to read these profiles",
        "- `*_group_composition.csv` contains P(feature value | error group).",
        "- `*_by_value.csv` contains model FP rates given NORMAL + feature value.",
        "- These conditionals have DIFFERENT denominators; do not interchange them.",
        "- A feature's association with errors does NOT imply it caused those errors.",
        "- Rare feature values have unstable rates: inspect `normal_support`.",
        "",
        "## Most frequent `state` among Normal traffic (up to 10)",
        "```",
        state[["state", "normal_support", "stack_correct_rf_wrong", "rf_correct_stack_wrong", "rf_fp_rate_given_normal_and_value", "stack_fp_rate_given_normal_and_value"]].head(10).to_string(index=False),
        "```", "",
        "## Most frequent `proto` among Normal traffic (up to 10)",
        "```",
        proto[["proto", "normal_support", "stack_correct_rf_wrong", "rf_correct_stack_wrong", "rf_fp_rate_given_normal_and_value", "stack_fp_rate_given_normal_and_value"]].head(10).to_string(index=False),
        "```", "",
        "## `sttl` median and IQR by group",
        "```",
        sttl[["group", "support", "sttl_q1", "sttl_median", "sttl_q3"]].to_string(index=False),
        "```", "",
        "## Most common exact `sttl` values among Normal traffic",
        "```",
        sttl_exact[["sttl", "normal_support", "stack_correct_rf_wrong", "rf_correct_stack_wrong"]].head(10).to_string(index=False),
        "```", "",
    ]
    fin = state[state["state"].str.upper().eq("FIN")]
    if not fin.empty:
        row = fin.iloc[0]
        lines += [
            "## FIN: distinguish reversed conditional probabilities",
            f"- Among all {EXPECTED['normal']:,} Normal rows, {int(row['normal_support']):,} have state=FIN.",
            f"- Among Normal state=FIN rows, Stacking has FP rate {row['stack_fp_rate_given_normal_and_value']:.3%}.",
            "- The share of FIN in the 420 Stacking-correct/RF-wrong group is in",
            "  `state_group_composition.csv` — a different conditional probability.",
            "",
        ]
    lines += [
        "## Scientific boundaries",
        "- No model refitting or post-test selection; these are diagnostic hypotheses only.",
        "- This step looks at Normal traffic (false alarms), not Fuzzers false negatives.",
        "- State/proto/sttl distributions may be confounded by other traffic properties.",
        "- A high conditional correctness on one subgroup does not prove broad deployment performance.",
        "",
        "## Next checkpoint",
        "Share this output folder for independent checking. After interpretation,",
        "continue to Attack/Fuzzers error profiles, still without modifying models.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = get_args()
    # Never write anything until the two input files are validated and joined.
    pred = read_checked_csv(args.predictions, CORE_PRED_COLS, "saved Phase-9 prediction table")
    test = read_checked_csv(args.test, DATA_COLS, "original official test CSV")
    matched = validated_join(pred, test)

    normal = matched[matched["label_saved"] == 0].copy()
    rf_correct = normal[RF_COL] == 0
    stack_correct = normal[STACK_COL] == 0
    normal["error_group"] = "both_wrong"
    normal.loc[rf_correct & stack_correct, "error_group"] = "both_correct"
    normal.loc[~rf_correct & stack_correct, "error_group"] = "stack_correct_rf_wrong"
    normal.loc[rf_correct & ~stack_correct, "error_group"] = "rf_correct_stack_wrong"

    counts = normal["error_group"].value_counts().to_dict()
    if counts != EXPECTED["normal_groups"]:
        raise ValueError(f"Paired Normal error counts do not match Phase 14 Step 1: {counts}")

    state_by_value, state_composition = profile_by_category(normal, "state")
    proto_by_value, proto_composition = profile_by_category(normal, "proto")
    sttl_summary = sttl_groups(normal)
    sttl_by_value, sttl_composition = profile_by_category(normal, "sttl")

    # Sanity checks ensure each profile reproduces the known paired disagreement counts.
    for name, profile in (("state", state_by_value), ("proto", proto_by_value),
                          ("sttl", sttl_by_value)):
        for col, exp in (("normal_support", 37000),
                         ("stack_correct_rf_wrong", 420),
                         ("rf_correct_stack_wrong", 278)):
            if int(profile[col].sum()) != exp:
                raise ValueError(f"{name} profile failed integrity check for {col}")

    args.out.mkdir(parents=True, exist_ok=True)
    products = {
        "state_by_value.csv": state_by_value,
        "state_group_composition.csv": state_composition,
        "proto_by_value.csv": proto_by_value,
        "proto_group_composition.csv": proto_composition,
        "sttl_group_summary.csv": sttl_summary,
        "sttl_by_value.csv": sttl_by_value,
        "sttl_group_composition.csv": sttl_composition,
    }
    for filename, table in products.items():
        table.to_csv(args.out / filename, index=False, encoding="utf-8")
    write_summary(args.out / "PHASE14_STEP3_SUMMARY.md", state_by_value, proto_by_value,
                  sttl_summary, sttl_by_value)

    print("PASS — 82,332 IDs aligned, labels matched, and frozen counts verified")
    print("Normal: both correct=26,719; Stack fixes RF FP=420; Stack adds FP=278; both wrong=9,583")
    print("No training, tuning, new predictions, or file changes to existing results.")
    print(f"OUTPUT: {args.out}")


if __name__ == "__main__":
    main()
