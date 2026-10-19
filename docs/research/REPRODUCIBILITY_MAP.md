# NCKH — P15-01 Reproducibility Map (canonical roadmap 0–20)

**Trạng thái: ĐÃ LẬP BẢN ĐỒ từ code snapshot + các script ZIP sau audit; còn chờ đối chiếu hiện trạng project trên máy để chốt P15-01 toàn phần.**

## Giới hạn bằng chứng
- **14 script cũ:** đã đọc nội dung Python từ `NCKH_FRESH_AUDIT_V2_20261010_224249.zip`, đối chiếu tồn tại trong inventory 234 file của lần chụp 2026-10-10; mã nguồn được **kiểm tra cú pháp**. Việc các script tồn tại trong ZIP **không chứng minh chúng đang còn nguyên trong project hiện tại**.
- **4 script bổ sung** (đóng Phase11 và ba Step Phase14): xác minh mã Python từ ZIP đã gửi trong cuộc trò chuyện; không nằm trong inventory cũ (được tạo/giao sau audit). Các output Phase11/14 từng được đối chiếu tổng hợp nhưng **không tái chạy lại trên raw file ở bước này**.
- Các cột `inputs`, `outputs` là **hợp đồng đường dẫn và output đại diện**, không bao quát mọi phụ thuộc tùy chọn hay mọi file được ghi. Cột số lượng trong inventory chỉ xác nhận PATH ở snapshot, **không xác thực hash nội dung large raw/OOF/predictions**.
- SHA-256 CSV áp dụng cho **source script bytes trong gói audit hoặc script ZIP đã giao**, chưa phải checksum file trên máy bạn. Không train/rerun model và **không chạm official TEST** trong P15-01.

## Đường đi dependency (khóa canonical numbering)
```text
TRAIN/TEST official CSV (Phase 2)
  ├─ P3: raw audit, overlap audit, novel-vector view
  ├─ P4: EDA / mô tả
  └─ TRAIN ─> P5: FS stage1 ─> P5: FS stage2/subsets JSON
                                   ├─ P6: baseline CV
                                   ├─ P7: base diversity OOF + ensemble OOF
                                   └─ P10: tuning ─> freeze_candidates.json
                                            └─ P11: ONE-TIME frozen TRAIN+official TEST holdout
                                                  ├─ saved metrics/cost ─> P11 closure
                                                  ├─ saved predictions ─> P12 paired stats
                                                  └─ saved predictions + raw TEST ─> P14 errors
  P13 retrospective = OOF + tuning + official aggregate + paired-stat evidence
  P16 early figures = saved reporting tables from P11/P12 (not Phase11 execution)
```

## Phases 2–5: dữ liệu, EDA, feature selection

**Phase 2:** lựa chọn benchmark được lưu bằng quyết định/tài liệu; không có script riêng bắt buộc. TRAIN/TEST public ở `data/raw/unsw-nb15/`. URL/version/license cần xác thực P15-03.

### P03-A · Phase 3 · `src/data/audit_unsw-nb15.py`
**Chức năng:** Raw-data profile, missing/inf, labels and hashes.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`; `data/raw/unsw-nb15/NUSW-NB15_features.csv`.
**Outputs đại diện:** `results/data_audit/unsw_nb15/raw_file_checksums.csv`; `results/data_audit/unsw_nb15/dataset_summary.json`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P03-B · Phase 3 · `src/data/audit_unsw-nb15_overlap.py`
**Chức năng:** Within/across split overlap and label conflicts; no blanket dedup.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`.
**Outputs đại diện:** `results/data_audit/unsw_nb15_overlap/overlap_consistency_summary.json`; `results/data_audit/unsw_nb15_overlap/cross_split_conflicts.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P03-C · Phase 3 · `src/data/build_unsw_experiment_views.py`
**Chức năng:** Build novel-vector sensitivity view (still same benchmark).
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`.
**Outputs đại diện:** `data/interim/unsw-nb15/test_unseen_vectors.csv`; `results/data_audit/unsw_nb15_views/view_summary.json`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P04-A · Phase 4 · `src/data/eda_unsw-nb15.py`
**Chức năng:** Descriptive EDA on TRAIN; TEST distribution contextual only.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`; `data/interim/unsw-nb15/test_unseen_vectors.csv`.
**Outputs đại diện:** `results/eda/unsw_nb15/tables/binary_class_distribution.csv`; `results/eda/unsw_nb15/tables/numeric_feature_summary_train.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P05-A · Phase 5 · `src/features/select_unsw_features_stage1.py`
**Chức năng:** Mutual information, redundancy, L1 and tree ranking.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`.
**Outputs đại diện:** `results/feature_selection/unsw_nb15/stage1/subsets/candidate_feature_subsets.json`; `results/feature_selection/unsw_nb15/stage1/tables/consensus_feature_ranking.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P05-B · Phase 5 · `src/features/select_unsw_features_stage2.py`
**Chức năng:** Stability seeds and RFECV; finalize feature candidates.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `results/feature_selection/unsw_nb15/stage1/subsets/candidate_feature_subsets.json`.
**Outputs đại diện:** `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`; `results/feature_selection/unsw_nb15/stage2/tables/selection_stability.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

## Phases 6–10: development, ensemble và tuning

### P06-A · Phase 6 · `src/models/run_unsw_baseline_development.py`
**Chức năng:** LR/DT/RF development CV with different feature sets.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`.
**Outputs đại diện:** `results/baselines/unsw_nb15/development_cv/tables/aggregate_metrics.csv`; `results/baselines/unsw_nb15/development_cv/tables/fold_metrics.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P07-A · Phase 7 · `src/models/run_unsw_diversity_oof.py`
**Chức năng:** OOF base model predictions/diversity and double-fault.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`.
**Outputs đại diện:** `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`; `results/ensemble/unsw_nb15/phase7_1_diversity/oof/all_features_oof_predictions.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P07-B · Phase 7 · `src/models/run_unsw_ensemble_phase7_2.py`
**Chức năng:** Development ensemble voting/stacking OOF comparison.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`.
**Outputs đại diện:** `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`; `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/oof/all_features_ensemble_oof.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

**Phase 8:** kiến trúc Stacking thể hiện qua code và freeze config của Phase 7/10/11; chưa có một spec kiến trúc chuyên biệt đóng Phase 8.

**Phase 9:** chính sách imbalance có ghi lý do không mặc định resampling; không có script ablation SMOTE/ROS riêng. Không được tuyên bố đã làm balanced-data factorial comparison.

### P10-A · Phase 10 · `src/models/run_unsw_phase8_controlled_tuning.py`
**Chức năng:** TRAIN-only controlled tuning and candidate freeze; local label phase8.
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`.
**Outputs đại diện:** `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`; `results/tuning/unsw_nb15/phase8_controlled/tables/rf42_grid_results.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

## Phases 11–14: frozen evaluation và hậu kiểm

### P11-A · Phase 11 · `src/models/run_unsw_phase9_final_holdout.py`
**Chức năng:** Original frozen official holdout; local label phase9 (DO NOT RERUN by default).
**Inputs:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`; `data/interim/unsw-nb15/test_unseen_vectors.csv`; `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json`; `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`.
**Outputs đại diện:** `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`; `results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P11-B · Phase 11 · `src/analysis/close_original_phase11.py`
**Chức năng:** Derive per-class and weighted F1 from frozen aggregate counts; local script placement requires validation.
**Inputs:** `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`; `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`.
**Outputs đại diện:** `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv`; `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_per_class_metrics.csv`.
**Evidence:** Delivered script ZIP (post-audit), not rechecked against current local project; 0/2 output đại diện có đường dẫn trong audit cũ.

### P12-A · Phase 12 · `src/analysis/run_unsw_phase10_statistics.py`
**Chức năng:** Paired bootstrap, McNemar, Wilson; local label phase10.
**Inputs:** `results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`; `results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv`.
**Outputs đại diện:** `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P13-A · Phase 13 · `src/analysis/run_unsw_phase13_ablation.py`
**Chức năng:** Retrospective ablation synthesis only; NOT causal full-factorial.
**Inputs:** `results/ensemble/unsw_nb15/phase7_1_diversity/oof/all_features_oof_predictions.csv`; `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/oof/all_features_ensemble_oof.csv`; `results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv`; `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`; `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`.
**Outputs đại diện:** `results/ablation/unsw_nb15/phase13_ablation/phase13_ablation_matrix.csv`; `results/ablation/unsw_nb15/phase13_ablation/comparability_audit.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

### P14-A · Phase 14 · `src/analysis/phase14_step1_error_transitions.py`
**Chức năng:** Paired correctness, family FN breakdown from frozen predictions.
**Inputs:** `results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`.
**Outputs đại diện:** `results/final_analysis/unsw_nb15/phase14_error_analysis_step1/class_pairwise_transitions.csv`; `results/final_analysis/unsw_nb15/phase14_error_analysis_step1/attack_family_transitions.csv`.
**Evidence:** Delivered script ZIP (post-audit), not rechecked against current local project; 0/2 output đại diện có đường dẫn trong audit cũ.

### P14-B · Phase 14 · `src/analysis/run_unsw_phase14_normal_feature_profiles.py`
**Chức năng:** Join by unique ID; descriptive Normal FP features.
**Inputs:** `results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`.
**Outputs đại diện:** `results/final_analysis/unsw_nb15/phase14_error_analysis_step3/state_by_value.csv`; `results/final_analysis/unsw_nb15/phase14_error_analysis_step3/sttl_by_value.csv`.
**Evidence:** Delivered script ZIP (post-audit), not rechecked against current local project; 0/2 output đại diện có đường dẫn trong audit cũ.

### P14-C · Phase 14 · `src/analysis/run_unsw_phase14_fuzzers_feature_profiles.py`
**Chức năng:** Join by unique ID; descriptive Fuzzers FN features.
**Inputs:** `results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`; `data/raw/unsw-nb15/UNSW_NB15_testing-set.csv`.
**Outputs đại diện:** `results/final_analysis/unsw_nb15/phase14_error_analysis_step4/fuzzers_pairwise_groups.csv`; `results/final_analysis/unsw_nb15/phase14_error_analysis_step4/proto_by_value.csv`.
**Evidence:** Delivered script ZIP (post-audit), not rechecked against current local project; 0/2 output đại diện có đường dẫn trong audit cũ.

## Phase 16: figures đã làm sớm

### P16-EARLY · Phase 16 · `src/analysis/run_unsw_phase11_results_figures.py`
**Chức năng:** Historical early figures/reporting; NOT canonical Phase11 completion.
**Inputs:** `results/final_analysis/unsw_nb15/phase10_statistics/tables/recomputed_point_metrics.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/bootstrap_metric_ci.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/official_vs_novel_degradation.csv`; `results/final_analysis/unsw_nb15/phase10_statistics/tables/performance_cost_tradeoff.csv`.
**Outputs đại diện:** `results/final_reporting/unsw_nb15/phase11_results_figures/phase11_metadata.json`; `results/final_reporting/unsw_nb15/phase11_results_figures/tables/table01_final_performance_with_ci.csv`.
**Evidence:** Fresh Audit V2 code snapshot; 2/2 output đại diện có đường dẫn trong audit cũ.

## Chỗ đặt file dễ sai / lưu ý học thuật
- **Local `phase8_controlled` = canonical Phase 10**; local `phase9_holdout` = canonical Phase 11; local `phase10_statistics` = canonical Phase 12. Giữ nguyên lịch sử tên file hiện tại, chỉ ánh xạ trong tài liệu.
- **`run_unsw_phase11_results_figures.py` thuộc early artifacts của canonical Phase 16**, không được dùng làm bằng chứng đã đóng Phase 11 trước khi có formal evaluation closure.
- **Phase13 ablation** đọc saved development OOF, grids và các aggregate đã lưu; không phải thí nghiệm can thiệp factor-controlled đầy đủ. File `results/ablation/.../development_metrics.csv` có provenance chưa rõ, không đưa làm required input.
- **P14-05** là tổng hợp tài liệu và kiểm toán số liệu, không có train/analyzer mới; hồ sơ `docs/research/ERROR_ANALYSIS_CLOSURE.md` và reconciliation JSON (được giao ở bản handoff trước).
- `attack_cat` chỉ dùng cho mô tả/lỗi theo nhóm, **không phải X binary**. Official TEST đã xem; mọi `rerun` P10/P11 để chọn model/threshold mới đều không hợp lệ với kết quả đã khóa.
- Feature selection đã chạy trên TRAIN trước development CV: CV có nguy cơ **selection optimism**. Final official holdout là bằng chứng primary (nhưng vẫn giới hạn trong cùng benchmark).
- Không khẳng định hỗ trợ external multi-dataset, temporal drift hay deployability; novel-vector chỉ là độ nhạy trong cùng benchmark.

## Còn thiếu để tăng mức tái lập
**P15-02:** Ghi version Python/packages/OS/hardware và khóa môi trường (audit cũ chưa thấy requirements/lock).
**P15-03:** Ghi download URL, citation, license, SHA-256 raw TRAIN/TEST, preprocessing/split details.
**P15-04:** Audit seed/folds/OHE/scaler/feature selection và mọi frozen hyperparameter/threshold từ source + output.
**P15-05:** Verify checksums live và minimal **read-only** rerun saved-artifact analyses trên output mới, không đụng frozen originals.
**P15-06:** Viết clean-start README và công bố rõ mức tái lập: saved-artifact vs end-to-end model retrain.

## P15-01 CHECKPOINT
| ID | Task | Trạng thái | Evidence |
|---|---|---|---|
| P15-01A | Xác định code entry points và canonical phase | DONE (archived evidence) | 18 script source parsed, source hashes trong CSV |
| P15-01B | Ghi script → inputs → representative outputs | DONE (static contract) | `P15_01_SCRIPT_IO_MATRIX.csv`, tài liệu này |
| P15-01C | Xác nhận code + output hiện tồn tại ở NCKH trên máy user | **PENDING** | Chạy inventory-only checker và gửi lại JSON; không train |
| P15-01 total | Mapping đáng tin ở mức static; local current-state verification | **PARTIAL** | Cần P15-01C trước khi đánh DONE toàn phần |

**Lệnh kiểm tra nhẹ (đứng tại thư mục NCKH):** `py tools\p15_01_inventory_check.py --project-root . --out results\reproducibility\p15_01_inventory\p15_01_local_inventory.json`.
Trình kiểm tra chỉ đọc các input và script. Nó tạo **một** JSON report ở folder mới chỉ định; không đọc nội dung CSV lớn, không đổi kết quả thí nghiệm.
