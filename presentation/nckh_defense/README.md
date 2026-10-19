# Bộ bảo vệ NCKH Ensemble IDS

- Mở `NCKH_Ensemble_IDS_Final.pptx` trong PowerPoint desktop hỗ trợ Morph, chạy từ slide1 với timing để xem bài chính6phút. File giữ native shapes/text/connectors và speaker notes, không flatten thành ảnh.
- `NCKH_Ensemble_IDS_Preview.mp4` là preview có voice-over tổng hợp tiếng Việt; chuyển động lấy từ PowerPoint native, không phải Manim mô phỏng.
- `NCKH_Ensemble_IDS_Static.pdf` gồm20 keyframe chính.12 phụ lục Q&A có trong PPTX (ẩn khỏi bài chính) và QnA_4_phut.md.
- Slide20 có A1–A12 để mở phụ lục; khi thuyết trình có thể gõ21…32 rồi Enter. Mỗi phụ lục có liên kết về kết luận.
- Luyện bài theo Kich_ban_thuyet_trinh_6_phut.md; xem Scientific_Evidence_Map.md và QA_Report.md trước khi sửa số liệu.

Tái dựng trên Windows có PowerPoint: `python -m pip install -r requirements_presentation.txt`; chạy lần lượt `python build_deck.py`, `python make_voice.py`, `python animate_export.py prepare`, `python animate_export.py video`, `python make_documents.py`, `python finalize_video.py`, `python validate_delivery.py`. Chạy từ repo gốc hoặc dùng absolute script path; thư mục output tự định vị. Không chạy pipeline train/model. PowerPoint timing test đã chứng minh transition duration phải trừ khỏi dwell; animation script xử lý điều này.

TTS cần Internet; nếu đã có MP3 và SHA đúng thì dùng lại. Giữ PDF/MP4/PPTX đã xuất để xem offline. Phiên bản thư viện thực tế được ghi trong requirements_presentation.txt. `audit/` giữ ledger nguồn, kiểm tra P21, QA độc lập và log xuất engine. `svg/` là asset trung gian; nguồn chính là content.py và build_deck.py. `checksums.sha256` kiểm tra các sản phẩm giao.
