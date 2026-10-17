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
| P15-ML | Full TRAIN artifact reconstruction (bounded local, 3 frozen candidates) | DONE_SCOPED_RECONSTRUCTION | 3 author full-run PASS + 69/69 actual local artifact verifier checks; docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md | Historical original env UNKNOWN; reviewer binary load & G3 release/demo separately OPEN; no TEST re-evaluation |
| PROP-DOCX | Fill original DOCX + render | BLOCKED tool/content | Original located, preserved | Runtime loader unavailable; verified literature/admin pending |
| REPORT | IDS LaTeX report + PDF | DONE_SCOPED_5CH_37P_BUILD | `report/main.tex`; `docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md`; run 38916942038 | 5 chapters / 37 pages, abstract removed, acronym glossary after TOC; all source/code-internal references absent from PDF; CI PASS; institutional signoff and signatures OPEN |
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

## P17 user-supplied NetFlow form reference — scoped closure (2026-10-16)

- `P17-PTIT-STYLE-40P = DONE_SCOPED`: referenced the uploaded 64-page NetFlow report for page types/style only; 8 chapters, 40 physical A4 pages, 7 figures, 10 tables, 12 bibliography entries; actual GitHub Actions TeX artifact QA verified no overfull/missing character/out-of-bounds text. Evidence `report/P17_PTIT_40PAGE_QA_2026-10-16.md`; associated source commit `13f310f975fc2405abbf35bd433b35021f630367`.
- G5 admin info, signoff and exact institutional form acceptance remain PENDING_HUMAN. No model retraining, no frozen result edits, no cleanup or identity copying.

## P17 báo cáo 5 chương — phiên bản hiện hành (16/10/2026)

- User requested structure aligned with uploaded NetFlow 5-chapter reference, while preserving original Ensemble Learning experiments. Source assembled into 5 top-level chapters; chapter fragments remain as sections and retain historic content not copied from example.
- Removed abstract; placed substantive acronym table after table of contents. User-visible PDF has no `notebook/`, `results/`, `.md`, `.json`, `SMOKE_ONLY` project text; training process and results remain described.
- GitHub Actions `38916942038` PASS; PDF **37 A4 pages**, 12 bibitems, no duplicate labels, 0 Overfull or missing glyph; scope evidence `docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md`.
- Native Nature Skills only present in user Windows Codex environment; ChatGPT did not load/execute `nature-writing`. Academic source-grounded revision and PDF postflight performed instead.
- P17 remains PARTIAL overall due to approval, actual signatures and other release gates. No retraining or official TEST revisions.

## P15 — GitHub read-only full-TRAIN preflight (16/10/2026)

- `P15-FULLTRAIN-PREFLIGHT = DONE_SCOPED_CODE`: files `tools/p15_fulltrain_preflight.py`, `tests/test_p15_fulltrain_preflight.py` and `docs/research/P15_FULLTRAIN_PREFLIGHT_README.md` pushed to `main` (commit `c64f06e2f7be97a05cf9e5969a2f1679126dd5e4`). Six fixture tests passed in a separate Python runtime; remote paths and content verified by GitHub fetch.
- No Windows/dataset-local preflight or full-TRAIN fitting has been run; the previous environment/capacity NO_GO and G3/P15 PARTIAL remain. Script never reads official TEST/trains and `training_authorized=false` by construction. No raw data/frozen result/script P9 modified.
- Next: after `git pull --ff-only origin main` run the new unit tests and the read-only preflight from repo root, inspect JSON, then design/review the isolated watchdog runner before any full TRAIN operation.

## 16/10/2026 — P15 Windows preflight (author-reported)

- **P15-WINDOWS-PREFLIGHT = DONE_SCOPED_USER_EVIDENCE:** Author ran six fixture unit tests (6/6 PASS) and a read-only preflight (11/12 PASS); evidence recorded in `docs/research/P15_LOCAL_PREFLIGHT_USER_RUN_2026-10-16.md`. This is reported console output, not an independent runner execution.
- **RAM gate FAILED:** available 2,157,973,504 bytes (~2.01 GiB) vs conservative 9-GiB threshold. Other 11 gates pass, including hashes, schema, versions, tracked Git cleanliness and disk. `training_authorized=false`, `reconstruction_status=NOT_RUN`. **G3/P15 still PARTIAL; no full-TRAIN fitting.**
- Next: do not try fitting or bypass memory guard. Continue independent P16/P18 tasks until a proper host and reviewed watchdog runner exist; then re-check on the execution host. Existing published 5-chapter PDF remains unchanged.

## P16 — Independent current 5-chapter PDF/figure audit (16/10/2026)

- **P16-PDF-37P-INDEPENDENT-QA = DONE_SCOPED**. Evidence `docs/research/P16_FIVE_CHAPTER_PDF_RENDERED_INDEPENDENT_QA_2026-10-16.md`. User-supplied PDF verified 37 A4 pages / 0 nonempty text spans out of page; rendered representative 10 pages; figure and results-table placement checked. Frozen CSV and P16 figure sources independently crosschecked: **49/49 PASS**, 0 fail, no new fit/TEST evaluation.
- **Warnings remain:** plotted labels on pages 20/22/29 smaller than 8 pt; heatmap page 22 at ~118 effective dpi; no 300 dpi print certificate. PDF preserved unchanged, no chart regeneration. Canonical **P16 IN_PROGRESS**; P15/G3 unchanged (RAM NO_GO).
- Next: decide standalone higher-resolution heatmap repair for future defense asset, or continue P18 reference verification; don't alter user-approved five-chapter PDF without new request.

## 16/10/2026 — P15 local 12GB watchdog/runner

- **P15-LOCAL-12GB-WATCHDOG = CODE_READY / NOT_WINDOWS_VERIFIED.** New files in `tools/p15_local_supervisor.py`, `tools/p15_local_worker.py`, `tests/test_p15_local_supervisor.py`, and `docs/research/P15_LOCAL_12GB_RUNBOOK_2026-10-16.md`. Author-facing commands are in the runbook. All 4 GitHub blobs were independently compared to locally tested source (SHA-1 exact matches).
- **16/16 isolated unit tests passed on synthetic/stub inputs**, including forced process-tree kill and explicit official TEST/interim CSV read rejection. No live Windows/UNSW-TRAIN run has occurred; **P15/G3 remain PARTIAL, full reproduction NOT VERIFIED**.
- New *alternative* admission policy for a monitored pilot on 12GB Windows: require >=4GiB free RAM (no launch with last user-reported ~2.01GiB), cap process-tree RSS to 2GiB, stop at <1.5GiB free system RAM or <10GiB free disk, up to 20 min per supervised run, one model at a time. **Historical P15 9GiB gate remains FAIL**; alternate thresholds are engineering safeguards, not measured minimum requirements.
- Pilot 10,000 stratified TRAIN-only rows, then full 175,341 TRAIN rows only with a matching passed pilot report and additional <75% cap headroom. CPU affinity 1–2 OS cores; frozen RF n_jobs and CV/hyperparameters unchanged. Worker only imports model builders and does not call P9 main; negative input guards and output new path/no overwrite.
- Next: user `git pull --ff-only origin main`, install fresh Python3.11 deps+psutil, run fixture tests, check available RAM. If <4GiB, **NO_GO, do not force**; otherwise pilot RF-17 first, then report peak and logs before deciding full work. Do not mark READY_FOR_SUBMISSION or inference demo until real reconstruct artifacts pass independent QA.

## 16/10/2026 — P15 12GB CI Windows verified

- **P15-LOCAL-WATCHDOG-WIN-CI = PASS_SCOPED**: GitHub Actions Windows Python3.11 `38928283823` ran **18/18 unit tests PASS**, after fixing Windows 8.3 path alias failures in the first CI run. QA report `docs/research/P15_LOCAL_12GB_WINDOWS_CI_QA_2026-10-16.md`; newly created supervisor/worker/tests/runbook in repo main. Tests include forced stop of a sleeping process and rejection of official TEST/interim CSV and missing full artifact; no ML fitting executed.
- **P15 FULLTRAIN NO_GO at user's reported RAM snapshot**: ~2.01 GiB free; original preflight 9GiB gate FAIL, alternative monitored pilot 4GiB gate FAIL. Continue only after fresh local RAM check >=4GiB and author-run RF17 pilot. New operational policy never overwrites historical 9GiB preflight or frozen results.
- Still missing: measured local pilot, RAM logs and three fully reconstructed artifacts on all official TRAIN; no demo inference or P15/G3 closure. Windows CI PASS does not imply scientific reproduction.

## 16/10/2026 — RF17-PILOT-AUTHOR-EVIDENCE and Git venv hygiene

- **RF17-PILOT-AUTHOR-EVIDENCE = DONE_SCOPED**: author-pushed report at `results/reproducibility/p15_local_rf17_pilot_01/`; PASS and worker PASS, 10,000 TRAIN rows, 17 features, threshold 0.5, exit 0, no TEST. Resource log 24 samples, peak process-tree RSS 370,864,128 B (~353.68 MiB), min available RAM 7,161,253,888 B (~6.67 GiB), starting available 7,474,434,048 B (~6.96 GiB), fit 5.125 s. Frozen P15 input hashes agree. Source `docs/research/P15_RF17_PILOT_GITHUB_EVIDENCE_QA_2026-10-16.md`. No full model artifact, no generalization metric; P15/G3 PARTIAL.
- **GIT-HYGIENE-GATE = OPEN AUTHOR_ACTION**: author commit `ab88db8` unintentionally tracks `.venv-p15-local/` (~7,401 tree items). Main .gitignore updated to ignore this folder and new full model .joblib; **still tracked** until author safely runs `git rm -r --cached -- .venv-p15-local` on Windows then verifies working Python remains and commits/pushes. Do **not** remotely delete tracked venv before user-side untracking; pulling deletion may destroy local environment. Author instructions: `docs/research/P15_GIT_VENV_SAFE_CLEANUP_2026-10-16.md`. No force push/history rewrite.
- Next P15 jobs: independently supervised `random_forest_42` pilot, then `stacking_42` pilot, with fresh >=4 GiB free RAM gate and new outdirs; review peak RSS / compatibility before any fullTRAIN job. Do not infer 10k pilot peak equals fullTRAIN peak.

## 16/10/2026 — RF42-PILOT-AUTHOR-EVIDENCE

- **RF42-PILOT-AUTHOR-EVIDENCE = PASS_DONE_SCOPED**. GitHub author-pushed `results/reproducibility/p15_local_rf42_pilot_01/` logs: 10,000 TRAIN rows, ordered42, threshold0.5, classes[0,1], worker/result PASS, no TEST. Measured peak process-tree RSS383,684,608 B (365.91 MiB) under 2GiB cap; RAM start6,057,549,824 B (5.642 GiB), min5,708,353,536 B (5.316 GiB), 55 samples, fit22.547s, exit0, stop_reason null. Source/builders/config hashes match RF17 and frozen anchors. Independent read-only log/source inspection **19/19 checks PASS** (by field values, not JSON key insertion order). Report `docs/research/P15_RF42_PILOT_GITHUB_EVIDENCE_QA_2026-10-16.md`.
- **GIT-VENV-CLEANUP = HEAD_VERIFIED**: current tracked tree has 0 `.venv-p15-local/` paths; original previous tracking of thousands of installed library files addressed without a history rewrite; ignores in `.gitignore`. Local physical venv still expected; RF42 pilot ran with it.
- P15 state: **RF17 pilot PASS, RF42 pilot PASS, Stacking pilot NOT_RUN, all three full TRAIN NOT_RUN**; P15/G3 still PARTIAL. Next Stacking pilot on fresh >=4 GiB free system RAM, under resource watchdog 2 GiB RSS cap; no automatic extrapolation to full TRAIN. User must pull current main and execute locally; checkpoint after Stacking logs.

## 16/10/2026 — STACK42-PILOT-AUTHOR-EVIDENCE = PASS_DONE_SCOPED

- Author push `b4707dc`: Stacking-42 pilot (10,000 TRAIN, 42 ordered features, threshold 0.5) `PASS`, worker passed, exit0, no watchdog stop, **170 resource samples**. Max sampled tree RSS `368455680` B (351.39 MiB of 2GiB cap), start available RAM `6140862464` B (5.719 GiB), min available `5776723968` B (5.380 GiB), fit `80.968 s`. Matching four frozen source hashes; no TEST. Independent source/log arithmetic **21/21 checks PASS** across all three pilots; QA `docs/research/P15_STACKING_PILOT_GITHUB_EVIDENCE_QA_2026-10-16.md`.
- P15 pilot checkpoint: **RF17=PASS, RF42=PASS, Stacking42=PASS**, all as 10k TRAIN-only software/resource checks. **NO FULL TRAIN ARTIFACTS** and P15/G3 remain PARTIAL; canonical 9GiB gate still false. Pilots do not guarantee full memory/runtime.
- **NEXT ACTION (user host):** fresh RAM>=4GiB, disk>=10GiB, no competing runs; first `random_forest_17` `--mode full` with matching RF17 pilot report, unique `results/reproducibility/p15_local_rf17_full_01` output and 2GiB tree RSS watcher. Confirm `run_report.json`, worker `train_rows=175341`, actual joblib artifact/hash on user disk and resource log before authorizing RF42 full. Do not push large .joblib or raw dataset; no TEST read or frozen result update. 20min timeout per model.

## 16/10/2026 — P15-RF17-FULL-AUTHOR = PASS_SCOPED_AUTHOR_EVIDENCE

- User pushed `results/reproducibility/p15_local_rf17_full_01/` to main at `78e9111`. Author-run watchdog `result=PASS`, worker passed, `mode=full` trained **175,341 official TRAIN rows** with frozen 17 features, binary classes [0,1], threshold0.5. Fit307.453s; 620 sampled RSS observations; peak535,023,616 B (510.24 MiB of2GiB), minimum system available5.222GiB, initial5.553GiB; exit0, stop_reason=null, no TEST. Frozen scientific source hashes match. Local artifact reported `random_forest_17_RECONSTRUCTED_FULL_TRAIN.joblib`,22,169,429 bytes, SHA256 b2751bfc6677a724bcadc85070e5848c0f183c3c81d508b5e4cdae82287c8818. Supervisor verified local file on author machine; independent review of pushed logs **20/20 checks PASS** but binary not uploaded/independently loaded. Scope and warnings: `docs/research/P15_RF17_FULL_TRAIN_GITHUB_EVIDENCE_QA_2026-10-16.md`.
- **Progress: 3/3 pilots PASS, 1/3 full TRAIN author-evidence PASS (RF17), 0/2 remaining full (RF42, Stacking). G3/P15 remains PARTIAL**, original 9GiB gate not passed, alternative monitored admission used. No new scientific TEST metrics, frozen results, thesis PDF or historical script changed.
- Next: user pulls and runs only `random_forest_42` full under same bounded supervisor and matching RF42 pilot with new `p15_local_rf42_full_01` output. Fresh available RAM>=4GiB, disk>=10GiB, no concurrent fit, 2GiB tree RSS cap; do not assume success from RF17 memory profile. Review logs before Stacking full. Don't push full binary joblib.

## 17/10/2026 — P15-RF42-TIMEOUT-RECOVERY-NO-DEADLINE

- **RF42 FULL attempt #01 = INCOMPLETE/TIMEOUT (do not present as fit success).** User pushed `results/reproducibility/p15_local_rf42_full_01/run_report.json` to main commit `5c02bf5`: resource log 2358 samples (last1200.12s), peak RSS483,598,336 B (~461.20 MiB), RAM available min5,823,201,280 B (~5.424 GiB), disk min30,537,601,024 B; stop_reason TIMEOUT, exit15, worker_checks FALSE. RAM did not hit 2GiB cap or 1.5GiB floor; no final model artifact from aborted attempt. Evidence and QA `docs/research/P15_RF42_TIMEOUT_RECOVERY_NO_DEADLINE_2026-10-17.md`.
- **Author-approved operational exception:** user requested no wall-time limit for BOTH remaining full candidates, with Windows laptop ~8–9GiB available RAM after closing apps (prospective claim, NOT a measured current reading). Change scoped to `--mode full --timeout-min 0`; pilots retain 5–20min bounded policy. Supervisor still continuously checks process-tree RSS<=2GiB, >=1.5GiB system free RAM, disk>=10GiB, initial RAM>=4GiB, source hashes/provenance/heartbeat, and cleans up process on abort; no scientific source/config/TEST/frozen results modified.
- **Windows CI verified:** [run 38940865179](https://github.com/nphu0811/EnsembleLearning/actions/runs/38940865179), 21/21 stdlib/psutil synthetic safety unit tests PASS and `tools/p15_run_remaining_full_windows.ps1` parsed by pwsh PASS. No live training in CI, no guarantee that full models fit.
- **NEXT:** user `git pull --ff-only origin main`, confirm fresh available RAM/disk and no other training, then execute **only** `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\p15_run_remaining_full_windows.ps1` from Windows repo root. Script runs RF42 full in new `p15_local_rf42_full_02` then Stacking full in new `p15_local_stack_full_01` ONLY IF RF42 report PASS and 175341 rows; no detached jobs or auto retry, no timeout cap for either. Keep power connected and automatic sleep disabled while running, preserve raw/model/P17/P9/historical reports, do not push .joblib. G3/P15 PARTIAL until both full, direct artifact QA/provenance independent review.

## 2026-10-17 — P15-THREE-FULL-AUTHOR-LOGS-2026-10-17

- **P15 FULL TRAIN RECONSTRUCTION = THREE_AUTHOR_RUNS_PASS_SCOPED**. User push `d090c163a3c20f5637a8e500fdb7afc552ddbe9f` includes RF17 full `p15_local_rf17_full_01`, RF42 full `p15_local_rf42_full_02`, Stacking42 full `p15_local_stack_full_01`, each with `run_report.json` PASS, `worker_result.json` passed, 175341 frozen TRAIN, threshold0.5, expected 17/42/42 features, input SHA matches, no TEST, exit0, no watchdog stop. Cross-checked report/start/worker/resources **75/75 read-only consistency assertions PASS**; source `docs/research/P15_THREE_FULL_TRAIN_AUTHOR_EVIDENCE_QA_2026-10-17.md`.
- **Measured fit/RSS**: RF17 307.453s /510.24MiB; RF42 1867.234s /693.57MiB; Stacking42 4759.094s /725.33MiB. All below 2GiB sampled process RSS ceiling, no low-RAM/disk watchdog trigger; user-side local serialized model SHA/size recorded but binary not pushed. Original RF42 #01 INCOMPLETE/TIMEOUT preserved; RF42 #02 fresh PASS. Full reconstruction in observed Python3.11.9/scikit-learn1.9.0 environment; **NOT ORIGINAL historical model identity**.
- **P15 ARTIFACT QA = PENDING_LOCAL_INDEPENDENT_LOAD**. Added `tools/p15_verify_full_artifacts.py` plus `tests/test_p15_artifact_acceptance.py`, fixture-only Windows CI; this verifier must run on author's own laptop and check all three actual joblib SHA/size, fitted estimator configuration, ordered schema, 16 TRAIN-derived rows probability semantics without fit/TEST. Upload only `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. Until reviewer sees PASS and independent provenance QA, P15 **PARTIAL / G3 not closed**. Do not retune, rerun TEST, change official PDF or claim new performance.

## 2026-10-17 — P15-ARTIFACT-VERIFIER-WINDOWS-CI

- New `tools/p15_verify_full_artifacts.py`: author-side, **read-only joblib verification** for 3 trusted local P15 full artifacts; input SHA/source/env comparison, actual file SHA256/size before+after deserialization, fitted estimator/frozen config/schema inspection, 16 official TRAIN-derived rows `predict_proba` sanity checks, **NO FIT, NO OFFICIAL TEST, NO scientific score**, exclusive output `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. Do not run joblib.load on untrusted downloaded pickle data.
- Windows GitHub Actions [run 38986685352](https://github.com/nphu0811/EnsembleLearning/actions/runs/38986685352) **PASS**, 21/21 watchdog tests +6/6 verifier fixture tests, plus compilation & PowerShell parse. Initial new-verifier CI run failed a test-file syntax typo (not runtime/science); repaired, preserved failure history.
- **P15 ARTIFACT INSPECTION STILL PENDING ON USER MACHINE.** Windows CI tests only fake files; they DO NOT load author's 3 actual .joblib models. User must pull, run verifier and push JSON result, then source-reviewed scientific gate decision. Avoid P15/G3 release-ready assertion until reviewed.

## 17/10/2026 — P15-DONE_SCOPED_RECONSTRUCTION / LOCAL_ARTIFACT_QA_ACCEPTED

- **Author acceptance report:** `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json` pushed commit `c81f99a548045d0f6900bec65509ad35da32a073`; `passed=true`, `training_performed=false`, `official_test_opened=false`.
- **Local actual binary checks 69/69 true**: RF17 20/20, RF42 20/20, Stacking42 29/29 (SHA256, byte sizes, model load, frozen fitted hyperparameters, 17/42 feature schema/order, labels[0,1], threshold0.5, 16 TRAIN-row probability sanity, unchanged hash after load). Remote consistency recheck of author report vs 3 worker+supervisor full TRAIN reports: candidate, model hash/size, inputs+versions, 175341 TRAIN rows and pass status all match. Earlier 75/75 read-only logs consistency pass retained. Actual binaries were checked on user Windows laptop, **not loaded by remote reviewer**; files are not in public Git.
- **P15 = DONE_SCOPED_RECONSTRUCTION**, record `docs/research/P15_FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md`. Historical 9GiB admission never claimed PASS; alternate resource-supervised 12GB local execution used. RF42 old TIMEOUT INCOMPLETE preserved. No test recomputation, no re-selection, no frozen PDF edits. **G3 overall remains PARTIAL / external binary review, original environment & live-demo/release approval OPEN**; administrative/writing/reference/source rights G0–G6 not auto-closed.
- **Do not repeat fit**. Next work: candidate-specific demo contract and release rights, P16/P18/P19/P20, source verification and proper manuscript+delivery gates. Re-verify only into NEW unique artifact QA outdir if necessary; original 3 models and acceptance JSON kept unchanged.
