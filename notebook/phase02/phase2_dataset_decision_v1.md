# PHASE 2 — Dataset Selection Decision v1.0

## Decision

### Primary dataset
**UNSW-NB15**

Use the official predefined training/testing partition for the main experimental matrix:
- Train: 175,341 records
- Test: 82,332 records
- 49 features including the class label in the official description
- 9 attack families

Purpose:
- full data audit
- feature-selection comparison
- baseline models
- voting/stacking/bagging/boosting
- imbalance experiments
- tuning
- repeated/statistical comparisons
- ablation

### Secondary validation dataset
**Improved / corrected CICIDS2017**, preferably the regenerated version from Engelen, Rimmer & Joosen rather than blindly using the original MachineLearningCSV.

Purpose:
- validate selected final models/pipelines on a second benchmark
- inspect class imbalance and rare attacks
- study split sensitivity / day-aware or scenario-aware evaluation where feasible
- check whether conclusions from UNSW-NB15 survive on a structurally different dataset

### Not selected as core
- **NSL-KDD**: computationally convenient but old and derived from KDD'99; useful only as historical benchmark if needed.
- **CSE-CIC-IDS2018**: highly relevant but ~16.2M flow records; too expensive for the full Phase-5→12 experimental matrix at this stage.
- **ToN-IoT**: valuable newer heterogeneous IoT/IIoT benchmark, but changes the application domain toward IoT/IIoT; reserve for future/extension work.
- **BCCC-CSE-CIC-IDS2018**: enhanced 2025 dataset with 46M records and 300 features; scientifically interesting but computationally excessive for the core student project.

## Why this two-dataset design?

The primary dataset should make exhaustive and reproducible experimentation feasible.
The secondary dataset should test whether the selected conclusions depend on one benchmark.

This is **multi-dataset validation**, not cross-dataset transfer: models will be trained and tested independently on each dataset because their feature schemas differ.

## Data provenance / availability status

| Dataset | Route | Source | Notes |
|---|---|---|---|
| UNSW-NB15 | reused public source | UNSW Canberra | Official raw/CSV files and predefined train/test partition are available |
| CICIDS2017 | reused public source | Canadian Institute for Cybersecurity, UNB | Official PCAP/CSV public release; citation requested |
| Improved CICIDS2017 | reused public research release | Engelen/Rimmer/Joosen research site | Regenerated flows with corrected CICFlowMeter behavior and improved labels |
| CSE-CIC-IDS2018 | reused public source | CIC/UNB via AWS | Redistributable with citation; very large |
| ToN-IoT | reused public source | UNSW Canberra | Heterogeneous IoT/IIoT, OS and network data |

## Scientific caveats

1. Do not merge predefined train and test files and randomly resplit UNSW-NB15 as the only evaluation.
2. Do not use the CICIDS2017 original CSVs without auditing duplicates, non-finite values, labels and feature-generation artifacts.
3. Preprocessing, feature selection and resampling are fitted on training data only.
4. A second dataset is optional until the primary experiment is stable; it must not delay the core study.
