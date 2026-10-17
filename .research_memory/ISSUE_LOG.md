# Issue log

## r03

- I-r03-01: prior manifest lệch HANDOFF/SKILL_USAGE do bổ sung runtime recheck, không artifact khoa học. Expected/actual được giữ trong resume_audit.json; refresh manifest có provenance ở checkpoint cuối.
- I-r03-02: DOCX count9 trong notes/matrix cũ sai; direct OOXML8 top-level/8 total và CRC PASS. Sửa current matrix, giữ historical audit.
- I-r03-03: Wiley direct403, MDPI web errors, RHU TLS certificate failure; không bypass. L04 dùng captured publisher indexed fields; L12 chưa nâng status. Chi tiết fetch_ledger/source captures.
- I-r03-04: stdout cp1252 khi đọc tiếng Việt OOXML lỗi; reconfigure UTF-8 thành công, không thay file nguồn. Một apply_patch có context không khớp đã bị reject nguyên patch; áp lại với context thực.

Use: ID | Severity | Issue | Evidence | Attempts | Resolution | Status.

| ID | Severity | Issue | Evidence / attempts | Resolution | Status |
|---|---|---|---|---|---|
| I01 | Major | Starter memory inconsistent with mature workspace | 18/48/36 inventory; old memory archived | Resume audit + current roadmap/canon | RESOLVED |
| I02 | Major | FS outside outer development folds | P15-04 source hashes/lines | Preserve outputs; disclose optimism, no unbiased CV claim | KNOWN_LIMITATION |
| I03 | Major | Original training environment/model missing | No local .pkl/.pickle/.joblib; old 3.14 smoke not original env | Fresh stdlib replay added, ML reproduction still pending | OPEN |
| I04 | Major | Template DOCX missing from workspace initially | Found separate original in Downloads; ZIP only LaTeX | Copy with exact SHA, 15/15 source matches | RESOLVED source preservation |
| I05 | Major | DOCX/LaTeX rendering dependencies | Loader not in exposed tools; TeX/soffice/pandoc absent PATH | Continue foundation and evidence work | OPEN tool gap |
| I06 | Administrative | Personal/signature/budget applicability unknown | Original form contains sample roles/names | [CẦN XÁC NHẬN], never copy as confirmed | AUTHOR_INPUT_NEEDED |
| I07 | Minor | Console Unicode cp1252 during OOXML print | First read failed UnicodeEncodeError | Retried python -X utf8, complete read succeeded | RESOLVED |
| I08 | Minor | Source figure checker misread width expression | WARN 4648.2mm vs rendered 183mm | Geometry explicitly verified, record warning | RESOLVED |
| I09 | Major | Literature metadata/full text not fully verified | Phase1 v0.1 matrix | P18 field ledger started, don't transfer unchecked claims | OPEN |
| I10 | Minor | Crossref rate limiting U01/U03 | Initial HTTP 429, subsequent sequential calls HTTP 200 | Preserve raw retry and initial summary | RESOLVED transport |
| I11 | Citation | IEEE geometric paper year differs | UNSW 2017 vs Crossref final 2019 5(4)481–494 | Working BibTeX final year with note; publisher direct blocked | CHECK_SUGGESTED |
| I12 | Tool | arXiv preflight SSL verification fails | skill preflight reports2/3 endpoints reachable | Use Crossref + publisher/institutional sources; no TLS bypass | OPEN source-specific |
| I13 | Tool | Crossref discovery429, several publisher fetches403/429/timeout | legacy_candidates.json and SEARCH_PROTOCOL_AND_QA | DOI route succeeded for12 finals+SSRN; remaining reading boundaries explicit | PARTIAL access |
| I14 | Citation | DUEN preprint/final version ambiguity | SSRN DOI versus final ESWA DOI | Store version relation, prefer final record, count1 study | RESOLVED identity/version |
| I15 | Foundation | RQ/output and chronology mapping incomplete | Two independent initial reviews below7.5 | Added06/07, repaired01–04; two rechecks above7.5 | RESOLVED bounded drafting |
| I16 | Audit helper | Overescaped regex did not extractRQ1 | First mapping-check command exited before output | Replaced parser with heading-line extraction; all5 original wordings match | RESOLVED |
| I17 | Source input | Văn bản đã dán (1)(4).txt not located in workspace | Inventory/search did not find original pasted prompt | MASTER/AGENTS govern current work; do not reconstruct missing text | AUTHOR_INPUT_NEEDED location; not blocking current tasks |

## r04 issues

- REF-L03 OPEN:Crossref/author254–262 versusUNSW254–263;publisherrobotcheck. KeepCHECK_SUGGESTED;metadata11/12verified.
- REVIEW-LIMIT OPEN:fullassemblyargumentreviewnoartifactbecauseusagequota;otherfullassemblyevidencereportexistsandread. No automaticretriesorscoresinvented.
- SMOKE-ASSERTION RESOLVED_SCOPED:initial41/42;RF17parallelprobasdiff2.22e-16,serialexact,reloadexact;numeric1e-12+exactlabelsrerun45/45. Frozenresearchunchanged.
- QA-PARSER RESOLVED:initialr04validatorregexmissedheadingRQformat;explicitparse5headings+exactwordingchecks added,30/30final.
- CHECKPOINT-GUARD RESOLVED:FORMcheckpointrejectedundeclaredworkinggapchange;declaredartifactsandreran,no silenthashrefresh.
- DISPLAY RESOLVED:rootrewrotedefensecontentdraftswithreadableVietnamese spacing,rechecked25/25source/timing;notpresentationvisualQA.

## r05 execution issues

Proposal revision first RQ parser included header; assertion stopped before output; anchored RQ1–5 repaired. Citation validator initial33/34 failed qualifier/convention parsing; exact documented placeholders and Proposed model qualifier handled, repaired34/34; initial JSON preserved. Capacity command used unsupported ConvertTo-Json -Property once; corrected PSCustomObject command produced real snapshot. No research results modified; no smoke rerun.


## 17/10/2026 QA findings and repairs

Entry stale manifest267/285,known author-deletedhistoricalZIP281/282reconciled in RESUME_AUDIT. First figurepreflight childcp1252vsparentUTF8causeddecode/NoneTypeerror;explicitchild-Xutf8fixedtoolboundary. Figuregeneration01KeyErrorattack_catrootcausedactualEDAfieldattack_category;attempt02completedbuttwoCIfooterlabels overlapped0.59pt;attempt03bottommarginrepairpassed6/6collision. Allattemptsretained. HistoricalsixcollisionFAILremainandareseparatefromfinalnewbundle. Printfont/118dpiheatmapandpre-P15page33provenanceopen;noapprovedPDFedit.


## P19 inventory finding, current 17/10/2026

The tracked review snapshot flags three historical SMOKE_ONLY.joblib files under results/reproducibility/r04_ml_smoke_repaired/smoke_models/. All three were tracked in initial commit c4ed771. No new model binary is staged; no files were loaded or removed. Inventory passed=false and code license is absent. Keep this release blocker; it is separate from accepted local P15 full-TRAIN reconstructions. Do not treat the final new-file staging check as a passing whole-repository release inventory. See release/review_inventory_2026_10_17_01/validation.json and the final review inventory snapshot.
