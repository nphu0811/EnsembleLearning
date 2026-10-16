# Hướng dẫn sử dụng bộ Master Prompt NCKH IDS

1. Đưa `MASTER_PROMPT.md`, `AGENTS.md`, `.research_memory/` vào **workspace nghiên cứu thật** (không thay thế code hoặc kết quả đang có). Nếu có `AGENTS.md` cũ, merge quy tắc, tránh ghi đè.
2. Đặt file zip mẫu `DE-TAI-NCKHSV-15.zip` và prompt gốc vào workspace hoặc cung cấp đường dẫn thực tế cho agent. Giữ các file mẫu gốc nguyên vẹn.
3. Mở Codex/agent có quyền đọc ghi và thực thi lệnh tại workspace. Dán `MASTER_PROMPT.md` hoặc yêu cầu agent đọc file này rồi thực hiện `KHỞI ĐỘNG NCKH`.
4. Khi chuyển phiên, dùng `TIẾP TỤC NCKH`; agent phải kiểm tra `.research_memory/HANDOFF.md` và các file evidence **trên ổ đĩa**, không tự suy đoán phase.
5. Không coi các file starter memory là bằng chứng nghiên cứu đã hoàn thành. Nội dung thực phải được agent xác nhận bằng source code, data và experiment outputs.

Bộ pack là **bộ điều phối công việc**. Nó không tự chạy nền, không tự tạo nghiên cứu khi không có phiên agent có quyền thực thi, và không thay thế yêu cầu xác minh hồ sơ hành chính/chữ ký.
