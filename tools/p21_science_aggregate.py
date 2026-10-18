"""Aggregate FIVE independently accepted P21 TRAIN-only seed reports.

Reads only compact JSON metadata; no ML/dataset/official TEST reads.
Refuses cherry-picked multiple successful attempts for any replication seed.
Descriptive replicated-FIT variability, NOT independent benchmark CI.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics

from p21_pilot_guards import ROOT, sha256_stream
from p21_science_acceptance import ARM_IDS,SEEDS,acceptable_science_worker

CONFIG=ROOT/"config/p21_train_only_protocol_2026_10_18.json"
BASE=ROOT/"results"/"controlled_extensions"
MEASURES=("macro_f1","mcc","attack_precision","attack_recall","fpr","fnr")
PAIRS={
    "RQ1_STACK42_MINUS_RF42":("A4_STACK42_NONE","A0_RF42_NONE"),
    "RQ2_RF17_MINUS_RF42":("A1_RF17_NONE","A0_RF42_NONE"),
    "RQ5_BALANCED_MINUS_NONE":("A2_RF42_BALANCED","A0_RF42_NONE"),
    "RQ5_OVERSAMPLE_MINUS_NONE":("A3_RF42_OVERSAMPLE","A0_RF42_NONE"),
}


def load_complete_seeds(base: Path, config: dict, protocol_sha: str):
    seen={}
    src=config["source"]["sha256"]
    root=base.resolve(strict=True)
    for path in sorted(base.glob("p21_train_only_science_seed_*/run_report.json")):
        if path.is_symlink() or path.parent.is_symlink() or path.parent.parent.resolve()!=root:
            raise ValueError("Suspicious science evidence symlink or traversal")
        report=json.loads(path.read_text(encoding="utf-8"))
        if report.get("status")!="PASS_INTERNAL_TRAIN_VALIDATION_SEED_ONLY":
            continue   # Failed/interrupted seeds remain auditable but are NOT results.
        seed=report.get("seed")
        worker=report.get("worker_checks")
        if (seed not in SEEDS or seed in seen or
                report.get("exit_code")!=0 or report.get("stop_reason") is not None or
                report.get("source_sha256")!=src or
                report.get("protocol_sha256")!=protocol_sha or
                report.get("official_test_opened") is not False or
                report.get("results_are_independent_external_test") is not False or
                not acceptable_science_worker(worker,seed,src,protocol_sha)):
            raise ValueError("Duplicate or invalid successful science seed report")
        seen[seed]={
            "worker":worker,
            "report_path":str(path.relative_to(ROOT)),
            "run_report_sha256":sha256_stream(path),
        }
    if set(seen)!=set(SEEDS):
        raise ValueError("INCOMPLETE: need exactly 5 accepted seed runs; missing "+
                         ", ".join(str(x) for x in SEEDS if x not in seen))
    return seen


def describe(numbers):
    if len(numbers)!=5 or not all(isinstance(x,(int,float)) and math.isfinite(x) for x in numbers):
        raise ValueError("Exactly five finite replicated statistics required")
    return {"mean":statistics.mean(numbers),"sample_std":statistics.stdev(numbers),
            "min":min(numbers),"max":max(numbers),"values_by_seed":numbers}


def summarize(seen):
    per_seed={}
    for seed in SEEDS:
        w=seen[seed]["worker"]
        per_seed[str(seed)]={
            "fit_ids_sha256":w["fit_row_ids_sha256"],
            "selected_feature_names":w["selector"]["feature_names"],
            "selected_features_sha256":w["selector"]["feature_names_sha256"],
            "metrics_by_arm":{a["arm"]:a["metrics"] for a in w["arms"]},
            "fit_seconds_by_arm":{a["arm"]:a["fit_seconds"] for a in w["arms"]},
        }
    arm_summary={}
    for arm in ARM_IDS:
        arm_summary[arm]={
            key:describe([per_seed[str(seed)]["metrics_by_arm"][arm][key]
                          for seed in SEEDS])
            for key in MEASURES
        }
        arm_summary[arm]["fit_seconds"]=describe([
            per_seed[str(seed)]["fit_seconds_by_arm"][arm] for seed in SEEDS])
    contrasts={}
    for label,(a,b) in PAIRS.items():
        contrasts[label]={
            k:describe([
                per_seed[str(seed)]["metrics_by_arm"][a][k]-
                per_seed[str(seed)]["metrics_by_arm"][b][k]
                for seed in SEEDS])
            for k in MEASURES
        }
    return per_seed,arm_summary,contrasts


def markdown_report(output: dict) -> str:
    fmt=lambda x:f'{x["mean"]:.6f} ± {x["sample_std"]:.6f}'
    lines=[
        "# P21 — Descriptive TRAIN-derived 5-seed internal-validation results",
        "",
        "> POST-HOC reused official TRAIN (not official TEST). All 5 seeds share",
        "> one grouped internal-validation partition. Not independent experiments",
        "> or a prospective test of superiority. No p-values or external claims.",
        "",
        "## Per-arm summaries (mean ± sample SD across five FIT replications)",
        "",
        "| Arm | Macro-F1 | MCC | FPR | FNR | Mean fit time (s) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm,stats in output["arm_summary"].items():
        lines.append(f"| {arm} | {fmt(stats['macro_f1'])} | {fmt(stats['mcc'])} | "
                     f"{fmt(stats['fpr'])} | {fmt(stats['fnr'])} | "
                     f"{stats['fit_seconds']['mean']:.3f} |")
    lines+=["","## Paired contrasts (first arm minus baseline)","","| Contrast | Δ Macro-F1 | Δ FNR | Δ FPR | Δ MCC |","|---|---:|---:|---:|---:|"]
    for name,s in output["contrasts"].items():
        lines.append(f"| {name} | {fmt(s['macro_f1'])} | {fmt(s['fnr'])} | "
                     f"{fmt(s['fpr'])} | {fmt(s['mcc'])} |")
    lines+=["",
        "## Mandatory interpretation",
        "",
        "- RQ1: comparison of lighter **group-safe** Stacking-Lite vs RF42-Lite.",
        "- RQ2: RF17 FIT-selected vs matched RF42, all RF parameters identical.",
        "- RQ5: weighting and oversampling are distinct interventions; note Normal",
        "  was the FIT minority, so no presumption that Attack recall improves.",
        "- Five seeds vary FIT subsamples and estimator seeds but use ONE shared",
        "  TRAIN-derived internal validation; no new independent external sample.",
        "- Selected17 features were re-learned per FIT seed (never reused from P9).",
        "- New group-safe inner CV is a disclosed P21 pre-full amendment.",
        "- Do not rewrite the historical official TEST P9/P15 results.",
        ""]
    return "\n".join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir",type=Path,required=True)
    args=p.parse_args()
    base=BASE.resolve(strict=True)
    out=args.out_dir if args.out_dir.is_absolute() else ROOT/args.out_dir
    if (out.exists() or out.is_symlink() or
        out.parent.resolve(strict=True)!=base or
        not out.name.startswith("p21_train_only_science_summary_")):
        p.error("Output must be a NEW direct P21 summary directory")
    cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
    protocol_sha=sha256_stream(CONFIG)
    seen=load_complete_seeds(BASE,cfg,protocol_sha)
    per_seed,arms,contrasts=summarize(seen)
    result={
        "scope":"POST_HOC_REUSED_TRAIN_INTERNAL_VALIDATION_ONLY",
        "completed_seed_count":5,"seeds":list(SEEDS),
        "source_sha256":cfg["source"]["sha256"],
        "protocol_sha256":protocol_sha,
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "official_test_read":False,
        "seeds_are_independent_external_tests":False,
        "novel_external_validation_performed":False,
        "grouped_stack_inner_cv_pre_full_amendment":True,
        "evidence":{str(k):{
            "report_path":v["report_path"],
            "report_sha256":v["run_report_sha256"]}
                    for k,v in seen.items()},
        "per_seed":per_seed,"arm_summary":arms,"contrasts":contrasts,
    }
    out.mkdir(mode=0o700,exist_ok=False)
    (out/"aggregate.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"report.md").write_text(markdown_report(result),encoding="utf-8")
    print(json.dumps({"status":"PASS_FIVE_SEED_DESCRIPTIVE_ONLY",
                      "seeds":list(SEEDS),"report":str(out/"report.md")},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
