"""P21 pilot safety guards. Standard library only; no dataset and no ML imports.

These checks are intentionally separate from worker fitting code and can be
exercised in CI without installing scikit-learn or accessing TRAIN/TEST.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = ROOT / "results" / "controlled_extensions"
TRAIN_REL = "data/raw/unsw-nb15/UNSW_NB15_training-set.csv"
TRAIN = ROOT / TRAIN_REL
GIB = 1024 ** 3


def safe_new_pilot_output(root: Path, raw: Path) -> Path:
    """Require one NEW direct sibling of other P21 runs, never an overwrite."""
    base = (root / "results" / "controlled_extensions").resolve(strict=True)
    candidate = raw if raw.is_absolute() else root / raw
    if candidate.exists() or candidate.is_symlink():
        raise ValueError("Pilot output already exists; use a fresh directory")
    parent = candidate.parent.resolve(strict=True)
    if parent != base or not candidate.name.startswith("p21_train_only_pilot_rf42_"):
        raise ValueError("Output must be a new direct p21_train_only_pilot_rf42_* directory")
    if candidate.name in {"", ".", ".."} or os.path.basename(str(candidate)) != candidate.name:
        raise ValueError("Invalid output basename")
    return parent / candidate.name


def validate_worker_scope(out: Path, root: Path = ROOT) -> None:
    resolved = out.resolve(strict=True)
    base = (root / "results" / "controlled_extensions").resolve(strict=True)
    if out.is_symlink() or resolved.name != "worker" or resolved.parent.parent != base:
        raise PermissionError("P21 worker must write only to supervised pilot worker directory")
    if not resolved.parent.name.startswith("p21_train_only_pilot_rf42_"):
        raise PermissionError("Wrong P21 pilot folder")


def guard_dataset_read(path, root: Path = ROOT) -> None:
    """Fail closed on reads of any unapproved project data file, not just TEST."""
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve(strict=False)
    data_root = (root / "data").resolve(strict=False)
    expected = (root / TRAIN_REL).resolve(strict=False)
    if resolved == expected:
        return
    if resolved == data_root or data_root in resolved.parents:
        raise PermissionError("P21 forbids all project data files except official TRAIN")
    if "UNSW_NB15_testing-set.csv".lower() in str(resolved).lower():
        raise PermissionError("P21 forbids official TEST anywhere")


def audit_file_open(event: str, args, root: Path = ROOT):
    # CPython audit event is raised for builtins.open/os.open including csv reads.
    if event != "open" or not args:
        return
    path = args[0]
    if isinstance(path, (str, bytes, os.PathLike)):
        guard_dataset_read(os.fsdecode(path), root=root)


def sha256_stream(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as reader:
        for part in iter(lambda: reader.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def within_resource_budget(available_ram: int, disk_free: int, cap: int,
                           floor: int = int(1.5 * GIB)) -> bool:
    return (available_ram >= max(4 * GIB, cap + floor + int(0.5 * GIB))
            and disk_free >= 10 * GIB and cap == 2 * GIB)


def within_pilot_size(n: int) -> bool:
    return 1000 <= n <= 20000
