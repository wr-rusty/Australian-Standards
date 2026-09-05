#!/usr/bin/env python3
"""
as1319.py — AS 1319-1994 safety signs from rule-based templates.

The standard gives no dimensioned drawing per sign; it gives sign forms, colours, and layouts in terms of
H (height of the largest letters) and D (symbol diameter / triangle side):
  D1  circle on a square board >= 1.2D; border 2.5-5 % of the shortest side, surround half the border
  D2  composite portrait: symbol at the top (0.1D margins), text below (0.5H gaps, H min lines)
  D3  text-only: H margins, 0.5H between lines
  D4  composite landscape: symbol left (0.2D margins, <= 1.6D), text right (H margins, 0.5H gaps)
  D5  symbol-only rectangle: 0.1D margins; text-only: 0.5H side margins
  C1  DANGER header: panel 11H x 3.3H, oval 8.5H x 2.2H, W = 0.1H, R = 15H max
  D6  DANGER layouts: horizontal (header left, text right, 0.5H margins) / landscape (header on top, text 0.75H below)
  3.1 arrows: style (a) B=0.64A C=0.08A D=0.23A E=0.30A R=0.045A; style (b) B=0.83A C=0.33A D=0.28A E=0.38A; L>=1.41A
Base-form proportions measured from the standard's own figures (t2.1_*): prohibition annulus 0.11D, slash 0.09D at 45
degrees, warning triangle border 0.08 of the side.  Text: PragmaticaCTT Bold (cap height 0.70 em), outlined.

Spec (tools/specs/AS1319/<NAME>.json):
  {"name":"NO_SMOKING","category":"prohibition","type":"symbol","symbol":"no_smoking","D":300}
  {"name":"HIGH_VOLTAGE_TEST_SITE","category":"danger","type":"text","size":[280,210],"lines":["HIGH VOLTAGE","TEST SITE"]}
  {"type":"composite","layout":"portrait","symbol":"no_pedestrians","lines":[...],"size":[w,h]}
  {"type":"multi","symbols":["head_protection","hearing_protection","no_open_flame"],"D":150}
  "arrow": "up|down|left|right" adds a 3.1 style (b) arrow; "H" fixes the letter height (else the largest that fits).
Output: AS 1319-1994/SVGs/<Category>/<NAME>.svg in the same header format as the AS 1743 set.
"""
import glob, json, math, os, sys, xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "Fonts", "PragmaticaCTT-Bold", "PRG75.TTF")
SYM = os.path.join(ROOT, "tools", "symbols", "as1319")
OUT = os.path.join(ROOT, "Australia", "National (AS 1319)", "SVGs")
TEMPLATE_DANGER = os.path.join(ROOT, "Design Templates", "DANGER_TEMPLATE.svg")
CAP = 0.70   # Pragmatica Bold cap height / em
OUT_SCALE = 0.1
COL = {"red": "#e22726", "blue": "#3a53a4", "green": "#0b804c", "yellow": "#f7b500", "black": "#000", "white": "#fff"}
CATEGORY = {"prohibition": "Prohibition", "restriction": "Restriction", "mandatory": "Mandatory", "warning": "Warning",
            "danger": "Danger", "emergency": "Safety & Emergency", "fire": "Fire"}
ANNULUS, SLASH, TRI_BORDER, TRI_R = 0.11, 0.09, 0.08, 0.06   # measured on t2.1_1 / t2.1_4 (TRI_R estimated)

def fmt(v):
    if isinstance(v, float): return f"{v:.2f}".rstrip("0").rstrip(".") or "0"
    return str(v)

# ------------------------------------------------------------------ text
_font = None
def font():
    global _font
    if _font is None:
        t = TTFont(FONT); _font = (t.getGlyphSet(), t.getBestCmap(), t["head"].unitsPerEm)
    return _font
def text_width(s, H):
    gs, cmap, upm = font(); k = H / (CAP * upm)
    names = [cmap.get(ord(c), cmap[ord(" ")]) for c in s]
    if not names: return 0
    adv = sum(gs[n].width for n in names)
    b0 = BoundsPen(gs); gs[names[0]].draw(b0); b1 = BoundsPen(gs); gs[names[-1]].draw(b1)
    l = b0.bounds[0] if b0.bounds else 0; r = (gs[names[-1]].width - b1.bounds[2]) if b1.bounds else 0
    return (adv - l - r) * k
def text_path(s, H, cx, baseline, colour):
    gs, cmap, upm = font(); k = H / (CAP * upm)
    names = [cmap.get(ord(c), cmap[ord(" ")]) for c in s]
    b0 = BoundsPen(gs); gs[names[0]].draw(b0); l = b0.bounds[0] if b0.bounds else 0
    w = text_width(s, H); x = cx - w / 2 - l * k; d = []
    for n in names:
        pen = SVGPathPen(gs, ntos=fmt); gs[n].draw(TransformPen(pen, (k, 0, 0, -k, x, baseline))); d.append(pen.getCommands()); x += gs[n].width * k
    return f'<path fill="{colour}" d="{" ".join(d)}"/>'

# ------------------------------------------------------------------ primitives
def rrect(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{fmt(r)}" ry="{fmt(r)}" fill="{fill}"{extra}/>'
def board(w, h, ground="white", border=True):
    """Sign board per D1: white ground with a black border 3 % of the shortest side, surround half that. Corners 5 %."""
    s = min(w, h); b = 0.03 * s; sur = b / 2; r = 0.05 * s
    out = [rrect(0, 0, w, h, r, COL["white"] if ground == "white" else COL[ground])]
    if border: out.append(rrect(sur, sur, w - 2 * sur, h - 2 * sur, r - sur, "none", f' stroke="{COL["black"]}" stroke-width="{fmt(b)}"'))
    return out, sur + b
def symbol_svg(sid):
    tree = ET.parse(os.path.join(SYM, sid + ".svg"))
    return [(e.get("d"), e.get("fill", "currentColor")) for e in tree.getroot().iter() if e.tag.endswith("path")]
def place_symbol(sid, x, y, D, colour):
    k = D / 1000.0
    return "".join(f'<path fill="{colour if f == "currentColor" else f}" fill-rule="evenodd" transform="translate({fmt(x)} {fmt(y)}) scale({fmt(k)})" d="{d}"/>' for d, f in symbol_svg(sid))
def form(category, x, y, D, symbol=None):
    """The sign form of diameter/side D with its symbol, top-left at (x, y)."""
    cx, cy = x + D / 2, y + D / 2; out = []
    if category in ("prohibition", "restriction"):
        out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(D / 2)}" fill="{COL["white"]}"/>')
        if symbol: out.append(place_symbol(symbol, x, y, D, COL["black"]))
        out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(D / 2 - ANNULUS * D / 2)}" fill="none" stroke="{COL["red"]}" stroke-width="{fmt(ANNULUS * D)}"/>')
        if category == "prohibition":
            L = D / 2 - ANNULUS * D / 2; t = SLASH * D / 2
            out.append(f'<path fill="{COL["red"]}" transform="rotate(45 {fmt(cx)} {fmt(cy)})" d="M{fmt(cx - L)} {fmt(cy - t)}h{fmt(2 * L)}v{fmt(2 * t)}h{fmt(-2 * L)}Z"/>')
    elif category == "mandatory":
        out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(D / 2)}" fill="{COL["blue"]}"/>')
        if symbol: out.append(place_symbol(symbol, x, y, D, COL["white"]))
    elif category == "warning":
        h = D * math.sqrt(3) / 2; top = y + (D - h) / 2   # centred in the D square
        pts = [(cx, top), (x + D, top + h), (x, top + h)]
        out.append(f'<path fill="{COL["black"]}" d="{rounded_tri(pts, TRI_R * D)}"/>')
        bw = TRI_BORDER * D; ins = bw * math.sqrt(3)   # inset of an equilateral triangle by bw
        pts2 = [(cx, top + 2 * ins), (x + D - ins * math.sqrt(3), top + h - ins), (x + ins * math.sqrt(3), top + h - ins)]
        out.append(f'<path fill="{COL["yellow"]}" d="{rounded_tri(pts2, max(0, TRI_R * D - bw))}"/>')
        if symbol: out.append(place_symbol(symbol, x, y, D, COL["black"]))
    elif category in ("emergency", "fire"):
        out.append(rrect(x, y, D, D, 0.05 * D, COL["green"] if category == "emergency" else COL["red"]))
        if symbol: out.append(place_symbol(symbol, x, y, D, COL["white"]))
    return "".join(out)
def rounded_tri(pts, r):
    n = 3; d = ""; segs = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1]); l1 = math.hypot(*v1); l2 = math.hypot(*v2)
        u1 = (v1[0] / l1, v1[1] / l1); u2 = (v2[0] / l2, v2[1] / l2); th = math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])))
        t = r / math.tan(th / 2) if r > 0 else 0; a = (p1[0] + u1[0] * t, p1[1] + u1[1] * t); b = (p1[0] + u2[0] * t, p1[1] + u2[1] * t)
        segs.append((a, b, 0 if (u1[0] * u2[1] - u1[1] * u2[0]) > 0 else 1))
    d = f"M{fmt(segs[0][0][0])} {fmt(segs[0][0][1])}"
    for i in range(n):
        a, b, sw = segs[i]
        if r > 0: d += f"A{fmt(r)} {fmt(r)} 0 0 {sw} {fmt(b[0])} {fmt(b[1])}"
        na = segs[(i + 1) % n][0]; d += f"L{fmt(na[0])} {fmt(na[1])}"
    return d + "Z"
def arrow_b(A, L, cx, cy, direction, colour):
    """Figure 3.1 style (b): head width A, head length B=0.83A, barb depth C=0.33A, shaft D=0.28A, notch E=0.38A."""
    B, C, Dw, E = 0.83 * A, 0.33 * A, 0.28 * A, 0.38 * A
    pts = [(L, 0), (L - B, -A / 2), (L - B + C, -A / 2), (L - B + E, -Dw / 2), (0, -Dw / 2), (0, Dw / 2), (L - B + E, Dw / 2), (L - B + C, A / 2), (L - B, A / 2)]
    ang = {"right": 0, "down": 90, "left": 180, "up": -90}[direction]
    d = "M" + "L".join(f"{fmt(px - L / 2)} {fmt(py)}" for px, py in pts) + "Z"
    return f'<path fill="{colour}" transform="translate({fmt(cx)} {fmt(cy)}) rotate({ang})" d="{d}"/>'
_danger = None
def danger_header(x, y, H):
    """C1 header at letter height H: panel 11H x 3.3H black, oval 8.5H x 2.2H red with a W=0.1H white outline,
    DANGER lettering from the Design Templates DANGER_TEMPLATE scaled to H (cap height)."""
    global _danger
    if _danger is None:
        root = ET.parse(TEMPLATE_DANGER).getroot(); ns = "{http://www.w3.org/2000/svg}"
        paths = [p.get("d") for p in root.iter(ns + "path")]
        _danger = paths[-1]   # the lettering (last path in the template); its cap height in template units:
    PW, PH, OW, OH, W = 11 * H, 3.3 * H, 8.5 * H, 2.2 * H, 0.1 * H
    cx, cy = x + PW / 2, y + PH / 2
    out = [rrect(x, y, PW, PH, 0, COL["black"]),
           f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(OW / 2)}" ry="{fmt(OH / 2)}" fill="{COL["red"]}" stroke="{COL["white"]}" stroke-width="{fmt(W)}"/>']
    # lettering: template cap height ~71.19 units (from y 100.83 to 172.02), width 172..682 -> scale to H
    k = H / 71.19; lw = (682.35 - 171.75) * k
    out.append(f'<path fill="{COL["white"]}" transform="translate({fmt(cx - lw / 2 - 171.75 * k)} {fmt(cy - H / 2 - 100.83 * k)}) scale({fmt(k)})" d="{_danger}"/>')
    return "".join(out), PW, PH

# ------------------------------------------------------------------ layouts
def fit_H(lines, width, height, side_margin_H=0.5, top_margin_H=1.0, gap_H=0.5, bottom_margin_H=1.0, Hmax=None):
    """Largest H such that the lines fit the box per D3 (margins and gaps in units of H)."""
    n = len(lines); Hh = height / (top_margin_H + bottom_margin_H + n + gap_H * (n - 1))
    for _ in range(3):
        wmax = max(text_width(s, Hh) for s in lines) if lines else 0
        Hw = Hh * (width - 2 * side_margin_H * Hh) / wmax if wmax else Hh
        Hh = min(Hh, Hw)
    return min(Hh, Hmax) if Hmax else Hh
def text_block(lines, H, x0, y0, width, colour, gap_H=0.5, align="center"):
    out = []; y = y0
    for s in lines:
        cx = x0 + width / 2
        out.append(text_path(s, H, cx, y + H, colour)); y += H + gap_H * H
    return "".join(out), y - gap_H * H

def build(spec):
    cat = spec["category"]; typ = spec["type"]; out = []
    dark_text = cat in ("prohibition", "restriction", "mandatory", "warning", "danger")
    tcol = COL["black"] if dark_text else COL["white"]
    if typ == "symbol":
        D = spec.get("D", 300); W = H = spec.get("board", round(1.2 * D))   # D1: board >= 1.2D
        if cat in ("emergency", "fire"): W = H = D   # the square is the sign (D5 margins live inside the colour)
        if cat in ("emergency", "fire"): out.append(form(cat, 0, 0, D, spec["symbol"]))
        else:
            b, inset = board(W, H); out += b; out.append(form(cat, (W - D) / 2, (H - D) / 2, D, spec["symbol"]))
    elif typ == "multi":
        D = spec.get("D", 150); syms = spec["symbols"]; n = len(syms); g = 0.15 * D; m = 0.15 * D
        if spec.get("layout") == "triangle" and n == 3:
            W = 2 * D + g + 2 * m; H = 2 * D + g + 2 * m; b, inset = board(W, H); out += b
            pos = [(m, m), (m + D + g, m), (m + (D + g) / 2, m + D + g)]
        else:
            W = n * D + (n - 1) * g + 2 * m; H = D + 2 * m; b, inset = board(W, H); out += b
            pos = [(m + i * (D + g), m) for i in range(n)]
        for s, (px, py) in zip(syms, pos): out.append(form(spec.get("cats", [cat] * n)[syms.index(s)] if spec.get("cats") else cat, px, py, D, s))
    elif typ == "text":
        W, H_ = spec["size"]; lines = spec["lines"]
        if cat == "danger":
            b, inset = board(W, H_); out += b
            layout = spec.get("layout", "horizontal" if W > 2.2 * H_ else "landscape")
            if layout == "horizontal":   # D6: header left, text right, 0.5H margins
                Hl = spec.get("H") or fit_H(lines, W - 11 * (H_ - 2 * inset) / 3.3 - 0, H_ - 2 * inset, 0.5, 1.0, 0.5, 1.0)
                hh = H_ - 2 * inset; Hd = hh / 3.3; hdr, PW, PH = danger_header(inset, inset, Hd); out.append(hdr)
                tx = inset + PW; tw = W - inset - tx
                Hl = spec.get("H") or fit_H(lines, tw, hh, 0.5, 1.0, 0.5, 1.0)
                n = len(lines); th = n * Hl + (n - 1) * 0.5 * Hl; blk, _ = text_block(lines, Hl, tx, inset + (hh - th) / 2, tw, tcol); out.append(blk)
            else:                          # header across the top, text below (0.75H below the header, H margins)
                Hd = (W - 2 * inset) / 11; hdr, PW, PH = danger_header(inset, inset, Hd); out.append(hdr)
                ty = inset + PH; th_avail = H_ - inset - ty
                Hl = spec.get("H") or fit_H(lines, W - 2 * inset, th_avail, 1.0, 0.75, 0.5, 1.0)
                blk, _ = text_block(lines, Hl, inset, ty + 0.75 * Hl, W - 2 * inset, tcol); out.append(blk)
        else:
            ground = {"warning": "yellow", "emergency": "green", "fire": "red"}.get(cat, "white")
            b, inset = board(W, H_, ground, border=(cat in ("mandatory", "prohibition", "restriction")))
            if ground != "white": inset = 0.03 * min(W, H_)
            out += b
            arrow = spec.get("arrow"); lx, lw = inset, W - 2 * inset
            if cat in ("prohibition", "restriction", "warning") and spec.get("emblem", True):   # fig 2.5: form at the left, text right (D4)
                D = min(1.6 * (H_ - 2 * inset) / 1.6, (H_ - 2 * inset) / 1.4); D = spec.get("D", D)
                out.append(form(cat, inset + 0.2 * D, (H_ - D) / 2, D, None)); lx = inset + 0.2 * D + D + 0.2 * D; lw = W - inset - lx
            avail_h = H_ - 2 * inset - (0 if not arrow else 0.0)
            Hl = spec.get("H") or fit_H(lines, lw, avail_h, 0.5, 1.0, 0.5, 1.0 + (2.0 if arrow else 0))
            n = len(lines); th = n * Hl + (n - 1) * 0.5 * Hl
            top = inset + (avail_h - th - (2.0 * Hl if arrow else 0)) / 2 if not arrow else inset + Hl
            blk, yend = text_block(lines, Hl, lx, top, lw, tcol); out.append(blk)
            if arrow:
                A = 1.6 * Hl; out.append(arrow_b(A, 1.41 * A * 1.2, lx + lw / 2, yend + 0.5 * Hl + 0.9 * A / 2 + A * 0.2, arrow, tcol))
    elif typ == "composite":
        W, H_ = spec["size"]; lines = spec["lines"]; sym = spec.get("symbol")
        b, inset = board(W, H_); out += b
        if spec.get("layout", "portrait") == "portrait":   # D2
            D = spec.get("D", (W - 2 * inset) / 1.2); sx = (W - D) / 2; sy = inset + 0.1 * D
            out.append(form(cat if cat != "danger" else "prohibition", sx, sy, D, sym))
            ty = sy + D + 0.5 * (spec.get("H") or 1)  # placeholder, recomputed below
            avail = H_ - inset - (sy + D)
            Hl = spec.get("H") or fit_H(lines, W - 2 * inset, avail, 0.5, 0.5, 0.5, 1.0)
            blk, _ = text_block(lines, Hl, inset, sy + D + 0.5 * Hl, W - 2 * inset, tcol); out.append(blk)
        else:                                                # D4
            D = spec.get("D", min((H_ - 2 * inset) / 1.4, (H_ - 2 * inset) - 0.4 * ((H_ - 2 * inset) / 1.4)))
            sx = inset + 0.2 * D; sy = (H_ - D) / 2; out.append(form(cat, sx, sy, D, sym))
            lx = sx + D + 0.2 * D; lw = W - inset - lx
            Hl = spec.get("H") or fit_H(lines, lw, H_ - 2 * inset, 0.5, 1.0, 0.5, 1.0)
            n = len(lines); th = n * Hl + (n - 1) * 0.5 * Hl
            blk, _ = text_block(lines, Hl, lx, (H_ - th) / 2, lw, tcol); out.append(blk)
    else: raise ValueError(typ)
    OW, OH = W * OUT_SCALE, H_ * OUT_SCALE if typ in ("text", "composite") else H * OUT_SCALE
    svg = [f'<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{fmt(OW * 25.4 / 72)}mm" height="{fmt(OH * 25.4 / 72)}mm" viewBox="0 0 {fmt(OW)} {fmt(OH)}">',
           f'<g transform="scale({fmt(OUT_SCALE)})">'] + out + ['</g>', '</svg>']
    return "\n".join(svg) + "\n"

def main(argv):
    specs = argv or sorted(glob.glob(os.path.join(ROOT, "tools", "specs", "AS1319", "*.json")))
    n = 0
    for sp in specs:
        spec = json.load(open(sp)); folder = os.path.join(OUT, CATEGORY[spec["category"]]); os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, spec["name"] + ".svg"), "w") as fh: fh.write(build(spec))
        n += 1
    print(f"{n} AS 1319 signs written to {OUT}")
if __name__ == "__main__": main(sys.argv[1:])
