# NCKH — Phase 15 P15-01 local inventory verification

**Source supplied by researcher:** `p15_01_inventory.zip`, containing `p15_01_local_inventory.json` (`generated_utc=2026-10-10T18:17:35.021770+00:00`).

## Checked counts

| Check | Present / expected | Status |
|---|---:|---|
| Mapped source scripts | 18 / 18 | PASS |
| Source scripts matching earlier archived SHA-256 | 18 / 18 | PASS, as recorded by local inventory checker |
| Mapped input path checks | 48 / 48 | PASS |
| Representative output path checks | 36 / 36 | PASS |

All 18 entries have `script_found` and `matches_archived_script_sha256=true`. The 48 input and 36 representative output records all report `exists=true` and positive file size. Two nonselected fallback source paths are absent at the project root; their selected source paths `src/analysis/close_original_phase11.py` and `src/analysis/phase14_step1_error_transitions.py` are both present, so those absences do not affect the mapped pipeline.

## Scientific constraints

- **P15-01 DONE**: the bounded task of mapping and confirming the *presence* of known scripts, representative inputs and outputs on the user's local project.
- This verification reviews the *reported inventory*, not a full independent rehash of the user's local files. The hash match flags were calculated by the inventory script on the user's Windows machine.
- `exists=true` and size >0 are NOT checksum/content validation for input CSVs or results. Output checks represent a subset, not every artifact.
- Phase numbering follows canonical 0–20. Historical paths `phase8_controlled`, `phase9_holdout`, `phase10_statistics`, `phase11_results_figures` correspond to canonical Phases 10, 11, 12, and early 16 as mapped in P15-01.
- The frozen official holdout experiment remains frozen. No retraining, retuning, or re-use of official TEST for selection is authorized by this evidence.

## Task board

| ID | Task | Status | Evidence |
|---|---|---|---|
| P15-01A | Entry-point inventory | DONE | 18/18 script paths |
| P15-01B | Script–input–output mapping | DONE | Existing P15-01 map, 48 input checks, 36 output checks |
| P15-01C | Current local state validation | DONE | User's P15-01 JSON, all mapped entries true, hash match flags 18/18 |
| P15-01 | Bounded inventory checkpoint | **DONE** | All A/B/C complete |
| P15-02 | Environment & dependency lock | IN PROGRESS | Snapshot script prepared; local run pending |

## Research decisions log

- **Decision:** Close P15-01 without rerunning any ML scripts. **Reason:** P15-01 concerns artifact locations and source snapshot mapping only. **Evidence:** Uploaded inventory results above. **Consequence:** Local presence is established; numerical reproducibility remains to be established separately.
- **Decision:** Capture current package metadata without automatically constructing a final dependency lock. **Reason:** Installed packages alone do not prove original training versions or compatible transitive dependency resolution. **Evidence:** No independently verified clean-environment replay yet. **Consequence:** P15-02 initially produces a *candidate* environment inventory requiring review.
