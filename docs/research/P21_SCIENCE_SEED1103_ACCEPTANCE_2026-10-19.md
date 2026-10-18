# P21 first scientific seed 1103 — read-only independent report QA (2026-10-19)

**Scope:** read-only check of files committed as author result in [e387d9f](https://github.com/nphu0811/EnsembleLearning/commit/e387d9f61e86d7e2264cb67148d4f3337b7840e7), not a second training run. Full five-seed P21 inference **INCOMPLETE (1/5)**.

## Authentic result files

- `results/controlled_extensions/p21_train_only_science_seed_1103_01/start.json`
- `results/controlled_extensions/p21_train_only_science_seed_1103_01/run_report.json`
- `results/controlled_extensions/p21_train_only_science_seed_1103_01/worker/worker_result.json`

## QA conclusion

**12/12 independently recomputed cross-file/metric consistency groups PASS**, from fetched GitHub JSON:
1. Seed 1103 identities across report and worker;
2. PASS status and TRAIN-reused internal-validation scope;
3. TRAIN SHA-256 `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`;
4. Protocol identity agrees across start, run and worker;
5. Exit 0/null stop, positive resource samples and peak below cap;
6. Explicit no-official-TEST and no-independent-external-test scope;
7. 60,000 FIT, 35,069 internal validation, group-disjoint outer split;
8. Fresh top17 selector (17 unique original features, 15 selector calls, no validation);
9. Exactly A0/A1/A2/A3/A4 arms in predeclared order;
10. Identical FIT row-identity digest across arms (original 60k; oversampling derived only from those identities);
11. Each arm confusion matrix sums to 35,069 with common true support **11,200 Normal + 23,869 Attack**;
12. Macro-F1, MCC, Attack precision/recall, FPR and FNR recomputed from all 5 arms' TN/FP/FN/TP within 1e-10 tolerance.

These checks establish **report integrity/consistency only**, not independent replay of raw data, no host process attestation, no external validation and no grounds for a significance statement.

- Resource wall: **1839.844 s (~30min 40s)**; peak tree RSS **393,740,288 bytes (375.5 MiB)**, 3,608 resource samples, minimum system available memory **3,301,068,800 bytes**; no full-training wall-time limit.
- Selector: fresh FIT-derived 17 features from the seed-specific 60k source sample, 35k rows for each selector seed; 15 selector calls; selector fit **210.640 s**, `eligible_stable_count=18`, `forced_top17_count=0`.
- Inner Stacking was `StratifiedGroupKFold` 3-fold by exact original predictors, based on pre-full documented amendment. This does not prove freedom from correlated sessions / time ordering.

## Exact per-arm internal-validation metrics for seed 1103

| Arm | Macro-F1 | MCC | FPR | FNR | FP | FN | Fit seconds |
|---|---:|---:|---:|---:|---:|---:|---:|
| A0 RF42 NONE | 0.944741 | 0.889842 | 0.093125 | 0.026185 | 1043 | 625 | 207.281 |
| A1 RF17 NONE | 0.938678 | 0.877752 | 0.102232 | 0.029536 | 1145 | 705 | 76.063 |
| A2 RF42 BALANCED | 0.944006 | 0.888242 | 0.061607 | 0.043194 | 690 | 1031 | 226.500 |
| A3 RF42 OVERSAMPLE | 0.944235 | 0.888487 | 0.072054 | 0.037580 | 807 | 897 | 376.062 |
| A4 STACK42 NONE | 0.944444 | 0.889167 | 0.091429 | 0.027441 | 1024 | 655 | 688.218 |

Compared with A0:
- RQ1 A4: **Δ Macro-F1 -0.000297**, FP **-19**, FN **+30**.
- RQ2 A1: **Δ Macro-F1 -0.006063**, FP **+102**, FN **+80**; RF fit time 76.063 vs 207.281 seconds (2.73× speedup for FIT, excluding selector compute cost).
- RQ5 A2: **Δ Macro-F1 -0.000735**, FP **-353**, FN **+406**.
- RQ5 A3: **Δ Macro-F1 -0.000506**, FP **-236**, FN **+272**.

**Scientific interpretation limit:** This is one of five predeclared FIT replications, with shared internal validation and reused original TRAIN context. Do not promote this exploratory seed snapshot to a full RQ1/RQ2/RQ5 inference; do not tune variants after seeing these scores or try to select a favorable subset of seeds.

## Methodology/metadata note

The nested `split.validation_evaluation_performed=false` field is copied from the **pre-fit split QA** produced by the splitting helper, not a claim that the overall scientific worker never evaluated the held-out internal fold. Actual `arms[*].metrics` are evaluations of P21 **internal validation**. Manuscript and defense must distinguish **no official TEST access** from **yes, internal validation was scored**. To preserve the 5-seed design after seed1103 was observed, do not silently edit original worker flags, hyperparameters, CV or published past JSON. Treat this as a documentary metadata-interpretation erratum.

## Subsequent reproducibility and publication gates

- Remain on exact predeclared seeds **2207, 3301, 4409, 5501** with original full-run code, same P21 protocol, grouped fold and source SHA; no TEST.
- Operator should rerun `tools/p21_run_all_seeds.ps1` once after pull: it recognizes seed1103 PASS and resumes pending seeds. Must not launch multiple supervisors in parallel.
- Detailed output logs/heartbeat/gates remain local. Only the three compact JSON reports per seed and final summary are appropriate for git staging (avoid `git add .`).
- Only when **5/5** seed reports pass the strict acceptance and aggregate checks may descriptive paired contrasts be placed into a **new** PDF V3; retain historical V2 and report post-hoc TRAIN-derived limitation and exact NotebookLM original evidence gaps.
- Do not claim PDF V3 compiled or CI successful without those independent observations.
