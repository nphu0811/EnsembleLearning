# P21 — nghiệm thu có giới hạn Feature Selection resource pilot (18/10/2026)

**QUYẾT ĐỊNH:** \`P21_SELECTOR17_FIT_ONLY_PILOT_DONE_SCOPED\` dựa trên tính nhất quán của báo cáo máy tác giả và kiểm thử chống giả mạo, **không phải kết quả học máy cho RQ2**. Các lượt thí nghiệm khoa học 5 seed × 5 cấu hình vẫn **chưa được phép chạy**.

## 1. Nguồn và nội dung commit

Tác giả push [commit b8820ed](https://github.com/nphu0811/EnsembleLearning/commit/b8820ed77fcde9040d59719cf8e10ece01b30e9b) lên \`main\` với **đúng ba** JSON:
- \`results/controlled_extensions/p21_train_only_pilot_selector17_01/start.json\`
- \`results/controlled_extensions/p21_train_only_pilot_selector17_01/run_report.json\`
- \`results/controlled_extensions/p21_train_only_pilot_selector17_01/worker/worker_result.json\`

Không có raw TRAIN/TEST CSV, joblib, row IDs, danh sách 17 đặc trưng pilot, \`resources.csv\` hay worker logs trong commit. File \`start.json\` có trạng thái \`INCOMPLETE/NOT_STARTED\` là snapshot trước khi chạy, hợp lệ; \`run_report.json\` sau cùng \`PASS_SELECTOR_RESOURCE_SMOKE_ONLY\`, \`exit_code=0\`, \`stop_reason=null\`.

## 2. Thông số được báo cáo từ Windows laptop

| Chỉ tiêu | Kết quả |
|---|---:|
| Dữ liệu được kiểm tra SHA | official TRAIN, 175341 hàng, SHA256 \`bec7dd5e...e0648fa\` |
| Fit pool / internal validation | 140272 / 35069; group split seed 20261018, validation fold0 |
| Pilot fit rows | 8000 (Normal=2555, Attack=5445) |
| Selector sample/seed | 4667 hàng chỉ từ pilot FIT |
| Phương pháp | Mutual Information + Spearman redundancy, LR L1, ExtraTrees |
| Seeds | 11,23,42,71,101 |
| Selector calls | 15 = 3 phương pháp × 5 seed |
| Đặc trưng gốc / được chọn | 42 / 17 |
| Số feature đạt >=2 phương pháp ổn định | 18 |
| Biến bổ sung do fallback | 0 |
| Thời gian selector | 15.531 giây |
| End-to-end | 57.547 giây |
| Peak process tree RSS | 381898752 byte ≈364.21 MiB, thấp hơn cap 2GiB |
| Minimum RAM available | 4684673024 byte ≈4.36 GiB, trên floor 1.5GiB |
| RAM available before start | 5016907776 byte ≈4.67 GiB |
| Disk before start | 31149944832 byte ≈29.01 GiB |
| Resource samples | 112, worker exit0, stop_reason=null, timeout 20 phút |
| Validation/Test hoặc scientific metrics | Cả ba loại đều được ghi \`false\` |

Theo worker JSON, \`no_validation_rows_used=true\`, \`validated_fit_index_exclusivity=true\`, \`group_disjoint=true\`; output không ghi các tên biến thí điểm. Những cờ này nhất quán với chốt mã nguồn nhưng **không phải kết quả quan sát OS độc lập trên laptop**.

## 3. Independent check trên bằng chứng đã push

- \`tools/p21_verify_selector_pilot_reports.py\` (read-only, Python stdlib) kiểm 15 mục: TRAIN SHA, protocol SHA (Windows CRLF/Git LF), start/run/worker JSON equality, budget, time, exact split, 15 selector calls, 17 predictor, seed, và cấm validation/TEST scoring.
- **15/15 kiểm tra độc lập trên metadata PASS**. \`tests/test_p21_selector_report_acceptance.py\` thêm 7 fixture tests: yêu cầu thay đổi model-result flags, timeout, RAM, feature counts, selector calls hoặc source identity phải bị phát hiện.
- [GitHub Actions 39068091845](https://github.com/nphu0811/EnsembleLearning/actions/runs/39068091845) **SUCCESS**, hai jobs \`protocol_only\` và \`synthetic_group_split\`: 37/37 standard-library tests (14 protocol +7 guards +5 RF report +4 selector safety +7 selector report), 7/7 synthetic ML tests (3 group +4 selectors), 29/29 frozen static checks. Trong CI không đọc official TRAIN/TEST, không tính metric từ data thật hoặc train model với data thật.
- Đợt giám sát địa phương \`resources.csv\` giữ trên laptop và không độc lập được duyệt từng mẫu; chấp nhận giới hạn này, không được gọi là reproducibility/external peer review.

## 4. Quyết định gate

**ĐÃ XONG:** bounded TRAIN-fit-only selector17 pilot (số liệu tài nguyên/khả thi). **CHƯA XONG:** Feature Selection \`60000 FIT / 35000 selection-samples\` trong thí nghiệm khoa học thực tế, matched RF17 vs RF42 trên validation nội bộ, RQ1 repeated refits, RQ5 weighting/resampling, Stack-Lite resource pilot.

**Next:** xây dựng riêng pilot RQ5 \`class_weight=None\` vs \`balanced\` vs FIT-only random oversampling cho RF42, không mở TEST, không tính/so sánh validation metrics ở pilot; đo thực tế thời gian/RSS dưới watchdog. Sau đó Stacking-Lite resource pilot riêng, và xin author approval cho thí nghiệm đầy đủ. Mọi thí nghiệm khoa học P21 đều là \`post-hoc TRAIN-derived internal validation\` và không thay thế kết quả official TEST lịch sử.

**Giữ nguyên:** bản PDF V2 47 trang, báo cáo P9, mô hình P15, RQ canon và các điều kiện phát hành/đóng P20.
