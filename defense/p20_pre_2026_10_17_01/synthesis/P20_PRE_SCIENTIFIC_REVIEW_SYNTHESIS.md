# P20-PRE — Tổng hợp ba lượt phản biện AI từ hồ sơ đã khóa

**Phạm vi:** mô phỏng phản biện khoa học nội bộ. **KHÔNG** phải hội đồng giáo sư thật, editorial decision, xác nhận công bố, nghiệm thu hoặc P20 final.

**Evidence snapshot:** commit nguồn reviewer `b3acf2e2f8ad15bdf4b11bb9450927a57309d968`; common packet 80 file, SHA-256 manifest `c0f0b3828ba16ce8312b489915cc4c56c9fc7c771dbeefe1d7a9bb78938b62b7`. Reviewer reports A/B/C được đọc từ GitHub, giữ nguyên nội dung; freeze index `review_reports_frozen.json` ghi digest cho 6 file. Reviewer C đã có freeze trước token limit; A/B được **chụp hash sau push**, không suy diễn đã freeze đúng thời điểm trước khi Codex hết token. Lời khai về ba lần gọi child agent `fork_turns=none` có trong `EXECUTION_BOUNDARIES.md`; không có OS sandbox, human independence hoặc kiểm toán cách ly process từ xa.

## Kết quả 3 reviewer (bản gốc giữ nguyên)

| Reviewer | Trọng tâm | Major | Minor | Questions | Recommendation |
|---|---|---:|---:|---:|---|
| A | ML, feature selection, implementation, experiment design | 3 | 4 | 16 | `MAJOR_REVISION_REQUIRED` |
| B | Thống kê, IDS errors, inference scope | 2 | 3 | 16 | `MAJOR_REVISION_REQUIRED` |
| C | Novelty, literature, reproducibility, communication | 3 | 2 | 14 | `MAJOR_REVISION_REQUIRED` |
| **Tổng** | | **8** | **9** | **46** | Major revision đồng thuận ở mức recommendation |

`synthesis/concern_register.json` đối chiếu **17/17** concern IDs, không loại bỏ ý kiến bất lợi hoặc sửa report. Có **9 nhóm việc còn OPEN**, **5/9 nhóm được >=2 reviewer cùng nêu**. Các reviewer tự gắn `blocking=false` cho mọi concern; mức **MAJOR** ở đây đòi hỏi cải thiện chất lượng manuscript/truy vết, không tự chứng minh các điểm kết quả mô tả hiện tại sai số học. Không nâng bất đồng/giới hạn thành CRITICAL nếu chưa có bằng chứng.

## Ưu tiên sửa theo nhóm

**MAJOR / ưu tiên cho bản bảo vệ và revision được phê duyệt:**

- **G01 (A-M2, B-M2, C-M3; consensus 3/3).** Phần Methods/đóng góp nói tới OOF, diversity và voting bất lợi nhưng PDF chưa đưa đủ bảng định lượng development để người đọc kiểm chứng. Chỉ bổ sung từ saved development CSV, rõ ràng phân biệt development với official TEST; không chọn lại mô hình.
- **G02 (A-M3, B-M1, C-M2; consensus 3/3).** PDF vật lý khoảng trang 33/35 phản ánh thời điểm trước P15; hiện đã có 3 mô hình `RECONSTRUCTED_FULL_TRAIN` với QA trên laptop của tác giả. Cần companion có ngày, phân biệt original historical model UNKNOWN và bản tái dựng, không âm thầm thay câu trong PDF khóa.
- **G03 (A-M1, C-m1; consensus 2/3, mức gộp Major).** Trình bày lineage stable17, thresholds/stability seeds, exact feature order, xử lý categorical, nested limitations, và việc RF17 khác RF42 cả hyperparameters. Không phát biểu giảm feature count gây ra toàn bộ chênh lệch thời gian/score.
- **G04 (C-M1).** Định vị rõ đóng góp case study/benchmark audit cạnh L06/L12/N02 có protocol/reading-scope khác nhau; prior art đã có stacking+feature selection+IDS. Không tuyên bố thuật toán mới, SOTA hoặc novel research gap toàn lĩnh vực.

**MINOR / làm rõ bằng companion, không cần experiment mới cho claim hẹp:**

- **G05 (A-m2, B-m1, C-m2).** Mô tả stratified joint-pattern bootstrap, sampling unit, paired interval, McNemar/Holm family; CI chứa 0 không chứng minh equivalence, bootstrap rows không là repeated-training uncertainty.
- **G06 (A-m4, B-m3).** Định nghĩa lại `ms/mẫu` là trung bình batch toàn tập trong môi trường lịch sử, không phải latency từng yêu cầu hay benchmark deployment.
- **G07 (A-m1).** Làm rõ sequence audit TRAIN/TEST, lựa chọn config trên development và frozen evaluation một lần; đọc metadata/kiểm kê TEST không đồng nghĩa dùng TEST để tune.
- **G08 (A-m3).** Ghi chi tiết within-split duplicate/label conflicts và exact-vector TRAIN/TEST overlap, không biến điều đó thành chứng nhận leakage-free.
- **G09 (B-m2).** Companion đầy đủ 9 attack families, supports/FN và Wilson CIs; các nhóm hiếm không đáng được suy diễn hiệu quả ổn định, và đây là phân tích detector nhị phân, không multiclass.

## Điểm khoa học có thể bảo vệ ngay trong phạm vi đã chứng minh

Bản thảo có case study IDS nhị phân trên official UNSW-NB15, configs/threshold/frozen protocol, source-linked confusion counts, thống kê paired, FP/FN trade-off, subgroup và P15 scoped full-TRAIN reconstruction. Dữ liệu đánh giá đã khóa cho RF42 và Stacking42 cho thấy RF42 **10,003 FP / 734 FN**, Stacking **9,861 FP / 852 FN** (Normal support 37,000, Attack 45,332): Stacking giảm 142 FP nhưng tăng 118 FN. Hiệu số Stacking trừ RF42 khoảng **+0.000497 Macro-F1** và **−0.000413 MCC**; paired confidence intervals hai hiệu số chứa 0. Vì vậy không kết luận Stacking tốt hơn tổng thể hay tương đương; người triển khai còn phải cân chi phí bỏ sót attack và false alarm.

RF17 so với RF42 là **so sánh hai pipeline**, không tách tác động nhân quả của 17 features vì hyperparameter cũng khác. Feature selection ngoài outer CV và meta selection chưa fully nested; novel-vector subset thuộc cùng TEST chứ không phải external validation. Bootstrap trên benchmark rows không đo ổn định qua training repetitions. Đóng góp được hỗ trợ tốt hơn với cách gọi **empirical IDS benchmark/error-and-cost audit**, chưa phải thuật toán Ensemble mới hoặc field-wide novelty.

## Boundary & hồ sơ tiếp theo

Bộ 80 file `packet_02/local_contents/` được giữ cục bộ/Git-ignored. Mình không thể chạy lại Python validator đầy đủ đối với exact 80 copied packet bytes trên GitHub. Remote đã kiểm tra **85/85 evidence anchors** tìm đúng đoạn trong năm source files nền tảng; **chưa thể chứng nhận 100% mọi anchor**. Việc truy xuất PDF thật trong phiên reviewer đã được Codex mô tả; reviewer report không đồng nghĩa independent human evaluation hoặc human-level source verification.

`tools/p20_validate_pre_review.py` đã được sửa để chấp nhận recommendation là chuỗi (A) hoặc object (B/C), **không sửa báo cáo reviewer**. Muốn xác nhận đầy đủ packet evidence phải chạy local `--phase reviews` và `--phase complete` với unique outdirs và kiểm tra `failed=0`; không tự suy ra test này đã PASS chỉ vì JSON/report có mặt.

`defense/defense_questions.json` có 27 câu hỏi/câu trả lời dự thảo, `SLIDE_OUTLINE_12_MINUTES.md` có 13 slide/12 phút; `draft_validation.json` ghi 65 checks pass, 0 fail trong phạm vi evidence substrings. Đây chưa phải hoàn thành đối chiếu toàn bộ response với concern register và chưa tạo PPTX/diễn tập. Không cấp G6 hay final acceptance.

**Disposition hiện hành:** `P20_PRE_REVIEW_COMPLETED_WITH_OPEN_CONCERNS` ở cấp tổng hợp từ báo cáo đã lưu, **pending full local evidence-pointer QA**. **P20 final = DEFERRED, G0–G6 overall và final submission = OPEN**. Không chỉnh PDF 37 trang, reference bibliography, frozen results, model binaries hoặc quyền phân phối. Các vấn đề G01–G09 nên được chuyển thành một companion response matrix để tác giả duyệt trước khi tích hợp vào manuscript; mọi thí nghiệm mới yêu cầu protocol mới chấp thuận, không dùng lại official TEST để retune.

## Các lệnh kiểm thử trên laptop (không fit)

```powershell
git pull --ff-only origin main
python -X utf8 tools/p20_validate_pre_review.py --phase reviews --out-dir defense/p20_pre_2026_10_17_01/qa_reviews_01
python -X utf8 tools/p20_validate_pre_review.py --phase complete --out-dir defense/p20_pre_2026_10_17_01/qa_complete_01
```

**Không chạy `--phase complete` cho đến khi `reviews` PASS**, và không tái sử dụng output dir đã tồn tại. Hai lệnh là hướng dẫn cần chạy, không phải chứng nhận đã chạy trong phiên này.
