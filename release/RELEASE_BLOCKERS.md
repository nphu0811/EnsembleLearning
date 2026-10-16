# Release blockers ngày 16/10/2026

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
