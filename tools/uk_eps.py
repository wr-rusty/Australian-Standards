#!/usr/bin/env python3
"""uk_eps.py — SVGs from the Department for Transport's own coloured sign artwork (gov.uk "Traffic sign images",
Crown copyright, Open Government Licence v3): Original EPS/<pack>/<diagram>.eps with the index spreadsheet
traffic-signs-images-image-details.xls (category, description, shape, colours, diagram number per file).

Ghostscript turns each EPS into a PDF, the fills are lifted exactly (legends are already outlined; no live text).
A plain white page rectangle behind a triangle, disc or rounded panel is dropped so the outside of the sign is
transparent; a white rectangle that is the sign's own border (a uniformly inset rectangular panel inside it) is kept.
The EPS files carry no scale, so the real size comes from the working drawing of the same diagram (Original PDFs/
SIZES.csv, from uk_sizes.py): the drawn size figure is applied to the sign's longer side. Sheets dimensioned in
x-heights only have no absolute size; those SVGs keep the artwork's own proportions at 1 pt = 10 mm and say so.
Output: <UK>/SVGs/<category>/<DESCRIPTION>_<DIAGRAM>.svg (header convention of the other packs) and SVGs/MANIFEST.csv.
  python3 tools/uk_eps.py [limit]      (UK_CACHE=<dir> for the EPS->PDF cache)"""
import os, re, sys, csv, subprocess, collections, pymupdf, xlrd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X
from shs_extract import fmt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UK = os.path.join(ROOT, "Processing", "United Kingdom", "National (TSRGD 2016)")
EPS_DIR = os.path.join(UK, "Original EPS")
GS = "/opt/homebrew/bin/gs"
MM_PER_PT = 25.4 / 72
FALLBACK_MM_PER_PT = 10.0     # no absolute size known: 1 pt of artwork = 10 mm (proportions exact, size nominal)
# Index rows whose EPS name differs from the file DfT shipped (the file is the same sign).
CATEGORIES = ["Bus and cycle signs", "Direction and tourist signs", "Information signs", "Level crossing signs", "Low bridge signs", "Miscellaneous", "Motorway signs",
              "On-street parking", "Pedestrian, cycle, equestrian", "Pedestrian zone signs", "Regulatory signs", "Road works and temporary", "Signs for cyclists and pedestrians",
              "Speed limit signs", "Tidal flow lane control", "Traffic calming", "Tram signs", "Warning signs"]
ALIAS = {"506.1lrr.eps": "507.1lrr.eps", "506.1rl.eps": "507.1rl.eps", "506.1rll.eps": "507.rll.eps",
         "618.2.eps": "618x2.eps", "618.3.eps": "618x3.eps", "618.4.eps": "618x4.eps", "637.2.eps": "637x2.eps", "637.2v.eps": "637x2v.eps"}

def eps_to_pdf(eps, cache):
    pdf = os.path.join(cache, os.path.splitext(os.path.basename(eps))[0] + ".pdf")
    if not os.path.exists(pdf):
        os.makedirs(cache, exist_ok=True)
        r = subprocess.run([GS, "-q", "-dNOPAUSE", "-dBATCH", "-dEPSCrop", "-sDEVICE=pdfwrite", f"-sOutputFile={pdf}", eps], capture_output=True, text=True)
        if r.returncode or not os.path.exists(pdf): raise RuntimeError(f"ghostscript failed: {r.stderr.strip()[:200]}")
    return pdf

def is_plain_rect(f):
    pts = X.item_points(f["items"])
    if any(it[0] == "c" for it in f["items"]) or len(pts) > 12: return False
    r = f["rect"]
    return all(abs(x - r.x0) < 0.5 or abs(x - r.x1) < 0.5 for x, _ in pts) and all(abs(y - r.y0) < 0.5 or abs(y - r.y1) < 0.5 for _, y in pts)

def bbox(fills):
    return pymupdf.Rect(min(f["rect"].x0 for f in fills), min(f["rect"].y0 for f in fills), max(f["rect"].x1 for f in fills), max(f["rect"].y1 for f in fills))

def split_subpaths(items):
    """Contiguous runs of items (a compound path's separate loops)."""
    runs = []; cur = []; end = None
    for it in items:
        if it[0] in ("re", "qu"):
            if cur: runs.append(cur); cur = []
            runs.append([it]); end = None; continue
        start = it[1]
        if cur and end is not None and (abs(start.x - end.x) > 0.05 or abs(start.y - end.y) > 0.05): runs.append(cur); cur = []
        cur.append(it); end = it[2] if it[0] == "l" else it[4]
    if cur: runs.append(cur)
    return runs

def flat_points(sub):
    pts = []
    for it in sub:
        if it[0] == "l": pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == "c":
            p0, p1, p2, p3 = it[1:5]
            for t in (0, 0.25, 0.5, 0.75, 1):
                pts.append((((1 - t) ** 3) * p0.x + 3 * ((1 - t) ** 2) * t * p1.x + 3 * (1 - t) * t * t * p2.x + t ** 3 * p3.x, ((1 - t) ** 3) * p0.y + 3 * ((1 - t) ** 2) * t * p1.y + 3 * (1 - t) * t * t * p2.y + t ** 3 * p3.y))
        else: pts += X.item_points([it])
    return pts

def shape_fill_ratio(sub):
    """Area of the loop over the area of its bounding box: 1 for a rectangle, ~0.79 for a disc, 0.5 for a triangle."""
    pts = flat_points(sub)
    if len(pts) < 3: return 1.0
    a = abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2
    r = sub_rect(sub); return a / max(r.get_area(), 1e-9)

def sub_rect(sub):
    pts = X.item_points(sub); return pymupdf.Rect(min(x for x, _ in pts), min(y for _, y in pts), max(x for x, _ in pts), max(y for _, y in pts))

def strip_page_white(fills, page_rect):
    """The DfT artwork often keeps the white artboard as a page-size rectangle: a fill of its own, or one loop of the
    white compound path (the loop's hole shows the red border beneath). Drop such a loop when the sign inside is not a
    rectangular panel with a uniform white border round it; keep it when it is (the white is then the sign's border)."""
    out = []; dropped = False
    for f in fills:
        r = f["rect"]
        if X.colour_name(f["fill"]) != "WHITE" or r.width < 0.97 * page_rect.width or r.height < 0.97 * page_rect.height: out.append(f); continue
        subs = split_subpaths(f["items"])
        page = [s for s in subs if is_plain_rect({"items": s, "rect": sub_rect(s)}) and sub_rect(s).width >= 0.97 * page_rect.width and sub_rect(s).height >= 0.97 * page_rect.height]
        if not page: out.append(f); continue
        rest = [s for s in subs if s not in page]
        inner_fills = [g for g in fills if g is not f]
        # The white is only an artboard when a page-filling non-rectangular face (disc, triangle, octagon, diamond) sits on it.
        big = max(inner_fills, key=lambda g: g["area"]) if inner_fills else None
        if big is None or big["rect"].width < 0.9 * page_rect.width or big["rect"].height < 0.9 * page_rect.height: out.append(f); continue
        outer = max(split_subpaths(big["items"]), key=lambda s: sub_rect(s).get_area())
        if shape_fill_ratio(outer) > 0.85: out.append(f); continue   # rectangular (or rounded) panel: the white is the sign's own background/border
        dropped = True
        if rest:
            items = [it for s in rest for it in s]; pts = X.item_points(items)
            nr = pymupdf.Rect(min(x for x, _ in pts), min(y for _, y in pts), max(x for x, _ in pts), max(y for _, y in pts))
            out.append({**f, "items": items, "rect": nr, "area": nr.get_area()})
    return out, ("white artboard behind the sign dropped" if dropped else "")

def extract(pdf):
    doc = pymupdf.open(pdf); page = doc[0]
    if not X.fills_on_page(page):
        raster = bool(page.get_images())
        return None, ("raster artwork (Photoshop EPS), no vector paths" if raster else "no filled artwork in the EPS")
    strokes = sum(1 for d in page.get_drawings() if d.get("color") is not None and (d.get("width") or 0) > 0.3)
    note = ""
    fills = X.fills_on_page(page)
    if strokes:   # thin borders drawn as stroked paths (countdown markers, plates): outline them so they become fills
        from nz_extract import strokes_to_fills
        keys = {(round(f["rect"].x0), round(f["rect"].y0), round(f["rect"].x1), round(f["rect"].y1), X.colour_name(f["fill"])) for f in fills}
        doc = pymupdf.open(strokes_to_fills(pdf)); page = doc[0]
        fills = X.fills_on_page(page)
        for f in fills:   # an outlined stroke is a ring or a band: paint it even-odd so its hole stays open
            if (round(f["rect"].x0), round(f["rect"].y0), round(f["rect"].x1), round(f["rect"].y1), X.colour_name(f["fill"])) not in keys: f["even_odd"] = True
        note = f"{strokes} stroked path(s) outlined with Inkscape"
    fills, n2 = strip_page_white(fills, page.rect)
    if n2: note = (note + "; " if note else "") + n2
    pr = bbox(fills)
    return {"panel": pr, "fills": fills, "glyphs": [], "missing_fonts": [], "strokes": strokes}, note

def diagram_key(dgno, stem):
    """'504.1' / '512.0' / '2901' -> 'p504x1' / 'p512' / 'p2901', the working-drawing register's diagram names."""
    for s in (dgno, stem):
        m = re.match(r"\s*(\d{3,4})(?:\.(\d))?", s or "")
        if m: return "p" + m.group(1) + (("x" + m.group(2)) if m.group(2) and m.group(2) != "0" else "")
    return ""

def main(limit=None):
    cache = os.environ.get("UK_CACHE", os.path.join(UK, ".pdfcache"))
    out = os.path.join(UK, "SVGs"); os.makedirs(out, exist_ok=True)
    sizes = {r["diagram"]: r for r in csv.DictReader(open(os.path.join(UK, "Original PDFs", "SIZES.csv")))} if os.path.exists(os.path.join(UK, "Original PDFs", "SIZES.csv")) else {}
    files = collections.defaultdict(list)
    for root, _, fs in os.walk(EPS_DIR):
        for f in fs:
            if f.lower().endswith(".eps"): files[f.lower()].append(os.path.join(root, f))
    sh = xlrd.open_workbook(os.path.join(EPS_DIR, "traffic-signs-images-image-details.xls")).sheet_by_index(0)
    head = [str(sh.cell_value(0, c)) for c in range(sh.ncols)]
    rows = [dict(zip(head, [str(sh.cell_value(r, c)) for c in range(sh.ncols)])) for r in range(1, sh.nrows)]
    seen_eps = set(); seen_fn = set(); manifest = []; n = 0
    for r in rows:
        eps_name = r["EPS"].strip().lower()
        if not eps_name or eps_name in seen_eps: continue
        seen_eps.add(eps_name)
        cat = r["Category"].strip()
        fam = next((c for c in CATEGORIES if cat.lower().startswith(c.lower())), cat.split(",")[0].strip()).title()
        others = cat[len(fam):].strip(", ") if cat.lower().startswith(fam.lower()) else ""
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        disk = ALIAS.get(eps_name, eps_name); alias_note = f"DfT file is named {disk}" if disk != eps_name else ""
        paths = files.get(disk)
        stem = os.path.splitext(r["EPS"].strip())[0]; code = stem.upper()
        name = re.sub(r"[^A-Z0-9]+", "_", r["Description"].upper()).strip("_")[:70] or "SIGN"
        dkey = diagram_key(r["DGNo"], stem); sz = sizes.get(dkey)
        if not paths:
            manifest.append([code, r["Description"], fam, "", "", r["DGNo"], "listed in the DfT index but not in any EPS pack"]); continue
        pref = [p for p in paths if fam.lower().replace(" ", "-").replace(",", "") in p.lower()]
        eps = (pref or paths)[0]
        try:
            sign, note = extract(eps_to_pdf(eps, cache))
        except RuntimeError as ex:
            sign, note = None, str(ex)
        if sign is None:
            manifest.append([code, r["Description"], fam, "", "", r["DGNo"], note]); continue
        pr = sign["panel"]; long_side = max(pr.width, pr.height)
        if sz and sz["size"]:
            mm_per_pt = float(sz["size"]) / long_side
            size_note = f"{sz['size']} mm (working drawing {dkey}; alternatives {sz['alternatives'].replace(' ', '/')})" if sz["alternatives"] else f"{sz['size']} mm (working drawing {dkey})"
        else:
            mm_per_pt = FALLBACK_MM_PER_PT
            size_note = ("working drawing " + dkey + " is dimensioned in x-heights: no absolute size; " if sz and sz["xheight"] else ("no size figure read from working drawing " + dkey + "; " if sz else "no working drawing for this diagram; ")) + "artwork kept at 1 pt = 10 mm (proportions exact, size nominal)"
        sign["scale"] = mm_per_pt / 25.4; sign["diamond"] = False; sign["bg"] = X.colour_name(sign["fills"][0]["fill"])
        svg, W, H = X.write_svg(sign, fam)
        fn = f"{name}_{code}.svg"; k = 2
        while fn in seen_fn: fn = f"{name}_{k}_{code}.svg"; k += 1
        seen_fn.add(fn)
        open(os.path.join(folder, fn), "w").write(svg); n += 1
        notes = "; ".join(t for t in (size_note, note, alias_note, f"also in DfT category {others}" if others else "") if t)
        manifest.append([code, r["Description"], fam, fn, f"{W:.0f}x{H:.0f} mm", r["DGNo"], notes])
        if limit and n >= limit: break
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "diagram", "notes"]); w.writerows(manifest)
    print(f"{n} SVGs written; {sum(1 for m in manifest if not m[3])} index rows without artwork; families: {dict(collections.Counter(m[2] for m in manifest if m[3]))}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
