# Author-authorized integrated PDF revision — RQ1–RQ5 (17 October 2026)

**Current decision:** five-chapter revised PDF successfully built and ready for author inspection, **NOT** P20 final closure, institutional release permission or scientific hypothesis validation. The user's submission rule is **one PDF only**; all evidence tables and RQ answers therefore appear **inside** chapters 1, 3, 4 and 5, not as an accompanying appendices-only submission.

## Preservation and provenance

- Earlier approved 37-page PDF file on author's submitted snapshot: `Bao_cao_NCKH_EnsembleLearning_5_chuong_09-SV-2026-CNTT2.pdf`, SHA-256 `8734ccdd5ef6a3495df55a0196bef2d71ae8d16f893fefd9882559a4c857218b`. Preserved unchanged.
- New TeX entry point: `report/main_revision_2026_10_17.tex` alongside untouched `report/main.tex`.
- Newly created chapter inputs: `report/chapters/revision_prior_work_2026_10_17.tex`, `methodology_revision_2026_10_17.tex`, `revision_rq_answers_2026_10_17.tex`, `validity_discussion_revision_2026_10_17.tex`, `conclusion_revision_2026_10_17.tex`. No original chapter files overwritten.
- Verified publisher article citation for closest prior art (Alsaffar et al., Journal of Big Data 11:133, 2024; DOI `10.1186/s40537-024-00994-7`) in `report/references_revision_2026_10_17.bib`. Total references in revised PDF: 13.
- Final source adjustment commit `d3d223051504bf1693a1965842dacdef48c9600b` adds deliberate section page break following print QA, preventing an explanatory sentence from being separated by a floating OOF table.
- Exact successful build `https://github.com/nphu0811/EnsembleLearning/actions/runs/38994119619`, job `Build NCKH five-chapter RQ revision PDF`, artifact `NCKH_EnsembleLearning_5Chapter_Revision_RQ1-RQ5_2026-10-17`. This build artifact is not a public official release.
- Final PDF bytes SHA-256 `828625f3dc6d21d9af0daa4cfa9e36b4cdc3a8128bfca66fa29467a28df58d3a`, file size 424,665 bytes; `45` physical A4 pages. The PDF was verified directly after downloading the exact CI artifact, not inferred from source alone.

## Evidence-grounded manuscript revisions

1. Related work table compares L06/L12/N02 and current project, clearly separates matched official holdout from random/merged-split experiments and states **NO novel algorithm** claim.
2. Methods give stable17 feature order and seed/stability rule, preprocessing categorical handling, TRAIN-vs-TEST chronology, exact conditional stratified paired bootstrap scope and limits; P15 reconstructs three separate full-TRAIN `joblib` in environment new to historical fit.
3. Chapter 4 now includes the **development OOF table** (RF, hard/soft Voting, Stacking on 42 features, Macro-F1, MCC, FPR, FNR), two pairwise-diversity statistics from frozen outputs, and detailed **RQ1–RQ5 answers**, including numerical comparisons, limitations and complete novel-vector table.
4. Chapter 5 integrates explicit RQ answers and replaces the prior 5-row evidence-only table with substantive result/limit statements. Historical P15 `full TRAIN not yet reconstructed` claim was corrected only **in revision**; original PDF and model results left intact.
5. **Scientific boundaries:** RQ1 repeated-training stability NOT established, RQ2 isolated causal feature-selection effect NOT established, RQ3 diversity mechanism NOT established, RQ4 novel-vector sensitivity ONLY within same TEST, RQ5 matched class-weight/resampling effect NOT established. No new fit, raw TEST read, bootstrap, model retuning, changed metric, frozen source edits or novel TEST selection.

## Actual QA results on final 45-page PDF

- XeLaTeX/BibTeX multi-pass build GitHub Actions **PASS**; no unresolved citations or LaTeX reference warnings in final `.log`; 13 references included.
- PDF `pdfinfo` and text extraction workflow **PASS**; text contains all five RQs, OOF/frozen numeric anchors, closest literature and rebuilt P15; no obsolete `bản tái dựng full TRAIN chưa thực hiện`.
- Local PyMuPDF PDF analysis: **45/45 pages readable**, no extracted text block bbox extending beyond page boundaries; sampled key pages 19–20, 33–36, 39–43 rendered and visually reviewed.
- One print issue identified during intermediate build: OOF development table floated above continuation of parent sentence across page 33/34. Fixed by nonfloating tables and a fresh page for section 4.7; rebuilt and visually verified section now begins intact at page 34.
- The inherited LaTeX source may still emit minor overfull hbox notices (21 warnings with a few-point excess) and prior P16 noted small labels / low-effective-resolution heatmap. Mechanical bbox QA does **not** prove all print-quality concerns are closed. Inspect printed PDF and correct if required by advisor; do not claim full P16 or P20 final closure based on a successful compile.

## Release distinction and follow-up

The author explicitly permitted creating a **new corrected five-chapter PDF**, keeping the approved historical version for provenance. The new PDF is the proposed single submission artifact, **pending author's visual/content review and final administrative approval**. The review's original 17 concerns (9 grouped) have not all been independently closed; some are addressed by manuscript evidence and require reviewer acceptance. P18 literature access/rights, P19 LICENSE/distribution rights and original-model provenance remain open independently. No model/dataset/private packet binary is included or pushed.

To rebuild locally from the repository after pulling: from `report/`, run XeLaTeX/BibTeX via `latexmk -xelatex -bibtex main_revision_2026_10_17.tex`. Never overwrite `report/main.tex` or the 37-page approved PDF. Download the build PDF from the successful GitHub Actions artifact or use the locally verified artifact copy.
