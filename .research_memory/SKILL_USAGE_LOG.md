# Nature Skills actual-use log

Log only skill instructions that were actually loaded and applied.

Use: Date | Task | Registered skill ID | SKILL.md location | References read | Actual action | Outputs | QA.

## 2026-10-16 actual actions

Skill root below is `C:/Users/admin/.codex/skills/`. SHA-256 of installed SKILL.md files in `results/reproducibility/resume_2026_10_16/bootstrap/nature_skill_registry.csv` pins inspected versions. `loaded=false` in that discovery snapshot means it does not track subsequent usage; this log is authoritative for actual loaded/applied work.

| Task | Registered ID / path | References actually read | Action / output | QA |
|---|---|---|---|---|
| P19-DRAFT | nature-data, nature-data/SKILL.md; manifest 2.2.0 | manifest.yaml; static/core/stance.md, workflow.md; references/fair-metadata-checklist.md, statement-patterns.md | Dataset/access inventory, statement, FAIR and unresolved fields in DATA_CODE_AVAILABILITY.md | Local pointers and UNSW live page checked; no fabricated license/DOI |
| PROP-FOUND | researchwrite, nature-proposal-writer/SKILL.md; manifest 1.1.1 | manifest.yaml; references/foundation-files.md, partial-proposal-scope.md, compose-mode.md, validation-checklist.md, stopping-rules.md, project-structure.md; templates/00_scope.md through 05_style_guide.md | Restored scope/canon/evidence/argument/contracts/style files and state | Foundation partial; no expert review/score/export claimed |
| P16-F1 | nature-figure, nature-figure/SKILL.md; manifest 2.8.0 | manifest.yaml; static/core/contract.md, stance.md; static/fragments/backend/python.md; references/qa-contract.md, figure-legend-conventions.md | Contract, Python forest plot and PDF/SVG/PNG/source data | Source 19 PASS/2 reviewed WARN, glyph min8, collision0/0, visual PNG inspection; single-panel alignment N/A |
| P18-UNSW | nature-ref-verifier, nature-ref-verifier/SKILL.md; manifest 1.0.1 | manifest.yaml; references/common-patterns.md | DOI-first Crossref requests, publisher/institutional cross-check; ledger/BibTeX/report for 5 records | 3 VERIFIED_METADATA, 2 CHECK_SUGGESTED; 0 full text read; no P18 complete claim |

`nature-reviewer` SKILL.md was read during discovery, but no reviewer workflow executed, no mutually blind reviewer reports created. Not logged as used. Documents skill was read for routing; no DOCX authoring/rendering executed because mandated dependency loader unavailable. Superpowers using-superpowers/verification-before-completion instructions read earlier; audit source tools were genuinely executed, not training scripts.

## 2026-10-16 r02

| Task | Registered ID / exact path | References read | Actual action / outputs | QA |
|---|---|---|---|---|
| P01/P18-LEGACY | nature-academic-search, C:/Users/admin/.codex/skills/nature-academic-search/SKILL.md | manifest.yaml; static/core/tools.md, routing-and-ops.md; references/workflows/wf1-multi-source-search.md; dedup-engine.md, source-tiers.md, search-strategy.md | Ran preflight; legacy query discovery, DOI lookup, publisher/institutional search, dedup/version relation; literature_matrix.csv + gap map | Crossref OK, arXiv SSL failed; no bypass;12 unique final records |
| P18-LEGACY | nature-ref-verifier, C:/Users/admin/.codex/skills/nature-ref-verifier/SKILL.md | common-patterns.md | Crossref DOI resolution, title/author/year/volume/page comparison, final/preprint distinction, ledger/BibTeX |4 VERIFIED_METADATA,8 pending field crosschecks; validation.json PASS |
| PROP-FOUND-R02 | researchwrite, C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md | references/professor-dispatch.md, evaluation-rubric.md; core/foundation references already read in r01 | Updated canon/evidence; dispatched two independent agent specialist passes as explicitly required by foundation review workflow | Reports must be inspected before scoring/gate; no human approval implied |

No nature-reader/paper-card workflow executed in r02; READING_NOTES are bounded source lookup notes, not full paper readers. Discovery alone is not skill execution.

Researchwrite execution detail r02: independently dispatched methods/feasibility and argument/positioning specialists because professor-dispatch.md explicitly says to run independent specialists in parallel when available. No installed professor skill execution claimed; generic agent specialist passes implement that documented review contract. Reviewers also loaded research-anti-slop.md for manual language criteria. Initial scores7.3125/7.25, repaired foundation, rechecks7.8125/7.75; original reports preserved. Synthesis written only after both rechecks. Partial prose drafted after both strict foundation gates passed; section QA separate. Not nature-reviewer/P20, not human supervision, not experimental verification.

Partial section reviewed independently:7.5/10 KEEP_INTERNAL_DRAFT, no P0/P1, four P2 wording/source-readability findings. Applied exact minor edits, checked10 section source paths and original review report hashes. No post-repair rescore or full-proposal QA claimed. Tool discovery r02 still found no load_workspace_dependencies or scholarly MCP search_crossref; direct Crossref/web fallback was used and DOCX authoring/export not attempted.

DOCX-RUNTIME-RECHECK 2026-10-16 | documents | C:/Users/admin/.codex/plugins/cache/openai-primary-runtime/documents/26.1013.11914/skills/documents/SKILL.md | tasks/verify_render.md read | registry/config/runtime diagnosis; no authoring/render | exports/docx_export_2026_10_16/RUNTIME_RECHECK.md; recheck_validation.json | BLOCKED resolver/renderer; preservation checked.
DOCX-RUNTIME-RECHECK 2026-10-16 | plugin-management | C:/Users/admin/.codex/plugins/cache/openai-curated-remote/plugin-management/0.1.0/skills/plugin-management/SKILL.md | search_plugins documents/runtime | no relevant resolver found; no plugin mutation.


## r03 —16/10/2026

- P18-FIELD-R03: nature-ref-verifier; exact C:/Users/admin/.codex/skills/nature-ref-verifier/SKILL.md; manifest1.0.1 + references/common-patterns.md read. Applied DOI-first saved-identity checks, second-primary field comparisons, severity/name/year handling and scoped report/BibTeX updates. Outputs literature/resume_r03_2026_10_16/, current matrix/subset.18/18 bookkeeping PASS;6 verified/6 pending, U01/U03 open; not whole-paper verification.
- PROP-PRODUCTS-R03: researchwrite alias, exact C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md; manifest1.1.1; hybrid-mode, compose-mode, partial-proposal-scope, validation-checklist, stopping-rules, project-structure, evaluation-rubric, professor-dispatch read. Reused passed r02 foundation; read04/06/07, drafted missing bounded product/application/schedule/budget sections, dispatched one narrow independent feasibility/template reviewer as permitted by skill. Review and source validation under qa_logs/r03*. No full proposal or DOCX export.
- nature-data router was read during routing only; no new availability workflow executed. Not logged as applied. No nature-reviewer/P20 or human approval claimed. Registry hashes pinned in r03 resume_audit.json; reviewer additional references recorded in its report.


## r04 — actual loaded/applied skills

- R04-REF: nature-ref-verifier exact C:/Users/admin/.codex/skills/nature-ref-verifier/SKILL.md, manifest1.0.1, common-patterns.md. DOI-first freshCrossref6records,field source matching,conflict classification,ledger/BibTeX/currentmatrix.28/28recordchecks;11verified,L03warning;notP18complete.
- R04-REF: nature-academic-search exact C:/Users/admin/.codex/skills/nature-academic-search/SKILL.md, manifest2.0.0; static/core/tools.md,routing-and-ops.md; wf2-citation-verification.md,source-tiers.md,dedup-engine.md,citation-parser.md; scripts/preflight.py read/executed. ScholarlyMCP absent;Crossref/webfallback;2/3APIpreflight reachable,arXivTLSfail;noTLSbypass. No exhaustive discovery/systematic review claim.
- R04-READ: nature-reader exact C:/Users/admin/.codex/skills/nature-reader/SKILL.md2.1.1; manifest read, references/grounding-rules.md; source-linked question branch (not full reader). Selected actualL06Methods,L09indexedIntroduction,L03author docs,D01announcement,D02summaryobjectives;source_mapCSV/notes,10anchorchecks.
- R04-GAP/LIT/ASSEMBLY: researchwrite exact C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md +manifest1.1.1; hybrid-mode,compose-mode,partial-proposal-scope,validation-checklist,professor-dispatch,evaluation-rubric,stopping-rules,project-structure read. Foundation00-07 andpassedr02review reused. Two independent non-overlapping partialreviews per dispatch;minorrepairs;fullassemblyevidencereport saved butfullargumentreviewquota-failed. No fabricatedexpert/humanapproval/P20. Reviewers loadedresearch-anti-slop.md and recordedmanualVietnamese adaptation.
- R04-ML-SMOKE: superpowers verification-before-completion andsystematic-debugging exact C:/Users/admin/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills/.../SKILL.md; actualfreshsmoke41/42fail,isolateddiagnosis,singleassertionrepair,rerun45/45,pipcheck and6unit tests. test-driven-development SKILLread for failed integrationregression before repair;do notclaim allnewtoolswerebuiltTDD. No fullTRAINreproduction claim.
- using-superpowers SKILL+references/codex-tools read after registry refresh. Applicable workspace/userpreservation/autonomous instructions overridebranchcleanup or approval conventions;nohistorydeletion/commitfiction.
- write-like-me SKILL read for defensecontent;tool not exposed andnoprivatewritingretrieval done. Usedexistingacademicdrafts as taskformat guidance,not a retrievedpersonalstylematch. nature-downloaderrouter/deliveryreference read forroutingonly;no downloader executed,SI notrequested/downloaded. executing-plans reference read forroutingonly;not claiming itsbranch/commitworkflow. No newdocument/slidesauthoring/render workflow executed.

## R05-ASSEMBLY-REVIEW / 16-10-2026

Actual registry inspected via resume audit; researchwrite registered name at C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md, manifest1.1.1. Root read manifest and revise-mode, professor-dispatch, validation-checklist, evaluation-rubric, stopping-rules, research-anti-slop references. Applied revise diagnosis/brief, independent AI specialist dispatch, targeted prose repair, citation/frozen-boundary validation and recheck. No numerical score used; Vietnamese manual anti-slop/source-strength review only. Outputs r05 review/recheck/revision/validation/resolution. Reviewer own loaded resources recorded in report. nature-reviewer SKILL.md inspected but not applied: user requested one proposal argument report, not Nature panel. nature-figure router inspected for next-task routing, no plotting/figure workflow executed in this review. Superpowers using-superpowers+Codex reference and verification-before-completion read/applied as process guidance; not Nature executions.


## 17/10/2026 — actual P16/P18/P19 skill execution

- nature-figure at C:/Users/admin/.codex/skills/nature-figure/SKILL.md;manifest2.8.0. Loadedmanifest,static/core/contract.md,stance.md,Pythonfragment,references/qa-contract.md,figure-contract.md,asset-adaptation.md,multipanel-evidence-architecture.md. Applied savedsource/claimaudit,Python-only sixsinglepanelalternatives,editablePDF/SVG/600dpiPNG,all9attackfamilies,alignmenthelperNOTAPPLICABLEsinglepanel,validate_figure.py,audit_pdf_text.py,audit_figure_collisions.py,actualvisualcontactreview. Outputs finalstandalone03,sourceCSV+hashes,QA JSON.20sourcePASS/1PNG-noTIFFWARN/0FAIL;text6/6/collision6/6PASS. Historical12PDFsaudited,text12PASS/collision6PASS6FAIL. Failures retained.
- nature-statistics at C:/Users/admin/.codex/skills/nature-statistics/SKILL.md. Loadedreferences/statistical-reporting.md,figure-statistics.md,reviewer-checklist.md,common-failure-modes.md and ../nature-shared/core/consistency-sweep.md. Applied confusion-countmetricidentities,unit/replication/conditionalCI/SD/Holm/causal-boundaryaudit. Output2132checksummaryandP16QAincludinglabelledderivedWeightedF1. No newexperiment/CI orfullstatisticalvalidityclaim.
- pdf:pdf at C:/Users/admin/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md. Read-onlyactualPDFSHA/37pages,Poppler100dpiallpages,PyMuPDFgeometry,178checks,fivecontactsheetsvisuallyinspected. NoauthoringoperationorPDFmodification.
- nature-ref-verifier at C:/Users/admin/.codex/skills/nature-ref-verifier/SKILL.md and references/common-patterns.md. Offline currentBibTeXfieldcomparison againstsavedmultisourceledger,24claimcontexts,readingscopeclassification.119/119PASS;12records;0newnetworkqueries/0fulltextreads. No bibliography rewrite.
- nature-data at C:/Users/admin/.codex/skills/nature-data/SKILL.md;manifest2.2.0,static/core/stance.md,workflow.md,references/fair-metadata-checklist.md. Applied bounded auditofexistingavailabilityprovenance,README,QAenvironmentlimitations,FAIR/rightsreview;P19readinessnoteandtrackedreviewinventory. NoDOI/license/finalreleaseinvented.
- using-superpowersSKILL+Codexreference,verification-before-completionSKILLandsystematic-debuggingSKILLread/appliedasprocessguidance. nature-reviewerSKILLreadforP20routingonly,notexecuted;no3reviewerpanelorindependenthumanreviewclaim. No subagent spawned.


##17/10/2026 P18deep

17/10/2026 P18deep actualskills: nature-academic-search SKILL/manifest2.0.0,coretools/routing,wf1/wf2,source-tiers,dedup loaded;preflightexecuted2/3reachable(arXivTLSfail);officialweb/Crossref fallback,DOIdedup,3newidentitychecks. nature-reader SKILL2.1.1 andgrounding-rules branchsource-linkedquestions: L06selectedpublisherMethods/results/conclusion,L12PDFpp5-20selected,N02publisherMethod/results/limitations,notfull-papertranslation. nature-ref-verifier SKILL/manifest1.0.1+common-patterns fromsameconversationreused,3DOImetadatafieldcrosschecks,L03VORattemptfailretained,U01/U03closedchecksnotrerun. PDFread-onlyworkflow appliedlocalL12pageextraction/render/visualpp16-18. nature-downloaderSKILLinspectedroutingonly,notexecuted;noSIrequested/fetched. researchwritenotusedbecausenoproposaldrafting;noNaturepanelorhumanreviewclaimed.


##17/10/2026 P19safe/P20prep actualusage

nature-data SKILL/manifest2.2.0/corestance/coreworkflow/FAIRmetadatareferencesloadedinconversation,reusedwithcoreworkflowreread:read-onlydataset/model/sourceavailabilityclassification,smokeprovenanceinventory,rightsdecisionlist,allowlistinternalmanifest. OutputP19safeaudit,245mechanical/121independentQA,3pathunit tests. NoarchivalDOI/license/publicauthorizationinvented.
nature-reviewer SKILLandtechnical-concern-taxonomy.md/domain-specific-review-gates.md(Engineeringsection)readforPREPARATIONONLY. Adaptedfiveaxes,evidencepointer/severity/blockingrubric,3futureemphasisbriefs,neutralpacket/isolationconditionsandquestionlist. NOactualreviewerreport,panel,pre-revieworindependenthumanendorsementclaimed. Researchwritenotappliedbecauseproposaldraftingnotundertaken. No subagents. ActualscopedP18skillsasrecordedinpriorentry;fulltexts/ZIPremainlocalignored.


## DEFENSE_2026_10_19
Read exact local officecli-pptx/morph-ppt/visual-ppt-builder/ppt-masterSKILL.md; Presentations skill+style_guidelines; PDF skill; superpowers using-superpowers+brainstorming; write-like-me. Remote MotionStudioSKILL and research-protocol/motion-grammar/speech-craft/craft/qa-checklist fetched and read. Actual applied techniques: !!Morph names, native shapes, timed voice measurement, independently delegated Gate3visualQA. OfficeCLI not installed/run; PPTMaster integrityguard exit0 surveyed only, exporter not run; Visual local references/scripts missing, remote schema read, not falsely executed. Nature Skills not used this turn. Exact paths, versions, sources, license/dependency caveats and applied-vs-surveyed status in presentation/nckh_defense/Skill_Decision_Matrix.md; QA48/48PASS.

## 2026-10-19 Creative V2 — actual scope
Humanizer3.1 read in full from blader/humanizer SKILL.md; snapshot audit/Humanizer_SKILL.md. Applied neutral factual file/embedded editing to38LaTeX passages and rewritten speech/Q&A, not AI detection. officecli-pptx local SKILL read; Gate3 independent screenshot reviewer used for29slides and fixes. morph-ppt base read, zeroMorph used inV2. PPTMaster animations/native guidance and VisualPPT RULES read; their engines not run. Browser skill read; built-in browser missingmodule/Chrome unavailable, Playwright fallback actual screenshots. Nature-polishing registry instruction read but no Nature operation claimed. Snapshot inherited surveys explicitly scoped as prior audit, not new executions.
