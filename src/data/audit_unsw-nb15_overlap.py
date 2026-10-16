"""
UNSW-NB15 Duplicate / Overlap Consistency Audit
================================================
Purpose:
    Investigate duplicate feature vectors and train/test overlap discovered
    in the first audit BEFORE deleting or cleaning anything.

This script:
    - does NOT modify raw data
    - does NOT drop duplicates
    - does NOT fit preprocessing/modeling components

Outputs:
    results/data_audit/unsw_nb15_overlap/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw" / "unsw-nb15"
RESULT_DIR = PROJECT_ROOT / "results" / "data_audit" / "unsw_nb15_overlap"

TRAIN_FILE = DATA_DIR / "UNSW_NB15_training-set.csv"
TEST_FILE = DATA_DIR / "UNSW_NB15_testing-set.csv"

ID_COL = "id"
TARGET_COL = "label"
ATTACK_COL = "attack_cat"
EXCLUDED_FROM_VECTOR = {ID_COL, TARGET_COL, ATTACK_COL}


def require_file(path: Path):
    if not path.exists():
        print(f"[ERROR] Missing file: {path}")
        sys.exit(1)


def read_csv(path: Path, name: str) -> pd.DataFrame:
    print(f"[LOAD] {name}: {path}")
    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]

    # In-memory normalization only; raw file is untouched.
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()

    print(f"       rows={len(df):,}, columns={len(df.columns)}")
    return df


def add_feature_hash(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    out["_feature_hash"] = pd.util.hash_pandas_object(
        out[feature_cols],
        index=False,
        categorize=True,
    ).astype("uint64")
    return out


def within_split_summary(df: pd.DataFrame, split: str) -> tuple[dict, pd.DataFrame]:
    group = df.groupby("_feature_hash", sort=False)

    stats = group.agg(
        row_count=("_feature_hash", "size"),
        label_nunique=(TARGET_COL, "nunique"),
        attack_nunique=(ATTACK_COL, "nunique"),
    )

    duplicate_groups = stats[stats["row_count"] > 1].copy()
    label_conflicts = duplicate_groups[duplicate_groups["label_nunique"] > 1]
    attack_conflicts = duplicate_groups[duplicate_groups["attack_nunique"] > 1]

    duplicate_rows = int(
        df["_feature_hash"].isin(duplicate_groups.index).sum()
    )
    extra_duplicate_rows = int(
        (duplicate_groups["row_count"] - 1).sum()
    )

    summary = {
        "split": split,
        "rows": int(len(df)),
        "unique_feature_vectors": int(df["_feature_hash"].nunique()),
        "duplicate_feature_vector_groups": int(len(duplicate_groups)),
        "rows_inside_duplicate_groups": duplicate_rows,
        "extra_duplicate_rows": extra_duplicate_rows,
        "duplicate_row_pct": round(duplicate_rows / len(df) * 100, 6),
        "label_conflict_groups": int(len(label_conflicts)),
        "attack_category_conflict_groups": int(len(attack_conflicts)),
    }

    conflicts = duplicate_groups[
        (duplicate_groups["label_nunique"] > 1)
        | (duplicate_groups["attack_nunique"] > 1)
    ].reset_index()

    if not conflicts.empty:
        conflict_hashes = set(conflicts["_feature_hash"].tolist())
        details = (
            df[df["_feature_hash"].isin(conflict_hashes)]
            [[ID_COL, TARGET_COL, ATTACK_COL, "_feature_hash"]]
            .sort_values(["_feature_hash", TARGET_COL, ATTACK_COL, ID_COL])
        )
    else:
        details = pd.DataFrame(
            columns=[ID_COL, TARGET_COL, ATTACK_COL, "_feature_hash"]
        )

    return summary, details


def exact_labeled_duplicate_summary(df: pd.DataFrame, split: str) -> dict:
    """
    Duplicate row after excluding only the artificial id.
    This means features + attack_cat + label are identical.
    """
    subset = [c for c in df.columns if c not in {ID_COL, "_feature_hash"}]

    extra = int(df.duplicated(subset=subset, keep="first").sum())
    all_copies = int(df.duplicated(subset=subset, keep=False).sum())

    return {
        "split": split,
        "duplicate_rows_excluding_id_including_all_copies": all_copies,
        "extra_duplicate_rows_excluding_id": extra,
        "extra_duplicate_pct": round(extra / len(df) * 100, 6),
    }


def cross_split_analysis(
    train: pd.DataFrame, test: pd.DataFrame
) -> tuple[dict, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_hashes = set(train["_feature_hash"].unique().tolist())
    test_hashes = set(test["_feature_hash"].unique().tolist())
    overlap = train_hashes & test_hashes

    train_overlap = train[train["_feature_hash"].isin(overlap)].copy()
    test_overlap = test[test["_feature_hash"].isin(overlap)].copy()

    train_meta = (
        train_overlap.groupby("_feature_hash")
        .agg(
            train_rows=("_feature_hash", "size"),
            train_label_nunique=(TARGET_COL, "nunique"),
            train_attack_nunique=(ATTACK_COL, "nunique"),
            train_labels=(TARGET_COL, lambda s: "|".join(map(str, sorted(set(s))))),
            train_attacks=(ATTACK_COL, lambda s: "|".join(sorted(set(map(str, s))))),
        )
    )

    test_meta = (
        test_overlap.groupby("_feature_hash")
        .agg(
            test_rows=("_feature_hash", "size"),
            test_label_nunique=(TARGET_COL, "nunique"),
            test_attack_nunique=(ATTACK_COL, "nunique"),
            test_labels=(TARGET_COL, lambda s: "|".join(map(str, sorted(set(s))))),
            test_attacks=(ATTACK_COL, lambda s: "|".join(sorted(set(map(str, s))))),
        )
    )

    comparison = train_meta.join(test_meta, how="inner").reset_index()

    comparison["label_sets_match"] = (
        comparison["train_labels"] == comparison["test_labels"]
    )
    comparison["attack_sets_match"] = (
        comparison["train_attacks"] == comparison["test_attacks"]
    )

    summary = {
        "unique_overlapping_feature_vectors": int(len(overlap)),
        "train_rows_in_overlap": int(len(train_overlap)),
        "test_rows_in_overlap": int(len(test_overlap)),
        "train_overlap_pct": round(len(train_overlap) / len(train) * 100, 6),
        "test_overlap_pct": round(len(test_overlap) / len(test) * 100, 6),
        "overlap_vectors_with_different_label_sets": int(
            (~comparison["label_sets_match"]).sum()
        ),
        "overlap_vectors_with_different_attack_sets": int(
            (~comparison["attack_sets_match"]).sum()
        ),
    }

    conflicts = comparison[
        (~comparison["label_sets_match"])
        | (~comparison["attack_sets_match"])
    ].copy()

    train_by_attack = (
        train_overlap.groupby([ATTACK_COL, TARGET_COL], dropna=False)
        .size()
        .reset_index(name="overlap_rows")
    )
    train_by_attack.insert(0, "split", "train")

    test_by_attack = (
        test_overlap.groupby([ATTACK_COL, TARGET_COL], dropna=False)
        .size()
        .reset_index(name="overlap_rows")
    )
    test_by_attack.insert(0, "split", "test")

    overlap_by_attack = pd.concat(
        [train_by_attack, test_by_attack],
        ignore_index=True,
    )

    return summary, comparison, conflicts, overlap_by_attack


def main():
    print("=" * 76)
    print("UNSW-NB15 DUPLICATE / CROSS-SPLIT CONSISTENCY AUDIT")
    print("NO CLEANING OR DELETION WILL BE PERFORMED")
    print("=" * 76)

    require_file(TRAIN_FILE)
    require_file(TEST_FILE)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    train = read_csv(TRAIN_FILE, "TRAIN")
    test = read_csv(TEST_FILE, "TEST")

    common_cols = [c for c in train.columns if c in test.columns]
    feature_cols = [c for c in common_cols if c not in EXCLUDED_FROM_VECTOR]

    print(f"\n[INFO] Feature-vector columns used: {len(feature_cols)}")
    print(f"[INFO] Excluded: {sorted(EXCLUDED_FROM_VECTOR)}")

    train = add_feature_hash(train, feature_cols)
    test = add_feature_hash(test, feature_cols)

    print("\n[1/4] Checking duplicate consistency within TRAIN...")
    train_summary, train_conflicts = within_split_summary(train, "train")

    print("[2/4] Checking duplicate consistency within TEST...")
    test_summary, test_conflicts = within_split_summary(test, "test")

    print("[3/4] Checking exact labeled duplicates excluding id...")
    labeled_dup = {
        "train": exact_labeled_duplicate_summary(train, "train"),
        "test": exact_labeled_duplicate_summary(test, "test"),
    }

    print("[4/4] Checking train/test overlap label consistency...")
    cross_summary, comparison, cross_conflicts, overlap_by_attack = (
        cross_split_analysis(train, test)
    )

    (RESULT_DIR / "within_train_conflicts.csv").write_text(
        train_conflicts.to_csv(index=False), encoding="utf-8"
    )
    (RESULT_DIR / "within_test_conflicts.csv").write_text(
        test_conflicts.to_csv(index=False), encoding="utf-8"
    )
    comparison.to_csv(
        RESULT_DIR / "cross_split_overlap_vectors.csv",
        index=False,
    )
    cross_conflicts.to_csv(
        RESULT_DIR / "cross_split_conflicts.csv",
        index=False,
    )
    overlap_by_attack.to_csv(
        RESULT_DIR / "cross_split_overlap_by_attack.csv",
        index=False,
    )

    all_summary = {
        "feature_vector_column_count": len(feature_cols),
        "feature_vector_columns": feature_cols,
        "excluded_columns": sorted(EXCLUDED_FROM_VECTOR),
        "within_train": train_summary,
        "within_test": test_summary,
        "exact_labeled_duplicates_excluding_id": labeled_dup,
        "cross_split": cross_summary,
    }

    (RESULT_DIR / "overlap_consistency_summary.json").write_text(
        json.dumps(all_summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "UNSW-NB15 DUPLICATE / OVERLAP CONSISTENCY REPORT",
        "=" * 76,
        "",
        "IMPORTANT:",
        "- No raw row was deleted.",
        "- No feature was deleted.",
        "- This audit only determines whether duplicate/overlapping vectors",
        "  carry consistent labels and attack categories.",
        "",
        "WITHIN TRAIN",
        f"Duplicate vector groups: {train_summary['duplicate_feature_vector_groups']:,}",
        f"Rows inside duplicate groups: {train_summary['rows_inside_duplicate_groups']:,}",
        f"Extra duplicate rows: {train_summary['extra_duplicate_rows']:,}",
        f"Groups with conflicting labels: {train_summary['label_conflict_groups']:,}",
        f"Groups with conflicting attack categories: {train_summary['attack_category_conflict_groups']:,}",
        "",
        "WITHIN TEST",
        f"Duplicate vector groups: {test_summary['duplicate_feature_vector_groups']:,}",
        f"Rows inside duplicate groups: {test_summary['rows_inside_duplicate_groups']:,}",
        f"Extra duplicate rows: {test_summary['extra_duplicate_rows']:,}",
        f"Groups with conflicting labels: {test_summary['label_conflict_groups']:,}",
        f"Groups with conflicting attack categories: {test_summary['attack_category_conflict_groups']:,}",
        "",
        "CROSS TRAIN/TEST",
        f"Unique overlapping vectors: {cross_summary['unique_overlapping_feature_vectors']:,}",
        f"Train rows involved: {cross_summary['train_rows_in_overlap']:,} "
        f"({cross_summary['train_overlap_pct']:.3f}%)",
        f"Test rows involved: {cross_summary['test_rows_in_overlap']:,} "
        f"({cross_summary['test_overlap_pct']:.3f}%)",
        f"Overlap vectors with different labels: "
        f"{cross_summary['overlap_vectors_with_different_label_sets']:,}",
        f"Overlap vectors with different attack categories: "
        f"{cross_summary['overlap_vectors_with_different_attack_sets']:,}",
        "",
        "NEXT:",
        "Use these results to decide whether duplicates should be preserved,",
        "removed only from training, or handled as a separate leakage-sensitivity",
        "evaluation track. Do not decide from duplicate count alone.",
    ]

    report = "\n".join(lines)
    (RESULT_DIR / "overlap_consistency_report.txt").write_text(
        report, encoding="utf-8"
    )

    print("\n" + report)
    print("\n[DONE]")
    print(f"[OUTPUT] {RESULT_DIR}")


if __name__ == "__main__":
    main()
