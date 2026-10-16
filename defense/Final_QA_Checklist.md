# Final QA r04 — chưa đạt release

Đây là checklist trạng thái, không phải chứng nhận hoặc chữ ký.

| Gate | Evidence có | Chưa đạt / việc phải kiểm |
|---|---|---|
|G0 Validity|Frozen RQ/canon; gap và tổng quan có scoped review|Review lập luận toàn đề cương bị ngắt; full manuscript còn thiếu; RQ4/RQ5 partial|
|G1 Data|282 historical hashes nguyên; provenance/protocol tests|FS ngoài development folds và overlap là known limits; không fully leakage-free|
|G2 Fairness|Frozen comparisons, negative findings, conditional CI|Chưa repeated training/full factorial; không causal FS hoặc resampling effect|
|G3 Reproducibility|Aggregate 3 CSV replay; fresh venv TRAIN smoke 45/45|Chưa full TRAIN reconstruction, original env hoặc final model/demo|
|G4 Writing|11/12 legacy metadata; source map, sections và bản ghép|L03 page conflict, U01/U03; full report, build/render và final citations còn thiếu|
|G5 Administrative|DOCX gốc 58 blocks/97 cells được audit|Chưa filled/rendered DOCX/PDF; danh tính, chữ ký, lịch, ngân sách, đơn vị và copies cần xác nhận|
|G6 Defense|Q&A 20 câu; kịch bản/runbook nội dung r04|Chưa PPTX/PDF, render, rehearsal, final inference, final inventory/ZIP|

Không đóng FINAL_NCKH.zip khi critical gates chưa đạt. QA hình thức phải xem từng trang DOCX/PDF/slide: Unicode, overflow, citations/cross-references, số hình/bảng và độ rõ. Source-presence checks không thay visual QA. Release chỉ chứa artifact được phép chia sẻ, có checksums và truy vết. Không tự điền giả thông tin hành chính hoặc chữ ký.
