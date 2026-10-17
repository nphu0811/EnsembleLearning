# P20-PRE common assessment contract

AI-simulated internal scientific criticism only. This is not a real human council,
editorial decision, publication certification or P20 final acceptance.

## Fixed source basis

Read only `packet_02/local_contents/` inside this task directory, its adjacent
`manifest.csv` and `receipt.json`, this contract, and your own emphasis brief.
The packet manifest SHA256 is
`c0f0b3828ba16ce8312b489915cc4c56c9fc7c771dbeefe1d7a9bb78938b62b7`.
There are 80 files, including the unchanged author-approved 37-page report.
`approved_report_pages.txt` uses physical PDF pages, not printed page numbers.
The PDF is authoritative if extraction and visual content disagree. Report source
chapters include historical/unused files; `report/main.tex` establishes active
inputs. Do not treat an unused chapter as a current manuscript claim.

Frozen tables include weighted F1 and AUC in P11, confusion matrices, P9 costs,
P10 paired bootstrap/McNemar/Wilson summaries, development CV, feature selection,
overlap/views, model source and freeze configurations. Read source without running
it. The P15 acceptance and three run reports are author-host records, not model
bytes. Original historical environment is not established by those records.

Literature catalog records exact reading scope. `literature_reported_facts.csv`
retains publisher-reported facts and locators from existing verification; these
are paraphrased secondary notes, not complete papers or independently replicated
external experiments. Abstract-only records cannot support unseen Methods claims.
No additional internet retrieval is part of this bounded pass. Missing full text
or VOR must stay missing. Do not infer field-wide novelty from an incomplete search.

No prior reviewer report, shared concern ledger, prior QA conclusions, draft
synthesis or other reviewer's emphasis is supplied. Do not inspect any sibling
output, research memory, old QA report or earlier defense Q&A outside the packet.
The processes share a filesystem. Separation is at invocation/context level and
depends on this access contract, not an OS permission barrier or different model
providers. Never assert independent human confirmation or broader blinding.

## Common criteria

Evaluate originality, scientific importance, technical soundness, relevance to
readers in IDS/ML/reproducibility, and readability for nonspecialists. Nature-style
axes are a methodological lens. This task does not target a Nature editorial
decision. Assess all axes, giving extra attention to your supplied emphasis.

Load the exact installed `nature-reviewer/SKILL.md` and its workflow, technical
taxonomy, engineering gates and QA references. For statistical reporting use
`nature-statistics/SKILL.md` and statistical-reporting/common-failure-modes as
applicable. Skills are instructions, not manuscript evidence. Use Vietnamese for
the main report. No identities, credentials, affiliations or invented observations.

Every concern must be evidence-grounded. Independently decide concern count;
there is no concern quota. Distinguish an actual manuscript overclaim from an
unsupported hypothetical extension. A disclosed limitation may remain a limitation
without being a factual error. Do not infer equivalence from a nonsignificant test.
Do not count development folds, bootstrap draws or benchmark rows as independent
training or network/session repetitions without evidence of that unit.

Do not train, import/execute ML scripts, open raw data or row-level prediction
CSVs, retune, rerun bootstrap, load models, alter frozen sources, change the PDF,
edit bibliography, choose LICENSE, delete/untrack files or publish a package.
You may create only your own new report files in the output directory provided.

## Report contract

Produce `report.md` and `report.json` in your assigned new reviewer directory.
Include overall scientific assessment, demonstrated strengths with pointers,
Major Concerns, Minor Comments, unsupported claims, document/interpretation-only
repairs, matters requiring a new approved experiment, at least ten deep defense
questions, assessment of all common criteria, audience and conditional recommendation.
Recommend MAJOR_REVISION_REQUIRED, NOT_READY or ACCEPTABLE_WITH_LIMITATIONS only
when justified. Do not automatically accept and do not grant P20 final closure.

JSON structure must have `reviewer`, `scope`, `packet_manifest_sha256`,
`overall_assessment`, `criteria_assessment` (five named axes), `strengths`,
`concerns`, `unsupported_claims`, `document_repairs`, `new_experiments_needed`,
`questions`, `taxonomy_coverage`, `recommendation`, `skills_read`.

Each concern object must contain `id` (A-M1/A-m1 or B/C), `severity`
(`MAJOR`/`MINOR`), `blocking` (boolean, false for Minor), `axis`, `issue_key`,
`claim_pointer`, `evidence_status` (VERIFIED/PARTIAL/UNVERIFIED/BLOCKED/
NOT_APPLICABLE), `evidence` (nonempty list), `concern`, `why_it_matters`,
`acceptance_test`, `resolution_route` (DOCUMENT/NEW_EXPERIMENT/BOTH/EXTERNAL),
`status` (`OPEN`), and `severity_rationale`.

Each evidence item must contain `path` relative to local_contents, `locator`
(verified page/section/table/row/function) and `anchor` (a short exact literal
substring of that text source). Use a supporting .tex/.py/.csv/.json or extracted
page text anchor even when the claim originates in the PDF. Never invent a line
or number. For unavailable evidence state that boundary explicitly and anchor the
availability record. Questions are objects with `id`, `question`, `evidence`
using the same pointer shape. Strengths should also contain evidence pointers.
Taxonomy coverage gives applicable/not applicable/not assessable for all 12 axes.

Finalize your report without reading other reports, then stop writing. Parent
will hash/freeze it and perform a separate synthesis only after all three finish.
Do not revise to manufacture difference or remove overlap. Avoid lengthy verbatim
quotes from third-party literature; use source-grounded paraphrases and links.
