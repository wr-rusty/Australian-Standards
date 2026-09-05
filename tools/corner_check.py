#!/usr/bin/env python3
"""corner_check.py — render every SVG under a folder on magenta and report signs whose corner pixels are not
transparent (white or other paint outside a rounded/diamond/octagon outline). Usage: corner_check.py <folder> <report.csv>"""
import os, sys, glob, subprocess, csv, tempfile
from PIL import Image
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
def check(svg, td):
    png = os.path.join(td, "c.png")
    subprocess.run([INK, svg, "--export-type=png", "--export-height=240", "--export-background=#ff00ff", f"--export-filename={png}"], capture_output=True)
    if not os.path.exists(png): return "render failed"
    im = Image.open(png).convert("RGB"); w, h = im.size; px = im.load(); bad = []
    for name, (x, y) in {"TL": (2, 2), "TR": (w - 3, 2), "BL": (2, h - 3), "BR": (w - 3, h - 3)}.items():
        r, g, b = px[x, y]
        if not (r > 200 and g < 80 and b > 200): bad.append(f"{name}={r},{g},{b}")
    os.remove(png); return ";".join(bad)
def main(folder, report):
    rows = []
    with tempfile.TemporaryDirectory() as td:
        for svg in sorted(glob.glob(os.path.join(folder, "**", "*.svg"), recursive=True)):
            r = check(svg, td)
            if r: rows.append([os.path.relpath(svg, folder), r])
    with open(report, "w", newline="") as fh: csv.writer(fh).writerows(rows)
    print(f"{len(rows)} signs with painted corners -> {report}")
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
