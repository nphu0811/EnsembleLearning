# R04 — independent citation and evidence-calibration review

Ngày 16/10/2026. Phạm vi chỉ gồm `drafts/sections/tong_quan_luan_cu_r04.md` và `literature/resume_r04_2026_10_16/GAP_MATRIX_R04.md`. Đây là review nội bộ bằng AI về literature/evidence, không phải P20, review toàn đề cương, xác nhận của GVHD hoặc release gate. Không thực hiện web search mới, training, prediction hay sửa frozen results.

## Cách đọc và nguồn đối chiếu

Đã đọc installed `C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md` (frontmatter `researchwrite`), `references/evaluation-rubric.md` và `references/research-anti-slop.md`. Rubric vốn dành cho proposal tiến sĩ materials/chemistry được adapt cho **một phần tổng quan NCKH sinh viên IDS**: feasibility là mức cụ thể của phép đối chiếu/giới hạn, novelty là positioning có căn cứ, không đòi phát minh thuật toán. Đã đọc foundation00–07 và `qa_logs/foundation_review_r02.md`; giữ nguyên nền đã PASS_SCOPED, không mở lại RQ hoặc biến known outcomes thành hypotheses tiên nghiệm.

Đối chiếu nội dung với r04 `SCOPED_READING_NOTES.md`, `source_claim_map.csv`, `FIELD_VERIFICATION_REPORT.md`, `legacy_verification_ledger.csv`, selected saved capture passages; cùng `resume_r02_2026_10_16/READING_NOTES.md` và r03 publisher-indexed L04 capture. Đây là kiểm tra tính khớp của những đoạn đã lưu, không chứng nhận toàn paper hoặc tính xác thực độc lập của mọi phần corpus.

## Findings theo mức độ

**P0: không phát hiện trong phạm vi đọc. P1: không phát hiện trong phạm vi đọc.** Không thấy bịa kết quả paper, nhận novelty toàn lĩnh vực, so trực tiếp scores khác protocol hoặc xóa tình trạng partial của RQ4/RQ5/G3.

**P2 — GAP_MATRIX_R04.md:10,14 — tăng tính tự chứa cho nguồn L03 đang còn conflict.** Hai hàng dùng author documentation để nói có labeling/experiment code; câu này được `reading_capture_2.json`, Tools & Documentation lines2–6 hỗ trợ. Page conflict của conference paper không phủ định nội dung trang công cụ. Tuy nhiên hàng G3 chỉ ghi L03 mà không nhắc lại warning; nếu trích riêng hàng đó, người đọc có thể hiểu nhầm đây là một citation paper đã fully verified. Thêm trực tiếp URL/locator `Tools & Documentation, Paper Code repository`, R04C03 và nhãn “documentation claim only; paper pagination unresolved” vào hàng G3 hoặc footnote chung cho cả hai hàng. Đây là sửa provenance, không yêu cầu bỏ bằng chứng hợp lệ hoặc đóng conflict bằng suy đoán.

**P2 — tong_quan_luan_cu_r04.md:3,15,19,29,33,35–36 và matrix:3,7–14 — vệ sinh chữ/số và định nghĩa thuật ngữ trước ghép DOCX.** Có các cụm dính như `mục33–38`, `năm2025`, `ngẫu nhiên80/20`, `đến2026`, `metadata11/12`, nhiều thuật ngữ English chưa giải nghĩa trong phần này. Chúng không đổi nội dung khoa học nhưng giảm khả năng đọc. Thêm khoảng trắng, dùng “bộ học ở tầng kết hợp” hoặc định nghĩa meta learner/OOF ở lần xuất hiện đầu trong đề cương đã ghép. Citation IDs hiện là nhãn nội bộ được khai báo rõ; phải resolve theo bibliography cuối khi xuất, không xem chúng là số reference hoàn chỉnh.

## Evidence và uncertainty đã được phân biệt đúng

| Nội dung kiểm | Bằng chứng hiện có | Điều chưa được xác nhận / giới hạn |
|---|---|---|
| L01, draft:7 | r04 web_capture_3 chứa indexed abstract về lựa chọn base classifier và combiner | Không suy nội dung toàn mapping study; không dùng số lượng bài hoặc empirical scores |
| L04, draft:19 | r03 web_capture_6 publisher-indexed abstract nói kết hợp feature sets bằng union/quorum | Phân biệt ensemble FS với ensemble classifier là đúng; chưa audit fit/split order |
| L06, draft:19 | reading_capture_3 Proposed model lines94–98: GNB/DT/LR, SGD, random80/20, CV predictions | Không chứng nhận tất cả transforms nested; không dùng accuracy của bài làm matched baseline |
| L05/L07/L08/L11/L12, draft:19–21 | Reading notes r02 và ledger ghi abstract/preview hoặc selected indexed Methods | Chỉ nhận thành phần/phương pháp đã có; không nhập efficacy, causal FS effect hoặc full protocol audit |
| L02/L09, draft:23 | L02 indexed selected audit passages; L09 reading_capture_1 Introduction tr.144490 phân biệt nguồn train/test | Không chuyển lỗi CIC sang UNSW; không coi novel-vector subset là external/temporal test |
| D01, draft:13 | reading_capture_4 official announcement lines25–31 nêu người, đề tài, lịch | Không phải bằng chứng đã bảo vệ thành công hoặc hiệu năng luận án |
| D02, draft:15 | reading_capture_4 cover2025 và objectives PDF3 lines56–57 có soft voting/stacking | Mục tiêu không phải kết quả đã chứng minh; chưa đọc toàn 27 trang/full thesis |
| L03, matrix:10,14 | Author documentation công khai code, R04C03 | Pagination254–262/254–263 chưa giải; không được đưa vào fully-verified final bibliography |

Số 11/12 là trạng thái metadata trong ledger, không phải 11 full-paper readings. Draft:29 nói rõ điều này. Cụm “gap” trong matrix được định nghĩa là khoảng thiếu bằng chứng của case study, không phải tuyên bố toàn lĩnh vực chưa có nghiên cứu tương tự. Draft:27 giữ FS/meta nesting limitations, RQ4/RQ5 và thiếu train replay. Không thấy nâng recommendation thành finding hoặc dùng reviewer score làm chứng nhận.

## Điểm chủ quan theo tám chiều

Các điểm sau chỉ là judgment hỗ trợ sửa văn bản; không phải metric nghiên cứu, independent experimental validation hoặc hoàn thành phase. Mỗi chiều chấm độc lập cho partial section, không dùng để chấm toàn proposal.

| Chiều adapt | Điểm /10 | Căn cứ trong phần được review |
|---|---:|---|
| Rõ vấn đề |8.0| Câu hỏi local benchmark và boundary nêu tại draft:9,27; RQ nguyên văn nằm ở foundation06 |
| Known → unknown → hệ quả |8.0| Matrix tách prior components, thiếu bằng chứng và kết luận được phép; không tạo field-wide gap |
| Khớp evidence |8.5| Source type và reading depth được ghi; còn P2 provenance L03 khi tách hàng |
| Chuỗi lập luận |8.0| Prior methods dẫn tới bounded local comparison, liên kết N1–N3 và RQs |
| Khả thi/kiểm được của phép đối chiếu |7.0| Locator và source map có; retraining/model/env còn mở đúng như foundation, chưa kiểm full protocol papers |
| Đóng góp/positioning |7.5| Case study trade-off/audit cụ thể; chưa đủ corpus cập nhật để chứng minh novelty rộng |
| Ranh giới rủi ro |8.5| Không false first claim, superiority, causal FS, external validation hoặc bảo vệ thành công |
| Ngôn ngữ |7.0| Tránh cường điệu và danh sách paper vô luận cứ; còn chữ/số dính và nhiều thuật ngữ chưa giải |

Trung bình chủ quan: **7.8125/10**. Recommendation: **KEEP_SCOPED_DRAFT / có thể gửi GVHD xem riêng phần này sau sửa P2**. Không phải READY_FOR_SUBMISSION, không đóng P01/P18/P20 hoặc G0–G6. Không cần đổi scientific tension/RQ hay chạy lại thực nghiệm để sửa những findings trên.

## Một sửa chữa có hệ quả lớn nhất

Làm rõ trong chính hàng G3 của gap matrix rằng nguồn L03 là **trang documentation của tác giả**, đưa URL/locator/R04C03 và giữ cảnh báo pagination paper. Sau sửa, kiểm lại rằng câu “authors publish labeling/experiment code” vẫn được phép, trong khi metadata L03 vẫn CHECK_SUGGESTED và vắng khỏi verified bibliography. Sửa này ngăn nhầm citation status khi gap matrix được tách ra dùng trong báo cáo/hỏi đáp. Không tự nâng điểm sau sửa nếu chưa recheck.
