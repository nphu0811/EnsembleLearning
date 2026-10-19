from pathlib import Path
import json,importlib.util,hashlib,csv,statistics
from creative_content import MAIN
O=Path(__file__).resolve().parent;R=O.parents[2]
def put(n,s):(O/n).write_text(s,encoding='utf-8')
def stamp(t):return f'{int(t)//60:02}:{t%60:05.2f}'
plan=json.loads((O/'NCKH_Ensemble_IDS_Creative_Final.motion.json').read_text(encoding='utf-8'))
meas=json.loads((O/'audio/measurements.json').read_text());t=0;parts=['# Kịch bản bảo vệ — 6 phút\n\nGiọng mẫu: vi-VN-HoaiMyNeural, rate −5%. Các tệp MP3 được đo bằng ffprobe; không kéo nhanh lời đọc. Bắt đầu nói sau 0,55 giây mỗi slide. Các cue dưới đây là tự động từ đầu slide, không cần bấm thêm. Kết thúc bài ở 06:00; phụ lục chỉ mở khi vấn đáp.\n\nTên trên văn bản giữ UNSW-NB15. Bản TTS dùng cách đọc “iu en ét đắp, en bê mười lăm”; khi bảo vệ có thể nói “bộ dữ liệu UNSW” sau lần giới thiệu đầu. TTS là giọng luyện tập, không thay cho đọc thử của người trình bày.\n']
for i,(scene,sec,view,title,speech) in enumerate(MAIN,1):
 m=meas[i-1];end=t+.55+m['speech_seconds'];events=plan[i-1]['events'];groups={}
 for e in events:groups.setdefault(round(e['at'],2),set()).add(e['kind'])
 cues='; '.join(f"+{at:g}s: {', '.join(sorted(k))}" for at,k in sorted(groups.items()))
 nxt='Nhóm xin cảm ơn hội đồng.' if i==17 else MAIN[i][3].replace('\n',' ')
 parts.append(f'## Cảnh {scene} · Slide {i:02} · {stamp(t)}–{stamp(t+sec)}\n\n**Thông điệp:** {title.replace(chr(10)," ")}\n\n**Lời nói chính xác** — bắt đầu {stamp(t+.55)}:\n\n{speech}\n\n**Dừng nói:** {stamp(end)}. Nghỉ còn {t+sec-end:.2f} giây đến hết slide.\n\n**Animation:** {cues}. Tên đối tượng, tọa độ và thời lượng đầy đủ trong `.motion.json`.\n\n**Chuyển ý:** hướng người nghe đến “{nxt}”. Không đọc thêm câu này nếu làm vượt slot.\n\n**Luyện tập:** giữ nhịp như tệp MP3; nhấn từ khóa trong thông điệp, nhìn hội đồng trong khoảng nghỉ. Slide {i} có {m["speech_seconds"]:.3f} giây lời đọc thực đo.\n')
 t+=sec
put('Kich_ban_6_phut_Humanized.md','\n'.join(parts))
from creative_qna import QA
q=['# Vấn đáp — 4 phút\n\nTrả lời phần chính trong 15–25 giây. Chỉ mở một phụ lục sát câu hỏi, bổ sung số liệu khi hội đồng yêu cầu. Từ slide kết luận, nhấn A1–A12; mỗi phụ lục có nút về kết luận. Các phụ lục 18–29 ẩn và không nằm trong video.\n']
from creative_qna import ANSWERS
for j,(title,question,a,source) in enumerate(QA,1):q.append(f'## A{j} · Slide {17+j}: {question}\n\n{ANSWERS[j-1]}\n\nNguồn: {source}.\n')
put('QnA_Humanized.md','\n'.join(q))
rows=json.loads((O/'audit/native_structure.json').read_text())
text='# Animation Manifest\n\nToàn bộ motion chính do PowerPoint TimeLine.MainSequence thực thi, xuất bằng PowerPoint CreateVideo. Không có Morph, video nhúng hoặc motion giả lập bằng FFmpeg. Wipe/Fade/Fly ở đây là hiệu ứng trên đối tượng trong slide; transition trang bằng none. FFmpeg chỉ chuẩn hóa timestamp video và ghép lời đọc.\n\n|Slide|Cảnh|Slot giây|Native effects|Motion paths|Scale|\n|---|---:|---:|---:|---:|---:|\n'
for i,r in enumerate(rows[:17]):text+=f'|{i+1}|{MAIN[i][0]}|{MAIN[i][1]}|{r["effects"]}|{r["motion_paths"]}|{r["scale"]}|\n'
text+='\nTổng: 17 slide có p:timing, 439 effect nodes, 59 p:animMotion, 15 p:animScale. Đối tượng đích đều tồn tại. 12 phụ lục ẩn. XML kiểm tra trong `audit/native_structure.json`; lệnh COM, motion path và repeat nằm trong `motion_engine.py`. Cấu hình riêng từng đối tượng trong `NCKH_Ensemble_IDS_Creative_Final.motion.json`.\n\nHero 2/network: slide2; feature:4; ensemble inference:5/9, OOF fit:6; FP/FN:11/12, hai thang riêng; P21:13; cost:16. Clip và chuỗi frame cùng slide nằm trong `hero_animations/`, kiểm tra sai biệt pixel trong `audit/motion_frame_evidence.json`. Pixel khác nhau chứng minh frame thay đổi; kết luận cơ chế cần xem chuỗi frame và source.\n'
put('Animation_Manifest.md',text)
put('Asset_Manifest.md','''# Asset Manifest

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
''')
oldmap=(O/'audit/Inherited_Scientific_Evidence_Map.md').read_text(encoding='utf-8')
put('Scientific_Evidence_Map.md','''# Scientific Evidence Map — Creative V2

Các đường dẫn và hash trong phần nguồn phía dưới đã có từ audit nghiên cứu; đối chiếu hash lại trong QA. Bảng slide mới sau đây thay thế số slide cũ của deck32 trang. Không chạy lại mô hình.

|Slide V2|Nội dung|Nguồn/field|
|---|---|---|
|1,11,12|−142 FP, +118 FN; RF10003/734; Stack9861/852|TEST official_test, fp/fn|
|3|175341 TRAIN,82332 TEST|V6 §3.1; protocol official split|
|4–9|42 predictor, LR/DT/RF, OOF/meta LR, inference|HIST_CODE build_preprocessor/make_stacking_42; DEV_CODE; V7 §3.2–3.4|
|7|RF42 lịch sử300 cây|HIST_CODE make RF42; không gán300 cho RF42-Lite|
|10|MacroF1 .863343/.863840; Δ+.0004966899; CI chứa0|TEST macro_f1,mcc; CI official_test; tọa độ CI tuyến tính đúng hai cận|
|13|5 FIT seed×5 arm,60000 FIT,35069 validation cố định|P21 per_seed, protocol; không5 TEST|
|14|F1 RF42 .945220/Stack .944731/RF17 .936751;225.250+84.600=309.850s,RF42241.119s|P21 per_seed, V7 bảng4.11; mean5; selector+model fit, chưa end-to-end|
|15|FPR/FNR ba nhánh, trung bình5seed|P21 metrics_by_arm fpr/fnr; Normal minority|
|16|L=FP+rFN; r=142/118; r1/1.2034/5|TEST fixed counts; chỉ mô hình chi phí giả định|
|17,18–29|Giới hạn, leakage, đóng góp|V7 §3.2–3.6,5.3–5.5; frozen source|

## Danh mục nguồn gốc và chi tiết khoa học đã kiểm tra

'''+oldmap.split('## Nguồn gốc',1)[1].split('## Claim → slide',1)[0]+'\n## Ranh giới bằng chứng\n\nHistorical official TEST và P21 không cùng tập đánh giá. P21 hậu nghiệm official TRAIN; 5 seed chỉ mô tả biến thiên fit có điều kiện trên1validation. stable17 lịch sử chọn trước CV còn selection optimism; không nói pipeline lịch sử hoàn toàn leakage-free. RF17 lịch sử đổi cả cấu hình, không FS-only. Không thuật toán mới, không IDS realtime, không khẳng định Stacking vượt trội.\n')
matrix=(O/'audit/Inherited_Skill_Decision_Matrix.md').read_text(encoding='utf-8')
put('Skill_Decision_Matrix.md','''# Skill Decision Matrix — V2

Humanizer3.1: đã đọc toàn bộ SKILL.md từ blader/humanizer, MIT; áp dụng file/embedded mode, văn phong trung tính. Đã sửa38 đoạn V7, viết lại17 lời nói theo cách diễn đạt tự nhiên, giữ thuật ngữ và công thức trong Q&A. Không dùng như bộ phát hiện AI hoặc cam kết người viết.

OfficeCLI PPTX: đã đọc SKILL local và quy tắc QA, thực hiện independent screenshot judge. Morph PPT: đã đọc skill nền; không dùng Morph trong V2 vì cần timeline trong slide. PPT Master: đọc phần animation/native shape; không chạy engine package. Visual PPT Builder: đọc SKILL/RULES, tự dựng native shapes, không gọi image builder. Mức sử dụng này phân biệt với cài đặt/chạy engine.

Pipeline thực chạy V2: python-pptx→PowerPoint COM MainSequence (motion/scale/entrance)→CreateVideo1080p30→FFmpeg ghép voice. Report: XeLaTeX→BibTeX→XeLaTeX2 lần, font Liberation. Design references: Playwright Chromium fallback có screenshot, ghi rõ các trang bị CAPTCHA. Không dùng GSAP, Manim, Blender hoặc Remotion trong production vì một engine PowerPoint đã đáp ứng animation và chỉnh sửa.

## Hồ sơ khảo sát các công cụ được yêu cầu

Phần dưới kế thừa hồ sơ khảo sát có snapshot trong audit của deck đầu; các mục thực thi cũ không được tính thành sử dụng production V2. Humanizer và native timeline ở trên là thay đổi V2.

'''+matrix)
put('README.md','''# NCKH Ensemble IDS — Creative Rebuild V2

Mở NCKH_Ensemble_IDS_Creative_Final.pptx trong PowerPoint desktop, bắt đầu slide show từ trang1, dùng timing tự động. Deck29trang:17chính/8cảnh/360giây và12phụlụcẩn. Click A1–A12 ở trang kết luận để mở phụ lục rồi “Về kết luận”. Các shape/text/chart đều là đối tượng native. Không embedded narration trong PPTX: lời đọc nằm trong MP4, MP3 và speaker notes để dễ luyện tập/chỉnh sửa.

Xem video NCKH_Ensemble_IDS_Creative_Preview.mp4. Đây là chuyển động thật xuất từ PowerPoint; FFmpeg chỉ chỉnh timestamp nhỏ và ghép voice, không dựng motion thay thế. StaticPDF là trạng thái bố cục cuối, không thể hiện các bước xuất hiện theo thời gian.

Báo cáo V7, LaTeX source zip, change log, Scientific_Integrity_QA và PDF_Comparison_V6_V7 nằm cùng thư mục. V6, deck cũ và kết quả nghiên cứu được giữ nguyên. Xem QA_Report.md trước khi đưa vào buổi bảo vệ; các giới hạn tiếp cận website và kiểm tra TTS được nêu rõ.

Để tái dựng: cài Python3.11, python-pptx, pywin32, numpy, Pillow, lxml, edge-tts; Microsoft PowerPoint desktop và FFmpeg/ffprobe. Chạy build_creative.py --render --video; measure_voice.py; finalize_creative_video.py; audit_native.py; qa_motion_frames.py; write_delivery_docs.py. Chạy tuần tự các tác vụ PowerPoint COM. PDF V7 tái dựng bằng build_report.py với TinyTeX/XeLaTeX và BibTeX.
''')
print('DOCS_WRITTEN')
