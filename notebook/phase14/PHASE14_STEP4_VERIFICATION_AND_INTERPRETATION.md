# NCKH — Canonical Phase 14 / Step 4

**Scope:** Independent consistency review of submitted `phase14_error_analysis_step4.zip` (10 CSV files, 1 Markdown summary; 11 files in output directory). **Status:** PASS for internal aggregate consistency; source-row alignment asserted by run summary but not independently replayed because official raw TEST and frozen prediction CSV are not in the archive.

## Inputs and integrity

- User-provided archive: `phase14_error_analysis_step4.zip`.
- Run summary reports 82,332 unique IDs aligned one-to-one, labels and attack categories matched, frozen RF-42 and Stacking-42 confusion matrices matched; these checks were **reported by the execution script**, not independently re-executed here.
- Independently re-calculated and checked every row of `state_by_value.csv`, `proto_by_value.csv`, and `sttl_by_value.csv` against their four error-group counts, total support, both models' FN numerators, net FN, and denominator-correct conditional FNRs.
- Independently reconciled all `*_group_composition.csv` counts and shares against every corresponding value in `*_by_value.csv`; group totals match.
- All `sttl`, `dload`, `ct_state_ttl` numeric summary group supports and quantile orderings match.
- **All completed aggregate assertions PASS.** No training, threshold, or model change was performed.

## Paired Fuzzers errors

Fuzzers support n=6,062:

| Paired correctness group | Samples |
|---|---:|
| RF and Stacking both catch | 5,261 |
| RF catches; Stacking misses | 180 |
| RF misses; Stacking catches | 47 |
| Both miss | 574 |
| **Total** | **6,062** |

RF misses = 47+574=621; Stacking misses = 180+574=754; net +133 Stacking FNs. RF FNR 621/6,062 = 10.24%; Stacking FNR 754/6,062 = 12.44%. These are binary Normal-versus-Attack misses within actual attack-family Fuzzers, not multiclass Fuzzers classification.

## Feature profiles

### Protocol (`proto`)

| Protocol | Support | RF FN | Stack FN | RF FNR | Stack FNR | New Stack FN | Stack rescues |
|---|---:|---:|---:|---:|---:|---:|---:|
| tcp | 3,713 | 446 | 535 | 12.01% | 14.41% | 110 | 21 |
| udp | 1,098 | 175 | 219 | 15.94% | 19.95% | 70 | 26 |

`tcp` and `udp` account for all 180 new Stacking FNs and all 47 rescued RF FNs in these outputs. Net TCP +89, net UDP +44. Across the observed test, UDP Fuzzers have higher conditional FNR than TCP Fuzzers for both models. These comparisons are descriptive; `proto` interacts with other features.

### Connection state (`state`)

| State | Support | RF FN | Stack FN | RF FNR | Stack FNR |
|---|---:|---:|---:|---:|---:|
| FIN | 3,703 | 445 | 534 | 12.02% | 14.42% |
| INT | 2,317 | 175 | 219 | 7.55% | 9.45% |

New Stacking FNs: FIN 110 and INT 70; rescued RF FNs: FIN 21 and INT 26. The similarities between state and protocol counts **do not establish** that their effects are independent; no joint cross-tabulation was provided.

### Source TTL (`sttl`)

`sttl=254` appears in 6,047/6,062 Fuzzers (99.75%), including all 180 new FNs and all 47 rescued FNs. Because this value is nearly universal among Fuzzers, it does **not** distinguish why Stacking rescues some samples but misses others. Zero FNs at `sttl=255` (n=14) or `sttl=62` (n=1) cannot justify a general rule on such small supports.

### Destination load (`dload`)

Median dload: both caught 2,277.79; RF caught / Stack missed 2,403.95; RF missed / Stack caught 0; both missed 3,368.10. Percent dload equal zero: 39.99%, 38.89%, 55.32%, and 25.96%, respectively. These are conditional distributions in selected paired error groups; group n=47 is particularly small. Do not interpret medians as thresholds or causal effects.

### `ct_state_ttl`

Median: both caught 1; new Stacking FNs 1; rescued RF FNs 2; both missed 1. This warrants cautious follow-up only; summary alone does not provide causal attribution.

## Interpretation and scientific limits

1. Stack42 creates 180 Fuzzers FNs that RF42 does not, rescues 47 that RF42 misses, and yields a net disadvantage of +133 FNs within Fuzzers.
2. TCP/UDP and FIN/INT are useful **descriptive strata**, not evidence that these features cause misses.
3. `sttl=254` is too ubiquitous within Fuzzers to explain the direction of paired disagreement alone. Its prominence in earlier Normal false-positive analysis suggests that single-feature explanations are especially inadequate.
4. Report subgroup denominators clearly: `P(miss | actual Fuzzers AND proto=udp)` is not `P(proto=udp | miss)`.
5. Frozen official TEST was used strictly for post-hoc description. No test-guided changes to architecture, feature set, model weights, thresholds, or training are justified.
6. Do not extrapolate to unseen deployments or another benchmark, and do not call this multiclass attack-family detection accuracy.

## Phase 14 Task Board

| ID | Task | Status | Evidence |
|---|---|---|---|
| P14-01 | Paired error transitions | DONE | Phase14 Step1 output |
| P14-02 | Attack family comparison | DONE | Phase14 Step1/2 |
| P14-03 | Normal FP feature profiles | DONE | Phase14 Step3 output |
| P14-04 | Fuzzers FN feature profiles | DONE (within saved-artifact scope) | This ZIP, independent aggregate checks |
| P14-05 | Final scientific synthesis of errors and limitations | TODO | Consolidate P14-01 to P14-04; no new training |

**Checkpoint:** Phase14 Step4 is complete within descriptive analysis; proceed to canonical Phase14 Step5, synthesis, once interpretation is understood.
