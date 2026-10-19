# P15 — Scoped closure: reconstructed full TRAIN + independent author-host artifact acceptance

**Ngày QA:** 17/10/2026.
**Kết luận chính:** **P15 = DONE_SCOPED_RECONSTRUCTION** (huấn luyện lại toàn bộ official TRAIN cho 3 frozen candidates và kiểm tra artifact trên laptop của tác giả).
**Không phải** ORIGINAL historical artifact / historical bitwise model equivalence / fresh scientific TEST evaluation / publication- or demo-release approval. **G3 tổng thể vẫn PARTIAL đối với original environment, provenance fidelity và release/demo gate.**

## Phạm vi bằng chứng

1. Commit tác giả chứa ba full-run logs: [`d090c163a3c20f5637a8e500fdb7afc552ddbe9f`](https://github.com/nphu0811/EnsembleLearning/commit/d090c163a3c20f5637a8e500fdb7afc552ddbe9f); mỗi full-run có `run_report.json`, `worker/worker_result.json`, `start.json`, `resources.csv`. Độc lập đối chiếu file nguồn đạt **75/75 phép so khớp báo cáo/log**; xem `docs/research/THREE_FULL_TRAIN_AUTHOR_EVIDENCE_QA_2026-10-17.md`.
2. Commit tác giả chứa file acceptance mới: [`c81f99a548045d0f6900bec65509ad35da32a073`](https://github.com/nphu0811/EnsembleLearning/commit/c81f99a548045d0f6900bec65509ad35da32a073), `results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json`. Báo cáo do `tools/p15_verify_full_artifacts.py` chạy trên **host tác giả** trả `passed=true`, `training_performed=false`, `official_test_opened=false`.
3. Kiểm tra riêng từng mô hình trên metadata đã push: **69/69 item.checks = true** (RF17 20/20; RF42 20/20; Stack42 29/29). So khớp kết quả acceptance với `worker_result.json` và `run_report.json` của từng mô hình: model name/full TRAIN 175341, reported SHA256+bytes, input SHA, environment versions, source/feature/threshold, reported run PASS đều nhất quán.
4. Công cụ verifier được kiểm thử fixture-only trên GitHub Actions Windows Python3.11: [run 38986685352](https://github.com/nphu0811/EnsembleLearning/actions/runs/38986685352) **21/21 watchdog + 6/6 verifier unit tests PASS**, source compile và PowerShell script parse PASS; **CI không có các model thực và không hề train**.

## Summary of reconstructed candidates

| Candidate | TRAIN rows / feature count | Fit time (s) | Peak sampled process-tree RSS (MiB) | Reported model bytes | SHA-256 from author-host verifier |
|---|---:|---:|---:|---:|---|
| `random_forest_17` | 175341 / 17 | 307.453 | 510.24 | 22169429 | `b2751bfc6677a724bcadc85070e5848c0f183c3c81d508b5e4cdae82287c8818` |
| `random_forest_42` | 175341 / 42 | 1867.234 | 693.57 | 42207326 | `9509b1561e50488c756ac986595da4efd9f75a8ede6a8fc4c1f04f15ce85ef8d` |
| `stacking_42` | 175341 / 42 | 4759.094 | 725.33 | 42368839 | `cb0d9b6c50ca19f83982a7bdf5d952d468cb6de9412234791db03efaee594995` |

All three `run_report.result = PASS`, worker passed, exit code 0, stop_reason null. Input SHA256 (TRAIN, P9 builder, frozen candidates, selected subsets) unchanged; class mapping `[0,1]`, threshold `0.5` preserved. Observed local Python3.11.9, NumPy2.4.6, pandas3.0.5, scikit-learn1.9.0, SciPy1.17.1, joblib1.5.3, threadpoolctl3.6.0 and psutil7.2.2. Fitted base-learner structure, Stacking inner-fold settings, model serialization/reload, 16 official TRAIN-derived rows `predict_proba` range/normalization and hash stability after reload all reported successful in actual author-side verification.

## Safety and history boundaries

- Historical `p15_local_rf42_full_01` stopped at 20-minute TIMEOUT and remains **INCOMPLETE**; successful retry under no wall-time deadline saved separately as `p15_local_rf42_full_02`. No failed output was turned into a PASS.
- Entire dataset for fitting is official TRAIN (175341); **official TEST not reopened for this reconstruction**. Training runner uses imported frozen P9 constructors only, never P9 `main()`; no scientific TEST metrics or candidate/threshold retuning.
- The 9GiB initially recommended conservative admission gate did not pass; an explicitly reviewed alternate local policy started only when available RAM >=4GiB, with <=2GiB sampled process-tree RSS ceiling, >=1.5GiB available-RAM floor, >=10GiB disk and watchdog. Reporting must not relabel the original gate as PASS.
- Artifacts **were not pushed to GitHub**, deliberately: .joblib files are binary serialized pickle/joblib and remain only on author laptop. A separate process on author host computed actual SHA256, file length, loaded the trusted files, inspected fitted estimators and performed TRAIN-only inference; this reviewer confirmed the **reported evidence**, not binary bytes independently in its own environment.
- No original historical environment lock exists. These files are explicitly `*_RECONSTRUCTED_FULL_TRAIN.joblib`, not `ORIGINAL`, and no historical test results were replaced. The 37-page five-chapter approved report PDF and all previously frozen results remain unchanged.

## P15 gate decision and remaining program work

**Closed in scope:** P15 full-TRAIN reconstruction on author's 12GiB laptop, three frozen candidates, frozen input/feature/threshold controls, software compatibility/reload/probability/schema checks, three persisted local model artifacts, resource/time provenance and remote reviewed author-host file-integrity acceptance JSON. **State:** `DONE_SCOPED_RECONSTRUCTION`.

**Not closed here:** historical identical-model reproducibility / original Python package environment reconstruction; independent **binary transfer/load on reviewer infrastructure**; separate G3 release or live demo evaluation authorization; rights to distribute model/dataset; scientific limitations on pre-CV feature selection and nested optimization; P16 figure QA, P18 bibliography, P19 packaging/rights, P20 external review, administrative G0–G6 release gates. Preserve these as distinct open items in task board and RELEASE_BLOCKERS.

**Next activity** is no longer any additional TRAIN fitting; prioritize separately scoped evidence publication/release review and P16/P18/P19, plus demo inference with its own explicit contract and no official TEST retuning. If a live inference demo is developed, it must load only author-verified `RECONSTRUCTED_FULL_TRAIN` artifacts and state their provenance rather than silently assigning historical TEST metrics.

**Re-run safeguard:** the file QA output path `results/reproducibility/p15_local_artifact_qa_01` is already occupied and must not be overwritten; if separately re-verifying, create a distinct output directory rather than deleting or overwriting any P15 record.
