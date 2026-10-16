# Kiểm chứng tham chiếu dataset ngày 16/10/2026

Phạm vi: 5 tài liệu trang chính thức UNSW-NB15 yêu cầu dẫn. Mục đích là tạo metadata đúng trước khi soạn bibliography, không review kết quả khoa học của paper. Đã áp dụng nature-ref-verifier, gồm DOI-first và so sánh field; đọc references/common-patterns.md khi phát hiện sai lệch năm.

## Kết quả

| ID | DOI | Kết quả | Đối chiếu |
|---|---|---|---|
| U01 | 10.1109/MilCIS.2015.7348942 | CHECK_SUGGESTED | Crossref + record UNSW khớp title/authors/year/DOI. Trang IEEE bị chặn 418; pages 1–6 chỉ có trong metadata Crossref của lượt kiểm này |
| U02 | 10.1080/19393555.2015.1125974 | VERIFIED_METADATA | Crossref + publisher indexed page khớp hai tác giả, title, 2016, tập 25(1–3), trang 18–31. Không lấy 2015 trong DOI làm năm xuất bản |
| U03 | 10.1109/TBDATA.2017.2715166 | CHECK_SUGGESTED | Crossref ghi final 2019, 5(4), 481–494, tác giả Nour Moustafa; Jill Slay; Gideon Creech. UNSW listing ghi 2017; chưa đọc được IEEE để chốt lịch early-access. Không tự khẳng định ngày online |
| U04 | 10.1007/978-3-319-59439-2_5 | VERIFIED_METADATA | Crossref + Springer khớp tác giả Moustafa, Creech, Slay, 2017, trang 127–156, DOI |
| U05 | 10.1007/978-3-030-72802-1_9 | VERIFIED_METADATA | Crossref + Springer khớp bốn tác giả, 2021, trang 117–135. BDTA 2020/WiCON 2020 là nhãn hội nghị, tách khỏi năm xuất bản proceedings |

Không phát hiện DOI gán sang paper khác trong 5 phản hồi Crossref thành công. `VERIFIED_METADATA` không xác nhận full text, experimental findings hoặc toàn bộ bibliography của đề tài.

## Nguồn và cách kiểm

1. [Trang UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset) cung cấp danh sách và điều kiện sử dụng.
2. Truy vấn trực tiếp `https://api.crossref.org/works/<DOI>`; phản hồi raw lưu `crossref_*.json`. U01/U03 lần đầu gặp HTTP 429; retry tuần tự thành công. Giữ initial summary, lưu retry riêng, không coi rate limit là DOI không hợp lệ.
3. [UNSW conference publications](https://research.unsw.edu.au/people/associate-professor-nour-moustafa/publications?type=conferencepapers) xác nhận U01; [UNSW publication listing](https://research.unsw.edu.au/people/associate-professor-nour-moustafa/publications?page=3) xác nhận U03 nhưng năm chưa khớp final Crossref.
4. [Publisher U02](https://www.tandfonline.com/doi/abs/10.1080/19393555.2015.1125974) được đọc qua search index khi direct open trả 403; field-level source availability được ghi trung thực.
5. [Springer U04](https://link.springer.com/chapter/10.1007/978-3-319-59439-2_5) và [Springer U05](https://link.springer.com/chapter/10.1007/978-3-030-72802-1_9) mở được trực tiếp. Nội dung đọc là trang metadata/abstract, không full chapter.

`reference_verification_ledger.csv` giữ field-by-field source, status, lý do. `dataset_references.bib` là bibliography làm việc cho 5 mục, chưa phải refs.bib cuối và chưa import vào template gốc. U03 dùng năm final 2019 theo Crossref, có note về listing 2017; phải xử lý cảnh báo trước khi P18 toàn bộ đóng.

## Việc kế tiếp

Kiểm U01/U03 trên publisher hoặc repository tác giả hợp pháp để đối chiếu fields còn thiếu. Mở rộng ledger cho literature matrix cũ và bổ sung nghiên cứu trong nước. Đọc nguồn đầy đủ trước khi dùng claim phương pháp/kết quả vượt abstract. Không dựng RQ hay novelty từ metadata alone. P18 và P01 tiếp tục PARTIAL.
