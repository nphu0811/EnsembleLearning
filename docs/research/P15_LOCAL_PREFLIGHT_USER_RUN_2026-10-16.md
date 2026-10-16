# P15 — Windows local read-only preflight: user-reported run

**Reported by:** project author in ChatGPT, 2026-10-16 15:19:49.860182 UTC (timestamp inside pasted JSON).  
**Scope of evidence:** Author-pasted PowerShell stdout; this repository update **did not independently rerun** the Windows preflight or the full model-training pipeline.  
**Project:** UNSW-NB15 binary IDS; P15/G3 remain PARTIAL.

## Commands reported as run locally

```powershell
python -m unittest discover -s tests -p "test_p15_fulltrain_preflight.py" -v
python tools/p15_fulltrain_preflight.py --project-root .
```

- Fixture-only tests: **6/6 passed** (0.285 s).
- Read-only preflight checks: **11/12 passed**; `preflight_checks_pass=false`, `training_authorized=false`, `reconstruction_status=NOT_RUN`.

| Gate | Reported result | Grounded observation |
|---|---|---|
| SHA-256 TRAIN | PASS | `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa` |
| SHA-256 P9 source | PASS | `3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480` |
| SHA-256 frozen configs | PASS | `cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6` |
| SHA-256 stable-feature list | PASS | `5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be` |
| TRAIN class counts | PASS | 175,341 lines: Normal 56,000; Attack 119,341 |
| Predictor schema | PASS | Exactly 42 ordered input features; no id/label/attack_cat predictor |
| Feature subset | PASS | Stable subset includes 17 known predictors |
| Frozen model/threshold | PASS | RF-17, RF-42, Stacking-42; threshold 0.5 |
| Python | PASS | 3.11.9 |
| Available RAM >= 9 GiB | **FAIL** | 2,157,973,504 bytes ~= 2.01 GiB; approximately 6.99 GiB below requested gate |
| Free disk >= 10 GiB | PASS | 31,032,864,768 bytes ~= 28.90 GiB |
| Tracked Git working tree clean | PASS | HEAD `78470b09080f51d534cb773c7524e0ae497fd46a`; `tracked_worktree_clean=true` |

## Interpretation and decisions

1. The six fixture tests pass, and the author-reported local project checks indicate a consistent TRAIN dataset, model source, locked configs, ordered schema and feature subset. Neither test suite nor preflight performs a training run or reads official TEST.
2. **NO_GO for full-TRAIN model rebuilding on the observed host snapshot.** Do not disable/bypass the 9-GiB RAM gate just to start training. On a 12-GB Windows laptop, this preflight threshold is a conservative protection and might require a different host; it is not a measured minimum RAM requirement of the models.
3. `git_clean_tracked_files` only checks changes to tracked files, not untracked files. No need for an author-side `git push` to report these read-only results. The author can pull the next repository commit when new changes are made upstream.
4. Even if resource gate passes later, launch remains unauthorized pending an isolated reviewed runner/watchdog, clean package provenance and a fresh resource check. The historical environment remains UNKNOWN; training results and release gates stay unchanged.
5. Next **unblocked** research work: continue publication-source/figure QA (P16) and research literature/citation verification (P18) using frozen evidence. Preserve the approved five-chapter report PDF; no new tuning on official TEST.

**Evidence boundary:** This note is a transcription and interpretation of user-supplied terminal output, not an independent Windows execution log or downloaded signed JSON.
