# P19 — Current Data/Code Availability supplement (16/10/2026)

**Supplemental check of public GitHub at commit `3007fe407abf760fbbc75df23b4376d4a24f9368`.** Preserve `docs/research/DATA_CODE_AVAILABILITY.md` as older historical draft; its statement that no public repository exists is now **outdated**.

## Code availability — now publicly visible, licensing not closed

- Source: https://github.com/nphu0811/EnsembleLearning, branch `main`; specific source snapshot (this audit) `3007fe407abf760fbbc75df23b4376d4a24f9368`.
- GitHub API reports visibility `public`. Source code and tooling under `src/`, `tools/`, `tests/` plus documentation and several derived/frozen aggregate results are tracked in the repo.
- **No top-level LICENSE/LICENCE/COPYING file found** in tracked tree. Public visibility does **not** automatically create an open-source license or grant redistribution rights. The author must choose and approve an appropriate code license only after checking provenance/third-party material.
- No immutable scholarly release DOI or stable archive version has been verified. Reference the exact commit when communicating the state of code that supports a manuscript.

## Data availability — source citation rather than repackaging raw data

- Official dataset: https://research.unsw.edu.au/projects/unsw-nb15-dataset. Research uses the official UNSW-NB15 train/test split (175,341/82,332), and the source page's academic-use conditions must be respected; do not assign a new license to UNSW raw data.
- `data/raw/`, `data/interim/`, `data/processed/` are listed in `.gitignore`; current tracked tree has **0 paths under `data/raw/`**. Therefore the public GitHub checkout **cannot by itself rerun full model fitting from raw traffic without separately obtaining the permitted dataset**.
- Frozen aggregate performance/paired statistics and figure source data are tracked, but they do not prove historical full-model reproduction. Dataset hash audits match the local prior snapshot, not a vendor-issued checksum.
- `results/reproducibility/r04_ml_smoke*/smoke_models/` currently contains **six tracked .joblib paths (two copies of three SMOKE_ONLY models)**. They are TRAIN-subset software-test artifacts, **not** serialized full-TRAIN final RF/Stacking models. Do not advertise or deploy them as final trained IDS.
- Historical environment versions for the final run are UNKNOWN. P15 clean smoke/replay and source QA do not establish exact historical end-to-end reproduction.

## Public-sharing triage, not cleanup authorization

- `NCKH_SHARE_FOR_REVIEW/` contains 10 tracked files including ZIP archives and inventory; the earlier r05 audit flagged path/email/template metadata and did not comprehensively certify public distribution. Re-audit permissions and personal traces before promoting this repo to a public archival release.
- A public repo's history may retain content even after deleting a tracked path. **This note does not delete, move, untrack or rewrite anything.** The user has reserved cleanup decisions for local Windows+Git synchronization.
- No evidence of a completed independent redistribution-rights and secrets/privacy clearance has been established by this check.

## Proposed wording for a later manuscript (conditional)

> The analysis code and selected derived evidence are available in the project's public GitHub repository at a version-specific commit. The raw UNSW-NB15 records are not distributed with this code and should be obtained via the dataset owners subject to their conditions. The original historical model-training environment and full-model serialized artifacts are not yet available for bitwise or full-training reproduction; source and aggregate replay have been audited separately.

This wording must be revisited after license/public-sharing approval, repository clean-up, frozen release tagging and final PDF verification. It is not a claim of FAIR compliance or license clearance.

**P19 STATUS: PARTIAL — PUBLIC_REPO_CONFIRMED, RIGHTS/LICENSE/RELEASE_PROVENANCE_OPEN.** G0–G6 and P20 remain incomplete.
