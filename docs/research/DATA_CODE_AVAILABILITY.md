# Khả dụng dữ liệu và mã nguồn

Trạng thái ngày 16/10/2026: bản dùng cho review nội bộ của đề tài NCKH, chưa phải tuyên bố đã công bố dữ liệu/mã nguồn. Áp dụng workflow `nature-data`; không áp điều kiện nộp Nature cho đề tài sinh viên.

## Data Availability

Nghiên cứu sử dụng UNSW-NB15 với hai file `UNSW_NB15_training-set.csv` (175.341 dòng) và `UNSW_NB15_testing-set.csv` (82.332 dòng). Nguồn truy cập là [trang UNSW-NB15 của UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset), kiểm tra ngày 16/10/2026. Trang nguồn cho phép sử dụng nghiên cứu học thuật, yêu cầu thỏa thuận cho mục đích thương mại và dẫn các tài liệu được liệt kê. Đây không phải xác nhận giấy phép CC-BY hay quyền tái phân phối dữ liệu raw. URL tải lịch sử của bản local chưa được ghi nhận.

Trong workspace bàn giao, dữ liệu raw nằm ở `data/raw/unsw-nb15/`; subset dẫn xuất ở `data/interim/unsw-nb15/test_unseen_vectors.csv`. Kết quả dự đoán đã khóa nằm tại `results/final_evaluation/unsw_nb15/phase9_holdout/tables/official_test_predictions.csv`; bảng chỉ số, chi phí, CI và phân tích lỗi nằm dưới `results/final_evaluation/` và `results/final_analysis/`. Checksum và kiểm tra schema có trong `results/reproducibility/resume_2026_10_16/p15_03_dataset.json`. Checksum chỉ chứng minh đồng nhất với bản local trước đây, không phải fingerprint do nhà cung cấp công bố.

Các file CIC-IDS2017 tại `data/raw/cic-ids2017/` chưa được dùng làm external validation trong nghiên cứu đã khóa. Chưa xác minh corrected release, nên không gộp chúng vào bằng chứng kết luận UNSW.

## Code availability

Source hiện có tại `src/`, công cụ audit tại `tools/`, tests tại `tests/`. Repo local chưa có commit; chưa có public repository, DOI release hoặc software licence được tác giả xác nhận. Không tuyên bố code đã publicly available. Môi trường hiện tại và môi trường import Python 3.14 lịch sử không xác lập original training environment.

`docs/research/REPRODUCIBILITY_RUNBOOK.md` cung cấp smoke hậu xử lý chỉ đọc aggregate tables. Ba CSV P11 tái lập giống từng byte trong venv Python 3.11.9 cô lập. Đây không phải replay huấn luyện và không chứng minh tái tạo runtime gốc. Chưa có serialized model hoặc inference demo đã kiểm định.

## Inventory và access route

| Nhóm hỗ trợ kết quả | Route hiện có | Định danh / vị trí | Điều còn thiếu |
|---|---|---|---|
| UNSW raw | reused public source | Trang UNSW; 3 local file hash | Historical download URL; ghi rõ terms thay vì tự gán license |
| Novel-vector view | local derived data, planned supplement | data/interim/unsw-nb15/; build_unsw_experiment_views.py | Repository/version và README/schema cho phát hành |
| OOF/development outputs | local generated outputs, planned supplement | results/baselines/, results/ensemble/ | Canonical manifest và giới hạn selection optimism |
| Frozen predictions/metrics/cost | local generated outputs, planned supplement | results/final_evaluation/ | Persistent public identifier chưa có |
| CI/ablation/error tables | local generated outputs, planned supplement | results/final_analysis/, results/ablation/ | Source-data map cho từng hình/bảng cuối |
| Software | local project | src/, tools/, tests/ | Licence, versioned archive, ML replay |
| Models | not available locally | Không tìm thấy .pkl/.pickle/.joblib | Không được thay bằng model size CSV |
| CIC candidate | not applicable to current claims | data/raw/cic-ids2017/ | Không claim đã xác minh/công bố |

## Citation và repository actions

Nguồn dataset được dẫn bằng tác giả tập thể UNSW Canberra, *The UNSW-NB15 Dataset*, URL ở trên, ngày truy cập 16/10/2026. Đây là web dataset citation, không tự tạo DOI. P18 cần kiểm chứng đầy đủ metadata năm paper trang nguồn liệt kê trước khi đưa vào bibliography cuối. Không suy ra đã đọc full text từ listing.

Ưu tiên phát hành code + derived tables + manifests trong archive có version/identifier sau khi tác giả chốt quyền chia sẻ và license. Không tạo repository hay gửi dữ liệu ra ngoài trong phiên này. Raw data được hướng dẫn tải từ nguồn, không mặc nhiên bundle.

## FAIR audit

| Trục | Kết quả | Resolution test |
|---|---|---|
| Findable | PARTIAL | UNSW có URL; derived outputs chưa persistent ID |
| Accessible | PARTIAL | Source page truy cập được; chưa thử download route và chưa có public derived archive |
| Interoperable | PARTIAL | CSV/JSON/Python; cần data dictionary/units và liên kết table-panel cuối |
| Reusable | PARTIAL | Có raw/source hashes và pipeline; thiếu code license, original env, ML reproduction |

Thiếu license/repository/version và xác minh thư mục output không thể được giải quyết bằng câu “available upon request”. Giữ các trường đó là PENDING; hồ sơ chưa submission-ready.
