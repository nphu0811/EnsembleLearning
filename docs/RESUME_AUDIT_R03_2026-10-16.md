# Resume audit r03 — 16/10/2026

Đã đọc toàn bộ MASTER_PROMPT.md, AGENTS.md và STATE/HANDOFF/TASK_BOARD/CANON/DECISIONS trước thay đổi. Không restart phase, fit/predict, truy cập test để chọn model hoặc sửa raw/frozen evidence.

Machine audit trước sửa: `results/reproducibility/resume_2026_10_16_r03/resume_audit.json`; command `python tools/resume_checkpoint_audit.py --out-dir results/reproducibility/resume_2026_10_16_r03`.

- 148 prior artifacts:146 hash khớp;2 lệch là HANDOFF.md và SKILL_USAGE_LOG.md. Đuôi hai file chứa checkpoint xuất DOCX/runtime recheck sau r02; checkpoint đó cũng đã ghi stale HANDOFF hash. Không có mismatch artifact khoa học trong manifest. Không gọi148/148 PASS ở thời điểm vào phiên. Snapshot audit giữ expected/actual, không xóa sai khác bằng cách sửa audit.
- 282/282 historical research files trong preservation manifest khớp. Reuse các experiment có evidence trong giới hạn canon; không suy mọi phase đã DONE.
- ZIP nguyên bản CRC PASS,15 file và extraction đều khớp, không DOCX. DOCX riêng CRC PASS, OOXML **8 top-level tables,8 total tables**. Handoff/matrix cũ nói9 là lỗi đếm/ghi chép; sửa current matrix và bổ sung đính chính, giữ audit lịch sử. Chưa visual QA.
- Registry filesystem:20 Nature SKILL.md, alias researchwrite trong nature-proposal-writer; hashes ở machine audit. Đã đọc nature-ref-verifier SKILL+manifest+common-patterns và thực hiện field crosschecks. researchwrite được đọc với references phù hợp trước bổ sung partial sections; không ghi các skill chỉ đọc router là đã thực thi.
- Python3.11.9; không xelatex/lualatex/tectonic/LibreOffice trên PATH. Tool registry lượt này không có load_workspace_dependencies. Không thay tình trạng tool bằng suy đoán từ lần trước.
- `python -m unittest discover -s tests -v`:6/6 PASS. Đây là test audit provenance/protocol, không phải training reproduction. Lệnh đọc OOXML ban đầu lỗi stdout cp1252; đã sửa bằng stdout UTF-8 và đọc thành công, không tác động DOCX.

## Task thực hiện

P18: field crosschecks8 legacy entries;2 mới đạt VERIFIED_METADATA (L04/L11),4 verified trước được giữ. Current subset6;6 legacy entries và dataset U01/U03 còn pending. Source captures, raw fetch results, report và18/18 bookkeeping checks tại `literature/resume_r03_2026_10_16/`. Chỉ có selected reading L02, không full-paper hoặc systematic-review completion.

Proposal: bổ sung mục nhu cầu/ứng dụng, sản phẩm/chất lượng, tiến độ/kinh phí ở partial draft riêng theo form; evidence/provenance và QA riêng. Không sửa RQ hoặc hứa model/demo đã có. Không merge thành full proposal, không DOCX/PDF export hay phê duyệt GVHD.

## Quality gates và resume

P15 PARTIAL; P01/P18 PARTIAL; proposal INTERNAL_DRAFT; release NOT_READY_FOR_SUBMISSION. Nguồn lực model reconstruction, original environment, serialized model, render runtime, full report/references, slides/demo và xác nhận hành chính vẫn mở. Xem HANDOFF hiện hành để tiếp tục; audit r01/r02 giữ nguyên.
