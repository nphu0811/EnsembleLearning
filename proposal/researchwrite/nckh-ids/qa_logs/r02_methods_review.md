# R02 — Independent methods and feasibility foundation review

Date: 2026-10-16. Reviewer: AI specialist pass, methods/feasibility; not human supervisor review. Review objects: proposal foundation 00–05, frozen research design, ENSEMBLE_FRAMEWORK, CLAIM_EVIDENCE_MATRIX, R02 READING_NOTES, and research memory. No other specialist report read. No network, training, prediction, source/data edits or experiment execution. Only this report is written.

Skill actually read: researchwrite (installed directory nature-proposal-writer), manifest v1.1.1, SKILL.md, evaluation-rubric.md, professor-dispatch.md and research-anti-slop.md. The rubric was written for Chinese doctoral materials/chemistry proposals. Here it is adapted to a Vietnamese student binary IDS foundation: physical experimental conditions become dataset/split/fit order/control/metric/resource specifications; novelty means a defensible benchmark contribution, not an obligatory new algorithm. Language score covers foundation clarity only, not finished DOCX prose. Scores are judgments, not validation results.

## Recommendation and bounded gate

INTERNAL FOUNDATION — REPAIR BEFORE FORMAL DRAFTING. Average 7.31/10, below the skill's strict foundation_score >7.5 gate. Useful enough for a supervisor discussion if clearly labeled incomplete; not final proposal or submission readiness. The frozen retrospective scope and claim restraint are strong. The principal gap is an operational RQ/objective → method → artifact → acceptance mapping that acknowledges unanswered parts of the original questions. No P0 defect observed in the documents reviewed; this does not certify absence of leakage in code or chronology.

## Evidence and checks performed

Read actual freeze_candidates.json and the first rows of final_metrics.csv, cost_metrics.csv and paired_bootstrap_differences.csv. Freeze names/configurations and thresholds match the framework description; saved official rows show RF42 FP=10003/FN=734 and Stack42 FP=9861/FN=852, supporting the stated 142 fewer false positives and 118 more false negatives. Saved Macro-F1 difference CI includes zero. These are checks of existing saved artifacts, not recomputed metrics or independent proof of execution chronology. Seven representative paths, including freeze, final/cost/paired tables, diversity table, ensemble CV table and original DOCX, exist. Diversity/CV table contents were not audited in this pass. No comprehensive hash audit, test suite, full training reproduction, DOCX rendering or external citation verification was performed.

## Findings

### P0

None observed within this bounded document review. Never repair any finding below by tuning or adding candidates against the already observed TEST.

### P1 — repair before formal foundation approval

1. **Objectives remain a contract promise rather than an executable mapping.** `proposal/researchwrite/nckh-ids/04_section_contracts.md:7` requires each objective to have an artifact/gate but does not supply individual objective rows. `03_argument_map.md:9` states RQ1 only; RQ2–RQ5 reside mainly in the external canon and C05–C08. Add one compact mapping using the original RQ wording, operational subquestion, frozen comparator, evidence artifact, inference boundary, completion status and acceptance check. RQ1 can support a bounded comparison, not establish stability across independent retraining; RQ2 is a joint feature/configuration pipeline comparison; RQ3 association is descriptive and selection-affected; RQ4 is partial within-benchmark sensitivity, not the original split-protocol contrast; RQ5 has no matched intervention. Retain the original RQs and mark these limitations explicitly rather than quietly rewriting them. This is documentation repair within the existing scope.

2. **Feasibility of the remaining software/demonstration product is not operationally bounded.** `01_research_canon.md:22` says no serialized inference model exists; `03_argument_map.md:15` notes unknown original environment and missing ML replay; `04_section_contracts.md:10` still lists a demo conditionally without inputs, resource estimate, dependency or fallback deliverable. Existing cost rows demonstrate historical costs, not present-machine feasibility. Add separate acceptance paths for (a) saved-result/reporting replay, (b) a future isolated TRAIN-only reconstruction using fixed configurations if authorized and feasible, and (c) a tested inference demo only if a real usable artifact is produced. Record environment/hardware availability as UNKNOWN where unconfirmed. Completion of (a) cannot pass (b)/(c). Do not promise reconstruction success or automatically execute models to satisfy this review. This can be repaired as a plan; executing a new training workflow is a separate task under the existing research contract.

3. **The motivation is result-grounded but the literature gap is not yet comparative.** `03_argument_map.md:5` honestly uses already observed results as the tension; `01_research_canon.md:9–14` and `READING_NOTES.md:7–23` establish prior component use and differing evaluation contexts. They do not establish a broadly missing protocol, or what this project adds relative to the closest comparable benchmark. Add a bounded comparison of a small number of directly relevant sources using only fields actually read: split, task, model/FS role, evaluation/reporting, verification depth and unknown fields. Frame the contribution as a local audit/trade-off case if broader novelty remains unverified. Full-text acquisition is needed only for claims requiring that depth; do not make metadata stand in for it. No need to expand datasets or claim a new algorithm.

### P2 — useful precision and maintainability repairs

4. **Reproducibility details depend on several transitive files.** `ENSEMBLE_FRAMEWORK.md:9–17` supplies useful pipeline/configuration specifics but does not name the exact 17-feature manifest, learned preprocessing schema or development fold allocation in this note. Link the existing authoritative paths and distinguish what was inspected from what is historical. Add no invented values. This is not evidence that these files are absent.

5. **A statistical interpretation rule should be explicit at the objective/output boundary.** `03_argument_map.md:19` correctly bounds row bootstrap and selection optimism, and `CLAIM_EVIDENCE_MATRIX.md:9` rejects equivalence. Carry this into the acceptance mapping: CI including zero supports an inconclusive superiority comparison, not equal models; FPR/FNR trade-off is reported jointly; row uncertainty is conditional on this benchmark and does not quantify retraining stability. No new post-test margin or decision threshold is warranted.

6. **Risk disclosure needs a fallback for every promised output.** The foundation has good forbidden-claim rules but `04_section_contracts.md:10–12` does not identify what happens if the model artifact/environment cannot be recovered or schedule confirmation is unavailable. Preserve explicit unresolved gates and a staged review deliverable; do not silently drop required final products or call the release complete.

7. **Normalize status wording as evidence evolves.** `01_research_canon.md:14` acknowledges domestic sources while `01_research_canon.md:30` says domestic literature is unresolved. State “limited domestic topic evidence; detailed comparative synthesis incomplete.” `04_section_contracts.md:15` predates this review and should eventually point to completed QA with unresolved findings, rather than suggesting that no review has occurred. This does not make the bibliography complete.

## Eight independent scores

| Dimension (adapted) | Score /10 | Reason |
|---|---:|---|
| Problem clarity | 8.0 | RQ1 is dedicated and bounded; remaining RQ operational coverage is dispersed rather than visible in one foundation mapping. |
| Scientific tension | 7.0 | Detection trade-offs and inferential credibility motivate the work; comparative literature gap remains provisional and the known results must remain retrospective. |
| Evidence matching | 8.0 | C-IDs, saved table checks and explicit source-reading boundaries are good; static freeze consistency does not prove chronology and not every literature field is verified. |
| Logical chain | 6.5 | The section contract promises objective/artifact/gate mapping without enumerating it, leaving partial RQ4 and unanswered RQ5 easy to misrepresent. |
| Method feasibility | 6.5 | Frozen pipeline and historical costs are concrete, but unknown environment/model availability and undefined reconstruction/demo gates prevent a reproducible remaining-work plan. |
| Contribution specificity | 6.5 | Audit/trade-off contribution is restrained and appropriate; its placement against the nearest prior protocols remains unsupported beyond component-level precedents. |
| Risk boundaries | 8.0 | Test freeze, FS optimism, same-benchmark sensitivity and noncausal FS comparison are explicit; output-specific failure paths remain incomplete. |
| Language clarity | 8.0 | Concise Vietnamese foundation, consistent cautions, few unsupported intensifiers; final prose, citations and rendered form have not been assessed. |

Arithmetic: (8+7+8+6.5+6.5+6.5+8+8)/8 = 7.3125. This pass does not substitute a score for artifact validation.

## Fact / interpretation / input / scope separation

**Supported within the reviewed local evidence:** three frozen candidates at threshold 0.5; saved official counts/paired interval consistent with the canon; documented non-nested FS/meta selection limits; binary evaluation; reporting replay distinct from training reproducibility; literature notes expressly limit reading depth. The limitations are part of the usable foundation, not a reason to claim completion of the original ambitious protocol.

**Plausible but unverified interpretations:** linear/tree diversity might explain complementarity; development optimism could alter rankings; current machine could reconstruct training within acceptable resources. None is established by the files checked here. No external paper was independently verified in this pass.

**Author/qualified-owner input:** original environment/model provenance if available, access to appropriate hardware/time, verified institutional schedule/budget/identity/signature information. No need to request another copy of the original DOCX: its presence was checked. Administrative input is not a reason to stop the independent mapping repair.

**Recommendations that change scientific scope or commitments:** adding multiclass, new datasets/external validation, new resampling interventions, fully nested FS reruns, new base learners or post-test threshold selection would create a new experiment/protocol decision, not a prose fix. This report does not authorize or require them. Any future extension must remain separate from the frozen final test and follow the impact-analysis/approval rules. Changing original RQ wording to imply broader completion would also be improper.

## Most consequential repair

Write the explicit RQ/objective–method–output–gate matrix before section prose. Keep original RQs, identify partial/unanswered portions, and make each output's completion criterion independent of model superiority. This makes a narrow honest student IDS proposal possible without altering frozen results. Then clarify the remaining reproduction/demo feasibility plan and reassess these three low-scoring dimensions; do not raise scores merely because the report exists.

Conflict summary: not applicable to this independent pass; no other specialist review read. Permanence candidate: none. A human supervisor has not approved the scope or findings by virtue of this AI review.
