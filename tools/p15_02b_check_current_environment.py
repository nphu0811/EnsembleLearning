#!/usr/bin/env python3
"""P15-02B: local, read-only verification of an existing P15-02 environment snapshot.

Runs stdlib checks and `python -m pip check` (no install or package imports).
Output: results/reproducibility/p15_02b_runtime_check/p15_02b_runtime_check.json
No original data, training, or official-test predictions are read or changed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DIRECT = (
    'joblib', 'matplotlib', 'numpy', 'pandas', 'scikit-learn', 'scipy', 'threadpoolctl'
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def subprocess_result(args: list[str], timeout: int = 30) -> dict:
    try:
        r = subprocess.run(args, capture_output=True, text=True,
                           errors='replace', timeout=timeout, check=False)
        return {'run': True, 'returncode': r.returncode,
                'stdout': r.stdout.strip()[:3000], 'stderr': r.stderr.strip()[:1000]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'run': False, 'error': type(e).__name__, 'details': str(e)[:300]}


def main() -> int:
    ap = argparse.ArgumentParser(description='P15-02B lightweight dependency verification (read-only).')
    ap.add_argument('--project-root', default='.')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    snapshot_path = root / 'results/reproducibility/p15_02_environment/p15_02_environment.json'
    if not snapshot_path.is_file():
        print(f'ERROR: P15-02 snapshot not found: {snapshot_path}', file=sys.stderr)
        return 2
    with snapshot_path.open('r', encoding='utf-8-sig') as f:
        snapshot = json.load(f)
    expected = snapshot.get('installed_direct_dependency_candidate_versions', {})
    if not isinstance(expected, dict) or not all(k in expected for k in DIRECT):
        print('ERROR: invalid P15-02 snapshot: 7 direct dependencies missing', file=sys.stderr)
        return 2
    observed = {}
    matches = {}
    requirements_python = {}
    for name in DIRECT:
        try:
            observed[name] = metadata.version(name)
            requirements_python[name] = metadata.metadata(name).get('Requires-Python')
        except metadata.PackageNotFoundError:
            observed[name] = None
            requirements_python[name] = None
        matches[name] = observed[name] == str(expected[name])

    # Investigate historical Python provenance; Phase 13 has metadata but did not train.
    history_path = root / 'results/ablation/unsw_nb15/phase13_ablation/analysis_metadata.json'
    historical = {'path': 'results/ablation/unsw_nb15/phase13_ablation/analysis_metadata.json',
                  'exists': history_path.is_file(), 'phase13_training_performed': None,
                  'recorded_python': None, 'recorded_pandas': None}
    if history_path.is_file():
        try:
            with history_path.open('r', encoding='utf-8-sig') as f:
                d = json.load(f)
            historical.update(phase13_training_performed=d.get('training_performed'),
                              recorded_python=d.get('python'),
                              recorded_pandas=d.get('pandas'))
        except (OSError, ValueError) as exc:
            historical['error'] = f'{type(exc).__name__}: {exc}'[:300]
    pip_check = subprocess_result([sys.executable, '-m', 'pip', 'check'], timeout=45)
    py_versions = None
    if platform.system() == 'Windows':
        candidates = subprocess_result(['py', '-0'], timeout=12)
        if candidates.get('run'):
            found = re.findall(r'(?<!\d)3\.\d+(?:\.\d+)?',
                               candidates.get('stdout','')+'\n'+candidates.get('stderr',''))
            py_versions = sorted(set(found))
        else:
            py_versions = []

    installed_list = []
    for dist in metadata.distributions():
        name = dist.metadata.get('Name')
        if name:
            installed_list.append({'name': name, 'version': dist.version})
    installed_list.sort(key=lambda d: d['name'].lower())
    report = {
        'task': 'P15-02B current runtime cross-check (no installations/training)',
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'source_snapshot_sha256': sha256_file(snapshot_path),
        'snapshot_python': snapshot.get('python', {}).get('version'),
        'now_python': platform.python_version(),
        'os': platform.system(), 'snapshot_os': snapshot.get('system', {}).get('os'),
        'runtime_matches_snapshot_python': platform.python_version() == snapshot.get('python',{}).get('version'),
        'versions_visible_to_py_launcher': py_versions,
        'direct_dependencies_expected': {k: str(expected[k]) for k in DIRECT},
        'direct_dependencies_observed': observed,
        'direct_dependencies_match_snapshot': matches,
        'direct_deps_all_match': all(matches.values()),
        'direct_dependency_requires_python_metadata': requirements_python,
        'pip_check': pip_check,
        'pip_check_pass': pip_check.get('run') and pip_check.get('returncode') == 0,
        'installed_distribution_metadata': installed_list,
        'historical_phase13_metadata': historical,
        'interpretation': [
            'The snapshot describes the CURRENT machine, not proven original training environment.',
            'Phase13 Python metadata is analysis-only, not evidence of final model training Python.',
            'No isolated clean install or full retraining has been performed.',
            'pip check only tests declared installed dependency consistency, not reproducibility.',
            'Installed package metadata is not a resolver-generated hashed lockfile.',
        ],
    }
    output = root / 'results/reproducibility/p15_02b_runtime_check/p15_02b_runtime_check.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print('P15-02B snapshot comparison:', 'PASS' if report['runtime_matches_snapshot_python'] and report['direct_deps_all_match'] else 'REVIEW')
    print('pip check:', 'PASS' if report['pip_check_pass'] else 'REVIEW')
    print('Historical Phase13 Python:', historical['recorded_python'])
    print('Report:', output)
    return 0  # review may be needed; do not treat snapshot mismatch as a script crash.


if __name__ == '__main__':
    raise SystemExit(main())
