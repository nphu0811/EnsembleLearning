#!/usr/bin/env python3
# Canonical Phase 14 — Error Analysis, Step 1: paired error transitions
#
# READ-ONLY INPUT: saved Phase-9 predictions from the three frozen pipelines.
# OUTPUT: aggregate error-transition tables and a short summary.
# Does NOT train, tune, change threshold, select features, or modify Phase-9 data.

from pathlib import Path
import argparse
import pandas as pd

DEFAULT_INPUT = Path(
    "results/final_evaluation/unsw_nb15/phase9_holdout/"
    "tables/official_test_predictions.csv"
)
DEFAULT_OUTPUT = Path(
    "results/final_analysis/unsw_nb15/phase14_error_analysis_step1"
)
RF = "random_forest_42_pred"
STACK = "stacking_42_pred"
EXPECTED = {
    "n": 82332,
    "normal": 37000,
    "attack": 45332,
    "rf": {"tn": 26997, "fp": 10003, "fn": 734, "tp": 44598},
    "stack": {"tn": 27139, "fp": 9861, "fn": 852, "tp": 44480},
    "pair": {
        "both_correct": 71104,
        "rf_only_correct": 491,
        "stack_only_correct": 515,
        "both_wrong": 10222,
    },
}

def analyze(df):
    needed = {"label", "attack_cat", RF, STACK}
    missing = sorted(needed - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in ["label", RF, STACK]:
        if df[col].isna().any() or not set(df[col].unique()).issubset({0, 1}):
            raise ValueError(f"Column {col!r} must contain only binary values 0, 1.")

    if len(df) != EXPECTED["n"]:
        raise ValueError(
            f"Expected {EXPECTED['n']} official TEST rows, received {len(df)}. "
            "Do not use a filtered/subsampled prediction file in Step 1."
        )

    y = df["label"].astype(int)
    rf = df[RF].astype(int)
    st = df[STACK].astype(int)

    if int((y == 0).sum()) != EXPECTED["normal"]:
        raise ValueError("Unexpected Normal support.")
    if int((y == 1).sum()) != EXPECTED["attack"]:
        raise ValueError("Unexpected Attack support.")

    calc_rf = {
        "tn": int(((y == 0) & (rf == 0)).sum()),
        "fp": int(((y == 0) & (rf == 1)).sum()),
        "fn": int(((y == 1) & (rf == 0)).sum()),
        "tp": int(((y == 1) & (rf == 1)).sum()),
    }
    calc_stack = {
        "tn": int(((y == 0) & (st == 0)).sum()),
        "fp": int(((y == 0) & (st == 1)).sum()),
        "fn": int(((y == 1) & (st == 0)).sum()),
        "tp": int(((y == 1) & (st == 1)).sum()),
    }
    if calc_rf != EXPECTED["rf"] or calc_stack != EXPECTED["stack"]:
        raise ValueError(
            "Confusion counts disagree with the frozen Phase-11 output. "
            "Check source/version rather than changing model settings."
        )

    rf_ok = rf.eq(y)
    st_ok = st.eq(y)
    pair = {
        "both_correct": rf_ok & st_ok,
        "rf_only_correct": rf_ok & ~st_ok,
        "stack_only_correct": ~rf_ok & st_ok,
        "both_wrong": ~rf_ok & ~st_ok,
    }
    pair_counts = {k: int(v.sum()) for k, v in pair.items()}
    if pair_counts != EXPECTED["pair"]:
        raise ValueError(
            f"Pairwise counts mismatch: {pair_counts} != {EXPECTED['pair']}"
        )

    rows = []
    for name, mask in [
        ("Normal", y.eq(0)),
        ("Attack", y.eq(1)),
        ("Total", pd.Series(True, index=y.index)),
    ]:
        row = {"true_class": name, "support": int(mask.sum())}
        for k, v in pair.items():
            row[k] = int((mask & v).sum())
        rows.append(row)
    class_transitions = pd.DataFrame(rows)

    attacks = df[y.eq(1)].copy()
    attacks["rf_missed"] = rf[y.eq(1)].eq(0).to_numpy()
    attacks["stack_missed"] = st[y.eq(1)].eq(0).to_numpy()
    attacks["rf_missed_stack_caught"] = (
        attacks["rf_missed"] & ~attacks["stack_missed"]
    )
    attacks["rf_caught_stack_missed"] = (
        ~attacks["rf_missed"] & attacks["stack_missed"]
    )
    attacks["both_missed"] = (
        attacks["rf_missed"] & attacks["stack_missed"]
    )
    profile = attacks.groupby("attack_cat", dropna=False).agg(
        n_attack=("label", "size"),
        rf_false_negatives=("rf_missed", "sum"),
        stacking_false_negatives=("stack_missed", "sum"),
        rf_missed_stack_caught=("rf_missed_stack_caught", "sum"),
        rf_caught_stack_missed=("rf_caught_stack_missed", "sum"),
        both_missed=("both_missed", "sum"),
    ).reset_index()
    profile["fn_difference_stacking_minus_rf"] = (
        profile["stacking_false_negatives"] -
        profile["rf_false_negatives"]
    )
    profile["rf_miss_rate"] = (
        profile["rf_false_negatives"] / profile["n_attack"]
    )
    profile["stacking_miss_rate"] = (
        profile["stacking_false_negatives"] / profile["n_attack"]
    )
    profile = profile.sort_values(
        ["fn_difference_stacking_minus_rf", "n_attack"],
        ascending=[False, False]
    )

    if int(profile["n_attack"].sum()) != EXPECTED["attack"]:
        raise ValueError("Attack-family total does not match official TEST.")
    if int(profile["rf_false_negatives"].sum()) != EXPECTED["rf"]["fn"]:
        raise ValueError("RF false-negative total mismatch.")
    if int(profile["stacking_false_negatives"].sum()) != EXPECTED["stack"]["fn"]:
        raise ValueError("Stacking false-negative total mismatch.")

    return class_transitions, profile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(
            f"Missing input: {args.input}. Run from the NCKH project root "
            "or pass --input with the actual path."
        )

    df = pd.read_csv(
        args.input,
        usecols=["label", "attack_cat", RF, STACK],
        low_memory=False,
    )
    class_transitions, attack_transitions = analyze(df)
    args.out.mkdir(parents=True, exist_ok=True)
    class_transitions.to_csv(args.out / "class_pairwise_transitions.csv", index=False)
    attack_transitions.to_csv(args.out / "attack_family_transitions.csv", index=False)

    n0 = class_transitions.iloc[0]
    n1 = class_transitions.iloc[1]
    notes = f"""# Canonical Phase 14 — Error Analysis, Step 1

## Verified evidence

- Official test samples: {EXPECTED['n']:,}
- RF-only correct: 491
- Stacking-only correct: 515
- Both wrong: 10,222
- Both correct: 71,104
- RF-42 false positives: 10,003
- Stacking-42 false positives: 9,861
- RF-42 false negatives: 734
- Stacking-42 false negatives: 852

## By true class (paired transitions)

Normal traffic (n={n0['support']:,}):
- RF-only correct: {n0['rf_only_correct']:,} (Stacking introduces a false positive)
- Stacking-only correct: {n0['stack_only_correct']:,} (Stacking resolves an RF false positive)

Attack traffic (n={n1['support']:,}):
- RF-only correct: {n1['rf_only_correct']:,} (Stacking introduces a false negative)
- Stacking-only correct: {n1['stack_only_correct']:,} (Stacking catches an attack RF missed)

Net effects: 142 fewer false positives; 118 more false negatives for Stacking.

## Interpretation boundary

These are DESCRIPTIVE error comparisons on the frozen official TEST.
They do not establish the causal mechanism of the Stacking meta learner.
No model/threshold/feature changes are permitted after the holdout.

## Next

Interpret `attack_family_transitions.csv` with family supports and
Wilson uncertainty (already available in canonical Phase 12).
Do not pick a new model from these post-test diagnostic results.
"""
    (args.out / "PHASE14_STEP1_SUMMARY.md").write_text(notes, encoding="utf-8")
    print("PASS — locked Phase-11 counts verified")
    print(class_transitions.to_string(index=False))
    print(f"\nOutput: {args.out}")
    print("Files: class_pairwise_transitions.csv; attack_family_transitions.csv; PHASE14_STEP1_SUMMARY.md")

if __name__ == "__main__":
    main()
