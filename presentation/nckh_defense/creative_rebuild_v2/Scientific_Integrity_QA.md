# Scientific Integrity QA

PHASE 1: PASS. Humanizer3.1.0 được áp dụng như hướng dẫn biên tập, không phải công cụ xác định tác giả AI/người.

38 đoạn diễn đạt đã sửa trong bản nguồn riêng. Kiểm tra13file nội dung giữ nguyên chuỗi số; toàn bộ bảng/hình/công thức inline và display; lệnh cite/ref/label/texttt;3fileBibTeX byte-identical;6hình giữ nguyên hash. Đường dẫn hình được đóng gói lại, không sửa hình. Phần bìa/cam đoan/cảm ơn và RQ gốc giữ nguyên.

Biên dịch thực tế bằng XeLaTeX rồi BibTeX rồi2lượtXeLaTeX. Không thiếu glyph, citation/reference hay overfullbox tronglog cuối. Tất cả49trang được render, kiểm tra wordbounds và xem qua3contactsheet; mở riêng trang12/26/39/40/42/46. Không ghi việc này thành kiểm chứng khoa học độc lập hoặc người biên tập là giảng viên.

V6 SHA-256: 40b35c9a5c7f228ee91bbba94cfb0ccd701d52dd707a6f5b184171412ce6afc3
V7 SHA-256: 3579e41be58d24aee3807e000ffe6d762ebb857f1c588c1f0c503ef6f29cee0e

Không fit mô hình, không mở rawTEST, không thay confusionmatrix, metrics, protocol hay ranhgiớiP9/P15/P21. Các câu thiếu mốc lịch sử trong tổng quan được ghi riêng ở Scientific_Audit_Findings.md; chưa âm thầm sửa nội dung khoa học bằng thao tác ngôn ngữ.

Bằng chứng máy đọc: audit/scientific_source_invariants.json, audit/report_v7_qa.json, audit/report_build_1.log…4.log.
