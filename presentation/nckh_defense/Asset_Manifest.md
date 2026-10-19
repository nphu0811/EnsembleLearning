# Asset Manifest

| Asset | Nguồn / cách tạo | Định dạng và quyền chỉnh sửa | Giới hạn |
|---|---|---|---|
| Sơ đồ flow và pipeline | Tự dựng từ HIST_CODE/P21_CODE; build_deck.py | Native PowerPoint rectangles/ovals/text/arrow connectors | Minh họa cơ chế offline; chấm cyan không phải một packet trace đo được |
| RF tree schematic | Tự dựng vector nhánh cây để giải thích bagging | Native connectors + nodes | Minh họa cấu trúc;5 cây biểu tượng không phải số cây đã huấn luyện |
| FP/FN bars | P9 final_metrics.csv, cột fp/fn | Native rectangles/text; scale có ghi chú | FP0–11000, FN0–1000; không so độ dài giữa2 trục |
| P21 paired seed chart | aggregate.json per_seed metric | Native dots/segments/text | X-axis rút gọn ghi rõ; cùng validation |
| Selector+fit cost bars | V6 Bảng4.11 / frozen P21 | Native rectangles/text | Giây fit; không phải end-to-end |
| FPR/FNR scatter | Trung bình5 seed của A0/A2/A3 | Native dots/axes/text | P21 only; trục0, unit phần trăm |
| SVG files | Export dự phòng từ native geometry trong build_deck.py | svg/slide_01.svg…slide_32.svg | SVG là bản trung gian để chỉnh geometry; PPTX và PowerPoint renders là chuẩn fidelity, SVG không có Morph và text wrapping có thể khác |
| PNG previews | Microsoft PowerPoint export,1600×900 | renders/slide_NN.png | Chỉ kiểm chứng trạng thái tĩnh |
| Audio voice-over | edge-tts vi-VN-NamMinhNeural, rate−5%; spoken text trong content.py | audio/slide_NN.mp3 + narration.wav | Giọng tổng hợp để luyện tập, không giả giọng người trong nhóm; cần mạng để tái tạo |
| MP4 motion | PowerPoint CreateVideo; ghép audio bằng FFmpeg | H.2641080p30 + AAC | Xem audit và QA_Report về timing, không dùng mô phỏng Manim |
| Fonts | Aptos từ Microsoft Office local | Text giữ editable; không nhúng/redistribute file font | Máy nhận cần font tương thích dấu Việt |

Không dùng ảnh AI, stock photo, robot, não sáng, bảng mạch hoặc logo bên thứ ba. Không sao chép style pack/template của các repo khảo sát. Báo cáo V6 và kết quả gốc được giữ nguyên; nguồn tải khảo sát chỉ nằm trong audit để kiểm tra, không dùng làm hình slide.
