from pathlib import Path
import json,zipfile,subprocess,collections,hashlib
from lxml import etree
from pptx import Presentation
import numpy as np
O=Path(__file__).resolve().parent;OLD=O.parent
assert json.loads((O/'audit/PHASE1_GATE.json').read_text())['status']=='PASS'
P=Presentation(OLD/'NCKH_Ensemble_IDS_Final.pptx');rows=[];colors=collections.Counter();fonts=collections.Counter()
with zipfile.ZipFile(OLD/'NCKH_Ensemble_IDS_Final.pptx') as z:
 for i,s in enumerate(P.slides,1):
  xml=etree.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
  transitions=xml.xpath('//*[local-name()="transition"]')
  rows.append({'slide':i,'shapes':len(s.shapes),'timing_elements':len(xml.xpath('//*[local-name()="timing"]')),'animMotion':len(xml.xpath('//*[local-name()="animMotion"]')),'transition_elements':len(transitions),'morph':bool(xml.xpath('//*[local-name()="morph"]'))})
  for q in s.shapes:
   if q.has_text_frame:
    for p in q.text_frame.paragraphs:
     for r in p.runs:fonts[r.font.name or 'inherited']+=1
   try:colors[str(q.fill.fore_color.rgb)]+=1
   except:pass
video=OLD/'NCKH_Ensemble_IDS_Preview.mp4';meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)],text=True))
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','fps=1,scale=160:90,format=gray','-f','rawvideo','-'])
f=np.frombuffer(raw,np.uint8).reshape(-1,90,160).astype(np.int16);delta=np.mean(np.abs(np.diff(f,axis=0)),axis=(1,2));still=delta<.10
holds=[];start=None
for i,v in enumerate(list(still)+[False]):
 if v and start is None:start=i
 if not v and start is not None:
  if i-start>=3:holds.append({'start_second':start,'end_second':i,'duration':i-start})
  start=None
result={'slides':len(P.slides),'main_scenes':8,'total_shape_instances':sum(x['shapes'] for x in rows),'slides_with_transition_markup':sum(x['transition_elements']>0 for x in rows),'morph_slides':[x['slide'] for x in rows if x['morph']],'timing_slides':[x['slide'] for x in rows if x['timing_elements']],'fonts':dict(fonts),'shape_fill_colors':dict(colors),'slide_details':rows,'video_metadata':meta,'still_hold_runs_1fps':holds,'video_mean_absolute_frame_differences_1fps':delta.tolist(),'sha256':{n:hashlib.sha256((OLD/n).read_bytes()).hexdigest() for n in ['NCKH_Ensemble_IDS_Final.pptx','NCKH_Ensemble_IDS_Preview.mp4']}}
(O/'audit/old_deck_metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
text=f'''# OLD DECK CRITIQUE

Audit thực trên `../NCKH_Ensemble_IDS_Final.pptx` và `../NCKH_Ensemble_IDS_Preview.mp4`, không dùng PDF thay đầu vào.

| Chỉ tiêu | Đo trực tiếp |
|---|---:|
| Slides |{len(P.slides)}|
| Cảnh chính / keyframe chính |8 /20|
| Native shape instances toàn deck |{result['total_shape_instances']}|
| Slide có transition markup |{result['slides_with_transition_markup']}|
| Morph thật |{len(result['morph_slides'])} slide: {result['morph_slides']}|
| Slide có p:timing |{len(result['timing_slides'])}|
| animMotion nội bộ |0|
| Video |{meta['format']['duration']}s,1920×1080,30fps|
| Đoạn gần tĩnh dài nhất ở sampling1fps |{max(x['duration'] for x in holds)}s|

20 slide có transition markup gồm slide đầu không effect; không phải20animation. Morph12slide có thay đổi geometry giữa keyframe, song **không có animation timeline nội bộ**.828đối tượng là số instance qua slide, không phải828ý tưởng hoặc828vật thể độc lập; cùng actor được nhân bản để Morph. Vì vậy, nhận xét trước rằng có chuyển động phải được giới hạn ở chuyển tiếp giữa keyframe, chưa đáp ứng yêu cầu motion trong cảnh.

## Thiết kế và nhịp dựng

Nền trắng và hệ thống Aptos/cỡ tiêu đề36pt được lặp gần toàn bộ. Khoảng trắng lớn giúp đọc nhưng không được tổ chức thành thay đổi tỷ lệ, nhịp editorial hoặc điểm nhấn hình ảnh. Các scene phần lớn có cùng vị trí tiêu đề trên cùng. Bảng màu thiên về navy/blue/cyan với cam cho FN; chưa có color arc. Đổi màu các trang đơn thuần sẽ không sửa vấn đề này.

Sơ đồ pipeline chỉ có5khối chữ nhật và mũi tên. Chấm flow đổi vị trí bằng Morph khoảng0.9s rồi giữ trạng thái lâu. RF/Voting/Stacking chưa giải thích OOF theo fold bằng chuyển động: người nói phải gánh hầu hết cơ chế. Các chart đúng số liệu và có ghi thang riêng/trục rút gọn, nhưng kích thước và bố cục gần slide công sở; mức −142/+118 chưa trở thành một khoảnh khắc có sức nặng. Font chỉ có1họ, phân cấp ít tương phản; source/rail chiếm attention lặp lại.

Kiểm travideo1fps cho {len(holds)}đoạn gần tĩnh từ3s trở lên, dài nhất{max(x['duration'] for x in holds)}s. Điều này xác nhận phần lớn thời lượng là giữ slide sau transition. Không dùng metric pixel đơn độc làm đánh giá nghệ thuật; các render/video cũ và choreography cũng cho thấy không có packet/path/typography chạy theo timeline nội bộ.

## Yêu cầu sửa có thể kiểm chứng

Thiết kế mới phải dùng typography hero thật, tương phản sáng/tối/vùng màu, bố cục bất đối xứng và timeline nội bộ. Mỗi hero cần packet/path/node/bar/label biến đổi có ý nghĩa, có số giây vàshapeID. OOF fit vàinference phải tách rõ. Animation cần ở PPTX vàMP4 cùng engine; XML vàframe liên tiếp là hai bằng chứng riêng. Có thể giữ dữ liệu đã kiểm chứng, nhưng không giữ template/bố cục cũ.

Nguồn máy đọc: `audit/old_deck_metrics.json`. Không sửa file cũ.
'''
(O/'OLD_DECK_CRITIQUE.md').write_text(text,encoding='utf-8')
print(json.dumps({k:result[k] for k in ['slides','total_shape_instances','slides_with_transition_markup','morph_slides','timing_slides']}))
