# Phase 14 — Step 3: Normal-error feature profiles

Status: DESCRIPTIVE diagnostic on frozen predictions, not causal inference.

## Controls checked
- Official test / prediction join by unique `id`: PASS.
- `label` and `attack_cat` agree on every matched id: PASS.
- Both models' confusion matrices exactly match locked Phase 9/11: PASS.
- Normal error groups: 26,719 both correct; 420 Stacking-only correct;
  278 RF-only correct; 9,583 both wrong.

## How to read these profiles
- `*_group_composition.csv` contains P(feature value | error group).
- `*_by_value.csv` contains model FP rates given NORMAL + feature value.
- These conditionals have DIFFERENT denominators; do not interchange them.
- A feature's association with errors does NOT imply it caused those errors.
- Rare feature values have unstable rates: inspect `normal_support`.

## Most frequent `state` among Normal traffic (up to 10)
```
state  normal_support  stack_correct_rf_wrong  rf_correct_stack_wrong  rf_fp_rate_given_normal_and_value  stack_fp_rate_given_normal_and_value
  FIN           24172                     327                     200                           0.297493                              0.292239
  CON            6633                       2                       0                           0.000603                              0.000302
  INT            4485                      90                      78                           0.622520                              0.619844
  REQ            1707                       0                       0                           0.008787                              0.008787
  ACC               2                       0                       0                           0.000000                              0.000000
  RST               1                       1                       0                           1.000000                              0.000000
```

## Most frequent `proto` among Normal traffic (up to 10)
```
proto  normal_support  stack_correct_rf_wrong  rf_correct_stack_wrong  rf_fp_rate_given_normal_and_value  stack_fp_rate_given_normal_and_value
  tcp           27848                     330                     200                           0.258403                              0.253735
  udp            8097                      90                      78                           0.346672                              0.345190
  arp             987                       0                       0                           0.000000                              0.000000
 ospf              38                       0                       0                           0.000000                              0.000000
 igmp              30                       0                       0                           0.000000                              0.000000
```

## `sttl` median and IQR by group
```
                 group  support  sttl_q1  sttl_median  sttl_q3
            ALL_NORMAL    37000     31.0         62.0    254.0
          both_correct    26719     31.0         31.0     62.0
stack_correct_rf_wrong      420    254.0        254.0    254.0
rf_correct_stack_wrong      278    254.0        254.0    254.0
            both_wrong     9583    254.0        254.0    254.0
```

## Most common exact `sttl` values among Normal traffic
```
sttl  normal_support  stack_correct_rf_wrong  rf_correct_stack_wrong
  31           16702                       0                       0
 254           15049                     401                     217
  62            4129                      19                      61
   0             987                       0                       0
  29              50                       0                       0
   1              38                       0                       0
  60              24                       0                       0
  32              19                       0                       0
  30               2                       0                       0
```

## FIN: distinguish reversed conditional probabilities
- Among all 37,000 Normal rows, 24,172 have state=FIN.
- Among Normal state=FIN rows, Stacking has FP rate 29.224%.
- The share of FIN in the 420 Stacking-correct/RF-wrong group is in
  `state_group_composition.csv` — a different conditional probability.

## Scientific boundaries
- No model refitting or post-test selection; these are diagnostic hypotheses only.
- This step looks at Normal traffic (false alarms), not Fuzzers false negatives.
- State/proto/sttl distributions may be confounded by other traffic properties.
- A high conditional correctness on one subgroup does not prove broad deployment performance.

## Next checkpoint
Share this output folder for independent checking. After interpretation,
continue to Attack/Fuzzers error profiles, still without modifying models.
