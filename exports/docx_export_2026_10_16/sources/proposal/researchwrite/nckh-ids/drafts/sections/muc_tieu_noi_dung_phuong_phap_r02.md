# Dự thảo mục tiêu nội dung và phương pháp

Đề tài: **Nghiên cứu Ensemble Learning cho bài toán phát hiện xâm nhập mạng**.

Bản nội dung phục vụ điền các mục tương ứng của đề cương năm 2026 sau review. Hồ sơ được phục hồi từ nghiên cứu đã có kết quả; không xác nhận đã được duyệt trước thực nghiệm. Thông tin chủ trì, thành viên, GVHD, mã đề tài, lịch và chữ ký còn [CẦN XÁC NHẬN]. Chưa phải DOCX/PDF theo form đã render.

## Mục tiêu

Đánh giá hiệu quả và chi phí của các pipeline học kết hợp trong bài toán phân biệt lưu lượng bình thường với tấn công trên UNSW-NB15, đồng thời làm rõ giới hạn của quy trình và các đánh đổi giữa báo động giả, bỏ sót và chi phí tính toán. Việc đánh giá không đặt điều kiện mô hình kết hợp phải vượt mô hình đơn.

Các mục tiêu cụ thể gồm: đối chiếu kết quả của các pipeline đã khóa cùng khoảng bất định; mô tả khác biệt quan sát được về hiệu năng và chi phí giữa các pipeline có tập đặc trưng và cấu hình khác nhau; khảo sát tính bổ sung của lỗi từ dự đoán ngoài fold huấn luyện (out-of-fold, OOF); xác định phần nào của các câu hỏi về độ bền đánh giá và mất cân bằng đã có bằng chứng, phần nào chưa được trả lời. Toàn bộ RQ gốc và trạng thái tương ứng được giữ trong tài liệu 06_rq_method_output_gates.md [N1].

## Nội dung nghiên cứu

Tổng hợp các phương pháp ensemble và lựa chọn đặc trưng liên quan, chú ý cách chia dữ liệu, đầu vào meta learner và phạm vi so sánh. Voting, stacking và các cơ chế xử lý mất cân bằng đã xuất hiện trong prior work; nghiên cứu không nhận sự kết hợp các thành phần này là thuật toán mới [L05–L07]. Phần tổng quan trong nước sẽ dùng đúng loại nguồn và độ sâu đã đọc, không suy kết quả thực nghiệm từ thông báo bảo vệ luận án [D01–D02].

Đối với chuỗi thực nghiệm đã thực hiện, nội dung được trình bày gồm kiểm toán dữ liệu và feature-vector overlap, feature tracks, các mô hình đơn và ensemble, quy trình lựa chọn cấu hình trên TRAIN, đánh giá đóng băng, phân tích thống kê, ablation hồi cứu và lỗi theo nhóm tấn công. Khi diễn giải, phân biệt kết quả binary detector với dự đoán multiclass; giữ các kết quả kém hoặc không kết luận được [N2–N3].

Phần công việc còn lại là hoàn thiện nguồn trích dẫn, chuẩn hóa bảng/hình và chú thích, tài liệu tái lập, đánh giá khả năng tái dựng mô hình trong môi trường cô lập, chuẩn bị demo suy luận khi có artifact hợp lệ, hoàn thiện hồ sơ theo mẫu và bộ tài liệu bảo vệ. Đây là công việc cần kiểm định tiếp, không được liệt kê như sản phẩm đã hoàn thành [N4].

## Phương pháp và phạm vi diễn giải

Nghiên cứu kế thừa official TRAIN gồm 175.341 mẫu và TEST gồm 82.332 mẫu; Attack là lớp dương (1), Normal là lớp 0. Ba pipeline final đã khóa là RF-42, Stacking-42 và RF-17, với ngưỡng quyết định 0,5. Các predictors loại trừ id, label và attack_cat. Preprocessing được triển khai trong pipeline; stacking dùng hồi quy logistic (LR), cây quyết định (DT) và Random Forest (RF) làm base learners, LR làm meta learner với internal cross-validation (CV) [N2]. Mô tả này dựa trên source và metadata đã đối chiếu; kiểm tra tĩnh không thay việc tái lập huấn luyện và chưa xác nhận môi trường huấn luyện gốc.

Đánh giá dựa trên các bảng đã lưu gồm Macro-F1, MCC, per-class precision/recall/F1, FPR/FNR, ROC-AUC, PR-AUC và thời gian huấn luyện/suy luận được ghi trong bảng chi phí, với điều kiện đo và giới hạn môi trường được công khai. Khoảng tin cậy paired bootstrap thể hiện bất định có điều kiện trên các dòng benchmark, không thay repeated training; McNemar đánh giá paired correctness, không phải kiểm định trực tiếp Macro-F1. So sánh RF-17/RF-42 được diễn giải như trade-off giữa hai pipeline vì chúng còn khác hyperparameters [N1–N3].

Giới hạn đã xác định phải xuất hiện trong báo cáo: feature selection sử dụng toàn bộ TRAIN trước development CV, meta tuning chưa fully nested, official split có overlap và novel-vector view vẫn thuộc cùng benchmark. Vì vậy không gọi CV là ước lượng không thiên lệch sau selection, không khẳng định external/time-independent validation và không dùng TEST để chỉnh features, mô hình hoặc threshold. RQ4 giữ partial; hiệu quả controlled resampling trong RQ5 chưa có đủ bằng chứng [N1–N3].

## Kết quả đã có và sản phẩm cần hoàn thiện

Đã có source, frozen metrics và các bảng phân tích. Kết quả hiện có không chứng minh Stacking-42 vượt RF-42 tổng thể; giảm FP đi cùng tăng FN. Hồ sơ sẽ trình bày cả hai mặt cùng uncertainty và giới hạn, thay vì chỉ chọn chỉ số có lợi [N3].

Sản phẩm cần hoàn thiện gồm đề cương đúng mẫu, báo cáo LaTeX và PDF, source/config/tài liệu tái lập, bảng/hình có nguồn, demo được kiểm thử, slide, kịch bản và hỏi đáp hội đồng. Chất lượng được xác nhận bằng artifact, kiểm tra số liệu, tests và render; không đặt ngưỡng Accuracy tùy ý. Replay bảng aggregate, tái dựng ML và inference demo có ba gate riêng; phần chưa đạt tiếp tục ghi thiếu, không thay bằng một sản phẩm khác có tên tương tự [N4].

## Nguồn dùng trong dự thảo

[N1] `proposal/researchwrite/nckh-ids/06_rq_method_output_gates.md` và frozen research design được dẫn trong đó.

[N2] `docs/research/ENSEMBLE_FRAMEWORK.md`; `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json`; `results/reproducibility/resume_2026_10_16/protocol/P15_04_PROTOCOL_REPORT.md`.

[N3] `docs/CLAIM_EVIDENCE_MATRIX.md`, C03–C11 và các bảng gốc được liên kết tại đó.

[N4] `proposal/researchwrite/nckh-ids/07_remaining_work_feasibility.md`; `release/RELEASE_BLOCKERS.md`.

[L05] Khan và cộng sự, 2023, DOI10.1016/j.jnca.2022.103560. [L06] Thockchom và cộng sự, 2023, DOI10.1007/s40747-023-01013-7. [L07] Ren và cộng sự, 2023, DOI10.1016/j.eswa.2023.120420. Metadata và reading boundary theo `literature/resume_r02_2026_10_16/legacy_verification_ledger.csv` và `literature/resume_r02_2026_10_16/READING_NOTES.md`; không hàm ý full-paper review.

[D01–D02] Nguồn trường đại học và giới hạn sử dụng trong `literature/resume_r02_2026_10_16/DOMESTIC_SOURCES.md`. Các nhãn nguồn là nhãn soạn thảo nội bộ, chưa phải số thứ tự bibliography cuối.
