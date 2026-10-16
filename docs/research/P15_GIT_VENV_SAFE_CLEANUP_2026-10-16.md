# P15 — Safely stop tracking local Python venv (Windows)

**Reason:** Author's `ab88db8` added the installed `.venv-p15-local/` to Git. Installed environments contain machine-specific files and should be regenerated from requirements, not committed. About 7,401 tracked tree entries are under this folder. 

**Scope:** Git index cleanup only. Preserve physical laptop venv and all frozen science sources/results. **No force push, history rewrite, `git reset --hard`, `git clean -fd`, or manual deletion of the venv.** This instruction requires the author to execute commands **locally before** a remote deletion commit exists.

## On the original Windows NCKH checkout

Close training terminals to ensure no Python process is using the venv and then in PowerShell from repository root:

```powershell
git status --short
git pull --ff-only origin main

# Ignore pattern was added to .gitignore upstream.
git check-ignore --no-index .venv-p15-local/Lib/site-packages/joblib/__init__.py

# Remove ONLY from Git index; --cached means leave working files on disk.
git rm -r --cached -- .venv-p15-local

# The locally installed Python MUST still exist.
Test-Path .\.venv-p15-local\Scripts\python.exe

# Verify only the intended directory is staged for deletion.
git diff --cached --name-only | Select-Object -First 20
git diff --cached --name-only | Where-Object { $_ -notlike '.venv-p15-local/*' }
```

The final `Where-Object` output should be **empty**. `Test-Path` should print `True`; if not, STOP and restore the environment before continuing. If a different file is staged or there is an existing local merge/conflict, STOP and inspect, do not run further commands.

Then, only if the above checks are good:

```powershell
git commit -m "chore: untrack local P15 virtual environment"
git push origin main
```

Check the latest GitHub tree no longer contains `.venv-p15-local/`. The historical commit `ab88db8` will still include its previous blobs; a no-history-rewrite cleanup only corrects HEAD, not past public history. Any data-sharing/privacy review of past history is a separate task requiring the owner's authorization.

## Important coordination warning

Do **not** delete these files directly using the GitHub UI or a remote API commit **before** the original Windows checkout has safely removed them from its index. A later `git pull` of such a remote deletion could remove the local Python environment because Git currently tracks it. Performing `git rm --cached` on the laptop first preserves the local files while moving them out of version control.

If the user prefers a backup before Git changes, shut down training and copy only the reusable requirements/version information. Virtual environments themselves are normally recreated; no need to push one to a public repository.

## Then continue P15

Run remaining pilots, **sequentially**, each only if the fresh 4 GiB available RAM admission policy passes:

```powershell
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode pilot --candidate random_forest_42 --out-dir results/reproducibility/p15_local_rf42_pilot_01
.\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode pilot --candidate stacking_42 --out-dir results/reproducibility/p15_local_stack_pilot_01
```

For each one, stop and inspect `run_report.json` before running the next. Output paths must **not exist** prior to starting. Send the two reports for resource/provenance QA. Only then consider independent full-TRAIN fits one at a time; never call the original P9 `main()`.
