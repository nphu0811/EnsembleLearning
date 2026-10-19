# Research protocol (Phase 1 → Gate 1)

Research is the work that gives a deck its visual richness and its pull. Without facts there are no
specific images, without specific images the slides fall back to generic decoration, and generic
decoration is what makes a deck look "AI-made". Do this phase fully, even when the user only says "make slides".

## 1. Read what the user gave you first
- **Submission forms, contest rules, briefs**: copy the exact requirement text into `brief.md`. In the ca trù
  project the contest asked for "Video đội thi thuyết trình về sản phẩm đã hoàn thành để phục vụ công tác chấm
  điểm và phát sóng". That one sentence set the format (a recorded talk), the audience (judges plus TV) and the
  licence policy (broadcast, so no NC images).
- **Videos**: `python $S/video_frames.py video.mp4 --out WORK/research/frames --every 5 --sheet`. Look at every
  frame and write what is really shown (characters, objects, on-screen text, chapter titles). Later, the media
  audit in `accuracy.md` grades each frame.
- **Repos**: README, CHANGELOG, releases, docs/, the site, the brand board, issue templates. Note version
  numbers and dates exactly, and convert UTC to the user's zone.
- **Earlier decks or documents by the user**: reuse their names, spellings and terminology.

## 2. Source ladder (search in this order; cite the highest rung you reach)
| Rung | Heritage / culture | Product / tech |
|---|---|---|
| 1 primary | UNESCO nomination file and decision text (ich.unesco.org), national heritage institute, the museum record | the repo itself (code, README, CHANGELOG, LICENSE, release assets), the official site |
| 2 institutional | national museums (e.g. Bảo tàng Dân tộc học), universities, state media cultural sections | official docs, maintainers' posts, package registries |
| 3 scholarly / quality press | books, journal articles, long-form features with named experts | reputable tech press, benchmark pages with the method stated |
| 4 secondary | blogs, travel sites, Wikipedia (use it to find rung 1–3 sources, not as the final citation) | social posts, forums |

Search in **the local language and in English**, with and without diacritics ("ca trù", "ca tru",
"Ca tru singing", "hát ả đào"). Fetch the page itself (WebFetch, curl or a browser) and quote it. A search
snippet is not a source. Save raw pages in `research/` (`*.html`, `*.txt`) so a fact can be re-checked later.

## 3. Write `research/facts.md` (template provided by `gates.py init`)
- Number the sources: `(U1) UNESCO decision 4.COM 14.12 — https://...`. Facts cite the ID and the URL. Gate 4 requires at least 40% of storyboard rows to carry one of these IDs (or a table id such as `1.1`) in the on-slide text, not only in the speaker notes.
- One fact per row, short, with a tag:
  - `[verified]`: primary or institutional source, or two independent rung-3 sources
  - `[secondary]`: press or blog only, so phrase it carefully or leave it off the slides
  - `[claim]`: the owner's own words (README, website, the user's submission). Present it as "the team says…" or "designed to…"
  - `[disputed]`: sources disagree; write both versions and pick the one you will use
  - `[uncertain]`: keep it off the slides, or ask the user
- Record **exact wording** for official names and labels (for example the UNESCO list title in Vietnamese) and use it verbatim on the slide.
- Record **numbers with their scope**: "12/12 on HardMix-12, one run, one model, run by the owner" and not just "12/12".

## 4. The do-not-say list (required, at least 3 items)
Write what the deck must not claim, even though it is tempting. From the real projects:
- *Heritage*: "Lỗ Khê đình thờ tổ ca trù" (wrong, it worships another figure); a typo year copied from a press
  article; "cô đầu" in a title (pejorative connotation); modern province names for historical places (use the
  borders of the year the source describes).
- *Product*: a win, rank or award that was never published; "N stars/downloads" with no source; "Apache SDK
  published" when only a folder exists; "the auto mode is an AI classifier" when it is an allow-list; "works
  offline" without "only with a local model"; an outdated licence badge from an old social-preview image.

## 5. Gaps
List what you could not verify. Leave it off the slides, or mark it as the team's claim in the speaker notes.

## 6. Product decks: extra checks
- Read the CHANGELOG and releases for the **current** version and dates; the README can lag behind.
- Distinguish shipped, behind a flag, opt-in, and planned. Write the status in `brief.md` → `honest_status`.
- Use real screenshots from the product (label the version). An illustration of a terminal session is labelled "Minh hoạ" or "illustration".
- Benchmarks: name the suite, the subset, the model, the number of runs and who ran it, and keep the caveat on the slide.

## 7. Time-box
For a contest or pitch deck of 5–15 minutes, research takes 20–30% of the total effort. It is cheaper than
rebuilding after the user notices a wrong drum (it happened: the first ca trù art direction used the Đông Sơn
bronze drum, and the whole visual family had to be rebuilt).
