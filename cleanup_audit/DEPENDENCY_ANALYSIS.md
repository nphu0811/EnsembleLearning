# Phụ thuộc, Markdown và giới hạn kiểm định
228 LaTeX input/include/graphic/bibliography references; 9 chưa resolve qua cwd source/report (macro/dynamic/template paths có thể cần build). Xem latex_dependencies.csv; chưa gọi unresolved là broken file nếu dùng macro.
322 Markdown project ngoài memory/runtime được phân loại trong markdown_review.csv. Có/không literal reference không đủ để xóa nội dung cốt lõi hoặc lịch sử.
Imports Python, subprocess, PowerShell, workflows, config, manifest và Markdown thuộc tập 1,277 text project đã được dò tên/path ứng viên. Không đề xuất xóa bất kỳ module/CLI scientific nào, nên không suy diễn module unused từ import scan.
4 PDF V2–V5 có references trong builder/visual QA và evidence lịch sử. Builder tạo output không có nghĩa cần PDF pre-existing; visual QA đọc PDF có thể fail sau khi xóa nếu không chạy builder trước. Remote main đã xóa PDF và manual-only các builder; chưa đồng bộ local trong lượt này.
V6 PDF vẫn là đầu vào baseline của creative_rebuild_v2/qa_report_v7.py, cùng protected SHA maps; KEEP. Nguồn V7 gồm source riêng, fonts/assets và dependencies đã copy; không xóa report/ hoặc shared figures.
PPTX XML: 32-slide gốc không internal timing; 29-slide Creative có 439 effects; 10-slide có 313 effect nodes. Zero missing shape target không chứng minh PowerPoint không Repair. Giữ cả 3 và các concept/backups.
video_probes.json: ffprobe metadata, chưa full-decode/visual/audio listening hoặc native animation identity. Không xóa bản video tương ứng deck.
research_prechecks.json: fresh protocol 29/29 + five-seed PASS (5 seeds/25 arms). .venv Python 3.11.9, scientific package inventory đã lưu; không có chứng minh môi trường thay thế, KEEP.
STATE artifact manifest: 558 MATCH, 8 MISMATCH là .gitignore, mutable memory, README và roadmap. Không có missing entry; không thay checksum kỳ trước để biến finding thành PASS.
Không chạy training, inference, bootstrap, held-out TEST scoring, full PDF rebuild hoặc save/repair PPTX. Chỉ hash opaque dataset/model bytes.
