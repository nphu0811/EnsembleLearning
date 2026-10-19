# P19 reproducibility and availability review — 17/10/2026

**PARTIAL; NOT_READY_FOR_SUBMISSION.** Applied `nature-data` to the existing
availability statement and its current provenance claims. No final archive,
distribution license, DOI, release tag or publication approval is invented.

The root README now distinguishes historical scientific outputs, local reconstructed
full-TRAIN artifacts, read-only postprocessing QA and approved-report provenance.
The P16 requirements file explicitly describes the observed QA environment, not
the original training environment or a complete hash-locked dependency closure.
The Nature audit scripts and Poppler are documented external dependencies.

## Data availability draft, separate from the locked manuscript

This research uses the official UNSW-NB15 TRAIN/TEST files. Their original source
and dataset publication are documented in `docs/research/DATASET_PROVENANCE.md`
and the checked U01 bibliography record (DOI 10.1109/MilCIS.2015.7348942). Raw data
are not included in this new review bundle. Saved historical summary tables,
statistical outputs, source-to-display maps and QA reports are present in this
repository. Newly generated figure source CSVs are copied byte-for-byte from those
summaries and include SHA-256 manifests. Repository access is distinct from
permission to redistribute third-party data or source papers.

## Code availability draft

The source repository is `https://github.com/nphu0811/EnsembleLearning`. Source
versions can be identified by Git commits and the QA manifests. No archival DOI
or final release tag is confirmed. Project code licensing remains unconfirmed;
public visibility alone is not an open-source license. Three reconstructed model
files are retained on the author's laptop, with SHA/byte metadata and read-only
acceptance reports in the repository. They are not original historical models,
not included for redistribution, and not claimed to reproduce historical TEST
probabilities. Original training environment remains UNKNOWN.

## FAIR and release gates

| Item | Current evidence | Remaining boundary |
|---|---|---|
| Findable | Repository, commit identifiers, figure/report hashes | No archival dataset/code release identifier |
| Accessible | Saved CSV/JSON/code and source locations | Dataset route/license and third-party redistribution need confirmation |
| Interoperable | CSV/JSON/Python, metric units, captions and display map | Full historical heatmap matrix not saved in summary tables |
| Reusable | Source manifests, QA scripts, observed QA dependencies | Code license, training environment identity, complete dependency lock |
| Model provenance | Three TRAIN-only reconstructions; acceptance 69/69 | No historical binary identity or new TEST validity claim |
| G4 | Technical PDF and saved-result QA | P18 reading depth/novelty and print/snapshot-age findings |
| G5/G6 | Approved report preserved; text defense materials exist | Proposal form/render, institutional acceptance/signatures, slides and demo |

Release inventory is a review snapshot with hashes and distribution-review flags,
not a statement that every tracked file is authorized for redistribution. It does
not bundle datasets, venvs, credentials or model binaries. Existing third-party
templates, paper captures and historical ZIPs must not be assumed redistributable.
No FINAL_NCKH archive is built and no gate is promoted merely by producing a
manifest. Dataset/model licensing decisions remain author/rightsholder inputs.

### Actual inventory finding

The first tracked review snapshot contains **869 files** and **FAILS** its
forbidden-path check for three already tracked historical binaries under
`results/reproducibility/r04_ml_smoke_repaired/smoke_models/`:
`random_forest_17_SMOKE_ONLY.joblib`, `random_forest_42_SMOKE_ONLY.joblib`,
`stacking_42_SMOKE_ONLY.joblib`. No code LICENSE is tracked. This is evidence of
an existing release hygiene gap, not a failure of the P15 reconstructed artifacts
(which remain local). No new model binary is staged in this session. No model is
loaded or removed, and no historical Git cleanup is performed. Resolve whether
to retain historical smoke evidence locally and remove it from future releases
without deleting the author's physical copies. The review manifest itself is
retained with `passed=false`; a passing new-file staging check must not be used
to relabel the whole repository inventory PASS.

P20 final multi-context simulated panel is deferred pending a fixed review packet,
source-reading boundaries and release inputs. Its output must state AI simulation,
not actual external professors, institutional endorsement or publisher acceptance.
