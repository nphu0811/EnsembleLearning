# Canonical Phase 14 — Step 4: Fuzzers feature analysis

**Status:** descriptive error analysis on frozen official TEST predictions.

## Integrity checks
- 82,332 unique IDs aligned one-to-one with official test: PASS.
- Binary labels and attack categories matched for every ID: PASS.
- RF-42 / Stacking-42 confusion counts match frozen results: PASS.
- Fuzzers support 6,062 and four paired error groups verified: PASS.

## Fuzzers paired groups
```
           error_group    n  share_of_all_fuzzers
           both_caught 5261              0.867865
rf_caught_stack_missed  180              0.029693
rf_missed_stack_caught   47              0.007753
           both_missed  574              0.094688
```

- Stacking fixes 47 Fuzzers false negatives of RF but creates 180 new ones.
- Net difference: +133 FNs (Stacking minus RF).
- Both models miss the same 574 Fuzzers flows.

## How to read the CSV outputs
- `*_by_value.csv`: conditional FNR P(model misses | actual Fuzzers, feature=value).
- `*_group_composition.csv`: distribution P(feature=value | paired error group).
- `*_numeric_summary.csv`: quantiles within paired groups, not causal effects.
- Do NOT reverse conditional probabilities or infer general accuracy from selected disagreements.
- Low-support values are exploratory and should not be ranked as reliable deployment rules.

## Most frequent state values among Fuzzers
```
state  fuzzers_support  rf_caught_stack_missed  rf_missed_stack_caught  rf_fnr_given_fuzzers_and_value  stacking_fnr_given_fuzzers_and_value
  FIN             3703                     110                      21                        0.120173                              0.144207
  INT             2317                      70                      26                        0.075529                              0.094519
  REQ               32                       0                       0                        0.000000                              0.000000
  CON                9                       0                       0                        0.111111                              0.111111
  ACC                1                       0                       0                        0.000000                              0.000000
```

## Most frequent proto values among Fuzzers
```
proto  fuzzers_support  rf_caught_stack_missed  rf_missed_stack_caught  rf_fnr_given_fuzzers_and_value  stacking_fnr_given_fuzzers_and_value
  tcp             3713                     110                      21                        0.120119                              0.144088
  udp             1098                      70                      26                        0.159381                              0.199454
 unas              532                       0                       0                        0.000000                              0.000000
 ospf               69                       0                       0                        0.000000                              0.000000
  any               15                       0                       0                        0.000000                              0.000000
 sctp               12                       0                       0                        0.000000                              0.000000
 rsvp               10                       0                       0                        0.000000                              0.000000
  sep                7                       0                       0                        0.000000                              0.000000
```

## Most frequent sttl values among Fuzzers
```
sttl  fuzzers_support  rf_caught_stack_missed  rf_missed_stack_caught  rf_fnr_given_fuzzers_and_value  stacking_fnr_given_fuzzers_and_value
 254             6047                     180                      47                        0.102696                               0.12469
 255               14                       0                       0                        0.000000                               0.00000
  62                1                       0                       0                        0.000000                               0.00000
```

## Scientific interpretation boundary
- These subgroup associations do NOT establish that a feature causes a false negative.
- No model, threshold, feature subset or hyperparameter was modified after the official holdout.
- This analysis is an explanation of existing errors, not a new performance estimate.
- This binary detector's per-attack-category miss profile is NOT multiclass classification.

## Next
Send this output directory for independent verification and guided interpretation.
