# P20-PRE — Reviewer A citation erratum (A-Q11, evidence pointer index 1)

**Type:** reviewer-source citation typo; **not** scientific data correction, not a changed reviewer opinion, not a withdrawn review. **Status:** DOCUMENTED_OPEN_EXCEPTION pending author-host full packet QA and P20 review-revision acceptance.

- Frozen reviewer: `defense/p20_pre_2026_10_17_01/reviewer_A/report.json`, question `A-Q11`, zero-based `evidence[1]`, with `locator: header`.
- Reviewer **original** anchor, deliberately left untouched: `split,label_name,count,percentage`.
- Actually recorded header in `results/eda/unsw_nb15/tables/binary_class_distribution.csv`: `split,label,class_name,count,percentage`.
- Source and copied packet CSV row are recorded with SHA-256 `84e76743c9e423bf1db67afe15c1eb6091664fe57951f4beb78eb6edb38953a8` and length `201` bytes in the immutable 80-entry packet manifest.
- The inaccurate reviewer anchor did **not** modify binary class counts, class labels, model results or inference. A-Q11 discusses binary class balancing and rare attack-family support; its substantive question remains open for author response.
- Original reviewer A `report.md` and `report.json`, model source, original CSV, packet manifest/receipt, approved 37-page PDF and frozen science must **not** be edited as a repair.
- The validator may label exactly this confirmed mismatch as `ACCEPTED_DOCUMENTED_CITATION_ERRATUM` only if the actual packet and original CSV are byte-for-byte equal with the locked manifest, the original reviewer evidence tuple is exact, and this erratum exists. The raw strict anchor check remains false and must be reported as such.
- Any other mismatch remains an **UNRESOLVED_FAIL** and stops P20-PRE QA. Even when all other checks pass, status is `PASS_WITH_DOCUMENTED_CITATION_ERRATUM`, never `CLEAN_0_FAIL` or P20 final approval.
- Remote GitHub checks also noted a distinction between local packet receipt hash and checked-in manifest bytes. This separate provenance discrepancy is **not** waived by this citation erratum; original author-host packet SHA and all 80 local file copies must be checked in local full QA.

**Recheck (after pulling)**: use a **new** QA directory, keep `qa_reviews_01/validation.json` with 1195 PASS / 1 FAIL intact. Only after the review phase returns `PASS_WITH_DOCUMENTED_CITATION_ERRATUM` and `unresolved_failed=0` should the complete phase be launched with a new output directory. Push only the QA JSON(s), not the ignored packet files, raw datasets or model binaries.
