#!/usr/bin/env python3
"""Phase 15 P15-02C2. Optional, isolated *current-runtime* install test.

By default: preflight only; NO virtual environment created and NO pip install.
With --execute: create a clean venv, install pinned packages from wheels, then
verify pip check, isolated origins, and exact import versions. No dataset/model IO.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import traceback
from datetime import datetime, timezone

EXPECTED = {
    "joblib": "1.5.3", "matplotlib": "3.11.1", "numpy": "2.5.2",
    "pandas": "3.0.5", "scikit-learn": "1.9.0", "scipy": "1.18.1",
    "threadpoolctl": "3.6.0", "tzdata": "2026.3",
}
MIN_FREE_BYTES = 1_500_000_000  # conservative preflight threshold, NOT an exact space forecast


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(command: list[str], timeout: int = 1200) -> dict:
    try:
        result = subprocess.run(command, check=False, capture_output=True,
                                text=True, timeout=timeout,
                                env={**os.environ, "PYTHONNOUSERSITE": "1", "PIP_NO_INPUT": "1"})
        return {"returncode": result.returncode,
                "stdout": result.stdout[-50000:], "stderr": result.stderr[-50000:]}
    except Exception as exc:
        return {"returncode": -1, "stdout": "", "stderr": repr(exc)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-root", default=".")
    p.add_argument("--venv-dir", default=None, help="Isolation directory (default: PROJECT/.venv-nckh-repro-py314)")
    p.add_argument("--execute", action="store_true", help="Explicitly create venv and install pinned dependencies")
    args = p.parse_args()

    root = Path(args.project_root).resolve()
    deps = root / "reproducibility" / "requirements-observed-py314-NOT-ORIGINAL-TRAINING.txt"
    out = root / "results" / "reproducibility" / "p15_02c2_clean_env"
    out.mkdir(parents=True, exist_ok=True)
    venv = Path(args.venv_dir).expanduser().resolve() if args.venv_dir else root / ".venv-nckh-repro-py314"
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    pip_version_cmd = [str(python), "-m", "pip", "--version"]
    space = shutil.disk_usage(venv.parent if venv.parent.exists() else root)
    report = {
        "task": "P15-02C2 isolated CURRENT-runtime smoke test, not original-training verification",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root), "host_python": sys.version,
        "host_executable": sys.executable, "venv": str(venv),
        "execute_requested": args.execute,
        "requirements_file": str(deps),
        "requirements_sha256": sha256(deps) if deps.is_file() else None,
        "required_min_free_bytes": MIN_FREE_BYTES,
        "available_bytes_on_target_drive": space.free,
        "expected_versions": EXPECTED,
        "checkpoints": {},
        "limitations": ["Does not establish original training environment", "No model/dataset loading or retraining",
                        "Resolved dependency versions do not constitute a hash-locked supply-chain lock"],
    }

    def finish(status: str, code: int) -> int:
        report["status"] = status
        path = out / "p15_02c2_clean_env.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{status}. Report saved: {path}")
        return code

    if not deps.is_file():
        report["error"] = "Missing observed requirement file; please extract whole ZIP into NCKH root"
        return finish("BLOCKED_MISSING_REQUIREMENTS", 2)

    parsed = {}
    for line in deps.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            if "==" not in line:
                report["error"] = f"Unpinned requirement: {line}"
                return finish("BLOCKED_UNPINNED_REQUIREMENT", 2)
            name, version = line.split("==", 1)
            parsed[name.lower()] = version
    if parsed != EXPECTED:
        report["error"] = "Observed pins do not exactly match P15-02C1 verified versions"
        return finish("BLOCKED_VERSION_MISMATCH", 2)
    report["checkpoints"]["requirement_pins_match"] = True
    report["checkpoints"]["host_is_python_314"] = sys.version_info[:2] == (3, 14)
    report["checkpoints"]["free_disk_above_threshold"] = space.free >= MIN_FREE_BYTES
    report["checkpoints"]["venv_exists_before"] = venv.exists()

    if not args.execute:
        print("PREFLIGHT ONLY: no packages installed, no venv created.")
        print(f"Using host Python: {sys.executable}")
        print(f"Venv target: {venv}; free space: {space.free / 1e9:.2f} GB")
        print("To perform the isolated installation, rerun with --execute (network/disk required).")
        return finish("PREFLIGHT_ONLY", 0)

    if not report["checkpoints"]["host_is_python_314"]:
        return finish("BLOCKED_REQUIRES_PYTHON_314", 2)
    if not report["checkpoints"]["free_disk_above_threshold"]:
        return finish("BLOCKED_INSUFFICIENT_DISK_SPACE", 2)
    if venv.exists():
        report["error"] = "Target exists. Choose a NEW unused --venv-dir. Will not overwrite anything."
        return finish("BLOCKED_VENV_ALREADY_EXISTS", 2)
    if root == venv or root in venv.parents and venv == root / "results":
        return finish("BLOCKED_INVALID_VENV_PATH", 2)

    print("Creating isolated virtual environment. This step will NOT touch global packages.")
    create = run([sys.executable, "-m", "venv", str(venv)], timeout=240)
    report["checkpoints"]["create_venv"] = create
    if create["returncode"] != 0 or not python.is_file():
        return finish("FAILED_CREATE_VENV", 1)

    pv = run(pip_version_cmd, timeout=60)
    report["checkpoints"]["venv_pip_version"] = pv
    if pv["returncode"] != 0:
        return finish("FAILED_VENV_PIP_UNAVAILABLE", 1)

    print("Installing binary wheels into NEW venv only. This requires network and disk space.")
    install = run([str(python), "-m", "pip", "--disable-pip-version-check", "--no-input",
                   "install", "--no-cache-dir", "--only-binary=:all:", "-r", str(deps)], timeout=1500)
    (out / "install_stdout_tail.log").write_text(install["stdout"], encoding="utf-8")
    (out / "install_stderr_tail.log").write_text(install["stderr"], encoding="utf-8")
    report["checkpoints"]["pip_install_returncode"] = install["returncode"]
    if install["returncode"] != 0:
        report["error"] = "pip install failed. See the logs; do not modify global packages."
        return finish("FAILED_ISOLATED_PIP_INSTALL", 1)

    check = run([str(python), "-m", "pip", "check"], timeout=120)
    report["checkpoints"]["pip_check"] = check
    freeze = run([str(python), "-m", "pip", "freeze", "--all"], timeout=120)
    report["checkpoints"]["pip_freeze_returncode"] = freeze["returncode"]
    if freeze["returncode"] == 0:
        (out / "requirements-clean-py314-resolved-NOT-HASHED.txt").write_text(
            "# Clean analysis-runtime environment (NOT original model training); not a hash-locked list.\n"
            + freeze["stdout"], encoding="utf-8")

    smoke_code = '''import sys, json, importlib
from importlib import metadata
expected = ''' + repr(EXPECTED) + '''
modules = {"scikit-learn": "sklearn"}
results = {}
for name, expected_version in expected.items():
    mod = importlib.import_module(modules.get(name, name))
    version = metadata.version(name)
    results[name] = {"version": version, "matches": version == expected_version,
                     "origin": getattr(mod, "__file__", None)}
print(json.dumps({"executable": sys.executable, "prefix": sys.prefix,
                  "base_prefix": sys.base_prefix, "versions": results}))
'''
    smoke = run([str(python), "-c", smoke_code], timeout=180)
    report["checkpoints"]["smoke_returncode"] = smoke["returncode"]
    report["checkpoints"]["smoke_stderr"] = smoke["stderr"]
    if smoke["returncode"] != 0:
        return finish("FAILED_IMPORT_SMOKE", 1)
    try:
        imported = json.loads(smoke["stdout"])
    except Exception as exc:
        report["error"] = "Smoke import did not produce valid JSON: " + repr(exc)
        return finish("FAILED_PARSE_IMPORT", 1)
    report["checkpoints"]["imported_packages"] = imported
    isolated = (imported["prefix"] != imported["base_prefix"]
                and Path(imported["prefix"]).resolve() == venv)
    all_match = all(x["matches"] for x in imported["versions"].values())
    all_from_venv = all(
        item["origin"] and Path(item["origin"]).resolve().is_relative_to(venv)
        for item in imported["versions"].values()
    )
    report["checkpoints"]["venv_isolated"] = isolated
    report["checkpoints"]["all_pins_match"] = all_match
    report["checkpoints"]["all_module_paths_within_venv"] = all_from_venv
    report["checkpoints"]["pip_check_pass"] = check["returncode"] == 0
    if isolated and all_match and all_from_venv and check["returncode"] == 0:
        return finish("PASS_CLEAN_ENV_CURRENT_ANALYSIS_ONLY", 0)
    return finish("REVIEW_REQUIRED", 1)

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
        raise SystemExit(130)
