"""Read-only tracked-file/archive triage. Never emit matched private values."""
import argparse
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'local_user_path': r'(?i)(?:[A-Z]:[\\/]+Users[\\/]+|/Users/|/home/)[^\s"<>]+',
    'email_candidate': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'private_key_header': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'credential_candidate': r'\b(?:sk-proj-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[A-Z0-9]{16})\b',
    'template_identity_field': r'(?i)(?:MSSV|mã số sinh viên|họ và tên|ký và ghi rõ họ tên|Huỳnh Trọng Thưa)',
}
TEXT = {'.md', '.txt', '.csv', '.json', '.tex', '.sty', '.bib', '.py', '.yaml', '.yml', '.toml', '.xml', '.rels', '.env'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0')
    findings, skipped, archives = [], [], []
    scanned = 0

    def inspect(name, data, depth=0):
        nonlocal scanned
        suffix = Path(name).suffix.lower()
        if suffix in {'.zip', '.docx', '.pptx', '.xlsx'}:
            if depth >= 4:
                skipped.append({'path': name, 'reason': 'archive_depth_limit'})
                return
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    archives.append({'path': name, 'entries': len(z.infolist()), 'sha256': hashlib.sha256(data).hexdigest()})
                    for item in z.infolist():
                        if item.is_dir():
                            continue
                        child = name + '::' + item.filename
                        if item.file_size > 16 * 1024 * 1024:
                            skipped.append({'path': child, 'reason': 'entry_over_16MiB'})
                        else:
                            inspect(child, z.read(item), depth + 1)
            except (zipfile.BadZipFile, RuntimeError) as e:
                skipped.append({'path': name, 'reason': type(e).__name__})
            return
        if suffix not in TEXT:
            return
        try:
            content = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            skipped.append({'path': name, 'reason': 'non_utf8_text'})
            return
        scanned += 1
        for category, pattern in PATTERNS.items():
            lines = sorted({content.count('\n', 0, m.start()) + 1 for m in re.finditer(pattern, content)})
            if lines:
                findings.append({'path': name, 'category': category, 'lines': lines, 'sha256': hashlib.sha256(data).hexdigest(), 'status': 'TRIAGE_ONLY'})

    for rel in filter(None, tracked):
        path = ROOT / rel
        if path.is_file():
            inspect(rel, path.read_bytes())
        else:
            skipped.append({'path': rel, 'reason': 'tracked_path_absent'})
    report = dict(scope='Current git tracked files and readable nested archive text; no remote history audit, OCR, binary secret detection or privacy certification',
                  tracked_files=len(list(filter(None, tracked))), scanned_text_units=scanned,
                  categories={k: sum(f['category'] == k for f in findings) for k in PATTERNS},
                  findings=findings, archives=archives, skipped=skipped,
                  redaction='Only paths, line numbers, categories, hashes. No matched values copied.', mutations='NONE')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['tracked_files', 'scanned_text_units', 'categories']}))


if __name__ == '__main__':
    main()
