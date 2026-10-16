# RQ gốc tới mục tiêu thao tác, phương pháp và gate

Nguồn nguyên văn RQ: notebook/phase01/phase1_frozen_research_design_v1.md. Mục tiêu thao tác dưới đây là cách diễn đạt phần đã có thể đánh giá từ bằng chứng, không sửa RQ gốc hoặc bịa giả thuyết tiên nghiệm. Quyết định PASS dựa trên tính đúng của artifact/diễn giải, không buộc ensemble thắng.

| RQ gốc | Mục tiêu trong phạm vi hiện có | Phương pháp/comparator đóng băng | Artifact và metric | Giới hạn/kết luận được phép | Gate và trạng thái |
|---|---|---|---|---|---|
| RQ1: Under the same leakage-aware experimental protocol, does ensemble learning provide a stable improvement over matched individual machine-learning models in NIDS? | Kiểm tra hiệu quả quan sát của ba final pipeline và uncertainty có điều kiện trên benchmark | Stack42/RF42/RF17, official TEST; paired saved predictions, thống kê đã lưu | C03–C04; final_metrics.csv, paired_bootstrap_differences.csv, mcnemar_holm.csv | Chưa chứng minh superiority Stack42>RF42 hay stability qua independent retraining; không suy equivalence; FPR/FNR báo cáo cùng nhau | Aggregate arithmetic/freeze/hash PASS; RQ trả lời có giới hạn, từ “stable” chưa được kiểm chứng qua repeated training |
| RQ2: How do feature-selection strategies affect predictive performance, minority-class detection and computational cost of individual and ensemble models? | Mô tả performance–cost giữa feature tracks và binary attack-family misses trong phạm vi đã làm | Development tracks và final RF17/RF42; giữ hyperparameters khác nhau được công khai | C05, P13; cost_metrics.csv, phase13_ablation_matrix.csv, stable subsets | Joint pipeline trade-off; không causal feature-only effect. Minority-family detection chỉ được mô tả từ binary detector; CV selection optimism | Input hashes và aggregate checks PASS; RQ PARTIAL đối với isolated FS effect; không hàm ý RQ gốc bắt buộc multiclass |
| RQ3: To what extent is ensemble improvement associated with complementary error patterns among base learners, rather than simply combining the individually strongest models? | Đối chiếu descriptive OOF diversity với ensemble performance, giữ negative Voting | Saved OOF base/ensemble; không chọn lại learners bằng TEST | C06; pairwise_diversity.csv, aggregate_metrics.csv, P13 comparability audit | Association mô tả, không causal mechanism hoặc bảo đảm gain; OOF scores chịu selection và sample dependence | Bảng/source có, P13 input hashes PASS; cần kiểm reading của từng comparison trước số liệu cuối; RQ trả lời trong descriptive scope |
| RQ4: How sensitive are model rankings and reported performance to the data-splitting protocol (e.g. conventional stratified random split versus a defensible temporal/day/scenario-aware split when supported by the selected dataset)? | Báo cáo sensitivity official/novel-vector view hiện có | Cùng frozen models; novel subset thuộc official TEST | C07; final_metrics.csv official/novel rows, view_summary.json | Không phải random-vs-temporal/group comparison hoặc external validation; chưa có time/session metadata đáng tin cậy cho kết luận đó | View/source kiểm được; RQ PARTIAL, phần split-protocol contrast chưa có evidence |
| RQ5 phụ: How do selected imbalance-handling strategies affect minority-class recall, Macro-F1, false negatives and ensemble behavior when applied only within training folds? | Công khai scope no-resampling/class-weight diagnostic và phần chưa trả lời | Chỉ tái sử dụng evidence hiện có; không thêm sampling experiment sau TEST | C08; frozen configs/framework, diagnostic tables lịch sử | Không kết luận SMOTE/sampling vô ích, không matched intervention effect | RQ PARTIAL/UNANSWERED cho controlled resampling efficacy; không được ghi DONE |

Các path rút gọn được giải trong docs/CLAIM_EVIDENCE_MATRIX.md. Metadata/config static consistency không tự chứng minh chronology thực thi; historical execution provenance và original environment vẫn có giới hạn. Tất cả gate trên giữ nguyên positive class Attack=1, threshold0.5; không tạo equivalence margin, cost matrix hoặc decision rule mới từ TEST.

## Artifact resolver bổ sung

- Stable17 feature names: `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`, key stable_2plus_methods.
- Development recorded fold metrics: `results/baselines/unsw_nb15/development_cv/tables/fold_metrics.csv`. Đây không tự thay một fold allocation manifest riêng được kiểm chứng.
- Stable-track saved OOF: `results/ensemble/unsw_nb15/phase7_1_diversity/oof/stable_17_features_oof_predictions.csv` và `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/oof/stable_17_features_ensemble_oof.csv`.
- Novel-vector definition/counts: `results/data_audit/unsw_nb15_views/view_summary.json`.
- Reporting replay: `results/reproducibility/resume_2026_10_16/clean_replay_report.json`; source `src/analysis/close_original_phase11.py`.
- Preprocessing implementation source: `src/models/run_unsw_phase9_final_holdout.py`. Chưa có learned preprocessing schema từ serialized artifact đã xác nhận; source design không thay fitted transformer.

Chưa kiểm chứng một manifest độc lập chứa toàn bộ fold allocation và learned transformer. “Diagnostic tables lịch sử” ở RQ5 phải được resolve/đọc trước khi đưa số liệu chi tiết, không dùng alias này để khẳng định controlled effect.

## Mục tiêu và sản phẩm còn lại

O1: hoàn thiện đối chiếu prior work trong phạm vi claim được đọc, validation là DOI/field/source ledger và citation–claim map. O2: trình bày kết quả frozen theo ma trận trên, validation là source-data traceability, numeric QA, captions và visual review. O3: hoàn thiện documentation/reproducibility và demo theo các gate riêng trong07_remaining_work_feasibility.md. O4: soạn hồ sơ theo mẫu và chuẩn bị defense, validation là render/test và G0–G6; thông tin hành chính không được AI tự phê duyệt.

Không đặt mới giả thuyết sau khi có kết quả; không chuyển một mục tiêu chưa đạt thành completed để làm đề cương đầy đủ hơn.
