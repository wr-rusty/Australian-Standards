#!/usr/bin/env python3
"""nz_sheets.py — review sheets for the NZ extraction: NZTA's non-labelled GIF beside the extracted SVG, 12 pairs per image.
  python3 tools/nz_sheets.py <out_dir>"""
import os, sys, csv, glob, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import nz_extract as N
from PIL import Image, ImageDraw
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
def main(out):
    os.makedirs(out, exist_ok=True)
    reg = {r["code"]: r for r in csv.DictReader(open(os.path.join(N.NZ, "REGISTER.csv")))}
    tiles = []; n = 0; fam_prev = None
    def flush():
        nonlocal tiles, n
        if tiles: n += 1; save(tiles, os.path.join(out, f"NZ_{n:03d}.png")); tiles = []
    for row in csv.DictReader(open(os.path.join(N.NZ, "SVGs", "MANIFEST.csv"))):
        if not row["file"]: continue
        r = reg.get(row["code"]); gifs = [p for p in (r["local"].split(" | ") if r else []) if p.lower().endswith(".gif")]
        a = Image.open(os.path.join(N.NZ, gifs[0])).convert("RGB") if gifs else Image.new("RGB", (100, 100), "red")
        svg = os.path.join(N.NZ, "SVGs", row["family"], row["file"]); png = os.path.join(out, "_r.png")
        if os.path.exists(png): os.remove(png)
        subprocess.run([INK, svg, "--export-type=png", "--export-height=170", "--export-background=#dddddd", f"--export-filename={png}"], capture_output=True)
        try: b = Image.open(png).convert("RGB")
        except Exception: b = Image.new("RGB", (100, 170), "red"); print("render failed:", row["file"])
        h = 170; a = a.resize((max(1, int(a.width * h / a.height)), h)); b = b.resize((max(1, int(b.width * h / b.height)), h))
        for im in (a, b): pass
        if a.width > 330: a = a.resize((330, int(a.height * 330 / a.width)))
        if b.width > 330: b = b.resize((330, int(b.height * 330 / b.width)))
        t = Image.new("RGB", (a.width + b.width + 16, 192), "white"); t.paste(a, (0, 20)); t.paste(b, (a.width + 16, 20))
        ImageDraw.Draw(t).text((2, 3), f"{row['code']} {row['name'][:30]} [{row['size']}{' !' if row['notes'] else ''}]", fill="black"); tiles.append(t)
        if len(tiles) == 12: flush()
    flush(); print("sheets:", n)
def save(tiles, path):
    cols = 3; cw = max(t.width for t in tiles) + 10; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cw, rows * 194), "white")
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * cw, (i // cols) * 194))
    sh.save(path)
if __name__ == "__main__": main(sys.argv[1])
