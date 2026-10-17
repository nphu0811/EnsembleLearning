"""Audit current report citations against saved verified metadata and reading scopes.

Offline evidence reuse, not a fresh publisher query or full-text verification.
This parser intentionally supports the existing one-braced-field-per-line BibTeX
files only; it is not a general BibTeX parser.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[1]


def norm(text):
    return re.sub(r'[^a-z0-9]+','',unicodedata.normalize('NFKD',text.replace('\\&','&')).encode('ascii','ignore').decode().lower())


def parse(text):
    records={}
    for block in re.split(r'(?=^@)',text,flags=re.M):
        head=re.match(r'@\w+\{([^,]+),',block)
        if head:
            key=head[1]
            if key in records: raise ValueError('Duplicate BibTeX key '+key)
            fields=dict(re.findall(r'^\s*(\w+)\s*=\s*\{(.*)\},?\s*$',block,re.M))
            if not {'author','title','year','doi'}<=fields.keys(): raise ValueError('Unsupported or incomplete record '+key)
            records[key]=fields
    return records


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out-dir',required=True,type=Path);args=p.parse_args()
    out=args.out_dir;out.mkdir(parents=True,exist_ok=False)
    paths=['report/references_verified.bib','report/references_dataset_checked.bib',
           'literature/resume_r04_2026_10_16/legacy_verification_ledger.csv',
           'literature/UNSW_U01_U03_METADATA_FOLLOWUP_2026-10-16.md',
           'literature/verification_2026_10_16/dataset_references.bib','report/main.tex']
    manifests={};checks=[]

    def read(rel):
        path=ROOT/rel;raw=path.read_bytes();manifests[rel]=hashlib.sha256(raw).hexdigest()
        return raw.decode('utf-8-sig')

    def check(name,passed):checks.append(dict(check=name,passed=bool(passed)))

    bib={}
    for rel in paths[:2]:
        records=parse(read(rel));check('no cross-file duplicate keys',not bib.keys()&records.keys());bib.update(records)
    with (ROOT/paths[2]).open(encoding='utf-8-sig',newline='') as f: ledger={r['id']:r for r in csv.DictReader(f)}
    read(paths[2]);read(paths[3]);dataset=parse(read(paths[4]));main=read(paths[5])
    contexts=[]
    for chapter in re.findall(r'\\input\{(chapters/[^}]+)\}',main):
        rel='report/'+chapter+'.tex';text=read(rel)
        for match in re.finditer(r'\\cite\{([^}]+)\}',text):
            para=text[text.rfind('\n\n',0,match.start())+2:text.find('\n\n',match.end()) if '\n\n' in text[match.end():] else len(text)]
            for key in match[1].split(','):
                contexts.append(dict(key=key.strip(),source=rel,line=text[:match.start()].count('\n')+1,claim_context=para.strip()))
    cited={r['key'] for r in contexts}
    check('all 12 bibliography keys cited',cited==set(bib) and len(bib)==12)
    check('all DOIs distinct',len({r['doi'].lower() for r in bib.values()})==12)
    check('L03 excluded from report','legacyL03' not in cited)
    rows=[]
    fields={'author':'authors','title':'title','doi':'doi','year':'year','volume':'volume','number':'issue','pages':'pages_or_article'}
    for key,record in bib.items():
        if key.startswith('legacy'):
            old=ledger[key.removeprefix('legacy')]
            for field,old_field in fields.items():
                check(key+'/'+field+' matches saved ledger',norm(record.get(field,''))==norm(old[old_field]))
            check(key+'/venue matches ledger',norm(record.get('journal',record.get('booktitle','')))==norm(old['container']))
            check(key+'/verified metadata inherited',old['metadata_status']=='VERIFIED_METADATA')
            scope=old['reading_scope'];source=old['primary_url'];status=old['metadata_status']
        else:
            check('U01 exact dataset record',record==dataset[key])
            scope='METADATA_ONLY; U01 pages follow-up, no whole-paper read';source='literature/UNSW_U01_U03_METADATA_FOLLOWUP_2026-10-16.md';status='VERIFIED_METADATA_SCOPED_INHERITED'
        row=dict(key=key,doi=record['doi'],title=record['title'],metadata_status=status,
                 reading_scope=scope,full_text_verified_this_session=False,metadata_requeried_this_session=False,
                 evidence=source,citation_count=sum(r['key']==key for r in contexts))
        rows.append(row)
    for rel,digest in manifests.items():check('unchanged '+rel,hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest)
    with (out/'reference_reading_ledger.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (out/'citation_claim_contexts.json').write_text(json.dumps(contexts,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'source_manifest.json').write_text(json.dumps(manifests,indent=2),encoding='utf-8')
    result=dict(scope='OFFLINE_SAVED_METADATA_AND_READING_BOUNDARY_AUDIT',checks=checks,
                pass_count=sum(r['passed'] for r in checks),fail_count=sum(not r['passed'] for r in checks),
                records=len(rows),citation_instances=len(contexts),new_full_text_reads=0,new_network_queries=0)
    (out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
    for check in checks:
        if not check['passed']: print('FAIL',check['check'])
    return int(result['fail_count']>0)


if __name__=='__main__':raise SystemExit(main())
