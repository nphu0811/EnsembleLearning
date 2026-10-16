# NCKH — Canonical Phase 15, P15-02 Environment Audit Review

**Evidence:** User-supplied `p15_02_environment.zip` containing `p15_02_environment.json` (generated UTC 2026-10-10 18:23:23) and `p15_02_candidate_direct_dependencies.txt`.

## Direct verification performed

- ZIP opens correctly, contains one JSON and one text candidate dependency list (plus folder entry). JSON parses without error.
- Snapshot declares `scripts_checked=18`, `scripts_expected=18`, no recorded problems.
- OS Windows 11 x64, 8 logical CPUs; CPython **3.14.3**, running **outside** a virtual environment.
- Static-import discovery of all 18 inventoried scripts found package providers for `numpy`, `pandas`, `scipy`, `sklearn` and `matplotlib`. Versions are metadata reported **by the user's machine**, not independently imported or installed here.
- Direct/numeric dependency candidates: `joblib==1.5.3`, `matplotlib==3.11.1`, `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `scipy==1.18.1`, `threadpoolctl==3.6.0`.
- Snapshot reports **no project-root `requirements.txt`, `pyproject.toml`, `environment.yml` or lockfile** among the checked types. `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, and `VECLIB_MAXIMUM_THREADS` are not set as environment variables at the time of this snapshot (does not prove algorithms didn't fix their own seeds/threads).
- **Independent historical provenance cross-check:** `NCKH_AUDIT_BUNDLE.zip` contains `snapshot/results/ablation/unsw_nb15/phase13_ablation/analysis_metadata.json`, which states `python=3.11.9`, `pandas=3.0.5`, **`training_performed=false`**. Thus, at least one historical saved analysis used another Python version. This is **not evidence that RF-42/Stacking-42 were trained under 3.11.9**.

## Scientific judgment

**P15-02A — Snapshot: DONE.** The user's current interpreter and relevant installed distribution versions are recorded, including candidate pins. No missing distributions are reported in this snapshot.

**P15-02B — Verify package consistency and historical provenance: TODO, script supplied.** It will check the current installed versions against the snapshot and run `python -m pip check` offline. It also reads Phase13 metadata locally. The output will be a compact JSON with an installed distribution list.

**P15-02C — Full isolated reproducibility environment: TODO.** Build/check a compatible dependency manifest in a fresh virtual environment, verify direct imports, and record a resolver result and commands. Do not silently adopt today's installed versions as original model-training versions. No training/test reinterpretation in this stage.

**P15-02 overall: PARTIAL.** No claim of an exact dependency lock, original-training version provenance or clean-room replay is supported.

## Research Decisions Log

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Treat uploaded JSON as current-machine audit, not reproduction | Version inventory isn't a tested install | JSON scope; 7 candidate pins; no lockfile | P15-02 remains PARTIAL |
| Flag Python discrepancy without attributing to final model training | Phase13 was nontraining aggregation | Phase13 metadata `python=3.11.9`, `training_performed=false` | Require independent original-training provenance |
| Do not install/upgrade now | Changing live environment risks breaking artifacts and using laptop resources | Windows global interpreter and lack of venv | Read-only consistency check next |

## Task Board

| ID | Task | Status | Evidence |
|---|---|---|---|
| P15-01 | Script/input/output map and local presence | DONE | Previous verified local inventory |
| P15-02A | Current environment snapshot & basic imports | DONE | User-supplied P15-02 JSON and candidate pins |
| P15-02B | Local installed dependency consistency / provenance | TODO | Await output of supplied check script |
| P15-02C | Isolated install manifest and smoke run | TODO | None yet |
| P15-02 | Environment & dependency lock | PARTIAL | No validated lockfile, clean env or historical training provenance |

## Limitations

The review checks user-exported metadata plus historical Phase13 archived metadata. It **does not independently execute** any code on the Windows machine, inspect current raw data, import numerical libraries, reserialize models, train a model, or establish exact numeric reproducibility.
