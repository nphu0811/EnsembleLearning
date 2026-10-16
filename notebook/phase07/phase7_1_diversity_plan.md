# PHASE 7.1 — OOF Diversity Analysis

## Objective

Check whether strong candidate learners make complementary errors before combining them
into a heterogeneous ensemble.

## Base learners

- Logistic Regression
- Decision Tree
- Random Forest
- AdaBoost

## Feature tracks

- All 42 original model features
- 17 stable features selected by at least two feature-selection families

## OOF protocol

The official training split is divided into three stratified folds. Each fold is predicted
by models trained only on the other folds. Therefore every OOF prediction is made on a
sample the corresponding model did not train on.

## Diversity metrics

- Disagreement Rate
- Double-Fault Rate
- Pairwise Oracle Accuracy
- Q-statistic
- Error Correlation
- Probability Correlation

## Interpretation rule

High diversity by itself is not valuable. A weak classifier can disagree with everyone.
Candidate ensemble members must be judged jointly by:

1. predictive strength,
2. complementary errors,
3. computational cost.

`attack_cat` is retained only as metadata for attack-family miss analysis and is never
used as an input feature.

## Next

Phase 7.2 will use this evidence to construct a small number of justified Hard Voting,
Soft Voting, and Stacking configurations. The official test remains locked.
