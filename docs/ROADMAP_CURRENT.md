# Roadmap hiện hành sau resume ngày 16/10/2026

Checkpoint r04 ưu tiên: docs/RESUME_AUDIT_R04_2026-10-16.md. REF11/12metadata verified,L03warning;source-linked readings,gap/relatedwork vàformcontentassembly có;fullargumentreviewpendingusage limit. FreshTRAINsubsetsoftware smoke45/45 khôngfinalmodelreproduction. Defense script/runbook/checklistdraft có,khôngslides/demo. P15/P01/P18/P17/G0–G6 khôngtựDONE. Task graph/contracts docs/R04_TASK_CONTRACTS.md,task JSON .research_memory/r04/.

Checkpoint r03: docs/RESUME_AUDIT_R03_2026-10-16.md. P18 xác nhận metadata thêm L04/L11:6/12 legacy records verified,6 pending; U01/U03 giữ warning. Proposal có partial draft nhu cầu/sản phẩm/tiến độ/kinh phí theo form; chưa DOCX/PDF hoặc full proposal. Hai stale memory hashes vào phiên được audit riêng;282/282 historical files nguyên. DOCX có8 bảng (đính chính ghi chép9), ZIP15 entries không DOCX. Không mở lại experiment/model selection.

Đây là reconciliation bổ sung; giữ audit cũ như lịch sử. Trạng thái `VERIFIED_REUSE` chỉ là kế thừa evidence trong phạm vi đã thực hiện, không mở rộng thành hoàn thành mọi yêu cầu của MASTER.

| Phase | Trạng thái hiện tại | Evidence / việc còn thiếu |
|---|---|---|
| P00 | PARTIAL | Frozen RQ ở notebook/phase01; phục hồi canon và proposal foundation; giả thuyết tiên nghiệm không được tự bịa sau test |
| P01 | PARTIAL | literature/gap matrices có; thiếu screening log đầy đủ, kiểm chứng toàn bộ bibliography và nguồn trong nước |
| P02 | VERIFIED_REUSE trong scope UNSW | 3 raw checksum PASS; nguồn UNSW; CIC chỉ candidate chưa external validation |
| P03 | VERIFIED_REUSE có giới hạn | Audit/overlap/view outputs có; raw integrity PASS; không tuyên bố split không leakage |
| P04 | VERIFIED_REUSE cho EDA | Bảng/hình EDA có; publication QA riêng P16 |
| P05 | PARTIAL so với contract mới | Stable subsets có; FS ngoài development folds phải công khai, không làm lại để hợp thức hóa |
| P06 | VERIFIED_REUSE có giới hạn | Baseline folds/aggregates có; selection optimism giữ nguyên |
| P07 | VERIFIED_REUSE có giới hạn | OOF/diversity/voting/stacking có; giữ negative results |
| P08 | DOCUMENTATION_CLOSURE | Framework note chính thức bổ sung từ source/freeze; không thuật toán mới |
| P09 | PARTIAL | Class-weight/no-resampling scope; không có matched resampling ablation |
| P10 | VERIFIED_REUSE có giới hạn | phase8 frozen configs, no test-loaded; meta tuning không fully nested |
| P11 | VERIFIED_REUSE binary | 3 CSV closure tái lập từng byte trong venv mới; không phải multiclass |
| P12 | VERIFIED_REUSE có giới hạn | phase10 CI/McNemar có; hashes qua P13 input audit; không rerun bootstrap |
| P13 | VERIFIED_REUSE retrospective | 19 input hash khớp; không full-factorial/component leave-one-out |
| P14 | VERIFIED_REUSE descriptive | Step1/3/4/5 + closure; 375 checks là evidence lịch sử, không nói vừa chạy lại |
| P15 | PARTIAL | Hash/protocol/tests/postprocessing clean replay đạt; training reproduction, original env, model artifact còn thiếu |
| P16 | IN_PROGRESS | Bắt đầu figure QA từ saved tables; draft cũ không tự động đạt |
| P17 | TODO | Có template LaTeX đã bảo quản; chưa có báo cáo IDS build/render đạt |
| P18 | TODO/PARTIAL | Literature list cũ; chưa verified refs.bib cho báo cáo cuối |
| P19 | IN_PROGRESS | Draft availability + inventory; license code, repository/version chưa chốt |
| P20 | TODO | Chỉ review đầy đủ sau khi có manuscript và package; không giả 3 reviewer |

## Thứ tự thực hiện

1. Đóng resume audit, template/registry và sửa persistent memory.
2. P15 hậu xử lý sạch, availability/code inventory và framework note. Không fit/predict hoặc thay frozen evidence.
3. P16 figure từ bảng đã khóa, source-data map và rendered QA.
4. P18 kiểm chứng bibliography + tổng quan trong nước; hoàn thiện foundation đề cương và nội dung theo form.
5. Xử lý môi trường DOCX/LaTeX, tạo báo cáo/proposal có render QA, không lấp trường cá nhân bằng ví dụ mẫu.
6. P15 phần ML reproduction cần kế hoạch thực thi riêng trong output cô lập; công khai environment gốc UNKNOWN. Demo cần model artifact đã kiểm định, không gọi saved-results viewer là live inference.
7. Slides, kịch bản, Q&A >=15 câu và demo runbook; review độc lập theo skill thích hợp, sửa major concerns.
8. G0–G6, checksum manifest, chỉ tạo FINAL_NCKH.zip sau critical gates đạt.

Mọi task có purpose/inputs/outputs/validation ở TASK_BOARD hoặc tài liệu contract đi kèm. Không đợi người dùng ra lệnh chuyển phase; blocker hành chính chỉ chặn phần phụ thuộc.

## Cập nhật lượt r02 ngày16/10

P01/P18: có `literature/literature_matrix.csv`12 records, `literature/gap_matrix.md`, working BibTeX12 entries và metadata-verified subset4 entries. Nguồn domestic D01/D02 đã tìm qua cơ sở đào tạo, reading boundary lưu rõ. Đây là tiến bộ trên partial tasks, không full systematic review/reference closure. Dataset refs U01/U03 warnings giữ nguyên. Proposal foundation nhận các literature facts trong phạm vi đọc, review độc lập đang xử lý trước drafting.
