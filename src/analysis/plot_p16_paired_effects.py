"""Plot one frozen paired-effect contrast. No statistics fitting or test access."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project-root', type=Path, default=Path.cwd())
    ap.add_argument('--outdir', type=Path, required=True)
    ap.add_argument('--qa-scripts', type=Path, required=True,
                    help='Directory containing audit_panel_alignment.py')
    args = ap.parse_args()
    root=args.project_root.resolve()
    out=args.outdir.resolve()
    if out.exists():
        raise SystemExit('Refuse overwrite; use a new output directory.')
    sys.path.insert(0,str(args.qa_scripts.resolve()))
    from audit_panel_alignment import require_matplotlib_panel_alignment
    source=root/'results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv'
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    expected='3338849b204702597a05c271cb309f2928e9850a1e2d5dedc6a54548256f7d90'
    if sha!=expected:
        raise ValueError('Frozen table hash differs; review evidence before rendering.')
    with source.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    selected=[r for r in rows if r['eval_view']=='official_test'
              and r['model_a']=='stacking_42' and r['model_b']=='random_forest_42']
    order=['macro_f1','mcc','false_positive_rate','false_negative_rate']
    assert len(selected)==4 and {r['metric'] for r in selected}==set(order)
    selected=sorted(selected,key=lambda r:order.index(r['metric']))
    for r in selected:
        assert float(r['ci_lower'])<=float(r['delta_a_minus_b'])<=float(r['ci_upper'])
        assert r['bootstrap_replicates']=='10000' and float(r['ci_level'])==0.95
    out.mkdir(parents=True)
    with (out/'source_data.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(selected[0]))
        writer.writeheader();writer.writerows(selected)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],
        'font.size':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':9,
        'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,
        'svg.fonttype':'none','pdf.fonttype':42,'axes.linewidth':0.8,
        'legend.frameon':False})
    fig,ax=plt.subplots(figsize=(183/25.4,100/25.4))
    fig.subplots_adjust(left=0.29,right=0.94,bottom=0.25,top=0.79)
    fig.suptitle('Paired effects on the official UNSW-NB15 test',x=0.06,y=0.96,
                 ha='left',fontsize=11,fontweight='bold')
    fig.text(0.06,0.875,'Stacking-42 minus RF-42  |  Points and 95% paired bootstrap intervals',fontsize=9)
    ax.axvline(0,color='#757575',linestyle='--',linewidth=0.8,zorder=0)
    for y,r in zip([3,2,1,0],selected):
        value=100*float(r['delta_a_minus_b'])
        lo=100*float(r['ci_lower']);hi=100*float(r['ci_upper'])
        ax.errorbar(value,y,xerr=[[value-lo],[hi-value]],fmt='o',
                    color='#275D7F',ecolor='#275D7F',capsize=4,markersize=5,
                    elinewidth=1.5,zorder=2)
    ax.set_yticks([3,2,1,0],['Macro-F1','MCC','False positive rate','False negative rate'])
    ax.tick_params(axis='y',length=0,pad=9)
    ax.set_ylim(-0.65,3.65)
    ax.set_xlim(-0.65,0.45)
    ax.set_xticks([-0.6,-0.4,-0.2,0,0.2,0.4])
    ax.set_xlabel('Difference × 100 (rate differences in percentage points)',labelpad=10)
    fig.text(0.06,0.065,'82,332 benchmark rows; 10,000 bootstrap resamples. Intervals are conditional on these rows.',fontsize=8)
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig,json_out=str(out/'paired_effects.alignment.json'),
        overlay_svg=str(out/'paired_effects.alignment.svg'),tolerance_pt=1.5,
        gutter_tolerance_pt=1.5,strict=True)
    fig.savefig(out/'paired_effects.pdf')
    fig.savefig(out/'paired_effects.svg')
    fig.savefig(out/'paired_effects.png',dpi=600)
    plt.close(fig)
    metadata={'input':source.relative_to(root).as_posix(),'input_sha256':sha,
        'source_rows':len(rows),'selected_rows':len(selected),
        'selection_rule':'official_test; stacking_42 minus random_forest_42; all four stored metrics',
        'omitted_rows':len(rows)-len(selected),'omission_reason':'Other model/view contrasts outside this figure contract; preserved in source',
        'transform':'All delta/CI values multiplied by 100; not relative percent change',
        'new_bootstrap':False,'training_or_prediction':False,'width_mm':183,'height_mm':100,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version':matplotlib.__version__}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(json.dumps(metadata,indent=2))


if __name__=='__main__':
    main()
