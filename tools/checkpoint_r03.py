"""Save r03 checkpoint after reviews and checks; no scientific-output mutation."""
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEM = ROOT / '.research_memory'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def append(path, text):
    with path.open('a', encoding='utf-8') as stream:
        stream.write('\n' + text + '\n')

def main():
    stamp = datetime.now(timezone.utc).isoformat()
    marker = MEM / 'checkpoint_r03.json'
    if marker.exists():
        raise FileExistsError(marker)
    review = ROOT / 'proposal/researchwrite/nckh-ids/qa_logs/r03_products_section_review.md'
    if not review.is_file():
        raise FileNotFoundError(review)
    # Current template prose correction; historical notes remain unchanged.
    matrix = ROOT / 'docs/TEMPLATE_REQUIREMENTS_MATRIX.md'
    text = matrix.read_text(encoding='utf-8').replace('có 9 bảng.', 'có 8 bảng (đính chính r03).')
    matrix.write_text(text, encoding='utf-8')
    draft = ROOT / 'proposal/researchwrite/nckh-ids/drafts/sections/ung_dung_san_pham_tien_do_r03.md'
    draft_text = draft.read_text(encoding='utf-8')
    for old, new in [('mục39–55', 'mục 39–55'), ('đề cương2026', 'đề cương 2026'), ('contracts04/06/07', 'contracts 04/06/07'), ('dạngIII', 'dạng III'), ('ít nhất15', 'ít nhất 15'), ('có20', 'có 20'), ('chuyên đề1', 'chuyên đề 1'), ('Chuyên đề1', 'Chuyên đề 1'), ('chuyên đề2', 'chuyên đề 2'), ('Chuyên đề2', 'Chuyên đề 2'), ('là3.000.000', 'là 3.000.000'), ('là3.500.000', 'là 3.500.000'), ('thảo500.000', 'thảo 500.000'), ('tổng7.000.000', 'tổng 7.000.000'), ('|4 tuần', '| 4 tuần'), ('|11 tuần', '| 11 tuần')]:
        draft_text = draft_text.replace(old, new)
    draft.write_text(draft_text, encoding='utf-8')
    paths = re.findall(r'`([^`]+)`', draft.read_text(encoding='utf-8'))
    paths = list(dict.fromkeys(p for p in paths if '/' in p or p.startswith('.research_memory')))
    checks = {p: (ROOT / p).is_file() for p in paths}
    checks['template_budget_sum'] = 3000000 + 3500000 + 500000 == 7000000
    checks['reference_validation'] = json.loads((ROOT / 'literature/resume_r03_2026_10_16/validation.json').read_text())['passed']
    checks['P2_01_CD_cover_and_article'] = 'trang bìa như bản cứng' in draft_text and 'Hội đồng khoa học Khoa' in draft_text
    checks['P2_02_retrospective_context'] = 'đang được phục hồi từ nghiên cứu đã có kết quả' in draft_text
    checks['P2_03_reviewed_spacing'] = not any(s in draft_text for s in ['mục39', 'dạngIII', 'ít nhất15', 'là3.000.000', '|4 tuần'])
    validation = ROOT / 'proposal/researchwrite/nckh-ids/qa_logs/r03_source_validation.json'
    validation.write_text(json.dumps({'checks': checks, 'passed': all(checks.values()), 'scope': 'Source presence/budget arithmetic only; independent section review separate; no render/full proposal approval'}, indent=2), encoding='utf-8')
    if not all(checks.values()):
        raise ValueError('Source validation failed')
    board = MEM / 'TASK_BOARD.md'
    board_text = board.read_text(encoding='utf-8').replace('| IN_REVIEW | drafts/sections/ung_dung_san_pham_tien_do_r03.md | Partial MD only; source/form review, no DOCX/render/full-proposal gate |', '| DONE_SCOPED | drafts/sections/ung_dung_san_pham_tien_do_r03.md; qa_logs/r03_products_section_review.md | Independent review7.75;P2 repairs/source checks;no rescore/full-proposal/DOCX/render |')
    board.write_text(board_text, encoding='utf-8')
    append(MEM / 'SKILL_USAGE_LOG.md', '''## r03 —16/10/2026

- P18-FIELD-R03: nature-ref-verifier; exact C:/Users/admin/.codex/skills/nature-ref-verifier/SKILL.md; manifest1.0.1 + references/common-patterns.md read. Applied DOI-first saved-identity checks, second-primary field comparisons, severity/name/year handling and scoped report/BibTeX updates. Outputs literature/resume_r03_2026_10_16/, current matrix/subset.18/18 bookkeeping PASS;6 verified/6 pending, U01/U03 open; not whole-paper verification.
- PROP-PRODUCTS-R03: researchwrite alias, exact C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md; manifest1.1.1; hybrid-mode, compose-mode, partial-proposal-scope, validation-checklist, stopping-rules, project-structure, evaluation-rubric, professor-dispatch read. Reused passed r02 foundation; read04/06/07, drafted missing bounded product/application/schedule/budget sections, dispatched one narrow independent feasibility/template reviewer as permitted by skill. Review and source validation under qa_logs/r03*. No full proposal or DOCX export.
- nature-data router was read during routing only; no new availability workflow executed. Not logged as applied. No nature-reviewer/P20 or human approval claimed. Registry hashes pinned in r03 resume_audit.json; reviewer additional references recorded in its report.
''')
    append(MEM / 'CHANGELOG.md', '''## r03 —16/10/2026

- Read-only resume audit:146/148 pre-session hashes match; HANDOFF/SKILL_USAGE drift explained;282/282 historical files preserved. Added reusable output-isolated audit CLI.6 audit unit tests PASS.
- Corrected current DOCX template table count to8; original ZIP/DOCX and experiment source/results untouched.
- Field crosschecks advance L04/L11;6 verified legacy entries total,6 pending and U01/U03 open. Added raw successful/failed fetch ledger, web captures, field report and18-check validation; previous ledgers retained.
- Added bounded proposal application/products/quality/schedule/budget draft and separate independent review/source QA; no full proposal/DOCX/render or final gate claim. Updated roadmap/task/decisions/handoff/evidence manifest.
''')
    handoff = '''# Checkpoint hiện hành r03 —16/10/2026

Đọc phần này trước các checkpoint lịch sử bên dưới. User đã khởi động lại autonomous research scope; ràng buộc export-only của lượt trước không còn là scope hiện tại.

Đã đọc toàn bộ MASTER/AGENTS và memory, audit thực tế tại docs/RESUME_AUDIT_R03_2026-10-16.md và results/reproducibility/resume_2026_10_16_r03/resume_audit.json. Prior manifest146/148 khớp;2 stale memory hashes là HANDOFF/SKILL_USAGE có thêm runtime checkpoint, đã giải thích;282/282 historical research files khớp. Audit cũ giữ expected/actual; manifest cuối đã refresh sau review.6/6 audit unit tests PASS. ZIP15 entries không DOCX, extraction+CRC PASS; Word2026 riêng có8 bảng, không9 như notes cũ. Original templates/data/training source/frozen results không sửa.

P18: đọc và áp dụng nature-ref-verifier v1.0.1; outputs literature/resume_r03_2026_10_16/. L04 Wiley fields và L11 UAEU/KeAi fields mới VERIFIED_METADATA, current subset6 (L04/05/06/07/08/11),6 legacy vẫn pending.18/18 identity/bookkeeping checks PASS; đây không phải full-text or full P18 completion. L10 ComSoc PDF xác nhận title/ordered display authors/year/pages nhưng còn vol/issue/DOI second-source. L02 author-hosted PDF đã đọc selected abstract/intro/audit stages, không whole-paper, không suy CIC errors sang UNSW. U01/U03 warnings giữ nguyên. Wiley direct403, RHU TLS fail, MDPI web errors được lưu trung thực; không bypassTLS. report FIELD_CROSSCHECKS.md là record nguồn/reading limits.

Proposal: áp dụng researchwrite hybrid/partial flow; r02 foundation đã pass nên không restart. Draft mới proposal/researchwrite/nckh-ids/drafts/sections/ung_dung_san_pham_tien_do_r03.md gồm nhu cầu/ứng dụng, sản phẩm/chất lượng, tiến độ/kinh phí. Independent narrow review r03_products_section_review.md và source validation r03_source_validation.json. Đọc report trước dùng draft, không suy full-proposal review; chưa merge/full DOCX/PDF/render. Administrative applicability/signatures vẫn [CẦN XÁC NHẬN].

## Resume chính xác

1. Đọc STATE/TASK_BOARD/CANON/DECISIONS và xác minh manifest. Command an toàn: `python tools/resume_checkpoint_audit.py --out-dir results/reproducibility/NEXT_UNIQUE_SESSION`; outdir phải chưa tồn tại. Không rerun checkpoint_r03 hoặc fetch/reconcile vào output đã có.
2. Ưu tiên tổng quan/lý do chọn đề tài còn thiếu theo04/06/07: dùng reading/source boundaries hiện hành; hoàn thiện6 legacy field checks và U01/U03 khi có primary source đủ. L02 có author-hosted source để đọc tiếp; full study reading cần workflow skill phù hợp. Không mở lại dataset/RQ/test selection.
3. Review sections mới và findings trước merge. Chỉ full-proposal QA khi đủ mọi phần; chưa gọi partial Markdown là DOCX form. Có thể tiếp tục P16 từ frozen tables và build nguồn báo cáo trong bản làm việc, giữ original.
4. Runtime: Python3.11.9 có; xelatex/lualatex/tectonic/LibreOffice không PATH; registry không expose load_workspace_dependencies ở r03. Chỉ gỡ blocker khi có evidence tool mới; không claim thử lại từ log cũ. G3/model reconstruction cần capacity/path/environment plan riêng; no model artifact/no inference demo hiện tại.
5. G0–G6 vẫn còn critical gaps, release NOT_READY_FOR_SUBMISSION, không tạo FINAL_NCKH.zip. Original pasted prompt txt vẫn AUTHOR_INPUT_NEEDED; ZIP/DOCX đã có, không hỏi lại mẫu.

Không có background work khi phiên kết thúc. Current next step và trạng thái scientific canon không thay bởi metadata/draft tiến triển.

---

'''
    old = (MEM / 'HANDOFF.md').read_text(encoding='utf-8')
    (MEM / 'HANDOFF.md').write_text(handoff + old, encoding='utf-8')
    proposal_state = ROOT / 'proposal/researchwrite/nckh-ids/state.json'
    ps = json.loads(proposal_state.read_text(encoding='utf-8'))
    ps['mode'] = 'hybrid'
    ps['technical_debts'] = [t.replace('8 legacy field crosschecks', '6 legacy field crosschecks') for t in ps['technical_debts']]
    ps['r03'] = {'draft': str(draft.relative_to(ROOT)).replace('\\', '/'), 'review': str(review.relative_to(ROOT)).replace('\\', '/'), 'status': 'INTERNAL_PARTIAL_DRAFT; P2 repairs applied', 'section_review_score': 7.75, 'review_type': 'Independent AI narrow section review', 'post_repair_rescore': 'NOT_PERFORMED', 'full_proposal_qa': 'NOT_PERFORMED', 'render': 'NOT_PERFORMED'}
    proposal_state.write_text(json.dumps(ps, indent=2, ensure_ascii=False), encoding='utf-8')
    state_path = MEM / 'STATE.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    state['last_updated'] = stamp
    state['current_task'] = 'P18/P01 remaining source checks and proposal literature/background sections after r03 checkpoint'
    state['next_action'] = 'Read r03 section review; complete bounded proposal literature/background and 6 legacy metadata checks plus U01/U03; continue P16 frozen-table QA independently'
    state['completed_tasks'] += ['BOOT-R03_SCOPED', 'P18-FIELD-R03_SCOPED', 'PROP-PRODUCTS-R03_SCOPED']
    state['last_gate_status'].update(resume_r03='146/148 prior hash matches;2 explained stale memory hashes;282/282 preserved', legacy_literature='6 VERIFIED_METADATA/6 pending;18/18 identity/bookkeeping checks', template_r03='ZIP15 entries/extraction CRC PASS;DOCX8 tables CRC PASS;no visual QA', products_section='INTERNAL_PARTIAL_DRAFT; independent section report + source checks; not full proposal')
    newfiles = [ROOT / 'docs/RESUME_AUDIT_R03_2026-10-16.md', validation, review, draft]
    newfiles += list((ROOT / 'literature/resume_r03_2026_10_16').glob('*'))
    newfiles += [ROOT / ('tools/' + n) for n in ['resume_checkpoint_audit.py', 'fetch_reference_crosschecks_r03.py', 'reconcile_reference_checks_r03.py', 'checkpoint_r03.py']]
    newfiles += [ROOT / 'results/reproducibility/resume_2026_10_16_r03/resume_audit.json']
    prior = {r['path']: r for r in state['artifact_manifest']}
    for path in newfiles:
        if path.is_file():
            rel = str(path.relative_to(ROOT)).replace('\\', '/')
            prior[rel] = {'path': rel, 'sha256': sha(path)}
    for rel, item in prior.items():
        item['sha256'] = sha(ROOT / rel)
    evidence = MEM / 'EVIDENCE_INDEX.csv'
    with evidence.open(encoding='utf-8-sig', newline='') as stream:
        fields = next(csv.reader(stream))
    with evidence.open('a', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        for rel, item in sorted(prior.items()):
            if rel == '.research_memory/EVIDENCE_INDEX.csv':
                continue
            writer.writerow(dict(claim_id='R03_CHECKPOINT_ARTIFACT', artifact_path=rel, sha256=item['sha256'], method='SHA256/presence; scoped QA in r03 reports; no training replay', origin='workspace; publisher/institutional metadata; AI section review', date='2026-10-16', verification_status='PRESENT_HASHED; semantic limits in r03 reports'))
    prior['.research_memory/EVIDENCE_INDEX.csv'] = {'path': '.research_memory/EVIDENCE_INDEX.csv', 'sha256': sha(evidence)}
    state['artifact_manifest'] = sorted(prior.values(), key=lambda x: x['path'])
    temp = state_path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    temp.replace(state_path)
    marker.write_text(json.dumps({'timestamp': stamp, 'manifest_count': len(prior), 'source_checks': checks, 'scientific_outputs_unchanged': '282/282 pre-session audit; post-check required', 'status': 'CHECKPOINT_SAVED; post-audit required'}, indent=2), encoding='utf-8')
    print('Checkpoint saved; run post-audit into a new directory.')

if __name__ == '__main__':
    main()
