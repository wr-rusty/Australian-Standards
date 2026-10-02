import sys, os, json, glob
sys.path.insert(0, "tools")
import compare_drawing as C
from PIL import Image, ImageDraw
out = sys.argv[1]; codes = sys.argv[2:]
tiles = []; H = int(__import__('os').environ.get('OVH','230'))
for code in codes:
    try:
        spec = C.spec_for(code)
        if spec.get("skip"): continue
        crop, gen, h, v = C.compare(spec)
        sc = C.score(crop, gen); print(f"{code}\t{sc:.3f}")
        ov = C.overlay(crop, gen); s = H / crop.height
        parts = [t.resize((max(1, int(t.width * s)), H)) for t in (crop, gen, ov)]
        t = Image.new("RGB", (sum(p.width for p in parts) + 10, H + 16), "white"); x = 0
        for p in parts: t.paste(p, (x, 16)); x += p.width + 5
        ImageDraw.Draw(t).text((2, 2), f"{code}{'=' + str(v) if v is not None else ''}  {sc:.3f}", fill="black"); tiles.append(t)
    except SystemExit as ex: print(code, "FAIL", ex)
    except Exception as ex: print(code, "ERR", repr(ex))
# pack tiles into rows up to 2000 px wide, pages up to 6 rows
rows = [[]]
for t in tiles:
    if sum(x.width for x in rows[-1]) + t.width > 2000 and rows[-1]: rows.append([])
    rows[-1].append(t)
per = int(os.environ.get("PER", 6))
for i in range(0, len(rows), per):
    rs = rows[i:i + per]
    sheet = Image.new("RGB", (2000, len(rs) * (H + 20)), "#b0b0b0"); y = 0
    for r in rs:
        x = 0
        for t in r: sheet.paste(t, (x, y)); x += t.width + 6
        y += H + 20
    sheet.save(f"{out}_{i // per:02d}.png")
