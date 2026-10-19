# Scientific Evidence Map — Creative V2

Các đường dẫn và hash trong phần nguồn phía dưới đã có từ audit nghiên cứu; đối chiếu hash lại trong QA. Bảng slide mới sau đây thay thế số slide cũ của deck32 trang. Không chạy lại mô hình.

|Slide V2|Nội dung|Nguồn/field|
|---|---|---|
|1,11,12|−142 FP, +118 FN; RF10003/734; Stack9861/852|TEST official_test, fp/fn|
|3|175341 TRAIN,82332 TEST|V6 §3.1; protocol official split|
|4–9|42 predictor, LR/DT/RF, OOF/meta LR, inference|HIST_CODE build_preprocessor/make_stacking_42; DEV_CODE; V7 §3.2–3.4|
|7|RF42 lịch sử300 cây|HIST_CODE make RF42; không gán300 cho RF42-Lite|
|10|MacroF1 .863343/.863840; Δ+.0004966899; CI chứa0|TEST macro_f1,mcc; CI official_test; tọa độ CI tuyến tính đúng hai cận|
|13|5 FIT seed×5 arm,60000 FIT,35069 validation cố định|P21 per_seed, protocol; không5 TEST|
|14|F1 RF42 .945220/Stack .944731/RF17 .936751;225.250+84.600=309.850s,RF42241.119s|P21 per_seed, V7 bảng4.11; mean5; selector+model fit, chưa end-to-end|
|15|FPR/FNR ba nhánh, trung bình5seed|P21 metrics_by_arm fpr/fnr; Normal minority|
|16|L=FP+rFN; r=142/118; r1/1.2034/5|TEST fixed counts; chỉ mô hình chi phí giả định|
|17,18–29|Giới hạn, leakage, đóng góp|V7 §3.2–3.6,5.3–5.5; frozen source|

## Danh mục nguồn gốc và chi tiết khoa học đã kiểm tra



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


## Ranh giới bằng chứng

Historical official TEST và P21 không cùng tập đánh giá. P21 hậu nghiệm official TRAIN; 5 seed chỉ mô tả biến thiên fit có điều kiện trên1validation. stable17 lịch sử chọn trước CV còn selection optimism; không nói pipeline lịch sử hoàn toàn leakage-free. RF17 lịch sử đổi cả cấu hình, không FS-only. Không thuật toán mới, không IDS realtime, không khẳng định Stacking vượt trội.
