from pathlib import Path
import json
import win32com.client
O=Path(__file__).resolve().parent
old=json.loads((O/'audit/text_overflow_com.json').read_text(encoding='utf-8'))
a=win32com.client.DispatchEx('PowerPoint.Application');p=None
try:
 p=a.Presentations.Open(str(O/'NCKH_Ensemble_IDS_Final.pptx'),True,False,False)
 rows=[]
 for v in old:
  q=p.Slides(v['slide']).Shapes(v['shape'])
  rows.append({'slide':v['slide'],'shape':v['shape'],'height':q.Height,'bound_height':q.TextFrame2.TextRange.BoundHeight})
 result={'status':'PASS' if all(x['height']>=x['bound_height'] for x in rows) else 'FAIL','rows':rows}
 (O/'audit/textframe_repair_verified.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result['status'])
finally:
 if p is not None:p.Close()
 a.Quit()
