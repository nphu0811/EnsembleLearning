## P21 stable17 selector pilot source QA PASS — 18/10/2026

**Current P21 next step:** TRAIN-fit-only 17-feature selector pilot was IMPLEMENTED, not run on author laptop. It checks sample exclusivity, performs 5 seeds × 3 methods (MI redundancy, L1 Logistic Regression, ExtraTrees single-threaded), ranks exactly 17 original predictors deterministically, discards pilot feature names, and never scores validation/TEST. The launcher has a separate opt-in token, ≤20min wall-time, one CPU, 2GiB RSS tree cap, 1.5GiB system RAM floor and 4GiB starting available gate. Synthetic GitHub QA [39065559976](https://github.com/nphu0811/EnsembleLearning/actions/runs/39065559976) SUCCESS: **30/30 stdlib tests, 7/7 synthetic ML tests, 29/29 frozen source/protocol checks**. Exact usage and scientific caveats: [P21 selector pilot QA](docs/research/P21_SELECTOR17_FIT_ONLY_PILOT_QA_2026-10-18.md).

**Status: CODE_READY; AUTHOR_SELECTOR_PILOT_NOT_RUN; FULL_P21_RQ1_RQ2_RQ5_NOT_AUTHORIZED.** Previously accepted RF42 8k pilot unchanged. After user runs selector pilot, audit resource/metadata report before building separately approved class-weighting/oversampling and Stack-Lite pilots. Neither pilot creates new official TEST metrics or warrants PDF V3.

---

## P21 RF42 pilot 8000 TRAIN rows — accepted scoped 18/10/2026

**Latest P21 update:** User pushed commit `34bcdeac4dd4379413154de6aad88ccec8c89a60` with `start.json`, `run_report.json`, `worker/worker_result.json` for supervised **8000-row official TRAIN-only RF42 resource pilot**. Final supervisor status `PASS_RESOURCE_SMOKE_ONLY`, exit0, 51.86s wall, 11.391s fit+16 TRAIN probe, peak 371728384B (~354.5MiB), min available 4333109248B (~4.04GiB), 101 watchdog samples; fold0 group-disjoint fit pool140272/validation35069, **zero validation predictions**, no TEST or accuracy metrics. A read-only cross-record auditor now validates committed reports: **14/14 acceptance checks PASS**, 5 report fixture tests PASS, [CI 39062897494](https://github.com/nphu0811/EnsembleLearning/actions/runs/39062897494) SUCCESS (29 unit tests total +29 static source checks). Review `docs/research/P21_RF42_PILOT_AUTHOR_RESULT_ACCEPTANCE_2026-10-18.md`.

**P21 current status** `RF42_ANCHOR_PILOT_DONE_SCOPED; RQ1/RQ2/RQ5_SCIENTIFIC_RUNS_NOT_AUTHORIZED`. User-local 101-sample telemetry file not committed or independently read on GitHub; do not misstate evidence scope. Next: implement **TRAIN-fit-only 17-feature selector pilot** with leakage/resource guard and synthetic tests; then separate weighting/oversampling/Stacking pilots; only with explicit author approval run full matrix. V2 PDF, TEST, P15 and P20 original snapshots untouched.

---
## P21-PILOT IMPLEMENTED, NOT RUN — 18/10/2026

**New after P21 design:** author verified TRAIN-only local static preflight `30/30 PASS`, including TRAIN source SHA, without model fit or official TEST. Implemented *only the RF42 anchor resource smoke* in `tools/p21_pilot_supervisor.py` + `tools/p21_pilot_worker.py`, with separate `tools/p21_pilot_guards.py`; implementation evidence `docs/research/P21_RF42_PILOT_IMPLEMENTATION_QA_2026-10-18.md`. It requires exact author opt-in token, starts with >=4GiB available, >=10GiB free disk, enforces 2GiB process-tree RSS and 1.5GiB system free floor, one logical CPU, <=20-minute timeout, no scientific validation metrics and no artifact. **CI [39061822482](https://github.com/nphu0811/EnsembleLearning/actions/runs/39061822482) PASS: 14 protocol tests + 7 resource guard tests + 3 synthetic group-split tests + 29 static source checks.** No dataset used by CI and no ML fit performed. **P21 training has NOT occurred.** RQ2 selector stability, weighting/oversampling and RQ1 Stacking pilots remain OPEN and require separate review; this one smoke does NOT approve 5x5 scientific matrix or PDF V3. Next: author separately decides whether to run the opt-in RF42 pilot; do not run in assistant/background.

---
# CHECKPOINT HIỆN HÀNH — 18/10/2026: PDF V2 đạt QA, chờ phản biện lại bản thảo

**Nguồn có ưu tiên cao nhất cho tiến độ P15–P20 hiện hành:** checkpoint này; các bản dưới là lịch sử, không dùng làm trạng thái mới nhất. Commit nguồn build: `964216c720bac26d6aea838ad03931238ebbece6`; [GitHub Actions V2 PASS](https://github.com/nphu0811/EnsembleLearning/actions/runs/38999397120). PDF hiện có tại `exports/report_revision_v2_2026_10_17/Bao_cao_NCKH_EnsembleLearning_REVISION_V2.pdf`: **47 trang A4**, SHA256 `5300f9de92a7fc3834294b015382acfff80c9f0384ef9d6a32419e2bf72b52f3`. PDF gốc 37 trang, SHA256 `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`, không thay đổi. Biên bản `docs/research/REPORT_REVISION_V2_PRINT_FIX_VERIFIED_2026-10-17.md`.

| Phase | Trạng thái ưu tiên hiện hành | Phần chưa hoàn tất |
|---|---|---|
| P15 | **DONE_SCOPED_RECONSTRUCTION**: RF17, RF42, Stacking42 full official TRAIN, 3/3 PASS, 69/69 author-host artifact checks | Original historical environment/bitwise identity và release/demo acceptance chưa xác nhận; không train hoặc mở lại TEST |
| P16 | **DONE_SCOPED_AUDIT_WITH_OPEN_PRINT_FINDINGS** | V2 47 trang đã sửa bố cục và qua XeLaTeX QA, nhưng heatmap gốc hiệu dụng ~118dpi và chất lượng chữ nhỏ vẫn cần xem ở cỡ in |
| P17 | **REVISION_V2_PDF_TECH_QA_PASS / AUTHOR_FINAL_REVIEW_PENDING** | 5 chương, RQ1–RQ5 tích hợp trong **một PDF**; cần tác giả kiểm nội dung, mẫu biểu, thông tin hành chính và ký duyệt, không tự tuyên bố sẵn sàng nộp |
| P18 | **PARTIAL**: 7 bài đối chiếu, đọc các mục liên quan của 3 bài, 136 kiểm tra scoped PASS | L03 publisher VOR/phân trang, paper chưa tiếp cận toàn văn, giới hạn novelty/metadata và kiểm chứng nội dung sâu |
| P19 | **PARTIAL / INTERNAL_REVIEW_ONLY**: allowlist/ZIP nội bộ được QA | LICENSE, quyền phân phối code/model/data/PDF và 3 smoke joblib Git-tracked chưa quyết định; không công bố release |
| P20 | **PRE_REVIEW_QA_ACCEPTED_WITH_ERRATUM; FINAL_DEFERRED** | 3 reviewer AI, 17 concerns → 9 nhóm đều OPEN trong register; local P20 complete 1400 PASS/1 literal anchor FAIL được giải trình A-Q11, 0 unresolved. **Chưa adjudicate/review lại PDF V2**; không phải 3 reviewer là người thật hay P20 final |

**Thứ tự công việc đúng tiếp theo:** (1) tác giả đưa **duy nhất PDF V2 chính xác** vào NotebookLM để yêu cầu phản biện theo trang và tách rõ lỗi chắc chắn/thiếu minh chứng/ngoài phạm vi; không dùng tóm tắt tự động làm bằng chứng; (2) triage từng phát hiện, kiểm chứng với source/result frozen trong Git; (3) chạy `P20-PRE post-V2` hoặc vòng reviewer mô phỏng mới độc lập trên đúng SHA của V2, phân xử từng G01–G09, giữ concern OPEN nếu chưa đạt acceptance test; (4) kiểm tra chất lượng in và thông tin nộp/chữ ký, quyền trích dẫn/tài liệu; (5) chỉ đóng final/gates theo bằng chứng. **Không retrain, không retune/đọc lại official TEST hoặc sửa số liệu để đạt claim.**

**Cảnh báo trạng thái lịch sử:** các dòng phía dưới ghi `P17 37 trang`, `P20 chỉ chuẩn bị`, `P15 chưa full TRAIN` hoặc `G4 chưa build PDF` là checkpoint trước các cập nhật này. G0–G6 tổng thể **không** tự được nâng PASS; `NOT_READY_FOR_UNCONDITIONAL_SUBMISSION` vẫn đúng về kiểm định khoa học/phê duyệt.

---


# 17/10/2026 — revised five-chapter PDF integrates RQ1-RQ5

**NEW VERSION approved for author-side drafting**: a separate single-file PDF of 45 physical A4 pages has been built by XeLaTeX with direct quantified answers to all RQ1–RQ5, OOF/Voting/Diversity and prior art, and corrected P15 reconstruction provenance in the five chapters. See `docs/research/P20_RQ1_RQ5_INTEGRATED_PDF_REVISION_QA_2026-10-17.md` and successful Action `38994119619`. Original user-approved 37-page PDF/source and frozen model/evaluation results unchanged. RQ1 stable gain across training runs, RQ2 isolated causal feature effect, RQ3 diversity mechanism, RQ5 matched class-imbalance interventions all remain unverified; RQ4 result scoped to same TEST vector-overlap subset. **Revised PDF is pending user content approval; P20-final and release gates still open.**

---

# P19 safe-release update —17/10/2026

P19PARTIAL:3trackedhistoricalsmokemodelsread-onlyinventoried,Gitblob/local/metadatahashesagree. Noindexcleanupneededforallowlistdraft. Local INTERNAL_REVIEW_ONLY ZIP46entries,245mechanical+121independentchecksPASS,3path testsPASS;notpublicauthorized,norunnabletrainingrelease,noFINAL. Code/data/model/report/template/thirdpartyrightsremain. docs/research/P19_SAFE_RELEASE_AUDIT_2026-10-17.md and trackedmanifestshowexactscope. P20rubric/setupready,fullpanelDEFERRED. P18sevenpaper/3selectedbodyreads remainsPARTIAL;L03VOR/accessgapsopen. P15DONE_SCOPED_RECONSTRUCTION,P16DONE_SCOPED_AUDIT_WITH_OPEN_PRINT_FINDINGS. NoPDF/bib/frozenresultchanges.

---

# P18 deep verification update —17/10/2026

P18 remainsPARTIAL. SelectedMethods/results/limitationsread for3closestpapers in7papershortlist;136source/identitychecksPASS,24assertionsmapped. NewN02priorartusesUNSW+MI-Boruta+stackingbutmergedrandomsplit;nohead-to-headscoreclaim. L12notUNSWandpublishedreportingscopeconflictretained. L03VORunavailable,U01/U03verifiedscopeunchanged. See docs/research/P18_DEEP_METHODS_VERIFICATION_2026-10-17.md. P19safeallowlistinternaldraftnext;P20deferred. P15DONE_SCOPED_RECONSTRUCTION;P16DONE_SCOPED_AUDIT_WITH_OPEN_PRINT_FINDINGS;approved37pagePDFuntouched.
---

# Current roadmap checkpoint 17/10/2026 — P16/P18/P19

P15 remains DONE_SCOPED_RECONSTRUCTION;no additionalTRAINfitting. P16 savedsummary2132checks and actualauthorPDF178checksPASS;all37pages rendered/contact-reviewed;17displaymap saved. Six independent183mmPDF/SVG/600dpiPNG alternatives passedtext6/6andcollision6/6. P16 overall IN_PROGRESS because unchangedapprovedPDF hasfont/118dpiheatmap/snapshot-agefindings, and historical6/12collisionflags remain. See docs/research/P16_COMPREHENSIVE_QA_2026-10-17.md.

P18 offline currentreportmetadata/claim-context/readingledger119/119PASS,12refs/24instances;no newfulltextreads ornetworkqueries. U01/U03existingfollowup takesprecedence over stale memory. L03publisherpagination andclosest-methodreading/noveltyworkremain. P19README,QArequirements,availabilityreviewandreviewinventoryadvancewithinPARTIAL;noFINarchive. P20finalpaneldeferredinputgates. AllG0-G6remainseparatelygoverned;NOT_READY_FOR_SUBMISSION.

Next safe work: exactsourceTRAIN-only highresolutionheatmapplan orP18source-groundedreading;complete proposalform/defenseandrightsindependently. Do not modifyapprovedreport orreruncompletedP15. Currenthandoff is authoritative.

---

# Roadmap hiện hành sau resume ngày 16/10/2026

## Cập nhật P15 ngày 17/10/2026 — trạng thái ưu tiên hiện hành

**P15 = DONE_SCOPED_RECONSTRUCTION**: cả 3 mô hình frozen RF17/RF42/Stack42 đã fit 100% official TRAIN trên laptop tác giả; `run_report.json` đều PASS, full artifact `*_RECONSTRUCTED_FULL_TRAIN.joblib` được author-host read-only SHA/deserialize/structure/probability QA `artifact_acceptance.json` xác nhận 69/69 checks true, đối chiếu remote metadata PASS. Tài liệu chính thức: `docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md`. Đây không phải ORIGINAL historical model/bitwise match hoặc đánh giá TEST; G3 release tổng thể còn PARTIAL do original provenance và demo/release gate riêng. Không lặp training để tự ý làm khớp số metric cũ; P16/P18/P19/P20, G0–G6 tiếp tục kiểm soát độc lập.

Các đoạn r05 và r04 phía dưới mô tả snapshot cũ tại 16/10, **không phải trạng thái P15 mới nhất**. Những quyết định/giới hạn dữ liệu lịch sử vẫn giữ nguyên.

## Cập nhật r05 — 16/10/2026, ưu tiên hiện hành

R04-ASSEMBLY missing independent full argument/form review đã hoàn tất bằng report r05 ở context riêng; baP1 và haiP2 sửa trong draft r05, reviewer recheck chấp nhận internal content;34/34 mechanical checks PASS. HaiP0 hành chính và filled/rendered DOCX/PDF vẫn OPEN. Xem qa_logs/r05_review_resolution.md dưới proposal/researchwrite/nckh-ids/. Phase0–20 và G0–G6 không tự DONE. FullTRAIN plan có input hashes/capacity/budget/isolation nhưng NO_GO do RAM headroom/runner chưa đạt, không fit mới. Public surface triage có finding paths/email/template fields, không cleanup hoặc push.

Checkpoint r04 ưu tiên: docs/RESUME_AUDIT_R04_2026-10-16.md. REF11/12metadata verified,L03warning;source-linked readings,gap/relatedwork vàformcontentassembly có;fullargumentreviewpendingusage limit. FreshTRAINsubsetsoftware smoke45/45 khôngfinalmodelreproduction. Defense script/runbook/checklistdraft có,khôngslides/demo. P15/P01/P18/P17/G0–G6 khôngtựDONE. Task graph/contracts docs/R04_TASK_CONTRACTS.md,task JSON .research_memory/r04/.

Checkpoint r03: docs/RESUME_AUDIT_R03_2026-10-16.md. P18 xác nhận metadata thêm L04/L11:6/12 legacy records verified,6 pending; U01/U03 giữ warning. Proposal có partial draft nhu cầu/sản phẩm/tiến độ/kinh phí theo form; chưa DOCX/PDF hoặc full proposal. Hai stale memory hashes vào phiên được audit riêng;282/282 historical files nguyên. DOCX có8 bảng (đính chính ghi chép9), ZIP15 entries không DOCX. Không mở lại experiment/model selection.

Đây là reconciliation bổ sung; giữ audit cũ như lịch sử. Trạng thái `VERIFIED_REUSE` chỉ là kế thừa evidence trong phạm vi đã thực hiện, không mở rộng thành hoàn thành mọi yêu cầu của MASTER.

| Phase | Trạng thái hiện tại | Evidence / việc còn thiếu |
|---|---|---|
| P00 | PARTIAL | Frozen RQ ở notebook/phase01; phục hồi canon và proposal foundation; giả thuyết tiên nghiệm không được tự bịa sau test |
| P01 | PARTIAL | literature/gap matrices có; thiếu screening log đầy đủ, kiểm chứng toàn bộ bibliography và nguồn trong nước |
| P02 | VERIFIED_REUSE trong scope UNSW | 3 raw checksum PASS; nguồn UNSW; CIC chỉ candidate chưa external validation |
| P03 | VERIFIED_REUSE có giới hạn | Audit/overlap/view outputs có; raw integrity PASS; không tuyên bố split không leakage |
| P04 | VERIFIED_REUSE cho EDA | Bảng/hình EDA có; publication QA riêng P16 |
| P05 | PARTIAL so với contract mới | Stable subsets có; FS ngoài development folds phải công khai, không làm lại để hợp thức hóa |
| P06 | VERIFIED_REUSE có giới hạn | Baseline folds/aggregates có; selection optimism giữ nguyên |
| P07 | VERIFIED_REUSE có giới hạn | OOF/diversity/voting/stacking có; giữ negative results |
| P08 | DOCUMENTATION_CLOSURE | Framework note chính thức bổ sung từ source/freeze; không thuật toán mới |
| P09 | PARTIAL | Class-weight/no-resampling scope; không có matched resampling ablation |
| P10 | VERIFIED_REUSE có giới hạn | phase8 frozen configs, no test-loaded; meta tuning không fully nested |
| P11 | VERIFIED_REUSE binary | 3 CSV closure tái lập từng byte trong venv mới; không phải multiclass |
| P12 | VERIFIED_REUSE có giới hạn | phase10 CI/McNemar có; hashes qua P13 input audit; không rerun bootstrap |
| P13 | VERIFIED_REUSE retrospective | 19 input hash khớp; không full-factorial/component leave-one-out |
| P14 | VERIFIED_REUSE descriptive | Step1/3/4/5 + closure; 375 checks là evidence lịch sử, không nói vừa chạy lại |
| P15 | **DONE_SCOPED_RECONSTRUCTION (17/10/2026)** | 3/3 frozen candidates full TRAIN 175341 rows + local `.joblib` acceptance PASS 69/69; observed RAM traces reviewed 75/75 consistency, no TEST. Historical original environment/model bitwise identity UNKNOWN; independent reviewer binary load and G3 release/demo gate still OPEN. See P15 closure QA. |
| P16 | IN_PROGRESS | Bắt đầu figure QA từ saved tables; draft cũ không tự động đạt |
| P17 | PARTIAL (FIVE_CHAPTER_37P_PDF_QA_PASS) | Báo cáo 5 chương như mẫu tham khảo; 37 trang A4, bỏ Tóm tắt, Danh mục từ viết tắt đặt sau Mục lục với cột giải nghĩa theo vai trò; không in đường dẫn source Markdown/JSON trong PDF; XeLaTeX/BibTeX PASS, 12 tài liệu, không thiếu glyph/nhãn/cảnh báo tràn dòng. Xác nhận chữ ký, form nộp, các gate học thuật vẫn OPEN. |
| P18 | TODO/PARTIAL | Literature list cũ; chưa verified refs.bib cho báo cáo cuối |
| P19 | IN_PROGRESS | Draft availability + inventory; license code, repository/version chưa chốt |
| P20 | TODO | Chỉ review đầy đủ sau khi có manuscript và package; không giả 3 reviewer |

## Thứ tự thực hiện

1. Đóng resume audit, template/registry và sửa persistent memory.
2. P15 hậu xử lý sạch, availability/code inventory và framework note. Không fit/predict hoặc thay frozen evidence.
3. P16 figure từ bảng đã khóa, source-data map và rendered QA.
4. P18 kiểm chứng bibliography + tổng quan trong nước; hoàn thiện foundation đề cương và nội dung theo form.
5. Xử lý môi trường DOCX/LaTeX, tạo báo cáo/proposal có render QA, không lấp trường cá nhân bằng ví dụ mẫu.
6. P15 phần ML reproduction cần kế hoạch thực thi riêng trong output cô lập; công khai environment gốc UNKNOWN. Demo cần model artifact đã kiểm định, không gọi saved-results viewer là live inference.
7. Slides, kịch bản, Q&A >=15 câu và demo runbook; review độc lập theo skill thích hợp, sửa major concerns.
8. G0–G6, checksum manifest, chỉ tạo FINAL_NCKH.zip sau critical gates đạt.

Mọi task có purpose/inputs/outputs/validation ở TASK_BOARD hoặc tài liệu contract đi kèm. Không đợi người dùng ra lệnh chuyển phase; blocker hành chính chỉ chặn phần phụ thuộc.

## Cập nhật lượt r02 ngày16/10

P01/P18: có `literature/literature_matrix.csv`12 records, `literature/gap_matrix.md`, working BibTeX12 entries và metadata-verified subset4 entries. Nguồn domestic D01/D02 đã tìm qua cơ sở đào tạo, reading boundary lưu rõ. Đây là tiến bộ trên partial tasks, không full systematic review/reference closure. Dataset refs U01/U03 warnings giữ nguyên. Proposal foundation nhận các literature facts trong phạm vi đọc, review độc lập đang xử lý trước drafting.

## 2026-10-16 — P17 five-chapter layout takes precedence

User-requested structure follows five top-level chapters of uploaded PTIT NetFlow reference. The previous eight-chapter 40-page PDF status is preserved in historical QA documents only; **current PDF has five chapters and 37 A4 pages** after removing the abstract and moving the substantive acronym glossary immediately after TOC. Actual compile/run: https://github.com/nphu0811/EnsembleLearning/actions/runs/38916942038 ; QA file `docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md`. All frozen experimental results remain unchanged. Nature Skills were not directly available in this ChatGPT runtime, and no Nature skill execution is claimed.


## P19 inventory finding, current 17/10/2026

The tracked review snapshot flags three historical SMOKE_ONLY.joblib files under results/reproducibility/r04_ml_smoke_repaired/smoke_models/. All three were tracked in initial commit c4ed771. No new model binary is staged; no files were loaded or removed. Inventory passed=false and code license is absent. Keep this release blocker; it is separate from accepted local P15 full-TRAIN reconstructions. Do not treat the final new-file staging check as a passing whole-repository release inventory. See release/review_inventory_2026_10_17_01/validation.json and the final review inventory snapshot.
