# overlay-only strips, stacked: ovv.py out.png CODE...
import sys; sys.path.insert(0,'tools')
import compare_drawing as C
from PIL import Image, ImageDraw
out=sys.argv[1]; tiles=[]
for code in sys.argv[2:]:
    val=None
    if '=' in code: code,val=code.split('=')
    spec=C.spec_for(code); crop,gen,h,v=C.compare(spec, val); ov=C.overlay(crop,gen)
    for t in (crop,ov):
        t=t.copy(); t.thumbnail((1500,700)); tiles.append((f"{code} {v or ''} {C.score(crop,gen):.3f}",t))
W=max(t.width for _,t in tiles); H=sum(t.height+16 for _,t in tiles); sh=Image.new('RGB',(W,H),'white'); y=0
for lab,t in tiles:
    ImageDraw.Draw(sh).text((2,y+2),lab,fill='black'); sh.paste(t,(0,y+16)); y+=t.height+16
sh.save(out); print(sh.size)
