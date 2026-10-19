# NCKH — Canonical Phase 15 / P15-03 Dataset & Split Provenance

**Scope:** P15-03A local integrity check; P15-03B source/usage attribution. This is **not** a retraining or a repeated official-test evaluation.

## Research evidence and rationale

- Original benchmark: **UNSW-NB15**, *official preset* TRAIN 175,341 rows and TEST 82,332 rows; each 45 columns as recorded in Phase 3.
- Publisher documentation: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- Publisher names the preset train and test CSV files, describes attack categories and the original benchmark context.
- The university page states academic research use is free, commercial use requires agreement with authors, and several research papers should be cited. The latest actual file download URL used by this NCKH project is **UNKNOWN** unless documented separately; publisher documentation by itself does not establish historical download provenance.
- *Do not confuse* original UNSW-NB15 with CIC-UNSW-NB15 or UNSW-NB15 V2/V3 derivative datasets.

## Historical Phase 3 local SHA-256 baseline

Recovered from `snapshot/results/data_audit/unsw_nb15/raw_file_checksums.csv` in the fresh audit snapshot dated 2026-10-10. **These are historical NCKH audit fingerprints, not UNSW-published official checksums.**

| CSV filename | bytes | SHA-256 |
|---|---:|---|
| `UNSW_NB15_training-set.csv` | 32,293,018 | `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa` |
| `UNSW_NB15_testing-set.csv` | 15,380,800 | `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559` |
| `NUSW-NB15_features.csv` | 4,044 | `c55f19cceebb6360dc50f44f8a5f246ccefbcf8a6c604ac1ad46e643869cafce` |

The third filename is intentionally `NUSW-NB15_features.csv` because that is the recorded source filename in this project. Do not rename source data just for this audit.

## What script validates

1. All three original files exist at recorded paths.
2. Each raw file size and full streaming SHA-256 equal historical Phase 3 baseline.
3. TRAIN/TEST CSVs have identical column sequence, 45 fields including `id`, `label`, `attack_cat`, `proto`, `service`, `state`.
4. TRAIN/TEST row counts and binary `label` class counts match the prior dataset audit.
5. Stores report JSON with only aggregate statistics and checksums, without raw records.

The script does **not** recompute feature selection, alter predictions, modify data or touch trained models. A PASS establishes local raw file bitwise identity to the prior Phase 3 audit **only**. It cannot prove the recorded academic source URL is the precise historical download source.

## Checkpoints / Task Board

| ID | Task | Status before user run | Required evidence |
|---|---|---|---|
| P15-03A | Raw file hash, row count and schema cross-check | **AWAITING_USER_RUN** | `p15_03_dataset_integrity.json` with PASS and file hash matches |
| P15-03B | Dataset publication, terms and local download provenance | **PARTIAL** | Publisher page confirmed; exact historical download URL UNKNOWN |
| P15-03 | Entire dataset & split provenance | **PARTIAL** | Close only after P15-03A and source-use reporting are reconciled |

## Decision

No re-download or re-split. Preserve benchmark provided TRAIN and TEST as is. Do not apply test-time tuning or treat novel-vector subset as independent external benchmark.
