# Ghi chú nguồn có giới hạn

Các ID L giữ mapping notebook/phase01. Đây là ghi chú đoạn đã đọc, không paper card hoặc full-paper review. Không lấy accuracy paper khác làm benchmark ngang hàng khi protocol khác.

## L05, OE-IDS

[QUB institutional record](https://pure.qub.ac.uk/en/publications/an-optimized-ensemble-prediction-model-using-automl-based-on-soft/) và [publisher preview](https://www.sciencedirect.com/science/article/pii/S1084804522002016): có AutoML, soft voting, feature reduction và resampling trên UNSW/CICIDS2017. Vì vậy kết hợp các thành phần đó tự nó chưa xác lập novelty. Chưa kiểm toàn bộ split/fit order. Không chép con số detection rate có ký hiệu phần trăm bất thường ở abstract institutional.

## L06, stacking đã công bố

[Publisher](https://link.springer.com/article/10.1007/s40747-023-01013-7), mục Proposed model và Pre-processing: GNB/LR/DT tạo đầu vào cho SGD; meta learner dùng cross-validated predictions. Paper mô tả random80/20 và Chi-square. Protocol khác official split NCKH, nên không so trực tiếp scores. Đoạn này đủ bác claim stacking+FS chưa từng có; chưa đủ kiểm toán mọi bước preprocessing. Đã đọc phần Methods HTML, chưa toàn bài.

## L07, DUEN

[Publisher](https://www.sciencedirect.com/science/article/pii/S0957417423009223), abstract/preview: dynamic undersampling trong boosting nhằm xử lý imbalance và độ khó mẫu. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4341598) là version khác; dùng DOI final10.1016/j.eswa.2023.120420. Không so trực tiếp multiclass Macro-F1 của DUEN với binary NCKH. Chưa kiểm full protocol hoặc tái lập số liệu paper.

## L08, filter FS

[Publisher abstract](https://link.springer.com/article/10.1007/s10207-023-00767-y) xem xét nhiều filter/classifier trên ba dataset; đây là cơ sở khảo sát tác động FS theo mô hình. Online2023 và final volume2024 được phân biệt. Chưa đọc nội dung subscription, không suy rằng mọi pipeline đã nested đúng.

## L11–L12

[L11 publisher abstract](https://www.sciencedirect.com/science/article/pii/S2666764924000390) phân tích FS/normalization trên nhiều dataset và thuật toán, hỗ trợ việc báo cáo chi phí cùng hiệu quả. [L12 publisher-indexed Methods](https://www.mdpi.com/2073-431X/14/3/82) có CFS và embedded XGBoost trong quy trình ensemble. L12 direct fetch429; chưa kiểm fit/split order. Không dùng các nguồn này để khẳng định novelty hay công bằng đánh giá của NCKH.

## D01, công trình tại Lạc Hồng

[Thông báo chính thức](https://lhu.edu.vn/783/41967/Lich-bao-ve-luan-an-tien-si-cap-Truong-nganh-Khoa-hoc-may-tinh-NCS-Hoang-Ngoc-Thanh-thang-12-nam-2022.html) xác nhận Hoàng Ngọc Thanh, tên luận án về học máy phối hợp/tiền xử lý cho IDS và lịch bảo vệ2022. Đây là bằng chứng chủ đề đã được nghiên cứu tại Việt Nam. Chưa đọc luận án, không xác nhận kết quả, thuật toán cụ thể hoặc việc bảo vệ đã hoàn tất từ thông báo lịch.

## D02, tóm tắt luận án tại UET

[Tóm tắt gốc](https://uet-test.uet.edu.vn/wp-content/uploads/2025/11/Tom-tat-LATS-cua-NCS-Vo-Van-Hoang_QH-20-HTTT-tieng-Viet-1.pdf), bìa và phần mục tiêu2025: Võ Văn Hoàng nghiên cứu chất lượng dữ liệu, suy luận kết hợp và sampling. Các đoạn chương3 được kiểm tra phân biệt phần NIDS với phần malware; không nhập kết quả malware làm NIDS. Chưa đọc đủ27 trang hoặc luận án đầy đủ; không trích số hiệu năng.

## Nguồn chưa đủ dùng cho claim chi tiết

L01–L04, L09–L10 hiện có metadata, nhưng cần đọc nguồn phù hợp để xác nhận claim trong matrix cũ. L02 claim “>20%” và L08 claim “228 variants” không được tự động nhập vào prose cuối chỉ vì có trong ghi chú cũ. L08 abstract có228 nhưng chưa cần con số này cho lập luận. U01/U03 warnings giữ nguyên.
