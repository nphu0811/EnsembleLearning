from pathlib import Path
import hashlib,json
import win32com.client
O=Path(__file__).resolve().parent;a=win32com.client.DispatchEx('PowerPoint.Application');p=None;rows=[]
try:
 p=a.Presentations.Open(str(O/'NCKH_Ensemble_IDS_Creative_Final.pptx'),True,False,False)
 for i in range(1,18):
  path=O/'renders'/f'slide_{i:02}.png';old=hashlib.sha256(path.read_bytes()).hexdigest();p.Slides(i).Export(str(path),'PNG',1600,900);new=hashlib.sha256(path.read_bytes()).hexdigest();rows.append(dict(slide=i,identical=old==new))
finally:
 if p is not None:p.Close()
 a.Quit()
(O/'audit/main_render_identity.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');assert all(r['identical'] for r in rows);print('17_MAIN_RENDER_IDENTITY_PASS')
