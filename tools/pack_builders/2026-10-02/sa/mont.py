"""mont.py out.png cols CODE... — thumbnails of sheets (frame area only), labelled"""
import sys
from PIL import Image, ImageDraw
SA="/Users/russell/Local/GitHub/Australian-Standards/Processing/Australia/SA/Original PNGs/"
out=sys.argv[1]; cols=int(sys.argv[2]); codes=sys.argv[3:]; tw=int(1900/cols)
ims=[]
for c in codes:
    im=Image.open(SA+c+".png").convert("RGB"); W,H=im.size
    if H>=W: im=im.crop((int(W*0.02),int(H*0.02),int(W*0.98),int(H*0.74)))
    im.thumbnail((tw,tw*1.3)); ImageDraw.Draw(im).rectangle((0,0,len(c)*7+6,13),fill="yellow"); ImageDraw.Draw(im).text((3,1),c,fill="black"); ims.append(im)
rows=[ims[i:i+cols] for i in range(0,len(ims),cols)]
Ht=sum(max(i.height for i in r) for r in rows)
sheet=Image.new("RGB",(tw*cols,Ht),"white"); y=0
for r in rows:
    x=0
    for i in r: sheet.paste(i,(x,y)); x+=tw
    y+=max(i.height for i in r)
sheet.save(out); print(out,sheet.size)
