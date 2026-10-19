# Skill Decision Matrix — V2

Humanizer3.1: đã đọc toàn bộ SKILL.md từ blader/humanizer, MIT; áp dụng file/embedded mode, văn phong trung tính. Đã sửa38 đoạn V7, viết lại17 lời nói theo cách diễn đạt tự nhiên, giữ thuật ngữ và công thức trong Q&A. Không dùng như bộ phát hiện AI hoặc cam kết người viết.

OfficeCLI PPTX: đã đọc SKILL local và quy tắc QA, thực hiện independent screenshot judge. Morph PPT: đã đọc skill nền; không dùng Morph trong V2 vì cần timeline trong slide. PPT Master: đọc phần animation/native shape; không chạy engine package. Visual PPT Builder: đọc SKILL/RULES, tự dựng native shapes, không gọi image builder. Mức sử dụng này phân biệt với cài đặt/chạy engine.

Pipeline thực chạy V2: python-pptx→PowerPoint COM MainSequence (motion/scale/entrance)→CreateVideo1080p30→FFmpeg ghép voice. Report: XeLaTeX→BibTeX→XeLaTeX2 lần, font Liberation. Design references: Playwright Chromium fallback có screenshot, ghi rõ các trang bị CAPTCHA. Không dùng GSAP, Manim, Blender hoặc Remotion trong production vì một engine PowerPoint đã đáp ứng animation và chỉnh sửa.

## Hồ sơ khảo sát các công cụ được yêu cầu

Phần dưới kế thừa hồ sơ khảo sát có snapshot trong audit của deck đầu; các mục thực thi cũ không được tính thành sử dụng production V2. Humanizer và native timeline ở trên là thay đổi V2.

# Skill Decision Matrix

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
