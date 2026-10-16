"""Read all original OOXML blocks/cells and map content without editing DOCX."""
import csv
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'proposal/researchwrite/nckh-ids'
OUT=P/'template_audit_r04'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def words(element):
    return ''.join(x.text or '' for x in element.findall('.//w:t',NS))

def main():
    OUT.mkdir(exist_ok=False)
    original=ROOT/'templates/original/Mau-De-cuong-NCKH-Sinh-vien-2026-7-trieu.docx'
    before=hashlib.sha256(original.read_bytes()).hexdigest()
    with zipfile.ZipFile(original) as archive:
        assert archive.testzip() is None
        tree=ET.fromstring(archive.read('word/document.xml'))
    body=tree.find('w:body',NS)
    entries=[]
    for i,element in enumerate(body):
        item=dict(body_index=i,type=element.tag.rsplit('}',1)[-1],text=words(element),rows=[])
        for ri,row in enumerate(element.findall('w:tr',NS)):
            item['rows'].append([dict(cell_index=ci,text=words(cell)) for ci,cell in enumerate(row.findall('w:tc',NS))])
        entries.append(item)
    (OUT/'original_body_snapshot.json').write_text(json.dumps(dict(source=original.relative_to(ROOT).as_posix(),sha256=before,blocks=entries),indent=2,ensure_ascii=False),encoding='utf-8')
    method='proposal/researchwrite/nckh-ids/drafts/sections/muc_tieu_noi_dung_phuong_phap_r02.md'
    lit='proposal/researchwrite/nckh-ids/drafts/sections/tong_quan_luan_cu_r04.md'
    products='proposal/researchwrite/nckh-ids/drafts/sections/ung_dung_san_pham_tien_do_r03.md'
    groups=[
      ([0,1,5],'Header/date/institution','[CẦN XÁC NHẬN] date and institutional applicability','AUTHOR_INPUT_NEEDED','docs/TEMPLATE_REQUIREMENTS_MATRIX.md'),
      ([8],'Topic','Nghiên cứu Ensemble Learning cho bài toán phát hiện xâm nhập mạng','CONTENT_DRAFT',method),
      ([9,10],'Code/scientific field','[CẦN XÁC NHẬN] official code/field','AUTHOR_INPUT_NEEDED','docs/TEMPLATE_REQUIREMENTS_MATRIX.md'),
      ([11,12,13,14],'Objectives','Mục tiêu + frozen RQ resolver','CONTENT_DRAFT',method),
      ([15,16,17],'Research content/methods','Nội dung nghiên cứu; Phương pháp và phạm vi diễn giải','CONTENT_DRAFT',method),
      ([18,19,20],'Results','Kết quả đã có và sản phẩm cần hoàn thiện; preserve pending status','CONTENT_DRAFT',method),
      ([21,22,23,24,25,26,27,28,29,30,31,32],'Unit/cooperation/leader/members/advisor','[CẦN XÁC NHẬN] identities,roles,phone,units;no sample identity copying','AUTHOR_INPUT_NEEDED','docs/TEMPLATE_REQUIREMENTS_MATRIX.md'),
      ([33,34],'Research context','Luận cứ chọn đề tài','CONTENT_DRAFT',lit),
      ([35,36],'Domestic research','Sơ lược tình hình nghiên cứu trong nước','CONTENT_DRAFT',lit),
      ([37,38],'International research','Sơ lược tình hình nghiên cứu ngoài nước; bounded gap','CONTENT_DRAFT',lit),
      ([39,40,41],'Need/application','Offline research prototype; model dependency and no deployment claim','CONTENT_DRAFT',products),
      ([42,43],'Product classes I/II/III','Proposed III;official ticks require confirmation;preserve all source cells','AUTHOR_INPUT_NEEDED',products),
      ([44,45],'Result product quantity','Report03 copies per source;applicability pending','AUTHOR_INPUT_NEEDED',products),
      ([46,47],'Type I technical criteria','No TypeI product proposed;keep original table;[CẦN XÁC NHẬN] applicability','AUTHOR_INPUT_NEEDED',products),
      ([48,49],'TypeII/III science/quality','CD/report cover/article revision/software02A4 conditions kept','CONTENT_DRAFT',products),
      ([50,51],'Schedule','4/11/11/4 weeks per form;retrospective status explicit;no dates invented','AUTHOR_INPUT_NEEDED',products),
      ([52,53],'Budget','3m+3.5m+0.5m=7m;blank monetary cells and source notes preserved','AUTHOR_INPUT_NEEDED',products),
      ([55],'Signatures','[CẦN XÁC NHẬN];no signing/sample names treated as identity','AUTHOR_INPUT_NEEDED','docs/TEMPLATE_REQUIREMENTS_MATRIX.md'),
    ]
    mapping={i:dict(group=label,planned_content=content,status=status,content_source=source) for ids,label,content,status,source in groups for i in ids}
    rows=[]
    for entry in entries:
        i=entry['body_index']
        if i not in mapping:
            if entry['text'].strip():
                raise ValueError('Unmapped nonempty block '+str(i))
            mapping[i]=dict(group='Layout/empty/section properties',planned_content='Preserve structural block in future DOCX copy',status='STRUCTURE_PRESERVE',content_source='docs/TEMPLATE_REQUIREMENTS_MATRIX.md')
        rows.append(dict(body_index=i,source_type=entry['type'],source_text=entry['text'],**mapping[i]))
    with (OUT/'field_coverage.csv').open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    compact=lambda i:entries[i]['text'].replace(' ','')
    checks=dict(all_body_blocks_mapped=len(rows)==len(body),all_nonempty_mapped=all(e['body_index'] in mapping for e in entries if e['text'].strip()),eight_tables=sum(e['type']=='tbl' for e in entries)==8,content_sources_exist=all((ROOT/r['content_source']).is_file() for r in rows),budget_source_3m='3.000.000' in compact(53),budget_source_3_5m='3.500.000' in compact(53),budget_source_0_5m='500.000' in compact(53),budget_source_7m='7.000.000' in compact(53),report_03='03' in compact(45),software_02_A4='02trangA4' in compact(49),CD_cover='trangbìanhưbảncứng' in compact(49),article_council='HộiđồngkhoahọcKhoa' in compact(49),schedule=all(x+'tuần' in compact(51) for x in ['4','11']),original_unchanged=hashlib.sha256(original.read_bytes()).hexdigest()==before)
    result=dict(checks=checks,passed=all(checks.values()),body_blocks=len(rows),table_cells=sum(len(row) for e in entries for row in e['rows']),source_sha256=before,scope='Read-only original OOXML and planned content coverage; not filled DOCX, render, official field confirmation or final G5')
    (OUT/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),blocks=len(rows),cells=result['table_cells'])))
    if not result['passed']:raise SystemExit(1)

if __name__=='__main__':main()
