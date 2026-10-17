"""Read-only P16 audit of saved summaries; no raw data, predictions or estimators.

Run with a NEW --out-dir. Derived weighted F1 is explicitly a summary identity,
not a new experiment. The accepted report and all scientific inputs stay read-only.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import statistics
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P9 = 'results/final_evaluation/unsw_nb15/phase9_holdout/tables/'
P10 = 'results/final_analysis/unsw_nb15/phase10_statistics/tables/'
P11 = 'results/final_reporting/unsw_nb15/phase11_results_figures/'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(row):
    tn, fp, fn, tp = (int(row[k]) for k in ('tn', 'fp', 'fn', 'tp'))
    n = tn + fp + fn + tp
    f_pos = 2 * tp / (2 * tp + fp + fn)
    f_neg = 2 * tn / (2 * tn + fp + fn)
    return dict(accuracy=(tn + tp) / n,
                balanced_accuracy=(tp / (tp + fn) + tn / (tn + fp)) / 2,
                precision=tp / (tp + fp), recall_detection_rate=tp / (tp + fn),
                f1=f_pos, macro_f1=(f_pos + f_neg) / 2,
                weighted_f1=((tn + fp) * f_neg + (tp + fn) * f_pos) / n,
                mcc=(tp * tn - fp * fn) / math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)),
                false_positive_rate=fp / (tn + fp), false_negative_rate=fn / (tp + fn))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    checks, inputs = [], {}

    def track(path):
        path = Path(path)
        rel = path.relative_to(ROOT).as_posix()
        inputs.setdefault(rel, sha(path))
        return path

    def load(rel):
        path = track(ROOT / rel)
        with path.open(encoding='utf-8-sig', newline='') as stream:
            return list(csv.DictReader(stream))

    def check(name, passed, detail=''):
        checks.append(dict(check=name, passed=bool(passed), detail=detail))

    def close(name, actual, expected, tol=1e-11):
        check(name, math.isclose(float(actual), float(expected), rel_tol=0, abs_tol=tol),
              f'{actual} vs {expected}; abs tolerance {tol}')

    final = load(P9 + 'final_metrics.csv')
    by_key = {(r['eval_view'], r['pipeline']): r for r in final}
    derived = []
    for key, row in by_key.items():
        values = metrics(row)
        check(f'{key}: confusion n', sum(int(row[x]) for x in ('tn','fp','fn','tp')) == int(row['n_rows']))
        for metric, value in values.items():
            if metric in row:
                close(f'{key}: {metric}', row[metric], value)
        derived.append(dict(eval_view=key[0], pipeline=key[1], **values,
                            provenance='DERIVED_FROM_FROZEN_CONFUSION_COUNTS; no new predictions'))
    point = load(P10 + 'recomputed_point_metrics.csv')
    for row in point:
        original = by_key[(row['eval_view'], row['pipeline'])]
        for field in row:
            if field in original and field not in ('eval_view', 'pipeline'):
                close(f'P10 point {row["pipeline"]}/{row["eval_view"]}/{field}', row[field], original[field])

    ci = load(P10 + 'bootstrap_metric_ci.csv')
    for row in ci:
        close(f'CI point {row["pipeline"]}/{row["eval_view"]}/{row["metric"]}', row['point_estimate'],
              by_key[(row['eval_view'],row['pipeline'])][row['metric']])
        check('CI ordering', float(row['ci_lower']) <= float(row['point_estimate']) <= float(row['ci_upper']))
        check('CI definition', float(row['ci_level']) == .95 and int(row['bootstrap_replicates']) == 10000)
    delta = load(P10 + 'paired_bootstrap_differences.csv')
    for row in delta:
        a = by_key[(row['eval_view'],row['model_a'])]
        b = by_key[(row['eval_view'],row['model_b'])]
        close('paired delta ' + str((row['eval_view'],row['model_a'],row['model_b'],row['metric'])),
              row['delta_a_minus_b'], float(a[row['metric']]) - float(b[row['metric']]))
        excludes = float(row['ci_lower']) > 0 or float(row['ci_upper']) < 0
        check('CI excludes zero flag', excludes == (row['ci_excludes_zero'] == 'True'))
        check('paired CI ordering', float(row['ci_lower']) <= float(row['delta_a_minus_b']) <= float(row['ci_upper']))

    attacks = load(P9 + 'attack_category_miss_profile.csv')
    for key, row in by_key.items():
        parts = [r for r in attacks if r['eval_view'] == key[0]]
        check(f'{key}: attack support', sum(int(r['attack_rows']) for r in parts) == int(row['fn']) + int(row['tp']))
        check(f'{key}: attack FN sum', sum(int(r[key[1]+'_false_negatives']) for r in parts) == int(row['fn']))
        for part in parts:
            close('attack miss rate', part[key[1]+'_miss_rate'], int(part[key[1]+'_false_negatives'])/int(part['attack_rows']))
    attack_ci = load(P10 + 'attack_family_miss_rate_ci.csv')
    for row in attack_ci:
        original = next(r for r in attacks if r['eval_view'] == row['eval_view'] and r['attack_cat'] == row['attack_cat'])
        close('attack CI source FN', row['false_negatives'], original[row['pipeline']+'_false_negatives'])
        close('attack CI source rate', row['miss_rate'], original[row['pipeline']+'_miss_rate'])
        check('Wilson interval contains rate', float(row['wilson_95_lower']) <= float(row['miss_rate']) <= float(row['wilson_95_upper']))

    mcnemar = load(P10 + 'mcnemar_holm.csv')
    for view in {r['eval_view'] for r in mcnemar}:
        ordered = sorted([r for r in mcnemar if r['eval_view'] == view], key=lambda r: float(r['p_exact_raw']))
        previous = 0
        for i, row in enumerate(ordered):
            previous = min(1., max(previous, (len(ordered)-i)*float(row['p_exact_raw'])))
            close('Holm adjustment (per-view three pair family)', row['p_holm'], previous)
            check('discordant total', int(row['discordant_total']) == int(row['a_wrong_b_correct']) + int(row['a_correct_b_wrong']))

    # Means and sample SD must reproduce their own development folds. Different
    # historical timing runs are deliberately not required to agree cross-stage.
    for stem, group in [('results/baselines/unsw_nb15/development_cv/tables/', ('subset','model')),
                        ('results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/', ('feature_track','configuration'))]:
        folds = load(stem + 'fold_metrics.csv')
        aggregates = load(stem + 'aggregate_metrics.csv')
        for row in folds:
            for metric, value in metrics(row).items():
                if metric in row:
                    close(f'{stem} fold {row["fold"]}/{metric}', row[metric], value)
        for agg in aggregates:
            rows = [r for r in folds if all(r[k] == agg[k] for k in group)]
            check('fold count', len(rows) == int(agg['cv_folds']) == 3)
            for field in agg:
                if field.endswith(('_mean','_std')):
                    base, suffix = field.rsplit('_',1)
                    if base in rows[0]:
                        values = [float(r[base]) for r in rows]
                        expected = statistics.mean(values) if suffix == 'mean' else statistics.stdev(values)
                        close(f'{stem} {tuple(agg[k] for k in group)}/{field}', agg[field], expected)

    # Each report display is enumerated from the actual included chapter files.
    main_text = track(ROOT/'report/main.tex').read_text(encoding='utf-8')
    displays = []
    chapters = re.findall(r'\\input\{(chapters/[^}]+)\}', main_text)
    for chapter in chapters:
        path = track(ROOT / 'report' / (chapter + '.tex'))
        text = path.read_text(encoding='utf-8')
        for match in re.finditer(r'\\begin\{(table|figure)\}(.*?)\\end\{\1\}', text, re.S):
            kind, body = match.group(1), match.group(2)
            labels = re.findall(r'\\label\{([^}]+)\}', body)
            graphics = re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', body)
            check('display caption and label', '\\caption{' in body and len(labels) == 1, str(labels))
            for graphic in graphics:
                check('included graphic exists', (ROOT/'report'/graphic).is_file(), graphic)
            displays.append(dict(kind=kind, label=labels[0] if labels else '', source=path.relative_to(ROOT).as_posix(),
                                 line=text[:match.start()].count('\n')+1, graphics=graphics, body=body))
    results_tex = (ROOT/'report/chapters/results_discussion.tex').read_text(encoding='utf-8')
    labels = {'random_forest_42':'RF-42', 'stacking_42':'Stacking-42', 'random_forest_17':'RF-17'}
    blocks = {r['label']:r['body'] for r in displays}
    cost = load(P9 + 'cost_metrics.csv')
    for pipe, label in labels.items():
        row = by_key[('official_test',pipe)]
        expected = [f'{float(row["macro_f1"]):.6f}', f'{float(row["mcc"]):.6f}',
                    f'{float(row["false_positive_rate"])*100:.4f}', f'{float(row["false_negative_rate"])*100:.4f}', row['fp'],row['fn']]
        table_row = next(x for x in blocks['tab:ket-qua-official'].splitlines() if x.startswith(label))
        check('report official row '+pipe, [x.strip() for x in table_row.split('&')[1:]] == expected[:-1]+[expected[-1]+' \\\\'])
        novel = by_key[('novel_vector_test',pipe)]
        for number in (row['macro_f1'], novel['macro_f1']):
            check('report novel rounding '+pipe, f'{float(number):.6f}' in blocks['tab:novel-vector'])
        c = next(r for r in cost if r['pipeline'] == pipe)
        for field, digits in [('train_time_seconds',3),('inference_ms_per_sample',6),('serialized_model_size_mb',3)]:
            check('report historical cost '+pipe+'/'+field, f'{float(c[field]):.{digits}f}' in blocks['tab:chi-phi'])
    for row in delta:
        if (row['eval_view'],row['model_a'],row['model_b']) == ('official_test','stacking_42','random_forest_42'):
            for field in ('delta_a_minus_b','ci_lower','ci_upper'):
                check('report paired CI rounding '+row['metric']+'/'+field, f'{float(row[field]):+.6f}' in blocks['tab:chenh-lech-ci'])
    check('report Holm rounded', '0.468377' in results_tex)
    check('report avoids equivalence', 'không} chứng minh hai mô hình tương đương' in results_tex)

    acceptance_path = track(ROOT/'results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json')
    acceptance = json.loads(acceptance_path.read_text(encoding='utf-8'))
    items = [v for r in acceptance['results'].values() for v in r['checks'].values()]
    check('P15 saved acceptance exactly 69 true', len(items) == 69 and all(v is True for v in items))
    check('P15 saved no fit/TEST', acceptance['training_performed'] is False and acceptance['official_test_opened'] is False)
    for candidate, run in acceptance['run_names'].items():
        base = ROOT/'results/reproducibility'/run
        supervisor = json.loads(track(base/'run_report.json').read_text(encoding='utf-8'))
        worker = json.loads(track(base/'worker/worker_result.json').read_text(encoding='utf-8'))
        check('P15 run PASS '+candidate, supervisor['result'] == 'PASS' and worker['passed'] is True)

    pdfs = sorted(set(list((ROOT/'results/eda/unsw_nb15/figures').glob('*.pdf')) +
                      list((ROOT/P11/'figures').glob('*.pdf')) + list((ROOT/'results/figures').glob('*/*.pdf'))))
    import fitz
    pdf_inventory = []
    for path in pdfs:
        track(path)
        doc = fitz.open(path)
        page = doc[0]
        spans = [s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
        outside = [s['text'] for s in spans if not (page.rect + (-1,-1,1,1)).contains(fitz.Rect(s['bbox']))]
        images = [dict(pixel_width=i[2],pixel_height=i[3],effective_dpi=[72*i[2]/r.width,72*i[3]/r.height])
                  for i in page.get_images(full=True) for r in page.get_image_rects(i[0])]
        record = dict(path=path.relative_to(ROOT).as_posix(),pages=len(doc),width_mm=page.rect.width*25.4/72,
                      height_mm=page.rect.height*25.4/72,min_text_pt=min((s['size'] for s in spans),default=None),
                      text_spans=len(spans),outside_text=outside,raster_images=images,
                      warning_under_8pt=any(s['size'] < 8 for s in spans))
        check('PDF single page '+record['path'], len(doc) == 1)
        check('PDF media-box text '+record['path'], not outside)
        pdf_inventory.append(record)
        page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(out/(path.stem+'.preview.png'))
        doc.close()

    for rel, expected in inputs.items():
        check('input unchanged '+rel, sha(ROOT/rel) == expected)
    with (out/'derived_metric_identities.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(derived[0])); writer.writeheader();writer.writerows(derived)
    (out/'display_inventory.json').write_text(json.dumps(displays,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'pdf_inventory.json').write_text(json.dumps(pdf_inventory,indent=2),encoding='utf-8')
    (out/'source_manifest.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
    result=dict(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                scope='SAVED_SUMMARIES_ONLY; no raw TRAIN/TEST or prediction CSV read; no fitting/bootstrap',
                checks=checks,pass_count=sum(r['passed'] for r in checks),fail_count=sum(not r['passed'] for r in checks),
                pdf_count=len(pdfs),display_count=len(displays),pdf_tool_version=fitz.VersionBind,
                limitations=['Accepted 37-page PDF absent locally; prior sampled QA reused, not rerun.',
                             'Input hash stability and text bounds do not prove full semantic or visual correctness.',
                             'Existing multipanel figures have no fresh backend alignment manifest.',
                             'Historical training environment UNKNOWN; reconstructed artifacts are separate.'])
    (out/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('pass_count','fail_count','pdf_count','display_count')}))
    for row in checks:
        if not row['passed']: print('FAIL:',row)
    return int(result['fail_count'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
