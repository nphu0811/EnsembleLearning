"""Prepare new report tables from frozen aggregates, never evaluate models."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    'metrics': 'results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv',
    'cost': 'results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv',
    'paired': 'results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv',
}
NAMES = {'random_forest_42': 'RF-42', 'stacking_42': 'Stacking-42', 'random_forest_17': 'RF-17'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.relative_to(ROOT / 'results/tables')
    out.mkdir(parents=True, exist_ok=False)
    before = {key: sha(ROOT / rel) for key, rel in INPUTS.items()}
    source = {key: read(ROOT / rel) for key, rel in INPUTS.items()}
    official = [r for r in source['metrics'] if r['eval_view'] == 'official_test']
    metrics = {r['pipeline']: r for r in official}
    costs = {r['pipeline']: r for r in source['cost']}
    checks = {'three_unique_official_models': len(official) == len(metrics) == 3 and set(metrics) == set(NAMES),
              'cost_join_exact_candidates': set(costs) == set(NAMES)}
    numeric = lambda a, b: math.isclose(float(a), float(b), abs_tol=1e-12, rel_tol=1e-12)
    for name, r in metrics.items():
        tn, fp, fn, tp = (int(r[k]) for k in ['tn', 'fp', 'fn', 'tp'])
        total = tn + fp + fn + tp
        f1_attack = 2 * tp / (2 * tp + fp + fn)
        f1_normal = 2 * tn / (2 * tn + fp + fn)
        denominator = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        checks[name + '_frozen_rows_threshold_features'] = total == int(r['n_rows']) == 82332 and float(r['decision_threshold']) == 0.5 and r['original_feature_count'] == costs[name]['original_feature_count']
        checks[name + '_metrics_from_confusion'] = all([
            numeric(r['macro_f1'], (f1_attack + f1_normal) / 2),
            numeric(r['mcc'], (tp * tn - fp * fn) / denominator),
            numeric(r['false_positive_rate'], fp / (tn + fp)),
            numeric(r['false_negative_rate'], fn / (tp + fn)),
            numeric(r['recall_detection_rate'], tp / (tp + fn)),
        ])
        checks[name + '_cost_inference_units'] = numeric(costs[name]['inference_ms_per_sample'], float(costs[name]['inference_time_seconds']) * 1000 / total)
    paired = [r for r in source['paired'] if r['eval_view'] == 'official_test' and r['model_a'] == 'stacking_42' and r['model_b'] == 'random_forest_42']
    wanted = ['macro_f1', 'mcc', 'false_positive_rate', 'false_negative_rate']
    paired_map = {r['metric']: r for r in paired if r['metric'] in wanted}
    checks['four_unique_paired_effect_rows'] = len(paired_map) == 4
    for key in wanted:
        r = paired_map[key]
        checks[key + '_delta_from_official_aggregates'] = numeric(r['delta_a_minus_b'], float(metrics['stacking_42'][key]) - float(metrics['random_forest_42'][key]))
        lo, hi = float(r['ci_lower']), float(r['ci_upper'])
        checks[key + '_CI_semantics'] = lo <= hi and (r['ci_excludes_zero'].lower() == 'true') == (lo > 0 or hi < 0) and float(r['ci_level']) == 0.95 and int(r['bootstrap_replicates']) == 10000
    checks['FP_FN_tradeoff_direction'] = int(metrics['stacking_42']['fp']) - int(metrics['random_forest_42']['fp']) == -142 and int(metrics['stacking_42']['fn']) - int(metrics['random_forest_42']['fn']) == 118

    tables = {
        'official_performance': ([metrics[k] for k in NAMES], ['pipeline', 'original_feature_count', 'n_rows', 'decision_threshold', 'macro_f1', 'mcc', 'recall_detection_rate', 'false_positive_rate', 'false_negative_rate', 'tn', 'fp', 'fn', 'tp']),
        'historical_cost': ([costs[k] for k in NAMES], list(source['cost'][0])),
        'stack_minus_rf42': ([paired_map[k] for k in wanted], list(paired[0])),
    }
    for name, (rows, fields) in tables.items():
        path = out / (name + '.csv')
        with path.open('x', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        expected = [{key: row[key] for key in fields} for row in rows]
        checks[name + '_CSV_tokens_preserved'] = read(path) == expected

    def perf_row(name, tex=False):
        r = metrics[name]
        return [NAMES[name], f"{float(r['macro_f1']):.6f}", f"{float(r['mcc']):.6f}", f"{float(r['false_positive_rate']):.6f}", f"{float(r['false_negative_rate']):.6f}", r['fp'], r['fn']]

    md = '# P16 — source tables r05, chưa render vào báo cáo\n\n'
    md += 'Official holdout binary, Attack=1, n=82.332, threshold0.5. Số thập phân trong phần hiển thị được làm tròn; CSV giữ nguyên token nguồn. Không fit/predict/bootstrap mới.\n\n'
    md += '| Model | Macro-F1 | MCC | FPR | FNR | FP | FN |\n|---|---:|---:|---:|---:|---:|---:|\n'
    for name in NAMES:
        md += '| ' + ' | '.join(perf_row(name)) + ' |\n'
    md += '\nBảng A. So sánh đóng băng trên official TEST; Stacking giảm142FP nhưng tăng118FN so với RF42. Các tỷ lệ ở đơn vị0–1. Không có cost matrix để quy hai loại lỗi về một lợi ích tổng thể. Không dùng bảng để đổi threshold hoặc candidate.\n\n'
    md += '| Model | Features | Train s | Inference s / 82.332 rows | ms/row | Size MiB (legacy field mb) |\n|---|---:|---:|---:|---:|---:|\n'
    for name in NAMES:
        r = costs[name]
        md += '| ' + ' | '.join([NAMES[name], r['original_feature_count'], f"{float(r['train_time_seconds']):.3f}", f"{float(r['inference_time_seconds']):.6f}", f"{float(r['inference_ms_per_sample']):.6f}", f"{float(r['serialized_model_size_mb']):.3f}"]) + ' |\n'
    md += '\nBảng B. Chi phí ghi trong run lịch sử, không phải benchmark mới trên máy hiện tại. Original environment UNKNOWN; không có uncertainty/repeated-training cho thời gian. Kích thước được source tính byte/(1024²), nên hiển thị MiB dù tên cột lịch sử là mb. Kích thước lịch sử không chứng minh artifact final còn trên máy. RF17 và RF42 khác hyperparameters; đây là joint pipeline trade-off, không causal feature-only ablation.\n\n'
    md += '| Metric | Δ Stack42−RF42 | 95% CI lower | 95% CI upper |\n|---|---:|---:|---:|\n'
    for key in wanted:
        r = paired_map[key]
        md += '| ' + ' | '.join([key] + [f"{float(r[k]):.9f}" for k in ['delta_a_minus_b', 'ci_lower', 'ci_upper']]) + ' |\n'
    md += '\nBảng C. Paired bootstrap10.000 replicates đã lưu, không bootstrap lại; delta là điểm metric ở đơn vị0–1, không phải phần trăm. CI có điều kiện trên benchmark rows, không thay repeated training hoặc external validation. CI Macro-F1/MCC chứa0: chưa chứng minh superiority, không suy equivalence. McNemar là kiểm paired correctness riêng, không trực tiếp test Macro-F1. FS fullTRAIN trước development CV, meta selection chưa fully nested, overlap/split dependence vẫn là giới hạn.\n'
    (out / 'TABLES_AND_CAPTIONS.md').write_text(md, encoding='utf-8')
    # Standard source only. No claim of compiled or visual layout acceptance.
    tex = '% Generated from frozen aggregate CSV. NOT COMPILED OR VISUALLY VERIFIED.\n'
    tex += '\\begin{table}[htbp]\n\\centering\n\\small\n\\begin{tabular}{lrrrrrr}\n\\hline\nModel & Macro-F1 & MCC & FPR & FNR & FP & FN \\\\\n\\hline\n'
    for name in NAMES:
        tex += ' & '.join(perf_row(name)) + ' \\\\\n'
    tex += '\\hline\n\\end{tabular}\n\\caption{Frozen official holdout, Attack=1, n=82332, threshold 0.5. Stacking-42 reduces FP by 142 and increases FN by 118 relative to RF-42. See source-data manifest and the conditional uncertainty table; no overall superiority or equivalence is established.}\n\\label{tab:r05-official-performance}\n\\end{table}\n'
    (out / 'official_performance.tex').write_text(tex, encoding='utf-8')
    checks['inputs_unchanged'] = all(sha(ROOT / rel) == before[key] for key, rel in INPUTS.items())
    (out / 'source_data_manifest.json').write_text(json.dumps(dict(inputs={key: dict(path=rel, sha256=before[key]) for key, rel in INPUTS.items()}, outputs={p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()}, raw_or_predictions_read=False, new_training_or_bootstrap=False, render='NOT_PERFORMED; no TeX engine available', frozen_limitations='FS/meta not fully nested; row dependence; unknown historical environment; RF17 joint-pipeline contrast'), indent=2), encoding='utf-8')
    validation = dict(checks=checks, passed=all(checks.values()), total=len(checks), passed_count=sum(checks.values()), scope='New source table numeric/join/unit/traceability QA only; no model evaluation or visual/PDF acceptance')
    (out / 'validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')
    print(json.dumps({'passed': validation['passed'], 'count': validation['passed_count'], 'total': validation['total'], 'failures': [k for k, v in checks.items() if not v]}))
    if not validation['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
