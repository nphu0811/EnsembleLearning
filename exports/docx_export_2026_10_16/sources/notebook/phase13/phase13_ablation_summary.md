# ORIGINAL PHASE 13 — ABLATION SYNTHESIS

Ngày: 04/10/2026. Nguồn: saved TRAIN-only development OOF Phase 7.1/7.2; same-grid Phase-8 summaries; frozen Phase-9 metrics and Phase-10 paired statistics. Không train model, không nạp official TEST vào ablation runner và không tạo statistical tests mới.

## Main comparisons: 42 features, pooled TRAIN OOF

| Pipeline | Macro-F1 | MCC | FPR | FNR |
|---|---:|---:|---:|---:|
| LR | 0.9218 | 0.8498 | 17.80% | 1.21% |
| DT | 0.9368 | 0.8738 | 7.44% | 4.63% |
| RF | 0.9504 | 0.9016 | 9.42% | 1.82% |
| Hard Voting (LR+DT+RF) | 0.9473 | 0.8963 | 10.94% | 1.45% |
| Soft Voting (LR+DT+RF) | 0.9468 | 0.8941 | 9.52% | 2.25% |
| Stacking (LR+DT+RF) | 0.9515 | 0.9032 | 8.05% | 2.37% |

Các metric được tính lại từ predictions OOF đã lưu. Pooled OOF không phải sáu lần lặp độc lập. Fold means ± SD (descriptive) trong S72 cũng cho cùng thứ hạng chính: RF-42 Macro-F1 0.95039 ± 0.00085; Hard Voting 0.94732 ± 0.00145; Soft Voting 0.94676 ± 0.00125; Stacking 0.95148 ± 0.00083. Không dùng SD của ba folds làm CI/SEM.

Voting không vượt RF trong development CV. Stacking hơn RF khoảng 0.0011 Macro-F1 ở pooled OOF; chênh lệch số học nhỏ này là development evidence và không phải bằng chứng robust superiority. Mẫu lỗi trade-off cũng khác: stacking OOF giảm FPR so với RF khoảng 1.37 điểm phần trăm, đồng thời tăng FNR khoảng 0.55 điểm phần trăm. Các giá trị này mô tả đúng development OOF, không thay cho Phase-10 holdout uncertainty.

## Reduced feature track: 17 features

Pooled OOF Macro-F1/MCC: RF 0.9413/0.8836; Hard Voting 0.9399/0.8813; Soft Voting 0.9389/0.8790; Stacking 0.9418/0.8839. Trên cùng OOF rows, 42-feature minus 17-feature Macro-F1 của RF là +0.00909; Hard Voting +0.00746; Soft Voting +0.00781; Stacking +0.00973. Đây là paired descriptive development contrasts. Candidate FS được lấy từ TRAIN trước CV, do đó có selection optimism; không xem các delta này là final unbiased FS effects.

Trong S72 cùng run, RF training trung bình giảm từ 42.39 xuống 26.24 giây/fold và serialized size từ 68.91 xuống 55.25 MB; inference giảm từ 0.01433 xuống 0.01205 ms/sample. Các pipeline 17-feature rẻ hơn trong run này, nhưng số đo phụ thuộc môi trường thực thi.

Trên frozen holdout, RF-42 so với RF-17 có Δ Macro-F1 +0.002670 (95% CI [+0.000878, +0.004524]), MCC +0.004029 ([+0.000883, +0.007278]), FPR −0.005973 ([−0.009514, −0.002568]); FNR delta +0.000574 ([−0.000618, +0.001765]). RF-17 train nhanh hơn khoảng 6.48×, inference nhanh hơn khoảng 2.44× và model nhỏ hơn khoảng 48.9%. Tuy nhiên RF42=(300 trees, max_features 0.5, leaf 1) và RF17=(150, 0.5, leaf 2): frozen holdout difference gộp feature-set lẫn hyperparameters, không cô lập nhân quả FS.

## Combination rule và held-out boundary

OOF pairings Phase 7.1/7.2 có 175,341/175,341 unique keys cho mỗi track; toàn bộ keys, labels, folds khớp; shared RF predicted labels khớp 100%. LR và DT predictions chỉ có trong S71 OOF; S72 lưu outputs của ensemble. Probability/score của RF khác nhau giữa hai files nên không ghép score để dựng lại ensemble. Stacking ở đây dùng đúng output S72 nested CV.

Saved Phase-9/10 results được giữ như contrast frozen riêng: Stacking-42 chưa chứng minh ưu thế tổng thể hơn RF-42; Macro-F1/MCC paired CIs chứa zero, McNemar Holm p=0.468377, trong khi FPR giảm và FNR tăng với CIs không chứa zero. Phase-10 paired uncertainty được tái sử dụng, không tính lại. Novel-vector view vẫn sensitivity, không external validation.

## Tuning and imbalance branches

Trong saved RF grids, frozen RF42 cùng-config CV mean Macro-F1 0.95333 so với default `(150, sqrt, leaf=2)` 0.95039 (Δ +0.00294); frozen RF17 0.94223 so với default 0.94129 (Δ +0.00094). Đây là same-grid, selection-conditional mean differences; CSV chỉ lưu marginal summaries, không tái tạo paired uncertainty. Chỉ thuật lại lựa chọn đã khóa, không lựa chọn lại config.

Meta LR tại C=0.5: `class_weight=balanced` trừ `None` có Δ Macro-F1 −0.00180, MCC −0.00371, attack recall −0.01442 trên historical five-fold meta CV. Đây là meta-level selected-grid diagnostic, không phải thử nghiệm imbalance có đối chứng cho toàn pipeline.

TRAIN label counts: Attack 119,341/175,341 (68.06%); Normal 56,000/175,341 (31.94%). Primary binary training split không khiến Attack là minority class. Không có matched resampling experiment; do đó ghi nhánh **no synthetic resampling** là lựa chọn scope/design đã thực hiện, không kết luận SMOTE/resampling vô ích. Xem `phase13_imbalance_closure_note.md`.

## Interpretation limits and remaining questions

- Diversity/error complementarity đã thấy ở OOF nhưng không bảo đảm Voting/Stacking thắng RF.
- Không có leave-one-base-learner-out analysis; không thể gán gain/loss riêng cho LR, DT hoặc RF trong Stack.
- Phase-7 Stacking outer/inner CV không cùng estimand với Phase-8 global OOF meta 5-fold CV; tuning gain của Stacking = NOT COMPARABLE.
- Fold rows dùng chung overlapping training sets; flow rows có thể phụ thuộc nhau. Không coi 175,341 OOF rows hoặc ba folds là độc lập để suy diễn population uncertainty.
- Không dùng Accuracy làm kết luận duy nhất, không nói p>0.05 chứng minh tương đương, không suy ra causal/domain/temporal explanation.
- RQ4 vẫn PARTIAL. Original Phase 13 không thay thế Phase 14 error analysis.

## CHECKPOINT

| ID | Task | Status | Evidence |
|---|---|---|---|
| P13-01 | Audit OOF exact sample/fold alignment | DONE | `comparability_audit.csv`: 175,341 matched keys per track; RF prediction agreement 1.0 |
| P13-02 | Individual/combination development synthesis | DONE | `phase13_ablation_matrix.csv`, rows A1/A2; negative Voting preserved |
| P13-03 | Fixed-config 42 vs 17 development contrasts | DONE | `phase13_ablation_matrix.csv`, rows A3; selection optimism disclosed |
| P13-04 | Cost/performance synthesis | DONE | Matrix A4; Phase-9/10 frozen comparisons retained separately |
| P13-05 | Tuning protocol comparability | DONE | Same-grid RF and meta-weight diagnostics; Stacking cross-protocol contrast excluded |
| P13-06 | Imbalance closure | DONE | `phase13_imbalance_closure_note.md` |
| P13-07 | Provenance and synthesis QA | DONE | `analysis_metadata.json`, input SHA-256, locked evidence preserved |

Phase 13 ablation synthesis is complete within retrospective saved-artifact scope. No model was retrained, no post-test selection was performed, and no new inferential uncertainty test was run. Feature-level error causation and full reproducibility remain later-phase work.
