# ROADMAP RECONCILIATION — NCKH

Ngày đối chiếu: 04/10/2026 (Asia/Saigon).
Đề tài: **NGHIÊN CỨU ENSEMBLE LEARNING CHO BÀI TOÁN PHÁT HIỆN XÂM NHẬP MẠNG**.

**Trạng thái: roadmap gốc Phase 0–20 đã được đối chiếu. Original Phase 13 đã có retrospective synthesis; project audit thấy một số phase chỉ đạt một phần. Xem `docs/ROADMAP_PHASE_AUDIT_2026-10-07.md` để biết trạng thái theo từng phase.**
Phân biệt **original phase** (roadmap gốc) và **executed phase** (nhãn experiment trong repo). Không rename valid evidence để ép hai hệ numbering khớp nhau. Không chạy training, inference trên TEST, bootstrap hay sửa pipeline trong lần cập nhật này.

## 1. Roadmap gốc đã phục hồi và provenance

User xác nhận roadmap đã phục hồi và yêu cầu cập nhật tài liệu theo hai file:

- `C:/Users/admin/Downloads/ROADMAP_RECONCILIATION_RECOVERED.md` — roadmap, scientific mapping và status.
- `C:/Users/admin/Downloads/CODEX_CONTINUATION_AFTER_RECOVERY.md` — phạm vi Phase 13 và constraints.

SHA-256 lúc đọc nguồn: recovered reconciliation `D6E406401C3B6C5A4421B84BEE161DBF1E97A8DDF0C243DDA79FF0E7D335DFFF`; continuation `A7177FCE7DE15FBC27983B1AD552429748C11B19316DAC824CAB9DC54CB84E30`.

Nguồn xa hơn được file phục hồi ghi là Project Library, `Đã dán markdown (1)(1).md`; chưa trực tiếp truy xuất bản Library này. Hai file user cung cấp là nguồn đối chiếu hiện tại. Các chỉ dẫn thực thi trong file chỉ áp dụng trong phạm vi user đã giao: cập nhật reconciliation và lập plan; **chưa thực thi aggregation/analysis hay thí nghiệm**.

| Original phase | Nội dung chính xác đã phục hồi |
|---|---|
| 11 | Evaluation Protocol |
| 12 | Validation và Statistical Test |
| 13 | Ablation Study |
| 14 | Error Analysis |
| 15 | Reproducibility |
| 16 | Scientific Figures |
| 17 | Viết báo cáo NCKH |
| 18 | Quản lý trích dẫn |
| 19 | Data Availability |
| 20 | Review báo cáo cuối |

### Lịch sử tìm kiếm trước khi user cung cấp bản phục hồi

Đã đọc toàn bộ bốn file trong `nckh_codex_handoff/` và handoff user cung cấp trong chat.
Đã tìm trong toàn bộ project, gồm file ẩn ngoài `.git/`, tài liệu `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.ipynb`, source `.py`, cấu hình, README, task board và decision log.
Từ khóa: Phase 11–18, roadmap, master/original prompt, workflow, study, publication-level figure QA. Đã kiểm tra tên file prompt/roadmap, chat export (`.jsonl`, `.html`), archive `.zip`, `.docx`, foundation/canon/state/section contracts/style guide.

Kết quả tại checkpoint trước (giữ để bảo toàn lịch sử, không phải blocker hiện tại):

- Không tìm thấy master roadmap/original prompt hoặc chat export chứa định nghĩa đầy đủ Phase 11–18.
- `notebook/phase04/phase4_eda_plan.md:26`: “No publication-level figure QA yet; that is reserved for Phase 16.” Đây là manh mối trực tiếp, không phải toàn bộ đặc tả Phase 16.
- `src/data/eda_unsw-nb15.py:98` cũng ghi figure QA dành cho Phase 16.
- `nckh_codex_handoff/HANDOFF_STATUS.json` ghi `UNRESOLVED_MUST_RECOVER`.
- Các nhãn Phase 11–13 trong README, draft, reporting script và reporting metadata là workflow sai đã được handoff cảnh báo; không dùng chúng để khôi phục roadmap.
- Phase-1 decision log còn nhắc SMOTE ở Phase 9, trong khi experiment chain thực tế có Phase 9 là frozen holdout. Dấu vết kế hoạch cũ này không đủ để suy ra Phase 11–18.
- `CODEX_MASTER_HANDOFF_PROMPT.md` được README handoff nhắc tới nhưng không có trong folder/project hiện tại.
- Chat tham chiếu `6ab01bb8-c538-83ec-80a4-be99852dc948` chưa đọc được: phiên hiện tại không có tool `read_thread`, preview được cung cấp là null. Không tuyên bố đã kiểm tra nội dung chat đó.

`nckh_codex_handoff/HANDOFF_STATUS.json` và handoff notes được giữ nguyên như snapshot lịch sử; trạng thái `UNRESOLVED_MUST_RECOVER` trong snapshot đã được cập nhật bằng tài liệu reconciliation này. Không dùng snapshot đó để mở lại blocker đã giải quyết.

## 2. Trạng thái repo và evidence chính thức

Git lúc tiếp quản: `master`, **chưa có commit**, index chưa có file tracked; `data/`, `nckh_codex_handoff/`, `notebook/`, `results/`, `src/` đều untracked. Không có lịch sử Git để khôi phục roadmap. Không tạo commit/branch trong lần đối chiếu này.
Không tìm thấy `AGENTS.md`. `config/`, `data/processed/` và `.kilo/worktrees/` trống.

```text
NCKH/
├── config/                         (trống)
├── data/
│   ├── raw/
│   │   ├── unsw-nb15/             (3 CSV)
│   │   └── cic-ids2017/           (5 CSV theo ngày; chưa xác minh là corrected release)
│   ├── interim/unsw-nb15/         test_unseen_vectors.csv
│   └── processed/                 (trống)
├── src/
│   ├── data/                      audit, overlap audit, views, EDA (4 scripts)
│   ├── features/                  FS stage 1/2 (2 scripts)
│   ├── models/                    baseline, diversity, ensemble, tuning, holdout (5 scripts)
│   └── analysis/                  Phase-10 stats, premature reporting (2 scripts)
├── results/
│   ├── data_audit/                 unsw_nb15, overlap, views
│   ├── eda/unsw_nb15/              figures, tables, summary
│   ├── feature_selection/unsw_nb15/ stage1, stage2
│   ├── baselines/unsw_nb15/        development_cv
│   ├── ensemble/unsw_nb15/         phase7_1_diversity, phase7_2_ensemble_cv
│   ├── tuning/unsw_nb15/           phase8_controlled
│   ├── final_evaluation/unsw_nb15/ phase9_holdout
│   ├── final_analysis/unsw_nb15/   phase10_statistics
│   └── final_reporting/unsw_nb15/  phase11_results_figures (premature)
├── notebook/                      README_INDEX.md, phase01–phase13
├── nckh_codex_handoff/             4 file đã đọc
└── docs/                          checkpoint tiếp quản và inventories mới
```

Handoff xác định **executed Phase 0–10** DONE. Bảng sau mô tả experiment chain theo nhãn đã thực hiện, không phải official original numbering. Mức kiểm chứng: **đối chiếu artifact, không tái chạy thí nghiệm và không tái xác minh citation**.

| Phase | Trạng thái chính thức theo handoff | Evidence hiện có / giới hạn kiểm chứng |
|---|---|---|
| 0 — Design | DONE theo handoff | Phase-1 logs lưu quyết định nền; chưa tìm thấy bộ foundation riêng (canon, scope lock, argument map, contracts, style guide, state). Chưa xác minh độc lập việc hoàn tất Phase 0. |
| 1 — Literature | DONE | `notebook/phase01/`: checkpoint, frozen design, literature/gap matrices, task board, decision log. Không gọi lại các skill hoặc xác minh DOI trong lần này. |
| 2 — Dataset | DONE | `notebook/phase02/`: dataset decision, task board, decision log; primary UNSW, secondary corrected CIC là candidate. |
| 3 — Audit | DONE | Policy tại `notebook/phase03/`; outputs tại `results/data_audit/unsw_nb15*`; scripts ở `src/data/`. View metadata xác nhận 42 features, novel subset 73,791. |
| 4 — EDA | DONE | `notebook/phase04/phase4_eda_plan.md`; `results/eda/unsw_nb15/`: 8 figure files, 7 tables, summary. |
| 5 — FS | DONE | Plans tại `notebook/phase05/`; stage1/2 metadata, subsets, ranking/stability tables; stage2 summary ghi 17/13/12/7 features. |
| 6 — Baselines | DONE | `notebook/phase06/`; `results/baselines/unsw_nb15/development_cv/`: metadata, fold/aggregate metrics, trade-off và summary. |
| 7.1 — Diversity | DONE | Plan, saved OOF ở `results/ensemble/unsw_nb15/phase7_1_diversity/oof/`, pairwise diversity và runtime tables. |
| 7.2 — Ensembles | DONE | Plan, saved OOF và tables ở `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/`; summary giữ negative result của Voting. |
| 8 — Tuning/freeze | DONE | `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`, grids và threshold diagnostic; configs khớp Phase-9 metadata. |
| 9 — Final holdout | DONE | `results/final_evaluation/unsw_nb15/phase9_holdout/`: metadata, summary, 5 CSV gồm sample predictions, final/cost metrics. |
| 10 — Statistics/errors | DONE | `results/final_analysis/unsw_nb15/phase10_statistics/`: metadata, summary, 7 statistical CSV; `notebook/phase10/phase10_final_evidence_and_rq_answers.md`. |
| “11–13” reporting cũ | PREMATURE_REPORTING_DRAFTS | Có artifact nhưng không hoàn thành original Phase 13/16/17; original 11/12 được bao phủ bởi evidence khác. |

### Status theo original roadmap — mapping bằng nội dung khoa học

| Original phase | Evidence / executed numbering | Trạng thái và việc còn thiếu |
|---|---|---|
| 0 — Proposal/design | Frozen design/RQs trong Phase 1 | Một phần/cần xác minh: bộ foundation riêng chưa có trong workspace. |
| 1 — Literature review | Literature/gap matrices trong Phase 1 | Một phần: synthesis có, search/screening protocol tái lập và full citation verification chưa thấy. |
| 2 — Dataset | Dataset decision | Đạt cốt lõi; CIC secondary chưa xác minh corrected release, không phải external validation. |
| 3 — Audit | Cleaning policy, audit outputs/scripts | Đạt cốt lõi; một số checklist outlier/corruption/split feasibility cần xác nhận rõ. |
| 4 — EDA | EDA plan, tables, figures | Đạt cốt lõi; publication QA để Phase 16. |
| 5 — Feature Selection | Filter + embedded + wrapper evidence | Đạt theo thiết kế; development CV có selection optimism đã công khai. |
| 6 — Baselines | LR/DT/RF cùng CV và feature tracks | Đạt theo scope chọn lọc. |
| 7 — Ensemble | Diversity, RF/Ada, Voting, Stacking | Đạt phần chính; negative Voting được giữ; blending không thực hiện. |
| 8 — Proposed Ensemble Framework | LR+DT+RF và feature tracks | Một phần; cần design note end-to-end chính thức. |
| 9 — Class Imbalance | No-resampling closure, meta-weight diagnostic | Một phần; không có matched resampling experiment, không kết luận resampling vô ích. |
| 10 — Hyperparameter Optimization | Executed Phase 8 grids/freeze | Đạt trong scope tuning TRAIN-only; configs giữ nguyên. |
| 11 — Evaluation Protocol | Executed Phase 9 holdout/cost | Một phần; thiếu Weighted-F1 và per-class Normal/Attack P/R/F1/support. |
| 12 — Statistical Validation | Executed Phase 10 bootstrap/McNemar/Wilson | Đạt theo thiết kế có điều kiện; giới hạn phụ thuộc dữ liệu được giữ. |
| 13 — Ablation Study | Retrospective saved-artifact synthesis | Một phần; không cô lập mọi component/matched resampling. Xem `notebook/phase13/phase13_ablation_summary.md`. |
| 14 — Error Analysis | Attack-family misses/pairwise errors | Một phần; feature-level FP/FN patterns chưa đủ. |
| 15 — Reproducibility | Scripts/metadata/output chain | Một phần; README/environment/config/Git packaging còn thiếu, chưa có serialized model. |
| 16 — Scientific Figures | Existing premature and EDA figures | Chưa hoàn tất chính thức; publication-level QA chưa có evidence. |
| 17 — Viết báo cáo NCKH | Premature prose/manuscript drafts | Chưa hoàn tất chính thức; template hiện có là đề tài Android malware khác. |
| 18 — Quản lý trích dẫn | Early reference notes | Một phần; chưa có full reference verification ledger. |
| 19 — Data Availability | Audit/checksum/provenance | Chưa hoàn tất statement cuối. |
| 20 — Review báo cáo cuối | Chưa có final report NIDS | Chưa bắt đầu. |

Audit đầy đủ và evidence/gap theo từng phase: `docs/ROADMAP_PHASE_AUDIT_2026-10-07.md`.

Các closure/reporting gaps ở original 8/9/11 được công khai, không yêu cầu tái chạy các phase đã bao phủ; Phase 13 kế thừa evidence hiện có theo yêu cầu user.

Không tìm thấy `.pkl`, `.pickle`, `.joblib` model artifact. `src/models/run_unsw_phase9_final_holdout.py` đo size bằng `pickle.dumps` trong bộ nhớ; CSV cost vẫn là evidence đã lưu, nhưng không được khẳng định có frozen model file sẵn để triển khai.

Đối chiếu trực tiếp CSV đã lưu:

| Pipeline — official TEST | Macro-F1 | MCC | FPR | FNR |
|---|---:|---:|---:|---:|
| Stacking-42 | 0.863840 | 0.750497 | 26.65% | 1.88% |
| RF-42 | 0.863343 | 0.750910 | 27.04% | 1.62% |
| RF-17 | 0.860673 | 0.746881 | 27.63% | 1.56% |

`paired_bootstrap_differences.csv` và `mcnemar_holm.csv` khớp handoff: Stack − RF42 có Δ Macro-F1 +0.000497, CI [−0.000312, +0.001309], Holm p 0.468377; FPR giảm và FNR tăng với CI không chứa 0. Không chứng minh robust overall superiority, cũng không chứng minh tương đương thống kê. RF17 giữ vai trò efficiency trade-off. RQ4 = PARTIAL.

FS đã học trên official TRAIN trước later CV: development scores không được đổi thành unbiased final estimates. Bootstrap uncertainty có điều kiện trên benchmark rows, không chứng minh network flows độc lập.

## 3. Mapping các artifact reporting làm sớm

**Phân loại về mặt trạng thái ngay tại checkpoint này: PREMATURE_REPORTING_DRAFTS. Chưa move/rename/sửa file gốc.**
Mapping đường dẫn dưới đây là đề xuất bảo toàn provenance. Tên `old_phase*` giữ dấu vết nhãn cũ. Phase tái sử dụng đã xác định theo **loại nội dung**: figures/tables → original 16; Results/Discussion/Conclusion/manuscript → 17; reference-verification → 18; provenance/data-availability notes → 19 nếu có. Draft hỗn hợp có thể phục vụ nhiều phase; không đánh DONE phase đích chỉ vì draft tồn tại. Danh sách từng file nằm ở `docs/PREMATURE_REPORTING_INVENTORY.csv` (snapshot 54 file cũ, không bao gồm ablation plan mới).

Riêng `notebook/phase13/phase13_ablation_plan.md` là **official original Phase 13** mới; không đưa vào quarantine cùng `phase13_1_*` đến `phase13_4_*` là reporting drafts cũ. Chưa thực hiện bất kỳ move/rename nào trong lần cập nhật này.

| Đường dẫn hiện tại | Đích bảo quản đề xuất | Công dụng tương lai có điều kiện |
|---|---|---|
| `notebook/phase11/` (4 file) | `docs/drafts/premature_reporting/old_phase11_notes/` | Tables/captions → original 16; synthesis prose → original 17. |
| `results/final_reporting/unsw_nb15/phase11_results_figures/` (19 file) | `results/drafts/premature_reporting/unsw_nb15/old_phase11_results_figures/` | 6 figures ở PNG/PDF, 4 tables, 3 notes/metadata; candidate đầu vào figure QA Phase 16, không tính là QA đã hoàn tất. |
| `notebook/phase12/phase12_1_results_draft.md` | `docs/drafts/premature_reporting/old_phase12/phase12_1_results_draft.md` | Original 17 — Results. |
| `notebook/phase12/phase12_2_discussion_draft.md` | `docs/drafts/premature_reporting/old_phase12/phase12_2_discussion_draft.md` | Original 17 — Discussion. |
| `notebook/phase12/phase12_3_limitations_contributions.md` | `docs/drafts/premature_reporting/old_phase12/phase12_3_limitations_contributions.md` | Giữ limitations/negative results, kiểm tra lại claim khi tái dùng. |
| `notebook/phase12/phase12_4_final_conclusion.md` | `docs/drafts/premature_reporting/old_phase12/phase12_4_final_conclusion.md` | Draft, chưa phải final conclusion của toàn roadmap. |
| `notebook/phase13/phase13_1_*` (3 file) | `docs/drafts/premature_reporting/old_phase13/` | Integration/checklist → original 17; reference notes → 18. |
| `notebook/phase13/phase13_2_*` (4 file) | Cùng đích `old_phase13/` | Full draft/early sections/checkpoint → original 17; reference addendum → 18. |
| `notebook/phase13/phase13_3_*` (4 file) | Cùng đích `old_phase13/` | Abstract/audited draft → original 17; citation phần audit → 18. |
| `notebook/phase13/phase13_4_*` (4 file) | Cùng đích `old_phase13/` | Placement, manuscript, QA, checkpoint; không phải official QA completion. |
| `notebook/phase13/figures/` (6 file), `tables/` (5 file) | Giữ cấu trúc tương đối dưới `old_phase13/` | Bản figure/table đi kèm manuscript; provenance vẫn trỏ Phase 9/10. |
| `src/analysis/run_unsw_phase11_results_figures.py` | Giữ source tại chỗ; ghi nhãn lịch sử trong mapping | Reporting generator làm sớm; không chạy/sửa output path trong lần tiếp quản. |
| `notebook/README_INDEX.md` | Giữ tại chỗ; cần bổ sung cảnh báo sau khi chốt mapping | Historical index không có quyền xác định official Phase 11/12. |

Trước khi thực hiện move: dùng manifest hash để đối chiếu trước/sau, sửa relative figure/table links và source output paths nếu cần, ghi old → new path vào decision log. Không xóa bản cũ chỉ vì phase label sai; không sửa metadata thành một official phase chưa biết.

## 4. Bước tiếp theo, inputs/outputs và checkpoint

Original Phase 13 — Ablation Study đã được tổng hợp hồi cứu trên saved TRAIN-only CV/OOF từ executed 6–8, frozen results từ 9 và paired statistics từ 10. Outputs: `src/analysis/run_unsw_phase13_ablation.py`, `results/ablation/unsw_nb15/phase13_ablation/phase13_ablation_matrix.csv`, `comparability_audit.csv`, `analysis_metadata.json`, cùng summary và imbalance closure note tại `notebook/phase13/`. Đây là retrospective synthesis trong scope artifacts có sẵn, không phải full component-isolation ablation; xem audit để biết thiếu leave-one-base-learner-out và matched resampling contrasts. Không train model, nạp TEST hay chạy inferential tests mới trong lần tổng hợp.

Kết quả đọc metadata/source hiện tại: outer 3-fold StratifiedKFold (shuffle, seed 42) của executed 6/7/8 RF cùng thiết kế; exact row/fold alignment chưa kiểm tra đầy đủ. Phase-7.2 Stacking inner seed 137; Phase-8 meta CV 5 folds seed 271 trên global base OOF nên không so trực tiếp để claim tuning gain. RF42 vs RF17 frozen khác cả hyperparameters, vì vậy holdout comparison là bundled pipeline trade-off, không phải isolated feature ablation.

### Research Task Board — tiếp quản

| ID | Task | Status (TODO/DOING/DONE/BLOCKED) | Evidence/Output |
|---|---|---|---|
| H-01 | Đọc toàn bộ handoff | DONE | 4 file trong `nckh_codex_handoff/`; mục 1 tài liệu này |
| H-02 | Kiểm tra Git và cây thư mục | DONE | Mục 2; `docs/TAKEOVER_FILE_INVENTORY.csv` |
| H-03 | Phục hồi roadmap gốc đến Phase 20 | DONE | Hai file user cung cấp; mục 1 |
| H-04 | Locate evidence 0–10 và đối chiếu kết quả khóa | DONE | Mục 2; Phase 0 chỉ có indirect evidence và handoff |
| H-05 | Locate/mapping premature artifacts | DONE | Mục 3; `docs/PREMATURE_REPORTING_INVENTORY.csv` |
| H-06 | Tạo reconciliation checkpoint | DONE | `docs/ROADMAP_RECONCILIATION.md` |
| H-07 | Move/rename có provenance sau khi chốt mapping | TODO | Mapping mục 3; chưa có move log |
| H-08 | Map original 8–12 vào existing evidence | DONE | Bảng original status, mục 2; closure/reporting gaps công khai |
| H-09 | Lập official Phase-13 ablation plan | DONE | `notebook/phase13/phase13_ablation_plan.md` |
| H-10 | Thực thi ablation aggregation/analysis | DONE (retrospective scope) | Phase-13 summary/matrix/audit/metadata và imbalance closure note; không phải full component-isolation ablation |
| H-11 | Audit project theo roadmap gốc Phase 0–20 | DONE | `docs/ROADMAP_PHASE_AUDIT_2026-10-07.md` |

### Research Decisions Log — tiếp quản

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Phục hồi numbering theo original roadmap | User đã cung cấp nguồn phục hồi | Hai file Downloads; bảng original status | Gỡ blocker roadmap; tiếp tục ở original 13, giữ executed evidence labels. |
| Chỉ lập plan, chờ duyệt trước thực thi | Phạm vi user giao ở lượt hiện tại | Yêu cầu trực tiếp của user; ablation plan | Không chạy aggregation, analysis hoặc experiment mới trước duyệt. |
| Reclassify reporting về trạng thái, giữ nguyên đường dẫn hiện tại | Bảo toàn provenance và tránh broken links | Mapping original 16–19 và inventory | Không tính các draft là official phases DONE; official ablation plan mới được tách khỏi draft cũ. |
| Giữ nguyên frozen configs/predictions/stats | Official TEST đã mở; không post-test selection | Phase-8 freeze, Phase-9/10 metadata | Không sửa model/features/threshold/hyperparameters dựa TEST. |
| Không nâng mức kết luận | Overall superiority không được evidence hỗ trợ | Paired CI và McNemar đã lưu | Stack = FP/FN trade-off; RF17 = efficiency; RQ4 PARTIAL. |
| Ghi nhận Phase-0 foundation/model files chưa tìm thấy | Phân biệt handoff claim và artifact tại workspace | File inventory; Phase-9 size measurement code | Không tự tạo lại foundation hoặc train model để lấp thiếu hụt. |

### Files phải giữ nguyên

- Toàn bộ `data/raw/`, gồm UNSW và CIC; không cleaning tại chỗ.
- `data/interim/unsw-nb15/test_unseen_vectors.csv` và `results/data_audit/unsw_nb15_views/`: sensitivity view đã khóa.
- `results/tuning/unsw_nb15/phase8_controlled/`, nhất là `freeze_candidates.json`; feature subsets trong `results/feature_selection/`.
- Toàn bộ `results/final_evaluation/unsw_nb15/phase9_holdout/`, nhất là `tables/official_test_predictions.csv`.
- Toàn bộ `results/final_analysis/unsw_nb15/phase10_statistics/`.
- Existing scripts, methodological notes và reporting drafts được bảo toàn trong lần tiếp quản; thay đổi tổ chức sau này phải có mapping/provenance.

`docs/TAKEOVER_FILE_INVENTORY.csv` ghi tên/kích thước các file trước khi tạo checkpoint; `docs/TAKEOVER_PRESERVATION_SHA256.csv` ghi SHA-256 của toàn bộ existing non-raw files. Manifest này là baseline tại thời điểm tiếp quản, không chứng minh file chưa từng thay đổi trước đó. Raw không được hash lại trong checkpoint; historical checksums tại `results/data_audit/unsw_nb15/raw_file_checksums.csv` chưa được kiểm chứng lại.

**CHECKPOINT: roadmap đã phục hồi và project được audit theo toàn bộ Phase 0–20. Original Phase 13 retrospective synthesis đã được tạo từ evidence đã lưu; một số phase còn gap được ghi rõ trong audit. Lần audit này không chạy experiment và không thay đổi frozen holdout evidence.**
