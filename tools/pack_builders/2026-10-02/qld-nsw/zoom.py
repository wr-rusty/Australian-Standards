# zoom.py CODE x0 y0 x1 y1 [dpi] -> x/z_CODE.png : region (200-dpi PNG px) re-rendered from the PDF at dpi
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, 'tools')
import tsc, pymupdf
from PIL import Image
code = sys.argv[1]; x0, y0, x1, y1 = [float(v) for v in sys.argv[2:6]]; dpi = float(sys.argv[6]) if len(sys.argv) > 6 else 400
page, (M, ox, oy) = tsc.load(code); k = dpi / 200
M2 = M * pymupdf.Matrix(k, k)
pix = page.get_pixmap(matrix=pymupdf.Matrix(1, 1) , alpha=False) if False else None
# render whole page with M2 then crop (page rotation is already inside M via rotation_matrix; get_pixmap applies rotation itself, so strip it)
R = pymupdf.Matrix(page.rotation_matrix); R.invert()
pm = page.get_pixmap(matrix=R * M2 if False else (pymupdf.Matrix(dpi / 72, dpi / 72) * tsc.Sheet(code, [0, 0, 1, 1], 1)._turn_only()), alpha=False)
im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples).crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)))
out = os.path.join(os.path.dirname(__file__), 'x', 'z_' + code.replace('(', '_').replace(')', '') + '.png'); im.save(out); print(out, im.size)
