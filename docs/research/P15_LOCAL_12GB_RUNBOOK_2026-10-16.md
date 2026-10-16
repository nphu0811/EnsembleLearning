# P15 — Huấn luyện lại TRAIN trên laptop 12 GB (runner + watchdog)

**Trạng thái:** code đã kiểm thử bằng fixture, **chưa chạy trên máy Windows của tác giả**, P15/G3 vẫn PARTIAL. Tài liệu này KHÔNG chứng nhận ba mô hình đã tái lập. Chỉ dùng để lập kế hoạch và tiến hành từng bước có giám sát.

## 1. Vì sao cần quy trình khác?

- Snapshot người dùng gửi: RAM trống **2,157,973,504 bytes ≈ 2.01 GiB**; đĩa trống ≈28.90 GiB. Bản P15 preflight chuẩn đạt **11/12**; gate **>= 9 GiB RAM trống FAIL**.
- 9 GiB là **ngưỡng vận hành bảo thủ trong kế hoạch R05**, không phải mức bộ nhớ ML đã đo được. Không sửa/ép PASS ngưỡng 9 GiB của script cũ.
- Phương án mới dành cho Windows laptop 12 GB: chỉ chạy *một* mô hình tại một thời điểm, bắt đầu với pilot trên **10,000 dòng từ official TRAIN**, đo real-time trước khi cân nhắc full 175,341 TRAIN. Ngưỡng thận trọng mặc định: RAM trống trước khi khởi chạy **>=4 GiB**, tổng RSS các process trong cây **<2 GiB**, RAM trống hệ thống **>=1.5 GiB**, đĩa trống **>=10 GiB**. Ngưỡng này là **đề xuất kỹ thuật chưa được hiệu chuẩn**, không bảo đảm đủ RAM cho full fit.
- Số 205 MiB của serialized model RF-42 trong kết quả lịch sử KHÔNG phải giới hạn working RAM. Hiệu suất của một pilot nhỏ cũng không dự báo chắc chắn RAM sử dụng ở full size.

## 2. Cấu trúc và tính bất biến

File mới: `tools/p15_local_supervisor.py` (bộ giám sát) và `tools/p15_local_worker.py` (tiến trình huấn luyện), với `tests/test_p15_local_supervisor.py`. **Không sửa** `src/models/run_unsw_phase9_final_holdout.py`, raw CSV, `freeze_candidates.json`, stable feature subset, frozen predictions/bảng kết quả hoặc PDF.

Worker chỉ import hàm `build_frozen_models` từ source P9, không bao giờ gọi `main()` (hàm này đọc TEST và ghi output cũ). Worker đặt audit-hook chặn đọc các CSV dữ liệu khác TRAIN, kiểm SHA-256 trước/sau, dùng seed 42/137 và frozen threshold 0.5. Không tuning, không feature selection mới, không eval TEST. Pilot lấy mẫu stratified deterministic **chỉ để đo tài nguyên**, không đo chính xác khoa học hoặc quyết định model/threshold. Full fit vẫn dùng 100% TRAIN.

Giới hạn CPU 1–2 cores được đặt bằng OS affinity *trước* khi worker bắt đầu import/training. Không sửa hyperparameters `n_jobs=-1` của RF hay inner CV=3 của Stacking. Môi trường Python/BLAS threads được ghi lại; điều kiện vận hành này có thể khác lịch sử nên chỉ gọi model là **RECONSTRUCTED_FULL_TRAIN**, không phải `ORIGINAL`.

Watchdog lấy mẫu 0.5 giây: process-tree RSS, RAM hệ thống, dung lượng đĩa và elapsed time. Vượt cap, lỗi cảm biến, timeout, hoặc thiếu RAM/đĩa sẽ gọi kill process tree. Worker kiểm tra heartbeat, tự dừng nếu supervisor không còn cập nhật >20 giây. Nếu máy Windows cấp phát bộ nhớ nhanh hơn chu kỳ đo, nguy cơ đơ/OOM không thể loại trừ 100%; không coi watchdog là hard OS memory quota. Với máy có ứng dụng quan trọng chưa lưu, KHÔNG chạy full TRAIN.

## 3. Chuẩn bị lần đầu (PowerShell ở thư mục gốc NCKH)

Đồng bộ GitHub và kiểm tra:

```powershell
 git status
 git pull --ff-only origin main
 py -3.11 -m venv .venv-p15-local
 .\.venv-p15-local\Scripts\python.exe -m pip install -r reproducibility/requirements-r04-smoke-py311-NOT-ORIGINAL.txt psutil
 .\.venv-p15-local\Scripts\python.exe -m pip check
 .\.venv-p15-local\Scripts\python.exe -m unittest discover -s tests -p 'test_p15_local_supervisor.py' -v
```

Nếu cần, tắt các ứng dụng nặng (Docker/WSL, Android Studio, NetBeans, nhiều tab browser), **lưu mọi công việc trước** và restart Windows; đừng tắt antivirus, Windows services hoặc giới hạn pagefile/virtual memory tuỳ tiện. Đợi máy ổn định. Đo RAM:

```powershell
 .\.venv-p15-local\Scripts\python.exe -c "import psutil;print('RAM trống GiB:',round(psutil.virtual_memory().available/1024**3,2))"
```

Nếu nhỏ hơn **4 GiB** thì **DỪNG**: runner sẽ từ chối chạy model; không hạ ngưỡng để ép thực thi. Mức >=4 GiB chỉ đủ điều kiện bắt đầu *pilot có giám sát*, không phải chứng minh full sẽ vừa RAM. Nếu khó đạt 4 GiB, lựa chọn an toàn là máy khác/cloud hoặc nâng cấp RAM; không tự nhận P15 hoàn thành.

## 4. Pilot: chạy từng mô hình, không bao giờ chạy đồng thời

**Sau khi đã có >=4 GiB RAM trống**, bắt đầu với RF-17:

```powershell
 .\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode pilot --candidate random_forest_17 --out-dir results/reproducibility/p15_local_rf17_pilot_01
```

Đọc `results/reproducibility/p15_local_rf17_pilot_01/run_report.json`. Các trường cần xem: `result`, `stop_reason`, `peak_tree_rss_bytes`, `min_ram_seen_bytes`, `resource_samples`, `package_versions`, `worker_checks`. `result=PASS` chỉ chứng minh pilot TRAIN-subset + kiểm tra phần mềm đạt; không phải mô hình full.

Nếu RF-17 ổn, lần lượt chạy các pilot **sau khi RAM hồi phục**:

```powershell
 .\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode pilot --candidate random_forest_42 --out-dir results/reproducibility/p15_local_rf42_pilot_01
 .\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode pilot --candidate stacking_42 --out-dir results/reproducibility/p15_local_stack_pilot_01
```

Mỗi lệnh chạy xong hẳn rồi mới chạy lệnh kế tiếp. Pilot PASS với peak RAM <75% cap mới đủ điều kiện kỹ thuật **được cân nhắc** full với cùng cấu hình; vẫn có thể thiếu RAM ở full vì data scale khác.

## 5. Full TRAIN: chỉ thực hiện nếu pilot hợp lệ, RAM đã hồi phục

**Cảnh báo:** Đây là lần chạy huấn luyện thật, có thể chậm, quá RAM hoặc bị dừng bởi watchdog. Không thể bảo đảm thành công trên laptop 12 GB. Đừng thực hiện nếu còn công việc khác đang chạy.

```powershell
 .\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate random_forest_17 --pilot-report results/reproducibility/p15_local_rf17_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_rf17_full_01
 .\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate random_forest_42 --pilot-report results/reproducibility/p15_local_rf42_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_rf42_full_01
 .\.venv-p15-local\Scripts\python.exe tools/p15_local_supervisor.py --mode full --candidate stacking_42 --pilot-report results/reproducibility/p15_local_stack_pilot_01/run_report.json --out-dir results/reproducibility/p15_local_stack_full_01
```

**Mỗi full run tối đa 20 phút theo mặc định**. Ba lệnh là ba lượt độc lập, tuyệt đối không chạy song song. Nếu timeout/abort, giữ log để xác định giới hạn thay vì tăng ngưỡng mù quáng. Nhớ khôi phục RAM >=4 GiB trước mỗi lượt. Tên outdir phải duy nhất; chương trình từ chối ghi đè. Kết quả full thành công là một `.joblib` có tên `*_RECONSTRUCTED_FULL_TRAIN.joblib` và `worker_result.json` trong `.../worker/`; supervisor ghi `run_report.json`, logs và RAM time-series CSV ở folder cha.

Không commit GitHub các model lớn hoặc raw UNSW data. Chỉ gửi nội dung **`run_report.json`** và `worker_result.json` (đã rà soát đường dẫn máy) để kiểm tra, không cần chia sẻ số liệu nhạy cảm hay bản `.joblib`.

## 6. Điều kiện đánh giá P15 sau các lượt chạy

- **PILOT PASS:** chỉ xác nhận pipeline và giới hạn tài nguyên trên tập TRAIN 10,000 dòng.
- **FULL PASS một model:** serialized artifact tồn tại, hash, 42/17 feature schema, class `[0,1]`, threshold `0.5`, loaded model roundtrip xác suất/nhãn từ 16 dòng TRAIN, negative-input schema guards đạt, nguồn không thay.
- **P15 G3 chưa tự đóng:** cần cả ba artifact full, package/runtime provenance và độc lập kiểm log/hashes, nguồn đầu vào, kết quả kiểm định ở môi trường thực. Không khẳng định tái lập bitwise các historical metrics; official TEST chưa mở cho reconstruction. Demo chỉ dùng artifact đã kiểm định và có ghi nhãn mới.

## 7. Quy tắc xử lý lỗi

- `NO_GO_NO_WORKER_STARTED`: scientific input hoặc RAM/disk chưa đạt, không có mô hình chạy.
- `PROCESS_TREE_RSS_CAP`, `AVAILABLE_RAM_FLOOR`, `DISK_SPACE_FLOOR`, `TIMEOUT`: watchdog dừng hoặc đánh dấu lượt đó **INCOMPLETE**; không tự tiếp tục.
- `WORKER_FAILED_OR_MISSING_VALIDATION`: xem `worker.stderr.log` và `run_report.json`; đừng sử dụng artifact temp/dở dang.
- Không sửa ngưỡng 0.5, không hạ số cây/folds, không chọn lại feature, không gọi TEST để làm cho số liệu giống lịch sử.

**Tình trạng trong phiên chuẩn bị này:** 16 unit tests kiểm tra logic budget/guard/watcher/output/pilot đã đạt trên fixture không có data thật; chưa test end-to-end trên Windows hoặc giới hạn RAM thật. Tác giả cần chạy trong môi trường thực và báo cáo kết quả trước khi nâng trạng thái.
