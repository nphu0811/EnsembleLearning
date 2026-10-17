# P18 targeted deep verification, 17/10/2026

Entry commit `7c3530e40dd34eb63b9c7fde6b4eecda817e5a74`; current manifest
508/508 matched. This is a targeted closest-method investigation, not an exhaustive
systematic review or proof of novelty. Existing U01/U03 scoped verification is
reused, not repeated. No change to the report bibliography or approved PDF.

Selection has two strata. First, deepen existing L06 (stacking on UNSW), L12
(correlation/embedded FS plus stacking), L09 (external-validity contrast), L08
(filter-FS reporting). Second, follow publisher related-article links to directly
relevant studies N01 (mRMR and stacking, 2025), N02 (MI-Boruta and stacking on UNSW,
2024), N03 (multi-layer stacking including UNSW, 2026). This relevance-driven
selection is access-limited and cannot establish complete coverage of the field.
Same DOI denotes one work. A preprint is not substituted for the final article.

Search tools used official web search/open, primary publisher pages, Crossref DOI
API and institutional repository routes. Dedicated scholarly MCP endpoints were
not exposed in this session; no such call is claimed. Actual API preflight found
PubMed/Crossref reachable and arXiv TLS certificate verification failure. No TLS
verification was disabled, credentials supplied, subscription bought or access
control bypassed. A Windows TLS request to the institutional L09 PDF also returned
403; that failure was retained. Supporting information was not requested or fetched.
`nature-downloader` was inspected for routing, but its download-delivery workflow
was not executed; source-linked reading used `nature-reader` grounding rules.

Questions for each paper

1. Which dataset files, classification task and split actually define the result?
2. What is stated about fitted preprocessing/FS inside folds and OOF stacking?
3. Is tuning separate from final evaluation, and is any threshold protocol stated?
4. What imbalance treatment, metrics, interval/test and computation cost are shown?
5. Are different datasets fitted separately, or is a model transferred across them?
6. Which claim can be compared to this project without silently equating protocols?

Reading status distinguishes `VERIFIED` source statements, `PARTIAL` selected
sections/identity, `UNVERIFIED` unestablished nesting or comparability,
`BLOCKED` inaccessible full text/VOR, and `NOT_APPLICABLE`. Absence of a detail in
selected sections does not prove the authors omitted it everywhere or that their
implementation leaks. A paper's claimed performance is not independently reproduced.

Source captures and page extractions stay in ignored `local_sources/`. HTTP 200
alone is not acceptance: multiple Springer requests returned the same 3038-byte
JavaScript challenge, and IEEE returned an empty/non-PDF response. They do not
count as full text. The readable publisher web-tool body captures for L06/N02 are
separate evidence from those failed direct-download attempts. L12 is a validated
23-page publisher-hosted PDF with a matching DOI and CC BY 4.0 notice on page 1.
Full PDFs, extracted whole texts and third-party page images are not added to Git
or the release draft. Public ledgers retain URLs, byte hashes, section locators,
paraphrased findings and explicit reading boundaries.

Output acceptance requires a source/reading ledger, comparison matrix, claim map,
gap assessment, disclosure of access failures, validation against real source
anchors and unchanged frozen project artifacts. Source-anchor tests verify
traceability, not peer-review agreement or the correctness of every paper.
