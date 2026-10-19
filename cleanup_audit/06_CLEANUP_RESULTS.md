# Kết quả cleanup đã được duyệt — 19/10/2026

Trạng thái: cleanup phạm vi được duyệt và rename tài liệu đã kiểm tra đạt; đã commit/push nhánh `codex/workspace-cleanup-20261019`, remote xác nhận đúng implementation commit. Chưa merge main.

- Kiểm kê 52,059 file gồm Git; hash toàn bộ 48,405 file ngoài Git, 0 lỗi đọc.
- Đã loại đúng 4 PDF V2–V5 khỏi local bằng fast-forward tới 6 commit có sẵn trên remote. Các file này đã được xóa trên GitHub trong commit `3dc7caa179ce1baf8441b426ae145a7f7a874c73`; commit cleanup mới không xóa thêm file tracked nào.
- Đo trước/sau đúng 4 đường dẫn: 1,648,103 → 0 bytes; số logical file bytes được loại là **1,648,103 (~1.57 MiB)**. Không tuyên bố thay đổi physical free disk hoặc Git history.
- Đổi tên **53 Markdown** theo công việc, bỏ P/Phase trong tên; cập nhật **26 file tham chiếu** ban đầu, thêm mục lục hiện hành và bộ phân giải đường dẫn tài liệu cho resume audit. Danh sách chính xác và SHA trước/sau: RENAMED_FILES_MANIFEST.json.
- Không archive. Ngoài 4 PDF và 53 đường dẫn đổi tên, không có file gốc mất ngoài danh sách. Giữ mọi dataset, model, train/TEST results, protocol/config, nguồn train, notebook và snapshot/manifest kiểm chứng.
- Đã đối chiếu SHA-256 lại **1,059 file bất biến**, 0 thay đổi ngoài ý muốn. Không train, predict, bootstrap hoặc đánh giá TEST.
- GON dùng một cây NCKH hiện đủ nhóm công việc; full workspace nhiều root vẫn có sẵn.

## Phiên bản giữ lại

- Báo cáo V7: `presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf`, 49 trang, SHA `3579e41be58d24aee3807e000ffe6d762ebb857f1c588c1f0c503ef6f29cee0e`; giữ nguồn LaTeX/fonts/bib/figures và ZIP nguồn.
- V6 giữ tại vị trí gốc vì là đầu vào/baseline QA của V7.
- Giữ PPTX gốc 32 slide, Creative V2 29 slide và ứng viên 10 slide, cùng MP4/PDF/backup tương ứng. Chưa xác minh lại desktop no-Repair/animation; không nhận bản 10 slide đã ổn định.
- Định danh phase trong dữ liệu/model/kết quả, source train/TEST và notebook/protocol đóng băng không rename. Tên cũ trong snapshot/review/checksum lịch sử giữ nguyên; current resume audit tra cứu qua manifest mà không sửa expected hash.

## Validation

- Rename mapping/đường dẫn hiện hành: 53/53 tài liệu, 95 file consumer, 0 lỗi.
- Protocol validator: 29/29. P21: đủ 5 seed × 5 arm, PASS chỉ đọc.
- 24 unit tests liên quan: PASS. Sửa đúng một fixture test Windows tạo CRCRLF khi input đã là CRLF; chỉ chuẩn hóa dữ liệu giả trong RAM trước kiểm tra LF/CRLF. Không sửa JSON đóng băng hay nới điều kiện validator. Lần lỗi trước được giữ trong local post_cleanup_checks.json.
- P20 reviewer audit: 944 PASS, 0 FAIL, 1 cảnh báo provenance có sẵn, 14 anchor local-only giữ trạng thái SKIPPED; không sửa báo cáo reviewer.
- Git diff --check và cached diff --check: PASS. Allowlist đóng gói hiện hành không mất file.
- Review độc lập chỉ đọc: không phát hiện lỗi cần sửa.
- Historical resume digest vẫn 547/566 và preservation 262/282: sai khác metadata/navigation và historical absence giữ nguyên minh bạch, không thay expected hash để ghi PASS giả. Kết quả scoped cleanup ở VALIDATION_SUMMARY.json.

## Dung lượng và file giữ lại

Baseline toàn workspace: 4,193,776,701 logical bytes. Snapshot sau thao tác: 4,238,729,273 bytes gồm Git và evidence audit; tăng 44,952,572 bytes. Audit mới chiếm 39,617,825 bytes tại thời điểm đo. **Workspace không giảm ròng dung lượng trong lượt này** vì tạo evidence và đồng bộ Git. Các inventory/duplicate/environment CSV lớn giữ local và không đưa vào commit.

48,405 file gốc ngoài Git được kiểm tra: 4 xóa, 53 đổi đường dẫn, 48,348 đường dẫn gốc còn lại được giữ. Không tính file mới của audit/navigation. Đây là số snapshot file, không phải số file Git tracked.

## Git và phục hồi

- Commit gốc local: `72dd60d669a40554e7c6e884413bb96f837b58ba`.
- Đồng bộ an toàn bằng fetch + fast-forward tới origin/main `6d2424431849ea1bd432baf1b4da09d2c5e1b651`; giữ các thay đổi chưa commit và Word lock chưa tracked.
- Cleanup implementation commit: `acf80302649ebeab3f2a52b230551248d1bd63a3`. Push: VERIFIED bằng git ls-remote. Main merge: CHỜ DUYỆT CUỐI. Receipt commit sau đó chỉ ghi trạng thái publication; xem PUBLICATION_RECEIPT.json.
- Có thể phục hồi một PDF bằng `git restore --source=72dd60d --worktree -- <đường-dẫn-chính-xác-trong-DELETED_FILES_MANIFEST.json>`. Không dùng reset hard, git clean, force push hoặc rewrite history.
- Phục hồi rename theo mapping hoặc Git history trên một nhánh riêng; không khôi phục hàng loạt đè các thay đổi mới.
