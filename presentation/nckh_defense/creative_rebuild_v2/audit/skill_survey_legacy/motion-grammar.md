# Motion grammar (how the deck moves)

"Có khi nhiều slide để phục vụ cho một motion hoàn chỉnh, từng frame và mọi thứ." Professional motion decks
are animated films cut into slides: each slide is a **keyframe**, and Morph interpolates between them.

## 1. Vocabulary
| Term | Meaning |
|---|---|
| Scene | one idea of the talk (Hook, Problem, Meet the hero, How it works, Proof, Close) |
| Keyframe run | 3–5 consecutive slides of one scene; same composition, objects move between them |
| `!!name` layer | a shape with exactly the same name on neighbouring slides; Morph moves, resizes, rotates and recolours it |
| Component part | `!!h.title`, `!!b.bar2`, `!!tl.dot1`: parts named by the engine from a component's name; set the component, the parts move |
| `@fade3-label` | entrance effect, order 3 (fade, float or wipe); plays after the Morph, 220 ms stagger |
| `@blink2-dot` | an emphasis loop that blinks forever (cursor, live dot, "recording" light) |
| Parking | an object waiting off-slide (x ≥ 13.6 in or y ≤ -2 in) so it can fly in via Morph; audits ignore it |
| Hold beat | a keyframe pair where the picture holds still and only the words change (a question, then its answer) |

## 2. Camera language (what a scene is for)
A scene is a shot. Decide what the camera does before you place anything:
- **Establish → detail → reveal.** Show the whole, move in on the part that matters, then show what it means.
- **One primary move per transition.** The thing the audience should follow moves the most; everything
  else holds or follows a little (secondary motion: a caption fades in after the move lands).
- **Distance sets duration.** Small moves 1000–1300 ms; across-the-slide moves and size changes ×2 or
  more 1500–1800 ms; a colour bloom, an assembly or the close 2000 ms.
- **Direction means something.** Forward in time = left to right; zooming in = into detail; lifting
  (a card moves up 0.2–0.25 in) = attention.
- **Let it land.** Entrances start after the Morph (motion.py staggers them from 350–500 ms); no more
  than 3 per slide; persistent objects never get entrances.

## 3. How Morph pairs objects
- Morph pairs shapes whose **names match** (with the `!!` prefix the pairing is by name only). Shapes with
  no partner fade in or out.
- Names must be **unique per slide** (`check_deck.py` errors on duplicates) and keep the same **kind** on both
  slides (picture↔picture, text↔text, group↔group; a picture that turns into a shape will not morph).
- Text in a paired text box morphs as a whole by default (`byObject`). Set `"morph": "byChar"` on the
  slide to morph letter by letter ("31%" → "2×" → "2,4"; "Ca trù" → "2009"), or `"byWord"` to move the
  words two slides share. The option applies to the whole transition into that slide.
- Images morph best when they are the **same image file**: crop, scale and position change smoothly.
  A different image under the same name cross-fades.
- Groups (cards, screens) morph as one object: move, scale and recolour the whole card.
- `!!` names that appear on only one slide are "lonely" (`check_deck.py` warns). That is fine for a
  deliberate entrance or a component part that only exists in one keyframe (a bar's value label).

## 4. Keyframe recipes (each = one scene of 3–5 slides)
| Recipe | K1 → K2 → K3 (→ K4) | Engine |
|---|---|---|
| Assemble | parts scattered or parked → drifting closer → locked together + title arrives | layered PNGs with the same box; strings as `line`s computed from the object's box |
| Push-in | full-bleed photo → 1.25× with an offset (box or crop moves ≥ 10% of the width) → detail + label | `image` with a changed box or `focus` |
| Highlight walk | 3 cards at rest → card 1 lit and lifted → card 2 → card 3 | `card` × 3, `set` `state` lit/dim and `y` |
| Counter | big number 1 → 2 → 3, the line under it changes | `stat`, `"morph": "byChar"` |
| Bar grow | bars at 0 → grown with values → one bar highlighted | `bars` `grow` 0 → 1, then `highlight` |
| Reveal | 1 item → 2 → 3, earlier items quiet | `list` `reveal` k, `focus` i |
| Colour bloom | muted (veil 60–70%, mono hero parked) → hero lands in colour with a 2 s Morph | a second ground or `_mono`/`_color` pair under one name |
| Timeline walk | the signature lies down into a rail → the active node walks 1 → 2 → 3 | `timeline` `active` i |
| Screen tour | screen whole → zoom on the part that matters (+ a lit callout) → back out | `screen` component box changes; a `rect` ring `!!hl` |
| Book | closed cover → pages open → a screen appears inside the open book | `!!pageL/!!pageR` rects + framed image |
| Zoom to detail | object whole → enlarged so one part fills the slide (+ ring `!!hl`) → back out | same image, bigger box, off-slide overflow allowed |
| Hold | the picture stays; the words change (question → answer) | at most one per scene and 10% of transitions (audited) |
| Circular close | the opening keyframe again; objects return to their first positions | copy the first slide's shapes with `"from": "<first id>"` |
Every scene should use one of these, or a variation. The 48-slide ca trù deck had 14 scenes; the 34-slide neko deck had 10.
The storyboard `visual` cell is the dominant image of that row. Naming one file on five rows fails Gate 4 even when the run is a legal Morph: stop at 4, or bring in a second visual.

## 5. Durations
Plan them on the slides in `deck.json` (`"ms": 2000`, `"morph": "byChar"`, `"keep_timing": true`);
`build_deck.py` writes `deck/motion.json` with the right file numbers. A `WORK/motion.json` keyed by
slide FILE number still works and sits underneath.
```json
{"default_ms": 1300, "stagger_ms": 220, "dur": {"3": 2000}, "option": {"7": "byChar"}, "keep_timing": [50]}
```
- 1300 ms default (the style pack may change it); 1500–1600 for intro keyframes; **2000 for blooms,
  assemblies, the anchor moments and the close**; 1000 for quick counters.
- Keys are slide **FILE** numbers (`slide12.xml` → `"12"`). After `ooxml.py sequence` they differ from
  deck positions; `ooxml.py order DIR` prints the mapping.
- `motion.py` looks for motion.json in the unpacked folder, then its parent (deck/), then WORK, and
  prints which one it used.

## 6. Entrances and loops
- Entrances are for **new information** on a keyframe (a caption, a source line, a callout). Persistent objects move with Morph; don't give them entrances.
- Order numbers run from 1 per slide. Keep it to 3 entrances per slide at most; the talk has a time budget.
- `@blink<N>-label`: one living detail (a terminal cursor, a "live" dot). One per slide at most.
- Hand-made animation: `"keep_timing": true` on the slide and `motion.py` leaves its `p:timing` alone (it still sets the Morph).

## 7. What motion.py guarantees
- Exactly **one** transition per slide (Morph wrapped in `mc:AlternateContent` with a fade fallback for old versions).
- It removes every older transition first, so it is **idempotent**: run it after every edit (`studio.py build` does).
- `p:timing` is rebuilt from the `@` names unless the slide keeps its timing.
- XML order inside `p:sld`: cSld, clrMapOvr, transition, timing, extLst.
Check: `check_deck.py` reports morph ms, entrances and shared layers per slide, and errors if a slide has 0 or 2+ transitions.

## 8. Limits (say them to the user)
LibreOffice renders static frames only: Morph, entrances and blink are visible **only in PowerPoint 365 / 2019+**
(Keynote and Google Slides ignore Morph). The render proves layout; the user must play the deck in PowerPoint.
