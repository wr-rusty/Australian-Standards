"""contact.py — contact sheets (grey ground) of the SA SVGs generated in this run: Inkscape render + PIL."""
import os, sys, subprocess, csv, json, glob, tempfile
from PIL import Image, ImageDraw
ROOT="/Users/USER/Local/GitHub/Australian-Standards"; OUT=ROOT+"/Processing/Australia/SA/SVGs (generated)"
INK="/Applications/Inkscape.app/Contents/MacOS/inkscape"
S=os.path.dirname(os.path.abspath(__file__))
old=set(json.load(open(S+"/before_files.json")))
rows=[r for r in csv.DictReader(open(OUT+"/MANIFEST.csv")) if r["file"] and r["file"] not in old]
print(len(rows),"files generated in this run")
cache=S+"/thumbs"; os.makedirs(cache,exist_ok=True)
TH=150; todo=[]
for r in rows:
    src=OUT+"/"+r["file"]; dst=cache+"/"+r["file"].replace("/","__")+".png"
    r["png"]=dst
    if not os.path.exists(dst) or os.path.getmtime(dst)<os.path.getmtime(src): todo.append((src,dst))
if todo:
    acts=";".join(f"file-open:{s};export-filename:{d};export-height:{TH};export-do;file-close" for s,d in todo)
    for i in range(0,len(todo),60):
        chunk=todo[i:i+60]
        acts=";".join(f"file-open:{s};export-filename:{d};export-height:{TH};export-do;file-close" for s,d in chunk)
        subprocess.run([INK,"--actions",acts],capture_output=True)
fams={}
for r in rows: fams.setdefault(r["file"].split("/")[0],[]).append(r)
n=0
for fam,rs in fams.items():
    per=70
    for p in range(0,len(rs),per):
        chunk=rs[p:p+per]; cols=10; cw=190; ch=TH+26
        sheet=Image.new("RGB",(cols*cw,((len(chunk)+cols-1)//cols)*ch+24),(128,128,128)); d=ImageDraw.Draw(sheet)
        d.text((6,4),f"{fam}  {p+1}-{p+len(chunk)} of {len(rs)}",fill="white")
        for i,r in enumerate(chunk):
            x=(i%cols)*cw; y=24+(i//cols)*ch
            try:
                im=Image.open(r["png"]).convert("RGBA")
                if im.width>cw-8: im=im.resize((cw-8,max(1,int(im.height*(cw-8)/im.width))))
                sheet.paste(im,(x+(cw-im.width)//2,y+(TH-im.height)//2),im)
            except Exception as ex: d.text((x+4,y+60),"MISSING",fill="red")
            d.text((x+3,y+TH+2),r["code"][:28],fill="white"); d.text((x+3,y+TH+13),os.path.basename(r["file"])[:30],fill=(220,220,220))
        fn=f"{S}/contact_{fam.replace(' ','_').replace('/','-')}_{p//per:02d}.png"; sheet.save(fn); print(fn,sheet.size); n+=1
