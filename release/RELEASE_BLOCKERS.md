# Release blockers ngày 16/10/2026

## P17 — Thông tin MỚI NHẤT: báo cáo năm chương (16/10/2026)

- Bản PDF hiện hành có **5 chương, 37 trang A4**, bỏ Tóm tắt, Danh mục từ viết tắt nằm sau Mục lục. Bản 8 chương/40 trang dưới đây là **đã thay thế**, chỉ còn giá trị lịch sử QA.
- [P17 five-chapter build run](https://github.com/nphu0811/EnsembleLearning/actions/runs/38916942038): XeLaTeX/BibTeX PASS, không trùng nhãn, không glyph thiếu/Overfull; bảng chỉ số/12 trích dẫn tiếp tục hiện diện.
- Bản PDF không in đường dẫn nội bộ tới `.md`, `.json`, `notebook/` hoặc `results/`. Nội dung tập trung vào lý thuyết, xử lý dữ liệu, huấn luyện, kết quả và thảo luận. Chi tiết tại `docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md`.
- **Chữ ký thật, chấp thuận biểu mẫu của cơ sở đào tạo, kiểm định trích dẫn/toàn văn học thuật và các release gates khác vẫn mở.** Không suy ra PASS của phần mềm quét tương đồng từ việc PDF build thành công.


## Cập nhật P17 báo cáo 40 trang theo mẫu tham khảo (mới nhất)

- **G4 báo cáo kỹ thuật**: XeLaTeX/BibTeX 40 trang A4 PASS (CI `38907313697`), 7 hình/10 bảng/12 bibliography; không có Overfull hay thiếu glyph; đã xem PDF thật. Có logo PTIT, khung bìa, màu mục lục/biểu đồ và đầu/chân trang dựa trên mẫu người dùng cung cấp. Bài tham khảo chỉ dùng về hình thức, không chép kết quả hoặc danh tính.
- **G5 quản trị** vẫn OPEN: đơn vị/lớp/tên người thực hiện/MSSV/GVHD/mã đề tài/chữ ký và xác nhận form chuẩn còn thiếu. P17 tổng thể PARTIAL; không tự tuyên bố đã nộp/được trường duyệt.
- G0–G3, G6, original-training provenance và release rights không thay đổi. Xem `report/P17_PTIT_40PAGE_QA_2026-10-16.md`.


## Cập nhật P17 CI/PDF — 16/10/2026 (ưu tiên hiện hành)

- **G4 technical PDF build/render: PASS trong phạm vi kỹ thuật**, không còn BUILD_BLOCKED trên máy: GitHub Actions run 38901027329 thành công, XeLaTeX + BibTeX; 22 trang A4, 12 bibliography items, 2 vector figures, 5 results tables; sau sửa 0 Overfull, 0 missing glyph, 0 text boundary outliers. Biên bản `report/P17_PDF_QA_2026-10-16.md`; CI mới block regression. Không gọi G4 final/approved vì bibliography L03 và mẫu chuẩn trường còn treo.
- **G5 vẫn AUTHOR_INPUT_NEEDED** (tên SV/GVHD/trường/đơn vị/ngày/ký/xác nhận form). G0–G3/G6 không tự đóng. Chưa release chính thức, không thay mô hình/test.
- Dòng `G4 BLOCKED` trong bảng lịch sử dưới đây chỉ mô tả **trước build 16/10**; trạng thái hiện hành là scoped technical pass + final P17 partial. Không sửa lại audit cũ.


## Cập nhật r05 — 16/10/2026, ưu tiên hiện hành

- Independent full argument/form content review đã hoàn tất; ARG-R05-01–05 addressed trong bản r05 và recheck riêng. Không còn blocker usage limit cho review này; không thay G4/G5 bằng reviewer judgment.
- ARG-R05-00A/B vẫn OPEN: xác nhận tác giả/đơn vị và actual filled/rendered DOCX/PDF; P18L03/U01/U03 và report build/render còn thiếu.
- G3 PARTIAL: fullTRAIN reconstruction plan-only NO_GO, khoảng1,48GiB RAM trống tại snapshot, chưa watchdog/runner; không training mới hoặc final demo.
- Public sharing clearance PARTIAL: tracked/archive triage đọc633files/1165textunits; paths/email/template identity fields cần rà soát. Không xóa/untrack/history rewrite. Xem docs/PUBLIC_SURFACE_AUDIT_R05.md.
- G0–G6 vẫn mở, NOT_READY_FOR_SUBMISSION; không FINAL_NCKH.zip.

## Cập nhật r04 — ưu tiên hiện hành

- G0/G1/G2 vẫn PARTIAL; giữ FS ngoài development folds, meta tuning chưa fully nested, overlap và giới hạn RQ4/RQ5. Không thay khoa học bằng reviewer score.
- G3 PARTIAL: fresh venv software smoke trên TRAIN đạt45/45 sau chẩn đoán/sửa assertion; có3model SMOKE_ONLY. Chưa fullTRAIN reconstruction/originalenv/finalmodel hoặcfinalinference. Initialfail41/42 giữriêng.
- G4: legacy metadata11/12verified;L03pageconflict vàU01/U03open. Tổngquan/gapdraft cóscopedreviews;fullproposalargumentreview bịusage limit,reportIDSbuild/render chưađạt.
- G5: góiMD theoform/coverage58blocks97cells có,khôngfilled/renderedDOCX/PDF;danh tính/chữký/tínhápdụng đơnvị,lịch,ngânsách,copies vẫnchờxácnhận.
- G6 NOT_READY:Q&A20,script/runbook/checklisttext có;chưaPPTX/PDF/render/rehearsal/finaldemo. Source/timingchecks khôngthayreadiness.

Current evidence: docs/RESUME_AUDIT_R04_2026-10-16.md và.research_memory/r04/. Cácbảngbêndưới làlịch sửtrước cậpnhật,khôngdùngcounts bibliography/modelsmokecũ đểresume. KhôngFINAL_NCKH.zip.

Trạng thái tổng thể **NOT_READY_FOR_SUBMISSION**. Không tạo FINAL_NCKH.zip.

| Gate | Trạng thái | Critical gap / điều kiện đóng |
|---|---|---|
| G0 Research validity | PARTIAL | RQ/claim map phải phản ánh RQ4 partial, RQ5 thiếu controlled resampling; không novelty/superiority vượt evidence; literature cần kiểm chứng |
| G1 Data safety | PARTIAL | Hash/protocol PASS; FS ngoài development folds và overlap đã được ghi nhận. Không cấp chứng nhận leakage-free |
| G2 Fairness | PARTIAL | Có frozen comparison; không repeated training/full factorial; giữ giới hạn và negative findings |
| G3 Reproducibility | PARTIAL | Clean aggregate replay PASS; original env, clean ML training replay, model artifact còn thiếu |
| G4 Writing | BLOCKED cho bản cuối | Chưa report IDS buildable/rendered; refs chưa verified toàn bộ |
| G5 Administrative | AUTHOR_INPUT_NEEDED | Danh tính, GVHD, ngày, chữ ký, tính áp dụng ngân sách/lịch/copies; chưa DOCX/PDF điền mẫu đạt QA |
| G6 Defense | NOT_READY | Đã có20 câu Q&A dạng draft với evidence/path QA; còn thiếu slides, script, live inference demo, rehearsal và checksum final inventory |

Tool gaps: không thấy dependency loader artifact trong tools hiện tại; không TeX/LibreOffice trên PATH. Tiếp tục Markdown/source-data/figures/kiểm chứng nguồn độc lập; không dùng tool gap làm lý do xin phép chuyển phase.
