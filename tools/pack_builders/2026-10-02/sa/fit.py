"""fit.py — place legend tokens on measured ink components (positions read off the sheet at 1200 dpi)."""
import meas, mk
_cache={}
def comps(code,box,W,H,view=False,dpi=1200):
    key=(code,tuple(box))
    if key not in _cache:
        b=[v*1653/1413 for v in box] if view else list(box)
        out,pp=meas.run(code,b,W,H,dpi=dpi,minmm=1.5,show=False)
        _cache[key]=(out,pp)
    return _cache[key]
class Fit:
    def __init__(s,code,box,W,H,view=False):
        s.out,s.pp=comps(code,box,W,H,view); s.W=W; s.H=H; s.used=set(); s.log=[]
    def cands(s,cls):
        return [c for c in s.out.get(cls,[]) if not (c[2]-c[0]>0.9*s.W and c[3]-c[1]>0.9*s.H)]
    def text(s,cls,txt,series,height,y,colour=None,tol=4,xmin=None,xmax=None,top=None):
        n=len(txt.replace(" ","").replace("I","I"))
        cs=[c for c in s.cands(cls) if id(c) not in s.used and abs(c[1]-y)<tol and abs((c[3]-c[1])-height)<max(3,0.12*height) and (xmin is None or c[0]>=xmin) and (xmax is None or c[0]<=xmax)]
        cs.sort(key=lambda c:c[0]); take=cs[:n]
        if len(take)<n: raise SystemExit(f"fit: {txt!r} at y {y}: only {len(take)} comps of {n}")
        for c in take: s.used.add(id(c))
        x=round(take[0][0],1); t=top if top is not None else round(sorted(c[1] for c in take)[len(take)//2]*2)/2
        w=take[-1][2]-take[0][0]; fw=mk.ink(txt,series,height)
        s.log.append(f"{txt} {height}{series} x {x} top {t} w {w:.1f} (font {fw})")
        e=mk.T(txt,series,height,t,align="left",x=x)
        if colour: e["colour"]=colour
        return e
    def dash(s,cls,y,colour="black",tol=8,xmin=None,xmax=None,hmax=8):
        cs=[c for c in s.cands(cls) if id(c) not in s.used and abs((c[1]+c[3])/2-y)<tol and (c[3]-c[1])<hmax and 8<(c[2]-c[0])<25 and (xmin is None or c[0]>=xmin) and (xmax is None or c[0]<=xmax)]
        cs.sort(key=lambda c:c[0])
        if not cs: raise SystemExit(f"fit: dash at y {y} not found")
        c=cs[0]; s.used.add(id(c)); f=0.0
        s.log.append(f"dash x {c[0]:.1f}-{c[2]:.1f} y {c[1]:.1f}-{c[3]:.1f}")
        return mk.rect(round(c[0],1),round(c[1],1),round(c[2]-c[0]-0.6,1),round(c[3]-c[1]-0.6,1),colour)
    def big(s,cls,y,wmin,wmax,tol=12):
        cs=[c for c in s.cands(cls) if id(c) not in s.used and abs(c[1]-y)<tol and wmin<=(c[2]-c[0])<=wmax]
        if not cs: raise SystemExit(f"fit: big comp at y {y} not found")
        c=min(cs,key=lambda c:abs(c[1]-y)); s.used.add(id(c)); return c
    def arrow(s,cls,y,colour):
        c=s.big(cls,y,140,160); L=155 if c[2]-c[0]>150 else 146
        x=round((c[0]+c[2])/2-L/2,1); yy=round((c[1]+c[3])/2-16,1)
        s.log.append(f"arrow x {x} y {yy}"); return mk.arrow_d(x,yy,L,colour)
    def symbol(s,cls,sid,y,wmin,wmax,colour="black",extra=()):
        c=s.big(cls,y,wmin,wmax)
        # swallow small comps inside/just below (wheels)
        x0,y0,x1,y1=c[:4]
        for o in s.cands(cls):
            if id(o) in s.used: continue
            if o[0]>=x0-1 and o[2]<=x1+1 and o[1]>=y0-1 and o[1]<y1+2: s.used.add(id(o)); y1=max(y1,o[3]); 
        w,h=mk.symbox(sid); sc=(x1-x0-0.6)/w
        s.log.append(f"symbol {sid} x {x0:.1f}-{x1:.1f} y {y0:.1f}-{y1:.1f}; national {w:.0f}x{h:.0f} at {sc:.3f} -> h {h*sc:.1f}")
        return mk.sym(sid,round(x0,1),round(y0,1),round(w*sc,1),round(h*sc,1),colour)
    def left(s):
        return [(cls,[round(v,1) for v in c[:4]]) for cls in s.out for c in s.cands(cls) if id(c) not in s.used and max(c[2]-c[0],c[3]-c[1])>3]
