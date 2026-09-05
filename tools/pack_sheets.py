#!/usr/bin/env python3
"""pack_sheets.py — review sheets for a sheet-extracted pack: source PDF page beside the extracted SVG, 9 pairs per image.
  python3 tools/pack_sheets.py <pack_dir> <out_dir> [limit]   (pack_dir holds SVGs/MANIFEST.csv with a 'source' column)"""
import os, sys, csv, subprocess, pymupdf
from PIL import Image, ImageDraw
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
def main(pack, out, limit=None):
    os.makedirs(out, exist_ok=True); tiles = []; n = 0; done = 0
    def flush():
        nonlocal tiles, n
        if tiles: n += 1; save(tiles, os.path.join(out, f"{os.path.basename(pack).replace(' ', '_')}_{n:03d}.png")); tiles = []
    for row in csv.DictReader(open(os.path.join(pack, "SVGs", "MANIFEST.csv"))):
        if not row["file"]: continue
        if limit and done >= limit: break
        done += 1
        src, _, pg = row["source"].partition("#page=")
        if not src.lower().endswith(".pdf"):                    # a DWG source: show the sibling PDF scan if there is one
            sib = os.path.splitext(src)[0] + ".pdf"; src = sib if os.path.exists(os.path.join(pack, sib)) else ""
        if src:
            page = pymupdf.open(os.path.join(pack, src))[int(pg) - 1 if pg else 0]; pix = page.get_pixmap(dpi=36); a = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        else: a = Image.new("RGB", (200, 300), "white")
        if a.height > 300: a = a.resize((int(a.width * 300 / a.height), 300))
        svg = os.path.join(pack, "SVGs", row["family"], row["file"]); png = os.path.join(out, "_r.png")
        if os.path.exists(png): os.remove(png)
        subprocess.run([INK, svg, "--export-type=png", "--export-height=240", "--export-background=#dddddd", f"--export-filename={png}"], capture_output=True)
        try: b = Image.open(png).convert("RGB")
        except Exception: b = Image.new("RGB", (100, 240), "red")
        if b.width > 360: b = b.resize((360, int(b.height * 360 / b.width)))
        t = Image.new("RGB", (a.width + b.width + 16, 325), "white"); t.paste(a, (0, 22)); t.paste(b, (a.width + 16, 22))
        ImageDraw.Draw(t).text((2, 3), f"{row['code']} {row['name'][:28]} [{row['size']}{' !' if 'check' in row['notes'] else ''}]", fill="black"); tiles.append(t)
        if len(tiles) == 9: flush()
    flush(); print("sheets:", n)
def save(tiles, path):
    cols = 3; cw = max(t.width for t in tiles) + 10; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cw, rows * 327), "white")
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * cw, (i // cols) * 327))
    sh.save(path)
if __name__ == "__main__": main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
