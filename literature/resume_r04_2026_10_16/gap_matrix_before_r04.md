# Gap synthesis có giới hạn sau reconciliation r02

r03 supplement: metadata subset6, ledger hiện hành literature/resume_r03_2026_10_16/legacy_verification_ledger.csv. L02 selected abstract/introduction/audit-stage reading cung cấp cơ sở cho nhu cầu kiểm toán pipeline dữ liệu CICIDS2017; không suy UNSW có cùng lỗi. L04 là ensemble feature selection theo publisher abstract, cần phân biệt với ensemble classifier. Không thay field-wide novelty hoặc validity conclusions từ việc metadata được xác minh.

Đây là positioning dựa trên nguồn đã đọc, không novelty claim hay systematic review hoàn tất. Evidence lookup: literature/resume_r02_2026_10_16/legacy_verification_ledger.csv và READING_NOTES.md. Danh mục cũ giữ nguyên để truy vết.

| Trục | Evidence liên quan | Hệ quả đối với NCKH | Điều chưa được chứng minh |
|---|---|---|---|
| Kết hợp ensemble và FS | L05, L06, L12; D01 chủ đề luận án | Không gọi sự kết hợp này là mới | Chưa audit mọi giải pháp đã công bố |
| OOF/stacking | L06 Methods có cross-validation predictions | OOF là yêu cầu thiết kế, không đóng góp mới tự thân | NCKH meta tuning/FS không fully nested |
| Imbalance | L07 dynamic undersampling; D02 mục tiêu sampling | RQ5 phải giữ PARTIAL, không suy sampling vô ích | Chưa matched resampling ablation trong NCKH |
| Performance và chi phí | L08/L11 abstract; frozen cost tables NCKH | Báo cáo trade-off và điều kiện đo | Không suy ưu thế hardware/deployment phổ quát |
| Validation robustness | L09 mới metadata; NCKH official/novel cùng benchmark | Công khai lack of external/time validation | Không tuyên bố novelty về cross-dataset hoặc temporal protocol |

Đóng góp có thể bảo vệ trong scope hiện tại là kiểm toán chuỗi benchmark đã lưu, so sánh các pipeline đóng băng và phân tích đánh đổi FPR/FNR/chi phí kèm giới hạn selection optimism. Khả năng công bố/novelty chưa được xác nhận. Không dùng tên thuật toán mới để che việc kết hợp thành phần đã có.

Ưu tiên tiếp: full-source reading L01/L02/L09 cho validity/split; kiểm đủ metadata còn thiếu; cập nhật literature2026 theo chiến lược có log nếu cần claim cập nhật. Không thay dataset/RQ theo kết quả search.
