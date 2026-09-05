#!/usr/bin/env python3
"""nz_extract.py — SVGs from the NZTA sign-specification EPS files (crawled by nz_crawl.py).

Each EPS is the sign's artwork drawn at 1:10 (Illustrator; legends outlined, no dimension marks). Ghostscript turns it
into a PDF, the fills are lifted exactly, and the drawing is scaled ×10 to real size. The register's dimension "a" (or
the first width figure) is compared with the drawn width; a mismatch beyond 2% is noted in the manifest.
Output: <NZ>/SVGs/<category>/<TITLE>_<CODE>.svg (header convention of the other sets) and <NZ>/SVGs/MANIFEST.csv.
  python3 tools/nz_extract.py [register.csv]"""
import os, re, sys, csv, subprocess, math
from shs_extract import fmt
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NZ = os.path.join(ROOT, "New Zealand", "National (TCD Manual)")
GS = "/opt/homebrew/bin/gs"
MM_PER_PT = 25.4 / 72
DRAWN_SCALE = 10          # the EPS files are drawn at 1:10
FAMILY = {"Regulatory": "Regulatory Signs", "Permanent warning": "Permanent Warning Signs", "Temporary warning": "Temporary Warning Signs",
          "Symbol": "Symbols", "Parking": "Parking Signs", "General advisory": "General Advisory Signs", "Motorist service": "Motorist Service Signs",
          "Tourist": "Tourist Signs", "Guide": "Guide Signs", "Arrow": "Arrows"}

def eps_to_pdf(eps, cache):
    pdf = os.path.join(cache, os.path.splitext(os.path.basename(eps))[0] + ".pdf")
    if not os.path.exists(pdf):
        os.makedirs(cache, exist_ok=True)
        r = subprocess.run([GS, "-q", "-dNOPAUSE", "-dBATCH", "-dEPSCrop", "-sDEVICE=pdfwrite", f"-sOutputFile={pdf}", eps], capture_output=True, text=True)
        if r.returncode or not os.path.exists(pdf): raise RuntimeError(f"ghostscript failed: {r.stderr.strip()[:200]}")
    return pdf

def register_widths(dim):
    """Sign widths in mm from the register's dimension list: every figure after 'a' (several sizes), else the first WxH."""
    m = re.search(r"\ba\s*:?\s*((?:\d{2,5}(?:\.\d+)?\s*(?:mm)?\s*(?:\([^)]*\)\s*)?)+)", dim)
    if m: return [float(v) for v in re.findall(r"\d{2,5}(?:\.\d+)?", re.sub(r"\([^)]*\)", "", m.group(1)))]
    m = re.search(r"(\d{2,5})\s*[x×]\s*(\d{2,5})", dim)
    return [float(m.group(1))] if m else []

NOTE_FONTS = ("Whitney", "Arial", "Myriad", "Helvetica", "Times")
_font_cache = {}

def glyph_items(doc, xref, fontname, ext, ch, origin, size):
    """Outline of one character of an embedded font as PyMuPDF-style items in page coordinates."""
    from fontTools.pens.recordingPen import RecordingPen
    key = (doc.name, xref)
    if key not in _font_cache:
        gs = None; upm = 1000; cmap = None
        try:
            _, fext, _, buf = doc.extract_font(xref)
            import io
            if fext in ("pfa", "pfb"):
                import tempfile
                from fontTools.t1Lib import T1Font
                with tempfile.NamedTemporaryFile(suffix="." + fext, delete=False) as fh: fh.write(buf); path = fh.name
                t1 = T1Font(path); os.unlink(path); gs = t1.getGlyphSet()
            elif fext == "cff":
                from fontTools.cffLib import CFFFontSet
                cff = CFFFontSet(); cff.decompile(io.BytesIO(buf), None); gs = cff[0].CharStrings
            elif fext in ("ttf", "otf"):
                from fontTools.ttLib import TTFont
                tt = TTFont(io.BytesIO(buf)); gs = tt.getGlyphSet(); upm = tt["head"].unitsPerEm; cmap = tt.getBestCmap()
        except Exception: gs = None
        _font_cache[key] = (gs, upm, cmap)
    gs, upm, cmap = _font_cache[key]
    if gs is None: return None
    from fontTools import agl
    name = None
    if cmap: name = cmap.get(ord(ch))
    if not name:
        name = agl.UV2AGL.get(ord(ch)) or ("uni%04X" % ord(ch))
    if name not in gs: return None
    pen = RecordingPen()
    try: gs[name].draw(pen)
    except Exception: return None
    k = size / upm; ox, oy = origin
    def P(pt): return (ox + pt[0] * k, oy - pt[1] * k)
    items = []; cur = None; startp = None
    for op, args in pen.value:
        if op == "moveTo": cur = startp = P(args[0])
        elif op == "lineTo": q = P(args[0]); items.append(("l", cur, q)); cur = q
        elif op == "curveTo":
            pts = [P(a) for a in args]
            if len(pts) == 3: items.append(("c", cur, pts[0], pts[1], pts[2])); cur = pts[2]
            else:
                for q in pts: items.append(("l", cur, q)); cur = q
        elif op == "qCurveTo":
            pts = [P(a) for a in args if a is not None]
            for i in range(len(pts) - 1):   # implied on-curve points between consecutive off-curve points
                c1 = pts[i]; nxt = pts[i + 1] if i + 1 < len(pts) - 1 else pts[-1]
                mid = nxt if i + 1 == len(pts) - 1 else ((c1[0] + nxt[0]) / 2, (c1[1] + nxt[1]) / 2)
                b1 = (cur[0] + 2 / 3 * (c1[0] - cur[0]), cur[1] + 2 / 3 * (c1[1] - cur[1])); b2 = (mid[0] + 2 / 3 * (c1[0] - mid[0]), mid[1] + 2 / 3 * (c1[1] - mid[1]))
                items.append(("c", cur, b1, b2, mid)); cur = mid
        elif op in ("closePath", "endPath"):
            if cur and startp and cur != startp: items.append(("l", cur, startp))
            cur = startp
    return items

def text_fills(doc, page, box):
    """Live text inside a box, outlined from the embedded fonts, as extra fills; also the fonts it could not outline."""
    raw = page.get_text("rawdict"); fonts = {}
    for f in page.get_fonts(): fonts.setdefault(f[3].split("+")[-1], []).append(f)   # a font can be embedded several times (subsets)
    out = []; missing = set(); notes = []
    for b in raw["blocks"]:
        if not b.get("lines"): continue
        for l in b["lines"]:
            for sp in l["spans"]:
                txt = "".join(c["c"] for c in sp["chars"]).strip()
                if not txt: continue
                ox, oy = sp["origin"]
                if not (box.x0 <= ox <= box.x1 and box.y0 <= oy <= box.y1): continue
                base = sp["font"].split("+")[-1]
                if any(n in base for n in NOTE_FONTS): notes.append(txt); continue
                colour = pymupdf.sRGB_to_rgb(sp["color"]) if isinstance(sp.get("color"), int) else (0, 0, 0)
                colour = tuple(v / 255 for v in colour)
                for c in sp["chars"]:
                    if not c["c"].strip(): continue
                    items = None
                    for f in fonts.get(base, []):
                        items = glyph_items(doc, f[0], base, f[1], c["c"], c["origin"], sp["size"])
                        if items: break
                    if not items: missing.add(f"{base} '{c['c']}'"); continue
                    xs = [p[0] for it in items for p in it[1:]]; ys = [p[1] for it in items for p in it[1:]]
                    r = pymupdf.Rect(min(xs), min(ys), max(xs), max(ys))
                    out.append({"rect": r, "fill": colour, "items": items, "area": r.get_area(), "even_odd": True})
    return out, sorted(missing), notes

def extract(pdf, whole=False):
    """Drawings on the EPS page. Fills are clustered by proximity (a sign with its border is one cluster; an assembly's
    plates, or the same sign at several sizes, are separate clusters). Live text is outlined from the embedded fonts.
    Identical drawings at several sizes are folded (the caller picks the size); plain swatches and specks are dropped."""
    doc = pymupdf.open(pdf); page = doc[0]
    fills = X.fills_on_page(page)
    if not fills: return []
    U = pymupdf.Rect(min(f["rect"].x0 for f in fills), min(f["rect"].y0 for f in fills), max(f["rect"].x1 for f in fills), max(f["rect"].y1 for f in fills))
    m = 0.02 * max(U.width, U.height)
    parent = list(range(len(fills)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(fills)):
        ri = fills[i]["rect"] + (-m, -m, m, m)
        for j in range(i + 1, len(fills)):
            if ri.intersects(fills[j]["rect"]): parent[find(i)] = find(j)
    groups = {}
    for i in range(len(fills)): groups.setdefault(find(i), []).append(fills[i])
    if whole: groups = {0: fills}     # a symbol sheet is one drawing however many separate shapes it has
    signs = []
    for g in groups.values():
        box = pymupdf.Rect(min(f["rect"].x0 for f in g), min(f["rect"].y0 for f in g), max(f["rect"].x1 for f in g), max(f["rect"].y1 for f in g))
        if box.get_area() < 0.005 * U.get_area(): continue                      # specks, margin labels
        glyphs, missing, notes = text_fills(doc, page, box)
        content = g + glyphs
        if len(content) == 1 and len(content[0]["items"]) <= 5 and not glyphs: continue   # a plain swatch
        panel = max(g, key=lambda f: f["area"])
        if panel["area"] >= 0.9 * box.get_area():                                # a bordered sign: drop what sits outside its outline
            hull = X.convex_hull(X.item_points(panel["items"]))
            content = [f for f in content if f is panel or X.in_hull(hull, ((f["rect"].x0 + f["rect"].x1) / 2, (f["rect"].y0 + f["rect"].y1) / 2))]
            pr = panel["rect"]
        else: pr = box
        strokes = sum(1 for d in page.get_drawings() if d.get("fill") is None and d.get("width", 0) > 0.5 and pr.intersects(d["rect"]))
        def rel(f):
            r = f["rect"]; return (round((r.x0 - pr.x0) / pr.width, 2), round((r.y0 - pr.y0) / pr.height, 2), round(r.width / pr.width, 2), round(r.height / pr.height, 2), X.colour_name(f["fill"]))
        signs.append({"panel": pr, "fills": content, "glyphs": [], "scale": DRAWN_SCALE * MM_PER_PT / 25.4, "missing_fonts": missing, "notes_text": notes,
                      "strokes": strokes, "bg": X.colour_name(panel["fill"]), "sig": tuple(sorted(rel(f) for f in content)), "diamond": X.is_diamond(X.convex_hull(X.item_points(panel["items"])), panel["rect"])})
    signs.sort(key=lambda s: -s["panel"].get_area())
    kept = []
    for s in signs:
        dup = [k for k in kept if k["sig"] == s["sig"] and abs(k["panel"].width / k["panel"].height - s["panel"].width / s["panel"].height) < 0.03]
        if dup: dup[0].setdefault("alts", []).append(s); continue
        kept.append(s)
    return kept

def choose_size(sign, widths):
    """Among the same drawing at several sizes, the one matching the register's first size; else the largest."""
    alts = [sign] + sign.get("alts", [])
    def w_mm(s):
        w = s["panel"].width * DRAWN_SCALE * MM_PER_PT
        return w / math.sqrt(2) if s["diamond"] else w
    for want in widths:
        for s in alts:
            if abs(w_mm(s) - want) <= 0.06 * want or abs(s["panel"].height * DRAWN_SCALE * MM_PER_PT - want) <= 0.06 * want:
                s["sizes"] = len(alts); return s
    sign["sizes"] = len(alts); return sign

# Symbols NZTA withholds (Standards NZ copyright notice on the sheet) but draws as sample content on tourist sign sheets:
# symbol code -> (tourist sheet code, which pictogram under the notice: "tall" or "wide"), lifted from there.
RECOVERED = {"ST10": ("VI3L", "tall"), "ST11": ("VJ4R", "wide")}
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"

def recover_symbol(reg, code, widths, cache, folder, fn):
    """Lift a withheld pictogram from a tourist sheet: white shapes become black, the sign-coloured cut-outs become holes
    (Inkscape path booleans), scaled so its height matches the register's symbol size."""
    src, want = RECOVERED[code]
    eps = [p for p in reg[src]["local"].split(" | ") if p.lower().endswith(".eps")][0]
    doc = pymupdf.open(eps_to_pdf(os.path.join(NZ, eps), cache)); page = doc[0]
    nb = None
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                t = "".join(c["c"] for c in sp["chars"])
                if "copyright" in t.lower() or "Standards" in t or "Note" in t: nb = pymupdf.Rect(sp["bbox"]) if nb is None else nb | pymupdf.Rect(sp["bbox"])
    fills = [f for f in X.fills_on_page(page) if f["rect"].intersects(nb) and f["area"] < 0.2 * page.rect.get_area()]
    parent = list(range(len(fills)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(fills)):
        for j in range(i + 1, len(fills)):
            if (fills[i]["rect"] + (-3, -3, 3, 3)).intersects(fills[j]["rect"]): parent[find(i)] = find(j)
    groups = {}
    for i in range(len(fills)): groups.setdefault(find(i), []).append(fills[i])
    cl = []
    for g in groups.values():
        box = pymupdf.Rect(min(f["rect"].x0 for f in g), min(f["rect"].y0 for f in g), max(f["rect"].x1 for f in g), max(f["rect"].y1 for f in g)); cl.append((box, g))
    box, g = max([c for c in cl if (c[0].height > c[0].width) == (want == "tall")], key=lambda c: c[0].get_area())
    target = widths[0] if widths else box.height * DRAWN_SCALE * MM_PER_PT
    k = target / box.height          # pt -> mm so the pictogram is `target` mm tall
    def T(p): return ((p[0] - box.x0) * k, (p[1] - box.y0) * k)
    W, H = box.width * k, box.height * k
    body = []; bi = hi = 0
    for f in g:
        if X.colour_name(f["fill"]) == "WHITE": bi += 1; body.append(f'<path id="b{bi}" fill="#000000"{" fill-rule=\"evenodd\"" if f.get("even_odd") else ""} d="{X.path_d(f["items"], T)}"/>')
        else: hi += 1; body.append(f'<path id="h{hi}" fill="#ff0000"{" fill-rule=\"evenodd\"" if f.get("even_odd") else ""} d="{X.path_d(f["items"], T)}"/>')
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        rawp = os.path.join(td, "raw.svg"); outp = os.path.join(td, "out.svg")
        open(rawp, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">' + "".join(body) + "</svg>")
        acts = f"select-by-id:{','.join('b%d' % i for i in range(1, bi + 1))};path-union;select-clear;"
        if hi: acts += f"select-by-id:{','.join('h%d' % i for i in range(1, hi + 1))};path-union;select-clear;select-all;path-difference;"
        subprocess.run([INK, rawp, "--actions", acts + f"export-plain-svg;export-filename:{outp};export-do"], capture_output=True, text=True)
        d = re.findall(r'\sd="([^"]+)"', open(outp).read())
    d = " ".join(d)
    # path coordinates are in mm; write the repo header (1 pt = 1 cm, mm × 0.1 inside a scale(0.1) group)
    OW, OH = W * 0.1, H * 0.1
    svg = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{fmt(OW * 25.4 / 72)}mm" height="{fmt(OH * 25.4 / 72)}mm" viewBox="0 0 {fmt(OW)} {fmt(OH)}">',
           '<g transform="scale(0.1)">', f'  <path fill="#000000" fill-rule="evenodd" d="{d}"/>', "</g>", "</svg>"]
    open(os.path.join(folder, fn), "w").write("\n".join(svg) + "\n")
    return W, H, src

def main(register=None):
    register = register or os.path.join(NZ, "REGISTER.csv")
    out = os.path.join(NZ, "SVGs"); cache = os.path.join(os.environ.get("NZ_CACHE", os.path.join(NZ, ".pdfcache")))
    rows = []; seen = {}
    reg_by_code = {r["code"]: r for r in csv.DictReader(open(register))}
    for r in csv.DictReader(open(register)):
        fam = FAMILY.get(r["category"], r["category"]); folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        eps_files = [p for p in r["local"].split(" | ") if p.lower().endswith(".eps")]
        if not eps_files:
            rows.append([r["code"], r["title"], fam, "", "", r["dimensions"], "no EPS file on the register entry"]); continue
        for i, rel in enumerate(eps_files):
            eps = os.path.join(NZ, rel)
            try: signs = extract(eps_to_pdf(eps, cache), whole=(fam == "Symbols"))
            except RuntimeError as ex:
                rows.append([r["code"], r["title"], fam, "", "", r["dimensions"], str(ex)]); continue
            if not signs:
                rows.append([r["code"], r["title"], fam, "", "", r["dimensions"], "no filled artwork in the EPS"]); continue
            name = re.sub(r"[^A-Z0-9]+", "_", r["title"].upper()).strip("_") or "SIGN"
            code = r["code"].replace(" ", "").replace("/", "-")
            stem_variant = ""
            if len(eps_files) > 1:   # several drawings on one entry: name the extra ones from the file name
                stem = os.path.splitext(os.path.basename(rel))[0]
                stem_variant = re.sub(r"[^A-Z0-9]+", "_", re.sub(rf"(?i)^{re.escape(code)}[-_ ]*", "", stem).upper()).strip("_")[:30]
            widths = register_widths(r["dimensions"])
            for vi, sign in enumerate(signs):
                sign = choose_size(sign, widths); note = ""
                if fam == "Symbols" and widths:   # symbol sheets are drawn at their own scale: size them to the register
                    drawn = sign["panel"].width * DRAWN_SCALE * MM_PER_PT
                    if abs(drawn - widths[0]) > 0.06 * widths[0]:
                        sign["scale"] *= widths[0] / drawn; note = f"symbol sheet drawn at {drawn:.0f} mm wide; scaled to the register's {fmt(widths[0])} mm"
                svg, W, H = X.write_svg(sign, fam)
                w_eff = W / math.sqrt(2) if sign["diamond"] else W
                if widths and vi == 0 and not note and not any(abs(w_eff - want) <= 0.06 * want or abs(H - want) <= 0.06 * want for want in widths):
                    note = f"drawn width {W:.0f} mm vs register {'/'.join(fmt(w) for w in widths)} mm — check"
                if sign.get("sizes", 1) > 1: note = (note + "; " if note else "") + f"drawn at {sign['sizes']} sizes on the sheet; {'register size' if widths else 'largest'} kept"
                if sign["missing_fonts"]: note = (note + "; " if note else "") + f"text in {', '.join(sign['missing_fonts'])} could not be outlined — check"
                if sign["strokes"]: note = (note + "; " if note else "") + f"{sign['strokes']} stroked path(s) ignored"
                variant = stem_variant
                if vi: variant = (variant + "_" if variant else "") + (sign["bg"] if sign["bg"] != signs[0]["bg"] else f"VAR{vi + 1}")
                fn = f"{name}_{variant}_{code}.svg" if variant else f"{name}_{code}.svg"
                n = 2
                while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(code) + r"\.svg$", f"_{n}_{code}.svg", fn); n += 1
                seen[fn] = 1
                withheld = [t for t in sign["notes_text"] if "copyright" in t.lower()]
                if withheld and fam != "Symbols": note = (note + "; " if note else "") + "sheet carries a Standards NZ copyright notice over one example pictogram (NZS 8603 symbol)"
                if withheld and fam == "Symbols" and r["code"] in RECOVERED:
                    W, H, src = recover_symbol(reg_by_code, r["code"], widths, cache, folder, fn)
                    rows.append([r["code"], r["title"], fam, fn, f"{W:.0f}x{H:.0f} mm", r["dimensions"], f"artwork lifted from the {src} tourist sheet where NZTA draws it (symbol sheet carries only a Standards NZ copyright notice); holes cut with Inkscape booleans"]); continue
                if withheld and fam == "Symbols":   # NZTA does not supply the artwork (Standards NZ copyright); the sheet carries only a notice
                    idir = os.path.join(out, "intervene", fam); os.makedirs(idir, exist_ok=True)
                    open(os.path.join(idir, fn), "w").write(svg)
                    rows.append([r["code"], r["title"], "intervene/" + fam, fn, f"{W:.0f}x{H:.0f} mm", r["dimensions"], "artwork not supplied by NZTA: sheet says " + " ".join(withheld)[:120]]); continue
                open(os.path.join(folder, fn), "w").write(svg)
                rows.append([r["code"], r["title"], fam, fn, f"{W:.0f}x{H:.0f} mm", r["dimensions"], note])
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "register_dimensions", "notes"]); w.writerows(rows)
    iv = [r for r in rows if r[2].startswith("intervene/")]
    if iv:
        with open(os.path.join(out, "intervene", "INTERVENE_LIST.md"), "w") as fh:
            fh.write("# Signs needing a manual check\n\n")
            for r in iv: fh.write(f"- {r[2][len('intervene/'):]}/{r[3]} ({r[0]}): {r[6]}\n")
    import collections
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))
    print("notes:", sum(1 for r in rows if r[6]))

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else None)
