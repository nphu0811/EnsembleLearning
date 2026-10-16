# NCKH — Canonical Phase 15 / Reproducibility — Opening Checklist

**Trạng thái:** PARTIAL / NOT CLOSED. Đây là **kế hoạch kiểm định**, không phải tuyên bố đã tái lập thành công.

## Vì sao cần Phase 15?

NCKH không chỉ phải có metric đẹp mà còn phải chứng minh người khác có thể biết **input nào**, **code nào**, **config/freeze nào** tạo ra những bảng kết quả nào. Tái lập báo cáo từ predictions đã khóa và tái chạy huấn luyện end-to-end là **hai mức khác nhau**; cần ghi nhãn đúng.

## Task Board ban đầu

| ID | Task | Status | Bằng chứng hoàn tất phải có |
|---|---|---|---|
| P15-01 | Inventory các entry-point scripts, input/output contracts | TODO | File `REPRODUCIBILITY_MAP.md` mapping canonical phases 2–14 → script, input, config, output |
| P15-02 | Environment & dependency lock | TODO | Python phiên bản cụ thể, `requirements`/lock, hệ điều hành/CPU/RAM, lệnh tạo environment |
| P15-03 | Dataset & split provenance | TODO | Public download citation/URL, kích thước/hashes files TRAIN/TEST, record giới hạn license, `id` và nhãn, policy preprocessing |
| P15-04 | Seed, CV, train-only fitting, frozen configs | TODO | Kiểm tra source + config + artifacts: seeds, n_folds, OOF, scaler/OHE/feature selection, model params, threshold; chỉ ghi DONE khi chứng minh được |
| P15-05 | Output integrity & minimal replay | TODO | Hash của frozen predictions/tables, kiểm tra tính nhất quán; rerun **read-only** Phase 11–14 aggregate analyses trên copy hoặc path mới, so khớp outputs |
| P15-06 | Clean-start instructions & limitations | TODO | README với commands, expected outputs, memory/runtime, giới hạn external validation và lỗi thực tế; review bởi một người khác nếu khả thi |

## Bước đầu tiên: P15-01, không train lại

Kiểm tra danh sách các scripts **đang có trong project**, mapping từng phase chuẩn sang entry-point và output. Chỉ khi xác nhận code/config/data prerequisites mới tiếp tục Phase 15. Không trộn phase local 8–10 với canonical 10–12; tránh đánh dấu các early drafts là DONE.

**Cách làm nhẹ cho máy:** Bắt đầu audit văn bản (`README`, script paths, YAML/JSON config, nhỏ), không chạy lại RF hay Stacking; không yêu cầu nén lại toàn bộ dataset/model hàng trăm MB. Các bước cần rerun phải được quyết định theo thời gian/RAM và giá trị khoa học, không chạy bừa.

**Điều kiện đóng Phase 15:** đủ provenance, config, environment, entry-point/run order, hashes, frozen scope và lệnh chạy lại minimal audit có log PASS. Nếu chưa end-to-end retrain, README phải ghi rõ mức tái lập mới chỉ là saved-artifact-level.
