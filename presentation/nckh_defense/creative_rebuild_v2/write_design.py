from pathlib import Path
from creative_content import MAIN
O=Path(__file__).resolve().parent
(O/'Creative_Direction.md').write_text('''# Creative Direction

## Ba bản thử có artifact thật
Concept_A.pptx/mp4: typography/fieldcream+coral, số−142/+118, nativefly/wipe/scale. Concept_B.pptx/mp4: graph/packetpath, nềnink; nodeactivation vàpacket chạy trong cùngslide. Concept_C.pptx/mp4: fieldviolet, gianttype, vòng dịch/chuyểnscale. Mỗi clip9s, mockup là PowerPointPNG riêng; không dùng bộ ảnh thayclip.

| Concept | Sáng tạo | Hiểu nội dung | Chiếu phòng thi | Motion thật | Học thuật | 6phút |
|---|---|---|---|---|---|---|
| A Editorial Research | Chữ và số rất nổi | Tốt nhất cho bằng chứng | Tương phản tốt | Internal timeline | Phù hợp số liệu | Dễ giữ nhịp |
| B Kinetic Cyber Systems | Luồng dữ liệu có cơ chế | Tốt cho architecture | Nét cần đủ sáng | Packet motionpath/node | Phải ghi minh họa offline | Cần cue fit/infer |
| C Experimental Motion Identity | Hình học mạnh | Dễ thành trang trí | Mảng màu nổi | Move/scale thật | Dùng cho mở/chốt | Dùng hạn chế |

Chọn A+B; lấy colorarc củaC ởscenechốt. Không giữ bố cụcdeckcũ. Motif: một bản ghi chuyển qua hệ thống, sau đó tách thành hai loại lỗi. Chữhero48–185pt, body21–30pt; Arial/Aptos/Consolas hỗ trợViệt. Màu:ink#10162F,cream#F8F5EE,cyan#24C3D9,coral#FF7058,lime#C5F66A,violet#7958F5. Khônggradient. SceneFNcoral/chữink;sceneP21cream/violetđểphânbiệtTEST.

Đánh giá trên là tự phản biện thiết kế, không phải điểm của hội đồng. NativePowerPointtimeline làpipelinechính; khôngnhúngvideoManimvàkhônglấywebscreenshotlàmslide. ReferenceLollypopbịCAPTCHA,giớihạnđãghirõởDesign_Reference_Study.md.
''',encoding='utf-8')
motion={'hook':'Fly hero và packet; nhịp câu hỏi','traffic':'Network graph: path drawing, node activation, packet cycles, Normal/Attack labels','data':'Typography TRAIN/TEST và progressive reveal','features':'Cột identifier/target gạch/dịch;42 biến và vector tạo tuần tự','infer':'Feature vector fan-out LR/DT/RF, bộ gộp, hai đầu ra','oof':'3lượt fold học/giữ, ghép OOF matrix, fit metaLR','forest':'Cây bootstrap vector, packet hội tụ','vote':'3 learner → luật gộp cố định, reveal Hard/Soft','stack':'Base đã học → xác suất → meta, packet suy luận','score':'Hai F1, Δ và CI chứa0','fp':'Thanh FP0–11000 grow, giảm142','fn':'Kinetic+118, thanh FN0–1000 grow','matrix':'5seed×5arm activation→1validation chung','selection':'Selector+RF17 stackbar so RF42fit;F1giảm','rates':'FPR/FNR scatter, Balanced/Oversample reveal theo cue','loss':'Ba cột r=1, r=142/118, r=5; bars cùng thang, hiện theo bước','close':'Typography kết luận, cue đóng góp/giới hạn/dữ liệu mới'}
lines=['# Storyboard Cinematic','17slide chính,8cảnh/360s;12phụlụcẩn. Mỗi slide chính có internal timeline. Transitionnone, không dựa vào page transition để giả animation.','|Slide|Cảnh|Slot|Thông điệp|Motion|','|---|---:|---|---|---|']
t=0
for i,(s,d,v,title,speech) in enumerate(MAIN,1):
 lines.append(f'|{i}|{s}|{t//60:02}:{t%60:02}–{(t+d)//60:02}:{(t+d)%60:02}|{title.replace(chr(10)," ")}|{motion[v]}|');t+=d
(O/'Storyboard_Cinematic.md').write_text('\n\n'.join(lines),encoding='utf-8')
print('DESIGN_AND_STORYBOARD_SAVED',t)
