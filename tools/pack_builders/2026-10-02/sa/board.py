"""board.py — hazard-marker boards / symbol plates: located by the drawn outline on the full page render, artwork traced from the filled artwork."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h, meas, mk, auto
from mk import *
from scipy import ndimage as ndi
def outlines(code, aspect, tol=0.03, minpx=40, dpi=600):
    """bboxes (200-dpi px) of stroked outline paths in the sheet's PDF whose bbox has the given aspect (the sign outline the CAD draws), reading order; falls back to filled shapes"""
    import pymupdf
    p=pymupdf.open(h.pdf_for(code))[0]; k=200/72; out=[]
    if abs(p.rect.width*k-np.asarray(h.page_img(code,50)).shape[1]*4)>20: return []   # sideways sheet: give pp by hand
    H80=p.rect.height*0.80
    for d in p.get_drawings():
        r=d["rect"]
        if r.width*k<minpx or r.height*k<minpx or r.y1>H80 or r.width>0.9*p.rect.width: continue
        if abs((r.width/r.height)/aspect-1)>tol: continue
        if d["type"]=="s" and len(d["items"])<3: continue
        b=(r.x0*k,r.y0*k,r.x1*k,r.y1*k)
        if not any(abs(b[0]-o[0])<3 and abs(b[1]-o[1])<3 and abs(b[2]-o[2])<3 and abs(b[3]-o[3])<3 for o in out): out.append(b)
    out.sort(key=lambda b:(round(b[1]/80),b[0]))
    return out
def tile(box,cols=4):
    """a box read off a 4-column montage tile (tile-local px) -> sheet px at 200 dpi"""
    k=(1900/cols)/(0.96*1653)
    return (box[0]/k+33,box[1]/k+47,box[2]/k+33,box[3]/k+47)
def snap(code, rough, size, artwork=True, pad=45, dpi=600):
    """sign outline (200-dpi px) near a rough box: bbox of the filled artwork inside the padded box (when it reaches every edge), then each side snapped to the drawn outline"""
    f=dpi/200; x0,y0,x1,y1=rough
    box=list(rough)
    if artwork:
        a2=np.asarray(h.fills_img(code,dpi)); cl=meas.classes(a2); m=cl["black"]|cl["orange/yellow"]|cl["blue"]|cl["green"]|cl["red"]|cl["brown"]
        sub=m[int((y0-pad)*f):int((y1+pad)*f),int((x0-pad)*f):int((x1+pad)*f)]
        sub=ndi.binary_opening(sub,structure=np.ones((25,25),bool))   # drops dimension arrowheads
        ys,xs=np.nonzero(sub)
        if len(xs):
            bx=[(x0-pad)+xs.min()/f,(y0-pad)+ys.min()/f,(x0-pad)+(xs.max()+1)/f,(y0-pad)+(ys.max()+1)/f]
            # use the artwork bbox only on the sides where it comes close to the rough box
            box=[bx[i] if abs(bx[i]-rough[i])<pad*0.8 else rough[i] for i in range(4)]
    a=np.asarray(h.page_img(code,dpi))
    (X0,Y0,X1,Y1),oks=meas.refine(a,box,f,slack=6)
    pp=[X0/f,Y0/f,X1/f,Y1/f]
    kx=(pp[2]-pp[0])/size[0]; ky=(pp[3]-pp[1])/size[1]
    if abs(kx/ky-1)>0.015: print(f"   {code}: snapped outline aspect off (kx {kx:.4f}, ky {ky:.4f}; snapped {oks}) {[round(v) for v in pp]}")
    return pp
def B(code,name,legend,size,sid,desc,note,drawing=None,which=0,rough=None,radius=0,ground="white",layers=("black",),turn=None,hands=None,drawn_hand=None,folder=None,tol=0.05,pp=None,extra=None,inset=0,src='fills',**kw):
    dname=drawing or code
    if turn: dname=h.ensure_upright(dname,turn)
    if pp is None and rough is not None: pp=snap(dname,tile(rough),size)
    if pp is None:
        bs=outlines(dname,size[0]/size[1],tol)
        if len(bs)<=which: raise SystemExit(f"{code}: outline with aspect {size[0]/size[1]:.2f} not found ({len(bs)} candidates)")
        pp=bs[which]
    auto.SRC=src
    A=auto.Auto(dname,size,ground="white" if ground in ("white","none") else ground,pp=list(pp),radius=radius)
    els=[]
    cls={"black":"black","yellow":"orange/yellow","red":"red","blue":"blue","green":"green","white":"white","brown":"brown","orange":"orange/yellow"}
    for c in A.out: 
        pass
    # trace all requested colour layers within the outline
    a=auto.page(dname,A.dpi); F=A.dpi/200; X0,Y0,X1,Y1=[v*F for v in A.pp]; kx=(X1-X0)/size[0]; ky=(Y1-Y0)/size[1]
    sub=a[int(Y0):int(Y1)+1,int(X0):int(X1)+1]; cm=meas.classes(sub); m=np.zeros(sub.shape[:2],bool)
    for l in layers: m|=(sub.min(axis=2)>200) if l=='white' else cm[cls[l]]
    ys,xs=np.nonzero(m)
    if len(xs)==0: raise SystemExit(f"{code}: no {layers} artwork inside the outline")
    ink=[xs.min()/kx,ys.min()/ky,(xs.max()+1)/kx,(ys.max()+1)/ky]
    A.out={cls[layers[0]]:[ink]}; A.used=set()
    e=A.trace(cls[layers[0]],sid,box=(-1,-1,size[0]+1,size[1]+1),colours=list(layers) if (len(layers)>1 or layers[0]!="black") else None,inset_mm=inset,pad=0.5,bg=(0,84,166) if layers==('white',) else 255)
    auto.SRC='fills'
    els.append(e)
    if extra: els+=extra(A)
    k={}
    if hands: k["hands"]=hands; k["drawn_hand"]=drawn_hand or hands[0]
    if folder: k["folder"]=folder
    k.update(kw)
    sy={sid:{"source":dname,"pack":"SA","desc":desc+" (traced from the sheet's filled artwork)"}}
    if len(layers)>1 or layers[0]!="black": sy[sid]["colours"]=list(layers)
    mk.spec(code,name,legend,size,ground,els,f"{note} Layout: {size[0]} x {size[1]}, {ground if ground!='none' else 'transparent outside the artwork'}, R{radius}, no border. The board is located by its drawn outline; its artwork ({desc}) is taken from the sheet's own filled shapes (PDF fills rendered at 1000 dpi without the dimension lines, traced), ink box x {e['x']:.0f}-{e['x']+e['w']:.0f}, y {e['y']:.0f}-{e['y']+e['h']:.0f}.",
            radius=radius,drawing=dname if dname!=code else None,panel_px=A.pp,symbols=sy,**k)
    return A
