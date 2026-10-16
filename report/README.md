# Báo cáo NCKH Ensemble Learning — bản nguồn hiện hành

**Trạng thái 16/10/2026:** báo cáo XeLaTeX gồm **5 chương, 37 trang A4**, theo cách tổ chức của mẫu PTIT được người dùng cung cấp. Bản PDF từ CI đã được kiểm tra kỹ thuật, nhưng chưa phải hồ sơ nộp được khoa/GVHD phê duyệt. Chứng cứ: [P17 Five-Chapter QA](../docs/research/P17_FIVE_CHAPTER_RESTRUCTURE_QA_2026-10-16.md).

## Cấu trúc PDF

Bìa → Lời cam đoan → Lời cảm ơn → **Mục lục → Danh mục từ viết tắt** (giải thích theo đúng vai trò trong NIDS) → Danh sách hình/bảng → năm chương sau → tài liệu tham khảo.

1. **Cơ sở lý thuyết:** bối cảnh NIDS, bài toán nhị phân, LR/DT/RF, Voting, Stacking, OOF, tài liệu liên quan.
2. **Dữ liệu và quy trình tiền xử lý:** official UNSW-NB15, EDA, phân bố lớp, tương quan và overlap.
3. **Xây dựng mô hình và thiết kế thực nghiệm:** pipeline, feature selection, cấu hình RF-42/Stacking-42/RF-17, trình tự train và evaluation.
4. **Kết quả thực nghiệm và đánh giá:** frozen official TEST metrics, paired bootstrap, McNemar, chi phí, sai số.
5. **Thảo luận và hướng phát triển:** kết luận có giới hạn, tính hợp lệ, hướng cải thiện.

**Không có Tóm tắt.** Không chèn các đường dẫn `.md`, `.json` hoặc file nhật ký GitHub trong nội dung PDF; source code có thể nộp riêng. Biểu đồ và bảng số liệu đều xuất phát từ artifact thí nghiệm của project.

## Cấu trúc nguồn

- `main.tex`: định dạng trang, logo/màu PTIT, **đúng năm lệnh `\\chapter{}`** và thứ tự chèn nội dung.
- `frontmatter.tex`: lời cam đoan, lời cảm ơn; **không giả chữ ký**.
- `abbreviations.tex`: bảng từ viết tắt và ý nghĩa trong bài toán phát hiện xâm nhập.
- `chapters/`: các file `.tex` nhỏ được `\\input{}` như **section/subsection**, không còn là tám chương độc lập.
- `references_verified.bib` và `references_dataset_checked.bib`: 12 trích dẫn đang dùng.
- `BUILD.md`: hướng dẫn build bằng CI/TeX; các báo cáo QA cũ về phiên bản tám chương/40 trang mang tính lịch sử.

## Kiểm tra và đồng bộ

GitHub Actions [P17 XeLaTeX build](https://github.com/nphu0811/EnsembleLearning/actions/workflows/p17-latex.yml) tự build lại khi thay đổi source trong `report/`, kiểm tra 30–40 trang, undefined references, `Overfull \\hbox` và missing glyph. Lần xác minh PDF 5 chương đầu tiên: [run 38916942038](https://github.com/nphu0811/EnsembleLearning/actions/runs/38916942038) — PASS.

Đồng bộ máy local (chỉ khi working tree sạch): `git pull --ff-only origin main`. Không tự xóa bản mẫu gốc hoặc kết quả thực nghiệm. Bốn thành viên, mã sinh viên, lớp, mã đề tài, ngày và GVHD đã được điền theo thông tin người dùng cung cấp; nhóm vẫn cần ký thật, đối chiếu hình thức nộp và xác nhận quyền phát hành.

## Giới hạn khoa học không được loại bỏ

So sánh Stacking-42 và RF-42 chưa chứng minh cải thiện Macro-F1/MCC tổng thể; Stacking giảm FP nhưng tăng FN. RF-17 khác RF-42 cả số feature và tham số RF. Feature selection trước development CV, sự trùng vector TRAIN/TEST, meta tuning chưa fully nested, chưa có external/temporal validation và môi trường huấn luyện gốc chưa được xác minh là các giới hạn cần được công bố. Đừng sử dụng official TEST để chọn lại cấu hình sau khi đã đánh giá.

**Nature Skills:** Registry của Codex trên máy Windows có `nature-writing`, nhưng phiên ChatGPT này không có quyền tải/chạy SKILL.md tương ứng; không ghi nhận giả skill execution. Việc biên tập được kiểm chứng bằng report nguồn, bài mẫu và bản PDF thực.
