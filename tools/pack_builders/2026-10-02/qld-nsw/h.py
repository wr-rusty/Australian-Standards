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
            first=codes[0] if codes else "SA"+r['id']
            _reg[first]=r; r['_codes']=codes
    return _reg
def pdf_for(code): return SA+"/"+reg()[code]['local']
def page_img(code, dpi=200, clip200=None):
    """render upright as the 200-dpi PNG; clip in 200-dpi px coords"""
    from PIL import Image
    ref=Image.open(f"{SA}/Original PNGs/{code}.png"); 
    p=pymupdf.open(pdf_for(code))[0]
    k=dpi/72
    for turn in (0,90,-90,180):
        m=pymupdf.Matrix(k,k)*pymupdf.Matrix(turn)
        r=p.rect*pymupdf.Matrix(200/72,200/72)*pymupdf.Matrix(turn)
        if abs(abs(r.width)-ref.width)<3 and abs(abs(r.height)-ref.height)<3: break
    pix=p.get_pixmap(matrix=m,alpha=False)
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    if clip200:
        f=dpi/200; im=im.crop(tuple(int(v*f) for v in clip200))
    return im
if __name__=="__main__":
    code=sys.argv[1]; box=[float(v) for v in sys.argv[2:6]]; dpi=int(sys.argv[6]) if len(sys.argv)>6 else 500
    out=sys.argv[7] if len(sys.argv)>7 else f"{S}/crop.png"
    im=page_img(code,dpi,box); im.save(out); print(out, im.size)
