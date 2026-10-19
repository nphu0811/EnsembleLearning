# Independent visual and scientific QA

Review date: 2026-10-19 (Asia/Saigon). Reviewer: independent agent, separate from deck author. Checklist: officecli-pptx SKILL.md Gate 3, lines 524–553.

## Scope

Reviewed all 32 actual PowerPoint PNG renders at 1600 × 900 through four contact sheets, with full-resolution detail inspection of slides 2, 10, 12, 13, 16, 18 and 24. Slides 1–20 form the main narrative; slides 21–32 are Q&A. Inspected content.py and relevant build_deck.py sections. Checked numerical claims against final_metrics.csv, paired_bootstrap_differences.csv, P21 aggregate.json (summary 20261019_022655) and extracted V6 report text.

This review covers visible static composition and selected scientific claims. It does not certify animation playback, audio pronunciation, six-minute video duration, hidden-slide export behavior, actual projector legibility or every source-code implementation detail. Those require separate checks.

## Initial findings — REJECT

- Slide 2: Normal → IDS → Attack diagram suggested conversion of normal records into attacks, rather than binary classification. Requested neutral traffic-record input and branching outputs.
- Slide 10: OOF explanation visibly overlapped the Random Forest block. Title approached the right edge. Requested a reserved explanation area and a wrapped or reduced title.
- Slides 12 and 13: value 10.003 overlapped the next Stacking42 row label. Slide 13 also had 734 overlapping the next FN row label. Requested separate label/value positioning or increased row spacing.
- Slide 18: French word “Moyenne” remained in Vietnamese presentation. Requested “Trung bình”.

No actionable static defect was found in the other slides within the stated review scope. Slide 24's two-line title remains clear of its question and body. Slide 16 explicitly identifies its truncated Macro-F1 axis and paired seed lines. Slides 12–13 explicitly state that FP and FN use separate scales.

## Scientific checks

- Historical RF42/Stacking42 Macro-F1 and MCC agree with official_test rows of final_metrics.csv.
- Historical FP values 10,003 → 9,861 and FN values 734 → 852 support −142 FP and +118 FN.
- Paired-bootstrap Macro-F1 and MCC confidence intervals contain zero. Wording avoids claiming equivalence or Stacking superiority.
- Cost threshold 142/118 ≈ 1.2034 follows from the stated hypothetical loss function and fixed predictions.
- P21 mean Macro-F1 RF42-Lite 0.9452196197 and Stacking-Lite 0.9447313497 match aggregate.json.
- P21 FPR/FNR directions and scatter positions match the computed arm means.
- RF17 fit 84.600 s + selector 225.250 s = 309.850 s, compared with RF42 fit 241.119 s, agrees with V6. Caveat that these are not end-to-end costs is visible.
- Narrative separates historical official TEST from post-hoc internal TRAIN validation; five FIT seeds are not portrayed as independent external tests.

## Fix verification — cycle 1

Reopened the regenerated full-resolution PowerPoint renders slide_02.png, slide_10.png, slide_12.png, slide_13.png and slide_18.png after fixes.

- Slide 2: traffic-record input and Normal/Attack output branches now correctly represent classification. PASS.
- Slide 10: wrapped title has sufficient margin; model blocks and OOF explanation no longer collide. PASS.
- Slides 12–13: numerical values now sit above and to the right of their respective bars, separated from model labels. No overlap. PASS.
- Slide 18: “Trung bình” corrected; chart remains readable. PASS.

**Gate 3 PASS for static rendered slides within the review scope.** No unresolved actionable visual or scientific issue from this audit. Deck author remains responsible for final save/flush and separate animation/video/technical verification.
