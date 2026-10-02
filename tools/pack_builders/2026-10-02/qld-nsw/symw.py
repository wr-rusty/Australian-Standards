"""write tools/symbols/<sid>.svg from plan vector fills: translate so viewBox = bbox; subpaths re-wound for nonzero fill (holes reversed)"""
import re, os
from svgpathtools import parse_path, Path
def bbox_of(ds):
    xs=[];ys=[]
    for d in ds:
        x0,x1,y0,y1=parse_path(d).bbox(); xs+=[x0,x1]; ys+=[y0,y1]
    return min(xs),min(ys),max(xs),max(ys)
def area(sub):
    a=0
    for seg in sub:
        for i in range(8):
            p=seg.point(i/8); q=seg.point((i+1)/8); a+=p.real*q.imag-q.real*p.imag
    return a/2
def fix(d):
    """even-odd compound -> nonzero: outer subpaths one winding, nested ones the other"""
    P=parse_path(d); subs=P.continuous_subpaths()
    if len(subs)<2: return P
    from shapely.geometry import Polygon
    polys=[Polygon([(s.point(t/40).real,s.point(t/40).imag) for s in sub for t in range(40)]) for sub in subs]
    out=[]
    for i,sub in enumerate(subs):
        depth=sum(1 for j,p in enumerate(polys) if j!=i and p.buffer(0).contains(polys[i].buffer(0).representative_point()))
        want=1 if depth%2==0 else -1
        if (area(sub)>0)!=(want>0): sub=sub.reversed()
        out+=list(sub)
    return Path(*out)
def ser(P):
    from svgpathtools import Line, CubicBezier, QuadraticBezier
    f=lambda z: '%s %s' % (('%.2f' % z.real).rstrip('0').rstrip('.') or '0', ('%.2f' % z.imag).rstrip('0').rstrip('.') or '0')
    out=[]
    for sub in P.continuous_subpaths():
        out.append('M'+f(sub[0].start))
        for seg in sub:
            if isinstance(seg,Line): out.append('L'+f(seg.end))
            elif isinstance(seg,CubicBezier): out.append('C'+f(seg.control1)+' '+f(seg.control2)+' '+f(seg.end))
            elif isinstance(seg,QuadraticBezier): out.append('Q'+f(seg.control)+' '+f(seg.end))
            else: raise ValueError(seg)
        out.append('Z')
    return ''.join(out)
def write(sid, ds, fills=None, force=True):
    x0,y0,x1,y1=bbox_of(ds); out=[]
    for i,d in enumerate(ds):
        P=fix(d).translated(complex(-x0,-y0)); dd=ser(P)
        out.append(f'<path fill="{fills[i] if fills else "currentColor"}" d="{dd}"/>')
    p=f'tools/symbols/{sid}.svg'
    if os.path.exists(p) and not force: raise SystemExit('exists '+p)
    open(p,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x1-x0:.2f} {y1-y0:.2f}">\n'+'\n'.join(out)+'\n</svg>\n')
    return [round(v,1) for v in (x0,y0,x1-x0,y1-y0)]
