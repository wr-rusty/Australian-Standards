"""qb.py — helpers for writing QLD specs from the sheet PDFs (scratch)."""
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
ROOT = "/Users/USER/Local/GitHub/Australian-Standards"
sys.path.insert(0, ROOT + "/tools")
import signgen as G
PNG = ROOT + "/Processing/Australia/QLD/Original PNGs/"
BASE = ("TMR Queensland design sheet (Q-series book / TC-series), colour drawing 'not to scale' with a lettered dimension table; "
        "every dimension from the sheet, AS 1744 (plus0) spacing. The sheets give no letter widths, so there is no width check. ")
R2 = 2 ** 0.5
def width(text, series, h): return G.face(series).ink_width(text, h)
def runs(drawing, panel_px, W, y0, y1, mingap=12, x0=None, x1=None, ink=None):
    """ink runs (mm, from the sign's left edge) on rows y0..y1 mm of the sign in the sheet PNG"""
    im = Image.open(PNG + drawing + ".png").convert("RGB"); k = (panel_px[2] - panel_px[0]) / W
    ink = ink or (lambda p: p[0] < 110 and p[1] < 110 and p[2] < 110)
    xa = int(panel_px[0] + (x0 if x0 is not None else 0.06 * W) * k); xb = int(panel_px[0] + (x1 if x1 is not None else 0.94 * W) * k)
    cols = [x for x in range(xa, xb) if any(ink(im.getpixel((x, y))) for y in range(int(panel_px[1] + y0 * k), int(panel_px[1] + y1 * k)))]
    if not cols: return []
    segs = []; st = pv = cols[0]
    for x in cols[1:]:
        if (x - pv) / k > mingap: segs.append((st, pv)); st = x
        pv = x
    segs.append((st, pv))
    return [(round((a - panel_px[0]) / k, 1), round((b + 1 - panel_px[0]) / k, 1)) for a, b in segs]
def rows(drawing, panel_px, W, x0, x1, y0, y1, mingap=6, ink=None):
    """ink row runs (mm from the sign's top) in the column band x0..x1 mm"""
    im = Image.open(PNG + drawing + ".png").convert("RGB"); k = (panel_px[2] - panel_px[0]) / W
    ink = ink or (lambda p: p[0] < 110 and p[1] < 110 and p[2] < 110)
    ys = [y for y in range(int(panel_px[1] + y0 * k), int(panel_px[1] + y1 * k)) if any(ink(im.getpixel((x, y))) for x in range(int(panel_px[0] + x0 * k), int(panel_px[0] + x1 * k)))]
    if not ys: return []
    segs = []; st = pv = ys[0]
    for y in ys[1:]:
        if (y - pv) / k > mingap: segs.append((st, pv)); st = y
        pv = y
    segs.append((st, pv))
    return [(round((a - panel_px[1]) / k, 1), round((b + 1 - panel_px[1]) / k, 1)) for a, b in segs]
def gaps(rr): return [round(rr[i + 1][0] - rr[i][1], 1) for i in range(len(rr) - 1)]
def sym(vcode, sid, groups):
    """write tools/symbols/<sid>.svg from the sheet's vector items; returns px bbox (x0, y0, x1, y1)"""
    out = subprocess.run([sys.executable, "-W", "ignore", os.path.dirname(os.path.abspath(__file__)) + "/vec.py", "sym", vcode, sid] + groups, capture_output=True, text=True)
    if "px bbox" not in out.stdout: raise SystemExit(out.stdout + out.stderr)
    b = out.stdout.split("[")[1].split("]")[0].split(); return tuple(float(v) for v in b)
def mm(pxbox, panel_px, W):
    k = W / (panel_px[2] - panel_px[0])
    return [round((pxbox[0] - panel_px[0]) * k, 1), round((pxbox[1] - panel_px[1]) * k, 1), round((pxbox[2] - pxbox[0]) * k, 1), round((pxbox[3] - pxbox[1]) * k, 1)]
def diamond_px(bbox, r, side):
    """sharp bounding square (panel_px) of a drawn rounded diamond whose bbox is `bbox` px"""
    D = side * R2; cut = r * (R2 - 1); k = (bbox[2] - bbox[0]) / (D - 2 * cut); e = cut * k
    return [round(bbox[0] - e, 1), round(bbox[1] - e, 1), round(bbox[2] + e, 1), round(bbox[3] + e, 1)]
def mk(code, name, legend, size, elements, notes, panel_px=None, drawing=None, base=True, **kw):
    s = {"code": code, "pack": "QLD"}
    if drawing and drawing != code: s["drawing"] = drawing
    s.update({"name": name, "legend": legend, "shape": kw.pop("shape", "rect"), "size": size})
    for k in ("radius", "ground", "edge", "border", "borders", "vary", "hands", "drawn_hand", "hand_values", "folder", "symbols", "intervene", "drawn_value", "which"):
        if k in kw and kw[k] is not None: s[k] = kw.pop(k)
    s.setdefault("ground", "yellow")
    if kw: raise SystemExit("unknown " + str(kw))
    if panel_px: s["panel_px"] = [round(v, 1) for v in panel_px]
    s["elements"] = elements; s["notes"] = (BASE if base else "") + notes
    with open(f"{ROOT}/tools/specs/QLD/{code}.json", "w") as fh: json.dump(s, fh, indent=1, ensure_ascii=False); fh.write("\n")
    return s
def skip(code, reason, legend=""):
    s = {"code": code, "pack": "QLD", "skip": reason}
    if legend: s["legend"] = legend
    with open(f"{ROOT}/tools/specs/QLD/{code}.json", "w") as fh: json.dump(s, fh, indent=1, ensure_ascii=False); fh.write("\n")
def T(text, series, h, top, **kw):
    e = {"type": "text", "text": text, "series": series, "height": h, "top": top}; e.update(kw); return e
def TW(words, series, h, top, gap, **kw):
    e = {"type": "text", "words": words, "series": series, "height": h, "top": top, "gap": gap}; e.update(kw); return e
def S(sid, x, y, w, h, **kw):
    e = {"type": "symbol", "id": sid, "x": round(x, 2), "y": round(y, 2), "w": round(w, 2), "h": round(h, 2), "colour": "black"}; e.update(kw); return e
YB = lambda e, b: {"edge": {"colour": "yellow", "width": e}, "border": {"colour": "black", "width": b}}
import vec as _vec, pymupdf as _mu
def page(vcode): return _vec.page_for(vcode)
def fills(vcode):
    p = page(vcode); M = p.rotation_matrix; out = []
    for i, d in enumerate(p.get_drawings()):
        if "f" not in d["type"]: continue
        r = d["rect"] * M; r.normalize(); K = _vec.K
        out.append((i, _vec.hexc(d.get("fill")), (r.x0 * K, r.y0 * K, r.x1 * K, r.y1 * K), len(d["items"])))
    return out
def title(vcode):
    p = page(vcode); K = _vec.K; out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            r = _mu.Rect(l["bbox"]) * p.rotation_matrix; r.normalize()
            t = " ".join(sp["text"].strip() for sp in l["spans"]).strip()
            if r.y0 * K > 1900 and r.x0 * K > 740 and t and "APPROVED" not in t and "ENGINEER" not in t and "Date" not in t and "Traffic Eng" not in t: out.append(t)
    return " / ".join(out)
def texts(vcode, ymax=1250):
    """live text lines (text, font, size px, bbox px) above ymax"""
    p = page(vcode); K = _vec.K; out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            r = _mu.Rect(l["bbox"]) * p.rotation_matrix; r.normalize()
            t = " ".join(sp["text"].strip() for sp in l["spans"]).strip()
            if t and r.y0 * K < ymax: out.append((t, l["spans"][0]["font"], l["spans"][0]["size"] * K, (r.x0 * K, r.y0 * K, r.x1 * K, r.y1 * K)))
    return out

def symentry(sid, src, desc, colours=("black",)): return {sid: {"source": src, "pack": "QLD", "desc": desc, "colours": list(colours), "vector": "extracted from the sheet PDF (not traced)"}}
def dia(cx, cy, side, e, b, r, ground="yellow", edgec="yellow", borderc="black"):
    out = []; h = side * R2 / 2
    for inset, col, rr in [(0, edgec, r), (e, borderc, r - e), (e + b, ground, r - e - b)]:
        d = h - inset * R2
        out.append({"type": "polygon", "points": [[round(cx, 2), round(cy - d, 2)], [round(cx + d, 2), round(cy, 2)], [round(cx, 2), round(cy + d, 2)], [round(cx - d, 2), round(cy, 2)]], "radius": max(rr, 0), "colour": col})
    return out
def find_diamond(vcode, which=0):
    """(outer yellow drawn-bbox px, [indices of fills]) of the which-th largest yellow diamond on the page"""
    fl = [f for f in fills(vcode) if f[1] in ("#f7d719", "#ffe200", "#fff200", "#ffdd00", "#fcd116", "#f8d800") or (f[1].startswith("#f") and f[1][3] in "cdef" and f[1][5] in "0123")]
    fl = [f for f in fl if abs((f[2][2] - f[2][0]) - (f[2][3] - f[2][1])) < 3 and f[2][2] - f[2][0] > 150]
    fl.sort(key=lambda f: -(f[2][2] - f[2][0]))
    return fl[which]
def inside_diamond(b, d, margin=0):
    cx, cy = (d[0] + d[2]) / 2, (d[1] + d[3]) / 2; h = (d[2] - d[0]) / 2 - margin
    if all(abs(x - cx) + abs(y - cy) <= h for x in (b[0], b[2]) for y in (b[1], b[3])): return True
    # a wide item (tracks across the sign): its edge mid-points inside and clearly smaller than the diamond
    mx, my = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return (b[2] - b[0]) < 0.93 * (d[2] - d[0]) and (b[3] - b[1]) < 0.93 * (d[3] - d[1]) and all(abs(x - cx) + abs(y - cy) <= h for x, y in ((b[0], my), (b[2], my), (mx, b[1]), (mx, b[3])))
def diamond_symbol_spec(code, vcode, drawing, side, e, b, r, name, legend, sid, desc, notes, colours=("#373435", "#201e1e", "#111211", "#1f1a17", "#242222", "#000000", "#2b2a29", "#231f20"), extra_els=None, **kw):
    D = side * R2; o = find_diamond(vcode); ppx = diamond_px(o[2], r, side)
    k = (ppx[2] - ppx[0]) / D; inner = (e + b) * R2 * k
    dark = lambda h: h != "-" and all(int(h[i:i + 2], 16) < 0x60 for i in (1, 3, 5))
    items = [f for f in fills(vcode) if dark(f[1]) and f[0] != o[0] and inside_diamond(f[2], ppx, inner - 1) and max(f[2][2] - f[2][0], f[2][3] - f[2][1]) > 3]
    bx = sym(vcode, sid, [",".join(str(f[0]) for f in items)]); m = mm(bx, ppx, D)
    c = D / 2
    note = (f" Symbol: the sheet PDF's own vector artwork (tools/symbols/{sid}.svg, items {items[0][0]}-{items[-1][0]}), placed as the sheet draws it: {m[2]} x {m[3]} with its box {round(c - m[0], 1)} left / {round(m[0] + m[2] - c, 1)} right of the vertical centreline and {round(c - m[1], 1)} above / {round(m[1] + m[3] - c, 1)} below the horizontal centreline.")
    s = mk(code, name, legend, [round(D, 2), round(D, 2)], [S(sid, *m)] + (extra_els or []), notes + note + " Black on retroreflective yellow.", panel_px=ppx, drawing=drawing, shape="diamond", radius=r,
           symbols=symentry(sid, drawing, desc), **YB(e, b), **kw)
    return m
BLACK = lambda p: p[0] < 110 and p[1] < 110 and p[2] < 110
WHITE = lambda p: p[0] > 200 and p[1] > 200 and p[2] > 200
GREEN = lambda p: p[1] > p[0] + 25 and p[1] > p[2] + 15 and p[0] < 120
def line(drawing, ppx, W, text, series, h, top, ink=None, x0=None, x1=None, colour=None, centre_tol=6, cx=None, mingap=None, align=None):
    """a legend line placed as the (to-scale) sheet draws it: extent measured on the PNG between the cap lines; word gaps as drawn
    (runs split at gaps > 0.42 h), AS 1744 letter spacing. _drawn = (left, right, gaps, drawn width / AS 1744 width of the words)"""
    words = text.split(" "); ink = ink or BLACK
    x0 = x0 if x0 is not None else 0.03 * W; x1 = x1 if x1 is not None else 0.97 * W
    rr = runs(drawing, ppx, W, top + 0.2 * h, top + 0.8 * h, mingap=3 * h, x0=x0, x1=x1, ink=ink)
    a, b = rr[0][0], rr[-1][1]; tot = sum(width(w, series, h) for w in words)
    kw = {}
    if colour: kw["colour"] = colour
    c = (a + b) / 2
    if align == "right": kw["align"] = "right"; kw["x"] = round(b, 1)
    elif align == "left": kw["align"] = "left"; kw["x"] = round(a, 1)
    elif cx is not None: kw["cx"] = cx
    elif abs(c - W / 2) > centre_tol: kw["cx"] = round(c, 1)
    if len(words) == 1:
        e = T(text, series, h, top, **kw); e["_drawn"] = (round(a), round(b), [], round((b - a) / tot, 3)); return e
    wr = runs(drawing, ppx, W, top + 0.05 * h, top + 0.95 * h, mingap=mingap or 0.42 * h, x0=x0, x1=x1, ink=ink)
    if len(wr) == len(words): g = [round(v) for v in gaps(wr)]; ratio = sum(q - p for p, q in wr) / tot
    else: g = [round(max(0.5 * h, (b - a - tot) / (len(words) - 1)))] * (len(words) - 1); ratio = 0
    e = TW(words, series, h, top, g if len(set(g)) > 1 else g[0], **kw); e["_drawn"] = (round(a), round(b), g, round(ratio, 3)); return e
def clean(els):
    info = []
    for e in els:
        if "_drawn" in e: info.append((e.get("text") or " ".join(e.get("words", [])), e.pop("_drawn")))
    return info
def page_notes(vcode):
    p = page(vcode); out = []
    for b in p.get_text("blocks"):
        if b[1] * _vec.K > 1100 and b[1] * _vec.K < 1900 and len(b[4]) > 30: out.append(b[4].replace("\n", " ").strip())
    return out
