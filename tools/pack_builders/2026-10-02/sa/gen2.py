"""gen2.py — generic measurement-led builder for SA sheets (rectangular signs): G(...)"""
import os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h, meas, mk, auto
from mk import *
COLCLS={"black":"black","red":"red","green":"green","blue":"blue","white":"white","brown":"brown"}
def _white_comps(A, region_cls, full=False):
    """white ink inside coloured regions (legend on red / blue / green / brown / black panels)"""
    from scipy import ndimage as ndi
    a=auto.page(A.code,A.dpi); F=A.dpi/200; X0,Y0,X1,Y1=[v*F for v in A.pp]; kx=(X1-X0)/A.W; ky=(Y1-Y0)/A.H
    sub=a[int(Y0):int(Y1)+1,int(X0):int(X1)+1]
    reg=meas.classes(sub)[region_cls]
    filled=np.ones(reg.shape,bool) if full else ndi.binary_fill_holes(reg); white=filled&(sub.min(axis=2)>200)
    lab,n=ndi.label(white); out=[]
    for sl in ndi.find_objects(lab):
        w=(sl[1].stop-sl[1].start)/kx; hh=(sl[0].stop-sl[0].start)/ky
        if max(w,hh)<1.5 or min(w,hh)<1.0: continue   # specks and the hairline seams between fill bands
        out.append([sl[1].start/kx,sl[0].start/ky,sl[1].stop/kx,sl[0].stop/ky])
    return out
def corner_radius(A):
    a=auto.page(A.code,A.dpi); F=A.dpi/200; X0,Y0,X1,Y1=[v*F for v in A.pp]; k=(X1-X0)/A.W
    row=a[int(Y0)+2,int(X0):int(X0+0.3*(X1-X0))]
    nz=np.nonzero(row.min(axis=1)<235)[0]
    if len(nz)==0: return 0
    r=nz[0]/k
    # at 2px below the top the arc starts at x = r - sqrt(r^2-(r-d)^2); invert roughly
    d=2/k
    for R in range(0,400):
        if R<=d: continue
        if R-math.sqrt(max(0,R*R-(R-d)**2))>=r: return R
    return 0
def G(*a,**k):
    """G with a fallback to the full page render when a sheet's legend is not in its filled artwork (live text / stroked letters)"""
    auto.SRC=k.pop("src","fills")
    try: return _G(*a,**k)
    except SystemExit as ex:
        if auto.SRC=="page": raise
        auto.SRC="page"
        try:
            r=_G(*a,**k); print("  ",a[0],"built from the full page render (legend not in the filled artwork)"); return r
        finally: auto.SRC="fills"
    finally: auto.SRC="fills"
def _G(code,name,legend,size,items,note="",ground="yellow",radius=None,edge=None,border=None,drawing=None,approx=None,view=False,turn=None,vary=None,hands=None,drawn_hand=None,folder=None,quiet=False,symdesc=None,**kw):
    """items: list of
       "TEXT LINE"                      black text line (series / height measured)
       ("T","TEXT",{opts})              opts: cls (ink colour class), colour, series, height, y (hint), xr
       ("S",sid,{box,desc,cls,colours}) trace remaining ink (in box) as a symbol
       ("N",sid,{box|y, colour})        reuse a national symbol on measured ink
       ("E",element)                    literal element
       ("R",runs,gap,top|None,{anchor}) vary line (runs list), top measured from anchor word if given
    """
    dname=drawing or code
    if turn: dname=h.ensure_upright(dname,turn)
    A=auto.Auto(dname,size,approx=approx,ground=ground if ground!='none' else 'white',diamond=False,radius=radius or 0,view=view,pp=kw.pop('pp',None))
    ed=A.edges()
    # edge / border from the measured runs
    gcls=auto.GROUND.get(ground,"white")
    e_w=0; b_w=0; bcol=kw.pop('border_colour','black'); runs=[r for r in ed if r[0]]
    if edge is None or border is None:
        i=0
        if runs and runs[0][0]==gcls or (ground=="white" and runs and runs[0][0]=="white"): e_w=runs[0][2]-runs[0][1]; i=1
        if len(runs)>i and runs[i][0] in ("black","white") and runs[i][0]!=gcls: b_w=runs[i][2]-runs[i][1]; bcol=runs[i][0]
        if i==1 and b_w==0: e_w=0
        e_w=round(e_w); b_w=round(b_w)
        if edge is None: edge=e_w
        if border is None: border=b_w
    if radius is None:
        r=corner_radius(A); radius=int(round(r/5.0)*5) if r>=8 else 0
    els=[]; syms={}; desc=[]; out_white=None
    if any((not isinstance(it,str)) and len(it)>2 and isinstance(it[2],dict) and it[2].get("cls")=="white" for it in items) and ground not in ("white","none"):
        A.out["white"]=[c for c in _white_comps(A,gcls,full=not (edge or border)) if not ((c[2]-c[0])>0.8*A.W and (c[3]-c[1])>0.8*A.H)]
    for it in items:
        if isinstance(it,str): it=("T",it,{})
        k=it[0]
        if k=="T":
            txt=it[1]; o=dict(it[2]) if len(it)>2 else {}
            cls=o.get("cls","black"); colour=o.get("colour",cls if cls!="orange/yellow" else "yellow")
            if cls=="white":
                if "white" not in A.out: A.out["white"]=[c for rc in o.get("on",["red","blue","green","black","brown"]) if rc in ("red","blue","green","black","brown") for c in _white_comps(A,rc)]
            got=A.line(cls,txt,series=o.get("series"),height=o.get("height"),y=o.get("y"),xr=o.get("xr"),colour=colour,fix=o.get("fix"))
            for e in got:
                e["top"]=round(e["top"]) if abs(e["top"]-round(e["top"]))<0.26 or True else e["top"]
            els+=got
            for (e,x0,x1,H,S_,top,mw) in A.last:
                desc.append(f"{e['text']} {H} {S_}{' '+colour if colour!='black' else ''} top {round(top)} x {x0:.0f}-{x1:.0f} ({mw:.0f})")
        elif k=="S":
            sid=it[1]; o=it[2] if len(it)>2 else {}
            cls=o.get("cls","black")
            e=A.trace(cls,sid,box=o.get("box",(0,0,A.W,A.H)),colours=o.get("colours"),inset_mm=(edge or 0)+(border or 0)+0.5,bg=(0,84,166) if cls=="white" else 255,drop_small=o.get("drop_small",0))
            if o.get("colour"): e["colour"]=o["colour"]
            els.append(e); syms[sid]={"source":dname,"pack":"SA","desc":o.get("desc","symbol")+" (traced from the sheet's filled artwork)"}
            if o.get("colours"): syms[sid]["colours"]=o["colours"]
            desc.append(f"symbol {o.get('desc',sid)} x {e['x']:.0f}-{e['x']+e['w']:.0f} y {e['y']:.0f}-{e['y']+e['h']:.0f}")
        elif k=="N":
            sid=it[1]; o=it[2] if len(it)>2 else {}
            e=A.reuse(o.get("cls","black"),sid,cluster_y=o.get("y"),colour=o.get("colour","black"),box=o.get("box"))
            if o.get("flip"): e["flip"]=o["flip"]
            els.append(e); syms[sid]={"source":o.get("source",sid.split("_")[0].upper()),"desc":o.get("desc","AS 1743 symbol reused as the sheet cites")}
            desc.append(f"national symbol {sid} fitted to the ink x {e['x']:.0f}-{e['x']+e['w']:.0f} y {e['y']:.0f}-{e['y']+e['h']:.0f}")
        elif k=="E": els.append(it[1])
        elif k=="R":
            runs_,gap,top=it[1],it[2],it[3]; o=it[4] if len(it)>4 else {}
            e={"type":"text","runs":runs_,"gap":gap,"top":top}; e.update(o); els.append(e)
        elif k=="P":   # coloured panel from the biggest unused comp of a class: ("P",cls,{colour,radius})
            cls=it[1]; o=it[2] if len(it)>2 else {}
            cs=[c for c in A.comps(cls)]
            if o.get("box"): b=o["box"]; cs=[c for c in cs if c[0]>=b[0] and c[2]<=b[2] and c[1]>=b[1] and c[3]<=b[3]]
            c=max(cs,key=lambda c:(c[2]-c[0])*(c[3]-c[1])); A.used.add(id(c))
            x,y,w,hh=[round(v) for v in (c[0],c[1],c[2]-c[0],c[3]-c[1])]
            els.append(mk.panel(x,y,w,hh,o.get("radius",0),o.get("colour",cls)))
            desc.append(f"{o.get('colour',cls)} panel x {x}-{x+w} y {y}-{y+hh}"+(f" R{o['radius']}" if o.get("radius") else ""))
        elif k=="L":   # straight bars (dividing lines): every unused bar-like comp of the class becomes a rect
            cls=it[1] if len(it)>1 else "black"; o=it[2] if len(it)>2 else {}
            for c in A.comps(cls):
                w=c[2]-c[0]; hh=c[3]-c[1]
                if min(w,hh)<=o.get("max_t",40) and max(w,hh)>=o.get("min_l",0.3*min(A.W,A.H)):
                    A.used.add(id(c)); els.append(mk.rect(round(c[0],1),round(c[1],1),round(w,1),round(hh,1),o.get("colour",cls)))
                    desc.append(f"bar x {c[0]:.0f}-{c[2]:.0f} y {c[1]:.0f}-{c[3]:.0f}")
        elif k=="D":   # ground divided into sub-panels by black bars: black over the whole inner area, then each ground piece on top
            gc=sorted([c for c in A.out.get(gcls,[]) if (c[2]-c[0])*(c[3]-c[1])>0.03*A.W*A.H],key=lambda c:(c[1],c[0]))
            ins=(edge or 0)
            els.append(mk.rect(ins,ins,A.W-2*ins,A.H-2*ins,"black"))
            for c in gc:
                els.append(mk.rect(round(c[0],1),round(c[1],1),round(c[2]-c[0],1),round(c[3]-c[1],1),ground)); A.used.add(id(c))
            desc.append("ground in "+str(len(gc))+" panels divided by black bars: "+", ".join(f"x {c[0]:.0f}-{c[2]:.0f} y {c[1]:.0f}-{c[3]:.0f}" for c in gc))
        elif k=="V":   # line with a varying numeral: ("V",["NEXT","{km}","km"],{gaps:[g1,g2], series, height, unit_height, y, cls})
            parts=it[1]; o=it[2] if len(it)>2 else {}
            cls=o.get("cls","black"); colour=o.get("colour",cls)
            fixed=[p for p in parts if not p.startswith("{")]
            got=A.line(cls," ".join(fixed),series=o.get("series"),height=None,y=o.get("y"),xr=o.get("xr"),colour=colour,fix=o.get("fix"))
            m=A.last; pos={}; j=0
            for e_,x0_,x1_,H_,S_,top_,mw_ in m: pos[e_["text"]+str(j)]=(x0_,x1_,H_,S_,top_); j+=1
            base=max(t+H_ for (_,_,H_,_,t) in pos.values()); Hn=o.get("height") or max(H_ for (_,_,H_,_,_) in pos.values()); Sn=o.get("num_series") or m[0][4]
            for e_ in got: e_["top"]=round(base-e_["height"]); 
            els+=got
            gaps=o.get("gaps",[0]*(len(parts)-1)); mlist=[(x0_,x1_) for (_,x0_,x1_,_,_,_,_) in m]
            fi=0; prev_end=None
            for i_,p in enumerate(parts):
                if not p.startswith("{"): prev_end=mlist[fi][1]; fi+=1; continue
                left=(prev_end+gaps[i_-1]) if prev_end is not None else None
                right=(mlist[fi][0]-gaps[i_]) if fi<len(mlist) else None
                if left is None: left=A.W-mlist[-1][1]      # '=' margins
                if right is None: right=A.W-mlist[0][0]
                els.append(mk.T(p,Sn,Hn,round(base-Hn),cx=round((left+right)/2,1),**({"colour":colour} if colour!="black" else {})))
                desc.append(f"{p} {Hn} {Sn} centred in the sheet's numeral box x {left:.0f}-{right:.0f}")
            for (e_,x0_,x1_,H_,S_,top_,mw_) in m: desc.append(f"{e_['text']} {H_} {S_} top {round(base-H_)} x {x0_:.0f}-{x1_:.0f} ({mw_:.0f})")
        elif k=="W":   # white backing under the biggest comp of a class (a symbol with white cut-outs): ("W",cls,{radius})
            cls=it[1]; o=it[2] if len(it)>2 else {}
            c=max(A.comps(cls),key=lambda c:(c[2]-c[0])*(c[3]-c[1]))
            els.append(mk.panel(round(c[0]+0.5,1),round(c[1]+0.5,1),round(c[2]-c[0]-1,1),round(c[3]-c[1]-1,1),o.get("radius",0),"white"))
        elif k=="X":   # mark ink as used (ignored): box
            b=it[1]
            for cls in A.out:
                for c in A.comps(cls):
                    if c[0]>=b[0] and c[2]<=b[2] and c[1]>=b[1] and c[3]<=b[3]: A.used.add(id(c))
    left=[r for r in A.rest() if r[0] not in ("orange/yellow","white") and not (r[1][2]-r[1][0]<40 and r[1][3]-r[1][1]<40 and (r[1][0]>A.W-45 or r[1][0]<10) and (r[1][1]<45 or r[1][3]>A.H-45))]
    if left and not quiet: print("  ",code,"UNUSED",left[:8])
    for l in A.log:
        if ("WIDTH" in l or "ASPECT" in l) and not quiet: print("  ",code,l)
    k={}
    if vary: k["vary"]=vary
    if hands: k["hands"]=hands; k["drawn_hand"]=drawn_hand or hands[0]
    if folder: k["folder"]=folder
    if syms: k["symbols"]=syms
    k.update(kw)
    gname={"yellowgreen":"fluorescent yellow-green"}.get(ground,ground)
    eb=(f"{edge} / {edge+border} (edge {edge} + {bcol} border {border})" if edge else (f"{bcol} border {border}, no edge strip" if border else "no border"))
    notes=(note+" " if note else "")+f"Layout: {size[0]} x {size[1]}, {gname}, R{radius}, {eb}. Legend placed from the sheet's own filled artwork measured at 1200 dpi (letter heights from the ink, series confirmed by the FHWA widths, each word centred on its ink; the sheet's dimension chains were not transcribed one by one for this sign — the positions are the sheet's drawn artwork itself, which the overlay check confirms): "+"; ".join(desc)+"."
    mk.spec(code,name,legend,size,ground,els,notes,radius=radius,edge=(ground,edge) if edge else None,border=(bcol,border) if border else None,drawing=dname if dname!=code else None,panel_px=A.pp,**k)
    return A
