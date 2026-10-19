# Ma trận phiên bản và nguồn hiện hành
Chấp nhận nội dung V7 được kế thừa từ yêu cầu người dùng; trạng thái ổn định PowerPoint chưa được suy ra từ ngày tạo.
| Artifact | Hiện hành/ứng viên | Bản trước | Bằng chứng | Có thể xóa? | Dự phòng |
|---|---|---|---|---|---|
| Báo cáo | V7: presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf | V1–V6: lịch sử/đầu vào; V2–V5 deleted upstream | README + V7 source/invariants + PDF parse | PDF V2–V5 REVIEW; source/QA KEEP | Có: V6 và nguồn |
| Nguồn V7 | presentation/nckh_defense/creative_rebuild_v2/report_v7/source/; LaTeX_Revision_V7_Source.zip | report/ vẫn chứa V6 và chapters phụ thuộc | build_report.py, humanize_report.py, latex_dependencies.csv | KEEP nguồn và mọi dependency, cả file không mang nhãn V7 | Có, ZIP + source |
| PPTX 10 slide | Ứng viên chưa ổn định: script_first_v3/final_10_slide_v1/NCKH_Ensemble_IDS_10_Slides_Final.pptx | Không xác nhận thay thế 29/32 slide | README ghi Repair; XML không chứng minh no-Repair | KEEP tất cả cho đến desktop gate | Bắt buộc |
| Creative V2 | creative_rebuild_v2/NCKH_Ensemble_IDS_Creative_Final.pptx; 29 slide | Bản 32 slide gốc giữ để dự phòng | QA_Report.md ghi historical COM/render; fresh no-Repair chưa chứng nhận | KEEP | Có: bản gốc + ZIP |
| Video Neural 10 slide | NCKH_Ensemble_IDS_10_Slides_Preview_NeuralVoice.mp4 | Offline preview là fallback, không native animation equivalent | FINAL_HANDOFF.md + builder source | KEEP cả hai đến paired runtime QA | Có |
| Video Creative V2/gốc | Mỗi MP4 giữ theo deck/source tương ứng | Không so bằng mtime/size | artifact_inspection.json + handoff + timeline | KEEP native silent/preview khi chưa chứng minh rebuild mất mát=0 | Có |
| Source train/TEST/model | src/, config/, results/, notebook/, scientific tools | Không có thay thế được cho phép trong cleanup | Protocol/frozen SHA + user constraint | KEEP, không rename hay sửa I/O | Giữ lịch sử |
| Tên phase và Markdown | phase_name_review.csv phân loại KEEP/REVIEW | Không tự bỏ P* khỏi định danh provenance | Imports, outputs, checksum, workflow phụ thuộc | Đổi tên chỉ sau mapping đồng bộ riêng; chưa đổi | Giữ thông tin cốt lõi |
Không di chuyển source V7 khỏi presentation chỉ để đẹp cây thư mục: builder, bibliography, figures, report/ V6 và checksum có ràng buộc. Workspace GON hiện đủ các nhóm là bước tổ chức trước mắt.
report/README.md và STATE/HANDOFF còn nhiều trạng thái cũ 37/47 trang hoặc pilot pending; current artifact/P21 validator phải được đối chiếu thay vì tin văn bản cũ.
Source-to-export và dependency LaTeX: latex_dependencies.csv. Desktop no-Repair, animation, logo/font và video-frame correspondence vẫn là gate riêng.
