# Dry run — DỪNG TRƯỚC KHI XÓA
**Chưa xóa, archive, di chuyển, đổi tên, commit hoặc push. Chỉ cấu hình hiển thị workspace được chỉnh theo yêu cầu bổ sung.**
Nhóm A: 0 cache file đề xuất DELETE, 0 bytes (0.00 MiB) logical bytes dự kiến. Chưa đo freed disk space.
Nhóm B/REVIEW: 4 file; KHÔNG được chạy xóa cho tới khi giải quyết dependency/baseline và bạn duyệt đường dẫn cụ thể.
Manifest thực thi tương lai: deletion_candidates.csv, mỗi dòng có full path, bytes, SHA-256, Git status, lý do, replacement, dependency scan, risk và tính phục hồi. Chỉ DELETE được duyệt mới được phép thực thi.
| Nhóm | Hành động | Phạm vi | Điều kiện |
|---|---|---|---|
| A_CACHE | DELETE sau duyệt | Cache tái tạo, không tracked/protected | Rehash + Git + exact paths trước xóa |
| B_OLD_REPORT_EXPORT | REVIEW | 4 PDF V2–V5 đã bị xóa ở origin/main; local chưa pull | Phân biệt apply incoming commit với cleanup mới; sửa navigation nếu cần; giữ source/QA |
| C_PRESENTATION | KEEP | Mọi PPTX, MP4, backup, source và delivery ZIP | No-Repair/animation/pairing chưa khép |
| D_RESEARCH | KEEP | data/results/config/src/notebook/evidence/model | Không rename train/TEST I/O hoặc model |
| E_ENVIRONMENT | KEEP | venv/runtime, logs/evidence chưa rõ | Không có chứng minh replacement/rebuild tương đương |
| F_NAMES_AND_MD | KEEP/REVIEW | phase_name_review.csv + core docs | Không xóa MD cốt lõi; rename cần full mapping/callers/checksums |
## Các đường dẫn đề xuất
| Action | Full path | Bytes | Git | Ref count |
|---|---|---|---|---|
| REVIEW | C:\Users\admin\Documents\ChatGPT\NCKH\exports\report_revision_v2_2026_10_17\Bao_cao_NCKH_EnsembleLearning_REVISION_V2.pdf | 379512 | tracked | 6 |
| REVIEW | C:\Users\admin\Documents\ChatGPT\NCKH\exports\report_revision_v3_2026_10_19\Bao_cao_NCKH_EnsembleLearning_REVISION_V3.pdf | 411326 | tracked | 5 |
| REVIEW | C:\Users\admin\Documents\ChatGPT\NCKH\exports\report_revision_v4_2026_10_19\Bao_cao_NCKH_EnsembleLearning_REVISION_V4.pdf | 430720 | tracked | 5 |
| REVIEW | C:\Users\admin\Documents\ChatGPT\NCKH\exports\report_revision_v5_2026_10_19\Bao_cao_NCKH_EnsembleLearning_REVISION_V5.pdf | 426545 | tracked | 5 |
Số tracked trong nhóm DELETE: 0. Chưa có file biến mất khỏi GitHub do lượt này. Incoming upstream deletions được ghi riêng trong git_snapshot.json.
Giảm logical working-tree bytes khác giảm Git history: xóa tracked file không thu hồi blob lịch sử; không rewrite hoặc force-push.
## Giới hạn dependency audit
Đã đọc 1,277 file text project không nằm trong runtime/environment (<=6MB mỗi file); exact-path + basename matches lưu candidate_dependencies.csv. Có thể có dynamic path/external consumers: không kết luận unused chỉ vì zero match.
Mọi rename/move source hoặc generated output ngoài cache còn REVIEW. Các link QA/manifest là evidence không được sửa như navigation thông thường.
## Bước sau khi duyệt
Chọn exact paths/group A đã duyệt; recheck Git user changes + hashes + workspace containment; tạo codex/cleanup-* và ghi HEAD/manifest; dùng git rm chỉ với tracked được duyệt; xóa local đúng file được duyệt; validate frozen/P21/report/links; commit cleanup riêng; push nhánh cleanup. Main cần duyệt cuối riêng.
DELETED_FILES_MANIFEST.json và 06_CLEANUP_RESULTS.md chỉ tạo sau thực thi; không tạo kết quả giả khi chưa xóa.
Nhóm A hiện rỗng. Mục cần quyết định là đồng bộ 4 PDF V2–V5 với remote sau khi xử lý tham chiếu; tổng logical bytes nếu bỏ 4 PDF là 1,648,103 (~1.57 MiB), chưa giải phóng. Giữ nguyên tất cả nhóm còn lại. Việc dùng workspace GON đầy đủ không cấp phép xóa.
