#!/usr/bin/env python3
"""
shs_extract.py — lift sign artwork from the FHWA Standard Highway Signs design sheets (vector PDFs).

Each SHS page shows one or more signs with lettered dimensions and a table of values per sign size.
For every sign on a page:
  * fills inside the sign's outline are kept as drawn (panel, border, symbols, outlined legends); dimension
    lines, arrowheads, dimension-letter masks and anything outside the outline are dropped
  * legend characters set in the embedded Series*2000 fonts (2004/2012 sheets) are re-outlined with the
    repo's FHWA Series fonts at the exact per-glyph positions FHWA drew them
  * the drawing is scaled to real size from the size table: the row marked as conventional-road size where
    the sheet marks one (2004/2012), else the conventional-road size recorded for the same code in those
    editions (tools/shs_conventional_sizes.json), else a documented default that is written to the manifest
  * a left/right variant drawn only as a small thumbnail is scaled from the same table (the thumbnail is an
    exact scaled copy); a variant not drawn at all is mirrored from its sibling when the sign has no legend
Output: SVGs in the same header convention as the AS 1743 set (mm, viewBox 1 pt = 1 cm), plus a manifest.
"""
import os, re, sys, json, math, csv
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import signgen   # fonts, fmt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "USA", "Federal (MUTCD 2023)", "SVGs")
IN_MM = 25.4
CODE_RE = re.compile(r"^([A-Z]{1,2}\d{0,2}-\d{1,2}[a-zA-Z]{0,2}(?:\s?[LRVHC])?(?:\([^)]*\))?)$")
EMBEDDED_CAP = 0.285   # cap height / em of the embedded FHWA Series 2000 Type 1 fonts (from their glyph bounds)
SERIES = {"SeriesB2000": "B", "SeriesC2000": "C", "SeriesD2000": "D", "SeriesE2000": "E", "SeriesModE2000": "Emod", "SeriesF2000": "F",
          "HighwayB98": "B", "HighwayC98": "C", "HighwayD98": "D", "HighwayE98": "E", "HighwayME98": "Emod", "HighwayF98": "F",
          "HighwayB66": "B", "HighwayC66": "C", "HighwayD66": "D", "HighwayE66": "E", "HighwayME66": "Emod", "HighwayF66": "F",
          "FHWASeriesB": "B", "FHWASeriesC": "C", "FHWASeriesD": "D", "FHWASeriesE": "E", "FHWASeriesF": "F", "FHWASeriesE2000EX": "E"}
# cap height / em of the embedded fonts, measured from their 'H' outline (2004/2012 sheets): the Series*2000 and Highway*98
# Type 1 fonts are 0.285, the Highway*66 fonts 0.667; anything else is measured from the extracted font file at run time
CAP_RATIO = {}
DEFAULT_NAMES = {"OM": "OBJECT MARKER", "D": "GUIDE SIGN", "E": "GUIDE SIGN", "I": "GENERAL INFORMATION SIGN", "M": "ROUTE SIGN", "G": "GUIDE SIGN"}
CONVENTIONAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shs_conventional_sizes.json")))
NOTE_START = ("COLORS", "LEGEND", "BACKGROUND", "SYMBOL", "BORDER", "SEE ", "NOTE", "*", "—", "-", "(")

def fmt(v): return signgen.fmt(v)

def cap_ratio(doc, fontname):
    """Cap height / em of an embedded font, from its 'H' (or 'E', 'I') outline."""
    if fontname in CAP_RATIO: return CAP_RATIO[fontname]
    ratio = None
    for pno in range(len(doc)):
        for f in doc[pno].get_fonts():
            if f[3].split("+")[-1] != fontname: continue
            try:
                _, ext, _, buf = doc.extract_font(f[0])
                from fontTools.pens.boundsPen import BoundsPen
                if ext in ("pfa", "pfb"):
                    import tempfile
                    from fontTools.t1Lib import T1Font
                    with tempfile.NamedTemporaryFile(suffix="." + ext, delete=False) as fh: fh.write(buf); path = fh.name
                    gs = T1Font(path).getGlyphSet(); os.unlink(path); upm = 1000
                elif ext == "cff":
                    import io
                    from fontTools.cffLib import CFFFontSet
                    cff = CFFFontSet(); cff.decompile(io.BytesIO(buf), None); gs = cff[0].CharStrings; upm = 1000
                elif ext in ("ttf", "otf"):
                    import io
                    from fontTools.ttLib import TTFont
                    tt = TTFont(io.BytesIO(buf)); gs = tt.getGlyphSet(); upm = tt["head"].unitsPerEm
                else: gs = None
                if gs:
                    for ch in "HEIT":
                        if ch in gs:
                            pen = BoundsPen(gs if ext != "cff" else None); gs[ch].draw(pen)
                            if pen.bounds: ratio = (pen.bounds[3] - pen.bounds[1]) / upm; break
            except Exception: ratio = None
            if ratio: break
        if ratio: break
    if not ratio:
        fam = font_family(fontname)
        ratio = 0.667 if fam.endswith("66") else 0.285 if (fam.startswith("Series") or fam.endswith("98")) else None
    CAP_RATIO[fontname] = ratio
    return ratio
def font_family(font): return font.split("+")[-1].split("-")[0]
def base_code(c): return re.sub(r"\s?[LR]$", "", c.replace(" ", ""))

def page_lines(page):
    d = page.get_text("dict"); out = []
    for b in d["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            txt = "".join(s["text"] for s in l["spans"]).strip()
            if not txt: continue
            out.append({"bbox": l["bbox"], "text": txt, "size": max(s["size"] for s in l["spans"]),
                        "series": any(font_family(s["font"]) in SERIES for s in l["spans"])})
    return out

def is_note(t):
    u = t.upper()
    return u.startswith(NOTE_START) or "COLORS" in u or "RETROREFLECTIVE" in u or "EDITION" in u or "SEE PAGE" in u or re.fullmatch(r"[\d.,\s/x×-]+", u) is not None

def page_signs(page):
    """Find sign code labels and their names on the page."""
    lines = page_lines(page); labels = []
    for l in lines:
        m = CODE_RE.match(l["text"].replace("  ", " "))
        if m and l["size"] >= 12 and not l["series"]:
            x0, y0, x1, y1 = l["bbox"]; labels.append({"code": l["text"], "x": (x0 + x1) / 2, "y": y0, "bbox": l["bbox"]})
    def namey(l):
        t = l["text"]
        return sum(ch.isalpha() for ch in t) >= 3 and not CODE_RE.match(t) and not is_note(t) and l["size"] <= 12 and not l["series"]
    for lab in labels:
        cands = [(abs((l["bbox"][0] + l["bbox"][2]) / 2 - lab["x"]) + (l["bbox"][1] - lab["bbox"][3]), l["text"]) for l in lines
                 if 0 < l["bbox"][1] - lab["bbox"][3] < 25 and abs((l["bbox"][0] + l["bbox"][2]) / 2 - lab["x"]) < 120 and namey(l)]
        cands += [(l["bbox"][0] - lab["bbox"][2], l["text"]) for l in lines      # same line, to the right of the code
                  if lab["bbox"][1] - 2 < (l["bbox"][1] + l["bbox"][3]) / 2 < lab["bbox"][3] + 2 and 0 < l["bbox"][0] - lab["bbox"][2] < 40 and namey(l) and l["text"].upper() == l["text"]]
        cands.sort(); hints = [c for c in cands if c[1].upper().strip("() ") in ("ENGLISH", "METRIC")]
        lab["hint"] = hints[0][1].upper().strip("() ") if hints else ""
        cands = [c for c in cands if c not in hints]
        lab["name"] = cands[0][1] if cands else ""
    for lab in labels:   # unnamed L/R variant: its sibling's name
        if not lab["name"]:
            sib = [o for o in labels if o["name"] and base_code(o["code"]) == base_code(lab["code"])]
            if sib: lab["name"] = sib[0]["name"]
    used = {l["name"] for l in labels}
    def followed_by_note(l):   # "WARNING SIGN" above "COLORS: ..." is a colour-note heading, not a title
        return any(0 < o["bbox"][1] - l["bbox"][3] < 14 and abs(o["bbox"][0] - l["bbox"][0]) < 20 and o["text"].upper().startswith("COLORS") for o in lines)
    titles = [l for l in lines if l["text"].upper() == l["text"] and 4 < len(l["text"]) < 60 and namey(l) and l["text"] not in used
              and l["text"].strip("() ") not in ("ENGLISH", "METRIC")
              and not re.search(r"\d", l["text"]) and not followed_by_note(l)]
    for lab in labels:   # still unnamed: the page's group title
        if not lab["name"] and titles:
            lab["name"] = min(titles, key=lambda t: abs(t["bbox"][1] - lab["y"]))["text"]
    return labels

def default_name(lab, sign):
    txt = legend_text(sign).strip()
    if txt and len(txt) <= 40 and sum(ch.isalpha() for ch in txt) >= 3: return txt.upper()
    fam = re.match(r"[A-Z]+", lab["code"]).group(0)
    return DEFAULT_NAMES.get(fam, DEFAULT_NAMES.get(fam[0], ""))

def fills_on_page(page):
    out = []; seen = set()
    for dr in page.get_drawings():
        if dr.get("fill") is None: continue
        r = dr["rect"]; key = (round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1), dr["fill"], len(dr["items"]))
        if key in seen: continue
        seen.add(key); out.append({"rect": r, "fill": dr["fill"], "items": dr["items"], "area": r.get_area(), "even_odd": dr.get("even_odd")})
    return out

def item_points(items):
    pts = []
    for it in items:
        k = it[0]
        if k == "l": pts += [it[1], it[2]]
        elif k == "c": pts += [it[1], it[2], it[3], it[4]]
        elif k == "re": r = it[1]; pts += [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
        elif k == "qu": q = it[1]; pts += [q.ul, q.ur, q.lr, q.ll]
    return [(float(p[0]), float(p[1])) for p in pts]

def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def in_hull(hull, p, tol=0.5):
    """Point inside a convex polygon (counter-clockwise hull), with a small tolerance in points."""
    n = len(hull)
    if n < 3: return False
    for i in range(n):
        a, b = hull[i], hull[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]; L = math.hypot(ex, ey) or 1
        if (ex * (p[1] - a[1]) - ey * (p[0] - a[0])) / L < -tol: return False
    return True

def is_triangle(items):
    if not 3 <= len(items) <= 4 or any(it[0] != "l" for it in items): return False
    return len({(round(p[0], 1), round(p[1], 1)) for it in items for p in (it[1], it[2])}) == 3

def is_diamond(hull, pr):
    """A square drawn point-up: outline points sit at the bbox mid-edges and none near its corners."""
    if abs(pr.width - pr.height) > 0.02 * pr.width or len(hull) < 4: return False
    w = pr.width; corners = [(pr.x0, pr.y0), (pr.x1, pr.y0), (pr.x1, pr.y1), (pr.x0, pr.y1)]
    if any(math.hypot(p[0] - c[0], p[1] - c[1]) < 0.2 * w for p in hull for c in corners): return False
    cx, cy = (pr.x0 + pr.x1) / 2, (pr.y0 + pr.y1) / 2
    mids = [(cx, pr.y0), (pr.x1, cy), (cx, pr.y1), (pr.x0, cy)]
    return all(any(math.hypot(p[0] - m[0], p[1] - m[1]) < 0.12 * w for p in hull) for m in mids)

def path_d(items, T):
    d = []
    for it in items:
        k = it[0]
        if k == "l": p, q = it[1], it[2]; d.append(f"M{fmt(T(p)[0])} {fmt(T(p)[1])}L{fmt(T(q)[0])} {fmt(T(q)[1])}")
        elif k == "c":
            p0, p1, p2, p3 = it[1:5]; a, b, c, e = T(p0), T(p1), T(p2), T(p3)
            d.append(f"M{fmt(a[0])} {fmt(a[1])}C{fmt(b[0])} {fmt(b[1])} {fmt(c[0])} {fmt(c[1])} {fmt(e[0])} {fmt(e[1])}")
        elif k == "re":
            r = it[1]; a = T((r.x0, r.y0)); b = T((r.x1, r.y1)); d.append(f"M{fmt(a[0])} {fmt(a[1])}H{fmt(b[0])}V{fmt(b[1])}H{fmt(a[0])}Z")
        elif k == "qu":
            q = it[1]; pts = [T(q.ul), T(q.ur), T(q.lr), T(q.ll)]; d.append("M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts) + "Z")
    return "".join(_join(d))

def _join(segs):
    """Merge consecutive 'M a L b' segments that continue from the previous end point into one subpath."""
    out = []; last_end = None
    for s in segs:
        m = re.match(r"M([-\d.]+) ([-\d.]+)(.*)", s)
        if m and last_end and (m.group(1), m.group(2)) == last_end: out.append(m.group(3))
        else: out.append(s)
        e = re.findall(r"[LC][^LCMHVZ]*", s)
        if e:
            nums = re.findall(r"-?\d+\.?\d*", e[-1]); last_end = (nums[-2], nums[-1]) if len(nums) >= 2 else None
        else: last_end = None
    return out

def colour_name(c):
    r, g, b = c[:3]
    if r > 0.9 and g > 0.9 and b > 0.9: return "WHITE"
    if r < 0.25 and g < 0.25 and b < 0.25: return "BLACK"
    if r > 0.7 and g < 0.35 and b < 0.35: return "RED"
    if r > 0.85 and g > 0.45 and g < 0.7 and b < 0.3: return "ORANGE"
    if r > 0.85 and g > 0.7 and b < 0.4: return "YELLOW"
    if b > 0.4 and r < 0.3 and g < 0.6: return "BLUE"
    if g > 0.35 and r < 0.3 and b < 0.5: return "GREEN"
    if r > 0.3 and g < 0.4 and b < 0.3: return "BROWN"
    if r < 0.6 and g > 0.5 and b > 0.5: return "TEAL"
    return "VARIANT"

def hexcol(c): return "#%02x%02x%02x" % tuple(int(round(v * 255)) if v <= 1 else int(v) for v in c)

def parse_table(page, below_y, x_center):
    """Return (headers, rows, flagged_row_index or None) for the dimension table nearest below below_y."""
    d = page.get_text("dict"); cells = []
    for b in d["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for s in l["spans"]:
                t = s["text"].strip()
                if t and s["size"] <= 12 and s["bbox"][1] > below_y: cells.append((s["bbox"], t))
    if not cells: return None
    rows = {}
    for bb, t in cells: rows.setdefault(round(bb[1] / 4) * 4, []).append((bb[0], t, bb))
    ordered = sorted(rows.items())
    header = None
    for y, cs in ordered:
        cs.sort(); letters = [c for c in cs if re.fullmatch(r"[A-Z]{1,2}|SIGN", c[1])]
        if len(letters) < 3: continue
        seq = [c[1] for c in letters if c[1] != "SIGN"]
        if seq != sorted(seq) or len(set(seq)) != len(seq) or seq[0] not in ("A", "B", "H", "O", "V", "AA"): continue
        lo, hi = letters[0][0], letters[-1][0]
        if any(lo < c[0] < hi for c in cs if c not in letters): continue      # other text inside the header span: not a header
        header = (y, [c for c in letters if c[1] != "SIGN"]); break
    if not header: return None
    hx = [(bb[0] + bb[2]) / 2 for _, _, bb in header[1]]; hnames = [t for _, t, _ in header[1]]
    left_edge = min(bb[0] for _, _, bb in header[1]) - 6
    rows_out = []; flag_letters = {}
    data = []
    for y, cs in ordered:
        if y <= header[0]: continue
        cs.sort(); intab = [c for c in cs if c[0] >= left_edge]; marks = [t for x0, t, _ in cs if left_edge - 30 < x0 < left_edge and t in ("C", "E", "F", "M", "O")]
        if intab and len(intab) >= 3 and all(re.fullmatch(r"[A-Z]{1,2}|SIGN", c[1]) for c in intab): break   # a second table (multi-row headers) ends this one
        nums = [c for c in intab if re.fullmatch(r"[\d.]+", c[1])]
        if len(nums) >= 2 and intab and (re.fullmatch(r"[\d.]+", intab[0][1]) or "digit" in intab[0][1].lower() or intab[0][1].lower() in ("min", "max")):
            data.append((y, [c for c in intab if re.fullmatch(r"[\d.]+ ?[A-Z]?\*?|[\d.]+|[\d.]+ [A-Z]\(?M?\)?|VAR", c[1])], marks))
    for y, cs, marks in data:
        row = {}
        for x0, t, bb in cs:
            cx = (bb[0] + bb[2]) / 2; j = min(range(len(hx)), key=lambda i: abs(hx[i] - cx)); row[hnames[j]] = t
        rows_out.append((y, row)); flag_letters[len(rows_out) - 1] = marks
    if not rows_out: return None
    flagged = None
    for i, marks in flag_letters.items():
        if "C" in marks: flagged = i; break
    else:
        for i, marks in flag_letters.items():
            if marks: flagged = i; break
    return hnames, [r for _, r in rows_out], flagged

def row_A(row):
    try: return float(re.match(r"[\d.]+", row.get("A", "")).group(0))
    except (AttributeError, ValueError): return None

def choose_row(code, rows, flagged, square):
    """Size row to draw at. Returns (row, note)."""
    if flagged is not None: return rows[flagged], ""
    As = [row_A(r) for r in rows]
    known = CONVENTIONAL.get(base_code(code))
    if known:
        for want in known:
            for r, a in zip(rows, As):
                if a == want: return r, f"size {fmt(a)} in: conventional-road row for {base_code(code)} in the 2004/2012 sheets (2024 table has no marker)"
    if len(rows) == 1: return rows[0], ""
    if square:   # diamonds: 30 in is the conventional-road size unless the table starts higher
        for r, a in zip(rows, As):
            if a == 30: return r, "size 30 in: no conventional-road marker in the table and no earlier edition of this code; 30 in diamond chosen — check"
        cands = [(a, r) for r, a in zip(rows, As) if a is not None and a >= 24]
    else: cands = [(a, r) for r, a in zip(rows, As) if a is not None]
    if not cands: return rows[0], "size row: first table row (no size value read) — check"
    a, r = min(cands, key=lambda c: c[0]); return r, f"size {fmt(a)} in: smallest table row (no conventional-road marker, no earlier edition of this code) — check"

def inline_width(page, pr, lab):
    """Overall width figure annotated under (or over) the drawing: a plain number centred on the panel."""
    d = page.get_text("dict"); best = None
    for b in d["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                t = sp["text"].strip()
                if not re.fullmatch(r"\d{1,3}(?:\.\d+)?", t) or sp["size"] > 12: continue
                bb = sp["bbox"]; cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
                v = float(t)
                if not 6 <= v <= 240: continue
                if abs(cx - (pr.x0 + pr.x1) / 2) <= 0.12 * pr.width:
                    below = pr.y1 - 2 < bb[1] < lab["y"] + 2; above = pr.y0 - 45 < bb[3] < pr.y0 + 2
                    if not (below or above): continue
                    dist = min(abs(bb[1] - pr.y1), abs(pr.y0 - bb[3]))
                    if best is None or dist < best[0]: best = (dist, v, "w")
                elif abs(cy - (pr.y0 + pr.y1) / 2) <= 0.12 * pr.height and (pr.x0 - 45 < bb[2] < pr.x0 + 2 or pr.x1 - 2 < bb[0] < pr.x1 + 45):
                    dist = min(abs(pr.x0 - bb[2]), abs(bb[0] - pr.x1)) + 5      # height figure beside the drawing
                    if best is None or dist < best[0]: best = (dist, v, "h")
    return (best[1], best[2]) if best else None

def side_figure(page, pr):
    """A diamond's side length: a lone figure written along its upper-left edge."""
    best = None
    for b in page.get_text("dict")["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                t = sp["text"].strip()
                if not re.fullmatch(r"\d{1,2}(?:\.\d+)?", t) or sp["size"] > 12: continue
                bb = sp["bbox"]; cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
                if not (pr.x0 - 30 < cx < (pr.x0 + pr.x1) / 2 and pr.y0 - 30 < cy < (pr.y0 + pr.y1) / 2): continue
                v = float(t)
                if not 6 <= v <= 60: continue
                d = abs(cx - (pr.x0 + (pr.x0 + pr.x1) / 2) / 2) + abs(cy - (pr.y0 + (pr.y0 + pr.y1) / 2) / 2)   # near the edge midpoint
                if best is None or d < best[0]: best = (d, v)
    return best[1] if best else None

def page_glyphs(raw, pr, doc):
    glyphs = []
    for b in raw["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                fam = font_family(sp["font"])
                if fam not in SERIES: continue
                cr = cap_ratio(doc, sp["font"].split("+")[-1])
                if not cr: continue
                for c in sp["chars"]:
                    ox, oy = c["origin"]; bb = c["bbox"]
                    if pr.x0 - 2 <= ox <= pr.x1 + 2 and pr.y0 - 2 <= oy <= pr.y1 + 2 and c["c"].strip():
                        glyphs.append({"c": c["c"], "x": ox, "y": oy, "bbox": bb, "series": SERIES[fam], "size": sp["size"], "cap": cr,
                                       "colour": hexcol(pymupdf.sRGB_to_rgb(sp["color"])) if isinstance(sp.get("color"), int) else "#000"})
    return glyphs

ANNOTATION_FONTS = ("NimbusSan", "Aptos", "TimesNewRoman", "Arial", "Calibri", "Myriad", "Helvetica")

def foreign_legend(raw, pr):
    """Legend-sized text inside the panel set in a font the extractor cannot outline (logo lettering etc.)."""
    found = set()
    for b in raw["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                fam = font_family(sp["font"]); name = sp["font"].split("+")[-1]
                if fam in SERIES or any(a in name for a in ANNOTATION_FONTS) or sp["size"] < 14 or not "".join(c["c"] for c in sp["chars"]).strip(): continue
                ox, oy = sp["origin"]
                if pr.x0 <= ox <= pr.x1 and pr.y0 <= oy <= pr.y1: found.add(name)
    return sorted(found)

def annotation_spans(raw):
    """Origins of dimension letters / figures / notes (non-Series text of small size)."""
    out = []
    for b in raw["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                if font_family(sp["font"]) in SERIES or sp["size"] > 12: continue
                for c in sp["chars"]:
                    if c["c"].strip(): out.append(((c["bbox"][0] + c["bbox"][2]) / 2, (c["bbox"][1] + c["bbox"][3]) / 2))
    return out

def looks_like_text(fills, panel_area):
    """Outlined legend present? Several small many-vertex fills."""
    n = sum(1 for f in fills if f["area"] < 0.02 * panel_area and len(f["items"]) >= 6)
    return n >= 3

def extract_page(doc, pno, family):
    page = doc[pno]; labels = page_signs(page)
    if not labels: return []
    fills = fills_on_page(page)
    raw = page.get_text("rawdict"); ann = annotation_spans(raw)
    big = [f for f in fills if f["area"] > 4000]
    def contained(f, g): return g["rect"].x0 - 1 <= f["rect"].x0 and g["rect"].y0 - 1 <= f["rect"].y0 and g["rect"].x1 + 1 >= f["rect"].x1 and g["rect"].y1 + 1 >= f["rect"].y1
    panels = [f for f in big if not any(g is not f and g["area"] > f["area"] and contained(f, g) for g in big)]
    def has_glyph(pr):
        for b in raw["blocks"]:
            if not b.get("lines"): continue
            for l in b["lines"]:
                for sp in l["spans"]:
                    if font_family(sp["font"]) in SERIES and pr.x0 <= sp["origin"][0] <= pr.x1 and pr.y0 <= sp["origin"][1] <= pr.y1: return True
        return False
    def has_content(f): return has_glyph(f["rect"]) or any(g is not f and contained(g, f) and g["area"] > 20 for g in fills)
    panels = [f for f in panels if not (len(f["items"]) == 1 and f["fill"] == (1.0, 1.0, 1.0) and not has_content(f))]   # plain white masks
    # assign panels to labels: a label sits below its sign, or beside it (diamond tips); nearest unclaimed panel wins
    def dist(lab, f):
        r = f["rect"]
        if r.y0 > lab["y"]: return 1e9                     # panel entirely below the label: not its sign
        dx = 0 if r.x0 - 30 <= lab["x"] <= r.x1 + 30 else min(abs(lab["x"] - r.x0), abs(lab["x"] - r.x1))
        dy = max(0, lab["bbox"][1] - r.y1)
        return dx + 0.5 * dy
    claimed = {}
    for lab in sorted(labels, key=lambda l: l["y"]):
        cands = [(dist(lab, f), i) for i, f in enumerate(panels) if i not in claimed]
        cands = [c for c in cands if c[0] < 400]
        if cands: claimed[min(cands)[1]] = lab
    for i, f in enumerate(panels):   # leftover panels (colour variants drawn beside the dimensioned one) attach to the nearest label
        if i in claimed: continue
        cands = [(dist(lab, f), lab) for lab in labels]; cands = [c for c in cands if c[0] < 400]
        if cands: claimed[i] = min(cands, key=lambda c: c[0])[1]
    per_label = {}
    for i, lab in claimed.items(): per_label.setdefault(id(lab), []).append(panels[i])
    results = []; by_label = {}
    def bg_colour(panel):
        ins = [f for f in fills if contained(f, panel) and f["area"] >= 0.5 * panel["area"]]
        non_white = [f for f in ins if colour_name(f["fill"]) != "WHITE"]
        return colour_name(non_white[-1]["fill"]) if non_white else colour_name(panel["fill"])
    # biggest drawings first so a thumbnail can take its scale from the dimensioned sibling
    for lab in sorted(labels, key=lambda l: -max([p["area"] for p in per_label.get(id(l), [])] or [0])):
        ps = per_label.get(id(lab), [])
        if not ps: continue
        def legend_len(p): return len(page_glyphs(raw, p["rect"], doc))
        ps = sorted(ps, key=lambda p: (legend_len(p), dist(lab, p)))          # primary: plainest legend, then nearest to the label
        widest = max(p["rect"].width for p in ps)
        insets = [p for p in ps[1:] if p["rect"].width < 0.6 * widest and not any(o is not lab and base_code(o["code"]) == base_code(lab["code"]) for o in labels)]
        ps = [p for p in ps if p not in insets]
        primary_bg = bg_colour(ps[0])
        for vi, panel in enumerate(ps):
            pr = panel["rect"]
            bg = bg_colour(panel)
            variant = "" if vi == 0 else (bg if bg != primary_bg else f"VAR{vi + 1}")
            hull = convex_hull(item_points(panel["items"]))
            def is_annotation(f):
                r = f["rect"]; items = f["items"]
                c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
                if not in_hull(hull, c): return True                                                            # outside the sign outline
                if len(items) == 1 and items[0][0] == "re" and min(r.width, r.height) <= 0.8 and max(r.width, r.height) > 9 * min(r.width, r.height): return True   # dimension ticks
                if min(r.width, r.height) <= 1.5 and colour_name(f["fill"]) == "WHITE" and max(r.width, r.height) > 12: return True   # white dimension-line masks
                if is_triangle(items) and f["area"] < 60: return True                                            # dimension arrowheads
                if f["area"] < 400 and any(r.x0 <= ax <= r.x1 and r.y0 <= ay <= r.y1 for ax, ay in ann): return True   # mask under a dimension letter/figure
                if len(items) == 1 and items[0][0] == "re" and f["area"] < 120 and colour_name(f["fill"]) == bg: return True   # background-coloured mask square
                if f["area"] < 30 and len(items) <= 4 and all(it[0] == "l" for it in items) and max(r.width, r.height) < 2.5 * min(r.width, r.height): return True   # arrowhead fragments
                return False
            glyphs = page_glyphs(raw, pr, doc)
            inside = [f for f in fills if (f is panel or contained(f, panel)) and not is_annotation(f)]   # page paint order kept
            dup = sum(1 for i, f in enumerate(inside) for g in inside[i + 1:] if f["fill"] == g["fill"] and len(f["items"]) == len(g["items"]) and abs(f["area"] - g["area"]) < 0.02 * f["area"]
                      and 0 < abs(f["rect"].x0 - g["rect"].x0) + abs(f["rect"].y0 - g["rect"].y0) < 6 and f["area"] > 200)
            square = abs(pr.width - pr.height) < 2
            tab = parse_table(page, lab["bbox"][3], lab["x"]); note = ""
            scale_in_per_pt = None; row = {}
            if tab:
                hnames, rows, flagged = tab
                row, note = choose_row(lab["code"], rows, flagged, square)
                A = row_A(row)
                if A:
                    if is_diamond(hull, pr): scale_in_per_pt = A * math.sqrt(2) / pr.width   # diamond: A is the side length
                    else: scale_in_per_pt = A / pr.width
            if not scale_in_per_pt:
                sib = [s for s in results if base_code(s["code"]) == base_code(lab["code"]) and s["scale_src"] in ("table", "inline")]
                kin = [s for s in results if s not in sib and s["code"].split("-")[0] == lab["code"].split("-")[0] and s["scale_src"] in ("table", "inline")
                       and abs(s["panel"].width / s["panel"].height - pr.width / pr.height) < 0.05 and is_diamond(s["hull"], s["panel"]) == is_diamond(hull, pr)]
                if sib:
                    s = sib[0]; scale_in_per_pt = s["scale"] * s["panel"].width / pr.width; row = s["row"]
                    note = f"scaled from the dimensioned {s['code']} drawing (thumbnail)"
                elif kin:
                    s = kin[0]; scale_in_per_pt = s["scale"] * s["panel"].width / pr.width; row = s["row"]
                    note = f"no dimension of its own; drawn to the same size as {s['code']} on the sheet — check"
            src = "table" if scale_in_per_pt else ""
            if not scale_in_per_pt:
                wv = inline_width(page, pr, lab)
                if wv and wv[1] == "w": scale_in_per_pt = wv[0] / pr.width; note = f"scale from the drawing's overall width dimension ({wv[0]} in)"; src = "inline"
                elif wv: scale_in_per_pt = wv[0] / pr.height; note = f"scale from the drawing's overall height dimension ({wv[0]} in)"; src = "inline"
                elif is_diamond(hull, pr) and side_figure(page, pr):
                    sv = side_figure(page, pr); scale_in_per_pt = sv * math.sqrt(2) / pr.width; note = f"scale from the drawing's side dimension ({sv} in)"; src = "inline"
                if not scale_in_per_pt: note = "no size table or width dimension read; drawn at page scale (1 pt = 0.1 in)"; scale_in_per_pt = 0.1; src = "page"
            if insets: note = (note + "; " if note else "") + f"{len(insets)} smaller detail drawing(s) beside it on the sheet not extracted"
            if vi and variant.startswith("VAR"):
                extra = [w for w in legend_text({"glyphs": glyphs}).split() if w not in legend_text(by_label[id(lab)][0]).split()]
                if extra: variant = re.sub(r"[^A-Z0-9]+", "_", " ".join(extra).upper()).strip("_")[:24] or variant
            if lab.get("hint") == "METRIC" and not variant: variant = "METRIC"
            sign = {"code": lab["code"], "name": lab["name"], "variant": variant, "bg": bg, "panel": pr, "fills": inside, "glyphs": glyphs, "scale": scale_in_per_pt,
                    "scale_src": src, "row": row, "note": note, "page": pno + 1, "hull": hull, "text_like": looks_like_text(inside, panel["area"])}
            if dup: sign["intervene"] = f"{dup} overlapping duplicate shape(s) in the sheet's drawing (FHWA artwork fault); needs a manual check"
            foreign = foreign_legend(raw, pr)
            if foreign: sign["intervene"] = f"legend set in {', '.join(foreign)} on the sheet, a font the extractor cannot outline; that lettering is missing"
            if not sign["name"]: sign["name"] = default_name(lab, sign)
            results.append(sign); by_label.setdefault(id(lab), []).append(sign)
    # L/R variants that the sheet does not draw: mirror the sibling when it carries no legend
    for lab in labels:
        if id(lab) in by_label or not re.search(r"[LR]$", lab["code"].replace(" ", "")): continue
        sibs = [s for o in labels if o is not lab and base_code(o["code"]) == base_code(lab["code"]) for s in by_label.get(id(o), [])]
        if not sibs: continue
        s = sibs[0]
        if s["text_like"]:
            results.append({**s, "code": lab["code"], "name": lab["name"] or s["name"], "intervene": f"{lab['code']} is not drawn on the sheet and {s['code']} carries an outlined legend that cannot be mirrored automatically"})
            continue
        results.append({**s, "code": lab["code"], "name": lab["name"] or s["name"], "mirror": True, "note": f"mirrored from {s['code']} (not drawn separately on the sheet)"})
    return results

def write_svg(sign, family):
    pr = sign["panel"]; k = sign["scale"] * IN_MM       # pt -> mm
    W, H = pr.width * k, pr.height * k
    mirror = sign.get("mirror")
    def T(p):
        x = (p[0] - pr.x0) * k
        return ((W - x) if mirror else x, (p[1] - pr.y0) * k)
    body = []
    for f in sign["fills"]:   # page paint order
        body.append(f'<path fill="{hexcol(f["fill"])}"{" fill-rule=\"evenodd\"" if f.get("even_odd") else ""} d="{path_d(f["items"], T)}"/>')
    # legend: outline each glyph with the repo's font at FHWA's drawn size and position.
    # The embedded Series*2000 Type 1 fonts have cap height 285/1000 em, so drawn cap height = 0.285 * font size.
    for g in sign["glyphs"]:
        fc = signgen.face(g["series"])
        capH = g["size"] * g.get("cap", EMBEDDED_CAP) * k
        name, adv, l, r, sx, shift = fc.glyph(g["c"])
        x, y = T((g["x"], g["y"]))
        if mirror: x = W - ((g["x"] - pr.x0) * k + adv * capH / signgen.CAP)   # keep the text reading left to right, mirror its slot
        d = fc.path(g["c"], capH, x + l * capH / signgen.CAP, y)
        body.append(f'<path fill="{g.get("colour", "#000")}" d="{d}"/>')
    OW, OH = W * 0.1, H * 0.1
    svg = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{fmt(OW * 25.4 / 72)}mm" height="{fmt(OH * 25.4 / 72)}mm" viewBox="0 0 {fmt(OW)} {fmt(OH)}">',
           '<g transform="scale(0.1)">'] + ["  " + b for b in body] + ["</g>", "</svg>"]
    return "\n".join(svg) + "\n", W, H

def rect_str(r): return f"{r.x0:.1f},{r.y0:.1f},{r.x1:.1f},{r.y1:.1f}"

def legend_text(sign):
    lines = []   # glyphs grouped by baseline (within half a cap height), each line left to right
    for g in sorted(sign["glyphs"], key=lambda g: g["y"]):
        cap = g["size"] * g.get("cap", EMBEDDED_CAP)
        if lines and abs(g["y"] - lines[-1][0]) < 0.5 * cap: lines[-1][1].append(g)
        else: lines.append((g["y"], [g]))
    out = []
    for _, gl in lines:
        last = None
        for g in sorted(gl, key=lambda g: g["x"]):
            if last and g["x"] - last["bbox"][2] > 0.3 * g["size"] * g.get("cap", EMBEDDED_CAP): out.append(" ")
            out.append(g["c"]); last = g
        out.append(" ")
    return "".join(out).strip()

def signature(sign):
    return (round(sign["panel"].width, 1), round(sign["panel"].height, 1), len(sign["fills"]), tuple(sorted(round(f["area"]) for f in sign["fills"])), legend_text(sign))

def main(pdf, family, pages=None):
    doc = pymupdf.open(pdf); rows = []
    folder = os.path.join(OUT, family); os.makedirs(folder, exist_ok=True)
    written = {}   # filename -> (signature, page, colour)
    intervene = []
    for pno in (pages or range(len(doc))):
        for s in extract_page(doc, pno, family):
            svg, W, H = write_svg(s, family)
            name = re.sub(r"[^A-Z0-9]+", "_", s["name"].upper()).strip("_") or "SIGN"
            code = s["code"].replace(" ", "")
            variant = s.get("variant", "")
            txt = legend_text(s).upper()
            if not variant and ("KM/H" in txt or "KM" in txt.split() or " M" in txt) and "METRIC" not in name: variant = "METRIC"
            fn = f"{name}_{variant}_{code}.svg" if variant else f"{name}_{code}.svg"
            sig = signature(s)
            if fn in written:
                if written[fn][0] == sig: continue        # same drawing repeated (e.g. the code shown on two pages)
                bg = s.get("bg", "")
                if bg and bg != written[fn][2]: variant = (variant + "_" if variant else "") + bg
                else:
                    n = 2
                    while f"{name}_{variant + '_' if variant else ''}{n}_{code}.svg" in written: n += 1
                    variant = f"{variant + '_' if variant else ''}{n}"
                s["note"] = (s["note"] + "; " if s["note"] else "") + f"same code and name as page {written[fn][1]} but a different drawing; suffixed"
                fn = f"{name}_{variant}_{code}.svg"
            written[fn] = (sig, s["page"], s.get("bg", ""))
            if s.get("intervene"):
                idir = os.path.join(OUT, "intervene", family); os.makedirs(idir, exist_ok=True)
                open(os.path.join(idir, fn), "w").write(svg); intervene.append((fn, s["page"], s["intervene"]))
                rows.append([code, s["name"], "intervene/" + fn, f"{W/IN_MM:.1f}x{H/IN_MM:.1f} in", s["row"].get("A", ""), s["page"], s["intervene"], rect_str(s["panel"])])
                continue
            open(os.path.join(folder, fn), "w").write(svg)
            rows.append([code, s["name"], fn, f"{W/IN_MM:.1f}x{H/IN_MM:.1f} in", s["row"].get("A", ""), s["page"], s["note"], rect_str(s["panel"])])
    with open(os.path.join(folder, "_extract_manifest.csv"), "a", newline="") as fh:
        csv.writer(fh).writerows(rows)
    if intervene:
        with open(os.path.join(OUT, "intervene", "INTERVENE_LIST.md"), "a") as fh:
            for fn, page, why in intervene: fh.write(f"- {family}/{fn} (page {page}): {why}\n")
    print(f"{len(rows)} signs from {os.path.basename(pdf)} -> {folder}")
    for r in rows: print("  ", r)

if __name__ == "__main__":
    pdf, family = sys.argv[1], sys.argv[2]
    pages = [int(p) - 1 for p in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
    main(pdf, family, pages)
