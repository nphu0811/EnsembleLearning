"""
Build UNSW-NB15 evaluation views without modifying raw data.

Creates:
  data/interim/unsw-nb15/test_unseen_vectors.csv
  results/data_audit/unsw_nb15_views/view_summary.json

The official raw train/test CSV files remain untouched.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "unsw-nb15"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim" / "unsw-nb15"
RESULT_DIR = PROJECT_ROOT / "results" / "data_audit" / "unsw_nb15_views"

TRAIN_FILE = RAW_DIR / "UNSW_NB15_training-set.csv"
TEST_FILE = RAW_DIR / "UNSW_NB15_testing-set.csv"

EXCLUDE_FROM_VECTOR = {"id", "attack_cat", "label"}


def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].astype("string").str.strip()
    return out


def feature_hash(df: pd.DataFrame, feature_cols: list[str]) -> pd.Series:
    view = normalize_strings(df[feature_cols])
    return pd.util.hash_pandas_object(view, index=False, categorize=True)


def main():
    if not TRAIN_FILE.exists() or not TEST_FILE.exists():
        raise FileNotFoundError(
            "Could not find UNSW-NB15 raw train/test files under "
            f"{RAW_DIR}"
        )

    train = pd.read_csv(TRAIN_FILE, low_memory=False)
    test = pd.read_csv(TEST_FILE, low_memory=False)

    train.columns = [str(c).strip() for c in train.columns]
    test.columns = [str(c).strip() for c in test.columns]

    if set(train.columns) != set(test.columns):
        raise ValueError("Train and test schema do not match.")

    feature_cols = [
        c for c in train.columns
        if c in test.columns and c not in EXCLUDE_FROM_VECTOR
    ]

    train_hash = feature_hash(train, feature_cols)
    test_hash = feature_hash(test, feature_cols)

    train_hash_set = set(train_hash.unique().tolist())
    overlap_mask = test_hash.isin(train_hash_set)
    novel_mask = ~overlap_mask

    novel_test = test.loc[novel_mask].copy()

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    out_csv = INTERIM_DIR / "test_unseen_vectors.csv"
    novel_test.to_csv(out_csv, index=False)

    overlap_ids = test.loc[overlap_mask, ["id", "attack_cat", "label"]].copy()
    overlap_ids.to_csv(RESULT_DIR / "test_overlap_rows.csv", index=False)

    summary = {
        "official_train_rows": int(len(train)),
        "official_test_rows": int(len(test)),
        "feature_vector_columns": feature_cols,
        "feature_vector_column_count": len(feature_cols),
        "overlapping_test_rows": int(overlap_mask.sum()),
        "overlapping_test_pct": round(float(overlap_mask.mean() * 100), 6),
        "novel_vector_test_rows": int(novel_mask.sum()),
        "novel_vector_test_pct": round(float(novel_mask.mean() * 100), 6),
        "raw_files_modified": False,
        "purpose": (
            "Secondary leakage/repetition sensitivity evaluation only; "
            "does not replace official test."
        ),
    }

    (RESULT_DIR / "view_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 72)
    print("UNSW-NB15 EVALUATION VIEWS")
    print("=" * 72)
    print(f"Official train       : {len(train):,}")
    print(f"Official test        : {len(test):,}")
    print(
        f"Seen-in-train test   : {overlap_mask.sum():,} "
        f"({overlap_mask.mean()*100:.3f}%)"
    )
    print(f"Novel-vector test    : {novel_mask.sum():,}")
    print()
    print("Raw data modified    : NO")
    print(f"Created              : {out_csv}")
    print(f"Summary              : {RESULT_DIR / 'view_summary.json'}")


if __name__ == "__main__":
    main()
