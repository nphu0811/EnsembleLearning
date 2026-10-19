from pathlib import Path
import json,hashlib
import win32com.client
from creative_content import MAIN
from creative_qna import ANSWERS
O=Path(__file__).resolve().parent
plan=json.loads((O/'NCKH_Ensemble_IDS_Creative_Final.motion.json').read_text(encoding='utf-8'))
for i,row in enumerate(MAIN):plan[i]['speech']=row[4]
for i,answer in enumerate(ANSWERS,17):plan[i]['speech']=answer
(O/'NCKH_Ensemble_IDS_Creative_Final.motion.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');(O/'main_plan.json').write_text(json.dumps(plan[:17],ensure_ascii=False,indent=2),encoding='utf-8')
flags=json.loads((O/'audit/text_bounds.json').read_text(encoding='utf-8'))['flagged'];a=win32com.client.DispatchEx('PowerPoint.Application');p=None;identity=[]
try:
 p=a.Presentations.Open(str(O/'NCKH_Ensemble_IDS_Creative_Final.pptx'),False,False,False)
 for i,row in enumerate(MAIN,1):
  ns=p.Slides(i).NotesPage
  for q in ns.Shapes:
   if q.Type==14 and q.PlaceholderFormat.Type==2:q.TextFrame.TextRange.Text=f'Cảnh {row[0]} | {row[1]} giây\n'+row[4]
 for f in flags:
  q=p.Slides(f['slide']).Shapes(f['shape'])
  q.Height=max(q.Height,f['bound_height']+2);q.Width=max(q.Width,f['bound_width']+2)
 for j,answer in enumerate(ANSWERS,18):
  p.Slides(j).Shapes('text-6').TextFrame.TextRange.Text=answer
  p.Slides(j).Shapes('text-6').Width=9.7*72
  for q in p.Slides(j).NotesPage.Shapes:
   if q.Type==14 and q.PlaceholderFormat.Type==2:q.TextFrame.TextRange.Text=answer
 p.Save()
 for i in sorted(set(f['slide'] for f in flags)):
  path=O/'renders'/f'slide_{i:02}.png';old=hashlib.sha256(path.read_bytes()).hexdigest();p.Slides(i).Export(str(path),'PNG',1600,900);new=hashlib.sha256(path.read_bytes()).hexdigest();identity.append(dict(slide=i,render_identical=old==new))
 for i in range(18,30):p.Slides(i).Export(str(O/'renders'/f'slide_{i:02}.png'),'PNG',1600,900)
 for s in p.Slides:s.SlideShowTransition.Hidden=False
 p.SlideShowSettings.RangeType=1;p.SaveAs(str(O/'NCKH_Ensemble_IDS_Static.pdf'),32)
finally:
 if p is not None:p.Saved=True;p.Close()
 a.Quit()
if identity:(O/'audit/bounds_render_identity.json').write_text(json.dumps(identity,indent=2),encoding='utf-8')
print(identity)
