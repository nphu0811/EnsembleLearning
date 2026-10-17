# P18 đọc và đối chiếu phương pháp — 17/10/2026

**Trạng thái: PARTIAL.** Tiếp nối commit `7c3530e`; không làm lại 119 phép kiểm
tra cũ. Đã đọc các phần phương pháp, thiết lập, kết quả và kết luận liên quan của
**ba công trình L06, L12, N02**, trong shortlist bảy bài. Đây không phải đọc trọn
bảy bài hoặc toàn bộ 12 tài liệu trong báo cáo. Không sửa bibliography/PDF.

## Phạm vi nguồn và QA

- L06, Thockchom và cộng sự (2023), DOI
  [10.1007/s40747-023-01013-7](https://link.springer.com/article/10.1007/s40747-023-01013-7).
  Đọc publisher HTML từ Proposed model/Pre-processing đến các kết quả binary,
  multiclass, so sánh và Conclusion. Phần Methods từng được đọc hẹp ở r04 được
  kế thừa; lượt này mở rộng tới kết quả và giới hạn. Direct PDF trả HTML thử thách,
  không được tính là PDF tải thành công.
- L12, Nassreddine và cộng sự (2025), DOI
  [10.3390/computers14030082](https://www.mdpi.com/2073-431X/14/3/82).
  Xác nhận PDF publisher 23 trang; đọc trang vật lý 5–10 và 11–20, đối chiếu
  identity/license trang 1. Đã xem ảnh thật trang 16–18 để kiểm tra bảng và prose.
  Không nhận đã đọc hết Introduction hoặc References.
- N02, Alsaffar và cộng sự (2024),
  [Shielding networks](https://link.springer.com/article/10.1186/s40537-024-00994-7).
  Đây là bài gần phương pháp được bổ sung từ publisher related-article links.
  Đọc Methodology/Data description/MI-Boruta/Stacked ensemble, Performance
  evaluation, Experimental results và Conclusion/limitations qua HTML publisher.
  Không tải được PDF bằng direct request; không đánh đồng hai đường truy cập.

Các bài N01 (2025, DOI 10.1007/s11227-025-07609-9) và N03 (2026, DOI
10.1007/s12083-025-02172-9) chỉ đọc abstract/metadata publisher. Metadata ba bài
mới đã đối chiếu Crossref với publisher về title, thứ tự tác giả, năm, volume và
article number. L08 vẫn subscription-preview; L09 giữ phạm vi đọc hẹp đã có,
không thay bản journal bằng arXiv preprint. **FULL_TEXT_UNAVAILABLE** được ghi
cho các phần không tiếp cận được bằng các đường hợp pháp đã dùng, không có
nghĩa toàn văn không tồn tại ở bất cứ đâu.

Artifact trong `literature/deep_verification_2026_10_17_01/`:

- `READING_PROTOCOL.md`, `curated_reading.json` và verification ledger.
- `qa_03/literature_comparison_matrix.csv`: bảy bài, tám trục phương pháp bắt buộc.
- `qa_03/claim_to_source_map.csv`: **24 assertion có locator và mức bằng chứng**.
- `qa_03/local_source_manifest.json`: hash/size của các capture giữ cục bộ.
- `qa_03/validation.json`: **136 PASS / 0 FAIL** cho traceability/identity/coverage.

Các phép kiểm tra này xác nhận anchor tồn tại và phép đối chiếu metadata, không
chứng nhận thí nghiệm của tác giả đúng hoặc thay thế phản biện độc lập. QA đầu
`qa_01` có 126 PASS/1 FAIL vì claim C10 trỏ vào capture thiếu đoạn five-fold.
Đã lấy đúng đoạn publisher về stacking, sửa liên kết capture, giữ nguyên kết luận
và bảo tồn kết quả fail. `qa_02` đạt 127/127; `qa_03` thêm chín check metadata mới.

## Đối chiếu quyết định phương pháp

| Trục | Nguồn đọc được | Hệ quả đối với công trình hiện tại |
|---|---|---|
| Split và so sánh số liệu | L06 mô tả random 80/20. N02 nói rõ gộp TRAIN/TEST rồi chia random 80/20, phần 20% dùng cho test/validation | **VERIFIED khác protocol**. Không xếp hạng trực tiếp score của họ với official TEST cố định của NCKH |
| Feature selection và leakage | L06 dùng Chi-square; N02 MI-Boruta; L12 correlation/embedded FS | **VERIFIED có prior art**. Full nesting của các phép fit trong mọi fold chưa được xác lập từ phần đã đọc; không kết tội leakage khi chưa kiểm code |
| OOF stacking | L06 nêu cross-validated base predictions để train meta; N02 mô tả five-fold base CV, MLP meta. L12 nêu LR meta nhưng diễn giải CV chung | Khái niệm OOF/stacking đã có. Không suy từ chữ CV rằng scaler/FS/tuning đều nested đúng; OOF implementation chi tiết của L12 vẫn **UNVERIFIED** |
| Tuning, threshold, imbalance | L12 nêu SMOTE-TOMEK, repeated CV; L06 để augmentation/cost-sensitive improvement ở future work; N02 có tham số và MI cutoff thăm dò | **PARTIAL** về toàn bộ selection protocol. Không gán threshold0.5 hay matched resampling cho bài không nêu. NCKH chưa có đối chứng resampling kiểm soát |
| Metrics và thống kê | Các bài có precision/recall/F1/accuracy; N02 nêu FPR/FNR. Không xác lập được tương đương averaging của F1 hoặc paired inference với Macro-F1/MCC hiện tại | Không đổi F1 thành Macro-F1, không so các loại CI/SD như nhau. CI benchmark-row của NCKH không là training-repeat stability |
| Chi phí | L06 bàn memory/time; N02 có hardware và một bộ computation times; L12 nêu môi trường Colab/desktop | **PARTIAL** về scope đo. Không so thời gian ngắn chưa rõ stage với end-to-end full-TRAIN fit lịch sử |
| Generalization/unknown attacks | L06/N02 đánh giá trên nhiều dataset; L12 đề xuất mở rộng domain ở future work | Separate fits trên hai benchmark không tự trở thành cross-network transfer, temporal split hoặc unknown-attack validation |

Các row đầy đủ giữ trạng thái **VERIFIED/PARTIAL/UNVERIFIED/BLOCKED/
NOT_APPLICABLE** theo từng chi tiết. “Chưa xác lập trong phần đọc” không được
diễn giải thành “bài hoàn toàn không có”. Không chạy code bên ngoài hoặc tái lập
score của paper trong task này.

## Phát hiện cần phản biện và tránh chọn số liệu thuận lợi

**L12 có reporting/scope discrepancy được kiểm tra trên PDF thật.** Accuracy
stacking của CIC ở Table5a trang16 là `0.9997`; đoạn prose gần đó trang17 ghi
`0.9992`; Table7 trang18 ghi `99.99%`. Phép đổi đơn vị thông thường của `0.9997`
là `99.97%`, nên không thể hòa giải tất cả chỉ bằng đổi fraction/percent. Có thể
khác scope thí nghiệm hoặc lỗi trình bày; hiện chưa xác minh nguyên nhân. Ngoài
ra, Methods nhấn mạnh embedded XGBoost trong khi hàng so sánh ghi RF. Giữ cả
các giá trị/locator trong ledger, không chọn một score rồi tự sửa bài hay dùng nó
làm đối chứng thắng/thua. Xem `qa_03/published_reporting_discrepancy.json`.

**N02 cũng có chi tiết cần thận trọng:** Data description ghi TEST `83,332`,
khác `82,332` trong file đã kiểm chứng của NCKH. Không thể suy ra actual CSV của
external experiment chỉ từ typo tiềm năng. Điều chắc chắn hơn và quan trọng hơn
cho so sánh là tác giả mô tả gộp hai partition và random split. Binary/multiclass
results của bài cũng phải tách riêng, không lấy F1 multiclass so Macro-F1 binary.

## Contribution và research gap

**VERIFIED trong phạm vi NCKH:** có frozen official split/config/threshold,
paired effects và FP/FN trade-off truy vết được, phân tích lỗi theo họ tấn công,
novel-vector sensitivity trong cùng TEST, historical performance/cost và giới hạn
được công khai. P15 bổ sung reconstructed full-TRAIN artifact provenance; không
biến nó thành original binary reproduction.

**PARTIAL, chỉ là khác biệt thiết kế:** kết hợp learner cụ thể, stable17/42 track,
official holdout thay vì merged random split, metric emphasis và cách tổ chức
kiểm toán. Những khác biệt này không tự chứng minh thuật toán mới hoặc novelty
đủ chuẩn công bố. Các paper L06/N02 đã đủ bác bỏ tuyên bố rộng rằng stacking +
feature selection + UNSW-NB15 là ý tưởng chưa từng có; N03 bổ sung prior-art topic
gần đây nhưng mới ở abstract scope.

**UNVERIFIED/không được claim:** state of the art; causal feature-count benefit;
fully leakage-free/nested selection; superiority hoặc equivalence từ CI chứa0;
unknown attacks, real-time deployment hoặc external/temporal generalization.

Những thiếu sót cần xử lý là **khoảng thiếu bằng chứng của nghiên cứu này**, không
phải khoảng trống toàn lĩnh vực: nested FS/tuning, matched imbalance/threshold
trade-off, independent training-repeat uncertainty, session/time/host/external
validation và chi phí vận hành. Nếu nghiên cứu tiếp phải có protocol/data/holdout
mới được phê duyệt; không retune TEST hoặc sửa kết quả đóng băng hiện tại.

## Reference blockers và bước tiếp

**L03 BLOCKED_VOR:** IEEE landing/stamp không trả được PDF VOR (direct request
202/empty, web abstract route418). Giữ xung đột254–262/254–263; không đếm thêm
nguồn thứ cấp như cách giải quyết VOR và không sửa bibliography. U01/U03 giữ
đúng follow-up đã xác minh, không hỏi lại hoặc chạy lại check đã đóng.

P18 tiếp theo là quyền truy cập hợp pháp cho các Methods chưa đọc và kiểm VOR
L03. Không mở rộng novelty claim khi corpus còn access/selection bias. P19 có thể
làm độc lập bằng allowlist package, không cần xóa hay untrack ba model smoke.
