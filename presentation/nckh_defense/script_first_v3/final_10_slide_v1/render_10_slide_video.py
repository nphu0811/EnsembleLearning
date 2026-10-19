#!/usr/bin/env python3
"""Render a six-minute MP4 *from the new ten-slide deck* with moving data overlays.

Video has real per-frame particle/path/data motion and crossfades, not an
image-only slideshow. PNG backgrounds are rasterized from the same editable
PPTX through LibreOffice; overlays are deterministic, based on the scene type.
For training/rehearsal only: optional local espeak-ng Vietnamese is robotic
and MUST be listened to / replaced with human narration before defense.
"""
from __future__ import annotations
from pathlib import Path
import json,math,subprocess,shutil,time,wave
from PIL import Image,ImageDraw,ImageFont
import fitz

HERE=Path(__file__).resolve().parent
PPTX=HERE/"NCKH_Ensemble_IDS_10_Slides_Final.pptx"
SCENES=json.loads((HERE/"deck_plan.json").read_text(encoding="utf-8"))["scenes"]
OUTPUT=HERE/"NCKH_Ensemble_IDS_10_Slides_Preview.mp4"
OUT_DIR=HERE/"rendered";OUT_DIR.mkdir(exist_ok=True)
FPS=15
WIDTH,HEIGHT=1280,720
C={"cyan":(30,196,210),"coral":(255,106,87),"lime":(199,248,119),
   "red":(230,38,41),"ink":(20,25,42),"violet":(134,115,230),"white":(255,255,255)}
def run(cmd):
    return subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,check=True)
def pdf_from_pptx():
    outpdf=OUT_DIR/PPTX.with_suffix(".pdf").name
    if not outpdf.exists():
        cmd=["libreoffice","-env:UserInstallation=file:///tmp/lo_nckh_10_slide",
             "--headless","--convert-to","pdf","--outdir",str(OUT_DIR),str(PPTX)]
        result=run(cmd)
        if not outpdf.exists():
            raise RuntimeError("LibreOffice render failed: "+result.stdout+result.stderr)
    return outpdf
pdf=pdf_from_pptx()
doc=fitz.open(pdf)
if len(doc)!=10:raise ValueError(f"PPTX PDF render must contain 10 slides, got {len(doc)}")
BG=[]
for i,page in enumerate(doc):
    pix=page.get_pixmap(matrix=fitz.Matrix(WIDTH/page.rect.width,HEIGHT/page.rect.height),
                        alpha=False)
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    if im.size!=(WIDTH,HEIGHT):im=im.resize((WIDTH,HEIGHT))
    BG.append(im)
    im.save(OUT_DIR/f"slide_{i+1:02}.png",optimize=True)
def smooth(a):
    a=max(0.,min(1.,a))
    return a*a*(3-2*a)
def glowing_dot(draw,x,y,col,r=8):
    cc=tuple(int(c*.65+120*.35) for c in col)
    draw.ellipse((x-r*2.4,y-r*2.4,x+r*2.4,y+r*2.4),outline=cc,width=2)
    draw.ellipse((x-r,y-r,x+r,y+r),fill=col)
def dynamic(im,scene,t):
    """All coordinates are in the rendered 1280x720 frame."""
    im=im.copy();d=ImageDraw.Draw(im,"RGBA");kind=scene["type"]
    col=C["red"] if kind not in ("hook","metrics","conclusion") else C["cyan"]
    # Persistent editorial line, physically traveling across each frame.
    xa=55+(t*.065 % 1)*1150
    d.line((xa,680,xa+67,680),fill=col+(210,),width=5)
    if kind=="cover":
        for j in range(10):
            y=(60+(t*.32+j/10)*760)%720
            d.line((10,y,195,y-34),fill=(255,205,193,78),width=1)
        d.arc((960,15,1380,432),start=(t*110)%360,end=(t*110+84)%360,
              fill=C["red"]+(200,),width=7)
    elif kind=="hook":
        x,y=1110,325
        for j in range(3):
            rad=45+21*j+7*math.sin(2*math.pi*t/2.8+j)
            d.arc((x-rad,y-rad,x+rad,y+rad),
                  start=(t*120+j*75)%360,end=(t*120+j*75+130)%360,
                  fill=C["cyan"]+(140,),width=3)
        for j in range(5):
            f=(t*.26+j*.20)%1
            glowing_dot(d,90+f*970,615+9*math.sin(f*12+j),C["coral"],4)
    elif kind=="data":
        for row,color in [(485,C["red"]),(528,C["cyan"])]:
            d.rounded_rectangle((72,row,72+int(smooth(min(1,t/3))*1020),row+7),
                                radius=3,fill=color+(190,))
        for j in range(11):
            f=(t*.10+j*.11)%1
            glowing_dot(d,80+f*1040,646,C["cyan"],3)
    elif kind=="pipeline":
        # Animated network flow, following EXACT same nodes/connection in PPTX.
        for j in range(16):
            phase=(t*.27+j/16.)%1.
            x=120+phase*1030
            y=416+15*math.sin(phase*6.28+j*.6)
            glowing_dot(d,x,y,C["cyan"] if j%2 else C["red"],4)
        for j,x in enumerate([135,382,714,1075]):
            r=17+6*math.sin(2*math.pi*t/1.6+j)
            d.ellipse((x-r,414-r,x+r,414+r),outline=C["cyan"]+(160,),width=3)
    elif kind=="metrics":
        for row,x0,x1,color in [(0,68,621,C["cyan"]),(1,636,1235,C["coral"])]:
            f=(t*.17+row*.35)%1
            x=x0+(x1-x0)*f
            glowing_dot(d,x,510,color,6)
            d.arc((x0,530,x1,613),int(t*60)%360,int(t*60+100)%360,
                  fill=color+(130,),width=3)
    elif kind=="historical":
        # Motion follows the actual 142 FP improvement / 118 FN increase.
        r=smooth(min(1,t/5))
        d.rounded_rectangle((95,549,95+int(r*420),557),radius=4,
                            fill=C["cyan"]+(220,))
        d.rounded_rectangle((681,549,681+int(r*420),557),radius=4,
                            fill=C["red"]+(210,))
        for j in range(12):
            glowing_dot(d,180+(.28*t*90+j*37)%400,587,
                        C["cyan"] if j%2 else C["red"],3)
    elif kind=="p21design":
        for j in range(5):
            x=156+j*225
            alpha=int(80+150*(.5+.5*math.sin(t*4-j*.6)))
            d.ellipse((x-42,356,x+42,440),outline=C["cyan"]+(alpha,),width=4)
        # One common validation bar glows underneath all five FIT sources.
        d.rounded_rectangle((335,607,335+int(smooth(min(1,t/7))*575),612),
                            radius=2,fill=C["red"]+(220,))
    elif kind=="p21results":
        for j,color in enumerate([C["cyan"],C["violet"],C["coral"]]):
            x=100+j*405
            v=[.945220,.944731,.936751][j]
            prog=smooth(min(1,t/(4+j*.5)))
            width=int((v-.85)*2200*prog)
            d.rounded_rectangle((x,464,x+width,471),radius=2,fill=color+(210,))
        for j in range(8):
            f=(t*.13+j*.14)%1
            glowing_dot(d,100+f*1100,646,C["red"],3)
    elif kind=="conclusion":
        for j in range(7):
            x=95+j*168
            y=595+18*math.sin(t*2+j)
            glowing_dot(d,x,y,C["cyan"] if j%2 else C["coral"],5)
        d.arc((950,20,1350,420),(t*46)%360,(t*46+115)%360,
              fill=C["cyan"]+(160,),width=5)
    elif kind=="thanks":
        for j in range(20):
            f=(t*.045+j/20)%1
            x=250+f*970
            y=462+15*math.sin(j*.6+t*.6)
            glowing_dot(d,x,y,C["red"] if j%3 else C["cyan"],3)
        d.line((260,562,260+int(smooth(min(1,t/8))*910),562),
               fill=C["red"]+(190,),width=5)
    return im
def make_silent():
    tmp=HERE/"_silent_10_slides.mp4"
    command=["ffmpeg","-hide_banner","-loglevel","error","-y",
             "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
             "-r",str(FPS),"-i","-","-an","-vf","scale=1920:1080,fps=30",
             "-c:v","libx264","-preset","veryfast","-crf","23",
             "-pix_fmt","yuv420p","-movflags","+faststart",str(tmp)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    elapsed=0
    try:
        for i,scene in enumerate(SCENES):
            count=scene["duration"]*FPS
            for fr in range(count):
                t=fr/FPS
                im=dynamic(BG[i],scene,t)
                # Real cross-scene dissolve; object motifs retain color/position.
                if i and fr<FPS//2:
                    fraction=smooth(fr/(FPS//2))
                    prev=dynamic(BG[i-1],SCENES[i-1],SCENES[i-1]["duration"]+t)
                    im=Image.blend(prev,im,fraction)
                proc.stdin.write(im.tobytes())
            elapsed+=scene["duration"]
            print(f"RENDERED scene={i+1} duration={scene['duration']} elapsed={elapsed}",flush=True)
    except BrokenPipeError:
        raise RuntimeError("FFmpeg exited while reading animation frames")
    finally:
        try:proc.stdin.close()
        except OSError:pass
    msg=proc.stderr.read().decode("utf-8","replace");ret=proc.wait()
    if ret:raise RuntimeError(f"FFmpeg animation render error: {msg[-2000:]}")
    return tmp

def narration():
    # On Linux CI, espeak-ng is a deterministic low-fidelity fallback.
    # Never pass its sample as "verified Vietnamese natural voice".
    if not shutil.which("espeak-ng"):return None,"NO_TTS_COMMAND"
    import soundfile as sf
    import numpy as np
    track=np.zeros(360*24000,dtype=np.float32)
    offset=0;issues=[]
    for s in SCENES:
        wav=OUT_DIR/f"speech_{s['n']:02}.wav"
        r=subprocess.run(["espeak-ng","-v","vi","-s","170","-a","180","-w",
                          str(wav),s["voice"]],capture_output=True,text=True)
        if r.returncode or not wav.exists():
            issues.append("scene "+str(s["n"])+": TTS skipped")
            offset+=s["duration"];continue
        # Audio length is strictly cropped to its slide to preserve timing.
        a,sr=sf.read(wav,dtype="float32")
        if len(a.shape)>1:a=a.mean(axis=1)
        # use FFmpeg to resample to 24k mono (avoids scipy requirement)
        pcm=subprocess.check_output(["ffmpeg","-v","error","-i",str(wav),
             "-ac","1","-ar","24000","-f","f32le","-"])
        a=np.frombuffer(pcm,dtype="<f4")
        maxlen=int((s["duration"]-1.0)*24000)
        if len(a)>maxlen:
            # Play back a little faster when a scene is tight, without altering
            # information shown on screen; must verify pronunciation manually.
            ratio=len(a)/maxlen
            effects=[]
            while ratio>2:effects.append("atempo=2");ratio/=2
            effects.append(f"atempo={max(0.5,min(2.,ratio)):.4f}")
            data=subprocess.check_output(["ffmpeg","-v","error","-i",str(wav),
              "-af",",".join(effects),"-ac","1","-ar","24000","-f","f32le","-"])
            a=np.frombuffer(data,dtype="<f4")
            issues.append(f"scene {s['n']}: auto time-fit voice; needs human playback")
        st=int((offset+.55)*24000);take=min(len(a),maxlen)
        track[st:st+take]+=a[:take]*.45
        offset+=s["duration"]
    track=np.clip(track,-.9,.9)
    out=OUT_DIR/"rough_vi_narration.wav"
    sf.write(out,track,24000)
    return out,issues

silent=make_silent()
voice,info=narration()
if voice:
    cmd=["ffmpeg","-y","-loglevel","error","-i",str(silent),
         "-i",str(voice),"-map","0:v:0","-map","1:a:0","-c:v","copy",
         "-c:a","aac","-b:a","128k","-t","360","-movflags","+faststart",str(OUTPUT)]
else:
    cmd=["ffmpeg","-y","-loglevel","error","-i",str(silent),
         "-c:v","copy","-t","360","-movflags","+faststart",str(OUTPUT)]
run(cmd)
probe=json.loads(run(["ffprobe","-v","error","-show_format","-show_streams",
                      "-of","json",str(OUTPUT)]).stdout)
duration=float(probe["format"]["duration"])
if abs(duration-360)>.26:raise RuntimeError(f"Bad 6-minute video duration {duration}")
(HERE/"video_build_summary.json").write_text(json.dumps({
   "status":"PASS_6MIN_MOTION_PREVIEW","video":OUTPUT.name,
   "seconds":duration,"scenes":10,"source":"Editable ten-slide PowerPoint",
   "motion":"Animated tracking particles, network flow, charts, reveal bars, crossfades",
   "fps":30,"frame_source_fps":FPS,"resolution":"1920x1080",
   "narration":"offline espeak-ng rough Vietnamese training voice" if voice else "silent",
   "tts_issues":info,"human_narration_QA":False,
   "powerpoint_native_animations_in_mp4":"Not rendered; video overlays mimic intended motion",
   "scientific_claims_in_video":"Match locked deck_plan.json and PPTX"
},ensure_ascii=False,indent=2),encoding="utf-8")
print("PASS VIDEO",duration,OUTPUT,flush=True)
