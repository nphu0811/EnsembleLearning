# R05 — Independent assembled proposal argument and form-feasibility review

Review date: 2026-10-16. Reviewer: an AI subagent assigned a separate argument/form review. This is an independent pass within the current AI workflow, not independent human peer review, a credentialed professor's assessment, administrative approval, or approval of past work. No prior `qa_logs` review was opened. Research and form facts below were derived from the draft and source packet; memory was read for restart context, not used as a substitute for this review.

**Disposition: suitable for targeted revision and supervisor discussion; not ready for submission.** The core argument is defensible as a bounded benchmark case study. No newly discovered P0 scientific contradiction was found in this pass. There are three P1 content repairs and inherited P0 submission dependencies. A review outcome cannot close G0–G6 or turn partial RQs into completed research. No numerical reviewer score is assigned or used as a completion gate.

## Frozen review target and scope

- Target: `proposal/researchwrite/nckh-ids/drafts/De_cuong_noi_dung_review_r04.md`, 180 lines; SHA-256 `dfef1dffa3fdd8efbb558b65a02cb13c443da8529c5efba169d6b7dc7ad47bac`. All line references below refer to this version.
- Original form: `templates/original/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx`, SHA-256 `bedb06dcecfc40a4d04a9412022509f039f7c4e64e6d779aa13b7dc9ec3d26c7`. Read-only ZIP CRC and direct OOXML comparison to `template_audit_r04/original_body_snapshot.json` passed: 58 body blocks, eight tables, 97 cells. Body indices below are zero-based, matching that snapshot. This is structural/text verification, not rendered visual QA.
- Loaded contract: `MASTER_PROMPT.md`, `AGENTS.md`, `.research_memory/STATE.json`, `HANDOFF.md`, `TASK_BOARD.md`, `RESEARCH_CANON.md`, `DECISIONS.md`. Loaded proposal foundations `00_scope.md` through `07_remaining_work_feasibility.md`.
- Loaded researchwrite installation: `C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md`; frontmatter name `researchwrite`, manifest version 1.1.1. Read `manifest.yaml` and references `revise-mode.md`, `professor-dispatch.md`, `validation-checklist.md`. Applied diagnosis-before-rewrite, claim classification, argument-chain review, and the argument/form specialist remit. This is a review-only pass; no draft revision, export, scoring, or separate professor service execution is claimed.
- Source packet read: `docs/CLAIM_EVIDENCE_MATRIX.md`, `literature/gap_matrix.md`, `literature/resume_r04_2026_10_16/source_claim_map.csv`, `SCOPED_READING_NOTES.md`, original snapshot and `field_coverage.csv`, `release/RELEASE_BLOCKERS.md`, `.research_memory/r04/R04-FINAL-CHECKPOINT.json`, `docs/research/R04_ML_SMOKE_REPORT.md`. Checked actual repaired smoke `validation.json` and `run_metadata.json` on disk. This pass did not reopen papers for fresh full-text review or independently rerun historical experiments.
- Only this report is authored by this reviewer. No raw data, template, frozen protocol/result, training source, proposal draft, or evidence table was changed. No model fitting or TEST access was performed.

## What works and should be preserved

The objective at lines 17–19 permits an unfavorable ensemble result. The literature discussion distinguishes existing components from novelty (lines 53, 65–77) and does not infer a domestic research gap from two limited institutional sources (59–61). That is proportionate to the reading packet.

The methods/results boundary is unusually clear: binary labels and the frozen candidates/threshold are explicit (31); conditional row bootstrap is separated from retraining stability and McNemar from Macro-F1 testing (33); FS/meta-selection optimism and limited robustness/resampling evidence are disclosed (35). The RF17/RF42 contrast remains a joint pipeline comparison rather than a causal FS ablation. These qualifications are substantive safeguards and must survive shortening for the Word form.

Lines 3, 55 and 114 openly identify a recovered dossier after experiments. Retain that chronology, negative/uncertain findings at 39, and the distinction between report replay, reconstruction and final inference at 41. Do not invent prior approval or new hypotheses to make this look prospective.

## Objective → RQ → method → evidence → contribution → product

The following is the reviewer's reconstruction of the existing argument, not a rewritten research contract. RQ wording/status is supplied by foundation 06; the assembled draft currently makes readers follow that resolver.

| Objective and draft evidence | Frozen RQ | Method and evidence allowed by packet | Contribution justified | Product and remaining boundary |
|---|---|---|---|---|
| Evaluate detection/error/cost, lines 17–19, 31–39 | RQ1: stable ensemble improvement over matched individual models | Frozen Stack42/RF42/RF17; official saved evaluation and C03/C04; paired uncertainty/correctness analyses | Conditional benchmark comparison; no established Stack42 superiority or equivalence, no independent retraining stability | Tables/uncertainty figure/report; arithmetic/provenance checks do not complete the stability clause |
| Describe feature-track performance/cost, lines 19, 33, 67 | RQ2: FS, performance, minority detection and cost | C05; historical feature tracks, RF17/RF42 and cost/ablation tables; hyperparameters differ | Joint pipeline trade-off; binary detector attack-family misses, no isolated FS causal effect | Feature/cost/error tables and limitations; RQ remains partial for isolated FS effects |
| Describe error complementarity, lines 19, 73 | RQ3: association of complementary errors with gain | C06; saved OOF diversity and ensemble development summaries | Descriptive association, including negative voting evidence; no guarantee of gain | Diversity/ensemble table and interpretation; no new base-learner selection on TEST |
| Establish robustness limits, lines 35, 69, 73–75 | RQ4: sensitivity to split protocols | C07; official/novel-vector views within UNSW | Sensitivity within this benchmark only | View analysis and explicit unanswered temporal/day/scenario contrast; RQ4 partial |
| Establish imbalance-evidence limits, lines 19, 35, 67 | Secondary RQ5: fold-contained imbalance strategies | C08; no matched resampling intervention in current packet | Honest evidence-gap statement | Config/protocol documentation; no efficacy conclusion, no new post-TEST intervention to close the RQ |
| Finish auditable dossier and usable software, lines 27, 41, 83, 91–101 | Supports RQ interpretation/G3–G6, not a new scientific RQ | C09 replay; gate B reconstruction and gate C inference; TRAIN-only software smoke is intermediate evidence | Traceability and a qualified reproducibility record | DOCX/PDF, LaTeX/report, code, figures, final inference and defense; each retains its own acceptance gate |

The main weak link is presentation: this chain is recoverable from the packet, but not stated compactly inside the assembled proposal. The substantive gaps are acknowledged rather than concealed. Fixing presentation must not silently redefine “stable,” RQ4 or RQ5 to fit completed outputs.

## Claim classification and source fit

This minimum claim audit covers the full assembled text, including claims that are sound. “Supported” means supported within the supplied local packet and reading limits, not a fresh certification of each experiment or paper.

| # | Draft lines / claim | Classification and assessment |
|---|---|---|
| 1 | 3, 114: recovered dossier, no prior approval claim | Honest scope/chronology statement; author acceptance still unknown |
| 2 | 17: evaluate rather than require ensemble superiority | Research objective; consistent with canon and C03 |
| 3 | 19: use OOF errors and keep original RQs | Method/objective commitment; foundation 06 supplies the detail |
| 4 | 23, 53, 65–67: ensemble/FS/voting components have prior art | Supported within stated abstracts/Methods snippets; not a comprehensive novelty search |
| 5 | 25, 35: binary detector, no multiclass outcome substitution | Consistent with canon; preserve attack-family distinction |
| 6 | 31: official TRAIN/TEST sizes and labels | Supported by C01 and canon; local data hashes are not official checksums |
| 7 | 31: RF42/Stack42/RF17 and threshold 0.5 | Supported by C02; static consistency does not prove entire execution chronology |
| 8 | 31: stacking LR/DT/RF → LR with internal CV | Source-grounded architecture description; does not establish fully nested feature/meta selection |
| 9 | 33: paired bootstrap is conditional on benchmark rows | Correctly limited; does not replace repeated training or external validation |
| 10 | 33: McNemar is paired correctness, not direct Macro-F1 test | Appropriate inferential boundary |
| 11 | 33, 67: RF17/RF42 is a pipeline trade-off | Supported by C05; correct causal restraint |
| 12 | 35: FS before development CV/meta tuning not fully nested | Supported by C11/canon; essential caveat |
| 13 | 39: no overall superiority; FP decreases while FN increases | Supported by C03/C04; no equivalence inference |
| 14 | 59: domestic announcement establishes topic/schedule only | Fits R04C04; no successful-defense or thesis-result inference |
| 15 | 61: UET summary establishes objectives only | Fits R04C05; no whole-thesis or deployment inference |
| 16 | 65: published stacking uses CV meta inputs/random 80/20 | Fits R04C01; explicitly declines full nesting certification/matched-score comparison |
| 17 | 69: novel-vector view is not cross-dataset evaluation | Fits R04C02/C07; does not transfer CIC-specific faults to UNSW |
| 18 | 75: value is traceable bounded case study | Plausible contribution framing; field-wide novelty remains unproven |
| 19 | 83: no model artifact currently available | Ambiguous/stale at the current checkpoint: three SMOKE_ONLY models exist; valid fullTRAIN final model remains unavailable; see ARG-R05-03 |
| 20 | 89, 101, 118: 03 reports, CD/02 A4 conditions, seven-million sample budget | Exact form-derived requirements with applicability pending, not enacted local policy or actual expenditure |

## Original form, schedule and budget feasibility

| Original form field | Assembled coverage | Assessment |
|---|---|---|
| Header/title/code/field; body 0–10 | Lines 5–11 | Present as content/pending administrative fields; no copied sample identity |
| Objectives/content/results; 11–20 | 13–41 | Substantive coverage. Methods are explicitly placed within Nội dung, respecting original label sequence |
| Units/personnel/adviser; 21–32 | 43–49 | Pending appropriately; not evidence of completed administrative form |
| Research situation domestic/international; 33–38 | 51–77 | Bounded synthesis present; source depth and non-exhaustiveness explicit |
| Need/application; 39–41 | 79–85 | Research/teaching use is proposed, no receiving institution or live deployment invented |
| Product classes; 42–43 | 87–89, 103 | III proposed; original I/II/III classification remains for formal confirmation |
| Product quantities; 44–45 | 89, 91–97 | 03 report volumes retained. Expanded internal acceptance table must not replace the original five-column quantity table |
| Type I quality; 46–47 | 103 | No Type I product fabricated; original table preserved pending N/A convention |
| Type II/III requirements; 48–49 | 99–101 | CD/report cover/final article if any/software explanation ≤02 A4 retained; do not convert optional paper to promised accepted paper |
| Schedule; 50–51 | 105–114 | 4+11+11+4 = 30 weeks matches original. Honest that this is neither actual chronology nor remaining schedule; execution feasibility remains open |
| Costs; 52–53 | 116–122 | 3,000,000+3,500,000+500,000 = 7,000,000 VND matches original. Preserve blank money cells and funding notes; these are not zero costs or actual spending |
| Signatures; 55 | 124–126 | Correctly pending; no sample signatory adopted as verified identity |

The outline covers all substantive form regions in order, but coverage is not a filled form or layout acceptance. No basis here to approve the 30-week duration or conclude the sample budget pays for reconstruction. Compute cost may be zero cash on existing equipment or may require resources; both remain unverified. Do not invent a budget line or assume unpriced work is funded. Main deliverables depend on final model, supported DOCX/LaTeX build/render paths and author information; adding all of them to the final four-week row does not demonstrate capacity.

## Findings and concrete repair contracts

### P0 dependencies inherited from the source packet — block submission, not further bounded revision

**ARG-R05-00A — Author and institutional acceptance remains required.** Evidence: lines 7, 11, 45–49, 89, 114, 118, 120, 126; original form body 1, 9–10, 21–32, 45, 51, 53, 55. Missing information includes identities/roles, signatures, applicability of institution, copies, schedule and budget, and whether this recovered dossier is acceptable. The draft already states these honestly; no new prose should manufacture their resolution. **Repair:** retain explicit placeholders and record real author/institution input when obtained. **Acceptance:** field-by-field trace to supplied confirmations; recovered chronology remains explicit; genuine signatories act for themselves. AI review cannot satisfy this test.

**ARG-R05-00B — The submission artifact has not been built and visually verified.** Evidence: line 3 and source `release/RELEASE_BLOCKERS.md` G5; original snapshot/coverage are read-only. **Repair:** after content fixes, fill a separate copy of the original DOCX, retain original labels/tables/blank monetary cells, render DOCX/PDF with the supported workflow and inspect every page. **Acceptance:** actual files, traceable source-copy provenance, structure/content checks and visual QA with no truncation/overlap/missing signatures region. This report does not claim such execution. Keep the original immutable.

### P1 content repairs

**ARG-R05-01 — The assembled proposal delegates the testable RQ/status chain to a working file.** Evidence: Mục tiêu lines 19 and 132; Tổng quan 55, 73–75; the actual explicit five-RQ mapping exists in foundation 06. A reader of the proposal sees broad objectives and caveats but must open the repository to know exactly which RQ is answered, partial or unanswered and which output checks it. This weakens the proposal's central argument even though the packet is internally consistent. **Repair:** add a compact in-document RQ/objective–method–artifact–status crosswalk inside Nội dung (or an attached proposal appendix allowed by the form). Preserve original RQ wording by attachment or clear original wording plus faithful Vietnamese description. Include O1–O4 remaining-work objectives, and explicitly say which parts cannot be answered by present evidence. Do not add new experiments, preregistered hypotheses or change frozen RQs. **Acceptance:** each RQ1–RQ5 maps to one method/evidence/output and inferential limit in the proposal itself; RQ1 stability unverified by independent retraining, RQ2 causal FS partial, RQ4 partial, RQ5 controlled efficacy unanswered; a reader need not resolve an internal Markdown path to understand them.

**ARG-R05-02 — The form schedule is preserved, but the remaining work has no operational feasibility plan.** Evidence: lines 27, 41, 93–97, 109–114, 118. Foundation 07 separates A/B/C usefully, yet still contains unknown resources. The draft explicitly disclaims a remaining schedule, so it should not be rejected for falsifying dates; the real issue is that model reconstruction, final demo, builds/renders and defense remain commitments without a resource owner, decision point or bounded fallback. A preserved 30-week form and unchanged sample budget are insufficient to judge whether completion is feasible. **Repair:** add a short remaining-work appendix: dependency order; responsible role pending actual assignment; required existing hardware/runtime or author input; time/resource bounds to be assessed before any heavy job; objective pass/fail and stop condition for B/C; deliverables that proceed while blocked. State that reconstruction failure leaves the final demo and release open, while documentation work proceeds. Link available r04 capacity evidence before making a new capacity assertion. Keep the original budget and schedule cells unchanged unless the responsible author supplies a real revision. **Acceptance:** every remaining product has input/dependency, role, resource assumption, gate and failure action; no unbounded job or unsupported four-week guarantee; no substitution of aggregate viewer/SMOKE_ONLY model for final inference. Dates and monetary allocations remain pending where unconfirmed. No full training is required to repair this planning defect.

**ARG-R05-03 — Current-product status omits the completed TRAIN-only software smoke.** Evidence: lines 83 (unqualified no model artifact), 94 (clean-environment training unverified), 96, 97 and 114; resolver lines 160–165 point to foundation 07 and mixed older status sources. The later r04 checkpoint and actual `r04_ml_smoke_repaired/validation.json` establish 45/45 checks, three fitted/serialized/reloaded SMOKE_ONLY models on 2,000/500 disjoint official-TRAIN rows. They do not establish fullTRAIN reconstruction or final inference. The current wording can be read as denying any clean-environment fit/model artifact, while the final-model gap is real. **Repair:** refresh the status column and foundation B/C descriptions with explicit two-level status: software smoke passed, final reconstruction/model/demo not achieved. Prefer “chưa có artifact mô hình final/fullTRAIN hợp lệ cho demo” over unqualified “chưa có artifact mô hình.” Add `R04_ML_SMOKE_REPORT.md` and repaired validation/metadata to the resolver; update defense text status to acknowledge the r04 script/runbook/checklist while retaining no PPTX/PDF/rehearsal/finaldemo. **Acceptance:** all status occurrences agree on aggregate replay PASS, software smoke PASS_SCOPED, original env UNKNOWN, full reconstruction/final artifact absent, final inference/defense incomplete. No promotion of smoke runtime/metrics to scientific or deployment evidence; preserve failed initial run and repair record. This is a documentation repair, not a reason to rerun the completed smoke.

### P2 improvements

**ARG-R05-04 — Source resolvers mix current and historical ledger checkpoints.** Evidence: line 140 resolves M:L05–L07 to r02, while line 148 resolves the same stable IDs to r04; 165 cites r02 defense validation. This is not proof the claims are false: the IDs/DOIs are stable, and reading boundaries remain necessary. **Repair:** identify the current metadata ledger once, keep r02/r03 notes explicitly as scoped-reading provenance, and mark historical status evidence as historical. **Acceptance:** every stable cited L/D/N/S label resolves unambiguously; no historical verification count is presented as current; reading depth is not upgraded by changing metadata pointer.

**ARG-R05-05 — Some first-use terms and acceptance criteria are too compressed for the proposal audience.** Evidence: lines 17–19, 25, 31–35, 39, 93–99 use pipeline, feature tracks, FP/FN, MCC, FPR/FNR, PR-AUC, paired bootstrap without all first-use definitions. This is readability/validation specificity, not an invitation to add a textbook section. **Repair:** add a short glossary/first-use expansions for core metrics and errors and refer nonessential engineering detail to appendices. In product acceptance, name the numeric/source/render evidence expected rather than relying only on “kiểm thử” or “G0–G6.” **Acceptance:** a Vietnamese student-research council reader can identify positive class, FP/FN meanings, main comparison metric and product checks without repository knowledge; no metric definitions or software tolerance become newly invented statistical hypotheses or acceptance margins.

## Completed evidence versus future commitments

| Already evidenced in packet / direct file checks | Still future, partial or requiring input |
|---|---|
| Historical source/frozen tables and bounded argument chain; no total ensemble-superiority claim | Broader novelty/systematic literature survey, independent retraining stability, temporal/external validation, controlled resampling efficacy |
| Aggregate reporting replay, original form snapshot and coverage | Filled/rendered DOCX/PDF, approved administrative applicability, genuine signatures |
| Repaired TRAIN-only software smoke with 45/45 checks and three SMOKE_ONLY artifacts | Valid fullTRAIN reconstruction/final serialized preprocessing/model, final inference demo and end-to-end acceptance |
| Saved tables and one QA'd figure; defense text/Q&A described in r04 checkpoint | Complete figure set/report build/render, PPTX/PDF, rehearsal, final release inventory/ZIP |

No future acceptance item above is retrospectively treated as complete. No recommendation requires fitting on TEST, tuning after TEST, rewriting frozen outcomes, renaming unfinished work as a finished substitute, or inventing administrative facts. Expanding the scientific scope would require a separate explicit decision; this review recommends no such expansion.

## Revision order and review acceptance

1. Repair ARG-R05-03 status against actual r04 evidence; retain the exact final-model limitation.
2. Repair ARG-R05-01 with a self-contained crosswalk; mechanically compare original RQs and frozen candidate/threshold language.
3. Repair ARG-R05-02 with a bounded remaining-work plan and resource/input conditions; do not start full training as part of these prose fixes.
4. Apply P2 resolver/terminology edits and check claim strength/source boundaries, form region coverage, budget arithmetic and 30-week sample schedule again.
5. Recheck the revised draft against these stable issue IDs. Keep P0 dependencies visibly open until actual author input and supported artifact/render evidence exist.

The single most consequential revision is to make the in-proposal objective/RQ/output/status chain explicit while distinguishing completed evidence from remaining work. The packet already supports that chain; writing it inside the proposal strengthens reviewability without claiming new science.

## Review execution notes

Read-only direct DOCX check passed CRC, SHA-256, and exact snapshot equality for all 58 blocks before a terminal encoding error interrupted printing Vietnamese table text. A subsequent UTF-8 stdout read printed the relevant preserved table rows and target hash successfully. This was an output-encoding issue, not a changed or corrupt DOCX. Repaired smoke validation contains 45 true checks and `passed: true`; metadata records the TRAIN-only subset and SMOKE_ONLY scope. No new smoke or historical scientific test was run. Existing reviews were not consulted, and this report is frozen as the independent pre-reconciliation assessment.
