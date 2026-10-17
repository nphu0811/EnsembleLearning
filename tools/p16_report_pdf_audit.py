"""Audit an author-supplied report PDF without modifying it; render with Poppler."""
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    pdf = args.pdf.resolve()
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    doc = pymupdf.open(pdf)
    checks, pages = [], []

    def check(name, passed, detail=''):
        checks.append(dict(check=name,passed=bool(passed),detail=detail))

    def table(rel):
        with (ROOT/rel).open(encoding='utf-8-sig',newline='') as stream:
            return list(csv.DictReader(stream))

    check('accepted snapshot hash', digest == '8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b')
    check('37 pages', len(doc) == 37)
    for i,page in enumerate(doc):
        text=page.get_text()
        spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
        outside=[s['text'] for s in spans if not (page.rect+(-1,-1,1,1)).contains(pymupdf.Rect(s['bbox']))]
        check(f'page {i+1}: A4', abs(page.rect.width-595.276)<1 and abs(page.rect.height-841.89)<1)
        check(f'page {i+1}: no replacement character', '\ufffd' not in text)
        check(f'page {i+1}: no off-page text', not outside)
        images=[dict(width_px=img[2],height_px=img[3],dpi=[72*img[2]/r.width,72*img[3]/r.height])
                for img in page.get_images(full=True) for r in page.get_image_rects(img[0])]
        pages.append(dict(physical_page=i+1,min_text_pt=min(s['size'] for s in spans),
                          under_8pt=[dict(text=s['text'],size=s['size']) for s in spans if s['size']<8],
                          images=images,outside=outside,text=text))
    texts=[r['text'] for r in pages]
    final=table('results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv')
    for row in final:
        if row['eval_view']=='official_test':
            expected=[f'{float(row["macro_f1"]):.6f}', f'{float(row["mcc"]):.6f}',
                      f'{100*float(row["false_positive_rate"]):.4f}', f'{100*float(row["false_negative_rate"]):.4f}',row['fp'],row['fn']]
            for value in expected:
                check('PDF table 4.1 '+row['pipeline']+'/'+value, value in texts[26].split())
        else:
            check('PDF table 4.5 '+row['pipeline'],f'{float(row["macro_f1"]):.6f}' in texts[29])
    for row in table('results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv'):
        if (row['eval_view'],row['model_a'],row['model_b'])==('official_test','stacking_42','random_forest_42'):
            for field in ('delta_a_minus_b','ci_lower','ci_upper'):
                value=f'{float(row[field]):+.6f}'
                check('PDF table 4.2 '+row['metric']+'/'+field,value in texts[27].split())
    for row in table('results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv'):
        for field,digits in [('train_time_seconds',3),('inference_ms_per_sample',6),('serialized_model_size_mb',3)]:
            value=f'{float(row[field]):.{digits}f}'
            check('PDF table 4.3 '+row['pipeline']+'/'+field,value in texts[28].split())
    for number in ['6062','621','754','+133','18871','57','14','-43','20399','56','84','+28','45332','734','852','+118']:
        check('PDF table 4.4 value '+number,number in texts[29].split())
    check('PDF Holm p', '0.468377' in texts[27])
    check('FP delta label','-142' in texts[27])
    check('FN delta label','+118' in texts[27])
    # The seven figures and ten tables are unique body captions; ignore lists.
    figure_labels=[];table_labels=[]
    for text in texts[9:]:
        figure_labels += re.findall(r'Hình\s+(\d+\.\d+)\.',text)
        table_labels += re.findall(r'Bảng\s+(\d+\.\d+)\.',text)
    expected_fig=['1.1','2.1','2.2','2.3','2.4','4.1','4.2']
    expected_tables=['2.1','2.2','3.1','4.1','4.2','4.3','4.4','4.5','5.1','5.2']
    check('seven body figure captions',sorted(figure_labels)==sorted(expected_fig),str(figure_labels))
    check('ten body table captions',sorted(table_labels)==sorted(expected_tables),str(table_labels))
    poppler=shutil.which('pdftoppm')
    if not poppler: raise RuntimeError('Poppler pdftoppm unavailable; do not claim second-renderer QA')
    render=ROOT/'tmp/pdfs'/out.name
    render.mkdir(parents=True,exist_ok=False)
    subprocess.run([poppler,'-r','100','-png',str(pdf),str(render/'page')],check=True,capture_output=True)
    page_files=sorted(render.glob('page-*.png'))
    check('Poppler rendered all pages',len(page_files)==len(doc))
    # Contact sheets are QA diagnostics, never replacements for source figures.
    sheets=[]
    for start in range(0,len(page_files),9):
        canvas=Image.new('RGB',(1050,1530),'#dddddd');draw=ImageDraw.Draw(canvas)
        for offset,path in enumerate(page_files[start:start+9]):
            image=Image.open(path).convert('RGB');image.thumbnail((340,475))
            x=(offset%3)*350+(350-image.width)//2;y=(offset//3)*510+24
            canvas.paste(image,(x,y));draw.text((x,y-18),f'Physical page {start+offset+1}',fill='black')
        name=f'contact_{start+1:02d}_{min(start+9,len(doc)):02d}.png'
        canvas.save(out/name);sheets.append(name)
    check('input PDF hash unchanged',hashlib.sha256(pdf.read_bytes()).hexdigest()==digest)
    report=dict(pdf_source=str(pdf),sha256=digest,pages=len(doc),checks=checks,
                pass_count=sum(r['passed'] for r in checks),fail_count=sum(not r['passed'] for r in checks),
                page_details=pages,contact_sheets=sheets,rendered_pages_directory=str(render),
                render_engine='Poppler pdftoppm 100 dpi',geometry_engine='PyMuPDF '+pymupdf.VersionBind,
                scope='Read-only; no report edits, no dataset read, no fit/predict; automated bounds are not an overlap proof.')
    (out/'pdf_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('sha256','pages','pass_count','fail_count','contact_sheets')}))
    for row in checks:
        if not row['passed']: print('FAIL:',row)
    return int(report['fail_count']>0)


if __name__=='__main__':
    raise SystemExit(main())
