"""Freeze a local-only, explicit-source P20-PRE dossier. No ML/data execution."""
import csv
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'defense/p20_pre_2026_10_17_01/packet_02'
PDF = Path('C:/Users/admin/Downloads/Bao_cao_NCKH_EnsembleLearning_09-SV-2026-CNTT2.pdf')
PDF_SHA = '8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources():
    files = [ROOT / 'notebook/phase01/phase1_frozen_research_design_v1.md']
    files += [ROOT / 'report/main.tex', ROOT / 'report/references_verified.bib']
    files += list((ROOT / 'report/chapters').glob('*.tex'))
    files += list((ROOT / 'src/models').glob('*.py'))
    files += list((ROOT / 'src/features').glob('*.py'))
    files += [ROOT / 'src/analysis/run_unsw_phase10_statistics.py']
    files += [ROOT / 'src/analysis/close_original_phase11.py']
    groups = {
        'results/baselines/unsw_nb15/development_cv': ['experiment_metadata.json', 'tables/aggregate_metrics.csv', 'tables/fold_metrics.csv'],
        'results/ensemble/unsw_nb15/phase7_2_ensemble_cv': ['experiment_metadata.json', 'tables/aggregate_metrics.csv', 'tables/pooled_oof_metrics.csv'],
        'results/ensemble/unsw_nb15/phase7_1_diversity': ['tables/pairwise_diversity.csv', 'tables/individual_oof_metrics.csv'],
        'results/tuning/unsw_nb15/phase8_controlled': ['freeze_candidates.json', 'experiment_metadata.json', 'tables/rf17_grid_results.csv', 'tables/rf42_grid_results.csv', 'tables/stacking42_meta_grid_results.csv', 'tables/stacking42_threshold_sensitivity.csv'],
        'results/final_evaluation/unsw_nb15/phase9_holdout': ['experiment_metadata.json', 'tables/final_metrics.csv', 'tables/cost_metrics.csv', 'tables/pairwise_error_counts.csv', 'tables/attack_category_miss_profile.csv'],
        'results/final_evaluation/unsw_nb15/phase11_evaluation_closure': ['phase11_final_evaluation_complete.csv', 'phase11_confusion_matrices.csv', 'phase11_per_class_metrics.csv'],
        'results/final_analysis/unsw_nb15/phase10_statistics': ['experiment_metadata.json', 'tables/paired_bootstrap_differences.csv', 'tables/bootstrap_metric_ci.csv', 'tables/mcnemar_holm.csv', 'tables/attack_family_miss_rate_ci.csv', 'tables/official_vs_novel_degradation.csv', 'tables/performance_cost_tradeoff.csv'],
        'results/final_analysis/unsw_nb15/phase14_error_analysis_step1': ['class_pairwise_transitions.csv', 'attack_family_transitions.csv'],
        'results/data_audit/unsw_nb15': ['dataset_summary.json', 'duplicate_summary.json', 'train_test_overlap.json', 'raw_file_checksums.csv'],
        'results/data_audit/unsw_nb15_views': ['view_summary.json'],
        'results/data_audit/unsw_nb15_overlap': ['overlap_consistency_summary.json', 'cross_split_overlap_by_attack.csv'],
        'results/feature_selection/unsw_nb15/stage1': ['stage1_metadata.json'],
        'results/feature_selection/unsw_nb15/stage2': ['rfecv_metadata.json', 'stability_summary.json', 'subsets/stage2_candidate_subsets.json', 'tables/selection_stability.csv'],
        'results/eda/unsw_nb15/tables': ['binary_class_distribution.csv', 'attack_category_distribution.csv'],
        'results/reproducibility/p15_local_artifact_qa_01': ['artifact_acceptance.json'],
    }
    for directory, names in groups.items():
        files += [ROOT / directory / name for name in names]
    for run in ['p15_local_rf17_full_01', 'p15_local_rf42_full_02', 'p15_local_stack_full_01']:
        files += [ROOT / 'results/reproducibility' / run / 'run_report.json']
    files += list((ROOT / 'results/figures/p16_standalone_2026_10_17_03').glob('*.pdf'))
    files += list((ROOT / 'results/figures/p16_r05_error_tradeoff').glob('*.pdf'))
    return sorted(set(files))


def main():
    import pymupdf as fitz
    OUT.mkdir(parents=True, exist_ok=False)
    content = OUT / 'local_contents'
    content.mkdir()
    rows = []
    for path in sources() + [PDF]:
        assert path.is_file(), path
        if path == PDF:
            relative, kind = 'approved_report.pdf', 'AUTHOR_APPROVED_REPORT_LOCAL_ONLY'
            assert sha(path) == PDF_SHA
        else:
            relative, kind = path.relative_to(ROOT).as_posix(), 'FROZEN_PROJECT_SOURCE_OR_SUMMARY'
            assert not any(x in relative.lower() for x in ['predictions', 'probabilities', '/oof/', '.joblib', 'data/raw', 'reviewer', 'review_packet_setup']), relative
        dest = content / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        assert sha(dest) == sha(path)
        rows.append(dict(packet_path=relative, original_path=str(path), sha256=sha(dest), bytes=dest.stat().st_size, evidence_type=kind))

    # New representation of the supplied manuscript, preserving physical page locators.
    with fitz.open(PDF) as doc:
        assert len(doc) == 37
        text = '\n\n'.join(f'## PHYSICAL PAGE {i+1}\n{p.get_text()}' for i, p in enumerate(doc))
    (content / 'approved_report_pages.txt').write_text(text, encoding='utf-8')

    # Reading scope and publisher-reported facts only. No audit conclusions or review hints.
    reading = json.loads((ROOT / 'literature/deep_verification_2026_10_17_01/curated_reading.json').read_text(encoding='utf-8'))
    papers = reading['papers']
    scope_keys = ['id', 'doi', 'url', 'reading_status', 'sections_read', 'access']
    catalog = [{k: p[k] for k in scope_keys} for p in papers]
    (content / 'literature_scope.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
    with (ROOT / 'literature/deep_verification_2026_10_17_01/qa_03/claim_to_source_map.csv').open(encoding='utf-8-sig') as f:
        facts = [r for r in csv.DictReader(f) if r['kind'] == 'AUTHOR_REPORTED']
    with (content / 'literature_reported_facts.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(facts[0])); writer.writeheader(); writer.writerows(facts)
    for name in ['approved_report_pages.txt', 'literature_scope.json', 'literature_reported_facts.csv']:
        p = content / name
        rows.append(dict(packet_path=name, original_path='GENERATED_REPRESENTATION;see build script and upstream source', sha256=sha(p), bytes=p.stat().st_size, evidence_type='EXTRACT_OR_SCOPED_SOURCE_CATALOG'))
    with (OUT / 'manifest.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    receipt = dict(source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                   manifest_sha256=sha(OUT / 'manifest.csv'), entries=len(rows),
                   label='INTERNAL_REVIEW_ONLY;P20_PRE;NOT_PUBLIC_RELEASE',
                   excluded=['raw data', 'row-level predictions', 'model binaries', 'third-party full texts', 'prior reviewer/QA conclusions'],
                   official_test_read=False, training=False, bootstrap=False, report_changed=False)
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
