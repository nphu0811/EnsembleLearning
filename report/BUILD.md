# P17 — Chạy build báo cáo trên checkout có đầy đủ source

Đây là quy trình để **kiểm định source P17**, không phải bằng chứng build đã hoàn tất. Thực hiện trong thư mục `NCKH/report`; cần cài XeLaTeX và BibTeX (`xelatex --version`, `bibtex --version`). Bộ LaTeX mẫu gốc nằm ở `templates/original/`, **không được sửa/xóa**.

PowerShell (từ gốc project):

```powershell
git status
cd report
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Kiểm tra `main.pdf`, `main.log` và cảnh báo `undefined citation`, `undefined reference`, `Overfull`, `Missing character`, lỗi font. **Không tự cho PASS khi mới chỉ có file PDF**. Render từng trang kiểm tra: dấu tiếng Việt, bảng không tràn, bìa placeholder, TOC, bibliography đầy đủ, không có tên giả.

Output `*.aux`, `*.toc`, `*.out`, `*.bbl`, `*.blg`, `main.pdf` là artifact build cục bộ; **không dùng `git add .`** để đưa vào repo khi chưa QA và chốt output. `.gitignore` hiện chưa loại toàn bộ artifact LaTeX; việc chỉnh ignore/cleanup do người dùng quyết định.

Để kiểm tra không có thay đổi ngoài ý muốn: quay về gốc `cd ..`, chạy `git status` rồi chỉ stage những file nguồn cần thiết.

Nếu không có XeLaTeX, giữ `BUILD_BLOCKED`, tiếp tục P18/P19 hoặc review source, không giả lập thành công.

Các đầu ra dự kiến của một lần build thực: `main.pdf`, file log, kiểm tra font/glyph và biên bản QA layout. Việc ghép đúng form chuẩn trường, duyệt tác giả/GVHD và hoàn tất bibliography là các gate độc lập chưa được đóng.

## GitHub Actions build khả dụng (16/10/2026)

Máy Windows của bạn có thể không cài XeLaTeX/BibTeX. Trong project hiện đã có `.github/workflows/p17-latex.yml`; workflow tự build trên GitHub khi `report/**` thay đổi, hoặc có thể chạy thủ công ở tab Actions. Lấy PDF + log ở mục **Artifacts → p17-report-pdf-and-logs** của run tương ứng.

- Run đầu `38900247221`: build có 16 cảnh báo Overfull (max170.67pt); **không** được coi là layout QA pass.
- Sau sửa nguồn `cb556fc`, run `38901027329`: 22 trang A4; XeLaTeX+BibTeX thành công; 0 Overfull, 0 missing glyph, 12 mục tài liệu tham khảo; rendered PDF đã được kiểm tra. Xem `report/PDF_QA_2026-10-16.md`.
- Workflow đã có điều kiện phát hiện Overfull/Missing character ở log cuối; nếu lỗi xuất hiện, CI phải fail.

Phần hướng dẫn cũ bên trên là **phương án build trên máy**, không phải yêu cầu bắt buộc. P17 vẫn thiếu duyệt theo mẫu chuẩn cơ sở đào tạo và thông tin thật. Không commit/copy bản build tạm vào các evidence frozen trước khi nghiệm thu.
