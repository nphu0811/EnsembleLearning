# Ma trận yêu cầu mẫu

Nguồn đã kiểm tra ngày 16/10/2026 bằng ZIP CRC, SHA-256 và OOXML. Chưa render tài liệu.

`templates/original/DE-TAI-NCKHSV-15.zip` là bản sao của `C:/Users/admin/Downloads/DE-TAI-NCKHSV-15.zip`. ZIP có 15 file, chỉ là LaTeX. `templates/original/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx` được sao chép từ file riêng cùng tên trong Downloads; có 9 bảng. Toàn bộ 15 file LaTeX trong folder workspace cũ khớp ZIP. Nguồn và checksum chi tiết tại `results/reproducibility/resume_2026_10_16/bootstrap/template_audit.json`.

Chỉ áp dụng cấu trúc LaTeX cho báo cáo kết quả; Word quản lý đề cương. Nội dung Android/CNN, danh tính và số liệu ví dụ trong LaTeX không thuộc evidence IDS.

| Nguồn / vị trí | Trường hoặc mục | Điều kiện | Nội dung cung cấp / kế hoạch | Artifact đầu ra | Trạng thái kiểm định |
|---|---|---|---|---|---|
| DOCX body 8–10 | Tên, mã đề tài, lĩnh vực | Giữ bố cục mẫu | Tên đề tài theo MASTER; mã/lĩnh vực hành chính cần xác nhận | proposal/De_cuong_NCKH_2026.docx | STRUCTURE_VERIFIED; chưa điền |
| DOCX 11–20 | Mục tiêu, nội dung, kết quả | Nhất quán RQ đã khóa | Foundation theo researchwrite, không hứa ensemble thắng | DOCX + PDF đề cương | FOUNDATION_IN_PROGRESS |
| DOCX 21–32 | Đơn vị, chủ trì, thành viên, GVHD | Không lấy tên mẫu làm xác nhận | [CẦN XÁC NHẬN] họ tên, MSSV, lớp, liên hệ, học hàm/học vị | DOCX | AUTHOR_INPUT_NEEDED |
| DOCX 33–38 | Tổng quan trong/ngoài nước | Bắt buộc điền theo chữ trong form | Kế thừa literature matrix; phải xác minh nguồn và bổ sung trong nước | DOCX, verified refs | CITATION_AUDIT_PENDING |
| DOCX 39–41 | Nhu cầu và khả năng áp dụng | Bắt buộc | Research prototype offline trên flow CSV; chưa chứng minh vận hành mạng thật | DOCX | CONTENT_PENDING |
| DOCX bảng body 43 | Loại sản phẩm I–III | Giữ các ô gốc | Dự kiến phần mềm, phương pháp và bảng số liệu dạng III; xác nhận khi nộp | DOCX | STRUCTURE_VERIFIED |
| DOCX bảng 45 | Báo cáo 03 quyển | Mẫu ghi 03, không tự sửa | Xác nhận quy định áp dụng với đơn vị | DOCX | AUTHOR_INPUT_NEEDED |
| DOCX bảng 47,49 | Chỉ tiêu chất lượng | Không đặt ngưỡng Accuracy không có căn cứ | Metrics, uncertainty, reproducibility, tính đầy đủ; mẫu còn ghi CD và thuyết minh phần mềm không quá 02 trang A4 | DOCX, phần mềm, demo runbook | STRUCTURE_VERIFIED; áp dụng cần xác nhận |
| DOCX bảng 51 | Tiến độ | 4 / 11 / 11 / 4 tuần | Giữ thời lượng; chuyên đề dự kiến protocol–baseline và ensemble–đánh giá; lịch thực tế chưa xác nhận | DOCX | AUTHOR_INPUT_NEEDED |
| DOCX bảng 53 | Kinh phí | Tổng 7.000.000 VND | Giữ 3.000.000, 3.500.000, 500.000 và các ô trống của mẫu; không ghi là đã chi | DOCX | STRUCTURE_VERIFIED; phê duyệt chưa có |
| DOCX bảng 55 | Chữ ký | Không giả chữ ký/ngày ký | Tên người đại diện có sẵn trong mẫu cũng chưa xác nhận đang áp dụng | DOCX + bản ký người dùng | AUTHOR_INPUT_NEEDED |
| LaTeX main.tex | Bìa, cam đoan, cảm ơn, mục lục, viết tắt, hình/bảng, chương, references | Bám template gốc | Tạo working copy; giữ gốc; thay nội dung ví dụ | report/Bao_cao_NCKH.pdf + sources | TEMPLATE_VERIFIED; chưa build |
| LaTeX styles/settings.tex, thesis.sty | Khổ giấy, font, margin, bìa | Không dùng metadata mẫu như sự thật | A4, lề 20/20/30/20 mm theo source; kiểm tra font Việt khi render | Báo cáo PDF | BUILD_TOOL_UNAVAILABLE |
| LaTeX chapters/, pages/, refs.bib | Nội dung IDS và citations | Loại placeholder và nội dung Android | Chỉ dùng bảng đã khóa và nguồn đã kiểm chứng; cam đoan chưa ký | Báo cáo + BibTeX | CONTENT_PENDING |
| MASTER_PROMPT.md | Tóm tắt, code, slides, demo, manifest | Yêu cầu bổ sung ngoài template | Có task riêng; không mặc định template chứa đủ | release/FINAL_NCKH/ | NOT_READY |

QA cuối: mở/render từng trang DOCX/PDF; không tràn/đè chữ; Unicode Việt; mục lục/cross-reference đúng; chưa có render thì không đánh PASS hình thức. Không gắn nhãn READY_FOR_SUBMISSION khi còn trường xác nhận.
