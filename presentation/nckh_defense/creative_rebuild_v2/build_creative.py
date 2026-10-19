from pathlib import Path
import json,sys,math,importlib.util
from motion_engine import *
from creative_content import MAIN
O=Path(__file__).resolve().parent;ROOT=O.parents[2]
d=Deck()
def caption(t,x=.6,y=6.25,w=12,size=22,color=None):return d.text(t,x,y,w,.65,size,color)
def rail(x,y,w,color,at):
 n=d.line(x,y,x+w,y,color,2,True);d.anim(n,'wipe',at,.8);return n
def number(n,x,y,w,size=120,color=None,name=None):return d.text(n,x,y,w,2.0,size,color,True,'Arial',name)
def circular_node(label,x,y,color,at=0,r=.47):
 n=d.ring(x,y,r,color);d.anim(n,'fade',at,.4)
 q=d.text(label,x-r-.15,y-.18,2*r+.3,.4,17,color,True,'Consolas',align=PP_ALIGN.CENTER);d.anim(q,'fade',at+.2,.4)
 return n
def network(dur):
 nodes=[(.8,3.6),(1.7,2.4),(2.1,5.3),(3.5,3.3),(4.7,5.1),(5.5,2.9),(7,4),(8.9,3),(9.4,5),(11.3,3.8),(12.3,2.3)]
 edges=[(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,6),(5,6),(6,7),(6,8),(7,9),(8,9),(9,10)]
 for j,(a,b) in enumerate(edges):
  x,y=nodes[a];xx,yy=nodes[b];n=d.line(x,y,xx,yy,DARKGRAY,1.4);d.anim(n,'wipe',.25+j*.08,.7)
 for j,(x,y) in enumerate(nodes):
  n=d.ring(x,y,.14,CYAN if j%3 else LIME);d.anim(n,'fade',.3+j*.1,.5)
  d.pulse(n,1+j*.15,1.8,3,125)
 for j,(a,b) in enumerate(edges):
  x,y=nodes[a];xx,yy=nodes[b];d.packet(x,y,xx,yy,1.7+(j%4)*.55,2.1,7,CYAN if j%2 else CORAL,f'network-packet-{j}')
 return nodes

for i,(scene,sec,view,title,speech) in enumerate(MAIN,1):
 bg={'hook':INK,'traffic':INK,'data':CREAM,'features':CREAM,'infer':INK,'oof':CREAM,'forest':VIOLET,'vote':CREAM,'stack':INK,'score':CREAM,'fp':INK,'fn':CORAL,'matrix':CREAM,'selection':INK,'rates':CREAM,'loss':INK,'close':LIME}[view]
 src='UNSW-NB15 · sơ đồ minh họa pipeline offline theo mã nguồn; không phải traffic triển khai'
 if scene==5:src='Official TEST lịch sử · 82.332 bản ghi · RF42 so với Stacking42 · ngưỡng 0,5'
 if scene in [6,7]:src='P21 hậu nghiệm trên TRAIN · 5 FIT seed · cùng 35.069 dòng internal validation'
 if view=='loss':src='Phân tích giả định · dự đoán official TEST lịch sử · L=FP+rFN · chỉ cặp RF42/Stacking42'
 if view=='close':src='NCKH Ensemble IDS · Dương Ngọc Phú / Phạm Thế Vỹ / Vũ Văn Kiên / Lê Hoàng Nguyên Quân · GVHD: TS. Lê Ngọc Hiếu'
 d.page(scene,sec,bg,title,speech,f'ENSEMBLE / IDS                         {view.upper()}',src)
 if view=='hook':
  d.text('Nghiên cứu Ensemble Learning\ncho phát hiện xâm nhập mạng',.6,.95,10,1,21,GRAY)
  for n,t,x,y,w,col in [('hook1','BỚT CẢNH BÁO.',.55,2.05,12,CREAM),('hook2','AN TOÀN HƠN?',.55,3.25,12,CORAL)]:
   a=d.text(t,x,y,w,1.3,65,col,True,'Arial',n);d.anim(a,'fly',.6 if n=='hook1' else 4.5,.85)
  n=number('?',10.2,4.5,2.3,115,LIME);d.pulse(n,8,1.7,3,112)
  caption('Một câu hỏi về cái giá của sai lầm.',.65,6.05,9,25)
  for j in range(3):d.packet(.8+j*.5,5.4,8+j*.5,5.4,1+j*1.8,3,4,CYAN)
 elif view=='traffic':
  d.title('MỘT BẢN GHI.  HAI KHẢ NĂNG.',.6,.9,12,1.15,45)
  network(sec)
  n=d.text('NORMAL',8.65,1.8,3,.4,21,LIME,True,'Consolas');d.anim(n,'fade',5,.5)
  n=d.text('ATTACK',9.1,5.4,3,.4,21,CORAL,True,'Consolas');d.anim(n,'fade',9,.5)
  caption('Sơ đồ minh họa flow và quyết định nhị phân.',.6,6.3,11,23)
 elif view=='data':
  d.title('DỮ LIỆU CỐ ĐỊNH.\nCÂU HỎI MỞ.',.55,1.05,8,2.0,54)
  d.rect(9.65,1.0,3.1,5.55,VIOLET)
  a=number('175.341',.55,3.75,8.8,93,INK);d.anim(a,'wipe',.5,1.1)
  d.text('dòng TRAIN chính thức',.65,5.25,8,.5,25)
  a=number('82.332',9.86,2.4,2.8,46,CREAM);d.anim(a,'fly',4,.9)
  d.text('TEST\nCHÍNH THỨC',9.94,3.55,2.5,1.0,23,CREAM,True)
  caption('RF là mốc tham chiếu. Voting / Stacking có cải thiện?',.65,6.25,12,22)
 elif view=='features':
  d.title('GIỮ GÌ\nCHO MÔ HÌNH?',.55,1,5.4,2.0,60)
  cols=[('id',CORAL),('label',CORAL),('attack_cat',CORAL),('proto',INK),('service',INK),('state',INK)]
  for j,(t,col) in enumerate(cols):
   y=1.15+j*.64;x=7.35
   a=d.text(t,x,y,4.7,.5,26,col,True,'Consolas',f'feature-label-{j}');d.anim(a,'fade',.6+j*.38,.35)
   if j<3:
    n=d.line(x-.1,y+.22,x+3.6,y+.22,CORAL,3);d.anim(n,'wipe',3.7+j*.8,.5);d.move(a,1.0,0,7+j*.45,.7)
   else:d.move(a,-.7,0,8+(j-3)*.8,.8)
  n=number('42',.65,3.55,4.5,130,VIOLET);d.anim(n,'fly',7.3,.9)
  d.text('predictor gốc',.8,5.45,5.1,.6,29)
  for j in range(14):
   a=d.rect(6.9+j*.35,5.55,.24,.6,CYAN if j%3 else VIOLET,name=f'vector-cell-{j}');d.anim(a,'wipe',10+j*.18,.5)
  caption('One-hot biến phân loại · Nhánh LR có chuẩn hóa',.65,6.45,12,22)
  for j in range(3):d.packet(6.5,5.82,12.3,5.82,13+j*.4,1.4,2,CYAN)
 elif view=='infer':
  d.title('KHI DỰ ĐOÁN',.55,.95,11,1.0,49)
  d.text('Một đường dữ liệu. Ba mô hình cơ sở.',.62,2.0,11,.55,25,GRAY)
  # Layers are circles, a learned decision surface and an output fork, not box chain.
  circular_node('x',1.15,4.3,CYAN,0,.35)
  d.text('feature\nvector',.65,5.0,1.8,.8,19,CYAN)
  for j,(lab,yy) in enumerate([('LR',3),('DT',4.3),('RF',5.6)]):
   a=d.line(1.5,4.3,4.0,yy,CYAN,2,True);d.anim(a,'wipe',.8+j*.4,.6)
   circular_node(lab,4.6,yy,CYAN,1.4+j*.4)
   a=d.line(5.15,yy,7.5,4.3,GRAY,1.6,True);d.anim(a,'wipe',3+j*.3,.7)
   for z in range(2):d.packet(1.6,4.3,4.4,yy,3.8+j*.5+z*.6,1.3,4,CYAN)
  a=d.rect(7.65,3.57,1.45,1.45,VIOLET,kind=MSO_SHAPE.DIAMOND);d.anim(a,'fade',4,.6)
  d.text('GỘP',7.83,4.05,1.1,.4,19,CREAM,True,align=PP_ALIGN.CENTER)
  for j,(lab,yy,col) in enumerate([('Normal',3.2,LIME),('Attack',5.35,CORAL)]):
   a=d.line(9.1,4.3,10.65,yy,col,2,True);d.anim(a,'wipe',6+j,.8)
   a=d.text(lab,10.75,yy-.3,2,.6,28,col,True);d.anim(a,'fade',7+j,.4)
   d.packet(9.2,4.3,10.6,yy,9+j*.6,1.3,6,col)
  caption('Các base learner và bộ gộp đã được fit; ngưỡng quyết định 0,5.',.65,6.5,12,21)
 elif view=='oof':
  d.title('META LEARNER HỌC TỪ\nDỰ ĐOÁN NGOÀI FOLD.',.55,.95,12,1.7,45)
  d.text('FIT BASE',.65,3.1,2,.4,19,VIOLET,True,'Consolas');d.text('OOF',7.35,3.1,2,.4,19,VIOLET,True,'Consolas');d.text('FIT META',10.3,3.1,2.5,.4,19,VIOLET,True,'Consolas')
  for row in range(3):
   for col in range(3):
    x=2.65+col*1.15;y=3.7+row*.75;held=row==col
    n=d.rect(x,y,1,.42,CORAL if held else VIOLET,name=f'fold-r{row}c{col}');d.anim(n,'wipe',row*3.6+.5+col*.15,.5)
    d.text('giữ' if held else 'học',x+.13,y+.05,.8,.3,14,CREAM,True,'Consolas')
   n=d.line(6.3,3.91+row*.75,7.6,3.91+row*.75,VIOLET,2,True);d.anim(n,'wipe',3.1+row*3.6,.6)
   for c in range(3):
    n=d.rect(7.85+c*.3,3.7+row*.75,.21,.42,VIOLET);d.anim(n,'fade',3.6+row*3.6+c*.15,.4)
  n=d.line(9.0,4.6,10.35,4.6,INK,2,True);d.anim(n,'wipe',12.2,.8)
  n=d.ring(11.1,4.6,.6,VIOLET);d.anim(n,'fade',13,.5);d.pulse(n,13.6,1,2,115)
  n=d.text('LR',10.8,4.38,1,.4,24,VIOLET,True,'Consolas');d.anim(n,'fade',13,.4)
  caption('Mỗi dòng OOF được dự đoán bởi mô hình chưa học dòng đó.',.65,6.15,12,24)
  d.text('P21 dùng inner grouped CV theo vector trùng; lịch sử dùng StratifiedKFold.',.65,6.7,12,.3,15,DARKGRAY)
 elif view=='forest':
  d.title('RỪNG ĐÃ LÀ\nMỘT ENSEMBLE.',.55,1,8.4,2.1,60)
  for j in range(7):
   x=1+j*1.65;y=4.0+(j%2)*.3
   pts=[(x,y),(x-.34,y+.4),(x+.34,y+.4)]
   for xx,yy in pts[1:]:
    n=d.line(x,y,xx,yy,CREAM,1.6);d.anim(n,'wipe',1+j*.2,.45)
   for k,(xx,yy) in enumerate(pts):
    n=d.dot(xx,yy,.065,LIME);d.anim(n,'fade',1.1+j*.2+k*.1,.3)
   n=d.line(x,y+.8,6.4,5.75,CREAM,1.2);d.anim(n,'wipe',3+j*.2,.6)
   d.packet(x,y+.8,6.4,5.75,5+j*.28,1.8,5,LIME)
  d.text('300',9.65,1.2,3,1.6,88,LIME,True);d.text('cây ở RF42\nlịch sử',9.9,2.75,2.7,1,23,CREAM)
  caption('Bootstrap + đặc trưng ngẫu nhiên → tổng hợp dự đoán',.6,6.3,12,24)
 elif view=='vote':
  d.title('VOTING',.55,.9,10,1.1,76)
  d.text('Luật gộp được định trước.',.65,2.05,11,.6,29)
  for j,(lab,col) in enumerate([('LR',VIOLET),('DT',CYAN),('RF',CORAL)]):
   x=2.0;y=3.25+j*1.1;circular_node(lab,x,y,col,.5+j*.4,.4)
   n=d.line(x+.5,y,7.8,4.35,col,1.6,True);d.anim(n,'wipe',2+j*.4,.8)
   d.packet(x+.5,y,7.8,4.35,3+j*.6,1.7,5,col)
  d.rect(7.8,3.95,.8,.8,VIOLET,kind=MSO_SHAPE.DIAMOND)
  d.text('ĐA SỐ\nPHIẾU',9.2,3.0,3.4,1.2,33,VIOLET,True)
  n=d.text('TRUNG BÌNH\nXÁC SUẤT',9.2,4.8,3.5,1.2,29,INK,True);d.anim(n,'fade',7,.5)
  caption('Khác cách học chưa bảo đảm sửa được lỗi chung.',.65,6.4,12,24)
 elif view=='stack':
  d.title('STACKING',.55,.95,7.8,1.2,76)
  d.text('Luật gộp được học từ OOF.',.65,2.1,9,.6,30,GRAY)
  for j,(lab,y) in enumerate([('LR',3.5),('DT',4.7),('RF',5.9)]):
   circular_node(lab,1.4,y,CYAN,.4+j*.2,.38)
   n=d.line(2.1,y,6.5,4.55,CYAN,1.5,True);d.anim(n,'wipe',1.5+j*.3,.7)
   n=d.text('p(Attack)',3.0,6.1 if j==2 else y-.5,3,.4,17,CYAN,font='Consolas');d.anim(n,'fade',2+j*.4,.4)
   d.packet(2.1,y,6.5,4.55,3+j*.5,2.0,6,CYAN)
  n=d.rect(6.5,3.65,1.8,1.8,VIOLET,kind=MSO_SHAPE.DIAMOND);d.anim(n,'fade',3,.7)
  d.text('META\nLR',6.84,4.02,1.1,.8,23,CREAM,True,align=PP_ALIGN.CENTER)
  rail(8.55,4.55,2.1,LIME,5);n=d.text('Normal\n/ Attack',10.9,3.9,2.0,1.2,27,LIME,True);d.anim(n,'fade',6,.5)
  d.packet(8.6,4.55,10.7,4.55,7,2.0,5,LIME)
  d.text('INFERENCE',9.6,1.25,3.1,.6,24,LIME,True,'Consolas')
  caption('FIT: OOF → meta LR      INFERENCE: base đã học → xác suất → meta',.65,6.55,12,20)
 elif view=='score':
  d.title('GẦN NHAU\nĐẾN MỨC NÀO?',.55,.95,7.5,1.8,54)
  for j,(lab,val,col) in enumerate([('RF42','0,863343',INK),('Stacking42','0,863840',VIOLET)]):
   x=.65+j*6.3;n=d.text(lab,x,3.25,5.8,.45,25,col,True);d.anim(n,'fade',1+j*3,.5)
   n=d.text(val,x,3.85,5.8,1.2,58,col,True,'Arial');d.anim(n,'wipe',1.5+j*3,1)
  n=d.text('Δ Macro-F1  +0,000497',.65,5.3,12,.6,32,INK,True);d.anim(n,'fly',8,.7)
  n=d.text('CI 95% của Δ Macro-F1 / Δ MCC chứa 0.',.65,6.15,12,.6,25,DARKGRAY);d.anim(n,'fade',12,.6)
  # Exact sourced paired CI for Delta Macro-F1, linear axis -0.0004..0.0014.
  ci_x=lambda v:9.0+(v+.0004)/.0018*3.6
  n=d.line(ci_x(-.0003118042125941106),1.35,ci_x(.0013089503250197615),1.35,VIOLET,3);d.anim(n,'wipe',13,1)
  zero=ci_x(0);d.line(zero,1.05,zero,1.65,INK,1);d.text('0',zero-.08,1.75,.4,.25,12,INK,font='Consolas')
  n=d.dot(ci_x(.0004966898940774733),1.35,.055,VIOLET);d.anim(n,'fade',14,.4)
  d.text('CI 95% Δ Macro-F1',9.0,.85,3.7,.3,13,INK,True)
  d.text('−0,000312              +0,001309',9.0,2.17,3.8,.3,10,DARKGRAY,font='Consolas')
 elif view=='fp':
  d.title('BỚT CẢNH BÁO GIẢ.',.55,.95,12,1.1,52)
  n=number('−142',.45,2.15,7.1,150,CYAN);d.anim(n,'fly',.4,.9)
  d.text('FP',8.75,2.5,3,1,70,CYAN,True,'Consolas')
  for j,(lab,val,col) in enumerate([('RF42',10003,CREAM),('Stacking42',9861,CYAN)]):
   y=4.7+j*.85;d.text(lab,.65,y-.25,2.3,.4,19,GRAY)
   n=d.rect(3.25,y,7.9*val/11000,.26,col,name=f'fp-bar-{j}');d.anim(n,'wipe',3+j*3,2.1)
   n=d.text(f'{val:,}'.replace(',','.'),11.1,y-.12,1.65,.5,27,col,True,'Consolas');d.anim(n,'fade',5+j*3,.5)
  d.line(3.25,6.6,11.15,6.6,GRAY,1);d.text('0',3.2,6.72,.5,.25,12,GRAY);d.text('11.000 FP',9.5,6.72,2,.25,12,GRAY)
  for j in range(2):d.packet(3.25,4.83,10.3,4.83,10+j*2,2,3,CYAN)
 elif view=='fn':
  d.text('PHẦN ĐỔI LẠI',.6,1.0,11,.6,24,INK,True,'Consolas')
  n=number('+118',.4,1.65,9.2,185,INK);d.anim(n,'fly',.4,1.1);d.pulse(n,5,1.4,2,106)
  n=d.title('BẢN GHI TẤN CÔNG\nBỊ BỎ SÓT THÊM.',.6,4.3,8.0,1.5,36,INK);d.anim(n,'wipe',3,.8)
  for j,(lab,val) in enumerate([('RF42',734),('Stacking42',852)]):
   x=9.35+j*1.55;h=2.65*val/1000;n=d.rect(x,5.9-h,.9,h,INK,name=f'fn-bar-{j}');d.anim(n,'wipe',9+j*3,2)
   n=d.text(str(val),x-.05,2.65,1.45,.55,28,INK,True,'Consolas');d.anim(n,'fade',11+j*3,.4)
   d.text(lab,x-.1,6.05,1.55,.4,12,INK,True,'Consolas')
  d.text('FN: thang riêng 0–1.000',8.95,6.6,3.8,.3,14,INK)
  caption('Số bản ghi trên cùng TEST; chưa phải số sự cố độc lập.',.65,6.45,8.0,18,INK)
 elif view=='matrix':
  d.title('5 LƯỢT FIT.\n1 VALIDATION CHUNG.',.55,1,12,1.75,50)
  arm=['RF42','RF17','Balanced','Oversample','Stack-Lite']
  for j,a in enumerate(arm):d.text(a,2.1+j*1.6,3.1,1.6,.35,16,VIOLET,True,'Consolas',align=PP_ALIGN.CENTER)
  for row,seed in enumerate([1103,2207,3301,4409,5501]):
   y=3.78+row*.45;n=d.text(str(seed),.8,y-.05,1.2,.3,16,INK,font='Consolas');d.anim(n,'fade',.5+row*2,.3)
   for col in range(5):
    x=2.7+col*1.6;n=d.dot(x,y+.1,.085,VIOLET if col%2 else INK);d.anim(n,'fade',1+row*2+col*.15,.25)
   n=d.line(9.75,y+.1,11.0,4.8,VIOLET,1.3,True);d.anim(n,'wipe',2.4+row*2,.6)
   d.packet(9.65,y+.1,10.95,4.8,3.1+row*2,1.2,1,VIOLET)
  n=d.ring(11.8,4.8,.58,VIOLET);d.anim(n,'fade',3,.6);d.pulse(n,5,1.2,6,111)
  d.text('35.069',10.8,5.65,2.2,.5,26,VIOLET,True,'Consolas')
  d.text('60.000 dòng FIT / seed',.8,6.4,6,.5,24,INK)
  d.text('cùng một validation',8.1,6.4,4.7,.5,21,VIOLET)
 elif view=='selection':
  d.title('BỚT BIẾN.\nBỚT CHI PHÍ?',.55,.95,7.5,1.9,55)
  d.text('P21 · Macro-F1 trung bình',8.1,1.2,4.8,.4,18,GRAY)
  d.text('RF42-Lite   0,945220\nStack-Lite  0,944731\nRF17-Lite   0,936751',8.1,1.85,4.8,1.4,21,CREAM,font='Consolas')
  # Real measured components, single seconds axis0–350.
  for j,(label,parts) in enumerate([('RF42-Lite',[(241.119,CYAN)]),('RF17-Lite',[(225.250,VIOLET),(84.600,LIME)])]):
   y=4.0+j*1.05;d.text(label,.65,y-.15,2.55,.4,23,CREAM,True)
   x=3.35
   for k,(val,col) in enumerate(parts):
    n=d.rect(x,y,7.9*val/350,.4,col,name=f'cost-{j}-{k}');d.anim(n,'wipe',2+j*6+k*3,2)
    x+=7.9*val/350
  n=d.text('225,250 + 84,600 = 309,850 s',.65,6.08,12,.65,32,LIME,True,'Consolas');d.anim(n,'fade',15,.6)
  d.text('Violet: chọn biến 225,250 s   |   Lime: fit RF17 84,600 s',3.35,5.6,9.3,.35,17,CREAM)
  d.text('RF42 fit: 241,119 s · RF17: chọn biến + fit · chưa phải end-to-end',.65,6.65,12,.3,16,GRAY)
 elif view=='rates':
  d.title('ÍT CẢNH BÁO GIẢ HƠN.\nBỎ SÓT NHIỀU HƠN.',.55,.9,12,1.55,45)
  x,y,w,h=2.1,6.0,8.5,3.05
  d.line(x,2.65,x,y,INK,1.5);d.line(x,y,11.2,y,INK,1.5)
  for a in [0,4,8,12]:d.text(str(a),x+a/12*w-.1,6.1,.6,.3,13,DARKGRAY,font='Consolas')
  for a in [0,2,4]:d.text(str(a),1.55,y-a/5*h-.1,.5,.3,13,DARKGRAY,font='Consolas')
  d.text('FNR %',.65,2.65,1.5,.4,18,INK,True,'Consolas');d.text('FPR %',11.3,6.05,1.5,.4,18,INK,True,'Consolas')
  pts=[('RF42',9.6196,2.3989,INK),('Balanced',6.4554,4.1870,VIOLET),('Oversample',7.4107,3.5670,'147B88')]
  origin=None
  for j,(label,fpr,fnr,col) in enumerate(pts):
   xx=x+fpr/12*w;yy=y-fnr/5*h
   if j==0:origin=(xx,yy)
   else:
    n=d.line(*origin,xx,yy,col,2,True);d.anim(n,'wipe',5+(j-1)*5,1.7)
    d.packet(*origin,xx,yy,5+(j-1)*5,1.7,1,col)
   n=d.dot(xx,yy,.09,col);d.anim(n,'fade',1+j*5,.5)
   n=d.text(label,xx+(.2 if j!=1 else -1.6),yy+(.1 if j==0 else -.6),2.4,.4,21,col,True);d.anim(n,'fade',1.4+j*5,.5)
  caption('Trung bình 5 FIT seed · Normal là lớp ít mẫu trong TRAIN.',.65,6.65,12,20)
 elif view=='loss':
  d.title('L = FP + r × FN',.55,.9,12,1.25,58)
  d.text('r: chi phí giả định của FN / FP',.65,2.15,12,.5,25,GRAY)
  # Three spatially separated exact scenarios. Progressive chart builds remain
  # readable in the static PDF; no overlapping state text in the editable file.
  states=[(1,0.8),(142/118,8.2),(5,15.2)]
  for j,(r,at) in enumerate(states):
   rs='1,2034' if j==1 else str(int(r))
   group=[];xx=.75+j*4.15
   group.append(d.text('r = '+rs,xx,3.05,3.85,.6,29,LIME,True,'Consolas'))
   lrf=10003+734*r;lst=9861+852*r
   for k,(lab,val,col) in enumerate([('RF42',lrf,CYAN),('Stacking42',lst,CORAL)]):
    yy=4.15+k*1.0;group.append(d.text(lab,xx,yy-.3,1.7,.35,16,col,True))
    group.append(d.rect(xx,yy+.15,3.3*val/15000,.28,col,name=f'loss-r{j}-bar{k}'))
    group.append(d.text(f'{val:,.1f}'.replace(',',' ').replace('.',','),xx+1.65,yy-.35,1.8,.4,18,col,True,'Consolas'))
   group.append(d.text('Stacking thấp hơn' if j==0 else 'Hai tổn thất bằng nhau' if j==1 else 'RF42 thấp hơn',xx,6.15,3.8,.65,22,CREAM,True))
   for n in group:
    d.anim(n,'wipe' if n.startswith('loss-') else 'fade',at,.7)
  d.text('Cùng trục tổn thất quy ước 0–15.000; không phải tiền thiệt hại.',.65,6.85,12,.25,13,GRAY)
 elif view=='close':
  d.title('CHỌN TỪ\nLOẠI LỖI\nCẦN GIẢM.',.55,1.0,8.7,4.5,70,INK)
  for j,t in enumerate(['Đối chiếu các cấu hình.','Kiểm soát thí nghiệm.','Nêu rõ giới hạn.']):
   n=d.text(t,8.9,2.0+j*1.15,3.8,.8,27,INK,True);d.anim(n,'wipe',2+j*4,.7)
  n=d.text('Cần dữ liệu mạng mới và chi phí thực tế.',.65,6.35,12,.6,26,INK);d.anim(n,'fade',15,.5)
  for j in range(3):d.packet(8.9,5.6,12.3,5.6,3+j*2.3,2,5,INK)

# Appendix has a distinct editorial layout and no timed content in main movie.
from creative_qna import QA
for j,(title,q,a,source) in enumerate(QA,1):
 d.page(8,30,CREAM,title,a,f'VẤN ĐÁP / A{j:02}',source)
 d.text(f'{j:02}',.55,1.05,2.5,1.2,78,VIOLET,True,'Arial')
 d.text(q,3.15,1.15,9.55,1.5,36,INK,True)
 d.text(a,3.15,3.0,9.7,2.9,25,INK)
 d.text('Trả lời chính trong 15–25 giây.',3.15,6.45,9.5,.4,18,DARKGRAY)
 d.s._element.set('show','0')
# jump links from closing; labels short and explicit.
closing=d.p.slides[16]
for j in range(12):
 q=closing.shapes.add_textbox(Inches(.65+j*.95),Inches(6.9),Inches(.7),Inches(.2));q.text=f'A{j+1}';q.text_frame.paragraphs[0].font.size=Pt(10);q.click_action.target_slide=d.p.slides[17+j]
for s in list(d.p.slides)[17:]:
 q=s.shapes.add_textbox(Inches(10.9),Inches(.25),Inches(1.8),Inches(.3));q.text='Về kết luận';q.text_frame.paragraphs[0].font.size=Pt(12);q.click_action.target_slide=closing
for si,name,height,width in [(4,'hero-title',218,None),(17,'text-5',66.8,None),(19,'text-5',None,694.5)]:
 q=next(q for q in d.p.slides[si-1].shapes if q.name==name)
 if height:q.height=Pt(height)
 if width:q.width=Pt(width)
target=O/'NCKH_Ensemble_IDS_Creative_Final.pptx';d.save(target)
(O/'main_plan.json').write_text(json.dumps(d.pages[:17],ensure_ascii=False,indent=2),encoding='utf-8')
print('BUILT',len(d.p.slides),'slides',sum(len(x['events']) for x in d.pages),'internal animation events',flush=True)
if '--render' in sys.argv:native_render(target,main_count=17,render_dir=O/'renders',pdf=O/'NCKH_Ensemble_IDS_Static.pdf')
if '--video' in sys.argv:native_render(target,main_count=17,video=O/'Creative_native_silent.mp4')
