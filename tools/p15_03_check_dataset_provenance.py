"""P15-03A: read-only, bounded-memory validation of original UNSW-NB15 CSVs.

Baseline SHA-256 values were recorded in Phase 3's raw_file_checksums.csv
and independently recovered from the 2026-10-10 audit snapshot. These
are historical local baselines, NOT official UNSW-published hashes.

Never uses or trains any model. Does not write to any data/ or frozen results/.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

RAW_DIR = Path('data/raw/unsw-nb15')
BASELINE = [
    {'file':'UNSW_NB15_training-set.csv','size_bytes':32293018,'sha256':'bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa','rows':175341,'columns':45,'label_counts':{'0':56000,'1':119341}},
    {'file':'UNSW_NB15_testing-set.csv','size_bytes':15380800,'sha256':'734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559','rows':82332,'columns':45,'label_counts':{'0':37000,'1':45332}},
    {'file':'NUSW-NB15_features.csv','size_bytes':4044,'sha256':'c55f19cceebb6360dc50f44f8a5f246ccefbcf8a6c604ac1ad46e643869cafce','rows':None,'columns':None,'label_counts':None}
]

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def inspect_csv(path: Path):
    """Read one CSV row at a time; keep only column names and aggregate counts."""
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.reader(stream)
        header = next(reader)
        missing = sorted(set(['id','label','attack_cat','proto','service','state'])-set(header))
        problems = []
        if missing:
            problems.append('missing_columns:'+','.join(missing))
        label_index = header.index('label') if 'label' in header else None
        label_counts = {'0':0,'1':0}
        count = 0
        for row in reader:
            count += 1
            if len(row) != len(header):
                problems.append('invalid_row_width')
                break
            if label_index is not None:
                value = row[label_index]
                if value in label_counts:
                    label_counts[value] += 1
                else:
                    problems.append('unexpected_label')
                    break
    return {'rows':count, 'columns':len(header), 'label_counts':label_counts, 'header':header, 'problems':problems}


def audit(root: Path, specs=BASELINE):
    root = Path(root).resolve()
    report = {
        'check_id':'P15-03A',
        'generated_utc':datetime.now(timezone.utc).isoformat(),
        'project_root':str(root),
        'python_executable':sys.executable,
        'python_version':platform.python_version(),
        'baseline_source':'Phase3 raw_file_checksums.csv (audit snapshot 2026-10-10); NOT UNSW official checksums',
        'scope':'Original three raw CSV files only; no training or re-evaluation',
        'files':[]
    }
    train_test_headers=[]
    for spec in specs:
        name=spec['file']
        path=root / RAW_DIR / name
        record={'file':name, 'relative_path':str(RAW_DIR/name), 'status':'FAIL', 'checks':{}, 'problems':[]}
        if not path.is_file():
            record['problems'].append('MISSING_FILE')
            report['files'].append(record)
            continue
        actual_size=path.stat().st_size
        actual_sha=file_sha256(path)
        record['actual_size_bytes']=actual_size
        record['actual_sha256']=actual_sha
        record['checks']['size_match']=actual_size==spec['size_bytes']
        record['checks']['hash_match']=actual_sha.lower()==spec['sha256'].lower()
        if spec.get('rows') is not None:
            try:
                info=inspect_csv(path)
                record['rows']=info['rows']
                record['columns']=info['columns']
                record['label_counts']=info['label_counts']
                record['checks']['rows_match']=info['rows']==spec['rows']
                record['checks']['columns_match']=info['columns']==spec['columns']
                record['checks']['labels_match']=info['label_counts']==spec['label_counts']
                record['checks']['schema_valid']=not info['problems']
                record['problems'].extend(info['problems'])
                train_test_headers.append(info['header'])
            except (UnicodeError, csv.Error, ValueError, StopIteration, OSError) as exc:
                record['problems'].append('CSV_READ_FAILURE:'+type(exc).__name__)
        if not all(record['checks'].values()) or record['problems']:
            for check, passed in record['checks'].items():
                if not passed:
                    record['problems'].append(check)
        else:
            record['status']='PASS'
        report['files'].append(record)
    report['train_test_columns_identical']=(len(train_test_headers)==2 and train_test_headers[0]==train_test_headers[1]) if len(specs)==3 else None
    if report['train_test_columns_identical'] is False:
        report['problems']=['TRAIN_TEST_SCHEMA_MISMATCH']
    report['status']='PASS' if all(f['status']=='PASS' for f in report['files']) and report['train_test_columns_identical'] is not False else 'FAIL'
    report['warning']='A PASS validates local raw files against a historical audit, not the exact URL/location from which the files were originally downloaded.'
    return report


def main() -> int:
    parser=argparse.ArgumentParser(description='Read-only UNSW-NB15 raw file provenance verification (P15-03A).')
    parser.add_argument('--project-root',type=Path,default=Path('.'))
    parser.add_argument('--out',type=Path,default=Path('results/reproducibility/p15_03_dataset/p15_03_dataset_integrity.json'))
    args=parser.parse_args()
    root=args.project_root.resolve()
    out=(root / args.out).resolve() if not args.out.is_absolute() else args.out.resolve()
    if out.exists():
        print('REFUSED_OVERWRITE: '+str(out))
        print('Pass a different --out filename if you need a second audit.')
        return 3
    if not out.is_relative_to(root / 'results' / 'reproducibility'):
        print('REFUSED_OUTSIDE_AUDIT_DIR: output must be under results/reproducibility/')
        return 3
    report=audit(root)
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
        f.write('\n')
    for f in report['files']:
        print(f"{f['file']}: {f['status']} {', '.join(f['problems'])}")
    print('P15-03A DATA INTEGRITY: '+report['status'])
    print('Report: '+str(out))
    return 0 if report['status']=='PASS' else 2

if __name__=='__main__':
    raise SystemExit(main())
