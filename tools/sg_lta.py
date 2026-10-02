#!/usr/bin/env python3
"""sg_lta.py — SVGs from the Land Transport Authority's Standard Details of Road Elements (SDRE, April 2014 edition,
Revision G of March 2025): the traffic-sign chapters 15 (mandatory), 16 (prohibitory), 17 (warning), 18 (informatory),
19 (supplementary plates) and the cycling signs of chapter 21, in Processing/Singapore/National (LTA)/Original PDFs/.

Every sheet is a vector CAD plot at a stated scale (1:10 on the sign sheets): faces are coloured fills, every visible
character (legends and dimension figures alike) is an outlined black fill, and an invisible Times-Roman text layer
repeats the annotations (titles, notes, dimension figures) for searching. For every sign on a sheet:
  * the sign is found by its body: the plate edge (a closed loop of 0.72 pt black strokes — a white 600 x 600 board
    with 50 mm corners carries most faces) or, where there is no plate line, the outermost large fill;
  * fills inside the body are kept as drawn, in paint order; fills that are the glyphs of an annotation (they sit on a
    span of the invisible text layer) are dropped, as are dimension lines and all other strokes;
  * a plate drawn only as a line becomes a white fill with a 2 mm black keyline (the library's convention for
    white-edged signs, as in the AS 1743 pack), so the board is visible on a white plan;
  * the real size is the drawn size times the sheet's stated scale; sheets marked not to scale are skipped;
  * the name is the underlined title under the sign; a sign without a title is named from NAMES below.
SDRE gives the signs no codes: the code is the sheet's drawing number and the sign's position on it in reading order
(TFM1-1 = LTA/SDRE14/15/TFM1, first sign). Guide-sign example sheets (not to scale, site-specific legends) are skipped.
Output: <SG>/SVGs/<family>/<NAME>_<CODE>.svg and SVGs/MANIFEST.csv.
  python3 tools/sg_lta.py            build
  python3 tools/sg_lta.py --list     print what is found per sheet, write nothing"""
import os, re, sys, csv, math, collections, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SG = os.path.join(ROOT, "Processing", "Singapore", "National (LTA)")
PDFS = os.path.join(SG, "Original PDFs")
CHAPTERS = [("SDRE14-15_TFM_1-2_March_2025.pdf", "Mandatory Signs"), ("SDRE14-16_TFP_1-6_March_2025.pdf", "Prohibitory Signs"),
            ("SDRE14-17_TFW_1-9_March_2025.pdf", "Warning Signs"), ("SDRE14-18_TFI_1-19_March_2025.pdf", "Informatory Signs"),
            ("SDRE14-19_TFS_1-2_March_2025.pdf", "Supplementary Plates"), ("SDRE17-21_CYC_1-12_March_2025.pdf", "Cycling Signs")]
AREA = pymupdf.Rect(78, 38, 1166, 708)      # the drawing field of the A3 sheet (the title block is below it)
KEYLINE_MM = 2.0
# Sheets (drawing number) that are skipped whole, with the reason written to the manifest.
GUIDE = "directional (guide) sign layouts, not to scale, with example destinations: guide signs are outside the library's scope"
SKIP_SHEETS = {**{f"CYC{i}": "cycling-path layout, marking or construction sheet, not sign faces" for i in (1, 2, 3, 4, 6, 7, 8, 9, 12)},
               "TFI8": GUIDE, "TFI9": GUIDE, "TFI10": GUIDE,
               "TFI18": "gantry height-limit panels: the length varies with the number of lanes (table on the sheet) and the panel carries a placeholder for the height-limit sign"}
# Signs with no title of their own on the sheet, or whose title needs help: (drawing, index) -> name.
REV = " - REVERSE SIDE - "
NAMES = {("TFP3", 1): "RESTRICTION OF MOVEMENT OF VEHICLES WITH 3 OR MORE AXLES", ("TFP3", 4): "RESTRICTION OF MOVEMENT OF VEHICLES WITH 3 OR MORE AXLES - RESTRICTED HOURS PLATE",
         ("TFP3", 3): "PEDESTRIAN CROSSING PROHIBITION" + REV + "PEDESTRIANS USE CROSSING", ("TFP3", 5): "PEDESTRIAN CROSSING PROHIBITION" + REV + "PEDESTRIANS USE UNDERPASS",
         ("TFP3", 7): "PEDESTRIAN CROSSING PROHIBITION" + REV + "PEDESTRIANS USE OVERPASS",
         ("TFP4", 1): "CYCLIST CROSSING PROHIBITION" + REV + "CYCLISTS USE CROSSING", ("TFP4", 2): "CYCLIST CROSSING PROHIBITION" + REV + "CYCLISTS USE UNDERPASS",
         ("TFP4", 4): "CYCLIST CROSSING PROHIBITION" + REV + "CYCLISTS USE OVERPASS", ("TFP4", 3): "FOUR WAITING LANES AHEAD",
         ("TFP6", 2): "PEDESTRIAN AND CYCLISTS CROSSING PROHIBITION" + REV + "PEDESTRIANS AND CYCLISTS USE CROSSING",
         ("TFP6", 4): "CYCLIST CROSSING PROHIBITION - SIGN INDICATING FIFTY METRES 50M - TO LEFT", ("TFP6", 5): "CYCLIST CROSSING PROHIBITION - SIGN INDICATING FIFTY METRES 50M - TO RIGHT",
         ("TFI4", 1): "END OF EXPRESSWAY (TYPE I)", ("TFI4", 2): "END OF EXPRESSWAY 500 M",
         ("TFI11", 1): "LEFT TURN GREEN ARROW AHEAD", ("TFI11", 2): "LEFT TURN ON RED", ("TFI11", 3): "GIVE WAY TO PEDESTRIANS AND MAIN ROAD TRAFFIC",
         ("TFI12", 1): "BEWARE OF TURNING VEHICLES", ("TFI12", 2): "WATCH OUT FOR TRAFFIC FROM SIDE ROAD", ("TFI12", 3): "MOTORCYCLES AND SLOWER TRAFFIC KEEP LEFT",
         ("TFI13", 1): "SPEED CAMERA AHEAD", ("TFI14", 2): "RIGHT TURN LANE AHEAD", ("TFI14", 3): "RIGHT TURN LANES AHEAD",
         ("TFI19", 3): "340mm X 990mm OBJECT MARKER - STRIPES FALLING TO RIGHT", ("TFI19", 4): "340mm X 990mm OBJECT MARKER - STRIPES FALLING TO LEFT",
         ("TFS1", 1): "SCHOOL ZONE FOR 400M", ("TFS1", 3): "DIRECTIONAL ARROW - RIGHT", ("TFS1", 5): "DIRECTIONAL ARROW - BOTH WAYS",
         ("TFS1", 4): "VEHICLES NOT EXCEEDING 2500 KG IN UNLADEN WEIGHT", ("TFS1", 7): "EXCEPT AUTHORISED VEHICLES",
         ("TFS2", 1): "EXCEPT AMBULANCE AND POLICE VEHICLES", ("TFS2", 2): "WAY OUT - RIGHT", ("TFS2", 3): "WAY OUT - AHEAD", ("TFS2", 4): "EXCEPT LOADING UNLOADING",
         ("CYC10", 3): "STAY ON TRACK - CYCLISTS ON LEFT", ("CYC10", 4): "STAY ON TRACK - PEDESTRIANS ON LEFT",
         ("CYC11", 1): "NO RIDING PLATE - AHEAD", ("CYC11", 3): "NO RIDING", ("CYC11", 4): "NO RIDING PLATE - RIGHT", ("CYC11", 5): "NO RIDING PLATE - LEFT"}
# Signs the sheet draws out of scale: the stated overall width is applied and the drawing's own proportions kept.
WIDTHS = {("TFI1", 1): 1029, ("TFI1", 2): 1368}
# Scale where the sheet's own statement cannot be used as found: (drawing, index) -> (scale, note for the manifest).
SCALES = {("TFI13", 1): (10, "title block says 1:100, the sheet's figures (1107 x 1888) give 1:10"),
          ("TFI14", 2): (10, "'SCALE 1:10' is under the title shared with the sign beside it"), ("TFI14", 3): (10, "'SCALE 1:10' is under the title shared with the sign beside it"),
          ("TFI19", 3): (10, "'SCALE 1:10' is under the title shared with the sign beside it"), ("TFI19", 4): (10, "'SCALE 1:10' is under the title shared with the sign beside it")}
NUMERIC = re.compile(r"(R\s?)?[\d.\s\u00b0()xX=,]+(mm|m)?")
# Drafting notes written on a sign face (colour call-outs, logo placeholders): their glyphs are not part of the sign.
NOTE_WORDS = {"BLACK", "(BLACK)", "OUTLINE", "2mm WIDE", "2mm WIDE OUTLINE", "W", "H", "I", "TE", "NPP LOGO", "LOGO", "P.A."}
# Bodies that are not built: (drawing, index) -> reason.
SITE = "site-specific example (a named place, with a placeholder where a logo goes)"
NOT_SIGNS = {("TFP6", 6): "assembly view of the sign above on its post: the arrow plate is TFS1-3 / TFS1-5", ("TFP6", 7): "assembly view of the sign above on its post: the arrow plate is TFS1-3 / TFS1-5",
             ("TFI7", 3): "site-specific example (a named road)", ("TFI7", 4): SITE, ("TFI7", 7): SITE,
             ("TFI15", 2): "pedestrian push-button instruction plate carrying the LTA logo and a telephone number: not a traffic sign face",
             ("TFI15", 3): "pedestrian push-button instruction plate carrying the LTA logo and a telephone number: not a traffic sign face"}
# Sheets where only the bodies with these titles are signs (the rest is a layout).
ONLY = {"CYC5": {"BICYCLE CROSSING SIGN"}}

def rnd(p): return (round(p[0], 1), round(p[1], 1))

def stroke_loops(strokes):
    """Closed loops among the plate-weight black strokes: segments chained end to end, every joint of degree 2."""
    segs = []
    for d in strokes:
        for it in d["items"]:
            if it[0] == "l": segs.append((rnd(it[1]), rnd(it[2]), it))
            elif it[0] == "c": segs.append((rnd(it[1]), rnd(it[4]), it))
            elif it[0] == "re":
                r = it[1]; c = [pymupdf.Point(r.x0, r.y0), pymupdf.Point(r.x1, r.y0), pymupdf.Point(r.x1, r.y1), pymupdf.Point(r.x0, r.y1)]
                for i in range(4): segs.append((rnd(c[i]), rnd(c[(i + 1) % 4]), ("l", c[i], c[(i + 1) % 4])))
    nodes = collections.defaultdict(list)
    def key(p):   # snap to an existing node within 0.25 pt
        for dx in (0, -0.1, 0.1, -0.2, 0.2):
            for dy in (0, -0.1, 0.1, -0.2, 0.2):
                k = (round(p[0] + dx, 1), round(p[1] + dy, 1))
                if k in nodes: return k
        return p
    ends = []; drawn = set()
    for i, (a, b, it) in enumerate(segs):
        if a == b: ends.append(None); continue
        ka = key(a); kb = key(b)
        if (ka, kb, it[0]) in drawn or (kb, ka, it[0]) in drawn: ends.append(None); continue     # the same line plotted twice
        drawn.add((ka, kb, it[0])); nodes[ka].append(i); nodes[kb].append(i); ends.append((ka, kb))
    used = set(); loops = []
    for i in range(len(segs)):
        if i in used or ends[i] is None: continue
        chain = [(i, False)]; used.add(i); start, cur = ends[i]; ok = True
        while cur != start:
            nxt = [j for j in nodes[cur] if j not in used]
            if len(nodes[cur]) != 2 or len(nxt) != 1: ok = False; break
            j = nxt[0]; used.add(j); a, b = ends[j]
            if a == cur: chain.append((j, False)); cur = b
            else: chain.append((j, True)); cur = a
        if not ok or len(chain) < 3: continue
        items = []
        for j, rev in chain:
            it = segs[j][2]
            if not rev: items.append(it)
            elif it[0] == "l": items.append(("l", it[2], it[1]))
            else: items.append(("c", it[4], it[3], it[2], it[1]))
        for n in range(len(items)):     # make the joints exact so the outline is one closed subpath
            it = items[n]; prev = items[n - 1]; start = prev[2] if prev[0] == "l" else prev[4]
            items[n] = ("l", start, it[2]) if it[0] == "l" else ("c", start, it[2], it[3], it[4])
        pts = X.item_points(items)
        loops.append({"items": items, "rect": pymupdf.Rect(min(x for x, _ in pts), min(y for _, y in pts), max(x for x, _ in pts), max(y for _, y in pts))})
    return loops

def scaled_items(items, r, t):
    """The loop moved in by t on every side (exact for the straight sides of a plate; corners follow)."""
    cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2; sx = (r.width - 2 * t) / r.width; sy = (r.height - 2 * t) / r.height
    def P(p): return pymupdf.Point(cx + (p[0] - cx) * sx, cy + (p[1] - cy) * sy)
    return [(it[0],) + tuple(P(p) for p in it[1:5]) if it[0] == "c" else ("l", P(it[1]), P(it[2])) for it in items]

def trace_hatch(strokes, pr, cache_dir):
    """A symbol the sheet draws as a hatch of thousands of hairlines (no fill): the hairlines are painted at 16 px/pt,
    opened (so lone dimension lines vanish and the hatched solid stays) and traced with potrace back to outlines."""
    import subprocess, tempfile
    from PIL import Image, ImageDraw, ImageFilter
    Z = 16; W, H = int(pr.width * Z) + 2, int(pr.height * Z) + 2
    im = Image.new("L", (W, H), 255); dr = ImageDraw.Draw(im)
    for d in strokes:
        for it in d["items"]:
            if it[0] == "l": pts = [it[1], it[2]]
            elif it[0] == "c": pts = [it[1], it[2], it[3], it[4]]
            else: continue
            dr.line([((q.x - pr.x0) * Z, (q.y - pr.y0) * Z) for q in pts], fill=0, width=8)
    im = im.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.MinFilter(13))     # white grows 6 px, then black grows back
    tmp = tempfile.mkdtemp(dir=cache_dir); pbm = os.path.join(tmp, "h.pbm"); svg = os.path.join(tmp, "h.svg")
    im.point(lambda v: 0 if v < 128 else 255).convert("1").save(pbm)
    subprocess.run(["/opt/homebrew/bin/potrace", "-b", "svg", "-t", "40", "-a", "1.0", "-O", "0.4", "-o", svg, pbm], check=True)
    items = []
    for d in re.findall(r'<path d="([^"]+)"', open(svg).read()):
        toks = re.findall(r"[MmLlCcZz]|-?\d+\.?\d*", d); i = 0; cur = (0.0, 0.0); cmd = None
        def P(x, y): return pymupdf.Point(pr.x0 + (x / 10) / Z, pr.y0 + (H - y / 10) / Z)      # potrace: tenths of a pixel, y up
        while i < len(toks):
            if toks[i].isalpha(): cmd = toks[i]; i += 1
            if cmd in "zZ": continue
            if cmd in "Mm":
                x, y = float(toks[i]), float(toks[i + 1]); i += 2
                cur = (x, y) if cmd == "M" else (cur[0] + x, cur[1] + y); cmd = "l" if cmd == "m" else "L"
            elif cmd in "lL":
                x, y = float(toks[i]), float(toks[i + 1]); i += 2
                nxt = (x, y) if cmd == "L" else (cur[0] + x, cur[1] + y); items.append(("l", P(*cur), P(*nxt))); cur = nxt
            elif cmd in "cC":
                v = [float(t) for t in toks[i:i + 6]]; i += 6
                pts = [(v[0], v[1]), (v[2], v[3]), (v[4], v[5])] if cmd == "C" else [(cur[0] + v[0], cur[1] + v[1]), (cur[0] + v[2], cur[1] + v[3]), (cur[0] + v[4], cur[1] + v[5])]
                items.append(("c", P(*cur), P(*pts[0]), P(*pts[1]), P(*pts[2]))); cur = pts[2]
    return items

def sheet_info(page):
    """Drawing number, scale and title from the title block's text layer."""
    t = page.get_text("text", clip=pymupdf.Rect(760, 708, 1170, 842))
    m = re.search(r"LTA/SDRE\d+/\d+/(\w+)", t); s = re.search(r"\b1\s*:\s*(\d+)\b", t)
    return (m.group(1) if m else ""), (int(s.group(1)) if s else None), ("N.T.S" if re.search(r"N\.?T\.?S|NOT TO SCALE", t) else "")

def page_signs(page):
    drawings = page.get_drawings()
    spans = []     # the invisible annotation layer
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip(): spans.append({"rect": pymupdf.Rect(s["bbox"]), "text": s["text"].strip(), "size": s["size"], "dir": l["dir"]})
    def is_annotation(r):
        """A glyph of a dimension figure or drafting note: it sits on a text-layer span that is a number or a known note.
        Legends set in a live font (the cycling sheets) are in the text layer too, and are words: those are kept."""
        return any(sp["rect"].x0 - 1 <= r.x0 and sp["rect"].y0 - 1 <= r.y0 and sp["rect"].x1 + 1 >= r.x1 and sp["rect"].y1 + 1 >= r.y1
                   and (NUMERIC.fullmatch(sp["text"]) or sp["text"] in NOTE_WORDS or not AREA_SIGNS(sp)) for sp in spans)
    fills = []; plate_strokes = collections.defaultdict(list)
    thin_strokes = [d for d in drawings if d.get("color") is not None and X.colour_name(d["color"]) == "BLACK" and (d.get("width") or 0) < 0.5 and d["rect"].width < 40 and d["rect"].height < 40]
    big = [d["rect"] for d in drawings if AREA.contains(d["rect"]) and d["rect"].width > 60 and d["rect"].height > 20 and (d.get("fill") is not None)]
    def AREA_SIGNS(sp):   # the span lies on a large fill (a sign face), so it can be a legend
        return any(b.contains(sp["rect"]) for b in big)
    for d in drawings:
        r = d["rect"]
        if not AREA.contains(r): continue
        if d.get("fill") is not None:
            fills.append({"rect": r, "fill": d["fill"], "items": d["items"], "area": r.get_area(), "even_odd": d.get("even_odd"), "seq": d.get("seqno", 0),
                          "note": X.colour_name(d["fill"]) == "BLACK" and r.width < 30 and r.height < 30 and is_annotation(r)})
        col = d.get("color")
        if col is not None and X.colour_name(col) == "BLACK" and 0.3 <= (d.get("width") or 0) <= 1.2 and d.get("dashes") in (None, "[] 0"):
            plate_strokes[round(d["width"], 2)].append(d)
    # revision clouds are loops of many small arcs; a plate edge has a handful of segments
    loops = [l for w in plate_strokes for l in stroke_loops(plate_strokes[w]) if l["rect"].width > 40 and l["rect"].height > 25 and len(l["items"]) <= 40]
    bodies = [{"rect": l["rect"], "loop": l} for l in loops]
    bodies += [{"rect": f["rect"], "fill": f} for f in fills if not f["note"] and max(f["rect"].width, f["rect"].height) > 60 and min(f["rect"].width, f["rect"].height) > 20]
    # cluster bodies that overlap: one sign each
    clusters = []
    for b in sorted(bodies, key=lambda b: -b["rect"].get_area()):
        for c in clusters:
            i = pymupdf.Rect(c["rect"]); i.intersect(b["rect"])
            if not i.is_empty and i.get_area() > 0.5 * b["rect"].get_area(): c["members"].append(b); break
        else: clusters.append({"rect": pymupdf.Rect(b["rect"]), "members": [b]})
    signs = []
    for c in clusters:
        outer = c["members"][0]; pr = c["rect"]
        inside = [f for f in fills if not f["note"] and pr.x0 - 0.6 <= f["rect"].x0 and pr.y0 - 0.6 <= f["rect"].y0 and pr.x1 + 0.6 >= f["rect"].x1 and pr.y1 + 0.6 >= f["rect"].y1]
        if not inside: continue
        # a black line loop inside the body that is not just the edge of a fill is a printed outline (reverse-side messages)
        import uk_eps
        edges = [uk_eps.sub_rect(q) for f in inside if len(f["items"]) < 400 for q in uk_eps.split_subpaths(f["items"])] + [f["rect"] for f in inside]
        def same(a, b): return abs(a.x0 - b.x0) < 0.8 and abs(a.y0 - b.y0) < 0.8 and abs(a.x1 - b.x1) < 0.8 and abs(a.y1 - b.y1) < 0.8
        inner = [m["loop"] for m in c["members"][1:] if m.get("loop") and not any(same(e, m["rect"]) for e in edges)]
        backing = None
        if not outer.get("loop"):   # no plate line: the body is a fill; its outline, filled white, backs any holes cut in it
            import uk_eps
            sub = max(uk_eps.split_subpaths(outer["fill"]["items"]), key=lambda q: uk_eps.sub_rect(q).get_area())
            backing = {"items": sub, "rect": uk_eps.sub_rect(sub), "white": X.colour_name(outer["fill"]["fill"]) == "WHITE"}
        fl = sorted(inside, key=lambda f: f["seq"]); traced = False
        thin = [d for d in thin_strokes if pr.contains(d["rect"])]
        if len(thin) > 1000:
            cache = os.environ.get("SG_CACHE", os.path.join(SG, ".cache")); os.makedirs(cache, exist_ok=True)
            items = trace_hatch(thin, pr, cache)
            if items: fl.append({"rect": pr, "fill": (0, 0, 0), "items": items, "even_odd": True}); traced = True
        signs.append({"panel": pr, "fills": fl, "plate": outer.get("loop"), "backing": backing, "inner": inner, "glyphs": [], "traced": traced})
    # titles: annotation spans of title size under a sign
    titles = [s for s in spans if 8.6 <= s["size"] <= 10.5 and abs(s["dir"][0] - 1) < 1e-3 and AREA.contains(s["rect"]) and len(s["text"]) > 2]
    for s in signs:
        pr = s["panel"]; cx = (pr.x0 + pr.x1) / 2
        under = sorted([t for t in titles if t["rect"].y0 > pr.y1 - 2 and t["rect"].y0 < pr.y1 + 95 and t["rect"].x0 - 25 < cx < t["rect"].x1 + 25], key=lambda t: t["rect"].y0)
        lines = []
        for t in under:
            if lines and t["rect"].y0 - lines[-1]["rect"].y1 > 6: break
            lines.append(t)
        s["title"] = " ".join(t["text"] for t in lines)
        # "SCALE 1:10" under the title, on sheets whose title block says AS SHOWN
        sc = sorted([t for t in spans if re.match(r"SCALE\s*1\s*:\s*\d+", t["text"]) and pr.y1 - 2 < t["rect"].y0 < pr.y1 + 120 and t["rect"].x0 - 60 < cx < t["rect"].x1 + 60], key=lambda t: t["rect"].y0)
        s["scale"] = int(re.search(r":\s*(\d+)", sc[0]["text"]).group(1)) if sc else None
        # dimension figures drawn round the sign (for checking the scaled size against the sheet's own numbers)
        near = pymupdf.Rect(pr.x0 - 75, pr.y0 - 75, pr.x1 + 75, pr.y1 + 75)
        s["figures"] = sorted({float(t["text"]) for t in spans if re.fullmatch(r"\d{2,5}(\.\d+)?", t["text"]) and near.contains(t["rect"])})
    # reading order: rows by the panel centre, then left to right
    signs.sort(key=lambda s: (s["panel"].y0 + s["panel"].y1) / 2)
    rows = []
    for s in signs:
        cy = (s["panel"].y0 + s["panel"].y1) / 2
        if rows and cy - rows[-1][0] < 90: rows[-1][1].append(s)
        else: rows.append([cy, [s]])
    return [s for _, row in rows for s in sorted(row, key=lambda s: s["panel"].x0)]

def build_fills(sign, k):
    """Paint list for the SVG: the plate (white, with its keyline) first, then the fills as drawn."""
    out = []
    if sign["plate"]:
        lp = sign["plate"]; t = KEYLINE_MM / k
        out.append({"fill": (1, 1, 1), "items": lp["items"]})
        out.append({"fill": (0, 0, 0), "items": lp["items"] + scaled_items(lp["items"], lp["rect"], t), "even_odd": True})
    if sign["backing"]:
        out.append({"fill": (1, 1, 1), "items": sign["backing"]["items"]})
    out += sign["fills"]
    if sign["backing"] and sign["backing"]["white"]:   # a white-edged body drawn as a fill gets the same keyline
        lp = sign["backing"]; out.append({"fill": (0, 0, 0), "items": lp["items"] + scaled_items(lp["items"], lp["rect"], KEYLINE_MM / k), "even_odd": True})
    for lp in sign["inner"]:
        t = KEYLINE_MM / k; out.append({"fill": (0, 0, 0), "items": lp["items"] + scaled_items(lp["items"], lp["rect"], t), "even_odd": True})
    return out

def stated(v, figures):
    return next((f for f in figures if abs(f - v) <= max(1.0, 0.006 * v)), None)

def main(list_only=False, draft=False):
    out = os.path.join(SG, "SVGs"); manifest = []; n = 0; fams = collections.Counter()
    for pdf, family in CHAPTERS:
        doc = pymupdf.open(os.path.join(PDFS, pdf))
        for pno in range(len(doc)):
            page = doc[pno]; drawing, sheet_scale, nts = sheet_info(page); src = f"{pdf} p{pno + 1}"
            if not drawing: continue      # chapter contents page
            if drawing in SKIP_SHEETS:
                manifest.append([drawing, "", family, "", "", src, "sheet skipped: " + SKIP_SHEETS[drawing]]); continue
            signs = page_signs(page)
            if list_only: print(f"== {src} {drawing} scale 1:{sheet_scale} {nts} — {len(signs)} bodies")
            for i, s in enumerate(signs, 1):
                code = f"{drawing}-{i}"; pr = s["panel"]; scale = SCALES.get((drawing, i), (sheet_scale or s["scale"], ""))[0]
                title = NAMES.get((drawing, i), s["title"])
                if drawing in ONLY and s["title"] not in ONLY[drawing]: continue
                if (drawing, i) in NOT_SIGNS:
                    manifest.append([code, title.title(), family, "", "", src, "not built: " + NOT_SIGNS[(drawing, i)]]); continue
                k = (scale or 0) * 25.4 / 72      # mm of sign per point of sheet
                if (drawing, i) in WIDTHS: k = WIDTHS[(drawing, i)] / pr.width
                W, H = pr.width * k, pr.height * k
                fw, fh = stated(W, s["figures"]), stated(H, s["figures"])
                if list_only:
                    print(f"   {code:9s} 1:{scale} {W:5.0f}x{H:<5.0f} stated {fw}x{fh} fills {len(s['fills']):3d} {'plate' if s['plate'] else 'fill '} inner {len(s['inner'])} title {title!r}")
                    continue
                if not scale:
                    manifest.append([code, title.title(), family, "", "", src, "not built: no scale stated for this drawing"]); continue
                if not title:
                    if not draft: manifest.append([code, "", family, "", "", src, "not built: no title on the sheet and none assigned"]); continue
                    title = "UNTITLED"
                sign = {"panel": pr, "scale": k / 25.4, "fills": build_fills(s, k), "glyphs": []}
                svg, W, H = X.write_svg(sign, family)
                name = re.sub(r"[^A-Z0-9]+", "_", title.upper()).strip("_")[:70]
                fn = f"{name}_{code}.svg"
                folder = os.path.join(out, family); os.makedirs(folder, exist_ok=True)
                open(os.path.join(folder, fn), "w").write(svg); n += 1; fams[family] += 1
                notes = [f"drawn at 1:{scale}"]
                if (drawing, i) in WIDTHS: notes = [f"marked 1:{scale} but not drawn to it: width {WIDTHS[(drawing, i)]} from the sheet's figure, height follows the drawing (nominal)"]
                elif fw and fh: notes.append(f"{fw:g} x {fh:g} dimensioned on the sheet")
                elif fw or fh: notes.append(f"{'width' if fw else 'height'} {(fw or fh):g} dimensioned on the sheet, the other side from the scale")
                else: notes.append("overall size not dimensioned on the sheet: from the scale")
                if s["plate"]: notes.append("plate edge drawn as a line: white fill with a 2 mm keyline")
                elif s["backing"]["white"]: notes.append("white edge: 2 mm keyline added")
                if s["traced"]: notes.append("symbol drawn on the sheet as a hatch of hairlines, not a fill: traced from them (potrace)")
                if s["inner"]: notes.append(f"{len(s['inner'])} black line outline(s) drawn 2 mm wide")
                if (drawing, i) in SCALES: notes.append(SCALES[(drawing, i)][1])
                if (drawing, i) in NAMES: notes.append("name assigned (the sheet's title is shared, or the sign has none)")
                manifest.append([code, title.title(), family, f"{family}/{fn}", f"{W:.0f}x{H:.0f} mm", src, "; ".join(notes)])
    if list_only: return
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "source", "notes"]); w.writerows(manifest)
    print(f"{n} SVGs written; {sum(1 for m in manifest if not m[3])} rows not built; families: {dict(fams)}")

if __name__ == "__main__":
    main(list_only="--list" in sys.argv, draft="--draft" in sys.argv)
