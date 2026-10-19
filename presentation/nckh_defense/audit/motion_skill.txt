---
name: motion-pptx-studio
description: Build cinematic, professionally designed PowerPoint decks with real Morph motion (multi-slide keyframe scenes, a recurring signature object, entrances) plus a timed speaker script, for any kind of talk — product launches and demos, startup and contest pitches, business reviews and data stories, lectures and explainers, events and campaigns, culture and heritage. Use it whenever someone wants a presentation, slide deck or .pptx that must look designed rather than templated ("motion pptx", "Morph", "slide động", "thuyết trình chuyên nghiệp", "pitch deck", "ấn tượng", a contest, broadcast or investor deck), even if they never say Morph. Ships five style packs with Vietnamese-ready fonts, a deck engine with components, an asset kit, research and licence gates, layout and craft audits, and worked examples measured against an accepted reference deck.
---

# Motion PPTX Studio

Version 4.0.0. Python 3.9+, LibreOffice and poppler; works in any harness with a shell (Claude Code, Codex,
Cursor, Grok Bot, a plain LLM with tools: `references/harness-adapters.md`).

The standard comes from a real user and is kept word for word:

> "Tìm hiểu kỹ văn hoá Ca Trù để tìm và tải backgroud sao cho phù hợp nhé và đảm bảo độ chính xác tuyệt đối"
> "với các pptx chuyên nghiệp tôi đều thấy họ có nhiều cảnh nhiều motion, có khi nhiều slide để phục vụ cho một motion hoàn chỉnh, từng frame và mọi thứ, cần làm chuyên nghiệp nhé"
> "Trông chưa ổn lắm, cần chọn font cần tài nguyên asset, mọi thứ khác nhé" · "Ca Trù phải để tiếng Việt chứ nhỉ ?"

The accepted result of that standard is the reference deck in `assets/reference/` (48 slides, measured in
`references/reference-bar.md`). Look at it before you design anything. Every deck this skill makes should
hold up next to it.

## The one idea

**A motion deck is a short film shot on one set.**

1. **The set** stays the same on every slide: a material ground, a chrome (frame, page number, source
   line), a grid, a type system. A style pack holds it; the engine applies it. Morph can only show change
   against things that stay still.
2. **The signature** is one object that belongs to the subject — the instrument's three strings, the
   product's cursor, the headline number — living in the margin on most slides and becoming the hero at
   the hook, the turn and the close.
3. **The camera** moves inside each scene: 3–5 keyframes where the composition really changes (assemble,
   push in, walk the highlight, grow the bars, reveal the list), never one slide per idea with the words
   swapped.

Two ways this fails, both seen in delivered decks: **generic** (a default theme, stock icons, slogans, one
template on every scene) and **static** (Morph as a page turn, one screenshot held still while the words
change). The fix for both is the same: a real system, a real signature, real objects of the subject, and
scenes built as camera moves. `references/craft.md` gives the numbers.

## Size it first

Tell the user the size and a time estimate before any other work.

| Size | Slides | Effort | Do |
|---|---|---|---|
| Short | 8–15 (≤ 5 min talk) | 1–2 h | build it |
| Standard | 20–35 (5–12 min) | 3–6 h | say so, then build it |
| Long | 40+ (12+ min), or several decks | 6 h+ | propose a Standard version that keeps the core; build the Long one only when the user chooses it |

Have a rendered sample (Gate 3) within the first hour, and tell the user when a phase runs past twice its share.

## Non-negotiable rules

1. **No deck before Gate 4.** Brief, research, assets, design and storyboard come first. The sample deck of Gate 3 is the exception: it is how the design is chosen.
2. **Every claim traces to `research/facts.md`; every image to `assets/CREDITS.md`.** No source, no slide. Sources live in the storyboard's `source` column, the notes and the credits slide, not printed on content slides.
3. **Look at every image and every render yourself.** Titles, tags, file names and passing checks are not evidence.
4. **One system, one signature, many camera moves.** A scene is 3–5 keyframes; a shared subject image must move (box or crop ≥ 10% of the width, or a shared `!!` shape ≥ 6%, or ≥ 30% of pixels); one hold beat per scene at most; some `!!` layer on ≥ 60% of slides. `check_deck.py` measures all of it.
5. **On-slide language follows the audience** (Vietnamese topic, Vietnamese slides), including text inside photos.
6. **Budget speech in words, not seconds per slide** (130 wpm). Measure the script before delivery.
7. **Never overstate.** Status (finished, design-only, planned), results, licences and awards exactly as sourced; illustrative numbers and drawn screens say so.
8. **Ask the user at most once, at the start** (time limit, language, honest status, style if it matters). Otherwise choose a documented default in `brief.md` and tell them.
9. **Never game a check.** Do not edit thresholds, create placeholder files or copy rows to pass. The reference deck must pass every audit (`tests/test_audit.py`); a check that fails it is a wrong check, a deck that only passes checks is not done.

## Setup (once per machine)
```bash
bash scripts/setup.sh            # check: python-pptx lxml Pillow numpy fonttools python-docx cairosvg, LibreOffice, poppler
bash scripts/setup.sh --install  # install what is missing (pip --user, falls back to a venv)
```
Set `S=<absolute path of this skill>/scripts` and `WORK=<project folder>`. Every tool explains itself with `-h`.

## The pipeline

```bash
python $S/studio.py new WORK --kind heritage|product|pitch|business|education|event|other \
       --style lacquer-heritage|noir-product|paper-editorial|boardroom-data|studio-pop --title "…" --fonts
python $S/gates.py check WORK --gate N        # N = 0..6; FAIL means stop and do the missing work
```

### Phase 0 · Brief → Gate 0
Fill `WORK/brief.md`: topic, audience, kind, size, talk_minutes, on-slide language, forbidden items, **honest
status**, presenter, reference talk, user media, style, and **the user's own words verbatim**. Read any video,
form or repo the user gave first. Read the playbook for the kind in `references/genres.md`.

### Phase 1 · Research → Gate 1 (`research-protocol.md`, `cultural-visual-accuracy.md`)
`research/facts.md`: sourced facts, tagged `[verified]` / `[secondary]` / `[claim]` / `[disputed]` / `[uncertain]`,
with a **do-not-say list**. `research/accuracy.md`: the TRUE objects and motifs, the WRONG associations, an anatomy
checklist (heritage, product, education), and an audit of the user's media. Depth scales with the kind
(`genres.md`: heritage 15 facts from 3 domains … event 6 from 2). A reference talk → `research/lessons.md`.

### Phase 2 · Assets → Gate 2 (`asset-sourcing.md`)
Real, licensed images (`fetch_commons.py search/keep` writes CREDITS), at least twice as many looked at as kept,
rejected ones listed. Then make the deck's own materials with `make_assets.py`: `ground` (lacquer, noir, paper,
clean, halftone), `foil` (an SVG drawing of a TRUE object in gold, silver, ink, chalk, neon…), `layers` (one PNG per
moving part on one canvas), `photo` (duotone/sepia/mono + colour pair), `pattern`, `glow`. No openly licensed
imagery → illustrate from the TRUE list (labelled) or set `asset_scarcity` and shrink the deck.

### Phase 3 · Art direction → Gate 3 (`craft.md`, `styles.md`, `art-direction.md`, `reference-bar.md`)
- **Style**: start from the pack for the kind; make `design/style.json` the subject's own (sourced palette,
  fonts that pass `check_fonts.py --lang vi`, the same roles).
- **Signature**: write it under `## Signature` in `art-direction.md` — what it is, where it rests, what it
  becomes at the hook, the turn and the close, which `!!` parts it has.
- **Colour arc**: two grounds or a bloom, written as `S1-S4 #0E0A07 → S6-S11 #F1E4C8`.
- **Sample and compare**: turn the starter into your direction, `studio.py build WORK --group sample`, copy
  title and body renders to `design/samples/`, then `studio.py compare WORK WORK/renders/sample-1` and answer
  its questions. Change direction now, not after 40 slides.

### Phase 4 · Storyboard → Gate 4 (`storyboard-template.md`, `motion-grammar.md`, `speech-craft.md`)
```bash
python $S/words_budget.py plan --minutes 6 --slides 34     # → ~754 words total, ~22 per slide
```
`WORK/storyboard.md`: one row per slide — scene, keyframe role, composition (`layout`), `!!` layers, a real visual,
on-slide text, `source` (fact IDs), words, morph ms. 8+ scenes for talks of 5 min or more; ≥ 60% of scenes are runs
of 3+ keyframes, each a recipe from `motion-grammar.md` §4; distinct visuals ≥ scenes, none on more than 4 rows;
an anchor phrase on 3 slides; a colour arc; a circular close.

### Phase 5 · Build in groups of 2–4 scenes → Gate 5 (`build-engine.md`, `qa-checklist.md`)
Write `WORK/deck.json` against the style: components (`heading`, `card`, `stat`, `screen`, `timeline`, `bars`,
`list`, `quote`), roles instead of sizes, `col` instead of x/w, keyframes as `"from": "prev"` + `set`, `"scene"`,
`"ms"` and `"morph"` on the slides. When parts must line up (strings on a neck, a cursor that becomes the screen),
generate deck.json from a `make_deck.py`, as the examples do.
```bash
python $S/studio.py build WORK --group g1         # build → motion → pack → render (new folder) → audit with renders
python $S/studio.py compare WORK WORK/renders/g1-1
python $S/gates.py check WORK --gate 5 --group g1 --deck WORK/deck/preview-g1.pptx
```
Fix every layout warning first, then look: contact sheet, the comparison, every changed slide, 4× crops where
things meet (`craft.md` §12). Write defects in `notes/g1.md`, fix them in one pass, rebuild into `g1-2`.
Naming: `!!name` persists (Morph pairs it), `@fade|float|wipe<N>-label` enters, `@blink<N>-label` loops.

### Phase 6 · Finish and deliver → Gate 6 (`delivery.md`)
```bash
python $S/finish_dedupe.py WORK/deck/unpacked && python $S/ooxml.py clean WORK/deck/unpacked
python $S/ooxml.py pack WORK/deck/unpacked WORK/deck/final.pptx && bash $S/render.sh WORK/deck/final.pptx WORK/renders/final-1
python $S/words_budget.py measure WORK/deck/final.pptx --target 6:00
python $S/deliver.py WORK --deck WORK/deck/final.pptx --name Project_Motion --title "Kịch bản thuyết trình"
python $S/gates.py check WORK --gate 6
```
`deliver/` = `.pptx` + speaker-script `.docx` + `fonts/` (static TTF, OFL, install README) + `CREDITS.md` + `.zip`.

## Craft rules (short form; `references/craft.md` has the reasons and numbers)

- **Ground is a material**, never a flat fill; a second ground or a bloom marks the turn.
- **Chrome never moves**: frame or rule, page number, source line, at the same place on every slide.
- **One signature**, several `!!` parts, parked off-slide between appearances, paying off in the close.
- **Type roles only**: kicker 11–13 tracked caps · title 40–56, ≤ 8 words, the conclusion · body 15–17, ≤ 3 lines ·
  display/numeral for one word or one number. Two families. No orphan word on a title's last line.
- **One lit accent per frame**; contrast 4.5:1 for anything read; quiet text as a mixed solid colour (`fade`).
- **Composition varies, the system does not**: pick from the composition library; one focal point; a third of the frame empty.
- **Words**: the slide shows, the speaker tells. ≤ 30 words per keyframe; numbers with unit, period and source.
- **Imagery**: real → drawn from the TRUE list → nothing. Photos graded into the palette; drawn objects in one finish; screens in a device with a shadow.
- **Detail belongs to something**, ends on something, and rewards a 4× look; nothing floats.
- **Motion**: one primary move per transition; 1300 ms default, 2000 for assemblies, blooms and the close; ≤ 3 entrances, only for new information.

## Final message to the user (always)
Files delivered; slide and scene count; measured speaking time against the target; fonts to install;
**what must be checked in PowerPoint 365** (Morph, entrances and blink are invisible in LibreOffice renders);
decisions taken without asking; claims left out because they could not be verified; the audit's remaining warnings
and why they are deliberate.

## Reference map

| File | Read it when |
|---|---|
| `references/craft.md` | before Phase 3 and before every review: the set, signature, grid, type, colour, compositions, words, imagery, depth, data, anti-patterns, the critic's pass |
| `references/reference-bar.md` + `assets/reference/` | before Phase 3: what the accepted deck does, measured; how to compare |
| `references/genres.md` | Phase 0: arc, signature, evidence, research depth and traps for each kind of deck |
| `references/styles.md` | Phase 3: the five packs, changing one, a style from a brand board, all keys |
| `references/research-protocol.md` | Phase 1: source ladder, tagging, do-not-say list, product research |
| `references/cultural-visual-accuracy.md` | any cultural or heritage topic: true and wrong motifs, anatomy, user-media audit |
| `references/asset-sourcing.md` | Phase 2: where to search, licences, keep/reject, the asset kit |
| `references/art-direction.md` | Phase 3: style, signature, fonts, palette, motifs, layered objects, colour arc, samples |
| `references/motion-grammar.md` | Phases 4–5: camera language, Morph pairing, keyframe recipes, durations, entrances |
| `references/storyboard-template.md` | Phase 4: table format, scene structure, worked example |
| `references/speech-craft.md` | Phases 1/4: hook, anchor, pauses, circular close, word budget |
| `references/build-engine.md` | Phase 5: deck.json, components, generator scripts, OOXML editing, gotchas |
| `references/qa-checklist.md` | every render: layout warnings, audit, visual, accuracy, motion, language, licence, timing |
| `references/delivery.md` | Phase 6: package, fonts, credits, the hand-off message |
| `references/harness-adapters.md` | installing the skill; harness differences; weak-model mode |
| `examples/catru-mini`, `examples/product-launch`, `examples/data-story` | before building: the same bar in three styles, each with `make_deck.py`, `build.sh` and a contact sheet |
| `examples/case-catru-heritage.md`, `examples/case-neko-core-product.md` | the two delivered decks and every correction the user made |

Companion skills (optional, same repo): `heritage-visual-research` (Phases 1–2 alone) and `presentation-speech-craft`
(the script and the talk). Anthropic's `pptx` and `docx` skills are optional alternatives, never required.
