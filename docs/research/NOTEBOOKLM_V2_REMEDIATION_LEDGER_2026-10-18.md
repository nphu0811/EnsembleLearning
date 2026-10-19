# NotebookLM V2 findings — verified remediation ledger (2026-10-18)

**Status:** PARTIAL — authoritative verbatim NotebookLM 10-item / 4-CRITICAL + 6-MAJOR page-anchored output **not present** in repository. Never invent quotes, physical page numbers, or claim reviewer acceptance. Preserve historical 37-page PDF and V2 47-page PDF.

## Issues demonstrably supported by previously preserved review context

| Group | Supported issue | Scientific repair requirement | Status |
|---|---|---|---|
| N01 | Feature selection reused data before development CV in historical setup | Refit selectors exclusively inside each new FIT subset; do not present historical OOF as nested-FS validation | P21 protocol specified, selector resource smoke PASSED; scientific contrast NOT RUN |
| N02 | RQ2 lacks matched RF17 vs RF42 controlled ablation | Match FIT identities, RNG, RF hyperparameters, validation, processing; change only feature track | P21 protocol specified; full matched experiment NOT RUN |
| N03 | RQ1 lacks repeated independent refits | Five predeclared replicated FIT subsets and same internal-validation fold, report paired seeds and uncertainty with dependence caveat | P21 protocol specified; actual repeated study NOT RUN |
| N04 | RQ5 lacks matched class weighting and resampling | Control RF42 NONE vs BALANCED vs FIT-only random oversampling, disclose minority is Normal; compare FNR and FPR | P21 design + RQ5 fit-only sampler committed; resource/full experiments NOT RUN |
| N05 | McNemar conclusions may be overstated | Limit to paired discordance on same holdout; do not infer broad generalization | V2 prior review interpretation; inspect exact pages before edit |
| N06 | Novel-vector subset is not independent unseen-world test | Label as same official TEST subset / post-hoc sensitivity; no external test claim | V2 prior review interpretation; inspect exact pages before edit |
| N07 | P15 model reproduction/provenance caveat | Separate newly reconstructed full-TRAIN binaries from historical training environment | Integrated V2 revision previously tracked; must verify actual final pages |
| N08 | Cost comparison may mix pipelines / conditions | Make hardware, feature count and hyperparameter confounds explicit | Requires per-table source review |
| N09 | Dynamic stacking / diversity causal language | Distinguish observational double-fault/error correlation from proven causal superiority | Requires per-page evidence review |
| N10 | Statistical independence / duplicate-vector limitations | Disclose exact-vector group split only addresses one leakage path and official TRAIN/TEST reuse | V2 and P21 caveats known; page-level closure NOT VERIFIED |

These are **ten working review themes**, NOT a transcription or claim that these are the exact NotebookLM ten, their original severity, ordering or page references.

## PDF gate: do not falsify completion
1. Obtain authoritative NotebookLM verbatim output with PDF page anchors; map all ten to their original chapter/section/physical pages.
2. Compare the actual downloaded immutable V2 PDF against current LaTeX sources and prior P20 reviewer packet. Mark already-addressed paragraphs separately from open experimental gaps.
3. Execute P21 scientific TRAIN-derived extension only after safety/synthetic pilots and the author-host run; cite actual result hashes. A resource smoke is NOT a metric or proof of a research hypothesis.
4. Create a **new** LaTeX entry point/chapters and build revision V3 with XeLaTeX/BibTeX. Keep old V2 bytes unchanged. Full print QA: rendered all-pages visual inspection, glyph, footer, line overlap, diagrams and bibliography anchors.
5. Report P21 as post-hoc TRAIN-derived: it does not repair independence of prior official TEST. Present old metrics unchanged and new internal-validation metrics in clearly separate tables. Mark unresolved scientific limitations rather than claiming them fixed.

## Runtime authorization
The author requested no arbitrary WALL-CLOCK cutoff on genuinely long full model training. This does not waive the need for an explicit resource watchdog, free-RAM floor, failure logging, cancellation and on-disk safety. The existing 20-minute cap refers only to a bounded pilot and is not a justified full-study limit. A new full training launcher (not yet implemented) should avoid hard-coded training wall time while retaining memory and stop safety. There is **no** author-host full P21 execution evidence as of this ledger.

## Current deliverables
- `tools/p21_rq5_sampling.py`: self-contained pure FIT-only sampling, no training.
- `tests/test_p21_rq5_sampling.py`: synthetic-only regression tests.
- CI workflow wired to run the tests; actual result must be checked separately.
- `docs/research/RQ5_RESOURCE_PILOT_CONTRACT_2026-10-18.md`: bounded resource-gate specification.

**Do not claim:** revised PDF compiled, author-host RQ5 trained, stacking refit, exact NotebookLM 4C/6M fully addressed, P20 final passed, or final publication package ready.
