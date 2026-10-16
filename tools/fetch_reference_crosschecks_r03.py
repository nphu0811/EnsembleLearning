"""Save second-primary metadata sources; record errors without bypassing TLS."""
import concurrent.futures
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'literature/resume_r03_2026_10_16'
SOURCES = {
    'L04_wiley': 'https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/trit.2020.0073',
    'L10_comsoc': 'https://www.comsoc.org/system/files/2024-03/Publications_Contents_Digest_2024_Mar.pdf',
    'L11_uaeu': 'https://research.uaeu.ac.ae/en/publications/effects-of-feature-selection-and-normalization-on-network-intrusi/',
    'L12_author': 'https://www.rhu.edu.lb/directories/nassreddine-ghalia',
}

def fetch(item):
    key, url = item
    record = dict(id=key, url=url, retrieved=datetime.now(timezone.utc).isoformat())
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NCKH-reference-metadata-audit/1.0'})
        with urllib.request.urlopen(req, timeout=25) as response:
            content = response.read()
            record.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'))
        extension = '.pdf' if content.startswith(b'%PDF') else '.html'
        path = OUT / (key + extension)
        with path.open('xb') as stream:
            stream.write(content)
        record.update(path=str(path.relative_to(ROOT)).replace('\\', '/'), bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
    except Exception as exc:
        record['error'] = str(exc)
    return record

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, SOURCES.items()))
    (OUT / 'fetch_ledger.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    for result in results:
        print(json.dumps(result))

if __name__ == '__main__':
    main()
