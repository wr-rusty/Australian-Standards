import sys, meas
def comps(code,vbox,W,H,cols=("red","black","green","blue","orange/yellow","brown"),minmm=2.5,maxn=14,view=True,dpi=1200):
    box=[v*1653/1413 for v in vbox] if view else list(vbox)
    out,pp=meas.run(code,box,W,H,dpi=dpi,minmm=minmm)
    for name in cols:
        cs=out.get(name,[])
        if not cs: continue
        print(" ",name)
        for l in meas.lines(cs,W)[:25]:
            c2=sorted(l[4],key=lambda c:c[0])
            print(f"   y {l[1]:.1f}-{l[3]:.1f}: "+"  ".join(f"[{c[0]:.1f}-{c[2]:.1f} y{c[1]:.1f}-{c[3]:.1f}]" for c in c2[:maxn])+(" ..." if len(c2)>maxn else ""))
    return pp
if __name__=="__main__":
    code=sys.argv[1]; v=[float(x) for x in sys.argv[2:8]]
    comps(code,v[:4],v[4],v[5])
