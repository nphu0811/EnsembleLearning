# Canonical Phase 14 — Step 3: Verification & Scientific Interpretation

**Status:** DONE for Step 3; Phase 14 remains DOING.

## 1. Input

User-produced `phase14_error_analysis_step3.zip`: seven CSV tables plus `PHASE14_STEP3_SUMMARY.md`.

The source summary reports PASS for official TEST/prediction join by unique `id`, label/attack-category agreement and matching frozen confusion matrices. Independently, the seven output tables were re-aggregated and internally cross-checked. The raw joined records were not supplied in this ZIP, so the original join was not independently rerun here.

## 2. Independently verified numerical identities

For each of `state`, `proto`, and `sttl`: total Normal support = **37,000**; Stacking-correct/RF-wrong = **420**; RF-correct/Stacking-wrong = **278**; both correct = **26,719**; both wrong = **9,583**; RF FP = **10,003**; Stacking FP = **9,861**. All by-value count, error-group proportion, and conditional FP-rate relationships match their denominators.

## 3. Core findings

| Feature / value | Normal support | Stacking fixes RF FP | Stacking introduces FP | Net FP change (Stacking minus RF) |
|---|---:|---:|---:|---:|
| state=FIN | 24,172 | 327 | 200 | -127 |
| state=INT | 4,485 | 90 | 78 | -12 |
| proto=tcp | 27,848 | 330 | 200 | -130 |
| proto=udp | 8,097 | 90 | 78 | -12 |
| sttl=254 | 15,049 | 401 | 217 | **-184** |
| sttl=62 | 4,129 | 19 | 61 | **+42** |

`sttl=254` accounts for a net **184 fewer FP** under Stacking but `sttl=62` accounts for **42 additional FP**, yielding **-142 FP** overall.

Within Normal rows with `sttl=254`, RF-42 FP rate is **58.88%** and Stacking-42 FP rate is **57.66%**. Both models therefore struggle strongly in this feature-defined subgroup on the official benchmark; this is a descriptive association, not causal identification.

`state=FIN` constitutes 327/420 = **77.86%** of the Stacking-fixes-RF subgroup. Separately, on all 24,172 Normal rows with `state=FIN`, Stacking correctness is **70.78%**. These conditionals are different and must never be conflated.

`state=INT` also has high Normal conditional FP rates (RF 62.25%, Stacking 61.98%); rate comparisons should always include subgroup support. The rare `state=RST` has only one Normal observation and cannot support general conclusions.

## 4. Interpretation boundaries

- The observed variables were grouped one at a time; feature groups may overlap and be correlated.
- No causal explanation for the Stacking meta learner follows from these counts.
- This step covers **Normal FP errors** only, not false negatives among actual Attack flows.
- Any further use of official test is for fixed-pipeline, descriptive error analysis only. No model/feature/threshold changes are permitted.

## 5. Checkpoint

| Task | Status | Evidence |
|---|---|---|
| Step 3 input/output consistency | DONE | All seven CSVs independently checked |
| Normal subgroup FP analysis | DONE | state/proto/sttl by-value and composition tables |
| Distinguish P(feature\|error-group) vs P(error\|feature) | DONE | Explicit conditional interpretation |
| Feature-level causal explanation | NOT ESTABLISHED | Observational subgroup analysis only |
| Step 4: Attack/Fuzzers FN feature analysis | TODO | Requires saved frozen predictions and attack feature values |

**Next:** Canonical Phase 14 Step 4 — compare Attack/Fuzzers false-negative patterns between RF-42 and Stacking-42 using frozen predictions, with proper denominators and no retraining.
