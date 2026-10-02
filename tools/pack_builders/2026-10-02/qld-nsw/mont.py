import sys
from PIL import Image, ImageDraw
# mont.py out frac cols code...
out=sys.argv[1]; frac=float(sys.argv[2]); cols=int(sys.argv[3]); codes=sys.argv[4:]
ims=[]
for c in codes:
    im=Image.open(f"Processing/Australia/QLD/Original PNGs/{c}.png").convert("RGB"); w,h=im.size
    im=im.crop((int(0.05*w),int(0.02*h),int(0.97*w),int(frac*h))); TW=int(__import__("os").environ.get("TW","640")); s=TW/im.width; im=im.resize((TW,int(im.height*s)))
    ImageDraw.Draw(im).text((6,4),c,fill="red"); ims.append(im)
TW=int(__import__("os").environ.get("TW","640")); rows=[ims[i:i+cols] for i in range(0,len(ims),cols)]
H=sum(max(i.height for i in r) for r in rows); sh=Image.new("RGB",(TW*cols,H),"white"); y=0
for r in rows:
    x=0
    for im in r: sh.paste(im,(x,y)); x+=TW
    y+=max(i.height for i in r)
sh.save(out)
