# P17 — QA bản báo cáo 5 chương (16/10/2026)

**Phiên bản kiểm tra:** source commit `99ea68f641fb6abff06413ecae584e8b2df23e02`; GitHub Actions run [38916942038](https://github.com/nphu0811/EnsembleLearning/actions/runs/38916942038). **Phạm vi:** biên tập cấu trúc và kiểm tra kỹ thuật PDF; không phải xác nhận hội đồng hoặc chứng nhận không đạo văn.

## Cấu trúc chính thức của bản nguồn báo cáo hiện tại

1. **Cơ sở lý thuyết** — bối cảnh, mục tiêu, các mô hình LR/DT/RF, Voting/Stacking và nghiên cứu liên quan.
2. **Dữ liệu và quy trình tiền xử lý** — UNSW-NB15, EDA, kiểm toán overlap.
3. **Xây dựng mô hình và thiết kế thực nghiệm** — pipeline, Feature Selection, cấu hình huấn luyện, OOF, giao thức TRAIN/TEST, chỉ số đánh giá.
4. **Kết quả thực nghiệm và đánh giá** — confusion matrix, Macro-F1, MCC, paired bootstrap, chi phí và kết quả theo nhóm Attack.
5. **Thảo luận và hướng phát triển** — đánh đổi giữa FP/FN, độ tin cậy thống kê, các giới hạn và đề xuất hướng tiếp theo.

- Không còn chương `Tóm tắt`.
- `Danh mục từ viết tắt` nằm ngay **sau Mục lục**, trước Danh sách hình/bảng. Cột cuối trình bày **ý nghĩa/vai trò của từng khái niệm trong IDS**, thay vì chỉ dịch chữ từ tiếng Anh.
- Các file LaTeX trước đây mang tên `introduction.tex`, `related_work.tex`, `conclusion.tex`... vẫn được **sử dụng làm section/subsection** của năm chương; chúng không phải tám chương độc lập. Không xóa hoặc nhân đôi source khi chưa có quyết định cleanup.
- Trong văn bản PDF không còn dẫn đường dẫn dự án nội bộ `notebook/`, `report/`, `results/`, `.md`, `.json`, `SMOKE_ONLY`; đường dẫn `\\input{}`/`\\includegraphics{}` trong source LaTeX vẫn tồn tại để build và không in ra PDF.

## Kiểm định sau build có bằng chứng trực tiếp

| Điều kiện | Kết quả |
|---|---|
| XeLaTeX + BibTeX / GitHub Actions | PASS |
| Số trang vật lý, A4 | **37**, thỏa yêu cầu 30–40 trang nếu tính toàn tài liệu |
| Chương chính xuất hiện trong PDF TOC | **5**, đúng thứ tự trên |
| Vị trí danh mục từ viết tắt | Trang PDF 6–7; Mục lục bắt đầu trang PDF 4; Danh sách hình trang PDF 8 |
| Mục Tóm tắt | Không xuất hiện |
| Trích dẫn | 12 mục `\\bibitem{}` trong `main.bbl` |
| Nhãn LaTeX trùng, citation/reference undefined | 0 theo log cuối |
| `Overfull \\hbox`, `Missing character` | 0 theo log cuối |
| Ký tự tô màu trong phần chữ PDF | đen `#000000` và đỏ `#960017` |
| Khối chữ ra ngoài mép trang / text span ẩn alpha=0 | 0 trong kiểm tra PDF bằng PyMuPDF |
| Đường dẫn `.md`, `.json` nội bộ trong phần văn bản PDF | 0 |
| SHA-256 PDF | `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b` |

PDF được tải và đọc thực từ artifact của GitHub Actions; đã render các trang đại diện gồm bìa, mục lục, danh mục viết tắt, đầu mỗi chương và bibliography. Số liệu RF-42, Stacking-42, RF-17 và kết quả thống kê được kế thừa từ frozen metrics; không train lại hoặc chọn ngưỡng từ TEST trong công việc biên tập.

## Đánh giá văn phong và giới hạn QA

Bố cục dựa vào cấu trúc **5 chương lớn** của báo cáo NetFlow do người dùng cung cấp, nhưng chủ đề, phương pháp và kết quả là của đề tài Ensemble Learning. Các thuật ngữ được giải thích theo chức năng trong đề tài; các công thức được giữ nguyên. Phương pháp được mô tả bằng các bước xử lý/huấn luyện và mã nguồn nộp kèm; nội dung PDF không mang tính nhật ký GitHub.

**Nature Skills:** Các skill `nature-writing`/`nature-polishing` chỉ có trong môi trường Codex Windows theo registry dự án; chưa được tải/thi hành trong phiên ChatGPT này. Vì vậy **không ghi nhận** các skill ấy là đã sử dụng. Biên tập trong phiên này áp dụng kiểm tra bằng chứng khoa học, đối chiếu báo cáo mẫu và hậu kiểm PDF thật.

## Điều kiện nộp chính thức còn mở

Mẫu trường và thông tin hành chính đã được điền theo thông tin người dùng xác nhận, nhưng vẫn cần nhóm tự rà soát và ký thực tế; không có chữ ký được tạo hoặc giả lập. P15 tái lập toàn mô hình, P18 hệ thống hóa tài liệu, P19 quyền phát hành dữ liệu/mã nguồn và P20 duyệt đầy đủ vẫn còn các gate độc lập. Không coi 37 trang đạt kỹ thuật là giấy phép tuyên bố công trình được hội đồng duyệt hoặc không có tương đồng học thuật.
