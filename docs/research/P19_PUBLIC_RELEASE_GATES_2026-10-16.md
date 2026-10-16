# P19 — Kiểm toán tình trạng phát hành hiện hành (16/10/2026)

**Scope:** chỉ xác minh repository và quyền phát hành có thể quan sát được; `P19 = PARTIAL`, không công bố đây là hồ sơ FAIR hoặc release approved.

- GitHub repository [nphu0811/EnsembleLearning](https://github.com/nphu0811/EnsembleLearning) đã public; audit tree tại `de0a8593334a86001f20b71589ca2c4a85a2d257` có **615 tracked blobs** (có thể tiếp tục thay đổi ở commits sau).
- 0 file theo dõi dưới `data/raw/`; dataset UNSW-NB15 không được tái phân phối bằng bản báo cáo. Dữ liệu phải lấy đúng nguồn chủ sở hữu theo điều kiện sử dụng của họ.
- **Không có LICENSE/COPYING tại root**; hiển thị mã nguồn công khai không đồng nghĩa đã cấp phép tái sử dụng. Không tự thêm license nếu nhóm chưa lựa chọn.
- Có **3 `.joblib` SMOKE_ONLY** được theo dõi trong snapshot, nhưng không phải model full-TRAIN cuối. Không dùng làm demo IDS cuối hoặc gắn các số liệu official TEST với smoke model.
- `templates/original/` còn các tài nguyên mẫu lưu để đối chiếu. Cần rà quyền redistributing templates, hình và dữ liệu có nguồn khác trước khi tạo scholarly release; **không copy mẫu NetFlow người dùng upload vào repository**.
- Nhóm đã cung cấp bốn họ tên/MSSV, mã đề tài, lớp, GVHD, ngày để đưa vào **báo cáo và repository công khai theo yêu cầu**. Không suy ra từ đó quyền công khai số điện thoại, email riêng, chữ ký tay, tài liệu hành chính có dấu/tem hay thông tin cá nhân khác.
- Không thấy một signed tag và DOI gắn bản release chính thức được kiểm định trong kiểm tra này. PDF build artifact của Actions chỉ giữ thời hạn nhất định; khi nộp cần lưu snapshot file có SHA-256, ghi version/commit.
- Phase 15 vẫn chưa chứng minh tái lập end-to-end full TRAIN bằng môi trường lịch sử. Giữ provenance UNKNOWN, không tạo một model artifact giả để gỡ blocker.

**P19 decision:** `PUBLIC_SOURCE_VISIBLE` = verified; `PUBLIC_REUSE_LICENSE`, `THIRD_PARTY_RIGHTS`, `VERSIONED_ARCHIVAL_RELEASE`, `FULL_TRAIN_MODEL_AVAILABILITY` = OPEN. Cần quyết định của nhóm hoặc người phụ trách, không tự đóng bởi CI thành công.
