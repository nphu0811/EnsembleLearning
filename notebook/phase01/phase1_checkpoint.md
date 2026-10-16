# PHASE 1 CHECKPOINT

## Completed

- Loaded and followed `nature-academic-search` multi-source-search workflow.
- Built Boolean concept groups around NIDS, ensemble learning, feature selection, imbalance, dataset validity, generalization and splitting.
- Performed broad and targeted literature retrieval across publisher/academic sources.
- Deduplicated the key corpus using DOI/title identity.
- Used `nature-reader` grounding workflow for high-value accessible papers/materials.
- Built a literature evidence matrix.
- Built a research gap matrix.
- Updated research decisions.
- Froze primary RQs v1.0.

## Main scientific findings

1. Ensemble learning for IDS is already mature; stacking/voting/bagging/boosting are not novel by themselves.
2. Feature selection + ensemble is already well represented in the literature.
3. Class imbalance remains unresolved, especially for rare attacks.
4. CIC-IDS2017/CSE-CIC-IDS2018 have documented dataset-generation, feature-generation and labeling issues.
5. Cross-dataset studies show that near-perfect within-dataset performance may fail badly under distribution shift.
6. Therefore the project should emphasize trustworthy evaluation and explaining ensemble gains, not maximizing one accuracy number.

## Still unresolved

- Which dataset best supports the frozen RQs?
- Which split(s) are feasible and scientifically defensible for that dataset?
- Whether binary, multiclass, or a staged evaluation will be the core task.
- Final baseline and ensemble model set.
- Which feature-selection methods will be kept after feasibility analysis.

## Exact next step

PHASE 2 — compare candidate NIDS datasets and select the dataset(s) that can actually answer RQ1–RQ4 under student-level compute constraints.
