"""Write reviewable delivery documentation from the actual plan/evidence/audio."""
from pathlib import Path
import json,csv,hashlib,statistics,subprocess
from content import MAIN,QA,SCENES
O=Path(__file__).resolve().parent; R=O.parents[1]
def write(name,txt): (O/name).write_text(txt.strip()+'\n',encoding='utf-8')
def ts(t):return f'{int(t)//60:02}:{t%60:05.2f}'
voice=json.loads((O/'audio/voice_measurements.json').read_text())
plan=json.loads((O/'slide_plan.json').read_text(encoding='utf-8'))
def incoming(i):return 0 if i==0 else (.9 if MAIN[i][0]==MAIN[i-1][0] else .55)
times=[];start=0
for i,item in enumerate(MAIN):
 sc,dur,view,title,spoken=item;v=voice[i];speech_start=start+incoming(i)+.10;speech_end=speech_start+v['voice_seconds']
 times.append({'slide':i+1,'scene':sc,'start':start,'end':start+dur,'incoming_transition':incoming(i),'speech_start':speech_start,'speech_end':speech_end,'silence_after':start+dur-speech_end})
 start+=dur
(O/'timeline.json').write_text(json.dumps(times,indent=2),encoding='utf-8')
assert min(x['silence_after'] for x in times)>.4, times
script=['# Kịch bản bảo vệ 6 phút','Bản đọc thử: giọng tổng hợp tiếng Việt NamMinh, tốc độ −5%; đo từ 20 MP3 thật bằng ffprobe. Đây là voice-over để luyện tập, không phải bản thu của sinh viên. Không tăng tốc âm thanh để ép thời lượng. Tổng slot 360 giây, đã tính chuyển cảnh.','Chạy từ slide 1 với Use Timings. Có thể dùng chuột để điều khiển khi tập, nhưng bấm sớm sẽ làm lệch khung 6 phút. Nhìn hội đồng khi đặt câu hỏi và kết luận. Chỉ đọc ý nghĩa, không đọc hết số thập phân.']
messages={1:'Cái giá của sai lầm là động lực nghiên cứu.',2:'So sánh ensemble với RF mạnh trong đúng phạm vi dữ liệu.',3:'Pipeline offline có nhãn/feature/preprocessing tách biệt.',4:'Cơ chế gộp quyết định khác nhau; OOF bảo vệ tầng meta.',5:'Chênh điểm nhỏ che một đánh đổi FP/FN có ý nghĩa.',6:'P21 matched kiểm tra giới hạn; chi phí FS phải được tính.',7:'Chọn mô hình theo chi phí lỗi, chưa có giá thiệt hại thực.',8:'Đóng góp kiểm chứng trong phạm vi benchmark, giới hạn công khai.'}
motions={
'opening':'Giữ flow phân nhánh FP/FN; dừng ở câu hỏi mở đầu.',
'question':'Fade vào: đầu vào bản ghi, hai nhánh kết quả Normal/Attack.',
'dataset':'Morph đổi góc nhìn sang hai phạm vi dữ liệu; không gộp điểm.',
'architecture0':'Fade lập toàn cảnh. Chấm cyan ở đầu vào; hình minh họa một flow.',
'architecture1':'Morph 0,9 s: chấm flow đi tới feature, node đầu vào đã đi qua giữ màu xanh.',
'architecture2':'Morph 0,9 s: chấm tới learner; nhấn quy tắc fit trong phần train.',
'architecture3':'Morph 0,9 s: chấm tới đầu ra, node phân loại sáng; nêu FP/FN.',
'rf':'Fade: nhiều cây hội tụ vào bộ tổng hợp; không giả lập thuật toán học.',
'voting':'Morph: LR/DT/RF hội tụ về luật gộp cố định; không dùng xác suất giả làm kết quả.',
'stacking':'Morph: giữ ba learner có tên trùng, thay tầng gộp thành meta LR; nêu OOF ở training.',
'testscore':'Fade: hai giá trị Macro-F1 thật, kèm MCC và Δ rõ ràng.',
'testfp':'Morph sang thanh FP; vùng FN chờ, chưa hiện số. Hai thang riêng có ghi chú.',
'testfn':'Morph: hai thanh FN từ vạch chờ tới chiều dài số liệu thật; FP giữ nguyên.',
'testsummary':'Morph về hai hiệu số; CI chứa 0, không nói tương đương.',
'p21design':'Fade: 5 chấm FIT hội tụ về một validation, không vẽ thành 5 tập TEST.',
'p21score':'Morph sang điểm paired của 5 seed; giữ tên seed và ghi rõ trục rút gọn.',
'p21cost':'Morph sang thanh cộng selector + model; phép cộng đúng đơn vị giây.',
'tradeoff':'Fade: tọa độ FPR/FNR từ cùng validation; mọi trục bắt đầu 0.',
'cost':'Morph sang giả định tổn thất trên official TEST lịch sử; nguồn được đổi rõ.',
'closing':'Fade kết luận và giới hạn; liên kết A1–A12 mở phụ lục sau bài chính.'}
sb=['# Storyboard','## Brief và lựa chọn nghệ thuật','Khán giả: hội đồng NCKH Việt Nam, kể cả người không chuyên từng thuật toán. Mục tiêu: hiểu câu hỏi, cách kiểm chứng và đánh đổi; không giới thiệu sản phẩm thương mại. 16:9, 1600×900 render, native shapes/text/connector. Bản chính 20 keyframe = 8 cảnh; 12 phụ lục ẩn.','| Phương án | Rõ ràng /5 | Sáng tạo /5 | Trình chiếu /5 | Công sản xuất tương đối | Quyết định |','|---|---:|---:|---:|---|---|','| Scientific Minimalism | 5 | 3 | 5 | Thấp | Nền, typography và bằng chứng |','| Cinematic Research Storytelling | 4 | 5 | 4 | Cao | Lấy hook, reveal và nhịp nghỉ; không dùng cảnh điện ảnh gây nhiễu |','| Architectural Technology Motion | 5 | 5 | 4 | Vừa | Chọn làm cơ chế chuyển động chính |','Đây là đánh giá thiết kế nội bộ, không phải điểm chấm từ hội đồng. Kết hợp Minimalism + Architecture; dùng cinematic cho nhịp câu chuyện.','## Hệ thống hình ảnh','Trắng #FFFFFF; nền phụ #EFF6FC; navy #0D3560; blue #1769AA; cyan #139DCB; chữ #172B43. Cam nâu #B65B29 chỉ định FN hoặc cấu hình can thiệp, không mã hóa Attack bằng màu đơn độc. Aptos có dấu Việt. Title 36pt; body 18–30pt; số chính 43–64pt. Nguồn và trục nhỏ là chú thích, không mang luận điểm duy nhất.','Signature object: một chấm cyan tượng trưng bản ghi flow. Rail dưới trang giữ nhịp 8 cảnh; trong cảnh kiến trúc chấm đi giữa node có tên !!actor-flow-record. Các node kế thừa tên qua keyframe và đổi trạng thái; thanh FN thay chiều dài giữa slide12–13. Các đối tượng kết thúc scene fade ra; không dùng ghost off-canvas tích lũy.','## Nhịp 8 cảnh','| Cảnh | Khoảng thời gian | Thông điệp |','|---|---|---|']
cursor=0
for sc,d in SCENES:sb.append(f'| {sc} | {ts(cursor)}–{ts(cursor+d)} | {messages[sc]} |');cursor+=d
sb+=['## Keyframe và chuyển động','| Slide | Cảnh | Slot | Tiêu đề | Choreography |','|---|---:|---|---|---|']
for i,(item,t) in enumerate(zip(MAIN,times)):
 sc,dur,view,title,spoken=item
 script += [f'\n## Cảnh {sc} · slide {i+1} · {ts(t["start"])}–{ts(t["end"])}',f'**Thông điệp:** {messages[sc]}',f'**Kích hoạt:** {ts(t["start"])} — {motions[view]}',f'**Nói:** {ts(t["speech_start"])}–{ts(t["speech_end"])} ({voice[i]["voice_seconds"]:.3f} giây đã đo).',f'> {spoken}',f'**Ngừng nói:** {ts(t["speech_end"])}–{ts(t["end"])} ({t["silence_after"]:.2f} giây).',f'**Chuyển ý:** câu cuối nối sang “{MAIN[i+1][3].replace(chr(10)," ")}”.' if i+1<len(MAIN) else '**Chuyển ý:** kết thúc bài chính; chỉ mở phụ lục khi được hỏi.', '**Luyện tập:** nói rõ chủ ngữ, để chuyển động kết thúc trước khi giải thích; không đọc nguồn hoặc hướng dẫn này.']
 sb.append(f'| {i+1} | {sc} | {ts(t["start"])}–{ts(t["end"])} | {title.replace(chr(10)," ")} | {motions[view]} |')
script += ['\n## Kiểm định thời lượng',f'Tổng lời đọc đã đo: {sum(v["voice_seconds"] for v in voice):.3f} giây; phần còn lại dành cho {sum(incoming(i) for i in range(len(MAIN))):.2f} giây chuyển cảnh, 2 giây đệm đầu lời và các khoảng nghỉ. Chi tiết: audio/voice_measurements.json, timeline.json. Người thuyết trình cần tập lại với giọng thật; không giả định giọng tổng hợp bảo đảm mọi người nói đúng 360 giây.']
write('Kich_ban_thuyet_trinh_6_phut.md','\n\n'.join(script));write('Storyboard.md','\n\n'.join(sb))
qn=['# Vấn đáp trong 4 phút','Không đọc cả 12 câu liên tiếp. Nghe hết câu hỏi; trả lời trực tiếp trong 15–25 giây; chỉ bổ sung bằng chứng khi được hỏi. Dành tối đa khoảng 45 giây cho một câu khó để còn thời gian cho câu tiếp.','Cuối slide20 có A1–A12 liên kết đến slide21–32 đang ẩn. Trong slide show có thể gõ số slide + Enter. Mỗi phụ lục có “Về kết luận”. Slide show chính giới hạn 1–20, video không chứa phụ lục.']
for j,(title,q,a,src) in enumerate(QA,1):qn += [f'## A{j} · slide {20+j}: {q}',a,'Nguồn: '+src]
write('QnA_4_phut.md','\n\n'.join(qn))

e=['# Scientific Evidence Map','Ngày đối chiếu: 19/10/2026 (Asia/Saigon). Không fit/retrain, không đọc raw TEST, không sửa kết quả đóng băng. Toàn bộ số biểu diễn lấy từ artifact có sẵn, chỉ tái tính số học từ confusion counts và trung bình seed.','## Nguồn gốc','| ID | Artifact tương đối từ repository | SHA-256 |','|---|---|---|']
source_paths={
'V6':'exports/report_revision_v6_2026_10_19/Bao_cao_NCKH_EnsembleLearning_REVISION_V6.pdf',
'TEST':'results/final_evaluation/unsw_nb15/phase9_holdout/tables/final_metrics.csv',
'CI':'results/final_analysis/unsw_nb15/phase10_statistics/tables/paired_bootstrap_differences.csv',
'P21':'results/controlled_extensions/p21_train_only_science_summary_20261019_022655/aggregate.json',
'P21_PROTOCOL':'config/p21_train_only_protocol_2026_10_18.json',
'HIST_CODE':'src/models/run_unsw_phase9_final_holdout.py',
'DEV_CODE':'src/models/run_unsw_ensemble_phase7_2.py',
'P21_CODE':'tools/p21_science_core.py',
'SELECTOR':'tools/p21_selector_core.py',
}
hashes={}
for key,path in source_paths.items():
 h=hashlib.sha256((R/path).read_bytes()).hexdigest();hashes[path]=h;e.append(f'| {key} | `{path}` | `{h}` |')
(O/'audit/protected_sources_sha256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
e += ['## Claim → slide → bằng chứng','| Claim / số liệu | Slide | Truy vết | Giới hạn |','|---|---|---|---|',
'| 175.341 TRAIN, 82.332 TEST; Attack=1; 42 predictor gốc | 2–7, A3 | V6 PDF tr.27–28 (trang in16–17), §3.1–3.3 | Không phải bắt gói realtime; id/label/attack_cat bị loại |',
'| LR/DT/RF, Voting, Stacking meta LR OOF | 8–10, A2/A7 | HIST_CODE build_preprocessor/make_stacking_42; DEV_CODE CONFIGURATIONS; P21_CODE make_stacking | Phân biệt train meta bằng OOF và suy luận; RF tự nó đã là ensemble |',
'| RF42 Macro-F1 0.8633434737, MCC 0.7509102615 | 11 | TEST: pipeline=random_forest_42, eval_view=official_test | Ngưỡng0.5; cùng 82.332 dòng |',
'| Stacking42 Macro-F1 0.8638401636, MCC 0.7504972252 | 11 | TEST: pipeline=stacking_42, eval_view=official_test | Chỉ ΔMacro-F1 +0.0004966899; MCC thấp hơn |',
'| FP RF=10003, Stack=9861; FN RF=734, Stack=852 | 12–14 | TEST cột fp,fn; Δ(Stack−RF)=−142,+118 | Số bản ghi; FP/FN hai trục riêng ghi rõ |',
'| CI95% ΔMacro-F1 [−0.0003118042,+0.0013089503]; ΔMCC [−0.0019378760,+0.0011395704] | 14, A9 | CI: official_test, stacking_42 vs random_forest_42 | Paired bootstrap hàng dữ liệu, 10.000 lượt; không phải CI biến thiên train |',
'| 5 FIT seed, 5 arm; 60.000 FIT/seed; 35.069 validation cố định | 15, A5 | P21 per_seed + các report được aggregate trỏ tới; audit/p21_verifier.txt | Hậu nghiệm TRAIN; không phải 5 TEST hay external validation |',
'| P21 RF42-Lite mean F1 0.945220; Stacking-Lite 0.944731 | 16 | P21 per_seed[seed].metrics_by_arm[A0_RF42_NONE/A4_STACK42_NONE].macro_f1; trung bình5 | 5 điểm và các đoạn nối cùng seed. Trục rút gọn0.944–0.946 ghi trên chart |',
'| P21 RF17-Lite F1 0.936751; fit84.600s +selector225.250s=309.850s; RF42fit241.119s | 17, A6 | V6 PDFtr.41, Bảng4.11; P21 per_seed.fit_seconds_by_arm; seed run_report.json worker_checks.selector.fit_seconds | Các lời gọi fit đo được, không phải end-to-end; RF17 lịch sử không FS-only |',
'| Balanced/Oversample giảm FPR, tăng FNR so A0 | 18, A11 | P21 metrics_by_arm fpr,fnr; mean5 | Normal là minority TRAIN. Cùng validation; không chọn lại threshold |',
'| ΔL=−142+118r; hòa r=142/118≈1.2034 | 19, A10 | TEST confusion counts; V6 §5.1 PDFtr.43 | Giả định cost-ratio; chỉ đúng cặp RF42/Stacking42 và dự đoán cố định |',
'| Selection bias stable17 trước CV; P21 không sửa hồi tố | 6,20,A4 | V6 §3.2–3.4 PDFtr.27–29 | Không tuyên bố toàn bộ historical development leakage-free |',
'| Không thuật toán mới, không external validation/triển khai trực tiếp | 20,A1/A12 | V6 §3.1,§3.5,§5.3–5.5 | Đóng góp là đối chiếu/kiểm chứng trong phạm vi benchmark |',
'## Quy tắc không được nói','Không nói “Stacking vượt trội”, “5 TEST độc lập”, “P21 là external TEST”, “RF17 giảm tổng chi phí” hay “đã triển khai IDS realtime”. Không gộp mức F1 TEST và P21 vào một trục như cùng điều kiện. Không biến OOF lịch sử thành nested hoàn chỉnh. Không trình bày ngưỡng chi phí giả định như thiệt hại thực tế.']
write('Scientific_Evidence_Map.md','\n\n'.join(e))

write('Skill_Decision_Matrix.md','''# Skill Decision Matrix

Khảo sát registry thực tế tại `C:/Users/admin/.codex/skills/` và catalog phiên. Tên nature-proposal-writer đăng ký là researchwrite; không sử dụng Nature Skill trong lượt dựng slide này, nên không ghi giả một lần thực thi Nature. Snapshot nguồn web và SHA trong audit/source_fetch_ledger.json. Thư mục gốc registry khác nhau không được đồng nhất với package remote.

| Công cụ/skill | Đọc/kiểm tra thật | Tương thích và giấy phép | Quyết định và mức dùng thực tế |
|---|---|---|---|
| Motion PPTX Studio 4.0 | SKILL remote; research-protocol, motion-grammar, speech-craft, craft, qa-checklist đã tải/đọc | Python3.9+, python-pptx/LO/poppler theo tài liệu; chưa xác minh giấy phép toàn repo trong phạm vi lượt này | Áp dụng ý tưởng keyframe/signature/timing; KHÔNG cài/chạy studio.py, không tuyên bố pass toàn bộ studio gates; không sao chép style pack/code |
| Visual PPT Builder | SKILL local và remote; slide-plan-schema remote (local thiếu references/scripts) | Local package thiếu builder/validator được SKILL trỏ tới; API LICENSE remote404, chưa xác minh giấy phép | Dùng nguyên tắc native reconstruction và manifest; không gọi build_ppt.py không tồn tại; không sinh page AI |
| PPT Master6.7.2 | SKILL local, attribution_guard chạy exit0, routing.md, generate-pptx.md khảo sát | MIT theo GitHub license; SVG→native và narration engine có workflow riêng | Khảo sát cấu trúc native/export; không chọn production runtime PPT Master, không tuyên bố chạy exporter/gates của package |
| OfficeCLI Morph PPT | SKILL morph-ppt và nền officecli-pptx local, phần schema/visual gate | OfficeCLI Apache-2.0; CLI không có trong PATH khi kiểm tra | Áp dụng !!name pairing, native geometry và fresh independent screenshot QA; không tuyên bố đã dùng CLI. Thực thi Morph bằng PowerPoint COM |
| OpenAI Skills / Plugins | Catalog local; URL official hiện tại và 2 repo được mở/lưu | Skills là workflow; connector load_workspace_dependencies không có trong tool registry hiện tại | Presentations visual design guidance và PDF read/render guidance; PowerPoint local dùng để xuất PDF, không dùng container marker bị thiếu runtime |
| Anatomy | Official page đã đọc, install `npx skills add wheresryan22/anatomy`, native SVG/HTML/TS, React optional | MIT theo trang official; browser animation, nhiều chi tiết/3D beta | Không cài/dùng. Pipeline IDS ngắn dễ hiểu hơn bằng native PowerPoint; tránh thêm web runtime không cần thiết |
| ManimGX | Official docs/install/license trên trang, đã khảo sát | Python API + Rust/wgpu; pip/native và npm/browser. Code MIT; native wheels GPL-3.0-or-later do x264 theo official page | Không cài/chạy. Không cần render toán/3D; PowerPoint native hiện khả dụng nên giữ một engine để kiểm chứng motion |
| Superpowers brainstorming | SKILL chính xác đã đọc | Quy trình chung | Dùng brief đầy đủ và so3 creative directions trong Storyboard; user đã yêu cầu tự chọn và bắt đầu, nên không thêm vòng xin phép trái phạm vi tự động |
| write-like-me | SKILL đã đọc | Không tìm mẫu riêng tư ngoài phạm vi | Theo chỉ dẫn tiếng Việt/câu ngắn của brief; không tuyên bố đã truy xuất phong cách cá nhân |

Pipeline thực chạy: Python3.11 + python-pptx → PowerPoint16.0 COM (Morph, timing, PDF, PNG, CreateVideo) → FFmpeg ghép voice-over tiếng Việt, trim tail encode chính xác360s. Cài python-pptx, pywin32, edge-tts vào Python hiện có; không cài toàn bộ các skill khảo sát. Không dịch vụ API trả phí hoặc key mới.

Nguồn khảo sát: [Motion Studio](https://github.com/meiiie/meiiie_skillls/tree/main/motion-pptx-studio), [Visual PPT Builder](https://github.com/Clockworkhg/visual-ppt-builder), [PPT Master](https://github.com/hugohe3/ppt-master), [OfficeCLI](https://github.com/iOfficeAI/OfficeCLI/tree/main/skills/morph-ppt), [Anatomy](https://skills.wheresryan.sh/anatomy), [ManimGX](https://manimgx.academa.ai/), [Codex skills hiện hành](https://developers.openai.com/codex/skills), [OpenAI skills](https://github.com/openai/skills), [OpenAI plugins](https://github.com/openai/plugins).

Storytelling tham khảo [TEDx Speaker Guide](https://storage.ted.com/tedx/manuals/tedx_speaker_guide.pdf) và [Toastmasters: Storytelling Tips From Contest Winners](https://www.toastmasters.org/Magazine/Magazine%20Issues/2023/Sept/Storytelling%20Tips). Áp dụng một luận điểm trung tâm, tình huống cụ thể và khoảng dừng. Không sao chép câu chuyện cá nhân hay giả vờ đã xem/phân tích toàn bộ video cuộc thi.
''')
write('Asset_Manifest.md','''# Asset Manifest

| Asset | Nguồn / cách tạo | Định dạng và quyền chỉnh sửa | Giới hạn |
|---|---|---|---|
| Sơ đồ flow và pipeline | Tự dựng từ HIST_CODE/P21_CODE; build_deck.py | Native PowerPoint rectangles/ovals/text/arrow connectors | Minh họa cơ chế offline; chấm cyan không phải một packet trace đo được |
| RF tree schematic | Tự dựng vector nhánh cây để giải thích bagging | Native connectors + nodes | Minh họa cấu trúc;5 cây biểu tượng không phải số cây đã huấn luyện |
| FP/FN bars | P9 final_metrics.csv, cột fp/fn | Native rectangles/text; scale có ghi chú | FP0–11000, FN0–1000; không so độ dài giữa2 trục |
| P21 paired seed chart | aggregate.json per_seed metric | Native dots/segments/text | X-axis rút gọn ghi rõ; cùng validation |
| Selector+fit cost bars | V6 Bảng4.11 / frozen P21 | Native rectangles/text | Giây fit; không phải end-to-end |
| FPR/FNR scatter | Trung bình5 seed của A0/A2/A3 | Native dots/axes/text | P21 only; trục0, unit phần trăm |
| SVG files | Export dự phòng từ native geometry trong build_deck.py | svg/slide_01.svg…slide_32.svg | SVG là bản trung gian để chỉnh geometry; PPTX và PowerPoint renders là chuẩn fidelity, SVG không có Morph và text wrapping có thể khác |
| PNG previews | Microsoft PowerPoint export,1600×900 | renders/slide_NN.png | Chỉ kiểm chứng trạng thái tĩnh |
| Audio voice-over | edge-tts vi-VN-NamMinhNeural, rate−5%; spoken text trong content.py | audio/slide_NN.mp3 + narration.wav | Giọng tổng hợp để luyện tập, không giả giọng người trong nhóm; cần mạng để tái tạo |
| MP4 motion | PowerPoint CreateVideo; ghép audio bằng FFmpeg | H.2641080p30 + AAC | Xem audit và QA_Report về timing, không dùng mô phỏng Manim |
| Fonts | Aptos từ Microsoft Office local | Text giữ editable; không nhúng/redistribute file font | Máy nhận cần font tương thích dấu Việt |

Không dùng ảnh AI, stock photo, robot, não sáng, bảng mạch hoặc logo bên thứ ba. Không sao chép style pack/template của các repo khảo sát. Báo cáo V6 và kết quả gốc được giữ nguyên; nguồn tải khảo sát chỉ nằm trong audit để kiểm tra, không dùng làm hình slide.
''')
write('README.md','''# Bộ bảo vệ NCKH Ensemble IDS

- Mở `NCKH_Ensemble_IDS_Final.pptx` trong PowerPoint desktop hỗ trợ Morph, chạy từ slide1 với timing để xem bài chính6phút. File giữ native shapes/text/connectors và speaker notes, không flatten thành ảnh.
- `NCKH_Ensemble_IDS_Preview.mp4` là preview có voice-over tổng hợp tiếng Việt; chuyển động lấy từ PowerPoint native, không phải Manim mô phỏng.
- `NCKH_Ensemble_IDS_Static.pdf` gồm20 keyframe chính.12 phụ lục Q&A có trong PPTX (ẩn khỏi bài chính) và QnA_4_phut.md.
- Slide20 có A1–A12 để mở phụ lục; khi thuyết trình có thể gõ21…32 rồi Enter. Mỗi phụ lục có liên kết về kết luận.
- Luyện bài theo Kich_ban_thuyet_trinh_6_phut.md; xem Scientific_Evidence_Map.md và QA_Report.md trước khi sửa số liệu.

Tái dựng trên Windows có PowerPoint: `python -m pip install -r requirements_presentation.txt`; chạy lần lượt `python build_deck.py`, `python make_voice.py`, `python animate_export.py prepare`, `python animate_export.py video`, `python make_documents.py`, `python finalize_video.py`, `python validate_delivery.py`. Chạy từ repo gốc hoặc dùng absolute script path; thư mục output tự định vị. Không chạy pipeline train/model. PowerPoint timing test đã chứng minh transition duration phải trừ khỏi dwell; animation script xử lý điều này.

TTS cần Internet; nếu đã có MP3 và SHA đúng thì dùng lại. Giữ PDF/MP4/PPTX đã xuất để xem offline. Phiên bản thư viện thực tế được ghi trong requirements_presentation.txt. `audit/` giữ ledger nguồn, kiểm tra P21, QA độc lập và log xuất engine. `svg/` là asset trung gian; nguồn chính là content.py và build_deck.py. `checksums.sha256` kiểm tra các sản phẩm giao.
''')
pkgs=['python-pptx','pywin32','edge-tts','pymupdf','Pillow','requests','numpy']
import importlib.metadata
write('requirements_presentation.txt','\n'.join(f'{n}=={importlib.metadata.version(n)}' for n in pkgs))
print(json.dumps({'documents_written':9,'speech_seconds':sum(x['voice_seconds'] for x in voice),'minimum_silence_after':min(x['silence_after'] for x in times),'timeline_seconds':times[-1]['end']}))
