from pathlib import Path
import json,hashlib,zipfile,subprocess,importlib.metadata
O=Path(__file__).resolve().parent
required=['Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf','LaTeX_Revision_V7_Source.zip','Humanizer_Change_Log.md','Scientific_Integrity_QA.md','PDF_Comparison_V6_V7.md','NCKH_Ensemble_IDS_Creative_Final.pptx','NCKH_Ensemble_IDS_Creative_Preview.mp4','NCKH_Ensemble_IDS_Static.pdf','Kich_ban_6_phut_Humanized.md','QnA_Humanized.md','Storyboard_Cinematic.md','Creative_Direction.md','Design_Reference_Study.md','Skill_Decision_Matrix.md','Animation_Manifest.md','Asset_Manifest.md','Scientific_Evidence_Map.md','OLD_DECK_CRITIQUE.md','Contact_Sheet.jpg','README.md']
assert all((O/n).is_file() and (O/n).stat().st_size for n in required)
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
structure=read('audit/native_structure.json');voice=read('audio/measurements.json');vm=read('audit/video_metadata.json');science=read('audit/scientific_verification.json');identity=read('audit/main_render_identity.json');bounds=read('audit/text_bounds.json');motion=read('audit/motion_frame_evidence.json')
assert all(s['timing']==1 for s in structure[:17]);assert sum(s['motion_paths'] for s in structure)==59
assert all(r['remaining']>=1.1 for r in voice)
assert all(science['protected_hashes'].values());assert all(r['identical'] for r in identity)
assert not bounds['flagged'];assert all(max(r['mean_absolute_pixel_differences'])>.01 for r in motion)
video=next(s for s in vm['final']['streams'] if s['codec_type']=='video');assert (video['width'],video['height'])==(1920,1080) and video['r_frame_rate']=='30/1';assert abs(float(vm['final']['format']['duration'])-360)<.05
assert (O/'audit/full_video_decode.log').read_text()==' ' or not (O/'audit/full_video_decode.log').read_text().strip()
report=json.loads((O/'audit/report_v7_qa.json').read_text());assert report['status']=='PASS'
qa=f'''# QA Report — Creative Rebuild V2

Kết quả kỹ thuật: **PASS** cho PPTX có timeline thật, MP4 có motion và dữ liệu truy vết được. Các giới hạn tham khảo website và thẩm âm TTS được ghi riêng bên dưới; không tuyên bố đã hoàn tất những kiểm tra không thực hiện được.

## Ba điều kiện loại trực tiếp

|Gate|Kết quả|Bằng chứng|
|---|---|---|
|FAIL1: chỉ transition|Không vi phạm|17/17 main có p:timing;439 effects,59 motion paths,15 scale;0 Morph,0 page transition effect.568 native shape instances toàn29slide|
|FAIL2: slideshow tĩnh|Không vi phạm|PowerPoint CreateVideo; hero frame sequences cùng slide có packet/node/path/bar/kinetic changes; source và7clip đi kèm|
|FAIL3: sai số/phạm vi|Không phát hiện trong audit|CSV confusion counts đối chiếu, mean P21 đã truy vết; TEST/P21 tách;5 FITseed cùng1validation; cost giả định|

## Kiểm tra thực tế

- V7:38 đoạn biên tập ở LaTeX, XeLaTeX/BibTeX/2pass;49trang so V6 50trang.13 nguồn thành phần, bib, số, công thức và block bảo vệ kiểm tra bằng invariants. Đã render tất cả49trang và xem contact sheets; không missing glyph/ref/overfull. Xem Scientific_Integrity_QA và PDF_Comparison_V6_V7.
- PowerPoint: mở bằng Microsoft PowerPoint COM, render29trang, independent screenshot reviewer PASS sau2vòng sửa. Phụ lục mới được kiểm tra lại riêng. Source không flatten slide thành ảnh; font hỗ trợ tiếng Việt. Có hyperlink A1–A12 và quay về kết luận.
- Bounds:0 flag vượt ngưỡng height2pt/width6pt; {len(bounds.get('minor_glyph_overhang',[]))} text box có glyph overhang nhỏ2–6pt, vẫn trong canvas, đã được visual QA. Sửa kích thước box của các trường hợp lớn; main renders sau save trùng byte với renders đã dùng khi kiểm tra video.
- Main17slide/8cảnh.12Q&Aẩn và bản copy xuất video xóa vật lý12trang này trước CreateVideo; không ghép Q&A vào MP4. PDF tĩnh có29trang gồm phụ lục.
- MP4:1920×1080,30fps,{vm['final']['format']['duration']}giây. Native duration {vm['normalization']['native_seconds']:.6f}s; PTS factor {vm['normalization']['pts_factor']:.9f}. Chỉ chuẩn hóa timestamp nhỏ và ghép audio; không mô phỏng motion ngoài PowerPoint. Full stream decode không báo lỗi.
- Lời đọc17MP3: tổng{sum(r['speech_seconds'] for r in voice):.3f}s, voice HoaiMy−5%. Không tăng tốc audio. Mỗi slot bắt đầu sau0,55s, mọi file kết thúc trước slide kế; khoảng nghỉ thực tế ghi trong script/timeline. Đã rút14 đoạn sau lần đo đầu. Đây là đo TTS thực tế, chưa phải đọc thử của thành viên nhóm.
- V6, code nghiên cứu, frozen CSV/P21/protocol, PPTX/MP4cũ đều giữ nguyênSHA. Không fit/retrain, không mởrawTEST để thiết kế kết quả. Đối chiếu chi tiết ở audit/scientific_verification.json.

## Tự phản biện theo trọng số

|Tiêu chí|Trọng số|Tự đánh giá /10|Nhận xét|
|---|---:|---:|---|
|Khoa học|25%|9,5|Scope rõ, số chính xác; còn giới hạn historical selection trong chính nghiên cứu|
|Graphic design|25%|8,3|Giant type, color arc và graph thủ công; hình học vẫn được giản lược để chiếu phòng thi|
|Motion|20%|8,8|Native paths,scale,progressive chart; dùng fixed camera, không dựng3D|
|Storytelling/Việt|15%|8,4|Một luận điểm xuyên suốt, đo lời đọc; TTS chưa được người Việt nghe duyệt|
|Typography|10%|8,8|Hero150–185pt,body khoảng21–30pt; nguồn chân trang nhỏ để truy vết|
|Chỉnh sửa/ổn định|5%|9,2|Native objects và source; cần PowerPoint desktop và fonts tương ứng|

Điểm có trọng số tự đánh giá:8,81/10; là nhận định của người dựng, không phải điểm hội đồng hay chứng nhận độc lập.

## Giới hạn chưa được xác nhận

1. Lollypop/Designathon trả CAPTCHA; Locomotive/Behance bị chặn; ActiveTheory không hỗ trợ browser. Đã lưu ảnh thật và ledger, không nhận đã quan sát các hiệu ứng scroll của các trang bị chặn. Awwwards quan sát được2vị trí cuộn. Concept được tự dựng, không sao chép template.
2. TTS là giọng luyện tập. Đã kiểm tra thời lượng, decode và đối chiếu ASR tự động: các số FP/FN chính được nhận dạng; ASR base sai nhiều dấu và tên tiếng Anh. Môi trường này không cung cấp khả năng nghe audio cho reviewer, nên **chưa chứng nhận thẩm âm/phát âm tên mô hình**. Cần người trình bày nghe duyệt trước khi dùng voice-over ở buổi bảo vệ. Script chữ và số trên slide là chuẩn đối chiếu, không lấy transcript ASR làm nội dung khoa học.
3. Phụ lục15–25giây là mục tiêu câu trả lời chính, chưa đo giọng cho toàn bộ12đoạn. Hội đồng chọn câu hỏi trong4phút, không đọc lần lượt12câu.
4. Kiểm tra mở/render thực hiện trên PowerPoint của máy này. Không chứng nhận Morph/animation tương đương trên Google Slides, LibreOffice hoặc bản web. Không có narration nhúng trong PPTX; MP4 chứa voice, speaker notes chứa lời nói.

## Hồ sơ chứng cứ

audit/native_structure.json; main_render_identity.json; text_bounds.json; independent_v2_visual_qa.md; motion_frame_evidence.json; video_metadata.json; full_video_decode.log; voice_asr.json; scientific_verification.json; report_v7_qa.json; scientific_source_invariants.json. Contact_Sheet.jpg và hero_animations/*_frames.jpg phục vụ kiểm tra nhanh. `checksums.sha256` bao phủ nội dung release, ZIP được kiểm traCRC.
'''
(O/'QA_Report.md').write_text(qa,encoding='utf-8')
deps=['python-pptx','pywin32','numpy','Pillow','lxml','edge-tts','PyMuPDF','faster-whisper','playwright']
(O/'requirements.txt').write_text('\n'.join(f'{d}=={importlib.metadata.version(d)}' for d in deps)+'\n',encoding='utf-8')
required+=['QA_Report.md','requirements.txt']
files=[O/n for n in required]
files+=list(O.glob('*.py'))+list(O.glob('*.motion.json'))+list(O.glob('*.native_stats.json'))+[O/'timeline.json',O/'main_plan.json']
for sub in ['audit','references','concepts','hero_animations','renders','report_v7/source']:
 files.extend(p for p in (O/sub).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix.lower() not in ['.aux','.log','.out','.toc','.blg','.bbl'])
files+=list((O/'audio').glob('slide_*.mp3'))+[O/'audio/measurements.json']
files=sorted(set(files));entries=[(p,p.relative_to(O).as_posix()) for p in files]
checks='\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+name for p,name in entries)+'\n';(O/'checksums.sha256').write_text(checks,encoding='utf-8')
target=O/'NCKH_Ensemble_IDS_Creative_Delivery.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p,name in entries:z.write(p,name)
 z.write(O/'checksums.sha256','checksums.sha256')
with zipfile.ZipFile(target) as z:assert z.testzip() is None
(O/'audit/release_validation.json').write_text(json.dumps(dict(status='PASS_ARTIFACTS_WITH_DOCUMENTED_LIMITS',zip=str(target),bytes=target.stat().st_size,files=len(entries)+1,required=required,sha256=hashlib.sha256(target.read_bytes()).hexdigest()),indent=2),encoding='utf-8');print('RELEASE_PASS',target.stat().st_size)
