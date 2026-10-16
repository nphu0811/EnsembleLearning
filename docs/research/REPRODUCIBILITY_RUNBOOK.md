# Tái lập an toàn từ bằng chứng đã lưu

R04 bổ sung: fresh-environment TRAIN-only fit/serialize/reload smoke đạt45/45 trong outdir riêng, không officialTEST. Contract/report tại R04_ML_SMOKE_CONTRACT.md vàR04_ML_SMOKE_REPORT.md. Source command `tools/r04_train_only_smoke.py`; requirements observed `reproducibility/requirements-r04-smoke-py311-NOT-ORIGINAL.txt`. Model smoke subset không dùng làm demo final;G3/P15 vẫn PARTIAL. Initial41/42 fail vàdiagnosis giữ riêng,không xóa.

Chạy tại root NCKH. Các lệnh dưới đây không fit/predict, không chọn feature/threshold và không thay frozen results. Mỗi phiên dùng output mới để bảo toàn log. Python 3.11.9 hiện tại; original training environment UNKNOWN.

```powershell
python tools/p15_01_inventory_check.py --project-root . --out results/reproducibility/NEXT_SESSION/p15_01.json
python tools/p15_03_check_dataset_provenance.py --project-root . --out results/reproducibility/NEXT_SESSION/p15_03.json
python tools/p15_04_protocol_integrity.py --project-root . --out-dir results/reproducibility/NEXT_SESSION/protocol
python -m unittest discover -s tests -v
```

P15-01 và P15-04 phải đọc JSON status, không chỉ exit code. P15-03 đọc aggregate raw schema/checksum, không thực hiện đánh giá model.

Tái lập hậu xử lý aggregate trong venv stdlib riêng, không cần pip:

```powershell
python -m venv --without-pip .venv-analysis-smoke
.\.venv-analysis-smoke\Scripts\python.exe -I src/analysis/close_original_phase11.py --project-root . --outdir results/reproducibility/NEXT_SESSION/phase11_replay
.\.venv-analysis-smoke\Scripts\python.exe -I -m unittest discover -s tests -v
```

Đảm bảo outdir mới vì script closure lịch sử cho phép ghi đè. Đối chiếu SHA-256 ba CSV với `results/final_evaluation/unsw_nb15/phase11_evaluation_closure/`. Phiên 16/10 đã thực hiện điều này; bằng chứng `results/reproducibility/resume_2026_10_16/clean_replay_report.json`. Không chạy lại vào thư mục đó.

## Replay huấn luyện và demo

Chưa có một command train/demo được kiểm định end-to-end. Các script huấn luyện lịch sử có đường dẫn output cố định; đọc và lập mapping trước khi chạy, dùng workspace/output cô lập, không ghi đè frozen artifacts. Không dùng TEST để điều chỉnh mô hình sau kết quả. Fresh ML environment cần lock/version, input hashes, budget và log; so sánh sai khác được báo cáo, không sửa để khớp số lịch sử.

Inference demo cần serialized model cùng feature schema và package compatibility. Hiện chưa có. Saved-results viewer chỉ là evidence viewer, không thay thế demo inference.
