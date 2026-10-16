# Figure captions

**Figure 1. Official-test Macro-F1 with 95% bootstrap confidence intervals.**
The three frozen pipelines achieve similar overall Macro-F1. The Stacking-42 and RF-42
intervals strongly overlap, consistent with the paired analysis showing no clear overall
Macro-F1 advantage for Stacking.

**Figure 2. Official-test MCC with 95% bootstrap confidence intervals.**
RF-42 and Stacking-42 show nearly identical MCC, whereas RF-17 is slightly lower,
illustrating the small predictive cost associated with feature reduction.

**Figure 3. False-positive versus false-negative trade-off on the official test.**
Stacking-42 shifts the operating behavior toward fewer false positives but more false
negatives relative to RF-42. RF-17 has the lowest FNR among the three frozen pipelines
but the highest FPR.

**Figure 4. Official-test Macro-F1 versus training time.**
The figure highlights computational efficiency rather than a model ranking. RF-17
requires substantially less training time with a modest reduction in Macro-F1, while
Stacking-42 incurs the highest training cost without a clear overall Macro-F1 advantage
over RF-42.

**Figure 5. Sensitivity of Macro-F1 to previously unseen feature vectors.**
All three pipelines show lower Macro-F1 on the novel-vector subset than on the complete
official test, indicating sensitivity to the evaluation view. The analysis does not
establish the cause of the degradation.

**Figure 6. Attack-family miss rates with Wilson 95% confidence intervals.**
Fuzzers has the highest miss rate among the major attack families for all three models.
The figure includes attack families with at least 300 positive test samples; very rare
families are retained in the accompanying table rather than emphasized visually.
