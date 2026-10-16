# Contract bộ hỏi đáp chuẩn bị bảo vệ

Purpose: chuẩn bị20 câu hỏi phương pháp, thống kê, prior art, reproducibility và giới hạn sản phẩm từ evidence đã khóa. Scientific justification: hội đồng cần đánh giá claim không vượt dữ liệu. Inputs: claim matrix, framework, frozen metric/statistical tables, release blockers. Output: Hoi_dap_hoi_dong.md.

Implementation: câu hỏi→câu trả lời ngắn→đường dẫn evidence cụ thể. Tests: có>=15 câu, mọi path trích dẫn tồn tại, con số đối chiếu aggregate tables, không claim multiclass/live inference/novelty/superiority khi thiếu. Common failure: nhầm McNemar correctness với Macro-F1, bootstrap resamples với repeated training, sample predictions/model-size với model artifact. Repair bằng đối chiếu source, không tính thêm TEST metrics.

Downstream: defense slides/script và simulated review về sau. Gate hiện tại: DRAFT_FOR_REVIEW; kiểm structure/path/numbers có thể PASS nhưng chưa có rehearsal, council review hoặc slides. Không đánh P20/G6 DONE từ tài liệu này.
