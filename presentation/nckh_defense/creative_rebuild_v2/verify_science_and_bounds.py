from pathlib import Path
import json,hashlib,csv
import win32com.client
import pymupdf
O=Path(__file__).resolve().parent;R=O.parents[2]
expected=json.loads((O.parent/'audit/protected_sources_sha256.json').read_text())
expected.update({str(O.parent.relative_to(R)/n):h for n,h in json.loads((O/'audit/old_deck_metrics.json').read_text())['sha256'].items()})
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in expected.items()};assert all(hashes.values()),hashes
with (R/'results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv').open() as f:rows=list(csv.DictReader(f))
rf=next(x for x in rows if x['pipeline']=='random_forest_42' and x['eval_view']=='official_test');st=next(x for x in rows if x['pipeline']=='stacking_42' and x['eval_view']=='official_test')
assert (int(rf['fp']),int(st['fp']),int(rf['fn']),int(st['fn']))==(10003,9861,734,852)
assert int(st['fp'])-int(rf['fp'])==-142 and int(st['fn'])-int(rf['fn'])==118
assert abs(142/118-1.2033898305084745)<1e-12
doc=pymupdf.open(O/'NCKH_Ensemble_IDS_Static.pdf');assert len(doc)==29
pdfissues=[]
for i,p in enumerate(doc):
 if '\ufffd' in p.get_text():pdfissues.append({'slide':i+1,'issue':'replacement glyph'})
assert not pdfissues
a=win32com.client.DispatchEx('PowerPoint.Application');p=None;bounds=[]
try:
 p=a.Presentations.Open(str(O/'NCKH_Ensemble_IDS_Creative_Final.pptx'),True,False,False)
 for i in range(1,30):
  for q in p.Slides(i).Shapes:
   if q.HasTextFrame and q.TextFrame.HasText:
    tf=q.TextFrame2;tr=tf.TextRange
    bounds.append(dict(slide=i,shape=q.Name,text=q.TextFrame.TextRange.Text[:70],height=float(q.Height),bound_height=float(tr.BoundHeight),width=float(q.Width),bound_width=float(tr.BoundWidth)))
finally:
 if p is not None:p.Close()
 a.Quit()
over=[r for r in bounds if r['bound_height']>r['height']+2 or r['bound_width']>r['width']+6]
minor=[r for r in bounds if r['width']+2<r['bound_width']<=r['width']+6]
# COM bounds include glyph overhang; retain all flagged rows for visual adjudication.
(O/'audit/text_bounds.json').write_text(json.dumps(dict(flagged=over,minor_glyph_overhang=minor,width_tolerance_pt=6,height_tolerance_pt=2,rows=bounds),ensure_ascii=False,indent=2),encoding='utf-8')
(O/'audit/scientific_verification.json').write_text(json.dumps(dict(protected_hashes=hashes,confusion_counts_verified=True,cost_crossing=142/118,static_pdf_pages=len(doc),pdf_glyph_issues=pdfissues,com_bound_flags=len(over)),indent=2),encoding='utf-8')
print('SCIENCE_HASH_PDF_PASS; COM flags',len(over));print(json.dumps(over,ensure_ascii=True))
