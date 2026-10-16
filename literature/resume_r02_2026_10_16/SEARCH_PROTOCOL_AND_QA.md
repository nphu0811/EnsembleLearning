# Phạm vi tìm kiếm và kiểm chứng ngày 16/10/2026, lượt r02

Purpose: truy vết 12 mục literature matrix cũ và bổ sung nguồn trong nước phục vụ đề cương; không tuyên bố systematic review hoàn tất. Inputs: notebook/phase01/phase1_literature_matrix.md, frozen RQ, ledger dataset trước. Outputs: raw API metadata, verification ledger, working BibTeX, reading notes, gap map. Downstream: proposal foundation, P18 và chương tổng quan. Pass cho task này: 12 danh tính/DOI được resolve, version không đếm trùng, mọi claim có reading boundary; không yêu cầu mọi mục đạt multi-source verification.

## Workflow đã chạy

Đọc nature-academic-search SKILL, manifest, core/tools, core/routing-and-ops, wf1-multi-source-search, dedup-engine, source-tiers, search-strategy. Đọc nature-ref-verifier SKILL và common-patterns. MCP scholarly chuyên biệt không được expose; dùng Crossref REST trực tiếp và web tìm trang publisher/institutional. Không dùng API key, dịch vụ trả phí hoặc tài liệu tải lậu.

Preflight script của skill: PubMed OK, Crossref OK, arXiv API lỗi chứng chỉ SSL. Không tắt TLS verification. Lượt này dùng Crossref và trang nguồn, không cần PubMed cho IDS. Không gọi đây là đã tìm toàn bộ arXiv.

12 truy vấn Crossref query.bibliographic nằm nguyên văn cùng URL trong `legacy_candidates.json`; raw top3 response của các truy vấn thành công lưu riêng. Có 7 HTTP429 ở discovery. Sau khi biết DOI từ nguồn publisher/institutional, 13 DOI requests (12 final + 1 SSRN) tuần tự thành công; raw `*_crossref_doi.json` lưu đầy đủ. Không đánh rate limit là paper không tồn tại.

Web queries đã dùng gồm tên paper còn thiếu và các cụm: `phát hiện xâm nhập học kết hợp UNSW`; `phát hiện xâm nhập mạng ensemble tạp chí`; `Hoàng Ngọc Thanh học máy phối hợp site:lhu.edu.vn`; `ALID-GAN tạp chí`; `DUEN network ensemble Ren`. Search là discovery, nguồn đưa vào evidence là publisher/institutional, không dùng trang tổng hợp thương mại làm chứng cứ khoa học.

## Chọn và loại

Giữ 12 mục vì đây là danh mục kế thừa cần reconciliation, không phải xếp hạng bằng kết quả có lợi cho stacking. Không nhập các kết quả Crossref lệch chủ đề ở vị trí 2/3. Dedup theo DOI lowercase; SSRN DUEN có DOI khác nhưng là version của cùng nghiên cứu, đếm một study, chọn DOI tạp chí cuối. Các nguồn domestic được chọn do cơ sở đào tạo Việt Nam xác nhận, không suy nguồn trong nước chỉ từ họ tên Việt.

`legacy_verification_ledger.csv`: 12 final records, 4 VERIFIED_METADATA (L05–L08), 8 IDENTIFIED_NEEDS_FIELD_CROSSCHECK. Không gọi cả 12 đã verified toàn bộ fields. L11/L12 không có tác giả trong matrix cũ; nay có author metadata Crossref, chưa coi là đã đọc toàn văn. `legacy_working_references.bib` là bản làm việc, không thay original refs.bib và không được tự động coi final bibliography.

## Giới hạn đọc và QA

L06: đã đọc các đoạn Methods của publisher full HTML, chưa toàn bài. L12: chỉ đọc snippets Methods được search index, direct fetch lỗi429. L05/L07/L08/L11: metadata/abstract/preview. L01 institutional URL hiển thị JavaScript placeholder ở direct open; L02/L03 list bị timeout; L09 author PDF direct403. Giữ các hạn chế này, không lấp bằng suy đoán.

Hai trường hợp dataset refs U01/U03 từ lượt trước vẫn CHECK_SUGGESTED; lượt này không thu được publisher evidence mới để đóng chúng. Không lặp truy cập vô hạn. Các kết luận về split/leakage của paper khác chỉ được đưa ra khi đọc phần tương ứng; không đánh giá paper là leakage-free hoặc có leakage từ abstract.

QA kỹ thuật cuối: parse mọi raw JSON, DOI/title không rỗng, 12 DOI final không trùng, author/year/venue/pages lấy từ record đúng ID, DOI SSRN khác final được khai báo quan hệ. Semantic QA: source pointers và reading boundaries hiện rõ trong các notes. P01/P18 tổng thể vẫn PARTIAL.
