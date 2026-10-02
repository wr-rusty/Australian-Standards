"""meas.py CODE x0 y0 x1 y1 Wmm Hmm [dpi]  — box = approx sign outline in 200-dpi px. Prints refined panel_px and ink boxes in mm."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
from scipy import ndimage as ndi
def classes(a):
    r,g,b=[a[...,i].astype(int) for i in range(3)]
    return {"black": (r<110)&(g<110)&(b<110),
            "red": (r>170)&(g<110)&(b<110),
            "orange/yellow": (r>170)&(g>100)&(b<110),
            "green": (g>90)&(r<110)&(b<140)&(g>r+30),
            "blue": (b>120)&(r<110)&(g<140)&(b>g+20),
            "brown": (r>90)&(r<180)&(g>40)&(g<110)&(b<80)}
def refine(a, box, f, slack=14):
    x0,y0,x1,y1=[v*f for v in box]; s=int(slack*f)
    ink=(a.sum(axis=2)<600)
    def edge(v, lo, hi, axis, outward):
        v=int(v); rng=range(v-s, v+s+1); prof=[]
        for t in rng:
            line = ink[int(lo+0.2*(hi-lo)):int(hi-0.2*(hi-lo)), t] if axis==0 else ink[t, int(lo+0.2*(hi-lo)):int(hi-0.2*(hi-lo))]
            prof.append(line.mean())
        prof=np.array(prof); idx=np.where(prof>0.6)[0]
        if len(idx)==0: return float(v), False
        t = idx[0] if outward<0 else idx[-1]
        return float(rng[t]) + (0 if outward<0 else 1), True
    X0,ok0=edge(x0,y0,y1,0,-1); X1,ok1=edge(x1,y0,y1,0,1); Y0,ok2=edge(y0,x0,x1,1,-1); Y1,ok3=edge(y1,x0,x1,1,1)
    return (X0,Y0,X1,Y1),(ok0,ok2,ok1,ok3)
def run(code, box, W, H, dpi=800, minmm=1.5, show=True, norefine=False):
    im=h.page_img(code,dpi); a=np.asarray(im); f=dpi/200
    if norefine: (X0,Y0,X1,Y1),oks=[v*f for v in box],None
    else: (X0,Y0,X1,Y1),oks=refine(a,box,f)
    kx=(X1-X0)/W; ky=(Y1-Y0)/H
    if show: print(f"panel_px(200dpi) [{X0/f:.1f}, {Y0/f:.1f}, {X1/f:.1f}, {Y1/f:.1f}] snapped(l,t,r,b)={oks}  px/mm {kx/f:.4f} {ky/f:.4f}")
    sub=a[int(Y0):int(Y1)+1, int(X0):int(X1)+1]
    out={}
    for name,m in classes(sub).items():
        if m.sum()< (minmm*kx)**2: continue
        lab,n=ndi.label(m); sl=ndi.find_objects(lab); comps=[]
        for i,s in enumerate(sl):
            w=(s[1].stop-s[1].start)/kx; hh=(s[0].stop-s[0].start)/ky
            if max(w,hh)<minmm or min(w,hh)<0.25*minmm: continue
            if (lab[s]==i+1).sum() < 0.08*(s[1].stop-s[1].start)*(s[0].stop-s[0].start) and max(w,hh)<0.5*max(W,H): continue
            comps.append([s[1].start/kx, s[0].start/ky, s[1].stop/kx, s[0].stop/ky, int((lab[s]==i+1).sum())])
        out[name]=comps
    return out,(X0/f,Y0/f,X1/f,Y1/f)
def lines(comps, W):
    comps=sorted(comps,key=lambda c:(c[1],c[0])); L=[]
    for c in comps:
        for l in L:
            ov=min(l[3],c[3])-max(l[1],c[1])
            if ov>0.5*min(l[3]-l[1],c[3]-c[1]): l[0]=min(l[0],c[0]);l[1]=min(l[1],c[1]);l[2]=max(l[2],c[2]);l[3]=max(l[3],c[3]);l[4].append(c);break
        else: L.append([c[0],c[1],c[2],c[3],[c]])
    return L
def report(out, W, H):
    for name,comps in out.items():
        print("==",name)
        frames=[c for c in comps if any(o is not c and o[0]>=c[0]-.3 and o[1]>=c[1]-.3 and o[2]<=c[2]+.3 and o[3]<=c[3]+.3 for o in comps)]
        for c in frames: print(f"  FRAME x {c[0]:.1f}-{c[2]:.1f} y {c[1]:.1f}-{c[3]:.1f}  ({c[2]-c[0]:.1f} x {c[3]-c[1]:.1f})")
        rest=[c for c in comps if c not in frames]
        for l in lines(rest,W)[:30]:
            cs=sorted(l[4],key=lambda c:c[0])
            if len(cs)>40: print(f"  group x {l[0]:.1f}-{l[2]:.1f} y {l[1]:.1f}-{l[3]:.1f} ({len(cs)} comps)"); continue
            hh=l[3]-l[1]; words=[]; cur=[cs[0][0],cs[0][2]]
            for c in cs[1:]:
                if c[0]-cur[1]>0.42*hh: words.append(cur); cur=[c[0],c[2]]
                else: cur[1]=max(cur[1],c[2])
            words.append(cur)
            print(f"  x {l[0]:.1f}-{l[2]:.1f} (w {l[2]-l[0]:.1f}, R {W-l[2]:.1f})  y {l[1]:.1f}-{l[3]:.1f} (h {hh:.1f}, B {H-l[3]:.1f})  n={len(cs)}  words: "+" | ".join(f"{a:.1f}-{b:.1f} ({b-a:.1f})" for a,b in words))
def prof(code, box200, W, H, x=None, y=None, dpi=800):
    im=h.page_img(code,dpi); a=np.asarray(im); f=dpi/200
    X0,Y0,X1,Y1=[v*f for v in box200]; kx=(X1-X0)/W; ky=(Y1-Y0)/H
    cl=classes(a); res=[]
    if y is not None: n=int(X1-X0); pts=[(int(Y0+y*ky), int(X0+i)) for i in range(n)]; k=kx
    else: n=int(Y1-Y0); pts=[(int(Y0+i), int(X0+x*kx)) for i in range(n)]; k=ky
    cur=None
    for i,(yy,xx) in enumerate(pts):
        c=next((nm for nm,m in cl.items() if m[yy,xx]),None)
        if c!=cur:
            if cur: res[-1][2]=i/k
            if c: res.append([c,i/k,None])
            cur=c
    if cur: res[-1][2]=n/k
    return [(c,round(a_,1),round(b_,1)) for c,a_,b_ in res]
if __name__=="__main__":
    code=sys.argv[1]; box=[float(v) for v in sys.argv[2:6]]; W,H=float(sys.argv[6]),float(sys.argv[7])
    if "--view" in sys.argv: box=[v*1653/1413 for v in box]
    out,_=run(code,box,W,H,norefine="--norefine" in sys.argv)
    report(out,W,H)
