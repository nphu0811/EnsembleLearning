"""Read-only workspace audit; writes new evidence only inside cleanup_audit.

Never deletes, moves, renames, loads models, trains, or evaluates datasets.
Git metadata inventory includes .git; content hashing excludes .git objects.
Reparse points are recorded but never traversed. Run from the repository root.
"""
from pathlib import Path
import collections, concurrent.futures, csv, hashlib, json, os, re
import subprocess, sys, time, zipfile, xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'cleanup_audit'
STAMP = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()
ERRORS = []

def git(*args):
    p = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True)
    return {'code': p.returncode, 'stdout': p.stdout.decode('utf-8', 'replace'),
            'stderr': p.stderr.decode('utf-8', 'replace')}

def paths(*args):
    r = git(*args)
    if r['code']: raise RuntimeError(r)
    return set(x.replace('\\', '/') for x in r['stdout'].split('\0') if x)

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def csvout(name, rows, keys=None):
    rows = list(rows)
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys or list(rows[0]) if rows else keys or ['path'])
        w.writeheader(); w.writerows(rows)

def md(name, lines):
    (OUT / name).write_text('\n'.join(lines) + '\n', encoding='utf-8')

def table(headers, rows):
    return ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join('---' for _ in headers) + '|'] + [
        '| ' + ' | '.join(str(x).replace('|', '\\|').replace('\n', ' ') for x in row) + ' |' for row in rows]

def human(n): return f'{n / 1048576:,.2f} MiB'

def runtime(rel):
    return any(x.lower().startswith(('.venv', 'venv')) or 'runtime' in x.lower()
               or x.lower() == 'site-packages' for x in Path(rel).parts)

def protection(rel):
    top = rel.split('/')[0]
    if top in {'data','results','config','.research_memory','templates','notebook','src',
               'literature','reproducibility','defense','release','report','docs','proposal','exports'}:
        return 'Research data/source/config/evidence/history: KEEP exact path and bytes'
    if rel.startswith('tools/p') or rel.startswith('tests/test_p'):
        return 'Scientific tooling and tests: KEEP interfaces and provenance'
    if rel.endswith(('.joblib','.pkl','.pickle','.pt','.pth','.onnx','.h5','.hdf5')):
        return 'Model: KEEP; no deserialize'
    if 'report_v7/source/' in rel or rel.endswith(('REVISION_V7.pdf','LaTeX_Revision_V7_Source.zip')):
        return 'Current V7 report/source: KEEP'
    if rel.endswith(('.pptx','.mp4')):
        return 'Presentation/video: KEEP pending desktop no-Repair, animation and pairing gates'
    if rel.endswith(('.zip','.sha256')) or '/audit/' in rel:
        return 'Archive/checksum/QA provenance: KEEP pending complete dependency review'
    if runtime(rel): return 'Environment/runtime: KEEP until verified replacement + rebuild dependencies'
    return ''

def hashone(row):
    p = ROOT / row['path']
    try:
        start = p.stat()
        with p.open('rb') as f: h = hashlib.file_digest(f, 'sha256').hexdigest()
        end = p.stat()
        if (start.st_size,start.st_mtime_ns) != (end.st_size,end.st_mtime_ns):
            return row['path'], '', 'changed during hashing'
        return row['path'], h, ''
    except OSError as e: return row['path'], '', str(e)

def main():
    tracked = paths('ls-files','-z')
    untracked = paths('ls-files','--others','--exclude-standard','-z')
    ignored = paths('ls-files','--others','--ignored','--exclude-standard','-z')
    cmds = {
        'status': ['status','--porcelain=v1','--untracked-files=all'],
        'branches': ['branch','-vv'], 'remotes': ['remote','-v'],
        'head': ['rev-parse','HEAD'], 'origin_main_cached': ['rev-parse','origin/main'],
        'remote_main_live': ['ls-remote','origin','refs/heads/main'],
        'ahead_behind_cached': ['rev-list','--left-right','--count','HEAD...origin/main'],
        'unpublished': ['log','origin/main..HEAD','--oneline'],
        'incoming': ['log','HEAD..origin/main','--oneline'],
        'incoming_changes': ['diff','--name-status','HEAD..origin/main'],
        'recent_history': ['log','-25','--date=iso','--format=%h %ad %s'],
        'lfs': ['lfs','ls-files'], 'objects': ['count-objects','-v'],
        'attributes': ['ls-files','*gitattributes'],
    }
    gs = {k:git(*v) for k,v in cmds.items()}
    dump('git_snapshot.json', gs)
    rows=[]; dirs=[]; links=[]
    for folder, subdirs, files in os.walk(ROOT, followlinks=False):
        here=Path(folder)
        keep=[]
        for name in subdirs:
            p=here/name; st=p.lstat()
            if p.is_symlink() or getattr(st,'st_file_attributes',0) & 0x400:
                links.append(str(p)); continue
            keep.append(name); dirs.append(p.relative_to(ROOT).as_posix())
        subdirs[:]=keep
        for name in files:
            p=here/name; rel=p.relative_to(ROOT).as_posix()
            if rel.startswith('cleanup_audit/'): continue
            try:
                st=p.lstat()
                if p.is_symlink() or getattr(st,'st_file_attributes',0) & 0x400:
                    links.append(str(p)); continue
                status='tracked' if rel in tracked else 'ignored' if rel in ignored else 'untracked' if rel in untracked else 'git-internal' if rel.startswith('.git/') else 'not-listed'
                rows.append({'path':rel,'absolute_path':str(p),'bytes':st.st_size,
                    'mtime_ns':st.st_mtime_ns,'git_status':status,'extension':p.suffix.lower(),
                    'sha256':'','protection':protection(rel) if not rel.startswith('.git/') else 'Git history: KEEP'})
            except OSError as e: ERRORS.append({'path':rel,'error':str(e)})
    print(f'Inventory: {len(rows)} files, hashing all readable non-Git files',flush=True)
    hrows=[r for r in rows if not r['path'].startswith('.git/')]
    hashed={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for i,(rel,h,err) in enumerate(pool.map(hashone,hrows)):
            hashed[rel]=h
            if err: ERRORS.append({'path':rel,'error':err})
            if i and i%10000==0: print(f'Hashed {i}/{len(hrows)}',flush=True)
    for r in hrows:r['sha256']=hashed[r['path']]
    bypath={r['path']:r for r in rows}
    csvout('inventory.csv',rows)
    sums=collections.defaultdict(lambda:[0,0])
    for r in rows:
        parts=r['path'].split('/')
        for depth in range(1,min(len(parts),4)):
            k='/'.join(parts[:depth]);sums[k][0]+=1;sums[k][1]+=r['bytes']
    csvout('directory_sizes.csv',({'directory':k,'files':v[0],'bytes':v[1]} for k,v in sorted(sums.items(),key=lambda x:-x[1][1])))
    ext=collections.defaultdict(lambda:[0,0])
    for r in hrows:ext[r['extension'] or '(none)'][0]+=1;ext[r['extension'] or '(none)'][1]+=r['bytes']
    dump('summary.json',{'timestamp':STAMP,'root':str(ROOT),'files_including_git':len(rows),
        'directories':len(dirs),'bytes_including_git':sum(r['bytes'] for r in rows),
        'non_git_files':len(hrows),'non_git_bytes':sum(r['bytes'] for r in hrows),
        'tracked_index_entries':len(tracked),'untracked':len(untracked),'ignored':len(ignored),
        'hashed':sum(bool(r['sha256']) for r in hrows),'errors':ERRORS,'untraversed_reparse_points':links,
        'measurement':'logical file bytes, not allocated clusters or measured freed disk space; excludes audit outputs'})
    # Read all persisted research memory as context; retain provenance summaries.
    memory=[]
    for r in hrows:
        if r['path'].startswith('.research_memory/'):
            p=ROOT/r['path']
            try:
                t=p.read_text(encoding='utf-8-sig');memory.append({'path':r['path'],'lines':len(t.splitlines()),'sha256':r['sha256']})
            except (UnicodeError,OSError): pass
    csvout('memory_read_receipt.csv',memory)
    state=json.loads((ROOT/'.research_memory/STATE.json').read_text(encoding='utf-8-sig'))
    reconcile=[]
    for entry in state.get('artifact_manifest',[]):
        p=entry.get('path',''); actual=bypath.get(p,{}).get('sha256','')
        reconcile.append({'path':p,'expected_sha256':entry.get('sha256',''),'actual_sha256':actual,
                          'status':'MATCH' if actual and actual==entry.get('sha256') else 'MISMATCH' if actual else 'MISSING'})
    csvout('state_manifest_reconciliation.csv',reconcile)
    # A literal reference is evidence of dependency. Absence alone never proves unused.
    suffixes={'.py','.ps1','.sh','.yml','.yaml','.tex','.bib','.md','.json','.toml','.ini','.cfg','.txt','.code-workspace','.svg','.ipynb','.sha256'}
    corpus={}
    for r in hrows:
        rel=r['path']
        if runtime(rel) or '/__pycache__/' in rel:continue
        if r['extension'] not in suffixes and not ('manifest' in rel.lower() or 'checksum' in rel.lower()):continue
        if r['bytes']>6_000_000:continue
        try:corpus[rel]=(ROOT/rel).read_text(encoding='utf-8-sig')
        except (OSError,UnicodeError):pass
    def refs(rel):
        base=Path(rel).name
        return [{'source':p,'match':'full-path' if rel in t.replace('\\','/') else 'filename'}
                for p,t in corpus.items() if p!=rel and (rel in t.replace('\\','/') or base in t)]
    groups=collections.defaultdict(list);names=collections.defaultdict(list)
    for r in hrows:
        if r['sha256']:groups[r['sha256']].append(r)
        names[Path(r['path']).name.lower()].append(r)
    duplicate_groups=[(h,v) for h,v in groups.items() if len(v)>1]
    duprows=[]
    for i,(h,v) in enumerate(sorted(duplicate_groups,key=lambda x:-x[1][0]['bytes']*(len(x[1])-1)),1):
        for r in v:duprows.append({'group':i,'sha256':h,'bytes':r['bytes'],'path':r['path'],
            'git_status':r['git_status'],'protected':bool(r['protection']),
            'different_filename':len({Path(x['path']).name for x in v})>1})
    csvout('exact_duplicates.csv',duprows)
    collisions=[{'filename':name,'paths':json.dumps([r['path'] for r in v],ensure_ascii=False),
        'different_hashes':len({r['sha256'] for r in v})} for name,v in names.items() if len({r['sha256'] for r in v})>1]
    csvout('same_name_different_content.csv',collisions,['filename','paths','different_hashes'])
    # ZIP member and slide timing inspection does not exercise the Office runtime.
    media=[]; texedges=[]
    for r in hrows:
        rel=r['path'];p=ROOT/rel
        if runtime(rel):continue
        if r['extension'] in {'.pptx','.zip'}:
            item={'path':rel,'sha256':r['sha256']}
            try:
                with zipfile.ZipFile(p) as z:
                    item['bad_crc_member']=z.testzip(); item['members']=len(z.namelist())
                    item['uncompressed_bytes']=sum(x.file_size for x in z.infolist())
                    if r['extension']=='.pptx':
                        slides=[x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)]
                        item['slide_count']=len(slides);item['timing_slides']=0;item['effects']=0;item['broken_shape_targets']=[]
                        ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
                        for s in slides:
                            root=ET.fromstring(z.read(s)); ids={n.attrib['id'] for n in root.findall('.//p:cNvPr',ns)}
                            item['timing_slides']+=root.find('p:timing',ns) is not None
                            item['effects']+=len(root.findall('.//p:cTn[@presetID]',ns))
                            for n in root.findall('.//p:spTgt',ns):
                                if n.attrib.get('spid') not in ids:item['broken_shape_targets'].append({'slide':s,'spid':n.attrib.get('spid')})
                        item['desktop_no_repair']='NOT_VERIFIED';item['animation_runtime']='NOT_VERIFIED'
            except Exception as e:item['error']=str(e)
            media.append(item)
        if r['extension']=='.pdf':
            item={'path':rel,'sha256':r['sha256']}
            try:
                import pymupdf
                with pymupdf.open(p) as d:
                    item['pages']=len(d);item['can_extract_all_pages']=all(isinstance(x.get_text(),str) for x in d)
            except Exception as e:item['error']=str(e)
            media.append(item)
        if r['extension']=='.tex' and rel in corpus:
            for kind,target in re.findall(r'\\(input|include|includegraphics|bibliography)(?:\[[^\]]*\])?\{([^}]+)\}',corpus[rel]):
                for token in target.split(','):
                    opts=[p.parent/token,ROOT/token,ROOT/'report'/token]
                    suff=[''] if Path(token).suffix else ['','.tex'] if kind in {'input','include'} else ['','.bib'] if kind=='bibliography' else ['','.pdf','.png','.jpg','.svg']
                    found=next((str(q.with_suffix(q.suffix+s).relative_to(ROOT)).replace('\\','/') for q in opts for s in suff if q.with_suffix(q.suffix+s).is_file()),'')
                    texedges.append({'source':rel,'kind':kind,'target':token,'resolved':found})
    dump('artifact_inspection.json',media);csvout('latex_dependencies.csv',texedges,['source','kind','target','resolved'])
    # Safe candidates are limited to untracked, reproducible caches outside protected areas.
    candidates=[]; dependency=[]
    cache_names={'__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.ipynb_checkpoints'}
    for r in hrows:
        rel=r['path']; parts=Path(rel).parts
        if any(x in cache_names for x in parts) and not r['protection'] and r['git_status']!='tracked':
            rr=refs(rel); dependency.extend({'target':rel,**x} for x in rr)
            candidates.append({**{k:r[k] for k in ['path','absolute_path','bytes','sha256','git_status']},
                'group':'A_CACHE','action':'DELETE' if not rr else 'REVIEW','reason':'Generated cache; original source retained',
                'replacement':'Regenerate with original tools/environment','dependency_check':'literal full path + filename scan',
                'reference_count':len(rr),'irrecoverable_data':'no research data identified; cache only',
                'risk':'LOW' if not rr else 'REVIEW','estimated_reclaim_bytes':r['bytes'] if not rr else 0})
        if r['extension']=='.pdf' and re.search(r'REVISION_V[2-5]\.pdf$',rel):
            rr=refs(rel);dependency.extend({'target':rel,**x} for x in rr)
            candidates.append({**{k:r[k] for k in ['path','absolute_path','bytes','sha256','git_status']},
                'group':'B_OLD_REPORT_EXPORT','action':'REVIEW','reason':'V7 accepted; cached origin/main already deletes V2-V5; preserve source/QA',
                'replacement':'presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf',
                'dependency_check':'literal full path + filename scan; incoming Git diff inspected','reference_count':len(rr),
                'irrecoverable_data':'tracked PDF recoverable from recorded HEAD; historical source retained',
                'risk':'MEDIUM: resolve doc/QA references and remote baseline first','estimated_reclaim_bytes':0})
    csvout('deletion_candidates.csv',candidates,['path','absolute_path','bytes','sha256','git_status','group','action','reason','replacement','dependency_check','reference_count','irrecoverable_data','risk','estimated_reclaim_bytes'])
    csvout('candidate_dependencies.csv',dependency,['target','source','match'])
    protected=[r for r in hrows if r['protection']]
    csvout('protected_files.csv',({'path':r['path'],'sha256':r['sha256'],'bytes':r['bytes'],'reason':r['protection']} for r in protected))
    # Renaming is a separate reviewable proposal; no automatic provenance migration.
    rename=[]
    for r in hrows:
        rel=r['path']
        if runtime(rel) or not re.search(r'(?i)(?:^|[/_ -])(?:p\d{1,2}|phase[_ -]?\d{1,2})(?:[_ -]|$)',rel):continue
        if r['extension'] not in {'.md','.py','.ps1','.ipynb','.json','.csv','.tex'}:continue
        rename.append({'path':rel,'extension':r['extension'],'action':'KEEP' if r['protection'] else 'REVIEW',
            'reason':r['protection'] or 'Need complete caller, checksum, generated-output and replacement mapping before rename'})
    csvout('phase_name_review.csv',rename,['path','extension','action','reason'])
    total=sum(r['bytes'] for r in rows); stats=collections.Counter(r['git_status'] for r in rows)
    top=[(k,v[0],human(v[1])) for k,v in sorted(sums.items(),key=lambda x:-x[1][1]) if '/' not in k]
    md('01_INVENTORY.md',[
        '# Kiểm kê workspace — chỉ đọc',f'Đo lúc {STAMP}. Root: `{ROOT}`.',
        f'{len(rows):,} file; {len(dirs):,} thư mục; {total:,} bytes ({human(total)}) gồm `.git`. Không tính file audit mới tạo.',
        'Dung lượng là tổng logical bytes; không đồng nghĩa allocated disk space. Không có thao tác giải phóng dung lượng.',
        f'Git index: {len(tracked):,}; untracked: {len(untracked):,}; ignored: {len(ignored):,}. File trong .git được thống kê riêng.',
        *table(['Nhóm','File','Dung lượng'],top),
        '## File lớn nhất',*table(['Đường dẫn','Dung lượng','Git'],[(r['path'],human(r['bytes']),r['git_status']) for r in sorted(rows,key=lambda x:-x['bytes'])[:35]]),
        '## Loại file (không gồm .git)',*table(['Đuôi','File','Dung lượng'],[(k,v[0],human(v[1])) for k,v in sorted(ext.items(),key=lambda x:-x[1][1])]),
        '## Git',f"HEAD `{gs['head']['stdout'].strip()}`; cached origin/main `{gs['origin_main_cached']['stdout'].strip()}`.",
        f"Live remote check: `{gs['remote_main_live']['stdout'].strip()}` (exit {gs['remote_main_live']['code']}).",
        f"Ahead/behind: `{gs['ahead_behind_cached']['stdout'].strip()}`; không fetch/pull/merge/push.",
        '```',gs['status']['stdout'],gs['branches']['stdout'],gs['incoming_changes']['stdout'],'```',
        'Xem git_snapshot.json (history, LFS, objects, remote errors), inventory.csv, directory_sizes.csv; .gitignore và toàn bộ workflow đã đưa vào tập phân tích tham chiếu.',
        f'Hash/read errors: {len(ERRORS)}; reparse points không duyệt: {len(links)}. Xem summary.json.',
        f'STATE manifest: {dict(collections.Counter(x["status"] for x in reconcile))}. Mismatch/missing là reconciliation finding, không sửa bằng cách chạy lại nghiên cứu.',
        'Snapshot Git lấy trước thay đổi cấu hình hiển thị trong lượt audit nếu có; đối chiếu final_validation.json khi duyệt.' ])
    md('02_DUPLICATES.md',[
        '# SHA-256 và phân biệt phiên bản',
        f'Hash {sum(bool(r["sha256"]) for r in hrows):,}/{len(hrows):,} file ngoài .git, gồm data/model dưới dạng opaque bytes, môi trường và cache. Không deserialize model hoặc đọc hàng dữ liệu.',
        f'{len(duplicate_groups):,} nhóm exact SHA-256 duplicate; {len(collisions):,} nhóm cùng tên khác hash. Chi tiết đầy đủ trong exact_duplicates.csv và same_name_different_content.csv.',
        'Hash trùng không cấp phép xóa: runtime có file giống nhau nhưng nằm trong các package bắt buộc; snapshot scientific có provenance riêng.',
        '## Nhóm duplicate lớn nhất',*table(['SHA-256','Bytes mỗi file','Các bản sao'],[(h,v[0]['bytes'],'; '.join(x['path'] for x in v)) for h,v in sorted(duplicate_groups,key=lambda x:-x[1][0]['bytes']*(len(x[1])-1))[:20]]),
        'PDF khác hash: đã trích xuất toàn bộ trang để xác nhận đọc được, không suy ra nội dung tương đương. PPTX: CRC/XML/slide/timing/shape targets trong artifact_inspection.json; không thay cho no-Repair và animation runtime.',
        'Video khác hash được giữ riêng cho từng phương pháp dựng/voice. Không coi preview, offline TTS, Neural hoặc native render tương đương chỉ vì 360s.',
        'Obsolete/generated export chỉ đề xuất REVIEW; file chưa rõ chức năng KEEP. Không có dedup thực thi.' ])
    canonical=[
        ['Báo cáo','V7: presentation/nckh_defense/creative_rebuild_v2/Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf','V1–V6: lịch sử/đầu vào; V2–V5 deleted upstream','README + V7 source/invariants + PDF parse','PDF V2–V5 REVIEW; source/QA KEEP','Có: V6 và nguồn'],
        ['Nguồn V7','presentation/nckh_defense/creative_rebuild_v2/report_v7/source/; LaTeX_Revision_V7_Source.zip','report/ vẫn chứa V6 và chapters phụ thuộc','build_report.py, humanize_report.py, latex_dependencies.csv','KEEP nguồn và mọi dependency, cả file không mang nhãn V7','Có, ZIP + source'],
        ['PPTX 10 slide','Ứng viên chưa ổn định: script_first_v3/final_10_slide_v1/NCKH_Ensemble_IDS_10_Slides_Final.pptx','Không xác nhận thay thế 29/32 slide','README ghi Repair; XML không chứng minh no-Repair','KEEP tất cả cho đến desktop gate','Bắt buộc'],
        ['Creative V2','creative_rebuild_v2/NCKH_Ensemble_IDS_Creative_Final.pptx; 29 slide','Bản 32 slide gốc giữ để dự phòng','QA_Report.md ghi historical COM/render; fresh no-Repair chưa chứng nhận','KEEP','Có: bản gốc + ZIP'],
        ['Video Neural 10 slide','NCKH_Ensemble_IDS_10_Slides_Preview_NeuralVoice.mp4','Offline preview là fallback, không native animation equivalent','FINAL_HANDOFF.md + builder source','KEEP cả hai đến paired runtime QA','Có'],
        ['Video Creative V2/gốc','Mỗi MP4 giữ theo deck/source tương ứng','Không so bằng mtime/size','artifact_inspection.json + handoff + timeline','KEEP native silent/preview khi chưa chứng minh rebuild mất mát=0','Có'],
        ['Source train/TEST/model','src/, config/, results/, notebook/, scientific tools','Không có thay thế được cho phép trong cleanup','Protocol/frozen SHA + user constraint','KEEP, không rename hay sửa I/O','Giữ lịch sử'],
        ['Tên phase và Markdown','phase_name_review.csv phân loại KEEP/REVIEW','Không tự bỏ P* khỏi định danh provenance','Imports, outputs, checksum, workflow phụ thuộc','Đổi tên chỉ sau mapping đồng bộ riêng; chưa đổi','Giữ thông tin cốt lõi'],
    ]
    md('03_CANONICAL_VERSION_MATRIX.md',['# Ma trận phiên bản và nguồn hiện hành',
        'Chấp nhận nội dung V7 được kế thừa từ yêu cầu người dùng; trạng thái ổn định PowerPoint chưa được suy ra từ ngày tạo.',
        *table(['Artifact','Hiện hành/ứng viên','Bản trước','Bằng chứng','Có thể xóa?','Dự phòng'],canonical),
        'Không di chuyển source V7 khỏi presentation chỉ để đẹp cây thư mục: builder, bibliography, figures, report/ V6 và checksum có ràng buộc. Workspace GON hiện đủ các nhóm là bước tổ chức trước mắt.',
        'report/README.md và STATE/HANDOFF còn nhiều trạng thái cũ 37/47 trang hoặc pilot pending; current artifact/P21 validator phải được đối chiếu thay vì tin văn bản cũ.',
        'Source-to-export và dependency LaTeX: latex_dependencies.csv. Desktop no-Repair, animation, logo/font và video-frame correspondence vẫn là gate riêng.' ])
    md('04_PROTECTED_FILES.md',['# Danh sách bảo vệ trước dọn dẹp',
        f'{len(protected):,} file được liệt kê với đường dẫn, SHA-256 và lý do trong protected_files.csv; toàn bộ data/, results/, config/, .research_memory/, templates/, src/, notebook/, scientific scripts/tests mặc định KEEP.',
        'Bảo vệ toàn bộ UNSW/CIC raw, TRAIN/TEST, frozen P9/P15, P21 đủ 5 seed + aggregate, model/checkpoint, seed configs, leakage reports, manifest/checksum, scientific decision logs. Không sửa số liệu, không retrain/re-evaluate TEST.',
        'Bảo vệ báo cáo V7 + nguồn/bib/figure transitively cần thiết; các scientific snapshot trùng hash vẫn KEEP. Model không đổi tên, không load.',
        'Bảo vệ mọi PPTX/MP4 đến khi chứng nhận native desktop no-Repair, đủ nội dung/animation và backup hoạt động. Không tự coi PPTX 10 slide là canonical ổn định.',
        'Môi trường .venv-p15-local và các runtime vẫn KEEP: phải kiểm tra phiên bản/package và builder trước khi có đề xuất xóa cụ thể.',
        'templates/original có Word lock ~$ chưa commit: KEEP, có thể đang được Word sử dụng; không coi là rác để xóa.',
        'Git objects/history không hash nội dung trong audit này và không được xóa/rewrite. protected_files.csv là baseline tại thời điểm audit, không phải yêu cầu thay checksum lịch sử.' ])
    deletes=[r for r in candidates if r['action']=='DELETE']; reviews=[r for r in candidates if r['action']=='REVIEW']
    md('05_DELETION_PLAN.md',['# Dry run — DỪNG TRƯỚC KHI XÓA',
        '**Chưa xóa, archive, di chuyển, đổi tên, commit hoặc push. Chỉ cấu hình hiển thị workspace được chỉnh theo yêu cầu bổ sung.**',
        f'Nhóm A: {len(deletes)} cache file đề xuất DELETE, {sum(r["bytes"] for r in deletes):,} bytes ({human(sum(r["bytes"] for r in deletes))}) logical bytes dự kiến. Chưa đo freed disk space.',
        f'Nhóm B/REVIEW: {len(reviews)} file; KHÔNG được chạy xóa cho tới khi giải quyết dependency/baseline và bạn duyệt đường dẫn cụ thể.',
        'Manifest thực thi tương lai: deletion_candidates.csv, mỗi dòng có full path, bytes, SHA-256, Git status, lý do, replacement, dependency scan, risk và tính phục hồi. Chỉ DELETE được duyệt mới được phép thực thi.',
        *table(['Nhóm','Hành động','Phạm vi','Điều kiện'],[
            ['A_CACHE','DELETE sau duyệt','Cache tái tạo, không tracked/protected','Rehash + Git + exact paths trước xóa'],
            ['B_OLD_REPORT_EXPORT','REVIEW','4 PDF V2–V5 đã bị xóa ở origin/main; local chưa pull','Phân biệt apply incoming commit với cleanup mới; sửa navigation nếu cần; giữ source/QA'],
            ['C_PRESENTATION','KEEP','Mọi PPTX, MP4, backup, source và delivery ZIP','No-Repair/animation/pairing chưa khép'],
            ['D_RESEARCH','KEEP','data/results/config/src/notebook/evidence/model','Không rename train/TEST I/O hoặc model'],
            ['E_ENVIRONMENT','KEEP','venv/runtime, logs/evidence chưa rõ','Không có chứng minh replacement/rebuild tương đương'],
            ['F_NAMES_AND_MD','KEEP/REVIEW','phase_name_review.csv + core docs','Không xóa MD cốt lõi; rename cần full mapping/callers/checksums'],
        ]),
        '## Các đường dẫn đề xuất',*table(['Action','Full path','Bytes','Git','Ref count'],[(r['action'],r['absolute_path'],r['bytes'],r['git_status'],r['reference_count']) for r in candidates]),
        f'Số tracked trong nhóm DELETE: {sum(r["git_status"]=="tracked" for r in deletes)}. Chưa có file biến mất khỏi GitHub do lượt này. Incoming upstream deletions được ghi riêng trong git_snapshot.json.',
        'Giảm logical working-tree bytes khác giảm Git history: xóa tracked file không thu hồi blob lịch sử; không rewrite hoặc force-push.',
        '## Giới hạn dependency audit',
        f'Đã đọc {len(corpus):,} file text project không nằm trong runtime/environment (<=6MB mỗi file); exact-path + basename matches lưu candidate_dependencies.csv. Có thể có dynamic path/external consumers: không kết luận unused chỉ vì zero match.',
        'Mọi rename/move source hoặc generated output ngoài cache còn REVIEW. Các link QA/manifest là evidence không được sửa như navigation thông thường.',
        '## Bước sau khi duyệt',
        'Chọn exact paths/group A đã duyệt; recheck Git user changes + hashes + workspace containment; tạo codex/cleanup-* và ghi HEAD/manifest; dùng git rm chỉ với tracked được duyệt; xóa local đúng file được duyệt; validate frozen/P21/report/links; commit cleanup riêng; push nhánh cleanup. Main cần duyệt cuối riêng.',
        'DELETED_FILES_MANIFEST.json và 06_CLEANUP_RESULTS.md chỉ tạo sau thực thi; không tạo kết quả giả khi chưa xóa.',
        'Bạn có thể duyệt nhóm A và giữ nguyên nhóm còn lại, hoặc yêu cầu xem xét thêm. Việc dùng workspace GON đầy đủ không cấp phép xóa.' ])
    dump('audit_errors.json',ERRORS)
    print(json.dumps({'files':len(rows),'bytes':total,'hashed':len(hashed),'duplicate_groups':len(duplicate_groups),
        'delete_candidates':len(deletes),'delete_logical_bytes':sum(r['bytes'] for r in deletes),'review':len(reviews),
        'protected':len(protected),'errors':len(ERRORS)},indent=2),flush=True)

if __name__=='__main__': main()
