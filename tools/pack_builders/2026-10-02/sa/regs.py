import sys; sys.path.insert(0,'.')
import h,numpy as np,meas
from scipy import ndimage as ndi
def regs(code,cls="orange/yellow",minpx=80):
    a=np.asarray(h.fills_img(code,200)); m=meas.classes(a)[cls]; lab,n=ndi.label(ndi.binary_dilation(m,iterations=4))
    return [(o[1].start,o[0].start,o[1].stop,o[0].stop) for o in ndi.find_objects(lab) if (o[0].stop-o[0].start)>minpx and o[0].start<1900]
if __name__=="__main__":
    for c in sys.argv[1:]:
        code,_,cls=c.partition(":"); print(code,regs(code,cls or "orange/yellow"))
