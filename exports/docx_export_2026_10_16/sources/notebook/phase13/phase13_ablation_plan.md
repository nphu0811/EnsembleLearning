# ORIGINAL PHASE 13 — ABLATION STUDY PLAN

Ngày: 04/10/2026. Trạng thái: **EXECUTED — retrospective synthesis complete** (user xác nhận thầy đã đồng ý và yêu cầu tiếp tục).
Đây là original Phase 13 theo roadmap phục hồi; các `phase13_1_*`–`phase13_4_*` bên cạnh là premature reporting drafts, không phải ablation evidence.

## Objective và scientific rationale

Trả lời “khác biệt performance/behavior đến từ đâu?” bằng cách tách các contrast có kiểm soát trong **artifact đã có**: learner strength, combination rule, feature track và cost. Không giả định ensemble đã cải thiện; negative/null result là kết quả cần giải thích.

Đây là retrospective ablation synthesis, không phải preregistered factorial experiment và không phải leave-one-learner-out ablation. Không có evidence bỏ riêng LR/DT/RF khỏi Stacking; không thể định lượng contribution độc lập của từng learner. Giới hạn đó phải có trong summary.

Không retrain, không chọn model mới, không dùng official TEST để thiết kế hoặc tối ưu component. User duyệt plan trước khi tạo matrix kết quả hoặc chạy aggregation/analysis.

## Scientific questions

1. Trên cùng TRAIN-CV/feature track, LR/DT/RF và ensemble khác nhau thế nào về Macro-F1, MCC, FPR/FNR? RF vốn là bagging ensemble; gọi RF là strong reference, không gọi là một single-tree learner.
2. Với cùng trio LR+DT+RF, Hard Voting, Soft Voting và Stacking thay đổi error trade-off ra sao? Nested meta fitting của Stacking là một phần method contrast.
3. Giữ model/config cố định trên development evidence, 42 → 17 features thay đổi performance/cost thế nào?
4. Frozen RF42/RF17 có operational trade-off nào được saved holdout/statistics hỗ trợ, và phần nào không thể gán riêng cho FS?
5. Tuning RF có contrast development cùng protocol nào? Contrast nào không đủ điều kiện, đặc biệt Stacking meta CV?
6. No-resampling branch được chọn vì scope/design gì; class weights đã thử ở đâu, còn thiếu counterfactual nào?

## Inputs — exact source artifacts

Các đường dẫn dưới đây tương đối với project `C:/Users/admin/Documents/ChatGPT/NCKH/`.

| Key | Existing artifacts | Vai trò |
|---|---|---|
| S6 | `results/baselines/unsw_nb15/development_cv/experiment_metadata.json`; `tables/fold_metrics.csv`, `tables/aggregate_metrics.csv`, `tables/subset_tradeoff_summary.csv` trong cùng folder | LR/DT/RF development folds và FS screening; không có sample-level OOF Phase 6 để ghép tùy tiện. |
| S71 | `results/ensemble/unsw_nb15/phase7_1_diversity/experiment_metadata.json`; `oof/all_features_oof_predictions.csv`, `oof/stable_17_features_oof_predictions.csv`; `tables/individual_oof_metrics.csv`, `tables/pairwise_diversity.csv`, `tables/fold_runtime.csv` | Individual LR/DT/RF/AdaBoost OOF, fold keys, error complementarity; cost hỗ trợ, không pool runtime xuyên run. |
| S72 | `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/experiment_metadata.json`; `oof/all_features_ensemble_oof.csv`, `oof/stable_17_features_ensemble_oof.csv`; `tables/fold_metrics.csv`, `tables/aggregate_metrics.csv`, `tables/pooled_oof_metrics.csv`, `tables/comparison_vs_random_forest.csv` | RF, AdaBoost, Hard/Soft Voting, Stacking trên cùng outer folds; nguồn chính cho combination/feature contrasts. |
| S8 | `results/tuning/unsw_nb15/phase8_controlled/experiment_metadata.json`; `freeze_candidates.json`; `tables/rf42_grid_results.csv`, `tables/rf17_grid_results.csv`, `tables/stacking42_meta_grid_results.csv`, `tables/stacking42_base_oof_probabilities.csv` | RF grids, historical meta weights/C selection; không sử dụng grid để chọn lại config. |
| S9 | `results/final_evaluation/unsw_nb15/phase9_holdout/experiment_metadata.json`; `tables/final_metrics.csv`, `tables/cost_metrics.csv`, `tables/official_test_predictions.csv` | Chỉ đối chiếu 3 frozen pipelines, threshold 0.5; predictions chỉ đọc nếu integrity check/reporting cần, không inference lại. |
| S10 | `results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json`; `tables/paired_bootstrap_differences.csv`, `tables/mcnemar_holm.csv`, `tables/bootstrap_metric_ci.csv`, `tables/performance_cost_tradeoff.csv`, `tables/official_vs_novel_degradation.csv` | Reuse holdout effects/uncertainty đã khóa; không chạy lại bootstrap hoặc đổi comparison family. |
| SF | `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`; `results/data_audit/unsw_nb15/class_distribution.csv` | Exact 17-feature membership, counts Normal/Attack; không feature ranking mới. |
| SC | `src/models/run_unsw_baseline_development.py`, `run_unsw_diversity_oof.py`, `run_unsw_ensemble_phase7_2.py`, `run_unsw_phase8_controlled_tuning.py` trong `src/models/` | Đọc source để kiểm tra configs, preprocessing, folds; không import/execute các training scripts. |

Nguồn roadmap: hai file phục hồi do user cung cấp, được ghi tại `docs/ROADMAP_RECONCILIATION.md`. Premature tables/manuscript không thay thế S6–S10.

## Ablation axes và comparability hiện tại

Các trạng thái dưới đây dựa trên đọc source/metadata/header, **chưa phải kết quả exact alignment audit toàn bộ rows**.

| ID | Contrast | Nguồn | Mức so sánh / điều kiện |
|---|---|---|---|
| A1 | LR/DT/RF vs RF/Hard/Soft/Stack; riêng từng 42/17 track | S71 + S72; S6 cross-check | Conditionally comparable: seed 42, outer 3 folds; phải match `(row_index,id,y_true,fold)` và shared RF predictions. Không coi bản RF trùng là replication độc lập. |
| A2 | RF vs Hard vs Soft vs Stacking; Hard vs Soft, Soft vs Stack | S72 | Matched-method comparison trong cùng run/track. Hard/Soft cùng base trio; Stack thêm inner 3-fold seed 137, meta LR C=1, passthrough=False. Không nói chỉ thay một arithmetic rule ở contrast với Stack. |
| A3 | 42 vs 17 cho LR/DT/RF/Hard/Soft/Stack | S71 hoặc S72 theo model; S6 cross-check | Fixed-config development contrast: match rows/folds, preprocessing family và hyperparameters; số cột one-hot khác là hệ quả track. Mỗi model dùng một nguồn canonical để tránh duplicate evidence. |
| A4a | Cost của 42 vs 17 cho cùng model/config | S72 fold/aggregate cost; S6 secondary | Primary trong cùng run; mean/SD qua folds mô tả runtime, không hardware-independent benchmark. Không gộp cost S6 và S72 thành effect estimate. |
| A4b | Frozen RF42 vs RF17; Stack42 vs RF42 | S9 + S10 | Final bundled pipeline comparison. RF42=(300,0.5,leaf1), RF17=(150,0.5,leaf2): khác features VÀ params. Không gọi chênh lệch final là pure FS effect. Không có Stack17 holdout. |
| A5a | RF default vs historical frozen config ở mỗi track | S8; S6/S72 context | Ưu tiên so các rows trong cùng grid: default `(150,sqrt,leaf2)` có trong cả RF grids. Selection-conditional descriptive score delta, không unbiased tuning benefit; không tự thay frozen config bằng highest-rank row hiện nay. |
| A5b | S72 nested Stack vs S8 tuned meta CV | S72 + S8 | NOT COMPARABLE cho tuning gain: outer 3 folds/inner 3 seed137 khác meta 5-fold seed271 trên global base OOF, còn tuned RF thay đổi. Chỉ ghi protocol difference, không tính delta như ablation effect. |
| A6a | No-resampling branch | SF + existing configs | DESIGN JUSTIFICATION ONLY. TRAIN Attack=119,341 (68.06%), Normal=56,000 (31.94%). Không suy ra “không imbalance” hoặc resampling không có ích; không có matched resampling experiment. |
| A6b | Meta LR class_weight=None vs balanced tại cùng C | S8 meta grid | Có historical evidence, chỉ descriptive trong cùng meta-CV, bao gồm tất cả 5 C đã thử. Không chứng minh toàn pipeline xử lý imbalance tốt hơn, không áp dụng class_weight mới lên frozen models. |

AdaBoost được giữ như historical reference/context, không tự thêm final candidate. A1/A2 chồng lắp thì dẫn cùng canonical row, không đếm hai lần thành hai bằng chứng độc lập. Không thêm “Stack bỏ LR/DT/RF” hay resampling branch sau TEST.

## Comparability rules — fairness gates trước aggregation

1. Xác nhận file tồn tại, schema, provenance hash, row counts và uniqueness; chỉ đọc derived artifacts, không cần raw TRAIN/TEST cho scope này.
2. Match exact sample keys/folds giữa OOF tracks và S71/S72. TRAIN OOF mong đợi 175,341 rows mỗi track; nếu mismatch, dừng contrast và ghi NOT_COMPARABLE, không silently drop rows hoặc đổi folds.
3. Xác nhận same target/positive class (Attack=1), same feature membership/order, preprocessing train-fold-only, unknown categorical handling, seed và model/config. Metadata cùng seed chưa đủ chứng minh exact pairing; shared RF predictions cần cross-check.
4. Ưu tiên within-source contrasts. Nếu source và CSV không đủ lưu lịch sử environment hoặc fold indices (RF grid), ghi comparability có điều kiện; không dựng lại bằng training.
5. Tách `development_cv_fold_mean` khỏi `development_pooled_oof`, `official_test`, `novel_vector_test`. Không trừ pooled metric khỏi mean fold score. Canonical predictive effects A1–A3 dùng pooled OOF sau gate; fold means là bảng mô tả riêng.
6. Ghi Δ=A−B với rõ model/track/config và metric; FPR/FNR dùng rate hoặc percentage points nhất quán. Cost ratio ghi rõ tử/mẫu, thời gian đo và unit; size MB nếu có, không bịa missing size.
7. Development primary Macro-F1/MCC, operational FPR/FNR, cost train seconds/inference ms per sample/serialized MB. Accuracy chỉ secondary. Hard vote fraction không phải calibrated probability; AUC của hard-vote score chỉ diagnostic, không dùng để kết luận probability quality.
8. Ba folds là validation partitions có training overlap, không phải ba independent experiments. Fold SD là descriptive dispersion, không SEM/CI; không chạy paired t-test/Wilcoxon trên 3 folds để tạo significance.
9. Không tạo p-values/CI mới cho development ablation ở scope đầu. Holdout uncertainty chỉ reuse S10 và giữ original Holm family/scope. Không lấy CI của hai models riêng rồi suy ra CI difference. Không claim tương đương từ p>0.05.
10. FS candidates được học từ official TRAIN trước later CV, nên retrospective development estimates có selection optimism. TRAIN rows không đại diện independent networks; OOF pairing không tự loại bỏ flow dependence. Novel subset là sensitivity, không external validation; hai TEST views không là independent replications.
11. Không chọn subset/model/contrast vì kết quả đẹp. Báo đầy đủ contrasts đã định nghĩa, kể cả negative/null và NOT_COMPARABLE. Các metrics reporting thiếu ở original 11 (Weighted-F1, per-class binary P/R/F1/support) ghi backlog, không âm thầm mở rộng scope tính toán trước duyệt.

## What can/cannot be interpreted causally

Có thể nói: trong cùng fixed development protocol, thay feature track hoặc combination method đi kèm chênh lệch predictive/cost; complementary errors có nhưng không tự bảo đảm net gain. Đây là computational contrast có điều kiện trên benchmark, không causal explanation cho network attacks.

Không thể nói: learner nào “gây ra” gain của Stack khi chưa có leave-one-out contrast; diversity gây gain; temporal/domain shift gây holdout drop; FS riêng gây toàn bộ frozen RF17 cost gain; tuning chắc chắn cải thiện generalization; class_weight/resampling giúp hoặc không giúp toàn pipeline khi thiếu fair counterfactual. Khi không đủ evidence: **“Chưa có bằng chứng thực nghiệm để đưa ra kết luận này.”**

## No-post-test-selection guardrail / prohibited actions

- Không fit/refit/inference lại frozen models, không mở official TEST cho lựa chọn/tuning, không sửa features/hyperparameters/threshold (giữ 0.5).
- Không chọn lại trong RF/meta grids hoặc threshold sweep. Historical grid chỉ mô tả lựa chọn trước TEST và comparability.
- Không tạo official-test LR/DT/Voting/Stack17 outputs; chúng không nằm trong 3 frozen pipelines.
- Không SMOTE, class-weight experiment mới, re-split, dedup/relabel, raw edits hoặc overwrite outputs 6–10.
- Không giấu Voting negative result hoặc nâng claim Stack superiority. RF17 giữ efficiency trade-off; RQ4 PARTIAL.
- Không dùng draft reporting để chứng minh official phase đã hoàn thành; không move draft cũ trong scope lập plan này.

## Tasks sau khi user duyệt

1. Audit S6–S10/SF/SC về provenance, row alignment, config và metric definition; ghi fairness status trước tạo contrast.
2. Xây matrix contrasts A1–A6 theo schema dưới đây; loại khỏi numerical effects những contrast không fair, nhưng giữ hàng và lý do.
3. Aggregate existing metrics/OOF cho contrasts hợp lệ; reuse saved holdout statistics; không model training và không statistical test mới.
4. Viết synthesis trả lời questions, phân biệt development evidence, bundled final comparison và missing counterfactual; đóng no-resampling rationale bằng closure note.
5. Kiểm tra traceability, negative results và immutable hashes; trình CHECKPOINT Phase 13 trước khi chuyển Phase 14.

## Outputs và code/files to create/update

**Hiện tại chỉ tạo plan này và cập nhật reconciliation.** Các output sau là dự kiến, chưa tồn tại/chưa chạy:

- `results/ablation/unsw_nb15/phase13_ablation/phase13_ablation_matrix.csv`.
- `results/ablation/unsw_nb15/phase13_ablation/comparability_audit.csv` và `analysis_metadata.json` (input hashes, methods, no training, metric/source definitions).
- `notebook/phase13/phase13_ablation_summary.md`.
- `notebook/phase13/phase13_imbalance_closure_note.md` — original Phase 9 retrospective closure; ghi class-weight branch riêng, không giả vờ đã thử resampling.
- `src/analysis/run_unsw_phase13_ablation.py` — chỉ viết sau duyệt nếu cần, read-only existing inputs; output mới dưới ablation folder, không import training entry points, không overwrite evidence.
- Cập nhật board/log trong plan và `docs/ROADMAP_RECONCILIATION.md` khi có evidence thật.

Matrix schema: `contrast_id | axis | model_a | model_b | feature_track_a | feature_track_b | config_a | config_b | eval_view | estimator_type | metric | value_a | value_b | delta_a_minus_b | cost_ratio_a_over_b | n_rows | n_folds | comparability_status | source_a | source_b | uncertainty_source | interpretation_limit`.
Không đủ comparability/value: để trống numeric field, ghi reason; không điền 0. Source phải trỏ file và row selector có thể tái kiểm tra. `comparability_status` gồm MATCHED, CONDITIONAL, NOT_COMPARABLE, DESIGN_ONLY.

## Completion criteria

- User đã duyệt scope; audit đầy đủ exact pairing/config cho mỗi numerical contrast, mismatches công khai.
- Matrix/synthesis/metadata/closure note tồn tại, nguồn truy được; A5b được đánh NOT_COMPARABLE, no-resampling DESIGN_ONLY.
- Không mix mean-fold/pooled/test hoặc gán pure FS effect cho bundled RF holdout.
- Negative Voting/null overall Stack result, cost limitations, FS optimism, thiếu component ablation và RQ4 PARTIAL đều được giữ.
- Existing immutable artifacts/hash không thay đổi; không thí nghiệm mới hoặc tuning.
- CHECKPOINT Phase 13 được trình user; chỉ đánh DONE analysis task khi có artifact thật.

## Research Task Board

| ID | Task | Status (TODO/DOING/DONE/BLOCKED) | Evidence/Output |
|---|---|---|---|
| P13-01 | Lập plan và audit sơ bộ metadata/source/header | DONE | File plan này; exact alignment chưa chạy |
| P13-02 | User duyệt plan | DONE | User xác nhận thầy đã đồng ý và yêu cầu tiếp tục |
| P13-03 | Exact comparability/provenance audit | DONE | `results/ablation/unsw_nb15/phase13_ablation/comparability_audit.csv` |
| P13-04 | Aggregate ablation matrix | DONE | `results/ablation/unsw_nb15/phase13_ablation/phase13_ablation_matrix.csv` |
| P13-05 | No-resampling closure và class-weight context | DONE | `phase13_imbalance_closure_note.md` |
| P13-06 | Evidence-bounded synthesis và QA | DONE | `phase13_ablation_summary.md`, `analysis_metadata.json` |
| P13-07 | CHECKPOINT cuối phase | DONE | CHECKPOINT trong `phase13_ablation_summary.md`; không training hay TEST selection |

## Research Decisions Log

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Dùng retrospective saved-artifact synthesis | TEST đã mở; user chỉ giao plan trước thực thi | User request, recovered roadmap | Chờ duyệt; không bổ sung model experiment. |
| Fixed-config development FS và frozen holdout tách riêng | RF42/RF17 final khác cả params | S72 source; S8 freeze | Không gán toàn bộ final gain/loss cho FS. |
| Exclude cross-protocol Stack tuning effect | Nested outer evaluation khác global OOF meta CV | S72 metadata/source, S8 metadata/source | A5b chỉ protocol limitation. |
| Giữ no-resampling như design branch | Không có matched resampling evidence | SF class counts và configs | Closure note không claim resampling vô ích. |
| Giới hạn inference, giữ null/negative evidence | 3 CV folds không độc lập; missing counterfactual | S6–S10 protocols | Descriptive development, reuse locked holdout CI; không causal/superiority overclaim. |

## CHECKPOINT — retrospective synthesis

Phạm vi A1–A6 đã aggregate/diễn giải từ evidence hiện có. Không retrain, không test model mới, không statistical tests mới. Exact comparability audit và output ở summary đã hoàn thành. **Original Phase 13 retrospective synthesis DONE; feature-level error explanation chuyển Phase 14.**
