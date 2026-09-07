#!/usr/bin/env python3
"""uk_extract.py — DfT TSRGD 2016 working drawings (Crown copyright, Open Government Licence) into
Processing/United Kingdom/National (TSRGD 2016)/SVGs/<family>/<NAME>_<DIAGRAM>.svg with MANIFEST.csv.

The drawings are pure black line work with every legend outlined and no text objects: the sign's colours and sizes
live in the outlined NOTES, so the sheet is OCR'd (tesseract) for 'COLOURS : Background - RED  Legend & Border - WHITE'
and the size figures ('750 (900) (1200)'). The line work is polygonised (Shapely): the closed loops become faces, open
dimension lines drop out as dangles, and faces are coloured by nesting depth — border ring, background, legend,
background (counters) … — with the note's colours.  python3 tools/uk_extract.py [limit]  (UK_FILES=diag1,diag2 to pick)"""
import os, re, sys, csv, math, subprocess, collections, tempfile, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UK = os.path.join(ROOT, "Processing", "United Kingdom", "National (TSRGD 2016)")
PALETTE = {"WHITE": "#ffffff", "BLACK": "#000000", "RED": "#cc0000", "BLUE": "#0c3d8f", "GREEN": "#006c3b", "YELLOW": "#ffd400", "BROWN": "#6b3a1e", "GREY": "#8a8d8f", "ORANGE": "#f7921d"}
COLOUR = re.compile(r"WHITE|BLACK|RED|BLUE|GREEN|YELLOW|BROWN|GREY|GRAY|ORANGE", re.I)
FAMILY = {"2": "Warning Signs", "3": "Regulatory Signs", "4": "Regulatory Signs", "5": "Parking Signs", "6": "Regulatory Signs", "7": "Parking Signs", "8": "Regulatory Signs",
          "9": "Directional Signs", "10": "Directional Signs", "11": "Information Signs", "12": "Directional Signs", "13": "Temporary Signs", "14": "Signal and Crossing Signs", "15": "Pedestrian and Cycle Signs", "16": "Variable Message Signs"}

def hex2rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))

def ocr(page, clip=None, psm="3"):
    pix = page.get_pixmap(dpi=220, clip=clip)
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "p.png"); pix.save(png)
        r = subprocess.run(["tesseract", png, "stdout", "--psm", psm], capture_output=True, text=True)
    return r.stdout

def ocr_parts(page):
    """Whole sheet, the notes block (right), the title block (bottom)."""
    W, H = page.rect.width, page.rect.height
    return ocr(page), ocr(page, pymupdf.Rect(0.55 * W, 0.04 * H, W, 0.75 * H), "6"), ocr(page, pymupdf.Rect(0.12 * W, 0.86 * H, 0.62 * W, H), "6")

def parse_notes(text):
    """Colours by role and the size figures from the OCR'd sheet."""
    u = text.upper().replace("—", "-").replace("–", "-")
    colours = {}
    m = re.search(r"COLOURS?\s*[:\-]?\s*(.{0,300})", u, re.S)
    if m:
        seg = m.group(1).split("BEFORE USING")[0]
        for role_m in re.finditer(r"(BACKGROUND|LEGEND|BORDER|SYMBOL|ARROW|PANEL|LETTERS?|BAR|CHEVRON|STRIPE|DISC|CIRCLE)[^A-Z]{0,4}(?:&|AND)?[^A-Z]{0,4}(BACKGROUND|LEGEND|BORDER|SYMBOL|ARROW|PANEL|LETTERS?|BAR|CHEVRON|STRIPE|DISC|CIRCLE)?[^A-Z]{0,12}(" + COLOUR.pattern + r")", seg):
            col = role_m.group(3).upper().replace("GRAY", "GREY")
            for role in (role_m.group(1), role_m.group(2)):
                if role: colours.setdefault({"LETTER": "LEGEND", "LETTERS": "LEGEND", "PANEL": "BACKGROUND"}.get(role, role), col)
    m2 = re.search(r"\b(\d{3,4})\s*(?:\(\s*\d{3,4}\s*\)\s*)+", u)     # '750 (900) (1200)': the drawn size and its alternatives
    sizes = ([int(m2.group(1))] + [int(x) for x in re.findall(r"\((\d{3,4})\)", m2.group(0))]) if m2 else []
    sizes += [int(x) for x in re.findall(r"\b(\d{3,4})\b", u) if 100 <= int(x) <= 5000 and int(x) not in sizes]
    return colours, sizes

def parse_title(block):
    """'Regulatory Sign' / 'STOP SIGN' from the title-block OCR."""
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    kind = ""; title = ""
    m = re.search(r"(?:sport|port|Transport)\s*[,.=]*\s*([A-Z][A-Z0-9 ,'()/&.\-]{2,70}?)(?=\s+(?:[A-Za-z]{1,2}\s*[:;]|\d|BY\b)|\n|$)", block)
    if m: title = m.group(1).strip(" ,.-")
    for l in lines:
        m = re.search(r"(WARNING|REGULATORY|DIRECTIONAL|INFORMATION|PARKING|TEMPORARY|INFORMATORY|SUPPLEMENTARY|DIRECTION)\s+SIGN", l.upper())
        if m and not kind: kind = m.group(1).title() + " Signs"; continue
        if re.fullmatch(r"[A-Z0-9][A-Z0-9 ,'()/&.\-]{3,80}", l) and l.upper() == l and not re.search(r"TITLE|ISSUE|DATE|DRAWN|DIMENSIONS|DRAWING|MILLIMETRES|TRANSPORT|DEPARTMENT|APPROVED", l):
            if not title: title = l
    return title, kind

def linework(page):
    """Every stroked segment in upright page coordinates (curves flattened). Curves the drafting plotter emitted as
    strings of dots (each dot its own tiny path) are chained: every dot is joined to its nearest dots within 3.2 pt."""
    M = page.rotation_matrix; segs = []; dots = []; ends = []
    def P(q): r = pymupdf.Point(q) * M; return (r.x, r.y)
    for d in page.get_drawings():
        if d.get("fill") is not None: continue
        r = d["rect"]
        if r.width < 1.6 and r.height < 1.6 and d["items"]:   # a dot
            c = P(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)); dots.append(c); continue
        its = [it for it in d["items"] if it[0] in ("l", "c")]
        if its and not d.get("closePath"): ends += [P(its[0][1]), P(its[-1][2] if its[-1][0] == "l" else its[-1][4])]   # open path ends: dot chains may join here
        for it in d["items"]:
            if it[0] == "l": segs.append((P(it[1]), P(it[2])))
            elif it[0] == "c":
                p0, p1, p2, p3 = it[1], it[2], it[3], it[4]; prev = P(p0)
                for k in range(1, 9):
                    t = k / 8; u = 1 - t
                    q = (u*u*u*p0.x + 3*u*u*t*p1.x + 3*u*t*t*p2.x + t*t*t*p3.x, u*u*u*p0.y + 3*u*u*t*p1.y + 3*u*t*t*p2.y + t*t*t*p3.y)
                    cur = P(q); segs.append((prev, cur)); prev = cur
            elif it[0] == "re":
                rr = it[1]; c = [P((rr.x0, rr.y0)), P((rr.x1, rr.y0)), P((rr.x1, rr.y1)), P((rr.x0, rr.y1))]
                segs += [(c[i], c[(i + 1) % 4]) for i in range(4)]
            elif it[0] == "qu":
                q = it[1]; c = [P(q.ul), P(q.ur), P(q.lr), P(q.ll)]; segs += [(c[i], c[(i + 1) % 4]) for i in range(4)]
    if dots:   # chain the dots: each to its two nearest nodes (dots or open path ends) within reach; a grid keeps it linear
        nodes = dots + ends; nd = len(dots); grid = {}
        for i, (x, y) in enumerate(nodes): grid.setdefault((int(x // 4), int(y // 4)), []).append(i)
        for i in range(len(nodes)):
            x, y = nodes[i]; near = []
            for gx in range(int(x // 4) - 1, int(x // 4) + 2):
                for gy in range(int(y // 4) - 1, int(y // 4) + 2):
                    for j in grid.get((gx, gy), []):
                        if j != i:
                            dd = math.hypot(nodes[j][0] - x, nodes[j][1] - y)
                            if 0.05 < dd < 3.2: near.append((dd, j))
            for dd, j in sorted(near)[:2 if i < nd else 1]: segs.append((nodes[i], nodes[j]))   # a dot joins two neighbours, an open path end joins one
    return segs

def faces_from(segs, page_rect):
    """Enclosed regions of the line work: buffer every segment a hair and union them; the holes of that union are the
    faces (this closes the sub-point gaps between outline segments; open dimension lines enclose nothing)."""
    from shapely.geometry import LineString, Polygon
    from shapely.ops import unary_union
    lines = [LineString([a, b]).buffer(0.45, cap_style=2) for a, b in segs if math.hypot(a[0] - b[0], a[1] - b[1]) > 0.05]
    if not lines: return []
    net = unary_union(lines)
    geoms = list(net.geoms) if hasattr(net, "geoms") else [net]
    A = page_rect.width * page_rect.height; polys = []
    for g in geoms:
        for hole in g.interiors:
            p = Polygon(hole).buffer(0.45, join_style=2)      # give the face back the half line width
            parts = list(p.geoms) if hasattr(p, "geoms") else [p]
            for q in parts:
                if 2 < q.area < 0.5 * A: polys.append(q)
    return polys

def pick_sign(polys, page_rect):
    """The drawing: the touching group of faces holding the largest face that is not sheet furniture."""
    if not polys: return []
    polys = sorted(polys, key=lambda p: -p.area)
    W, H = page_rect.width, page_rect.height
    def furniture(p):
        b = p.bounds; w, h = b[2] - b[0], b[3] - b[1]
        return (w > 0.9 * W) or (h > 0.9 * H) or (b[1] > 0.82 * H and w > 0.25 * W)   # frame / title block strip
    cands = [p for p in polys if not furniture(p)]
    if not cands: return []
    seed = cands[0]; group = [seed]; frontier = [seed]; rest = [p for p in cands if p is not seed]
    while frontier:
        f = frontier.pop(); keep = []
        for p in rest:
            if p.touches(f) or p.intersects(f) or f.contains(p) or p.distance(f) < 0.6: group.append(p); frontier.append(p)
            else: keep.append(p)
        rest = keep
    return group

def Polygon_ext(p):
    from shapely.geometry import Polygon
    return Polygon(p.exterior)

def face_depths(group):
    """Nesting depth by peeling: the faces that touch the outside of the whole drawing are depth 0 (the border ring,
    even when dimension lines cut it into pieces); remove them and the faces now on the outside are depth 1 (the
    background); then the legend (2), counters (3) …"""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    rem = list(group); depth = {}; d = 0
    while rem and d < 12:
        u = unary_union([Polygon(p.exterior) for p in rem]); parts = list(u.geoms) if hasattr(u, "geoms") else [u]
        outline = unary_union([Polygon(q.exterior).boundary for q in parts])
        level = [p for p in rem if p.exterior.intersection(outline).length > 0.5 or p.exterior.distance(outline) < 0.3]
        if not level: level = rem[:]
        for p in level: depth[id(p)] = d
        rem = [p for p in rem if p not in level]; d += 1
    return depth

def colour_faces(group, colours):
    """Nesting depth → role: 0 border (if stated) then background, legend, background …"""
    depth = face_depths(group); order = sorted(group, key=lambda p: -Polygon_ext(p).area)
    bg = colours.get("BACKGROUND", "WHITE"); legend = next((colours[k] for k in ("LEGEND", "SYMBOL", "BAR", "ARROW", "LETTERS", "CHEVRON", "STRIPE") if k in colours), "BLACK"); border = colours.get("BORDER")
    ring = [bg, legend]
    roles = ([border] if border else []) + ring * 6
    out = []
    for p in order:
        d = depth[id(p)]; col = roles[min(d, len(roles) - 1)]
        out.append((p, col))
    return out

def poly_items(p):
    items = []
    for ring in [p.exterior] + list(p.interiors):
        cs = list(ring.coords)
        for i in range(len(cs) - 1): items.append(("l", (cs[i][0], cs[i][1]), (cs[i + 1][0], cs[i + 1][1])))
    return items

def extract(pdf):
    page = pymupdf.open(pdf)[0]; rect = (page.rect * page.rotation_matrix).normalize() if False else pymupdf.Rect(0, 0, page.rect.width, page.rect.height)
    text, notes, tblock = ocr_parts(page); colours, _ = parse_notes(notes if "COLOUR" in notes.upper() else text); title, kind = parse_title(tblock)
    colours2, sizes = parse_notes(text); colours = colours or colours2
    dn = re.search(r"P\s*(\d{3,4})", text.upper()); sizes = [s for s in sizes if not (dn and s == int(dn.group(1)))]
    segs = linework(page); polys = faces_from(segs, rect); group = pick_sign(polys, rect)
    if not group: return None, colours, sizes, title, kind, text
    depth = face_depths(group)
    def is_tile(p):   # an axis-aligned rectangle inside the background that only frames other faces (Transport alphabet tile outlines)
        b = p.bounds; rect_like = abs(p.area - (b[2] - b[0]) * (b[3] - b[1])) < 0.03 * p.area
        return depth[id(p)] >= 2 and rect_like and any(q is not p and p.contains(q.representative_point()) and 0.02 * p.area < q.area < p.area for q in group)
    group = [p for p in group if not is_tile(p)]
    coloured = colour_faces(group, colours)
    xs = [x for p, _ in coloured for x in p.bounds[0::2]]; ys = [y for p, _ in coloured for y in p.bounds[1::2]]
    pr = pymupdf.Rect(min(xs), min(ys), max(xs), max(ys))
    fills = [{"rect": pymupdf.Rect(*p.bounds), "fill": hex2rgb(PALETTE[c]), "items": poly_items(p), "area": p.area, "even_odd": True} for p, c in coloured]
    size = sizes[0] if sizes else None
    scale = (size / max(pr.width, pr.height)) / 25.4 if size else 10 / 72
    sign = {"panel": pr, "fills": fills, "glyphs": [], "scale": scale, "bg": colours.get("BACKGROUND", "WHITE")}
    note = []
    note.append(f"colours from the sheet's COLOURS note: {', '.join(f'{k.lower()} {v.lower()}' for k, v in colours.items())}" if colours else "no COLOURS note read (OCR) — white/black assumed — check")
    note.append(f"size {size} mm from the sheet's first size figure (others: {', '.join(str(s) for s in sizes[1:6])})" if size else "no size figure read; drawn at 1:10 — check")
    note.append("faces coloured by nesting depth — check")
    sign["note"] = "; ".join(note)
    return sign, colours, sizes, title, kind, text

def main(limit=None):
    out = os.path.join(UK, "SVGs"); rows = []; seen = {}
    reg = [r for r in csv.DictReader(open(os.path.join(UK, "REGISTER.csv"))) if r["local"]]
    only = os.environ.get("UK_FILES")
    if only: reg = [r for r in reg if r["diagram"] in only.split(",")]
    if limit: reg = reg[:limit]
    for i, r in enumerate(reg):
        pdf = os.path.join(UK, r["local"]); diag = r["diagram"]; code = re.sub(r"^p", "", diag).replace("x", ".").upper()
        try: sign, colours, sizes, title, kind = extract(pdf)[:5]
        except Exception as ex:
            rows.append([code, r["title"], FAMILY.get(str(int(r["schedule"])), "Other"), "", "", f"extraction failed: {str(ex)[:100]}", r["local"]]); print("  !!", code, str(ex)[:80], flush=True); continue
        fam = kind or FAMILY.get(str(int(r["schedule"])), "Other"); name = title or r["title"] or code
        if not sign:
            rows.append([code, name, fam, "", "", "no closed line work found for the sign", r["local"]]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        svg, W, H = X.write_svg(sign, fam)
        nm = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")[:60] or "SIGN"; fn = f"{nm}_{code}.svg"; k = 2
        while fn in seen: fn = f"{nm}_{k}_{code}.svg"; k += 1
        seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
        rows.append([code, name, fam, fn, f"{W:.0f}x{H:.0f} mm", sign["note"], r["local"]])
        if i % 25 == 0: print(f"{i + 1}/{len(reg)} {code} {name[:40]}", flush=True)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
