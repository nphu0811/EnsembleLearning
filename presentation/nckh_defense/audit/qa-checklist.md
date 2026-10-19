# QA checklist (every render, every group, and the final deck)

`python $S/studio.py build WORK --group <group>` builds, renders into a **new** `renders/<group>-N` folder (image viewers
cache by path) and audits with the renders. Open the contact sheet, put it next to the reference
(`studio.py compare`), then open every changed slide at full size and crop 4× where things meet (craft.md §12).
Write the defects in `WORK/notes/<group>.md`, fix them all in one pass, and re-build. Don't trust "it looks fine in the code".

## 0. Build-time layout warnings (`build_deck.py`, printed by `studio.py build`)
Fix every one before you look at the render; each is visible on screen:
- text that needs more height than its box, a word wider than its box, a single word on the last line of a title
- text outside the safe area (0.45 in from the edge; parked shapes are fine)
- two texts that overlap, or a text that runs over a card or a screen it does not belong to
- a card whose content is taller than the card; a font that is not installed (the checks above are then skipped)

## 1. Automatic (`check_deck.py DECK --anchor "…" [--forbid-notes] [--extra-forbid "cô đầu,MIT"] [--max-mb 25]`)
ERROR (exit 1): not exactly 1 transition on a slide; duplicate `!!` names on a slide; a `!!` pair with different kinds;
CJK characters on slides; template leftovers (lorem ipsum, "Click to add", "Title Here"); forbidden strings; size over the limit;
stuck keyframes (same dominant subject image, box/crop move under 10% of slide width, no shared `!!` shape moves 6% or more,
under 30% of pixels changed) beyond the hold-beat allowance (one per scene, 10% of transitions);
one subject image dominant on more than 4 slides, or (on a photo-led deck) fewer distinct subject images than consecutive runs;
the editorial-left template on more than 3 scenes; fewer than 2 font families on a deck of 8 or more slides;
on-slide text averaging under 8 words; **no persistent system** (no `!!` shape on 60% of the slides).
The same image, keyframe and layout errors run on a PDF: `python check_deck.py deck.pdf`.
WARN: a hold beat (make sure it is deliberate); text overflowing into other text or off the slide; text outside the 0.3 in
safe area; more than 12 text sizes; flat grounds on most slides; low contrast (with `--renders`); under 40% of slides citing a
fact ID on the slide or in the notes (with `--facts`); slides without notes; lonely `!!` names; fonts not installed; images
wider than 2560 px; duplicate media; anchor count.
The accepted reference deck passes this audit (`tests/test_audit.py`); a change that fails it is a wrong change.

## 2. Visual (look)
- [ ] It reads as one deck at thumbnail size: the same ground family, chrome, grid and type roles; the signature is present.
- [ ] Next to the reference (`studio.py compare`) it is as specific and as rich; nothing generic, flat or crowded.
- [ ] Every scene is a camera move: keyframes change composition positions, not only words (one hold beat per scene at most).
- [ ] Text is readable over its real background (veil or scrim behind text on photos; gold on a busy photo fails).
- [ ] Nothing collides, including in keyframe states (an object enlarged by Morph can cover the title: move the title).
- [ ] Nothing is accidentally off-slide (parking off-slide is deliberate; note it in the notes file).
- [ ] Photos are not stretched; crops keep the subject (focus point).
- [ ] Typography: no fallback font, diacritics intact, no heading broken mid-word, no single word alone on the last line of a title.
- [ ] Composition variety inside one system (craft.md §6): the same template on scene after scene is a defect; `check_deck.py` errors when the editorial-left template appears in more than 3 scenes.
- [ ] Every scene has a real visual (photo, screen, drawn TRUE motif). No stock icons or generic gradients standing in for content.

## 3. Accuracy (compare with `research/accuracy.md` and `facts.md`)
- [ ] Every object on a slide is on the TRUE list; count strings, pegs, beaters, hands and fingers.
- [ ] No WRONG-list motif (generic national symbols, neighbouring art forms, AI glow).
- [ ] No foreign script inside photos (look at pillars, plaques, signs, couplets) when the brief forbids it.
- [ ] Every number and claim matches facts.md, with its scope and caveat; nothing from the do-not-say list.
- [ ] User frames graded "never use" do not appear; "keep small" frames are ≤45% of the slide width inside a frame.
- [ ] Product: logo unaltered, version labels on screenshots, illustrations labelled as illustrations.

## 4. Motion (structure; the playback itself needs PowerPoint)
- [ ] `check_deck.py` per-slide lines show morph ms, entrances, and shared `!!` layers. A pair that shares a subject image and does not move it is an ERROR, not an info line. Look at the named slides.
- [ ] Planned durations applied (2000 ms on blooms and anchors); `motion.py` printed the motion.json it used.
- [ ] Blink only where planned; hand-made timing preserved for `keep_timing` slides.
- [ ] Final report says: "check Morph, entrances and blink in PowerPoint 365".

## 5. Language and licences
- [ ] On-slide language as in the brief (labels, captions, axes, credits too).
- [ ] Credit line on slides with CC BY/BY-SA photos; a credits slide lists them all; edited BY-SA marked "(đã chỉnh sửa)".
- [ ] CREDITS.md rows match the media actually embedded (check after finish: unused images removed, used ones present).

## 6. Timing
- [ ] `words_budget.py measure DECK --target M:SS` is within 10% of the target (or the overrun is accepted in brief.md).
- [ ] Anchor phrase spoken 3 times; pauses marked; the hook is not "Xin chào, hôm nay…".

## 7. Defect list format (`notes/<group>.md`)
```
# g3 (slides 6–8, S2 Vấn đề)
- round 1: slide 7 title collides with zoomed photo → title moved to x 6.8; slide 8 pillar text in photo → inpainted (01_clean)
- round 2: no visible defects; Morph durations 2000 on slide file 7 (bloom)
- left: Morph playback to check in PowerPoint
```
