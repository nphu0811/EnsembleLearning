# P16 r05 — bảng số liệu cho report/defense

PLAN: ba bảng trình bày mới từ frozen aggregate CSV, không phải experiment hoặc chạy lại P11/P12/P14. Core message: Stacking42 không chứng minh ưu thế tổng thể; FP/FN đánh đổi; RF17 là joint pipeline performance–cost comparison.

Inputs read-only: P9 `final_metrics.csv`, `cost_metrics.csv`; P10 `paired_bootstrap_differences.csv`. Không đọc raw TEST, predictions hoặc model, không bootstrap lại. Hash từng input trước/sau.

EXECUTE: stdlib Python xuất CSV giữ nguyên tokens gốc, Markdown đọc được và LaTeX table sources riêng, source-data manifest/captions. Không tạo plot trong task này; nature-figure chỉ đã đọc router, không claim figure workflow/visual QA.

VERIFY: đúng ba candidates/official view,82332rows/threshold0.5; join không thiếu/thừa; confusion totals/rates/Macro-F1/MCC khớp theo tolerance1e-12 cho roundoff; paired deltas khớp metric gốc và CI chứa/không chứa0 đúng; directionFP−142/FN+118; CSV outputs giữ tokens; cost không trộn với inference performance mới; input hashes không đổi.

REPAIR: giữ failure logs và output lần đầu nếu phát sinh; sửa generator/checker hoặc caption, không sửa frozen nguồn. CHECKPOINT sau output/test thật. Artifact filenames không phải bằng chứng PASS.

Acceptance chỉ cho source/numeric tables. TeX chưa có trên PATH, nên `.tex` chưa compile/render; MD/CSV không đóng P16 visual/full-report/G4/G6. Không giả precision đo lường từ các chữ số lưu, không gọi runtime lịch sử là ETA/current throughput; original training env UNKNOWN. RF17 còn khác hyperparameters. Không superiority/equivalence hoặc causal FS claim.
