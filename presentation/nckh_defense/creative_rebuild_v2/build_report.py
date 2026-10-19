from pathlib import Path
import subprocess,json,shutil,os
O=Path(__file__).resolve().parent;S=O/'report_v7/source';T=O/'runtime/TinyTeX/bin/windows'
env=os.environ.copy();env['PATH']=str(T)+os.pathsep+env.get('PATH','')
logs=[]
for i,command in enumerate([['xelatex.exe','-interaction=nonstopmode','-halt-on-error','main_revision_v7_2026_10_19.tex'],['bibtex.exe','main_revision_v7_2026_10_19'],['xelatex.exe','-interaction=nonstopmode','-halt-on-error','main_revision_v7_2026_10_19.tex'],['xelatex.exe','-interaction=nonstopmode','-halt-on-error','main_revision_v7_2026_10_19.tex']]):
 r=subprocess.run([str(T/command[0])]+command[1:],cwd=S,env=env,capture_output=True)
 (O/f'audit/report_build_{i+1}.log').write_bytes(r.stdout+r.stderr)
 print('STEP',i+1,'EXIT',r.returncode,flush=True)
 if r.returncode:print((r.stdout+r.stderr).decode('utf-8',errors='replace')[-3500:]);raise SystemExit(r.returncode)
shutil.copy2(S/'main_revision_v7_2026_10_19.pdf',O/'Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf')
print('V7_PDF_COMPILED',flush=True)
