# NCKH defense Creative Rebuild V2 — independent artifact acceptance

Date: 2026-10-19. This review continues an interrupted Codex session without rerunning training or overwriting the original presentation.

## Outcome: PASS_BINARY_TECHNICAL_AUDIT

- **GitHub Actions:** https://github.com/nphu0811/EnsembleLearning/actions/runs/39209607511
- **Independent read-only source:** [tools/verify_creative_release_portable.py](../../tools/verify_creative_release_portable.py), Python stdlib + `ffprobe` + `pdfinfo`.
- **Input:** committed binaries under `presentation/nckh_defense/creative_rebuild_v2/` from author commit `3795580`; the checker opened the actual files, not just claimed stats.

| Checked property | Independent observed result |
|---|---:|
| PowerPoint slides | 29 (17 main + 12 hidden Q&A) |
| Main slides with native timing and effects | 17/17 |
| Native animation effects | 439 |
| Native motion paths | 59 |
| Native scale events | 15 |
| MP4 duration | 360.000 seconds |
| MP4 resolution | 1920×1080 |
| MP4 audio track | Present |
| Humanized research PDF V7 | 49 pages; original SHA-256 matched |
| Static slide PDF | 29 pages |
| SHA manifest entries | 292 |
| Original ZIP members with correct SHA | 292/292 |
| Delivery ZIP CRC | PASS |
| LaTeX source ZIP CRC | PASS |
| Git LF/Windows CRLF normalized text | 100 files (reversible) |
| Known post-package regenerated summary | `audit/release_validation.json` |

**Explanation of the text hash exception:** The ZIP contains the author's original Windows bytes and all original manifest SHA values match. Git checkout normalizes 100 committed text files from CRLF to LF; this was verified by reversing that precise conversion rather than disabling integrity checks. The package-building script writes `audit/release_validation.json` after final ZIP creation to include the ZIP digest. It is the **sole allowed post-package mutable text report**; the member inside ZIP is itself hash-verified. PPTX, MP4, PDFs and original ZIP bytes have no exceptions.

This is a technical binary-integrity and internal-animation structure PASS. It does **not** confirm visual aesthetic merit, Vietnamese narration pronunciation, how PowerPoint behaves on the event PC, or effectiveness of IDS deployed on actual network traffic. PowerPoint's internal animation effects and observed MP4 motion are separate from human acceptance of their aesthetic quality.

## Last actions before defense

- Download the `creative_rebuild_v2` PPTX and MP4, **not** the older parent-directory pair.
- Listen to the entire voiceover and verify English ML terms/UNSW-NB15, and all numbers. Earlier automatic ASR was noisy; audio correctness remains human-PENDING.
- Run the slideshow using Microsoft PowerPoint desktop with **Use Timings**; verify 6-minute autoplay. PPTX narration is not embedded; live speaker uses the script.
- Check A1–A12 appendix hyperlinks and return to conclusion.
- Rehearse the spoken Vietnamese version on the same projector/PC before presentation.
- Report V7 is a *wording-humanized candidate* pending final adviser signoff; original V6 was preserved.

For the eight-scene timeline and direct artifact links, see `presentation/nckh_defense/creative_rebuild_v2/DEFENSE_FINAL_HANDOFF_V2.md`.

**No new model fits, official TEST accesses, frozen-data alterations or unfounded independent validation claims occurred in this acceptance.**
