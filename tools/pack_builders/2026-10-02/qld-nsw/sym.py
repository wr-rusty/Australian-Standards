"""Symbol makers for SA sheets (scratch): 
 inset(code, clip200, scale, sid, mode)  — fill the outline strokes of a grid inset (vector strokes from the PDF)
 htrace(code, panel200, W, H, box_mm, sid, dpi, **kw) — trace_symbol's tracer on a high-dpi render of the sheet"""
import sys, os, numpy as np, pymupdf
sys.path.insert(0, "."); sys.path.insert(0, "/Users/USER/Local/GitHub/Australian-Standards/tools")
import h, trace_symbol as T
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
def bez(p0,p1,p2,p3,n=24):
    return [((1-t)**3*p0.x+3*(1-t)**2*t*p1.x+3*(1-t)*t*t*p2.x+t**3*p3.x, (1-t)**3*p0.y+3*(1-t)**2*t*p1.y+3*(1-t)*t*t*p2.y+t**3*p3.y) for t in [i/n for i in range(n+1)]]
def inset(code, clip200, scale, sid, mode="all", K=60, force=True, white_seeds=(), save=None, colour=(0,0,0)):
    p=pymupdf.open(h.pdf_for(code))[0]
    clip=pymupdf.Rect(*[v*72/200 for v in clip200])
    W=int(clip.width*K)+40; H=int(clip.height*K)+40
    im=Image.new("L",(W,H),255); d=ImageDraw.Draw(im); n=0
    def P(x,y): return ((x-clip.x0)*K+20,(y-clip.y0)*K+20)
    for dr in p.get_drawings():
        if dr['type']!='s' or dr.get('color')!=colour: continue
        r=dr['rect']
        if not (r.x0>=clip.x0-0.5 and r.y0>=clip.y0-0.5 and r.x1<=clip.x1+0.5 and r.y1<=clip.y1+0.5): continue
        if len(dr['items'])==1 and dr['items'][0][0]=='l' and r.width<0.6 and r.height<0.6: continue   # grid dots
        n+=1
        for it in dr['items']:
            if it[0]=='l': pts=[(it[1].x,it[1].y),(it[2].x,it[2].y)]
            elif it[0]=='c': pts=bez(*it[1:5])
            elif it[0]=='re': r_=it[1]; pts=[(r_.x0,r_.y0),(r_.x1,r_.y0),(r_.x1,r_.y1),(r_.x0,r_.y1),(r_.x0,r_.y0)]
            elif it[0]=='qu': q=it[1]; pts=[(q.ul.x,q.ul.y),(q.ur.x,q.ur.y),(q.lr.x,q.lr.y),(q.ll.x,q.ll.y),(q.ul.x,q.ul.y)]
            else: continue
            d.line([P(*pt) for pt in pts], fill=0, width=5)
            for pt in pts[::len(pts)-1]: x,y=P(*pt); d.ellipse((x-2.5,y-2.5,x+2.5,y+2.5),fill=0)
    a=np.asarray(im)<128
    lab,nl=ndi.label(~a)
    ext=lab[0,0]
    if mode=="all": black=(lab!=ext)
    else:
        # depth by adjacency through strokes
        depth={ext:0}; frontier=[ext]; st=ndi.generate_binary_structure(2,2)
        while frontier:
            nxt=[]
            for l in frontier:
                grown=ndi.binary_dilation(lab==l, st, iterations=8)
                for m in np.unique(lab[grown]):
                    if m!=0 and m not in depth: depth[m]=depth[l]+1; nxt.append(m)
            frontier=nxt
        black=a.copy()
        for l,dep in depth.items():
            if dep%2==1: black|=(lab==l)
    for sx,sy in white_seeds:   # seeds in fraction of the canvas
        l=lab[int(sy*H),int(sx*W)]
        if l not in (0,ext): black&=(lab!=l)
    out=Image.fromarray(np.where(black,0,255).astype(np.uint8)).convert("RGB")
    if save: out.save(save)
    mm_per_px=25.4/72*scale/K
    Wmm=W*mm_per_px; Hmm=H*mm_per_px
    T.UPSCALE=1
    outp=os.path.join(T.SYM_DIR,sid+".svg")
    if os.path.exists(outp) and not force: return "exists"
    M=int(0.05*max(W,H))+10; big=Image.new("RGB",(W+2*M,H+2*M),"white"); big.paste(out,(M,M))
    return f"{n} strokes; "+T._trace_from_panel(big,(M,M,M+W-1,M+H-1),0,(0,0,Wmm,Hmm,Wmm,Hmm),sid,outp,None,110,False)
def htrace(code, panel200, W, Hm, box, sid, dpi=800, force=True, **kw):
    im=h.page_img(code,dpi); f=dpi/200
    ppx=tuple(v*f for v in panel200); ppx=(ppx[0],ppx[1],ppx[2]-1,ppx[3]-1)
    T.UPSCALE=kw.pop("upscale",2)
    outp=os.path.join(T.SYM_DIR,sid+".svg")
    if os.path.exists(outp) and not force: return "exists"
    return T._trace_from_panel(im,ppx,0,tuple(box)+(W,Hm),sid,outp,kw.pop("show",None),kw.pop("threshold",110),kw.pop("invert",False),**kw)
