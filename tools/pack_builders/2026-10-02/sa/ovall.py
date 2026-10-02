"""ovall.py prefix batchfile.py... — overlay every non-skip spec written by the given batch scripts (codes parsed from G(/spec( calls) ; prints scores, writes sheets only for scores over THR"""
import sys, re, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ov
from PIL import Image
THR=float(os.environ.get("THR","0.09")); out=sys.argv[1]; codes=sys.argv[2:]
strips=[]; res=[]
for c in codes:
    code,_,val=c.partition("=")
    try:
        r=ov.one(code,val or None)
        if not r: continue
        res.append((code,r[1]))
        if r[1]>THR: strips.append(r[0])
    except SystemExit as ex: print(code,"FAIL",ex)
    except Exception as ex: print(code,"ERR",repr(ex)[:200])
print(" ".join(f"{c}:{s:.3f}" for c,s in res))
per=6
for i in range(0,len(strips),per):
    ss=strips[i:i+per]
    sheet=Image.new("RGB",(max(s.width for s in ss),sum(s.height for s in ss)+8*len(ss)),"white"); y=0
    for s in ss: sheet.paste(s,(0,y)); y+=s.height+8
    sheet.save(f"{out}_{i//per:02d}.png"); print(f"{out}_{i//per:02d}.png",sheet.size)
