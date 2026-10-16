"""
UNSW-NB15 Data Audit
====================
Purpose:
    Audit the raw UNSW-NB15 predefined train/test CSV files WITHOUT modifying them.

Expected project structure:
    NCKH/
    ├── data/
    │   └── raw/
    │       └── unsw-nb15/
    │           ├── UNSW_NB15_training-set.csv
    │           ├── UNSW_NB15_testing-set.csv
    │           └── NUSW-NB15_features.csv
    ├── results/
    └── src/
        └── data/
            └── audit_unsw_nb15.py

Outputs:
    results/data_audit/unsw_nb15/
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw" / "unsw-nb15"
RESULT_DIR = PROJECT_ROOT / "results" / "data_audit" / "unsw_nb15"

TRAIN_FILE = DATA_DIR / "UNSW_NB15_training-set.csv"
TEST_FILE = DATA_DIR / "UNSW_NB15_testing-set.csv"
FEATURES_FILE = DATA_DIR / "NUSW-NB15_features.csv"

TARGET_COL = "label"
ATTACK_COL = "attack_cat"

# Columns that should NOT be used when checking exact feature-vector overlap.
# We do not automatically drop them from the dataset here.
OVERLAP_EXCLUDE = {"id", TARGET_COL, ATTACK_COL}

# Simple audit thresholds. These flag columns for review; they do NOT delete them.
NEAR_ZERO_DOMINANCE_THRESHOLD = 0.99
HIGH_CARDINALITY_RATIO_THRESHOLD = 0.95


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------

def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return SHA-256 checksum of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def json_safe(value):
    """Convert numpy/pandas values into JSON-safe Python values."""
    if value is None:
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        if np.isnan(value):
            return None
        if np.isposinf(value):
            return "Infinity"
        if np.isneginf(value):
            return "-Infinity"
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    return value


def save_json(data, path: Path):
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=json_safe),
        encoding="utf-8",
    )


def require_file(path: Path):
    if not path.exists():
        print(f"[ERROR] Missing file: {path}")
        sys.exit(1)


def normalize_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a COPY used only for audit comparisons.
    This does not alter the raw files or the original DataFrame.
    """
    out = df.copy()
    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].astype("string").str.strip()
    return out


def basic_summary(df: pd.DataFrame, name: str) -> dict:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(
        include=["object", "string", "category", "bool"]
    ).columns.tolist()

    return {
        "dataset": name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "memory_mb": round(float(df.memory_usage(deep=True).sum() / 1024**2), 3),
        "numeric_column_count": len(numeric_cols),
        "categorical_column_count": len(categorical_cols),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
    }


def column_profile(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    rows = []

    for col in df.columns:
        s = df[col]
        n = len(s)
        non_null = int(s.notna().sum())
        missing = int(s.isna().sum())
        nunique = int(s.nunique(dropna=True))

        if non_null:
            counts = s.value_counts(dropna=True)
            most_common_count = int(counts.iloc[0]) if len(counts) else 0
            most_common_value = counts.index[0] if len(counts) else None
            dominance = most_common_count / non_null
        else:
            most_common_count = 0
            most_common_value = None
            dominance = np.nan

        rows.append(
            {
                "dataset": dataset_name,
                "column": col,
                "dtype": str(s.dtype),
                "non_null": non_null,
                "missing": missing,
                "missing_pct": round((missing / n * 100) if n else 0, 6),
                "unique_non_null": nunique,
                "unique_ratio": round((nunique / non_null) if non_null else 0, 6),
                "most_common_value": str(most_common_value),
                "most_common_count": most_common_count,
                "dominance_ratio": round(float(dominance), 6)
                if not pd.isna(dominance)
                else None,
                "is_constant": nunique <= 1,
                "near_zero_variance_flag": (
                    nunique > 1
                    and not pd.isna(dominance)
                    and dominance >= NEAR_ZERO_DOMINANCE_THRESHOLD
                ),
                "high_cardinality_flag": (
                    non_null > 0
                    and (nunique / non_null) >= HIGH_CARDINALITY_RATIO_THRESHOLD
                ),
            }
        )

    return pd.DataFrame(rows)


def infinity_report(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    numeric = df.select_dtypes(include=[np.number])
    rows = []

    for col in numeric.columns:
        values = numeric[col].to_numpy(dtype=float, copy=False)
        pos_inf = int(np.isposinf(values).sum())
        neg_inf = int(np.isneginf(values).sum())

        if pos_inf or neg_inf:
            rows.append(
                {
                    "dataset": dataset_name,
                    "column": col,
                    "positive_infinity": pos_inf,
                    "negative_infinity": neg_inf,
                    "total_infinity": pos_inf + neg_inf,
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "dataset",
            "column",
            "positive_infinity",
            "negative_infinity",
            "total_infinity",
        ],
    )


def duplicate_report(df: pd.DataFrame, dataset_name: str) -> dict:
    full_duplicates = int(df.duplicated(keep=False).sum())
    full_duplicate_extra_rows = int(df.duplicated(keep="first").sum())

    feature_cols = [c for c in df.columns if c not in OVERLAP_EXCLUDE]

    if feature_cols:
        feature_duplicates = int(
            df.duplicated(subset=feature_cols, keep=False).sum()
        )
        feature_duplicate_extra_rows = int(
            df.duplicated(subset=feature_cols, keep="first").sum()
        )
    else:
        feature_duplicates = 0
        feature_duplicate_extra_rows = 0

    return {
        "dataset": dataset_name,
        "full_duplicate_rows_including_all_copies": full_duplicates,
        "full_duplicate_extra_rows": full_duplicate_extra_rows,
        "feature_vector_duplicate_rows_including_all_copies": feature_duplicates,
        "feature_vector_duplicate_extra_rows": feature_duplicate_extra_rows,
        "feature_vector_columns_excluded": sorted(OVERLAP_EXCLUDE),
    }


def class_distribution(df: pd.DataFrame, dataset_name: str, col: str) -> pd.DataFrame:
    if col not in df.columns:
        return pd.DataFrame(
            columns=["dataset", "column", "value", "count", "percentage"]
        )

    counts = df[col].value_counts(dropna=False)
    total = len(df)

    rows = []
    for value, count in counts.items():
        rows.append(
            {
                "dataset": dataset_name,
                "column": col,
                "value": str(value),
                "count": int(count),
                "percentage": round(float(count / total * 100), 6)
                if total
                else 0,
            }
        )
    return pd.DataFrame(rows)


def category_shift_report(
    train: pd.DataFrame, test: pd.DataFrame
) -> pd.DataFrame:
    """
    Detect categorical values present in test but unseen in train.
    This matters for future encoders.
    """
    rows = []
    common = [c for c in train.columns if c in test.columns]

    for col in common:
        if (
            pd.api.types.is_object_dtype(train[col])
            or pd.api.types.is_string_dtype(train[col])
            or pd.api.types.is_categorical_dtype(train[col])
        ):
            train_vals = set(train[col].dropna().astype(str).unique())
            test_vals = set(test[col].dropna().astype(str).unique())

            unseen = sorted(test_vals - train_vals)

            rows.append(
                {
                    "column": col,
                    "train_unique": len(train_vals),
                    "test_unique": len(test_vals),
                    "unseen_in_train_count": len(unseen),
                    "unseen_in_train_values": " | ".join(unseen[:50]),
                }
            )

    return pd.DataFrame(rows)


def train_test_overlap(
    train: pd.DataFrame, test: pd.DataFrame
) -> dict:
    """
    Check exact overlap of feature vectors between train and test.
    Excludes id, label and attack_cat.
    Uses row hashes to avoid an expensive full merge.
    """
    common_cols = [
        c
        for c in train.columns
        if c in test.columns and c not in OVERLAP_EXCLUDE
    ]

    if not common_cols:
        return {
            "common_feature_columns_used": [],
            "train_rows_with_vector_seen_in_test": 0,
            "test_rows_with_vector_seen_in_train": 0,
            "unique_overlapping_feature_vectors": 0,
        }

    train_view = normalize_string_columns(train[common_cols])
    test_view = normalize_string_columns(test[common_cols])

    train_hash = pd.util.hash_pandas_object(
        train_view, index=False, categorize=True
    )
    test_hash = pd.util.hash_pandas_object(
        test_view, index=False, categorize=True
    )

    train_unique_hash = set(train_hash.unique().tolist())
    test_unique_hash = set(test_hash.unique().tolist())
    overlap_hashes = train_unique_hash.intersection(test_unique_hash)

    return {
        "common_feature_columns_used": common_cols,
        "excluded_columns": sorted(OVERLAP_EXCLUDE),
        "train_rows_with_vector_seen_in_test": int(train_hash.isin(overlap_hashes).sum()),
        "test_rows_with_vector_seen_in_train": int(test_hash.isin(overlap_hashes).sum()),
        "unique_overlapping_feature_vectors": len(overlap_hashes),
    }


def label_attack_crosstab(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    if TARGET_COL not in df.columns or ATTACK_COL not in df.columns:
        return pd.DataFrame()

    table = pd.crosstab(
        df[ATTACK_COL].astype("string"),
        df[TARGET_COL],
        dropna=False,
    )
    table.insert(0, "attack_cat", table.index.astype(str))
    table.insert(0, "dataset", dataset_name)
    table = table.reset_index(drop=True)
    return table


def suspicious_columns(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Flag columns for manual review. This function NEVER drops anything.
    """
    rows = []
    n = max(len(df), 1)

    for col in df.columns:
        reasons = []
        name = col.lower().strip()
        nunique = df[col].nunique(dropna=True)
        unique_ratio = nunique / n

        if name in {"id", "index", "row_id", "record_id"}:
            reasons.append("identifier-like column name")

        if col == ATTACK_COL:
            reasons.append(
                "potential target leakage for binary classification because it encodes attack category"
            )

        if col == TARGET_COL:
            reasons.append("target column; must never be used as an input feature")

        if unique_ratio >= HIGH_CARDINALITY_RATIO_THRESHOLD:
            reasons.append("very high cardinality / possibly identifier-like")

        if any(token in name for token in ["timestamp", "time_stamp"]):
            reasons.append(
                "time-related field; may require split-aware handling rather than ordinary feature use"
            )

        if reasons:
            rows.append(
                {
                    "dataset": dataset_name,
                    "column": col,
                    "dtype": str(df[col].dtype),
                    "unique_non_null": int(nunique),
                    "unique_ratio": round(unique_ratio, 6),
                    "review_reason": "; ".join(reasons),
                }
            )

    return pd.DataFrame(rows)


def read_csv(path: Path, name: str) -> pd.DataFrame:
    print(f"[LOAD] {name}: {path}")
    df = pd.read_csv(path, low_memory=False)

    # Strip whitespace from column names only in memory.
    # Raw CSV is never rewritten.
    df.columns = [str(c).strip() for c in df.columns]

    print(f"       rows={len(df):,}, columns={len(df.columns)}")
    return df


# ---------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------

def main():
    print("=" * 72)
    print("UNSW-NB15 RAW DATA AUDIT")
    print("This script READS raw CSV files but NEVER modifies them.")
    print("=" * 72)

    require_file(TRAIN_FILE)
    require_file(TEST_FILE)

    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    train = read_csv(TRAIN_FILE, "TRAIN")
    test = read_csv(TEST_FILE, "TEST")

    # --------------------------------------------------------------
    # 1. Provenance
    # --------------------------------------------------------------
    print("\n[1/10] Computing raw-file checksums...")
    files = [TRAIN_FILE, TEST_FILE]
    if FEATURES_FILE.exists():
        files.append(FEATURES_FILE)

    provenance_rows = []
    for path in files:
        stat = path.stat()
        provenance_rows.append(
            {
                "file": path.name,
                "relative_path": str(path.relative_to(PROJECT_ROOT)),
                "size_bytes": stat.st_size,
                "sha256": sha256_file(path),
            }
        )

    provenance_df = pd.DataFrame(provenance_rows)
    provenance_df.to_csv(RESULT_DIR / "raw_file_checksums.csv", index=False)

    # --------------------------------------------------------------
    # 2. Schema
    # --------------------------------------------------------------
    print("[2/10] Checking schema...")
    train_cols = train.columns.tolist()
    test_cols = test.columns.tolist()

    schema = {
        "train_only_columns": sorted(set(train_cols) - set(test_cols)),
        "test_only_columns": sorted(set(test_cols) - set(train_cols)),
        "same_column_set": set(train_cols) == set(test_cols),
        "same_column_order": train_cols == test_cols,
        "train_columns": train_cols,
        "test_columns": test_cols,
    }
    save_json(schema, RESULT_DIR / "schema_comparison.json")

    # --------------------------------------------------------------
    # 3. Dataset summaries / dtypes
    # --------------------------------------------------------------
    print("[3/10] Profiling columns and data types...")
    summaries = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "train": basic_summary(train, "train"),
        "test": basic_summary(test, "test"),
    }
    save_json(summaries, RESULT_DIR / "dataset_summary.json")

    profiles = pd.concat(
        [
            column_profile(train, "train"),
            column_profile(test, "test"),
        ],
        ignore_index=True,
    )
    profiles.to_csv(RESULT_DIR / "column_profile.csv", index=False)

    # --------------------------------------------------------------
    # 4. Missing values
    # --------------------------------------------------------------
    print("[4/10] Checking missing values...")
    missing = profiles.loc[
        profiles["missing"] > 0,
        ["dataset", "column", "dtype", "missing", "missing_pct"],
    ].copy()
    missing.to_csv(RESULT_DIR / "missing_values.csv", index=False)

    # --------------------------------------------------------------
    # 5. Infinity
    # --------------------------------------------------------------
    print("[5/10] Checking +/- infinity...")
    inf = pd.concat(
        [
            infinity_report(train, "train"),
            infinity_report(test, "test"),
        ],
        ignore_index=True,
    )
    inf.to_csv(RESULT_DIR / "infinite_values.csv", index=False)

    # --------------------------------------------------------------
    # 6. Duplicates
    # --------------------------------------------------------------
    print("[6/10] Checking duplicate records...")
    duplicates = {
        "train": duplicate_report(train, "train"),
        "test": duplicate_report(test, "test"),
    }
    save_json(duplicates, RESULT_DIR / "duplicate_summary.json")

    # --------------------------------------------------------------
    # 7. Labels / attack categories
    # --------------------------------------------------------------
    print("[7/10] Checking class distributions...")
    distributions = pd.concat(
        [
            class_distribution(train, "train", TARGET_COL),
            class_distribution(test, "test", TARGET_COL),
            class_distribution(train, "train", ATTACK_COL),
            class_distribution(test, "test", ATTACK_COL),
        ],
        ignore_index=True,
    )
    distributions.to_csv(RESULT_DIR / "class_distribution.csv", index=False)

    crosstab = pd.concat(
        [
            label_attack_crosstab(train, "train"),
            label_attack_crosstab(test, "test"),
        ],
        ignore_index=True,
    )
    crosstab.to_csv(RESULT_DIR / "label_attack_crosstab.csv", index=False)

    # --------------------------------------------------------------
    # 8. Constant / NZV / suspicious fields
    # --------------------------------------------------------------
    print("[8/10] Flagging constant, near-zero-variance and suspicious columns...")
    flagged = profiles.loc[
        profiles["is_constant"]
        | profiles["near_zero_variance_flag"]
        | profiles["high_cardinality_flag"]
    ].copy()
    flagged.to_csv(RESULT_DIR / "flagged_columns.csv", index=False)

    suspicious = pd.concat(
        [
            suspicious_columns(train, "train"),
            suspicious_columns(test, "test"),
        ],
        ignore_index=True,
    )
    suspicious.to_csv(RESULT_DIR / "suspicious_columns.csv", index=False)

    # --------------------------------------------------------------
    # 9. Train/test category shift and exact overlap
    # --------------------------------------------------------------
    print("[9/10] Checking train/test category shift and feature-vector overlap...")
    category_shift = category_shift_report(train, test)
    category_shift.to_csv(
        RESULT_DIR / "categorical_train_test_shift.csv", index=False
    )

    overlap = train_test_overlap(train, test)
    save_json(overlap, RESULT_DIR / "train_test_overlap.json")

    # --------------------------------------------------------------
    # 10. Human-readable report
    # --------------------------------------------------------------
    print("[10/10] Writing audit report...")

    train_label_dist = (
        train[TARGET_COL].value_counts(dropna=False).to_dict()
        if TARGET_COL in train.columns
        else {}
    )
    test_label_dist = (
        test[TARGET_COL].value_counts(dropna=False).to_dict()
        if TARGET_COL in test.columns
        else {}
    )

    train_attack_count = (
        int(train[ATTACK_COL].nunique(dropna=False))
        if ATTACK_COL in train.columns
        else None
    )
    test_attack_count = (
        int(test[ATTACK_COL].nunique(dropna=False))
        if ATTACK_COL in test.columns
        else None
    )

    lines = [
        "UNSW-NB15 DATA AUDIT REPORT",
        "=" * 72,
        "",
        "IMPORTANT:",
        "- No cleaning was performed.",
        "- No feature was deleted.",
        "- No encoder/scaler/resampler/model was fitted.",
        "- Raw CSV files were not modified.",
        "",
        "1. SHAPE",
        f"Train: {train.shape[0]:,} rows x {train.shape[1]} columns",
        f"Test : {test.shape[0]:,} rows x {test.shape[1]} columns",
        "",
        "2. SCHEMA",
        f"Same column set  : {schema['same_column_set']}",
        f"Same column order: {schema['same_column_order']}",
        f"Train-only cols  : {schema['train_only_columns']}",
        f"Test-only cols   : {schema['test_only_columns']}",
        "",
        "3. MISSING / INFINITY",
        f"Columns with missing values: {missing['column'].nunique() if not missing.empty else 0}",
        f"Columns with infinity: {inf['column'].nunique() if not inf.empty else 0}",
        "",
        "4. DUPLICATES",
        f"Train full duplicate extra rows: {duplicates['train']['full_duplicate_extra_rows']:,}",
        f"Test full duplicate extra rows : {duplicates['test']['full_duplicate_extra_rows']:,}",
        f"Train feature-vector duplicate extra rows: {duplicates['train']['feature_vector_duplicate_extra_rows']:,}",
        f"Test feature-vector duplicate extra rows : {duplicates['test']['feature_vector_duplicate_extra_rows']:,}",
        "",
        "5. TARGET",
        f"Train label distribution: {train_label_dist}",
        f"Test label distribution : {test_label_dist}",
        f"Train attack categories : {train_attack_count}",
        f"Test attack categories  : {test_attack_count}",
        "",
        "6. TRAIN/TEST EXACT FEATURE-VECTOR OVERLAP",
        f"Unique overlapping feature vectors: {overlap['unique_overlapping_feature_vectors']:,}",
        f"Train rows whose vector also appears in test: {overlap['train_rows_with_vector_seen_in_test']:,}",
        f"Test rows whose vector also appears in train: {overlap['test_rows_with_vector_seen_in_train']:,}",
        f"Excluded from overlap comparison: {overlap.get('excluded_columns', [])}",
        "",
        "7. FLAGGED COLUMNS",
        f"Flagged constant/NZV/high-cardinality rows: {len(flagged):,}",
        f"Suspicious-column audit rows: {len(suspicious):,}",
        "",
        "NEXT STEP:",
        "Review these findings BEFORE deciding what to clean/drop/encode/scale.",
        "",
        f"Output directory: {RESULT_DIR}",
    ]

    report_path = RESULT_DIR / "audit_report.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 72)
    print("\n".join(lines))
    print("=" * 72)
    print("\n[DONE] Audit completed successfully.")
    print(f"[OUTPUT] {RESULT_DIR}")


if __name__ == "__main__":
    main()
