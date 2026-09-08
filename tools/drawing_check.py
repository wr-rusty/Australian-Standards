#!/usr/bin/env python3
"""drawing_check.py — score every generated AS 1743 sign against its drawing (border width, letter weight, placement).

For each spec: the sign is located in the drawing PNG (compare_drawing.panel_box), the generated SVG (the drawn hand,
the drawn `vary` value where the drawing names one, else the first value) is rendered to the same box, and the two
are compared as ink masks: score = differing pixels / ink pixels of the drawing, inside the panel and 6 % beyond it.
Dashed placeholders ("Varies" legends) and traced symbols inflate the score, so it ranks; a person judges.
Writes <out>.csv (code, file, score, note) and <out>.png (the worst N overlays).
  python3 tools/drawing_check.py out FAMILY [FAMILY ...]     (FAMILY = spec folder: R, W, TM, G, GE, T, MISC; N via env WORST)"""
import os, sys, csv, json, glob, subprocess, tempfile
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_drawing as C, trace_symbol as T, signgen as G
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def drawn_value(spec):
    v = spec.get("vary")
    if not v: return None
    shown = spec.get("drawn_value")
    return shown if shown is not None else v["values"][0]

def check(spec):
    hand = spec.get("drawn_hand") or (spec.get("hands") or [None])[0]
    value = drawn_value(spec)
    values = {spec["vary"]["key"]: value} if value is not None else {}
    values.update(spec.get("hand_values", {}).get(hand, {}))
    code = spec["code"] + (f"({hand})" if hand else "")
    fname = f"{spec['name'].format(**values)}_{code}.svg"
    fs = glob.glob(os.path.join(C.SVG_ROOT, "**", fname), recursive=True)
    if not fs: return None, "no SVG " + fname
    img = Image.open(T.resolve_png(spec["code"] if not spec.get("hands") else spec["code"])).convert("RGB")
    try: (x0, y0, x1, y1), inset = C.panel_box(img, spec)
    except SystemExit as ex: return None, str(ex)
    W, H = spec["size"]; k = (x1 - x0) / (W - 2 * inset)
    px0, py0 = x0 - inset * k, y0 - inset * k; pw, ph = W * k, H * k
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "g.png")
        subprocess.run([C.INK, fs[0], "--export-type=png", f"--export-width={max(1, round(pw))}", "--export-background=#ffffff", f"--export-filename={png}"], capture_output=True)
        gen = Image.open(png).convert("RGB").resize((max(1, round(pw)), max(1, round(ph))))
    m = int(0.06 * max(pw, ph)); box = (int(px0 - m), int(py0 - m), int(px0 + pw + m), int(py0 + ph + m))
    crop = img.crop(box); gen_c = Image.new("RGB", crop.size, "white"); gen_c.paste(gen, (int(px0 - box[0]), int(py0 - box[1])))
    A = crop.convert("L").point(lambda v: 255 if v < 140 else 0); B = gen_c.convert("L").point(lambda v: 255 if v < 140 else 0)
    from PIL import ImageChops
    diff = ImageChops.difference(A, B)
    ink = sum(1 for v in A.getdata() if v) or 1; d = sum(1 for v in diff.getdata() if v)
    ov = Image.merge("RGB", (crop.convert("L"), Image.new("L", crop.size, 255), gen_c.convert("L")))
    return (d / ink, crop, gen_c, ov, fname), ""

def main(out, fams):
    worst_n = int(os.environ.get("WORST", 40)); rows = []; strips = []
    for fam in fams:
        for sp in sorted(glob.glob(os.path.join(ROOT, "tools", "specs", fam, "*.json"))):
            spec = json.load(open(sp))
            if spec.get("skip") or G.folder_for(spec) in G.EXCLUDE_FOLDERS: continue
            try: res, note = check(spec)
            except SystemExit as ex: res, note = None, str(ex)
            except Exception as ex: res, note = None, f"error: {ex}"
            if res is None: rows.append([spec["code"], "", "", note]); continue
            score, crop, gen_c, ov, fname = res
            rows.append([spec["code"], fname, f"{score:.3f}", ""]); strips.append((score, spec["code"], crop, gen_c, ov))
            print(f"{spec['code']:14} {score:.3f}", flush=True)
    with open(out + ".csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "file", "score", "note"]); w.writerows(sorted(rows, key=lambda r: -(float(r[2]) if r[2] else -1)))
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
    print(f"{len(rows)} specs; {sum(1 for r in rows if r[3])} not comparable; results in {out}.csv / {out}.png")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
