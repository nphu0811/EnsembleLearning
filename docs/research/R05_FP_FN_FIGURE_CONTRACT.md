# P16 r05 — FP/FN paired count trade-off

Core question: số lỗi nào thay đổi khi chuyển từ RF42 sang Stacking42 trên cùng official benchmark?

Conclusion giới hạn: Stacking42 có142FP ít hơn và118FN nhiều hơn; không kết luận lợi ích vận hành tổng thể khi chưa có cost matrix. Một panel horizontal paired-count difference, vai trò comparison; không lặp forest plot metric CI đã QA trước đó. Không prior-work image/template adaptation.

Backend Python theo saved preference thật (`nature_figure_backend.py get` trả python), matplotlib hiện có. QA venv mới dùng system-site-packages cho plotting và PyMuPDF cài riêng; đây không môi trường huấn luyện và không giả original environment. Script, versions và export hashes được lưu.

Evidence: chỉ P9 final_metrics.csv, ba candidates giữ nguyên nhưng panel tập trung contrast Stack42−RF42 theo câu hỏi. RF17 không bị xóa khỏi nghiên cứu và có trong bảng P16 companion. Đọc official aggregate rows, không raw/predictions/TEST evaluation hoặc model selection. Source-data CSV có baseline, comparison, delta, denominators. Input hash trước/sau phải khớp.

Export: một panel, 120×65mm; PNG600dpi preview, PDF/SVG editable text. Báo cáo NCKH nội bộ, không claim journal clearance. Mọi glyph≥5pt, font sans-serif9pt, không mathtext thu nhỏ. Direct labels và signed counts, neutral baseline0; màu xanh/orange không phải kênh duy nhất, chữFP/FN và dấu delta phân biệt.

Uncertainty: exact differences của observed aggregate counts trên một benchmark cố định, không mean/repeated training hoặc error bars mới; không thêm CI từ suy đoán. n=82332 gồm37000Normal/45332Attack; units là counts. Conditional-rate CI đã lưu ở bảng companion/forest plot riêng; hình không thay repeated training/generalization evidence.

QA trước delivery: numeric/input hash; source validator; render-time alignment JSON phải ghi NOT APPLICABLE cho single panel; PDF glyph audit; collision audit và Python PNG visual inspection. FAIL cần repair và output vòng mới, không nới global tolerance hoặc che labels bằng box trắng. Các WARN phải giải thích. Caption giữ chronology/selection/environment limits qua companion tables. Không đóng toànP16/G4/G6 bằng một hình.
