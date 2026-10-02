import os, glob, subprocess, filecmp
from PIL import Image, ImageDraw
V="/private/tmp/claude-501/-Users-russell-Local-GitHub-Australian-Standards/864c19bd-a9fd-4e42-b214-2b760136839d/scratchpad"
root="Processing/Australia/QLD/SVGs (generated)"; old=V+"/oldgen/SVGs (generated)"
import csv, subprocess as sp
before={r[1] for r in csv.reader(open(V+"/MANIFEST.before.csv")) if len(r)>1}
mod=set(l.strip().strip('"') for l in sp.run(["git","-c","core.quotepath=off","diff","--name-only","--",root],capture_output=True,text=True).stdout.splitlines())
ch=[]
for f in sorted(glob.glob(root+"/**/*.svg",recursive=True)):
    rel=os.path.relpath(f,root)
    if rel not in before or f in mod: ch.append(f)
print("changed/new",len(ch))
os.makedirs(V+"/fin",exist_ok=True)
acts=[]
for i,f in enumerate(ch): acts.append(f'file-open:{f}; export-height:130; export-filename:{V}/fin/{i:04d}.png; export-do; file-close')
subprocess.run(["/Applications/Inkscape.app/Contents/MacOS/inkscape","--actions="+"; ".join(acts)],capture_output=True)
tiles=[]
for i,f in enumerate(ch):
    p=f"{V}/fin/{i:04d}.png"
    if not os.path.exists(p): print("no render",f); continue
    im=Image.open(p).convert("RGBA"); t=Image.new("RGB",(max(im.width,110)+8,152),"#9a9a9a"); t.paste(im,(4,4),im)
    ImageDraw.Draw(t).text((4,138),os.path.basename(f)[:-4].rsplit("_",1)[-1][:24],fill="black"); tiles.append(t)
rows=[[]]
for t in tiles:
    if sum(x.width for x in rows[-1])+t.width>2000 and rows[-1]: rows.append([])
    rows[-1].append(t)
for pg in range(0,len(rows),10):
    rs=rows[pg:pg+10]; sh=Image.new("RGB",(2000,len(rs)*154),"#9a9a9a"); y=0
    for r in rs:
        x=0
        for t in r: sh.paste(t,(x,y)); x+=t.width
        y+=154
    sh.save(f"{V}/final_{pg//10:02d}.png")
print(len(rows))
