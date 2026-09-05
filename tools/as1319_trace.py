#!/usr/bin/env python3
"""as1319_trace.py — vectorise the AS 1319 pictograms (Appendix B tables) from the repo's small rasters.
Each pictogram is extracted as the symbol colour only (black inside prohibition/warning signs, white inside
mandatory/emergency signs), the surrounding sign shape is discarded, and the outline is written to
tools/symbols/as1319/<id>.svg with a viewBox in units of the sign's nominal size D (0..1000 = D)."""
import os, re, subprocess, sys, tempfile
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(ROOT, "AS 1319-1994", "Original PNGs"); OUT = os.path.join(ROOT, "tools", "symbols", "as1319")
UP = 8
# id, source file, symbol colour, sign form (for the mask), category
TABLE = [
 ("no_smoking","tB1_1","black","circle","prohibition"),("no_open_flame","tB1_2","black","circle","prohibition"),
 ("no_pedestrians","tB1_3","black","circle","prohibition"),("not_drinking_water","tB1_4","black","circle","prohibition"),
 ("no_digging","tB1_5","black","circle","prohibition"),
 ("eye_protection","tB2_1","white","circle","mandatory"),("respiratory_protection","tB2_2","white","circle","mandatory"),
 ("half_mask_respirator","tB2_3","white","circle","mandatory"),("head_protection","tB2_4","white","circle","mandatory"),
 ("hearing_protection","tB2_5","white","circle","mandatory"),("hand_protection","tB2_6","white","circle","mandatory"),
 ("foot_protection","tB2_7","white","circle","mandatory"),("protective_clothing","tB2_8","white","circle","mandatory"),
 ("face_protection","tB2_9","white","circle","mandatory"),("face_screen","tB2_10","white","circle","mandatory"),
 ("general_hazard","tB3_1","black","triangle","warning"),("flammable","tB3_2","black","triangle","warning"),
 ("explosive","tB3_3","black","triangle","warning"),("toxic","tB3_4","black","triangle","warning"),
 ("corrosive","tB3_5","black","triangle","warning"),("radiation","tB3_6","black","triangle","warning"),
 ("electric_shock","tB3_7","black","triangle","warning"),("laser","tB3_8","black","triangle","warning"),
 ("moving_machinery","tB3_9","black","triangle","warning"),("forklift","tB3_10","black","triangle","warning"),
 ("non_ionising_radiation","tB3_11","black","triangle","warning"),("biohazard","tB3_12","black","triangle","warning"),
 ("guard_dog","tB3_13","black","triangle","warning"),
 ("first_aid","tB4_1","white","square","emergency"),("eye_wash","tB4_2","white","square","emergency"),
 ("safety_shower","tB4_3","white","square","emergency"),
]
def is_col(px, c):
    r, g, b = px[:3]
    return {"black": r < 100 and g < 100 and b < 100, "white": r > 190 and g > 190 and b > 190}[c]
def sign_region(img, form):
    """Pixel bbox of the coloured sign form (red annulus / blue disc / yellow triangle / green square)."""
    w, h = img.size; px = img.load(); xs = []; ys = []
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            coloured = (r > 170 and g < 140 and b < 140) or (b > 90 and r < 130 and g < 140 and b > r + 15) or (r > 190 and g > 130 and b < 110) or (g > 60 and r < 110 and b < 110 and g > r + 10)
            if coloured: xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)
def trace(sid, src, colour, form, force=False):
    outp = os.path.join(OUT, sid + ".svg")
    if os.path.exists(outp) and not force: return "exists"
    img = Image.open(os.path.join(PNG, src + ".png")).convert("RGB")
    x0, y0, x1, y1 = sign_region(img, form); D = max(x1 - x0, y1 - y0) + 1
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    crop = img.crop((x0, y0, x1 + 1, y1 + 1)); big = crop.resize((crop.width * UP, crop.height * UP), Image.LANCZOS)
    w, h = big.size; bp = big.load(); mask = Image.new("1", big.size, 255); mp = mask.load()
    # keep only symbol-colour pixels well inside the form (exclude the form's own border/annulus/slash region)
    for yy in range(h):
        for xx in range(w):
            X = (xx / UP + x0 - cx) / D * 2; Y = (yy / UP + y0 - cy) / D * 2     # -1..1 across the form
            if form == "circle": inside = X * X + Y * Y < 0.78 ** 2
            elif form == "triangle": inside = (Y > -0.55) and (abs(X) < (Y + 0.92) * 0.6) and Y < 0.75
            else: inside = abs(X) < 0.82 and abs(Y) < 0.82
            if inside and is_col(bp[xx, yy], colour): mp[xx, yy] = 0
    with tempfile.TemporaryDirectory() as td:
        pbm = os.path.join(td, "s.pbm"); mask.save(pbm)
        svg = subprocess.run(["potrace", "-s", "-t", "10", "-a", "1.2", "-O", "0.3", "-o", "-", pbm], capture_output=True, text=True, check=True).stdout
    m = re.search(r'transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([-\d.]+),([-\d.]+)\)"', svg); tx, ty, sx, sy = map(float, m.groups())
    paths = re.findall(r'<path d="([^"]+)"', svg)
    if not paths: return "nothing traced"
    # convert potrace coords -> units of D (0..1000 across the form bbox)
    k = 1000.0 / (D * UP)
    def conv(d):
        toks = re.findall(r"[MmCcLlZz]|-?\d+\.?\d*", d); out = []; i = 0; cur = None; start = None; cmd = None
        def T(x, y): return ((tx + sx * x) * k, (ty + sy * y) * k)
        def f(v): return f"{v:.1f}".rstrip("0").rstrip(".") or "0"
        while i < len(toks):
            if toks[i].isalpha(): cmd = toks[i]; i += 1; continue
            if cmd in "Mm":
                x, y = float(toks[i]), float(toks[i + 1]); i += 2
                if cmd == "m" and cur: x += cur[0]; y += cur[1]
                cur = (x, y); start = cur; X, Y = T(x, y); out.append(f"M{f(X)} {f(Y)}"); cmd = "l" if cmd == "m" else "L"
            elif cmd in "Cc":
                v = list(map(float, toks[i:i + 6])); i += 6
                if cmd == "c": v = [v[0] + cur[0], v[1] + cur[1], v[2] + cur[0], v[3] + cur[1], v[4] + cur[0], v[5] + cur[1]]
                a = T(v[0], v[1]); b = T(v[2], v[3]); c = T(v[4], v[5]); out.append(f"C{f(a[0])} {f(a[1])} {f(b[0])} {f(b[1])} {f(c[0])} {f(c[1])}"); cur = (v[4], v[5])
            elif cmd in "Ll":
                x, y = float(toks[i]), float(toks[i + 1]); i += 2
                if cmd == "l": x += cur[0]; y += cur[1]
                X, Y = T(x, y); out.append(f"L{f(X)} {f(Y)}"); cur = (x, y)
            elif cmd in "Zz": out.append("Z"); cur = start
        return "".join(out)
    d = " ".join(conv(p) for p in paths)
    os.makedirs(OUT, exist_ok=True)
    with open(outp, "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n<path fill="currentColor" fill-rule="evenodd" d="{d}"/>\n</svg>\n')
    return f"traced (form {D}px)"
if __name__ == "__main__":
    force = "--force" in sys.argv
    for sid, src, colour, form, cat in TABLE: print(sid, trace(sid, src, colour, form, force))
