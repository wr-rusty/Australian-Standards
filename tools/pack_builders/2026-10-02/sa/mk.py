"""spec builder helpers (scratch, SA)"""
import json, math, os, sys
ROOT="/Users/russell/Local/GitHub/Australian-Standards"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT+"/tools"); import signgen as G
PRE="DIT SA Standard Road Sign Index sheet (A4, legends and dimensions outlined, colour legend; size from the sheet's size table = register). Every dimension from the sheet; AS 1744 (plus0) spacing. "
E2="The sheet's two edge figures are the white edge and edge + black border, as the AS 1743 drawings. "
NAT="Complete/Australia/National (AS 1743)"
def ink(text, series, height, tracking="plus0"): return round(G.face(series, tracking).ink_width(text, height), 1)
def series_guess(text, height, width):
    return sorted(((round(abs(ink(text,s,height)-width),1), s, ink(text,s,height)) for s in ("B","C","D","E","Emod","F")))[:3]
def T(text, series, height, top, expect=None, **kw):
    e={"type":"text","text":text,"series":series,"height":height,"top":top}
    if expect is not None: e["expect"]=expect
    e.update(kw); return e
def Wd(words, gap, series, height, top, expect=None, **kw):
    e={"type":"text","words":words,"gap":gap,"series":series,"height":height,"top":top}
    if expect is not None: e["expect"]=expect
    e.update(kw); return e
def panel(x,y,w,h,r,colour): return {"type":"panel","x":x,"y":y,"w":w,"h":h,"radius":r,"colour":colour}
def rect(x,y,w,h,colour="black"): return {"type":"rect","x":x,"y":y,"w":w,"h":h,"colour":colour}
def poly(points,colour="black",radius=0,**kw):
    e={"type":"polygon","points":[list(p) for p in points],"colour":colour}
    if radius: e["radius"]=radius
    e.update(kw); return e
def bordered(x,y,w,h,r,edge,border,ground="white",bcol="black"):
    return [panel(x+edge,y+edge,w-2*edge,h-2*edge,max(0,r-edge),bcol), panel(x+edge+border,y+edge+border,w-2*(edge+border),h-2*(edge+border),max(0,r-edge-border),ground)]
def annulus(cx,cy,ro,ri,colour="red"): return {"type":"annulus","cx":cx,"cy":cy,"r_outer":ro,"r_inner":ri,"colour":colour}
def circle(cx,cy,r,colour="black"): return {"type":"circle","cx":cx,"cy":cy,"r":r,"colour":colour}
def slash(cx,cy,r,w,colour="red",dirn="ur-ll"):
    hw=w/2; a=math.asin(hw/r)
    base = -math.pi/4 if dirn=="ur-ll" else math.pi/4
    def pt(ang): return (cx+r*math.cos(ang), cy+r*math.sin(ang))
    p=[pt(base-a),pt(base+a),pt(base+math.pi-a),pt(base+math.pi+a)]
    f=G.fmt
    d=f"M{f(p[0][0])} {f(p[0][1])}A{f(r)} {f(r)} 0 0 1 {f(p[1][0])} {f(p[1][1])}L{f(p[2][0])} {f(p[2][1])}A{f(r)} {f(r)} 0 0 1 {f(p[3][0])} {f(p[3][1])}Z"
    return {"type":"path","d":d,"colour":colour}
def sym(id,x,y,w,h,colour="black",**kw):
    e={"type":"symbol","id":id,"x":x,"y":y,"w":w,"h":h,"colour":colour}; e.update(kw); return e
def symbox(id):
    paths,vb=G.symbol_paths(id); return vb[2],vb[3]
def symc(id,cx,cy,scale=1.0,**kw):
    w,h=symbox(id); w*=scale; h*=scale
    return sym(id,round(cx-w/2,2),round(cy-h/2,2),round(w,2),round(h,2),**kw)
def spec(code, name, legend, size, ground, elements, notes, radius=0, edge=None, border=None, drawing=None, panel_px=None, shape="rect", pre=PRE, **kw):
    s={"code":code,"pack":"SA","name":name,"legend":legend,"shape":shape,"size":list(size),"ground":ground}
    if radius: s["radius"]=radius
    if edge: s["edge"]={"colour":edge[0],"width":edge[1]}
    if border: s["border"]={"colour":border[0],"width":border[1]}
    if drawing and drawing!=code: s["drawing"]=drawing
    if panel_px: s["panel_px"]=[round(v) for v in panel_px]
    s.update(kw); s["elements"]=elements; s["notes"]=pre+notes
    save(s); return s
def skip(code, legend, why, drawing=None):
    s={"code":code,"pack":"SA"}
    if drawing and drawing!=code: s["drawing"]=drawing
    s["legend"]=legend; s["skip"]=why; save(s); return s
def nat(code, natcode, legend, drawing=None, size=""):
    return skip(code, legend, f"AS 1743 code {natcode} (the SA sheet is the national sign{' at its '+size+' size' if size else ''}): use {NAT} — state packs hold only state-specific signs, no national code is redrawn", drawing)
WRITTEN=[]
def save(s):
    p=f"{ROOT}/tools/specs/SA/{s['code']}.json"
    json.dump(s, open(p,"w"), indent=1, ensure_ascii=False); open(p,"a").write("\n"); WRITTEN.append(p)
import numpy as _np
def px(code, vbox, dpi=600, view=True):
    """panel_px (200-dpi px) from an approximate box read off the 1413-wide view, snapped to the drawn outline"""
    import meas, h
    box=[v*1653/1413 for v in vbox] if view else list(vbox)
    a=_np.asarray(h.page_img(code,dpi)); f=dpi/200
    (X0,Y0,X1,Y1),oks=meas.refine(a,box,f)
    r=[X0/f,Y0/f,X1/f,Y1/f]
    if not all(oks): print("  px",code,"not snapped:",oks,[round(v) for v in r])
    return r
def gen(codes=None):
    import subprocess
    ps=WRITTEN if codes is None else [f"{ROOT}/tools/specs/SA/{c}.json" for c in codes]
    r=subprocess.run([sys.executable, ROOT+"/tools/signgen.py"]+ps,capture_output=True,text=True,cwd=ROOT); print('\n'.join(l[:230] for l in r.stdout.splitlines() if 'SKIPPED' not in l), r.stderr[-2000:])

def arrow_d(x,y,L=155,colour="red"):
    p=[(0,16),(21.75,0),(42,0),(28.41,10),(L-28.41,10),(L-42,0),(L-21.75,0),(L,16),(L-21.75,32),(L-42,32),(L-28.41,22),(28.41,22),(42,32),(21.75,32)]
    return poly([(round(x+a,2),round(y+b,2)) for a,b in p],colour)
def arrow_r(x,y,L=125,colour="red"):
    p=[(L,16),(L-21.75,0),(L-42,0),(L-28.41,10),(0,10),(0,22),(L-28.41,22),(L-42,32),(L-21.75,32)]
    return poly([(round(x+a,2),round(y+b,2)) for a,b in p],colour)
def arrow_l(x,y,L=125,colour="red"):
    p=[(0,16),(21.75,0),(42,0),(28.41,10),(L,10),(L,22),(28.41,22),(42,32),(21.75,32)]
    return poly([(round(x+a,2),round(y+b,2)) for a,b in p],colour)
ARROWNOTE=" Arrows are the AS 1743 R5-14 (double, 155 x 32) and R5-16 (single, 125 x 32) open-chevron arrows the sheet cites, drawn as polygons with the national dimensions (shaft 12, head 42 long x 32 wide, barbs 12 thick)."
def emit3(code,name,legend,size,els,arrow,notes,**kw):
    """base spec with the double arrow as drawn + _LEFT / _RIGHT specs with the sheet's single-arrow alternatives. arrow=(y_top,colour[,x_double,L_double])"""
    y,colour=arrow[:2]; W=size[0]; xd=arrow[2] if len(arrow)>2 else (W-155)/2; Ld=arrow[3] if len(arrow)>3 else 155
    out=[spec(code,name,legend+" (double arrow)",size,"white",els+[arrow_d(xd,y,Ld,colour)],notes+ARROWNOTE,**kw)]
    kw2=dict(kw); kw2["drawing"]=kw.get("drawing") or code
    for word,fn in (("LEFT",arrow_l),("RIGHT",arrow_r)):
        out.append(spec(f"{code}_{word}",name,legend+f" ({word.lower()} arrow)",size,"white",els+[fn((W-125)/2,y,125,colour)],notes+ARROWNOTE+f" This spec is the sheet's {word.lower()}-arrow alternative (R5-16, 125 long, centred); the sheet draws the double arrow.",**kw2))
    return out
