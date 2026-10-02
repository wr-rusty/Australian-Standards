"""vw.py CODE... -> view/<CODE>.png : drawing area cropped (frame, title block, colour legend removed), prints crop origin (200-dpi px)"""
import sys, numpy as np
from PIL import Image
SA="/Users/russell/Local/GitHub/Australian-Standards/Processing/Australia/SA/Original PNGs/"
for code in sys.argv[1:]:
    im=Image.open(SA+code+".png").convert("RGB"); a=np.asarray(im); H,W=a.shape[:2]
    if W>H: print(code,"LANDSCAPE",W,H)
    dark=(a.sum(axis=2)<700)
    # frame: find title block top = first long horizontal line below 75% height
    rows=dark.mean(axis=1); cols=dark.mean(axis=0)
    ys=[y for y in range(int(H*0.6),H) if rows[y]>0.7]
    bot=(ys[0]-6) if ys else int(H*0.84)
    top=next((y for y in range(0,int(H*0.2)) if rows[y]>0.7),0)+6
    xs=[x for x in range(W) if cols[x]>0.5]
    left=(xs[0]+6) if xs else 0; right=(xs[-1]-6) if xs else W
    sub=dark[top:bot,left:right]
    r=np.where(sub.any(axis=1))[0]; c=np.where(sub.any(axis=0))[0]
    y0,y1,x0,x1=top+r[0],top+r[-1],left+c[0],left+c[-1]
    crop=im.crop((x0-4,y0-4,x1+4,y1+4)); crop.save(f"view/{code}.png"); print(code,"origin",x0-4,y0-4,"size",crop.size)
