# inkbox.py CODE x0 y0 x1 y1 W_mm margin_mm [ya yb] : bbox (mm) of non-ground ink inside the sign, margin in from the outline
import sys; from PIL import Image
code=sys.argv[1]; x0,y0,x1,y1,W,m=[float(v) for v in sys.argv[2:8]]
im=Image.open(f'Processing/Australia/NSW/Original PNGs/{code}.png').convert('RGB'); px=im.load(); k=(x1-x0)/W; H=(y1-y0)/k
ya=float(sys.argv[8]) if len(sys.argv)>8 else m; yb=float(sys.argv[9]) if len(sys.argv)>9 else H-m
g=px[int(x0+(m+3)*k),int(y0+(m+3)*k)]
xs=[];ys=[]
for y in range(int(y0+ya*k),int(y0+yb*k)):
    for x in range(int(x0+m*k),int(x1-m*k)):
        p=px[x,y]
        if max(p)<110 or (p[0]>200 and p[1]<90 and p[2]<90): xs.append(x); ys.append(y)
print('H',round(H,1),'ink mm', round((min(xs)-x0)/k,1), round((min(ys)-y0)/k,1), round((max(xs)+1-x0)/k,1), round((max(ys)+1-y0)/k,1))
