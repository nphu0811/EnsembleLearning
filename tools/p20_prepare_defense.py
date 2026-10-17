"""Draft source-linked defense answers from frozen summaries. No new evaluation."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'defense/p20_pre_2026_10_17_01'
CONTENT = TASK / 'packet_02/local_contents'


def rows(path):
    with (CONTENT / path).open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def ev(path, locator, anchor):
    assert anchor in (CONTENT / path).read_text(encoding='utf-8-sig'), (path, anchor)
    return dict(path=path, locator=locator, anchor=anchor)


def main():
    out = TASK / 'defense'
    out.mkdir(exist_ok=False)
    metric = 'results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_final_evaluation_complete.csv'
    confusion = 'results/final_evaluation/unsw_nb15/phase11_evaluation_closure/phase11_confusion_matrices.csv'
    paired = 'results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv'
    mc = 'results/final_analysis/unsw_nb15/phase10_statistics/tables/mcnemar_holm.csv'
    stats = 'results/final_analysis/unsw_nb15/phase10_statistics/experiment_metadata.json'
    cost = 'results/final_evaluation/unsw_nb15/phase9_holdout/tables/cost_metrics.csv'
    freeze = 'results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json'
    methods = 'report/chapters/methodology.tex'
    conclusions = 'report/chapters/conclusion.tex'
    results = 'report/chapters/results_discussion.tex'
    intro = 'report/chapters/introduction.tex'
    view = 'results/data_audit/unsw_nb15_views/view_summary.json'
    p9 = 'src/models/run_unsw_phase9_final_holdout.py'
    lit = 'literature_reported_facts.csv'
    scope = 'literature_scope.json'
    rf, st, small = [next(r for r in rows(metric) if r['eval_view']=='official_test' and r['pipeline']==p) for p in ['random_forest_42','stacking_42','random_forest_17']]
    delta = next(r for r in rows(paired) if r['eval_view']=='official_test' and r['model_a']=='stacking_42' and r['model_b']=='random_forest_42' and r['metric']=='macro_f1')
    questions = []

    def add(theme, difficulty, question, answer, evidence):
        questions.append(dict(id=f'DQ{len(questions)+1:02d}', theme=theme, difficulty=difficulty,
                              question=question, answer=answer, evidence=evidence,
                              status='DRAFT_SOURCE_GROUNDED;NOT_REHEARSED'))

    add('scope','MEDIUM','Công trình thực sự giải quyết bài toán nào?',
        'Phân loại nhị phân Normal=0 và Attack=1 trên UNSW-NB15. attack_cat chỉ dùng phân tích lỗi theo nhãn thật. Chúng tôi không có detector đa lớp, thử nghiệm live IDS hoặc chứng minh thuật toán ensemble mới.',
        [ev(methods,'Thiết kế và tập dữ liệu','Normal = 0 và Attack = 1')])
    add('split','MEDIUM','TRAIN và TEST được tổ chức thế nào, TEST có được dùng chọn ngưỡng không?',
        'Giữ official TRAIN 175.341 dòng và TEST 82.332 dòng. TEST có 37.000 Normal và 45.332 Attack. Cấu hình và threshold 0,5 đã khóa trước final evaluation; vòng phản biện này chỉ đọc summaries, không mở raw TEST hoặc dự đoán từng dòng.',
        [ev(methods,'Thiết kế và tập dữ liệu','TRAIN có 175\\,341 dòng'),ev(freeze,'All candidates decision_threshold','"decision_threshold": 0.5')])
    add('overlap','HARD','8.541 dòng trùng TRAIN có khiến toàn bộ kết quả vô hiệu không?',
        'Đó là overlap theo vector 42 predictors, không tự chứng minh mọi hình thức leakage hay làm mọi hàng TEST vô giá trị. Chúng tôi báo cáo official view và sensitivity view 73.791 novel-vector rows. Hai view phụ thuộc nhau, không phải hai thí nghiệm độc lập. Novel-vector cũng không chứng minh unseen attack families.',
        [ev(view,'overlapping_test_rows/novel_vector_test_rows','"overlapping_test_rows": 8541')])
    add('feature_selection','HARD','Feature selection có hoàn toàn nested và leakage-free không?',
        'Không. Stable features được chọn trên toàn bộ official TRAIN trước development CV. Vì vậy điểm CV có nguy cơ lạc quan. Final TEST không được dùng fit selector theo source, nhưng điều đó không biến development selection thành fully nested. Muốn đo lợi ích quy trình FS phải có nghiên cứu nested mới được phê duyệt, không sửa bảng hiện tại.',
        [ev(methods,'Feature selection và preprocessing','toàn bộ official TRAIN trước development cross-validation')])
    add('stacking','HARD','OOF stacking khác với meta học từ dự đoán in-sample ở đâu?',
        'P9 dựng StackingClassifier với các base pipeline LR, DT, RF và cv=inner_cv; inner StratifiedKFold có 3 folds. predict_proba của các clone trong CV tạo đầu vào meta LR, passthrough=False. OOF tránh để mỗi base dự đoán đúng hàng mà nó fit trong bước tạo meta inputs; nó không tự loại mọi thiên lệch ở bước chọn base/siêu tham số.',
        [ev(p9,'make_stacking_42','cv=inner_cv'),ev(p9,'make_stacking_42','passthrough=False')])
    add('selection_bias','HARD','Tại sao có OOF vẫn chưa được gọi là fully nested model selection?',
        'OOF là một ranh giới fit của stacking. Base/config selection và meta hyperparameter search có thể dùng thông tin phát triển chung. Báo cáo đã ghi meta tuning chưa fully nested; không thể coi CV đánh giá lại sau selection là unbiased outer test. Muốn khắc phục phải thiết kế outer/inner selection mới với holdout hợp lệ riêng.',
        [ev(methods,'Các pipeline được khóa','meta tuning chưa hoàn toàn nested')])
    add('ablation','HARD','Có thể nói giảm 42 xuống 17 feature làm mô hình nhanh hơn 6,48 lần không?',
        'Không thể quy riêng cho feature count. RF42 có 300 cây, min_samples_leaf=1; RF17 có 150 cây, min_samples_leaf=2. Kết quả là trade-off giữa hai pipeline cùng thay feature và hyperparameters. Cần matched hoặc factorial experiment để phân biệt các tác động, chưa được phép chạy trong checkpoint này.',
        [ev(freeze,'random_forest_42/random_forest_17','"n_estimators": 150'),ev(methods,'Comparison caveat','pipeline-level performance--cost trade-off')])
    add('imbalance','HARD','Nghiên cứu đã chứng minh resampling không cần thiết chưa?',
        'Chưa. TRAIN nghiêng về Attack và TEST có prevalence khác. Meta frozen dùng class_weight=None; một trường class_weight hoặc một tìm kiếm meta không là controlled imbalance ablation. RQ5 chưa có đối chứng matched về sampling/weighting trong folds. Không dùng official TEST để lựa chọn SMOTE hay class weight mới.',
        [ev(freeze,'stacking_42 meta_learner','"class_weight": null'),ev(conclusions,'Công việc còn thiếu','Với RQ5')])
    add('threshold','HARD','FPR cao có cho phép hạ hoặc nâng ngưỡng ngay để cứu kết quả không?',
        'Không. Threshold hiện là 0,5 cho cả ba candidate. Phân tích hậu nghiệm có thể giải thích hạn chế nhưng không được chọn threshold theo TEST. Một operating point khác cần validation và contract mới; không gắn score mới vào kết quả frozen.',
        [ev(freeze,'decision_threshold','"decision_threshold": 0.5'),ev(methods,'Final evaluation','Không dùng TEST để chọn lại mô hình')])
    add('accuracy','MEDIUM','Accuracy khoảng 87% đã đủ để gọi IDS tốt chưa?',
        f'Chưa. RF42 accuracy={float(rf["accuracy"]):.6f}, attack Recall={float(rf["recall_attack"]):.6f}, nhưng FPR={float(rf["fpr"])*100:.4f}%. Recall cao đi cùng lượng báo động giả lớn. Chưa có prevalence vận hành, chi phí cảnh báo hoặc điều kiện network thực để kết luận utility.',
        [ev(metric,'random_forest_42 official_test',rf['accuracy']),ev(confusion,'random_forest_42 official_test','26997,10003,734,44598')])
    add('metrics','MEDIUM','Macro F1 và Weighted F1 trả lời các câu hỏi nào?',
        f'Macro F1 cho hai lớp trọng số bằng nhau; Weighted F1 dùng support của từng lớp. RF42 có Macro F1={float(rf["macro_f1"]):.6f} và Weighted F1={float(rf["weighted_f1"]):.6f}; Stacking có {float(st["macro_f1"]):.6f} và {float(st["weighted_f1"]):.6f}. Không đổi F1 Attack hoặc F1 không ghi averaging của external paper thành Macro F1.',
        [ev(metric,'official_test macro_f1/weighted_f1',rf['weighted_f1'])])
    add('error_cost','HARD','Giảm 142 FP nhưng tăng 118 FN có phải cải thiện tổng thể?',
        'Đây là trade-off quan sát. RF42 FP=10.003, FN=734; Stacking FP=9.861, FN=852. Không có ma trận chi phí hay trọng số attack-family vận hành nên chưa quy thành lợi ích tổng thể. Ít lỗi tổng cộng hơn về số học không tự đồng nghĩa tốt hơn về an ninh.',
        [ev(confusion,'RF42 and stacking official_test','stacking_42,official_test,27139,9861,852,44480')])
    add('paired_CI','HARD','CI chứa 0 chứng minh hai mô hình tương đương hay Stacking tốt hơn không?',
        f'Không cho cả hai. Delta Macro F1 Stacking-RF42={float(delta["delta_a_minus_b"]):.12f}; CI95% [{float(delta["ci_lower"]):.12f}, {float(delta["ci_upper"]):.12f}]. Chưa đủ bằng chứng superiority trên thước đo này. Equivalence cần biên thực tiễn định trước và phép suy luận phù hợp; không được tạo biên hậu nghiệm để hợp thức hóa.',
        [ev(paired,'official_test stacking_42 vs random_forest_42 macro_f1',delta['ci_lower'])])
    add('McNemar','HARD','McNemar p=0,468377 có phải p-value cho chênh lệch Macro F1?',
        'Không. Exact two-sided McNemar dùng 491 và 515 trường hợp discordant về đúng/sai tổng thể, p Holm=0,46837651914684564. Nó kiểm tra paired correctness, không trực tiếp Macro F1, MCC hoặc equivalence. Cần giữ riêng paired metric CI.',
        [ev(mc,'official_test stacking_42 vs random_forest_42','491,515,1006,0.46837651914684564')])
    add('multiplicity','HARD','Holm có điều chỉnh mọi CI và mọi phân tích hậu nghiệm không?',
        'Không. Holm ở bảng McNemar áp dụng ba pairwise correctness comparisons trong mỗi evaluation view theo implementation. CI bootstrap metric là pointwise; hai view dùng chung nhiều dòng, attack-family và các profile là exploratory. Không tuyên bố toàn bộ tập phát hiện đã được familywise control.',
        [ev(mc,'three pairs per view','p_exact_raw,p_holm'),ev(stats,'mcnemar','"familywise_correction": "Holm"')])
    add('bootstrap_unit','HARD','10.000 bootstrap draws có nghĩa 10.000 lần tái huấn luyện độc lập không?',
        'Không. Source dùng stratified paired multinomial bootstrap trên joint prediction patterns của benchmark đã khóa, giữ ghép cặp và support theo lớp. CI có điều kiện trên rows và mô hình đã fit. Không định lượng độ bất định do huấn luyện lại, model selection hoặc session/host dependence; không nhân n thực nghiệm lên 10.000.',
        [ev(stats,'bootstrap type and interpretation','stratified paired multinomial bootstrap over joint prediction patterns')])
    add('attack_family','HARD','Tại sao không gọi bảng Fuzzers/Generic là kết quả multiclass?',
        'Model vẫn dự đoán Normal/Attack. Bảng phân nhóm FN theo nhãn thật attack_cat sau dự đoán binary. Stacking tăng 133 FN ở Fuzzers và giảm 43 ở Generic so RF42, cho thấy tác động không đồng đều. Không đánh giá đúng loại tấn công được dự đoán.',
        [ev(results,'Phân tích lỗi theo họ tấn công','6062  & 621 & 754 & +133')])
    family = 'results/final_analysis/unsw_nb15/phase10_statistics/tables/attack_family_miss_rate_ci.csv'
    add('rare_attack','HARD','RF17 không bỏ sót Worms có chứng minh phát hiện hoàn hảo họ này không?',
        'Không. Chỉ có 44 Worms trong benchmark; RF17 FN=0 nhưng Wilson95% miss-rate upper=0,08029560375848066. Đây vẫn là row-based interval có giả định, không bảo đảm cho Worms ngoài benchmark hoặc session độc lập.',
        [ev(family,'official_test Worms random_forest_17','official_test,Worms,random_forest_17,44,0,0.0,0.0,0.08029560375848066')])
    add('generalization','HARD','Novel-vector có tương đương unknown attacks, temporal hay external validation không?',
        'Không. Novel-vector chỉ khác đúng vector predictors của TRAIN. Nhãn attack families, môi trường và phân bố có thể cùng nguồn. Cả official và novel-view vẫn thuộc một TEST; chưa có time/session/host split hoặc network mới. Tuyên bố zero-day hay transfer sẽ vượt evidence.',
        [ev(view,'purpose','Secondary leakage/repetition sensitivity evaluation only; does not replace official test.')])
    add('runtime','HARD','Có thể dùng thời gian lịch sử để cam kết tốc độ real-time không?',
        'Không. Các số train lịch sử RF42=371,244s, Stacking=980,170s, RF17=57,255s; inference là thời gian batch chia số mẫu, không latency end-to-end từng flow. Original environment UNKNOWN và chưa đo capture/feature extraction, tải, jitter hoặc hardware vận hành. P15 timings ở môi trường tái dựng là provenance khác.',
        [ev(cost,'pipeline timing rows','371.2439486999938'),ev(cost,'inference column','inference_ms_per_sample')])
    acceptance = 'results/reproducibility/p15_local_artifact_qa_01/artifact_acceptance.json'
    add('reproducibility','HARD','P15 đã hoàn tất mà trang 33 nói chưa có full TRAIN artifact, trả lời thế nào?',
        'Trang 33 là snapshot trước reconstruction. P15 hiện có ba reconstructed full-TRAIN artifacts đã qua author-host acceptance 69/69. Chúng không chứng minh giống binary lịch sử hay tái lập TEST scores trong môi trường gốc. Dùng companion status note, không sửa PDF đã duyệt và không gán score lịch sử cho artifact mới.',
        [ev(acceptance,'scope','NOT original model or scientific TEST validation'),ev(conclusions,'Công việc còn thiếu','bản tái dựng full TRAIN chưa thực hiện')])
    add('references','HARD','L06, L12 và N02 đã đủ để tuyên bố thuật toán của đề tài mới không?',
        'Chưa. Ghi chép nguồn cho thấy L06 có Chi-square và stacking; N02 MI-Boruta, RF/XGB/Catboost tới MLP trên UNSW; L12 hybrid FS/SMOTE-Tomek/stacking nhưng không phải UNSW. Khác learner/config/protocol không tự là methodological novelty. Phần đọc là selected sections; N01/N03 chỉ abstract nên không tự dựng Methods của họ.',
        [ev(lit,'L06 C02/C03;N02 C09/C10;L12 C15','MI and Boruta selected sets are intersected'),ev(scope,'reading_status records','PARTIAL_SELECTED_FULLTEXT_SECTIONS_READ')])
    add('protocol_comparison','HARD','Tại sao không so điểm đề tài trực tiếp với paper N02?',
        'N02 mô tả gộp TRAIN/TEST rồi random80/20, khác official holdout của đề tài. Task binary/multiclass, averaging, preprocessing và scope đo chi phí còn khác. Chúng tôi dùng bài để xác định prior art và thiết kế, không lập bảng xếp hạng thắng/thua qua score không matched.',
        [ev(lit,'N02 Methodology/Data description C08','aggregated the training and testing datasets')])
    add('contribution','HARD','Nếu không có thuật toán mới, đóng góp có thể bảo vệ là gì?',
        'Một case study thực nghiệm có kiểm toán trên UNSW-NB15. Điểm có evidence là chuỗi source/config/results đã khóa, đối chiếu RF/ensemble, error complementarity và giới hạn của nó, paired metric uncertainty, FP/FN và cost trade-off, overlap sensitivity và reconstructed-artifact provenance. Chưa đủ để quảng bá SOTA hoặc phương pháp mới; giá trị công bố còn cần đánh giá theo venue và bằng chứng bổ sung.',
        [ev(conclusions,'Đóng góp trong phạm vi đã chứng minh','một chuỗi thực nghiệm trên benchmark')])
    add('new_study','HARD','Những thiếu sót nào không thể sửa bằng câu chữ?',
        'Tính ổn định qua independent training, isolated causal effect của FS, matched imbalance comparison, external/session/time generalization và deployment cost cần nghiên cứu mới. Tài liệu có thể giới hạn claim và ghi đúng status, không tạo dữ liệu cho các câu hỏi này. Mọi nghiên cứu tiếp phải có protocol và holdout hợp lệ được phê duyệt, không tái sử dụng TEST hiện tại để chọn thắng.',
        [ev(conclusions,'Công việc còn thiếu và hướng nghiên cứu','thí nghiệm matched và nested feature selection')])
    add('negative_results','MEDIUM','Vì sao phải giữ Voting không tốt bằng RF và Stacking chưa thắng rõ?',
        'Đó là bằng chứng trả lời RQ1 trong scope đã làm. Chọn chỉ điểm thuận lợi sẽ thay đổi câu hỏi thành tìm mô hình thắng. Báo cáo giữ cả kết quả Voting không thuận lợi và kết luận Stacking không xác lập superiority tổng thể. Development CV không thay final holdout và cũng không phải training-repeat replication.',
        [ev(conclusions,'Đóng góp trong phạm vi đã chứng minh','Kết quả không thuận lợi của Voting')])
    add('deployment','HARD','Có thể trình diễn live inference bằng official TEST và công bố gói hiện tại chưa?',
        'Chưa trong contract này. Không mở official TEST/prediction CSV và không có live demo được nghiệm thu. Demo tương lai cần dữ liệu thử hợp lệ, schema và provenance của reconstructed artifact theo contract riêng. Quyền code/license, data/model và tài liệu bên thứ ba cần quyết định của chủ sở hữu; manifest nội bộ không cấp quyền phát hành.',
        [ev(acceptance,'scope','P15_LOCAL_ARTIFACT_READONLY_QA')])

    payload = dict(status='DRAFT_DEFENSE_PREPARATION;NOT_P20_FINAL', questions=questions,
                   evidence_basis='Fixed packet_02. Source summaries only, no new predictions, statistics or model execution.')
    (out / 'defense_questions.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    text = ['# Bộ hỏi đáp bảo vệ P20-PRE', '', 'DRAFT. 27 câu hỏi, chưa rehearsal hoặc được hội đồng thật xác nhận. Các câu trả lời là đề xuất cho phần bảo vệ, không phải sửa PDF hoặc khẳng định concern đã đóng.', '']
    for q in questions:
        text += [f'## {q["id"]} {q["question"]}', '', f'Mức độ {q["difficulty"]}. Chủ đề {q["theme"]}.', '', q['answer'], '', 'Nguồn trong immutable packet', '']
        text += [f'- `{e["path"]}`. {e["locator"]}.' for e in q['evidence']]
        text += ['']
    (out / 'DEFENSE_QA.md').write_text('\n'.join(text), encoding='utf-8')
    print(json.dumps(dict(questions=len(questions), status=payload['status'])))


if __name__ == '__main__':
    main()
