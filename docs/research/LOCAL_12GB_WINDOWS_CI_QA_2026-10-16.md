# P15 local 12GB — Windows guard test QA (16/10/2026)

**Scope:** Python safety/guard implementation, NOT ML reproduction.

## Independent Windows CI result

- GitHub Actions run: https://github.com/nphu0811/EnsembleLearning/actions/runs/38928283823
- Head SHA checked: `1de823f6b56dbdedac25341949819a6b3a05d49f`.
- Runner: `windows-latest`, Python 3.11, installed `psutil` only; **no research data, no model fitting, no official TEST access**.
- Unit test invocation: `python -m unittest discover -s tests -p "test_p15_local_supervisor.py" -v`.
- **18/18 tests PASS**, workflow result SUCCESS. Test log includes `Ran 18 tests`.
- First Windows run `38928057082` FAILED two path-format assertions caused by Windows 8.3 temporary folder aliases (e.g., `RUNNER~1`). The implementation/test were corrected using canonical path comparison. Second intermediate run `38928275761` ran before both changes were on HEAD; latest full source commit passed. The failures are preserved as repair history.

## What was tested

- Resource gates: the author's previously observed approximately 2.01 GiB free RAM must **not start** a worker; conditional monitored pilot policy requires >=4 GiB RAM free, process-tree RSS cap 2 GiB, system free RAM floor 1.5 GiB and disk floor 10 GiB.
- Output creation only in NEW subfolders of `results/reproducibility/`, refusal to overwrite existing output or write into frozen result directories.
- Read-only source load and explicit forbidden official TEST and interim CSV paths.
- Matching prior pilot evidence, same candidate/config/source hashes; no pilot means no full job.
- Actual kill of a synthetic sleeping subprocess (not ML).
- No successful result for a missing/tampered model artifact; pilot cannot present a full artifact.

## NOT proven

These tests do not establish memory upper bounds of full RF-17/RF-42/Stacking-42, Windows full fit/predict success, joblib serialization/reload on actual 175,341 TRAIN rows, or original-scikit-learn-version reproducibility. The watchdog is sampled at 0.5s and does not substitute for a kernel-enforced hard memory quota. The current author-reported free RAM was ~2.01 GiB and fails both original 9-GiB gate and new 4-GiB conditional pilot gate.

P15/G3 remains **PARTIAL**. The user-approved 5-chapter research PDF, original P9 source, frozen configs, official results and raw dataset were not altered.

## Next user action

Pull the latest main, follow `docs/research/LOCAL_12GB_RUNBOOK_2026-10-16.md` to create a clean Python 3.11 venv, run 18 tests, measure RAM. If less than 4 GiB is free, do not train. If >=4 GiB, run only the supervised RF-17 pilot first; inspect `run_report.json` and RAM trace before considering further sequential jobs.
