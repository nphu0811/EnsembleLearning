"""Hash a tracked research snapshot for review; never builds a release archive.

Mutable research memory and the inventory itself are excluded to avoid recursive
hash updates. Presence in this inventory does not grant redistribution rights.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',required=True,type=Path)
    args=parser.parse_args();out=args.out_dir.resolve();out.mkdir(parents=True,exist_ok=False)
    files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode('utf-8').split('\0')
    rows=[];forbidden=[]
    for name in sorted(set(files)-{''}):
        if name.startswith('.research_memory/') or name.startswith(out.relative_to(ROOT).as_posix()+'/'):
            continue
        p=ROOT/name
        if not p.is_file():continue
        lower=name.lower();parts=lower.split('/')
        banned=(lower.startswith('data/raw/') or any(x.startswith('.venv') or x in ('venv','__pycache__') for x in parts)
                or p.suffix.lower() in ('.joblib','.pkl','.pickle') or p.name.lower() in ('.env','credentials.json','id_rsa'))
        if banned:forbidden.append(name)
        review=('THIRD_PARTY_RIGHTS_REVIEW' if lower.startswith(('templates/','literature/')) or p.suffix.lower()=='.zip'
                else 'PROJECT_LICENSE_UNCONFIRMED')
        digest=hashlib.sha256()
        with p.open('rb') as stream:
            for block in iter(lambda:stream.read(1048576),b''):digest.update(block)
        rows.append(dict(path=name,bytes=p.stat().st_size,sha256=digest.hexdigest(),distribution_status=review,
                         forbidden_new_release_path=banned))
    with (out/'review_inventory.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result=dict(files=len(rows),forbidden_tracked_paths=forbidden,passed=not forbidden,
                scope='TRACKED_REVIEW_SNAPSHOT; excludes mutable research memory; no archive, license grant, or secret-content audit',
                code_license_files=subprocess.check_output(['git','ls-files','*LICENSE*','*LICENCE*'],cwd=ROOT,text=True).splitlines(),
                source_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    (out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))
    return int(not result['passed'])


if __name__=='__main__':raise SystemExit(main())
