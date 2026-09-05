#!/usr/bin/env python3
"""contact_sheets.py — render generated signs beside their AS 1743 drawings for visual review.
  python3 tools/contact_sheets.py 'tools/specs/TM/*.json' out_dir [per_sheet]
One pair per spec (the drawn hand, one representative vary value). Sheets are PNGs named <family>_NN.png."""
import csv, glob, json, os, subprocess, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from signgen import folder_for
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
OUT = os.path.join(ROOT, "Australia", "National (AS 1743)", "SVGs"); PNG = os.path.join(ROOT, "Australia", "National (AS 1743)", "Original PNGs")
def pick_value(vary):
    vals = vary["values"]
    for pref in (60, 40, 2, 300, 6, 5): 
        if pref in vals: return pref
    return vals[len(vals) // 2]
def main(pattern, outdir, per=6):
    os.makedirs(outdir, exist_ok=True)
    manifest = {r["code"]: r for r in csv.DictReader(open(os.path.join(OUT, "MANIFEST.csv")))}
    pairs = []
    for sp in sorted(glob.glob(pattern)):
        spec = json.load(open(sp))
        if spec.get("skip"): continue
        values = {spec["vary"]["key"]: pick_value(spec["vary"])} if spec.get("vary") else {}
        hand = spec.get("drawn_hand") or (spec["hands"][0] if spec.get("hands") else None)
        if hand: values.update(spec.get("hand_values", {}).get(hand, {}))
        code = spec["code"] + (f"({hand})" if hand else "")
        fname = f"{spec['name'].format(**values)}_{code}.svg"
        path = os.path.join(OUT, folder_for(spec), fname)
        if not os.path.exists(path): path = os.path.join(OUT, "intervene", folder_for(spec), fname)
        row = manifest.get(code, {})
        pairs.append((spec["code"], path if os.path.exists(path) else None, row.get("check", ""), fname))
    fam = os.path.basename(os.path.dirname(pattern.rstrip("/*.json"))) or "specs"
    n = 0
    for i in range(0, len(pairs), per):
        tiles = []
        for code, path, check, fname in pairs[i:i + per]:
            h = 360
            draw = code.split("(")[0]
            cand = [f for f in os.listdir(PNG) if f == draw + ".png" or f.startswith(draw + "(") and f.endswith(".png")]
            o = Image.open(os.path.join(PNG, cand[0])).convert("RGB") if cand else Image.new("RGB", (300, h), "grey")
            o = o.resize((max(1, int(o.width * h / o.height)), h))
            if path:
                png = os.path.join(outdir, "_r.png")
                subprocess.run([INK, path, "--export-type=png", f"--export-height={h}", "--export-background=#ffffff", f"--export-filename={png}"], capture_output=True)
                g = Image.open(png).convert("RGB") if os.path.exists(png) else Image.new("RGB", (300, h), "red")
                if g.width > 900: g = g.resize((900, int(g.height * 900 / g.width)))
            else:
                g = Image.new("RGB", (300, h), (255, 220, 220)); ImageDraw.Draw(g).text((10, 10), "NOT GENERATED\n" + check[:60], fill="black")
            if o.width > 900: o = o.resize((900, int(o.height * 900 / o.width)))
            t = Image.new("RGB", (o.width + g.width + 30, h + 24), "white"); t.paste(o, (0, 24)); t.paste(g, (o.width + 30, 24))
            ImageDraw.Draw(t).text((4, 4), f"{code}   {fname}   [{check[:80]}]", fill="black"); tiles.append(t)
        W = max(t.width for t in tiles); H = sum(t.height for t in tiles)
        sheet = Image.new("RGB", (W, H), "white"); y = 0
        for t in tiles: sheet.paste(t, (0, y)); y += t.height
        n += 1; sheet.save(os.path.join(outdir, f"{fam}_{n:02d}.png"))
    print(f"{len(pairs)} signs -> {n} sheets in {outdir}")
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6)
