"""auto.py — measurement-led spec drafting for SA sheets: sign located by its ground colour (or outline), legend ink measured at 1200 dpi,
text lines matched to the legend given, letter height from the ink, series from the FHWA widths; symbols traced at high dpi."""
import os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h, meas, mk, sym as symmod
from scipy import ndimage as ndi
R2=math.sqrt(2)
_img={}
SRC="fills"
def page(code,dpi):
    if (code,dpi,SRC) not in _img: _img[(code,dpi,SRC)]=np.asarray((h.fills_img if SRC=="fills" else h.page_img)(code,dpi))
    return _img[(code,dpi,SRC)]
GROUND={"yellow":"orange/yellow","orange":"orange/yellow","yellowgreen":"orange/yellow","red":"red","green":"green","blue":"blue","brown":"brown"}
class Auto:
    def __init__(s,code,size,approx=None,ground="yellow",diamond=False,radius=50,view=True,dpi=1200,open_px=0,minmm=1.5,which_big=True,pp=None):
        s.code=code; s.ground=ground; s.diamond=diamond; s.radius=radius; s.dpi=dpi; s.log=[]; s.used=set()
        if diamond: side=size if isinstance(size,(int,float)) else size[0]; s.W=s.H=round(side*R2,2)
        else: s.W,s.H=size
        approx_given=approx
        if approx is None: approx=(30,30,1620,1960); view=False
        box=[v*1653/1413 for v in approx] if view else list(approx)
        a=page(code,300); f=1.5; pad=25
        x0,y0,x1,y1=[int(v*f) for v in (box[0]-pad,box[1]-pad,box[2]+pad,box[3]+pad)]
        x0=max(0,x0); y0=max(0,y0)
        sub=a[y0:y1,x0:x1]
        if approx_given is None and ground in ('white','none','black'): a=a[:int(a.shape[0]*0.80)]
        if pp is not None: s.pp=list(pp)
        elif ground in ("white","none","black") and approx_given is None:
            # the black border ring (or black ground): the black component whose bbox has the sign's aspect, largest first
            m=meas.classes(a)["black"]; lab,n=ndi.label(m); best=None
            for i,o in enumerate(ndi.find_objects(lab)):
                w_=o[1].stop-o[1].start; h_=o[0].stop-o[0].start
                if w_<60 or h_<60: continue
                if abs((w_/h_)/(s.W/s.H)-1)>0.06: continue
                if best is None or w_*h_>best[0]: best=(w_*h_,o)
            if best is None: raise SystemExit(f"{code}: no black border ring with aspect {s.W/s.H:.2f} found")
            o=best[1]; F6=dpi/200; A6=page(code,dpi)
            bx0,by0,bx1,by1=o[1].start/f,o[0].start/f,o[1].stop/f,o[0].stop/f
            def bedge(v,lo,hi,axis,first):
                ts=[]
                for t in range(int((v-3)*F6),int((v+3)*F6)):
                    strip=A6[t,int(lo*F6):int(hi*F6)] if axis==1 else A6[int(lo*F6):int(hi*F6),t]
                    if (strip.max(axis=1)<110).mean()>0.3: ts.append(t)
                return ((ts[0] if first else ts[-1]+1)/F6) if ts else v
            mx0=bx0+0.3*(bx1-bx0); mx1=bx0+0.7*(bx1-bx0); my0=by0+0.3*(by1-by0); my1=by0+0.7*(by1-by0)
            s.pp=[bedge(bx0,my0,my1,0,True),bedge(by0,mx0,mx1,1,True),bedge(bx1,my0,my1,0,False),bedge(by1,mx0,mx1,1,False)]
        elif ground in ("white","none","black"):
            (X0,Y0,X1,Y1),oks=meas.refine(page(code,600),box,3.0)
            s.pp=[X0/3,Y0/3,X1/3,Y1/3]
            if not all(oks): s.log.append(f"outline not snapped {oks}")
        else:
            m=meas.classes(sub)[GROUND[ground]]
            if ground=="yellowgreen":
                r,g,b=[sub[...,i].astype(int) for i in range(3)]; m=(g>170)&(b<120)&(r>120)
            m=ndi.binary_dilation(m,structure=np.ones((11,11),bool))
            lab,n=ndi.label(m)
            if n==0: raise SystemExit(f"{code}: no {ground} ground near {box}")
            objs=ndi.find_objects(lab); areas=[(o[0].stop-o[0].start)*(o[1].stop-o[1].start) for o in objs]; big=int(np.argmax(areas))+1   # the edge strip rings the ground: largest bbox
            sl=objs[big-1]
            if not diamond:   # ground split into sub-panels by black bars: take every ground piece joined to the biggest through black
                both=m|ndi.binary_dilation(meas.classes(sub)["black"],structure=np.ones((3,3),bool))
                lab2,n2=ndi.label(both); l2=lab2[sl][lab[sl]==big][0]
                ys_,xs_=np.nonzero((lab2==l2)&m)
                sl=(slice(ys_.min(),ys_.max()+1),slice(xs_.min(),xs_.max()+1))
            # refine at 1200 dpi around the bbox
            bx0,by0,bx1,by1=[(x0+sl[1].start+5)/f,(y0+sl[0].start+5)/f,(x0+sl[1].stop-5)/f,(y0+sl[0].stop-5)/f]
            A=page(code,dpi); F=dpi/200; q=6
            def edge(lo,hi,fixed0,fixed1,axis,first):
                # scan for first/last row/col containing ground colour, near the estimate
                vals=[]
                for t in range(int((lo-q)*F),int((lo+q)*F)):
                    strip = A[t, int(fixed0*F):int(fixed1*F)] if axis==1 else A[int(fixed0*F):int(fixed1*F), t]
                    mm=meas.classes(strip[None,...])[GROUND[ground]] if ground!="yellowgreen" else ((strip[...,1].astype(int)>170)&(strip[...,2].astype(int)<120)&(strip[...,0].astype(int)>120))[None,...]
                    vals.append((t,mm.any()))
                ts=[t for t,v in vals if v]
                return ((ts[0] if first else ts[-1]+1)/F) if ts else lo
            X0=edge(bx0,None,by0,by1,0,True); X1=edge(bx1,None,by0,by1,0,False); Y0=edge(by0,None,bx0,bx1,1,True); Y1=edge(by1,None,bx0,bx1,1,False)
            if diamond:   # the drawn tips are rounder than stated: locate the sharp diamond from its straight edges (u = x+y, v = x-y extents)
                comp=(lab[sl]==big)&meas.classes(sub[sl])[GROUND[ground]] if ground!="yellowgreen" else (lab[sl]==big)
                if ground=="yellowgreen":
                    q_=sub[sl]; comp=comp&(q_[...,1].astype(int)>170)&(q_[...,2].astype(int)<120)&(q_[...,0].astype(int)>120)
                ys_,xs_=np.nonzero(comp); xs_=(xs_+x0+sl[1].start)/f; ys_=(ys_+y0+sl[0].start)/f
                u=xs_+ys_; v=xs_-ys_; um,uM,vm,vM=u.min(),u.max()+1/f,v.min(),v.max()+1/f
                cx=((um+uM)/2+(vm+vM)/2)/2; cy=((um+uM)/2-(vm+vM)/2)/2; d=((uM-um)+(vM-vm))/4
                X0,X1,Y0,Y1=cx-d,cx+d,cy-d,cy+d
            if not diamond:   # a black border with no edge strip lies outside the ground: walk out over it
                A=page(code,dpi); F=dpi/200
                def blk(x,y):
                    p=A[int(y),int(x)]; return int(p[0])<110 and int(p[1])<110 and int(p[2])<110
                def walk(x,y,dx,dy):
                    n=0
                    while n<F*60 and 0<=int(y+dy*(n+1))<A.shape[0] and 0<=int(x+dx*(n+1))<A.shape[1] and blk(x+dx*(n+1),y+dy*(n+1)): n+=1
                    return n/F
                my=(Y0+Y1)/2*F; mx=(X0+X1)/2*F; q=0.31
                wl=sorted(walk(X0*F-1,Y0*F+f_*(Y1-Y0)*F,-1,0) for f_ in (0.31,0.5,0.69))[1]; wr=sorted(walk(X1*F,Y0*F+f_*(Y1-Y0)*F,1,0) for f_ in (0.31,0.5,0.69))[1]
                wt=sorted(walk(X0*F+f_*(X1-X0)*F,Y0*F-1,0,-1) for f_ in (0.31,0.5,0.69))[1]; wb=sorted(walk(X0*F+f_*(X1-X0)*F,Y1*F,0,1) for f_ in (0.31,0.5,0.69))[1]
                X0-=wl; X1+=wr; Y0-=wt; Y1+=wb
            s.pp=[X0,Y0,X1,Y1]
        s.kx=(s.pp[2]-s.pp[0])/s.W; s.ky=(s.pp[3]-s.pp[1])/s.H
        if abs(s.kx/s.ky-1)>0.012: s.log.append(f"ASPECT off: kx {s.kx:.4f} ky {s.ky:.4f}")
        # components
        A=page(code,dpi); F=dpi/200
        X0,Y0,X1,Y1=[v*F for v in s.pp]; kx=(X1-X0)/s.W; ky=(Y1-Y0)/s.H
        sub=A[int(Y0):int(Y1)+1,int(X0):int(X1)+1]; s.out={}; s.hair={}
        for name,m in meas.classes(sub).items():
            hair=[]
            if open_px: m=ndi.binary_opening(m,structure=np.ones((open_px,open_px),bool))
            if m.sum()<(minmm*kx)**2: continue
            lab,n=ndi.label(m); comps=[]
            for i,sl in enumerate(ndi.find_objects(lab)):
                w=(sl[1].stop-sl[1].start)/kx; hh=(sl[0].stop-sl[0].start)/ky
                if max(w,hh)<minmm: continue
                if w>0.8*s.W and hh>0.8*s.H: continue      # border ring / ground
                if name=="black" and (w>0.9*s.W or hh>0.9*s.H) and (lab[sl]==i+1).mean()<0.15: continue   # a piece of the border ring
                c=[sl[1].start/kx,sl[0].start/ky,sl[1].stop/kx,sl[0].stop/ky]
                if diamond:
                    cx=(c[0]+c[2])/2; cy=(c[1]+c[3])/2
                    if abs(cx-s.W/2)+abs(cy-s.H/2) > s.W/2-(0.04*s.W/R2+2)*R2: continue   # outside the ground (dimension lines, border pieces)
                    if w>0.45*s.W and hh>0.45*s.H and (lab[sl]==i+1).mean()<0.08: continue
                thin=min(w,hh)*s.kx*0.127
                if thin<0.45 and max(w,hh)/max(0.01,min(w,hh))>2.5: hair.append(c); continue
                comps.append(c)
            if comps: s.out[name]=comps
            if hair: s.hair[name]=hair
    # ---- measured border layers
    def edges(s):
        A=page(s.code,s.dpi); F=s.dpi/200; X0,Y0,X1,Y1=[v*F for v in s.pp]
        if s.diamond:   # walk in from the left tip along the horizontal centre line
            y=int((Y0+Y1)/2); row=A[y-2:y+3,int(X0):int(X0+0.25*(X1-X0))]
        else:
            y=int(Y0+0.5*(Y1-Y0)); row=A[y-2:y+3,int(X0):int(X0+0.3*(X1-X0))]
            if meas.classes(row)["black"][2].mean()>0.5: y=int(Y0+0.37*(Y1-Y0)); row=A[y-2:y+3,int(X0):int(X0+0.3*(X1-X0))]
        cl=meas.classes(row); k=(X1-X0)/s.W; runs=[]; cur=None
        for i in range(row.shape[1]):
            c=next((n for n,m in cl.items() if m[2,i]),"white" if row[2,i].min()>200 else None)
            if c!=cur or not runs: runs.append([c,i/k,None]); cur=c
            runs[-1][2]=(i+1)/k
        div=R2 if s.diamond else 1
        off=s.radius*(R2-1)*R2 if s.diamond else 0   # rounded tip starts this far in along the centre line
        res=[(c,round((a-off)/div,1),round((b-off)/div,1)) for c,a,b in runs if c and b-a>0.4][:5]
        return res
    # ---- clustering
    def comps(s,cls): return [c for c in s.out.get(cls,[]) if id(c) not in s.used]
    def clusters(s,cls,gapx=None,xr=None):
        cs=sorted([c for c in s.comps(cls) if xr is None or xr[0]<=c[0]<=xr[1]],key=lambda c:(c[1],c[0])); L=[]
        for c in cs:
            for l in L:
                ov=min(l[3],c[3])-max(l[1],c[1])
                if ov>0.5*min(l[3]-l[1],c[3]-c[1]): l[0]=min(l[0],c[0]);l[1]=min(l[1],c[1]);l[2]=max(l[2],c[2]);l[3]=max(l[3],c[3]);l[4].append(c);break
            else: L.append([c[0],c[1],c[2],c[3],[c]])
        L.sort(key=lambda l:l[1])
        for l in L: l[4].sort(key=lambda c:c[0])
        return L
    def show(s):
        for cls in s.out:
            for l in s.clusters(cls):
                print(f"   {cls:6s} y {l[1]:.1f}-{l[3]:.1f} x {l[0]:.1f}-{l[2]:.1f} n={len(l[4])} "+" ".join(f"{c[0]:.0f}+{c[2]-c[0]:.0f}x{c[3]-c[1]:.0f}" for c in l[4][:16]))
    # ---- text
    @staticmethod
    def nglyph(t): return sum(2 if ch in "ij:;=\"" else 3 if ch=="%" else 1 for ch in t if ch!=" ")
    def line(s,cls,text,cluster=None,colour=None,series=None,height=None,y=None,centre_tol=1.2,xr=None,fix=None):
        series0,height0=series,height
        """place one legend line (words split on spaces) on a measured cluster (next unused one by default)"""
        cl=s.clusters(cls,xr=xr)
        if y is not None: l=min(cl,key=lambda l:abs(l[1]-y))
        else:
            need=s.nglyph(text); l=next((l for l in cl if len(l[4])==need-text.count("-") or len(l[4])==need),None)
            if l is None: raise SystemExit(f"{s.code}: no unused {cls} cluster with {need} glyphs for {text!r}: "+str([(round(l[1]),len(l[4])) for l in cl]))
        cs=l[4]; need=s.nglyph(text)
        if "-" in text and len(cs)<need:   # dashes are hairline-thin at sheet scale: fetch them from the hairline list
            hs=[c for c in s.hair.get(cls,[]) if l[1]<=(c[1]+c[3])/2<=l[3] and l[0]<c[0]<l[2] and (c[2]-c[0])>2*(c[3]-c[1])]
            cs=sorted(cs+hs,key=lambda c:c[0]); l[4]=cs
        if len(cs)!=need: raise SystemExit(f"{s.code}: {text!r} needs {need} glyphs, cluster at y {l[1]:.0f} has {len(cs)}")
        words=text.split(" "); els=[]; i=0
        for wd in words:
            n=s.nglyph(wd); wc=cs[i:i+n]; i+=n
            for c in wc: s.used.add(id(c))
            hs=sorted(c[3]-c[1] for c in wc); hs=[v for v in hs if v>0.6*hs[-1]]; hm=max(hs)/1.035 if any(ch.islower() for ch in wd) else (hs[0] if all(ch in 'OCSGQJU0368925&' for ch in wd) is False else hs[0]/1.03)
            if fix and wd in fix: series,height=fix[wd]
            else: series,height=series0,height0
            if height: H=height
            else:
                H=round(hm/5)*5 if abs(hm-round(hm/5)*5)<=max(1.6,0.025*hm) else round(hm)
            flat=[c for c in wc if hs[0]*0.99<=(c[3]-c[1])<=hs[0]*1.012] or wc
            base=sorted(c[3] for c in flat)[len(flat)//2]
            if any(ch in "gjpqy," for ch in wd) : base=min(c[3] for c in wc)
            top=round((base-H)*2)/2
            mw=wc[-1][2]-wc[0][0]
            if series: S=series; fw=mk.ink(wd,S,H)
            else:
                cand=sorted(((abs(mk.ink(wd,S_,H)-mw),S_) for S_ in (("E","Emod","D","C","B","F") if any(ch.islower() for ch in wd) else ("B","C","D","E","F"))))
                S=cand[0][1]; fw=mk.ink(wd,S,H)
            flag="" if abs(fw-mw)<=max(2.0,0.025*mw) else "  **WIDTH**"
            s.log.append(f"{wd} {H}{S} top {top} x {wc[0][0]:.1f} ink {mw:.1f} (font {fw}){flag}")
            x=round(wc[0][0]+(mw-fw)/2,1)   # centre the font's ink on the measured ink
            e=mk.T(wd,S,H,top,align="left",x=x)
            if colour and colour!="black": e["colour"]=colour
            els.append((e,wc[0][0],wc[-1][2],H,S,top,mw))
        # single centred word -> centred element
        out=[]
        if len(els)==1 and abs((els[0][1]+els[0][2])/2-s.W/2)<centre_tol:
            e=els[0][0]; e.pop("align"); e.pop("x"); out=[e]
        else: out=[e[0] for e in els]
        s.last=els
        return out
    def lines(s,cls,texts,colour=None,**kw):
        out=[]
        for t in texts: out+=s.line(cls,t,colour=colour,**kw)
        return out
    # ---- symbols
    def trace(s,cls,sid,cluster_y=None,pad=2.0,colours=None,box=None,force=True,open_=0,threshold=110,invert=False,take=None,dpi=1000,inset_mm=None,exclude=None,bg=255,drop_small=0):
        """trace the unused comps of a cluster (or everything unused in `box` mm) as one symbol; returns the placed element"""
        if box is None:
            cl=s.clusters(cls)
            l=min(cl,key=lambda l:abs(l[1]-cluster_y)) if cluster_y is not None else max(cl,key=lambda l:(l[2]-l[0])*(l[3]-l[1]))
            cs=l[4]
        else:
            cs=[c for c in s.comps(cls) if c[0]>=box[0] and c[2]<=box[2] and c[1]>=box[1] and c[3]<=box[3]]
        if not cs: raise SystemExit(f"{s.code}: nothing to trace for {sid}")
        for c in cs: s.used.add(id(c))
        if drop_small: cs=[c for c in cs if max(c[2]-c[0],c[3]-c[1])>=drop_small] or cs
        x0=min(c[0] for c in cs); y0=min(c[1] for c in cs); x1=max(c[2] for c in cs); y1=max(c[3] for c in cs)
        outp=os.path.join(symmod.T.SYM_DIR,sid+".svg")
        if force or not os.path.exists(outp):
            from PIL import Image
            F=dpi/200; a=np.array(page(s.code,dpi)); X0,Y0,X1,Y1=[v*F for v in s.pp]; kx=(X1-X0)/s.W; ky=(Y1-Y0)/s.H
            px0=int(X0+(x0-pad)*kx)-4; py0=int(Y0+(y0-pad)*ky)-4; px1=int(X0+(x1+pad)*kx)+5; py1=int(Y0+(y1+pad)*ky)+5
            sub=a[py0:py1,px0:px1].copy()
            yy,xx=np.mgrid[py0:py1,px0:px1]; mx=(xx-X0)/kx; my=(yy-Y0)/ky
            if s.diamond: inside=np.abs(mx-s.W/2)+np.abs(my-s.H/2)<=s.W/2-(inset_mm if inset_mm is not None else 30)*R2-3
            else:
                g=(inset_mm if inset_mm is not None else 0); inside=(mx>=g)&(mx<=s.W-g)&(my>=g)&(my<=s.H-g)
            inside&=(mx>=x0-pad)&(mx<=x1+pad)&(my>=y0-pad)&(my<=y1+pad)
            if not s.diamond and s.radius:   # outside the rounded corners (leader arrowheads touch them)
                r_=max(0.0,s.radius-(inset_mm or 0)); g_=(inset_mm or 0)
                dx=np.maximum(np.maximum(g_+r_-mx,mx-(s.W-g_-r_)),0); dy=np.maximum(np.maximum(g_+r_-my,my-(s.H-g_-r_)),0)
                inside&=(dx*dx+dy*dy)<=(r_+0.3)**2
            if exclude:
                for ex in exclude: inside&=~((mx>=ex[0])&(mx<=ex[2])&(my>=ex[1])&(my<=ex[3]))
            if not isinstance(bg,int):   # white artwork on a coloured ground: drop the hairline seams between the CAD's fill bands
                sub=ndi.median_filter(sub,size=(7,7,1))
            sub[~inside]=bg
            if drop_small:   # dimension arrowheads lying on the ground: dark components smaller than drop_small mm
                dk=sub.max(axis=2)<110; lb,nn=ndi.label(dk)
                for j,o in enumerate(ndi.find_objects(lb)):
                    if max((o[1].stop-o[1].start)/kx,(o[0].stop-o[0].start)/ky)<drop_small: sub[o][lb[o]==j+1]=bg
            M=int(0.04*max(sub.shape[:2]))+20; img=Image.new("RGB",(sub.shape[1]+2*M,sub.shape[0]+2*M),"white" if bg==255 else tuple(bg)); img.paste(Image.fromarray(sub),(M,M)); symmod.T.UPSCALE=2
            kw={}
            if colours: kw["colours"]=colours
            r=symmod.T._trace_from_panel(img,(M,M,M+(px1-px0)-1,M+(py1-py0)-1),0,(0,0,(px1-px0)/kx,(py1-py0)/ky,(px1-px0)/kx,(py1-py0)/ky),sid,outp,None,threshold,invert,open_px=open_,keep_specks=True,**kw)
        w,hh=mk.symbox(sid)
        s.log.append(f"symbol {sid}: ink x {x0:.1f}-{x1:.1f} y {y0:.1f}-{y1:.1f} ({x1-x0:.1f} x {y1-y0:.1f}); traced {w:.1f} x {hh:.1f}")
        return mk.sym(sid,round((x0+x1)/2-w/2,1),round((y0+y1)/2-hh/2,1),round(w,1),round(hh,1))
    def reuse(s,cls,sid,cluster_y=None,colour="black",box=None):
        """place an existing symbol on a measured cluster's bbox (aspect kept, fitted to width)"""
        if box is None:
            cl=s.clusters(cls); l=min(cl,key=lambda l:abs(l[1]-cluster_y)) if cluster_y is not None else max(cl,key=lambda l:(l[2]-l[0])*(l[3]-l[1])); cs=l[4]
        else: cs=[c for c in s.comps(cls) if c[0]>=box[0] and c[2]<=box[2] and c[1]>=box[1] and c[3]<=box[3]]
        for c in cs: s.used.add(id(c))
        x0=min(c[0] for c in cs); y0=min(c[1] for c in cs); x1=max(c[2] for c in cs); y1=max(c[3] for c in cs)
        w,hh=mk.symbox(sid); sc=min((x1-x0)/w,(y1-y0)/hh)
        s.log.append(f"reuse {sid}: ink {x1-x0:.1f} x {y1-y0:.1f} at ({x0:.1f},{y0:.1f}); symbol {w:.0f} x {hh:.0f} scale {sc:.3f} (aspect ink {(x1-x0)/(y1-y0):.3f} vs {w/hh:.3f})")
        return mk.sym(sid,round((x0+x1)/2-w*sc/2,1),round((y0+y1)/2-hh*sc/2,1),round(w*sc,1),round(hh*sc,1),colour)
    def rest(s):
        return [(cls,[round(v,1) for v in c]) for cls in s.out for c in s.comps(cls) if max(c[2]-c[0],c[3]-c[1])>3]

def verify(A, els, cls="black", tol=2.5, quiet=False):
    """compare stated text elements with the measured ink: prints deviations over tol (mm)"""
    bad=[]
    allc=[c for k,cl in A.out.items() if k!="orange/yellow" for c in cl if c[2]-c[0]<0.4*A.W]+[c for cl in A.hair.values() for c in cl]
    for e in els:
        if e.get("type")!="text": continue
        runs=e.get("runs") or [{"text":w} for w in e.get("words",[e.get("text")])]
        if any("{" in r["text"] for r in runs): continue
        gap=e.get("gap",0); gaps=gap if isinstance(gap,list) else [gap]*(len(runs)-1)
        ws=[mk.ink(r["text"],r.get("series",e.get("series")),r.get("height",e.get("height"))) for r in runs]
        tot=sum(ws)+sum(gaps); H=max(r.get("height",e.get("height")) for r in runs)
        al=e.get("align","center")
        x0=e.get("cx",A.W/2)-tot/2 if al=="center" else (e["x"] if al=="left" else e["x"]-tot)
        y0=e["top"]; y1=y0+H
        cs=[c for c in allc if c[1]<y1-0.3*H and c[3]>y0+0.3*H and c[2]>x0-0.2*H and c[0]<x0+tot+0.2*H and (c[3]-c[1])>0.5*H]
        if not cs: bad.append(f"{runs[0]['text']}: no ink found at y {y0}"); continue
        mx0=min(c[0] for c in cs); mx1=max(c[2] for c in cs); my0=sorted(c[1] for c in cs)[len(cs)//2]; my1=sorted(c[3] for c in cs)[len(cs)//2]
        d=dict(dx0=mx0-x0,dx1=mx1-(x0+tot),dtop=my0-y0,dbase=my1-y1)
        if any(abs(v)>tol for v in d.values()): bad.append(" ".join(r["text"] for r in runs)+": "+" ".join(f"{k} {v:+.1f}" for k,v in d.items()))
    if bad and not quiet: print("  VERIFY",A.code,"; ".join(bad))
    return bad

def letters(A, word, series, H, top, cls="black", colour=None, xr=None):
    """one element per letter, each centred on the letter's measured ink (the sheet's own letter spacing)"""
    cs=[c for c in A.out.get(cls,[]) if c[1]<top+0.7*H and c[3]>top+0.3*H and (c[3]-c[1])>0.6*H and (xr is None or xr[0]<=c[0]<=xr[1])]
    cs.sort(key=lambda c:c[0]); n=Auto.nglyph(word)
    if len(cs)!=n: raise SystemExit(f"{A.code}: letters {word!r}: {len(cs)} comps at top {top}")
    out=[]
    for ch,c in zip(word.replace(" ",""),cs):
        w=mk.ink(ch,series,H); e=mk.T(ch,series,H,top,align="left",x=round((c[0]+c[2])/2-w/2,1))
        if colour: e["colour"]=colour
        out.append(e)
    return out

def slash(A, near_x, near_y, cls="black", colour="black", bbox=None, t=None):
    """the oblique stroke of km/h as a parallelogram on the measured ink (bbox + horizontal thickness at mid-height)"""
    cs=[c for c in A.out.get(cls,[]) if c[0]-5<=near_x<=c[2]+5 and c[1]<=near_y<=c[3] and (c[3]-c[1])>1.3*(c[2]-c[0])*0.8]
    if bbox: x0,y0,x1,y1=bbox
    else:
        c=max(cs,key=lambda c:c[3]-c[1]); x0,y0,x1,y1=c
    r=[q for q in meas.prof(A.code,A.pp,A.W,A.H,y=(y0+y1)/2,dpi=1200) if q[0]==cls and x0-1<=q[1] and q[2]<=x1+1]
    t=t or (r[0][2]-r[0][1] if r else 0.22*(x1-x0))
    A.log.append(f"slash bbox x {x0:.1f}-{x1:.1f} y {y0:.1f}-{y1:.1f} thickness {t:.1f}")
    return mk.poly([(round(x1-t,1),round(y0,1)),(round(x1,1),round(y0,1)),(round(x0+t,1),round(y1,1)),(round(x0,1),round(y1,1))],colour)
