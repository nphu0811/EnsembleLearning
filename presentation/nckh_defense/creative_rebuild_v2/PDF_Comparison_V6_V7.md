# So sánh PDF V6 và V7

V6:50trang. V7:49trang. BảnV7 rút gọn câu và thay phân trang; số trang giảm không phải bỏ bảng/kếtquả. Giữ fontLiberationSerif2 bằng filefont gốc đóng gói (OFL); TeXLive2026 local thay cho buildLinux trướcđó.13nguồnLaTeX được kiểm tra bấtbiến khoa học;6hình không thay;3filebibliography không thay.

38đoạn sửa có trước/sau ởHumanizer_Change_Log.md. Toàn bộ diff nguồn: audit/diff_*.patch; diff textPDF: audit/PDF_text_comparison.patch. Hai diff khác nhau vì PDF có header/footer/TOC/phântrang được biên dịch lại.

Đã render49trang và xem3contactsheet; kiểm tra sốtựđộng trên source thay vì so chuỗi số toànPDF vốn chứa sốtrang. Không dùng OCR để viết đè PDF.
