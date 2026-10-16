# Kiểm tra lại blocker DOCX ngày 16/10/2026

Phạm vi: chỉ xuất DOCX. Không sửa bản thảo, roadmap, số liệu, kết quả hoặc protocol. Không tạo DOCX và không chạy render khi các điều kiện runtime còn thiếu.

## Bằng chứng trong phiên hiện tại

- Đã đọc MASTER_PROMPT.md và sáu file memory bắt buộc. Manifest STATE: 147/148 SHA-256 khớp; HANDOFF.md có checkpoint xuất DOCX đã thêm sau manifest, được ghi nhận thay vì coi mọi hash đều đạt.
- Registry callable được lưu đầy đủ tại tool_inventory_recheck.json. Không có load_workspace_dependencies, tool search để expose loader, hoặc resolver tương đương. Có node_repl/js và js_add_node_module_dir; mô tả chỉ cung cấp Node REPL và nhận package path, không resolve managed Node/Python/native binaries.
- MCP resource templates trả về danh sách trống; resource catalog không cung cấp runtime/dependency skill. Skill roots và plugin cache được kiểm tra: không thấy runtime skill chính thức cung cấp resolver. Không suy đoán tên tool hoặc gọi tool không có schema.
- documents@openai-primary-runtime enabled=true trong config.toml. Plugin manifest phiên bản 26.1013.11914 khai báo skills, không khai báo MCP bootstrap/resolver. Catalog search documents và runtime workspace dependencies không trả về plugin giải quyết loader; không cài plugin không liên quan.
- runtime.json xác nhận Windows x64, Node v24.19.0, Python 3.12.14, bundledSkills=[], libreOfficeVersion=null. Executable Node/Python và package docx tồn tại trên đĩa. Không dùng các path tự tìm để bỏ qua bước resolver.
- Không có biến môi trường RUNTIME_* hoặc CODEX_PRIMARY_RUNTIME_* trong phiên shell. Không tìm thấy soffice.exe trong dependencies. Có Poppler, nhưng không có bước DOCX sang PDF được Documents chấp nhận.
- Đã đọc Documents SKILL.md, tasks/verify_render.md và Plugin Management SKILL.md. Không sửa skills, cấu hình hoặc cài thư viện toàn cục. Không chạy marker authoring vì chưa authoring.

## Kết luận và sửa ở phía host

Thiếu hai thành phần: (1) workspace dependency loader callable hoặc runtime skill chính thức trả về Node/Python, package directory, native binary paths; (2) bundled LibreOffice do resolver resolve, hoặc workflow Windows chính thức tương thích hợp đồng Documents. Runtime đã cài và Documents đã bật; chưa đủ bằng chứng phân biệt nguyên nhân nội bộ tool exposure với host runtime initialization. Không khẳng định plugin bị tắt hoặc runtime chưa cài.

Nhờ quản trị/hỗ trợ Codex kiểm tra tích hợp primary runtime và expose resolver thật, đồng thời cung cấp bundle render DOCX được hỗ trợ. Gửi runtime.json, tool_inventory_recheck.json và recheck_validation.json. Sau khi host được sửa, refresh/mở phiên và xác minh registry; không cam kết mở phiên mới tự sửa được lỗi. Không thêm endpoint đoán, sửa SKILL.md hoặc dùng desktop LibreOffice thay bundle.

Khi đủ hai điều kiện, đọc hướng dẫn tạo theo mẫu, dùng paths resolver trả về, chạy marker đúng một lần trước authoring, tạo bản làm việc, render bằng render_docx.py và xem mọi trang PNG trước khi giao.

## Bảo toàn nội dung

SOURCE_MANIFEST.csv và recheck_validation.json kiểm tra nguồn/bản sao. Bao_cao_NCKH_bao_toan.md cùng figures/ và sources/ được giữ nguyên, không viết lại. Đây là toàn bộ bản thảo hiện có, chưa phải báo cáo hoàn chỉnh đã duyệt; checkpoint hiện hành vẫn ghi nội dung và review còn thiếu. Không biến việc bảo toàn thành claim hoàn tất khoa học.

Mẫu báo cáo là ZIP LaTeX trong templates/original/; DOCX năm 2026 là mẫu đề cương riêng. Không dùng mẫu đề cương làm mẫu báo cáo.
