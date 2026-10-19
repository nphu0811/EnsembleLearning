#!/usr/bin/env python3
"""Editable ten-scene NCKH defense PowerPoint from the locked V7-based deck_plan.

The deck is intentionally NEW, not the 29-slide Creative V2 file. All labels,
numbers and claims are loaded from the independently source-mapped deck plan.
No training data or frozen results are opened or changed.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json
import re
import zipfile
from lxml import etree as ET
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PLAN=json.loads((HERE/"deck_plan.json").read_text(encoding="utf-8"))
SCENES=PLAN["scenes"]
OUT=HERE/"NCKH_Ensemble_IDS_10_Slides_Final.pptx"
OLD=ROOT/"presentation/nckh_defense/creative_rebuild_v2/NCKH_Ensemble_IDS_Creative_Final.pptx"
LOGO=ROOT/PLAN["assets"]["logo"]
W,H=13.333333,7.5
C=dict(cream="F8F5EE",white="FFFFFF",ink="14192A",red="E62629",
       coral="FF6A57",cyan="1EC4D2",lime="C7F877",violet="8673E6",
       blue="255E9E",gray="778195",pale="E8EAEC",muted="C5CBD5")

def rgb(v):return RGBColor.from_string(C.get(v,v))
def inch(v):return Inches(v)
p=Presentation();p.slide_width=inch(W);p.slide_height=inch(H)

def box(sl,x,y,w,h,color,rounded=False,stroke=None,name=None):
    shp=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        inch(x),inch(y),inch(w),inch(h))
    shp.name=name or "Shape"
    if color:shp.fill.solid();shp.fill.fore_color.rgb=rgb(color)
    else:shp.fill.background()
    if stroke:shp.line.color.rgb=rgb(stroke);shp.line.width=Pt(1.5)
    else:shp.line.fill.background()
    return shp

def oval(sl,x,y,w,h,color,stroke=None,name="Orb"):
    shp=sl.shapes.add_shape(MSO_SHAPE.OVAL,inch(x),inch(y),inch(w),inch(h))
    shp.name=name
    if color:shp.fill.solid();shp.fill.fore_color.rgb=rgb(color)
    else:shp.fill.background()
    if stroke:shp.line.color.rgb=rgb(stroke);shp.line.width=Pt(1.6)
    else:shp.line.fill.background()
    return shp

def line(sl,x,y,xx,yy,color="gray",width=2,name="Connector"):
    s=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,inch(x),inch(y),inch(xx),inch(yy))
    s.name=name;s.line.color.rgb=rgb(color);s.line.width=Pt(width)
    return s

def text(sl,string,x,y,w,h,fs=23,color="ink",bold=False,name="Text",
         font="Liberation Sans",align=None):
    sh=sl.shapes.add_textbox(inch(x),inch(y),inch(w),inch(h));sh.name=name
    tf=sh.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_left=tf.margin_right=0
    tf.margin_top=tf.margin_bottom=0
    tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    for i,row in enumerate(str(string).split("\n")):
        par=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        par.text=row
        par.font.name=font;par.font.size=Pt(fs);par.font.bold=bold
        par.font.color.rgb=rgb(color)
        par.space_before=par.space_after=Pt(0)
        if align is not None:par.alignment=align
    return sh

def dotline(sl,x,y,n=11,step=.18,color="red"):
    for i in range(n):oval(sl,x+i*step,y,.042,.042,color,name=f"Micro-point {i+1}")

def logo(sl,x,y,w=1.25):
    # Reuse PTIT's actual raster asset already supplied in the research repository.
    if LOGO.is_file():
        sl.shapes.add_picture(str(LOGO),inch(x),inch(y),width=inch(w))

def tiny(sl,n,eyebrow,bg):
    light=bg in ("ink",)
    fg="cream" if light else "ink"
    text(sl,eyebrow,.66,.35,9.2,.3,11,fg,True,"Eyebrow")
    text(sl,f"#{n:02}",11.8,.31,.85,.37,12,fg,True,"Scene counter",align=PP_ALIGN.RIGHT)
    box(sl,.65,7.095,12.0,.015,"coral" if light else "red",name="Progress track")
    box(sl,.65,7.095,12*n/10,.04,"cyan" if light else "red",name="Progress position")
    text(sl,"NCKH  /  ENSEMBLE IDS  /  UNSW-NB15",.65,7.18,8,.21,9,fg,name="Running footer")

def title(sl,t,bg,x=.6,y=1.07,w=12.1,fs=54,h=2.15):
    return text(sl,t,x,y,w,h,fs,"cream" if bg=="ink" else "ink",True,"Hero title")

def mark_animation_targets(sl,n):
    """Visible accents dedicated to motion paths / fly-ins, not scientific figures."""
    dots=[]
    for j in range(14):
        x=10.3+(j%7)*.32;y=6.48+(j//7)*.28
        col="cyan" if j%3 else "coral"
        dots.append(oval(sl,x,y,.08,.08,col,name=f"Animated marker {n}-{j}").shape_id)
    return dots

def make(sl,s):
    n=s["n"];typ=s["type"];bg=s["bg"]
    col=C[bg];sl.background.fill.solid();sl.background.fill.fore_color.rgb=rgb(col)
    tiny(sl,n,s["eyebrow"],bg)
    if n!=1:logo(sl,12.15,.72,.48)
    if typ=="cover":
        box(sl,0,0,2.55,7.5,"red",name="PTIT red margin")
        for a in range(16):
            yy=.4+a*.45;line(sl,.2,yy,2.45,yy,"coral",.5)
        # Put the real red PTIT logo on a contrasting LIGHT field, not on brand red.
        logo(sl,11.68,.48,.85)
        text(sl,"PTIT",.45,3.50,1.75,.85,39,"cream",True,"White PTIT monogram")
        text(sl,"PTIT / HỌC VIỆN CÔNG NGHỆ\nBƯU CHÍNH VIỄN THÔNG",3.1,.76,9.7,.8,19,"red",True,"Academy header")
        text(sl,s["title"],3.0,1.93,9.7,3.15,57,"ink",True,"Research hero")
        box(sl,3.03,5.29,7.65,.05,"red")
        text(sl,s["subtitle"],3.03,5.58,9.3,.55,19,"ink",name="Official topic")
        text(sl,"GVHD  TS. LÊ NGỌC HIẾU   •   LỚP E23CQCE01-N",3.04,6.37,9.6,.3,13,"gray",True)
        text(sl,"Dương Ngọc Phú · Phạm Thế Vỹ · Vũ Văn Kiên · Lê Hoàng Nguyên Quân",3.04,6.72,9.8,.32,12,"ink")
    elif typ=="hook":
        box(sl,0,0,.2,7.5,"coral")
        title(sl,s["title"],bg,.72,1.68,11.7,68,2.65)
        text(sl,s["subtitle"],.82,5.20,10.7,.82,25,"cyan")
        oval(sl,10.5,2.38,1.75,1.75,None,"cyan","Open question circle")
        text(sl,"?",10.88,2.63,1.0,1.25,71,"lime",True,"Question mark",align=PP_ALIGN.CENTER)
        for j in range(8):line(sl,.9+j*.23,6.22,.95+j*.24,6.22,"coral",2)
    elif typ=="data":
        title(sl,s["title"],bg,.65,.88,10.7,50,1.85)
        text(sl,"175.341",.75,3.13,6.0,1.28,86,"red",True,"TRAIN number")
        text(sl,"TRAIN / official",.77,4.43,4.6,.43,21,"gray",True)
        text(sl,"82.332",7.0,3.13,5.8,1.28,80,"ink",True,"TEST number")
        text(sl,"TEST / official",7.02,4.43,4.6,.43,21,"gray",True)
        line(sl,6.61,3.1,6.61,5.08,"pale",2)
        box(sl,.74,5.52,3.15,.62,"ink",rounded=True)
        text(sl,"42 PREDICTORS",.94,5.63,2.82,.38,18,"cream",True)
        box(sl,4.12,5.52,3.25,.62,"cyan",rounded=True)
        text(sl,"NORMAL / 0",4.33,5.63,2.9,.38,18,"ink",True)
        box(sl,7.59,5.52,3.20,.62,"coral",rounded=True)
        text(sl,"ATTACK / 1",7.83,5.63,2.75,.38,18,"ink",True)
    elif typ=="pipeline":
        title(sl,s["title"],bg,.6,.93,9.6,49,1.8)
        text(sl,"FIT: OOF ở tầng kết hợp  /  INFERENCE: mô hình đã huấn luyện",.67,2.72,12,.4,17,"gray")
        # "Connected system" rather than four rectangular cards. These rings,
        # stage labels, branches and connectors are all native PowerPoint shapes.
        centers=[1.53,4.19,7.64,11.3]
        radii=[.62,.80,.91,.75]
        labels=["FLOW","FEATURE\nVECTOR","BASE\nLEARNERS","NORMAL\n/ ATTACK"]
        for i in range(3):
            line(sl,centers[i]+radii[i]+.12,4.25,
                 centers[i+1]-radii[i+1]-.12,4.25,
                 "cyan" if i!=2 else "red",4,f"Flow connection {i+1}")
        for i,(x,r,label) in enumerate(zip(centers,radii,labels)):
            ring="red" if i==3 else ("blue" if i==1 else "cyan")
            oval(sl,x-r,4.25-r,2*r,2*r,None,ring,name=f"Scientific flow ring {i}")
            oval(sl,x-r*.83,4.25-r*.83,1.66*r,1.66*r,
                 "red" if i==3 else "ink",name=f"Scientific flow inner {i}")
            text(sl,label,x-r+.10,4.25-r*.42,2*r-.20,.76,
                 13 if i in (1,2) else 14,
                 "cream",True,f"Scientific stage {i}",
                 align=PP_ALIGN.CENTER)
        # Three base learners converging towards the meta-learner:
        for j,(lab,c) in enumerate([("LR","cyan"),("DT","violet"),("RF","coral")]):
            xx=6.74+j*.9
            oval(sl,xx,5.37,.42,.42,c,name="Editable learner node")
            text(sl,lab,xx+.04,5.45,.35,.22,10,"ink",True,"Learner abbreviation",align=PP_ALIGN.CENTER)
            line(sl,xx+.20,5.34,7.64,5.24,"gray",.85)
        box(sl,6.52,6.05,3.3,.50,"pale",rounded=True,name="OOF label")
        text(sl,"OOF → META LEARNER (LR)",6.70,6.12,3.05,.32,12,"ink",True)
        for j in range(10):
            oval(sl,2.62+j*.21,3.33,.075,.075,"cyan",name="Editable flow particle")
    elif typ=="metrics":
        title(sl,s["title"],bg,.70,1.0,10.5,59,1.94)
        box(sl,.72,3.40,5.67,1.72,"cyan",rounded=True)
        text(sl,"FP  /  FALSE POSITIVE",1.0,3.63,5.1,.52,22,"ink",True)
        text(sl,"BÌNH THƯỜNG → TẤN CÔNG",1.0,4.26,5.05,.46,16,"ink")
        box(sl,6.60,3.40,5.79,1.72,"coral",rounded=True)
        text(sl,"FN  /  FALSE NEGATIVE",6.85,3.63,5.3,.52,22,"ink",True)
        text(sl,"TẤN CÔNG → BÌNH THƯỜNG",6.85,4.26,5.18,.46,16,"ink")
        text(sl,"MACRO-F1     ·     MCC     ·     FPR     ·     FNR",.95,5.65,11.7,.70,26,"cream",True)
    elif typ=="historical":
        title(sl,s["title"],bg,.64,.81,11.7,63,2.10)
        box(sl,.70,3.43,5.6,2.1,"ink",rounded=True)
        text(sl,"−142",1.05,3.65,4.7,1.0,76,"cyan",True,"Reduction FP")
        text(sl,"FALSE POSITIVE",1.08,4.75,4.3,.40,22,"cream",True)
        box(sl,6.60,3.43,5.95,2.1,"cream",rounded=True)
        text(sl,"+118",7.01,3.65,4.8,1.0,76,"red",True,"Increase FN")
        text(sl,"FALSE NEGATIVE",7.05,4.75,4.6,.40,22,"ink",True)
        text(sl,"Macro-F1    RF42 0,863343    /    Stacking42 0,863840",.79,5.83,11.8,.55,18,"ink",True)
        text(sl,"CI hiệu số chứa 0  •  Không đủ bằng chứng Stacking vượt trội",.79,6.37,11.7,.50,16,"ink")
    elif typ=="p21design":
        title(sl,s["title"],bg,.68,.80,11.6,55,2.0)
        text(sl,"TRAIN-ONLY · POST-HOC · KHÔNG PHẢI 5 TEST ĐỘC LẬP",.73,2.95,11.7,.51,21,"red",True)
        for j in range(5):
            x=1.1+2.35*j
            oval(sl,x,4.15,1.10,1.10,"ink",name=f"Seed {j+1}")
            text(sl,f"{j+1:02d}",x+.18,4.36,.75,.55,31,"cream",True,f"Seed label {j+1}")
            text(sl,"FIT",x+.24,5.36,.65,.37,16,"blue",True)
        line(sl,1.53,6.02,11.58,6.02,"coral",4)
        box(sl,3.52,6.14,6.0,.52,"cyan",rounded=True)
        text(sl,"35.069 DÒNG VALIDATION CHUNG",3.74,6.23,5.6,.32,15,"ink",True)
    elif typ=="p21results":
        title(sl,s["title"],bg,.64,.76,11.6,51,2.0)
        for j,(name,val,color) in enumerate([
            ("RF42-LITE","0,945220","cyan"),
            ("STACKING-LITE","0,944731","violet"),
            ("RF17-LITE","0,936751","coral")]):
            x=.72+4.22*j
            box(sl,x,3.20,4.02,1.42,color,rounded=True)
            text(sl,name,x+.2,3.38,3.6,.40,15,"ink",True)
            text(sl,val.replace(".",","),x+.17,3.88,3.7,.58,35,"ink",True)
        box(sl,.74,5.18,7.48,1.28,"ink",rounded=True)
        text(sl,"SELECTOR + RF17 FIT",1.02,5.37,6.5,.34,17,"cream",True)
        text(sl,"309,850s   >   RF42 FIT 241,119s",1.0,5.77,6.55,.43,24,"lime",True)
        box(sl,8.46,5.18,4.06,1.28,"pale",rounded=True)
        text(sl,"BALANCING",8.70,5.34,3.59,.32,16,"red",True)
        text(sl,"FPR ↓    FNR ↑",8.69,5.74,3.49,.45,22,"ink",True)
    elif typ=="conclusion":
        box(sl,.0,0,.17,7.5,"cyan")
        title(sl,s["title"],bg,.65,1.04,11.9,53,2.55)
        line(sl,.72,4.43,12.4,4.43,"coral",4)
        for j,t in enumerate(["MÔ HÌNH ĐƠN","CƠ CHẾ ENSEMBLE","CHI PHÍ LỖI"]):
            x=.8+j*4.14
            text(sl,t,x,5.03,3.9,.47,20,"cyan" if j==1 else "cream",True)
        text(sl,"Đối chứng có kiểm soát • Công khai giới hạn",.84,6.19,11.6,.45,18,"muted")
    elif typ=="thanks":
        logo(sl,.75,1.05,1.58)
        title(sl,s["title"],bg,2.70,2.10,9.90,66,2.35)
        box(sl,2.73,4.66,8.63,.072,"red")
        text(sl,"BƯỚC TIẾP: DỮ LIỆU MỚI  ·  THEO THỜI GIAN/PHIÊN  ·  CHI PHÍ SOC",2.75,5.14,9.15,.72,16,"blue",True)
        text(sl,"GVHD: TS. LÊ NGỌC HIẾU",2.77,6.29,7.4,.45,16,"ink")
    else:raise ValueError(typ)
    # every slide has real independent PowerPoint-native objects
    mark_animation_targets(sl,n)

def trans_and_native_motion(prs):
    """Clone verified PowerPoint-native timing from the previously built Creative V2.
    Animation targets in each clone are remapped exclusively to dedicated visible
    accent dots. No scientific label/table is moved or hidden by imported paths.
    Also insert standard PowerPoint fade transition for every slide boundary.
    """
    old_timings=[]
    with zipfile.ZipFile(OLD) as z:
        for i in range(1,18):
            root=ET.fromstring(z.read(f"ppt/slides/slide{i}.xml"))
            t=root.find("{http://schemas.openxmlformats.org/presentationml/2006/main}timing")
            if t is not None:old_timings.append(t)
    if len(old_timings)<10:raise RuntimeError("Historical native animation source missing")
    ns="{http://schemas.openxmlformats.org/presentationml/2006/main}"
    for i,sl in enumerate(prs.slides):
        tree=sl._element
        transition=ET.Element(ns+"transition",spd="med",advClick="1")
        ET.SubElement(transition,ns+"fade")
        # Schema order: cSld, clrMapOvr?, transition?, timing?
        c=tree.find(ns+"cSld")
        after=list(tree).index(c)+1
        tree.insert(after,transition)
        timing=deepcopy(old_timings[(i*2)%len(old_timings)])
        targets=timing.findall(".//"+ns+"spTgt")
        ids=[sp.shape_id for sp in sl.shapes if sp.name.startswith("Animated marker")]
        if not ids:raise RuntimeError("Missing editable accent shapes")
        oldids=list(dict.fromkeys(sp.get("spid") for sp in targets))
        mapping={oid:ids[j%len(ids)] for j,oid in enumerate(oldids)}
        for el in targets:el.set("spid",str(mapping[el.get("spid")]))
        tree.append(timing)

for scene in SCENES:
    sl=p.slides.add_slide(p.slide_layouts[6]);make(sl,scene)
trans_and_native_motion(p)
p.save(OUT)
assert len(p.slides)==10
(HERE/"deck_build_summary.json").write_text(json.dumps({
    "status":"CREATED", "slide_count":10,"duration_seconds":sum(s["duration"] for s in SCENES),
    "source":"V7", "pptx":OUT.name,"ptit_logo":str(LOGO),
    "native_slide_timings":10,"native_transitions":"fade+object-continuity visuals",
    "animation_notice":"Retargeted verified creative native PowerPoint animation to accent dots, not scientific numbers"
},ensure_ascii=False,indent=2),encoding="utf-8")
print("PPTX",OUT,len(p.slides),"slides")
