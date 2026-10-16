"""
PHASE 11 — Final Results & Figures
==================================

Reads Phase-10 statistical tables only.
No model training, tuning, feature selection, or threshold changes.

Expected project input:
results/final_analysis/unsw_nb15/phase10_statistics/tables/

Outputs:
results/final_reporting/unsw_nb15/phase11_results_figures/
"""

from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


MODEL_ORDER = [
    "stacking_42",
    "random_forest_42",
    "random_forest_17",
]

MODEL_LABELS = {
    "stacking_42": "Stacking-42",
    "random_forest_42": "RF-42",
    "random_forest_17": "RF-17",
}


def friendly_model_name(name: str) -> str:
    return MODEL_LABELS.get(name, name)


def select_major_attack_families(
    df: pd.DataFrame,
    min_rows: int = 300,
) -> pd.DataFrame:
    return df.loc[
        df["attack_rows"] >= min_rows
    ].copy()


def _save_figure(fig, output_stem: Path):
    fig.savefig(
        output_stem.with_suffix(".png"),
        dpi=300,
        bbox_inches="tight",
    )
    fig.savefig(
        output_stem.with_suffix(".pdf"),
        bbox_inches="tight",
    )
    plt.close(fig)


def _load_tables(input_dir: Path) -> dict[str, pd.DataFrame]:
    names = {
        "point": "recomputed_point_metrics.csv",
        "ci": "bootstrap_metric_ci.csv",
        "delta": "paired_bootstrap_differences.csv",
        "mcnemar": "mcnemar_holm.csv",
        "attack": "attack_family_miss_rate_ci.csv",
        "degradation": "official_vs_novel_degradation.csv",
        "cost": "performance_cost_tradeoff.csv",
    }

    tables = {}
    for key, filename in names.items():
        path = input_dir / filename
        if not path.exists():
            raise FileNotFoundError(path)
        tables[key] = pd.read_csv(path)

    return tables


def _metric_ci_table(
    point_df: pd.DataFrame,
    ci_df: pd.DataFrame,
) -> pd.DataFrame:
    official = point_df.loc[
        point_df["eval_view"] == "official_test"
    ].copy()

    rows = []
    for model in MODEL_ORDER:
        p = official.loc[
            official["pipeline"] == model
        ].iloc[0]

        row = {
            "pipeline": model,
            "model": friendly_model_name(model),
            "n_rows": int(p["n_rows"]),
            "accuracy": p["accuracy"],
            "balanced_accuracy": p["balanced_accuracy"],
            "precision": p["precision"],
            "recall_detection_rate": p["recall_detection_rate"],
            "f1": p["f1"],
            "macro_f1": p["macro_f1"],
            "mcc": p["mcc"],
            "false_positive_rate": p["false_positive_rate"],
            "false_negative_rate": p["false_negative_rate"],
        }

        for metric in [
            "macro_f1",
            "mcc",
            "false_positive_rate",
            "false_negative_rate",
        ]:
            c = ci_df.loc[
                (ci_df["eval_view"] == "official_test")
                & (ci_df["pipeline"] == model)
                & (ci_df["metric"] == metric)
            ].iloc[0]

            row[f"{metric}_ci_lower"] = c["ci_lower"]
            row[f"{metric}_ci_upper"] = c["ci_upper"]

        rows.append(row)

    return pd.DataFrame(rows)


def _pairwise_summary(
    delta_df: pd.DataFrame,
    mcnemar_df: pd.DataFrame,
) -> pd.DataFrame:
    delta = delta_df.loc[
        delta_df["eval_view"] == "official_test"
    ].copy()

    mc = mcnemar_df.loc[
        mcnemar_df["eval_view"] == "official_test"
    ].copy()

    rows = []

    pairs = (
        delta[
            ["model_a", "model_b"]
        ]
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )

    for a, b in pairs:
        row = {
            "model_a": friendly_model_name(a),
            "model_b": friendly_model_name(b),
        }

        for metric in [
            "macro_f1",
            "mcc",
            "false_positive_rate",
            "false_negative_rate",
        ]:
            d = delta.loc[
                (delta["model_a"] == a)
                & (delta["model_b"] == b)
                & (delta["metric"] == metric)
            ].iloc[0]

            row[f"delta_{metric}_a_minus_b"] = d[
                "delta_a_minus_b"
            ]
            row[f"{metric}_ci_lower"] = d["ci_lower"]
            row[f"{metric}_ci_upper"] = d["ci_upper"]
            row[f"{metric}_ci_excludes_zero"] = bool(
                d["ci_excludes_zero"]
            )

        m = mc.loc[
            (mc["model_a"] == a)
            & (mc["model_b"] == b)
        ].iloc[0]

        row["mcnemar_p_holm"] = m["p_holm"]
        row["mcnemar_reject_0_05"] = bool(
            m["reject_h0_alpha_0_05"]
        )
        row["a_wrong_b_correct"] = int(
            m["a_wrong_b_correct"]
        )
        row["a_correct_b_wrong"] = int(
            m["a_correct_b_wrong"]
        )

        rows.append(row)

    return pd.DataFrame(rows)


def plot_metric_ci(
    ci_df: pd.DataFrame,
    metric: str,
    ylabel: str,
    output_stem: Path,
):
    data = ci_df.loc[
        (ci_df["eval_view"] == "official_test")
        & (ci_df["metric"] == metric)
    ].copy()

    data["order"] = data["pipeline"].map(
        {m: i for i, m in enumerate(MODEL_ORDER)}
    )
    data = data.sort_values("order")

    x = np.arange(len(data))
    y = data["point_estimate"].to_numpy()

    yerr = np.vstack([
        y - data["ci_lower"].to_numpy(),
        data["ci_upper"].to_numpy() - y,
    ])

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.errorbar(
        x,
        y,
        yerr=yerr,
        fmt="o",
        capsize=5,
        linewidth=1.3,
    )
    ax.set_xticks(
        x,
        [friendly_model_name(v) for v in data["pipeline"]],
    )
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Frozen pipeline")
    ax.set_title(
        f"Official test: {ylabel} with 95% bootstrap CI"
    )
    ax.grid(axis="y", alpha=0.25)

    for xi, yi in zip(x, y):
        ax.annotate(
            f"{yi:.4f}",
            (xi, yi),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

    _save_figure(fig, output_stem)


def plot_fpr_fnr_tradeoff(
    point_df: pd.DataFrame,
    output_stem: Path,
):
    data = point_df.loc[
        point_df["eval_view"] == "official_test"
    ].copy()

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    for model in MODEL_ORDER:
        row = data.loc[
            data["pipeline"] == model
        ].iloc[0]

        x = 100 * row["false_positive_rate"]
        y = 100 * row["false_negative_rate"]

        ax.scatter(
            [x],
            [y],
            s=70,
        )
        ax.annotate(
            friendly_model_name(model),
            (x, y),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=9,
        )

    ax.set_xlabel("False Positive Rate (%)")
    ax.set_ylabel("False Negative Rate (%)")
    ax.set_title(
        "Official test: false-positive / false-negative trade-off"
    )
    ax.grid(alpha=0.25)

    _save_figure(fig, output_stem)


def plot_performance_cost(
    cost_df: pd.DataFrame,
    output_stem: Path,
):
    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    for model in MODEL_ORDER:
        row = cost_df.loc[
            cost_df["pipeline"] == model
        ].iloc[0]

        x = row["train_time_seconds"]
        y = row["macro_f1"]

        ax.scatter(
            [x],
            [y],
            s=70,
        )
        annotation_offset = (
            (-78, 6)
            if model == "stacking_42"
            else (6, 6)
        )

        ax.annotate(
            friendly_model_name(model),
            (x, y),
            xytext=annotation_offset,
            textcoords="offset points",
            fontsize=9,
        )

    ax.margins(x=0.08, y=0.10)
    ax.set_xscale("log")
    ax.set_xlabel("Training time (seconds, log scale)")
    ax.set_ylabel("Macro-F1")
    ax.set_title(
        "Official test performance versus training cost"
    )
    ax.grid(alpha=0.25)

    _save_figure(fig, output_stem)


def plot_official_vs_novel(
    degradation_df: pd.DataFrame,
    output_stem: Path,
):
    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    x = np.array([0, 1])

    for model in MODEL_ORDER:
        row = degradation_df.loc[
            degradation_df["pipeline"] == model
        ].iloc[0]

        y = np.array([
            row["official_macro_f1"],
            row["novel_macro_f1"],
        ])

        ax.plot(
            x,
            y,
            marker="o",
            label=friendly_model_name(model),
        )

    ax.set_xticks(
        x,
        ["Official test", "Novel-vector test"],
    )
    ax.set_ylabel("Macro-F1")
    ax.set_title(
        "Sensitivity to previously unseen feature vectors"
    )
    ax.grid(axis="y", alpha=0.25)
    ax.legend()

    _save_figure(fig, output_stem)


def plot_attack_family_miss_rate(
    attack_df: pd.DataFrame,
    output_stem: Path,
    min_rows: int = 300,
):
    data = attack_df.loc[
        attack_df["eval_view"] == "official_test"
    ].copy()

    data = select_major_attack_families(
        data,
        min_rows=min_rows,
    )

    category_order = (
        data[
            ["attack_cat", "attack_rows"]
        ]
        .drop_duplicates()
        .sort_values(
            "attack_rows",
            ascending=False,
        )["attack_cat"]
        .tolist()
    )

    x = np.arange(
        len(category_order)
    )
    offsets = {
        "stacking_42": -0.20,
        "random_forest_42": 0.0,
        "random_forest_17": 0.20,
    }
    markers = {
        "stacking_42": "o",
        "random_forest_42": "s",
        "random_forest_17": "^",
    }

    fig, ax = plt.subplots(figsize=(11.0, 5.5))

    for model in MODEL_ORDER:
        d = (
            data.loc[
                data["pipeline"] == model
            ]
            .set_index("attack_cat")
            .loc[category_order]
            .reset_index()
        )

        y = 100 * d["miss_rate"].to_numpy()
        lower = 100 * d["wilson_95_lower"].to_numpy()
        upper = 100 * d["wilson_95_upper"].to_numpy()

        yerr = np.vstack([
            y - lower,
            upper - y,
        ])

        ax.errorbar(
            x + offsets[model],
            y,
            yerr=yerr,
            fmt=markers[model],
            capsize=3,
            linewidth=1.0,
            label=friendly_model_name(model),
        )

    label_rows = (
        data[
            ["attack_cat", "attack_rows"]
        ]
        .drop_duplicates()
        .set_index("attack_cat")
        .loc[category_order]
    )

    labels = [
        f"{cat}\n(n={int(label_rows.loc[cat, 'attack_rows'])})"
        for cat in category_order
    ]

    ax.set_xticks(
        x,
        labels,
        rotation=35,
        ha="right",
    )
    ax.set_ylabel("Miss rate / FNR within attack family (%)")
    ax.set_xlabel("Attack family")
    ax.set_title(
        f"Official test attack-family miss rates "
        f"(families with n ≥ {min_rows})"
    )
    ax.grid(axis="y", alpha=0.25)
    ax.legend()

    _save_figure(fig, output_stem)


def build_results_markdown(
    final_table: pd.DataFrame,
    pairwise: pd.DataFrame,
    degradation: pd.DataFrame,
    cost: pd.DataFrame,
) -> str:
    def pct(x):
        return 100 * float(x)

    st = final_table.loc[
        final_table["pipeline"] == "stacking_42"
    ].iloc[0]

    rf42 = final_table.loc[
        final_table["pipeline"] == "random_forest_42"
    ].iloc[0]

    rf17 = final_table.loc[
        final_table["pipeline"] == "random_forest_17"
    ].iloc[0]

    pair = pairwise.loc[
        (pairwise["model_a"] == "Stacking-42")
        & (pairwise["model_b"] == "RF-42")
    ].iloc[0]

    d_st = degradation.loc[
        degradation["pipeline"] == "stacking_42"
    ].iloc[0]
    d_rf42 = degradation.loc[
        degradation["pipeline"] == "random_forest_42"
    ].iloc[0]
    d_rf17 = degradation.loc[
        degradation["pipeline"] == "random_forest_17"
    ].iloc[0]

    c_st = cost.loc[
        cost["pipeline"] == "stacking_42"
    ].iloc[0]
    c_rf42 = cost.loc[
        cost["pipeline"] == "random_forest_42"
    ].iloc[0]
    c_rf17 = cost.loc[
        cost["pipeline"] == "random_forest_17"
    ].iloc[0]

    train_ratio_st_rf = (
        c_st["train_time_seconds"]
        / c_rf42["train_time_seconds"]
    )
    train_ratio_rf42_rf17 = (
        c_rf42["train_time_seconds"]
        / c_rf17["train_time_seconds"]
    )

    lines = [
        "# PHASE 11 — Results-ready synthesis",
        "",
        "## 1. Final official-test performance",
        "",
        (
            f"Trên official test gồm {int(st['n_rows']):,} mẫu, "
            f"Stacking-42 đạt Macro-F1 = {st['macro_f1']:.4f} "
            f"(95% CI [{st['macro_f1_ci_lower']:.4f}, "
            f"{st['macro_f1_ci_upper']:.4f}]), trong khi RF-42 đạt "
            f"{rf42['macro_f1']:.4f} "
            f"(95% CI [{rf42['macro_f1_ci_lower']:.4f}, "
            f"{rf42['macro_f1_ci_upper']:.4f}]). "
            f"Chênh lệch Stacking-42 − RF-42 là "
            f"{pair['delta_macro_f1_a_minus_b']:+.6f}; "
            f"CI của chênh lệch chứa 0 nên chưa có bằng chứng rõ rằng "
            f"Stacking cải thiện Macro-F1 tổng thể."
        ),
        "",
        (
            f"Trade-off lỗi lại rõ hơn: Stacking-42 giảm FPR từ "
            f"{pct(rf42['false_positive_rate']):.2f}% xuống "
            f"{pct(st['false_positive_rate']):.2f}%, nhưng FNR tăng từ "
            f"{pct(rf42['false_negative_rate']):.2f}% lên "
            f"{pct(st['false_negative_rate']):.2f}%. "
            f"McNemar sau Holm cho cặp Stacking-42/RF-42 có "
            f"p = {pair['mcnemar_p_holm']:.3f}, nên không có bằng chứng "
            f"khác biệt về overall paired correctness."
        ),
        "",
        "## 2. Feature-selection / efficiency trade-off",
        "",
        (
            f"RF-17 đạt Macro-F1 = {rf17['macro_f1']:.4f}, thấp hơn "
            f"RF-42 ({rf42['macro_f1']:.4f}) một lượng nhỏ, nhưng thời gian "
            f"train giảm từ {c_rf42['train_time_seconds']:.1f}s xuống "
            f"{c_rf17['train_time_seconds']:.1f}s, tương đương RF-17 train "
            f"nhanh hơn khoảng {train_ratio_rf42_rf17:.2f}×. "
            f"Kích thước model giảm từ {c_rf42['serialized_model_size_mb']:.1f} MB "
            f"xuống {c_rf17['serialized_model_size_mb']:.1f} MB."
        ),
        "",
        "## 3. Ensemble-complexity trade-off",
        "",
        (
            f"Stacking-42 cần {c_st['train_time_seconds']:.1f}s để train, "
            f"khoảng {train_ratio_st_rf:.2f}× RF-42, trong khi chênh lệch "
            f"Macro-F1 tổng thể chỉ khoảng "
            f"{st['macro_f1'] - rf42['macro_f1']:+.4f}. "
            f"Do đó lợi ích chính của Stacking trong thí nghiệm này nằm ở "
            f"việc thay đổi cân bằng FP/FN hơn là cải thiện tổng thể."
        ),
        "",
        "## 4. Novel-vector sensitivity",
        "",
        (
            f"Macro-F1 giảm trên novel-vector subset ở cả ba pipeline: "
            f"Stacking-42 {d_st['delta_novel_minus_official_macro_f1']:+.4f}, "
            f"RF-42 {d_rf42['delta_novel_minus_official_macro_f1']:+.4f}, "
            f"RF-17 {d_rf17['delta_novel_minus_official_macro_f1']:+.4f}. "
            f"Đây là bằng chứng về độ nhạy với evaluation view, không phải "
            f"bằng chứng nhân quả cho temporal/domain shift."
        ),
        "",
        "## 5. Figure set",
        "",
        "- Figure 1: Official-test Macro-F1 với 95% bootstrap CI.",
        "- Figure 2: Official-test MCC với 95% bootstrap CI.",
        "- Figure 3: Trade-off giữa FPR và FNR.",
        "- Figure 4: Macro-F1 so với training cost.",
        "- Figure 5: Official test so với novel-vector test.",
        "- Figure 6: Miss rate theo attack family với Wilson 95% CI.",
    ]

    return "\n".join(lines)


def build_caption_markdown() -> str:
    return """# Figure captions

**Figure 1. Official-test Macro-F1 with 95% bootstrap confidence intervals.**
The three frozen pipelines achieve similar overall Macro-F1. The Stacking-42 and RF-42
intervals strongly overlap, consistent with the paired analysis showing no clear overall
Macro-F1 advantage for Stacking.

**Figure 2. Official-test MCC with 95% bootstrap confidence intervals.**
RF-42 and Stacking-42 show nearly identical MCC, whereas RF-17 is slightly lower,
illustrating the small predictive cost associated with feature reduction.

**Figure 3. False-positive versus false-negative trade-off on the official test.**
Stacking-42 shifts the operating behavior toward fewer false positives but more false
negatives relative to RF-42. RF-17 has the lowest FNR among the three frozen pipelines
but the highest FPR.

**Figure 4. Official-test Macro-F1 versus training time.**
The figure highlights computational efficiency rather than a model ranking. RF-17
requires substantially less training time with a modest reduction in Macro-F1, while
Stacking-42 incurs the highest training cost without a clear overall Macro-F1 advantage
over RF-42.

**Figure 5. Sensitivity of Macro-F1 to previously unseen feature vectors.**
All three pipelines show lower Macro-F1 on the novel-vector subset than on the complete
official test, indicating sensitivity to the evaluation view. The analysis does not
establish the cause of the degradation.

**Figure 6. Attack-family miss rates with Wilson 95% confidence intervals.**
Fuzzers has the highest miss rate among the major attack families for all three models.
The figure includes attack families with at least 300 positive test samples; very rare
families are retained in the accompanying table rather than emphasized visually.
"""


def run_phase11(
    input_dir: Path,
    output_dir: Path,
):
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    figure_dir = (
        output_dir / "figures"
    )
    table_dir = (
        output_dir / "tables"
    )

    figure_dir.mkdir(
        exist_ok=True
    )
    table_dir.mkdir(
        exist_ok=True
    )

    tables = _load_tables(
        input_dir
    )

    final_table = _metric_ci_table(
        tables["point"],
        tables["ci"],
    )
    pairwise = _pairwise_summary(
        tables["delta"],
        tables["mcnemar"],
    )

    final_table.to_csv(
        table_dir
        / "table01_final_performance_with_ci.csv",
        index=False,
    )
    pairwise.to_csv(
        table_dir
        / "table02_pairwise_effects_and_mcnemar.csv",
        index=False,
    )

    tables["cost"].assign(
        model=tables["cost"]["pipeline"].map(
            MODEL_LABELS
        )
    ).to_csv(
        table_dir
        / "table03_performance_cost_tradeoff.csv",
        index=False,
    )

    tables["attack"].to_csv(
        table_dir
        / "table04_attack_family_miss_rate_ci.csv",
        index=False,
    )

    plot_metric_ci(
        tables["ci"],
        "macro_f1",
        "Macro-F1",
        figure_dir
        / "fig01_official_macro_f1_ci",
    )

    plot_metric_ci(
        tables["ci"],
        "mcc",
        "Matthews Correlation Coefficient (MCC)",
        figure_dir
        / "fig02_official_mcc_ci",
    )

    plot_fpr_fnr_tradeoff(
        tables["point"],
        figure_dir
        / "fig03_fpr_fnr_tradeoff",
    )

    plot_performance_cost(
        tables["cost"],
        figure_dir
        / "fig04_macro_f1_vs_training_cost",
    )

    plot_official_vs_novel(
        tables["degradation"],
        figure_dir
        / "fig05_official_vs_novel_macro_f1",
    )

    plot_attack_family_miss_rate(
        tables["attack"],
        figure_dir
        / "fig06_attack_family_miss_rate_ci",
        min_rows=300,
    )

    results_text = (
        build_results_markdown(
            final_table,
            pairwise,
            tables["degradation"],
            tables["cost"],
        )
    )

    (
        output_dir
        / "phase11_results_ready_text.md"
    ).write_text(
        results_text,
        encoding="utf-8",
    )

    (
        output_dir
        / "phase11_figure_captions.md"
    ).write_text(
        build_caption_markdown(),
        encoding="utf-8",
    )

    metadata = {
        "phase": 11,
        "model_training_performed": False,
        "source": (
            "Phase-10 statistical tables only"
        ),
        "figures": [
            "fig01_official_macro_f1_ci",
            "fig02_official_mcc_ci",
            "fig03_fpr_fnr_tradeoff",
            "fig04_macro_f1_vs_training_cost",
            "fig05_official_vs_novel_macro_f1",
            "fig06_attack_family_miss_rate_ci",
        ],
        "figure_formats": [
            "PNG 300 dpi",
            "PDF vector",
        ],
        "attack_figure_min_rows": 300,
        "post_test_rule": (
            "No model, threshold, feature, or hyperparameter "
            "changes were made."
        ),
    }

    (
        output_dir
        / "phase11_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def main():
    script_path = Path(
        __file__
    ).resolve()
    project_root = (
        script_path.parents[2]
    )

    input_dir = (
        project_root
        / "results"
        / "final_analysis"
        / "unsw_nb15"
        / "phase10_statistics"
        / "tables"
    )

    output_dir = (
        project_root
        / "results"
        / "final_reporting"
        / "unsw_nb15"
        / "phase11_results_figures"
    )

    run_phase11(
        input_dir,
        output_dir,
    )

    print(
        f"[DONE] Phase 11 outputs: {output_dir}"
    )


if __name__ == "__main__":
    main()
