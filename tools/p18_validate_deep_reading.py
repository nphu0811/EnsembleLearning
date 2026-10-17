"""Validate source-linked reading anchors and export a bounded comparison ledger.

Does not judge paper validity or run ML. Locally retained source captures are
required; public ledgers preserve their hashes/URLs without redistributing texts.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import unicodedata


def norm(s):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s)).lower().strip()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir',type=Path,required=True)
    parser.add_argument('--out-dir',type=Path,required=True)
    args=parser.parse_args();base=args.input_dir;out=args.out_dir
    out.mkdir(parents=True,exist_ok=False)
    reading=json.loads((base/'curated_reading.json').read_text(encoding='utf-8'))
    checks=[]
    def ck(name,passed):checks.append(dict(check=name,passed=bool(passed)))
    papers=reading['papers'];claims=reading['claims'];by_id={r['id']:r for r in papers}
    ck('unique paper IDs',len(by_id)==len(papers)==7)
    ck('unique normalized DOIs',len({r['doi'].lower() for r in papers})==7)
    ck('24 unique claims',len({r['id'] for r in claims})==len(claims)==24)
    required=['split','preprocessing_fs','stacking_oof','tuning','threshold_imbalance','metrics','statistics_cost','external_validation']
    for row in papers:
        ck('all comparison axes explicit '+row['id'],all(row.get(k) for k in required))
        ck('no whole-paper-read upgrade '+row['id'],'FULL_PAPER_READ' not in row['reading_status'])
    pages=json.loads((base/'local_sources/L12.pages.json').read_text(encoding='utf-8'))
    ck('L12 valid PDF signature',(base/'local_sources/L12.pdf').read_bytes().startswith(b'%PDF'))
    ck('L12 23 pages',len(pages)==23)
    ck('L12 DOI identity','computers14030082' in pages[0]['text'])
    ck('L12 explicit CC BY notice','Attribution (CC BY)' in pages[0]['text'])
    statuses={'VERIFIED','PARTIAL','UNVERIFIED','BLOCKED','NOT_APPLICABLE'}
    for row in claims:
        ck('known paper '+row['id'],row['paper'] in by_id)
        ck('explicit status '+row['id'],row['status'] in statuses)
        if 'page' in row:
            source=pages[row['page']-1]['text']
            ck('source physical page '+row['id'],pages[row['page']-1]['physical_page']==row['page'])
        else:
            p=base/'local_sources'/row['capture'];source=p.read_text(encoding='utf-8')
            ck('correct DOI present in capture '+row['id'],by_id[row['paper']]['doi'].lower() in source.lower())
        ck('anchor found '+row['id'],norm(row['anchor']) in norm(source))
    # Independent extraction from actual rendered/inspected publisher PDF pages.
    table=float(re.search(r'Stacking approach\s+([0-9.]+)',pages[15]['text'])[1])
    prose=float(re.search(r'best performance in accuracy \(([0-9.]+)\)',pages[16]['text'])[1])
    comparison=float(re.search(r'Our Proposal[\s\S]*?\n10\s+([0-9.]+)',pages[17]['text'])[1])
    discrepancy=dict(source='L12 publisher PDF',table5a_page16_fraction=table,nearby_prose_page17_fraction=prose,
                     table7_page18_percent=comparison,table5a_percent=table*100,
                     status='PARTIAL_SCOPE_OR_REPORTING_CONFLICT; no correction or accusation',
                     conclusion='Published values differ beyond simple fraction-to-percent conversion; experimental-scope clarification is needed.')
    ck('observed table5a anchor value',table==.9997)
    ck('observed nearby prose value',prose==.9992)
    ck('observed comparison value',comparison==99.99)
    ck('reporting discrepancy retained',table!=prose and round(table*100,2)!=comparison)
    (out/'published_reporting_discrepancy.json').write_text(json.dumps(discrepancy,indent=2),encoding='utf-8')
    for row in papers:
        if row['id'].startswith('N'):
            meta_path=base/(row['id']+'_crossref.json')
            if row['id']=='N02':meta_path=base/'N02_crossref_retry.json'
            meta=json.loads(meta_path.read_text(encoding='utf-8'))['message']
            ck('new DOI exact identity '+row['id'],meta['DOI'].lower()==row['doi'].lower())
            # Public publisher capture contains title, author display and issue.
            web=(base/'local_sources/publisher_N01_N03_previews.web.txt').read_text(encoding='utf-8') if row['id']!='N02' else (base/'local_sources/publisher_N02_split.web.txt').read_text(encoding='utf-8')
            ck('new paper title corroborated '+row['id'],norm(meta['title'][0]) in norm(web))
            full_meta=(base/'local_sources/publisher_new_metadata.web.txt').read_text(encoding='utf-8')
            names=[norm(' '.join([a.get('given',''),a.get('family','')])) for a in meta['author']]
            positions=[norm(full_meta).find(name) for name in names]
            ck('new ordered authors corroborated '+row['id'],all(i>=0 for i in positions) and positions==sorted(positions))
            ck('new final year present '+row['id'],str(meta['published']['date-parts'][0][0]) in full_meta)
            ck('new volume and article present '+row['id'],meta['volume'] in full_meta and meta['article-number'] in full_meta)
    fields=list(papers[0])
    with (out/'literature_comparison_matrix.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(papers)
    fields=sorted(set().union(*(r.keys() for r in claims)))
    with (out/'claim_to_source_map.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(claims)
    manifest=[]
    for p in sorted((base/'local_sources').glob('*')):
        if p.is_file():manifest.append(dict(path=p.as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),distribution='LOCAL_READING_ONLY; not in draft package or Git'))
    (out/'local_source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    summary=dict(checks=checks,pass_count=sum(r['passed'] for r in checks),fail_count=sum(not r['passed'] for r in checks),
                 paper_count=7,selected_body_read_count=3,abstract_or_prior_scope_count=4,new_claims=24,
                 scope='Source-anchor, identity, coverage and observed reporting-discrepancy checks, not independent experimental reproduction or peer review.')
    (out/'validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='checks'}))
    for row in checks:
        if not row['passed']:print('FAIL',row['check'])
    return int(summary['fail_count']>0)


if __name__=='__main__':raise SystemExit(main())
