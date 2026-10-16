# PHASE 13.3 — MANUSCRIPT AUDIT REPORT

## Audit scope

Bản Phase 13.2 được rà về:
- section numbering;
- duplicated Results/Discussion/RQ statements;
- internal editorial notes;
- citation style;
- terminology consistency;
- Abstract/Keywords;
- claim safety.

## Structural changes

1. Bỏ toàn bộ working headers như `PHASE 13.2`.
2. Bỏ các “Ghi chú sử dụng trong báo cáo” và “Ghi chú biên tập”.
3. Bỏ phần RQ summary lặp lại ở cuối Discussion; RQ answers chỉ giữ ở Conclusion.
4. Bỏ `Limitations-to-future-work mapping` khỏi thân manuscript vì Future Work đã có trong Conclusion.
5. Chuẩn hóa section chính thành:
   - 1. Giới thiệu
   - 2. Công trình liên quan
   - 3. Phương pháp nghiên cứu
   - 4. Kết quả thực nghiệm
   - 5. Thảo luận
   - 6. Hạn chế của nghiên cứu
   - 7. Đóng góp của nghiên cứu
   - 8. Kết luận
6. Chuẩn hóa citation trong Discussion từ author-year sang numeric style `[1]–[6]`.
7. Bổ sung Tóm tắt và Từ khóa dựa trên final evidence.

## Terminology decisions

- `official test`: dùng cho predefined UNSW-NB15 test partition.
- `final holdout`: chỉ dùng khi nhấn mạnh vai trò phương pháp của official test.
- `novel-vector subset/test`: sensitivity view, không gọi là external validation.
- `attack_cat`: metadata cho error analysis, không gọi là multiclass target.
- `RF-42`, `RF-17`, `Stacking-42`: tên pipeline cuối được giữ nhất quán.
- `Macro-F1`, `MCC`, `FPR`, `FNR`: giữ nguyên viết tắt sau khi đã giới thiệu.
- `feature selection`, `ensemble`, `stacking`, `voting`: giữ thuật ngữ tiếng Anh khi dịch sang tiếng Việt dễ gây thiếu chính xác.

## Claim audit

Các claim sau vẫn bị cấm trong bản audited:
- Stacking “significantly better” hoặc “best”.
- Ensemble luôn tốt hơn individual model.
- Novel-vector test là external validation.
- Performance drop là do temporal/domain shift.
- Per-attack error analysis là multiclass classification result.
- RF là model tốt nhất cho NIDS nói chung.

## Automated checks

- working_phase_headers_removed: PASS
- editorial_notes_removed: PASS
- continuous_top_level_sections: PASS
- no_old_section_11: PASS
- bibliography_present: PASS
- abstract_present: PASS
- keywords_present: PASS
- no_todo_marker: PASS

## Remaining manuscript tasks

- Kiểm tra format theo mẫu trường/khoa nếu có.
- Chèn bảng và figure vào vị trí cuối cùng.
- Kiểm tra toàn bộ bibliography nếu thêm nguồn mới ngoài `[1]–[7]`.
- Chuyển sang DOCX/PDF chỉ sau khi cấu trúc manuscript được duyệt.
