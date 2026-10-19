# P19 safe release audit and internal draft — 17/10/2026

**PARTIAL. INTERNAL_REVIEW_ONLY. Public release BLOCKED.** No artifact deletion,
Git untracking, history rewrite, model loading, training or LICENSE creation.
The P18 checkpoint was committed/pushed as
`ccfde4e56176a212e8108b3de5a3cf869f7861ce` before this package snapshot.

## Three historical smoke artifacts

All are tracked, introduced in initial commit
`c4ed771` (full introducing commit and current Git blob IDs are in the CSV).
Read-only file hashes and lengths agree with the existing smoke `run_metadata.json`.
They came from2000fit/500validation rows of official TRAIN, not full-TRAIN final
models. Their presence is evidence of software smoke, not permission to distribute
models or proof of scientific TEST performance.

| Candidate | Relative path below results/reproducibility/r04_ml_smoke_repaired/ | Bytes | SHA256 |
|---|---|---:|---|
| RF17 | smoke_models/random_forest_17_SMOKE_ONLY.joblib | 411288 | 70f34043cb360acaf8942c7c63f019be6425eac5f68708de9250cf6643532c1a |
| RF42 | smoke_models/random_forest_42_SMOKE_ONLY.joblib | 730001 | b77786277c1a53298330fbe35c0d936fdef164404b3c43c28e2b844f56b7c120 |
| Stack42 | smoke_models/stacking_42_SMOKE_ONLY.joblib | 737273 | be9209ca833eb6667832e9a8a3ee3b6347d5e8b0dc457eed713b496621c59c14 |

Evidence `release/internal_review_draft_2026_10_17_01/smoke_artifact_inventory.csv`
also records tracking, metadata origin, evidence class and exclusion decision.
Files were hashed only, never deserialized. Actual `.joblib` copies remain where
they were. Reconstructed full-TRAIN P15 binaries are separate local artifacts and
are not copied, loaded or assigned historical TEST scores.

The historical `p15_02c2_clean_env.zip` remains absent/untracked in HEAD; deletion
commit is recorded in `historical_zip_status.json`. No archive is restored from
history and no old manifest is rewritten to pretend presence.

## Safe package mechanism

**Index cleanup is unnecessary to make an allowlist release draft.** The script
copies only selected evidence into a new directory. All three smoke binaries are
excluded even while remaining tracked in the repository. `git archive HEAD`
would include tracked files and is not the mechanism used here.

Do not casually commit a tracked-file deletion. A later pull can remove that file
from another checkout's disk. `.gitignore` alone does not change tracked status.
If an owner later chooses cleanup, it needs a separate local-copy preservation,
hash-verification and checkout-impact plan. This session takes no such action.

`tools/p19_safe_review_draft.py` produced a local
`INTERNAL_REVIEW_ONLY_NCKH_DRAFT.zip` with **46 entries**, including45manifest rows
and the manifest itself. It is a reading dossier, not a runnable source release:
some report dependencies/templates and all model/data inputs are deliberately
excluded. The unchanged approved37pagePDF is included only in this local internal
copy and retains its existing SHA. Full paper PDFs/captures and third-party images
are excluded; public ledgers provide links/locators and paraphrased findings.

Fresh package QA **245 PASS / 0 FAIL** checks smoke metadata, original files,
path containment, explicit allowlist, copy/ZIP hashes, CRC, duplicate entries,
internal labels, forbidden artifact classes, limited private-key/token patterns,
unchanged index and unchanged approvedPDF. No actual model or raw data is in the
archive. Pattern triage is limited, not a complete secrets certification.

Local archive SHA256
`2334bfc706a3781b0156b8c9180a3f5b592e4e85a64febf2c21c4fb2afa87fe5`,
533069bytes. Archive and copied contents are Git-ignored. Only inventory,
manifest, validation and review policy/report are committed. This is a fixed
snapshot of selected inputs at package creation; later memory updates do not
silently alter its copied files. `validation.json` records source commit and scope.

## Rights decisions needed from authors/rightsholders

1. Confirm code ownership/contributor consent and choose a code license, if public
   code release is desired. No license has been inferred or added.
2. Decide whether model redistribution is authorized at all. If yes, establish
   dataset-derived/model rights and exact artifact/provenance scope. Default draft
   excludes both smoke and reconstructed binaries.
3. Confirm permission for raw/derived data distribution under the actual dataset
   terms. Until then use official source instructions and restricted allowlists.
4. Confirm which report, institutional template/logo, identities and third-party
   figure/document assets may be publicly distributed. Internal review access is
   not blanket public permission.

These are decisions for a later public release, not a request to approve the
already authorized read-only inventory/internal draft. No public ZIP publication
or repository cleanup is attempted.

## P20 and remaining gates

`defense/REVIEW_PACKET_SETUP_2026-10-17.md` prepares common evidence inputs,
rubric, three future emphasis briefs and evidence-based defense questions.
**No simulated reviewer reports or independent human review were run.** The draft
dossier contains status/QA commentary and must not be presented as a final blind
review packet; freeze a neutral common packet and run isolated contexts only when
dependencies and scope are settled. P20 remains DEFERRED.

P15 remains DONE_SCOPED_RECONSTRUCTION; P16 remains
DONE_SCOPED_AUDIT_WITH_OPEN_PRINT_FINDINGS. P18/P19 PARTIAL. Print/snapshot-age,
source-reading/VOR, original historical environment, rights, proposal/form,
signatures, defense slides/demo and other G0–G6 blockers are not closed by this
mechanical package PASS. No FINAL_NCKH.zip or submission-ready claim.

Independent check `independent_validation.json` adds **121 PASS / 0 FAIL**,
including direct `git cat-file` comparison of the three tracked model blobs with
local bytes, separate ZIP/manifest verification and frozen-input/PDF hashes.
Path safety tests in `tests/test_p19_safe_review_paths.py` pass **3/3**, exercising
traversal, absolute/Windows paths, restricted artifacts and accepted review paths.
Two audit scripts and the tests compile. No ML test or experiment was rerun.
