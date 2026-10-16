# R04 — kiểm chứng 6 legacy entries còn treo

Ngày16/10/2026. Contract R04-REF: giải từng field bằng nguồn thực, không tăng trạng thái vì chỉ DOI resolve. Core skills: nature-ref-verifier1.0.1 và nature-academic-search2.0.0 workflow citation-verification. MCP scholarly không expose; dùng Crossref trực tiếp và web publisher/institutional metadata. Preflight thực tế: PubMed OK0.4s, Crossref OK1.1s, arXiv FAIL TLS0.1s; exit1 do2/3 reachable. Không bypassTLS, không cấu hình credential. Đây là citation audit, không systematic discovery mới hoặc cập nhật toàn literature tới2026.

## Fields và source coverage

| ID | Trường được đối chiếu | Source thực tế / capture | Status |
|---|---|---|---|
| L01 | Title, Tama→Lim, Computer Science Review39,2021,100357; DOI | Crossref fresh200; UNIST publisher-PDF first-page indexed ở captures3/7, DOI có cùngURL; direct JS placeholder | VERIFIED_METADATA; online2020/final2021 phân biệt; không đọc toàn PDF |
| L02 | Full title, Engelen→Rimmer→Joosen; SPW2021;7–12;DOI | Crossref fresh200; author institutional project page exact BibTeX/IEEE citation, captures5/6 | VERIFIED_METADATA; nguồn page range đã giải quyết, không suy từ số trang PDF |
| L03 | Title, ordered five authors, CNS2022 và DOI; pages có conflict | Crossref254–262; author project page/index exact BibTeX254–262 (captures9/10); UNSW coauthor254–263 (capture1), KU10pages (capture7); publisher direct robot check | CHECK_SUGGESTED. Giữ254–262 theo working record; chưa chứng nhận đã giải conflict. DBLP middle initialTimothy M. là warning riêng, không tự sửa tên |
| L09 | Full title, Cantone→Marrocco→Bria,2024,DOI; volume12 và144489–144508 | Crossref200; IRIS institutional indexed author-PDF first page (capture7); curated DBLP official record capture10 xác nhận volume/pages; direct PDF403 | VERIFIED_METADATA. Full pagination chưa visually check trên PDF sơ cấp; thông tin pages có Crossref+DBLP agreement. Không claim full-text audit |
| L10 | Title, journal21(1),Feb2024,1190–1212,DOI; ordered authors | Fresh Crossref; IEEE publisher indexed metadata capture3; IEEE ComSoc digest r03 page26 xác nhận display names | VERIFIED_METADATA; online25/7/2023 phân biệt final2024. Không đổi family token chỉ từ display name |
| L12 | Full title, Nassreddine→Nassereddine→Al-Khatib, Computers2025,14(3),article82,DOI | Fresh Crossref; MDPI publisher indexed XML Share and Cite (capture7), DOAJ corroboration capture4 | VERIFIED_METADATA;82 là article number. Direct429 không được gọi thành successful page download |

Các DOI-first API responses6/6 HTTP200 lưu riêng; API ledger có timestamp/hash. Field-specific JSON/CSV status được tạo bởi r04_reconcile_references.py. Machine validation chỉ kiểm saved-record/matrix/BibTeX consistency; không thay manual source matching trong bảng trên.

## Kết luận và blockers

Current verified subset tăng6→11; L03 bị loại khỏi subset vì conflict chưa đóng. Không xóa ledger r02/r03 hoặc sửa bibliography/template gốc. L03 vẫn được nhận diện rõ study và có abstract từ tác giả; chỉ dùng claim trong reading scope với warning bibliography, không đưa vào final bibliography được gọi “fully verified”.

U01/U03 dataset reference warnings: tra cứu bổ sung qua publisher không có đủ field evidence mới, còn nguyên. U01 trang1–6 chưa đủ second-primary trong inspected records; U03 year2017 ở listing so với final volume2019 chưa có publisher indexed final record đủ để đóng. Không dùng bibliography của paper thứ ba để giải quyết. Hai mục này không cản viết tổng quan có nguồn khác, nhưng P18 final còn PARTIAL.

Không tải bài/SI bằng downloader trong task này; chỉ metadata API và nguồn web đã đọc. Router downloader đã xem để đánh giá routing nhưng workflow tải chưa thực thi. Do đó không log nó là skill đã áp dụng; không dùng đường vòng để vượt cửa xác nhận SI hoặc đăng nhập. Bước tiếp theo: source-linked reading theo câu hỏi cụ thể, cập nhật gap map rồi prose.
