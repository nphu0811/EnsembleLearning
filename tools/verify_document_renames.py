"""Verify approved documentation relocation without changing frozen evidence.

Also supplies a narrow resolver for historical Markdown paths in resume audits.
Historical expected hashes stay unchanged, including explained mismatches.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='cleanup_audit/RENAMED_FILES_MANIFEST.json'


def resolve_document_path(root: Path, relative: str) -> Path:
    """Resolve only explicit, contained .md migrations; never remap science files."""
    root=root.resolve()
    original=root/relative
    if original.is_file() or not (root/MANIFEST).is_file():
        return original
    if PurePosixPath(relative).suffix!='.md' or PurePosixPath(relative).parts[0] not in {'docs','report','defense'}:
        return original
    data=json.loads((root/MANIFEST).read_text(encoding='utf-8'))
    entries=[x for x in data['renames'] if x['old_path']==relative]
    if len(entries)!=1:
        return original
    rel=PurePosixPath(entries[0]['new_path'])
    if rel.is_absolute() or '..' in rel.parts or ':' in str(rel) or '\\' in str(rel):
        raise ValueError('Invalid relocated document path')
    candidate=(root/str(rel)).resolve()
    if not candidate.is_relative_to(root) or rel.suffix!='.md' or rel.parts[0] not in {'docs','report','defense'}:
        raise ValueError('Relocation outside documentation scope')
    return candidate


def audit(root=ROOT):
    data=json.loads((root/MANIFEST).read_text(encoding='utf-8'))
    failures=[]
    destinations=[]
    for x in data['renames']:
        old=root/x['old_path'];new=resolve_document_path(root,x['old_path'])
        destinations.append(x['new_path'].casefold())
        if old.exists():failures.append('legacy path still present: '+x['old_path'])
        if new!=root/x['new_path'] or not new.is_file():
            failures.append('missing or inconsistent destination: '+x['new_path']);continue
        raw=new.read_bytes()
        actual=hashlib.sha256(raw).hexdigest()
        git_lf=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()
        if actual!=x['sha256_after'] and git_lf!=x['git_lf_sha256_after']:
            failures.append('changed document bytes: '+x['new_path'])
    if len(destinations)!=len(set(destinations)):failures.append('duplicate destination names')
    # Current live consumers must use canonical names. Historical snapshots stay exact.
    targets=[root/'README.md',root/'00_BAN_DO_DU_AN.md',root/'tools/p19_safe_review_draft.py']
    # This catalog intentionally quotes legacy identifiers beside working new links.
    targets+=[p for p in (root/'docs').rglob('*.md') if p.name!='CURRENT_DOCUMENTS.md']
    targets+=list((root/'report').glob('*.md'))
    for p in targets:
        text=p.read_text(encoding='utf-8-sig')
        for x in data['renames']:
            if x['old_path'] in text or Path(x['old_path']).name in text:
                failures.append('stale live reference: '+p.relative_to(root).as_posix()+' -> '+x['old_path'])
    return {'status':'PASS' if not failures else 'FAIL','documents_verified':len(destinations),
            'live_reference_files_checked':len(targets),'failures':failures,
            'scientific_path_remapping':False,'historical_hashes_rewritten':False}


if __name__=='__main__':
    result=audit();print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['failures']))
