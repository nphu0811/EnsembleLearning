# R02 methods/feasibility — targeted recheck

Date: 2026-10-16. Independent AI methods/feasibility pass, not human supervisor approval. Read changed foundation 01–04 and new 06_rq_method_output_gates.md / 07_remaining_work_feasibility.md against this reviewer's own original findings. No other specialist report read. Original r02_methods_review.md preserved; SHA-256 before recheck: 264830c9e9ba4c40ab44760770df0626c7692afd15d3b79d1e3a5c24f5c44c13. No network, model execution, data/source edits or new statistical calculations. Only this recheck is written.

Rubric: same transparent adaptation of researchwrite v1.1.1 evaluation-rubric.md from doctoral materials proposals to a Vietnamese student binary IDS foundation. Dataset/split/fit controls and software-resource gates replace physical experiment conditions. The review scores the foundation's ability to support bounded drafting, not completion of the experiments or final products.

## Gate

**PASS FOR BOUNDED FOUNDATION DRAFTING — 7.81/10 (>7.5).** Formal prose may describe the audited binary benchmark and explicitly incomplete work using the limits now recorded. This does not pass G0–G6, certify a fully leakage-free protocol, prove original execution chronology, establish field-wide novelty, finish RQ4/RQ5, or approve retrospective institutional submission. Supervisor-facing text must preserve the retrospective chronology and unresolved product gates.

The increase is justified by substantive mapping and conditional acceptance rules: 06 names the frozen comparator/output/status for every original RQ; 07 separates reporting replay, model reconstruction and inference demo with distinct dependency/failure gates; prior-work placement is now expressly limited to a local case study. Merely adding files would not justify this change.

## Finding dispositions

| Original finding | Disposition | Evidence and residual limit |
|---|---|---|
| P1.1: no executable objective/method/output mapping | Resolved for bounded drafting | 06:7–11 retains all original RQs, separates operational questions, frozen comparator, output, inferential limits and partial status; 06:17 maps remaining writing/software products. RQ1 retraining stability, RQ4 split contrast and RQ5 controlled resampling remain unproved rather than marked complete. |
| P1.2: reproduction/demo feasibility unbounded | Resolved as a foundation planning defect; implementation gates remain open | 07:9–13 separates A/B/C acceptance, unknown hardware/environment, reconstruction provenance and blocked demo. No unconditional success promise. Capacity assessment and exact dependencies remain mandatory before a resource-heavy job, so B/C feasibility has not been experimentally established. |
| P1.3: literature gap not comparative | Resolved for local audit/trade-off contribution only | 03 now distinguishes component precedents from a project-specific question and labels known results retrospective; 07:30–35 gives a bounded comparator table with explicit unknowns. It still cannot support field-wide novelty or claims that prior work lacks fairness. |
| P2.4: method details rely on transitive paths | Open, nonblocking for drafting with citations to authoritative evidence | New mapping improves table names but “stable subsets,” “diagnostic tables lịch sử” and some source aliases are still not uniquely resolved. Exact feature/preprocessing/fold-manifest links are still needed before runnable-methods or end-to-end reproducibility claims. |
| P2.5: statistical interpretation at output boundary | Resolved | 06:7 explicitly rejects equivalence and retraining-stability inference, requires joint FPR/FNR interpretation; 06:13 preserves threshold0.5 and rejects post-test margins/cost decision rules. |
| P2.6: promised-output failure paths | Resolved as disclosure/planning issue | 07:9–13 provides mismatch/failure, partial G3/P15 and blocked-demo outcomes; 07:24 keeps institutional schedule/resource uncertainty visible without deleting final obligations. |
| P2.7: stale domestic/review status | Resolved | 01 now distinguishes topic-level domestic evidence from missing detailed synthesis; 04 acknowledges initial completed reviews and the need for recheck. This is not a bibliography-completion claim. |

No new P0/P1 identified in this limited recheck. Remaining P2 items should be corrected while drafting; they do not authorize completing partial research questions by prose.

## Residual precision issues

- **P2, 06:13: path-resolution statement is broader than its resolver.** docs/CLAIM_EVIDENCE_MATRIX.md resolves the major phase families, but it does not locate view_summary.json or the replay report/source paths. Actual paths checked here include results/data_audit/unsw_nb15_views/view_summary.json, results/reproducibility/resume_2026_10_16/clean_replay_report.json and src/analysis/close_original_phase11.py. Add these exact paths or a compact artifact index; “stable subsets” and historical diagnostic tables should also get unique pointers before detailed numerical claims.
- **P2, 06:8: keep RQ2 limitation aligned to its wording.** “PARTIAL đối với isolated FS effect/minority multiclass” should not imply the original question required multiclass. The actual missing distinction is causal isolation of FS versus joint pipeline/configuration differences, with limited minority-family detection analysis from a binary detector. Multiclass remains outside the implemented scope, not a newly required experiment.
- **P2, 06:10: absence of trustworthy time/session metadata is a documented project limit, not newly independently verified in this recheck.** Preserve its provenance and avoid interpreting this as proof that no defensible split study could ever be designed.
- Source-reading boundaries still apply to 07:30–32. No external source was reopened here, and “closest” prior work is a pragmatic selected comparison, not a systematic-search conclusion. Keep that distinction in prose.

## Artifact existence checks

Used read-only filesystem search to resolve the new mapping. Found:

- results/ablation/unsw_nb15/phase13_ablation/phase13_ablation_matrix.csv
- results/data_audit/unsw_nb15_views/view_summary.json
- results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv
- results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv
- results/ensemble/unsw_nb15/phase7_1_diversity/oof/stable_17_features_oof_predictions.csv
- results/ensemble/unsw_nb15/phase7_2_ensemble_cv/oof/stable_17_features_ensemble_oof.csv
- results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv
- results/reproducibility/resume_2026_10_16/clean_replay_report.json
- src/analysis/close_original_phase11.py

The final/cost/paired tables and freeze were already read during the original pass. Read the saved clean_replay_report.json here: it records no training/prediction, two zero-return commands and three byte-identical CSV comparisons, with training_reproduction=NOT_PERFORMED. This is consistent with A's claimed historical scope; these commands were not rerun. Existence of OOF artifacts does not independently validate their fold construction. A supplementary search for feature/preprocessing/fold manifests did not locate a uniquely named manifest; that search also reported no configs/ directory. Neither observation proves missing feature provenance throughout the workspace. No new broad hash audit was performed.

## Independent dimension rescore

| Adapted dimension | Original | Recheck | Reason |
|---|---:|---:|---|
| Problem clarity | 8.0 | 8.0 | RQ1 remains precise; full original RQ list and partial answers are now visible. No improvement in external empirical coverage is inferred. |
| Scientific tension | 7.0 | 7.5 | The revised argument starts from established component use and a bounded project question; known results are explicitly retrospective. Broad gap remains unverified. |
| Evidence matching | 8.0 | 8.0 | Source-type caveats and static-chronology limits remain sound; new documents add no independent experimental or full-text validation. |
| Logical chain | 6.5 | 8.0 | Original questions now map to frozen method/output/status and remaining objectives have named acceptance categories. Exact path aliases remain a minor repair. |
| Method feasibility | 6.5 | 7.5 | Reporting replay, fixed-configuration reconstruction and tested inference have distinct gates and honest failure paths. Unknown resources prevent a stronger reproducibility score. |
| Contribution specificity | 6.5 | 7.0 | Local audit/trade-off case is now placed against selected precedents without novelty inflation. Full comparative synthesis remains limited. |
| Risk boundaries | 8.0 | 8.5 | Output-specific failure branches, reconstruction provenance and retrospective institutional acceptance supplement existing leakage/test limitations. |
| Language clarity | 8.0 | 8.0 | Clear compact foundation; minor compressed spacing/aliases remain. Final Vietnamese prose and rendered DOCX are unassessed. |

Arithmetic: (8+7.5+8+8+7.5+7+8.5+8)/8 = 7.8125. The foundation threshold is passed by documentation adequacy within the declared scope, not by resolving the underlying experimental limitations.

## Evidence / interpretation / author input / scope separation

Supported in this pass: the revised mapping and fallback rules exist and are internally consistent with the original review; representative referenced artifact paths exist; saved replay report explicitly excludes training reproduction. Unverified interpretations: current resources can complete reconstruction, artifact recovery will succeed, literature establishes a general gap, or the historical protocol chronology is fully proven. Author/qualified-owner input remains original environment/artifact provenance if available, acceptable resource budget and institutional acceptance/schedule/identity/signatures. No new request is required to proceed with independent drafting and path cleanup.

Scope-changing work remains separate: new datasets/multiclass, rerun nested selection studies, resampling interventions, new candidate selection or thresholds, and a new split-protocol study. None is authorized or required by this score. Preserve the frozen TEST and do not reinterpret a resource-recovery task as permission to optimize against observed results.

Most consequential next step: draft only the bounded objectives/methods/products allowed by 06/07, carry all partial statuses into prose, and replace ambiguous artifact aliases with unique paths. Do not describe this internal foundation gate as human approval or release readiness. No conflict reconciliation performed; no other reviewer report read. Permanence candidate: none.
