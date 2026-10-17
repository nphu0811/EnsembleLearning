# P18 current-report citation audit — 17/10/2026

**DONE_SCOPED_OFFLINE_AUDIT; P18 overall PARTIAL.** Applied the installed
`nature-ref-verifier` workflow to current BibTeX, saved field-verification records,
actual citation locations, and recorded reading scopes. No fresh network queries,
new source search or whole-paper reading occurred in this task.

`tools/p18_current_report_citation_audit.py` returned **119 PASS / 0 FAIL**.
The report has 12 distinct cited records, 12 distinct DOI values and 24 citation-key
instances. No orphan, undefined or duplicate key was found. Eleven legacy records
match saved verified ledger fields for ordered authors, title, DOI, publication
year, venue, volume, issue and pages/article number. U01 matches the existing
dataset bibliography record and inherits the documented institutional page-range
follow-up. The conflicting L03 is not accidentally cited.

Evidence in `literature/report_audit_2026_10_17_01/` contains a reading ledger,
all 24 source-linked claim contexts, source SHA-256 manifest and validation JSON.
The PDF bibliography was visually inspected on physical pages 36–37 in the P16
review. Current report bibliography files were left unchanged.

## Claim-to-source assessment

| Source | Report use | Evidence boundary / disposition |
|---|---|---|
| L01 | IDS ensemble literature overview | Existing metadata/abstract boundary only; supports topic attribution, not a complete systematic-review replication |
| L02 | Need to audit IDS datasets | Existing selected abstract/intro/methods; case is CICIDS2017, not proof of UNSW errors |
| L04–L06 | Existing ensemble and stacking approaches | Attribute the studied approach; no harmonized numeric superiority comparison across different protocols |
| L07 | Dynamic ensemble and imbalance | Demonstrates that imbalance has prior work; does not establish a resampling effect for this project |
| L08, L11, L12 | Feature-selection/normalization/correlation literature | Supports topic/approach attribution within saved reading bounds; cannot isolate the cause of RF17 performance |
| L09 | Within-dataset versus cross-dataset validity | Existing selected source passage; does not turn novel-vector TEST subset into external validation |
| L10 | Unknown/atypical/polymorphic intrusion survey | Survey topic attribution only; does not validate this detector for unknown attacks |
| U01 | UNSW-NB15 dataset publication | Verified metadata; no new full-text, data licensing or exact collection-history validation |

The current related-work prose is conservative about differing protocols, lack of
external validation and novelty. It does not claim a new ensemble algorithm or a
field-wide research gap. The source locations and exact quoted context in the JSON
allow the next reader to check every citation without guessing where it appears.

## Remaining concerns

- **P1 reading depth.** Metadata agreement is not claim-support validation. For
  stronger methodological statements, read and preserve exact relevant full-text
  passages of the closest ensemble/FS studies. Do not upgrade the ledger's
  abstract-only or selected-passage entries to FULL_TEXT_READ.
- **P1 novelty.** A broad, up-to-date search and comparison of closest protocols
  remains incomplete. The defensible contribution is a bounded benchmark/error/
  cost audit; no field-wide novelty is established.
- **P2 L03 conflict.** Existing sources disagree on 254–262 versus 254–263. Keep
  `CHECK_SUGGESTED`; inspect publisher version of record before certifying the
  full legacy corpus. It is excluded from the current 12-item report bibliography.
- **P2 foundation attribution.** The report attributes ensemble/FS principles to
  applied IDS papers. If a future authorized revision adds historical-priority
  claims or detailed derivations, verify appropriate primary method sources first.
- U03 final issue/year follow-up already exists. Earlier memory saying both
  U01/U03 are wholly unresolved is stale. U03 publisher VOR was not visually
  inspected, and U03 is not part of this report's twelve entries.

No bibliography patch or report edit is applied. No simulated final panel review
is claimed. Next P18 action is source-grounded reading of closest-method passages
and L03 publisher pagination, not rerunning this completed bookkeeping audit.
