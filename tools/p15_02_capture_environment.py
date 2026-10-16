#!/usr/bin/env python3
"""P15-02: Capture an offline, non-invasive reproducibility environment inventory.

Reads the P15-01 script inventory and Python source files (AST only).
Does not import project modules, read datasets, train models, or install packages.
A list of detected package versions is a candidate snapshot, NOT a full lockfile.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import re
import sys
from datetime import datetime, timezone

ALIAS_DISTRIBUTIONS = {
    "sklearn": "scikit-learn",
    "skimage": "scikit-image",
    "imblearn": "imbalanced-learn",
    "PIL": "Pillow",
    "yaml": "PyYAML",
    "cv2": "opencv-python",
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "joblib": "joblib",
    "statsmodels": "statsmodels",
    "threadpoolctl": "threadpoolctl",
}
# Recorded for numerical reproduction, even when transitively installed.
NUMERICAL_RUNTIME_PACKAGES = ("numpy", "pandas", "scipy", "scikit-learn", "joblib", "threadpoolctl")
ENV_VARIABLES = ("PYTHONHASHSEED", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
CONFIG_FILES = ("requirements.txt", "requirements-dev.txt", "pyproject.toml", "poetry.lock", "uv.lock", "environment.yml", "conda-lock.yml", "Pipfile.lock")


def sha256_file(path: Path) -> str:
    hash_obj = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            hash_obj.update(piece)
    return hash_obj.hexdigest()


def file_under_root(root: Path, rel: str) -> Path:
    candidate = (root / rel).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as ex:
        raise ValueError(f"Unsafe inventory path outside project root: {rel}") from ex
    return candidate


def extract_import_roots(file_path: Path) -> tuple[list[str], list[str]]:
    text = file_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(text, filename=file_path.name)
    imports = set()
    relative = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                relative.add("." * node.level + (node.module or ""))
            elif node.module:
                imports.add(node.module.split(".", 1)[0])
    return sorted(imports), sorted(relative)


def version_of(distribution: str) -> str | None:
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--inventory", default="results/reproducibility/p15_01_inventory/p15_01_local_inventory.json")
    parser.add_argument("--out", default="results/reproducibility/p15_02_environment/p15_02_environment.json")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        parser.error("Project root does not exist")
    inventory_path = file_under_root(root, args.inventory)
    if not inventory_path.is_file():
        parser.error("P15-01 JSON not found; run P15-01 first")
    inventory = json.loads(inventory_path.read_text(encoding="utf-8-sig"))
    entries = inventory.get("script_entries", [])
    if not isinstance(entries, list) or not entries:
        parser.error("Invalid P15-01 inventory: no script_entries")

    provider_map = metadata.packages_distributions()
    stdlib_roots = set(getattr(sys, "stdlib_module_names", [])) | set(sys.builtin_module_names) | {"__future__"}
    # Check first-level local .py files and packages to avoid labelling project modules as pip dependencies.
    local_roots = {p.stem for p in root.glob("*.py")}
    local_roots |= {p.name for p in root.iterdir() if p.is_dir() and (p / "__init__.py").is_file()}
    local_roots |= {"src", "tools"}
    imports_by_script = []
    imported_roots = set()
    problems = []
    for entry in entries:
        relative = entry.get("script_found")
        entry_id = entry.get("id", "unknown")
        if not isinstance(relative, str) or not relative:
            problems.append(f"Missing script_found for {entry_id}")
            continue
        try:
            source_path = file_under_root(root, relative)
            if not source_path.is_file():
                problems.append(f"Source file absent: {relative}")
                continue
            roots, rel_imports = extract_import_roots(source_path)
            digest = sha256_file(source_path)
        except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
            problems.append(f"Cannot examine {relative}: {type(exc).__name__}: {exc}")
            continue
        imported_roots.update(roots)
        imports_by_script.append({
            "id": entry_id,
            "phase": entry.get("phase"),
            "script": relative.replace("\\", "/"),
            "sha256": digest,
            "top_level_imports": roots,
            "relative_imports": rel_imports,
        })

    dependencies = []
    for module in sorted(imported_roots):
        if module in stdlib_roots:
            continue
        if module in local_roots or file_under_root(root, f"{module}.py").is_file():
            continue
        providers = provider_map.get(module, [])
        if module in ALIAS_DISTRIBUTIONS:
            expected = ALIAS_DISTRIBUTIONS[module]
            providers = [expected] + [p for p in providers if p.casefold() != expected.casefold()]
        providers = list(dict.fromkeys(providers))
        provider_versions = [{"distribution": name, "version": version_of(name)} for name in providers]
        dependencies.append({
            "module": module,
            "providers": provider_versions,
            "status": ("installed" if any(p["version"] is not None for p in provider_versions)
                       else "unresolved_or_missing"),
            "provider_ambiguity": len([p for p in provider_versions if p["version"] is not None]) > 1,
        })

    numerical_runtime = [
        {"distribution": p, "version": version_of(p)} for p in NUMERICAL_RUNTIME_PACKAGES
    ]
    runtime_env = {}
    for env_var in ENV_VARIABLES:
        val = os.environ.get(env_var)
        runtime_env[env_var] = int(val) if val is not None and re.fullmatch(r"\d+", val) else ("set_non_numeric" if val is not None else None)

    configs = []
    for relative in CONFIG_FILES:
        p = file_under_root(root, relative)
        configs.append({
            "path": relative,
            "exists": p.is_file(),
            "sha256": sha256_file(p) if p.is_file() else None,
        })

    all_packages = {}
    for dep in dependencies:
        for provider in dep["providers"]:
            if provider["version"] is not None:
                all_packages[provider["distribution"]] = provider["version"]
    for entry in numerical_runtime:
        if entry["version"] is not None:
            all_packages[entry["distribution"]] = entry["version"]
    all_packages = dict(sorted(all_packages.items(), key=lambda kv: kv[0].lower()))

    out_path = file_under_root(root, args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path = out_path.with_name("p15_02_candidate_direct_dependencies.txt")
    if out_path == inventory_path or candidate_path == inventory_path:
        parser.error("Refusing to overwrite P15-01 source inventory")
    report = {
        "task": "P15-02 local Python environment & source import snapshot",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "offline read-only inventory; NOT a model rerun, complete lockfile, or guarantee of reproducibility",
        "source_p15_01_inventory_sha256": sha256_file(inventory_path),
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "version_full": sys.version.split(" [", 1)[0],
            "executable_filename": Path(sys.executable).name,
            "in_virtualenv": sys.prefix != sys.base_prefix,
            "architecture": platform.architecture()[0],
        },
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "logical_cpu_count": os.cpu_count(),
            "thread_environment": runtime_env,
        },
        "scripts_checked": len(imports_by_script),
        "scripts_expected": len(entries),
        "imports_by_script": imports_by_script,
        "third_party_imports": dependencies,
        "numerical_runtime_dependencies": numerical_runtime,
        "installed_direct_dependency_candidate_versions": all_packages,
        "dependency_declaration_files": configs,
        "problems": problems,
        "limitations": [
            "Static AST import discovery cannot detect dependencies loaded dynamically or only in notebooks.",
            "The generated version-pinned dependency list is a candidate, NOT a complete resolver-produced lock.",
            "OS/CPU/compiler/BLAS/CUDA and all transitive dependencies may affect numerical reproducibility.",
            "No package installation, dataset reading, training, or internet access occurs.",
        ],
    }
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    candidate = [
        "# P15-02 CANDIDATE dependencies only — NOT a validated lockfile.",
        "# Based on source imports and installed package metadata from the machine that ran the script.",
        "# Review against fresh-environment setup before claiming full reproducibility.",
    ]
    candidate += [f"{p}=={v}" for p, v in all_packages.items()]
    candidate_path.write_text("\n".join(candidate) + "\n", encoding="utf-8")

    unresolved = [d["module"] for d in dependencies if d["status"] != "installed"]
    print("P15-02 CAPTURE COMPLETED")
    print(f"Scripts parsed: {len(imports_by_script)}/{len(entries)}")
    print(f"Detected third-party import roots: {len(dependencies)}")
    print(f"Candidate distributions with version: {len(all_packages)}")
    print(f"Unresolved or missing imports: {unresolved or 'none'}")
    print(f"Problems: {problems or 'none'}")
    print(f"Saved: {out_path.relative_to(root)}")
    print(f"Saved: {candidate_path.relative_to(root)}")
    return 0 if len(imports_by_script) == len(entries) and not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
