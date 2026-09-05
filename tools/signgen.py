#!/usr/bin/env python3
"""
signgen.py — generate AS 1743 sign SVGs from JSON specs (tools/specs/**/*.json).

Rules (agreed with Russell, Sept 2026):
* One SVG per drawing at the size the standard illustrates. Variants only where the
  standard draws a meaningful difference: legend values that "vary" (speeds), (L)/(R).
* Header matches Russell's Illustrator speed-sign exports: viewBox in points at
  1 pt = 1 cm of drawn sign (a 600 mm sign -> viewBox 60 wide), width/height given in
  mm at 72 pt/in (60 pt = 21.17mm), e.g. his 60_SPEED_SIGN.svg is
  width="23.25mm" height="30.78mm" viewBox="0 0 65.91 87.26". Specs stay in mm.
* Text is outlined from the FHWA Series fonts with AS 1744 spacing (plus0 tracking).
* Nothing not on the drawing is added.  Symbols come from tools/symbols/<id>.svg
  (traced from the drawings, flagged in the manifest).

Output: <repo>/AS 1743-2023/Processed/<folder>/<NAME>_<CODE>[(L|R)].svg + MANIFEST.csv
"""
import csv, glob, json, math, os, re, sys, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arrows as _arrows
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "Fonts", "fhwa-series-font-family")
SYM_DIR = os.path.join(ROOT, "tools", "symbols")
OUT_ROOT = os.path.join(ROOT, "AS 1743-2023", "Processed")
SERIES_FILES = {"B": "Fhwaseriesb2025{t}.otf", "C": "Fhwaseriesc2024{t}.otf",
                "D": "Fhwaseriesd2024{t}.otf", "E": "Fhwaseriese2024{t}.otf",
                "Emod": "Fhwaseriesemod2024{t}.otf", "F": "Fhwaseriesf2025{t}.otf"}
CAP = 8000
MM = 80   # font units per mm at 100 mm cap height (10000 upm, cap 8000)
# AS 1744 hyphen spacing (left, width, right) at 100 mm cap; the FHWA fonts' hyphen glyph is 50/50/50
HYPHEN = {"B": (3, 31, 3), "C": (3, 35, 3), "D": (3, 35, 3), "E": (3, 35, 3), "Emod": (3, 35, 3), "F": (4, 35, 4)}
COLOURS = {"yellow": "#ffe40d", "red": "#ed1c24", "white": "#fff", "black": "#000",
           "orange": "#f58020", "green": "#0b804c", "blue": "#3a53a4", "brown": "#754c24",
           "yellowgreen": "#c4d82e", "grey": "#8c8c8c"}
KEYLINE_MM = 2.0
WIDTH_MISMATCH_TO_INTERVENE = False
EXCLUDE_FOLDERS = {"Freeway Signs", "Guide Signs"}   # not traffic signs for the platform (Russell, 2026-09-05); specs kept, not generated   # drawing width figures that contradict AS 1744 spacing are accepted as typos (Russell, 2026-09-05)
OUT_SCALE = 0.1   # mm -> output units (1 unit = 1 cm)

def col(c): return COLOURS.get(c, c)
def fmt(v):
    if isinstance(v, float): return f"{v:.2f}".rstrip("0").rstrip(".") or "0"
    return str(v)

# ----------------------------------------------------------------- fonts / text
_faces = {}
class Face:
    def __init__(self, series, tracking="plus0"):
        self.series = series
        self.font = TTFont(os.path.join(FONT_DIR, SERIES_FILES[series].format(t=tracking)))
        self.gs = self.font.getGlyphSet(); self.cmap = self.font.getBestCmap(); self._b = {}
    def bounds(self, g):
        if g not in self._b:
            p = BoundsPen(self.gs); self.gs[g].draw(p); self._b[g] = p.bounds or (0, 0, 0, 0)
        return self._b[g]
    def glyph(self, ch):
        """(name, advance, ink_left, ink_right, x_scale, x_shift) in font units; hyphen re-spaced per AS 1744."""
        n = self.cmap[ord(ch)]; b = self.bounds(n)
        if ch == "-":
            l, w, r = HYPHEN[self.series]
            sx = (w * MM) / (b[2] - b[0]); shift = l * MM - b[0] * sx
            return n, (l + w + r) * MM, l * MM, (l + w) * MM, sx, shift
        return n, self.gs[n].width, b[0], b[2], 1.0, 0.0
    def layout(self, text):
        gl = [self.glyph(ch) for ch in text]
        xs, x = [], 0
        for g in gl: xs.append(x); x += g[1]
        return gl, xs, gl[0][2], xs[-1] + gl[-1][3]
    def ink_width(self, text, H):
        _, _, l, r = self.layout(text); return (r - l) * H / CAP
    def path(self, text, H, x_ink_left, baseline):
        gl, xs, l, _ = self.layout(text); s = H / CAP; d = []
        for g, x in zip(gl, xs):
            n, _, _, _, sx, shift = g
            pen = SVGPathPen(self.gs, ntos=fmt)
            self.gs[n].draw(TransformPen(pen, (s * sx, 0, 0, -s, x_ink_left + (x - l + shift) * s, baseline)))
            d.append(pen.getCommands())
        return " ".join(d)

def face(series, tracking="plus0"):
    key = (series, tracking)
    if key not in _faces: _faces[key] = Face(series, tracking)
    return _faces[key]

# ----------------------------------------------------------------- geometry
def rounded_rect_path(x, y, w, h, r):
    r = max(0, min(r, w / 2, h / 2))
    if r == 0: return f"M{fmt(x)} {fmt(y)}h{fmt(w)}v{fmt(h)}h{fmt(-w)}Z"
    return (f"M{fmt(x + r)} {fmt(y)}h{fmt(w - 2 * r)}a{fmt(r)} {fmt(r)} 0 0 1 {fmt(r)} {fmt(r)}"
            f"v{fmt(h - 2 * r)}a{fmt(r)} {fmt(r)} 0 0 1 {fmt(-r)} {fmt(r)}h{fmt(-(w - 2 * r))}"
            f"a{fmt(r)} {fmt(r)} 0 0 1 {fmt(-r)} {fmt(-r)}v{fmt(-(h - 2 * r))}a{fmt(r)} {fmt(r)} 0 0 1 {fmt(r)} {fmt(-r)}Z")

def rounded_polygon_path(pts, r):
    """r: one radius for every corner, or a list with one radius per vertex."""
    n = len(pts); out = []; radii = r if isinstance(r, (list, tuple)) else [r] * n
    for i in range(n):
        r = radii[i]
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*v1); l2 = math.hypot(*v2); u1 = (v1[0] / l1, v1[1] / l1); u2 = (v2[0] / l2, v2[1] / l2)
        theta = math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])))
        t = r / math.tan(theta / 2) if r > 0 else 0
        a = (p1[0] + u1[0] * t, p1[1] + u1[1] * t); b = (p1[0] + u2[0] * t, p1[1] + u2[1] * t)
        out.append((a, b, 0 if (u1[0] * u2[1] - u1[1] * u2[0]) > 0 else 1))
    d = f"M{fmt(out[0][0][0])} {fmt(out[0][0][1])}"
    for i in range(n):
        a, b, sw = out[i]; r = radii[i]
        if r > 0: d += f"A{fmt(r)} {fmt(r)} 0 0 {sw} {fmt(b[0])} {fmt(b[1])}"
        na = out[(i + 1) % n][0]; d += f"L{fmt(na[0])} {fmt(na[1])}"
    return d + "Z"

def octagon_pts(w, inset=0):
    s = w - 2 * inset; c = s * (1 - 1 / (1 + math.sqrt(2))) / 2; o = inset
    return [(o + c, o), (o + s - c, o), (o + s, o + c), (o + s, o + s - c), (o + s - c, o + s), (o + c, o + s), (o, o + s - c), (o, o + c)]

def triangle_pts(W, h, inset=0):
    cx = W / 2; hh = h - 3 * inset; ww = hh * 2 / math.sqrt(3); top = inset
    return [(cx - ww / 2, top), (cx + ww / 2, top), (cx, top + hh)]

def diamond_pts(W, H, inset=0):
    """Square on its corner; W = H = diagonal. Inset is perpendicular to the edges."""
    d = inset * math.sqrt(2); cx, cy = W / 2, H / 2
    return [(cx, d), (W - d, cy), (cx, H - d), (d, cy)]

def pentagon_pts(W, H, inset=0):
    """Route-marker shield (G8-9): flat top, points down-left/right, apex at bottom centre."""
    # approximated from G8-9-1: top width W, shoulders at 111 below top, bottom width 200/360 of W
    top_w = W - 2 * inset; sh = 0.31 * H; bw = 0.556 * W
    return [(inset, inset), (W - inset, inset), (W - inset, sh), ((W + bw) / 2 - inset * 0.3, H - inset), ((W - bw) / 2 + inset * 0.3, H - inset), (inset, sh)]

def circle_path(cx, cy, r):
    return f"M{fmt(cx - r)} {fmt(cy)}a{fmt(r)} {fmt(r)} 0 1 0 {fmt(2 * r)} 0a{fmt(r)} {fmt(r)} 0 1 0 {fmt(-2 * r)} 0Z"

def shape_path(spec, W, H, inset, radius):
    kind = spec.get("shape", "rect")
    if kind == "rect": return rounded_rect_path(inset, inset, W - 2 * inset, H - 2 * inset, max(0, radius - inset))
    if kind == "octagon": return rounded_polygon_path(octagon_pts(W, inset), max(0, radius - inset))
    if kind == "triangle": return rounded_polygon_path(triangle_pts(W, H, inset), max(0, radius - inset))
    if kind == "diamond": return rounded_polygon_path(diamond_pts(W, H, inset), max(0, radius - inset))
    if kind == "circle": return circle_path(W / 2, H / 2, W / 2 - inset)
    raise ValueError(kind)

# ----------------------------------------------------------------- symbols
_symbols = {}
def symbol_paths(sid):
    """Return (list of (d, fill), bbox) for tools/symbols/<sid>.svg (any <path> elements)."""
    if sid in _symbols: return _symbols[sid]
    p = os.path.join(SYM_DIR, sid + ".svg")
    if not os.path.exists(p): raise FileNotFoundError(f"symbol {sid} missing ({p})")
    tree = ET.parse(p); root = tree.getroot()
    vb = [float(v) for v in root.get("viewBox").split()]
    paths = []
    for el in root.iter():
        if el.tag.endswith("path"): paths.append((el.get("d"), el.get("fill", "currentColor")))
    _symbols[sid] = (paths, vb); return _symbols[sid]

# ----------------------------------------------------------------- build one sign
def series_for(el, text):
    s = el.get("series", "D")
    if s == "speed": return "D" if len(text) <= 2 or text in ("110", "115") else "C"
    return s

def build(spec, values, hand=None):
    W, H = float(spec["size"][0]), float(spec["size"][1])
    def sub(s): return s.format(**values) if isinstance(s, str) else s
    radius = spec.get("radius", 0)
    OW, OH = W * OUT_SCALE, H * OUT_SCALE
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{fmt(OW * 25.4 / 72)}mm" height="{fmt(OH * 25.4 / 72)}mm" viewBox="0 0 {fmt(OW)} {fmt(OH)}">',
           f'<g transform="scale({fmt(OUT_SCALE)})">',
           '  <g id="panel">']
    inset = 0.0
    edge = spec.get("edge")
    if edge:
        out.append(f'    <path id="edge" fill="{col(edge["colour"])}" d="{shape_path(spec, W, H, 0, radius)}"/>'); inset = edge["width"]
    for i, border in enumerate(spec.get("borders", [spec["border"]] if spec.get("border") else [])):
        bi = inset + border.get("inset", 0)
        out.append(f'    <path id="border{i or ""}" fill="{col(border["colour"])}" d="{shape_path(spec, W, H, bi, radius)}"/>')
        inset = bi + border["width"]
    if spec["ground"] != "none":   # "none": transparent — the sign's own shape is drawn by polygon/path elements
        out.append(f'    <path id="ground" fill="{col(spec["ground"])}" d="{shape_path(spec, W, H, inset, radius)}"/>')
    if spec.get("keyline"):
        out.append(f'    <path id="keyline" fill="#000" fill-rule="evenodd" d="{shape_path(spec, W, H, 0, radius)} {shape_path(spec, W, H, KEYLINE_MM, radius)}"/>')
    out.append('  </g>\n  <g id="legend">')
    checks, flags = [], []
    mirror = hand == "R" and spec.get("drawn_hand", "L") == "L" or hand == "L" and spec.get("drawn_hand") == "R"
    def mx(x): return W - x if mirror else x
    for el in spec.get("elements", []):
        if el.get("hand") and hand and el["hand"] != hand: continue
        t = el["type"]; colour = col(el.get("colour", "black"))
        if t == "annulus":
            out.append(f'    <path fill="{colour}" fill-rule="evenodd" d="{circle_path(mx(el["cx"]), el["cy"], el["r_outer"])} {circle_path(mx(el["cx"]), el["cy"], el["r_inner"])}"/>')
        elif t == "circle":
            out.append(f'    <circle fill="{colour}" cx="{fmt(mx(el["cx"]))}" cy="{fmt(el["cy"])}" r="{fmt(el["r"])}"/>')
        elif t == "rect":
            x = el["x"]; w = el["w"]
            if mirror: x = W - x - w
            out.append(f'    <rect fill="{colour}" x="{fmt(x)}" y="{fmt(el["y"])}" width="{fmt(w)}" height="{fmt(el["h"])}"' + (f' rx="{fmt(el["rx"])}"' if el.get("rx") else "") + '/>')
        elif t == "panel":   # sub-panel (e.g. white road-name panel on guide signs)
            out.append(f'    <path fill="{colour}" d="{rounded_rect_path(el["x"], el["y"], el["w"], el["h"], el.get("radius", 0))}"/>')
        elif t == "path":    # raw path in mm coordinates (hand-entered geometry, e.g. bars, stripes)
            tr = f' transform="translate({fmt(W)} 0) scale(-1 1)"' if mirror and el.get("mirror", True) else ""
            out.append(f'    <path fill="{colour}" d="{el["d"]}"{tr}/>')
        elif t == "polygon":
            pts = el["points"]
            if mirror and el.get("mirror", True): pts = [(W - x, y) for x, y in pts]
            st = el.get("stroke")   # optional outline: {"colour": "black", "width": 2}, drawn inside the fill edge
            stroke = f' stroke="{col(st["colour"])}" stroke-width="{fmt(st["width"])}" stroke-linejoin="round"' if st else ""
            out.append(f'    <path fill="{colour}"{stroke} d="{rounded_polygon_path(pts, el.get("radius", 0))}"/>')
        elif t == "arrow":   # geometric arrow from stated dimensions (tools/arrows.py)
            d, warn = _arrows.place(el, W)
            if warn: flags.append(f"arrow-size:{warn}")
            tr = f' transform="translate({fmt(W)} 0) scale(-1 1)"' if mirror and el.get("mirror", True) else ""
            out.append(f'    <path fill="{colour}" d="{d}"{tr}/>')
        elif t == "symbol":
            paths, vb = symbol_paths(el["id"])
            bx, by, bw, bh = el["x"], el["y"], el["w"], el["h"]
            s = min(bw / vb[2], bh / vb[3])
            ox = bx + (bw - vb[2] * s) / 2 - vb[0] * s; oy = by + (bh - vb[3] * s) / 2 - vb[1] * s
            flip = (el.get("flip") or "")          # local: mirror the symbol within its own box
            tr = f"translate({fmt(ox)} {fmt(oy)}) scale({fmt(s)})"
            if "h" in flip: tr = f"translate({fmt(2 * bx + bw)} 0) scale(-1 1) " + tr
            if "v" in flip: tr = f"translate(0 {fmt(2 * by + bh)}) scale(1 -1) " + tr
            if el.get("rotate"): tr = f"rotate({fmt(el['rotate'])} {fmt(bx + bw / 2)} {fmt(by + bh / 2)}) " + tr
            if mirror and el.get("mirror", True): tr = f"translate({fmt(W)} 0) scale(-1 1) " + tr   # whole-layout (R) hand
            out.append(f'    <g transform="{tr}">')
            for d, f in paths:
                out.append(f'      <path fill="{colour if f in ("currentColor", None) else f}" d="{d}"/>')
            out.append('    </g>')
            flags.append(f"symbol:{el['id']}")
        elif t == "text":
            # runs: [{"text","series","height","tracking"}] share one baseline; plain text/words = one run each
            if el.get("runs"):
                runs = [dict(r) for r in el["runs"]]
            else:
                runs = [{"text": w} for w in el.get("words", [el.get("text")])]
            for r in runs:
                r["text"] = sub(r["text"]); r.setdefault("series", el.get("series", "D")); r.setdefault("height", el.get("height"))
                r.setdefault("tracking", el.get("tracking", "plus0"))
            gap = el.get("gap", 0)
            gaps = gap if isinstance(gap, list) else [gap] * max(0, len(runs) - 1)
            Hmax = max(r["height"] for r in runs); top = el["top"]; baseline = top + Hmax
            widths = []; inks = []
            for r in runs:
                fc = face(series_for(r, r["text"]), r["tracking"]); ink = fc.ink_width(r["text"], r["height"])
                inks.append(ink); widths.append(r["slot"] if r.get("slot") else ink)
            total = sum(widths) + sum(gaps)
            align = el.get("align", "center")
            if align == "center": x = (el.get("cx", W / 2)) - total / 2
            elif align == "left": x = el["x"]
            else: x = el["x"] - total
            if mirror and el.get("mirror", False): x = W - x - total
            d = []
            for i, (r, wd, ink) in enumerate(zip(runs, widths, inks)):
                fc = face(series_for(r, r["text"]), r["tracking"])
                d.append(fc.path(r["text"], r["height"], x + (wd - ink) / 2, baseline)); x += wd + (gaps[i] if i < len(gaps) else 0)
            rot = el.get("rotate")
            tr = f' transform="rotate({fmt(rot)} {fmt(x - total / 2 - (gaps[-1] if False else 0) + 0)} {fmt(top + Hmax / 2)})"' if rot else ""
            if rot:  # rotate about the line's centre: x is now past the last run, so centre = x_end - total/2
                x_end = x - (gaps[-1] if len(gaps) >= len(runs) else 0)
                tr = f' transform="rotate({fmt(rot)} {fmt(x_end - total / 2)} {fmt(top + Hmax / 2)})"'
            out.append(f'    <path fill="{colour}" d="{" ".join(d)}"{tr}/>')
            exp = el.get("expect")
            if exp is not None:
                exps = exp if isinstance(exp, list) else [exp]
                if len(exps) == 1 and len(runs) > 1 and el.get("expect_total", False): checks.append(("".join(r["text"] for r in runs), round(total, 1), exps[0]))
                else:
                    for r, wd, e in zip(runs, widths, exps):
                        if e is not None: checks.append((r["text"], round(wd, 1), e))
        else:
            raise ValueError(t)
    out.append('  </g>\n</g>\n</svg>')
    return "\n".join(out) + "\n", checks, flags

def folder_for(spec):
    """Output subfolder under Processed: the spec's own "folder" if set, else by sign family."""
    if spec.get("folder"): return spec["folder"]
    code = spec["code"].upper()
    fam = code.split("-")[0]
    if code.startswith(("TRA", "TRB")): return "Tourist Signs"
    if fam.startswith("GE"): return "Freeway Signs"
    if fam.startswith("GM"): return "Guide Signs"
    if fam == "G7": return "Service Signs"
    if fam == "G11": return "Tourist Signs"
    if fam.startswith("G"): return "Guide Signs"
    if fam == "R5": return "Parking Signs"
    if fam.startswith(("R", "RM")): return "Regulatory Signs"
    if fam.startswith(("W", "WM")): return "Warning Signs"
    if fam.startswith(("T", "TM")): return "Temporary Signs"
    if fam.startswith("D4"): return "Hazard Markers"
    return "Other"

def expand(spec):
    vary = spec.get("vary")
    valsets = [{vary["key"]: v} for v in vary["values"]] if vary else [{}]
    hands = spec.get("hands") or [None]
    for values in valsets:
        for hand in hands:
            v = dict(values); v.update(spec.get("hand_values", {}).get(hand, {}))
            code = spec["code"] + (f"({hand})" if hand else "")
            yield v, hand, f"{spec['name'].format(**v)}_{code}.svg"

def main(argv):
    specs = argv or sorted(glob.glob(os.path.join(ROOT, "tools", "specs", "**", "*.json"), recursive=True))
    rows = []; bad = 0; n = 0
    for sp in specs:
        with open(sp) as fh: spec = json.load(fh)
        if spec.get("skip"): 
            rows.append([spec["code"], "", "", spec.get("legend", ""), "SKIPPED: " + spec.get("skip"), "", ""]); continue
        if folder_for(spec) in EXCLUDE_FOLDERS:
            rows.append([spec["code"], "", "", spec.get("legend", ""), "EXCLUDED: " + folder_for(spec), "", ""]); continue
        for values, hand, fname in expand(spec):
            try:
                svg, checks, flags = build(spec, values, hand)
            except FileNotFoundError as e:
                rows.append([spec["code"], "", "", spec.get("legend", ""), f"BLOCKED: {e}", "symbol missing", ""]); continue
            status = []
            for w, got, exp in checks:
                if abs(got - exp) > max(3, 0.02 * exp): status.append(f"width {w}: {got} vs drawing {exp}"); bad += 1
            # signs needing a human decision go to intervene/<family>: QA-flagged specs, and width mismatches
            reason = spec.get("intervene") or ("; ".join(status) if status and WIDTH_MISMATCH_TO_INTERVENE else "")
            sub = os.path.join("intervene", folder_for(spec)) if reason else folder_for(spec)
            folder = os.path.join(OUT_ROOT, sub); os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, fname), "w") as fh: fh.write(svg)
            n += 1
            rows.append([spec["code"] + (f"({hand})" if hand else ""), os.path.relpath(os.path.join(folder, fname), OUT_ROOT),
                         f"{spec['size'][0]}x{spec['size'][1]}", spec.get("legend", "").format(**values),
                         "; ".join(status) or "ok", reason, " ".join(sorted(set(flags))) + ((" " + spec["notes"]) if spec.get("notes") else "")])
    os.makedirs(OUT_ROOT, exist_ok=True)
    with open(os.path.join(OUT_ROOT, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "file", "drawn_size_mm", "legend", "check", "intervene", "notes"]); w.writerows(rows)
    print(f"{n} files written; width mismatches: {bad}")
    for r in rows:
        if r[4] != "ok": print("  ", r[0], r[4])

if __name__ == "__main__":
    main(sys.argv[1:])
