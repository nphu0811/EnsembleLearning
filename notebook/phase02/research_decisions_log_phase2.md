# Research Decisions Log — v0.1

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Do not define novelty as “apply ensemble to dataset X.” | Similar ensemble + FS designs already exist. | Recent peer-reviewed NIDS studies identified in Phase-0 scoping. | Phase 1 must search for defensible methodological or model-design gaps. |
| Treat leakage-safe evaluation as a core design axis. | A model score is not useful if train/test separation does not reflect the data-generation process. | Methodological principle; NIDS-specific evidence pending Phase 1. | Dataset selection must preserve timestamps/day/scenario metadata where possible. |
| Keep RQs preliminary until Phase 1. | Nature proposal workflow requires evidence before strengthening claims. | `nature-proposal-writer` compose-mode. | RQs may be changed after literature synthesis. |
| Do not default to SMOTE. | Synthetic oversampling may change traffic-feature relationships and is dataset-dependent. | To be evaluated in Phase 9 literature/experiments. | Include no-resampling and class-weight baselines. |
| Use minority-sensitive + efficiency metrics in addition to accuracy. | NIDS classes may be imbalanced and computational cost matters. | Recent class-imbalance/feature-selection literature. | Macro-F1, MCC, PR-AUC/FPR/FNR and runtime become planned outputs. |

## Phase-1 updates

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Do not claim FS + ensemble as novelty. | Multiple 2020–2025 studies already combine them. | L04–L08, L12 | Novelty must come from evaluation/design question. |
| Elevate dataset validity/leakage to a core research axis. | Peer-reviewed work documents creation/label/flow errors in CIC datasets. | L02–L03 | Phase 2/3 must audit raw benchmark structure before training. |
| Keep diversity-guided ensemble as a candidate, not a claimed novelty. | Literature uses heterogeneous ensembles; explicit error-diversity-guided selection still needs fuller search. | L01, L06 | Search this axis further before freezing RQ3. |
| Treat minority performance separately from global accuracy. | Ensemble papers still report weaknesses on rare classes; imbalance-specific ensembles exist. | L06–L07 | Macro-F1, per-class recall, FPR/FNR and MCC remain mandatory. |
| Cross-dataset generalization is important but optional for core scope. | Strong 2024 evidence shows within-dataset scores can fail cross-dataset. | L09 | Use as motivation; decide feasibility after dataset selection. |

## Phase-2 updates

| Decision | Reason | Evidence | Consequence |
|---|---|---|---|
| Select UNSW-NB15 as primary benchmark. | Official compact train/test partition makes the full experiment matrix feasible while retaining 9 contemporary attack families and 49 described features. | UNSW official dataset page. | Full FS/ensemble/tuning/statistics pipeline runs here first. |
| Select corrected CICIDS2017 as secondary validation benchmark. | Five-day attack schedule, severe class imbalance and documented corrections make it useful for robustness/split analysis. | UNB official CICIDS2017 page + Engelen et al. corrected release. | Only shortlisted models/pipelines are replicated here initially. |
| Do not use original CICIDS2017 blindly. | Published work documents flow-construction/feature/label problems and provides regenerated corrected data. | Engelen et al. 2021 research release. | Dataset version becomes part of experiment metadata. |
| Defer CSE-CIC-IDS2018. | ~16.2M flows makes repeated FS/tuning/CV expensive for one-person research. | Official UNB page and published dataset statistics. | Can be added only if compute/time remains or supervisor requests it. |
| Exclude NSL-KDD from core evidence. | Small and easy but derived from old KDD'99 traffic. | Literature + historical provenance. | May appear only as historical benchmark in related work. |
