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
| P17 | Report writing | TODO_FINAL_OUTPUT | Working source/template available; no checked complete IDS LaTeX PDF |
| P18 | Citation management | PARTIAL | 11/12 legacy metadata verified at r04; L03 pagination conflict, U01/U03 warning; final refs.bib QA open |
| P19 | Data availability | IN_PROGRESS | Draft provenance/repository material; public release/license/version and rights review pending |
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
