# Cleanup đã thực thi sau duyệt

Xem [kết quả](06_CLEANUP_RESULTS.md), [mapping đổi tên](RENAMED_FILES_MANIFEST.json), [file đã xóa](DELETED_FILES_MANIFEST.json) và [validation](VALIDATION_SUMMARY.json). 01–05 là snapshot audit trước duyệt; các inventory/patch lớn giữ local, được ignore riêng.

---

# Audit workspace NCKH — dừng ở dry run

Đọc lần lượt 01_INVENTORY.md, 02_DUPLICATES.md, 03_CANONICAL_VERSION_MATRIX.md, 04_PROTECTED_FILES.md và 05_DELETION_PLAN.md. DEPENDENCY_ANALYSIS.md giải thích các tham chiếu và giới hạn. final_validation.json là kiểm tra mới nhất cho lượt audit + cấu hình workspace, không phải chứng nhận cleanup đã thực thi.

inventory.csv chứa snapshot toàn workspace; exact_duplicates.csv dùng SHA-256, không cấp phép xóa tự động. protected_files.csv, markdown_review.csv và phase_name_review.csv bảo vệ provenance/đường dẫn đang dùng. Các CSV lớn là evidence local: chưa stage hoặc push chúng; quyết định đóng gói trước commit để tránh đưa inventory môi trường vào Git không cần thiết.

Không xóa/đổi tên/di chuyển file trong lượt này. Không train/predict/đánh giá TEST. Bản GON được mở rộng theo chỉ thị mới nhất. Nhóm cache DELETE rỗng. Chỉ 4 PDF V2–V5 ở trạng thái REVIEW (đã bị xóa upstream, local chưa đồng bộ); phụ thuộc và duyệt exact paths phải được xử lý trước khi sync/remove. Mọi PPTX và video giữ nguyên vì desktop no-Repair/animation gate chưa khép.

Các đầu ra mới của audit làm tăng dung lượng local; inventory baseline loại cleanup_audit ra khỏi phép đo. Không có số dung lượng đã giải phóng. 06_CLEANUP_RESULTS.md và DELETED_FILES_MANIFEST.json chỉ tạo sau một lần cleanup thực thi được duyệt.

Chạy lại inventory từ root nếu cần: `python -B -X utf8 cleanup_audit/audit_workspace.py` (sẽ refresh audit evidence; không xóa). `refresh_analysis.py` cập nhật phân tích từ snapshot đã có, không rehash toàn bộ. Bản snapshot trong phiên này đã được bổ sung bằng research_prechecks.json, video_probes.json, workspace_checks.json và final_validation.json.
