#!/usr/bin/env python3
"""Optional Vietnamese neural-voice upgrade for the TEN slide motion preview.

Does not rebuild PPTX nor change scientific contents. Uses edge-tts (network),
with retry, and the same locked deck_plan.json. The original offline practice
MP4 is preserved; a separate *_NeuralVoice.mp4 is written on success.
"""
import asyncio,hashlib,json,subprocess,sys,wave
from pathlib import Path
import numpy as np
import edge_tts
HERE=Path(__file__).resolve().parent
SCENES=json.loads((HERE/"deck_plan.json").read_text(encoding="utf-8"))["scenes"]
VOICE="vi-VN-HoaiMyNeural"
RATE="-4%"
A=HERE/"neural_voice";A.mkdir(exist_ok=True)
INPUT=HERE/"NCKH_Ensemble_IDS_10_Slides_Preview.mp4"
OUTPUT=HERE/"NCKH_Ensemble_IDS_10_Slides_Preview_NeuralVoice.mp4"
def call(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)
def adapt_pronunciation(txt):
    return (txt.replace("UNSW-NB15","iu en ét đắp, en bê mười lăm")
               .replace("P21","pi hai mươi mốt")
               .replace("OOF","ô ô ép")
               .replace("FPR","ép pi a")
               .replace("FNR","ép en a")
               .replace("MCC","em xi xi"))
async def one(scene):
    i=scene["n"];source=A/f"slide_{i:02}.mp3"
    txt=adapt_pronunciation(scene["voice"])
    sig=hashlib.sha256(f"{VOICE}|{RATE}|{txt}".encode()).hexdigest()
    hashfile=source.with_suffix(".sha256")
    if source.exists() and hashfile.exists() and hashfile.read_text()==sig:
        return source
    for attempt in range(4):
        try:
            await edge_tts.Communicate(txt,VOICE,rate=RATE).save(str(source))
            hashfile.write_text(sig,encoding="utf-8")
            return source
        except Exception as e:
            if attempt==3:raise RuntimeError(f"Neural TTS failure slide {i}: {e}") from e
            await asyncio.sleep(2+attempt*3)
async def main():
    # Never blast 10 simultaneous requests into a public endpoint.
    files=[]
    for scene in SCENES:
        files.append(await one(scene))
    track=np.zeros(360*24000,dtype=np.float32)
    start=0;details=[]
    for scene,source in zip(SCENES,files):
        duration=scene["duration"]
        raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(source),
                  "-ar","24000","-ac","1","-f","f32le","-"])
        samples=np.frombuffer(raw,dtype="<f4")
        original=len(samples)/24000
        max_time=duration-.95
        tempo=1.
        if original>max_time:
            tempo=original/max_time
            effects=[]
            while tempo>2:effects.append("atempo=2");tempo/=2
            effects.append(f"atempo={tempo:.5f}")
            raw=subprocess.check_output(["ffmpeg","-v","error","-i",str(source),
                  "-af",",".join(effects),"-ar","24000","-ac","1","-f","f32le","-"])
            samples=np.frombuffer(raw,dtype="<f4")
        offset=int((start+.38)*24000)
        take=min(len(samples),int(max_time*24000))
        track[offset:offset+take]+=.82*samples[:take]
        details.append({"slide":scene["n"],"slot_sec":duration,
                        "speech_original_sec":round(original,3),
                        "speech_final_sec":round(take/24000,3),
                        "time_fitted":original>max_time})
        start+=duration
    if start!=360:raise AssertionError(start)
    track=np.clip(track,-.93,.93)
    wav=A/"Neural_Vietnamese_Narration.wav"
    with wave.open(str(wav),"wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000)
        w.writeframes((track*32767).astype("<i2").tobytes())
    call(["ffmpeg","-y","-loglevel","error","-i",str(INPUT),
          "-i",str(wav),"-map","0:v:0","-map","1:a:0",
          "-c:v","copy","-c:a","aac","-b:a","160k",
          "-t","360","-movflags","+faststart",str(OUTPUT)])
    info=json.loads(call(["ffprobe","-v","error","-show_format","-show_streams",
                          "-of","json",str(OUTPUT)]).stdout)
    length=float(info["format"]["duration"])
    if abs(length-360)>.26:raise RuntimeError("Neural video duration changed")
    report={"status":"PASS_NEURAL_VIETNAMESE_PREVIEW",
            "video":OUTPUT.name,"voice":VOICE,"rate":RATE,
            "duration_seconds":length,"narration_slots":details,
            "script_source":"deck_plan.json","audio_timelines_changed":False,
            "human_proper_noun_pronunciation_QA":False,
            "quality_notice":"This is synthesized speech for rehearsal; manually inspect names/ML acronyms and replace with live voice for defense.",
            "pptx_and_research_untouched":True}
    (HERE/"neural_voice_qa.json").write_text(
         json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"status":report["status"],"duration":length,
                      "voice":VOICE,"fitted":sum(x["time_fitted"] for x in details)},
                     ensure_ascii=False),flush=True)
if __name__=="__main__":
    asyncio.run(main())
