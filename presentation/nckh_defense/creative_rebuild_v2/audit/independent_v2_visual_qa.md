# Independent V2 visual and scientific critique

Date: 2026-10-19, Asia/Saigon. This is a fresh review of creative_rebuild_v2; the earlier white/blue deck approval is not reused.

## Scope and method

Reviewed all 29 new actual PowerPoint renders through four contact sheets, then inspected slides 4, 6, 9, 10, 12, 14, 15, 16 and 17 at full 1600×900 resolution. Read creative_content.py, build_creative.py and motion_engine.py. Compared principal numbers with the existing official TEST metrics, paired-bootstrap differences and P21 summary used in the project. No PowerPoint COM session was opened, and no production file was edited.

The bold type, cream/navy/violet/coral/lime palette and asymmetry are intentional and acceptable. This audit does not impose the earlier deck's style. Strongest visible scenes are 3, 7, 11, 12 and 17. The large +118 treatment correctly says records rather than independent incidents.

## Verdict: REJECT pending fixes

1. **Slide 16 — blocking static-export failure.** All three time-separated loss scenarios are simultaneously visible in the actual PNG: r values overlap, loss values overlap and all three conclusions collide. The source deliberately uses entrance/exit events, so this finding does not prove slideshow failure. It does prove the current static rendering is unreadable and therefore cannot serve as the requested static PDF page. Fix with an export-only static version that displays one clearly identified scenario, or three non-overlapping scenario rows/columns. Preserve the animated PPTX if playback is correct. Reinspect the corrected static page and separately capture timed video frames around 1 s, 9 s and 16 s to confirm clean state replacement.

2. **Slide 10 — unsourced quantitative-looking CI geometry.** The top-right violet segment and zero marker look like a measured confidence interval, but build_creative.py hardcodes the endpoints and zero location without using a metric or bounds, and labels neither the interval nor endpoints. The text claim is correct; the drawing is not a traceable numerical chart. Replace it with the real ΔMacro-F1 interval [−0.0003118042, +0.0013089503], point estimate +0.0004966899 and a labeled zero line, or remove the drawing. If retained only as a conceptual sketch, explicitly label it as such and avoid a data-chart appearance.

3. **Slide 14 — missing component labels.** The stacked timing bar uses purple and lime without a legend identifying selection versus model fit. The bottom arithmetic supplies numbers but leaves the visual mapping implicit. Add short labels such as “chọn biến 225,250 s” and “fit 84,600 s”, matched to colors. Give RF42's bar its 241,119 s label nearby. This preserves the sparse composition while making the evidence understandable without narration.

## Additional actionable improvements

- **Slide 9:** Three probability arrows end before the meta learner without converging into it; the upper and lower arrows are vertically outside the diamond. Join the three paths into the meta input, or add a vector brace/input edge. The present gap weakens the pipeline explanation. Footer “INFERENCE: base refit” can suggest training at prediction time; change to “base đã refit” or “base đã học → xác suất → meta”. Narration already mostly distinguishes the stages correctly.
- **Slide 8:** All three Voting output rails lie at the same y coordinate, passing through the lower edges of later model circles. They read as a bus or chain. Separate three output paths and converge them at the fixed aggregation rule; keep Hard and Soft clearly identified as alternatives.
- **Slide 3 narration:** “U en ét đắp” is an unclear pronunciation substitute for UNSW-NB15, while the screen only shows split counts. Use the exact dataset identifier in the written script, with a separate pronunciation instruction for voice generation; listen to the spoken result. This is a script issue, not a PNG defect.
- **Slide 15:** Label the plotted points explicitly as averages over five FIT seeds. Footer communicates the scope but does not explicitly say these coordinates are means. The direction of the arrows is not independently certified by static screenshots; check playback frames.

## Scientific assessment

No mismatch found in displayed historical Macro-F1, +0.000497 difference, −142 FP, +118 FN, P21 Macro-F1 means, selection/fit timing arithmetic, or plotted P21 FPR/FNR coordinates. Official TEST and post-hoc TRAIN validation are separated. Five seeds are explicitly not five independent tests. CI-containing-zero language avoids an equivalence or superiority claim. OOF training and inference are separated by slides 6 and 9; slide 6's three-fold sketch is compatible with the three-fold grouped CV in tools/p21_science_core.py, but does not establish all historical training details.

The appendix body text is readable in the reviewed renders. No actionable overlap or clipping found there. Small source footers and appendix jump links are secondary navigation/evidence, not primary projected content.

## Limits

No full video, audio, live slideshow or runtime animation was inspected in this audit. Static exports show initial positions and all shapes, not timing states. Therefore this report does not certify motion correctness, exact six-minute duration, pronunciation, hidden-slide exclusion, or the absence of overlap during movement. Claims about those require separate timed playback validation. No final Gate 3 PASS is granted until the blocking static failure and quantitative CI drawing are resolved and the changed renders are reinspected.

## Fix verification — cycle 1

Reopened only the current slide_08.png, slide_09.png, slide_10.png, slide_14.png, slide_15.png and slide_16.png at full resolution, ignoring older contact sheets.

- Slide 8: independent paths now converge into the aggregation symbol. PASS.
- Slide 9: meta input connections and “base đã học” footer resolve prior conceptual issues. However the new RF-to-meta diagonal crosses the bottom p(Attack) label. REJECT for this local regression; move the lower probability label away from that diagonal, for example below the RF row with adequate footer clearance.
- Slide 10: named CI, limits, zero and point estimate are now shown; geometry is consistent with the sourced interval. PASS.
- Slide 14: selector/fit component legend now explicit. PASS.
- Slide 15: mean over five FIT seeds now explicit. PASS.
- Slide 16: three separate cost scenarios are now readable simultaneously. All displayed cost values and conclusions are consistent with the stated loss function. PASS.

Only slide 9's new connector/label overlap remains unresolved in the screenshot gate. No motion/audio claim is made.

## Fix verification — cycle 2 and final screenshot verdict

Reopened the newly rendered slide_09.png at full 1600×900 resolution. The bottom p(Attack) label is now below the RF-to-meta connector, with clear space above the footer. The overlap is resolved. PASS.

**Final Gate 3 screenshot judgment: PASS within the scope above.** All actionable screenshot defects from the fresh V2 audit and fix cycle are resolved. Initial rejection findings are retained above as audit history; they are superseded by these successful rechecks. This verdict covers static screenshots only and does not certify motion, audio or export duration. Deck author remains responsible for final save/flush and separate playback verification.

## Appendix wording refresh — final regression review

Read all 12 revised answers in creative_qna.py and reviewed all updated slide_18.png through slide_29.png using newly generated 800×450-per-slide contact sheets. Also reopened slides 23, 24, 25, 26, 27 and 29 at full 1600×900 resolution. Reviewed the new PNGs rather than relying on the older contact sheet.

**Appendix regression verdict: PASS.** No clipping, text collision, unreadable body text or scientific wording regression found. Revised prose keeps the no-new-algorithm claim, benchmark limitation, historical selection optimism, internal P21 scope, five training seeds, timing units, OOF/inference distinction, positive-class FPR/FNR definitions, CI-versus-equivalence distinction and hypothetical cost threshold. The P21 feature-selection answer retains exact decimal-second values and the end-to-end caveat. The cost answer retains the restriction to the compared fixed predictions. The deployment answer remains explicit that the work is offline and P15 is not proof of bitwise historical-artifact identity.

The displayed 15–25-second note is a speaking target for a core answer, not a measured reading time for the entire paragraph. No appendix audio timing was evaluated. Main slides and video were not re-reviewed in this appendix-only refresh; the previous screenshot PASS for their unchanged visuals remains applicable.
