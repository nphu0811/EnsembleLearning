"""Read-only artifact inventory and explicit-allowlist INTERNAL_REVIEW_ONLY ZIP.

No model deserialization, index changes, deletion, training or dataset access.
No wildcard package selection. This is a review dossier, not a runnable release.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SMOKE_BASE='results/reproducibility/r04_ml_smoke_repaired/'
SMOKE={k:SMOKE_BASE+'smoke_models/'+k+'_SMOKE_ONLY.joblib'
       for k in ('random_forest_17','random_forest_42','stacking_42')}
PDF_SHA='8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b'
ALLOWLIST=[
    'README.md',
    'docs/research/FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md',
    'results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json',
    'docs/research/COMPREHENSIVE_QA_2026-10-17.md',
    'docs/research/COMPANION_ADDENDUM_2026-10-17.md',
    'docs/research/DEEP_METHODS_VERIFICATION_2026-10-17.md',
    'docs/research/CURRENT_REPORT_READING_BOUNDARIES_2026-10-17.md',
    'docs/research/RELEASE_READINESS_2026-10-17.md',
    'release/INTERNAL_REVIEW_DRAFT_POLICY_2026-10-17.md',
    'defense/REVIEW_PACKET_SETUP_2026-10-17.md',
    'release/RELEASE_BLOCKERS.md',
    'literature/deep_verification_2026_10_17_01/READING_PROTOCOL.md',
    'literature/deep_verification_2026_10_17_01/verification_ledger.csv',
    'literature/deep_verification_2026_10_17_01/qa_03/literature_comparison_matrix.csv',
    'literature/deep_verification_2026_10_17_01/qa_03/claim_to_source_map.csv',
    'literature/deep_verification_2026_10_17_01/qa_03/published_reporting_discrepancy.json',
    'results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv',
    'results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv',
    'results/final_evaluation/unsw_nb15/phase9_holdout/tables/attack_category_miss_profile.csv',
    'results/final_evaluation/unsw_nb15/phase9_holdout/tables/pairwise_error_counts.csv',
    'results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv',
    'results/final_analysis/unsw_nb15/phase10_statistics/tables/bootstrap_metric_ci.csv',
    'results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv',
    'results/figures/p16_paired_effects_2026_10_16/paired_effects.pdf',
    'results/figures/p16_paired_effects_2026_10_16/source_data.csv',
    'results/figures/p16_r05_error_tradeoff/error_tradeoff.pdf',
    'results/figures/p16_r05_error_tradeoff/source_data.csv',
    'results/figures/p16_standalone_2026_10_17_03/attack_family_wilson.pdf',
    'results/figures/p16_standalone_2026_10_17_03/source_attack_family_miss_rate_ci.csv',
    'report/main.tex', 'report/frontmatter.tex','report/abbreviations.tex',
    'report/references_verified.bib','report/references_dataset_checked.bib',
    'report/chapters/introduction.tex','report/chapters/theoretical_foundations.tex',
    'report/chapters/related_work.tex','report/chapters/dataset_eda.tex',
    'report/chapters/methodology.tex','report/chapters/results_discussion.tex',
    'report/chapters/validity_discussion.tex','report/chapters/conclusion.tex',
    'reproducibility/requirements-p16-qa-py311-NOT-TRAINING.txt'
]


def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):digest.update(block)
    return digest.hexdigest()


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True,encoding='utf-8').strip()


def forbidden(name):
    p=PurePosixPath(name);lower=name.lower()
    return (p.is_absolute() or '..' in p.parts or ':' in name or '\\' in name
            or any(x.startswith('.venv') or x in ('venv','__pycache__','local_sources','original') for x in p.parts)
            or p.suffix.lower() in ('.joblib','.pickle','.pkl','.zip','.dll','.exe')
            or lower.startswith(('data/','templates/')) or 'predictions.csv' in lower
            or p.name in ('.env','credentials.json','id_rsa'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',required=True,type=Path)
    parser.add_argument('--approved-pdf',required=True,type=Path)
    args=parser.parse_args();out=args.out_dir.resolve()
    if not out.is_relative_to(ROOT/'release'):raise ValueError('Output must be inside workspace release/')
    out.mkdir(parents=True,exist_ok=False)
    checks=[]
    def ck(name,passed,detail=''):checks.append(dict(check=name,passed=bool(passed),detail=detail))
    before_index=git('ls-files','--stage')
    meta_path=ROOT/SMOKE_BASE/'run_metadata.json'
    meta=json.loads(meta_path.read_text(encoding='utf-8'))
    rows=[]
    for candidate,name in SMOKE.items():
        path=ROOT/name;digest=sha(path);model=meta['models'][candidate]
        tracked=git('ls-files','--',name)==name
        initial=git('log','--diff-filter=A','--format=%H','--',name).splitlines()
        blob=git('rev-parse','HEAD:'+name)
        ck('smoke tracked '+candidate,tracked)
        ck('smoke bytes match original metadata '+candidate,path.stat().st_size==model['bytes'])
        ck('smoke hash match original metadata '+candidate,digest==model['sha256'])
        ck('smoke source TRAIN-only '+candidate,model['train_rows']==2000 and model['validation_rows']==500)
        rows.append(dict(candidate=candidate,path=name,bytes=path.stat().st_size,sha256=digest,
                         git_tracked=tracked,git_head_blob=blob,introduced_commit=initial[-1] if initial else 'UNKNOWN',
                         evidence_class='HISTORICAL_TRAIN_SUBSET_SOFTWARE_SMOKE; NOT_FULL_TRAIN',
                         metadata_source=SMOKE_BASE+'run_metadata.json',distribution_status='EXCLUDED_FROM_DRAFT_AND_PUBLIC_RELEASE_PENDING_RIGHTS'))
    with (out/'smoke_artifact_inventory.csv').open('w',encoding='utf-8',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    # Historical absence is recorded, not repaired or recovered from Git.
    missing='results/reproducibility/p15_02c2_clean_env.zip'
    history=dict(path=missing,exists_in_HEAD_checkout=(ROOT/missing).exists(),tracked=bool(git('ls-files','--',missing)),
                 deletion_commit=git('log','--diff-filter=D','-1','--format=%H','--',missing),
                 status='HISTORICAL_DELETION_RECORDED; NOT_RESTORED_OR_PACKAGED')
    ck('historical ZIP still absent and untracked',not history['exists_in_HEAD_checkout'] and not history['tracked'])
    (out/'historical_zip_status.json').write_text(json.dumps(history,indent=2),encoding='utf-8')

    contents=out/'draft_contents';contents.mkdir()
    manifest=[]
    notice=('INTERNAL_REVIEW_ONLY\nNOT_AUTHORIZED_FOR_PUBLIC_RELEASE\n'
            'Draft factual review dossier. Not FINAL_NCKH or runnable reproduction package.\n'
            'No license grant. No models, raw datasets, third-party full texts or credentials.\n'
            'Sources/figures are partial review inputs; original templates and some dependencies excluded.\n'
            'Final P20 remains DEFERRED; packet is not mutually blind panel input yet.\n')
    (contents/'INTERNAL_REVIEW_ONLY.txt').write_text(notice,encoding='utf-8')
    for name in ALLOWLIST:
        ck('safe allowlist path '+name,not forbidden(name))
        source=(ROOT/name).resolve()
        if forbidden(name) or not source.is_relative_to(ROOT) or not source.is_file():raise ValueError('Rejected source '+name)
        expected=sha(source);destination=contents/name;destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,destination)
        ck('copied file hash '+name,sha(destination)==expected)
        manifest.append(dict(package_path=name,bytes=source.stat().st_size,sha256=expected,origin=name,
                             evidence_class='SELECTED_PROJECT_EVIDENCE; REVIEW_ONLY',distribution_status='INTERNAL_REVIEW_ONLY; PUBLIC_RIGHTS_UNCONFIRMED'))
    pdf=args.approved_pdf.resolve();ck('approved PDF exact identity',sha(pdf)==PDF_SHA)
    if sha(pdf)!=PDF_SHA:raise ValueError('Approved PDF hash mismatch')
    pdf_dest=contents/'approved_report/Bao_cao_37p_UNCHANGED.pdf';pdf_dest.parent.mkdir();shutil.copyfile(pdf,pdf_dest)
    manifest.append(dict(package_path='approved_report/Bao_cao_37p_UNCHANGED.pdf',bytes=pdf.stat().st_size,
                         sha256=PDF_SHA,origin='AUTHOR_SUPPLIED_APPROVED_REPORT; original source path recorded locally',
                         evidence_class='AUTHOR_APPROVED_REPORT_SNAPSHOT',distribution_status='INTERNAL_REVIEW_ONLY; PUBLIC_DISTRIBUTION_NOT_AUTHORIZED'))
    manifest.append(dict(package_path='INTERNAL_REVIEW_ONLY.txt',bytes=(contents/'INTERNAL_REVIEW_ONLY.txt').stat().st_size,
                         sha256=sha(contents/'INTERNAL_REVIEW_ONLY.txt'),origin='generated notice',evidence_class='SCOPE_LABEL',distribution_status='INTERNAL_REVIEW_ONLY'))
    manifest_path=out/'draft_manifest.csv'
    with manifest_path.open('w',encoding='utf-8',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)
    shutil.copyfile(manifest_path,contents/'DRAFT_MANIFEST.csv')
    archive=out/'INTERNAL_REVIEW_ONLY_NCKH_DRAFT.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for row in manifest:z.write(contents/row['package_path'],row['package_path'])
        z.write(contents/'DRAFT_MANIFEST.csv','DRAFT_MANIFEST.csv')
    with zipfile.ZipFile(archive) as z:
        ck('ZIP CRC',z.testzip() is None)
        ck('ZIP exact allowlist',set(z.namelist())=={r['package_path'] for r in manifest}|{'DRAFT_MANIFEST.csv'})
        ck('ZIP no duplicate entries',len(z.namelist())==len(set(z.namelist())))
        ck('ZIP explicit internal labels',b'NOT_AUTHORIZED_FOR_PUBLIC_RELEASE' in z.read('INTERNAL_REVIEW_ONLY.txt'))
        for row in manifest:
            name=row['package_path'];ck('ZIP entry safe '+name,not forbidden(name))
            ck('ZIP entry hash '+name,hashlib.sha256(z.read(name)).hexdigest()==row['sha256'])
        ck('manifest copy exact',z.read('DRAFT_MANIFEST.csv')==manifest_path.read_bytes())
    # Limited deterministic content triage. No content or match values emitted.
    patterns=[rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
              rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'\bsk-proj-[A-Za-z0-9_-]{30,}']
    findings=[]
    for row in manifest:
        p=contents/row['package_path']
        if p.suffix.lower() in ('.md','.tex','.bib','.txt','.csv','.json'):
            raw=p.read_bytes()
            if any(re.search(pattern,raw) for pattern in patterns):findings.append(row['package_path'])
    ck('limited known-token/private-key pattern triage',not findings,str(findings))
    for row in manifest:
        if row['origin'] in ALLOWLIST:ck('source unchanged after package '+row['origin'],sha(ROOT/row['origin'])==row['sha256'])
    for row in rows:ck('smoke unchanged after package '+row['candidate'],sha(ROOT/row['path'])==row['sha256'])
    ck('Git index unchanged',git('ls-files','--stage')==before_index)
    ck('approved PDF unchanged',sha(pdf)==PDF_SHA)
    ck('no final archive',archive.name!='FINAL_NCKH.zip' and not (out/'FINAL_NCKH.zip').exists())
    result=dict(source_commit=git('rev-parse','HEAD'),scope='INTERNAL_REVIEW_ONLY; NO_PUBLIC_RELEASE_AUTHORIZATION',
                checks=checks,pass_count=sum(r['passed'] for r in checks),fail_count=sum(not r['passed'] for r in checks),
                smoke_artifacts=3,package_manifest_rows=len(manifest),zip_entries=len(manifest)+1,
                archive_relative_path=archive.relative_to(ROOT).as_posix(),archive_sha256=sha(archive),archive_bytes=archive.stat().st_size,
                code_license_present=bool(git('ls-files','*LICENSE*','*LICENCE*')),models_deserialized=False,index_cleanup=False,
                public_release_status='BLOCKED_RIGHTS_AND_SCIENTIFIC_ADMIN_GATES',
                limitations='Review dossier only; no runnable training environment. Pattern triage is not a comprehensive secret audit. Source captures are local and excluded.')
    (out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
    return int(result['fail_count']>0)


if __name__=='__main__':raise SystemExit(main())
