"""ov.py out_prefix CODE...  — compare_drawing's overlay on a high-dpi render of the SA sheet (panel_px from the spec, else C.locate)."""
import sys, os, json, warnings
warnings.filterwarnings("ignore")
ROOT="/Users/USER/Local/GitHub/Australian-Standards"
sys.path.insert(0,"."); sys.path.insert(0,ROOT+"/tools")
import compare_drawing as C, h
from PIL import Image, ImageDraw
def one(code, value=None, height=520, target=1000):
    spec=C.spec_for(code)
    if spec.get("skip"): return None
    png,hand,which=C.drawing_for(spec)
    if value is None: value=C.drawn_value(spec)
    svg=C.svg_for(spec,value,hand)
    img200=Image.open(png).convert("RGB")
    px0,py0,pw,ph=C.locate(spec,which,img200)
    if spec.get("panel_px"):
        x0,y0,x1,y1=spec["panel_px"]; px0,py0,pw,ph=x0,y0,x1-x0,y1-y0
    dpi=int(min(1200,max(200,200*target/max(pw,ph)))); f=dpi/200
    dcode=os.path.basename(png)[:-4]
    m=0.05*max(pw,ph)
    box=(px0-m,py0-m,px0+pw+m,py0+ph+m)
    crop=h.page_img(dcode,dpi,box)
    gen=C.render(svg,pw*f,ph*f)
    gen_c=Image.new("RGB",crop.size,"white"); gen_c.paste(gen,(int(px0*f)-int(box[0]*f),int(py0*f)-int(box[1]*f)))
    sc=C.score(crop,gen_c,tol=max(2,int(2*f/2)))
    ov=C.overlay(crop,gen_c); s=height/crop.height
    if crop.width*s*3>1900: s=1900/3/crop.width
    tiles=[t.resize((max(1,int(t.width*s)),max(1,int(t.height*s)))) for t in (crop,gen_c,ov)]
    out=Image.new("RGB",(sum(t.width for t in tiles)+40,tiles[0].height+16),"white"); x=0
    for t in tiles: out.paste(t,(x,16)); x+=t.width+20
    ImageDraw.Draw(out).text((4,2),f"{code}{'='+str(value) if value is not None else ''}  score {sc:.3f}",fill="black")
    return out,sc
if __name__=="__main__":
    out=sys.argv[1]; strips=[]; per=int(os.environ.get("PER","4"))
    for c in sys.argv[2:]:
        code,_,val=c.partition("=")
        try:
            r=one(code,val or None)
            if r: strips.append(r[0]); print(f"{code}\t{r[1]:.3f}")
        except SystemExit as ex: print(code,"FAIL",ex)
        except Exception as ex: print(code,"ERR",repr(ex))
    for i in range(0,len(strips),per):
        ss=strips[i:i+per]
        sheet=Image.new("RGB",(max(s.width for s in ss),sum(s.height for s in ss)+8*len(ss)),"white"); y=0
        for s in ss: sheet.paste(s,(0,y)); y+=s.height+8
        sheet.save(f"{out}_{i//per:02d}.png"); print(f"{out}_{i//per:02d}.png",sheet.size)
