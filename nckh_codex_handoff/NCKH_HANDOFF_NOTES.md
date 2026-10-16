# NCKH PROJECT HANDOFF NOTES — CHATGPT → CODEX

## 1. Vì sao cần handoff này?

Project đã đi đúng tương đối chặt từ Phase 0 tới Phase 10.

Sau Phase 10, assistant đã tự rút ngắn workflow và gán sai:
- Phase 11 = final figures,
- Phase 12 = writing,
- Phase 13 = manuscript.

User phát hiện việc này không khớp prompt gốc, vì roadmap thật còn study/analysis phases và publication-level figure QA chỉ tới Phase 16.

Mục tiêu của handoff:
- giữ nguyên evidence tốt;
- không làm mất artifact đã tạo;
- phục hồi đúng roadmap;
- không làm lại/contaminate official holdout.

---

# 2. Cái gì chắc chắn ĐÚNG?

## A. Phase 0–10 là backbone chính thức

Các phase này đã tạo thành một research chain có logic:

`scope → literature → dataset → audit → EDA → FS → baseline → diversity → ensemble → tuning → frozen holdout → paired statistics`

Đây là phần mạnh nhất của project.

## B. Official test discipline được giữ đúng

- TEST không được dùng cho FS/tuning.
- Phase 9 mới mở TEST.
- Phase 10 chỉ dùng saved predictions.
- Sau Phase 9 không đổi hyperparameter/feature/threshold.

Đây là điểm quan trọng khi bảo vệ.

## C. Null/negative results được giữ

- Hard/Soft Voting không vượt RF.
- Stacking không có robust overall superiority.
- FS không “improve accuracy”; nó tạo efficiency trade-off.

Không được sửa narrative để biến negative result thành positive claim.

## D. Statistical interpretation đúng hướng

Stacking vs RF:
- Macro-F1 delta CI chứa 0
- MCC delta CI chứa 0
- McNemar Holm p không reject
- FPR giảm có CI không chứa 0
- FNR tăng có CI không chứa 0

Kết luận hợp lý:
- overall gần tương đương;
- operational error trade-off khác nhau.

---

# 3. Cái gì đã làm SAI?

Sai chủ yếu là **workflow orchestration**, không phải số liệu Phase 9/10.

## Sai 1 — tự đổi roadmap sau Phase 10

Assistant tự đặt Phase 11–13 mới mà không kiểm tra master workflow.

## Sai 2 — viết báo cáo quá sớm

Đã tạo:
- Results draft
- Discussion
- Limitations
- Contributions
- Conclusion
- Integrated manuscript
- Abstract
- Figure/table placement

trong khi original roadmap chưa tới report-writing phase.

## Sai 3 — publication figure QA bị kéo lên sớm

Plan Phase 4 đã ghi rõ:
> publication-level figure QA reserved for Phase 16

nhưng assistant lại làm kiểu này ở pseudo-Phase 11/13.

## Sai 4 — đánh dấu “Phase 11/12/13 DONE” sai semantics

Các artifact đó có thể hoàn thiện về mặt file, nhưng **không có nghĩa official phase tương ứng trong roadmap đã DONE**.

---

# 4. Artifact làm sai timing có dùng lại được không?

Có.

### Có thể dùng lại sau:
- final tables dựa Phase 10
- six figures dựa locked statistics
- captions
- Results draft
- Discussion draft
- Limitations/Contributions draft
- Conclusion draft
- manuscript integration
- abstract
- placement map

### Nhưng:
- move vào `docs/drafts/premature_reporting/` hoặc tên tương tự
- xóa/đổi phase numbering trong metadata sau khi roadmap được phục hồi
- không cite chúng như evidence độc lập;
- evidence source vẫn là Phase 9/10.

---

# 5. Locked configurations

## RF-42
- 300 trees
- max_features = 0.5
- min_samples_leaf = 1
- threshold = 0.5

## RF-17
- 150 trees
- max_features = 0.5
- min_samples_leaf = 2
- threshold = 0.5

## Stacking-42
- base LR + DT + tuned RF-42
- meta LR C = 0.5
- no class weighting
- threshold = 0.5

Không đổi.

---

# 6. Locked final results

| Pipeline | Macro-F1 | MCC | FPR | FNR |
|---|---:|---:|---:|---:|
| Stacking-42 | 0.863840 | 0.750497 | 26.65% | 1.88% |
| RF-42 | 0.863343 | 0.750910 | 27.04% | 1.62% |
| RF-17 | ~0.8607 | ~0.7469 | ~27.63% | ~1.56% |

Do not regenerate a different “official” value unless reproducing the exact saved pipeline for audit.
Never use a new value to retune.

---

# 7. Locked paired statistics

## Stack − RF42
- Δ Macro-F1 +0.000497, CI [-0.000312, +0.001309]
- Δ MCC -0.000413, CI [-0.001938, +0.001140]
- Δ FPR -0.003838, CI [-0.005243, -0.002432]
- Δ FNR +0.002603, CI [+0.001853, +0.003375]
- McNemar Holm p = 0.468377

## RF42 − RF17
- Δ Macro-F1 +0.002670, CI [+0.000878, +0.004524]
- Δ MCC +0.004029, CI [+0.000883, +0.007278]
- Δ FPR -0.005973, CI [-0.009514, -0.002568]
- Δ FNR +0.000574, CI [-0.000618, +0.001765]
- McNemar Holm p = 0.011161

---

# 8. Known RQ status

## RQ1
Answered:
- no robust overall Stacking superiority vs RF42
- supported FP/FN trade-off

## RQ2
Answered:
- RF17 gives strong computational savings
- small predictive cost

## RQ3
Answered:
- complementary errors exist
- diversity alone insufficient

## RQ4
PARTIAL:
- official vs novel view differs
- CV vs holdout differs
- no clean temporal/day/scenario experiment yet

Do not upgrade RQ4 to full without new valid design.

---

# 9. Data caveats that must survive handoff

UNSW-NB15:
- duplicate feature vectors common
- train/test overlap exists
- some conflicting labels for identical observed vectors
- do not blind dedup
- do not majority relabel
- novel-vector evaluation is sensitivity only

Binary imbalance note:
attack is not necessarily the minority in primary train partition, so do not reflexively apply SMOTE just because “IDS data are imbalanced”.

---

# 10. Repository hygiene for Codex

On takeover:

1. inspect, do not assume;
2. make a backup branch or clean commit if Git policy allows;
3. never overwrite raw data;
4. never overwrite final Phase-9 predictions;
5. never overwrite Phase-10 stats without provenance;
6. isolate premature reporting drafts;
7. preserve scripts that reproduce existing results;
8. record any file move/rename in decision log.

Suggested quarantine:

```text
docs/
└── drafts/
    └── premature_reporting/
        ├── old_phase11_*
        ├── old_phase12_*
        └── old_phase13_*
```

Do not execute this move before showing proposed mapping to user.

---

# 11. Known roadmap clue

The project contains at least one explicit clue:

`phase4_eda_plan.md` says publication-level figure QA is reserved for **Phase 16**.

Therefore any current file labeled Phase 11/13 that performs publication figure QA is misnumbered.

No other Phase 11–18 mapping is safe to invent.

---

# 12. What Codex should produce first

Create:

`docs/ROADMAP_RECONCILIATION.md`

with four sections:

1. Recovered original roadmap Phase 11–18
2. Official current status
3. Premature artifact reclassification map
4. Next official phase + exact inputs/outputs

Then wait for user approval before continuing the next official phase.

---

# 13. User preference

User wants to understand the research, not just receive files.

At each major step:
- explain scientific purpose;
- explain how to defend it orally;
- show project path;
- ask for actual run output where needed;
- do not dump an entire pipeline at once.

