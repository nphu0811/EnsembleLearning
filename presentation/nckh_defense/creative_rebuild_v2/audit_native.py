from pathlib import Path
import zipfile,json,hashlib,subprocess
from lxml import etree as E
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;ROOT=O.parents[2]
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
ppt=O/'NCKH_Ensemble_IDS_Creative_Final.pptx';rows=[]
with zipfile.ZipFile(ppt) as z:
 for i in range(1,30):
  x=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
  ids=set(x.xpath('//p:cNvPr/@id',namespaces=N));targets=x.xpath('//p:spTgt/@spid',namespaces=N)
  shape_count=len(x.xpath('//p:spTree/*[self::p:sp or self::p:cxnSp or self::p:pic or self::p:graphicFrame or self::p:grpSp]',namespaces=N))
  rows.append(dict(slide=i,hidden=x.get('show')=='0',shapes=shape_count,timing=len(x.xpath('//p:timing',namespaces=N)),motion_paths=len(x.xpath('//p:animMotion',namespaces=N)),scale=len(x.xpath('//p:animScale',namespaces=N)),transitions=len(x.xpath('//p:transition/*',namespaces=N)),effects=len(x.xpath('//p:cTn[@presetID]',namespaces=N)),target_refs_valid=all(t in ids for t in targets)))
 assert all(r['timing']==1 and r['motion_paths']+r['effects']>0 for r in rows[:17])
 assert all(r['hidden'] for r in rows[17:]);assert all(r['target_refs_valid'] for r in rows)
(O/'audit/native_structure.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
fs=[O/'renders'/f'slide_{i:02}.png' for i in range(1,30)]
im=Image.new('RGB',(1600,8*245),'#ddd');dr=ImageDraw.Draw(im)
for i,f in enumerate(fs):
 im.paste(Image.open(f).resize((400,225)),((i%4)*400,(i//4)*245));dr.text(((i%4)*400+8,(i//4)*245+228),f'Slide {i+1:02}',fill='black')
im.save(O/'Contact_Sheet.jpg')
print(json.dumps({'main_timing_slides':sum(r['timing'] for r in rows[:17]),'motion_paths':sum(r['motion_paths'] for r in rows),'scales':sum(r['scale'] for r in rows),'effects':sum(r['effects'] for r in rows),'native_shapes':sum(r['shapes'] for r in rows),'hidden_QA':sum(r['hidden'] for r in rows)}))
