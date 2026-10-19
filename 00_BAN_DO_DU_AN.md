# BẢN ĐỒ DỰ ÁN NCKH — BẮT ĐẦU TỪ ĐÂY

Đây là **bản chỉ đường**, không phải bản nghiên cứu khác. Bạn vẫn làm việc trên cùng một repository, cùng một bộ kết quả train/TEST.

## Hai cách mở dự án trong VS Code

**Chế độ gọn — một cây thư mục, đầy đủ nhóm công việc:** mở `NCKH_GON.code-workspace` hoặc mở trực tiếp thư mục NCKH (do `.vscode/settings.json` đã cấu hình). Explorer hiện đủ các nhóm nghiên cứu, báo cáo, slide/video, tài liệu, công cụ, kiểm thử và bộ nhớ; chỉ ẩn cache, môi trường và thư mục tạm. Năm thư mục nghiên cứu cốt lõi:

| Thư mục | Dùng để làm gì? | Ghi chú |
|---|---|---|
| [config/](config/) | Cấu hình dataset, pipeline, thí nghiệm | Không thay đổi protocol đóng băng |
| [data/](data/) | Dữ liệu raw/interim/processed | Local CSV không nhất thiết được push lên Git; **không xóa** |
| [notebook/](notebook/) | Nhật ký triển khai/phân tích từng bước | Tên `phase*` là định danh để truy vết |
| [results/](results/) | Kết quả train, TEST, bảng, hình, thống kê | **Bất biến**: không rename, xóa, chạy lại |
| [src/](src/) | Source chính phục vụ xử lý/training/inference | Không sửa I/O, không thay thuật toán |

**Chế độ đầy đủ — khi cần viết báo cáo, làm slide, kiểm thử:** mở `NCKH_DAY_DU.code-workspace`. Chế độ này gom tên thư mục thành các mục tiếng Việt có thứ tự: nghiên cứu → báo cáo → thuyết trình → hỗ trợ. Các thư mục vẫn ở nguyên chỗ trên ổ cứng; không có file nào được di chuyển.

Các nhóm hỗ trợ dưới đây cũng hiện trực tiếp trong bản GON; bản đầy đủ vẫn dành cho cách mở từng nhóm thành root riêng.

**Cách chuyển:** VS Code → **File → Open Workspace from File...** → chọn một trong hai file `.code-workspace` ở thư mục NCKH. Có thể dùng **File → Open Folder... → NCKH** để trở lại chế độ gọn. Cửa sổ chưa cập nhật sau `git pull` thì dùng **Developer: Reload Window** trong Command Palette (Ctrl+Shift+P).

> File và thư mục bị ẩn trong Explorer **không bị xóa hay đổi đường dẫn**; có thể dùng chế độ đầy đủ để xem, build và chạy source khi cần.

## Các nhóm thư mục phụ (trong chế độ đầy đủ)

| Nhóm | Vị trí vật lý | Công dụng |
|---|---|---|
| **Báo cáo và bài viết** | [report/](report/), [exports/](exports/), [proposal/](proposal/) | Nguồn LaTeX, PDF từng bản, đề cương |
| **Trình chiếu và bảo vệ** | [presentation/](presentation/), [defense/](defense/) | PPTX, MP4, script, Q&A |
| **Tài liệu học thuật** | [docs/](docs/), [literature/](literature/) | Roadmap, audit, bài báo và trích dẫn |
| **Vận hành, kiểm thử** | [tools/](tools/), [tests/](tests/), [reproducibility/](reproducibility/) | Script kiểm định và hướng dẫn tái lập |
| **Biểu mẫu, nộp hồ sơ** | [templates/](templates/), [release/](release/) | Mẫu và checklist bàn giao |
| **Bộ nhớ nghiên cứu** | [.research_memory/](.research_memory/) | Quyết định, evidence, trạng thái, lịch sử |
| **CI và Git** | [.github/](.github/), [AGENTS.md](AGENTS.md), [MASTER_PROMPT.md](MASTER_PROMPT.md) | Điều phối Codex, quy tắc dự án |

## Những tệp quan trọng cần tìm

- **Báo cáo PDF V7 đã được chấp nhận về nội dung:** [Báo cáo NCKH](presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf).
- **Kịch bản thuyết trình 6 phút:** [Kịch bản](presentation/nckh_defense/script_first_v3/KICH_BAN_THUYET_TRINH_6_PHUT_V7.md).
- **Nội dung 10 slide đối chiếu PDF:** [Content pack](presentation/nckh_defense/script_first_v3/final_10_slide_v1/CONTENT_PACK_VA_KICH_BAN_10_SLIDE.md).
- **Video luyện tập:** [Preview NeuralVoice](presentation/nckh_defense/script_first_v3/final_10_slide_v1/NCKH_Ensemble_IDS_10_Slides_Preview_NeuralVoice.mp4).
- **PowerPoint 10 slide:** [Bản PPTX đang cần PowerPoint Repair](presentation/nckh_defense/script_first_v3/final_10_slide_v1/NCKH_Ensemble_IDS_10_Slides_Final.pptx); giữ các bản dự phòng.
- **Kiểm định và bàn giao:** [Handoff](.research_memory/HANDOFF.md), [Roadmap](docs/ROADMAP_CURRENT.md), [Báo cáo dọn repo](.research_memory/SAFE_PRESENTATION_CLEANUP_2026_10_19.md).

## Vì sao không di chuyển những thư mục cũ vào folder mới?

Các lệnh train, bài kiểm thử, GitHub Actions, file JSON/CSV và báo cáo khoa học có liên kết bằng **đường dẫn thực**, ví dụ `results/.../phase9_holdout/...`. Di chuyển folder hàng loạt hoặc bỏ chữ `Phase 1` trong tên thật có thể làm mất liên kết, sai hash/provenance hoặc khiến mô hình không thể tái lập.

**Cập nhật theo yêu cầu cleanup:** 53 tài liệu đã được đổi sang tên công việc, bỏ mã phase; xem [bảng tên mới](docs/CURRENT_DOCUMENTS.md). Giữ nguyên tên thật của dữ liệu, model, kết quả thí nghiệm, protocol đóng băng và mã nguồn train/TEST. Bản GON hiện đủ nhóm công việc trong một cây NCKH.

## Kiểm tra sau khi kéo Git

```powershell
cd "C:\Users\admin\Documents\ChatGPT\NCKH"
git status --short
git pull --ff-only origin main
code NCKH_GON.code-workspace
```

Nếu có file local chưa commit, xử lý/lưu lại trước khi pull. Để mở mọi thư mục:

```powershell
code NCKH_DAY_DU.code-workspace
```

**Không chạy** `git clean -fdx`, **không xóa** dataset CIC-IDS2017/UNSW-NB15 đang có trên máy và **không đổi** thư mục `results/` hoặc source train.
