import sys
from PIL import Image
# crop.py out code [x0 y0 x1 y1 fractions] ...
out=sys.argv[1]; ims=[]
args=sys.argv[2:]; i=0
while i<len(args):
    code=args[i]; i+=1
    box=(0.04,0.02,0.97,0.62)
    if i+3<len(args) and args[i].replace('.','').isdigit():
        box=tuple(float(a) for a in args[i:i+4]); i+=4
    im=Image.open(f"Processing/Australia/QLD/Original PNGs/{code}.png").convert("RGB")
    w,h=im.size; ims.append(im.crop((int(box[0]*w),int(box[1]*h),int(box[2]*w),int(box[3]*h))))
W=sum(i.width for i in ims); H=max(i.height for i in ims)
sh=Image.new("RGB",(W,H),"white"); x=0
for im in ims: sh.paste(im,(x,0)); x+=im.width
sh.save(out)
