#!/usr/bin/env python3
"""svg_sheets.py — contact sheets of every SVG in a pack (no source page), N per image, for a quick visual review.
  python3 tools/svg_sheets.py <pack_dir> <out_dir> [per_sheet]"""
import os, sys, csv, subprocess
from PIL import Image, ImageDraw
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
def main(pack, out, per=30):
    os.makedirs(out, exist_ok=True); rows = [r for r in csv.DictReader(open(os.path.join(pack, "SVGs", "MANIFEST.csv"))) if r.get("file")]
    tiles = []; n = 0
    def flush():
        nonlocal tiles, n
        if not tiles: return
        n += 1; cols = 6; cw = 330; rh = 250; rows_ = (len(tiles) + cols - 1) // cols
        sh = Image.new("RGB", (cols * cw, rows_ * rh), "white")
        for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * cw, (i // cols) * rh))
        sh.save(os.path.join(out, f"{os.path.basename(pack).replace(' ', '_')}_{n:03d}.png")); tiles = []
    for r in rows:
        f = r["file"] if "/" in r["file"] else os.path.join(r.get("family", ""), r["file"])
        svg = os.path.join(pack, "SVGs", f); png = os.path.join(out, "_r.png")
        if os.path.exists(png): os.remove(png)
        subprocess.run([INK, svg, "--export-type=png", "--export-height=200", "--export-background=#dddddd", f"--export-filename={png}"], capture_output=True)
        try: b = Image.open(png).convert("RGB")
        except Exception: b = Image.new("RGB", (100, 200), "red")
        if b.width > 310: b = b.resize((310, max(1, int(b.height * 310 / b.width))))
        t = Image.new("RGB", (330, 250), "white"); t.paste(b, (5, 28))
        note = r.get("notes", r.get("check", "")); ImageDraw.Draw(t).text((3, 3), f"{r['code']} {r['name'][:26]}", fill="black"); ImageDraw.Draw(t).text((3, 14), f"{r.get('drawn_size', r.get('size', ''))} {'!' if 'check' in note else ''}", fill="gray")
        tiles.append(t)
        if len(tiles) == per: flush()
    flush(); print("sheets:", n)
if __name__ == "__main__": main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30)
