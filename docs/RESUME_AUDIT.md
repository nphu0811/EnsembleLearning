# Resume audit ngày 16/10/2026

## Kết luận phục hồi

Workspace là nghiên cứu đang thực hiện, không phải dự án mới. `.research_memory` đầu phiên là skeleton; đã sao lưu tại `results/reproducibility/resume_2026_10_16/bootstrap/starter_memory/`. Chuỗi thực nghiệm UNSW-NB15, frozen holdout, thống kê, ablation và error analysis có artifact thật. Không chạy lại huấn luyện hoặc chọn mô hình.

Điểm tiếp tục là **P15 còn một phần**, đồng thời chuẩn bị đề cương, availability và P16 từ bảng đã khóa. Các nhãn `phase8`, `phase9`, `phase10` trên đĩa lần lượt ánh xạ canonical P10, P11, P12. Không đổi tên artifact để ép khớp roadmap.

## Kiểm định trong phiên

Thư mục bằng chứng: `results/reproducibility/resume_2026_10_16/`.

| Kiểm tra | Kết quả | Bằng chứng và giới hạn |
|---|---|---|
| Inventory P15-01 | 18/18 script, 48/48 input, 36/36 output | `p15_01_inventory.json`; kiểm tra tồn tại, không chứng minh nội dung mọi file |
| Raw UNSW | 3/3 PASS | `p15_03_dataset.json`; SHA-256, schema, số dòng/nhãn khớp baseline nội bộ, không phải checksum do UNSW công bố |
| Protocol | 9/9 PASS có giới hạn | `protocol/p15_04_protocol_integrity.json`; 7 source hash khớp lịch sử, freeze bằng nhau, threshold 0.5 |
| Bằng chứng tổng hợp | 79/79 PASS | `bootstrap/saved_evidence_checks.json`; 19 input hash P13 và 60 phép kiểm metric/Weighted-F1 trên 6 model-view rows |
| Unit tests | 6/6 PASS | `bootstrap/unit_tests.log` |
| Tái lập hậu xử lý trong venv mới | 3/3 CSV giống từng byte; 6 test PASS | `clean_replay_report.json`, `clean_replay_0.log`, `clean_replay_1.log`; Python stdlib, không cài package, không train/predict |
| Bảo toàn artifact đầu phiên | Manifest 282 file | `bootstrap/preservation_manifest.csv`; đối chiếu lại cuối phiên |
| Bộ mẫu | ZIP 15 file LaTeX, DOCX riêng | `bootstrap/template_audit.json`; 15/15 file trong folder cũ khớp ZIP |
| Nature registry | 20 SKILL.md | `bootstrap/nature_skill_registry.csv`; tên đăng ký khác folder với `researchwrite`; discovery không đồng nghĩa execution |

## Sửa nhận định lỗi thời

- `docs/P15_03B_SOURCE_AND_P15_04_SCOPE.md` còn ghi chờ output người dùng. P15-04 nay được chạy trực tiếp và có kết quả mới.
- Audit 07/10 còn ghi P11 thiếu Weighted-F1/per-class. Các bảng closure đã tồn tại và vừa tái lập giống từng byte; không mở lại gap này.
- Audit 07/10 còn ghi P14 thiếu feature profiles. Step3–5 có dữ liệu tổng hợp và reconciliation cũ 375/375; phiên này xác nhận file tồn tại, chưa tái chạy 375 phép kiểm hoặc phép nối raw rows. Kế thừa closure với đúng giới hạn đó.
- `docs/TEMPLATE_MAPPING.md` mô tả DOCX như nằm trong ZIP. ZIP thực tế không chứa DOCX; bản riêng tìm thấy tại Downloads. Nguồn thực tế đã được ghi trong manifest mới.
- Môi trường hiện tại là Python 3.11.9. Báo cáo clean-runtime Python 3.14.3 là bằng chứng lịch sử trên máy khác, không phải môi trường đang chạy hoặc môi trường huấn luyện gốc.

## Giới hạn khoa học bắt buộc

Feature selection học trên toàn bộ TRAIN trước development CV. Meta tuning không hoàn toàn nested. Hai vấn đề này ngăn gọi CV là đánh giá không thiên lệch sau selection. Giữ nguyên kết quả lịch sử, công khai giới hạn; không sửa lịch sử bằng một lần train mới sau khi đã xem TEST.

Official split có overlap feature vectors; novel-vector subset không phải external test hoặc time/session-independent validation. Attack-family binary misses không phải multiclass classification. RF-17 và RF-42 có hyperparameter khác nhau nên so sánh final không cô lập duy nhất số feature.

Stacking-42 trừ RF-42 có Δ Macro-F1 0.00049669, CI 95% [-0.00031180, 0.00130895]; không chứng minh ưu thế tổng thể hay tương đương thống kê. Có giảm FP 142 và tăng FN 118 trên official test. Các CI cũ có điều kiện trên benchmark rows, không chứng minh flow độc lập.

## Thiếu sót còn thật

Chưa có original training environment; chưa có serialized model trên workspace; chưa replay training trong fresh ML environment. Chưa có báo cáo IDS LaTeX/PDF, đề cương điền form DOCX/PDF, slides, inference demo hay final release hợp lệ. Thông tin tác giả/GVHD/chữ ký chưa xác nhận. Công cụ dependency loader cho document không được expose; không có TeX/LibreOffice trên PATH. Không coi đây là lỗi nghiên cứu hoặc xin xác nhận chuyển phase; làm tiếp các phần độc lập và lưu blocker.

Roadmap hiện hành: `docs/ROADMAP_CURRENT.md`. Task board và handoff hiện hành nằm tại `.research_memory/`.
