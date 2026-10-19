# Speech craft (script, timing, delivery)

The deck supports a talk. A gorgeous deck with a 12-minute script for a 6-minute slot fails. A good talk
is what makes the slides land.

## 1. Learn from a reference talk (when the user gives one, or pick one)
Watch the real video (yt-dlp + subtitles + `video_frames.py`) and write `research/lessons.md` with timecodes.
The reference used in both case studies: Dananjaya Hettiarachchi, "I See Something", Toastmasters World
Championship of Public Speaking 2014, https://youtu.be/-wLEsZWevrA. Observed techniques:
- **Opens with a prop and a sense** (a rose crushed and dropped in a bin), not with a title or "hello, today I will…".
- **One anchor sentence repeated** (four times) at structural moments.
- **Emotional ups and downs**: humour, then quiet, then humour.
- **Marked pauses** of 2–3 s after the key lines.
- **Fixed stage positions** per part of the story; the message is spoken through characters' lines.
- **Circular close**: a whole rose taken out of the same bin.
- He used **no slides at all**, so in a deck the slides must play the role of the prop and the stage positions.

## 2. Translate to the deck
| Technique | In the deck |
|---|---|
| Prop / sense hook | slide 1 = one object in darkness (a string, a cursor) + a spoken question; no title yet |
| Anchor phrase ×3 | `!!phrase` on 3 slides (setup, middle, end), said aloud each time; check with `check_deck.py --anchor` |
| Ups and downs | alternate muted problem scenes with the playful hero (mascot) scenes |
| "Muted to colour" magic | colour arc: veil and greyscale, then a 2 s bloom when the hero appears |
| Pauses | write `[ngừng 2 giây]` / `[pause 2s]` in the notes; they are counted as time, not words |
| Circular close | the last scene repeats the first keyframe with the object restored |

## 3. Word budget (the rule that fixes the biggest timing failure)
Measured reality: the ca trù deck was planned as "48 slides × 7 s = 5.6 min" and the script ran **11:53–13:36**
(1663 words + 24 pauses). The neko deck was planned at ~6 min and ran **8:28** (1088 words). Seconds per slide
do not work with Morph decks because there are many silent keyframes.
```bash
python $S/words_budget.py plan --minutes 6 --slides 34          # ~754 words, ~22 per slide (130 wpm, 6 pauses)
python $S/words_budget.py measure WORK/deck/final.pptx --target 6:00 --scenes WORK/deliver/scenes.json
```
- Vietnamese speaking pace for presentations: 130 wpm (careful) to 150 wpm (fluent). Plan at 130.
- Keyframes inside a run often carry 0–10 words; the first slide of a scene carries the idea.
- Lines starting with Nguồn, Source, Ảnh, Photo, Motion, Ghi chú, Note, Cue or Credit are not counted (directions and sources).
- `measure` exits 1 when the estimate is more than 10% over target: cut words from the heaviest slides it lists.

## 4. Notes format (per slide)
```
[Cảnh 2 · Vấn đề]
Agent viết code ngày nay rất giỏi. Nhưng nhiều khi nó làm trước, rồi mới báo.
[ngừng 2 giây]
Nguồn: README.md (F2.2) https://github.com/...
```
Short sentences, one idea each, spoken language (not written prose). Claims marked `[claim]` in facts.md
are framed as "chúng tôi thiết kế để…" / "the team says…".

## 5. Speaker-script document
`deliver.py` exports the notes and runs `script_docx.py`, which writes a .docx with scenes, slide numbers, spoken
text, grey source lines, pause marks and a per-scene time estimate. Give it to the presenter with the deck.

## 6. Delivery tips to pass on (contest video or live)
Look at the lens on the hook question; let each Morph finish before speaking; stand still during the
anchor phrase; rehearse with a timer twice; the last sentence is the anchor phrase, then silence.
