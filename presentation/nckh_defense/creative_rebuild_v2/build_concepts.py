from pathlib import Path
from motion_engine import *
O=Path(__file__).resolve().parent;D=O/'concepts';D.mkdir(exist_ok=True)

d=Deck();d.page(1,9,CREAM,'Editorial Research',tag='CONCEPT A / EDITORIAL RESEARCH',source='Official TEST lịch sử · Stacking42 so với RF42 · minh họa thiết kế bằng dữ liệu thật')
d.rect(8.7,0,4.64,7.5,CORAL)
n=d.title('BỚT\nCẢNH BÁO.',.55,1.0,8.0,2.4,72);d.anim(n,'fly',0,.8)
n=d.text('−142',.45,3.6,7.8,2.2,150,INK,True,'Arial');d.anim(n,'wipe',1.2,1.2)
n=d.text('+118',8.95,2.05,4.1,1.8,96,INK,True,'Arial');d.anim(n,'fly',3,.8);d.pulse(n,4,1.2,2,107)
d.text('BỎ SÓT THÊM',9.0,3.75,3.7,.7,27,INK,True)
d.text('FP giảm. FN tăng.',.6,6.2,7.2,.6,30,INK)
d.save(D/'Concept_A.pptx');native_render(D/'Concept_A.pptx',video=D/'Concept_A.mp4',render_dir=D/'A_renders')

d=Deck();d.page(1,9,INK,'Kinetic Cyber Systems',tag='CONCEPT B / KINETIC CYBER SYSTEMS',source='Sơ đồ vector minh họa traffic; không phải mạng đã triển khai hoặc trace đo được')
d.title('MỘT FLOW.\nNHIỀU QUYẾT ĐỊNH.',.6,1.0,8.6,1.9,55)
nodes=[(1.0,4.1),(2.6,3.4),(2.8,5.3),(4.9,4.5),(7.4,3.6),(7.7,5.4),(10.4,4.5),(12.0,3.3)]
for j,(x,y) in enumerate(nodes):
 for k in range(j+1,min(j+3,len(nodes))):
  xx,yy=nodes[k];n=d.line(x,y,xx,yy,DARKGRAY,1.7);d.anim(n,'wipe',j*.12,.7)
 n=d.ring(x,y,.2,CYAN);d.anim(n,'fade',j*.15,.35);d.pulse(n,.7+j*.2,1.2,2)
for j in range(8):
 x,y=nodes[j%7];xx,yy=nodes[(j%7)+1];d.packet(x,y,xx,yy,1+j*.35,1.8,2,LIME if j%2 else CYAN)
d.text('Luồng dữ liệu đi qua mô hình,\nkhông đi qua một ảnh minh họa.',.65,6.05,11.9,.8,24,CREAM)
d.save(D/'Concept_B.pptx');native_render(D/'Concept_B.pptx',video=D/'Concept_B.mp4',render_dir=D/'B_renders')

d=Deck();d.page(1,9,VIOLET,'Experimental Motion Identity',tag='CONCEPT C / EXPERIMENTAL MOTION IDENTITY',source='142 /118 là hiệu số lỗi official TEST lịch sử; hình học không đại diện metric độc lập')
d.text('SAI\nỞ ĐÂU?',.55,1.15,8.7,3.3,110,CREAM,True,'Arial')
for j in range(3):
 n=d.ring(10.0,3.7,1.1+j*.38,LIME);d.move(n,-.7-j*.15,.1*j,0,6);d.pulse(n,0,2,2,115)
n=d.rect(8.95,2.8,2.1,2.1,CORAL,kind=MSO_SHAPE.DIAMOND);d.move(n,.3,.5,1,5)
d.text('FP / FN',8.5,5.8,3.7,.6,31,CREAM,True,'Consolas')
n=d.text('Mỗi quyết định đều có chi phí.',.65,5.75,7.5,.8,28,CREAM);d.anim(n,'wipe',2,.8)
d.save(D/'Concept_C.pptx');native_render(D/'Concept_C.pptx',video=D/'Concept_C.mp4',render_dir=D/'C_renders')
print('THREE_REAL_NATIVE_CONCEPT_CLIPS_READY',flush=True)
