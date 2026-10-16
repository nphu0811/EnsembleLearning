"""One observed paired-count contrast. No training, selection, or resampling."""
import argparse
import csv
import hashlib
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--qa-scripts', type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.relative_to(ROOT / 'results/figures')
    out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(args.qa_scripts))
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    from audit_panel_alignment import require_matplotlib_panel_alignment

    original = SOURCE.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    with SOURCE.open(encoding='utf-8', newline='') as f:
        rows = {r['pipeline']: r for r in csv.DictReader(f) if r['eval_view'] == 'official_test'}
    baseline, comparison = rows['random_forest_42'], rows['stacking_42']
    deltas = [int(comparison[k]) - int(baseline[k]) for k in ['fp', 'fn']]
    assert deltas == [-142, 118]
    assert all(int(r['n_rows']) == 82332 and float(r['decision_threshold']) == 0.5 for r in [baseline, comparison])
    normal = int(baseline['tn']) + int(baseline['fp'])
    attack = int(baseline['tp']) + int(baseline['fn'])
    assert (normal, attack) == (37000, 45332)
    assert int(comparison['tn']) + int(comparison['fp']) == normal
    assert int(comparison['tp']) + int(comparison['fn']) == attack
    with (out / 'source_data.csv').open('x', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['error', 'RF42_count', 'Stack42_count', 'delta_Stack42_minus_RF42', 'class_denominator'])
        for key, delta, denominator in zip(['fp', 'fn'], deltas, [normal, attack]):
            writer.writerow([key, baseline[key], comparison[key], delta, denominator])
    mpl.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'], 'font.size': 9,
                         'axes.spines.top': False, 'axes.spines.right': False, 'axes.spines.left': False,
                         'svg.fonttype': 'none', 'pdf.fonttype': 42, 'text.usetex': False})
    fig, ax = plt.subplots(figsize=(120 / 25.4, 65 / 25.4))
    fig.subplots_adjust(left=0.27, right=0.96, bottom=0.25, top=0.83)
    ax.barh([1, 0], deltas, height=0.42, color=['#3C7286', '#C17F45'], edgecolor='none')
    ax.axvline(0, color='#777777', linewidth=0.7)
    ax.set_yticks([1, 0], ['False positives', 'False negatives'])
    ax.tick_params(axis='y', length=0, pad=8)
    ax.set_xlim(-220, 220)
    ax.set_xticks([-200, -100, 0, 100, 200])
    ax.set_ylim(-0.65, 1.65)
    ax.set_xlabel('Change in count (Stacking-42 minus RF-42)', labelpad=8)
    for y, delta in zip([1, 0], deltas):
        ax.annotate(f'{delta:+d}', xy=(delta, y), xytext=(-5 if delta < 0 else 5, 0),
                    textcoords='offset points', ha='right' if delta < 0 else 'left', va='center', fontsize=9)
    fig.text(0.27, 0.94, 'Fewer false alarms, more missed attacks', fontsize=9, ha='left', va='top')
    fig.canvas.draw()
    alignment = require_matplotlib_panel_alignment(fig, json_out=out / 'alignment.json', strict=True)
    fig.savefig(out / 'error_tradeoff.pdf')
    fig.savefig(out / 'error_tradeoff.svg')
    fig.savefig(out / 'error_tradeoff.tiff', dpi=600)
    fig.savefig(out / 'error_tradeoff.png', dpi=600)
    plt.close(fig)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == digest
    caption = '''# FP/FN trade-off — caption and integrity notes

Observed error-count changes for Stacking-42 relative to RF-42 on the same official UNSW-NB15 holdout (n=82,332; 37,000 Normal and 45,332 Attack; threshold=0.5; Attack=1). False positives decrease by142 and false negatives increase by118. Signed count labels and separate error categories identify direction; colours provide redundant distinction. These are exact differences between two saved confusion matrices, not means across repeated fits, so no newly estimated uncertainty bars are shown. Paired rate/metric uncertainty is reported in the companion evidence tables. No net operational benefit, statistical equivalence, independent retraining stability or external validation is established. No new fit, bootstrap, threshold selection or official TEST evaluation was performed. Frozen FS/meta-selection and benchmark dependence limitations remain applicable. Source data accompany the figure.
'''
    (out / 'CAPTION.md').write_text(caption, encoding='utf-8')
    manifest = dict(source=SOURCE.relative_to(ROOT).as_posix(), source_sha256=digest,
                    source_before_after_match=True, observed_deltas=deltas,
                    python=platform.python_version(), matplotlib=mpl.__version__,
                    selected_backend='python', size_mm=[120, 65], dpi=600,
                    alignment_verdict=alignment.get('verdict'), scope='single observed paired count contrast; no repeated-training inference',
                    outputs={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file()})
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps({'deltas': deltas, 'input_unchanged': True, 'alignment': alignment.get('verdict')}))


if __name__ == '__main__':
    main()
