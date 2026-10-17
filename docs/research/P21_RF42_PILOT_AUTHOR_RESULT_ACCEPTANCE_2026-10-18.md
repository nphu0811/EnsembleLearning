# P21 — nghiệm thu có giới hạn pilot tài nguyên RF-42 (18/10/2026)

**Kết luận:** `RF42_PILOT_REPORTED_EVIDENCE_ACCEPTED`, `P21_SCIENTIFIC_EXPERIMENTS_NOT_AUTHORIZED`. Không đánh đồng việc pilot khởi chạy thành công với giá trị Macro-F1 hoặc ưu thế Ensemble. Tài liệu này chỉ kiểm toán **hồ sơ JSON do máy tác giả tạo và push**, không độc lập quan sát toàn bộ quá trình chạy Windows.

## 1. Bằng chứng nguyên gốc

- Commit tác giả `34bcdeac4dd4379413154de6aad88ccec8c89a60` (`P21`) chỉ thêm ba file JSON:
  - `results/controlled_extensions/p21_train_only_pilot_rf42_01/start.json`
  - `results/controlled_extensions/p21_train_only_pilot_rf42_01/run_report.json`
  - `results/controlled_extensions/p21_train_only_pilot_rf42_01/worker/worker_result.json`
- File `start.json` ghi `INCOMPLETE/NOT_STARTED` vì là bản **chụp trước khi chạy**, không phải thất bại. `run_report.json` là kết quả cuối `PASS_RESOURCE_SMOKE_ONLY`, `exit_code=0`, `stop_reason=null`. Worker PASS với `scope=P21_RF42_ANCHOR_PILOT_ONLY; no RQ result`.
- Dữ liệu official TRAIN SHA256 `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`; cả supervisor/worker đều ghi cùng checksum. User-host static preflight trước đó 30/30 PASS, không dùng official TEST.
- Protocol digest ghi trong start và run `3a4c21cd069432c36cb8cfcdb863dbd4898845cd095fb4111be34b8d0c455c86`. Giới hạn tiêu chuẩn theo cấu hình `config/p21_train_only_protocol_2026_10_18.json`.
- Python local `.venv-p15-local`, numpy2.4.6/pandas3.0.5/scikit-learn1.9.0, psutil7.2.2. Mã nguồn P21 worker/launcher và lịch sử P9/P15 không bị thay đổi trong commit tác giả.

## 2. Đo thực tế (chỉ P21 RF42 anchor 8000 FIT rows)

| Trường | Giá trị từ JSON |
|---|---:|
| `pilot_rows` | 8000, gồm 2555 Normal + 5445 Attack |
| Kích thước official TRAIN | 175341 |
| Nội bộ `StratifiedGroupKFold` fold0 seed 20261018 | Fit pool 140272 / held-out validation 35069 |
| Fraction validation | 0.200005; tỷ lệ Normal 0.319370 |
| Group and row overlap | `false` (ghi `group_disjoint=true,row_disjoint=true`) |
| Model smoke | RF42, 150 trees, min_leaf2, max_features0.5, class_weight=None, seed1103, threshold0.5 |
| Fit + 16 TRAIN-probe probability checks | 11.391 seconds |
| End-to-end wall-clock | 51.86 seconds |
| Process tree peak RSS | 371728384 bytes ≈ 354.51 MiB, dưới cap 2147483648 bytes (2 GiB) |
| System available RAM at start | 4676845568 bytes ≈ 4.356 GiB (>=4 GiB gate) |
| Minimum system available seen | 4333109248 bytes ≈ 4.035 GiB (>1.5 GiB floor) |
| Resource samples | 101 (0.5s monitoring); budget 20min |
| Free disk initially | 31139655680 bytes ≈ 29.0 GiB |
| Exit | 0, stop_reason=null |
| Scientific validation metrics / TEST read / model artifact | all flagged `false` |

**Giới hạn:** số RAM peak là kết quả watchdog được báo cáo, không phải phép đo mới do GitHub CI chạy trên laptop. Chỉ kiểm tra nhóm trùng `42` predictor gốc, chưa tách session/host/time. Không có một dòng validation nào dùng để `fit` theo cấu trúc worker và khai báo báo cáo; QA này không đo được accuracy/recall.

## 3. Kiểm định chéo sau khi tác giả push

- New read-only standard-library validator `tools/p21_verify_pilot_reports.py` checks exact source hash and protocol digest, nested worker result equality, start/run provenance, model config, TRAIN-derived split, no output/re-evaluation, RAM/disk/wall budget.
- 14/14 checks passed on committed JSON; test `tests/test_p21_pilot_report_acceptance.py` added 5 fixture-only negative/positive checks to catch forged success flags and changed settings; all 5/5 passed.
- GitHub Actions [run 39062897494](https://github.com/nphu0811/EnsembleLearning/actions/runs/39062897494) **SUCCESS**: 14/14 protocol tests +7/7 pilot safety tests +5/5 pilot report tests +3/3 synthetic group tests = **29/29 unit tests**, **29/29 static source checks** and **14/14 metadata-report acceptance checks**. CI did not install/fit ML in the acceptance job, did not open official TRAIN/TEST or load `.joblib`; synthetic split job uses only fabricated 42-column rows.
- **Not independently audited:** full local `resources.csv` samples and worker log are Git-ignored and remain on laptop; actual process access history is documented by source guard and self-declared flags, not a forensic OS capture. This caveat remains on the accepted pilot.

## 4. Gate decision and what remains

`P21_RF42_ANCHOR_RESOURCE_PILOT_DONE_SCOPED`: pilot accepted, **no RQ1/RQ2/RQ5 model comparison yet**. Do **not** extrapolate 8k RF fit time or 354MiB RSS linearly to 60k/5-seed, 15 feature selector fits or inner-CV Stacking: runtime/memory profiles differ.

**Next recommended pilot:** fit-only stable17 feature selection on TRAIN-fit subset (5 selection seeds × MI/L1/ET, max pilot resource restrictions) with deterministic ranking; independently prove that validation labels never enter feature selection. Then resource pilots for `class_weight=balanced`, random oversampling on FIT, and Stacking-Lite. Preserve all raw experimental results and output from P9/P15, official TEST and the 47-page PDF V2. Each pilot requires author opt-in and independent resource QA.

Only after all component pilots passed and new explicit author approval may execute P21 5-seed 60000-row scientific arm matrix. A new PDF V3 must follow outcomes/independent scientific QA rather than precede them. P18/P19/P20 release gates remain separately OPEN.
