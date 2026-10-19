# Danh sách bảo vệ trước dọn dẹp
47,873 file được liệt kê với đường dẫn, SHA-256 và lý do trong protected_files.csv; toàn bộ data/, results/, config/, .research_memory/, templates/, src/, notebook/, scientific scripts/tests mặc định KEEP.
Bảo vệ toàn bộ UNSW/CIC raw, TRAIN/TEST, frozen P9/P15, P21 đủ 5 seed + aggregate, model/checkpoint, seed configs, leakage reports, manifest/checksum, scientific decision logs. Không sửa số liệu, không retrain/re-evaluate TEST.
Bảo vệ báo cáo V7 + nguồn/bib/figure transitively cần thiết; các scientific snapshot trùng hash vẫn KEEP. Model không đổi tên, không load.
Bảo vệ mọi PPTX/MP4 đến khi chứng nhận native desktop no-Repair, đủ nội dung/animation và backup hoạt động. Không tự coi PPTX 10 slide là canonical ổn định.
Môi trường .venv-p15-local và các runtime vẫn KEEP: phải kiểm tra phiên bản/package và builder trước khi có đề xuất xóa cụ thể.
templates/original có Word lock ~$ chưa commit: KEEP, có thể đang được Word sử dụng; không coi là rác để xóa.
Git objects/history không hash nội dung trong audit này và không được xóa/rewrite. protected_files.csv là baseline tại thời điểm audit, không phải yêu cầu thay checksum lịch sử.
