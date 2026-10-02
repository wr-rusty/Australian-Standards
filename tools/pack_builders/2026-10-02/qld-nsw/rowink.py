# rowink.py CODE x0 y0 x1 y1 W_mm  ya yb [mingap_mm] [colour] : ink runs across a band (mm from sign top), box = sign outline px
import sys; from PIL import Image
code=sys.argv[1]; x0,y0,x1,y1,W=[float(v) for v in sys.argv[2:7]]; ya,yb=float(sys.argv[7]),float(sys.argv[8]); mg=float(sys.argv[9]) if len(sys.argv)>9 else 25
col=sys.argv[10] if len(sys.argv)>10 else 'dark'
im=Image.open(f'Processing/Australia/NSW/Original PNGs/{code}.png').convert('RGB'); k=(x1-x0)/W; px=im.load()
def ink(p):
    if col=='dark': return max(p)<110
    if col=='white': return min(p)>215
    if col=='red': return p[0]>170 and p[1]<110 and p[2]<110
    if col=='notyellow': return not (p[0]>200 and p[1]>170 and p[2]<120)
cols=[]
for x in range(int(x0),int(x1)+1):
    cols.append(any(ink(px[x,y]) for y in range(int(y0+ya*k),int(y0+yb*k)+1)))
runs=[]; s=None
for i,c in enumerate(cols+[False]):
    if c and s is None: s=i
    if not c and s is not None: runs.append([s,i-1]); s=None
m=[]
for r in runs:
    if m and (r[0]-m[-1][1])/k<mg: m[-1][1]=r[1]
    else: m.append(r)
print([(round(a/k,1),round((b+1)/k,1),round((b+1-a)/k,1)) for a,b in m])
# vertical extent of ink in band columns
rows=[y for y in range(int(y0+ya*k),int(y0+yb*k)+1) if any(ink(px[x,y]) for x in range(int(x0+40*k),int(x1-40*k)))]
if rows: print('rows mm', round((rows[0]-y0)/k,1), round((rows[-1]+1-y0)/k,1))
