"""Fetch DOI-first metadata for the exact pending list, preserving prior files."""
import csv
import json
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'literature/resume_r04_2026_10_16'

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    with (ROOT/'literature/resume_r03_2026_10_16/legacy_verification_ledger.csv').open(encoding='utf-8-sig') as f:
        records=[r for r in csv.DictReader(f) if r['metadata_status']!='VERIFIED_METADATA']
    ledger=[]
    for r in records:
        url='https://api.crossref.org/works/'+r['doi']
        item={'id':r['id'],'url':url,'time':datetime.now(timezone.utc).isoformat()}
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'NCKH-exact-reference-audit/1.0'})
            with urllib.request.urlopen(req,timeout=20) as response:
                raw=response.read()
                item['http_status']=response.status
            p=OUT/(r['id']+'_crossref.json')
            p.write_bytes(raw)
            msg=json.loads(raw)['message']
            item.update(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(raw).hexdigest(),title=msg.get('title'),page=msg.get('page'),volume=msg.get('volume'),issue=msg.get('issue'),published=msg.get('published'),author=msg.get('author'))
        except Exception as exc:
            item['error']=str(exc)
        ledger.append(item)
        print(json.dumps({k:v for k,v in item.items() if k not in ['author']},ensure_ascii=True))
        (OUT/'api_ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False),encoding='utf-8')

if __name__=='__main__':
    main()
