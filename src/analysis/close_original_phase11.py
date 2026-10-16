#!/usr/bin/env python3
"""Original Phase 11 — Evaluation Protocol, read-only closure.

Input: saved Phase 9 aggregate metrics and cost CSVs (NOT raw data, NOT predictions).
Output: report tables and checkpoint. No training/tuning/changes to source files.

Usage from NCKH root:
    py close_original_phase11.py

Or:
    python close_original_phase11.py --project-root /path/to/NCKH
"""
import argparse
import csv
import math
from pathlib import Path

METRICS_REL = "results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv"
COST_REL = "results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv"
OUT_REL = "results/final_evaluation/unsw_nb15/phase11_evaluation_closure"

MODEL_NAMES = {"random_forest_42": "RF-42", "stacking_42": "Stacking-42", "random_forest_17": "RF-17"}
VIEW_NAMES = {"official_test": "Official test", "novel_vector_test": "Novel-vector subset"}


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def div(a, b):
    return a / b if b else 0.0


def f1_from_pr(p, r):
    return div(2.0 * p * r, p + r)


def validate(name, actual, expected, tolerance=1e-10):
    if not math.isclose(actual, float(expected), rel_tol=tolerance, abs_tol=tolerance):
        raise ValueError(f"Source consistency FAILED for {name}: calculated={actual}, saved={expected}")


def md_table(rows, cols):
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    lines += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", type=Path, default=Path.cwd(), help="Root NCKH directory")
    ap.add_argument("--outdir", type=Path, default=None, help="Optional output directory")
    args = ap.parse_args()

    root = args.project_root.resolve()
    metric_path, cost_path = root / METRICS_REL, root / COST_REL
    if not metric_path.is_file() or not cost_path.is_file():
        raise FileNotFoundError(f"Expected the original saved CSVs, but missing: {metric_path} or {cost_path}")
    out = args.outdir.resolve() if args.outdir else root / OUT_REL
    if out == metric_path.parent or out == cost_path.parent:
        raise ValueError("Output directory must not overwrite the original Phase 9 result directory")
    out.mkdir(parents=True, exist_ok=True)

    metrics, costs = read_csv(metric_path), read_csv(cost_path)
    by_cost = {r["pipeline"]: r for r in costs}
    per_cls, matrices, combined = [], [], []
    seen = set()
    for r in metrics:
        name, view = r["pipeline"], r["eval_view"]
        if (name,view) in seen:
            raise ValueError(f"Repeated source evaluation row: {(name,view)}")
        seen.add((name,view))
        if name not in MODEL_NAMES or view not in VIEW_NAMES:
            raise ValueError(f"Unexpected pipeline/view: {name}/{view}; inspect before accepting")
        tn, fp, fn, tp = (int(r[k]) for k in ("tn", "fp", "fn", "tp"))
        n0, n1, total = tn + fp, tp + fn, tn + fp + fn + tp
        assert n0 >= 0 and n1 >= 0 and total > 0
        if total != int(r["n_rows"]):
            raise ValueError(f"Count total mismatch: {name}/{view}")

        # Treat Normal as class 0 positive in one-vs-rest reporting.
        p0, r0 = div(tn, tn+fn), div(tn,tn+fp)
        p1, r1 = div(tp,tp+fp), div(tp,tp+fn)
        f0, f1 = f1_from_pr(p0,r0), f1_from_pr(p1,r1)
        macro = (f0+f1)/2
        weighted = (f0*n0+f1*n1)/total
        accuracy = (tn+tp)/total
        bacc = (r0+r1)/2
        fpr, fnr = div(fp,tn+fp), div(fn,tp+fn)
        for label, support, pr, rec, f in [("Normal",n0,p0,r0,f0),("Attack",n1,p1,r1,f1)]:
            per_cls.append({"pipeline":name,"eval_view":view,"class":label,"support":support,"precision":pr,"recall":rec,"f1":f})
        matrices.append({"pipeline":name,"eval_view":view,"tn":tn,"fp":fp,"fn":fn,"tp":tp,
                         "true_normal":n0,"true_attack":n1,"total":total})
        for key, result in [("macro_f1",macro),("accuracy",accuracy),("balanced_accuracy",bacc),
                            ("precision",p1),("recall_detection_rate",r1),("f1",f1),
                            ("false_positive_rate",fpr),("false_negative_rate",fnr)]:
            validate(f"{name}/{view}:{key}",result,r[key])
        cost = by_cost.get(name)
        if cost is None:
            raise ValueError(f"Missing cost row: {name}")
        if int(cost["original_feature_count"]) != int(r["original_feature_count"]):
            raise ValueError(f"Mismatch feature count for: {name}")
        combined.append({
            "pipeline":name,"eval_view":view,"n_rows":total,"original_features":int(r["original_feature_count"]),
            "threshold":r["decision_threshold"],"accuracy":accuracy,"precision_attack":p1,
            "recall_attack":r1,"f1_attack":f1,"precision_normal":p0,"recall_normal":r0,
            "f1_normal":f0,"macro_f1":macro,"weighted_f1":weighted,"balanced_accuracy":bacc,
            "mcc":r["mcc"],"roc_auc":r["roc_auc"],"pr_auc":r["pr_auc"],"fpr":fpr,"fnr":fnr,
            "train_time_seconds":cost["train_time_seconds"],
            "inference_ms_per_sample":cost["inference_ms_per_sample"],
            "serialized_model_size_mb":cost["serialized_model_size_mb"],
        })

    if set(seen) != {(m,v) for m in MODEL_NAMES for v in VIEW_NAMES}:
        raise ValueError(f"Expected exactly 3 pipelines x 2 views, got {sorted(seen)}")

    per_fields = ["pipeline","eval_view","class","support","precision","recall","f1"]
    cm_fields = ["pipeline","eval_view","tn","fp","fn","tp","true_normal","true_attack","total"]
    summary_fields = list(combined[0])
    write_csv(out/"phase11_per_class_metrics.csv",per_cls,per_fields)
    write_csv(out/"phase11_confusion_matrices.csv",matrices,cm_fields)
    write_csv(out/"phase11_final_evaluation_complete.csv",combined,summary_fields)

    ordered = ["random_forest_42", "stacking_42", "random_forest_17"]
    official = {r["pipeline"]:r for r in combined if r["eval_view"] == "official_test"}
    cm_by = {r["pipeline"]:r for r in matrices if r["eval_view"] == "official_test"}
    short = [{"Pipeline":MODEL_NAMES[n],"Weighted F1":f'{official[n]["weighted_f1"]:.6f}',
              "Macro-F1":f'{official[n]["macro_f1"]:.6f}',
              "MCC":f'{float(official[n]["mcc"]):.6f}',
              "Normal recall":f'{official[n]["recall_normal"]:.2%}',
              "Attack recall":f'{official[n]["recall_attack"]:.2%}'} for n in ordered]
    cms = [{"Pipeline":MODEL_NAMES[n],"TN":cm_by[n]["tn"],"FP":cm_by[n]["fp"],
            "FN":cm_by[n]["fn"],"TP":cm_by[n]["tp"]} for n in ordered]
    msg = """# Original Phase 11 — Evaluation Protocol: CHECKPOINT

**Trạng thái: DONE (trong phạm vi binary UNSW-NB15 đã khóa).**

## Nguồn và tính toàn vẹn

- Chỉ đọc `results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv` và `cost_metrics.csv`.
- Không huấn luyện/tune/reselect model, không dùng raw data hoặc official-test predictions ở mức từng mẫu.
- Phát sinh Weighted-F1, precision/recall/F1/support của từng lớp và explicit confusion counts từ aggregate TN/FP/FN/TP đã lưu.
- Kiểm lại tám chỉ số từ confusion counts (Accuracy, Balanced Accuracy, Attack Precision/Recall/F1, Macro-F1, FPR/FNR) và tất cả khớp với nguồn gốc.
- AUC/MCC, runtime và model size **sao chép từ bảng đã khóa**, không suy ra lại từ confusion counts.

## Official test (82,332 mẫu)

""" + md_table(short,["Pipeline","Weighted F1","Macro-F1","MCC","Normal recall","Attack recall"]) + "\n\n" + """## Confusion matrix — actual labels theo hàng, predicted labels theo cột

""" + md_table(cms,["Pipeline","TN","FP","FN","TP"]) + """

Với nhãn Attack = 1:
- TN: Normal dự đoán Normal.
- FP: Normal dự đoán Attack (báo động giả).
- FN: Attack dự đoán Normal (bỏ sót tấn công).
- TP: Attack dự đoán Attack.

Chi tiết official + novel-vector: ba CSV cùng thư mục.

## Computational complexity

Số feature, training time, inference ms/sample và serialized model size có trong `phase11_final_evaluation_complete.csv`.
Chi phí đo được chỉ áp dụng cho môi trường thử nghiệm hiện có. Không tuyên bố benchmark phần cứng phổ quát hoặc đã đo memory/energy/real-time throughput. Random Forest có nhiều cây; Stacking có thêm base learners và meta learner nên computation phức tạp hơn một pipeline RF đơn, nhưng runtime thực nghiệm mới là evidence so sánh chính.

## Giới hạn và cách diễn giải

- Weighted F1 bị ảnh hưởng bởi support của từng lớp; không dùng để thay thế Macro-F1, MCC hay FPR/FNR.
- `precision`, `recall`, `f1` nguyên bản trong `final_metrics.csv` là của **Attack (class 1)**, không phải của Normal.
- Per-attack-family miss rate chỉ là phân tích lỗi của binary detector, không phải multiclass precision/recall.
- Novel-vector subset là cùng benchmark, không phải external validation.
- Không có bằng chứng tổng thể Stacking-42 vượt RF-42 rõ ràng: paired CI của chênh lệch Macro-F1 chứa 0 (Phase 12).

## Research Decisions Log

**Decision:** Đóng Phase 11 bằng cách bổ sung derived metrics từ confusion counts đã lưu.  
**Reason:** Checklist roadmap gốc còn thiếu Weighted F1, per-class P/R/F1/support và ma trận nhầm lẫn trình bày tường minh.  
**Evidence:** `final_metrics.csv`, `cost_metrics.csv`, ba bảng xuất từ script này, kiểm toán identity số học PASS.  
**Consequence:** Giữ nguyên 3 frozen pipelines, official holdout và mọi kết luận khoa học; không phát sinh tuning hoặc model selection mới.

## CHECKPOINT

| ID | Task | Status | Evidence |
|---|---|---|---|
| P11-01 | Accuracy, Precision, Recall, F1, Macro-F1, MCC, ROC/PR-AUC | DONE | Original final_metrics.csv + final_evaluation_complete.csv |
| P11-02 | Weighted F1 | DONE | phase11_final_evaluation_complete.csv |
| P11-03 | Per-class P/R/F1/support | DONE | phase11_per_class_metrics.csv |
| P11-04 | Confusion matrices | DONE | phase11_confusion_matrices.csv |
| P11-05 | FPR/FNR, detection rate, balanced accuracy | DONE | final_evaluation_complete.csv |
| P11-06 | Training/inference cost, original feature counts and model size | DONE | final_evaluation_complete.csv |
| P11-07 | Recompute and verify metrics from locked confusion counts | DONE | Assertion checks in close_original_phase11.py |
| P11-08 | Hardware-independent complexity claims | NOT CLAIMED | Qualitative limitation above |

**Bước tiếp theo:** Original Phase 12 statistical validation đã có artifact từ trước; đối chiếu và dùng lại. Original Phase 13 có retrospective ablation tổng hợp, không coi là full factorial. Sau đó bắt đầu **Original Phase 14 — Error Analysis**, chỉ dùng frozen predictions và không thay model.
"""
    (out / "PHASE11_CHECKPOINT.md").write_text(msg, encoding="utf-8")
    print(f"Phase 11 closure COMPLETE: {out}")
    print("Created 4 output files; original saved metrics/cost unchanged.")

if __name__ == "__main__":
    main()
