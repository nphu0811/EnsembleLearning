# Public surface triage r05

Ngày 16/10/2026. Scope là nội dung Git đang track tại entry commit `c4ed771815675ace26f4df574a691fc67ed00179`, không xác nhận toàn bộ lịch sử remote hoặc từng lần tải xuống. `git ls-remote origin HEAD` khớp local. Không push, xóa, untrack hay sửa archive.

Lệnh thực: `python tools/r05_public_surface_audit.py --out results/reproducibility/resume_2026_10_16_r05/public_surface_audit.json`.

633 tracked files; 1.165 text units đã đọc, bao gồm nội dung archive lồng nhau. Report JSON lưu path, dòng, category và SHA-256, không chép matched values. Không có entry bị bỏ qua theo danh sách `skipped`; tệp nhị phân không phải ZIP không được OCR hoặc scan nội dung.

| Nhóm finding | Text units có hit | Diễn giải / đề xuất |
|---|---:|---|
| Local user paths | 79 | Có cả `NCKH_SHARE_FOR_REVIEW` archives, inventory/environment/provenance, handoff và skill logs. Đề xuất bản chia sẻ mới dùng đường dẫn tương đối hoặc ký hiệu workspace; không sửa bằng chứng gốc. |
| Email candidates | 14 | Gồm source captures của literature và diagnostics. Cần phân loại địa chỉ công khai của nguồn so với thông tin tài khoản; pattern không xác nhận là dữ liệu riêng. |
| Template identity fields | 27 | Có tên/chức danh/ô ký trong DOCX và LaTeX mẫu, bản snapshot và archive. Đây không phải danh tính tác giả đã xác thực. Bản điền mới chỉ dùng thông tin được xác nhận; bảo toàn nguyên mẫu. |
| Private key headers | 0 | Không có hit theo regex đã chạy. Không bao quát mọi định dạng bí mật. |
| Credential candidates | 0 | Không có hit với các mẫu OpenAI/GitHub/AWS đã liệt kê trong script. Không phải secret scanning toàn diện. |

Các path và dòng cụ thể nằm trong JSON, kể cả `NCKH_SHARE_FOR_REVIEW/NCKH_CODE_DOCS.zip::...`, `NCKH_RESULTS.zip::...` và `templates/original/...::word/document.xml`. FULL_INVENTORY/MANIFEST/EXCLUDED_FILES và mọi text tracked cũng được đọc trong lượt scan; không suy một tệp không có hit là đã được duyệt chia sẻ.

Acceptance của task read-only đạt khi report tồn tại, counts khớp, archives được đọc và không có mutation. Release privacy clearance vẫn **PARTIAL**. Cleanup đề xuất là tạo bản phân phối đã rà soát riêng sau khi tác giả quyết định phạm vi công khai; không xóa dữ liệu track chỉ dựa `.gitignore`, không rewrite Git history. Chưa thực thi cleanup hoặc thu hồi nội dung đã public.
