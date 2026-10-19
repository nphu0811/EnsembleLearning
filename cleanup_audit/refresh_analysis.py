"""Refresh analysis from the captured inventory without repeating the full hash scan."""
import csv, importlib.util, json, re
from pathlib import Path

O=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('workspace_audit',O/'audit_workspace.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
R=a.ROOT
rows=list(csv.DictReader((O/'inventory.csv').open(encoding='utf-8-sig')))
for r in rows:
    r['protection']=a.protection(r['path']) if not r['path'].startswith('.git/') else 'Git history: KEEP'
a.csvout('inventory.csv',rows)
protected=[r for r in rows if r['protection'] and not r['path'].startswith('.git/')]
a.csvout('protected_files.csv',({'path':r['path'],'sha256':r['sha256'],'bytes':r['bytes'],'reason':r['protection']} for r in protected))
p=O/'04_PROTECTED_FILES.md';t=p.read_text(encoding='utf-8');t=re.sub(r'\d[\d,]* file được liệt kê',f'{len(protected):,} file được liệt kê',t);p.write_text(t,encoding='utf-8')
edges=[]
for r in rows:
    rel=r['path'];p=R/rel
    if p.suffix!='.tex' or a.runtime(rel):continue
    text=p.read_text(encoding='utf-8-sig',errors='replace')
    for kind,target in re.findall(r'\\(input|include|includegraphics|bibliography)(?:\[[^\]]*\])?\{([^}]+)\}',text):
        for token in target.split(','):
            suffixes=[''] if Path(token).suffix else ['','.tex'] if kind in {'input','include'} else ['','.bib'] if kind=='bibliography' else ['','.pdf','.png','.jpg','.svg']
            bases=[p.parent/token,R/token,R/'report'/token]
            # report_v7/source uses its own cwd for figures, bib and shared inputs.
            if '/report_v7/source/' in rel:bases.insert(0,R/'presentation/nckh_defense/creative_rebuild_v2/report_v7/source'/token)
            found=[]
            for base in bases:
                for suffix in suffixes:
                    q=Path(str(base)+suffix)
                    if q.is_file():
                        try:found.append(q.resolve().relative_to(R).as_posix())
                        except ValueError:pass
            edges.append({'source':rel,'kind':kind,'target':token,'resolved':next(iter(found),'')})
a.csvout('latex_dependencies.csv',edges,['source','kind','target','resolved'])
mds=[]
texts={}
for r in rows:
    rel=r['path']
    if a.runtime(rel) or rel.startswith('.git/') or int(r['bytes'])>6_000_000:continue
    if Path(rel).suffix.lower() in {'.py','.ps1','.md','.json','.tex','.yml','.yaml','.sha256','.txt','.ipynb'}:
        try:texts[rel]=(R/rel).read_text(encoding='utf-8-sig').replace('\\','/')
        except (OSError,UnicodeError):pass
for r in rows:
    rel=r['path']
    if Path(rel).suffix.lower()!='.md' or a.runtime(rel) or rel.startswith(('.git/','.research_memory/')):continue
    refs=[p for p,t in texts.items() if p!=rel and (rel in t or Path(rel).name in t)]
    mds.append({'path':rel,'sha256':r['sha256'],'bytes':r['bytes'],'reference_count':len(refs),
                'action':'KEEP','reason':r['protection'] or 'Core/unknown document: no proof of supersession and safe deletion',
                'references':json.dumps(refs,ensure_ascii=False)})
a.csvout('markdown_review.csv',mds,['path','sha256','bytes','reference_count','action','reason','references'])
unresolved=[e for e in edges if not e['resolved']]
a.md('DEPENDENCY_ANALYSIS.md',[
    '# Phụ thuộc, Markdown và giới hạn kiểm định',
    f'{len(edges)} LaTeX input/include/graphic/bibliography references; {len(unresolved)} chưa resolve qua cwd source/report (macro/dynamic/template paths có thể cần build). Xem latex_dependencies.csv; chưa gọi unresolved là broken file nếu dùng macro.',
    f'{len(mds)} Markdown project ngoài memory/runtime được phân loại trong markdown_review.csv. Có/không literal reference không đủ để xóa nội dung cốt lõi hoặc lịch sử.',
    'Imports Python, subprocess, PowerShell, workflows, config, manifest và Markdown thuộc tập 1,277 text project đã được dò tên/path ứng viên. Không đề xuất xóa bất kỳ module/CLI scientific nào, nên không suy diễn module unused từ import scan.',
    '4 PDF V2–V5 có references trong builder/visual QA và evidence lịch sử. Builder tạo output không có nghĩa cần PDF pre-existing; visual QA đọc PDF có thể fail sau khi xóa nếu không chạy builder trước. Remote main đã xóa PDF và manual-only các builder; chưa đồng bộ local trong lượt này.',
    'V6 PDF vẫn là đầu vào baseline của creative_rebuild_v2/qa_report_v7.py, cùng protected SHA maps; KEEP. Nguồn V7 gồm source riêng, fonts/assets và dependencies đã copy; không xóa report/ hoặc shared figures.',
    'PPTX XML: 32-slide gốc không internal timing; 29-slide Creative có 439 effects; 10-slide có 313 effect nodes. Zero missing shape target không chứng minh PowerPoint không Repair. Giữ cả 3 và các concept/backups.',
    'video_probes.json: ffprobe metadata, chưa full-decode/visual/audio listening hoặc native animation identity. Không xóa bản video tương ứng deck.',
    'research_prechecks.json: fresh protocol 29/29 + five-seed PASS (5 seeds/25 arms). .venv Python 3.11.9, scientific package inventory đã lưu; không có chứng minh môi trường thay thế, KEEP.',
    'STATE artifact manifest: 558 MATCH, 8 MISMATCH là .gitignore, mutable memory, README và roadmap. Không có missing entry; không thay checksum kỳ trước để biến finding thành PASS.',
    'Không chạy training, inference, bootstrap, held-out TEST scoring, full PDF rebuild hoặc save/repair PPTX. Chỉ hash opaque dataset/model bytes.',
])
p=O/'01_INVENTORY.md';t=p.read_text(encoding='utf-8').replace('Snapshot Git lấy trước thay đổi cấu hình hiển thị trong lượt audit nếu có;','Snapshot Git lấy sau thay đổi cấu hình hiển thị, trước chỉnh nhãn README/bản đồ;');p.write_text(t,encoding='utf-8')
p=O/'05_DELETION_PLAN.md';t=p.read_text(encoding='utf-8');t=t.replace('Bạn có thể duyệt nhóm A và giữ nguyên nhóm còn lại, hoặc yêu cầu xem xét thêm.','Nhóm A hiện rỗng. Mục cần quyết định là đồng bộ 4 PDF V2–V5 với remote sau khi xử lý tham chiếu; tổng logical bytes nếu bỏ 4 PDF là 1,648,103 (~1.57 MiB), chưa giải phóng. Giữ nguyên tất cả nhóm còn lại.');p.write_text(t,encoding='utf-8')
print(json.dumps({'protected_files':len(protected),'latex_edges':len(edges),'unresolved_latex_edges':len(unresolved),'markdown_review':len(mds)},indent=2))
