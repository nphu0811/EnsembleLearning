# Đóng góp và giới hạn dùng khi bảo vệ

DRAFT companion cho phần trình bày. Không thay báo cáo 37 trang, không đóng
concern hoặc cấp chứng nhận nộp/công bố.

## Phát biểu đóng góp có thể bảo vệ

Chúng tôi thực hiện một case study thực nghiệm có kiểm toán cho phát hiện xâm nhập
nhị phân trên official UNSW-NB15. Các pipeline, threshold và kết quả cuối được
đóng băng, liên kết với nguồn xử lý, audit dữ liệu, các bảng chỉ số và phân tích
sai số. Trong scope này, Stacking thay đổi đánh đổi FP/FN so với Random Forest,
nhưng paired uncertainty chưa xác lập ưu thế tổng thể trên Macro F1 hoặc MCC.
So sánh RF17/RF42 cho thấy trade-off giữa hai pipeline khác cấu hình, chưa tách
hiệu ứng nhân quả của feature count. Phân tích attack-family và novel-vector
bổ sung mô tả giới hạn của benchmark. Tái dựng P15 chứng minh được phạm vi
full-TRAIN artifacts và author-host acceptance, tách biệt với binary lịch sử.

Phân loại phù hợp hiện nay là **nghiên cứu thực nghiệm có benchmark audit**.
Chưa có bằng chứng cho một methodological contribution mới, SOTA, hiệu quả ngoài
benchmark hoặc khả năng triển khai IDS thời gian thực. Chất lượng ghi nhận và
kiểm toán là điểm có thể bảo vệ, không tự trở thành novelty của toàn lĩnh vực.

Nguồn trong packet gồm `report/chapters/conclusion.tex`, phần Đóng góp trong phạm
vi đã chứng minh; `results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv`;
`results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json` và P15
`artifact_acceptance.json`.

## Giới hạn phải chủ động nói

1. Stable feature selection trước development CV có selection optimism risk.
2. OOF stacking không đồng nghĩa toàn bộ base/meta/FS selection đã fully nested.
3. RF17 đổi cả số feature, số cây và kích thước lá, không là isolated FS ablation.
4. Official TEST có 8.541 dòng overlap vector TRAIN. Novel-vector view vẫn cùng
   TEST, không external/unknown-attack validation.
5. Bootstrap/Wilson trên benchmark rows có giả định về sampling. Không đại diện
   independent training, session, host hoặc domain replication.
6. CI chứa 0 và McNemar không reject không chứng minh equivalence. McNemar chỉ
   kiểm overall correctness; Holm không tự áp cho mọi CI/profile hậu nghiệm.
7. FPR khoảng 27% và trade-off thêm FN chưa có operational cost matrix.
8. Các attack families hiếm có support nhỏ. Binary subgroup analysis không là
   multiclass detector và feature profiles không chứng minh cơ chế nhân quả.
9. Chi phí lịch sử là snapshot với original environment UNKNOWN; batch average
   inference time không chứng minh end-to-end latency hoặc production capacity.
10. P15 artifacts là RECONSTRUCTED_FULL_TRAIN. Chưa tái chứng minh scientific TEST
    scores của binary mới và không thể gọi original-model identity.
11. Đọc tài liệu có giới hạn selected sections/abstract; không tuyên bố exhaustive
    gap search hoặc gán Methods cho nguồn chưa truy cập.
12. PDF vẫn giữ font nhỏ, heatmap độ phân giải thấp và snapshot trang 33 trước P15.
    Dùng companion hiện hành khi giải thích. Quyền phân phối và các gate nộp đề
    tài chưa được thay bằng kết quả review AI.

Các điểm 1–11 có nguồn trong immutable packet. Điểm 12 kế thừa companion P16/P17
và P19 ngoài packet, không được phát cho reviewer như gợi ý concern.

## Câu nói cần tránh và câu thay thế

| Không được suy ra | Cách diễn giải có evidence |
|---|---|
| Stacking tốt hơn RF nói chung | Có trade-off FP/FN cụ thể trên một holdout; chưa đủ bằng chứng superiority tổng thể |
| Hai mô hình tương đương | CI chứa 0 chưa loại được chênh lệch theo hai hướng; chưa có thiết kế equivalence |
| FS làm giảm thời gian theo hệ số đã đo | Hai pipeline khác feature và hyperparameters có chi phí lịch sử khác nhau |
| Leak-free vì không dùng TEST train | Feature selection/meta selection trong development còn giới hạn; không tuyên bố leak-free toàn bộ |
| Novel-vector là unknown attacks | Đó là sensitivity view theo exact feature-vector overlap trong cùng TEST |
| P15 tái lập hoàn toàn kết quả lịch sử | Đã tái dựng frozen candidates trên full TRAIN và kiểm artifact trong môi trường mới |
| Chúng tôi đã được ba giáo sư chấp nhận | Đây là ba lượt review AI trong ngữ cảnh riêng, không có xác nhận người thật |

Chưa chỉnh sửa báo cáo. Mọi đề xuất thay nội dung artifact đã duyệt phải là quyết
định tác giả riêng; thí nghiệm mới cần protocol và dữ liệu/holdout hợp lệ riêng.
