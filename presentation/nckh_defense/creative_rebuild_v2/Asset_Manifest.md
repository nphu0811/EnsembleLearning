# Asset Manifest

|Asset|Nguồn|Quyền/ghi chú|
|---|---|---|
|Toàn bộ 568 shape instances|Tự dựng trong Python/PowerPoint|Text, vector, connectors, graph, cây, matrix, bars chỉnh sửa được; không có AI raster slide|
|Dữ liệu chart|CSV/JSON nghiên cứu sẵn có|Không huấn luyện lại; Scientific_Evidence_Map.md chỉ đúng file/field|
|Fonts slide|Arial, Aptos, Consolas cài tại máy|Không phân phối font Microsoft trong gói; cần font tương ứng khi sửa máy khác|
|Font PDF V7|Liberation Serif, đóng gói kèm bản quyền|OFL; audit/report_font_provenance.json|
|Voice|Microsoft Edge vi-VN-HoaiMyNeural|TTS mẫu luyện tập, rate−5%; không giả giọng người thật; không nhạc nền|
|Reference screenshot|Các website trong references/ledger|Chỉ làm chứng cứ khảo sát; không đưa vào PPTX hay video|
|Concept clips A/B/C|Tự dựng native PowerPoint|9 giây/clip; không thay sản phẩm cuối|
|PDF V7|Nguồn V6 sao chép, biên tập38 đoạn|Không ghi đè V6; nguồn và diff được bàn giao|

Mã sinh deck: build_creative.py, motion_engine.py, creative_content.py. Code video: finalize_creative_video.py, qa_motion_frames.py. Renderer engine Microsoft PowerPoint bản cài tại máy; không nhúng Microsoft Office vào gói. TinyTeX portable chỉ là runtime xây PDF, loại khỏi ZIP bàn giao; build_report.py ghi đường dẫn runtime có thể cấu hình lại.
