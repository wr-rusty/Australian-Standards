#!/usr/bin/env python3
"""shs_sheets.py — review sheets for the SHS extraction: page drawing crop | extracted SVG, 12 per sheet.
Pairs come from the family's _extract_manifest.csv (code, name, file, size, A, page, note, panel rect).
  python3 tools/shs_sheets.py <pdf> <family> <out_dir> [manifest.csv]"""
import os, sys, csv, subprocess, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import shs_extract as X
from PIL import Image, ImageDraw
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
def main(pdf, family, out, manifest=None):
    os.makedirs(out, exist_ok=True); doc = pymupdf.open(pdf); tiles = []; n = 0
    folder = os.path.join(X.OUT, family); manifest = manifest or os.path.join(folder, "_extract_manifest.csv")
    for row in csv.reader(open(manifest)):
        if len(row) < 8: continue
        code, name, fn, size, A, page, note, rect = row[:8]
        x0, y0, x1, y1 = map(float, rect.split(","))
        pix = doc[int(page) - 1].get_pixmap(clip=pymupdf.Rect(x0 - 6, y0 - 6, x1 + 6, y1 + 6), dpi=90)
        a = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        svg = os.path.join(X.OUT, fn) if fn.startswith("intervene/") else os.path.join(folder, fn)
        png = os.path.join(out, "_r.png")
        if os.path.exists(png): os.remove(png)
        subprocess.run([INK, svg, "--export-type=png", f"--export-height={a.height}", "--export-background=#dddddd", f"--export-filename={png}"], capture_output=True)
        b = Image.open(png).convert("RGB") if os.path.exists(png) else Image.new("RGB", (100, a.height), "red")
        h = 180; a = a.resize((max(1, int(a.width * h / a.height)), h)); b = b.resize((max(1, int(b.width * h / b.height)), h))
        if a.width > 380: a = a.resize((380, int(a.height * 380 / a.width)))
        if b.width > 380: b = b.resize((380, int(b.height * 380 / b.width)))
        t = Image.new("RGB", (a.width + b.width + 16, 200), "white"); t.paste(a, (0, 20)); t.paste(b, (a.width + 16, 20))
        flag = " INTERVENE" if fn.startswith("intervene/") else (" pagescale" if "page scale" in note else (" check" if "check" in note else ""))
        ImageDraw.Draw(t).text((2, 3), f"p{page} {code} {name[:26]} [{size}{flag}]", fill="black"); tiles.append(t)
        if len(tiles) == 12:
            n += 1; save(tiles, os.path.join(out, f"{family.replace(' ', '_')}_{n:03d}.png")); tiles = []
    if tiles: n += 1; save(tiles, os.path.join(out, f"{family.replace(' ', '_')}_{n:03d}.png"))
    print(family, "sheets:", n)
def save(tiles, path):
    cols = 3; cw = max(t.width for t in tiles) + 10; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cw, rows * 202), "white")
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * cw, (i // cols) * 202))
    sh.save(path)
if __name__ == "__main__": main(*sys.argv[1:])
