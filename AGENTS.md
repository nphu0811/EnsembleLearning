# NCKH IDS — Always-on WORKSPACE RULES (for sessions that are actually running)

Read `MASTER_PROMPT.md` before work. Treat it as the primary research contract. This file is a concise persistent pointer for Codex-like coding agents, not a background task scheduler.

At the start of every session:
1. Load `.research_memory/STATE.json`, `HANDOFF.md`, `TASK_BOARD.md`, `RESEARCH_CANON.md`, `DECISIONS.md`, and validate claimed outputs on disk.
2. Inspect the real installed skill registry. Read the exact `SKILL.md` and required references before logging that you used a Nature Skill. Skill folder and registered name may differ.
3. Identify the highest-priority unblocked task, execute it, produce artifacts, run checks, fix issues, update memory and continue within available run time.
4. NEVER fabricate papers, results, metrics, logs, skill executions, signatures or administrative facts. Never tune on the held-out test, or fit preprocessing/FS outside training folds.
5. Preserve `templates/original/`, raw data, frozen protocols and verified existing artifacts. Do not overwrite originals or silently restart completed phases.
6. The final deliverables are proposal DOCX/PDF based on the original 2026 form; LaTeX report PDF + sources based on provided template; reproducible Python project/results; defense slide deck/script/Q&A/demo; checksummed submission release.
7. Don't mark DONE without artifact + passing validation + evidence. Record blockers honestly and do independent work where possible.
8. No work persists after the interactive agent session ends; always save reliable restart instructions to `.research_memory/HANDOFF.md`.

If a required original user-uploaded ZIP or document is missing, record its location as `AUTHOR_INPUT_NEEDED` and work on other valid tasks. Do not hallucinate the contents.
