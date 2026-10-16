# Research Task Board

Checkpoint hiện hành r03: `docs/RESUME_AUDIT_R03_2026-10-16.md`. Prior manifest146/148 khớp (2 stale memory hashes), historical preservation282/282. DOCX count được đính chính8 bảng. Các hàng r01/r02 dưới đây giữ evidence lịch sử; cập nhật mới ưu tiên:

| ID | Task | Status | Evidence | Gate |
|---|---|---|---|---|
| BOOT-R03 | Resume inventory/template/registry reconciliation | DONE_SCOPED | resume_2026_10_16_r03/resume_audit.json | Drift explained;282/282 preserved;ZIP/DOCX CRC PASS;6/6 unit tests |
| P18-FIELD-R03 | Crosscheck8 pending legacy records | DONE_SCOPED | literature/resume_r03_2026_10_16/FIELD_CROSSCHECKS.md; validation.json |2 newly verified,6/12 total verified;6 legacy +U01/U03 pending;18/18 bookkeeping checks |
| PROP-PRODUCTS-R03 | Nhu cầu/sản phẩm/chất lượng/tiến độ/kinh phí | DONE_SCOPED | drafts/sections/ung_dung_san_pham_tien_do_r03.md; qa_logs/r03_products_section_review.md | Independent review7.75;P2 repairs/source checks;no rescore/full-proposal/DOCX/render |

| ID | Task | Status | Evidence | Gate |
|---|---|---|---|---|
| BOOT-01 | Inventory workspace and existing artifacts | DONE | resume_2026_10_16/bootstrap/workspace_inventory.csv; p15_01_inventory.json | PASS presence scope |
| BOOT-02 | Audit and preserve original templates | DONE | templates/original/; template_audit.json; TEMPLATE_REQUIREMENTS_MATRIX.md | PASS structural; visual pending |
| BOOT-03 | Discover and load relevant Nature Skills | DONE | nature_skill_registry.csv; SKILL_USAGE_LOG.md | PASS actual usage recorded |
| BOOT-04 | Reconcile phase state | DONE | docs/RESUME_AUDIT.md; ROADMAP_CURRENT.md | PASS bounded audit |
| P15-R1 | Current raw and protocol checks | DONE | p15_03_dataset.json; protocol/ | PASS with protocol caveats |
| P15-R2 | Replay aggregate reporting in fresh stdlib venv | DONE | clean_replay_report.json; 3 identical CSVs | PASS, no ML replay claim |
| P08-DOC | Document locked framework | DONE | docs/research/ENSEMBLE_FRAMEWORK.md | PASS source/freeze matching |
| PROP-FOUND | Restore proposal foundation | DONE_SCOPED | proposal/researchwrite/nckh-ids/00–07; qa_logs/foundation_review_r02.md | Both rechecks >7.5 for bounded drafting; final scientific/admin gates open |
| P19-DRAFT | Data/code availability and FAIR audit | DONE scoped draft | docs/research/DATA_CODE_AVAILABILITY.md | PARTIAL release rights/identifier |
| P16-F1 | Paired-effect forest plot | DONE | results/figures/p16_paired_effects_2026_10_16/ | Figure QA PASS, P16 not complete |
| P18-UNSW | Verify foundational dataset references | PARTIAL | literature/verification_2026_10_16/: ledger, raw Crossref, BibTeX | 3 VERIFIED_METADATA; 2 CHECK_SUGGESTED; no full-text claim |
| P18-LEGACY | Reconcile12 legacy reference identities | DONE_SCOPED | literature/resume_r02_2026_10_16/validation.json, ledger/BibTeX |12 DOI resolved,4 metadata verified;8 field crosschecks pending |
| P01-DOMESTIC | Establish bounded domestic context | DONE_SCOPED | DOMESTIC_SOURCES.md and READING_NOTES.md |2 primary institutional topic sources; detailed comparison partial |
| PROP-SECTION | Draft objectives/content/methods | DONE_SCOPED | Partial draft + qa_logs/r02_section_review.md, r02_section_repair_validation.json |7.5 KEEP_INTERNAL_DRAFT; minor edits applied; no full proposal/DOCX claim |
| P16-REST | QA remaining evidence figures/tables | TODO | Existing drafts require explicit contracts | NOT_RUN |
| P15-ML | Clean ML reproduction / model artifact | TODO | Current original env UNKNOWN | NOT_RUN; isolated run plan required |
| PROP-DOCX | Fill original DOCX + render | BLOCKED tool/content | Original located, preserved | Runtime loader unavailable; verified literature/admin pending |
| REPORT | IDS LaTeX report + PDF | DONE_SCOPED_PDF_BUILD_QA | `report/main.tex`; `report/P17_PDF_QA_2026-10-16.md`; Actions 38901027329; commit cb556fc | G4 technical XeLaTeX/BibTeX+render QA PASS; institutional template/admin/final release gates OPEN |
| DEFENSE-QA | Prepare evidence-grounded council questions | DONE_SCOPED | defense/Hoi_dap_hoi_dong.md; qa_validation_r02.json |20 questions,33 paths checked; DRAFT_FOR_REVIEW |
| DEFENSE | Slides, script, inference demo and final rehearsal | TODO | MASTER requirements | Depends on evidence/report/model; Q&A draft exists |
| RELEASE | G0–G6 and final checksum package | BLOCKED | release/RELEASE_BLOCKERS.md | NOT_READY_FOR_SUBMISSION |

Paths beginning resume_2026_10_16 are under results/reproducibility/. Contract for each scientific task is in the linked artifact or P16_PAIRED_EFFECT_CONTRACT.md. Preserve all historical completed experiment outputs; do not rerun fitting merely to update status.

## r04 R04-RESUME

DONE_SCOPED — 174/174 prior artifact hashes and282/282 historical files match; ZIP15 entries and DOCX8 tables CRC PASS; skills registry inspected

Evidence: `.research_memory/r04/R04-RESUME.json`.

## r04 R04-REF

DONE_SCOPED — Five of six pending legacy entries resolved;11/12 metadata verified; L03 retained CHECK_SUGGESTED page conflict; U01/U03 open;28/28 bookkeeping checks PASS; no full P18 completion

Evidence: `.research_memory/r04/R04-REF.json`.

## r04 R04-READ

DONE_SCOPED — Five source-linked claims anchored to actual passages;10/10 capture checks PASS;L06 selected Methods,L09 indexed Introduction,D01/D02 bounded domestic sources;no full-paper read claim

Evidence: `.research_memory/r04/R04-READ.json`.

## r04 R04-FORM-AUDIT

DONE_SCOPED — Original DOCX58 blocks/97 cells captured;14/14 coverage checks PASS;working gap draft also checkpointed pending review repairs;no fill/render/admin approval

Evidence: `.research_memory/r04/R04-FORM-AUDIT.json`.

## r04 R04-GAP-LIT

DONE_SCOPED — Updated gap matrix and related-work/rationale draft;30/30 source/RQ checks and3/3 repair checks PASS;two independent scoped reviews with minor repairs;not full proposal/P01/P18 closure

Evidence: `.research_memory/r04/R04-GAP-LIT.json`.

## r04 R04-SMOKE-PLAN

DONE_SCOPED — Capacity and frozen source paths inspected;bounded2000/500 TRAIN-only smoke contract and observed-version requirements saved;no fit or original-environment claim yet

Evidence: `.research_memory/r04/R04-SMOKE-PLAN.json`.

## r04 R04-ASSEMBLY

PARTIAL — All proposal content assembled in original field order;10/10 initial checks,6/6 P2 repair checks;one evidence review saved;independent full argument review interrupted by usage limit;not DOCX/render/full gate

Evidence: `.research_memory/r04/R04-ASSEMBLY.json`.

## r04 R04-ML-SMOKE

DONE_SCOPED — Fresh venv pip check PASS;TRAIN-only three frozen builders fit/serialize/reload;initial41/42 failed bitwise RF17 assertion,diagnosed2.22e-16 parallel-sum drift;repaired45/45 PASS and6/6 audit tests;not final models/G3 closure

Evidence: `.research_memory/r04/R04-ML-SMOKE.json`.

## r04 R04-DEFENSE-CONTENT

DONE_SCOPED — Drafted12-position720-second defense script,evidence walkthrough/final inference dependency runbook and G0-G6 checklist;source/timing validation PASS;not slides/render/rehearsal or live demo

Evidence: `.research_memory/r04/R04-DEFENSE-CONTENT.json`.

## r04 R04-FINAL-CHECKPOINT

PARTIAL — r04 advanced references11/12,gap/relatedwork,full content mapping and assembly,TRAIN-only software smoke45/45,defense content25/25;full argument review interrupted by quota;G0-G6 remain open;no final release

Evidence: `.research_memory/r04/R04-FINAL-CHECKPOINT.json`.

## r05 R05-ASSEMBLY-REVIEW

DONE_SCOPED — Independent full argument/form review and recheck saved;3P1/2P2 addressed in separate r05 draft;34/34 source-boundary checks;author/renderP0 open;no training or release closure

Evidence: `.research_memory/r05/R05-ASSEMBLY-REVIEW.json`.

## P17 2026-10-16 continuation checkpoint

- REPORT source = 5 chapters + main entry; 12 BibTeX sources; 2 P16 figures linked; exact frozen performance numbers unchanged.
- GitHub Actions 38900247221 (first SUCCESS but 16 Overfull); patch cb556fc; run 38901027329 SUCCESS, 0 Overfull, 0 missing glyph, 22 A4 pages. Independent extracted-PDF QA at `report/P17_PDF_QA_2026-10-16.md`.
- G4 technical build/layout = DONE_SCOPED; P17 full = PARTIAL pending administrative form and institutional signoff. No final model/fullTRAIN reproduction and no source data cleanup performed.

## P18 report bibliography closure checkpoint (2026-10-16)

- `P18-REPORT-BIB-QA = DONE_SCOPED`: independently checked all 12 cited keys against report sources, 12 distinct DOI entries and actual XeLaTeX/BibTeX `main.bbl` output; zero duplicate/unresolved/uncited, 0 warnings. See `docs/research/P18_REPORT_BIBLIOGRAPHY_QA_2026-10-16.md`.
- P18 overall PARTIAL because L03 VOR page conflict, varying reading scopes and no exhaustive systematic search. P17 technical PDF QA scoped PASS, institutional final signoff pending.
