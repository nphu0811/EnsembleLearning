# NCKH IDS — Tiến độ kiểm toán sau ChatGPT tiếp quản (16/10/2026)

**GitHub base checkpoint:** `13cafe08cfb013bd4e765829f3ebf4add6bcd167` (Codex r05).  
**ChatGPT tiếp tục:** commits `f074df8bdc9ff141848751d83d7bb7491bd89a06` và `4e029b62f3778a75f5db68a8210b64592552504e` trên `main`.  
**Authoritative inputs:** `docs/ROADMAP_CURRENT.md`, `.research_memory/RESEARCH_CANON.md`, `.research_memory/r05/R05-ASSEMBLY-REVIEW.json`, `release/RELEASE_BLOCKERS.md`, frozen result CSVs. Đây là **supplementary current status**, không thay thế các lịch sử audit/checkpoint r01–r05.

## Progress theo canonical Phase 0–20

| Phase | Task (canonical) | State after review | Evidence / open gate |
|---|---|---|---|
| P00 | Research proposal | PARTIAL | r05 content + independent argument/form review có; tác giả/GVHD/admin và DOCX/PDF chưa có |
| P01 | Systematic literature review | PARTIAL | Literature/gap/reading notes; full screening/verification chưa đủ |
| P02 | Dataset selection | VERIFIED_REUSE_SCOPED | UNSW-NB15, raw train/test/features local SHA-256 audit, source identity; historical download URL chưa biết |
| P03 | Data audit and preprocessing | VERIFIED_REUSE_WITH_LIMITS | Audit/overlap evidence, no blanket leakage-free claim |
| P04 | EDA | VERIFIED_REUSE_SCOPED | EDA artifacts; publication-ready figures separately under P16 |
| P05 | Feature selection | PARTIAL_LIMITED_VALIDATION | Stable 17 features; selection trên full TRAIN trước development CV |
| P06 | Baseline models | VERIFIED_REUSE_WITH_LIMITS | Saved individual-model results and development CV; selection optimism |
| P07 | Ensemble learning | VERIFIED_REUSE_WITH_LIMITS | Diversity/OOF, voting negative results, Stacking; no superiority claim |
| P08 | Proposed ensemble framework | DOCUMENTATION_CLOSURE | `docs/research/ENSEMBLE_FRAMEWORK.md`, frozen specs |
| P09 | Imbalance strategy | PARTIAL | Class weight/resampling conclusions must remain bounded; no matched resampling experiment |
| P10 | Hyperparameter optimization | VERIFIED_REUSE_WITH_LIMITS | Saved tuning + frozen candidates; meta tuning not fully nested |
| P11 | Evaluation protocol | VERIFIED_REUSE_BINARY | Official n=82,332; historical closure 3 CSV byte-identical from clean aggregate replay |
| P12 | Validation & statistical test | VERIFIED_REUSE_WITH_LIMITS | Paired bootstrap CIs/McNemar; dependent-row and generalizability caveats |
| P13 | Ablation study | VERIFIED_REUSE_RETROSPECTIVE | Saved aggregate scope, not full factorial/isolated feature causal effect |
| P14 | Error analysis | VERIFIED_REUSE_DESCRIPTIVE | Saved detailed profiles and reconciliation; associations not causal |
| P15 | Reproducibility | PARTIAL | Raw hashes, protocol, postprocessing replay, R04 TRAIN-only smoke45/45; unknown original env; NO_GO full TRAIN model reconstruction |
| P16 | Scientific figures | IN_PROGRESS | Historical paired forest plot; r05 error tradeoff & frozen tables; two ChatGPT independent scoped audits below |
| P17 | Report writing | 40P_PDF_SCOPED_QA_PASS / FORM_NOT_APPROVED | Reference-inspired PTIT styling: 8 chapters, 40 physical A4 pages, 7 figures and 10 tables, 12 bibliography items; XeLaTeX/BibTeX build+independent visual/text/page-boundary QA PASS, 0 overfull/0 missing glyphs. Author/student IDs/adviser and institutional form approval remain OPEN. |
| P18 | Citation management | PARTIAL | 11/12 legacy metadata verified r04, U01 pages1–6 independently corroborated, U03 final 2019 vol5(4) corroborated; L03 page conflict disclosed with evidence favoring254–263, VOR PDF check open; final complete bibliography pending |
| P19 | Data availability | IN_PROGRESS | Public GitHub repository confirmed; raw data not tracked; source/derived tables available; no root LICENSE or final model artifact; privacy/release/version/rights checks open |
| P20 | Final review | TODO | G0–G6, completeness, rendered reports, inference demo and scientific limitations not all closed |

**Không đếm VERIFIED_REUSE hoặc DONE_SCOPED như đầy đủ mọi gate của một phase.** Phase order/IDs không được đổi.

## Kết quả ChatGPT tiếp quản — evidence trực tiếp

**P16-R05 tables / FP-FN figure:**
- `docs/research/P16_R05_INDEPENDENT_AUDIT_2026-10-16.md`
- **141/141** fresh independent numeric/source assertions PASS.
- **14/14** fresh SVG structure assertions PASS; PNG visually previewed.
- Signed FP−142/FN+118, figure 120×65mm; no numeric differences from frozen CSV.
- Independent PDF glyph/render check **NOT PERFORMED**. Historical source preflight's 3048mm width WARN is inconsistent with actual 120mm SVG geometry; preserve warning, no silent overwrite.

**P16 paired forest plot:**
- `docs/research/P16_FOREST_INDEPENDENT_AUDIT_2026-10-16.md`
- **79/79** fresh independent CSV/SVG checks PASS; PNG visually previewed; frame183×100mm.
- Four correctly selected paired effect rows, all CI fields match frozen source; Macro-F1/MCC CI span zero, FPR negative, FNR positive.
- Codex's historical PDF text/collision PASS was **read from saved report, not independently rerun**.

**Scientific conclusion remains frozen:** Stacking-42 vs RF-42 ΔMacro-F1≈+0.000497 with CI spanning zero; 142 fewer FP and 118 more FN on official TEST; RF17 is pipeline-level cost/performance trade-off, not isolated feature effect. Threshold=0.5 and all candidate configurations remain unchanged.

## Next highest-priority unblocked tasks

1. **P16 remaining release QA:** check vector/PDF font and glyphs and final report page render, complete figure/table inventory and source/caption map. Without available binary renderer/TeX tool, keep specific QA BLOCKED and work on source assets. Do not mark full P16 DONE.
2. **P17 source writing:** assemble an evidence-grounded IDS report from preserved template, avoiding old Android example text; references/tables tied to frozen evidence. Build/render QA later.
3. **P18 citation closure:** resolve L03 from authoritative publisher/source without guessing pagination; U01/U03 source warnings; final bibliography consistency.
4. **P15 reconstruction:** plan remains NO_GO (RAM headroom/runner); do not run full model training unless resource/overwrite gates pass. No original training environment claim; smoke models are not final models.
5. **P00/administrative:** use r05 internal content draft; cannot fill identity/signature/applicability without human confirmation. DOCX/PDF and print QA still open.
6. **P19/P20/defense:** release/license safety, actual validated full model for inference demo, slides/rehearsal, final acceptance gates.

**Integrity/safety:** These takeover commits add only scoped verification documentation. No raw data, official TEST, frozen metrics/configs/predictions, models, templates, original sources or pre-existing checkpoint files were modified. Persistent r05 STATE/HANDOFF has not been rewritten in this limited documentation-only takeover; use this report plus r05 memory as the future handoff, and refresh the memory manifest in a controlled verified next checkpoint rather than partially editing hash-tracked files.

## Bổ sung ChatGPT source-writing / citation / availability — 16/10/2026

- **P17 new working manuscript:** `report/main.tex`, `report/chapters/{introduction,related_work,methodology,results_discussion,conclusion}.tex`, `report/references_verified.bib`, `report/references_dataset_checked.bib`. Both P16 saved PDFs are linked in results chapter by relative paths. `report/README.md` and `report/BUILD.md` specify correct scope.
- **Independent read-only cross-file audit (after additions): 78/78 PASS**: 5 input chapters, 12 BibTeX keys / 12 cited, no duplicate labels, all LaTeX `\\ref` keys resolved, balanced audited environment tokens, P16 figures' PDFs tracked, official dataset source cited. These checks do NOT prove compilation/render; this remains the next P17 gate. Preflight XeLaTeX minimal separate Vietnamese document built in container, **not the actual report**.
- **P18:** `literature/L03_PAGE_CONFLICT_FOLLOWUP_2026-10-16.md`, `literature/UNSW_U01_U03_METADATA_FOLLOWUP_2026-10-16.md`: L03 publisher-final PDF unchecked; U01 bibliographic page evidence stronger; U03 final 2019 issue corroborated. No silent mutation of original ledger.
- **P19:** `docs/research/DATA_CODE_AVAILABILITY_PUBLIC_UPDATE_2026-10-16.md`: repository now public, but missing root license, raw dataset not committed, SMOKE_ONLY models must not be mistaken for full TRAIN models.
- **Cleanup scope:** strictly advice only per user. No deletion, moving, untracking or history rewriting performed.
- **Next safe work:** run actual XeLaTeX/BibTeX for working report and visually QA pages/figures; align with preserved original institutional template without inventing admin fields; continue resolving remaining citation and release gates. P15 fullTRAIN reconstruction still NO_GO, no retuning official TEST.

## P17 production-style PDF build/QA checkpoint (2026-10-16)

- Reproducible CI workflow: `.github/workflows/p17-latex.yml`, user desktop does not need XeLaTeX; XeLaTeX+BibTeX executed in GitHub Action TeX Live container.
- Baseline run: https://github.com/nphu0811/EnsembleLearning/actions/runs/38900247221 (22 A4 pages, compile PASS; 16 overfull hbox warnings, max170.67429pt, 4 PDF text blocks outside page safe x-boundary; 12 BibTeX records).
- Layout fix commit: `cb556fc8d5b587708e747afce0d3024a482833c1` (`xurl` + `\\path{}` and emergency stretch; 5 TeX source files; no scientific numbers altered).
- Rerun: https://github.com/nphu0811/EnsembleLearning/actions/runs/38901027329 (XeLaTeX/BibTeX build PASS, 22 A4 pages, no missing characters, **0 overfull**, 4 underfull minor warnings, **0 text bounding-box boundary outliers**; 12 bibliography entries and expected model statistics present). Inspection used actual PDF artifact from CI, `fitz` text and page geometry, 22-page contact sheet plus close-up four relevant pages.
- Formal scoped QA record: `report/P17_PDF_QA_2026-10-16.md`. New workflow gate blocks future Overfull/Missing glyph, not merely compilation failure.
- **Scope:** technically rendered standalone working report, not original institutional template with admin data, no claim P17 full DONE or release G4 final acceptance. Original training model/environment not reproduced; P15 still PARTIAL.

## P18 compiled-report reference QA (2026-10-16)

`docs/research/P18_REPORT_BIBLIOGRAPHY_QA_2026-10-16.md` records real BibTeX output: 12/12 distinct citations/bibitems, 12 unique DOIs, 0 missing/uncited/duplicate keys, no final BibTeX or LaTeX undefined citation warnings. Status **DONE_SCOPED_REPORT_BIBLIOGRAPHY**, not full P18: L03 disputed pagination and non-exhaustive/full-text literature remain OPEN. No changed scientific result or bibliography source values.

## P17 reformatted to 40 pages using sample report as layout reference (2026-10-16)

User-provided `Bao_cao_NetFlow.pdf` inspected as a **64-page structural/visual reference only**. Current report has 8 evidence-bounded chapters, PTIT original logo (no third-party identity reused), double cover frame, carmine-linked TOC, blue accents, 4 original Phase4 EDA figures, 2 P16 figures, and OOF conceptual diagram. XeLaTeX CI run 38907313697 on commit `13f310f975fc2405abbf35bd433b35021f630367` returned 40 A4 pages with 0 overfull, 0 missing glyph, 12 bibliography entries and no out-of-page text. See `report/P17_PTIT_40PAGE_QA_2026-10-16.md`. This supersedes the 22-page *design status* only; preserved historical audit values remain valid for their old artifact. P17 still PARTIAL: administrative names, approved template/signature, P18 total and P20 final approval remain OPEN.
