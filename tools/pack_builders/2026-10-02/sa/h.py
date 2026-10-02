"""helpers: crop(code, box200, dpi) -> png path; pdf_for(code)"""
import csv, os, re, sys, pymupdf
ROOT="/Users/russell/Local/GitHub/Australian-Standards"; SA=ROOT+"/Processing/Australia/SA"
S=os.path.dirname(os.path.abspath(__file__))
_reg=None
def reg():
    global _reg
    if _reg is None:
        _reg={}
        for r in csv.DictReader(open(SA+"/REGISTER.csv")):
            if not r['local']: continue
            codes=[c.strip() for c in r['codes'].split("|") if c.strip()]
            first=codes[0].replace(" ","") if codes else "SA"+r["id"]
            _reg[first]=r; r['_codes']=codes
    return _reg
UP="_upright"
_bt={}
def base_turn(code, p, ref):
    """rotation that reproduces the Original PNG: first size match; sideways sheets are checked against the PNG's content (90 or -90). Upright re-renders keep the first size match (their extra turn was set against it)."""
    key=code
    if key in _bt: return _bt[key]
    from PIL import Image, ImageChops
    turn=0
    for turn in (0,90,-90,180):
        r=p.rect*pymupdf.Matrix(200/72,200/72)*pymupdf.Matrix(turn)
        if abs(abs(r.width)-ref.width)<3 and abs(abs(r.height)-ref.height)<3: break
    if not code.endswith(UP) and turn in (90,-90):
        best=None; small=ref.convert("L").resize((200,int(200*ref.height/ref.width)))
        for t in (90,-90):
            pix=p.get_pixmap(matrix=pymupdf.Matrix(0.5,0.5)*pymupdf.Matrix(t),alpha=False)
            im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples).convert("L").resize(small.size)
            d=sum(ImageChops.difference(im,small).histogram()[40:])
            if best is None or d<best[0]: best=(d,t)
        turn=best[1]
    _bt[key]=turn; return turn
def _turns():
    import json
    p=os.path.join(S,"turns.json"); return json.load(open(p)) if os.path.exists(p) else {}
def base(code): return code[:-len(UP)] if code.endswith(UP) else code
def pdf_for(code): return SA+"/"+reg()[base(code)]['local']
def ensure_upright(code, turn):
    """render <code>_upright.png (200 dpi) for a sheet whose PNG was rendered sideways; turn = extra degrees"""
    import json
    t=_turns(); t[code]=turn; json.dump(t,open(os.path.join(S,"turns.json"),"w"))
    out=f"{SA}/Original PNGs/{code}{UP}.png"
    if not os.path.exists(out): page_img(code+UP,200).save(out)
    return code+UP
def page_img(code, dpi=200, clip200=None):
    """render upright as the 200-dpi PNG; clip in 200-dpi px coords"""
    from PIL import Image
    ref=Image.open(f"{SA}/Original PNGs/{base(code)}.png"); 
    p=pymupdf.open(pdf_for(code))[0]
    k=dpi/72
    turn=base_turn(code,p,ref); m=pymupdf.Matrix(k,k)*pymupdf.Matrix(turn)
    if code.endswith(UP): turn+=_turns()[base(code)]; m=pymupdf.Matrix(k,k)*pymupdf.Matrix(turn)
    pix=p.get_pixmap(matrix=m,alpha=False)
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    if clip200:
        f=dpi/200; im=im.crop(tuple(int(v*f) for v in clip200))
    return im
if __name__=="__main__":
    code=sys.argv[1]; box=[float(v) for v in sys.argv[2:6]]; dpi=int(sys.argv[6]) if len(sys.argv)>6 else 500
    out=sys.argv[7] if len(sys.argv)>7 else f"{S}/crop.png"
    im=page_img(code,dpi,box); im.save(out); print(out, im.size)

_fdoc={}
def fills_doc(code):
    """a copy of the sheet with only its filled shapes (no stroked line-work: centre lines, dimension lines, outlines)"""
    if code in _fdoc: return _fdoc[code]
    src=pymupdf.open(pdf_for(code)); p=src[0]
    out=pymupdf.open(); q=out.new_page(width=p.rect.width,height=p.rect.height)
    sh=q.new_shape(); n=0
    for d in p.get_drawings():
        if d.get("fill") is None: continue
        for it in d["items"]:
            if it[0]=="l": sh.draw_line(it[1],it[2])
            elif it[0]=="c": sh.draw_bezier(it[1],it[2],it[3],it[4])
            elif it[0]=="re": sh.draw_rect(it[1])
            elif it[0]=="qu": sh.draw_quad(it[1])
        sh.finish(fill=d["fill"],color=d["fill"],width=0.1,even_odd=bool(d.get("even_odd")),closePath=True); n+=1
    sh.commit(); _fdoc[code]=(out,p.rotation,p.rect)
    return _fdoc[code]
def fills_img(code, dpi=200, clip200=None):
    from PIL import Image
    ref=Image.open(f"{SA}/Original PNGs/{base(code)}.png")
    doc,rot,rect=fills_doc(code); p=doc[0]; k=dpi/72
    base_=pymupdf.open(pdf_for(code))[0]
    turn=base_turn(code,base_,ref)
    if base_.rotation: p.set_rotation(base_.rotation)
    if code.endswith(UP): turn+=_turns()[code[:-len(UP)]]
    pix=p.get_pixmap(matrix=pymupdf.Matrix(k,k)*pymupdf.Matrix(turn),alpha=False)
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    if clip200:
        f=dpi/200; im=im.crop(tuple(int(v*f) for v in clip200))
    return im
