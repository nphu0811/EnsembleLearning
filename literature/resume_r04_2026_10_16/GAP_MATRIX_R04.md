# Research Gap Matrix r04

Mục đích: xác định câu hỏi còn cần giải thích trong case study đã khóa, không nhận khoảng trống của toàn lĩnh vực. Literature corpus hiện là danh mục mục tiêu được kế thừa, chưa systematic search/screening cập nhật2026. Metadata11/12 verified; L03 page conflict mở. RQs không thay đổi. Các source/reading scopes giải tại ledger và SCOPED_READING_NOTES.md.

| Trục / RQ | Prior work biết từ phần đã đọc | Scope NCKH / evidence | Khoảng thiếu thực sự và hệ quả | Kết luận được phép |
|---|---|---|---|---|
| Ensemble design /RQ1 | L01 mapping-study abstract;L05 soft voting;L06 stacking GNB/DT/LR→SGD với CV meta inputs | LR/DT/RF→LR, frozen RF42/Stack42/RF17; C02–C04 | Chưa independent retraining stability; development selection optimism | So sánh có điều kiện trên benchmark; không nhận stacking hoặc combination mới |
| Feature selection /RQ2 | L04 ensemble feature selection;L08 filters;L11 FS/normalization;L12 filter+embedded snippets |42/17 predictors, frozen cost/performance;C05 | RF17/RF42 khác hyperparameters; không isolated causal effect | Joint pipeline performance–cost trade-off; không suy số features là nguyên nhân duy nhất |
| Error complementarity /RQ3 | L06 chọn base learners và dùng CV outputs; chưa audit empirical diversity của mọi paper | Saved OOF diversity/negative Voting;C06 | Association mô tả, không leave-one-component causal study;selection dependence | Có thể mô tả complementarity; không khẳng định diversity bảo đảm gain hoặc prior work không xét diversity |
| Dataset integrity /G1 | L02 selected audit stages;L03 author code/docs, page warning | Raw hashes, overlap audit, feature views;C01/C07 | Không biết mọi historical execution/env;không fully leakage-free | Kiểm toán cần minh bạch; không chuyển lỗi/tỷ lệ lỗi CIC sang UNSW |
| Split robustness /RQ4 | L09 indexed Introduction phân biệt within/cross-dataset | Official/novel views đều UNSW;C07 | Chưa temporal/day/scenario hay external validation;novel view không dataset độc lập | RQ4 PARTIAL;không claim đã giải bài toán generalization ngoài benchmark |
| Imbalance /RQ5 phụ | L07 dynamic undersampling preview;D02 summary mục tiêu data-quality/sampling | No-resampling/class-weight scope;C08 | Không matched resampling intervention;không mở chọn model sau TEST | RQ5 PARTIAL/UNANSWERED cho efficacy;không kết luận SMOTE/sampling vô ích |
| Trong nước /positioning | D01 thông báo Lạc Hồng;D02 tóm tắt UET có voting/stacking mục tiêu | NCKH là nghiên cứu sinh viên binary benchmark | Chưa whole-thesis/result/protocol comparison;không domestic survey exhaustive | Hướng ensemble/preprocessing đã có trong nước;không claim đầu tiên tại Việt Nam |
| Reproducibility /G3 | R04C03, L03 author Tools & Documentation, Paper Code repository: công khai labeling/experiment code; documentation claim only, paper pagination unresolved | Aggregate replay 3 CSV đạt;original env UNKNOWN/model thiếu;C09/C11 | Chưa ML clean replay/serialized transformer/model | Static integrity và reporting replay có giá trị riêng;không end-to-end reproduction |

## Luận cứ khoa học

Những thành phần thiết kế đã có prior art; câu hỏi có ích cho hồ sơ này là sự đánh đổi của chính các pipeline đã khóa và độ tin cậy mà protocol hiện có cho phép. Known outcomes không được viết thành hypothesis trước thực nghiệm. Đóng góp đề xuất là case study có truy vết, báo cáo cả uncertainty, lỗi và chi phí cùng giới hạn; chưa chứng minh novelty cấp lĩnh vực.

## Acceptance và QA

Mỗi hàng có source/reading boundary, RQ/gate và inferential limit. Source-C IDs nội bộ giải tại docs/CLAIM_EVIDENCE_MATRIX.md, R04C IDs giải source_claim_map.csv. Không đưa score paper khác vào matched baseline table. Không yêu cầu sửa frozen data/results hoặc đổiRQ để “đóng” khoảng thiếu. RQ4/RQ5 vàG3 vẫn partial ngay khi prose/gap map được review đạt.
