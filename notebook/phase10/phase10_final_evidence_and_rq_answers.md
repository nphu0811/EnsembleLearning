# PHASE 10 — FINAL EVIDENCE SYNTHESIS

## Dataset and protocol

- Primary dataset: UNSW-NB15.
- Official test size: 82,332.
- Novel-vector sensitivity subset: 73,791.
- Final frozen pipelines:
  - Stacking-42
  - Random Forest-42
  - Random Forest-17
- No model retraining/tuning was performed in Phase 10.
- Statistical analysis used saved Phase-9 predictions only.

---

## RQ1 — Does ensemble provide stable improvement over a strong individual/reference model?

### Official test: Stacking-42 minus RF-42

- Macro-F1 delta: +0.000497
  - 95% CI: [-0.000312, +0.001309]
- MCC delta: -0.000413
  - 95% CI: [-0.001938, +0.001140]
- FPR delta: -0.003838
  - 95% CI: [-0.005243, -0.002432]
- FNR delta: +0.002603
  - 95% CI: [+0.001853, +0.003375]

McNemar:
- Stacking wrong / RF correct: 491
- Stacking correct / RF wrong: 515
- Holm-adjusted p = 0.468377

### Interpretation

There is no clear evidence that Stacking-42 improves overall predictive performance over
RF-42 in terms of Macro-F1, MCC, or overall paired correctness.

However, Stacking-42 consistently changes the error trade-off:
- fewer false positives,
- more false negatives.

The same qualitative pattern appears on the novel-vector subset.

### Allowed claim

"Stacking did not demonstrate a robust overall superiority over Random Forest on the
official holdout. Its main effect was a statistically supported reduction in false
positive rate accompanied by a statistically supported increase in false negative rate."

### Not allowed

- "Stacking is significantly better than Random Forest."
- "Ensemble always improves IDS performance."
- "Stacking is the best model."

---

## RQ2 — How does feature selection affect performance and computational cost?

### Official test: RF-42 minus RF-17

- Macro-F1 delta: +0.002670
  - 95% CI: [+0.000878, +0.004524]
- MCC delta: +0.004029
  - 95% CI: [+0.000883, +0.007278]
- FPR delta: -0.005973
  - 95% CI: [-0.009514, -0.002568]
- FNR delta: +0.000574
  - 95% CI: [-0.000618, +0.001765]

McNemar:
- Holm-adjusted p = 0.011161

### Computational cost

RF-42:
- Train time: 371.24 s
- Inference: 0.008679 ms/sample
- Size: 205.49 MB

RF-17:
- Train time: 57.26 s
- Inference: 0.003562 ms/sample
- Size: 105.04 MB

RF-17 therefore:
- trains about 6.48x faster,
- reduces training time by about 84.6%,
- infers about 2.44x faster,
- reduces inference time by about 59.0%,
- reduces serialized model size by about 48.9%.

### Interpretation

Feature reduction creates a strong efficiency gain but incurs a small predictive cost on
the full official test. The FNR difference between RF-42 and RF-17 is not clearly
distinguishable from zero in the paired bootstrap.

On the novel-vector subset, the Macro-F1 and MCC differences between RF-42 and RF-17
are less clearly separated, although RF-42 still has a lower FPR.

### Allowed claim

"Feature selection produced a substantial computation–performance trade-off: the
17-feature Random Forest was much cheaper to train and deploy, while the 42-feature
Random Forest retained a small but measurable predictive advantage on the official test."

### Not allowed

- "Feature selection improves accuracy."
- "17 features are universally better."
- "Removing features has no predictive cost."

---

## RQ3 — Is ensemble behavior associated with complementary error patterns?

### Evidence

Phase 7 OOF analysis showed that base learners made non-identical errors.

On the final official test:
- Stacking correct / RF-42 wrong: 515 cases
- Stacking wrong / RF-42 correct: 491 cases
- Total discordant correctness cases: 1,006

These counts demonstrate that the two pipelines do not fail on exactly the same samples.

However, the discordant counts are nearly balanced and McNemar does not reject equal
overall error rate.

### Interpretation

Complementary errors exist, but they do not automatically translate into a net overall
accuracy/Macro-F1 advantage.

Stacking appears to exploit the base predictions mainly by moving the decision boundary
toward fewer false alarms, at the cost of more missed attacks.

### Allowed claim

"Complementary errors were empirically observed among the base learners, but diversity
alone was insufficient to guarantee superior ensemble performance. The way predictions
were combined determined the final FP/FN trade-off."

---

## RQ4 — Sensitivity to evaluation protocol / distribution change

### Current evidence

Development CV produced substantially higher scores than the final official holdout.

On the final test, moving from the full official test to the novel-vector subset changed:

Stacking-42:
- Macro-F1: -0.005715
- MCC: -0.009788
- FNR: +0.003002

RF-42:
- Macro-F1: -0.005870
- MCC: -0.009868
- FNR: +0.002521

RF-17:
- Macro-F1: -0.004950
- MCC: -0.008434
- FNR: +0.002650

### Interpretation

All frozen pipelines degrade on previously unseen feature vectors, especially through
higher false-negative rates.

However, the current UNSW-NB15 files do not provide a clean temporal/day/scenario split
suitable for a direct temporal-vs-random split experiment.

Therefore RQ4 is only partially answered.

### Allowed claim

"Performance is sensitive to the evaluation view: all pipelines degraded on the
novel-vector subset, and final official-holdout performance was materially lower than
development CV performance."

### Not allowed

- "Temporal distribution shift caused the performance drop."
- "Random splitting causes leakage" as a conclusion from these experiments alone.
- "The model generalizes poorly to all unseen networks."

---

# Attack-family findings

The most difficult major attack family was Fuzzers.

Official test miss rates:

- Stacking-42: 754 / 6062 = 12.44%
  - 95% Wilson CI: [11.63%, 13.29%]
- RF-42: 621 / 6062 = 10.24%
  - 95% Wilson CI: [9.51%, 11.03%]
- RF-17: 623 / 6062 = 10.28%
  - 95% Wilson CI: [9.54%, 11.07%]

Stacking performs notably better for Generic attacks:
- Stacking-42: 14 misses / 18,871
- RF-42: 57 misses / 18,871
- RF-17: 3 misses / 18,871

Rare classes such as Worms have very small sample counts (44 samples), so percentage
differences must be interpreted cautiously.

---

# Performance–cost trade-off

## Stacking-42 vs RF-42

Stacking-42:
- Macro-F1: 0.863840
- MCC: 0.750497
- Train: 980.17 s
- Inference: 0.012445 ms/sample
- Size: 206.22 MB

RF-42:
- Macro-F1: 0.863343
- MCC: 0.750910
- Train: 371.24 s
- Inference: 0.008679 ms/sample
- Size: 205.49 MB

Stacking therefore:
- requires about 2.64x the training time,
- requires about 1.43x the inference time,
- has essentially the same serialized size,
- does not show a clear overall Macro-F1/MCC advantage.

---

# Research Decisions Log

## Decision 1
Do not claim Stacking superiority.

Reason:
Macro-F1 and MCC paired bootstrap CIs for Stacking-42 vs RF-42 include zero; McNemar
Holm-adjusted p = 0.468377.

Consequence:
Present Stacking primarily as an FP/FN trade-off rather than as a globally superior model.

## Decision 2
Retain RF-17 as the efficiency-oriented pipeline.

Reason:
Large reductions in training/inference cost and model size, with only a small predictive
loss on the official test.

Consequence:
Report RF-17 as an efficiency trade-off, not as the highest-performance pipeline.

## Decision 3
Do not perform any post-test tuning.

Reason:
Official test has already been opened.

Consequence:
All remaining work is analysis, visualization, writing, and secondary robustness work
that does not alter the frozen UNSW pipelines.

## Decision 4
Treat RQ4 as partially answered unless a separate defensible split experiment is added.

Reason:
Current UNSW-NB15 files do not provide a clean temporal/day/scenario identifier.

Consequence:
Avoid causal claims about temporal/domain shift.

---

# Task Board

| ID | Task | Status | Evidence |
|---|---|---|---|
| P10-01 | Bootstrap metric CIs | DONE | bootstrap_metric_ci.csv |
| P10-02 | Paired bootstrap differences | DONE | paired_bootstrap_differences.csv |
| P10-03 | Exact McNemar | DONE | mcnemar_holm.csv |
| P10-04 | Holm correction | DONE | mcnemar_holm.csv |
| P10-05 | Attack-family uncertainty | DONE | attack_family_miss_rate_ci.csv |
| P10-06 | Novel-vector sensitivity | DONE | official_vs_novel_degradation.csv |
| P10-07 | Cost synthesis | DONE | performance_cost_tradeoff.csv |
| P10-08 | Evidence-based RQ interpretation | DONE | this document |
