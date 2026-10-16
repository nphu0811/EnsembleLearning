# R05 — reconciliation, verification và disposition

PLAN: `docs/R05_TASK_CONTRACT.md` và `revision_briefs/r05_assembly_brief.md`. EXECUTE: independent AI argument review ở context riêng, không đọc evidence review cũ; report được đóng băng trước bản r05. Tác giả sửa ở bản riêng qua `tools/r05_revise_proposal.py`, bảo toàn r04. VERIFY/REPAIR: source/citation/frozen-boundary checks và semantic recheck độc lập được lưu riêng.

| Finding | Kết quả |
|---|---|
| ARG-R05-01 | ADDRESSED_SCOPED: năm RQ nguyên văn từ frozen design, bảng thao tác/outputs/limits, O1–O4 trong nội dung |
| ARG-R05-02 | ADDRESSED_PLAN_ONLY: dependency, vai trò chưa giao, nguồn lực/gate/stop actions; không khẳng định khả thi thực thi hoặc đủ budget |
| ARG-R05-03 | ADDRESSED_SCOPED: aggregate replay và TRAIN smoke phân biệt fullTRAIN/final model/demo; defense text drafts ghi đúng |
| ARG-R05-04 | ADDRESSED_SCOPED: current r04 metadata, historical reading/Q&A provenance có nhãn |
| ARG-R05-05 | ADDRESSED_SCOPED: glossary; pr_auc nói rõ average precision theo source, không đổi số liệu |
| ARG-R05-00A | OPEN: tác giả/GVHD/đơn vị, danh tính/lịch/kinh phí/copies/chữ ký và chấp nhận hồ sơ phục hồi |
| ARG-R05-00B | OPEN: filled DOCX/PDF và render/page QA chưa có |

Independent recheck `r05_assembled_argument_recheck.md` không tìm thêm lỗi nội dung material, chấp nhận các sửa đổi trong phạm vi internal content/author input. Không phải người phản biện con người, approval, full proposal PASS hoặc P20. Evidence review r04 và argument review r05 khác phạm vi, không có xung đột để che hoặc bỏ finding.

Validation thực: `python tools/r05_validate_proposal.py --out proposal/researchwrite/nckh-ids/qa_logs/r05_validation_repaired.json` →34/34 PASS. Các kiểm cơ học không thay semantic recheck, full-text review, render hoặc training. Không chạy lại smoke hoặc mở official TEST CSV. Input hashes cho kế hoạch reconstruction đối chiếu thực tế khớp.

Giữ failure logs thật: lần chạy script sửa đầu tiên dừng vì parser bắt thêm hàng header RQ, chưa ghi draft; sửa regex chỉ nhận RQ1–5. Initial validator33/34, không resolve qualifier “Proposed model” và các ký hiệu convention Lxx/Dxx/Nx/Sx; sửa parser tách qualifier/ghi convention placeholders riêng, không nới tập citation được phép. `r05_validation_initial.json` giữ nguyên. Một lệnh PowerShell capacity dùng nhầm tham số ConvertTo-Json đã thất bại; lệnh Select/custom-object sau đó tạo snapshot thật. Không lỗi nào là kết quả nghiên cứu hoặc lý do sửa frozen outputs.

Manual Vietnamese prose/source check giữ nguyên câu phủ định superiority/novelty, binary/FP-FN trade-off, chronology, FS/meta-selection optimism, RQ4/RQ5 còn thiếu. Không chạy anti-slop cho tiếng Anh/Trung rồi nhận đã kiểm tiếng Việt. Không gán reviewer score. **R05-ASSEMBLY-REVIEW DONE_SCOPED**, proposal/form/release vẫn PARTIAL và NOT_READY_FOR_SUBMISSION.
