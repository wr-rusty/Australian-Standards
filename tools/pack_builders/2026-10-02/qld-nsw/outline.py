# outline.py CODE [which]: bbox of big dark-bordered sign: largest connected dark component(s) on the sheet excluding frame
import sys; sys.path.insert(0,'tools')
from PIL import Image
import compare_drawing as C
code=sys.argv[1]
img=Image.open(f'Processing/Australia/NSW/Original PNGs/{code}.png').convert('RGB'); w,h=img.size
small=img.resize((w//2,h//2))
comps=C._components(small, lambda p: max(p)<80, 300)
out=[]
for c in comps:
    x0,y0,x1,y1=c['box']
    if (x1-x0)>0.85*small.width or (y1-y0)>0.85*small.height: continue
    if y0>0.78*small.height: continue
    out.append((c['n'],[2*x0,2*y0,2*x1+1,2*y1+1]))
out.sort(reverse=True)
for n,b in out[:5]: print(n,b)
