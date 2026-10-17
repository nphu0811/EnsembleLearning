"""P21 supervised TRAIN-only resource pilot. No official TEST; no scientific scores.

Executes only one FIT-only Stacking-Lite resource arm after an explicit, exact opt-in string.
P21 scientific experiment and 5-seed matrix remain NOT AUTHORIZED/NOT RUN.
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

from p21_pilot_guards import (
    ROOT, GIB, TRAIN, safe_new_pilot_output, sha256_stream,
    within_pilot_size, within_resource_budget,
)
from p21_protocol_validator import static_audit
from p15_local_supervisor import resource_sample, stop_tree

WORKER = ROOT / "tools" / "p21_stack_lite_pilot_worker.py"
CONSENT = "I_AUTHORIZE_TRAIN_ONLY_P21_STACK_LITE_PILOT"
CAP_BYTES = 2 * GIB
FLOOR_BYTES = int(1.5 * GIB)
EXPECTED_VERSION = [3, 11]


def pilot_timeout_ok(minutes: float) -> bool:
    return 5 <= minutes <= 20


def acceptable_worker(result: dict, rows: int, source_sha: str) -> bool:
    return (
        result.get("passed") is True
        and result.get("scope") == "P21_STACK_LITE_FIT_ONLY_RESOURCE_PILOT; no RQ result"
        and result.get("source_sha256") == source_sha
        and result.get("pilot_fit_rows") == rows
        and result.get("feature_count") == 42
        and result.get("pilot_component") == "A4_STACK42_LITE"
        and result.get("inner_cv_folds") == 3
        and result.get("inner_cv_seed") == 137
        and result.get("fit_seconds",0) > 0
        and result.get("split",{}).get("group_disjoint") is True
        and result.get("split",{}).get("validation_evaluation_performed") is False
        and all(result.get(x) is False for x in (
            "validation_predicted","official_test_opened",
            "scientific_metrics_calculated","model_artifact_saved"))
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--pilot-rows", type=int, default=8000)
    parser.add_argument("--timeout-min", type=float, default=20.0)
    parser.add_argument("--authorize", type=str, required=True,
                        help="Explicit pilot-only opt-in: " + CONSENT)
    args = parser.parse_args()
    if args.authorize != CONSENT:
        parser.error("Refuse training: exact P21 pilot-only authorization required")
    if not within_pilot_size(args.pilot_rows):
        parser.error("P21 pilot fit size must be 1000..20000")
    if not pilot_timeout_ok(args.timeout_min):
        parser.error("P21 pilot must have a wall-time bound of 5..20 minutes")
    try:
        raw = args.out_dir
        base = (ROOT / "results/controlled_extensions").resolve(strict=True)
        candidate = raw if raw.is_absolute() else ROOT / raw
        if candidate.exists() or candidate.is_symlink() or candidate.parent.resolve(strict=True) != base or not candidate.name.startswith("p21_train_only_pilot_stacklite_"):
            raise ValueError("RQ5 output must be a new direct p21_train_only_pilot_stacklite_* directory")
        out = candidate
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    try:
        import psutil
    except ImportError:
        print("NO_GO: psutil required, no subprocess started", file=sys.stderr)
        return 2

    # First complete source integrity (official TRAIN raw bytes; not a model fit).
    audit = static_audit(verify_train=True)
    if audit["failed"] or audit["passed"] != 30:
        print(json.dumps({"status": "NO_GO_SOURCE_AUDIT", "failed": [
            x["id"] for x in audit["checks"] if not x["pass"]
        ]}, indent=2))
        return 2

    config_path = ROOT / "config/p21_train_only_protocol_2026_10_18.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if (config["training_authorized"] is not False or
            config["first_experiment_executed"] is not False or
            config["runtime"]["pilot_required"] is not True):
        print("NO_GO: only a design-stage pilot can run with this launcher", file=sys.stderr)
        return 2

    # Ensure expected version on selected interpreter; never pip install.
    check = subprocess.run([sys.executable, "-c",
        "import sys,importlib.metadata,json; import numpy,pandas,sklearn,scipy,psutil,threadpoolctl; "
        "print(json.dumps({'python':list(sys.version_info[:2]),'versions':"
        "{n:importlib.metadata.version(n) for n in "
        "['numpy','pandas','scikit-learn','scipy','psutil','threadpoolctl']}}))"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=30, check=False)
    try:
        spec = json.loads(check.stdout.strip()) if check.returncode == 0 else None
    except json.JSONDecodeError:
        spec = None
    if not spec or spec["python"] != EXPECTED_VERSION:
        print("NO_GO: Python 3.11 ML environment unavailable (or unexpected error)",
              file=sys.stderr)
        return 2
    # Optional provenance strictness: compatible P15 library stack, no auto change.
    if (spec["versions"].get("scikit-learn") != "1.9.0" or
            spec["versions"].get("pandas") != "3.0.5"):
        print("NO_GO: expected author-verified P15 scikit-learn/pandas versions",
              file=sys.stderr)
        return 2

    available = int(psutil.virtual_memory().available)
    disk = int(shutil.disk_usage(ROOT).free)
    budget = {
        "system_available_bytes": available, "disk_free_bytes": disk,
        "process_tree_rss_cap_bytes": CAP_BYTES,
        "system_available_floor_bytes": FLOOR_BYTES,
        "passed": within_resource_budget(available, disk, CAP_BYTES, FLOOR_BYTES),
    }
    if not budget["passed"]:
        print(json.dumps({"status": "NO_GO_RESOURCE_GATE", "budget": budget}, indent=2))
        return 2

    # Separate immutable execution directory; keep failed records and no overwrites.
    out.mkdir(mode=0o700, exist_ok=False)
    (out / "worker").mkdir()
    report = {
        "phase": "P21", "status": "INCOMPLETE", "scope": "TRAIN_ONLY_STACK_LITE_RESOURCE_PILOT",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_sha256": sha256_stream(config_path),
        "train_sha256": config["source"]["sha256"],
        "python_executable": sys.executable,
        "versions": spec["versions"], "pilot_rows": args.pilot_rows,
        "timeout_minutes": args.timeout_min, "budget": budget,
        "peak_tree_rss_bytes": 0, "resource_samples": 0,
        "official_test_opened": False, "scientific_metrics_calculated": False,
        "model_artifact_saved": False, "full_P21_training_authorized": False,
        "exit_code": None, "stop_reason": "NOT_STARTED",
    }
    (out / "start.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")

    env = os.environ.copy()
    env.update({
        "P21_STACK_WATCHED": "1", "PYTHONDONTWRITEBYTECODE": "1",
        "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1", "LOKY_MAX_CPU_COUNT": "1",
    })
    proc = None
    started = time.monotonic()
    peak = 0
    min_available = None
    reason = None
    samples = 0
    stdout_handle = (out / "worker.stdout.log").open("w", encoding="utf-8")
    stderr_handle = (out / "worker.stderr.log").open("w", encoding="utf-8")
    args_worker = [sys.executable, "-u", str(WORKER), "--out-dir", str(out / "worker"),
                   "--pilot-rows", str(args.pilot_rows)]
    kwargs = {"cwd": str(ROOT), "env": env,
              "stdout": stdout_handle, "stderr": stderr_handle}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    try:
        proc = subprocess.Popen(args_worker, **kwargs)
        parent = psutil.Process(proc.pid)
        affinity = parent.cpu_affinity()
        if not affinity:
            raise RuntimeError("Missing worker CPU affinity")
        parent.cpu_affinity([affinity[0]])
        (out / "heartbeat").touch()
        (out / "go.signal").write_text("P21_STACK_LITE_PILOT_ONLY\n", encoding="utf-8")

        with (out / "resources.csv").open("w", encoding="utf-8") as log:
            log.write("seconds,tree_rss_bytes,available_ram_bytes,disk_free_bytes,process_count\n")
            while proc.poll() is None:
                (out / "heartbeat").touch()
                data = resource_sample(psutil, proc.pid, ROOT, CAP_BYTES, FLOOR_BYTES)
                peak = max(peak, data["rss_bytes"])
                min_available = (data["available_ram_bytes"] if min_available is None
                                 else min(min_available, data["available_ram_bytes"]))
                samples += 1
                log.write(
                    f"{time.monotonic()-started:.2f},{data['rss_bytes']},"
                    f"{data['available_ram_bytes']},{data['disk_free_bytes']},"
                    f"{data['processes_seen']}\n")
                log.flush()
                if data["stop_reason"]:
                    reason = data["stop_reason"]
                    break
                if time.monotonic() - started > args.timeout_min * 60:
                    reason = "TIMEOUT"
                    break
                time.sleep(0.5)
        if reason:
            stop_tree(psutil, proc.pid)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            reason = reason or "WORKER_WOULD_NOT_EXIT"
            stop_tree(psutil, proc.pid)
        report["exit_code"] = proc.returncode
    except (Exception, KeyboardInterrupt) as exc:
        reason = reason or ("INTERRUPTED" if isinstance(exc, KeyboardInterrupt)
                            else "WATCHDOG_ERROR_" + type(exc).__name__)
        report["watchdog_error"] = str(exc)[:400]
        if proc is not None:
            stop_tree(psutil, proc.pid)
    finally:
        stdout_handle.close()
        stderr_handle.close()
        report["stop_reason"] = reason
        report["peak_tree_rss_bytes"] = peak
        report["minimum_system_available_bytes"] = min_available
        report["resource_samples"] = samples
        report["wall_seconds"] = round(time.monotonic() - started, 3)
        worker_result = out / "worker" / "worker_result.json"
        if reason is None and report.get("exit_code") == 0 and worker_result.is_file():
            try:
                candidate = json.loads(worker_result.read_text(encoding="utf-8"))
                if (samples > 0 and peak > 0 and peak < CAP_BYTES and
                        acceptable_worker(candidate, args.pilot_rows, config["source"]["sha256"])
                        and sha256_stream(TRAIN) == config["source"]["sha256"]):
                    report["status"] = "PASS_STACK_LITE_RESOURCE_SMOKE_ONLY"
                    report["worker_checks"] = candidate
                else:
                    report["stop_reason"] = "WORKER_OUTPUT_INVALID"
            except (ValueError, OSError, KeyError):
                report["stop_reason"] = "WORKER_OUTPUT_UNREADABLE"
        elif reason is None:
            report["stop_reason"] = "WORKER_FAILED_OR_MISSING_OUTPUT"
        (out / "run_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    print(json.dumps({
        "status": report["status"], "stop_reason": report["stop_reason"],
        "peak_tree_rss_mib": round(peak / (1024*1024), 1),
        "elapsed_seconds": report["wall_seconds"],
        "report": str(out / "run_report.json"),
    }, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS_STACK_LITE_RESOURCE_SMOKE_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
