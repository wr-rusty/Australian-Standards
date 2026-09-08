#!/usr/bin/env python3
"""compare_drawing.py — a generated AS 1743 sign laid over its drawing, to check border widths, letter weight and placement.

For each code: the sign's panel is located in the drawing PNG (as the symbol tracer does), the generated SVG is rendered
to the same pixel box, and a strip is written: drawing crop | generated | overlay (drawing in red, generated in blue:
where they agree the result is dark, a red or blue fringe is a difference).
  python3 tools/compare_drawing.py out.png CODE [CODE ...]        (CODE may carry a value: R4-1=100)"""
import os, sys, json, glob, subprocess, tempfile
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trace_symbol as T
import signgen as G
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
SVG_ROOT = os.path.join(ROOT, "Complete", "Australia", "National (AS 1743)", "SVGs")

def spec_for(code):
    fs = glob.glob(os.path.join(ROOT, "tools", "specs", "*", code + ".json"))
    if not fs: raise SystemExit(f"no spec for {code}")
    return json.load(open(fs[0]))

def svg_for(spec, value):
    name = spec["name"]; code = spec["code"]
    if value is not None: name = name.replace("{" + spec["vary"]["key"] + "}", str(value))
    fs = glob.glob(os.path.join(SVG_ROOT, "**", f"{name}_{code}.svg"), recursive=True)
    if not fs: raise SystemExit(f"no SVG for {name}_{code}")
    return fs[0]

def ring_box(img, colour):
    """Pixel bbox of the largest square-ish component of `colour` (an annulus), for signs without a usable outline."""
    w, h = img.size; px = img.load(); mask = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if (colour == "red" and T.is_ground(px[x, y], "red")) or (colour == "black" and r < 90 and g < 90 and b < 90): mask[y * w + x] = 1
    seen = bytearray(w * h); best = None
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[i] or seen[i]: continue
            stack = [i]; seen[i] = 1; n = 0; x0 = x1 = x; y0 = y1 = y
            while stack:
                j = stack.pop(); n += 1; jy, jx = divmod(j, w)
                x0 = min(x0, jx); x1 = max(x1, jx); y0 = min(y0, jy); y1 = max(y1, jy)
                for k in (j - 1, j + 1, j - w, j + w):
                    if 0 <= k < w * h and mask[k] and not seen[k] and abs((k % w) - jx) <= 1: seen[k] = 1; stack.append(k)
            bw, bh = x1 - x0, y1 - y0
            if bw > 0.15 * w and 0.9 < bw / max(bh, 1) < 1.1 and (best is None or bw * bh > best[0]): best = (bw * bh, x0, y0, x1, y1)
    if best is None: raise SystemExit("no ring found")
    return best[1:]

def panel_box(img, spec):
    """(pixel box, mm inset of that box from the sign outline). Coloured grounds and bordered white signs use the tracer's
    detection; white signs with an annulus are located by the ring itself (top-most annulus element, first hand)."""
    ann = [e for e in spec.get("elements", []) if e["type"] == "annulus"]
    if spec["ground"] == "white" and ann and not (spec.get("border") or spec.get("edge")):
        a = ann[0]
        try: x0, y0, x1, y1 = ring_box(img, "red" if a["colour"] == "red" else "black")
        except SystemExit: return T.find_white_panel(img), T.reference_inset(spec)
        k = (x1 - x0) / (2 * a["r_outer"]); W, H = spec["size"]
        return (x0 - (a["cx"] - a["r_outer"]) * k, y0 - (a["cy"] - a["r_outer"]) * k, x0 - (a["cx"] - a["r_outer"]) * k + W * k, y0 - (a["cy"] - a["r_outer"]) * k + H * k), 0
    if spec["ground"] in ("white", "none"): return T.find_white_panel(img), T.reference_inset(spec)
    return T.find_panel(img, spec["ground"]), T.reference_inset(spec)

def strip(code, value, height=420, zoom=None):
    spec = spec_for(code); img = Image.open(T.resolve_png(code)).convert("RGB")
    (x0, y0, x1, y1), inset = panel_box(img, spec)
    W, H = spec["size"]; k = (x1 - x0) / (W - 2 * inset)          # px per mm
    px0, py0 = x0 - inset * k, y0 - inset * k; pw, ph = W * k, H * k
    svg = svg_for(spec, value)
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "g.png")
        subprocess.run([INK, svg, "--export-type=png", f"--export-width={max(1, round(pw))}", "--export-background=#ffffff", f"--export-filename={png}"], capture_output=True)
        gen = Image.open(png).convert("RGB").resize((max(1, round(pw)), max(1, round(ph))))
    m = int(0.06 * max(pw, ph))
    box = (int(px0 - m), int(py0 - m), int(px0 + pw + m), int(py0 + ph + m))
    if zoom:   # fractions of the sign (x0, y0, x1, y1) to look at closely
        box = (int(px0 + zoom[0] * pw), int(py0 + zoom[1] * ph), int(px0 + zoom[2] * pw), int(py0 + zoom[3] * ph))
    crop = img.crop(box)
    gen_c = Image.new("RGB", crop.size, "white"); gen_c.paste(gen, (int(px0 - box[0]), int(py0 - box[1])))
    A = crop.convert("L"); B = gen_c.convert("L")
    ov = Image.merge("RGB", (A, Image.new("L", A.size, 255), B))
    s = height / crop.height
    tiles = [t.resize((max(1, int(t.width * s)), height)) for t in (crop, gen_c, ov)]
    out = Image.new("RGB", (sum(t.width for t in tiles) + 40, height + 24), "white"); x = 0
    for t in tiles: out.paste(t, (x, 24)); x += t.width + 20
    ImageDraw.Draw(out).text((4, 4), f"{code}{'=' + str(value) if value is not None else ''}   drawing | generated | overlay (red = drawing only, blue = generated only)", fill="black")
    return out

def main(out, codes):
    strips = []
    for c in codes:
        code, _, value = c.partition("=")
        zoom = None
        if "@" in value or "@" in code:   # CODE=val@x0,y0,x1,y1 (fractions of the sign)
            head, _, z = (value if "@" in value else code).partition("@"); zoom = [float(v) for v in z.split(",")]
            if "@" in value: value = head
            else: code = head
        try: strips.append(strip(code, value or None, 600 if zoom else 420, zoom))
        except SystemExit as ex: print(code, ex)
    sheet = Image.new("RGB", (max(s.width for s in strips), sum(s.height for s in strips) + 10 * len(strips)), "white"); y = 0
    for s in strips: sheet.paste(s, (0, y)); y += s.height + 10
    sheet.save(out); print(out, sheet.size)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
