# Smoke repair — serialization assertion, r04

Lượt đầu `r04_ml_smoke/validation.json` đạt41/42, exit1. Chỉ `random_forest_17_roundtrip_exact=false`. Không xóa/sửa kết quả fail. Ba model fit/serialize/reload thực đã chạy, nhưng gate smoke đầu chưa đạt.

Chẩn đoán trước sửa bằng `tools/r04_diagnose_smoke_roundtrip.py`, không refit và không đọc TEST. Cùng fitted RF17,5 repeated parallel predictions có max absolute difference2.220446049250313e-16;5 serial repeats bitwise identical vàserial reload exact. Labels tại0.5 giống nhau. Evidence `results/reproducibility/r04_smoke_roundtrip_diagnosis/diagnosis.json`.

Nguyên nhân được kiểm chứng: thứ tự cộng floating-point trong prediction song song, không phải artifact mất/corrupt. Contract bitwise probabilities quá chặt cho source RF n_jobs=-1. Sửa duy nhất assertion roundtrip thành allclose(rtol=atol=1e-12) kèm exact threshold labels, lưu cả bitwise flag vàmaxabs. Không đổi fitted algorithm/hyperparameters/threshold/source lịch sử hoặc scientific metrics. Tolerance dùng cho kiểm tra phần mềm serialization, không equivalence margin khoa học. Lượt rerun có outdir mới, bảo toàn fail vàdiagnosis.

Reproduction fail là integration regression có thật trước fix; diagnostic test kiểm giả thuyết scheduling. Không tạo bộ test giả để đánh xanh assertion. Sau fix chạy smoke toàn3builders trong cùng môi trường sạch cùng6audit unit tests; chỉ PASS khi có output thực. Áp dụng systematic-debugging/verification-before-completion; TDD reference đã đọc cho yêu cầu failed regression trước repair. Không claim toàn bộ công cụ trước đây được viết TDD.
