# Crawl Cerema's Box share "signauxroutiers" (official French road-sign SVGs, Licence Ouverte 2.0) and download every
# file into the given folder, writing BOX_MANIFEST.csv. Usage: python3 tools/fr_cerema_box.py "Processing/France/National (IISR)/Original SVG (Cerema)"
# Resumable: existing non-empty files are skipped. 2026-09-08: 530 SVGs in 16 folders.
import re, json, os, sys, time, urllib.request, urllib.parse
SHARED="dwrf655fhaolonqcspo0z0gvb06ms0n7"
ROOT="https://cerema.app.box.com/v/signauxroutiers"
OUT=sys.argv[1]
UA={"User-Agent":"Mozilla/5.0"}
def get(url):
    r=urllib.request.Request(url,headers=UA); return urllib.request.urlopen(r,timeout=60).read()
def items(folder_id):
    url=ROOT if folder_id is None else f"{ROOT}/folder/{folder_id}"
    h=get(url).decode('utf-8','replace')
    i=h.find('"items":[')
    if i<0: return []
    # balanced bracket scan
    j=i+len('"items":'); depth=0; k=j
    while k<len(h):
        c=h[k]
        if c=='[': depth+=1
        elif c==']':
            depth-=1
            if depth==0: break
        k+=1
    arr=json.loads(h[j:k+1])
    return [(it["type"],it["id"],it["name"],it.get("itemSize",0)) for it in arr]
manifest=[]
def walk(fid,path):
    for t,i,n,s in items(fid):
        if t=="folder": walk(i,path+[n])
        else:
            d=os.path.join(OUT,*path); os.makedirs(d,exist_ok=True)
            p=os.path.join(d,n); manifest.append(("/".join(path+[n]),i,s))
            if os.path.exists(p) and os.path.getsize(p)>0: continue
            u=f"https://cerema.app.box.com/index.php?rm=box_download_shared_file&shared_name={SHARED}&file_id=f_{i}"
            for a in range(3):
                try:
                    open(p,'wb').write(get(u)); break
                except Exception as e:
                    time.sleep(2)
            time.sleep(0.2)
    print("done", "/".join(path), len(manifest), flush=True)
walk(None,[])
with open(os.path.join(OUT,"BOX_MANIFEST.csv"),"w") as f:
    f.write("path,box_file_id,bytes\n")
    for p,i,s in manifest: f.write(f"{p},{i},{s}\n")
print("total files", len(manifest))
