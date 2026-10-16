# Canonical Phase 14 — Error Analysis, Step 1

## Verified evidence

- Official test samples: 82,332
- RF-only correct: 491
- Stacking-only correct: 515
- Both wrong: 10,222
- Both correct: 71,104
- RF-42 false positives: 10,003
- Stacking-42 false positives: 9,861
- RF-42 false negatives: 734
- Stacking-42 false negatives: 852

## By true class (paired transitions)

Normal traffic (n=37,000):
- RF-only correct: 278 (Stacking introduces a false positive)
- Stacking-only correct: 420 (Stacking resolves an RF false positive)

Attack traffic (n=45,332):
- RF-only correct: 213 (Stacking introduces a false negative)
- Stacking-only correct: 95 (Stacking catches an attack RF missed)

Net effects: 142 fewer false positives; 118 more false negatives for Stacking.

## Interpretation boundary

These are DESCRIPTIVE error comparisons on the frozen official TEST.
They do not establish the causal mechanism of the Stacking meta learner.
No model/threshold/feature changes are permitted after the holdout.

## Next

Interpret `attack_family_transitions.csv` with family supports and
Wilson uncertainty (already available in canonical Phase 12).
Do not pick a new model from these post-test diagnostic results.
