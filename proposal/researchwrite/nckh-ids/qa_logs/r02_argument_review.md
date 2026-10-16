# R02 independent argument and positioning review

Date: 2026-10-16. Reviewer: AI proposal-structure/claim-calibration specialist, independently dispatched under researchwrite. This is a local foundation-file review, not human supervision, approval, full-text literature verification, experimental verification, or administrative certification. No network, training, prediction, data/source modification, or other agent's review was used. Only this report was written.

## Scope and readiness

Reviewed AGENTS.md, MASTER_PROMPT.md; memory STATE/HANDOFF/TASK_BOARD/RESEARCH_CANON/DECISIONS; foundation files 00–05; literature/gap_matrix.md, DOMESTIC_SOURCES.md and READING_NOTES.md. Installed folder `C:/Users/admin/.codex/skills/nature-proposal-writer` identifies itself as `researchwrite`, manifest version 1.1.1. Loaded SKILL.md, manifest.yaml, evaluation-rubric.md, professor-dispatch.md and research-anti-slop.md. The saved local registry agrees with that alias; its historical `loaded=False` field is not evidence of this review's execution. File existence/readability was checked by actual reads; underlying experimental outputs and publisher sources were not independently revalidated here.

Verdict: **INTERNAL FOUNDATION; REPAIR BEFORE FORMAL DRAFTING**. Mean score **7.25/10**, below the skill's strict foundation threshold **>7.5**. A bounded supervisor discussion is reasonable with these open issues, but this score does not pass the foundation gate, certify the proposal, or authorize submission. The foundation is candid and has a defensible student benchmark-audit contribution. Its remaining weakness is the explicit literature→bounded gap→all frozen RQs→observable outputs chain, rather than lack of an invented novel algorithm.

## Findings

### P0

None identified within the reviewed text. Explicit bans on superiority, real-time deployment, fully leakage-free claims and retroactive prior hypotheses are appropriate. This is not a finding that unseen drafts or the implementation have no P0 defects.

### P1-A: The central tension starts with a known result, while the literature-to-question bridge remains implicit

Pointers: `proposal/researchwrite/nckh-ids/03_argument_map.md:3` and `:7`; `literature/gap_matrix.md:7` and `:13`; `00_scope.md:3`.

Supported observation: the argument opens with the observed small Macro-F1 difference/CI and FPR–FNR trade-off. The gap matrix correctly shows that ensemble+FS, OOF stacking and imbalance methods already exist, and explicitly withholds broad novelty. These facts support a retrospective audit rationale, but do not establish that the wider literature fails to report such trade-offs or fair comparisons.

Interpretation: a reader could mistake the favorable interpretation of known outputs for the original motivation unless the argument distinguishes its time layers more concretely. The explicit retrospective warning reduces that risk but does not complete the chain.

Repair within current scope: add a short bridge: (1) cited work establishes existing ensemble/FS approaches within the stated reading boundaries; (2) the unresolved question **for these frozen pipelines and this benchmark** is whether observed gain is reliable and what cost/error trade-offs accompany it; (3) the existing outputs are examined retrospectively to answer that bounded question. Present the known result as a diagnostic example or completed evidence, not a prospective prediction. Do not claim a field-wide omission without a documented search and source reading. This does not require changing the frozen RQ or rerunning models.

### P1-B: RQ1 is explicit, but RQ2–RQ5 lack operational outcome mappings in the foundation

Pointers: `03_argument_map.md:9` and `:11`; `04_section_contracts.md:7`; `.research_memory/RESEARCH_CANON.md:7` through `:11`; `literature/gap_matrix.md:9`.

Supported observation: only RQ1 is named in the argument map. The section contract requires each objective to have an artifact/gate, but provides a generic row rather than actual mappings. The primary canon retains RQ2–4 and secondary RQ5, with RQ4 partial and RQ5 lacking matched sampling evidence.

Repair within current scope: add one compact matrix with RQ, bounded objective, existing comparison/analysis, metric/output pointer, inference limit and completion status. RQ2 must say pipeline trade-off rather than isolated causal FS effect; RQ3 must ask for observed complementarity/gain association without guaranteeing improvement; RQ4 must mark official/novel-view evidence as partial and within one benchmark; RQ5 must remain unanswered/partial for sampling efficacy. An honest incomplete cell is preferable to a generic promise. Do not delete the unresolved RQs or manufacture new comparisons to make the table complete.

### P1-C: The proposal's future-work contract is not yet separated from completed research in the form mapping

Pointers: `00_scope.md:3` and `:5`; `04_section_contracts.md:7`, `:10` and `:11`; `05_style_guide.md` paragraph 2.

Supported observation: the scope and style guide correctly forbid claiming the proposal predates experiments; the form contract still combines objectives/content/results in one row and preserves template durations without listing completed versus remaining work.

Repair within current scope: declare the document a reconstruction/preparation from an existing research record. Mark completed experiments and known findings as such; reserve future tense and expected products for literature completion, QA, documentation, reproducibility work and deliverables that remain unvalidated. Map the 4/11/11/4-week form stages to provisional work descriptions without inventing start dates or asserting that historical experiments occurred on that future schedule. Any institutional requirement for a genuinely pre-experiment proposal needs author/GVHD clarification; the AI cannot confer retrospective approval.

### P2-A: Domestic coverage is sufficient for a bounded topic-existence claim, not a comparative domestic research gap

Pointers: `literature/resume_r02_2026_10_16/DOMESTIC_SOURCES.md:7`, `:8` and `:11`; `01_research_canon.md:14` and `:30`; `02_evidence_table.md:16`.

Supported observation: D01 is a defense notice, D02 a partially read thesis summary; D03 remains discovery-only. The foundation appropriately limits their use. The unresolved label “domestic literature” is too broad now that two usable topic-level sources exist.

Repair: distinguish “topic-level domestic context available” from “detailed method/result comparison pending.” Do not call D01/D02 two journal articles, infer successful defense from a schedule, or infer that Vietnamese work has not already investigated the proposed trade-offs. Detailed comparison requires reading appropriate primary materials; it is not a prerequisite to the narrow statement that related topics exist locally.

### P2-B: Generic evidence labels could be mistaken for independent certification

Pointers: `02_evidence_table.md:3` through `:16`; `01_research_canon.md:16`.

Supported observation: the table includes caveats such as static evidence not being execution proof and rerunning aggregate tables not being training replay. Its repeated `evidence-backed` status nevertheless mixes local experiment artifacts, publisher previews, Methods excerpts and thesis-topic notices.

Repair: preserve the caveats and add evidence-type/verification-boundary language to the table heading or status legend. Keep local-result validation separate from literature-source reading. The current review accepts these as documented local claims; it does not independently certify the experiment or literature.

## Eight dimensions

Adaptation: the original rubric targets Chinese doctoral proposals in materials/chemistry. Here “materials/controls/measurement” is interpreted as IDS dataset, split, fixed candidates, metrics and evidence traceability. Novelty is judged as a specific, useful student contribution rather than a doctoral mechanistic discovery. Language is a manual Vietnamese review using the structural anti-slop categories; no Chinese/English detector result is claimed. Each score concerns the supplied foundation, not the final DOCX or source code.

| Dimension | Score /10 | Reason |
|---|---:|---|
| Research question clarity | 8 | RQ1 is explicit, bounded and answerable without requiring ensemble victory; remaining frozen RQs are available only by reference rather than mapped in the argument. |
| Scientific tension | 6 | The FPR/FNR–cost tension is meaningful, but the current opening is a known local result and does not itself supply the literature-to-bounded-gap bridge (P1-A). |
| Evidence matching | 8 | Reading boundaries, unsupported claims, no-equivalence limitation and known-results status are explicit; underlying sources/results were not independently verified in this review. |
| Logical chain | 6 | The core RQ1 chain is coherent, but RQ2–5 have no explicit objective→analysis→output/status rows and completed/future work are not operationally separated (P1-B/C). |
| Method feasibility | 7 | Fixed binary scope, candidates, threshold and major selection/reproducibility limits are documented; the foundation remains a mapping rather than a reproducible protocol, and training replay/model availability are unresolved. |
| Contribution specificity | 7 | An audit of frozen benchmark pipelines and error/cost trade-offs is concrete and suitable for the student scope; wider literature distinctiveness remains unestablished and must not be claimed. |
| Risk boundaries | 8 | FS optimism, non-nested selection, within-benchmark dependence, partial RQ coverage and absent deployment are candid. The future-work/status matrix would make fallback and unresolved outcomes clearer. |
| Language quality | 8 | Vietnamese wording is restrained and avoids novelty/superiority slogans; mixed shorthand and repetitive pending labels suit internal notes better than final proposal prose. |

Mean: (8+6+8+6+7+7+8+8)/8 = **7.25**. The two scores below 7 identify structural repairs; they should not be raised by polishing wording alone.

## Evidence categories and authority limits

- **Supported by reviewed files:** binary/frozen scope and claim limits are explicit; prior-work descriptions have declared reading boundaries; the central argument currently names RQ1 alone; D01/D02 have restricted source types. Numeric experimental statements are recorded in the canon, not newly verified by this specialist.
- **Plausible but unverified interpretations:** benchmark trade-off auditing may have pedagogical or local methodological value; current wording may let a reader infer prior motivation from post-result diagnostics. Neither establishes publication novelty or actual reader response.
- **Author/GVHD input:** whether the institution accepts a reconstructed proposal in the original 2026 form; administrative identities, dates, budget/copies applicability and signatures. None should be invented. These do not prevent the structural mapping repairs.
- **Scope-changing recommendations not authorized here:** adding a dataset, temporal/external validation, multiclass prediction, resampling comparison, new model selection, changed threshold or rewritten frozen RQs. These require separate impact analysis/decision and cannot be smuggled into expected outcomes. This review recommends none as a prerequisite for the bounded audit positioning.

## Most consequential repair and acceptance check

Create the explicit **literature evidence→bounded benchmark question→each frozen RQ→existing analysis/output→inference limit/status** matrix, preceded by a clear completed-versus-remaining statement. This single repair resolves the largest chain defect while preserving chronology and scope. Re-review the argument after that edit; do not assert a passing score in advance.

Acceptance for this report: required files actually read; five prioritized findings with file/section pointers; eight independently reasoned scores and exact mean; supported/unverified/author/scope categories separated; no human approval, external verification, experiment execution or broad novelty claim. Report is complete as a bounded review artifact; project foundation and release gates remain open.
