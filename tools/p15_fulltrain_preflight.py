"""Read-only, stdlib-only gate checks before a proposed UNSW-NB15 full-TRAIN rebuild.

This script NEVER imports/executes training code, reads the official TEST,
fits a model, changes frozen evidence or authorizes a full-TRAIN job. Its output
is an auditable preflight report; a separate supervised runner/watchdog and an
explicit resource recheck are required before any actual reconstruction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_SHA256 = {
    "data/raw/unsw-nb15/UNSW_NB15_training-set.csv": "bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa",
    "src/models/run_unsw_phase9_final_holdout.py": "3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480",
    "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json": "cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6",
    "results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json": "5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be",
}
EXPECTED_CANDIDATES = {"random_forest_42", "stacking_42", "random_forest_17"}
FORBIDDEN_PREDICTORS = {"id", "label", "attack_cat"}
MIN_AVAILABLE_RAM_BYTES = 9 * 1024 ** 3
MIN_DISK_FREE_BYTES = 10 * 1024 ** 3


def sha256_stream(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_input(root: Path, relative: str) -> Path:
    """Reject missing paths, symlinks/junctions, or renamed/repointed files."""
    path = root / relative
    if not path.is_file() or path.is_symlink() or path.resolve(strict=True) != path:
        raise ValueError("missing/unsafe path: " + relative)
    return path


def available_ram_bytes() -> int | None:
    if sys.platform == "win32":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("length", ctypes.c_ulong), ("memory_load", ctypes.c_ulong),
                    ("total_phys", ctypes.c_ulonglong), ("avail_phys", ctypes.c_ulonglong),
                    ("total_page", ctypes.c_ulonglong), ("avail_page", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong), ("avail_virtual", ctypes.c_ulonglong),
                    ("avail_extended_virtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.length = ctypes.sizeof(status)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.avail_phys)
        except (AttributeError, OSError, ValueError):
            return None
    if sys.platform.startswith("linux"):
        try:
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
        except (OSError, ValueError, IndexError):
            pass
    return None


def _git_info(root: Path) -> dict:
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root,
            capture_output=True, text=True, timeout=10, check=True
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=root,
            capture_output=True, text=True, timeout=10, check=True
        ).stdout
        return {"head": head, "tracked_worktree_clean": not status.strip()}
    except (subprocess.CalledProcessError, OSError, subprocess.TimeoutExpired):
        return {"head": None, "tracked_worktree_clean": False}


def _record(checks: dict, key: str, passed: bool, detail: object) -> None:
    checks[key] = {"pass": bool(passed), "observed": detail}


def audit(
    root: Path, *, expected_hashes: dict | None = None,
    expected_train_rows: int = 175341, expected_normal: int = 56000,
    expected_attack: int = 119341, ram_bytes: int | None = None,
    disk_bytes: int | None = None, check_git: bool = True,
    expected_python: tuple[int, int] = (3, 11),
) -> dict:
    root = root.resolve(strict=True)
    checks: dict = {}
    hashes = EXPECTED_SHA256 if expected_hashes is None else expected_hashes

    for relative, expected in hashes.items():
        try:
            observed = sha256_stream(safe_input(root, relative))
            _record(checks, f"sha256:{relative}", observed == expected,
                    {"sha256": observed, "matches_expected": observed == expected})
        except (OSError, ValueError):
            _record(checks, f"sha256:{relative}", False, "missing/unreadable/unsafe")

    fields: list[str] = []
    rows = normal = attack = 0
    try:
        train_path = safe_input(root, "data/raw/unsw-nb15/UNSW_NB15_training-set.csv")
        with train_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = [x.strip() for x in (reader.fieldnames or [])]
            if len(fields) != len(set(fields)) or not {"id", "label", "attack_cat"}.issubset(fields):
                raise ValueError("unsafe/duplicate CSV columns")
            for row in reader:
                rows += 1
                label = str(row.get("label", "")).strip()
                if label == "0":
                    normal += 1
                elif label == "1":
                    attack += 1
                else:
                    raise ValueError(f"invalid label on row {rows}")
        _record(checks, "train_counts",
                (rows, normal, attack) == (expected_train_rows, expected_normal, expected_attack),
                {"rows": rows, "normal": normal, "attack": attack})
        predictors = [c for c in fields if c not in FORBIDDEN_PREDICTORS]
        _record(checks, "predictor_schema_42",
                len(predictors) == 42 and len(predictors) == len(set(predictors)),
                {"ordered_42": predictors, "count": len(predictors)})
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        _record(checks, "train_counts", False, type(exc).__name__)
        _record(checks, "predictor_schema_42", False, "TRAIN schema unavailable")
        predictors = []

    try:
        subset_path = safe_input(
            root, "results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json"
        )
        subset = json.loads(subset_path.read_text(encoding="utf-8"))["stable_2plus_methods"]
        good = (isinstance(subset, list) and len(subset) == 17 and
                len(set(subset)) == 17 and set(subset).issubset(set(predictors)))
        _record(checks, "stable_17_subset", good, {"features": subset})
    except (OSError, ValueError, KeyError, TypeError):
        _record(checks, "stable_17_subset", False, "unavailable/invalid")

    try:
        freeze_path = safe_input(
            root, "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json"
        )
        manifest = json.loads(freeze_path.read_text(encoding="utf-8"))
        good = isinstance(manifest, dict) and set(manifest) == EXPECTED_CANDIDATES
        if good:
            good = all(float(x["decision_threshold"]) == 0.5 for x in manifest.values())
        _record(checks, "frozen_candidates_threshold", good,
                {"candidates": sorted(manifest) if isinstance(manifest, dict) else []})
    except (OSError, ValueError, KeyError, TypeError):
        _record(checks, "frozen_candidates_threshold", False, "unavailable/invalid")

    _record(checks, "python_3_11", sys.version_info[:2] == expected_python, platform.python_version())
    available_ram = available_ram_bytes() if ram_bytes is None else ram_bytes
    available_disk = shutil.disk_usage(root).free if disk_bytes is None else disk_bytes
    _record(checks, "available_ram_ge_9gib",
            available_ram is not None and available_ram >= MIN_AVAILABLE_RAM_BYTES, available_ram)
    _record(checks, "disk_free_ge_10gib", available_disk >= MIN_DISK_FREE_BYTES, available_disk)
    git = _git_info(root) if check_git else {"head": "FIXTURE", "tracked_worktree_clean": True}
    _record(checks, "git_clean_tracked_files", git["tracked_worktree_clean"], git)

    return {
        "task": "P15_FULL_TRAIN_READ_ONLY_PREFLIGHT",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root), "checks": checks,
        "preflight_checks_pass": all(item["pass"] for item in checks.values()),
        "training_authorized": False,
        "reconstruction_status": "NOT_RUN",
        "reason": "A reviewed isolated runner, watchdog, package provenance and explicit fresh resource gate are still required. This tool never trains or reads TEST.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, help="New JSON report (exclusive create); optional")
    args = parser.parse_args()
    report = audit(args.project_root)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out is not None:
        dest = args.out.resolve()
        safe_base = args.project_root.resolve() / "results" / "reproducibility"
        if not dest.is_relative_to(safe_base) or dest.suffix != ".json":
            parser.error("--out must be an unused .json path under results/reproducibility")
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("x", encoding="utf-8") as handle:
            handle.write(payload)
    print(payload)
    return 0 if report["preflight_checks_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
