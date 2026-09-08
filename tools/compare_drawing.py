#!/usr/bin/env python3
"""compare_drawing.py — a generated AS 1743 sign laid over its drawing, to check border widths, letter weight and placement.

For each code: the sign's panel is located in the drawing PNG (as the symbol tracer does), the generated SVG is rendered
to the same pixel box, and a strip is written: drawing crop | generated | overlay (red = drawing only, blue = generated
only, green = both). Handed specs compare the drawn hand against the drawing that shows it (CODE(L).png / CODE(R).png,
or the (L)-above-(R) pair in one PNG); "vary" specs use the value the drawing illustrates when the notes name it
("60 shown", "dashed '2'"), else the first value.
  python3 tools/compare_drawing.py out.png CODE [CODE ...]        (CODE may carry a value: R4-1=100, and a zoom: R4-1@0,0,0.5,0.5)"""
import os, re, sys, json, glob, subprocess, tempfile
from PIL import Image, ImageDraw, ImageChops, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trace_symbol as T
import signgen as G
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
SVG_ROOT = os.path.join(ROOT, "Complete", "Australia", "National (AS 1743)", "SVGs")

def spec_for(code):
    fs = glob.glob(os.path.join(ROOT, "tools", "specs", "*", glob.escape(code) + ".json"))
    if not fs: raise SystemExit(f"no spec for {code}")
    return json.load(open(fs[0]))

# ----------------------------------------------------------------- which drawing, which hand, which value
def drawing_for(spec):
    """(png path, hand to compare, index of that hand's panel in the drawing). Handed specs: the drawn (dimensioned)
    hand is the first panel of a PNG that shows both hands (top or left), whichever the filename order — so the drawn
    hand's own PNG (CODE(L).png) or the pair PNG, panel 0; a spec of one hand without "hands" ("R2-9(R)") whose PNG is
    named for the other hand takes the second panel. Specs of another pack ("pack": "NSW") use that pack's sheet PNGs;
    "drawing" names the sheet when it is not the code, and "which" the sign's index on a multi-size sheet (left to right)."""
    code = spec["code"]; hands = spec.get("hands"); pack = spec.get("pack"); png_dir = T.png_dir(pack)
    if pack: return T.resolve_png(spec.get("drawing", code), pack), (spec.get("drawn_hand") or hands[0]) if hands else None, spec.get("which", 0)
    if not hands:
        m = re.search(r"\((L|R)\)$", code); png = T.resolve_png(code)
        return png, None, (1 if m and not png.endswith(code + ".png") else 0)
    drawn = spec.get("drawn_hand") or hands[0]
    cands = []
    for f in sorted(os.listdir(png_dir)):
        if f.startswith(code + "(") and f.endswith(".png"):
            hs = [t for t in re.findall(r"[A-Za-z]+", f[len(code):-4]) if t in ("L", "R")]
            if hs: cands.append((os.path.join(png_dir, f), hs))
    exact = os.path.join(png_dir, code + ".png")
    if os.path.exists(exact): return exact, drawn, 0
    for p, hs in cands:
        if drawn in hs: return p, drawn, 0
    if cands: return cands[0][0], cands[0][1][0], 0
    return T.resolve_png(code), drawn, 0

def drawn_value(spec):
    """The vary value the drawing illustrates: spec "drawn_value", else a value the notes name ("60 shown",
    "dashed '2'", "shows 60"), else the first value."""
    v = spec.get("vary")
    if not v: return None
    vals = v["values"]
    if spec.get("drawn_value") is not None: return spec["drawn_value"]
    notes = spec.get("notes", "")
    for m in re.finditer(r"\b([\d.]+) shown\b|dashed '([\d.]+)'|\bdashed ([\d.]+)\b|\bshows (?:a )?([\d.]+)\b", notes):
        cand = next(g for g in m.groups() if g)
        for val in vals:
            if str(val) == cand: return val
    return vals[0]

def svg_for(spec, value, hand=None):
    name = spec["name"]; code = spec["code"] + (f"({hand})" if hand else "")
    v = dict(spec.get("hand_values", {}).get(hand, {}))
    if value is not None: v[spec["vary"]["key"]] = value
    try: name = name.format(**v)
    except (KeyError, IndexError): pass
    fs = glob.glob(os.path.join(glob.escape(G.out_root(spec)), "**", glob.escape(f"{name}_{code}.svg")), recursive=True)
    if not fs: raise SystemExit(f"no SVG for {name}_{code}")
    return fs[0]

# ----------------------------------------------------------------- locating the sign in the drawing
def _components(img, keep, min_n=1):
    """Connected components of pixels satisfying keep(px): list of dicts n, box (x0, y0, x1, y1), rows, cols
    (pixel counts per row / column, for trimming thin outlines to their straight runs)."""
    w, h = img.size; px = img.load(); mask = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            if keep(px[x, y]): mask[y * w + x] = 1
    seen = bytearray(w * h); comps = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[i] or seen[i]: continue
            stack = [i]; seen[i] = 1; n = 0; x0 = x1 = x; y0 = y1 = y; rows = {}; cols = {}
            while stack:
                j = stack.pop(); n += 1; jy, jx = divmod(j, w)
                x0 = min(x0, jx); x1 = max(x1, jx); y0 = min(y0, jy); y1 = max(y1, jy)
                rows[jy] = rows.get(jy, 0) + 1; cols[jx] = cols.get(jx, 0) + 1
                for k in (j - 1, j + 1, j - w, j + w):
                    if 0 <= k < w * h and mask[k] and not seen[k] and abs((k % w) - jx) <= 1: seen[k] = 1; stack.append(k)
            if n >= min_n: comps.append({"n": n, "box": (x0, y0, x1, y1), "rows": rows, "cols": cols})
    return comps

def _trim(c):
    """bbox of a component's long straight runs (rows / columns holding >= half the fullest one): a thin outline
    without the dimension lines that touch it."""
    rmax = max(c["rows"].values()); cmax = max(c["cols"].values())
    ry = [y for y, n in c["rows"].items() if n >= 0.5 * rmax]; cx = [x for x, n in c["cols"].items() if n >= 0.5 * cmax]
    return (min(cx), min(ry), max(cx), max(ry))

def _pick(boxes, which, soft):
    """The `which`-th box top-to-bottom then left-to-right; soft: a drawing with too few panels shows the wanted one alone."""
    if not boxes: raise SystemExit("panel not found")
    boxes = sorted(set(tuple(b) for b in boxes), key=lambda b: b[1]); rows = []   # rows: boxes that overlap vertically
    for b in boxes:
        for r in rows:
            if min(b[3], r[0][3]) - max(b[1], r[0][1]) > 0.5 * min(b[3] - b[1], r[0][3] - r[0][1]): r.append(b); break
        else: rows.append([b])
    boxes = [b for r in rows for b in sorted(r, key=lambda b: b[0])]
    if which >= len(boxes):
        if soft: which = 0
        else: raise SystemExit(f"drawing shows {len(boxes)} panel(s), wanted no. {which + 1}")
    return boxes[which]

def ground_box(img, colour, which=0, soft=True):
    """Pixel bbox of a coloured ground: the largest region of that colour plus same-coloured sub-panels beside it
    (white dividers), but not a same-coloured edge strip around it (its pieces overlap the ground's bbox)."""
    comps = [c for c in _components(img, lambda p: T.is_ground(p, colour), 400)]
    if not comps: raise SystemExit("ground colour not found")
    big = max(c["n"] for c in comps); comps = sorted([c for c in comps if c["n"] > 0.02 * big], key=lambda c: -c["n"])
    clusters = []
    for c in comps:
        x0, y0, x1, y1 = c["box"]; placed = False
        for cl in clusters:
            gap = 0.08 * max(cl[3] - cl[1], cl[4] - cl[2])
            beside = x0 >= cl[3] - 3 or x1 <= cl[1] + 3 or y0 >= cl[4] - 3 or y1 <= cl[2] + 3   # not wrapped round it like an edge strip
            thin = min(x1 - x0, y1 - y0) < 0.08 * min(cl[3] - cl[1], cl[4] - cl[2])               # a piece of an edge strip cut by dimension lines
            if beside and not thin and x0 <= cl[3] + gap and x1 >= cl[1] - gap and y0 <= cl[4] + gap and y1 >= cl[2] - gap:
                cl[0] += c["n"]; cl[1] = min(cl[1], x0); cl[2] = min(cl[2], y0); cl[3] = max(cl[3], x1); cl[4] = max(cl[4], y1); placed = True; break
        if not placed: clusters.append([c["n"], x0, y0, x1, y1])
    return _pick([cl[1:] for cl in clusters if cl[0] > 0.25 * big], which, soft)

def band_box(img, colour, aspect, which=0, soft=True):
    """Pixel bbox of a coloured border band on a white sign: the largest hollow component of that colour whose bbox
    has the band's aspect (so a legend swatch or a big letter of the same colour is passed over)."""
    w, h = img.size; cands = []
    for c in _components(img, lambda p: T.is_ground(p, colour), 400):
        x0, y0, x1, y1 = c["box"]; bw, bh = x1 - x0 + 1, y1 - y0 + 1
        if bw > 0.15 * w and c["n"] < 0.6 * bw * bh and 0.9 < (bw / bh) / aspect < 1.1: cands.append((bw * bh, c["box"]))
    if not cands: raise SystemExit(f"no {colour} border band found")
    big = max(a for a, _ in cands)
    return _pick([b for a, b in cands if a > 0.3 * big], which, soft)

def ring_box(img, colour, which=0, soft=True):
    """Pixel bbox of the largest square-ish component of `colour` (an annulus or disc), for signs without a usable outline."""
    w, h = img.size
    keep = (lambda p: T.is_ground(p, "red")) if colour == "red" else (lambda p: p[0] < 90 and p[1] < 90 and p[2] < 90)
    cands = []
    for c in _components(img, keep, 400):
        x0, y0, x1, y1 = c["box"]; bw, bh = x1 - x0, y1 - y0
        if bw > 0.15 * w and 0.9 < bw / max(bh, 1) < 1.1: cands.append((bw * bh, c["box"]))
    if not cands: raise SystemExit("no ring found")
    big = max(a for a, _ in cands)
    return _pick([b for a, b in cands if a > 0.3 * big], which, soft)

def outline_box(img, aspect, which=0, soft=True):
    """Unbordered white signs: the drawing's thin outline — a hollow dark component whose straight runs box the sign's aspect."""
    w, h = img.size; cands = []
    for c in _components(img, lambda p: p[0] < 170 and p[1] < 170 and p[2] < 170, 500):
        # the outline's sides are long straight runs; so are dimension lines touching it: take the pair of columns and
        # pair of rows among the long runs that box the sign's aspect (largest such box)
        rmax = max(c["rows"].values()); cmax = max(c["cols"].values())
        ys = sorted(y for y, n in c["rows"].items() if n >= 0.5 * rmax)[:24]; xs = sorted(x for x, n in c["cols"].items() if n >= 0.5 * cmax)[:24]
        best = None
        for x0 in xs:
            for x1 in xs:
                if x1 - x0 < 0.25 * w: continue
                for y0 in ys:
                    for y1 in ys:
                        bw, bh = x1 - x0 + 1, y1 - y0 + 1
                        if bh > 20 and 0.95 < (bw / bh) / aspect < 1.05 and (best is None or bw * bh > best[0]): best = (bw * bh, (x0, y0, x1, y1))
        if best and c["n"] < 0.5 * best[0]: cands.append(best)
    if not cands: raise SystemExit("no outline found")
    big = max(a for a, _ in cands)
    return _pick([b for a, b in cands if a > 0.3 * big], which, soft)

def diamond_box(img, colour, box):
    """Sharp bbox of a diamond ground from its straight edges (the drawings round the tips more than radius - inset):
    half-diagonal a = w(y) / 2 + |y - cy| on rows 30 % and 70 % down, w(y) the ground region's own extent on that
    row (flood-filled from the row's centre, so the same-coloured edge strip outside the border is not counted)."""
    x0, y0, x1, y1 = box; w, h = img.size; px = img.load(); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; est = []
    for f in (0.3, 0.7):
        y = int(y0 + f * (y1 - y0)); start = None
        for dx in range(0, int((x1 - x0) / 2)):          # nearest ground pixel to the centre on this row
            for x in (int(cx) + dx, int(cx) - dx):
                if x0 <= x <= x1 and T.is_ground(px[x, y], colour): start = x; break
            if start is not None: break
        if start is None: continue
        seen = set(); stack = [(start, y)]; lo = hi = start
        while stack:
            x, yy = stack.pop()
            if (x, yy) in seen or not (x0 <= x <= x1 and y0 <= yy <= y1) or not T.is_ground(px[x, yy], colour): continue
            seen.add((x, yy))
            if yy == y: lo = min(lo, x); hi = max(hi, x)
            if abs(yy - y) < 6: stack += [(x - 1, yy), (x + 1, yy), (x, yy - 1), (x, yy + 1)]   # a band of rows: enough to bridge a symbol
        est.append((hi - lo) / 2 + abs(y - cy))
    if not est: return box
    a = sum(est) / len(est)
    return (cx - a, cy - a, cx + a, cy + a)

def insets(spec, e):
    """(left, top, right, bottom) mm from the sign's sharp outline to the bbox of the detected outline inset by e:
    the rounded corners pull a triangle's bbox in unevenly (equilateral, point down)."""
    if spec.get("shape") == "triangle":
        r = max(0, spec.get("radius", 0) - e); s = 3 ** 0.5 * e + (2 / 3 ** 0.5 - 1) * r
        return (s, e, s, 2 * e + r)
    return (e, e, e, e)

def panel_box(img, spec, which=0):
    """(pixel box, (l, t, r, b) mm insets of that box from the sign outline). Coloured grounds: the ground itself;
    white signs with a black border: the border ring; a coloured border on white: that band; no border: the drawing's
    thin outline, else the annulus / disc if there is one. `which`: the panel's index when the drawing shows several
    ((L) above or left of (R)); a handed spec whose drawing shows one panel takes that panel.
    Other packs' specs (whole design-plan sheets): the sheet frame is ignored; "panel_px" [x0,y0,x1,y1] gives the
    sign's outline in the PNG directly when detection fails."""
    if spec.get("panel_px"): return tuple(spec["panel_px"]), (0, 0, 0, 0)
    sheet = bool(spec.get("pack")); soft = bool(spec.get("hands"))
    ground = spec["ground"]; e = T.reference_inset(spec); ins = insets(spec, e); W, H = spec["size"]
    layers = [spec["edge"]] if spec.get("edge") else []
    layers += spec.get("borders", [spec["border"]] if spec.get("border") else [])
    first = next((l["colour"] for l in layers if l["colour"] != "white"), None)
    if sheet:
        if ground in ("white", "none"): return T.find_white_panel(img, which, sheet), ins
        return T.find_panel(img, ground, which, sheet), ins
    if ground not in ("white", "none"):
        box = ground_box(img, ground, which, soft)
        if spec.get("shape") == "diamond":   # the sharp ground diamond sits inset * sqrt2 along the diagonals (signgen.diamond_pts)
            e0 = T.ground_inset(spec) * 2 ** 0.5; return diamond_box(img, ground, box), (e0, e0, e0, e0)
        return box, ins
    if first not in (None, "black"): return band_box(img, first, (W - ins[0] - ins[2]) / (H - ins[1] - ins[3]), which, soft), ins
    if first == "black":
        boxes = []; aspect = (W - ins[0] - ins[2]) / (H - ins[1] - ins[3])
        for i in range(6):
            try: b = T.find_white_panel(img, i, sheet)
            except SystemExit: break
            if b in boxes: break
            boxes.append(b)
        big = max((b[2] - b[0]) * (b[3] - b[1]) for b in boxes) if boxes else 0   # rings only: not a big arrow or symbol
        boxes = [b for b in boxes if (b[2] - b[0]) * (b[3] - b[1]) > 0.5 * big and 0.85 < ((b[2] - b[0]) / max(1, b[3] - b[1])) / aspect < 1.15]
        return _pick(boxes, which, soft), ins
    try: return outline_box(img, W / H, which, soft), (0, 0, 0, 0)
    except SystemExit: pass
    rings = [el for el in spec.get("elements", []) if el["type"] in ("annulus", "circle") and el.get("colour") in ("red", "black")]
    for a in rings:
        r = a.get("r_outer", a.get("r"))
        try: x0, y0, x1, y1 = ring_box(img, a["colour"], which, soft)
        except SystemExit: continue
        k = (x1 - x0) / (2 * r)
        ox, oy = x0 - (a["cx"] - r) * k, y0 - (a["cy"] - r) * k
        return (ox, oy, ox + W * k, oy + H * k), (0, 0, 0, 0)
    raise SystemExit("no outline, border or ring found")

# ----------------------------------------------------------------- render, overlay, score
def locate(spec, which, img):
    """Pixel origin and size of the whole sign in the drawing."""
    (x0, y0, x1, y1), (il, it, ir, ib) = panel_box(img, spec, which)
    W, H = spec["size"]; k = (x1 - x0) / (W - il - ir)
    return x0 - il * k, y0 - it * k, W * k, H * k

def render(svg, pw, ph):
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "g.png")
        subprocess.run([INK, svg, "--export-type=png", f"--export-width={max(1, round(pw))}", "--export-background=#ffffff", f"--export-filename={png}"], capture_output=True)
        return Image.open(png).convert("RGB").resize((max(1, round(pw)), max(1, round(ph))))

def overlay(crop, gen_c):
    """red = drawing only, blue = generated only, green = both, white = neither."""
    A = crop.convert("L"); B = gen_c.convert("L")
    return Image.merge("RGB", (B, ImageChops.invert(ImageChops.difference(A, B)), A))

def score(crop, gen_c, tol=2):
    """Differing ink / drawing ink, ignoring differences within `tol` px (anti-aliasing, the scan's own fuzz)."""
    A = crop.convert("L").point(lambda v: 255 if v < 140 else 0); B = gen_c.convert("L").point(lambda v: 255 if v < 140 else 0)
    f = ImageFilter.MaxFilter(2 * tol + 1)
    onlyA = ImageChops.subtract(A, B.filter(f)); onlyB = ImageChops.subtract(B, A.filter(f))
    ink = sum(1 for v in A.getdata() if v) or 1
    return (sum(1 for v in onlyA.getdata() if v) + sum(1 for v in onlyB.getdata() if v)) / ink

def compare(spec, value=None, hand=None, margin=0.06, zoom=None):
    """(drawing crop, generated rendered into the same box, hand, value) for a spec."""
    png, drawn, which = drawing_for(spec)
    if hand is None: hand = drawn
    if value is None: value = drawn_value(spec)
    img = Image.open(png).convert("RGB"); svg = svg_for(spec, value, hand); best = None
    for w in ([0, 1] if spec.get("hands") and not spec.get("pack") else [which]):   # a pair drawing labels its panels in no fixed order
        try: px0, py0, pw, ph = locate(spec, w, img)
        except SystemExit:
            if best is None: raise
            break
        gen = render(svg, pw, ph)
        m = int(margin * max(pw, ph))
        box = (int(px0 - m), int(py0 - m), int(px0 + pw + m), int(py0 + ph + m))
        if zoom: box = (int(px0 + zoom[0] * pw), int(py0 + zoom[1] * ph), int(px0 + zoom[2] * pw), int(py0 + zoom[3] * ph))
        crop = img.crop(box)
        gen_c = Image.new("RGB", crop.size, "white"); gen_c.paste(gen, (int(px0 - box[0]), int(py0 - box[1])))
        sc = score(crop, gen_c)
        if best is None or sc < best[0]: best = (sc, crop, gen_c)
        if (px0, py0) == best[1:2] or w == 0 and best[0] < 0.12: break   # a clear match: no need to try the other panel
    return best[1], best[2], hand, value

def strip(code, value, height=420, zoom=None):
    spec = spec_for(code)
    crop, gen_c, hand, value = compare(spec, value, zoom=zoom)
    ov = overlay(crop, gen_c); s = height / crop.height
    tiles = [t.resize((max(1, int(t.width * s)), height)) for t in (crop, gen_c, ov)]
    out = Image.new("RGB", (sum(t.width for t in tiles) + 40, height + 24), "white"); x = 0
    for t in tiles: out.paste(t, (x, 24)); x += t.width + 20
    label = code + (f"({hand})" if hand else "") + (f"={value}" if value is not None else "")
    ImageDraw.Draw(out).text((4, 4), f"{label}   drawing | generated | overlay (red = drawing only, blue = generated only, green = both)   score {score(crop, gen_c):.3f}", fill="black")
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
