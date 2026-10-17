"""Independent P16 figure alternatives from frozen summary CSVs only.

Contract: preserve all three pipelines and all attack categories. Horizontal
intervals avoid CI-label collisions; no grid crosses labels. Every chart is a
single panel. No raw data, retraining, bootstrap, or changes to the report.
Python/Matplotlib exclusively. Structural adaptation of historical plot roles.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
ORDER=['random_forest_42','stacking_42','random_forest_17']
LABELS=['RF-42','Stacking-42','RF-17']
COLORS=['#3F677D','#B37646','#686868']
MARKERS=['o','s','^']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-scripts',type=Path,required=True)
    parser.add_argument('--out-dir',type=Path,required=True)
    args=parser.parse_args()
    out=args.out_dir.resolve();out.mkdir(parents=True,exist_ok=False)
    sys.path.insert(0,str(args.skill_scripts.resolve()))
    from audit_panel_alignment import require_matplotlib_panel_alignment
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],'font.size':9,'axes.titlesize':10,
                         'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':9,
                         'legend.fontsize':8,'pdf.fonttype':42,'svg.fonttype':'none',
                         'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False})
    sources={};exports=[]

    def load(rel,name):
        p=ROOT/rel;sources[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
        (out/name).write_bytes(p.read_bytes())
        with p.open(encoding='utf-8-sig',newline='') as stream: return list(csv.DictReader(stream))

    base='results/final_analysis/unsw_nb15/phase10_statistics/tables/'
    ci=load(base+'bootstrap_metric_ci.csv','source_bootstrap_metric_ci.csv')
    point=load(base+'recomputed_point_metrics.csv','source_recomputed_point_metrics.csv')
    cost=load('results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv','source_cost_metrics.csv')
    attack=load(base+'attack_family_miss_rate_ci.csv','source_attack_family_miss_rate_ci.csv')
    categories=load('results/eda/unsw_nb15/tables/attack_category_distribution.csv','source_attack_category_distribution.csv')

    def figure(height=85):
        fig,ax=plt.subplots(figsize=(183/25.4,height/25.4))
        fig.subplots_adjust(left=.27,right=.96,bottom=.30,top=.84)
        return fig,ax

    def save(fig,stem,footer):
        fig.text(.27,.04,footer,fontsize=8,va='bottom')
        fig.canvas.draw()
        require_matplotlib_panel_alignment(fig,json_out=str(out/(stem+'.alignment.json')),
                                           tolerance_pt=1.5,gutter_tolerance_pt=1.5,strict=True)
        fig.savefig(out/(stem+'.pdf'),facecolor='white')
        fig.savefig(out/(stem+'.svg'),facecolor='white')
        fig.savefig(out/(stem+'.png'),dpi=600,facecolor='white')
        exports.append(dict(path=(out/(stem+'.pdf')).relative_to(ROOT).as_posix(),
                            width_mm=183,height_mm=fig.get_figheight()*25.4,panels=1,alignment='NOT_APPLICABLE_SINGLE_PANEL'))
        plt.close(fig)

    for metric,title in [('macro_f1','Macro-F1'),('mcc','MCC')]:
        fig,ax=figure()
        for i,pipe in enumerate(ORDER):
            row=next(r for r in ci if r['pipeline']==pipe and r['eval_view']=='official_test' and r['metric']==metric)
            x=float(row['point_estimate']);lo=float(row['ci_lower']);hi=float(row['ci_upper'])
            assert lo<=x<=hi
            ax.errorbar(x,i,xerr=[[x-lo],[hi-x]],fmt=MARKERS[i],color=COLORS[i],capsize=3)
        ax.set_yticks(range(3),LABELS);ax.set_ylim(2.5,-.5)
        ax.set_xlabel(title+' (absolute scale)');ax.set_title('Official holdout: '+title+' and 95% intervals',loc='left')
        save(fig,metric+'_ci','82,332 benchmark rows; stored paired row bootstrap, 10,000 resamples.\nIntervals describe benchmark sampling, not repeated training or equivalence.')

    official={r['pipeline']:r for r in point if r['eval_view']=='official_test'}
    fig,ax=figure(95);fig.subplots_adjust(left=.17)
    for i,pipe in enumerate(ORDER):
        row=official[pipe];x=100*float(row['false_positive_rate']);y=100*float(row['false_negative_rate'])
        ax.scatter(x,y,color=COLORS[i],marker=MARKERS[i],s=35)
        ax.annotate(LABELS[i],(x,y),xytext=(7,7),textcoords='offset points',fontsize=9)
    ax.set_xlim(26.3,28.3);ax.set_ylim(1.48,2.04)
    ax.set_xlabel('False positive rate (%)');ax.set_ylabel('False negative rate (%)')
    ax.set_title('Official holdout: false alarm / missed attack trade-off',loc='left')
    save(fig,'fpr_fnr_tradeoff','One frozen pipeline per point; threshold 0.5; 82,332 benchmark rows.\nPoint estimates only. No training-repeat uncertainty is available.')

    fig,ax=figure(95);fig.subplots_adjust(left=.17)
    for i,pipe in enumerate(ORDER):
        row=next(r for r in cost if r['pipeline']==pipe);x=float(row['train_time_seconds'])
        assert np.isfinite(x) and x>0
        y=float(official[pipe]['macro_f1'])
        ax.scatter(x,y,color=COLORS[i],marker=MARKERS[i],s=35)
        ax.annotate(LABELS[i],(x,y),xytext=(7,7),textcoords='offset points',fontsize=9)
    ax.set_xlim(0,1250);ax.set_ylim(.860,.865)
    ax.set_xlabel('Historical training time (seconds)');ax.set_ylabel('Official holdout Macro-F1')
    ax.set_title('Performance and historical computation cost',loc='left')
    save(fig,'performance_cost','One historical timing per pipeline; original environment UNKNOWN.\nRF-17 also differs in hyperparameters. No isolated feature-count effect.')

    fig,ax=figure(155);fig.subplots_adjust(left=.29,bottom=.15,top=.88)
    rows=[r for r in attack if r['eval_view']=='official_test']
    names=sorted({r['attack_cat'] for r in rows})
    for i,pipe in enumerate(ORDER):
        for j,cat in enumerate(names):
            row=next(r for r in rows if r['pipeline']==pipe and r['attack_cat']==cat)
            x=100*float(row['miss_rate']);lo=100*float(row['wilson_95_lower']);hi=100*float(row['wilson_95_upper'])
            assert lo<=x+1e-12 and x<=hi+1e-12
            ax.errorbar(x,j+(i-1)*.23,xerr=[[max(0,x-lo)],[max(0,hi-x)]],fmt=MARKERS[i],
                        color=COLORS[i],capsize=2,label=LABELS[i] if j==0 else None)
    ticks=[f'{cat} (n={next(r["attack_rows"] for r in rows if r["attack_cat"]==cat)})' for cat in names]
    ax.set_yticks(range(len(names)),ticks);ax.set_ylim(len(names)-.4,-.7)
    ax.set_xlabel('Attack-family false negative rate (%)')
    ax.set_title('Binary detector errors across all nine attack families',loc='left',pad=30)
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.01),ncol=3,frameon=False)
    save(fig,'attack_family_wilson','All nine families retained, including Shellcode and Worms.\nStored Wilson 95% intervals; no multiclass or independent-traffic claim.')

    fig,ax=figure(150);fig.subplots_adjust(left=.29,bottom=.16,top=.88)
    names=sorted({r['attack_category'] for r in categories})
    for i,split in enumerate(['Train','Test']):
        selected=[r for r in categories if r['split']==split]
        vals=[int(next(r for r in selected if r['attack_category']==cat)['count']) for cat in names]
        assert all(v>0 for v in vals), 'Log axis requires strictly positive counts'
        ax.barh(np.arange(len(names))+(i-.5)*.35,vals,height=.32,color=COLORS[i],label=split)
    ax.set_yticks(range(len(names)),names);ax.invert_yaxis();ax.set_xscale('log')
    ax.set_xlabel('Records (log scale, positive counts)')
    ax.set_title('Official split category distribution',loc='left',pad=30)
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.01),ncol=2,frameon=False)
    save(fig,'category_distribution','All recorded categories retained, including Normal.\nDescriptive saved counts only; no model fitting or feature selection.')
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in sources.items())
    (out/'source_manifest.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
    (out/'figure_inventory.json').write_text(json.dumps(exports,indent=2),encoding='utf-8')
    print(json.dumps(dict(figures=len(exports),source_files=len(sources),input_hashes_unchanged=True)))


if __name__=='__main__':
    main()
