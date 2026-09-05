#!/usr/bin/env python3
"""sheet_extract.py — lift sign artwork from CAD-style sign design sheets (state registers: NSW design plans, QLD TC
signs and Q-series, and similar PDFs): a title block, notes, colour legend and dimension lines around one or more drawn
signs, legends set in embedded fonts, sometimes outlines drawn as strokes and shapes exported as triangles.

Method per page:
  1. the original PDF gives the text (fonts, positions): where the title block and notes are, which figures are
     dimensions, the sheet's stated size / scale, and (for the drivers) the sign code and name;
  2. Inkscape re-exports the page with every glyph converted to a path (`--pdf-font-strategy=draw-all`), so legends
     in any embedded font come through as exact fills;
  3. fills that sit under annotation text (dimension figures, notes) are dropped; closed stroke outlines in the drawing
     area become white panels (line-drawn sheets); nearby fills are clustered into drawings; each drawing keeps what
     lies inside its outline (dimension arrowheads, leader masks and specks dropped; triangulated exports are unioned);
  4. the drawing is scaled to real size from a "W x H" figure, an overall width/height dimension, or a stated scale.
Content drawn sideways on the sheet is rotated upright first. Used by qld_extract.py and nsw_extract.py."""
import os, re, sys, math, subprocess, tempfile, hashlib
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X

MM_PER_PT = 25.4 / 72
SIGN_FONT = re.compile(r"AS1744|FHWA|Series[A-F]|Highway|Transport|Motorway", re.I)
TITLE_WORDS = ("APPROVED AS OFFICIAL", "COLOUR LEGEND", "COLOR LEGEND", "DESIGNED", "CHECKED", "PREPARED BY", "SHEET ", "SHEET No", "DRAWING FILE",
               "AMENDMENT", "REVISION", "MATERIALS:", "SIGN TO BE MANUFACTURED", "SCALE:", "NOTES", "Notes", "Department of Transport", "Transport for NSW",
               "Specification", "Legend", "Font Type", "Font Size", "Date")
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
CACHE = os.environ.get("SHEET_CACHE", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".sheet_cache"))

def fmt(v): return X.fmt(v)

def paths_pdf(pdf):
    """The sheet with every glyph converted to a path (cached)."""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5((os.path.abspath(pdf) + str(os.path.getmtime(pdf))).encode()).hexdigest()[:12]
    out = os.path.join(CACHE, f"{os.path.basename(pdf)[:-4]}_{key}.pdf")
    if not os.path.exists(out):
        r = subprocess.run([INK, "--pdf-font-strategy=draw-all", "--export-type=pdf", f"--export-filename={out}", pdf], capture_output=True, text=True, timeout=300)
        if not os.path.exists(out): raise RuntimeError("inkscape could not convert the sheet: " + r.stderr.strip()[-200:])
    return out

class Frame:
    """Coordinate transform: page space -> upright rendered space (page rotation plus sideways content)."""
    def __init__(self, page, spans_raw):
        M = page.rotation_matrix
        def rot(d): v = pymupdf.Point(d) * pymupdf.Matrix(M.a, M.b, M.c, M.d, 0, 0); return (v.x, v.y)   # page rotation applied to text directions
        legend = [s for s in spans_raw if SIGN_FONT.search(s["font"]) and len(s["text"]) > 1]
        dirs = [rot(s["dir"]) for s in (legend or [s for s in spans_raw if len(s["text"]) > 2])]
        vert = sum(1 for d in dirs if abs(d[1]) > abs(d[0])); horiz = len(dirs) - vert
        extra = 0
        if not dirs and page.rect.width < page.rect.height:   # text all outlined (old CAD exports): NSW draws landscape sheets on portrait pages, turned anticlockwise
            extra = -90
        if vert > horiz and dirs:
            up = sum(1 for d in dirs if abs(d[1]) > abs(d[0]) and d[1] < 0)
            extra = 90 if up >= vert / 2 else -90       # text running up the page reads upright after a +90 turn
        R = M * pymupdf.Matrix(extra)
        base = (page.rect * page.derotation_matrix).normalize()      # text and drawing coordinates are in the unrotated page space
        pr = (base * R).normalize()
        self.M = R * pymupdf.Matrix(1, 0, 0, 1, -pr.x0, -pr.y0)
        self.rect = (base * self.M).normalize()
        self.turned = extra
    @classmethod
    def baked(cls, page, like):
        self = cls.__new__(cls); R = pymupdf.Matrix(like.turned); pr = (page.rect * R).normalize()
        self.M = R * pymupdf.Matrix(1, 0, 0, 1, -pr.x0, -pr.y0); self.rect = (page.rect * self.M).normalize(); self.turned = like.turned
        return self
    def P(self, p): q = pymupdf.Point(p[0], p[1]) * self.M; return (q.x, q.y)
    def R(self, r): return (pymupdf.Rect(r) * self.M).normalize()

def raw_spans(page):
    raw = page.get_text("rawdict"); out = []
    for bi, b in enumerate(raw["blocks"]):
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                txt = "".join(c["c"] for c in sp["chars"]).strip()
                if txt: out.append({"text": txt, "font": sp["font"].split("+")[-1], "size": sp["size"], "bbox": pymupdf.Rect(sp["bbox"]), "origin": sp["origin"], "dir": l.get("dir", (1, 0)), "color": sp.get("color"), "block": bi, "block_bbox": pymupdf.Rect(b["bbox"])})
    return out

def page_fills(page, F):
    out = []
    for f in X.fills_on_page(page):
        items = []
        for it in f["items"]:
            k = it[0]
            if k == "l": items.append(("l", F.P(it[1]), F.P(it[2])))
            elif k == "c": items.append(("c", F.P(it[1]), F.P(it[2]), F.P(it[3]), F.P(it[4])))
            elif k in ("re", "qu"):
                if k == "re": r = it[1]; pts = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
                else: q = it[1]; pts = [q.ul, q.ur, q.lr, q.ll]
                pts = [F.P(p) for p in pts]; items += [("l", pts[i], pts[(i + 1) % 4]) for i in range(4)]
        r = F.R(f["rect"]); out.append({"rect": r, "fill": f["fill"], "items": items, "area": r.get_area(), "even_odd": f.get("even_odd")})
    return out

def closed_strokes(page, F):
    """Closed stroke paths (sign outlines on line-drawn sheets) as white virtual fills; thick strokes (drawn borders,
    bars) as filled bands in the stroke's colour."""
    out = []
    for d in page.get_drawings():
        if d.get("fill") is not None or d.get("width", 0) <= 0: continue
        items = d["items"]
        if not items or d["rect"].width < 10 or d["rect"].height < 10: continue
        pts = X.item_points(items)
        closed = items[0][0] == "re" or d.get("closePath") or (len(pts) >= 3 and math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 0.5)
        if d.get("width", 0) >= 2 and d.get("color") is not None:
            band = stroke_band(items, d["width"], closed)
            if band:
                f = {"rect": d["rect"] + (-d["width"], -d["width"], d["width"], d["width"]), "fill": tuple(d["color"]), "items": band, "area": d["rect"].get_area(), "even_odd": True}
                conv = page_fills_from([f], F)
                for c in conv: c["virtual"] = False; c["band"] = True
                out += conv
        if closed:
            f = {"rect": d["rect"], "fill": (1.0, 1.0, 1.0), "items": items, "area": d["rect"].get_area(), "even_odd": False}
            out += page_fills_from([f], F)
    return out

def stroke_band(items, width, closed):
    """Outline of a stroked path as a polygon (with hole for closed paths), via Shapely buffering."""
    from shapely.geometry import LineString, LinearRing, Polygon
    pts = []
    for it in items:
        if it[0] == "re":
            r = it[1]; pts += [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)]
        elif it[0] == "l": pts += [tuple(it[1]), tuple(it[2])]
        elif it[0] == "c": pts += [tuple(it[1]), tuple(it[4])]
        elif it[0] == "qu": q = it[1]; pts += [tuple(q.ul), tuple(q.ur), tuple(q.lr), tuple(q.ll), tuple(q.ul)]
    pts = [(float(x), float(y)) for x, y in pts]
    if len(pts) < 2: return None
    try:
        line = LineString(pts); poly = line.buffer(width / 2, join_style=2, cap_style=2)
    except Exception: return None
    geoms = list(poly.geoms) if hasattr(poly, "geoms") else [poly]
    out = []
    for gm in geoms:
        for ring in [gm.exterior] + list(gm.interiors):
            cs = list(ring.coords)
            for i in range(len(cs) - 1): out.append(("l", (cs[i][0], cs[i][1]), (cs[i + 1][0], cs[i + 1][1])))
    return out

def page_fills_from(fills, F):
    class _P: pass
    tmp = []
    for f in fills:
        items = []
        for it in f["items"]:
            k = it[0]
            if k == "l": items.append(("l", F.P(it[1]), F.P(it[2])))
            elif k == "c": items.append(("c", F.P(it[1]), F.P(it[2]), F.P(it[3]), F.P(it[4])))
            elif k in ("re", "qu"):
                if k == "re": r = it[1]; pts = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
                else: q = it[1]; pts = [q.ul, q.ur, q.lr, q.ll]
                pts = [F.P(p) for p in pts]; items += [("l", pts[i], pts[(i + 1) % 4]) for i in range(4)]
        r = F.R(f["rect"]); tmp.append({"rect": r, "fill": f["fill"], "items": items, "area": r.get_area(), "even_odd": f.get("even_odd"), "virtual": True})
    return tmp

def drawing_region(F, spans):
    """The sheet minus its title block: the block is the strip (bottom, top, left or right) holding the title words."""
    W, H = F.rect.width, F.rect.height
    tw = [s["bbox"] for s in spans if any(w.lower() in s["text"].lower() for w in TITLE_WORDS)]
    if not tw: return pymupdf.Rect(0, 0, W, 0.8 * H)
    tb = tw[0]
    for b in tw[1:]: tb |= b
    cx, cy = (tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2
    if tb.width >= tb.height or tb.height < 0.5 * H:          # a band across the sheet
        return pymupdf.Rect(0, 0, W, tb.y0 - 4) if cy > H / 2 else pymupdf.Rect(0, tb.y1 + 4, W, H)
    return pymupdf.Rect(0, 0, tb.x0 - 4, H) if cx > W / 2 else pymupdf.Rect(tb.x1 + 4, 0, W, H)   # a strip down one side

def is_number(t): return re.fullmatch(r"[\d.,]+\*?\s*(?:mm)?|R\s*\d+|\d+\s*[x×]\s*\d+|\d+\s*[A-Za-z]{1,3}\*?|[A-Za-z]{1,2}|\(\d+\)|[a-z]\d?", t.strip()) is not None

def clusters(fills, margin):
    parent = list(range(len(fills)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(fills)):
        ri = fills[i]["rect"] + (-margin, -margin, margin, margin)
        for j in range(i + 1, len(fills)):
            if ri.intersects(fills[j]["rect"]): parent[find(i)] = find(j)
    g = {}
    for i in range(len(fills)): g.setdefault(find(i), []).append(fills[i])
    return list(g.values())

def bbox_of(fs): return pymupdf.Rect(min(f["rect"].x0 for f in fs), min(f["rect"].y0 for f in fs), max(f["rect"].x1 for f in fs), max(f["rect"].y1 for f in fs))

def svg_path_items(d, dx, dy):
    toks = re.findall(r"[MLHVCZmlhvcz]|-?\d*\.?\d+(?:e-?\d+)?", d); items = []; i = 0; cur = None; start = None; cmd = None
    def num():
        nonlocal i; v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]): cmd = toks[i]; i += 1
        if cmd in ("M", "m"):
            x, y = num(), num()
            if cmd == "m" and cur: x += cur[0] - dx; y += cur[1] - dy
            cur = start = (x + dx, y + dy); cmd = "L" if cmd == "M" else "l"
        elif cmd in ("L", "l"):
            x, y = num(), num(); q = (x + dx, y + dy) if cmd == "L" else (cur[0] + x, cur[1] + y); items.append(("l", cur, q)); cur = q
        elif cmd in ("H", "h"):
            x = num(); q = (x + dx, cur[1]) if cmd == "H" else (cur[0] + x, cur[1]); items.append(("l", cur, q)); cur = q
        elif cmd in ("V", "v"):
            y = num(); q = (cur[0], y + dy) if cmd == "V" else (cur[0], cur[1] + y); items.append(("l", cur, q)); cur = q
        elif cmd in ("C", "c"):
            pts = [(num(), num()) for _ in range(3)]
            pts = [(x + dx, y + dy) for x, y in pts] if cmd == "C" else [(cur[0] + x, cur[1] + y) for x, y in pts]
            items.append(("c", cur, pts[0], pts[1], pts[2])); cur = pts[2]
        elif cmd in ("Z", "z"):
            if cur and start and cur != start: items.append(("l", cur, start))
            cur = start
        else: i += 1
    return items

def union_by_colour(fills, box):
    """Triangulated CAD exports: union the pieces of each colour so the shapes are clean paths. Polygonal pieces are
    unioned with Shapely (a hair of outset closes the seams between triangles); pieces with curves go through Inkscape."""
    groups = {}
    for f in fills: groups.setdefault((f["fill"], bool(f.get("virtual"))), []).append(f)
    out = []
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    for key, fs in groups.items():
        polys = [f for f in fs if all(it[0] == "l" for it in f["items"]) and len(f["items"]) >= 3]
        if len(polys) < 6: out += fs; continue
        out += [f for f in fs if f not in polys]
        shapes = []
        for f in polys:
            pts = [f["items"][0][1]] + [it[2] for it in f["items"]]
            try:
                pg = Polygon(pts)
                if not pg.is_valid: pg = pg.buffer(0)
                if pg.area > 0: shapes.append(pg)
            except Exception: pass
        if not shapes: continue
        total = sum(sh.area for sh in shapes); big = total > 0.15 * box.get_area()
        eps = max(0.15, (0.004 if big else 0.0012) * max(box.width, box.height))          # closes the seams between CAD triangles
        u = unary_union(shapes).buffer(eps, join_style=2).buffer(-eps, join_style=2)
        geoms = list(u.geoms) if hasattr(u, "geoms") else [u]
        for gm in geoms:
            if gm.is_empty or gm.area < 0.5: continue
            holes = [h for h in gm.interiors if Polygon(h).area > 0.001 * gm.area]   # sliver holes are seams, not counters
            rings = [gm.exterior] + holes; items = []
            for ring in rings:
                cs = list(ring.coords)
                for i in range(len(cs) - 1): items.append(("l", (cs[i][0], cs[i][1]), (cs[i + 1][0], cs[i + 1][1])))
            xs = [p[0] for it in items for p in it[1:]]; ys = [p[1] for it in items for p in it[1:]]
            out.append({"rect": pymupdf.Rect(min(xs), min(ys), max(xs), max(ys)), "fill": key[0], "items": items, "area": (max(xs) - min(xs)) * (max(ys) - min(ys)), "even_odd": True, "virtual": key[1]})
    return out

def _union_inkscape(fills, box):
    groups = {}
    for f in fills: groups.setdefault((f["fill"], bool(f.get("virtual"))), []).append(f)
    out = []
    with tempfile.TemporaryDirectory() as td:
        for gi, (key, fs) in enumerate(groups.items()):
            if len(fs) < 6: out += fs; continue
            def T(p): return (p[0] - box.x0, p[1] - box.y0)
            body = "".join(f'<path id="p{i}" fill="#000" d="{X.path_d(f["items"], T)}"/>' for i, f in enumerate(fs))
            rawp = os.path.join(td, f"g{gi}.svg"); outp = os.path.join(td, f"g{gi}o.svg")
            open(rawp, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{box.width}" height="{box.height}" viewBox="0 0 {box.width} {box.height}">{body}</svg>')
            subprocess.run([INK, rawp, "--actions", "select-all;path-union;export-plain-svg;export-filename:" + outp + ";export-do"], capture_output=True, text=True, timeout=300)
            ds = re.findall(r'\sd="([^"]+)"', open(outp).read()) if os.path.exists(outp) else []
            for d in ds:
                items = svg_path_items(d, box.x0, box.y0)
                if items:
                    xs = [p[0] for it in items for p in it[1:]]; ys = [p[1] for it in items for p in it[1:]]
                    out.append({"rect": pymupdf.Rect(min(xs), min(ys), max(xs), max(ys)), "fill": key[0], "items": items, "area": (max(xs) - min(xs)) * (max(ys) - min(ys)), "even_odd": True, "virtual": key[1]})
    return out

def size_table(spans):
    """Dimension table on QLD sheets: a header row of single letters (a b c ...) then rows of figures; first row -> {letter: value}."""
    rows = {}
    for s in spans: rows.setdefault(round(s["bbox"].y0 / 3) * 3, []).append(s)
    ordered = sorted(rows.items())
    for i, (y, cs) in enumerate(ordered):
        letters = sorted([c for c in cs if re.fullmatch(r"[a-z]{1,2}", c["text"].strip())], key=lambda c: c["bbox"].x0)
        if len(letters) < 3: continue
        for y2, cs2 in ordered[i + 1:i + 3]:
            nums = sorted([c for c in cs2 if re.fullmatch(r"\d{1,5}(?:\.\d+)?\s*[A-Za-z]{0,3}\*?", c["text"].strip())], key=lambda c: c["bbox"].x0)
            if len(nums) >= 3:
                out = {}
                for c in nums:
                    cx = (c["bbox"].x0 + c["bbox"].x1) / 2; l = min(letters, key=lambda L: abs((L["bbox"].x0 + L["bbox"].x1) / 2 - cx)); out[l["text"].strip()] = c["text"].strip()
                return out
    return None

def stated_size(spans):
    """'W x H' figure on the sheet (mm): the largest one with sign-sized values (font sizes like '8 x 16' are skipped)."""
    best = None
    for s in spans:
        m = re.fullmatch(r"(\d{2,5})\s*[x×]\s*(\d{2,5})(?:\s*mm)?", s["text"].strip())
        if m:
            w, h = float(m.group(1)), float(m.group(2))
            if max(w, h) >= 100 and (best is None or w * h > best[0] * best[1]): best = (w, h)
    return best

def stated_scale(spans):
    for s in spans:
        m = re.search(r"SCALE\s*:?\s*1\s*:\s*(\d+)", s["text"], re.I)
        if m: return float(m.group(1))
    return None

def dimension_figure(spans, pr):
    """Overall width (figure centred above/below the drawing) or height (figure beside it): the largest aligned figure."""
    best = None
    for s in spans:
        t = s["text"].strip().replace("mm", "").strip()
        if not re.fullmatch(r"\d{2,5}(?:\.\d+)?\*?", t): continue
        v = float(t.rstrip("*")); bb = s["bbox"]; cx = (bb.x0 + bb.x1) / 2; cy = (bb.y0 + bb.y1) / 2
        if abs(cx - (pr.x0 + pr.x1) / 2) <= 0.1 * pr.width and (pr.y0 - 60 < bb.y1 < pr.y0 + 2 or pr.y1 - 2 < bb.y0 < pr.y1 + 60):
            if best is None or v > best[1]: best = (0, v, "w")
        elif abs(cy - (pr.y0 + pr.y1) / 2) <= 0.1 * pr.height and (pr.x0 - 60 < bb.x1 < pr.x0 + 2 or pr.x1 - 2 < bb.x0 < pr.x1 + 60):
            if best is None or (best[2] == "h" and v > best[1]): best = (0, v, "h")
    return (best[1], best[2]) if best else None

def extract_page(pdf, pno=0, min_area_frac=0.02):
    """Drawings on a sheet: list of sign dicts for X.write_svg (panel, fills, scale, note, superseded, text)."""
    doc = pymupdf.open(pdf); page = doc[pno]
    spans0 = raw_spans(page); F = Frame(page, spans0)
    spans = [dict(s, bbox=F.R(s["bbox"]), origin=F.P(s["origin"]), block_bbox=F.R(s["block_bbox"])) for s in spans0]
    pdoc = pymupdf.open(paths_pdf(pdf)); ppage = pdoc[min(pno, len(pdoc) - 1)]
    F2 = Frame.baked(ppage, F)      # the converted page carries the page rotation in its content already
    fills = page_fills(ppage, F2) + closed_strokes(ppage, F2)
    if not fills: return []
    region = drawing_region(F, spans)
    superseded = any("SUPERSEDED" in s["text"].upper() for s in spans)
    def annotation(s): return not SIGN_FONT.search(s["font"]) and (is_number(s["text"]) or not region.contains(pymupdf.Point(s["origin"])))
    ann_boxes = [s["bbox"] + (-2.5, -2.5, 2.5, 2.5) for s in spans if annotation(s)]
    blocks = {}
    for s in spans: blocks.setdefault(s["block"], []).append(s)
    ann_boxes += [ss[0]["block_bbox"] + (-2.5, -2.5, 2.5, 2.5) for ss in blocks.values() if all(annotation(s) for s in ss)]   # a text object converted as one path
    from shapely.geometry import box as sbox
    from shapely.ops import unary_union
    ann_union = unary_union([sbox(b.x0, b.y0, b.x1, b.y1) for b in ann_boxes]) if ann_boxes else None
    def under_annotation(f):
        r = f["rect"]
        if any(b.contains(r) for b in ann_boxes): return True
        if ann_union is None or r.get_area() <= 0: return False
        return ann_union.intersection(sbox(r.x0, r.y0, r.x1, r.y1)).area >= 0.7 * r.get_area()   # a text block converted as one path
    def in_region(f):
        r = f["rect"]
        if f.get("virtual"): return region.contains(r) and r.get_area() < 0.5 * F.rect.get_area()     # outlines: wholly inside, never the sheet frame
        return region.contains(pymupdf.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)) and r.get_area() < 0.5 * F.rect.get_area()
    inside = [f for f in fills if in_region(f) and not under_annotation(f)]
    if not inside: return []
    U = bbox_of(inside); m = 0.015 * max(U.width, U.height)
    size_wh = stated_size(spans); scale_n = stated_scale(spans); table = size_table(spans)
    signs = []
    ann_spans = [s["bbox"] + (-3, -3, 3, 3) for s in spans if annotation(s)]
    def caption(box):
        """Short uppercase label under a drawing (LEFT / RIGHT / RURAL ...), used to name variants."""
        cs = [s for s in spans if not annotation(s) and box.y1 - 2 < s["bbox"].y0 < box.y1 + 30 and box.x0 - 10 < (s["bbox"].x0 + s["bbox"].x1) / 2 < box.x1 + 10
              and s["text"].strip().upper() == s["text"].strip() and 1 <= len(s["text"].split()) <= 3 and re.search(r"[A-Z]", s["text"])]
        return cs[0]["text"].strip() if cs else ""
    for g in clusters(inside, m):
        box = bbox_of(g)
        if box.get_area() < min_area_frac * region.get_area(): continue
        real = [f for f in g if not f.get("virtual")]
        if not real: continue                                                                        # outlines with nothing drawn inside
        def is_frame(v):
            inner = [f for f in real if v["rect"].contains(f["rect"]) and f["area"] >= 0.45 * v["area"]]
            return bool(inner) and not any(abs(f["rect"].x0 - v["rect"].x0) < 2 and abs(f["rect"].y0 - v["rect"].y0) < 2 and abs(f["rect"].x1 - v["rect"].x1) < 2 and abs(f["rect"].y1 - v["rect"].y1) < 2 for f in inner)
        g = [f for f in g if not (f.get("virtual") and is_frame(f))]
        if sum(1 for f in real if any(b.intersects(f["rect"]) for b in ann_spans)) >= 0.8 * len(real): continue   # a text block (table, note) converted to paths
        if len(real) > 25 and max(f["area"] for f in real) < 0.02 * box.get_area() and all(X.colour_name(f["fill"]) == "BLACK" for f in real): continue   # outlined text block
        if any(s["text"].strip().lower().startswith("example") and (box + (-40, -40, 40, 40)).contains(pymupdf.Point(s["origin"])) for s in spans): continue
        g = sorted([f for f in g if f.get("virtual")], key=lambda f: -f["area"]) + real            # outlines painted first, then the sheet's fills in order
        panel = max(g, key=lambda f: f["area"])
        hull = X.convex_hull(X.item_points(panel["items"]))
        bordered = panel["area"] >= 0.5 * box.get_area()
        if not bordered:   # a border ring drawn as a fill with nothing behind it: its outline becomes the white panel
            big = max(real, key=lambda f: f["area"])
            if big["area"] >= 0.85 * box.get_area() and len(big["items"]) >= 6:
                hb = X.convex_hull(X.item_points(big["items"]))
                if len(hb) >= 3:
                    items = [("l", hb[i], hb[(i + 1) % len(hb)]) for i in range(len(hb))]
                    virt = {"rect": big["rect"], "fill": (1.0, 1.0, 1.0), "items": items, "area": big["area"], "even_odd": False, "virtual": True}
                    g = [virt] + g; panel = virt; hull = hb; bordered = True
        assumed = False
        if not bordered and not any(f.get("virtual") for f in g):   # outline drawn as loose strokes: assume a white rectangular background
            r = box; items = [("l", (r.x0, r.y0), (r.x1, r.y0)), ("l", (r.x1, r.y0), (r.x1, r.y1)), ("l", (r.x1, r.y1), (r.x0, r.y1)), ("l", (r.x0, r.y1), (r.x0, r.y0))]
            virt = {"rect": r, "fill": (1.0, 1.0, 1.0), "items": items, "area": r.get_area(), "even_odd": False, "virtual": True}
            g = [virt] + g; panel = virt; hull = X.convex_hull(X.item_points(items)); bordered = True; assumed = True
        pr = panel["rect"] if bordered else box
        tri = [f for f in real if X.is_triangle(f["items"])]
        triangulated = len(tri) > 60 and len(tri) > 0.4 * max(1, len(real))
        def keep(f):
            r = f["rect"]; c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
            if bordered and not X.in_hull(hull, c) and f["area"] < 0.2 * box.get_area(): return False
            if not triangulated and X.is_triangle(f["items"]) and f["area"] < 0.004 * pr.get_area(): return False   # dimension arrowheads
            if min(r.width, r.height) <= 0.4 and max(r.width, r.height) > 15 * min(r.width, r.height): return False  # leader / mask lines
            if f.get("virtual") and f["area"] < 0.01 * pr.get_area(): return False                                 # small closed strokes: symbols' outlines, arrows
            return True
        content = [f for f in g if keep(f)]
        if not content or (len(content) == 1 and len(content[0]["items"]) <= 5): continue          # swatch / speck
        if triangulated: content = union_by_colour(content, box)
        pr = bbox_of(content) if not bordered else (pr | bbox_of([f for f in content if not f.get("virtual")]))   # stacked panels extend the sign
        note = []; scale = None
        dim = dimension_figure(spans, pr)
        if dim and dim[0] < 100: dim = None                                                          # a small figure is a detail, not the overall size
        if size_wh:
            land = pr.width >= pr.height
            sw, sh = (max(size_wh), min(size_wh)) if land else (min(size_wh), max(size_wh))
            scale = sw / pr.width; note.append(f"size from the sheet's {fmt(size_wh[0])} x {fmt(size_wh[1])} figure")
            if abs(sh / pr.height - scale) > 0.05 * scale: note.append(f"drawn proportions differ from the stated size ({fmt(pr.width * scale)} x {fmt(pr.height * scale)} mm drawn) — check")
        elif dim:
            scale = dim[0] / (pr.width if dim[1] == "w" else pr.height); note.append(f"size from the drawing's overall {'width' if dim[1] == 'w' else 'height'} dimension ({fmt(dim[0])} mm)")
        elif table and re.match(r"\d", table.get("a", "")):
            a = float(re.match(r"[\d.]+", table["a"]).group(0)); b = re.match(r"[\d.]+", table.get("b", "")); b = float(b.group(0)) if b else None
            if b and abs(a / b - pr.width / pr.height) > abs(b / a - pr.width / pr.height): a, b = b, a
            scale = a / pr.width; note.append(f"size from the sheet's dimension table, first row (a = {fmt(a)}{', b = ' + fmt(b) if b else ''}); other rows are size variants not produced")
        elif scale_n:
            scale = scale_n * MM_PER_PT; note.append(f"size from the stated drawing scale 1:{fmt(scale_n)}")
        else:
            scale = 10 * MM_PER_PT; note.append("no size found on the sheet; drawn at 1:10 — check")
        if superseded: note.append("sheet is stamped SUPERSEDED")
        if assumed: note.append("background assumed to be a white rectangle (outline drawn as loose strokes) — check")
        if triangulated: note.append("triangulated CAD export unioned")
        signs.append({"panel": pr, "fills": content, "glyphs": [], "scale": scale / 25.4, "bg": X.colour_name(panel["fill"]), "note": "; ".join(note), "superseded": superseded, "caption": caption(box),
                      "text": " ".join(s["text"] for s in spans if pr.contains(pymupdf.Point(s["origin"])))})
    signs.sort(key=lambda s: -s["panel"].get_area())
    def sig(sn):
        pr = sn["panel"]
        return tuple(sorted((round((f["rect"].x0 - pr.x0) / pr.width, 1), round((f["rect"].y0 - pr.y0) / pr.height, 1), round(f["rect"].width / pr.width, 1), round(f["rect"].height / pr.height, 1), X.colour_name(f["fill"])) for f in sn["fills"] if f["area"] > 0.002 * pr.get_area()))
    kept = []
    for sn in signs:
        same = [k for k in kept if sig(k) == sig(sn) and abs(k["panel"].width / k["panel"].height - sn["panel"].width / sn["panel"].height) < 0.03]
        if same: same[0]["sizes"] = same[0].get("sizes", 1) + 1; continue
        kept.append(sn)
    for sn in kept:
        if sn.get("sizes"): sn["note"] = (sn["note"] + "; " if sn["note"] else "") + f"drawn at {sn['sizes']} sizes on the sheet; largest kept"
    return kept

def sheet_spans(pdf, pno=0):
    doc = pymupdf.open(pdf); page = doc[pno]; spans0 = raw_spans(page); F = Frame(page, spans0)
    return [dict(s, bbox=F.R(s["bbox"]), origin=F.P(s["origin"])) for s in spans0], F
