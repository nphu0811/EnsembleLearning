"""Aggregate existing development OOF artifacts for original Phase 13.

Read-only with respect to source evidence. Does not load raw or official TEST
data, train models, tune candidates, or estimate new inferential uncertainty.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


ROOT = Path(__file__).resolve().parents[2]
S71 = ROOT / "results/ensemble/unsw_nb15/phase7_1_diversity"
S72 = ROOT / "results/ensemble/unsw_nb15/phase7_2_ensemble_cv"
OUT = ROOT / "results/ablation/unsw_nb15/phase13_ablation"
KEY = ["row_index", "id", "y_true", "fold"]
TRACKS = ("all_features", "stable_17_features")
INDIVIDUAL = ("logistic_regression", "decision_tree", "random_forest", "adaboost")
ENSEMBLES = ("hard_voting_lrdtrf", "soft_voting_lrdtrf", "stacking_lrdtrf")


def metric_values(y, pred, score=None):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    values = {
        "accuracy": accuracy_score(y, pred),
        "balanced_accuracy": balanced_accuracy_score(y, pred),
        "precision_attack": precision_score(y, pred, zero_division=0),
        "recall_attack": recall_score(y, pred, zero_division=0),
        "f1_attack": f1_score(y, pred, zero_division=0),
        "macro_f1": f1_score(y, pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y, pred),
        "fpr": fp / (fp + tn),
        "fnr": fn / (fn + tp),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }
    if score is not None:
        values["roc_auc"] = roc_auc_score(y, score)
        values["pr_auc"] = average_precision_score(y, score)
    return values


def load_aligned(track):
    left = pd.read_csv(S71 / "oof" / f"{track}_oof_predictions.csv")
    right = pd.read_csv(S72 / "oof" / f"{track}_ensemble_oof.csv")
    for label, frame in (("S71", left), ("S72", right)):
        if frame.duplicated(KEY).any():
            raise ValueError(f"{label} duplicate OOF keys: {track}")
        if len(frame) != 175_341:
            raise ValueError(f"Unexpected {label} row count: {track} {len(frame)}")
    merged = left.merge(
        right, on=KEY, how="outer", indicator=True,
        suffixes=("_s71", "_s72"), validate="one_to_one",
    )
    if not (merged["_merge"] == "both").all():
        raise ValueError(f"S71/S72 OOF keys do not match: {track}")
    checks = {}
    for model in ("random_forest",):
        col = f"{model}_pred"
        checks[model] = float((merged[f"{col}_s71"] == merged[f"{col}_s72"]).mean())
        if checks[model] != 1.0:
            raise ValueError(f"Shared {model} predicted labels differ: {track}")
    audit = {
        "feature_track": track,
        "n_s71": len(left), "n_s72": len(right),
        "n_matched": len(merged), "n_unique_keys": len(merged[KEY].drop_duplicates()),
        "n_folds": int(merged["fold"].nunique()),
        "shared_base_prediction_agreement": json.dumps(checks, sort_keys=True),
        "rf_probability_equals_score": bool(
            (merged["random_forest_prob"] == merged["random_forest_score"]).all()
        ),
    }
    return merged.drop(columns="_merge"), audit


def model_pred(frame, model):
    suffix = "_s71" if model in INDIVIDUAL else "_s72"
    column = f"{model}_pred{suffix}"
    if column not in frame:
        column = f"{model}_pred"
    return frame[column].to_numpy()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frames, audits, rows = {}, [], []
    for track in TRACKS:
        frame, audit = load_aligned(track)
        frames[track] = frame
        audits.append(audit)
        y = frame["y_true"].to_numpy()
        for model, source in [*((name, "S71 OOF") for name in INDIVIDUAL),
                              *((name, "S72 OOF") for name in ENSEMBLES)]:
            pred = model_pred(frame, model)
            score_col = f"{model}_prob_s71" if f"{model}_prob_s71" in frame else f"{model}_prob"
            if score_col not in frame:
                score_col = f"{model}_score_s72" if f"{model}_score_s72" in frame else f"{model}_score"
            score = frame[score_col].to_numpy() if score_col in frame else None
            rows.append({
                "contrast_id": "A1_individual_vs_combination",
                "model": model, "feature_track": track,
                "n_rows": len(frame), "n_folds": audit["n_folds"],
                "estimand": "pooled_oof_descriptive",
                "source": source, **metric_values(y, pred, score),
            })

    for model in (*INDIVIDUAL[:3], *ENSEMBLES):
        name = f"{model}_pred" + ("_s71" if model in INDIVIDUAL else "_s72")
        if name not in frames[TRACKS[0]]:
            name = f"{model}_pred"
        a, b = frames[TRACKS[0]], frames[TRACKS[1]]
        paired = a[KEY + [name]].merge(
            b[KEY + [name]], on=["row_index", "id", "y_true"],
            suffixes=("_42", "_17"), validate="one_to_one",
        )
        if len(paired) != 175_341 or not (paired.fold_42 == paired.fold_17).all():
            raise ValueError(f"42/17 OOF sample/fold mismatch: {model}")
        y = paired.y_true.to_numpy()
        values = {}
        for track, suffix in (("42", "_42"), ("17", "_17")):
            values[track] = metric_values(y, paired[name + suffix].to_numpy())
            rows.append({
                "contrast_id": "A3_fixed_config_feature_track",
                "model": model, "feature_track": track,
                "n_rows": len(paired), "n_folds": 3,
                "estimand": "pooled_oof_descriptive",
                "source": "S71/S72 OOF", **values[track],
            })
        for metric in ("macro_f1", "mcc", "fpr", "fnr", "accuracy"):
            rows.append({
                "contrast_id": "A3_paired_delta_42_minus_17",
                "model": model, "feature_track": "42_vs_17",
                "n_rows": len(paired), "n_folds": 3,
                "estimand": "difference_of_paired_pooled_oof_metrics",
                "source": "S71/S72 OOF", "metric_name": metric,
                "delta_a_minus_b": values["42"][metric] - values["17"][metric],
            })

    pooled = pd.DataFrame(rows)
    for track in TRACKS:
        subset = pooled[(pooled.feature_track == track) &
                        (pooled.contrast_id == "A1_individual_vs_combination")]
        rf = subset[subset.model == "random_forest"].iloc[0]
        for ensemble in ENSEMBLES:
            target = subset[subset.model == ensemble].iloc[0]
            for metric in ("macro_f1", "mcc", "fpr", "fnr"):
                rows.append({
                    "contrast_id": "A2_combiner_minus_RF",
                    "model": ensemble, "feature_track": track,
                    "n_rows": 175_341, "n_folds": 3,
                    "estimand": "difference_of_paired_pooled_oof_metrics",
                    "source": "S72 pooled OOF", "metric_name": metric,
                    "delta_a_minus_b": float(target[metric] - rf[metric]),
                })

    cost_table = pd.read_csv(S72 / "tables" / "aggregate_metrics.csv")
    for _, entry in cost_table.iterrows():
        if entry.configuration not in ("random_forest", *ENSEMBLES):
            continue
        rows.append({
            "contrast_id": "A4_cost_performance",
            "model": entry.configuration, "feature_track": entry.feature_track,
            "n_rows": 175_341, "n_folds": int(entry.cv_folds),
            "estimand": "historical_fold_mean_cost_and_cv_metrics",
            "source": "S72 aggregate_metrics.csv",
            "macro_f1": entry.macro_f1_mean, "mcc": entry.mcc_mean,
            "train_time_seconds_mean": entry.train_time_seconds_mean,
            "inference_ms_per_sample_mean": entry.inference_ms_per_sample_mean,
            "serialized_model_size_mb_mean": entry.serialized_model_size_mb_mean,
        })

    freeze = json.loads((ROOT / "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json").read_text())
    for track in ("42", "17"):
        grid_path = ROOT / f"results/tuning/unsw_nb15/phase8_controlled/tables/rf{track}_grid_results.csv"
        grid = pd.read_csv(grid_path)
        default = grid[(grid.param_model__max_features == "sqrt") &
                       (grid.param_model__min_samples_leaf == 2) &
                       (grid.param_model__n_estimators == 150)].iloc[0]
        candidate = freeze[f"random_forest_{track}"]["hyperparameters"]
        chosen = grid[(grid.param_model__max_features == str(candidate["max_features"])) &
                      (grid.param_model__min_samples_leaf == candidate["min_samples_leaf"]) &
                      (grid.param_model__n_estimators == candidate["n_estimators"])].iloc[0]
        for metric, column in (("macro_f1", "mean_test_macro_f1"), ("mcc", "mean_test_mcc"),
                               ("balanced_accuracy", "mean_test_balanced_accuracy"),
                               ("attack_recall", "mean_test_attack_recall")):
            rows.append({
                "contrast_id": "A5a_frozen_vs_default_same_grid",
                "model": f"random_forest_{track}", "feature_track": track,
                "n_folds": 3, "estimand": "same_grid_CV_mean_difference_selection_conditional",
                "source": str(grid_path.relative_to(ROOT)), "metric_name": metric,
                "default_config": "150 trees, sqrt, leaf=2",
                "frozen_config": json.dumps(candidate, sort_keys=True),
                "default_mean": float(default[column]), "frozen_mean": float(chosen[column]),
                "delta_a_minus_b": float(chosen[column] - default[column]),
                "uncertainty": "marginal summaries only; no paired inferential claim",
            })

    meta_path = ROOT / "results/tuning/unsw_nb15/phase8_controlled/tables/stacking42_meta_grid_results.csv"
    meta_grid = pd.read_csv(meta_path)
    meta_rows = meta_grid[meta_grid.param_C == 0.5]
    plain = meta_rows[meta_rows.param_class_weight.isna()].iloc[0]
    balanced = meta_rows[meta_rows.param_class_weight == "balanced"].iloc[0]
    for metric, column in (("macro_f1", "mean_test_macro_f1"), ("mcc", "mean_test_mcc"),
                           ("attack_recall", "mean_test_attack_recall")):
        rows.append({
            "contrast_id": "A6b_meta_class_weight_C_0_5",
            "model": "stacking_meta_logistic_regression", "feature_track": "42",
            "n_folds": 5, "estimand": "historical_meta_OOF_CV_mean_difference",
            "source": str(meta_path.relative_to(ROOT)), "metric_name": metric,
            "class_weight_none_mean": float(plain[column]),
            "class_weight_balanced_mean": float(balanced[column]),
            "delta_a_minus_b": float(balanced[column] - plain[column]),
            "uncertainty": "marginal summaries only; selection-conditional",
        })

    # Frozen official-holdout results are copied from Phase 9/10 verbatim.
    p9_path = ROOT / "results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv"
    p10_diff_path = ROOT / "results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv"
    p10_test_path = ROOT / "results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv"
    holdout = pd.read_csv(p9_path)
    holdout = holdout[(holdout.eval_view == "official_test") &
                      (holdout.pipeline.isin(["random_forest_42", "random_forest_17", "stacking_42"]))]
    for _, entry in holdout.iterrows():
        rows.append({
            "contrast_id": "A4_frozen_official_holdout_bundle",
            "model": entry.pipeline, "feature_track": str(entry.original_feature_count),
            "n_rows": int(entry.n_rows), "n_folds": 0,
            "estimand": "frozen_phase9_official_holdout_point_estimate",
            "source": str(p9_path.relative_to(ROOT)),
            **{name: entry[name] for name in (
                "accuracy", "balanced_accuracy", "precision", "recall_detection_rate",
                "f1", "macro_f1", "mcc", "false_positive_rate", "false_negative_rate",
            )},
        })
    effects = pd.read_csv(p10_diff_path)
    effects = effects[(effects.eval_view == "official_test") &
                      (((effects.model_a == "stacking_42") & (effects.model_b == "random_forest_42")) |
                       ((effects.model_a == "random_forest_42") & (effects.model_b == "random_forest_17")))]
    for _, effect in effects.iterrows():
        rows.append({
            "contrast_id": "A4_phase10_paired_holdout_effect",
            "model": effect.model_a, "comparator": effect.model_b,
            "feature_track": "frozen_pipelines", "n_rows": 82_332,
            "estimand": "saved_phase10_paired_bootstrap_difference",
            "source": str(p10_diff_path.relative_to(ROOT)),
            "metric_name": effect.metric,
            "delta_a_minus_b": effect.delta_a_minus_b,
            "ci_level": effect.ci_level, "ci_lower": effect.ci_lower,
            "ci_upper": effect.ci_upper,
        })
    mcnemar = pd.read_csv(p10_test_path)
    mcnemar = mcnemar[(mcnemar.eval_view == "official_test") &
                      (((mcnemar.model_a == "stacking_42") & (mcnemar.model_b == "random_forest_42")) |
                       ((mcnemar.model_a == "random_forest_42") & (mcnemar.model_b == "random_forest_17")))]
    for _, result in mcnemar.iterrows():
        rows.append({
            "contrast_id": "A4_phase10_mcnemar_holm",
            "model": result.model_a, "comparator": result.model_b,
            "feature_track": "frozen_pipelines", "n_rows": 82_332,
            "estimand": "saved_phase10_exact_paired_mcnemar_holm",
            "source": str(p10_test_path.relative_to(ROOT)),
            "a_wrong_b_correct": result.a_wrong_b_correct,
            "a_correct_b_wrong": result.a_correct_b_wrong,
            "p_holm": result.p_holm, "reject_h0_alpha_0_05": result.reject_h0_alpha_0_05,
        })

    audit_frame = pd.DataFrame(audits)
    audit_frame = pd.concat([audit_frame, pd.DataFrame([
        {"contrast_id": "A5b_stacking_tuning_gain", "comparability_status": "NOT_COMPARABLE",
         "reason": "Phase7.2 nested outer/inner CV differs from Phase8 five-fold meta CV on global base OOF; tuned RF also changes."},
        {"contrast_id": "A6a_synthetic_resampling", "comparability_status": "DESIGN_ONLY",
         "reason": "No matched resampling branch exists; TRAIN Attack is 68.06% and TEST is locked."},
        {"contrast_id": "A4_RF42_vs_RF17_isolated_FS", "comparability_status": "NOT_COMPARABLE_AS_PURE_FS",
         "reason": "Frozen Phase9 RF42 and RF17 differ in feature set and RF hyperparameters."},
    ])], ignore_index=True, sort=False)
    pd.DataFrame(rows).to_csv(OUT / "phase13_ablation_matrix.csv", index=False)
    audit_frame.to_csv(OUT / "comparability_audit.csv", index=False)
    inputs = [
        "src/models/run_unsw_baseline_development.py",
        "src/models/run_unsw_diversity_oof.py",
        "src/models/run_unsw_ensemble_phase7_2.py",
        "results/ensemble/unsw_nb15/phase7_1_diversity/experiment_metadata.json",
        "results/ensemble/unsw_nb15/phase7_2_ensemble_cv/experiment_metadata.json",
        *[f"results/ensemble/unsw_nb15/phase7_1_diversity/oof/{track}_oof_predictions.csv" for track in TRACKS],
        *[f"results/ensemble/unsw_nb15/phase7_2_ensemble_cv/oof/{track}_ensemble_oof.csv" for track in TRACKS],
        "results/ensemble/unsw_nb15/phase7_2_ensemble_cv/tables/aggregate_metrics.csv",
        "results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json",
        "results/tuning/unsw_nb15/phase8_controlled/tables/rf42_grid_results.csv",
        "results/tuning/unsw_nb15/phase8_controlled/tables/rf17_grid_results.csv",
        "results/tuning/unsw_nb15/phase8_controlled/tables/stacking42_meta_grid_results.csv",
        "results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv",
        "results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv",
        "results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv",
        "results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv",
        "results/data_audit/unsw_nb15/class_distribution.csv",
        "results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv",
        "results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv",
        "results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv",
        "results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv",
        "results/data_audit/unsw_nb15/class_distribution.csv",
    ]
    metadata = {
        "study": "Original Phase 13 retrospective ablation synthesis",
        "training_performed": False,
        "official_test_rows_or_predictions_loaded": False,
        "official_test_aggregate_metrics_reused": True,
        "new_uncertainty_tests_performed": False,
        "estimand": "pooled OOF; folds are not independent replications",
        "limitations": [
            "OOF rows may be dependent network flows.",
            "S71/S72 RF scores are not interchangeable; predictions match, score arrays do not.",
            "No component leave-one-out ablation is present.",
            "Feature-selection candidates were derived from TRAIN before this CV.",
        ],
        "python": platform.python_version(), "pandas": pd.__version__,
        "inputs_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in inputs
        },
    }
    (OUT / "analysis_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    print("Rows:", len(rows), "alignment:", audits)
    print(pd.DataFrame(rows).query(
        "contrast_id == 'A1_individual_vs_combination' and feature_track == 'all_features'"
    )[["model", "macro_f1", "mcc", "fpr", "fnr"]].to_string(index=False))


if __name__ == "__main__":
    main()
