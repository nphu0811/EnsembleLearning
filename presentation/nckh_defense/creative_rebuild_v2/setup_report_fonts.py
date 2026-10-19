import requests,re,tarfile,io,json
from pathlib import Path
O=Path(__file__).resolve().parent;src=O/'report_v7/source';p=src/'assets/fonts';p.mkdir(exist_ok=True)
u='https://deb.debian.org/debian/pool/main/f/fonts-liberation2/'
res=requests.get(u,timeout=30);res.raise_for_status()
links=re.findall(r'href="([^"]+all.deb)"',res.text);assert links, res.status_code
url=u+links[-1];res=requests.get(url,timeout=60);res.raise_for_status();b=res.content;off=8
while off<len(b):
 name=b[off:off+16].decode().strip();size=int(b[off+48:off+58]);data=b[off+60:off+60+size];off+=60+size+size%2
 if name.startswith('data.tar'):
  tf=tarfile.open(fileobj=io.BytesIO(data))
  for m in tf.getmembers():
   if ('LiberationSerif' in m.name and m.name.endswith('.ttf')) or m.name.endswith('/copyright'):
    (p/Path(m.name).name).write_bytes(tf.extractfile(m).read())
master=src/'main_revision_v7_2026_10_19.tex';s=master.read_text(encoding='utf-8')
old=r'\IfFontExistsTF{Liberation Serif}{\setmainfont{Liberation Serif}}{\setmainfont{TeX Gyre Termes}}'
new=r'\setmainfont{LiberationSerif-Regular.ttf}[Path=assets/fonts/,BoldFont=LiberationSerif-Bold.ttf,ItalicFont=LiberationSerif-Italic.ttf,BoldItalicFont=LiberationSerif-BoldItalic.ttf]'
s=s.replace(old,new);master.write_text(s,encoding='utf-8')
(O/'audit/report_font_provenance.json').write_text(json.dumps({'url':url,'files':[x.name for x in p.iterdir()],'note':'Explicit local LiberationSerif2 font files preserve the V6 family; no machine font installation needed.'},indent=2),encoding='utf-8');print('FONTS_READY')
