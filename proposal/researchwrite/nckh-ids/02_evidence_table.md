# Evidence table

## Source additions r04

| Claim | Evidence/source | Strength | Usable section | Risk | Status |
|---|---|---|---|---|---|
| Published stacking có CV meta inputs vàrandom80/20 | R04C01; L06 Proposed model | evidence-backed trong đoạn đọc | Tổng quan | Không audit toàn nesting | Scoped source read |
| Cross-dataset train/test khác nhau về nguồn | R04C02; L09 indexed Introduction144490 | evidence-backed | Gap/validity | NCKH novel view không external benchmark | Scoped indexed read |
| Dataset authors công khai labeling/experiment code | R04C03; L03 Tools & Documentation | evidence-backed cho tài liệu tác giả | Luận cứ audit | Không chứng nhận code hoặc lỗi UNSW;page conflict giữ warning | Scoped web read |
| Trong nước có chủ đề ensemble/preprocessing vàvoting/stacking | R04C04/05; D01announcement/D02summary objectives | evidence-backed về chủ đề | Tổng quan trong nước | Không metrics/whole thesis/defense outcome claim | Scoped primary source |

R04C IDs giải tại `literature/resume_r04_2026_10_16/source_claim_map.csv`. Không phải IDs giả của source paper; đây là claim IDs nội bộ.

Evidence-backed chỉ có nghĩa được nguồn chỉ rõ hỗ trợ trong phạm vi đọc/kiểm ghi ở cột risk. Local aggregate validation, publisher Methods/abstract và thông báo chủ đề luận án là ba loại bằng chứng khác nhau; không phải chứng nhận độc lập toàn bộ nghiên cứu. Source verification không đồng nghĩa full-text study review.

| Claim | Evidence/source | Strength | Usable section | Risk | Status |
|---|---|---|---|---|---|
| Có split UNSW 175341/82332 | C01; source UNSW | evidence-backed | Phương pháp | Local hash khác official provenance | evidence-backed |
| Có ba candidate khóa trước final evaluation theo manifest | C02 | evidence-backed | Nội dung/phương pháp | Static evidence không execution proof | evidence-backed |
| Cần xem đồng thời FPR/FNR | C03–C04 | evidence-backed trong dữ liệu này | Mục tiêu/chỉ tiêu | Không generalize mọi mạng | evidence-backed |
| RF17 là phương án chi phí thấp hơn cần đối chiếu hiệu năng | C05 | evidence-backed trong frozen cost table | Kết quả dự kiến/khả thi | Khác hyperparameters và hardware | evidence-backed |
| Diversity bảo đảm gain | C06 | unsupported | Không dùng | Claim quá mức | unsupported |
| Phát hiện unknown attacks ngoài benchmark | C07 | unsupported | Chỉ hướng phát triển | Không external validation | unsupported |
| Resampling vô ích | C08 | unsupported | Không dùng | Không matched experiment | unsupported |
| Chạy lại được bảng aggregate | C09 | evidence-backed | Tính khả thi | Không đồng nghĩa train replay | evidence-backed |
| AutoML + voting/FS không mới tự thân | L05 publisher preview/QUB; DOI10.1016/j.jnca.2022.103560 | evidence-backed phạm vi mô tả phương pháp | Tổng quan/đóng góp | Không full protocol audit | evidence-backed |
| OOF stacking có trong prior work | L06 Methods; DOI10.1007/s40747-023-01013-7 | evidence-backed | Tổng quan/phương pháp | Random80/20 khác official split NCKH | evidence-backed |
| Dynamic undersampling/boosting đã được nghiên cứu | L07 publisher preview; DOI10.1016/j.eswa.2023.120420 | evidence-backed | Tổng quan imbalance | Không suy kết quả binary NCKH | evidence-backed |
| Có hướng ensemble/preprocessing tại Việt Nam | D01 Lạc Hồng; D02 PDF UET | evidence-backed về chủ đề | Tổng quan trong nước | Chưa full thesis, không trích metrics | evidence-backed |

Các C-ID được giải trong `docs/CLAIM_EVIDENCE_MATRIX.md`. Không dùng bảng này thay kiểm chứng paper.
