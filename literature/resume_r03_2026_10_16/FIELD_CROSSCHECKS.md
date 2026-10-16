# P18 — kiểm chứng trường metadata r03, 16/10/2026

Contract: kế thừa 12 DOI đã resolve và 4 mục metadata-verified của r02; đối chiếu 8 mục còn treo bằng nguồn publisher/tác giả/cơ sở đào tạo. Output là ledger có trạng thái riêng từng mục, BibTeX subset, source captures và validation. Không dùng xác minh citation để suy tính hợp lệ phương pháp hoặc hoàn thành P01/P18.

## Kết quả đối chiếu

| ID | Nguồn sơ cấp đã xem | Trường xác nhận thêm | Kết luận / giới hạn |
|---|---|---|---|
| L01 | UNIST indexed PDF first-page, publisher indexed record; capture6 | Title, Tama→Lim, Computer Science Review 39, 2021, 100357 | DOI identity theo Crossref; direct UNIST là JS placeholder. Giữ pending trong lượt này, chưa gắn một publisher record có đủ DOI với các trường cuối |
| L02 | Author-hosted KU Leuven PDF; capture7/8 | Full title, Engelen→Rimmer→Joosen | Proceedings/year/pages chưa đủ second-source trong excerpt. Sáu trang PDF không phải bằng chứng trang 7–12; giữ pending |
| L03 | KU Leuven author publication list r02; search r03 chỉ ra citation trong paper khác | Không có record sơ cấp mới đủ trường | Giữ pending; không dùng bibliography của paper khác như publisher record của L03 |
| L04 | Wiley publisher indexed record; capture6 | Title, Doreswamy→Mohammad Kazim Hooshmand→Ibrahim Gad; CAAI Transactions on Intelligence Technology; 2020; 5(4); 283–293; DOI10.1049/trit.2020.0073 | VERIFIED_METADATA. Direct HTTP403 ghi trong fetch_ledger; xác nhận dựa publisher web result đã lưu. Không nhận đã download/read toàn bài |
| L09 | IRIS institution record; capture1 | Title, Cantone→Marrocco→Bria, 2024 | Volume/pages/DOI chưa đối chiếu đủ trong inspected institutional record; giữ pending |
| L10 | IEEE ComSoc digest, PDF page26 (1-based), capture3/5 | Title, ordered display names, year2024, pages1190–1212 | Giữ pending volume/issue/DOI second-source. Display Shahram Shah Heydari không đủ để tự sửa family token Heydari trong Crossref |
| L11 | UAEU institutional record + KeAi publisher index; capture2/3; saved HTML | Full ordered authors; full title; Data Science and Management; 2025; 8(1); 23–39; DOI10.1016/j.dsm.2024.08.001 | VERIFIED_METADATA. Năm final2025 phân biệt DOI/copyright2024; abstract-only, không audit protocol |
| L12 | RHU author institutional indexed list; capture4 | Ordered authors,2025, Computers14(3),82 | Institutional title rút gọn; MDPI direct lỗi, RHU direct TLS error không bypass. Giữ pending full title/DOI second-source |

Không sửa citation lịch sử hoặc templates/original. Current literature_matrix và refs_verified_subset được nâng từ4 lên6 mục verified; ledger r02 giữ nguyên. U01/U03 dataset warnings chưa có nguồn publisher mới để đóng. Không lấy citation trong paper thứ ba để giải quyết year conflict.

## Reading boundary và claim mới được phép

L02: đọc abstract, introduction và đoạn mô tả các bước audit dataset trên author-hosted PDF (trang1–3; phần III đầu). Tác giả kiểm tra các khâu tạo traffic/flow, gán nhãn, trích feature và benchmark CICIDS2017. Có thể viện dẫn làm động cơ kiểm toán nguồn và pipeline. Không suy UNSW có cùng lỗi hoặc cùng tỷ lệ lỗi; không đưa tỷ lệ/scores L02 vào bảng matched experiments NCKH. Chưa đọc/kiểm toàn bộ kết quả hoặc code của bài.

L04: chỉ metadata, abstract và đoạn introduction trong publisher result. Phân biệt ensemble feature selection (kết hợp các tập feature) với ensemble classifier (kết hợp dự đoán). Không kết luận thứ tự fit/split hoặc leakage từ abstract.

L11: metadata và institutional abstract. Có thể nói bài xem xét feature selection/normalization trên nhiều IDS datasets, gồm UNSW-NB15. Không dùng Accuracy của abstract làm baseline so ngang với protocol NCKH hoặc kết luận về nested validation.

Các source đầy đủ: [Wiley L04](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/trit.2020.0073), [UAEU L11](https://research.uaeu.ac.ae/en/publications/effects-of-feature-selection-and-normalization-on-network-intrusi/), [IEEE digest](https://www.comsoc.org/system/files/2024-03/Publications_Contents_Digest_2024_Mar.pdf), [KU Leuven L02](https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf).

QA: validation.json kiểm 12 DOI/title identities, uniqueness, số lượng subset và matrix/ledger consistency. Đây là kiểm bookkeeping; field-level corroboration là bảng review ở trên. P18 tổng thể PARTIAL; còn6 legacy entries và U01/U03. Raw fetch failures giữ nguyên, không mô tả thành successful download.
