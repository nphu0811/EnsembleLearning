# Canon cho đề cương

## Bổ sung nguồn r04 (không thay RQ hoặc cam kết)

Current metadata ledger: `literature/resume_r04_2026_10_16/legacy_verification_ledger.csv`,11 VERIFIED_METADATA vàL03 CHECK_SUGGESTED. Source-linked notes/map cùng thư mục: L06 Methods xác nhận CV meta inputs và random80/20; L09 indexed Introduction phân biệt within/cross-dataset; D01 announcement vàD02 summary objectives hỗ trợ bối cảnh trong nước. Đây là scoped readings, không full-source/systematic review. Giữ nguyên scientific tension/gates và foundation review r02; không có thay đổi scope hay concern mới buộc mở lại RQ.

Canon chính: `.research_memory/RESEARCH_CANON.md`; RQ nguyên gốc `notebook/phase01/phase1_frozen_research_design_v1.md`. File này là mapping viết đề cương, không thay canon.

## Literature facts

UNSW source page xác nhận standard split và điều kiện truy cập như `docs/research/DATA_CODE_AVAILABILITY.md`. Literature matrix cũ ở notebook/phase01 giữ làm lịch sử; bản đối chiếu mới là `literature/resume_r02_2026_10_16/legacy_verification_ledger.csv`.

- L05, DOI10.1016/j.jnca.2022.103560: AutoML và soft voting trong IDS đã có, cùng feature reduction/resampling theo publisher preview; không claim kết hợp này mới.
- L06, DOI10.1007/s40747-023-01013-7: Methods mô tả stacking GNB/LR/DT→SGD, cross-validated meta inputs và random80/20. Không đối chiếu trực tiếp scores với official split của NCKH.
- L07, DOI10.1016/j.eswa.2023.120420: dynamic undersampling trong boosting được nghiên cứu cho multiclass IDS, theo abstract/preview. Không dùng để kết luận resampling của NCKH.
- L08, DOI10.1007/s10207-023-00767-y: publisher abstract khảo sát nhiều filters/classifiers; final volume2024 khác online2023. Không suy nested validity từ abstract.

Nguồn và reading boundary trong `literature/resume_r02_2026_10_16/READING_NOTES.md`. Có D01 Lạc Hồng và D02 UET làm nguồn trong nước, chỉ dùng claims trong DOMESTIC_SOURCES. Chưa hoàn tất full review hoặc verified toàn bộ bibliography; không nâng metadata thành kết quả đã đọc.

## Experimental facts

Ba model final đã khóa, threshold 0.5. Macro-F1 Stack−RF42 CI chứa 0. Official confusion counts cho thấy FP giảm 142, FN tăng 118. Nguồn C02–C04 trong claim matrix. Binary labels, FS optimism và limitations theo canon chính.

## Model facts

LR+DT+RF stacking, OOF 3 inner folds, meta LR, không thuật toán mới. Chưa có inference model được serialize.

## Constraints và thuật ngữ

Chưa có yêu cầu riêng của GVHD đã xác minh. User yêu cầu giữ form, không bịa facts/chữ ký. Detection Rate=Recall của Attack; FPR=FP/(TN+FP), FNR=FN/(TP+FN). Macro-F1 trung bình không trọng số hai lớp; minority attack family không đồng nghĩa multiclass model.

## Forbidden / unresolved

Cấm superiority/novelty/real-time/fully leakage-free hoặc đã ký/được duyệt khi thiếu evidence. Nguồn domestic đã có topic-level evidence; detailed method/result comparison còn thiếu. Unresolved: full refs, original training env, model/demo và nguồn lực reconstruction; người thực hiện/GVHD; tính chấp nhận hồ sơ phục hồi, lịch/kinh phí/copies. Các mục chưa đạt không được mặc nhiên hứa đạt bằng một lần tái dựng.
