"""P15 local resource supervisor (Python 3.11 + psutil). Never evaluates TEST.

Separate from the historical P9 main() because that entry point opens official TEST
and overwrites frozen results. Run --mode pilot before authorizing --mode full.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / 'tools' / 'p15_fulltrain_preflight.py'
WORKER = ROOT / 'tools' / 'p15_local_worker.py'
CANDIDATES = ('random_forest_17', 'random_forest_42', 'stacking_42')
GIB = 1024 ** 3
MIN_FREE_FLOOR = int(1.5 * GIB)
MIN_START = int(4 * GIB)
DEFAULT_CAP = int(2.0 * GIB)
MIN_DISK_FREE = 10 * GIB


def load_preflight():
    spec = importlib.util.spec_from_file_location('p15_preflight_for_supervisor', PRE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))

def sha256_stream(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as reader:
        for chunk in iter(lambda: reader.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_new_output(root: Path, raw: Path) -> Path:
    base = (root / 'results' / 'reproducibility').resolve(strict=True)
    candidate = raw if raw.is_absolute() else root / raw
    if candidate.exists() or candidate.is_symlink():
        raise ValueError('Output already exists; choose a unique directory (no overwrite).')
    parent = candidate.parent.resolve(strict=True)
    if parent != base or candidate.name in ('.', '..') or not candidate.name.startswith('p15_local_'):
        raise ValueError('Output must be a NEW direct subdirectory of results/reproducibility/p15_local_*')
    if candidate.name != os.path.basename(str(candidate)):
        raise ValueError('Invalid output basename')
    return parent / candidate.name


def timeout_policy_valid(minutes: float, mode: str) -> bool:
    """20-minute bounded pilot; full may opt in to NO deadline via exactly 0."""
    return (5 <= minutes <= 20) or (mode == 'full' and minutes == 0)


def timeout_reached(elapsed_seconds: float, minutes: float) -> bool:
    """0 explicitly disables ONLY the wall-time deadline, never the resource watchdog."""
    return minutes > 0 and elapsed_seconds > minutes * 60


def resource_budget(available: int, disk: int, cap: int, floor: int = MIN_FREE_FLOOR) -> dict:
    required = max(MIN_START, cap + floor + int(0.5 * GIB))
    checks = {
        'memory_start': available >= required,
        'disk_start': disk >= MIN_DISK_FREE,
        'cap_is_bounded': int(0.5 * GIB) <= cap <= int(3.5 * GIB),
        'floor_protected': floor >= MIN_FREE_FLOOR,
    }
    return {'checks': checks, 'passed': all(checks.values()), 'observed_available_bytes': available,
            'required_available_bytes': required, 'disk_free_bytes': disk,
            'process_tree_rss_cap_bytes': cap, 'min_system_available_bytes': floor}


def check_pilot_evidence(path: Path, candidate: str, hashes: dict, interpreter: str, cap: int) -> bool:
    try:
        d = read_json(path)
        return (d['mode'] == 'pilot' and d['candidate'] == candidate and d['result'] == 'PASS'
                and d['source_hashes'] == hashes and d['python_executable'] == interpreter
                and int(d['budget']['process_tree_rss_cap_bytes']) == cap
                and d['worker_checks']['passed'] and d['release_certified'] is False
                and d['peak_tree_rss_bytes'] < cap * 0.75)
    except (OSError, ValueError, TypeError, KeyError):
        return False


def verify_worker_result(worker: dict, candidate: str, mode: str, worker_dir: Path,
                         input_hashes: dict, package_versions: dict) -> bool:
    """Verify worker claims against actual files before recording a PASS."""
    if not (worker.get('passed') is True and worker.get('candidate') == candidate
            and worker.get('mode') == mode and worker.get('input_sha256') == input_hashes
            and worker.get('package_versions') == package_versions and worker.get('threshold') == 0.5
            and worker.get('classes') == [0, 1]
            and worker.get('train_rows') == (175341 if mode == 'full' else worker.get('train_rows'))):
        return False
    artifact = worker.get('artifact')
    if mode == 'pilot':
        return artifact is None and 1000 <= worker.get('train_rows', 0) <= 25000
    if not isinstance(artifact, dict):
        return False
    filename = artifact.get('filename')
    if filename != candidate + '_RECONSTRUCTED_FULL_TRAIN.joblib':
        return False
    path = worker_dir / filename
    if path.is_symlink() or not path.is_file() or path.resolve().parent != worker_dir.resolve():
        return False
    return (path.stat().st_size > 0 and path.stat().st_size == artifact.get('bytes')
            and sha256_stream(path) == artifact.get('sha256'))

def resource_sample(psutil, pid: int, root: Path, cap: int, floor: int):
    """A failure to read resource counters means STOP, never presume safe."""
    process = psutil.Process(pid)
    members = [process] + process.children(recursive=True)
    total = 0
    for item in members:
        try:
            total += item.memory_info().rss
        except psutil.NoSuchProcess:
            continue
    available = int(psutil.virtual_memory().available)
    disk = int(shutil.disk_usage(root).free)
    reason = None
    if total >= cap:
        reason = 'PROCESS_TREE_RSS_CAP'
    elif available < floor:
        reason = 'AVAILABLE_RAM_FLOOR'
    elif disk < MIN_DISK_FREE:
        reason = 'DISK_SPACE_FLOOR'
    return {'rss_bytes': total, 'available_ram_bytes': available, 'disk_free_bytes': disk,
            'processes_seen': len(members), 'stop_reason': reason}


def stop_tree(psutil, pid: int) -> None:
    """Best-effort prompt stop of the whole process tree, including Windows joblib children."""
    try:
        p = psutil.Process(pid)
        members = p.children(recursive=True)
        for item in members:
            try: item.kill()
            except psutil.NoSuchProcess: pass
        try: p.kill()
        except psutil.NoSuchProcess: pass
        psutil.wait_procs(members + [p], timeout=4)
    except psutil.NoSuchProcess:
        return
    except (psutil.Error, OSError):
        if os.name == 'nt':
            try: subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'],
                                capture_output=True, timeout=10, check=False)
            except (OSError, subprocess.TimeoutExpired): pass
        else:
            try:
                import signal
                os.killpg(pid, signal.SIGKILL)
            except (ProcessLookupError, OSError): pass


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', required=True, choices=('pilot', 'full'))
    p.add_argument('--candidate', required=True, choices=CANDIDATES)
    p.add_argument('--out-dir', required=True, type=Path)
    p.add_argument('--pilot-rows', type=int, default=10000)
    p.add_argument('--pilot-report', type=Path, help='Mandatory successful matching pilot for --mode full')
    p.add_argument('--python', type=Path, default=Path(sys.executable), help='Python 3.11 with ML dependencies and psutil')
    p.add_argument('--max-tree-rss-gib', type=float, default=2.0)
    p.add_argument('--timeout-min', type=float, default=20.0,
                   help='5-20 min; for --mode full ONLY: set 0 for no wall-time deadline (RAM/disk watchdog stays active)')
    p.add_argument('--cpu-cores', type=int, default=2)
    args = p.parse_args()
    if not (1000 <= args.pilot_rows <= 25000): p.error('pilot-rows must be 1,000–25,000; no TEST rows')
    if not (1 <= args.cpu_cores <= 2): p.error('cpu-cores must be 1 or 2')
    if not timeout_policy_valid(args.timeout_min, args.mode):
        p.error('pilot timeout 5-20 min; full timeout 5-20 min or 0 for NO deadline (watchdog stays on)')
    cap = int(args.max_tree_rss_gib * GIB)
    if not (int(0.5 * GIB) <= cap <= int(3.5 * GIB)):
        p.error('tree RSS cap must be between 0.5 and 3.5 GiB')
    if args.mode == 'full' and not args.pilot_report:
        p.error('--pilot-report is required for full TRAIN')
    out = safe_new_output(ROOT, args.out_dir)
    # psutil is mandatory; refuse execution if independent monitoring unavailable.
    try:
        import psutil
    except ImportError:
        print('NO_GO: install psutil into the supervisor Python environment; no child started.', file=sys.stderr)
        return 2
    interpreter = str(args.python.resolve(strict=True))
    if not Path(interpreter).is_file(): p.error('Python interpreter missing')
    spec = subprocess.run([interpreter, '-c',
      'import sys,importlib.metadata,json; import pandas,numpy,sklearn,scipy,joblib,threadpoolctl,psutil; '
      'print(json.dumps({"python":list(sys.version_info[:2]),"versions":{n:importlib.metadata.version(n) for n in '
      '["pandas","numpy","scikit-learn","scipy","joblib","threadpoolctl","psutil"]}}))'],
      capture_output=True, text=True, timeout=30, check=False)
    if spec.returncode != 0:
        print('NO_GO: selected Python lacks required ML/monitor packages: ' + spec.stderr[-500:], file=sys.stderr)
        return 2
    env_details = json.loads(spec.stdout.strip())
    if env_details['python'] != [3, 11]:
        print('NO_GO: selected ML Python must be 3.11', file=sys.stderr)
        return 2
    pre = load_preflight()
    audit = pre.audit(ROOT)
    ignored = {'available_ram_ge_9gib'}
    science_ok = all(v['pass'] for k, v in audit['checks'].items() if k not in ignored)
    budgets = resource_budget(int(psutil.virtual_memory().available), int(shutil.disk_usage(ROOT).free), cap)
    if not science_ok or not budgets['passed']:
        print(json.dumps({'status': 'NO_GO_NO_WORKER_STARTED', 'science_checks_pass':science_ok,
            'failed_science_checks':[k for k,v in audit['checks'].items() if not v['pass'] and k not in ignored],
            'local_12gb_budget':budgets, 'original_9gib_gate':audit['checks']['available_ram_ge_9gib'],
            'note':'Alternative measured profile only; does not overwrite canonical P15 preflight'}, indent=2))
        return 2
    hashes = {k[len('sha256:'):]: v['observed']['sha256']
              for k,v in audit['checks'].items() if k.startswith('sha256:')}
    if args.mode == 'full':
        try:
            valid_pilot=check_pilot_evidence(args.pilot_report.resolve(strict=True),
                                             args.candidate, hashes, interpreter, cap)
        except (OSError, ValueError):
            valid_pilot=False
        if not valid_pilot:
            print('NO_GO: matching successful pilot required; headroom <75% of cap or provenance mismatch.', file=sys.stderr)
            return 2
    # Explicit output remains separate from all frozen outputs. Path must not exist.
    out.mkdir(mode=0o700, exist_ok=False)
    (out/'worker').mkdir()
    report = {'mode': args.mode, 'candidate': args.candidate, 'result':'INCOMPLETE',
      'source_hashes': hashes, 'python_executable':interpreter, 'package_versions':env_details['versions'],
      'git_head':audit['checks']['git_clean_tracked_files']['observed']['head'],
      'preflight': {'science_ok':science_ok,'canonical_9gib_gate_passed':audit['checks']['available_ram_ge_9gib']['pass']},
      'budget':budgets, 'wall_time_policy':{'timeout_min':args.timeout_min,
        'enabled':args.timeout_min>0,'operator_opted_into_no_deadline':args.mode=='full' and args.timeout_min==0},
      'release_certified':False, 'peak_tree_rss_bytes':0,
      'min_ram_seen_bytes':None,'worker_checks':{'passed':False},
      'timestamp_utc':datetime.now(timezone.utc).isoformat()}
    (out/'start.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    env = os.environ.copy()
    env.update({'P15_WATCHED':'1','PYTHONDONTWRITEBYTECODE':'1',
      'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1',
      'VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1', 'LOKY_MAX_CPU_COUNT':'2'})
    cmd = [interpreter, '-u', str(WORKER), '--out-dir',str(out/'worker'),
           '--candidate',args.candidate,'--mode',args.mode,'--pilot-rows',str(args.pilot_rows),
           '--cpu-cores',str(args.cpu_cores)]
    popen_kwargs={'cwd':str(ROOT),'env':env,'stdout':(out/'worker.stdout.log').open('w',encoding='utf-8'),
                  'stderr':(out/'worker.stderr.log').open('w',encoding='utf-8')}
    if os.name == 'nt':popen_kwargs['creationflags']=subprocess.CREATE_NEW_PROCESS_GROUP
    else:popen_kwargs['start_new_session']=True
    proc = None
    last_reason=None
    started=time.monotonic()
    peak=0
    low=None
    samples=0
    try:
        proc=subprocess.Popen(cmd,**popen_kwargs)
        pproc=psutil.Process(proc.pid)
        # Child explicitly waits for go.signal before touching TRAIN/ML imports.
        cpus=pproc.cpu_affinity()
        if not cpus or len(cpus)<args.cpu_cores:
            raise RuntimeError('insufficient CPU affinity permission/cores')
        pproc.cpu_affinity(cpus[:args.cpu_cores])
        (out/'heartbeat').touch()
        (out/'go.signal').write_text('supervised\n',encoding='utf-8')
        with (out/'resources.csv').open('w',encoding='utf-8') as log:
            log.write('seconds,tree_rss_bytes,system_available_bytes,disk_free_bytes,process_count\n')
            while proc.poll() is None:
                (out/'heartbeat').touch()
                try:
                    sample=resource_sample(psutil,proc.pid,ROOT,cap,MIN_FREE_FLOOR)
                except psutil.NoSuchProcess:
                    if proc.poll() is not None:break
                    raise
                peak=max(peak,sample['rss_bytes'])
                low=sample['available_ram_bytes'] if low is None else min(low,sample['available_ram_bytes'])
                samples +=1
                log.write(f"{time.monotonic()-started:.2f},{sample['rss_bytes']},{sample['available_ram_bytes']},{sample['disk_free_bytes']},{sample['processes_seen']}\n")
                log.flush()
                if sample['stop_reason']:
                    last_reason=sample['stop_reason'];break
                if timeout_reached(time.monotonic()-started, args.timeout_min):
                    last_reason='TIMEOUT';break
                time.sleep(0.5)
        if last_reason:stop_tree(psutil,proc.pid)
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            last_reason=last_reason or 'PROCESS_WOULD_NOT_EXIT'
            stop_tree(psutil,proc.pid)
        report['exit_code']=proc.returncode
    except (Exception,KeyboardInterrupt) as exc:
        last_reason=last_reason or ('INTERRUPTED' if isinstance(exc,KeyboardInterrupt) else 'WATCHDOG_ERROR_'+type(exc).__name__)
        if proc:stop_tree(psutil,proc.pid)
        report['watchdog_error']=str(exc)[:500]
    finally:
        for name in ('stdout','stderr'):
            stream=popen_kwargs[name]
            if not stream.closed:stream.close()
        report['peak_tree_rss_bytes']=peak
        report['min_ram_seen_bytes']=low
        report['resource_samples']=samples
        report['stop_reason']=last_reason
        details=out/'worker'/'worker_result.json'
        if not last_reason and report.get('exit_code')==0 and details.exists():
            worker=read_json(details)
            report['worker_checks']=worker
            if (samples >= 1 and peak > 0 and verify_worker_result(worker,args.candidate,args.mode,
                        out/'worker',hashes,env_details['versions'])):
                report['result']='PASS'
        elif not last_reason:
            report['stop_reason']='WORKER_FAILED_OR_MISSING_VALIDATION'
        # Report is only an execution record, not research test accuracy.
        report['release_certified']=False
        (out/'run_report.json').write_text(json.dumps(report, indent=2,ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'result':report['result'],'reason':report.get('stop_reason'),
                      'peak_rss_gib':round(peak/GIB,3),'report':str(out/'run_report.json')},indent=2))
    return 0 if report['result']=='PASS' else 2

if __name__=='__main__':
    raise SystemExit(main())
