# P18 — UNSW-NB15 dataset references U01 / U03 metadata follow-up (2026-10-16)

Scope: DOI, author/title, pages and publication-year semantics of two sources listed in `literature/verification_2026_10_16/dataset_references.bib`. This is a fresh source-field check, **not a whole-paper read** or statement that the full bibliography and P18 are DONE. Original r02/r04 captures are preserved.

## U01 — Moustafa & Slay (2015)

**DOI:** `10.1109/MilCIS.2015.7348942`  
**Title:** UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set).  
**Fields checked:** authors Nour Moustafa / Jill Slay, event MilCIS 2015, year 2015, **pages 1–6**, publisher IEEE.

- IEEE Xplore publication landing via DOI: https://doi.org/10.1109/MilCIS.2015.7348942 — title, authors, venue, year, DOI and publisher identifiable; page range may be absent from public HTML.
- University of Adelaide research repository: https://digital.library.adelaide.edu.au/items/d4e54baf-85d4-4e46-9028-e8ca66c9f46b — explicitly records `pp.1–6` and the same DOI/title/year.
- Curated DBLP: https://dblp.org/rec/conf/milcis/MoustafaS15.html — corroborates venue/year/pages1–6 and two ordered authors.

**Disposition U01:** **VERIFIED_METADATA_IN_THIS_SCOPE**, including previously warning-flagged pages 1–6 through a separate university-hosted institutional record plus IEEE title/DOI/publisher. Not a full-text validation of methods; not a confirmation of raw CSV license or exact download history.

## U03 — Moustafa, Slay & Creech (2019 journal issue)

**DOI:** `10.1109/TBDATA.2017.2715166`  
**Title:** Novel Geometric Area Analysis Technique for Anomaly Detection Using Trapezoidal Area Estimation on Large-Scale Networks.

- Curated DBLP: https://dblp.org/rec/journals/tbd/MoustafaSC19 — citation **IEEE Transactions on Big Data 5(4): 481–494 (2019)**.
- CiNii Research indexed journal metadata: https://cir.nii.ac.jp/crid/1360857702273971328 — publisher IEEE, official journal issue **5(4)**, publication date **2019-12-01**, pages **481–494**, DOI ending in `.2017.2715166`.
- University of Utah curated journal bibliography: https://ftp.math.utah.edu/pub/tex/bib/ieeetransbigdata.html — lists volume5, issue4, pages481–494, Dec2019 and DOI.

**Disposition U03:** **VERIFIED_FINAL_YEAR_AND_PAGINATION_BY_MULTIPLE_METADATA_INDICES; PUBLISHER_VOR_NOT_VISUALLY_CHECKED**. The DOI contains 2017 and early-online indexing could say 2017; **that does not change final-volume publication year 2019**. This source does not establish a new research result nor imply direct full-paper review. Direct IEEE journal PDF version-of-record was not visually inspected in this task.

## Consequences / evidence closure boundary

The above supports keeping fields already recorded in `dataset_references.bib`: U01 pages1–6, U03 year2019 5(4):481–494. Nothing in the original file was silently rewritten; it already contained those values. For a report citation, U01's original BibTeX record may be reused with the new field-level evidence, but its provenance should state only verified metadata.

`L03` remains a different conflict, documented in `literature/L03_PAGE_CONFLICT_FOLLOWUP_2026-10-16.md`. The new independent institutional checks strongly support 254–263, but Crossref/older project record still differs; no publisher final-PDF direct check.

**P18 STATUS:** PARTIAL overall. This task resolved the scoped U01 page-range warning and strengthened the U03 final-year field verification; it does not close L03, bibliography QA, reading depth or overall systematic literature review.
