#!/usr/bin/env python3
"""Conservative cleanup of local ignored Python caches ONLY.

Dry-run by default. Refuses Git-tracked files, symlinks, everything outside
approved code/doc roots, and research datasets/models/results/evidence.
Obsolete tracked presentation intermediates are removed by git pull after
the corresponding remote cleanup commit; do NOT clean those with this tool.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

CACHES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
ALLOW_ROOTS = {"src", "tools", "tests", "report", "docs", "proposal", "presentation",
               "notebook", "templates"}
PROTECT = {".git", ".research_memory", "data", "results", "config", "release",
           "literature", "venv", ".venv", ".venv-p15-local", "env", ".tox",
           "node_modules", "dist", "build"}


def all_tracked(root):
    done = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                          capture_output=True, check=True)
    return {x.decode("utf-8", "surrogateescape").replace("\\", "/")
            for x in done.stdout.split(b"\0") if x}


def find_candidates(root, tracked):
    out = []
    for topname in sorted(ALLOW_ROOTS):
        top = root / topname
        if not top.is_dir() or top.is_symlink():
            continue
        for dirname, dirs, files in os.walk(top, followlinks=False):
            folder = Path(dirname)
            dirs[:] = [v for v in dirs if not (folder / v).is_symlink()
                       and v not in PROTECT
                       and not v.lower().startswith((".venv", "venv", "_runtime"))]
            if folder.name not in CACHES:
                continue
            # Walk only inside this specific cache directory, including its
            # internal v/cache hierarchy. Never follow symlinks or descend
            # through protected path names, and skip Git-tracked members.
            dirs.clear()
            for cache_folder, cache_subdirs, cache_files in os.walk(
                folder, followlinks=False
            ):
                parent = Path(cache_folder)
                cache_subdirs[:] = [
                    x for x in cache_subdirs if not (parent / x).is_symlink()
                    and x not in PROTECT
                ]
                for name in cache_files:
                    f = parent / name
                    if f.is_symlink() or not f.is_file():
                        continue
                    rel = f.relative_to(root).as_posix()
                    if rel not in tracked:
                        out.append((f, f.stat().st_size))
    return sorted(out, key=lambda item: str(item[0]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    switches = parser.add_mutually_exclusive_group()
    switches.add_argument("--dry-run", action="store_true")
    switches.add_argument("--apply", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / ".git").exists():
        raise SystemExit("ERROR: not a Git project working tree")
    gitroot = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, check=True, text=True).stdout.strip()
    if Path(gitroot).resolve() != root:
        raise SystemExit("ERROR: --root must be repository root")
    tracked = all_tracked(root)
    candidates = find_candidates(root, tracked)
    total = sum(s for _, s in candidates)
    print("MODE:", "APPLY" if args.apply else "DRY RUN", "| ROOT:", root)
    for path, size in candidates:
        print(f"{size/1024:8.1f} KiB {path.relative_to(root).as_posix()}")
    print(f"Candidates={len(candidates)} Reclaimable={total/1048576:.2f} MiB")
    if not args.apply:
        print("No deletion performed; review list before using --apply.")
        return 0
    for path, _ in candidates:
        if path.is_symlink() or not path.is_file():
            raise RuntimeError("Changed target; stop: " + str(path))
        parts = path.relative_to(root).parts
        if len(parts) < 3 or parts[0] not in ALLOW_ROOTS or not any(
            x in CACHES for x in parts[1:-1]
        ) or any(x in PROTECT for x in parts):
            raise RuntimeError("Protected/invalid target: " + str(path))
        path.unlink()
    print(f"Deleted {len(candidates)} untracked cache files (~{total/1048576:.2f} MiB).")
    print("TRAIN/TEST, models, results, and Git tracked research files were not touched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
