"""Validate saved evidence without re-running experiments; never replace output."""
import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from verify_document_renames import resolve_document_path

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    state = json.loads((root / '.research_memory/STATE.json').read_text(encoding='utf-8-sig'))
    manifest = []
    for item in state['artifact_manifest']:
        path = resolve_document_path(root, item['path'])
        actual = sha(path) if path.is_file() else None
        manifest.append(dict(path=item['path'], resolved_path=path.relative_to(root).as_posix(),
                             expected=item['sha256'], actual=actual,
                             passed=actual == item['sha256']))
    preservation = []
    with (root / 'results/reproducibility/resume_2026_10_16/bootstrap/preservation_manifest.csv').open(encoding='utf-8-sig') as stream:
        for item in csv.DictReader(stream):
            path = resolve_document_path(root, item['path'])
            actual = sha(path) if path.is_file() else None
            preservation.append(dict(path=item['path'], resolved_path=path.relative_to(root).as_posix(),
                                     passed=actual == item['sha256']))
    registry = []
    for path in sorted((Path.home() / '.codex/skills').glob('nature-*/SKILL.md')):
        match = re.search(r'^name:\s*(.+)$', path.read_text(encoding='utf-8'), re.M)
        registry.append(dict(path=str(path), name=match[1].strip() if match else None, sha256=sha(path)))
    template = root / 'templates/original'
    with zipfile.ZipFile(template / 'DE-TAI-NCKHSV-15.zip') as archive:
        entries = [n for n in archive.namelist() if not n.endswith('/')]
        zip_check = dict(crc_error=archive.testzip(), entries=len(entries), has_docx=any(n.endswith('.docx') for n in entries),
                         extraction_match=all((template / 'latex' / n).is_file() and hashlib.sha256(archive.read(n)).hexdigest() == sha(template / 'latex' / n) for n in entries))
    with zipfile.ZipFile(template / 'Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx') as archive:
        xml = ET.fromstring(archive.read('word/document.xml'))
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        docx = dict(crc_error=archive.testzip(), top_level_tables=len(xml.findall('w:body/w:tbl', ns)),
                    all_tables=len(xml.findall('.//w:tbl', ns)), visual_qa='NOT_PERFORMED')
    report = dict(timestamp=datetime.now(timezone.utc).isoformat(), python=sys.version,
                  prior_artifacts=manifest, preservation=preservation, nature_registry=registry,
                  latex_zip=zip_check, docx=docx,
                  tools={k: shutil.which(k) for k in ['python', 'xelatex', 'lualatex', 'tectonic', 'libreoffice']})
    report['counts'] = dict(manifest=len(manifest), manifest_pass=sum(r['passed'] for r in manifest),
                            preservation=len(preservation), preservation_pass=sum(r['passed'] for r in preservation))
    (out / 'resume_audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['counts', 'latex_zip', 'docx', 'tools']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
