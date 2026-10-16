# P15 — Read-only preflight trước khi tái dựng mô hình

**Đề tài:** Nghiên cứu Ensemble Learning cho bài toán phát hiện xâm nhập mạng (UNSW-NB15).

**Trạng thái:** P15 PARTIAL / G3 OPEN / KHÔNG huấn luyện full TRAIN.

## Cập nhật bằng git pull (không cần giải nén ZIP)

Chạy PowerShell tại thư mục gốc của repository đã clone:

~~~powershell
git status
git pull --ff-only origin main
python -m unittest discover -s tests -p "test_p15_fulltrain_preflight.py" -v
python tools/p15_fulltrain_preflight.py --project-root .
~~~

Nếu dùng Python launcher trên Windows, có thể thay python bằng py -3.11. Không cần tải bộ ZIP P15 trong ChatGPT.

Nếu git status có chỉnh sửa local hoặc git pull bị từ chối, DỪNG và kiểm tra thay đổi; không dùng git reset --hard hay ép merge.

Chương trình in JSON báo cáo. Nếu một gate không đạt sẽ thoát mã 2 theo thiết kế; giữ JSON để chẩn đoán, không ép PASS.

Để lưu kết quả, chỉ định một file JSON mới dưới results/reproducibility/:

~~~powershell
python tools/p15_fulltrain_preflight.py --project-root . --out results/reproducibility/p15_preflight_unique_01.json
~~~

Thay tên unique cho lần chạy tiếp theo; chương trình dùng exclusive create và từ chối ghi đè.

## File được bổ sung trong repo

- tools/p15_fulltrain_preflight.py: tiền kiểm chỉ dùng Python standard library.
- tests/test_p15_fulltrain_preflight.py: sáu unit test sử dụng fixture giả, không đọc official TEST.
- docs/research/P15_FULLTRAIN_PREFLIGHT_README.md: tài liệu này.

Không thay hoặc khởi chạy src/models/run_unsw_phase9_final_holdout.py.

## Nội dung kiểm tra

- SHA-256 thực tế cho TRAIN, source P9, frozen candidates và danh sách 17 features; hashes được trích từ docs/research/R05_FULL_TRAIN_RECONSTRUCTION_PLAN.md.
- TRAIN 175341 dòng gồm Normal 56000 và Attack 119341, 42 predictors, 17 selected features hợp lệ.
- Ba frozen models: random_forest_42, stacking_42 và random_forest_17, threshold 0.5.
- Python 3.11, Git tracked working tree sạch, RAM trống tối thiểu 9 GiB và đĩa trống tối thiểu 10 GiB.

Không đổi hash hoặc threshold chỉ để ép chương trình báo PASS. Source/freeze sai hash cần kiểm tra nguồn gốc trước khi xử lý.

## Quy tắc khoa học và an toàn

Preflight KHÔNG import model builder, KHÔNG fit/predict, KHÔNG đọc official TEST, KHÔNG thay dữ liệu hay kết quả đã khóa.

Ngay cả khi tất cả checks PASS, trường training_authorized luôn false và reconstruction_status luôn NOT_RUN.
Để tái dựng mô hình full TRAIN thực sự, còn phải có runner cô lập, watchdog giới hạn tài nguyên, kiểm tra môi trường/packages, provenance và kiểm định roundtrip. Kết quả historical không được tự động xem là tái lập.

### CHECKPOINT

Đã thêm preflight và sáu kiểm thử fixture. Chưa chạy trên dữ liệu Windows thực tế, chưa huấn luyện trên full TRAIN và chưa tạo serialized final models hay live inference demo.

Bước tiếp theo: gửi lại JSON sau khi chạy từ repository local; xử lý đúng những gate bị từ chối, rồi mới xem xét kế hoạch runner.
