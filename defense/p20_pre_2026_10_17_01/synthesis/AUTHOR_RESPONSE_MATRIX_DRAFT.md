# P20-PRE — Bảng phản hồi tác giả (nháp, chưa sửa manuscript)

**Trạng thái:** `DRAFT; ALL_CONCERNS_OPEN`. Trả lời dựa trên hồ sơ đóng băng, không biến phản biện AI thành phán quyết của giáo sư thật. Chỉ đề xuất sửa companion hoặc bản thảo trong tương lai sau khi tác giả duyệt; PDF 37 trang hiện hành, raw data, metrics và model configs giữ nguyên.

| Group | Concern IDs | Draft response có evidence | Phương án/hành động | Trạng thái |
|---|---|---|---|---|
| G01 Development quantitative display | A-M2, B-M2, C-M3 | Diversity, OOF và Voting đều có outputs development lưu riêng; tường thuật trong PDF còn thiếu bảng chi tiết. Không lấy metric development gọi là official TEST. | Chuẩn bị bảng bổ sung từ `results/ensemble/unsw_nb15/phase7_1_diversity/tables/pairwise_diversity.csv`, `phase7_2_ensemble_cv/tables/pooled_oof_metrics.csv`, các Voting tables. Khai báo tên phase, split, n, metric và negative findings. | OPEN |
| G02 P15 provenance chronologic | A-M3, B-M1, C-M2 | PDF ghi đúng snapshot cũ tại thời điểm viết. Sau đó P15 đã tạo 3 reconstructed full TRAIN model, được laptop-side SHA/schema/proba QA chấp thuận; không có bằng chứng binary lịch sử bitwise giống. | Companion dated `2026-10-17` giải thích P15 3/3, 69/69 checks, snapshot trang 33/35; tránh thay PDF không có yêu cầu. | OPEN |
| G03 Stable17/FS lineage | A-M1, C-m1 | Track17 không tự chứng minh causal FS gain vì RF17/RF42 khác hyperparameters, FS chưa fully nested in outer development CV. | Dẫn chính xác 17 biến và thứ tự, 5 seeds, 3/5 stability rule, phương pháp và preprocessing categorical; phân biệt RFECV13 và stable17; ghi limitations. | OPEN |
| G04 Prior art / contribution | C-M1 | Các bài L06/N02 đã nghiên cứu stacking và FS cho IDS, nên đóng góp hẹp tốt nhất là kiểm toán benchmark, sai số và chi phí theo frozen protocol. | Ma trận prior art/claim với locator và reading-scope status; tách method invention khỏi empirical case study. | OPEN |
| G05 Paired/stratified uncertainty | A-m2, B-m1, C-m2 | Row-level bootstrap/Wilson phân tích bất định trong benchmark, không phản ánh repeated train/session variation; CI chứa0 không chứng minh equivalence. | Giải thích bootstrap strata/joint prediction patterns, inference unit, Holm family và các điều không thể suy ra. | OPEN |
| G06 Prediction time | A-m4, B-m3 | ms/sample là batch average (pipeline predict_proba + threshold), không phải single-call online latency. | Ghi nhãn/footnote rõ trong companion và slide bảo vệ, cùng giới hạn môi trường gốc UNKNOWN. | OPEN |
| G07 Chronology of TEST | A-m1 | Có thể kiểm tra tính toàn vẹn file TEST sớm mà không dùng nhãn/metric TEST để tuning; bản mô tả tuyến tính cần làm rõ giai đoạn. | Timeline loại thao tác audit file với development/selection và frozen one-time holdout; kiểm khớp source trước khi đề xuất sửa. | OPEN |
| G08 Duplicates/overlap | A-m3 | Vector trùng trong và giữa các split đặt giới hạn cho đánh giá tính độc lập; không chứng minh leakage-free. | Lưu lại counts và conflict-group source, không xóa record theo nhãn hay tự tạo split mới sau TEST. | OPEN |
| G09 Attack-family uncertainty | B-m2 | Bảng gộp được hỗ trợ số học nhưng có thể che bớt support và Wilson bounds từng họ, nhất là họ hiếm. | Companion 9 family support/FN/miss-rate/Wilson with explicit binary task/no multiclass claim. | OPEN |

## Các phát biểu phải giữ nguyên trong lời bảo vệ

- Stacking42 vs RF42: **FP giảm 142, FN tăng 118** trên official holdout, không có khẳng định superiority/equivalence tổng thể từ paired Macro-F1/MCC CI chứa zero.
- **Feature-count trade-off không phải isolated causal FS ablation** vì RF17 khác RF42 cả hyperparameters.
- Original historical environment/bitwise identity UNKNOWN; P15 là `DONE_SCOPED_RECONSTRUCTION`, không sao chép máy gốc hoặc kiểm chứng lại accuracy trên official TEST.
- Nghiên cứu có kết quả nhị phân trên benchmark và failure analysis; không khẳng định detection real-time, zero-day, external deployment hoặc novel ensemble algorithm.
- Reviewer A/B/C là **AI simulated separately invoked** theo dispatch records, không human independent peer review hoặc institutional approval.

## Đề xuất tiến độ

1. QA độc lập `--phase reviews`, `--phase complete` trên workspace của tác giả có đủ 80 packet files. Đọc và sửa lỗi **validator riêng**, không đổi report reviewer đã freeze.
2. Đối chiếu 27 câu trả lời bảo vệ hiện có với G01–G09 và phản ánh phần nào chỉ có trong companion; không viết lời bao biện trái source.
3. Tạo companion exhibits riêng từ outputs frozen nếu source availability/rights rõ, chạy numeric/figure QA và lấy **sự đồng ý của tác giả** nếu muốn đưa vào PDF.
4. Cập nhật trạng thái concern với bằng chứng hoàn thành từng acceptance test; không tự đóng tất cả vì số unit tests PASS.
5. P20 final / G6 / public release vẫn riêng và đang OPEN.

**Không chạy thêm ML, bootstrap hoặc official TEST; không phát hành gói nội bộ công khai.**
