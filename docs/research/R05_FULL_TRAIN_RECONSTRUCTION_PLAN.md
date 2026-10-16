# P15 — phương án tái dựng full TRAIN, chưa thực thi

Ngày 16/10/2026. Status **PLAN_ONLY / NO_GO tại snapshot hiện tại**. Đây là bước chuẩn bị sau smoke, không tái lập mô hình lịch sử, không sửa protocol, không training/predict mới. Original environment vẫn UNKNOWN.

## Căn cứ và budget đề xuất

Snapshot `results/reproducibility/resume_2026_10_16_r05/capacity_snapshot.json`: 8 logical processors, 12.554.305.536 byte RAM tổng, 1.554.996 KiB RAM đang trống (khoảng 1,48 GiB), 28.612.861.952 byte đĩa trống. Chỉ đo thời điểm hiện tại, không giả định tài nguyên sẽ được giữ riêng.

Budget kỹ thuật đề xuất cho một lần tái dựng, **chưa được xác nhận đủ nguồn lực**: tối đa 3 candidate đã khóa, mỗi candidate fit một lần trên toàn bộ 175.341 dòng TRAIN; stacking giữ đúng 3-fold nội bộ, bao gồm các fit nội bộ theo builder. Không search, resampling, FS lại, calibration, threshold/candidate selection hoặc repeated seed sweep. Không chi cloud/API, không mua dịch vụ; chi điện/thời gian máy chưa biết và không được ghi bằng 0 như một thực chi.

Ceiling vận hành đề xuất: 60 phút wall time cả batch, watchdog ngoài process; tối đa 7 GiB tổng working set của cây process; dừng nếu RAM trống dưới 2 GiB hoặc đĩa trống dưới 10 GiB. Cần RAM trống ít nhất 9 GiB trước khởi chạy để giữ headroom cho ceiling; hiện chưa đạt. Đây là **giới hạn bảo vệ đề xuất**, không phải dự báo RAM/runtime đo được. Nếu quá trần thì ghi INCOMPLETE, không nới trần hoặc fit lại tự động để cố đạt. Chưa có watchdog runner được triển khai nên cũng chưa đạt launch gate.

Historical cost table ghi RF42 371,24 s, Stack42 980,17 s, RF17 57,26 s; đó là thời gian lịch sử có environment limitations, không ETA cho máy này. Không nhân tuyến tính thời gian smoke 2.000 dòng thành full TRAIN. Chưa có upper bound bộ nhớ được đo trên full TRAIN.

## Input/provenance cần khóa trước launch

Các SHA-256 sau lấy từ smoke metadata và phải đối chiếu lại thực tế trước launch bằng streaming hash, không gọi validation là training:

| Input | SHA-256 |
|---|---|
| `data/raw/unsw-nb15/UNSW_NB15_training-set.csv` | `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa` |
| `src/models/run_unsw_phase9_final_holdout.py` | `3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480` |
| `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json` | `cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6` |
| `results/feature_selection/unsw_nb15/stage2/subsets/stage2_candidate_subsets.json` | `5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be` |

Ghi thêm git HEAD, source dirty diff, ordered 42/17 feature lists, 175.341 TRAIN row identities/order hash, nhãn Attack=1/Normal=0, seed42 và inner seed137, frozen configs/threshold0.5. Giữ preprocessing trong builder. RF `n_jobs=-1`, stacking `n_jobs=1` như source; không lặng lẽ thay hyperparameter để vừa budget. Có thể giới hạn CPU bằng affinity ở launcher và BLAS threads2, phải ghi như điều kiện execution, không claim lịch sử giống hệt.

Môi trường mới: Python3.11 và observed-version requirements R04 chỉ là starting point, **không original lock**. Trước fit cần fresh venv không system-site-packages, pip check, resolved freeze, wheel/download SHA-256 manifest và package provenance. Nếu pin unavailable, ghi blocker; không đổi version rồi nhận tái lập môi trường cũ. Không cài thêm hoặc fit trong task lập kế hoạch này.

## Chống đọc TEST và ghi đè

Runner tương lai chỉ import functions/builders; **không gọi main P9** vì main đọc TEST và ghi đường dẫn lịch sử. Chặn mọi dữ liệu CSV ngoài TRAIN bằng guard và deny official TEST/novel TEST ở launcher. Kiểm fixture ngoài TRAIN chỉ dùng dữ liệu tổng hợp theo schema; kiểm roundtrip dùng TRAIN rows có nhãn và báo đây là software check, không generalization metric. Không tính metric nhằm chọn model.

Output phải ở `results/reproducibility/full_train_reconstruction_<UNIQUE_RUN_ID>/`, resolved path nằm trong repo và được tạo exclusive (`exist_ok=False`). Venv, logs, wheel cache và serialized models tách khỏi mọi historical output và khỏi SMOKE_ONLY. Không symlink/junction tới data/templates/frozen result directories. Pre/post preservation hashes bao phủ raw, source, frozen configs/results và nguyên mẫu. Fail trước fit nếu output tồn tại hoặc bất kỳ hash đã khóa không khớp. Không mở tệp lịch sử để ghi.

Mỗi model chạy trong process riêng, ghi start/end/exit/timing/peak-memory, đầu ra tạm rồi atomic rename sau kiểm tra; timeout hoặc OOM giữ failure log, không tiếp tục coi batch thành công. Process con và watchdog phải dừng hết trước kết thúc phiên; không detached job.

## Acceptance và bước tiếp

1. Launch gate: RAM/disk đạt, budget được chủ máy chấp nhận nếu job được coi lớn, runner/watchdog đã review và negative guards được kiểm trước fit. Hiện RAM và runner gate chưa đạt nên không chạy.
2. Reconstruction gate: cả 3 fullTRAIN artifacts có model/learned preprocessing, ordered schema, class mapping/probability semantics, input/source/env hashes; load/serialize/roundtrip, valid/invalid schema checks và threshold labels đạt. Tolerance roundtrip1e-12 theo chẩn đoán R04 là tolerance phần mềm, không equivalence margin nghiên cứu.
3. Provenance gate: gọi artifacts là **RECONSTRUCTED_FULL_TRAIN**, không ORIGINAL hoặc SMOKE_ONLY. Không hứa bitwise historical results, không cho reconstructed probabilities ghi đè saved predictions/metrics.
4. Demo gate riêng: chỉ tiếp tục inference demo với artifacts đã qua bước2/3 và runbook rõ. Không dùng TEST để chọn artifact; không gán performance của model lịch sử cho reconstruction chưa được đánh giá. Official TEST không được mở trong job này; mọi đánh giá bổ sung tương lai cần contract riêng, không tuning.

Task plan đạt khi hash/budget/đường dẫn/ngăn TEST/overwrite/acceptance được đối chiếu và lưu validation. P15/G3 vẫn PARTIAL; không cấp full reproduction hoặc final demo readiness. Việc độc lập có thể tiếp tục ngay là source/citation checks, P16 và P17 source authoring.
