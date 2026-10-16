# R04 — assembled content: evidence and citation review

Ngày 16/10/2026. Đối tượng: `proposal/researchwrite/nckh-ids/drafts/De_cuong_noi_dung_review_r04.md`, phiên bản 178 dòng được đọc trong lượt này. Vai trò độc lập, giới hạn ở scientific evidence, citations và source resolver. Không review độ đầy đủ form, tài nguyên triển khai hoặc render; không ghi đây là DOCX QA, phê duyệt hành chính, P20 hoặc toàn bộ release acceptance. Chỉ ghi file review này; không sửa draft, source, memory, dữ liệu hay kết quả.

Áp dụng `researchwrite` từ `C:/Users/admin/.codex/skills/nature-proposal-writer/SKILL.md` cùng `references/evaluation-rubric.md` và `references/research-anti-slop.md` đã đọc. Đối chiếu foundation00–07, foundation_review_r02, r04 ledger/source map/reading notes/captures đã đọc ở review độc lập trước, current verified BibTeX và sources được resolver dẫn. Không tra web mới hoặc chạy thí nghiệm. Sự nhất quán của nguồn lưu không chứng nhận toàn bộ lịch sử thực thi.

## Kết luận giới hạn

**Không phát hiện P0/P1 trong phạm vi nội dung được review. KEEP_INTERNAL_CONTENT_DRAFT; sửa P2 trước đưa thành bản nội dung để GVHD đọc.** RQ, contribution và causal/statistical limits nhất quán với foundation. Không có L03 trong metadata bibliography được viện dẫn; phần conflict còn được nêu ở dòng77. Không thấy dùng scores paper khác làm matched baseline hoặc tự nhận full-paper/systematic review.

## Findings

**P2 — dòng136,151,157: resolver dẫn nguồn hiện còn một số đếm bibliography cũ.** `docs/CLAIM_EVIDENCE_MATRIX.md` được dùng cho M:N3, T:N2, P:S2. C15 trong tài liệu này hiện ghi subset “chỉ4 mục”, trong khi current `literature/refs_verified_subset.bib` có11 mục metadata verified, loại L03; nội dung assembled dòng77 nói11. M:N3 giới hạn rõ C03–C11, nên chưa làm sai luận điểm số liệu được cite. Tuy nhiên T:N2/P:S2 không khoanh phạm vi C-ID; người đọc theo resolver có thể gặp thông tin hiện trạng mâu thuẫn. Sửa C15 thành ghi chép lịch sử có nhãn checkpoint, hoặc cập nhật current source pointer/status sang r04 với11/12 và L03 CHECK_SUGGESTED. Không tăng reading depth hoặc gọi bibliography final hoàn tất khi sửa count.

**P2 — dòng146,148–152: namespace T mới có quy ước ngầm, và còn lỗi chữ/số dính.** Các citation `[T:L..]`, `[T:D..]`, `[T:N..]` đều có thể resolve bằng heading “Nguồn T” + ledger/list, nhưng các entry vẫn in `D01`, `N1` và các cụm `nhãnL`, `dùngL01`, `lịch31/12/2022`. Để bộ resolver tự chứa, đổi label hiển thị thành `[T:D01]`, `[T:N1]`... và ghi rõ `[T:Lxx] → ledger row id=Lxx → metadata/reading note`. P:S1–S7 có quy ước tương tự, có thể chuẩn hóa cùng cách. Đây là độ rõ của đường truy vết, không phải phát hiện nguồn bị thiếu hoặc nhãn trỏ sai.

**P2 — dòng167–176: metadata appendix còn dạng xuất thô.** Các `39()`, `212()`, `():`, brace `{Doreswamy}`/`{Imran}` là sản phẩm serialization/BibTeX, không phải trường metadata sai. Giữ nguyên tên/tokens trong data source, nhưng bỏ dấu ngoặc issue rỗng và brace khi trình bày cho người đọc; ghi rõ article number cho100357/103560/120420/82 để không làm chúng giống khoảng trang. Đây không phải lý do sửa DOI/year/authors đã đối chiếu.

## Resolver và kiểm chứng nội dung

| Nhóm | Kết quả đối chiếu | Ranh giới |
|---|---|---|
| M:N1–N4 | Các path trong dòng132–138 tồn tại;06 map RQ nguyên gốc,07 tách replay/reconstruction/demo, framework/freeze/protocol và claim matrix hỗ trợ Methods | M:N3 chỉ C03–C11; counts/current metadata C15 cần sửa P2 nếu dẫn toàn matrix |
| M:L05–L07 / M:D01–D02 | DOI/tác giả/năm khớp ledger; D01/D02 resolve tới DOMESTIC_SOURCES có loại nguồn và depth | Không lấy mục tiêu luận án làm kết quả; chưa full-paper/thesis review |
| T:L01,L02,L04–L09,L11,L12 | Ledger và metadata appendix thống nhất; các nhận định khớp scoped source passages | L09 chỉ indexed Introduction; L12 selected publisher-indexed Methods; không gọi direct download/full review |
| T:D01–D02 / T:N1–N3 | Institutional URLs và local notes đủ để resolve chủ đề, lịch/cover và RQ/gap limits | D01 lịch không chứng nhận bảo vệ thành công; D02 cover2025 không chứng nhận cấp bằng |
| P:S1–S7 | Canon/claim matrix/07/framework/template pointer/06/data-code note tồn tại và phù hợp mục đích dùng | Chỉ kiểm source resolution; không xác nhận form/administration/render trong vai trò này |
| Pipeline/numbers dòng31 | Protocol P15-04 xác nhận175341/82332, ba candidates, threshold0.5 và source lines; framework ghi LR/DT/RF→LR, predictor exclusions | Source+metadata static không thay training replay; draft nói rõ điều này |
| Metrics/statistics dòng33,39 | Saved final_metrics có các metrics được nêu; cost_metrics có train/inference times; paired bootstrap Macro-F1/MCC Stack−RF42 CI chứa0 | Không suy equivalence; McNemar không test trực tiếp Macro-F1; row bootstrap không repeated-training stability |
| Error trade-off dòng39 | official RF42 FP10003/FN734, Stack42 FP9861/FN852: giảmFP142/tăngFN118 | Draft chỉ nêu chiều thay đổi; không generalize lợi ích tổng thể |
| Replay/Q&A dòng94,97 | clean_replay_report:3 CSV byte-identical, training NOT_PERFORMED; defense/qa_validation_r02.json question_count20, full_defense_ready=false | Đúng là hậu xử lý và Q&A nội bộ, không ML/demo/defense readiness |

Chiều đọc nguồn không tự tăng vì metadata11/12 đã verified. L03 vắng khỏi verified subset; L10 nằm trong subset nhưng không được viện dẫn ở prose/metadata appendix, điều này không phải orphan citation. Không cần thêm L10 để làm đầy phần tổng quan.

## Chronology và giới hạn khoa học

Dòng3,25,55,114 phân biệt hồ sơ phục hồi và công việc cần làm, không tạo phê duyệt hồi tố. Dòng35,73,75 giữ selection trên full TRAIN trước development folds, meta tuning chưa fully nested, RF17/RF42 còn khác cấu hình, official/novel cùng benchmark, RQ4 partial và RQ5 controlled intervention chưa được trả lời. Dòng83,94,96 giữ model/retraining/demo chưa đạt. Dòng39 không chuyển CI chứa0 thành bằng chứng equivalence. Không cần đổi dữ liệu/RQ hoặc mở TEST để sửa các P2 trên.

## Tám điểm chủ quan, chỉ cho nội dung

Adapt rubric proposal cho NCKH IDS: feasibility ở đây là tính kiểm được của narrative/source chain, không audit tài nguyên; innovation là positioning cụ thể, không đòi thuật toán mới. Đây không phải điểm thực nghiệm hoặc bằng chứng hoàn thành.

| Chiều | Điểm/10 | Nhận xét |
|---|---:|---|
| Rõ vấn đề |8.0| Local comparison và RQ status được nối tới06 |
| Known→unknown→ý nghĩa |8.0| Prior components dẫn tới bounded trade-off case study |
| Evidence matching |8.0| Nguồn/limits rõ; còn source C15 cũ cần reconcile |
| Chuỗi lập luận |8.0| Mục tiêu–phương pháp–kết quả/sản phẩm nhất quán trong scope |
| Kiểm được của phương pháp |7.5| Source/metadata và gates cụ thể, chưa ML replay |
| Positioning/đóng góp |7.5| Đóng góp audit/trade-off cụ thể, không nhận field-wide novelty |
| Ranh giới rủi ro |8.5| Chronology, inference limits và sản phẩm còn thiếu không bị che |
| Ngôn ngữ |7.0| Không cường điệu; resolver/metadata còn dấu vết xuất thô |

Trung bình chủ quan **7.8125/10**. Recommendation chỉ là **nội dung nội bộ có thể giữ và sửa P2**. Không suy từ điểm này rằng đề cương đầy đủ, DOCX đã điền/render, bibliography hoàn tất hoặc các G0–G6 đã PASS. Một repair ưu tiên: reconcile current bibliography count/pointer trong nguồn C15 được các resolver dẫn tới, sau đó kiểm lại cả nội dung assembled và resolver cùng nói11/12 với L03 unresolved.
