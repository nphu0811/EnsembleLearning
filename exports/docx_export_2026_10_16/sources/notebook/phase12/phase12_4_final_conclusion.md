# PHASE 12.4 — FINAL CONCLUSION

> Trạng thái: bản nháp kết luận cuối cho báo cáo.  
> Mục tiêu: chốt kết quả nghiên cứu, trả lời các RQ, nêu đóng góp và hướng phát triển mà không lặp lại toàn bộ Discussion.

# 11. Kết luận

Nghiên cứu này khảo sát hiệu quả của Ensemble Learning cho bài toán phát hiện xâm nhập mạng trên UNSW-NB15 theo một quy trình thực nghiệm kiểm soát leakage, giữ official test độc lập với giai đoạn Feature Selection, model comparison và tuning. Thay vì chỉ so sánh Accuracy hoặc chọn mô hình có điểm số cao nhất, nghiên cứu đánh giá đồng thời hiệu năng dự đoán, cấu trúc lỗi, error complementarity giữa các base learner, chi phí tính toán và độ bất định thống kê.

Kết quả cho thấy Random Forest là một strong individual/reference model trong phạm vi các pipeline được khảo sát. Hard Voting và Soft Voting không cải thiện Macro-F1 so với Random Forest trong development analysis. Stacking tận dụng được thông tin bổ sung giữa Logistic Regression, Decision Tree và Random Forest tốt hơn Voting, nhưng trên official holdout không cho thấy ưu thế tổng thể rõ ràng so với RF-42 về Macro-F1, MCC hoặc overall paired correctness.

Sự khác biệt đáng chú ý nhất giữa Stacking-42 và RF-42 nằm ở cấu trúc lỗi. Stacking-42 giảm false-positive rate nhưng đồng thời tăng false-negative rate. Vì vậy, tác động chính của Stacking trong nghiên cứu này không phải là tạo ra một mô hình vượt trội toàn diện, mà là dịch chuyển điểm cân bằng giữa cảnh báo giả và tấn công bị bỏ sót. Kết quả này nhấn mạnh rằng trong NIDS, việc đánh giá ensemble chỉ dựa trên một metric tổng hợp có thể che khuất những khác biệt vận hành quan trọng.

Feature Selection cũng thể hiện một trade-off rõ ràng. RF-17 có hiệu năng dự đoán thấp hơn RF-42 một lượng nhỏ trên official test, nhưng giảm mạnh thời gian huấn luyện, thời gian suy luận và kích thước mô hình. Do đó, lợi ích nổi bật của Feature Selection trong nghiên cứu này nằm ở computational efficiency hơn là cải thiện predictive performance.

Phân tích diversity cho thấy các base learner có complementary errors, nhưng sự tồn tại của diversity không tự động bảo đảm ensemble gain. Kết quả Hard/Soft Voting và Stacking cho thấy hiệu quả cuối cùng phụ thuộc không chỉ vào việc các model mắc lỗi khác nhau, mà còn vào cách các prediction được kết hợp.

Ngoài ra, official-holdout performance thấp hơn đáng kể so với development CV, và cả ba frozen pipeline đều giảm performance trên novel-vector subset. Kết quả này cho thấy đánh giá NIDS nhạy với evaluation protocol/view và nhấn mạnh tầm quan trọng của việc giữ final holdout độc lập. Tuy nhiên, nghiên cứu hiện tại chưa đủ bằng chứng để quy sự suy giảm này cho temporal drift hoặc domain shift cụ thể.

---

## 11.1. Trả lời các câu hỏi nghiên cứu

### RQ1 — Ensemble có cải thiện ổn định so với model đơn mạnh hay không?

**Kết luận:** Chưa có bằng chứng cho thấy Stacking-42 cải thiện tổng thể một cách rõ ràng so với RF-42 trên official test.

Stacking-42 có Macro-F1 cao hơn RF-42 một lượng rất nhỏ, nhưng paired bootstrap CI của chênh lệch chứa 0; MCC cũng không cho thấy lợi thế rõ. Exact McNemar sau Holm correction không cho thấy khác biệt về overall paired correctness.

Tuy nhiên, Stacking-42 tạo ra một trade-off có bằng chứng rõ hơn:
- FPR thấp hơn,
- FNR cao hơn.

Vì vậy, ensemble trong nghiên cứu này không thể được kết luận là “tốt hơn” strong baseline một cách tổng quát.

---

### RQ2 — Feature Selection ảnh hưởng thế nào đến hiệu năng và chi phí?

**Kết luận:** Feature Selection tạo ra computational gain lớn với một predictive cost nhỏ.

RF-17:
- train nhanh hơn đáng kể RF-42,
- inference nhanh hơn,
- model nhỏ hơn gần một nửa,
- nhưng Macro-F1/MCC thấp hơn một lượng nhỏ trên official test.

Vì vậy, Feature Selection nên được xem như một công cụ tối ưu performance–cost trade-off thay vì một cơ chế bảo đảm tăng Accuracy.

---

### RQ3 — Ensemble improvement có liên quan đến complementary errors hay không?

**Kết luận:** Complementary errors tồn tại, nhưng không đủ để bảo đảm ensemble superiority.

OOF analysis cho thấy LR, DT và RF có những vùng lỗi khác nhau và có khả năng “cứu” nhau ở một số sample. Tuy nhiên:
- Voting không vượt RF,
- Stacking chỉ cải thiện rất nhỏ về aggregate metric,
- lợi ích rõ hơn nằm ở việc thay đổi FP/FN trade-off.

Do đó, diversity là điều kiện hữu ích cho ensemble design nhưng không phải điều kiện đủ cho net performance gain.

---

### RQ4 — Kết quả nhạy thế nào với evaluation protocol/view?

**Kết luận:** Performance nhạy với evaluation view, nhưng RQ4 chỉ được trả lời một phần.

Các model đạt điểm development CV cao hơn đáng kể so với official holdout, và performance tiếp tục giảm trên novel-vector test. Điều này cho thấy generalization estimate phụ thuộc vào cách đánh giá.

Tuy nhiên, nghiên cứu chưa thực hiện được temporal/day/scenario split trực tiếp, nên chưa thể kết luận nguyên nhân của sự suy giảm là temporal drift hoặc domain shift.

---

## 11.2. Đóng góp chính

Đóng góp của nghiên cứu chủ yếu nằm ở thiết kế và đánh giá thực nghiệm, bao gồm:

1. Xây dựng một leakage-aware, holdout-preserving evaluation protocol cho individual và ensemble classifiers trên UNSW-NB15.
2. Lựa chọn và phân tích ensemble dựa trên OOF error complementarity thay vì chỉ dựa vào single-model score.
3. Ghi nhận và giữ lại negative result của Hard/Soft Voting thay vì giả định ensemble luôn cải thiện.
4. Định lượng rõ performance–cost trade-off của Feature Selection.
5. Sử dụng paired bootstrap, exact McNemar, Holm correction và Wilson interval để tránh overinterpret các chênh lệch nhỏ.
6. Bổ sung novel-vector sensitivity view để kiểm tra robustness trong cùng benchmark.
7. Phân tích attack-family failure modes của binary detector thay vì chỉ báo cáo aggregate metric.
8. Duy trì workflow có thể tái lập từ audit, Feature Selection, model comparison, final holdout đến statistical analysis và reporting.

Các đóng góp này không được xem là một ensemble algorithm mới, mà là methodological và empirical contributions cho cách đánh giá Ensemble Learning trong NIDS.

---

## 11.3. Kết luận thực tiễn

Nếu mục tiêu là tối đa hóa predictive performance trong các pipeline đã đánh giá, RF-42 là một strong reference với hiệu năng tổng thể gần Stacking-42 nhưng chi phí thấp hơn đáng kể.

Nếu ưu tiên giảm false alarms, Stacking-42 có thể hấp dẫn hơn, nhưng phải chấp nhận FNR cao hơn.

Nếu ưu tiên computational efficiency, RF-17 là lựa chọn hợp lý nhờ giảm đáng kể training/inference cost và model size với mức giảm predictive performance tương đối nhỏ.

Do đó, nghiên cứu không đề xuất một “mô hình tốt nhất tuyệt đối”. Lựa chọn pipeline phụ thuộc vào trade-off giữa:
- detection performance,
- false alarms,
- missed attacks,
- computational cost,
- yêu cầu triển khai.

---

## 11.4. Hướng phát triển tiếp theo

Các hướng nghiên cứu tiếp theo phù hợp nhất gồm:

- external validation trên corrected CIC-IDS2017 hoặc một benchmark độc lập khác;
- multiclass hoặc hierarchical attack classification;
- temporal/scenario-aware evaluation khi dataset hỗ trợ metadata phù hợp;
- cost-sensitive thresholding trên một validation protocol mới, không tái sử dụng official test;
- nghiên cứu Dynamic Ensemble Selection như một extension độc lập;
- đo thêm RAM, throughput, latency và energy cost;
- grouped/session-level statistical resampling nếu có metadata phù hợp;
- đánh giá robustness trên attack family hiếm với sample size lớn hơn.

---

# 12. Câu kết luận ngắn dùng cho Abstract/Defense

> Nghiên cứu cho thấy Ensemble Learning không tự động vượt một strong individual model trong NIDS. Trên UNSW-NB15, Stacking không tạo ra lợi thế tổng thể rõ ràng so với Random Forest nhưng làm thay đổi đáng kể trade-off giữa false positive và false negative. Feature Selection mang lại lợi ích tính toán lớn với một mức giảm nhỏ về predictive performance. Kết quả nhấn mạnh rằng evaluation protocol, error structure và computational cost cần được xem xét đồng thời khi đánh giá ensemble IDS.

---

# CHECKPOINT — PHASE 12.4

| ID | Task | Status | Evidence |
|---|---|---|---|
| P12-09 | Final conclusion draft | DONE | Section 11 |
| P12-10 | Final RQ answers | DONE | Section 11.1 |
| P12-11 | Final contribution summary | DONE | Section 11.2 |
| P12-12 | Practical interpretation | DONE | Section 11.3 |
| P12-13 | Future-work summary | DONE | Section 11.4 |
| P12-14 | Abstract/defense closing statement | DONE | Section 12 |

---

# Trạng thái Phase 12

- Phase 12.1 — Results: **DONE**
- Phase 12.2 — Discussion: **DONE**
- Phase 12.3 — Limitations + Contributions: **DONE**
- Phase 12.4 — Final Conclusion: **DONE**

Phase 12 hiện đã hoàn tất ở mức nội dung draft.
