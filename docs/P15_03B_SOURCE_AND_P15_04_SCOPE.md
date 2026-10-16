# P15-03B: UNSW-NB15 source identity; P15-04 design audit scope

**Dataset:** UNSW-NB15, published by UNSW Canberra.

**Primary source:** https://research.unsw.edu.au/projects/unsw-nb15-dataset

**Using:** UNSW_NB15_training-set.csv (175,341 rows) and UNSW_NB15_testing-set.csv (82,332 rows), the published standard train/test split (not all 2,540,044 records).

**Local evidence:** P15-03A independently reported local SHA-256 matches vs earlier Phase 3 audit for training, testing, and feature-description CSVs. Those are internal checksums; actual historic download URL is not recorded.

**Research decision:** source identity and published standard split are confirmed; historic download URL remains UNKNOWN; no need to re-download files or modify data.

## P15-04 preliminary findings from historical source snapshot

1. Phase 9 reads official TRAIN/TEST, drops `id`, `label`, `attack_cat` from features, and fits frozen models using TRAIN features (source `src/models/run_unsw_phase9_final_holdout.py`, lines 222–232, 932–943, 991–1073).
2. Source sets random state 42 and stacking inner random state 137; Stage2 stability seeds = 11, 23, 42, 71, 101 (`run_unsw_phase9_final_holdout.py` lines 72–73; `select_unsw_features_stage2.py` lines 53–62).
3. sklearn preprocessing is nested in Pipeline; `StackingClassifier(cv=StratifiedKFold(...), stack_method='predict_proba')` constructs meta features without fitting on each inner validation row (`run_unsw_phase9_final_holdout.py` lines 270–325, 332–403, 466–509).
4. Phase 8 metadata states official_test_loaded=false. Phase 9 metadata holds the same three frozen candidate configurations as the Phase 8 manifest; decision thresholds all 0.5.
5. Caveat: Stable feature subset was selected on the full official TRAIN **before** development CV, not separately inside each development fold; CV estimates may be optimistic due to feature selection, even though the official test is distinct. This limitation must be disclosed.
6. Caveat: Shuffled stratified folds do not prove time/session independent generalization. Overlapping feature vectors across official train/test were already found in earlier audits. Do not claim leak-free temporal split.
7. Caveat: Meta model tuning uses OOF base predictions generated from the training set with base parameters chosen earlier on that train set. This is not fully nested selection. Saved development CV is not unbiased post-selection evidence.
8. Caveat: Static code and saved metadata are design evidence, not exact historical execution or original-training dependency provenance.

**Task Board:** P15-03A DONE; P15-03B DONE (dataset identity/source published; actual downloaded URL UNKNOWN); P15-04 static snapshot review DONE; P15-04 current project verification WAITING FOR USER OUTPUT.
