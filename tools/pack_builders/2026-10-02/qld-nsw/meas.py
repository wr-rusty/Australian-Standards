"""meas.py CODE y0mm y1mm : ink column runs (mm) between y0..y1 inside the spec's panel_px; gaps > 12mm listed"""
import sys, json
from PIL import Image
def runs(code, y0, y1, thr=110, drawing=None, mingap=12, x0mm=None, x1mm=None, colour=None):
    s=json.load(open(f"tools/specs/QLD/{code}.json")); px=s["panel_px"]; W=s["size"][0]
    im=Image.open(f"Processing/Australia/QLD/Original PNGs/{drawing or s.get('drawing',code)}.png").convert("RGB")
    k=(px[2]-px[0])/W
    def ink(p):
        if colour=="notyellow": return not (p[0]>200 and p[1]>170 and p[2]<120)
        return p[0]<thr and p[1]<thr+ (60 if colour=="green" else 0) and p[2]<thr+(80 if colour=="blue" else 0)
    cols=[]
    xa=int(px[0]+(x0mm or 40)*k); xb=int(px[0]+(x1mm or W-40)*k)
    for x in range(xa,xb):
        if any(ink(im.getpixel((x,y))) for y in range(int(px[1]+y0*k),int(px[1]+y1*k))): cols.append(x)
    segs=[]; st=pv=cols[0]
    for x in cols[1:]:
        if (x-pv)/k>mingap: segs.append((st,pv)); st=x
        pv=x
    segs.append((st,pv))
    return [(round((a-px[0])/k,1),round((b+1-px[0])/k,1)) for a,b in segs]
if __name__=="__main__":
    print(runs(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]), mingap=float(sys.argv[4]) if len(sys.argv)>4 else 12))
