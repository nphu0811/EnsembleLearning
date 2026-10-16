# R02 partial-section review

Date: 2026-10-16. Reviewer: independent AI argument/positioning specialist. Reviewed only `drafts/sections/muc_tieu_noi_dung_phuong_phap_r02.md` against foundation contracts 04, RQ/output gates 06 and feasibility/chronology 07. Used the same researchwrite eight-dimension rubric as the foundation reviews, transparently adapted from doctoral materials proposals to a Vietnamese student IDS section. This is a partial-content review, not full proposal review, supervisor acceptance, final export QA or experimental certification. The draft and earlier reports were not edited.

## Decision

**KEEP_INTERNAL_DRAFT — 7.50/10, above the section keep threshold >6.5.** No P0/P1 content overclaim identified within this section. Four local P2 repairs below would improve precision before incorporation into the form. No new experiment or scope expansion is needed to repair them.

The section preserves the important contracts: line 5 explicitly identifies a restored record; lines 19 and 33 distinguish pending products from completed research; line 31 withholds stacking superiority; lines 17 and 27 preserve binary/multiclass and within-benchmark limits; lines 19/33 make inference demo conditional rather than an existing capability. No prior hypothesis, approved date, real-time deployment, independent external validation, resampling efficacy or successful ML reconstruction is claimed.

## Actionable findings

All line references below refer to `proposal/researchwrite/nckh-ids/drafts/sections/muc_tieu_noi_dung_phuong_phap_r02.md` as read on this review date.

### P2-1: Replace causal-sounding “tác động” in the objective

Location: line 11, “mô tả tác động quan sát được của các feature tracks và cấu hình mô hình”. Line 25 correctly treats RF17/RF42 as a joint pipeline trade-off, but the objective's wording could still suggest an identified effect of feature selection.

Exact repair: replace that clause with **“mô tả khác biệt quan sát được về hiệu năng và chi phí giữa các pipeline có tập đặc trưng và cấu hình khác nhau”**. This aligns the objective directly with RQ2's partial/observational gate in 06. It changes no frozen question or result.

### P2-2: Identify the AUC quantities and interpretation of cost

Location: line 25 uses generic “AUC” and “chi phí train/inference”. The stored final metrics header contains separate `roc_auc` and `pr_auc`; the cost header contains train seconds, total inference seconds and inference milliseconds per sample. A generic AUC label can conceal a meaningful metric distinction when copied into final methods.

Exact repair: replace **“FPR/FNR, AUC và chi phí train/inference”** with **“FPR/FNR, ROC-AUC, PR-AUC và thời gian huấn luyện/suy luận được ghi trong bảng chi phí, với điều kiện đo và giới hạn môi trường được công khai”**. Do not imply historical runtimes establish present reconstruction capacity or production throughput. No values were recomputed in this review.

### P2-3: Keep the static-provenance limit visible beside historical method statements

Location: line 23 and source label N2 at line 39. The method description agrees with ENSEMBLE_FRAMEWORK and P15-04, but P15-04 explicitly says static source/metadata consistency does not prove the historical execution exactly followed the current source. The current wording is acceptable internally because the source document carries the caveat; a copied standalone section would be clearer if it carried the distinction too.

Exact repair: append to the method paragraph **“Mô tả này dựa trên source và metadata đã đối chiếu; kiểm tra tĩnh không thay việc tái lập huấn luyện và chưa xác nhận môi trường huấn luyện gốc.”** This preserves the distinction already required in 06/07 without falsely retracting the existence of saved results.

### P2-4: Resolve internal shorthand and source aliases before form use

Locations: lines 5, 11, 23, 45. Tokens such as `đề cương2026`, `tài liệu06_...`, `TRAIN175.341`, `dương1`, `threshold0,5`, and generic “ledger r02” remain suitable working notes but reduce readability and traceability if directly pasted into the form.

Exact repairs: use **“đề cương năm 2026”**, **“tài liệu 06_rq_method_output_gates.md”**, **“TRAIN gồm 175.341 mẫu và TEST gồm 82.332 mẫu; Attack là lớp dương (1), Normal là lớp 0”**, and **“ngưỡng quyết định 0,5”**. At line 45 replace **“theo ledger r02”** with **“theo `literature/resume_r02_2026_10_16/legacy_verification_ledger.csv` và `literature/resume_r02_2026_10_16/READING_NOTES.md`”**. Define LR/DT/RF/OOF on first use in the eventual standalone form content or its terminology section. Preserve internal IDs until bibliography renumbering is actually performed.

## Source and scope checks

Read ENSEMBLE_FRAMEWORK, CLAIM_EVIDENCE_MATRIX, P15_04_PROTOCOL_REPORT and the local ledger rows for L05–L07. Checked existence of the frozen manifest, release blockers, domestic-source note and final metrics/cost CSVs; inspected only the two CSV headers. Model configuration, split/feature exclusions and statistical interpretation are consistent with those local notes. L05–L07 author/year/DOI strings agree with their ledger entries. This is local cross-document consistency, not independent publisher/DOI verification or full-paper reading.

N1–N4 honestly point to internal records, with N3 explicitly pointing onward to original tables. D01–D02 remain bounded to topic/source-type use. The line 45 ledger alias should be made exact as above. No numerical evaluation, prediction, training, full-data read, source-paper fetch or new validation of underlying scientific results occurred. These source checks therefore do not close the project's reproducibility or literature-verification gaps.

Line 17's “ablation hồi cứu” is acceptable only with line 25's pipeline-confounding caveat and the unchanged 06 mapping. Do not later upgrade it to an isolated feature-only or component leave-one-out experiment. Omission of administrative tables, a full literature review and timeline from this partial section is not a defect; those remain separate contracted sections.

## Eight-dimension section score

Scores assess whether this particular section is keepable, not whether the full proposal or project passes. The rubric's materials/measurement concreteness maps here to dataset, comparisons, metrics and output gates; language assessment is manual Vietnamese review using structural anti-slop categories. No detector score is claimed.

| Dimension | Score /10 | Reason |
|---|---:|---|
| Research question clarity | 8 | The binary benchmark objective is explicit and does not presume an ensemble victory; the full frozen RQs and partial statuses are referenced honestly rather than silently rewritten. |
| Scientific tension | 7 | Error/cost trade-offs and prior component existence motivate the comparison; a detailed literature-gap argument is intentionally outside this partial section. |
| Evidence matching | 8 | Source IDs, known-result wording and reading boundaries are explicit. Exact ledger alias and static-provenance sentence remain useful refinements; experimental/source verification is not newly established here. |
| Logical chain | 8 | Objectives flow to historical content, methods/metrics, inference limits and separately gated pending products. The “tác động” objective needs the minor observational-wording repair. |
| Method feasibility | 7 | Dataset sizes, candidate scope and threshold are concrete; software/reconstruction gates are cross-referenced. Resource feasibility, original environment and usable model artifact remain unresolved rather than promised. |
| Contribution specificity | 7 | The section presents comparative audit/trade-off work and rejects algorithmic novelty. It does not establish a broader literature contribution, appropriately leaving that to other sections and evidence. |
| Risk boundaries | 8 | Selection optimism, non-nested meta tuning, benchmark dependence, partial RQ4/RQ5 and conditional demo completion are preserved. |
| Language quality | 7 | Prose is restrained and readable, but mixed English shorthand, attached number tokens and dense method sentences need editing for final form content. |

Mean: (8+7+8+8+7+7+8+7)/8 = **7.50/10**. Threshold **>6.5** is met. No score implies supervisor approval or export readiness.

## Evidence categories and next repair

- **Supported by reviewed text/local records:** historical/prospective work is separated; known performance conclusions are bounded; source strings and table schemas agree locally; no deployment or multiclass completion is claimed.
- **Interpretation, not new empirical fact:** the four wording repairs reduce likely reader ambiguity. Their benefit is a reviewer judgment, not experimental evidence.
- **Author input:** form acceptability and administrative details remain pending; this does not block keeping or repairing this internal section.
- **Scope-changing recommendations:** none. Additional comparisons, a changed RQ, new threshold, external dataset or new model selection are not required by this section review.

Most consequential repair: replace the line 11 causal-sounding objective with the exact observational pipeline-comparison wording in P2-1. Apply the remaining P2 edits before integrating the section into the 2026 form, preserving the partial-content and unvalidated-product labels.
