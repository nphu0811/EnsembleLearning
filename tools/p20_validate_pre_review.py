"""Check review provenance, evidence pointers and preservation, without ML execution."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'defense/p20_pre_2026_10_17_01'
PACKET = TASK / 'packet_02'
CONTENT = PACKET / 'local_contents'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_evidence_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        return None
    p = Path(value)
    if p.is_absolute() or '..' in p.parts:
        return None
    target = (CONTENT / p).resolve()
    return target if target.is_relative_to(CONTENT.resolve()) else None


def normalized(value):
    return re.sub(r'\s+', ' ', value).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase', choices=['packet', 'reviews', 'complete'], required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    checks = []

    def check(name, value):
        checks.append(dict(check=name, passed=bool(value)))

    receipt = json.loads((PACKET / 'receipt.json').read_text(encoding='utf-8'))
    check('immutable manifest SHA', sha(PACKET / 'manifest.csv') == receipt['manifest_sha256'])
    with (PACKET / 'manifest.csv').open(encoding='utf-8-sig') as f:
        entries = list(csv.DictReader(f))
    check('manifest entries', len(entries) == receipt['entries'] == 80)
    check('unique packet paths', len({r['packet_path'] for r in entries}) == len(entries))
    for row in entries:
        p = safe_evidence_path(row['packet_path'])
        check('safe path ' + row['packet_path'], p is not None)
        check('copy hash ' + row['packet_path'], p is not None and p.is_file() and sha(p) == row['sha256'])
        if not row['original_path'].startswith('GENERATED_'):
            origin = Path(row['original_path'])
            check('original preserved ' + row['packet_path'], origin.is_file() and sha(origin) == row['sha256'])
    names = [r['packet_path'] for r in entries]
    check('no forbidden classes', not any(any(k in n.lower() for k in ['predictions', 'probabilities', '.joblib', '.zip', 'local_sources', 'data/raw', 'reviewer_', 'synthesis']) for n in names))
    check('no prior review or audit conclusions', not any(n.endswith('.md') and n != 'notebook/phase01/phase1_frozen_research_design_v1.md' for n in names))
    setup = json.loads((TASK / 'dispatch_setup.json').read_text(encoding='utf-8'))
    for x in setup['inputs']:
        check('fixed dispatch input ' + x['path'], sha(TASK / x['path']) == x['sha256'])
    check('context fork none', setup['fork_turns'] == 'none')
    check('briefs preassigned', setup['all_briefs_fixed_before_reports'])

    def pointers(items, prefix):
        check(prefix + ' nonempty pointers', isinstance(items, list) and bool(items))
        for i, item in enumerate(items):
            p = safe_evidence_path(item.get('path'))
            check(f'{prefix} pointer{i} in packet', p is not None and item.get('path') in names)
            check(f'{prefix} pointer{i} locator', bool(item.get('locator')))
            anchor = item.get('anchor', '')
            text = p.read_text(encoding='utf-8-sig') if p and p.is_file() and p.suffix != '.pdf' else ''
            check(f'{prefix} pointer{i} literal anchor', bool(anchor) and normalized(anchor) in normalized(text))

    if args.phase in ['reviews', 'complete']:
        frozen = json.loads((TASK / 'review_reports_frozen.json').read_text(encoding='utf-8'))
        check('three frozen reports', len(frozen['reports']) == 3)
        for record in frozen['reports']:
            rid = record['reviewer']
            for item in record['files']:
                check(rid + ' frozen ' + item['path'], sha(TASK / item['path']) == item['sha256'])
            report = json.loads((TASK / f'reviewer_{rid}/report.json').read_text(encoding='utf-8'))
            check(rid + ' packet identity', report['packet_manifest_sha256'] == receipt['manifest_sha256'])
            raw_recommendation = report.get('recommendation')
            recommendation = (raw_recommendation if isinstance(raw_recommendation, str)
                              else (raw_recommendation.get('code', raw_recommendation.get('decision'))
                                    if isinstance(raw_recommendation, dict) else None))
            check(rid + ' reviewer ID', report.get('reviewer') == rid)
            check(rid + ' recommendation', recommendation in ['MAJOR_REVISION_REQUIRED', 'NOT_READY', 'ACCEPTABLE_WITH_LIMITATIONS'])
            check(rid + ' questions>=10', len(report['questions']) >= 10)
            check(rid + ' taxonomy12', len(report['taxonomy_coverage']) == 12)
            check(rid + ' common axes5', len(report['criteria_assessment']) >= 5)
            ids = [c['id'] for c in report['concerns']]
            check(rid + ' unique concern IDs', len(ids) == len(set(ids)))
            for c in report['concerns']:
                prefix = c['id']
                for key in ['claim_pointer', 'concern', 'why_it_matters', 'acceptance_test', 'severity_rationale', 'issue_key']:
                    check(prefix + ' ' + key, bool(c.get(key)))
                check(prefix + ' severity', c['severity'] in ['MAJOR', 'MINOR'])
                check(prefix + ' blocking calibration', isinstance(c['blocking'], bool) and (c['severity'] != 'MINOR' or not c['blocking']))
                check(prefix + ' open concern', c['status'] == 'OPEN')
                check(prefix + ' resolution route', c['resolution_route'] in ['DOCUMENT', 'NEW_EXPERIMENT', 'BOTH', 'EXTERNAL'])
                pointers(c['evidence'], prefix)
            for q in report['questions']:
                check(q['id'] + ' question', bool(q['question']))
                pointers(q['evidence'], q['id'])
    if args.phase == 'complete':
        register = json.loads((TASK / 'synthesis/concern_register.json').read_text(encoding='utf-8'))
        concerns = register['concerns']
        known = {}
        for rid in 'ABC':
            r = json.loads((TASK / f'reviewer_{rid}/report.json').read_text(encoding='utf-8'))
            known.update({c['id']: c for c in r['concerns']})
        flattened = [x for c in concerns for x in c['reviewer_concern_ids']]
        check('all local concerns retained', set(flattened) == set(known))
        check('no local concern mapped twice', len(flattened) == len(set(flattened)))
        for c in concerns:
            check(c['id'] + ' valid category', c['category'] in ['CRITICAL', 'MAJOR', 'MINOR', 'LIMITATION', 'BLOCKED'])
            check(c['id'] + ' open', c['status'] == 'OPEN')
            check(c['id'] + ' acceptance', bool(c['acceptance_test']))
            check(c['id'] + ' consensus honesty', c['consensus'] == (len({x[0] for x in c['reviewer_concern_ids']}) >= 2))
        defense = json.loads((TASK / 'defense/defense_questions.json').read_text(encoding='utf-8'))
        check('20to30 defense questions', 20 <= len(defense['questions']) <= 30)
        for q in defense['questions']:
            check(q['id'] + ' answer', bool(q['answer']))
            pointers(q['evidence'], q['id'])
        check('P20-PRE disposition', register['disposition'] == 'P20_PRE_REVIEW_COMPLETED_WITH_OPEN_CONCERNS')
    result = dict(phase=args.phase, passed=sum(x['passed'] for x in checks), failed=sum(not x['passed'] for x in checks), checks=checks,
                  boundary='Traceability/structure/preservation checks. Not proof of scientific correctness or public release authorization.')
    (args.out_dir / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['phase', 'passed', 'failed']}))
    if result['failed']:
        print(json.dumps([c for c in checks if not c['passed']], ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
