"""One-session read-only evidence audit and original-template preservation.

No model fit/predict, no inference and no raw row analysis. Existing evidence is
hashed, not rewritten. Run from workspace root. Outputs refuse replacement.
"""
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import math
import platform
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/reproducibility/resume_2026_10_16/bootstrap'

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)

def save_csv(path, rows, fields):
    with path.open('x', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def read_csv(rel):
    with (ROOT / rel).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    # Snapshot all existing research bytes before writing any new templates/docs.
    rows = []
    for base in ['data', 'src', 'config', 'notebook', 'results',
                 'DE-TAI-NCKHSV-15', 'nckh_codex_handoff']:
        for p in sorted((ROOT / base).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and OUT not in p.parents:
                rows.append({'path':p.relative_to(ROOT).as_posix(),
                             'bytes':p.stat().st_size, 'sha256':digest(p)})
    save_csv(OUT / 'preservation_manifest.csv', rows, ['path','bytes','sha256'])
    inventory=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and not any(x in p.parts for x in ['.git','__pycache__','.kilo']):
            inventory.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size})
    save_csv(OUT / 'workspace_inventory.csv', inventory, ['path','bytes'])

    old_memory = OUT / 'starter_memory'
    shutil.copytree(ROOT / '.research_memory', old_memory)
    sources = [Path('C:/Users/admin/Downloads/DE-TAI-NCKHSV-15.zip'),
               Path('C:/Users/admin/Downloads/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx')]
    original = ROOT / 'templates/original'
    original.mkdir(parents=True, exist_ok=True)
    copied=[]
    for src in sources:
        dst=original / src.name
        if dst.exists():
            raise RuntimeError(f'Refuse overwrite {dst}')
        shutil.copy2(src,dst)
        copied.append({'source':str(src),'destination':dst.relative_to(ROOT).as_posix(),
                       'sha256':digest(dst),'same_bytes':digest(src)==digest(dst)})
    comparisons=[]
    with zipfile.ZipFile(original / sources[0].name) as z:
        assert z.testzip() is None
        for item in z.infolist():
            rel=Path(item.filename)
            assert not rel.is_absolute() and '..' not in rel.parts
            if item.is_dir():
                continue
            target=original / 'latex' / rel
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as f:
                f.write(z.read(item))
            existing=ROOT / 'DE-TAI-NCKHSV-15' / rel
            comparisons.append({'entry':item.filename,'sha256':digest(target),
                'existing_sha256':digest(existing) if existing.is_file() else None,
                'existing_matches_zip':existing.is_file() and digest(target)==digest(existing)})
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(original / sources[1].name) as z:
        assert z.testzip() is None
        root=ET.fromstring(z.read('word/document.xml'))
        body=root.find('w:body',ns)
        blocks=[]
        for index,el in enumerate(body):
            if el.tag.endswith('}p'):
                blocks.append({'body_index':index,'type':'paragraph',
                    'text':''.join(x.text or '' for x in el.findall('.//w:t',ns))})
            elif el.tag.endswith('}tbl'):
                blocks.append({'body_index':index,'type':'table','rows':[
                    [' | '.join(''.join(t.text or '' for t in p.findall('.//w:t',ns))
                     for p in cell.findall('w:p',ns)) for cell in row.findall('w:tc',ns)]
                    for row in el.findall('w:tr',ns)]})
        save_json(OUT / 'proposal_template_structure.json', blocks)
    save_json(OUT / 'template_audit.json', {'copied_originals':copied,
        'zip_contains_docx':False,'zip_entries':comparisons,
        'docx_table_count':len([b for b in blocks if b['type']=='table']),
        'scope':'ZIP and OOXML structural inspection; visual rendering NOT performed'})

    skills=[]
    for base in [Path('C:/Users/admin/.codex/skills'),Path('C:/Users/admin/.agents/skills')]:
        for p in sorted(base.glob('nature-*/SKILL.md')):
            txt=p.read_text(encoding='utf-8-sig')
            name=re.search(r'^name:\s*(.+)',txt,re.M)
            skills.append({'folder':p.parent.name,'registered_name':name.group(1).strip() if name else '',
                'skill_path':str(p),'sha256':digest(p),'loaded':False})
    save_csv(OUT / 'nature_skill_registry.csv', skills,
             ['folder','registered_name','skill_path','sha256','loaded'])

    checks=[]
    metadata=json.loads((ROOT / 'results/ablation/unsw_nb15/phase13_ablation/analysis_metadata.json').read_text())
    for rel,expected in metadata['inputs_sha256'].items():
        p=ROOT / rel
        checks.append({'check':'P13 input hash','path':rel,
            'pass':p.is_file() and digest(p)==expected})
    metrics=read_csv('results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv')
    closure=read_csv('results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv')
    for row in metrics:
        tn,fp,fn,tp=[int(row[c]) for c in ['tn','fp','fn','tp']]
        prec=tp/(tp+fp); recall=tp/(tp+fn)
        f1=2*tp/(2*tp+fp+fn); normal_f1=2*tn/(2*tn+fp+fn)
        n=tn+fp+fn+tp
        expected={'accuracy':(tp+tn)/n,'balanced_accuracy':(recall+tn/(tn+fp))/2,
            'precision':prec,'recall_detection_rate':recall,'f1':f1,
            'macro_f1':(f1+normal_f1)/2,'false_positive_rate':fp/(tn+fp),
            'false_negative_rate':fn/(tp+fn),
            'mcc':(tp*tn-fp*fn)/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))}
        for key,value in expected.items():
            checks.append({'check':f'{row["pipeline"]}/{row["eval_view"]}/{key}',
                'pass':math.isclose(float(row[key]),value,abs_tol=1e-12,rel_tol=1e-12)})
        matches=[r for r in closure if r['pipeline']==row['pipeline'] and r['eval_view']==row['eval_view']]
        assert len(matches)==1
        weighted=(f1*(tp+fn)+normal_f1*(tn+fp))/n
        checks.append({'check':f'{row["pipeline"]}/{row["eval_view"]}/closure_weighted_f1',
            'pass':math.isclose(float(matches[0]['weighted_f1']),weighted,abs_tol=1e-12)})
    save_json(OUT / 'saved_evidence_checks.json', {'checks':checks,
        'all_pass':all(c['pass'] for c in checks),
        'scope':'P13 input hashes and saved aggregate confusion metrics only; no model replay'})
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],
                          cwd=ROOT,capture_output=True,text=True)
    (OUT / 'unit_tests.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    versions={}
    for package in ['pandas','numpy','scipy','scikit-learn','matplotlib','python-docx','Pillow']:
        try: versions[package]=importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError: versions[package]='NOT_INSTALLED'
    save_json(OUT / 'session_environment.json',{'generated_utc':datetime.now(timezone.utc).isoformat(),
        'python':platform.python_version(),'executable':sys.executable,'platform':platform.platform(),
        'packages':versions,'original_training_environment':'UNKNOWN',
        'render_tools':{k:shutil.which(k) for k in ['pdflatex','xelatex','latexmk','tectonic','soffice','pandoc']},
        'test_returncode':result.returncode})
    print(json.dumps({'preserved_files':len(rows),'inventory_files':len(inventory),
        'nature_skills':len(skills),'zip_entries':len(comparisons),
        'zip_differences':sum(not x['existing_matches_zip'] for x in comparisons),
        'evidence_checks':len(checks),'evidence_pass':all(x['pass'] for x in checks),
        'unit_test_exit':result.returncode},indent=2))
    return 0 if all(x['pass'] for x in checks) and result.returncode==0 else 1

if __name__=='__main__':
    raise SystemExit(main())
