"""Read-only research-source inspection and byte-identical export staging.

This script does not author DOCX or initialize the artifact runtime.
Run from the NCKH workspace root. Existing staged files must match byte for byte.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tomllib
import zipfile

ROOT = Path.cwd().resolve()
OUT = ROOT / 'exports/docx_export_2026_10_16'
RUNTIME = Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime')
SKILL = Path('C:/Users/admin/.codex/plugins/cache/openai-primary-runtime/documents/26.1013.11914/skills/documents/SKILL.md')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def copy_exact(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert target.read_bytes() == source.read_bytes(), str(target)
    else:
        shutil.copy2(source, target)
    assert sha(source) == sha(target)
    return {'source': source.relative_to(ROOT).as_posix(),
            'preserved': target.relative_to(OUT).as_posix(),
            'bytes': source.stat().st_size, 'sha256': sha(source)}

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(parents=True, exist_ok=True)
    selected = set()
    for folder in ['notebook/phase11', 'notebook/phase12', 'notebook/phase13',
                   'results/final_reporting/unsw_nb15/phase11_results_figures']:
        selected.update(p for p in (ROOT/folder).rglob('*')
                        if p.is_file() and p.suffix.lower() in {'.md', '.bib', '.png', '.csv'})
    for rel in ['nckh_codex_handoff/PREMATURE_ARTIFACT_RECLASSIFICATION.md',
                '.research_memory/RESEARCH_CANON.md',
                'docs/TEMPLATE_REQUIREMENTS_MATRIX.md',
                'proposal/researchwrite/nckh-ids/drafts/sections/muc_tieu_noi_dung_phuong_phap_r02.md']:
        p = ROOT/rel
        if p.exists():
            selected.add(p)
    rows = [copy_exact(p, OUT/'sources'/p.relative_to(ROOT)) for p in sorted(selected)]
    main_source = ROOT/'notebook/phase13/phase13_4_manuscript_with_figures_tables.md'
    rows.append(copy_exact(main_source, OUT/'Bao_cao_NCKH_bao_toan.md'))
    image_refs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', main_source.read_text(encoding='utf-8-sig'))
    for ref in image_refs:
        assert not Path(ref).is_absolute() and '..' not in Path(ref).parts
        rows.append(copy_exact(main_source.parent/ref, OUT/ref))
    with (OUT/'SOURCE_MANIFEST.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['source','preserved','bytes','sha256'])
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        assert sha(ROOT/row['source']) == row['sha256'] == sha(OUT/row['preserved'])

    config = tomllib.loads(Path('C:/Users/admin/.codex/config.toml').read_text(encoding='utf-8'))
    runtime_manifest = json.loads((RUNTIME/'runtime.json').read_text(encoding='utf-8'))
    native_manifest = json.loads((RUNTIME/'dependencies/bin/override/native-executables.json').read_text(encoding='utf-8'))
    env_names = ['RUNTIME_NODE','RUNTIME_PYTHON','RUNTIME_NODE_MODULES','RUNTIME_BIN_DIR',
                 'CODEX_PRIMARY_RUNTIME_NODE_MODULES','CODEX_PRIMARY_RUNTIME_PYTHON','CODEX_PRIMARY_RUNTIME_ROOT']
    tool_inventory = json.loads((OUT/'tool_inventory.json').read_text(encoding='utf-8'))
    matches = [t['name'] for t in tool_inventory['tools'] if 'load_workspace_dependencies' in t['name']]
    zip_path = ROOT/'templates/original/DE-TAI-NCKHSV-15.zip'
    with zipfile.ZipFile(zip_path) as z:
        zip_members = [n for n in z.namelist() if not n.endswith('/')]
    evidence = {
        'status': 'BLOCKED_RUNTIME_RESOLVER_AND_RENDERER',
        'scope': 'DOCX export only; no research rerun or confirmed-content revision',
        'workspace': str(ROOT), 'skill': str(SKILL), 'skill_sha256': sha(SKILL),
        'loader_tools_exposed': matches,
        'documents_local_plugin_enabled': config.get('plugins',{}).get('documents@openai-primary-runtime'),
        'runtime_manifest': runtime_manifest,
        'native_executables': native_manifest,
        'runtime_env': {n: os.environ.get(n) for n in env_names},
        'managed_paths_exist': {
            rel: (RUNTIME/rel).exists() for rel in [
                'dependencies/node/bin/node.exe','dependencies/python/python.exe',
                'dependencies/node/node_modules/docx/package.json']},
        'soffice_on_path': shutil.which('soffice.exe'),
        'bundled_soffice_files': [str(p) for p in (RUNTIME/'dependencies').rglob('soffice.exe')],
        'word_connected_sessions_observed': 0,
        'public_plugin_lookup': 'documents@openai-primary-runtime: plugin_not_found; not evidence that local built-in plugin is absent',
        'template_zip_sha256': sha(zip_path), 'template_zip_members': zip_members,
        'template_zip_docx_count': sum(n.lower().endswith('.docx') for n in zip_members),
        'main_manuscript_source': main_source.relative_to(ROOT).as_posix(),
        'main_manuscript_sha256': sha(main_source),
        'content_status': 'Existing integrated manuscript is a historical premature reporting draft, not a final approved report. Preserved without rewriting.',
        'preservation': {'manifest_rows': len(rows), 'all_byte_hash_checks_pass': True,
                         'main_images': len(image_refs), 'all_main_image_links_resolve': all((OUT/r).is_file() for r in image_refs)},
        'docx_created': False, 'render_run': False, 'layout_verified': False,
        'global_installs_performed': False, 'skill_files_modified': False,
    }
    (OUT/'diagnostics.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'preservation': evidence['preservation'],
                      'loader_tools_exposed': matches,
                      'documents_enabled': evidence['documents_local_plugin_enabled'],
                      'managed_paths_exist': evidence['managed_paths_exist'],
                      'soffice_on_path': evidence['soffice_on_path'],
                      'bundled_soffice_files': evidence['bundled_soffice_files']}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
