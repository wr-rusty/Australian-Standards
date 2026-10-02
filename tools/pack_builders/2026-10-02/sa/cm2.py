import sys, meas
def comps(code,box,W,H,view=False,minmm=2.0,dpi=1200,cols=("red","black","green","blue","orange/yellow","brown")):
    box=[v*1653/1413 for v in box] if view else list(box)
    out,pp=meas.run(code,box,W,H,dpi=dpi,minmm=minmm,show=False)
    print(code,"panel_px",[round(v,1) for v in pp])
    for name in cols:
        cs=[c for c in out.get(name,[]) if not (c[2]-c[0]>0.9*W and c[3]-c[1]>0.9*H)]
        if not cs: continue
        print(" ",name)
        for l in meas.lines(cs,W)[:30]:
            c2=sorted(l[4],key=lambda c:c[0])
            print(f"   y {l[1]:.1f}-{l[3]:.1f}  x {l[0]:.1f}-{l[2]:.1f} ({l[2]-l[0]:.1f}): "+" ".join(f"{c[0]:.1f}+{c[2]-c[0]:.1f}"+(f"@{c[1]:.0f}-{c[3]:.0f}" if (c[3]-c[1])<0.8*(l[3]-l[1]) else "") for c in c2[:24]))
    return pp
