# Review folder mẫu báo cáo NCKH

Đường dẫn: `DE-TAI-NCKHSV-15/`. Đã đọc các file `.tex`, `.sty`, `.bib` hiện có. Folder này là **template/demo của một đề tài khác về phát hiện và phân loại Android malware bằng deep learning**, không phải dữ liệu đầu vào thực nghiệm NIDS.

Một `development_metrics.csv` có 12 dòng cũng xuất hiện trong `results/ablation/unsw_nb15/phase13_ablation/` nhưng không có trong inventory tiếp quản trước đó và không được analysis script đọc. Giữ nguyên như artifact chưa rõ provenance; output canonical Phase 13 nằm trong `phase13_ablation_matrix.csv` với input hashes trong `analysis_metadata.json`.

## Thành phần

- `main.tex`, `styles/settings.tex`, `thesis.sty`: cấu trúc luận văn và định dạng bìa/trang.
- `chapters/chap-0.phan-mo-dau.tex`, `chap-1-background.tex`, `chap-2-method.tex`, `chap-3.tex`, `conclusion.tex`: text mẫu, cần thay/biên soạn theo đề tài NCKH hiện tại.
- `pages/`: declaration, acknowledgments, abbreviations mẫu.
- `refs.bib`: chỉ vài mục tham khảo mẫu; không đại diện bibliography cho NIDS.
- `assets/`, `figures/`: logo và hình Android/CNN minh họa.

## Nội dung phải loại khỏi evidence NIDS

`chap-2-method.tex` có bảng UNSW-NB15 test với LR Macro/F1-style numbers (ví dụ LR 0.904, RF 0.936, CNN 0.952), XGBoost và SVM; không khớp frozen pipelines/evidence của project. Đây là nội dung mẫu, không được trích như kết quả nghiên cứu. Các đoạn về Drebin/CICAndMal2017/CICMalDroid2020, Android permissions, RNN/CNN/deep learning cũng thuộc đề tài khác. Template còn có duplicate placeholder sections/figures, citation dạng `[5]` không map chắc chắn sang `.bib`, và `refs.bib` gồm tài liệu ví dụ `latex2e`/Deep Learning cùng một paper Android.

## Cách dùng khi tới original Phase 17

Giữ template làm tài liệu tham khảo riêng; không ghi đè gốc ở Phase 13. Khi bắt đầu viết báo cáo, tạo working copy có provenance, cập nhật title/authors/supervisor/year theo thông tin user xác nhận, thay từng chapter bằng nội dung dựa trên evidence đã khóa, thay placeholder tables/figures và chuẩn hóa toàn bộ citations/bibliography. Phải chạy compile/QA khi tới phase đó; chưa compile hoặc sửa template trong lần review này.

## CHECKPOINT

| ID | Task | Status | Evidence |
|---|---|---|---|
| T-01 | Nhận diện loại template và cấu trúc file | DONE | File tree `DE-TAI-NCKHSV-15/` |
| T-02 | Đánh dấu nội dung mẫu không thuộc NIDS evidence | DONE | `chapters/chap-2-method.tex`, `refs.bib`, chapter samples |
| T-03 | Chuyển template sang báo cáo NIDS | TODO | Original Phase 17; chưa chỉnh template |
