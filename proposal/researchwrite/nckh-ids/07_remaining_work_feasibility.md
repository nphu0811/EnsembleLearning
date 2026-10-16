# Tách tiến độ đã thực hiện khỏi công việc còn lại

Hồ sơ đang được phục hồi từ nghiên cứu đã có kết quả. Không mô tả nó như một đề cương được lập/phê duyệt trước thí nghiệm. Nếu cơ sở yêu cầu đề cương hoàn toàn trước thực nghiệm, tính chấp nhận của hồ sơ phục hồi cần tác giả/GVHD xác nhận; AI không cấp phê duyệt hồi tố.

## Gate phần mềm và reproducibility riêng biệt

| Sản phẩm | Input và cách thực hiện | Nguồn lực biết được | Acceptance | Khi chưa đạt |
|---|---|---|---|---|
| A: hậu xử lý saved results | Aggregate metrics/cost, close_original_phase11.py, venv stdlib riêng | Python3.11.9 hiện có, không ML package/pip; replay đã chạy | Ba CSV khớp hash và test đạt; evidence clean_replay_report.json | Đánh fail/report mismatch; không sửa bảng frozen để khớp |
| B: tái dựng ML với cấu hình cố định | Cần đọc dependencies và hardcoded paths; chỉ dùng TRAIN để fit trong output/workspace cô lập; không candidate/threshold selection từ TEST | Original env UNKNOWN; hardware/RAM và thời gian hiện tại chưa được đánh giá; historical runtime không thay capacity estimate | Fresh ML env/lock, source/config/raw hashes, log thực thi, output cô lập, sai khác được giải thích; đánh giá cuối chỉ theo protocol đã khóa | Giữ G3/P15 PARTIAL; có source và report replay vẫn không thay training reproduction. Ghi blocker/budget trước job nặng |
| C: inference demo | Chỉ bắt đầu khi có serialized model hợp lệ, learned preprocessing/schema và môi trường tương thích | Model artifact hiện chưa có; budget UNKNOWN | Load model thật, schema validation, test valid/invalid CSV, output/probability semantics, runbook và smoke end-to-end | Demo BLOCKED dependency; có thể dùng evidence viewer cho review nhưng không gọi là inference hoặc đóng G6 |

B không hứa chắc sẽ thành công hoặc phục hồi bitwise mô hình lịch sử. Nếu không tìm được original artifact, mô hình dựng lại phải gắn nhãn reconstruction, tách provenance. Việc chạy cần tuân budget và scope hiện có; không tự mở lại model selection. Không xóa nghĩa vụ final demo chỉ vì phần phụ thuộc chưa đạt.

## Lịch theo form và trạng thái thực tế

| Chặng nguyên mẫu | Thời lượng giữ nguyên | Nội dung ánh xạ dự kiến | Trạng thái nghiên cứu thực tế |
|---|---|---|---|
| Xây dựng/duyệt đề cương |4 tuần | Hoàn thiện hồ sơ, RQ/evidence map, xác nhận hành chính | Đang phục hồi, chưa được duyệt; không tự gán lịch cũ |
| Chuyên đề1 |11 tuần | Dữ liệu/protocol/FS/baselines và kiểm toán | Có historical artifacts; phần giới hạn/reproducibility còn mở |
| Chuyên đề2 |11 tuần | Ensemble/đánh giá/error analysis và kiểm định | Có frozen results; không hứa rerun để tạo cải thiện |
| Báo cáo/tổng hợp |4 tuần | DOCX/LaTeX, figures, software/docs, defense/release QA | Chưa đầy đủ, cần runtime/model và nội dung được review |

Đây là ánh xạ nội dung vào form, không xác nhận nghiên cứu đã diễn ra theo lịch4/11/11/4 hoặc đặt ngày khởi đầu. Ngân sách/copies/chữ ký giữ pending. Nếu lịch hoặc nguồn lực không được xác nhận, giao bản review có nhãn thiếu mục; không READY_FOR_SUBMISSION.

## So sánh prior work gần nhất trong phạm vi đã đọc

| Study | Task/model/FS đã đọc | Split/đánh giá biết được | Unknown và hệ quả |
|---|---|---|---|
| L05 | AutoML soft voting, reduction/resampling | UNSW/CICIDS2017 theo preview | Chưa audit split/fit order; không claim nghiên cứu này thiếu fairness |
| L06 | GNB/LR/DT→SGD, Chi-square, binary/multiclass | Methods có random80/20 và CV meta inputs | Không matched official-split comparator; không lấy scores so ngang NCKH |
| L07 | Dynamic undersampling/boosting cho multiclass | Abstract/preview nêu hai benchmarks | Chưa full protocol; không so multiclass Macro-F1 với binary NCKH |
| NCKH | LR/DT/RF→LR;42/17 tracks | Published official split, frozen configs, conditional CI/error/cost | FS/meta không fully nested; no external/retraining stability; contribution local audit/trade-off |

Đối chiếu này chỉ xác định vị trí case study hiện tại so với các thành phần/phương pháp đã có; không chứng minh field-wide gap. Full source pointers và reading boundaries giữ tại literature/resume_r02_2026_10_16/READING_NOTES.md.
