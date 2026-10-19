from pathlib import Path
import json,subprocess,wave
import numpy as np
from creative_content import MAIN
O=Path(__file__).resolve().parent
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],text=True))
raw=O/'Creative_native_silent.mp4';native=probe(raw);duration=float(native['format']['duration'])
assert 359<duration<363,duration
ms=json.loads((O/'audio/measurements.json').read_text());track=np.zeros(360*48000,np.float32);timeline=[];start=0
for i,row in enumerate(MAIN,1):
 sec=row[1];voice=ms[i-1]['speech_seconds'];assert voice<=sec-1.1,(i,voice,sec)
 speech_start=start+.55
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(O/f'audio/slide_{i:02}.mp3'),'-f','s16le','-ac','1','-ar','48000','-'])
 a=np.frombuffer(data,np.int16).astype(np.float32)/32768;offset=round(speech_start*48000);track[offset:offset+len(a)]+=a
 timeline.append(dict(slide=i,scene=row[0],start=start,end=start+sec,speech_start=speech_start,speech_end=speech_start+voice,pause_seconds=sec-.55-voice));start+=sec
track*=.91/max(float(abs(track).max()),1e-8)
with wave.open(str(O/'audio/narration.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((track*32767).astype('<i2').tobytes())
(O/'timeline.json').write_text(json.dumps(timeline,indent=2),encoding='utf-8')
dest=O/'NCKH_Ensemble_IDS_Creative_Preview.mp4';factor=360/duration
cmd=['ffmpeg','-y','-v','warning','-i',str(raw),'-i',str(O/'audio/narration.wav'),'-filter_complex',f'[0:v]setpts={factor:.12f}*(PTS-STARTPTS),fps=30[v]','-map','[v]','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','360','-movflags','+faststart',str(dest)]
r=subprocess.run(cmd,capture_output=True,text=True);(O/'audit/ffmpeg_finalize.log').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
final=probe(dest);(O/'audit/video_metadata.json').write_text(json.dumps(dict(native=native,final=final,normalization=dict(native_seconds=duration,pts_factor=factor,voice_time_stretch=False,motion_engine='Microsoft PowerPoint CreateVideo; native same-slide timeline, zero Morph')),indent=2),encoding='utf-8')
print('FINAL',final['format']['duration'],flush=True)
r=subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,text=True);(O/'audit/full_video_decode.log').write_text(r.stderr,encoding='utf-8');assert r.returncode==0 and not r.stderr.strip(),r.stderr
print('FULL_DECODE_PASS',flush=True)
