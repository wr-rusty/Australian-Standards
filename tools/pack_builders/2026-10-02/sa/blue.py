"""blue.py — service-sign helpers: white legend on blue boards, blue legend on white plates (measured from the sheet's filled artwork)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h, meas, mk, auto, gen2
from mk import *
from scipy import ndimage as ndi
BLUE=(0,84,166)
def blue_boards(code, dpi=300):
    """bboxes (200-dpi px) of the solid blue areas on the sheet, largest first"""
    a=np.asarray(h.fills_img(code,dpi)); f=dpi/200; m=meas.classes(a)["blue"]; m[int(a.shape[0]*0.80):]=False
    lab,n=ndi.label(ndi.binary_dilation(m,iterations=6)); out=[]
    for i,o in enumerate(ndi.find_objects(lab)):
        mm=(lab[o]==i+1)&m[o]; ys,xs=np.nonzero(mm)
        if len(xs)<2000: continue
        out.append(((o[1].start+xs.min())/f,(o[0].start+ys.min())/f,(o[1].start+xs.max()+1)/f,(o[0].start+ys.max()+1)/f,int(mm.sum())))
    out.sort(key=lambda b:-b[4]); return out
def setup(code, size, pp, big=0.45):
    """Auto on pp with: A.out['blue'] and A.out['white'] holding only legend-sized components"""
    auto.SRC="fills"
    A=auto.Auto(code,size,ground="white",pp=list(pp))
    W,H=size
    def small(c): return (c[2]-c[0])<big*W and (c[3]-c[1])<big*H
    A.out["blue"]=[c for c in A.out.get("blue",[]) if small(c)]
    A.out["white"]=[c for c in gen2._white_comps(A,"blue") if small(c)]
    return A
def runs(code,pp,size,x=None,y=None):
    r=meas.prof(code,pp,size[0],size[1],x=x,y=y,dpi=1200)
    return [q for q in r if q[0]=="blue"]
