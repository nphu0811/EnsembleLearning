# P21 — Giao thức thực nghiệm bổ sung có kiểm soát cho RQ1, RQ2, RQ5

**Ngày thiết kế:** 18/10/2026. **Trạng thái:** `DESIGN_ONLY / NOT_EXECUTED / AUTHOR_PRE-FLIGHT_APPROVAL_PENDING`.

**Vai trò khoa học:** thí nghiệm bổ sung **sau khi đã quan sát kết quả chính thức** và phản biện V2. Đây là protocol được cố định `trước khi chạy P21`, **không phải preregistration tiên nghiệm của toàn đề tài**, không làm hồi tố các giả thuyết P00/RQ, không thay thế P9/P15 hay số liệu trong PDF V2 47 trang.

**Chỉ tiêu nguồn lực:** laptop Windows 12 GiB RAM; tuần tự 1 worker; resource watchdog giống P15; tránh nested feature-selection/staking 5-fold trên toàn 175341 TRAIN nếu không có cơ sở năng lực.

## 1. Nguồn, ranh giới và bảo toàn

- **Dữ liệu duy nhất được mở để fit/evaluate P21:** `data/raw/unsw-nb15/UNSW_NB15_training-set.csv`, 175341 hàng, 42 predictors sau khi loại `id`, `label`, `attack_cat`. Label 0=Normal, 1=Attack; tuyệt đối không sử dụng `attack_cat` làm đầu vào hoặc group để đánh giá.
- Bất kỳ đường dẫn chứa `UNSW_NB15_testing-set.csv`, `official_test`, `phase9_holdout`, `phase10_statistics`, `final_evaluation` chỉ được đọc như **metadata hướng dẫn/đối chiếu phạm vi** trước khi chạy, **không mở dữ liệu hoặc prediction rows**, không load model lịch sử để chấm lại TEST. Mã P21 worker tuyệt đối không import/call `main()` của runner P9.
- Khóa hash trước thực thi: TRAIN SHA256 `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`, P9 source SHA256 `3e7d1369222ccdf452116e069a0db3df55e1d6d683d0f92f4e2bcde0800ae480`, candidates freeze `cdda800318c5d2259e581bff5b194381be7434d654950377dd4b40fca50be0a6`, Stage2 subsets `5a8fe201c88b49a2c018778f6d159a107b6fdfa810c05c1606e42e6d675244be`. Các số này dùng bảo vệ **nguồn lịch sử**, KHÔNG tái sử dụng stable17 cũ làm feature selector mới.
- Ghi `P21` vào thư mục mới `results/controlled_extensions/p21_train_only_<unique_run>/`, không ghi đè bảng P6–P15, `results/final_evaluation`, PDF V2, `report/` hoặc `.research_memory` đã đóng. Giữ nguyên ba reconstructed full-TRAIN joblib của P15.
- **Không tuyên bố nguồn validation P21 hoàn toàn độc lập với công trình lịch sử**: nhóm đã sử dụng official TRAIN trước đây để chọn họ mô hình/config và stable17; do đó P21 là `TRAIN_REUSED_POST_HOC_CONTROLLED_EXTENSION`. Nó xử lý leakage *bên trong phép kiểm định mới* khi selector refit đúng chỗ, nhưng không cung cấp một external test mới hoặc phép xác nhận hoàn toàn mù về mô hình.

## 2. Một lần phân chia TRAIN-only, không tinh chỉnh theo validation

Chỉ có một split P21 (bất biến giữa toàn bộ candidate, seed và RQ):

1. Từ 175341 TRAIN, lập fingerprint của **42 giá trị predictor gốc**, không chứa label, ID hoặc `attack_cat`. Chuẩn hóa cách biểu diễn kiểu dữ liệu cho fingerprint, lưu hash; các hàng có vector trùng hoàn toàn phải cùng nhóm.
2. Dùng `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=20261018)`, lấy **fold 0** làm `INTERNAL_VALIDATION` (mục tiêu khoảng 20%), bốn fold còn lại tạo `DEVELOPMENT_FIT_POOL` (khoảng 80%). Một group không thể nằm ở cả hai bên; không dùng lại seed khác để săn kết quả tốt.
3. Cổng QA trước khi fit: hai tập không giao row IDs, không giao group fingerprints, cả hai có Normal và Attack; tỷ lệ validation trong [18%, 22%] và tần suất class Normal trong validation sai khác so với official TRAIN tối đa 2 điểm phần trăm. Nếu không đạt, **dừng** và ghi blocker thay vì tự động đổi seed/fold.
4. Từ FIT_POOL, đối với mỗi replication seed được khóa trước `[1103, 2207, 3301, 4409, 5501]`, tạo một mẫu fit phân tầng **60000 hàng không hoàn lại**. Các arm cho một seed dùng đúng **cùng row IDs** và cùng validation; giữa seed có thể chồng lấn fit rows (không tạo 5 tập validation độc lập). Lưu hash sorted row IDs và class supports, không push raw CSV hay ID cá nhân.
5. Không cho bất kỳ selector/transformer/resampler/model được `fit` trên INTERNAL_VALIDATION. Validation label chỉ được dùng tính các metrics đã định nghĩa sau `fit`; không xem sớm các metrics để chọn seed, arm, threshold, features hoặc hyperparameter. Nếu cần gắn `predict_proba`, đó là suy luận trên validation **chỉ sau fit**, không phải tuning.

`StratifiedGroupKFold` chỉ khống chế nhóm **exact-predictor overlap**, không thể thay thế session/host/time-based grouping khi không có metadata tin cậy. Không tuyên bố traffic/session leakage-free. Nếu support/cân bằng không đạt, dừng trước fit, phê duyệt phương án thay thế độc lập không xem score.

## 3. Đặc trưng: phép ablation ghép cặp RQ2 thực sự

**Cấm sử dụng** `stage2_candidate_subsets.json:stable_2plus_methods` có từ **toàn bộ official TRAIN** như tập 17 đặc trưng của phép primary matched ablation.

Đối với **mỗi** 60000-row FIT subset (một seed), xây dựng **TRAIN-SUBSET-STABLE-TOP17** từ dữ liệu fit của seed đó, không bao giờ đọc validation:

- Kế thừa loại selector **MI filter + redundancy threshold 0.95**, **L1 Logistic Regression**, **ExtraTrees**, mỗi phương pháp tạo top20 trên **5 mẫu phân tầng 35000 hàng chỉ từ FIT subset** với các seed lựa chọn cố định [11,23,42,71,101]. Không chạy Stage2 `main()` vì hàm đó đọc toàn bộ TRAIN và ghi đè artifact; chỉ tái sử dụng/đưa vào module thuần các hàm selector, với kiểm thử bảo đảm input frame chỉ chứa training subset.
- Một biến đạt `stable` trong phương pháp nếu xuất hiện >=3/5 lượt; `stable_method_votes` bằng số phương pháp có điều kiện đó. Sắp xếp: `stable_method_votes` giảm dần, `mean_selection_frequency` giảm dần, **tên feature tăng dần để xử lý tie**. Chọn đúng **17 feature gốc** đầu tiên. Nếu không đủ 17 biến đạt >=2 method votes, vẫn dùng thứ tự predeclared cho đủ 17 nhưng ghi rõ `forced_top17_count` và **không gọi đây là bản sao historical stable17**.
- Selector phải đi cùng replication fit, được cache **chỉ trong replication đó** và dùng lại ở các arm matched; không fit mới dựa trên validation outcome.
- Track so sánh chính là `ALL42` và `TRAIN_SUBSET_STABLE_TOP17`. Categorical `proto/service/state` được OneHotEncoder(handle_unknown='ignore') **fit trong Pipeline trên FIT**, không dùng sklearn preprocess fit trên toàn TRAIN trước split. Track17 có thể có/không có các categorical; count 17 là biến gốc, không phải số dummy columns.

**Matched RF hyperparameters cho cả hai arm (khác duy nhất feature track):**
`n_estimators=150`, `min_samples_leaf=2`, `max_features=0.5`, `class_weight=None`, `bootstrap=True`, `random_state=replication_seed`, `n_jobs=1`, `threshold=0.5`. Đây là **cấu hình mới theo giới hạn tài nguyên**, không là RF17/RF42 historical frozen arm.

RQ2 estimand: `delta = metric(RF17_Matched) - metric(RF42_Matched)` trên cùng validation rows và FIT subset. Primary: **Macro-F1**; secondary: MCC, Recall(Attack), FPR, FNR, FP, FN, wall-clock fit/predict time, process-tree peak RSS, serialized estimator size (nếu an toàn). Không kết luận feature count đơn độc gây ra mọi khác biệt giữa `stable17` và ALL42 vì quy trình selector có thay đổi input và có thể biến thiên qua seed; điều được cô lập trong từng replicate là **tập feature đã tạo bởi quy tắc fit-only** với RF config cố định.

## 4. RQ5: matched imbalance intervention trên RF42 (không SMOTE sai kiểu)

**Cùng** ALL42, cùng 60000 fit rows và cùng RF parameters/seed/validation cho 3 arm:

- `W0` NONE: `class_weight=None`; dữ liệu fit nguyên trạng.
- `W1` BALANCED: `class_weight='balanced'`; **không resampling**, cùng số lượng fit và preprocess.
- `W2` RANDOM_OVER_SAMPLING: `class_weight=None` và oversample bằng cách lấy ngẫu nhiên có hoàn lại từ **lớp thiểu số trên FIT** tới bằng support của lớp đa số, dùng replication seed; categorical rows giữ nguyên giá trị, không tạo trường `proto/service/state` tổng hợp phi thực tế. Chỉ resample trên FIT, trước `Pipeline.fit`; không bao giờ đụng validation.

`W0/W1` là **matched weighting contrast** tốt nhất vì không đổi training-row counts; `W0/W2` là contrast của **can thiệp resampling** (thay đổi empirical sample size/weights by duplication), không thể gọi là tác động trọng số thuần túy. **Không dùng SMOTE/SMOTE–TOMEK** trong nhánh giá rẻ vì categorical/mixed-space validity, chi phí và rủi ro leakage; nếu sau này cần, mở protocol riêng với SMOTENC đúng cách trong fit fold, không bổ sung hậu nghiệm vào P21.

Primary RQ5 outcome: **FNR(Attack)** và **Macro-F1** (co-primary; báo cáo từng cái, không tuyên bố familywise significance); secondary: Recall, Precision(Attack), FPR, MCC, FP/FN, thời gian, cấu trúc errors. Lớp thiểu số trong official TRAIN là **Normal**, dù `Attack=1`; `class_weight='balanced'` tự tính trọng số theo support, **không được giả định mặc định tăng Attack Recall**. Báo cáo cả false alarm lẫn misses.

## 5. RQ1: benchmark lặp lại có ghép cặp trong ngân sách

Dùng `ALL42`, `W0` không trọng số, cùng RF anchor `150 trees / leaf2` cho so sánh:

- `RF42_LITE`: giống RQ2 ALL42/ RQ5 W0 (kết quả **tái sử dụng từ cùng mô hình đã fit trong replication**, không fit thêm RF baseline).
- `STACKING42_LITE`: base LR(C=1.0,liblinear), DT(min_samples_leaf=2), RF42_LITE params đồng nhất; final LR(C=0.5, class_weight=None, solver=liblinear), `passthrough=False`, `stack_method='predict_proba'`, inner `StratifiedKFold(n_splits=3,shuffle=True,random_state=137)`; sequential `n_jobs=1`, các learner dùng cùng replication seed khi có randomness. Không dùng OOF validation để chọn meta C. Đây là **một cấu hình Stacking mới nhẹ hơn P9** (RF-base 150/leaf2 vs historical 300/leaf1), kết luận áp dụng cho cặp `*_LITE` chứ không thay kết quả `Stacking42` frozen.
- Cùng fit subset của seed và cùng INTERNAL_VALIDATION; threshold 0.5; ghi paired predictions/grouphash **cục bộ**, không công bố raw record-level flows.
- 5 replication seeds là **mức mô tả khả năng lặp lại**, không phải 5 independent external datasets, không là bảo đảm phát hiện superiority/equivalence phổ quát. Giữa seeds thay đổi fit subsample và estimator RNG cùng lúc; variance quan sát bao gồm cả sampling và thuật toán, **không cô lập được variance chỉ do random_state**.
- **Primary** RQ1: per-replication `Delta Macro-F1(Stack-Lite - RF-Lite)`, `mean/SD/min/max`, số seed Delta>0/Delta<0; secondaries: Delta MCC, FPR, FNR, FP, FN, Recall(Attack), time/cost. Không dùng `5 seeds` tạo p-values hoặc gọi CI iid; validation rows dùng lại giữa seeds và có grouping. Có thể mô tả consistency under repeated refits, **không kết luận stable superiority nếu thiếu sức mạnh thiết kế**.
- Không thay mô hình/threshold/feature sau khi nhìn metrics; nếu budget không cho phép đủ 5 seeds, báo `INCOMPLETE_RQ1_REPLICATION_COUNT` với tất cả kết quả âm tính/giữa chừng, không chỉ chạy thêm cho cấu hình chiến thắng.

## 6. Ma trận arm và chi phí khả thi

| Arm | RQ | Features | Weight/resampling | 1 fit / seed | Distinct fits over 5 seeds |
|---|---|---|---|---:|---:|
| `A0_RF42_NONE` | RQ1/RQ2/RQ5 | ALL42 | None | 1 | 5 |
| `A1_RF17_NONE` | RQ2 | FOLD-FIT STABLE-TOP17 | None | 1 | 5 |
| `A2_RF42_BALANCED` | RQ5 | ALL42 | balanced | 1 | 5 |
| `A3_RF42_OVERSAMPLE` | RQ5 | ALL42 | random oversample Normal FIT only | 1 | 5 |
| `A4_STACK42_NONE` | RQ1 | ALL42 | None | 1 | 5 |

**Tổng:** 5 feature-selection replicates, **20 RF fits + 5 Stacking fits** trên subset 60000, không phải 25 full 175341-row fits. Điều kiện budget quan trọng: stacking có inner CV 3 và fit base đầy đủ, nên một `Stacking` là nhiều estimator fits nội bộ; không được gọi chi phí chỉ như một RF fit. Không chạy song song 5 seed, không lưu 25 large joblibs (ưu tiên summary/metrics/hash; mô hình của arm mới có thể bỏ sau validation và kiểm tra theo retention policy). Nếu chạy thiếu, phân biệt `DESIGN_COMPLETE`, `PILOT_ONLY`, `PARTIAL_ARM_MATRIX`, `RESULTS_COMPLETE`; không tự DONE.

**Execution gates, tuyệt đối không fit tự động khi cài code:**
- Preflight không tải ML/dữ liệu: xác minh CPU/12GiB RAM, Python 3.11.9, phiên bản sklearn1.9.0, pandas3.0.5, numpy2.4.6, nguồn hash, tình trạng repo sạch, đủ disk (>=10GiB), system available>=4GiB, reserve available>=1.5GiB và per process-tree peak RSS cap 2GiB.
- `PILOT` riêng với 8000–20000 FIT rows, no official TEST, no scientific metrics/chọn model; tối thiểu kiểm thử input leak guard, fold fit-only, output path isolation, memory/time sampling. Đo thực tế một RF-42, selector và Stacking pilot; không extrapolate tuyến tính tốc độ từ ít rows.
- Sau pilot author phải **opt in** vào full P21 60000-row tier; dự toán thời gian và RAM được ghi từ telemetry. Chỉ chạy 1 worker, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`, `n_jobs=1`, watchdog 0.5s, cấm spawn song song/SLURM/autoretry. 2GiB process RSS cap; available floor1.5GiB, >=10GiB disk; stop/fail immutable nếu vi phạm.
- Runtimes ở P15 **không suy ra chắc cho P21**: RF17 full TRAIN ~307s; RF42 full TRAIN 300 trees ~1867s; Stacking full TRAIN ~4759s trên Windows 12GB, P21 dùng 60000 rows và RF150 nên phải đo pilot. Không cam kết một phiên dưới X phút; P21 được chia thành các session, cache feature selection fit-only có hash và phục hồi, không lặp task đã pass.
- Soft caps gợi ý trước triển khai: 30min cho 1 RF fit, 90min cho 1 Stacking fit; vượt giới hạn thì stop `INCOMPLETE_RESOURCE_BOUND` và kiểm tra tài nguyên, **không** đổi n_estimators hoặc subset size sau khi xem score. Full study có thể cần nhiều giờ, không bắt buộc làm ngay.
- Có thể giới hạn chỉ Tier RQ2/RQ5 nếu Stacking quá nặng: **không** coi RQ1 complete. Nếu pilot quá nặng, dừng toàn bộ và xin protocol resource revision theo cost-only telemetry trước khi xem metric, không chọn mô hình theo validation.

## 7. Metric, phân tích so sánh và chuẩn báo cáo

- Không fit metric computation preprocessor trên validation. `classes` phải đúng `[0,1]`. Dự đoán: `predict_proba[:,index(1)]>=0.5`; không thay threshold theo score.
- Confusion convention: `TN, FP, FN, TP`; `FPR=FP/(FP+TN)`, `FNR=FN/(FN+TP)`, `DetectionRate=1-FNR`; `MacroF1` trung bình F1(Normal) và F1(Attack), `MCC` `sklearn.metrics.matthews_corrcoef`.
- **Paired data:** cùng validation row IDs cho tất cả arm và mọi seed; mỗi contrast tính hiệu số ở mức metric từ cặp predictions trên *cùng* validation. Lưu complete-case per-arm results kể cả bất lợi và exact fit-row checksum; không lấy `5*validation_n` làm 5 lần mẫu độc lập.
- Bảng kết quả tách **per-seed values** và `mean, sample SD, range, signed win count`; không p-hacking, không gọi Wilcoxon với 5 seeds là bằng chứng mạnh, không đóng gói bootstrap trên validation rows như CI repeated-training. Nếu dùng bootstrap trong phân tích thứ cấp, phải predeclare block unit và tách uncertainty theo rows khỏi variability theo refit; không dùng để khẳng định external generalization.
- Nếu tính riêng `class_weight='balanced'`, ghi class weights, training class counts; với oversampling ghi supports sau can thiệp; báo resource overhead và FPR/FNR **theo từng class**.
- Bảng diễn giải khoa học phải nêu `TRAIN-derived internal validation`, `post-hoc extension`, `lighter new configurations`, và việc prior tuning full TRAIN có thể làm phạm vi suy luận hẹp. **Không** gộp vào official TEST historical table hoặc tự so sánh độ chính xác TRAIN/internal val với official TEST như hai benchmark tương đương.
- **Acceptance:** cơ học 100% leak guards/resource/config/rowgroup pairs pass; khoa học RQ2 có 5 paired matched contrasts; RQ5 có 5x 3-arm contrasts; RQ1 có 5 paired refits RF-vs-Stack; không nhất thiết `positive` mới đạt. Nếu kết quả âm tính, vẫn báo đầy đủ. Chỉ đặt `P21_RESULTS_COMPLETE_WITH_LIMITATIONS` sau independent reviewer; **không** tự động giải quyết P20/G0-G6.

## 8. Checklist triển khai và deliverables

1. `config/p21_train_only_protocol_2026_10_18.json` là hợp đồng thông số immutable được commit trước lần fit đầu tiên; `tools/p21_protocol_validator.py` kiểm tra invariant không cần mở dữ liệu ML.
2. Runner mới **chỉ dùng đường dẫn TRAIN allowlist**, từ chối mọi tham số input với tên chứa TEST/holdout, từ chối đường dẫn output hiện hữu/symlink/escape, từ chối khi thiếu `--supervised-run` và user opt-in rõ ràng; audit file access trong runtime và recheck hash. Tách pure split/selector/model/evaluation, có unit tests bằng synthetic data để kiểm tra no-leakage.
3. Output dir mới của từng execution chứa `protocol_sha256, git_commit, environment, train_file_sha256, split_hashes, ordered train-only features, configs, seed, per-arm metrics, confusion matrices, resources.csv, status.json, failure_reason, timing`. Chỉ push compact redacted JSON/tables và figure từ metrics, **không** raw data, per-record probability arrays, TRAIN row IDs, token/API keys, model binaries.
4. Negative unit tests: fail nếu bất kỳ `fit` nào nhận validation row ID hoặc y_val, fail nếu selector bắt đầu từ original global stable17, fail nếu class weight arm vô tình thay RF hyperparameters, fail nếu group overlap, fail nếu threshold !=0.5, fail nếu `testing-set.csv` hoặc P9 main() được mở, fail nếu output path trùng P9/P15/frozen folders.
5. Lưu `P21` hoàn toàn ngoài P15/P16/P17; cập nhật `TASK_BOARD/HANDOFF/ROADMAP` nhưng giữ original RQ canon không đổi. Chỉ sau source+result QA và tác giả quyết định mới được tạo **PDF V3** riêng; V2 47 trang vẫn bất biến.

## 9. Tuyên bố khoa học phù hợp sau thực thi

Nếu hoàn thành P21, có thể đánh giá `(a)` mức dao động của RF/Stacking *lite* qua 5 lần train với subsampling, `(b)` matched feature-track trade-off khi giữ RF hyperparams, `(c)` tác động so sánh từ class-weight và simple row oversampling **trên internal TRAIN-derived validation**. Không được tự suy ra đây là xác nhận original frozen RF/Stacking trên official TEST, prospective independent confirmation, hay biến thiên trên lưu lượng thật.

**Nguồn tham chiếu để thực thi:** `src/features/select_unsw_features_stage2.py` (MI/L1/ExtraTrees pure selector helpers; `main()` không dùng), `src/models/run_unsw_phase9_final_holdout.py` (đọc cấu trúc RF/Stacking, tuyệt đối không gọi `main()`), `results/tuning/unsw_nb15/phase8_controlled/freeze_candidates.json` (historical read-only), `docs/research/FULL_TRAIN_RECONSTRUCTION_SCOPED_CLOSURE_2026-10-17.md` (resource cost provenance). Không phụ thuộc NotebookLM như bằng chứng thí nghiệm.
