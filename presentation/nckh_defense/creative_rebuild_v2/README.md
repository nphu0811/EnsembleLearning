# NCKH Ensemble IDS — Creative Rebuild V2

Mở NCKH_Ensemble_IDS_Creative_Final.pptx trong PowerPoint desktop, bắt đầu slide show từ trang1, dùng timing tự động. Deck29trang:17chính/8cảnh/360giây và12phụlụcẩn. Click A1–A12 ở trang kết luận để mở phụ lục rồi “Về kết luận”. Các shape/text/chart đều là đối tượng native. Không embedded narration trong PPTX: lời đọc nằm trong MP4, MP3 và speaker notes để dễ luyện tập/chỉnh sửa.

Xem video NCKH_Ensemble_IDS_Creative_Preview.mp4. Đây là chuyển động thật xuất từ PowerPoint; FFmpeg chỉ chỉnh timestamp nhỏ và ghép voice, không dựng motion thay thế. StaticPDF là trạng thái bố cục cuối, không thể hiện các bước xuất hiện theo thời gian.

Báo cáo V7, LaTeX source zip, change log, Scientific_Integrity_QA và PDF_Comparison_V6_V7 nằm cùng thư mục. V6, deck cũ và kết quả nghiên cứu được giữ nguyên. Xem QA_Report.md trước khi đưa vào buổi bảo vệ; các giới hạn tiếp cận website và kiểm tra TTS được nêu rõ.

Để tái dựng: cài Python3.11, python-pptx, pywin32, numpy, Pillow, lxml, edge-tts; Microsoft PowerPoint desktop và FFmpeg/ffprobe. Chạy build_creative.py --render --video; measure_voice.py; finalize_creative_video.py; audit_native.py; qa_motion_frames.py; write_delivery_docs.py. Chạy tuần tự các tác vụ PowerPoint COM. PDF V7 tái dựng bằng build_report.py với TinyTeX/XeLaTeX và BibTeX.
