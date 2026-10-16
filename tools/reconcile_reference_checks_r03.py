"""Apply reviewed metadata crosschecks, preserving historical ledgers."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'literature/resume_r03_2026_10_16'

def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def write_csv(path, records):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

def main():
    ledger = rows(ROOT / 'literature/resume_r02_2026_10_16/legacy_verification_ledger.csv')
    updates = {
        'L04': ('https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/trit.2020.0073',
                'Crossref fields agree with publisher web-indexed record: title, ordered authors, 2020, journal, 5(4), 283-293 and DOI. Direct HTTP403; publisher result captured in web_capture_6.json. Abstract/selected introductory snippets only; no whole-paper read.'),
        'L11': ('https://research.uaeu.ac.ae/en/publications/effects-of-feature-selection-and-normalization-on-network-intrusi/',
                'Crossref agrees with UAEU institutional record and KeAi publisher index: ordered authors, title, final 2025, journal 8(1), 23-39, DOI. Saved institutional HTML; abstract/metadata only, no full protocol audit.'),
    }
    for record in ledger:
        if record['id'] in updates:
            record['primary_url'], record['note'] = updates[record['id']]
            record['metadata_status'] = 'VERIFIED_METADATA'
        if record['id'] == 'L10':
            record['primary_url'] = 'https://www.comsoc.org/system/files/2024-03/Publications_Contents_Digest_2024_Mar.pdf'
            record['note'] = 'IEEE ComSoc digest PDF p26 (1-based) confirms title, ordered display names, 2024 and 1190-1212. Volume/issue/DOI not independently matched in inspected excerpt. Crossref family Heydari vs display Shah Heydari requires name-token care; no automatic author patch.'
        if record['id'] == 'L02':
            record['primary_url'] = 'https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf'
            record['reading_scope'] = 'SELECTED_ABSTRACT_INTRO_METHODS'
            record['note'] = 'Author-hosted PDF first page and selected dataset-audit stages read; title/ordered authors match. Six PDF pages do not independently prove proceedings pagination 7-12. No full-paper review; do not transfer CIC-specific findings to UNSW.'
        if record['id'] == 'L12':
            record['note'] += ' r03 author institutional index corroborates authors/year/14(3)/82 but shortens title; direct MDPI errors and RHU TLS failure recorded. Keep pending.'
    target = OUT / 'legacy_verification_ledger.csv'
    if target.exists():
        raise FileExistsError(target)
    write_csv(target, ledger)
    matrix = rows(ROOT / 'literature/literature_matrix.csv')
    for item in matrix:
        record = next(r for r in ledger if r['id'] == item['id'])
        for key, source in [('verification_status', 'metadata_status'), ('reading_scope', 'reading_scope'), ('source_url', 'primary_url'), ('claim_limit', 'note')]:
            item[key] = record[source]
    write_csv(ROOT / 'literature/literature_matrix.csv', matrix)
    bib = (ROOT / 'literature/resume_r02_2026_10_16/legacy_working_references.bib').read_text(encoding='utf-8')
    entries = re.findall(r'@\w+\{legacyL\d+,.*?\n\}', bib, re.S)
    verified = {r['id'] for r in ledger if r['metadata_status'] == 'VERIFIED_METADATA'}
    selected = [entry for entry in entries if re.search(r'legacy(L\d+)', entry)[1] in verified]
    (ROOT / 'literature/refs_verified_subset.bib').write_text('% Metadata-verified subset only; r03 ledger records reading limits. Not final bibliography.\n\n' + '\n\n'.join(selected) + '\n', encoding='utf-8')
    checks = {
        'ledger_rows_12': len(ledger) == 12,
        'unique_dois_12': len({r['doi'] for r in ledger}) == 12,
        'verified_subset_6': len(selected) == len(verified) == 6,
        'matrix_status_matches': all(m['verification_status'] == next(r for r in ledger if r['id'] == m['id'])['metadata_status'] for m in matrix),
        'crossref_sources_exist': all((ROOT / r['raw_crossref']).is_file() for r in ledger),
        'no_full_read_claim': all('FULL_TEXT_READ' != r['reading_scope'] for r in ledger),
    }
    # Compare complete declared fields against the saved Crossref identity; second-source
    # confirmation is manually reviewed in FIELD_CROSSCHECKS.md, not inferred by this code.
    for r in ledger:
        message = json.loads((ROOT / r['raw_crossref']).read_text(encoding='utf-8'))['message']
        checks[r['id'] + '_doi_title'] = (message['DOI'].lower() == r['doi'].lower() and message['title'][0] == r['title'])
    (OUT / 'validation.json').write_text(json.dumps({'checks': checks, 'passed': all(checks.values()), 'verified': sorted(verified), 'pending': [r['id'] for r in ledger if r['id'] not in verified], 'scope': 'Metadata bookkeeping and saved identity checks; not full-text or final P18 QA'}, indent=2), encoding='utf-8')
    print(json.dumps({'checks': len(checks), 'passed': sum(checks.values()), 'verified': sorted(verified)}))
    if not all(checks.values()):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
