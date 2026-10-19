# Scientific Evidence Map

Ngày đối chiếu: 19/10/2026 (Asia/Saigon). Không fit/retrain, không đọc raw TEST, không sửa kết quả đóng băng. Toàn bộ số biểu diễn lấy từ artifact có sẵn, chỉ tái tính số học từ confusion counts và trung bình seed.

## Nguồn gốc

| ID | Artifact tương đối từ repository | SHA-256 |

|---|---|---|

| V6 | `exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf` | `40b35c9a5c7f228ee91bbba94cfb0ccd701d52dd707a6f5b184171412ce6afc3` |

| TEST | `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv` | `8a3ddd6a9e5876180bb9b62547c22b0a73faabee53fec7b8eb507cf62a0ddb20` |

| CI | `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv` | `3338849b204702597a05c271cb309f2928e9850a1e2d5dedc6a54548256f7d90` |

| P21 | `results/controlled_extensions/p21_train_only_science_summary_20261019_022655/aggregate.json` | `e587e7128591546c86a9b3769f809500dea43c0b84d590008fcac3068d7de071` |

| P21_PROTOCOL | `config/p21_train_only_protocol_2026_10_18.json` | `3a4c21cd069432c36cb8cfcdb863dbd4898845cd095fb4111be34b8d0c455c86` |

| HIST_CODE | `src/models/run_unsw_phase9_final_holdout.py` | `3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480` |

| DEV_CODE | `src/models/run_unsw_ensemble_phase7_2.py` | `d2f22ea57172053c6b21dab4eda182bd2fcba23ce1182e725197ea43a826e1fb` |

| P21_CODE | `tools/p21_science_core.py` | `19e4248328a8e5393d344df2f6ec9e3080128afb1a247c103e00dc4c29993ae4` |

| SELECTOR | `tools/p21_selector_core.py` | `1983977947672e94946d72752a16beb80c1bcacea0ca83f131877c96e79bd082` |

## Claim → slide → bằng chứng

| Claim / số liệu | Slide | Truy vết | Giới hạn |

|---|---|---|---|

| 175.341 TRAIN, 82.332 TEST; Attack=1; 42 predictor gốc | 2–7, A3 | V6 PDF tr.27–28 (trang in16–17), §3.1–3.3 | Không phải bắt gói realtime; id/label/attack_cat bị loại |

| LR/DT/RF, Voting, Stacking meta LR OOF | 8–10, A2/A7 | HIST_CODE build_preprocessor/make_stacking_42; DEV_CODE CONFIGURATIONS; P21_CODE make_stacking | Phân biệt train meta bằng OOF và suy luận; RF tự nó đã là ensemble |

| RF42 Macro-F1 0.8633434737, MCC 0.7509102615 | 11 | TEST: pipeline=random_forest_42, eval_view=official_test | Ngưỡng0.5; cùng 82.332 dòng |

| Stacking42 Macro-F1 0.8638401636, MCC 0.7504972252 | 11 | TEST: pipeline=stacking_42, eval_view=official_test | Chỉ ΔMacro-F1 +0.0004966899; MCC thấp hơn |

| FP RF=10003, Stack=9861; FN RF=734, Stack=852 | 12–14 | TEST cột fp,fn; Δ(Stack−RF)=−142,+118 | Số bản ghi; FP/FN hai trục riêng ghi rõ |

| CI95% ΔMacro-F1 [−0.0003118042,+0.0013089503]; ΔMCC [−0.0019378760,+0.0011395704] | 14, A9 | CI: official_test, stacking_42 vs random_forest_42 | Paired bootstrap hàng dữ liệu, 10.000 lượt; không phải CI biến thiên train |

| 5 FIT seed, 5 arm; 60.000 FIT/seed; 35.069 validation cố định | 15, A5 | P21 per_seed + các report được aggregate trỏ tới; audit/p21_verifier.txt | Hậu nghiệm TRAIN; không phải 5 TEST hay external validation |

| P21 RF42-Lite mean F1 0.945220; Stacking-Lite 0.944731 | 16 | P21 per_seed[seed].metrics_by_arm[A0_RF42_NONE/A4_STACK42_NONE].macro_f1; trung bình5 | 5 điểm và các đoạn nối cùng seed. Trục rút gọn0.944–0.946 ghi trên chart |

| P21 RF17-Lite F1 0.936751; fit84.600s +selector225.250s=309.850s; RF42fit241.119s | 17, A6 | V6 PDFtr.41, Bảng4.11; P21 per_seed.fit_seconds_by_arm; seed run_report.json worker_checks.selector.fit_seconds | Các lời gọi fit đo được, không phải end-to-end; RF17 lịch sử không FS-only |

| Balanced/Oversample giảm FPR, tăng FNR so A0 | 18, A11 | P21 metrics_by_arm fpr,fnr; mean5 | Normal là minority TRAIN. Cùng validation; không chọn lại threshold |

| ΔL=−142+118r; hòa r=142/118≈1.2034 | 19, A10 | TEST confusion counts; V6 §5.1 PDFtr.43 | Giả định cost-ratio; chỉ đúng cặp RF42/Stacking42 và dự đoán cố định |

| Selection bias stable17 trước CV; P21 không sửa hồi tố | 6,20,A4 | V6 §3.2–3.4 PDFtr.27–29 | Không tuyên bố toàn bộ historical development leakage-free |

| Không thuật toán mới, không external validation/triển khai trực tiếp | 20,A1/A12 | V6 §3.1,§3.5,§5.3–5.5 | Đóng góp là đối chiếu/kiểm chứng trong phạm vi benchmark |

## Quy tắc không được nói

Không nói “Stacking vượt trội”, “5 TEST độc lập”, “P21 là external TEST”, “RF17 giảm tổng chi phí” hay “đã triển khai IDS realtime”. Không gộp mức F1 TEST và P21 vào một trục như cùng điều kiện. Không biến OOF lịch sử thành nested hoàn chỉnh. Không trình bày ngưỡng chi phí giả định như thiệt hại thực tế.
