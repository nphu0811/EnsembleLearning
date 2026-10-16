# TRAIN-only software smoke — r04

Status: PASS_SCOPED sau repair assertion có bằng chứng; không end-to-end research reproduction. Initial run41/42 fail và repaired run45/45 pass được giữ riêng. Xem R04_SMOKE_REPAIR.md cho chẩn đoán và thay đổi acceptance. Không sửa6test lịch sử, source huấn luyện, dữ liệu, freeze hoặc bảng final.

## Thực thi

Môi trường mới `results/reproducibility/r04_ml_smoke_runtime/` tạo bằngPython3.11.9 venv, không system-site-packages; pip install theo observed-version requirements qua publicPyPI. Pip check:No broken requirements found. Resolved freeze tại `results/reproducibility/resume_2026_10_16_r04/smoke_resolved_requirements.txt`. Đây không phải original training environment/hashed requirements lock. Original env vẫn UNKNOWN.

```powershell
python -m venv results/reproducibility/NEXT_SMOKE_RUNTIME
& results/reproducibility/NEXT_SMOKE_RUNTIME/Scripts/python.exe -m pip --isolated install --index-url https://pypi.org/simple -r reproducibility/requirements-r04-smoke-py311-NOT-ORIGINAL.txt
& results/reproducibility/NEXT_SMOKE_RUNTIME/Scripts/python.exe -m pip check
& results/reproducibility/NEXT_SMOKE_RUNTIME/Scripts/python.exe -I tools/r04_train_only_smoke.py --out-dir results/reproducibility/NEXT_UNIQUE_SMOKE
```

Không chạy lại để chỉ đổi trạng thái; đã có pass vàhash. Chỉ rerun khi code/dependency/input thay đổi hoặc có concern cụ thể. Model builders được import từ source P9, không gọi main vì main đọcTEST vàghi fixed historical outputs. Sampling gồm2.000fit rows và500validation rows không trùng index, đều officialTRAIN;42/17predictors giữsubset đóng băng;ngưỡng0.5. Python audit hook chặn đọc CSV dữ liệu khácTRAIN;metadata ghi sole dataset read. Không metric scientific/Accuracy được tính hoặc dùng chọn model.

## Kiểm định

- Ba builders thực fit, serialize, reload;probabilities valid,classes[0,1].
- Negative schema:missing column,target/extra column,non-numeric,infinity,missing value,empty,duplicate headers bịreject cho cả3models;unseen categorical value được xử lý bởiencoder.
- Roundtrip allclose1e-12 vàexact threshold labels đạt. RF17 bitwise probabilities không khớp do parallel sum order;maxabs2.22e-16,đã diagnostic riêng.
- Repaired validation45/45 PASS;6historical audit unit tests PASS;pip check PASS.
- Input/model hashes,seed,index hashes,versions,timing thật trong run_metadata.json. Không extrapolate smoke runtime thành fullTRAIN runtime hoặcdeployment throughput.

## Artifact vàgiới hạn

`results/reproducibility/r04_ml_smoke_repaired/` có3SMOKE_ONLY.joblib,schema.json,run_metadata.json,validation.json. File model nhỏ được tạo thật nhưng **không phải** fullTRAIN final model,không thay trạng thái model_artifact_available của sản phẩm cuối. Không distribution/performance certification;không kiểm stability qua retraining/scenario/external data. Snapshot không giải FS optimism hoặcmetadata bibliography warnings.

G3/P15 vẫn PARTIAL: đạt thêm fresh environment fit/serialization software smoke;chưa full data pipeline reconstruction,original environment,fullTRAIN model hoặcfinal inference demo. GateB/C của feasibility cần cập nhật scoped evidence này nhưng không được gọi achieved.
