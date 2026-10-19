# Claim và bằng chứng

Path tương đối từ workspace root. Hash truy vết ở EVIDENCE_INDEX và preservation_manifest. Không dùng metadata/log thay artifact đầu ra.

| ID | Claim / RQ | Run/evidence | Source/config | Giới hạn / trạng thái |
|---|---|---|---|---|
| C01 | Binary UNSW standard split 175341/82332 | resume_2026_10_16/p15_03_dataset.json; raw CSV | tools/p15_03_check_dataset_provenance.py | Local historical hashes PASS, không official checksum |
| C02 | Ba final candidate, threshold 0.5 | phase8_controlled/freeze_candidates.json; phase9_holdout/experiment_metadata.json | run_unsw_phase8_controlled_tuning.py; run_unsw_phase9_final_holdout.py | P15-04 static consistency PASS |
| C03 | RQ1 chưa có superiority tổng thể Stack vs RF42 | phase9_holdout/tables/final_metrics.csv; phase10_statistics/tables/paired_bootstrap_differences.csv, mcnemar_holm.csv | run_unsw_phase10_statistics.py | CI Macro-F1/MCC chứa 0; không equivalence |
| C04 | Stack giảm FP 142, tăng FN 118 | final_metrics.csv; P11 confusion matrices | close_original_phase11.py | Official frozen binary predictions; không thay threshold |
| C05 | RQ2 pipeline RF17 trade-off | phase9_holdout/tables/cost_metrics.csv; phase13_ablation_matrix.csv | Frozen RF17 vs RF42 configs khác nhau | Không causal feature-only effect |
| C06 | RQ3 complementarity không bảo đảm gain | phase7_1_diversity/tables/pairwise_diversity.csv; phase7_2_ensemble_cv/tables/aggregate_metrics.csv | run_unsw_diversity_oof.py; run_unsw_ensemble_phase7_2.py | Development selection optimism, giữ voting negative |
| C07 | RQ4 chỉ partial robustness | official/novel rows trong final_metrics.csv | build_unsw_experiment_views.py | Cùng benchmark; không external/time split |
| C08 | RQ5 thiếu matched resampling | Existing frozen no-resampling protocol | ENSEMBLE_FRAMEWORK.md và nguồn lịch sử | UNSUPPORTED nếu claim sampling kém |
| C09 | Weighted-F1/per-class report tái lập | phase11_clean_replay/3 CSV + clean_replay_report.json | close_original_phase11.py, isolated stdlib venv | PASS hậu xử lý, không train reproducibility |
| C10 | Error profiles là mô tả | phase14_error_analysis_step1/3/4/5; ERROR_ANALYSIS_CLOSURE.md | phase14 analysis scripts | Không causal; 375 checks là evidence lịch sử |
| C11 | FS không nằm trong outer development fold | resume protocol source evidence | select_unsw_features_stage2.py | Bắt buộc công khai; không claim unbiased CV |
| C12 | Template DOCX riêng, ZIP LaTeX | bootstrap/template_audit.json, proposal_template_structure.json | templates/original/ | Structural PASS, visual QA chưa chạy |
| C13 | Ensemble+FS/voting không mới tự thân | L05/L06/L12: literature/resume_r02_2026_10_16/READING_NOTES.md và DOI raw | Publisher preview/selected Methods | Prior-art positioning, không novelty survey đầy đủ |
| C14 | Hướng IDS/ensemble/preprocessing đã có trong nước | D01 thông báo Lạc Hồng, D02 tóm tắt UET | DOMESTIC_SOURCES.md | Không suy kết quả hoặc trạng thái cấp bằng từ thông báo |
| C15 | Danh mục legacy có12 DOI final resolve; r04 xác nhận metadata11/12, L03 CHECK_SUGGESTED page conflict | literature/resume_r04_2026_10_16/legacy_verification_ledger.csv + FIELD_VERIFICATION_REPORT.md + validation.json | literature/refs_verified_subset.bib có11 mục; subset4 là checkpoint r02 lịch sử | Metadata verification không full-text/protocol verification; L03 và U01/U03 còn mở, P18 chưa hoàn tất |

Tên rút gọn `resume_2026_10_16` nằm dưới `results/reproducibility/`; `phase8_controlled` dưới `results/tuning/unsw_nb15/`; `phase9_holdout`/P11 dưới `results/final_evaluation/unsw_nb15/`; `phase10_statistics` và P14 dưới `results/final_analysis/unsw_nb15/`; P13 dưới `results/ablation/unsw_nb15/`; P7 dưới `results/ensemble/unsw_nb15/`.
