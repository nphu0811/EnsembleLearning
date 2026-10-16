"""Create a separate R05 revision. Preserve the reviewed R04 source verbatim."""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'proposal/researchwrite/nckh-ids'


def main():
    source = P / 'drafts/De_cuong_noi_dung_review_r04.md'
    target = P / 'drafts/De_cuong_noi_dung_review_r05.md'
    if target.exists():
        raise FileExistsError(target)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == 'dfef1dffa3fdd8efbb558b65a02cb13c443da8529c5efba169d6b7dc7ad47bac'
    text = source.read_text(encoding='utf-8')

    def replace(old, new):
        nonlocal text
        if text.count(old) != 1:
            raise ValueError('Expected exactly one replacement: ' + old[:60])
        text = text.replace(old, new)

    replace('gói nội dung phục vụ review r04', 'gói nội dung sửa sau review r05')
    replace('Hiện chưa có artifact mô hình để đáp ứng điều kiện đó.', 'Đã có ba artifact SMOKE_ONLY trên mẫu TRAIN để kiểm tra phần mềm; chưa có artifact mô hình final/fullTRAIN hợp lệ để đáp ứng điều kiện demo đó. [P:S8]')
    replace('Replay bảng aggregate đã đạt; huấn luyện trong môi trường sạch chưa được kiểm định', 'Replay bảng aggregate đạt; software smoke TRAIN-only trong venv mới đạt 45/45; fullTRAIN reconstruction chưa đạt, original environment UNKNOWN [P:S8]')
    replace('Phụ thuộc mô hình đã lưu; chưa đạt. Không dùng viewer kết quả thay demo', 'Phụ thuộc mô hình final/fullTRAIN và preprocessing đã lưu hợp lệ; chưa đạt. SMOKE_ONLY và viewer kết quả không thay demo')
    replace('Q&A nội bộ có 20 câu; các thành phần khác chưa đủ', 'Q&A nội bộ có 20 câu; đã có draft kịch bản 720 giây/runbook/checklist; chưa PPTX/PDF, rehearsal hoặc final demo [P:S9]')
    replace('Metadata và reading boundary theo `literature/resume_r02_2026_10_16/legacy_verification_ledger.csv` và `literature/resume_r02_2026_10_16/READING_NOTES.md`; không hàm ý full-paper review.', 'Metadata hiện hành theo `literature/resume_r04_2026_10_16/legacy_verification_ledger.csv`; `literature/resume_r02_2026_10_16/READING_NOTES.md` là provenance phần đọc trước đó, không phải current verification count; không hàm ý full-paper review.')
    replace('- Status sản phẩm: `.research_memory/TASK_BOARD.md`, `release/RELEASE_BLOCKERS.md`, `defense/qa_validation_r02.json`.', '- [P:S8]: `docs/research/R04_ML_SMOKE_REPORT.md`; `results/reproducibility/r04_ml_smoke_repaired/validation.json` và `run_metadata.json`.\n- [P:S9]: `defense/Kich_ban_thuyet_trinh.md`, `defense/Demo_runbook.md`, `defense/Final_QA_Checklist.md`, `defense/r04_content_validation.json`; `defense/qa_validation_r02.json` chỉ là evidence Q&A lịch sử.\n- [P:S10]: `docs/research/R05_FULL_TRAIN_RECONSTRUCTION_PLAN.md`; capacity snapshot và preflight validation của r05.\n- Status sản phẩm hiện hành được phân cấp tại phụ lục dưới đây; `.research_memory/TASK_BOARD.md` và `release/RELEASE_BLOCKERS.md` ghi gate tổng thể, không thay artifact.')

    foundation = (P / '06_rq_method_output_gates.md').read_text(encoding='utf-8')
    rqs = [line.split('|')[1].strip() for line in foundation.splitlines() if re.match(r'^\| RQ[1-5]', line)]
    assert len(rqs) == 5
    crosswalk = '''
#### Câu hỏi gốc và chuỗi kiểm định trong phạm vi đã thực hiện

Các RQ dưới đây được giữ nguyên từ thiết kế đã khóa, không đặt lại sau TEST. Đây là hồ sơ hồi cứu có giới hạn; phần chưa trả lời vẫn được ghi thiếu. [M:N1]

'''
    crosswalk += '\n\n'.join('- ' + rq for rq in rqs)
    crosswalk += '''

| RQ / mục tiêu thao tác | Phương pháp và bằng chứng đã lưu | Output, trạng thái và giới hạn |
|---|---|---|
| RQ1 — so sánh hiệu quả ensemble | Ba pipeline đóng băng; so sánh paired saved predictions, Macro-F1/MCC, bootstrap và McNemar [M:N3] | Bảng metric, CI và FP/FN. Chưa chứng minh stacking hơn RF42; CI chứa 0 không chứng minh tương đương. Stability qua independent retraining chưa được kiểm chứng. |
| RQ2 — mô tả đặc trưng và chi phí | Feature tracks, RF17/RF42, bảng cost và ablation hồi cứu [M:N3] | Bảng hiệu năng–chi phí và bỏ sót theo attack family của binary detector. PARTIAL cho effect riêng FS vì hyperparameters khác; không causal feature-only ablation. |
| RQ3 — tính bổ sung lỗi | Saved OOF diversity và kết quả ensemble development, giữ cả Voting kém [M:N3] | Bảng diversity/ensemble và association mô tả; không bảo đảm gain hoặc cơ chế nhân quả; chịu selection optimism. |
| RQ4 — độ nhạy đánh giá | Cùng frozen models, official và novel-vector views trong UNSW [M:N3] | Bảng theo view; PARTIAL. Chưa random-vs-temporal/day/scenario hoặc external validation; novel view không phải benchmark độc lập. |
| RQ5 phụ — mất cân bằng | Frozen no-resampling/class-weight scope; không matched resampling intervention [M:N1,M:N3] | Ghi config và giới hạn bằng chứng; controlled efficacy PARTIAL/UNANSWERED. Không kết luận sampling vô ích và không chọn can thiệp mới bằng TEST. |

Mục tiêu hoàn thiện O1 là kiểm nguồn/claim của tổng quan (output ledger và citation map); O2 là chuẩn hóa bảng/hình từ số liệu đóng băng (source-data map, numeric và visual QA); O3 là tài liệu tái lập và kiểm khả thi reconstruction/demo qua các gate A/B/C riêng; O4 là hồ sơ đúng mẫu và bảo vệ (DOCX/PDF, LaTeX/PDF, slides/script/Q&A và release checks). O1–O4 là công việc còn lại hoặc hoàn thiện một phần, không thay RQ hay xác nhận sản phẩm đã đạt. Dependency và tiêu chí kiểm từng sản phẩm nằm trong phụ lục kế hoạch phần việc còn lại. [M:N4,P:S8–S10]

Thuật ngữ đọc bảng: pipeline là chuỗi tiền xử lý và mô hình; feature track là một tập predictors cố định. Attack=1 là lớp dương; FP là Normal bị báo Attack, FN là Attack bị bỏ sót. FPR=FP/(TN+FP), FNR=FN/(TP+FN), TN/TP là dự đoán đúng Normal/Attack. Macro-F1 là trung bình F1 không trọng số hai lớp, được báo cùng MCC (Matthews correlation coefficient), ROC-AUC (diện tích đường ROC) và PR-AUC (trường pr_auc được tính bằng average precision, AP, trong source; không đồng nhất với tích phân hình thang đường precision–recall). Không dùng một metric để che đánh đổi lỗi. Paired bootstrap lấy mẫu đồng thời các dự đoán cùng dòng benchmark; CI là khoảng tin cậy có điều kiện, không repeated-training stability. [M:N2–N3]
'''
    replace('### Kết quả\n', crosswalk + '\n### Kết quả\n')
    appendix = '''## Phụ lục nội dung — kế hoạch phần việc còn lại và khả thi

Phụ lục này bổ sung khả năng kiểm tra nội dung, không thêm hoặc thay nhãn/bảng gốc của DOCX. Khi đưa vào Word phải giữ bảng sản phẩm 5 cột, các bảng I/II/III, lịch và các ô tiền trống; vị trí/độ dài phụ lục cần được kiểm khi render. Chưa có ngày khởi đầu, lịch còn lại được duyệt hoặc phân công nhân sự thật. Các vai trò dưới đây là vai trò cần giao, không phải danh tính đã xác nhận.

| Sản phẩm / thứ tự phụ thuộc | Vai trò cần giao; input và nguồn lực | Gate kiểm cụ thể và hành động khi chưa đạt |
|---|---|---|
| O1 tổng quan/citations → form/report | Người tổng hợp và người kiểm nguồn [CẦN XÁC NHẬN phân công]; ledger hiện có và đoạn nguồn đọc được | Mỗi claim trỏ passage/metadata đúng; L03 page conflict và U01/U03 giữ mở khi thiếu nguồn. Nguồn không đủ thì thu hẹp claim, không bịa DOI/pagination hoặc full-paper reading. |
| O2 bảng/hình → report/slides | Người phân tích và QA [CẦN XÁC NHẬN]; frozen CSV, script plotting/runtime thật | Source hash, công thức/nhãn/đơn vị, captions, export và visual inspection; lệch thì sửa script/prose và giữ failure log, không sửa frozen metric. |
| A replay/tài liệu code → O3 | Người phụ trách phần mềm [CẦN XÁC NHẬN]; Python và saved results đã có | Aggregate replay đã PASS; chỉ rerun khi input/code đổi hoặc có concern. TRAIN-only smoke mới đạt 45/45, không phải full reconstruction. |
| B fullTRAIN reconstruction → C demo | Người chạy và kiểm provenance [CẦN XÁC NHẬN]; source/config/TRAIN hashes, fresh env/wheel manifest, tài nguyên được kiểm trước job | Kế hoạch P15 riêng [P:S10]: một batch 3 frozen candidates, không TEST/tuning; proposed ceiling60 phút/7 GiB process tree, RAM trống trước chạy≥9 GiB và đĩa≥10 GiB; chưa được bảo đảm hoặc chấp thuận như lịch chạy. Snapshot r05 chỉ khoảng1,48 GiB RAM trống nên NO_GO, runner/watchdog cũng chưa triển khai. Dừng khi vượt trần hoặc hash/path/guard fail, lưu INCOMPLETE, không tự nới budget. |
| C demo suy luận → hồ sơ bảo vệ | Người phụ trách demo/QA [CẦN XÁC NHẬN]; chỉ model RECONSTRUCTED_FULL_TRAIN hợp lệ hoặc original artifact được xác minh, cùng learned schema/preprocessing | Load thật, class/probability semantics, valid/invalid CSV và roundtrip checks; chưa B thì C BLOCKED. Không lấy SMOKE_ONLY hoặc viewer thay demo; không gán metric lịch sử cho reconstruction chưa đánh giá. |
| O4 form Word, report LaTeX → PDF | Người viết, QA hình thức và tác giả/GVHD [CẦN XÁC NHẬN]; original templates, reviewed content, runtime build/render hỗ trợ | Copy provenance/hash; giữ nhãn/bảng gốc; references/crossrefs và số liệu đúng; build và xem từng trang, không truncation/overlap. Hiện loader/runtime DOCX và TeX chưa khả dụng trong lượt kiểm này; tiếp tục source/content, giữ G4/G5 mở. |
| O4 slides/script/Q&A/release | Người thuyết trình và QA [CẦN XÁC NHẬN]; report/hình ổn định, final demo và xác nhận hành chính | Q&A20, script720 giây và runbook/checklist mới là text drafts; cần PPTX/PDF render, rehearsal, inference thật, inventory/checksums và từng gate G0–G6. Thiếu dependency thì không FINAL/READY. |

Các ceiling trên là đề xuất bảo vệ vận hành cho kế hoạch reconstruction, không phải thời gian/RAM đã đo của full job, không phải equivalence margin. Có thể làm song song citation/source, figures và report source khi B/C bị chặn. Trước job lớn cần kiểm nguồn lực thực tế và quyết định budget của chủ máy; không khởi chạy trong công việc sửa đề cương này. [P:S8–S10]

Giữ lịch mẫu 4/11/11/4 tuần (30 tuần) chỉ làm ánh xạ, không cam kết hoàn thành mọi việc còn lại trong 4 tuần cuối. Phân công, ngày bắt đầu/kết thúc và khả năng bố trí thời gian [CẦN XÁC NHẬN]. Kinh phí mẫu 7.000.000 VND không chứng minh tài nguyên tính toán đã có hoặc được cấp. Không thuê cloud/API và không tự thêm khoản chi; điện/thời gian máy cùng mọi thực chi chưa được xác nhận, không ghi bằng0 như một sự kiện hành chính. Nếu tác giả không bố trí được model/runtime/hành chính, hồ sơ vẫn PARTIAL, không tự giảm nghĩa vụ final demo hoặc tạo release giả. [P:S5,P:S10]

'''
    replace('## Resolver nguồn nội bộ cho review\n', appendix + '## Resolver nguồn nội bộ cho review\n')
    with target.open('x', encoding='utf-8') as f:
        f.write(text)
    print(target.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
