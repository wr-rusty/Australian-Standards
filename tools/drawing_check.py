#!/usr/bin/env python3
"""drawing_check.py — score every generated AS 1743 sign against its drawing (border width, letter weight, placement).

For each spec: the sign is located in the drawing PNG (compare_drawing.panel_box), the generated SVG (the drawn hand
against the drawing that shows it; the `vary` value the drawing illustrates where the notes name one, else the first)
is rendered to the same box, and the two are compared as ink masks inside the panel (plus 2 %): score = differing
pixels / ink pixels of the drawing, ignoring differences within 2 px. Dashed placeholders ("Varies" legends) and
traced symbols inflate the score, so it ranks; a person judges. Writes <out>.csv (code, file, score, value, note) and
<out>.png (the worst N overlays: red = drawing only, blue = generated only, green = both).
  python3 tools/drawing_check.py out FAMILY [FAMILY ...]     (FAMILY = spec folder: R, W, TM, G, GE, T, MISC; N via env WORST)"""
import os, sys, csv, json, glob
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_drawing as C, signgen as G
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check(spec):
    crop, gen_c, hand, value = C.compare(spec, margin=0.02)
    code = spec["code"] + (f"({hand})" if hand else "")
    return C.score(crop, gen_c), crop, gen_c, C.overlay(crop, gen_c), os.path.basename(C.svg_for(spec, value, hand)), code, value

def main(out, fams):
    worst_n = int(os.environ.get("WORST", 40)); rows = []; strips = []
    for fam in fams:
        for sp in sorted(glob.glob(os.path.join(ROOT, "tools", "specs", fam, "*.json"))):
            spec = json.load(open(sp))
            if spec.get("skip") or G.folder_for(spec) in G.EXCLUDE_FOLDERS: continue
            try: res, note = check(spec), ""
            except SystemExit as ex: res, note = None, str(ex)
            except Exception as ex: res, note = None, f"error: {ex}"
            if res is None: rows.append([spec["code"], "", "", "", note]); print(f"{spec['code']:14} ---   {note}", flush=True); continue
            score, crop, gen_c, ov, fname, code, value = res
            rows.append([code, fname, f"{score:.3f}", "" if value is None else value, ""]); strips.append((score, code, crop, gen_c, ov))
            print(f"{code:14} {score:.3f}", flush=True)
    with open(out + ".csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "file", "score", "value", "note"]); w.writerows(sorted(rows, key=lambda r: -(float(r[2]) if r[2] else -1)))
    strips.sort(key=lambda s: -s[0]); strips = strips[:worst_n]
    if strips:
        h = 220; tiles = []
        for score, code, crop, gen_c, ov in strips:
            s = h / crop.height; ims = [t.resize((max(1, int(t.width * s)), h)) for t in (crop, gen_c, ov)]
            t = Image.new("RGB", (sum(i.width for i in ims) + 30, h + 20), "white"); x = 0
            for i in ims: t.paste(i, (x, 20)); x += i.width + 15
            ImageDraw.Draw(t).text((3, 3), f"{code}  score {score:.2f}", fill="black"); tiles.append(t)
        cols = 2; rows_ = (len(tiles) + cols - 1) // cols; cw = max(t.width for t in tiles)
        sheet = Image.new("RGB", (cols * (cw + 10), rows_ * (h + 30)), "white")
        for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * (cw + 10), (i // cols) * (h + 30)))
        sheet.save(out + ".png")
    print(f"{len(rows)} specs; {sum(1 for r in rows if r[4])} not comparable; results in {out}.csv / {out}.png")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
