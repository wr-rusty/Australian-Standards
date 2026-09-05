#!/usr/bin/env python3
"""overlay.py — render two SVGs (e.g. before/after a spec change) and write side-by-side + overlay PNG.
  python3 tools/overlay.py before.svg after.svg out.png [height]
Overlay: 'before' in red, 'after' in blue; where they coincide the result is dark, differences show as red or blue fringes."""
import subprocess, sys
from PIL import Image
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
def render(svg, png, h):
    subprocess.run([INK, svg, "--export-type=png", f"--export-height={h}", "--export-background=#ffffff", f"--export-filename={png}"], capture_output=True)
    return Image.open(png).convert("L")
def main(a, b, out, h=400):
    A = render(a, out + ".a.png", h); B = render(b, out + ".b.png", h)
    if A.size != B.size: B = B.resize(A.size)
    ov = Image.merge("RGB", (A, Image.new("L", A.size, 255), B))
    Ac = Image.open(out + ".a.png").convert("RGB"); Bc = Image.open(out + ".b.png").convert("RGB")
    t = Image.new("RGB", (Ac.width + Bc.width + ov.width + 40, h), "white"); t.paste(Ac, (0, 0)); t.paste(Bc, (Ac.width + 20, 0)); t.paste(ov, (Ac.width + Bc.width + 40, 0)); t.save(out)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 400)
