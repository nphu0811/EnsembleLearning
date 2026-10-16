#!/usr/bin/env python3
"""Audit effective Python package provenance; read-only except for dedicated audit outputs.
No installations, model loading, training, or dataset access.
"""
from __future__ import annotations

import argparse
import csv
import importlib
import importlib.metadata as md
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone

PACKAGES = {
    "joblib": "joblib", "matplotlib": "matplotlib", "numpy": "numpy",
    "pandas": "pandas", "scikit-learn": "sklearn", "scipy": "scipy",
    "threadpoolctl": "threadpoolctl", "tzdata": "tzdata",
}
EXPECTED = {
    "joblib": "1.5.3", "matplotlib": "3.11.1", "numpy": "2.5.2",
    "pandas": "3.0.5", "scikit-learn": "1.9.0", "scipy": "1.18.1",
    "threadpoolctl": "3.6.0",
}


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def subprocess_capture(cmd: list[str], timeout: int = 25) -> dict:
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return {"returncode": cp.returncode, "stdout": cp.stdout.strip(), "stderr": cp.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"error": str(e)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-root", default=".")
    p.add_argument("--skip-import", action="store_true", help="Avoid importing ML packages (faster, weaker verification)")
    args = p.parse_args()
    root = Path(args.project_root).resolve()
    out = root / "results" / "reproducibility" / "p15_02c1_package_provenance"
    out.mkdir(parents=True, exist_ok=True)

    distributions = {name: [] for name in PACKAGES}
    for dist in md.distributions():
        raw_name = dist.metadata.get("Name")
        if not raw_name:
            continue
        name = normalized(raw_name)
        if name in distributions:
            metadata_path = getattr(dist, "_path", None)
            try:
                package_root = str(Path(dist.locate_file("")).resolve())
            except (OSError, ValueError) as e:
                package_root = "UNKNOWN: " + str(e)
            distributions[name].append({
                "name": raw_name,
                "version": dist.version,
                "metadata_dir": str(Path(metadata_path).resolve()) if metadata_path else None,
                "install_root": package_root,
            })
    for value in distributions.values():
        value.sort(key=lambda item: (item["version"], str(item["metadata_dir"])))

    effective = {}
    for dist_name, module_name in PACKAGES.items():
        x = {"package": dist_name, "module": module_name}
        try:
            x["resolved_metadata_version"] = md.version(dist_name)
        except md.PackageNotFoundError:
            x["resolved_metadata_version"] = None
        try:
            spec = importlib.util.find_spec(module_name)
            x["module_spec_origin"] = spec.origin if spec else None
            x["module_search_locations"] = list(spec.submodule_search_locations or []) if spec else []
        except (ModuleNotFoundError, ValueError, ImportError) as e:
            x["find_spec_error"] = repr(e)
        if not args.skip_import:
            try:
                module = importlib.import_module(module_name)
                x["import_ok"] = True
                x["imported_version"] = getattr(module, "__version__", None)
                x["module_file"] = getattr(module, "__file__", None)
            except Exception as e:  # document import failure without masking it
                x["import_ok"] = False
                x["import_error"] = type(e).__name__ + ": " + str(e)
        effective[dist_name] = x

    snap_path = root / "results" / "reproducibility" / "p15_02b_runtime_check" / "p15_02b_runtime_check.json"
    snapshot_status = "not_found"
    if snap_path.is_file():
        try:
            snap = json.loads(snap_path.read_text(encoding="utf-8-sig"))
            snapshot_status = "loaded"
        except (ValueError, UnicodeError, OSError) as e:
            snapshot_status = "cannot_read: " + str(e)
            snap = None
    else:
        snap = None

    reasons = []
    duplicates = {}
    for name, entries in distributions.items():
        if len(entries) > 1:
            duplicates[name] = sorted(set(e["version"] for e in entries))
            reasons.append(f"Multiple dist-info records visible for {name}: {duplicates[name]}")
    for name, expected_version in EXPECTED.items():
        entry = effective[name]
        got = entry.get("resolved_metadata_version")
        if got != expected_version:
            reasons.append(f"{name}: expected {expected_version}, metadata resolver returned {got}")
        if not args.skip_import:
            if not entry.get("import_ok"):
                reasons.append(f"{name}: import failed")
            elif entry.get("imported_version") and entry["imported_version"] != expected_version:
                reasons.append(f"{name}: imported version differs: {entry['imported_version']}")
    if sys.version_info[:3] != (3, 14, 3):
        reasons.append(f"Python is {platform.python_version()}, unlike the P15-02B snapshot 3.14.3")

    report = {
        "task": "P15-02C1 runtime package provenance (read-only audit)",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "python": platform.python_version(),
        "sys_executable": sys.executable,
        "sys_prefix": sys.prefix,
        "sys_base_prefix": sys.base_prefix,
        "is_venv": sys.prefix != sys.base_prefix,
        "platform": platform.platform(),
        "python_launcher_inventory": subprocess_capture(["py", "-0p"]),
        "pip_check": subprocess_capture([sys.executable, "-m", "pip", "check"]),
        "p15_02b_snapshot": {"path": str(snap_path), "status": snapshot_status,
                             "observed_python": snap.get("now_python") if snap else None},
        "effective_packages": effective,
        "all_visible_distribution_records": distributions,
        "multiple_metadata_record_packages": duplicates,
        "known_snapshot_versions": EXPECTED,
        "issues_or_unresolved": reasons,
        "interpretation": [
            "Matching imports / pip check do not prove original model-training environment.",
            "Multiple visible dist-info directories can reflect residue or overlapping site paths; inspect recorded locations before remediation.",
            "This is an audit of the current runtime, not a fully hashed dependency lockfile or clean-install verification.",
            "No package install, dataset access, or model training performed."
        ],
        "audit_status": "REVIEW_NEEDED" if reasons else "CURRENT_RUNTIME_PROVENANCE_OK_NOT_INDEPENDENTLY_REPRODUCED",
    }
    (out / "p15_02c1_package_provenance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out / "p15_02c1_distribution_paths.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["package", "version", "metadata_dir", "install_root"])
        for name, entries in distributions.items():
            for entry in entries:
                w.writerow([name, entry["version"], entry["metadata_dir"], entry["install_root"]])
    print("P15-02C1 AUDIT WRITTEN:", out)
    print("STATUS:", report["audit_status"])
    print("Python:", report["python"], "at", report["sys_executable"])
    print("Visible multiple-metadata packages:", duplicates if duplicates else "none")
    print("This script does not modify installed packages or train models.")

if __name__ == "__main__":
    main()
