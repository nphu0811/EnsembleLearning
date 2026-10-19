# P21 — Four resource pilots accepted; full controlled TRAIN-only study ready for author-host QA (18 Oct 2026)

**Status: FULL SCIENCE IMPLEMENTED / NOT EXECUTED / SYNTHETIC CI RESULT NOT YET VERIFIED.** Do not misstate new validation scores or PDF V3 completion. Source branch: `main` as of this document.

## 1. Accepted author-host resource pilots

| Component | Source evidence | Outcome |
|---|---|---|
| RF42 anchor FIT-only | `p21_train_only_pilot_rf42_01` | resource smoke PASS |
| Stable 17 selector FIT-only | `p21_train_only_pilot_selector17_01` | resource smoke PASS |
| RQ5 RF42 three controlled arms | `p21_train_only_pilot_rq5_01` | resource smoke PASS; peak 316.4 MiB; 91.25s |
| RQ1 Stacking-Lite | `p21_train_only_pilot_stacklite_01` | resource smoke PASS; peak 336.0 MiB; 90.812s; fit 38.937s |

Pilot evidence is **not a measurement of scientific effectiveness**. Four successful low-row pilots do not guarantee that 60k-row full fits pass the 2 GiB memory cap.

## 2. Implemented but unrun full five-arm science

- `tools/p21_science_core.py`: locked RF/stack constructors and sklearn metrics; 3-fold grouped exact-predictor inner OOF (pre-run amendment).
- `tools/p21_science_worker.py`: one 60k-row FIT subset for each predeclared seed, selector MI/L1/ExtraTrees fresh on 35k FIT-only samples per selector seed, exactly five matched arms. Outer validation 35069 rows is TRAIN-derived and grouped exact-vector disjoint.
- `tools/p21_science_supervisor.py`: independent per-seed opt-in, four pilot resource evidence checks, official TRAIN SHA and frozen protocol audit, Python 3.11 sklearn1.9.0/pandas3.0.5 gate, 1 CPU, RSS 2 GiB, available host RAM floor 1.5 GiB, >=4 GiB at start, >=10 GiB free disk, watchdog heartbeat, **NO WALL-TIME LIMIT**. Worker output is never silently accepted without confusion-matrix consistency checks.
- `tools/p21_science_acceptance.py`: strict count reconciliation and paired-source identity checks; rejects partial arms and early TEST/tuning claims.
- `tools/p21_science_aggregate.py`: requires exactly one valid success for **every** seed 1103,2207,3301,4409,5501, rejects cherry-picked duplicates, prints per-seed and paired contrasts with mean ± sample SD (descriptive).
- `tools/p21_run_all_seeds.ps1`: Windows orchestrator with synthetic preflight, chronological per-seed run, **operator-invoked resume**; keeps failed attempts immutable and stops on resource failure.
- `docs/research/PRE_FULL_SCIENCE_GROUP_SAFE_CV_AMENDMENT_2026-10-18.md`: disclosed difference from original inner StratifiedKFold config.

This extension is **POST-HOC reused official TRAIN**, not a new independent TEST or preregistration of original P9. Three-way model/selector changes are controlled as predeclared; RQ1 stacking specifically uses grouped OOF inner CV per amendment rather than pilot's simple stratified fold.

## 3. Windows operator checklist (do not skip)

After `git pull --ff-only origin main`, from repository root with the author-verified `.venv-p15-local` Python:

```powershell
.\.venv-p15-local\Scripts\python.exe -m unittest discover -s tests -p "test_p21_science_acceptance.py" -v
.\.venv-p15-local\Scripts\python.exe -m unittest discover -s tests -p "test_p21_science_synthetic.py" -v
.\.venv-p15-local\Scripts\python.exe -m unittest discover -s tests -p "test_p21_science_aggregation.py" -v
.\.venv-p15-local\Scripts\python.exe -X utf8 tools/p21_protocol_validator.py --verify-local-train-sha
```

If all are PASS and GitHub CI is green, **author may explicitly run**:

```powershell
& .\tools\p21_run_all_seeds.ps1
```

The script carries its own exact scientific opt-in token to the supervisor; full science does not time out. It will stop safely on insufficient RAM; rerunning the script skips an already successfully accepted seed and chooses a new immutable directory only for an unfinished seed. Do NOT launch multiple runs concurrently.

**Important:** A programmatically successful resource pilot is no guarantee of absence of temporal/session leakage or external generalization. If any new code/tests fail, review and amend *before* looking at internal validation outcomes. Do not change or rerun a seed just because its metric is unfavorable.

## 4. Publication/evidence hygiene

New `.gitignore` prevents untracked runtime heartbeat/gate/CSV from being staged; prior already-tracked pilot telemetry files remain in Git history. Avoid `git add .` without verifying `git status`; stage only selected `start.json`, `run_report.json`, `worker/worker_result.json`, five-seed summary `aggregate.json`, `report.md`. Preserve detailed telemetry locally.

If and only if all five seed reports pass immutable checks, use the descriptive contrast report for careful manuscript revision. Keep original official P9 TEST results unchanged and label every P21 result as TRAIN-derived internal validation with reused training context and prior hypothesis awareness. A successful code or CI build is not evidence that the full run has happened.

## 5. Remaining blocked scientific and editorial work

- Actual full experiment 5 seeds × 5 arms is NOT EXECUTED as of this note.
- GitHub CI and author-host synthetic science tests must be inspected before launch.
- NotebookLM exact original remarks with page anchors are not preserved in repo; current 10-theme ledger is an approximation, not verbatim transcript.
- PDF V3 NOT REBUILT. Existing approved PDF(s) and historical P9/P15 sources remain untouched. Final PDF changes may be made only from real verified outcomes and the precise reviewer issues (if accessible).
- P18/P19 literature, release rights and institution approval remain independently open.
