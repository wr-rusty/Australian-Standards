"""fixwind.py sym.svg ... : rewrite each evenodd <path> so nonzero filling gives the same picture (signgen ignores fill-rule).
Subpaths are oriented by nesting depth (even = one direction, odd = the other). Verifies by rasterising both ways."""
import sys, re, os, subprocess, tempfile, io
import xml.etree.ElementTree as ET
from svgpathtools import parse_path, Path
from shapely.geometry import Polygon, Point
from PIL import Image, ImageChops
INK="/Applications/Inkscape.app/Contents/MacOS/inkscape"
def f(v): return f"{v:.3f}".rstrip("0").rstrip(".")
def poly(sp, n=40):
    pts=[]
    for seg in sp:
        k = 1 if seg.__class__.__name__=="Line" else n
        for i in range(k): 
            p=seg.point(i/k); pts.append((p.real,p.imag))
    return pts
def area(pts): return sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))/2
def fix(d):
    P=parse_path(d); subs=P.continuous_subpaths(); polys=[]
    for s in subs:
        pts=poly(s)
        try: pg=Polygon(pts).buffer(0)
        except Exception: pg=None
        polys.append((pts,pg))
    out=[]
    for i,s in enumerate(subs):
        pts,pg=polys[i]
        if pg is None or pg.is_empty: out.append(s); continue
        rp=pg.representative_point(); depth=sum(1 for j,(q,qg) in enumerate(polys) if j!=i and qg is not None and not qg.is_empty and qg.area>pg.area and qg.contains(rp))
        a=area(pts); want_pos = depth%2==0
        if (a>0)!=want_pos: s=s.reversed()
        out.append(s)
    ds=[]
    for s in out:
        dd=Path(*s).d()
        ds.append(dd if dd.rstrip().upper().endswith("Z") else dd+" Z")
    return " ".join(ds)
def raster(svgtext):
    with tempfile.TemporaryDirectory() as td:
        p=os.path.join(td,"a.svg"); open(p,"w").write(svgtext); o=os.path.join(td,"a.png")
        subprocess.run([INK,p,"--export-type=png","--export-width=600","--export-background=#ffffff",f"--export-filename={o}"],capture_output=True)
        return Image.open(o).convert("L").copy()
for fn in (sys.argv[1:] if __name__=="__main__" else []):
    txt=open(fn).read()
    if "evenodd" not in txt: continue
    truth=raster(txt.replace("currentColor","#000"))
    def rep(m):
        tag=m.group(0)
        if 'fill-rule="evenodd"' not in tag: return tag
        d=re.search(r' d="([^"]+)"',tag).group(1)
        return tag.replace(d,fix(d)).replace(' fill-rule="evenodd"','')
    new=re.sub(r"<path[^>]*>",rep,txt)
    got=raster(new.replace("currentColor","#000"))
    diff=ImageChops.difference(truth,got).point(lambda v:255 if v>100 else 0)
    n=sum(1 for v in diff.getdata() if v); nz=raster(txt.replace(' fill-rule="evenodd"','').replace("currentColor","#000"))
    was=sum(1 for v in ImageChops.difference(truth,nz).point(lambda v:255 if v>100 else 0).getdata() if v)
    print(os.path.basename(fn),"was wrong px:",was,"after:",n)
    if n<=60 and "--write" in os.environ.get("FW",""): open(fn,"w").write(new)
