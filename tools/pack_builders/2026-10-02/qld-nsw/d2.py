import sys
from qb import *
vc=sys.argv[1]; fl=fills(vc); ymax=float(sys.argv[2]) if len(sys.argv)>2 else 1200
big=[f for f in fl if f[2][2]-f[2][0]>300 and f[2][1]<ymax]
o=max(big,key=lambda f:(f[2][2]-f[2][0])*(f[2][3]-f[2][1])); W=float(sys.argv[3]); k=(o[2][2]-o[2][0])/W; x0,y0=o[2][0],o[2][1]
M=lambda b:[round((b[0]-x0)/k,1),round((b[1]-y0)/k,1),round((b[2]-x0)/k,1),round((b[3]-y0)/k,1)]
print("outer",o[0],o[1],[round(v,1) for v in o[2]],"k",round(k,4),"H",round((o[2][3]-y0)/k,1))
tx=texts(vc,ymax)
ar=sorted([t for t in tx if "Arial" in t[1] or "Century" in t[1]], key=lambda t:(t[3][0]>o[2][2], t[3][2]<x0, t[3][1]))
print("dims:", " | ".join(f"{t[0]}@{M(t[3])[0]:.0f},{M(t[3])[1]:.0f}" for t in ar if len(t[0])<12))
for t in tx:
    if "FHWA" in t[1]: print("F", repr(t[0]), t[1][10:], round(t[2]/k), M(t[3]))
import collections
seen=collections.Counter()
for f in fl:
    if f[2][1]<ymax and f[2][0]>=x0-2 and f[2][2]<=o[2][2]+2 and f[2][1]>=y0-2 and f[2][3]<=o[2][3]+2 and max(f[2][2]-f[2][0],f[2][3]-f[2][1])>12/1:
        m=M(f[2]); key=(f[1],round(m[2]-m[0]),round(m[3]-m[1])); seen[key]+=1
        if seen[key]<=2: print("V",f[0],f[1],m,"n",f[3])
