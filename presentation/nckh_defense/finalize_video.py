from pathlib import Path
import json,subprocess,wave
import numpy as np
O=Path(__file__).resolve().parent
raw=O/'intermediate/PowerPoint_native_silent.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],text=True))
native=probe(raw);duration=float(native['format']['duration'])
timeline=json.loads((O/'timeline.json').read_text());rate=48000
track=np.zeros(360*rate,dtype=np.float32)
for row in timeline:
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(O/f'audio/slide_{row["slide"]:02}.mp3'),'-f','s16le','-ac','1','-ar',str(rate),'-'])
 a=np.frombuffer(data,dtype=np.int16).astype(np.float32)/32768
 start=round(row['speech_start']*rate);assert start+len(a)<=len(track)
 track[start:start+len(a)]+=a
peak=float(np.max(np.abs(track)));track*=.91/max(peak,1e-8)
with wave.open(str(O/'audio/narration.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((track*32767).astype('<i2').tobytes())
factor=360/duration
dest=O/'NCKH_Ensemble_IDS_Preview.mp4'
cmd=['ffmpeg','-y','-v','warning','-i',str(raw),'-i',str(O/'audio/narration.wav'),'-filter_complex',f'[0:v]setpts={factor:.12f}*(PTS-STARTPTS),fps=30[v]',
 '-map','[v]','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-t','360','-movflags','+faststart',str(dest)]
r=subprocess.run(cmd,capture_output=True,text=True)
(O/'audit/ffmpeg_finalize.log').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
result=probe(dest)
(O/'audit/video_metadata.json').write_text(json.dumps({'native':native,'final':result,'normalization':{'native_seconds':duration,'final_target_seconds':360,'uniform_video_pts_factor':factor,'voice_time_stretch':False,'motion_origin':'Microsoft PowerPoint CreateVideo, real native Morph','note':'FFmpeg uniformly normalizes native video timestamps (~0.4%); no manually simulated motion. Narration authored directly on 360s timeline.'}},indent=2),encoding='utf-8')
print(json.dumps({'native_seconds':duration,'factor':factor,'final_seconds':result['format']['duration'],'bytes':dest.stat().st_size}),flush=True)
# Saved video frames prove actual runtime states, not merely PPTX static geometry.
frames=O/'video_frames';frames.mkdir(exist_ok=True)
for i,t in enumerate([10,45,90,145,216,269,307,347],1):
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(dest),'-frames:v','1',str(frames/f'scene_{i:02}.jpg')],check=True)
# Full stream decode catches invalid frames/audio packets.
r=subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,text=True)
(O/'audit/full_video_decode.log').write_text(r.stderr,encoding='utf-8');assert r.returncode==0 and not r.stderr.strip(),r.stderr
print('FULL_VIDEO_DECODE_PASS',flush=True)
