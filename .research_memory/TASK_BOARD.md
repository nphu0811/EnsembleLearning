## 2026-10-18 P21 Selector17 resource pilot accepted

| Work item | State | Evidence and next |
|---|---|---|
| P21 supervised RF42 resource pilot | **DONE_SCOPED** | 8k TRAIN FIT; no validation scoring |
| P21 3-method selector17 pilot | **DONE_SCOPED** | Author b8820ed; 8k FIT, selection sample4667/seed, 15 selector calls, selected17 (eligible stable18), RSS381898752B, 57.547s wall |
| P21 selector report metadata QA | **PASS 15/15** | \`tools/p21_verify_selector_pilot_reports.py\` +7 negative tests; [CI39068091845](https://github.com/nphu0811/EnsembleLearning/actions/runs/39068091845) SUCCESS (37+7 unit/synthetic tests;29 static checks). Evidence \`docs/research/P21_SELECTOR17_AUTHOR_PILOT_ACCEPTANCE_2026-10-18.md\` |
| P21 RQ5 weight/oversample pilot | **NEXT / NOT IMPLEMENTED / NOT AUTHORIZED** | Require matched RF42 NONE/BALANCED/fit-only minority random oversampling, same FIT source and watchdog, avoid validation scores |
| P21 RQ1 Stacking-Lite pilot | **PENDING / NOT AUTHORIZED** | Three-fold inner CV, separate time/RSS feasibility |
| P21 full scientific 5-seed/5-arm matrix | **BLOCKED / NOT AUTHORIZED** | Author opt-in only after all pilots/resource review; new separate TRAIN-derived internal validation, no TEST |
| PDF V3, P20-FINAL | **NOT AUTHORIZED / OPEN** | Preserve V2 47 pages/P9/P15/reviewer evidence and release gates |

Historical checkpoints below are not the latest P21 state.

---

## P21 selector17 pilot ready — 18/10/2026

| Task | State | Evidence / next |
|---|---|---|
| Fit-only stability selector implementation | **CODE_READY; NOT EXECUTED ON USER TRAIN** | tools/p21_selector_core.py: MI+Spearman 0.95, L1 LR, ExtraTrees200/n_jobs1, 5 fixed seeds, 17 exact original features. No historical stable17 reuse |
| Selector supervisor/worker | **CODE_READY; NO AUTHOR EXECUTION** | tools/p21_selector_pilot_supervisor.py and tools/p21_selector_pilot_worker.py; separate consent and protected output, ≤20min, RSS cap2GiB, startup RAM4GiB, one CPU |
| QA on synthetic fixtures | **PASS** | [CI39065559976](https://github.com/nphu0811/EnsembleLearning/actions/runs/39065559976): 30 unit tests +7 synthetic ML tests+29 static checks, no raw data or TEST |
| Actual selector pilot | **WAIT_AUTHOR_OPT_IN** | git pull; python .venv-p15-local/P21 selector supervisor with author opt-in; output new p21_train_only_pilot_selector17_01 |
| P21 weighting/oversampling/Stacking pilots | **NOT_IMPLEMENTED / NOT RUN** | Construct only after selector resource evidence scoped PASS |
| P21 full 5-seed scientific experiment | **NOT AUTHORIZED / NOT RUN** | Separate consent needed; V2/P9/P15 untouched |

See docs/research/P21_SELECTOR17_FIT_ONLY_PILOT_QA_2026-10-18.md. Old roadmap lines remain historical, not current gate status.

---

## P21 RF42 author pilot PASS — 18/10/2026

| Item | Status | Evidence and next |
|---|---|---|
| Author-host `p21_train_only_pilot_rf42_01` | **PASS_RESOURCE_SMOKE_ONLY** | Commit `34bcdeac`: 8k TRAIN fit; 51.86s wall; peak process RSS 371728384B; min available RAM4333109248B; TRAIN 175341; internal grouped split 140272/35069; no validation scoring, TEST, artifacts |
| Independent committed-report QA | **14/14 checks PASS** | `tools/p21_verify_pilot_reports.py`, 5 negative/positive fixture tests, [CI 39062897494](https://github.com/nphu0811/EnsembleLearning/actions/runs/39062897494) all jobs SUCCESS |
| P21 selector17 pilot | **NEXT/NOT_IMPLEMENTED** | Leakage-safe train-fit-only selector5x(35k sample) resource pilot; no validation fitting and no preexisting global stable17 |
| P21 balanced/oversample/Stack-Lite pilot | **NEXT/NOT_IMPLEMENTED** | Distinct bounded author opt-in and resource reports; RF42 pilot does not imply safe Stacking |
| P21 scientific 5x5 arm matrix | **BLOCKED—AUTHOR_OPT_IN_AND_PILOT_SUITE** | No new RQ metrics, no full 60k fit authorized |
| P21 PDF V3 | **NOT_AUTHORIZED** | Preserve PDF V2 47 pages and frozen P9/P15, open P18/P19/P20 review rights |

Status evidence: `docs/research/P21_RF42_PILOT_AUTHOR_RESULT_ACCEPTANCE_2026-10-18.md`.

---
## P21-RF42-PILOT PREPARED, NOT EXECUTED — 18/10/2026

| Task | Status | Evidence/next |
|---|---|---|
| P21-local-static-source-preflight | **30/30 PASS (user Windows)** | `--verify-local-train-sha`, official TRAIN SHA correct, `official_test_read=false`, `training_performed=false` |
| P21-sandbox/resource-protected RF42 anchor pilot code | **IMPLEMENTED, NOT RUN** | `tools/p21_pilot_supervisor.py`, `tools/p21_pilot_worker.py`, `tools/p21_pilot_guards.py`. Only 8k default/20k maximum fit rows from TRAIN-fit pool, no validation prediction, no model artifact. Separate author consent required |
| P21 synthetic QA | **PASS** | [CI 39061822482](https://github.com/nphu0811/EnsembleLearning/actions/runs/39061822482): 14+7+3 tests, 29 source checks; synthetic split verified group disjoint, collision fail-closed, null reject |
| P21-pilot-RF42 actual host run | **WAIT_AUTHOR_OPT_IN** | If desired, run bounded `--authorize I_AUTHORIZE_TRAIN_ONLY_P21_RF42_PILOT` on user Windows, new outdir `results/controlled_extensions/p21_train_only_pilot_rf42_01`, >=4GiB available and >=10GiB disk. No auto-run |
| P21 select17/weight/oversample/Stacking pilot | **NOT IMPLEMENTED / NOT APPROVED** | Inspect RF42 resource/time before implementing rest; additional synthetic ML leakage QA needed |
| P21 scientific 5-seed RQ1/RQ2/RQ5 fits | **NOT_AUTHORIZED / NOT_RUN** | New controlled study separate from P9/P15, 20 RF + 5 Stack fits only after complete pilot suite and explicit author approval |

All P21 changes preserve original 37-page/PDF V2 47-page, official TEST, original model evaluations, P15 reconstructed binaries and P20 reviews. Pilot resource smoke is not a science result.

---
# CHECKPOINT ƯU TIÊN 18/10/2026 — SAU PDF V2 VÀ P20-PRE

| Task | Trạng thái hiện hành | Bằng chứng/next exact action |
|---|---|---|
| P17 V2 manuscript | **DONE_SCOPED_TECHNICAL_BUILD; AUTHOR_REVIEW_PENDING** | 47-page A4 5-chapter PDF; SHA256 `5300f9de92a7fc3834294b015382acfff80c9f0384ef9d6a32419e2bf72b52f3`; successful [CI](https://github.com/nphu0811/EnsembleLearning/actions/runs/38999397120), `docs/research/REPORT_REVISION_V2_PRINT_FIX_VERIFIED_2026-10-17.md`. Original 37-page PDF unchanged |
| P20-PRE 3 AI reviewer QA | **DONE_SCOPED_WITH_DOCUMENTED_CITATION_ERRATUM** | `defense/p20_pre_2026_10_17_01/qa_complete_01/validation.json`: 1400 PASS, one strict A-Q11 anchor FAIL documented, zero unresolved; 17 concerns clustered to 9 OPEN groups |
| P20 POST-V2 REVIEW | **NEXT / NOT_RUN** | Have NotebookLM inspect exactly final V2 PDF, retain page-anchored issues, then replay source-grounded reviewer acceptance against V2 on all 9 groups without editing reviewer originals; P20 final remains DEFERRED |
| P16 final print presentation | **OPEN_FINDINGS** | Inspect actual printed size; ~118dpi inherited heatmap and small print remain to be considered; V2 mechanical overfull checks PASS |
| P18 overall | **PARTIAL** | Follow up L03 publisher pagination and lawful text gaps; no unsupported novelty claims |
| P19 overall | **PARTIAL/BLOCKED_RIGHTS** | LICENSE/rights for publication, model/data/third parties; do not distribute Git-tracked smoke binaries or internal-only archive |
| G0–G6 and final submission | **OPEN, not automatically authorized** | Author approval, academic validity, institutional form/signatures and final review release decision separate from a passing PDF build |

**NEXT EXACT ACTION**: NotebookLM critical review of uploaded `Bao_cao_NCKH_EnsembleLearning_REVISION_V2.pdf` ONLY (check source filename/date), with page citations and 9-group reviewer concerns; classify severity and refer results to `P20 POST-V2`. Preserve all frozen experiment results and original P20 reviewer evidence. All sections below this checkpoint are historical snapshots, not the latest priority.

---

# P19 safe draft and P20 preparation — current17/10/2026

| Task | Status | Evidence |
|---|---|---|
| P19-SMOKE-INVENTORY | DONE_SCOPED_READ_ONLY |3paths/size/SHA/Gitblob/introductioncommit/metadata;no deserialize ordelete |
| P19-INTERNAL-ALLOWLIST-DRAFT | DONE_SCOPED_INTERNAL_REVIEW_ONLY |46ZIPentries;245mechanical+121independentchecksPASS;3path testsPASS |
| P19 public release | PARTIAL/BLOCKED_RIGHTS |NoLICENSE;model/data/report/template/thirdpartyrightsundecided;noFINAL |
| P20 packet/rubric preparation | DONE_SCOPED_SETUP |defense/P20_REVIEW_PACKET_SETUP_2026-10-17.md;no reviewerreport |
| P20 full panel | DEFERRED |Neutralfrozenpacket/sourceaccess/finalinputsremain |

P18selectedbodyreads3of7shortlist;136checksPASS. P15/P16statespreserved;approvedreportandfrozenresultsunchanged.

---

# P18 deep verification — current17/10/2026

| Task | Status | Evidence |
|---|---|---|
| P18-DEEP-CLOSEST-METHODS | DONE_SCOPED_SELECTED_SECTIONS |7papers/3selected-bodyreads/24assertions;qa_03 136PASS0FAIL;deepverificationreport |
| P18 overall | PARTIAL |L03VOR,4access-limitedrows,fullclaimreading/noveltysearchremain |
| P19-SAFE-DRAFT | NEXT |Inventorythreehistoricalsmokemodels;allowlistinternalpackage,noindexcleanup |
| P20 | DEFERRED |Preparepacket/rubriconlywhenP18/P19boundedinputsready;noactualpanel |

P15andfrozenPDF/resultsunchanged;priorcheckpointsbelowretained.
---

# Current task checkpoint — 17/10/2026

| Task | Status | Fresh evidence |
|---|---|---|
| RESUME-P16 | DONE_SCOPED_WITH_RECONCILED_DRIFT | docs/RESUME_AUDIT_2026-10-17_P16.md;267/285oldhashes,281/282historicalfiles;known committed deletion |
| P15 | DONE_SCOPED_RECONSTRUCTION; DO NOT RETRAIN | originalclosure17/10;currentaudit69truechecks/3runPASS;75/75historicalQAinherited |
| P16-COMPREHENSIVE-AUDIT | DONE_SCOPED_WITH_OPEN_PRINT_FINDINGS |2132summary+178actualPDFchecksPASS;17displaymap;37pagecontactreview |
| P16-STANDALONE-ALTERNATIVES | DONE_SCOPED |6newfigures,text6/6,collision6/6;final03bundle;failed01/02preserved |
| P16 whole phase | IN_PROGRESS | Locked report embeddedfont/118dpiheatmap/snapshot-agefindings;historical6collisionFAILstilldisclosed |
| P18-CURRENT-REPORT-CLAIMS | DONE_SCOPED_OFFLINE |119checksPASS,12records,24contexts;0networkqueries/0newfulltextreads |
| P18 whole phase | PARTIAL |Closest-methodreading,noveltysearch,L03publisherpaginationopen |
| P19 | PARTIAL |README,QAenv,availabilityandreviewinventory;licensing/archival/fullenvgatesopen |
| P20 | DEFERRED_FINAL_PANEL_INPUT_GATES |No finalthree-reviewerpanelrun;fixedpacketandremaininginputsneeded |

Approved37pagePDF/source,frozenresultsandhistoricalmodels untouched. This currentsection supersedes stale phase/status statements below without rewriting theirhistory.

---

# Research Task Board

Checkpoint hiện hành r03: `docs/RESUME_AUDIT_R03_2026-10-16.md`. Prior manifest146/148 khớp (2 stale memory hashes), historical preservation282/282. DOCX count được đính chính8 bảng. Các hàng r01/r02 dưới đây giữ evidence lịch sử; cập nhật mới ưu tiên:

| ID | Task | Status | Evidence | Gate |
|---|---|---|---|---|
| BOOT-R03 | Resume inventory/template/registry reconciliation | DONE_SCOPED | resume_2026_10_16_r03/resume_audit.json | Drift explained;282/282 preserved;ZIP/DOCX CRC PASS;6/6 unit tests |
| P18-FIELD-R03 | Crosscheck8 pending legacy records | DONE_SCOPED | literature/resume_r03_2026_10_16/FIELD_CROSSCHECKS.md; validation.json |2 newly verified,6/12 total verified;6 legacy +U01/U03 pending;18/18 bookkeeping checks |
| PROP-PRODUCTS-R03 | Nhu cầu/sản phẩm/chất lượng/tiến độ/kinh phí | DONE_SCOPED | drafts/sections/ung_dung_san_pham_tien_do_r03.md; qa_logs/r03_products_section_review.md | Independent review7.75;P2 repairs/source checks;no rescore/full-proposal/DOCX/render |

| ID | Task | Status | Evidence | Gate |
|---|---|---|---|---|
| BOOT-01 | Inventory workspace and existing artifacts | DONE | resume_2026_10_16/bootstrap/workspace_inventory.csv; p15_01_inventory.json | PASS presence scope |
| BOOT-02 | Audit and preserve original templates | DONE | templates/original/; template_audit.json; TEMPLATE_REQUIREMENTS_MATRIX.md | PASS structural; visual pending |
| BOOT-03 | Discover and load relevant Nature Skills | DONE | nature_skill_registry.csv; SKILL_USAGE_LOG.md | PASS actual usage recorded |
| BOOT-04 | Reconcile phase state | DONE | docs/RESUME_AUDIT.md; ROADMAP_CURRENT.md | PASS bounded audit |
| P15-R1 | Current raw and protocol checks | DONE | p15_03_dataset.json; protocol/ | PASS with protocol caveats |
| P15-R2 | Replay aggregate reporting in fresh stdlib venv | DONE | clean_replay_report.json; 3 identical CSVs | PASS, no ML replay claim |
| P08-DOC | Document locked framework | DONE | docs/research/ENSEMBLE_FRAMEWORK.md | PASS source/freeze matching |
| PROP-FOUND | Restore proposal foundation | DONE_SCOPED | proposal/researchwrite/nckh-ids/00–07; qa_logs/foundation_review_r02.md | Both rechecks >7.5 for bounded drafting; final scientific/admin gates open |
| P19-DRAFT | Data/code availability and FAIR audit | DONE scoped draft | docs/research/DATA_CODE_AVAILABILITY.md | PARTIAL release rights/identifier |
| P16-F1 | Paired-effect forest plot | DONE | results/figures/p16_paired_effects_2026_10_16/ | Figure QA PASS, P16 not complete |
| P18-UNSW | Verify foundational dataset references | PARTIAL | literature/verification_2026_10_16/: ledger, raw Crossref, BibTeX | 3 VERIFIED_METADATA; 2 CHECK_SUGGESTED; no full-text claim |
| P18-LEGACY | Reconcile12 legacy reference identities | DONE_SCOPED | literature/resume_r02_2026_10_16/validation.json, ledger/BibTeX |12 DOI resolved,4 metadata verified;8 field crosschecks pending |
| P01-DOMESTIC | Establish bounded domestic context | DONE_SCOPED | DOMESTIC_SOURCES.md and READING_NOTES.md |2 primary institutional topic sources; detailed comparison partial |
| PROP-SECTION | Draft objectives/content/methods | DONE_SCOPED | Partial draft + qa_logs/r02_section_review.md, r02_section_repair_validation.json |7.5 KEEP_INTERNAL_DRAFT; minor edits applied; no full proposal/DOCX claim |
| P16-REST | QA remaining evidence figures/tables | TODO | Existing drafts require explicit contracts | NOT_RUN |
| P15-ML | Full TRAIN artifact reconstruction (bounded local, 3 frozen candidates) | DONE_SCOPED_RECONSTRUCTION | 3 author full-run PASS + 69/69 actual local artifact verifier checks; docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md | Historical original env UNKNOWN; reviewer binary load & G3 release/demo separately OPEN; no TEST re-evaluation |
| PROP-DOCX | Fill original DOCX + render | BLOCKED tool/content | Original located, preserved | Runtime loader unavailable; verified literature/admin pending |
| REPORT | IDS LaTeX report + PDF | DONE_SCOPED_5CH_37P_BUILD | `report/main.tex`; `docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md`; run 38916942038 | 5 chapters / 37 pages, abstract removed, acronym glossary after TOC; all source/code-internal references absent from PDF; CI PASS; institutional signoff and signatures OPEN |
| DEFENSE-QA | Prepare evidence-grounded council questions | DONE_SCOPED | defense/Hoi_dap_hoi_dong.md; qa_validation_r02.json |20 questions,33 paths checked; DRAFT_FOR_REVIEW |
| DEFENSE | Slides, script, inference demo and final rehearsal | TODO | MASTER requirements | Depends on evidence/report/model; Q&A draft exists |
| RELEASE | G0–G6 and final checksum package | BLOCKED | release/RELEASE_BLOCKERS.md | NOT_READY_FOR_SUBMISSION |

Paths beginning resume_2026_10_16 are under results/reproducibility/. Contract for each scientific task is in the linked artifact or P16_PAIRED_EFFECT_CONTRACT.md. Preserve all historical completed experiment outputs; do not rerun fitting merely to update status.

## r04 R04-RESUME

DONE_SCOPED — 174/174 prior artifact hashes and282/282 historical files match; ZIP15 entries and DOCX8 tables CRC PASS; skills registry inspected

Evidence: `.research_memory/r04/R04-RESUME.json`.

## r04 R04-REF

DONE_SCOPED — Five of six pending legacy entries resolved;11/12 metadata verified; L03 retained CHECK_SUGGESTED page conflict; U01/U03 open;28/28 bookkeeping checks PASS; no full P18 completion

Evidence: `.research_memory/r04/R04-REF.json`.

## r04 R04-READ

DONE_SCOPED — Five source-linked claims anchored to actual passages;10/10 capture checks PASS;L06 selected Methods,L09 indexed Introduction,D01/D02 bounded domestic sources;no full-paper read claim

Evidence: `.research_memory/r04/R04-READ.json`.

## r04 R04-FORM-AUDIT

DONE_SCOPED — Original DOCX58 blocks/97 cells captured;14/14 coverage checks PASS;working gap draft also checkpointed pending review repairs;no fill/render/admin approval

Evidence: `.research_memory/r04/R04-FORM-AUDIT.json`.

## r04 R04-GAP-LIT

DONE_SCOPED — Updated gap matrix and related-work/rationale draft;30/30 source/RQ checks and3/3 repair checks PASS;two independent scoped reviews with minor repairs;not full proposal/P01/P18 closure

Evidence: `.research_memory/r04/R04-GAP-LIT.json`.

## r04 R04-SMOKE-PLAN

DONE_SCOPED — Capacity and frozen source paths inspected;bounded2000/500 TRAIN-only smoke contract and observed-version requirements saved;no fit or original-environment claim yet

Evidence: `.research_memory/r04/R04-SMOKE-PLAN.json`.

## r04 R04-ASSEMBLY

PARTIAL — All proposal content assembled in original field order;10/10 initial checks,6/6 P2 repair checks;one evidence review saved;independent full argument review interrupted by usage limit;not DOCX/render/full gate

Evidence: `.research_memory/r04/R04-ASSEMBLY.json`.

## r04 R04-ML-SMOKE

DONE_SCOPED — Fresh venv pip check PASS;TRAIN-only three frozen builders fit/serialize/reload;initial41/42 failed bitwise RF17 assertion,diagnosed2.22e-16 parallel-sum drift;repaired45/45 PASS and6/6 audit tests;not final models/G3 closure

Evidence: `.research_memory/r04/R04-ML-SMOKE.json`.

## r04 R04-DEFENSE-CONTENT

DONE_SCOPED — Drafted12-position720-second defense script,evidence walkthrough/final inference dependency runbook and G0-G6 checklist;source/timing validation PASS;not slides/render/rehearsal or live demo

Evidence: `.research_memory/r04/R04-DEFENSE-CONTENT.json`.

## r04 R04-FINAL-CHECKPOINT

PARTIAL — r04 advanced references11/12,gap/relatedwork,full content mapping and assembly,TRAIN-only software smoke45/45,defense content25/25;full argument review interrupted by quota;G0-G6 remain open;no final release

Evidence: `.research_memory/r04/R04-FINAL-CHECKPOINT.json`.

## r05 R05-ASSEMBLY-REVIEW

DONE_SCOPED — Independent full argument/form review and recheck saved;3P1/2P2 addressed in separate r05 draft;34/34 source-boundary checks;author/renderP0 open;no training or release closure

Evidence: `.research_memory/r05/R05-ASSEMBLY-REVIEW.json`.

## P17 2026-10-16 continuation checkpoint

- REPORT source = 5 chapters + main entry; 12 BibTeX sources; 2 P16 figures linked; exact frozen performance numbers unchanged.
- GitHub Actions 38900247221 (first SUCCESS but 16 Overfull); patch cb556fc; run 38901027329 SUCCESS, 0 Overfull, 0 missing glyph, 22 A4 pages. Independent extracted-PDF QA at `report/P17_PDF_QA_2026-10-16.md`.
- G4 technical build/layout = DONE_SCOPED; P17 full = PARTIAL pending administrative form and institutional signoff. No final model/fullTRAIN reproduction and no source data cleanup performed.

## P18 report bibliography closure checkpoint (2026-10-16)

- `P18-REPORT-BIB-QA = DONE_SCOPED`: independently checked all 12 cited keys against report sources, 12 distinct DOI entries and actual XeLaTeX/BibTeX `main.bbl` output; zero duplicate/unresolved/uncited, 0 warnings. See `docs/research/P18_REPORT_BIBLIOGRAPHY_QA_2026-10-16.md`.
- P18 overall PARTIAL because L03 VOR page conflict, varying reading scopes and no exhaustive systematic search. P17 technical PDF QA scoped PASS, institutional final signoff pending.

## P17 user-supplied NetFlow form reference — scoped closure (2026-10-16)

- `P17-PTIT-STYLE-40P = DONE_SCOPED`: referenced the uploaded 64-page NetFlow report for page types/style only; 8 chapters, 40 physical A4 pages, 7 figures, 10 tables, 12 bibliography entries; actual GitHub Actions TeX artifact QA verified no overfull/missing character/out-of-bounds text. Evidence `report/P17_PTIT_40PAGE_QA_2026-10-16.md`; associated source commit `13f310f975fc2405abbf35bd433b35021f630367`.
- G5 admin info, signoff and exact institutional form acceptance remain PENDING_HUMAN. No model retraining, no frozen result edits, no cleanup or identity copying.

## P17 báo cáo 5 chương — phiên bản hiện hành (16/10/2026)

- User requested structure aligned with uploaded NetFlow 5-chapter reference, while preserving original Ensemble Learning experiments. Source assembled into 5 top-level chapters; chapter fragments remain as sections and retain historic content not copied from example.
- Removed abstract; placed substantive acronym table after table of contents. User-visible PDF has no `notebook/`, `results/`, `.md`, `.json`, `SMOKE_ONLY` project text; training process and results remain described.
- GitHub Actions `38916942038` PASS; PDF **37 A4 pages**, 12 bibitems, no duplicate labels, 0 Overfull or missing glyph; scope evidence `docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md`.
- Native Nature Skills only present in user Windows Codex environment; ChatGPT did not load/execute `nature-writing`. Academic source-grounded revision and PDF postflight performed instead.
- P17 remains PARTIAL overall due to approval, actual signatures and other release gates. No retraining or official TEST revisions.

## P15 — GitHub read-only full-TRAIN preflight (16/10/2026)

- `P15-FULLTRAIN-PREFLIGHT = DONE_SCOPED_CODE`: files `tools/p15_fulltrain_preflight.py`, `tests/test_p15_fulltrain_preflight.py` and `docs/research/P15_FULLTRAIN_PREFLIGHT_README.md` pushed to `main` (commit `c64f06e2f7be97a05cf9e5969a2f1679126dd5e4`). Six fixture tests passed in a separate Python runtime; remote paths and content verified by GitHub fetch.
- No Windows/dataset-local preflight or full-TRAIN fitting has been run; the previous environment/capacity NO_GO and G3/P15 PARTIAL remain. Script never reads official TEST/trains and `training_authorized=false` by construction. No raw data/frozen result/script P9 modified.
- Next: after `git pull --ff-only origin main` run the new unit tests and the read-only preflight from repo root, inspect JSON, then design/review the isolated watchdog runner before any full TRAIN operation.

## 16/10/2026 — P15 Windows preflight (author-reported)

- **P15-WINDOWS-PREFLIGHT = DONE_SCOPED_USER_EVIDENCE:** Author ran six fixture unit tests (6/6 PASS) and a read-only preflight (11/12 PASS); evidence recorded in `docs/research/P15_LOCAL_PREFLIGHT_USER_RUN_2026-10-16.md`. This is reported console output, not an independent runner execution.
- **RAM gate FAILED:** available 2,157,973,504 bytes (~2.01 GiB) vs conservative 9-GiB threshold. Other 11 gates pass, including hashes, schema, versions, tracked Git cleanliness and disk. `training_authorized=false`, `reconstruction_status=NOT_RUN`. **G3/P15 still PARTIAL; no full-TRAIN fitting.**
- Next: do not try fitting or bypass memory guard. Continue independent P16/P18 tasks until a proper host and reviewed watchdog runner exist; then re-check on the execution host. Existing published 5-chapter PDF remains unchanged.

## P16 — Independent current 5-chapter PDF/figure audit (16/10/2026)

- **P16-PDF-37P-INDEPENDENT-QA = DONE_SCOPED**. Evidence `docs/research/P16_FIVE_CHAPTER_PDF_RENDERED_INDEPENDENT_QA_2026-10-16.md`. User-supplied PDF verified 37 A4 pages / 0 nonempty text spans out of page; rendered representative 10 pages; figure and results-table placement checked. Frozen CSV and P16 figure sources independently crosschecked: **49/49 PASS**, 0 fail, no new fit/TEST evaluation.
- **Warnings remain:** plotted labels on pages 20/22/29 smaller than 8 pt; heatmap page 22 at ~118 effective dpi; no 300 dpi print certificate. PDF preserved unchanged, no chart regeneration. Canonical **P16 IN_PROGRESS**; P15/G3 unchanged (RAM NO_GO).
- Next: decide standalone higher-resolution heatmap repair for future defense asset, or continue P18 reference verification; don't alter user-approved five-chapter PDF without new request.

## 16/10/2026 — P15 local 12GB watchdog/runner

- **P15-LOCAL-12GB-WATCHDOG = CODE_READY / NOT_WINDOWS_VERIFIED.** New files in `tools/p15_local_supervisor.py`, `tools/p15_local_worker.py`, `tests/test_p15_local_supervisor.py`, and `docs/research/P15_LOCAL_12GB_RUNBOOK_2026-10-16.md`. Author-facing commands are in the runbook. All 4 GitHub blobs were independently compared to locally tested source (SHA-1 exact matches).
- **16/16 isolated unit tests passed on synthetic/stub inputs**, including forced process-tree kill and explicit official TEST/interim CSV read rejection. No live Windows/UNSW-TRAIN run has occurred; **P15/G3 remain PARTIAL, full reproduction NOT VERIFIED**.
- New *alternative* admission policy for a monitored pilot on 12GB Windows: require >=4GiB free RAM (no launch with last user-reported ~2.01GiB), cap process-tree RSS to 2GiB, stop at <1.5GiB free system RAM or <10GiB free disk, up to 20 min per supervised run, one model at a time. **Historical P15 9GiB gate remains FAIL**; alternate thresholds are engineering safeguards, not measured minimum requirements.
- Pilot 10,000 stratified TRAIN-only rows, then full 175,341 TRAIN rows only with a matching passed pilot report and additional <75% cap headroom. CPU affinity 1–2 OS cores; frozen RF n_jobs and CV/hyperparameters unchanged. Worker only imports model builders and does not call P9 main; negative input guards and output new path/no overwrite.
- Next: user `git pull --ff-only origin main`, install fresh Python3.11 deps+psutil, run fixture tests, check available RAM. If <4GiB, **NO_GO, do not force**; otherwise pilot RF-17 first, then report peak and logs before deciding full work. Do not mark READY_FOR_SUBMISSION or inference demo until real reconstruct artifacts pass independent QA.

## 16/10/2026 — P15 12GB CI Windows verified

- **P15-LOCAL-WATCHDOG-WIN-CI = PASS_SCOPED**: GitHub Actions Windows Python3.11 `38928283823` ran **18/18 unit tests PASS**, after fixing Windows 8.3 path alias failures in the first CI run. QA report `docs/research/P15_LOCAL_12GB_WINDOWS_CI_QA_2026-10-16.md`; newly created supervisor/worker/tests/runbook in repo main. Tests include forced stop of a sleeping process and rejection of official TEST/interim CSV and missing full artifact; no ML fitting executed.
- **P15 FULLTRAIN NO_GO at user's reported RAM snapshot**: ~2.01 GiB free; original preflight 9GiB gate FAIL, alternative monitored pilot 4GiB gate FAIL. Continue only after fresh local RAM check >=4GiB and author-run RF17 pilot. New operational policy never overwrites historical 9GiB preflight or frozen results.
- Still missing: measured local pilot, RAM logs and three fully reconstructed artifacts on all official TRAIN; no demo inference or P15/G3 closure. Windows CI PASS does not imply scientific reproduction.

## 16/10/2026 — RF17-PILOT-AUTHOR-EVIDENCE and Git venv hygiene

- **RF17-PILOT-AUTHOR-EVIDENCE = DONE_SCOPED**: author-pushed report at `results/reproducibility/p15_local_rf17_pilot_01/`; PASS and worker PASS, 10,000 TRAIN rows, 17 features, threshold 0.5, exit 0, no TEST. Resource log 24 samples, peak process-tree RSS 370,864,128 B (~353.68 MiB), min available RAM 7,161,253,888 B (~6.67 GiB), starting available 7,474,434,048 B (~6.96 GiB), fit 5.125 s. Frozen P15 input hashes agree. Source `docs/research/P15_RF17_PILOT_GITHUB_EVIDENCE_QA_2026-10-16.md`. No full model artifact, no generalization metric; P15/G3 PARTIAL.
- **GIT-HYGIENE-GATE = OPEN AUTHOR_ACTION**: author commit `ab88db8` unintentionally tracks `.venv-p15-local/` (~7,401 tree items). Main .gitignore updated to ignore this folder and new full model .joblib; **still tracked** until author safely runs `git rm -r --cached -- .venv-p15-local` on Windows then verifies working Python remains and commits/pushes. Do **not** remotely delete tracked venv before user-side untracking; pulling deletion may destroy local environment. Author instructions: `docs/research/P15_GIT_VENV_SAFE_CLEANUP_2026-10-16.md`. No force push/history rewrite.
- Next P15 jobs: independently supervised `random_forest_42` pilot, then `stacking_42` pilot, with fresh >=4 GiB free RAM gate and new outdirs; review peak RSS / compatibility before any fullTRAIN job. Do not infer 10k pilot peak equals fullTRAIN peak.

## 16/10/2026 — RF42-PILOT-AUTHOR-EVIDENCE

- **RF42-PILOT-AUTHOR-EVIDENCE = PASS_DONE_SCOPED**. GitHub author-pushed `results/reproducibility/p15_local_rf42_pilot_01/` logs: 10,000 TRAIN rows, ordered42, threshold0.5, classes[0,1], worker/result PASS, no TEST. Measured peak process-tree RSS383,684,608 B (365.91 MiB) under 2GiB cap; RAM start6,057,549,824 B (5.642 GiB), min5,708,353,536 B (5.316 GiB), 55 samples, fit22.547s, exit0, stop_reason null. Source/builders/config hashes match RF17 and frozen anchors. Independent read-only log/source inspection **19/19 checks PASS** (by field values, not JSON key insertion order). Report `docs/research/P15_RF42_PILOT_GITHUB_EVIDENCE_QA_2026-10-16.md`.
- **GIT-VENV-CLEANUP = HEAD_VERIFIED**: current tracked tree has 0 `.venv-p15-local/` paths; original previous tracking of thousands of installed library files addressed without a history rewrite; ignores in `.gitignore`. Local physical venv still expected; RF42 pilot ran with it.
- P15 state: **RF17 pilot PASS, RF42 pilot PASS, Stacking pilot NOT_RUN, all three full TRAIN NOT_RUN**; P15/G3 still PARTIAL. Next Stacking pilot on fresh >=4 GiB free system RAM, under resource watchdog 2 GiB RSS cap; no automatic extrapolation to full TRAIN. User must pull current main and execute locally; checkpoint after Stacking logs.

## 16/10/2026 — STACK42-PILOT-AUTHOR-EVIDENCE = PASS_DONE_SCOPED

- Author push `b4707dc`: Stacking-42 pilot (10,000 TRAIN, 42 ordered features, threshold 0.5) `PASS`, worker passed, exit0, no watchdog stop, **170 resource samples**. Max sampled tree RSS `368455680` B (351.39 MiB of 2GiB cap), start available RAM `6140862464` B (5.719 GiB), min available `5776723968` B (5.380 GiB), fit `80.968 s`. Matching four frozen source hashes; no TEST. Independent source/log arithmetic **21/21 checks PASS** across all three pilots; QA `docs/research/P15_STACKING_PILOT_GITHUB_EVIDENCE_QA_2026-10-16.md`.
- P15 pilot checkpoint: **RF17=PASS, RF42=PASS, Stacking42=PASS**, all as 10k TRAIN-only software/resource checks. **NO FULL TRAIN ARTIFACTS** and P15/G3 remain PARTIAL; canonical 9GiB gate still false. Pilots do not guarantee full memory/runtime.
- **NEXT ACTION (user host):** fresh RAM>=4GiB, disk>=10GiB, no competing runs; first `random_forest_17` `--mode full` with matching RF17 pilot report, unique `results/reproducibility/p15_local_rf17_full_01` output and 2GiB tree RSS watcher. Confirm `run_report.json`, worker `train_rows=175341`, actual joblib artifact/hash on user disk and resource log before authorizing RF42 full. Do not push large .joblib or raw dataset; no TEST read or frozen result update. 20min timeout per model.

## 16/10/2026 — P15-RF17-FULL-AUTHOR = PASS_SCOPED_AUTHOR_EVIDENCE

- User pushed `results/reproducibility/p15_local_rf17_full_01/` to main at `78e9111`. Author-run watchdog `result=PASS`, worker passed, `mode=full` trained **175,341 official TRAIN rows** with frozen 17 features, binary classes [0,1], threshold0.5. Fit307.453s; 620 sampled RSS observations; peak535,023,616 B (510.24 MiB of2GiB), minimum system available5.222GiB, initial5.553GiB; exit0, stop_reason=null, no TEST. Frozen scientific source hashes match. Local artifact reported `random_forest_17_RECONSTRUCTED_FULL_TRAIN.joblib`,22,169,429 bytes, SHA256 b2751bfc6677a724bcadc85070e5848c0f183c3c81d508b5e4cdae82287c8818. Supervisor verified local file on author machine; independent review of pushed logs **20/20 checks PASS** but binary not uploaded/independently loaded. Scope and warnings: `docs/research/P15_RF17_FULL_TRAIN_GITHUB_EVIDENCE_QA_2026-10-16.md`.
- **Progress: 3/3 pilots PASS, 1/3 full TRAIN author-evidence PASS (RF17), 0/2 remaining full (RF42, Stacking). G3/P15 remains PARTIAL**, original 9GiB gate not passed, alternative monitored admission used. No new scientific TEST metrics, frozen results, thesis PDF or historical script changed.
- Next: user pulls and runs only `random_forest_42` full under same bounded supervisor and matching RF42 pilot with new `p15_local_rf42_full_01` output. Fresh available RAM>=4GiB, disk>=10GiB, no concurrent fit, 2GiB tree RSS cap; do not assume success from RF17 memory profile. Review logs before Stacking full. Don't push full binary joblib.

## 17/10/2026 — P15-RF42-TIMEOUT-RECOVERY-NO-DEADLINE

- **RF42 FULL attempt #01 = INCOMPLETE/TIMEOUT (do not present as fit success).** User pushed `results/reproducibility/p15_local_rf42_full_01/run_report.json` to main commit `5c02bf5`: resource log 2358 samples (last1200.12s), peak RSS483,598,336 B (~461.20 MiB), RAM available min5,823,201,280 B (~5.424 GiB), disk min30,537,601,024 B; stop_reason TIMEOUT, exit15, worker_checks FALSE. RAM did not hit 2GiB cap or 1.5GiB floor; no final model artifact from aborted attempt. Evidence and QA `docs/research/P15_RF42_TIMEOUT_RECOVERY_NO_DEADLINE_2026-10-17.md`.
- **Author-approved operational exception:** user requested no wall-time limit for BOTH remaining full candidates, with Windows laptop ~8–9GiB available RAM after closing apps (prospective claim, NOT a measured current reading). Change scoped to `--mode full --timeout-min 0`; pilots retain 5–20min bounded policy. Supervisor still continuously checks process-tree RSS<=2GiB, >=1.5GiB system free RAM, disk>=10GiB, initial RAM>=4GiB, source hashes/provenance/heartbeat, and cleans up process on abort; no scientific source/config/TEST/frozen results modified.
- **Windows CI verified:** [run 38940865179](https://github.com/nphu0811/EnsembleLearning/actions/runs/38940865179), 21/21 stdlib/psutil synthetic safety unit tests PASS and `tools/p15_run_remaining_full_windows.ps1` parsed by pwsh PASS. No live training in CI, no guarantee that full models fit.
- **NEXT:** user `git pull --ff-only origin main`, confirm fresh available RAM/disk and no other training, then execute **only** `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\p15_run_remaining_full_windows.ps1` from Windows repo root. Script runs RF42 full in new `p15_local_rf42_full_02` then Stacking full in new `p15_local_stack_full_01` ONLY IF RF42 report PASS and 175341 rows; no detached jobs or auto retry, no timeout cap for either. Keep power connected and automatic sleep disabled while running, preserve raw/model/P17/P9/historical reports, do not push .joblib. G3/P15 PARTIAL until both full, direct artifact QA/provenance independent review.

## 2026-10-17 — P15-THREE-FULL-AUTHOR-LOGS-2026-10-17

- **P15 FULL TRAIN RECONSTRUCTION = THREE_AUTHOR_RUNS_PASS_SCOPED**. User push `d090c163a3c20f5637a8e500fdb7afc552ddbe9f` includes RF17 full `p15_local_rf17_full_01`, RF42 full `p15_local_rf42_full_02`, Stacking42 full `p15_local_stack_full_01`, each with `run_report.json` PASS, `worker_result.json` passed, 175341 frozen TRAIN, threshold0.5, expected 17/42/42 features, input SHA matches, no TEST, exit0, no watchdog stop. Cross-checked report/start/worker/resources **75/75 read-only consistency assertions PASS**; source `docs/research/P15_THREE_FULL_TRAIN_AUTHOR_EVIDENCE_QA_2026-10-17.md`.
- **Measured fit/RSS**: RF17 307.453s /510.24MiB; RF42 1867.234s /693.57MiB; Stacking42 4759.094s /725.33MiB. All below 2GiB sampled process RSS ceiling, no low-RAM/disk watchdog trigger; user-side local serialized model SHA/size recorded but binary not pushed. Original RF42 #01 INCOMPLETE/TIMEOUT preserved; RF42 #02 fresh PASS. Full reconstruction in observed Python3.11.9/scikit-learn1.9.0 environment; **NOT ORIGINAL historical model identity**.
- **P15 ARTIFACT QA = PENDING_LOCAL_INDEPENDENT_LOAD**. Added `tools/p15_verify_full_artifacts.py` plus `tests/test_p15_artifact_acceptance.py`, fixture-only Windows CI; this verifier must run on author's own laptop and check all three actual joblib SHA/size, fitted estimator configuration, ordered schema, 16 TRAIN-derived rows probability semantics without fit/TEST. Upload only `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. Until reviewer sees PASS and independent provenance QA, P15 **PARTIAL / G3 not closed**. Do not retune, rerun TEST, change official PDF or claim new performance.

## 2026-10-17 — P15-ARTIFACT-VERIFIER-WINDOWS-CI

- New `tools/p15_verify_full_artifacts.py`: author-side, **read-only joblib verification** for 3 trusted local P15 full artifacts; input SHA/source/env comparison, actual file SHA256/size before+after deserialization, fitted estimator/frozen config/schema inspection, 16 official TRAIN-derived rows `predict_proba` sanity checks, **NO FIT, NO OFFICIAL TEST, NO scientific score**, exclusive output `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. Do not run joblib.load on untrusted downloaded pickle data.
- Windows GitHub Actions [run 38986685352](https://github.com/nphu0811/EnsembleLearning/actions/runs/38986685352) **PASS**, 21/21 watchdog tests +6/6 verifier fixture tests, plus compilation & PowerShell parse. Initial new-verifier CI run failed a test-file syntax typo (not runtime/science); repaired, preserved failure history.
- **P15 ARTIFACT INSPECTION STILL PENDING ON USER MACHINE.** Windows CI tests only fake files; they DO NOT load author's 3 actual .joblib models. User must pull, run verifier and push JSON result, then source-reviewed scientific gate decision. Avoid P15/G3 release-ready assertion until reviewed.

## 17/10/2026 — P15-DONE_SCOPED_RECONSTRUCTION / LOCAL_ARTIFACT_QA_ACCEPTED

- **Author acceptance report:** `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json` pushed commit `c81f99a548045d0f6900bec65509ad35da32a073`; `passed=true`, `training_performed=false`, `official_test_opened=false`.
- **Local actual binary checks 69/69 true**: RF17 20/20, RF42 20/20, Stacking42 29/29 (SHA256, byte sizes, model load, frozen fitted hyperparameters, 17/42 feature schema/order, labels[0,1], threshold0.5, 16 TRAIN-row probability sanity, unchanged hash after load). Remote consistency recheck of author report vs 3 worker+supervisor full TRAIN reports: candidate, model hash/size, inputs+versions, 175341 TRAIN rows and pass status all match. Earlier 75/75 read-only logs consistency pass retained. Actual binaries were checked on user Windows laptop, **not loaded by remote reviewer**; files are not in public Git.
- **P15 = DONE_SCOPED_RECONSTRUCTION**, record `docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md`. Historical 9GiB admission never claimed PASS; alternate resource-supervised 12GB local execution used. RF42 old TIMEOUT INCOMPLETE preserved. No test recomputation, no re-selection, no frozen PDF edits. **G3 overall remains PARTIAL / external binary review, original environment & live-demo/release approval OPEN**; administrative/writing/reference/source rights G0–G6 not auto-closed.
- **Do not repeat fit**. Next work: candidate-specific demo contract and release rights, P16/P18/P19/P20, source verification and proper manuscript+delivery gates. Re-verify only into NEW unique artifact QA outdir if necessary; original 3 models and acceptance JSON kept unchanged.


## P19 inventory finding, current 17/10/2026

The tracked review snapshot flags three historical SMOKE_ONLY.joblib files under results/reproducibility/r04_ml_smoke_repaired/smoke_models/. All three were tracked in initial commit c4ed771. No new model binary is staged; no files were loaded or removed. Inventory passed=false and code license is absent. Keep this release blocker; it is separate from accepted local P15 full-TRAIN reconstructions. Do not treat the final new-file staging check as a passing whole-repository release inventory. See release/review_inventory_2026_10_17_01/validation.json and the final review inventory snapshot.

## P20-PRE SYNTHESIZED / LOCAL_PACKET_QA_PENDING 2026-10-17

- From author GitHub commit `b3acf2e`, all 3 simulated AI reviewer files exist, C upload matches SHA-256. Reports unmodified; A/B post-hoc freeze + C original freeze indexed; 8 Major / 9 Minor (A3/4, B2/3, C3/2), 46 reviewer questions; 3/3 `MAJOR_REVISION_REQUIRED`.
- `defense/p20_pre_2026_10_17_01/synthesis/concern_register.json` maps 17/17 into 9 OPEN groups (5 multi-reviewer), preserving severities; `synthesis/P20_PRE_SCIENTIFIC_REVIEW_SYNTHESIS.md` and `synthesis/AUTHOR_RESPONSE_MATRIX_DRAFT.md` accompany, but do NOT close concerns or authorize PDF edits. Draft 27 answer questions + 13 slide outline remain unfinalized; P20 final DEFERRED.
- GH Actions review audit `https://github.com/nphu0811/EnsembleLearning/actions/runs/38992306762` PASS **944 checks/0 fails**, warning count 2 and 14 packet-only pointers skipped in remote: original manifest receipt SHA vs committed manifest differs, and A-Q11-e1 CSV header differs vs tracked data table. **No full 80-file local packet validation done by assistant.** Read-only remote source spot audit 85/85 anchor matches five source files.
- **NEXT:** author `git pull --ff-only origin main`, then run `python -X utf8 tools/p20_validate_pre_review.py --phase reviews --out-dir defense/p20_pre_2026_10_17_01/qa_reviews_01` once on Windows laptop, investigate any FAIL before `--phase complete` into a fresh dir. Push validation JSON only. Preserve original 37-page PDF, frozen TEST, configs, models and old review reports; no human panel claims.

## 2026-10-17 — A-Q11 one-anchor local P20 QA exception documented

- Author-host `tools/p20_validate_pre_review.py --phase reviews --out-dir defense/p20_pre_2026_10_17_01/qa_reviews_01`: **1195 strict checks PASS, 1 strict FAIL** = exact `A-Q11 pointer1 literal anchor`. The frozen reviewer A says CSV header `split,label_name,count,percentage` but original and committed `results/eda/unsw_nb15/tables/binary_class_distribution.csv` uses `split,label,class_name,count,percentage`. Source CSV/packet path SHA in manifest `84e76743c9e423bf1db67afe15c1eb6091664fe57951f4beb78eb6edb38953a8`.
- Added independent `defense/p20_pre_2026_10_17_01/REVIEWER_A_Q11_CITATION_ERRATUM_2026-10-17.md`; no reviewer/file/manifest source rewritten. Scoped validator recognizes ONLY that one exact proven mismatch if packet and source SHA match, preserves original `failed=1`, distinguishes `accepted_exception_count=1`, `unresolved_failed=0`, `status=PASS_WITH_DOCUMENTED_CITATION_ERRATUM`. Any other failure remains unresolved and exits nonzero. Regression tests `tests/test_p20_anchor_erratum.py` added.
- **NEXT author laptop**: `git pull --ff-only origin main`; run reviews to NEW `qa_reviews_02`; only if status `PASS_WITH_DOCUMENTED_CITATION_ERRATUM` and unresolved=0 run `--phase complete` into NEW `qa_complete_01`. Preserve `qa_reviews_01` raw strict failed result. Do not upload 80-file copied packet, official TEST, original PDF, .joblib binaries or alter original review outputs. P20 final still DEFERRED; 9 reviewer concerns OPEN.

## 2026-10-17 P17 revision 45-page PDF integrated RQs

- User authorizes new revised 5-chapter **single PDF submission candidate**, original 37-page approved PDF frozen SHA preserved. New TeX is versioned under `report/main_revision_2026_10_17.tex` plus separate chapter copies; original P17/report source untouched.
- Final new PDF actually built `45` A4 pages; `424665` bytes, SHA256 `828625f3dc6d21d9af0daa4cfa9e36b4cdc3a8128bfca66fa29467a28df58d3a`, GitHub successful XeLaTex run `38994119619`. QA includes RQ1–RQ5 embedded, 13 refs with N02, P15 updated and old stale statement absent, 0 out-of-page text bounding boxes, page-break/table placement manually re-reviewed. Original SHA `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`.
- Evidence `docs/research/P20_RQ1_RQ5_INTEGRATED_PDF_REVISION_QA_2026-10-17.md`; PDF delivered as conversation file, reproducible via GitHub Actions build artifact. 4 P20 Major grouping domains addressed in revised wording and tables; **not yet formally accepted/closed by reviewers**. All frozen science holds.
- **Current manuscript QA = DRAFT_REVISION_READY_FOR_AUTHOR_REVIEW**, not formal READY_FOR_SUBMISSION. User only submits PDF, no external appendix. P20 final DEFERRED, independent human review absent, P18/P19 and G0–G6 separately tracked.

## 2026-10-18 — P21 four pilot PASS; FULL SCIENCE RUNNER IMPLEMENTED, UNEXECUTED

- Author-host P21 RQ5 3-arm resource pilot PASS: 8000 FIT, peak 316.4 MiB, elapsed 91.25 s; commit d2af75c; no validation scoring or official TEST. Local synthetic tests 8/8 sampling, 6/6 RQ5 acceptance PASS.
- Author-host Stacking-Lite FIT-only resource pilot PASS: 8000 FIT, 42 original features, 3-fold, peak 336.0 MiB, 90.812 s wall, 38.937 s fitting; author commit c075191; official TEST/outer validation not scored. Local stack acceptance 6/6 and static protocol 30/30 PASS.
- New science modules `tools/p21_science_core.py`, `p21_science_worker.py`, `p21_science_supervisor.py`, `p21_science_acceptance.py`, `p21_science_aggregate.py`, `p21_run_all_seeds.ps1` committed and CI wired. **NO FULL SCIENTIFIC FIT RUN SO FAR**, newly added synthetic science/aggregation tests and CI status not yet author-verified.
- Explicit pre-full amendment: Stacking inner OOF switches from ungrouped 3-fold to 3-fold `StratifiedGroupKFold` on exact original FIT predictor vectors; folds group-disjoint and precomputed before science evaluation. Recorded in `docs/research/P21_PRE_FULL_SCIENCE_GROUP_SAFE_CV_AMENDMENT_2026-10-18.md`. No changes to historical P9 or official TEST.
- Five independent launches by preselected FIT seeds [1103,2207,3301,4409,5501]; each fits 60000 only from TRAIN 140272 FIT pool, same internal validation 35069, five fixed arms A0-A4; selection fresh per seed. Scores post-hoc reused TRAIN internal ONLY, not new independent benchmark; aggregation requires 5/5 verified seed outputs, descriptive mean±SD, no claim of statistical superiority.
- User requested NO wall-time limit on heavy training. New full-science supervisor has **no full wall-clock deadline** while retaining RSS 2GiB, system RAM floor 1.5GiB, startup >=4GiB RAM and disk >=10GiB, one CPU, heartbeat, no silent retry/overwrite. Four pilot reports must be present before worker starts.
- `docs/research/P21_FULL_SCIENCE_PREEXECUTION_HANDOFF_2026-10-18.md` defines Windows exact checks; author action AFTER CI/synthetic success: `git pull`, run 3 new test suites and protocol SHA audit, then `& .\tools\p21_run_all_seeds.ps1`. **Never claim outcome before author runs.**
- `.gitignore` now ignores future transient heartbeat/go.signal/resources.csv/progress; already-tracked pilot telemetry stays in Git history, no destructive history rewrite.
- PDF V3/NotebookLM exact ten-issue page-specific repair remains NOT DONE; do not update evidence tables without measured science, do not invent NotebookLM verbatim remarks. P18/P19 rights and P20 final approvals remain open.

## 2026-10-19 — P21 Scientific seed1103 author-host PASS, 1/5 (immutable result)

- Author committed first **full scientific P21 TRAIN-derived internal-validation** result `e387d9f`; 5/5 arms completed **for seed 1103 only**. Independent read-only JSON consistency review **12/12 PASS**; see `docs/research/P21_SCIENCE_SEED1103_ACCEPTANCE_2026-10-19.md`. Report fields: `PASS_INTERNAL_TRAIN_VALIDATION_SEED_ONLY`, exit 0, no stop reason, 1839.844s, peak RSS 375.5 MiB, 3608 resource samples.
- Fixed 60k FIT subset and shared 35069 internal validation; normal support 11200, attack 23869. Full TRAIN SHA verified in report; official TEST NOT read as reported. Fresh 17 feature subset for seed1103 selected only on FIT. Stacking inner 3-fold group-disjoint under prior amendment.
- **Results provisional, single seed**: A0 RF42 Macro-F1 .944741/MCC .889842/FN 625/FP1043; A1 RF17 .938678/FN705/FP1145; A2 Balanced .944006/FN1031/FP690; A3 Oversample .944235/FN897/FP807; A4 StackLite .944444/FN655/FP1024. Metrics independently recomputed from confusion matrices, no significance claims; results apply ONLY to P21 post-hoc reused-TRAIN validation.
- **IMPORTANT metadata interpretation**: nested `split.validation_evaluation_performed=false` records **pre-fit split audit**, while five arm metrics demonstrably scored *internal validation*. The distinction must be explained in final PDF; do not claim no validation was scored. Do not edit originally committed reports or retrain seed1103 to change unfavorable results.
- **NEXT:** author should pull new QA-only commit and re-run `& .\tools\p21_run_all_seeds.ps1`, which will SKIP accepted seed1103 and sequentially execute seeds [2207,3301,4409,5501]. No full wall timeout; resource watchdog remains. Then independent acceptance and 5/5 summary, then NotebookLM-specific PDF V3 corrections. Do not publish partial seed1103 as complete RQ findings.

## 2026-10-19 — P21 5/5 SCIENCE RESULT COMPLETE / V3 PDF BUILT 56 PAGES

- Author-host completed all FIVE predeclared FIT seeds [1103,2207,3301,4409,5501] with 5 matched arms each (25/25 scientific fits); published aggregate author commit `6806542`. All 25 model metrics verified independently by recalculating Macro-F1/MCC/FPR/FNR from confusion counts; paired FIT identity and shared validation support consistent. Read-only acceptance doc `docs/research/P21_FIVE_SEED_SCIENCE_FULL_ACCEPTANCE_2026-10-19.md`; new strict stdlib verification `tools/p21_verify_full_five_seed.py` is also V3 CI gate.
- Core means (post-hoc reused-TRAIN INTERNAL VALIDATION ONLY): A0 RF42 MacroF1=0.945220, MCC=0.890971, FPR=9.6196%, FNR=2.3989%; A1 RF17 0.936751; A2 weighted 0.943877; A3 oversample 0.944886; A4 StackLite 0.944731. Deltas arm minus RF42: RQ1 Stack Δ MacroF1 -0.000488/FNR +0.1726pp; RQ2 RF17 -0.008468/FNR +0.5337pp; RQ5 weighted -0.001343/FPR -3.1643pp/FNR +1.7881pp; oversample -0.000334/FPR -2.2089pp/FNR +1.1680pp.
- COST nuance: RF17 FIT only 84.600s vs RF42 241.119s, but fresh FIT-only stable17 selector 225.250s per seed; selector+RF17 FIT 309.850s, ~28.5% longer than RF42 FIT. 14/17 features common to all five seed selections.
- **V3 full five-chapter report PDF has ACTUALLY COMPILED and been committed by GitHub Actions** commit `1419d682`. Path `exports/report_revision_v3_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V3.pdf`, 56 A4 pages, SHA256 `6fc7ea9e11cd892ea0f2cc9dccf12dee920620508c1c6a58b7649487804e0e8a`. Source commit of build `16cd595`; XeLaTeX/BibTeX, text extraction, required old/new outcomes, undefined citations, missing glyph and overfull hbox checks PASSED. Build QA `docs/research/REPORT_REVISION_V3_QA_2026-10-19.md`. Visual page-by-page render QA remains **PENDING** (do NOT claim final print-ready). V2/P9/P15 untouched.
- Five-chapter TeX V3 entrypoint `report/main_revision_v3_2026_10_19.tex`; matching V3 introduction/methodology/RQ/results/validity/conclusion chapters. Replaced stale old RQ1/2/5 summary claims, disclosed non-independent P21 shared validation, three classes of uncertainty; P21 source hash and group-safe OOF amendment are clearly separated from official TEST history. No direct .md source path references in printed report.
- Exact raw NotebookLM 10 comments/page anchors were not provided in this turn or available in repo. Current revision addresses documented deficiencies rather than certifying exact review closure. Future tasks: visual 56-page PDF QA/author read-through, NotebookLM precise comment crosswalk if supplied, approval/rights/P18-P20. Do not retrain full P21 or retune parameters based on achieved metrics.
