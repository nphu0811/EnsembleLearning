# NotebookLM 2026-10-19 review triage — evidence-led V4 revision

Reviewer input: user-uploaded NotebookLM text, scores 7.2/10 and "MAJOR REVISION"; 2 Critical + 3 Major + 2 Minor, original 5 mandatory edits. This is **automated reviewer feedback**, not proof of a real university committee decision. Page numbers refer to review's PDF version, not necessarily V4 after repagination.

| Comment | Review claim | Verified position / editorial decision |
|---|---|---|
| Critical 1: five FIT seeds share validation | Means/SD can be misread as 5 independent benchmark tests | VALID PRESENTATION RISK. Using one validation across five fixed FIT subsets is an intentional *paired conditional* study, not mathematically invalid SD. Name "SD theo FIT, validation cố định" in table and explain it cannot quantify new-network generalization; do NOT remove data or calculate invalid p-values. |
| Critical 2: feature selection cost | Historical RF17 fit 57.255s vs RF42 371.244s, but P21 selector+RF17 fit 309.850s vs RF42 fit 241.119s | VALID DIFFERENT COST UNITS. Give 3 distinct cost scenarios: historical fit-only (confounded RF hyperparams); P21 matched fit-only; P21 selector+fit. The +28.5% is measured only for selector+model fitting in P21, NOT total deployment end-to-end / production cost. Do NOT assert P21 inference speed benefit absent matched inference benchmark. |
| Major 1: old selection pre-CV | Reviewer calls historical development OOF Bảng 4.5 "RF17" biased | Historical stable17 selection was TRAIN-wide before CV: acknowledge and mark at the adjacent OOF table. However **the displayed pooled OOF table is explicitly 42-feature development**, not RF17 OOF; cannot falsely claim these specific 42-feature numbers were contaminated by stable17 selection. Qualify the risk for historic stable17 development results and complete historical selection protocol. |
| Major 2: missing FP/FN cost model | Historical Stacking reduces FP by 142, increases FN 118 | ADD deterministic cost-sensitivity table for normalized hypothetical ratio r=CFN/CFP in {1,5,10,50,100}. Stacking-RF loss = -142+118r, break-even 142/118 ≈1.2034. For r>threshold **RF42 has lower loss than historical Stacking42 only** (not universally optimal across all possible models). No real-world loss data assumed. |
| Major 3: novel-vector name misleading | Exact 42-feature overlap removal does not solve temporal/session dependence | RENAME user-facing manuscript "novel-vector view/subset" to "**exact-duplicate-filtered view**" while defining that duplicate means an *exact 42-predictor vector overlap*, not a full original record or session. Do not alter historical data, labels or TEST metric values. |
| Minor 1: overpacked attack-family Table 4.4 | 9x3 model cells have FN/FNR and Wilson CI small type | Separate main FN/FNR table from Wilson CI table with larger readable type. Do not delete CI values. Keep 9 attack families and three models unchanged. May shift table numbering; LaTeX refs by labels. |
| Minor 2: historical CPU/RAM undocumented | Cannot reproduce original 371.244s, 980.170s precisely | Add footnote immediately under historical cost table: process specs and parallelism not fully logged; do not invent multicore / CPU model or RAM. Distinguish author-host P21 resource settings. |

Five source-grounded mandatory edits: conditional SD header, cost narratives, hypothetical cost sensitivity, exact-vector terminology, and warning adjacent to historical OOF. No retraining or additional TEST reads authorized; source evidence is frozen author-verified P21 5/5 seed reports and historical P9 results.

## Corrections to the reviewer itself

- A common validation gives paired contrasts and conditional FIT-sampling variation; the limitation is *scope of inference*, not that sample SD is invalid.
- The claim "always RF42 optimal" must be restricted to comparing the two historical candidate confusion matrices at a fixed threshold with normalized cost.
- The review's "Feature Selection **only** saves inference" is not proven causally by the existing unmatched historic configs; matched P21 inference latency was not separately benchmarked. Historical batch inference metrics are descriptive only.
- Do not label the 42-feature development OOF table as RF17's biased OOF table if the table in the current manuscript contains only RF42/Voting/Stacking 42-track. The historical global stable17 leakage risk remains true separately.
- Statements about Fuzzers features, RF probability calibration or "production feasibility" require new diagnostics; preserve them as hypotheses, not measured conclusions.

## V4 verification gates

1. Copy versioned V3 to V4; preserve V3, P9, P15 and the five P21 seed reports byte-for-byte.
2. Verify every original FN/FNR/CI value in 9-family Table 4.4 remains after layout split.
3. Check all five chapter input files, table labels, references and bibliography, while preserving glossary after TOC.
4. Build PDF with XeLaTeX + BibTeX and block release on missing glyphs, citations, overfull boxes or missing P21 figures.
5. Render 4.4 and cost/conditional-SD pages for visual QA; numerical reviewer crosswalk with accurate new PDF pagination.

Status at issue: editorial response design — not by itself evidence PDF built.
