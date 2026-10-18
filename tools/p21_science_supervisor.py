"""P21 full five-arm one-seed TRAIN-only experiment supervisor.

Run ONE of 5 fixed seeds per invocation; external shell can sequence all five.
NO WALL-TIME LIMIT for scientific training; memory, disk, CPU and heartbeat
watchdogs are mandatory. No official TEST or historical frozen artifact writes.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from p21_pilot_guards import ROOT,GIB,TRAIN,sha256_stream,within_resource_budget
from p21_protocol_validator import static_audit
from p21_science_acceptance import SEEDS,acceptable_science_worker
from p15_local_supervisor import resource_sample,stop_tree

WORKER = ROOT / "tools" / "p21_science_worker.py"
CONFIG = ROOT / "config" / "p21_train_only_protocol_2026_10_18.json"
CONSENT = "I_AUTHORIZE_P21_TRAIN_ONLY_POST_HOC_FULL_SCIENCE"
CAP = 2 * GIB
FLOOR = int(1.5 * GIB)


def path_for_seed(raw: Path, seed: int) -> Path:
    base = (ROOT / "results" / "controlled_extensions").resolve(strict=True)
    candidate = raw if raw.is_absolute() else ROOT / raw
    if (candidate.exists() or candidate.is_symlink() or
            candidate.parent.resolve(strict=True) != base or
            not candidate.name.startswith(f"p21_train_only_science_seed_{seed}_") or
            candidate.name in ("",".","..")):
        raise ValueError("Use a new direct science output directory for this exact seed")
    return candidate


def pilots_pass(source_sha):
    """Four preceding author resource pilots are required on local disk."""
    base = ROOT / "results" / "controlled_extensions"
    for prefix, status in [
        ("p21_train_only_pilot_rf42_","PASS_RESOURCE_SMOKE_ONLY"),
        ("p21_train_only_pilot_selector17_","PASS_SELECTOR_RESOURCE_SMOKE_ONLY"),
        ("p21_train_only_pilot_rq5_","PASS_RQ5_RESOURCE_SMOKE_ONLY"),
        ("p21_train_only_pilot_stacklite_","PASS_STACK_LITE_RESOURCE_SMOKE_ONLY"),
    ]:
        success=False
        for path in sorted(base.glob(prefix+"*/run_report.json")):
            try:
                if path.is_symlink() or path.parent.is_symlink():
                    continue
                report=json.loads(path.read_text(encoding="utf-8"))
                checks=report.get("worker_checks",{})
                if (report.get("status")==status and
                    report.get("train_sha256")==source_sha and
                    report.get("exit_code")==0 and
                    checks.get("source_sha256")==source_sha and
                    checks.get("official_test_opened") is False and
                    checks.get("scientific_metrics_calculated") is False and
                    report.get("peak_tree_rss_bytes",0)>0 and
                    report.get("peak_tree_rss_bytes",CAP)>=CAP) :
                    continue
                if report.get("status")==status and (
                    report.get("train_sha256")==source_sha and
                    checks.get("source_sha256")==source_sha and
                    checks.get("official_test_opened") is False and
                    checks.get("scientific_metrics_calculated") is False and
                    report.get("peak_tree_rss_bytes",0)>0 and
                    report.get("peak_tree_rss_bytes",CAP)<CAP
                ):
                    success=True
            except (OSError,ValueError,TypeError,KeyError):
                continue
        if not success:
            raise ValueError("Missing accepted resource pilot: "+prefix)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",required=True,type=int,choices=SEEDS)
    parser.add_argument("--out-dir",required=True,type=Path)
    parser.add_argument("--authorize",required=True)
    args=parser.parse_args()
    if args.authorize!=CONSENT:
        parser.error("Exact author scientific scope consent missing")
    try:
        out=path_for_seed(args.out_dir,args.seed)
    except (OSError,ValueError) as exc:
        parser.error(str(exc))
    try:
        import psutil
    except ImportError:
        print("NO_GO: psutil required; no worker started",file=sys.stderr)
        return 2
    audit=static_audit(verify_train=True)
    if audit.get("failed") or audit.get("passed")!=30:
        print(json.dumps({"status":"NO_GO_PROTOCOL","audit":audit},indent=2))
        return 2
    cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
    source_sha=cfg["source"]["sha256"]
    if cfg["training_authorized"] is not False or cfg["first_experiment_executed"] is not False:
        print("NO_GO: immutable original P21 contract changed",file=sys.stderr)
        return 2
    try:
        pilots_pass(source_sha)
    except ValueError as exc:
        print("NO_GO_PILOT_EVIDENCE: "+str(exc),file=sys.stderr)
        return 2

    check=subprocess.run(
        [sys.executable,"-c",
         "import sys,importlib.metadata,json,numpy,pandas,sklearn,scipy,psutil,threadpoolctl; "
         "print(json.dumps({'python':list(sys.version_info[:2]),'versions':"
         "{x:importlib.metadata.version(x) for x in "
         "['numpy','pandas','scikit-learn','scipy','psutil','threadpoolctl']}}))"],
        cwd=str(ROOT),capture_output=True,text=True,check=False,timeout=30)
    try:
        envinfo=json.loads(check.stdout) if check.returncode==0 else None
    except (ValueError,TypeError):
        envinfo=None
    if (not envinfo or envinfo.get("python")!=[3,11] or
        envinfo["versions"].get("pandas")!="3.0.5" or
        envinfo["versions"].get("scikit-learn")!="1.9.0"):
        print("NO_GO_PYTHON_ENV: expected author-verified Python3.11/pandas3.0.5/sklearn1.9.0",file=sys.stderr)
        return 2
    available=int(psutil.virtual_memory().available)
    free=int(shutil.disk_usage(ROOT).free)
    if not within_resource_budget(available,free,CAP,FLOOR):
        print(json.dumps({"status":"NO_GO_RESOURCE_GATE",
            "available_bytes":available,"disk_free_bytes":free,
            "required_available_bytes":4*GIB,"cap_bytes":CAP,
            "floor_bytes":FLOOR},indent=2))
        return 2

    out.mkdir(mode=0o700,exist_ok=False)
    (out/"worker").mkdir()
    report={
        "phase":"P21","status":"INCOMPLETE","scope":"TRAIN_REUSED_POST_HOC_P21_SCIENCE",
        "seed":args.seed,
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "source_sha256":source_sha,
        "protocol_sha256":sha256_stream(CONFIG),
        "python_executable":sys.executable,
        "versions":envinfo["versions"],
        "resource_policy":{"peak_tree_rss_cap_bytes":CAP,
             "available_ram_floor_bytes":FLOOR,
             "start_available_bytes":available,"start_disk_free_bytes":free,
             "full_training_has_wall_timeout":False},
        "official_test_opened":False,
        "results_are_independent_external_test":False,
        "peak_tree_rss_bytes":0,"resource_samples":0,
        "stop_reason":"NOT_STARTED","exit_code":None,
    }
    (out/"start.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    env=os.environ.copy()
    env.update({
        "P21_SCIENCE_WATCHED":"1","PYTHONDONTWRITEBYTECODE":"1",
        "OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1","MKL_NUM_THREADS":"1",
        "VECLIB_MAXIMUM_THREADS":"1","NUMEXPR_NUM_THREADS":"1",
        "LOKY_MAX_CPU_COUNT":"1",
    })
    with (out/"worker.stdout.log").open("w",encoding="utf-8") as stdout, (
         out/"worker.stderr.log").open("w",encoding="utf-8") as stderr:
        kwargs={"cwd":str(ROOT),"env":env,"stdout":stdout,"stderr":stderr}
        if os.name=="nt":
            kwargs["creationflags"]=subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"]=True
        proc=None
        reason=None
        started=time.monotonic()
        peak=0
        min_avail=None
        samples=0
        try:
            proc=subprocess.Popen(
                [sys.executable,"-u",str(WORKER),"--seed",str(args.seed),
                 "--out-dir",str(out/"worker")],**kwargs)
            parent=psutil.Process(proc.pid)
            cpus=parent.cpu_affinity()
            if not cpus:
                raise RuntimeError("CPU affinity unavailable")
            parent.cpu_affinity([cpus[0]])
            (out/"heartbeat").touch()
            (out/"go.signal").write_text(
                "P21_TRAIN_ONLY_SCIENCE_SEED\n",encoding="utf-8")
            with (out/"resources.csv").open("w",encoding="utf-8") as log:
                log.write("seconds,tree_rss_bytes,available_ram_bytes,disk_free_bytes,process_count\n")
                while proc.poll() is None:
                    (out/"heartbeat").touch()
                    sample=resource_sample(psutil,proc.pid,ROOT,CAP,FLOOR)
                    peak=max(peak,sample["rss_bytes"])
                    available_now=sample["available_ram_bytes"]
                    min_avail=available_now if min_avail is None else min(min_avail,available_now)
                    samples+=1
                    log.write(f"{time.monotonic()-started:.2f},{sample['rss_bytes']},{available_now},{sample['disk_free_bytes']},{sample['processes_seen']}\n")
                    log.flush()
                    if sample["stop_reason"]:
                        reason=sample["stop_reason"]
                        break
                    # SCIENCE RUN: deliberately NO wall-clock timeout.
                    time.sleep(0.5)
            if reason:
                stop_tree(psutil,proc.pid)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                reason=reason or "UNSTOPPABLE_WORKER"
                stop_tree(psutil,proc.pid)
            report["exit_code"]=proc.returncode
        except (Exception,KeyboardInterrupt) as exc:
            reason=reason or ("INTERRUPTED" if isinstance(exc,KeyboardInterrupt)
                              else "WATCHDOG_ERROR_"+type(exc).__name__)
            report["watchdog_error"]=str(exc)[:400]
            if proc is not None:
                stop_tree(psutil,proc.pid)
        finally:
            report["stop_reason"]=reason
            report["peak_tree_rss_bytes"]=peak
            report["minimum_available_ram_bytes"]=min_avail
            report["resource_samples"]=samples
            report["elapsed_seconds"]=round(time.monotonic()-started,3)
            worker_report=out/"worker"/"worker_result.json"
            if reason is None and report.get("exit_code")==0 and worker_report.is_file():
                try:
                    result=json.loads(worker_report.read_text(encoding="utf-8"))
                    if (samples>0 and 0<peak<CAP and
                        acceptable_science_worker(result,args.seed,
                            source_sha,report["protocol_sha256"]) and
                        sha256_stream(TRAIN)==source_sha):
                        report["status"]="PASS_INTERNAL_TRAIN_VALIDATION_SEED_ONLY"
                        report["worker_checks"]=result
                    else:
                        report["stop_reason"]="INVALID_WORKER_METRICS_OR_SCOPE"
                except (OSError,ValueError,TypeError):
                    report["stop_reason"]="INVALID_WORKER_RESULT"
            elif reason is None:
                report["stop_reason"]="WORKER_FAILED_OR_MISSING_RESULT"
            (out/"run_report.json").write_text(
                json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":report["status"],"seed":args.seed,
        "stop_reason":report.get("stop_reason"),
        "peak_tree_rss_mib":round(peak/1024**2,1),
        "elapsed_seconds":report["elapsed_seconds"],
        "report":str(out/"run_report.json"),
        "no_full_training_time_limit":True,
    },ensure_ascii=False,indent=2))
    return 0 if report["status"]=="PASS_INTERNAL_TRAIN_VALIDATION_SEED_ONLY" else 2


if __name__=="__main__":
    raise SystemExit(main())
