"""Validate R05 source traceability and frozen boundaries, without fitting models."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'proposal/researchwrite/nckh-ids'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    draft = P / 'drafts/De_cuong_noi_dung_review_r05.md'
    text = draft.read_text(encoding='utf-8')
    checks = {}
    checks['r04_review_target_preserved'] = sha(P / 'drafts/De_cuong_noi_dung_review_r04.md') == 'dfef1dffa3fdd8efbb558b65a02cb13c443da8529c5efba169d6b7dc7ad47bac'
    checks['independent_report_frozen'] = sha(P / 'qa_logs/r05_assembled_argument_review.md') == '368996924d05576ad2d740ad3c4c7f395f93c1b97474be7e9b15f2051dfebdc0'
    snapshot = json.loads((P / 'template_audit_r04/original_body_snapshot.json').read_text(encoding='utf-8'))
    checks['original_docx_preserved'] = sha(ROOT / snapshot['source']) == snapshot['sha256']
    frozen_rq = (ROOT / 'notebook/phase01/phase1_frozen_research_design_v1.md').read_text(encoding='utf-8')
    original_questions = re.findall(r'^((?:Under the same|How do feature|To what extent|How sensitive|How do selected).+\?)$', frozen_rq, re.M)
    checks['five_questions_parsed_from_original'] = len(original_questions) == 5
    for i, question in enumerate(original_questions, 1):
        checks[f'rq{i}_exact_original_once'] = text.count(question) == 1
        checks[f'rq{i}_in_proposal_crosswalk'] = bool(re.search(r'^\| RQ' + str(i) + r'(?: | phụ)', text, re.M))

    allowed = {'M': {'N1', 'N2', 'N3', 'N4', 'L05', 'L06', 'L07', 'D01', 'D02'},
               'T': {'N1', 'N2', 'N3', 'D01', 'D02', 'L01', 'L02', 'L04', 'L05', 'L06', 'L07', 'L08', 'L09', 'L11', 'L12'},
               'P': {'S' + str(i) for i in range(1, 11)}}
    citations, unresolved, conventions = set(), [], []
    for match in re.finditer(r'\[([MTP]):([^\]]+)\]', text):
        namespace, payload = match.groups()
        if match[0] in {'[T:Lxx]', '[T:Dxx]', '[T:Nx]', '[P:Sx]'}:
            conventions.append(match[0])
            continue
        payload = re.split(r',\s*(?:abstract|indexed|selected|bìa|Proposed model)', payload)[0]
        for segment in payload.split(','):
            segment = segment.strip()
            explicit = re.match(r'^([MTP]):', segment)
            if explicit:
                namespace = explicit[1]
                segment = segment[2:]
            range_match = re.fullmatch(r'([NLDS])(\d+)\s*[–-]\s*(?:[NLDS])?(\d+)', segment)
            if range_match:
                kind, lo, hi = range_match.groups()
                ids = [kind + str(i).zfill(len(lo)) for i in range(int(lo), int(hi) + 1)]
            elif re.fullmatch(r'[NLDS]\d+', segment):
                ids = [segment]
            else:
                unresolved.append(match[0])
                continue
            for label in ids:
                citations.add((namespace, label))
                if label not in allowed[namespace]:
                    unresolved.append(namespace + ':' + label)
    checks['citation_tokens_parsed_and_resolved'] = bool(citations) and not unresolved
    with (ROOT / 'literature/resume_r04_2026_10_16/legacy_verification_ledger.csv').open(encoding='utf-8-sig') as f:
        ledger = {r['id']: r for r in csv.DictReader(f)}
    used = sorted({label for _, label in citations if label.startswith('L')})
    checks['all_used_paper_metadata_verified'] = all(ledger[k]['metadata_status'] == 'VERIFIED_METADATA' for k in used)
    checks['no_L03_citation'] = 'L03' not in used
    checks['paper_appendix_matches_used_ids'] = set(re.findall(r'^- (L\d+):', text, re.M)) == set(used)
    checks['cited_dois_present_unchanged'] = all(ledger[k]['doi'].lower() in text.lower() for k in used)
    paths = sorted(set(re.findall(r'`([^`\n]+)`', text)))
    local_paths = [p for p in paths if '/' in p and not p.startswith('http')]
    missing_paths = [p for p in local_paths if not (ROOT / p).is_file()]
    checks['all_explicit_local_source_paths_exist'] = not missing_paths

    smoke = json.loads((ROOT / 'results/reproducibility/r04_ml_smoke_repaired/validation.json').read_text(encoding='utf-8'))
    checks['inherited_smoke_45_checks_reused'] = smoke['passed'] and len(smoke['checks']) == 45 and all(smoke['checks'].values())
    metadata = json.loads((ROOT / 'results/reproducibility/r04_ml_smoke_repaired/run_metadata.json').read_text(encoding='utf-8'))
    checks['inherited_smoke_only_TRAIN_reads'] = metadata['dataset_csv_reads'] == ['data/raw/unsw-nb15/UNSW_NB15_training-set.csv']
    input_hashes = {path: {'expected': expected, 'actual': sha(ROOT / path)} for path, expected in metadata['input_sha256'].items()}
    checks['reconstruction_plan_input_hashes_current'] = all(v['actual'] == v['expected'] for v in input_hashes.values())
    plan = (ROOT / 'docs/research/R05_FULL_TRAIN_RECONSTRUCTION_PLAN.md').read_text(encoding='utf-8')
    checks['plan_contains_exact_input_hashes'] = all(v['expected'] in plan for v in input_hashes.values())
    freeze = json.loads((ROOT / 'results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json').read_text(encoding='utf-8'))
    checks['three_frozen_candidates_threshold_05'] = set(freeze) == {'random_forest_42', 'random_forest_17', 'stacking_42'} and all(v['decision_threshold'] == 0.5 for v in freeze.values())
    headers = ['### Mục tiêu', '### Nội dung', '### Kết quả', '## Đơn vị,', '### Trong nước', '### Ngoài nước', '## Nhu cầu', '## Sản phẩm', '## Tiến độ', '## Các khoản', '## Vùng chữ ký']
    checks['original_form_region_order'] = all(h in text for h in headers) and [text.index(h) for h in headers] == sorted(text.index(h) for h in headers)
    checks['sample_money_and_total_preserved'] = all(x in text for x in ['3.000.000', '3.500.000', '500.000', '7.000.000']) and 3000000 + 3500000 + 500000 == 7000000
    checks['sample_30_weeks_preserved_not_remaining_schedule'] = '30 tuần' in text and 'không cam kết hoàn thành' in text and 4 + 11 + 11 + 4 == 30
    checks['pending_admin_and_original_form_conditions_retained'] = text.count('[CẦN XÁC NHẬN') >= 15 and all(x in text for x in ['03 quyển', '02 trang A4', 'trang bìa như bản cứng', 'Hội đồng khoa học Khoa', 'ô tiền trống'])
    checks['explicit_non_submission_and_no_retrospective_approval'] = all(x in text for x in ['chưa điền DOCX', 'chưa render', 'Không có phê duyệt hồi tố', 'chưa đủ điều kiện nộp'])
    checks['smoke_final_model_and_environment_distinction'] = all(x in text for x in ['45/45', 'SMOKE_ONLY', 'original environment UNKNOWN', 'fullTRAIN reconstruction chưa đạt', 'final/fullTRAIN hợp lệ'])
    checks['PR_AUC_implementation_named'] = 'average precision, AP' in text and 'average_precision_score(' in (ROOT / 'src/models/run_unsw_phase9_final_holdout.py').read_text(encoding='utf-8')
    checks['remaining_products_have_bounded_dependency_plan'] = all(x in text for x in ['O1 tổng quan', 'O2 bảng/hình', 'A replay', 'B fullTRAIN', 'C demo', 'O4 form Word', 'O4 slides', 'NO_GO', 'INCOMPLETE', '60 phút/7 GiB', 'G0–G6'])
    audit = json.loads((ROOT / 'results/reproducibility/resume_2026_10_16_r05/public_surface_audit.json').read_text(encoding='utf-8'))
    checks['public_audit_includes_both_share_archives_and_original_docx'] = all(any(a['path'].startswith(prefix) for a in audit['archives']) for prefix in ['NCKH_SHARE_FOR_REVIEW/NCKH_CODE_DOCS.zip', 'NCKH_SHARE_FOR_REVIEW/NCKH_RESULTS.zip', 'templates/original/Mau-'])
    result = dict(checks=checks, passed=all(checks.values()), count=sum(checks.values()), total=len(checks),
                  scope='Mechanical source/citation/frozen-boundary checks only; independent semantic recheck separate; NOT DOCX render, paper full-text verification, training reproduction or submission acceptance',
                  unresolved_citations=unresolved, resolver_convention_placeholders=conventions, explicit_paths_checked=local_paths, missing_paths=missing_paths,
                  used_paper_ids=used, input_hashes=input_hashes, draft_sha256=sha(draft),
                  semantic_acceptance='See independent r05_assembled_argument_recheck.md; P0 author/form/render remain OPEN')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'count': result['count'], 'total': result['total'], 'failures': [k for k, v in checks.items() if not v]}))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
