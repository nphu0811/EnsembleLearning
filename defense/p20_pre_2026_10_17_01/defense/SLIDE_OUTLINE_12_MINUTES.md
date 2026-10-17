# Đề cương bảo vệ DRAFT, 13 slide, 12 phút

Nội dung và thời lượng dự kiến. Chưa tạo PPTX/PDF, chưa render hoặc rehearsal.
Mỗi slide chọn một thông điệp chính. Các figure là bản đã lưu, không sửa metric.
Packet-relative paths dưới đây tra được bằng manifest. Không dùng live inference.

| Slide | Giây | Nội dung chính | Evidence/visual đề xuất |
|---|---:|---|---|
| 1 | 30 | Tên đề tài, binary UNSW-NB15, scope case study | PDF trang 1, không thêm claim deployment |
| 2 | 40 | RQ1–5 và câu hỏi nào mới trả lời một phần | frozen phase1 design, introduction và conclusion; ghi rõ không preregistration mới |
| 3 | 60 | Official TRAIN175341/TEST82332, predictors và freeze | methodology; view_summary.json; freeze_candidates.json |
| 4 | 60 | Feature selection và preprocessing, ranh giới CV | source features và stage metadata; công khai chọn stable features trước CV |
| 5 | 65 | Baselines, Voting và Stacking LR/DT/RF → LR | development/ensemble aggregate tables; P9 make_stacking_42, innerCV3 |
| 6 | 65 | Ba pipeline cuối, metrics và confusion counts | P11 final_evaluation_complete/confusion_matrices; positive class Attack |
| 7 | 70 | Paired Macro F1/MCC CI và McNemar, chưa superiority/equivalence | P10 paired differences/mcnemar_holm; dùng paired figure trong PDF trang tương ứng |
| 8 | 60 | 142 FP ít hơn, 118 FN nhiều hơn; operational cost còn thiếu | error_tradeoff.pdf và confusion tables; đọc cả hai hướng lỗi |
| 9 | 60 | RF17/RF42 trade-off, đổi cả hyperparameters | freeze_candidates.json; P9 cost_metrics; performance_cost.pdf, không causal FS claim |
| 10 | 60 | Attack-family và novel-vector sensitivity | attack-family Wilson figure; P10 miss-rate CI; view_summary; không multiclass/external claim |
| 11 | 50 | Prior art và phạm vi đọc, đóng góp thực nghiệm | literature_scope.json, reported_facts C02/C03/C08/C09/C10/C15; không cross-paper score ranking |
| 12 | 60 | P15 tái dựng, provenance và các giới hạn quan trọng | artifact_acceptance.json và ba run_report; phân biệt page33 snapshot với hiện tại; original env UNKNOWN |
| 13 | 40 | Kết luận có thể bảo vệ và nghiên cứu tiếp | contribution note, câu hỏi nested/matched/repeats/external còn mở; không tuyên bố submission-ready |

Tổng 720 giây. Có thể dành phần hỏi đáp riêng ngoài 12 phút. Với thời lượng ngắn,
giữ CI và error trade-off; đưa bảng chi tiết development/attack families vào backup
slides. Không thay bằng một headline Accuracy cao.

Mỗi slide kết quả phải ghi benchmark/view, threshold và đơn vị. CI ghi rõ có điều
kiện trên benchmark. Figure thay thế P16 chỉ là artifact độc lập đã QA, không tự
thay figure bên trong PDF đã khóa. Nếu sau này tạo PPTX, lưu một bản DRAFT riêng,
render và kiểm từng slide trước khi gọi đó là sản phẩm bảo vệ.
