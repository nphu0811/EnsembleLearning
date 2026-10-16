"""Assemble review content in original field order, without authoring a DOCX."""
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'proposal/researchwrite/nckh-ids'

def section(text,title):
    match=re.search(r'^## '+re.escape(title)+r'\n(.*?)(?=^## |\Z)',text,re.M|re.S)
    if not match:raise ValueError(title)
    return match[1].strip()

def namespace(text,prefix):
    return re.sub(r'\[([NLDS]\d+[^\]]*)\]',lambda m:'['+prefix+':'+m[1]+']',text)

def main():
    out=P/'drafts/De_cuong_noi_dung_review_r04.md'
    if out.exists():raise FileExistsError(out)
    m=(P/'drafts/sections/muc_tieu_noi_dung_phuong_phap_r02.md').read_text(encoding='utf-8')
    t=(P/'drafts/sections/tong_quan_luan_cu_r04.md').read_text(encoding='utf-8')
    product=(P/'drafts/sections/ung_dung_san_pham_tien_do_r03.md').read_text(encoding='utf-8')
    sm=lambda title:namespace(section(m,title),'M')
    st=lambda title:namespace(section(t,title),'T')
    sp=lambda title:namespace(section(product,title),'P')
    text='''# Đề cương NCKH2026 — gói nội dung phục vụ review r04

Đây là bản nội dung Markdown được ghép theo thứ tự trường của DOCX gốc; chưa điền DOCX, chưa render và chưa đủ điều kiện nộp. Hồ sơ đang phục hồi từ nghiên cứu đã có kết quả; tác giả/GVHD cần xác nhận tính chấp nhận. Không có phê duyệt hồi tố hoặc chữ ký do AI xác nhận. Các nhãn M/T/P giúp tách resolver nguồn của từng phần soạn, chưa là bibliography numbering cuối.

## Thông tin đầu biểu mẫu

Mẫu2: Đề cương đề tài NCKH của sinh viên. Đơn vị/địa danh trong header mẫu: [CẦN XÁC NHẬN tính áp dụng]; ngày/tháng/năm ký: [CẦN XÁC NHẬN]. Không lấy tên hoặc vai trò in sẵn làm danh tính đã xác thực.

Tên đề tài: NGHIÊN CỨU ENSEMBLE LEARNING CHO BÀI TOÁN PHÁT HIỆN XÂM NHẬP MẠNG.

Mã số đề tài: [CẦN XÁC NHẬN]. Thuộc lĩnh vực KHCN: [CẦN XÁC NHẬN mã/tên lĩnh vực hành chính].

## Mục tiêu, nội dung và kết quả

### Mục tiêu

'''+sm('Mục tiêu')+'\n\n### Nội dung\n\n'+sm('Nội dung nghiên cứu')+'\n\nPhương pháp và giới hạn diễn giải (nội dung bổ sung trong vùng Nội dung, không phải nhãn mới của form gốc):\n\n'+sm('Phương pháp và phạm vi diễn giải')+'\n\n### Kết quả\n\n'+sm('Kết quả đã có và sản phẩm cần hoàn thiện')+'''

## Đơn vị, chủ trì, người tham gia và hướng dẫn

- Đơn vị chủ trì: [CẦN XÁC NHẬN tính áp dụng tên đơn vị trong mẫu].
- Đơn vị phối hợp (nếu có): [CẦN XÁC NHẬN có hay không và thông tin].
- Chủ trì: họ tên [CẦN XÁC NHẬN]; MSSV [CẦN XÁC NHẬN]; lớp [CẦN XÁC NHẬN]; điện thoại [CẦN XÁC NHẬN].
- Người tham gia: số lượng, họ tên, MSSV và lớp từng người [CẦN XÁC NHẬN]. Không tự thêm thành viên hoặc xác nhận không có.
- Người hướng dẫn: họ tên, học hàm/học vị [CẦN XÁC NHẬN].

## Sơ lược tình hình nghiên cứu, điều tra trong nước, ngoài nước

'''+st('Luận cứ chọn đề tài')+'\n\n### Trong nước\n\n'+st('Sơ lược tình hình nghiên cứu trong nước')+'\n\n### Ngoài nước\n\n'+st('Sơ lược tình hình nghiên cứu ngoài nước')+'\n\nTổng hợp luận cứ và giới hạn (đoạn kết trong vùng tổng quan):\n\n'+st('Khoảng thiếu bằng chứng và vị trí của đề tài')+'\n\n## Nhu cầu thực tế và khả năng áp dụng kết quả đề tài\n\n'+sp('Nhu cầu thực tế và khả năng áp dụng kết quả đề tài')+'\n\n## Sản phẩm giao nộp; kết quả, sản phẩm\n\n'+sp('Sản phẩm giao nộp và tiêu chí chất lượng')+'''

Vùng yêu cầu kỹ thuật dạngI: chưa đề xuất sản phẩm dạngI; bảo toàn bảng gốc và [CẦN XÁC NHẬN cách ghi không áp dụng]. Không xóa nhãn hoặc ghi sản phẩm thiết bị/vật liệu không có căn cứ. Các tiêu chí dạngII/III ở bảng trên là đề xuất nội dung, chưa là kết quả nghiệm thu.

## Tiến độ thực hiện các nội dung

'''+sp('Tiến độ thực hiện các nội dung')+'\n\n## Các khoản chi phí\n\n'+sp('Kinh phí và phần xác nhận')+'''

Khi điền DOCX, giữ các dòng xét duyệt đề cương, nhân công chuyên đề1/chuyên đề2, viết báo cáo, hội thảo, nghiệm thu; giữ ô tiền đang trống và ghi chú nguồn kinh phí trong mẫu. Chưa có căn cứ điền thêm số tiền hoặc xác nhận đã chi.

## Vùng chữ ký của mẫu

Chủ trì đề tài (ký và ghi rõ họ tên): [CẦN XÁC NHẬN]. Đơn vị chủ trì/người đại diện/chức danh: [CẦN XÁC NHẬN]. Giáo viên hướng dẫn (ký và ghi rõ họ tên): [CẦN XÁC NHẬN]. Chữ ký do người có thẩm quyền thực hiện; bản này không có chữ ký hoặc xác nhận hành chính.

## Resolver nguồn nội bộ cho review

Nguồn M (mục tiêu/nội dung/phương pháp):

'''+namespace(section(m,'Nguồn dùng trong dự thảo'),'M')+'\n\nNguồn T (tổng quan):\n\n'+namespace(section(t,'Nguồn và reading boundary'),'T')+'\n\nNguồn P (sản phẩm/tiến độ):\n\n'+namespace(section(product,'Nguồn nội bộ phục vụ review — không phải danh mục trích dẫn cuối'),'P')+'\n\n### Metadata các bài được viện dẫn\n\n'
    with (ROOT/'literature/resume_r04_2026_10_16/legacy_verification_ledger.csv').open(encoding='utf-8-sig') as f:
        ledger={r['id']:r for r in csv.DictReader(f)}
    used=['L01','L02','L04','L05','L06','L07','L08','L09','L11','L12']
    for key in used:
        r=ledger[key]
        text+=f"- {key}: {r['authors']}. {r['title']}. {r['container']}, {r['year']}; {r['volume']}({r['issue']}): {r['pages_or_article']}. DOI: {r['doi']}.\n"
    text+='\nD01/D02 là thông báo/tóm tắt luận án theo source types vàURLs trong resolver T, không được gọi là journal articles. Full field audit: template_audit_r04/field_coverage.csv. G5 vẫn mở.\n'
    text=text.replace('NCKH2026','NCKH 2026').replace('Mẫu2','Mẫu 2').replace('dạngI','dạng I').replace('dạngII/III','dạng II/III').replace('chuyên đề1','chuyên đề 1').replace('chuyên đề2','chuyên đề 2')
    out.write_text(text,encoding='utf-8')
    checks=dict(original_order=text.index('### Mục tiêu')<text.index('## Đơn vị,')<text.index('### Trong nước')<text.index('### Ngoài nước')<text.index('## Nhu cầu')<text.index('## Tiến độ')<text.index('## Các khoản'),admin_placeholders=text.count('[CẦN XÁC NHẬN')>=15,domestic_labels_kept='### Trong nước' in text and '### Ngoài nước' in text,report_copies='03 quyển' in text,CD_conditions='trang bìa như bản cứng' in text and 'Hội đồng khoa học Khoa' in text,no_pagination_conflict_reference='- L03:' not in text,used_refs_verified=all(ledger[k]['metadata_status']=='VERIFIED_METADATA' for k in used),coverage_validation=json.loads((P/'template_audit_r04/validation.json').read_text(encoding='utf-8'))['passed'],explicit_non_docx='chưa điền DOCX' in text,retrospective='phục hồi từ nghiên cứu đã có kết quả' in text)
    (P/'qa_logs/r04_assembly_validation.json').write_text(json.dumps(dict(checks=checks,passed=all(checks.values()),scope='Content/order/source coverage only; full-content review separate; no form/render/admin pass'),indent=2),encoding='utf-8')
    print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),output=out.relative_to(ROOT).as_posix())))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
