from pathlib import Path
import json,re,hashlib,difflib,zipfile
import pymupdf
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;ROOT=O.parents[2]
pdf=O/'Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf';d=pymupdf.open(pdf)
old=pymupdf.open(ROOT/'exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf')
render=O/'report_v7/renders';render.mkdir(exist_ok=True)
rows=[]
for i,p in enumerate(d):
 path=render/f'page_{i+1:02}.png';p.get_pixmap(matrix=pymupdf.Matrix(1.15,1.15)).save(path)
 outside=[w[4] for w in p.get_text('words') if w[0]<0 or w[1]<0 or w[2]>p.rect.width+.5 or w[3]>p.rect.height+.5]
 rows.append({'page':i+1,'words':len(p.get_text('words')),'outside_page':outside,'replacement_character':'\ufffd' in p.get_text(),'unresolved_marker':'??' in p.get_text()})
for batch in range((len(d)+19)//20):
 sheet=Image.new('RGB',(1250,4*375),'#dbe3ec');draw=ImageDraw.Draw(sheet)
 for j,i in enumerate(range(batch*20,min(len(d),(batch+1)*20))):
  im=Image.open(render/f'page_{i+1:02}.png');im.thumbnail((240,340));x=(j%5)*250;y=(j//5)*375;sheet.paste(im,(x,y));draw.text((x+8,y+344),f'V7 p.{i+1}',fill='black')
 sheet.save(O/f'report_v7/contact_{batch+1:02}.jpg')
text='\n'.join(p.get_text() for p in d);oldtext='\n'.join(p.get_text() for p in old)
(O/'audit/V7_full_text.txt').write_text(text,encoding='utf-8')
(O/'audit/PDF_text_comparison.patch').write_text(''.join(difflib.unified_diff(oldtext.splitlines(True),text.splitlines(True),fromfile='V6 PDF',tofile='V7 PDF')),encoding='utf-8')
log=(O/'report_v7/source/main_revision_v7_2026_10_19.log').read_text(encoding='utf-8',errors='replace')
warnings=[x for x in log.splitlines() if re.search(r'Overfull|Missing character:|Citation .*undefined|There were undefined references|Reference .*undefined',x)]
inv=json.loads((O/'audit/scientific_source_invariants.json').read_text(encoding='utf-8'))
passed=not warnings and all(not x['outside_page'] and not x['replacement_character'] and not x['unresolved_marker'] for x in rows) and inv['status']=='PASS'
result={'status':'PASS_AUTOMATED_PENDING_VISUAL_REVIEW' if passed else 'FAIL','v6_pages':len(old),'v7_pages':len(d),'v6_sha256':hashlib.sha256((ROOT/'exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf').read_bytes()).hexdigest(),'v7_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'latex_warnings':warnings,'pages':rows,'edited_passages':len(json.loads((O/'audit/humanizer_edits.json').read_text(encoding='utf-8')))}
(O/'audit/report_v7_qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['pages']},ensure_ascii=False))
