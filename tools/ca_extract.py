#!/usr/bin/env python3
"""ca_extract.py — Caltrans California Sign Specification sheets into USA/California/SVGs/<family>/<NAME>_<CODE>.svg with
MANIFEST.csv, via sheet_extract. Caltrans draws each sign in two tones (white panel, black legend) and states the real colours
in a COLORS note, so the drawing is recoloured from that note: on a light background the white panel takes the background
colour and black takes the dark legend colour (whites nested inside black stay white); on a dark background black takes the
background colour and every white takes the light legend colour. Sizes come from the sheet's SIGN SIZE (inches) table.
Scanned (raster) sheets are listed in the manifest but not drawn.
  python3 tools/ca_extract.py [limit]"""
import os, re, sys, csv, collections, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA = os.path.join(ROOT, "USA", "California")
RGB = {"WHITE": "#ffffff", "BLACK": "#231f20", "YELLOW": "#ffd046", "RED": "#bf301a", "ORANGE": "#f7921d", "GREEN": "#006f54", "BLUE": "#005a9c", "BROWN": "#7d4803",
       "FLUORESCENT YELLOW-GREEN": "#bed73d", "FLUORESCENT YELLOW": "#fff500", "FLUORESCENT ORANGE": "#f7921d", "FLUORESCENT PINK": "#ec6aa0", "PURPLE": "#6d276a", "YELLOW-GREEN": "#bed73d"}
LIGHT = {"WHITE", "YELLOW", "ORANGE", "FLUORESCENT YELLOW-GREEN", "FLUORESCENT YELLOW", "FLUORESCENT ORANGE", "FLUORESCENT PINK", "YELLOW-GREEN"}
COLOUR_RE = re.compile(r"FLUORESCENT\s+YELLOW[\s-]*GREEN|FLUORESCENT\s+YELLOW|FLUORESCENT\s+ORANGE|FLUORESCENT\s+PINK|YELLOW[\s-]+GREEN|WHITE|BLACK|GREEN|BLUE|RED|BROWN|YELLOW|ORANGE|PURPLE")
FAMILY = {"g": "Guide Signs", "sg": "Guide Signs", "r": "Regulatory Signs", "sr": "Regulatory Signs", "w": "Warning Signs", "sw": "Warning Signs",
          "c": "Temporary Traffic Control Signs", "sc": "Temporary Traffic Control Signs", "s": "School Signs", "markers": "Object Markers", "cfi": "Guide Signs", "rs": "Route Markers"}

def hex2rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))

def ca_region(F, spans):
    """Caltrans sheet: header band at the top (MUTCD NUMBER / CODE), drawing, then NOTE / SIGN SIZE tables / COLORS below."""
    W, H = F.rect.width, F.rect.height
    top = max([s["bbox"].y1 for s in spans if s["bbox"].y1 < 70] or [48])
    stops = [s["bbox"].y0 for s in spans if re.match(r"(NOTES?|SIGN\s*SIZE|SIZE|D?IMENSIONS|COLOU?RS?|OLOU?RS)\b", s["text"].strip().upper()) and s["bbox"].y0 > 0.25 * H]
    return pymupdf.Rect(0, top + 4, W, (min(stops) if stops else 0.8 * H) - 4)
SE.drawing_region = ca_region
_raw_spans = SE.raw_spans
def ca_spans(page):
    """The accessibility layer lays invisible alt-text fragments ('i', 'g', 'board w') over the drawing: drop the lower-case
    fragments (Caltrans dimension letters are upper-case) so they are not taken for annotations covering the legend."""
    return [s for s in _raw_spans(page) if not re.fullmatch(r"[a-z]{1,3}[,.]?", s["text"].strip())]
SE.raw_spans = ca_spans

CODE_RE = re.compile(r"\b([A-Z]{1,3}\s?\d{1,3}\s?[A-Z]?(?:\s?-\s?\d{1,3}\s?[A-Za-z]?)*(?:\s?\([A-Z]{2}\))?)\b")
def header(spans):
    """MUTCD number (left) and CA code (right) from the header band."""
    band = [s for s in spans if s["bbox"].y1 < 70 and not re.search(r"CALIFORNIA|TRANSPORTATION", s["text"], re.I)]
    left = " ".join(s["text"] for s in sorted(band, key=lambda s: s["bbox"].x0) if s["bbox"].x0 < 300)
    right = " ".join(s["text"] for s in sorted(band, key=lambda s: s["bbox"].x0) if s["bbox"].x0 >= 300)
    left = re.sub(r"MUTCD|NUMBER|C L|_+", " ", left, flags=re.I).strip(" -:")
    right = re.sub(r"\bCODE\b|_+|C L", " ", right, flags=re.I).strip(" -:")
    m = re.search(r"\b(none|non\s?e|n/a|no)\b", left, re.I)
    mutcd = "None" if m else (" ".join(x.replace(" ", "") for x in CODE_RE.findall(left.upper())) or left[:30])
    codes = CODE_RE.findall(right.upper()); code = codes[-1].replace(" ", "") if codes else re.sub(r"\s+", "", right)[:12]
    return mutcd, code

def colour_note(spans, region):
    """{element: COLOUR} from the COLORS note below the drawing."""
    below = sorted([s for s in spans if s["bbox"].y0 >= region.y1 - 2], key=lambda s: (round(s["bbox"].y0), s["bbox"].x0))
    text = " ".join(s["text"] for s in below).upper()
    i = text.find("COLORS"); i = text.find("COLOURS") if i < 0 else i
    if i < 0: return {}, ""
    text = text[i + 7:]; text = text.split("THE POLICY")[0].split("ADOPTED")[0].split("DRAWN")[0]
    out = {}; pos = 0; last_end = 0
    for m in COLOUR_RE.finditer(text):
        elem = text[last_end:m.start()]
        elem = re.split(r"[()]", elem)[-1]                                            # after any '(REFLECTIVE)' fragment, closed or not
        elem = re.sub(r"\b(NON-?\s?)?REFL\w*\b|\bRETRO\w*\b", " ", elem)
        elem = re.sub(r"[^A-Z,&/ ]+", " ", elem); elem = re.sub(r"\s+", " ", elem).strip(" -,&:;")
        for e in re.split(r",|&|\bAND\b", elem):
            e = e.strip(" -:;")
            if e: out.setdefault(e, re.sub(r"\s+", " ", m.group(0)).replace("YELLOW GREEN", "YELLOW-GREEN"))
        last_end = m.end()
        close = text.find(")", m.end())
        if 0 <= close < m.end() + 30: last_end = close + 1
    return out, text.strip()[:160]

def recolour(sign, colours):
    """Apply the COLORS note to the two-tone drawing (see module doc). Returns a note string."""
    fills = sign["fills"]
    if any(X.colour_name(f["fill"]) not in ("BLACK", "WHITE") for f in fills if not f.get("virtual")):
        return "sheet drawn in colour; colours kept as drawn" + ("" if colours else " (no COLORS note read)")
    bg = colours.get("BACKGROUND") or colours.get("BACKGOUND")
    assumed = ""
    if not bg:
        if not colours: return "no COLORS note read; drawn in the sheet's black and white — check"
        bg = "WHITE"; assumed = "; no BACKGROUND in the COLORS note, white assumed — check"
    others = {e: c for e, c in colours.items() if e not in ("BACKGROUND", "BACKGOUND")}
    darks = sorted({c for c in others.values() if c not in LIGHT}); lights = sorted({c for c in others.values() if c in LIGHT})
    blacks = [f for f in fills if X.colour_name(f["fill"]) == "BLACK"]
    notes = []
    if bg in LIGHT:
        dark = darks[0] if darks else "BLACK"; nested_white = (lights[0] if lights else "WHITE")
        if len(darks) > 1: notes.append(f"note names several dark colours ({', '.join(darks)}); all black areas drawn {dark} — check")
        for f in fills:
            n = X.colour_name(f["fill"])
            if n == "BLACK": f["fill"] = hex2rgb(RGB[dark])
            elif n == "WHITE":
                nested = any(b["rect"].contains(f["rect"]) and b["area"] > f["area"] * 1.05 for b in blacks)
                f["fill"] = hex2rgb(RGB[nested_white if nested else bg])
        notes.insert(0, f"colours from the sheet's COLORS note: background {bg}, legend {dark}")
    else:
        light = lights[0] if lights else "WHITE"
        if darks and any(d != bg for d in darks): notes.append(f"note names other dark colours ({', '.join(d for d in darks if d != bg)}) not told apart from the background — check")
        if len(lights) > 1: notes.append(f"note names several light colours ({', '.join(lights)}); all white areas drawn {light} — check")
        for f in fills:
            n = X.colour_name(f["fill"])
            if n == "BLACK": f["fill"] = hex2rgb(RGB[bg])
            elif n == "WHITE": f["fill"] = hex2rgb(RGB[light])
        notes.insert(0, f"colours from the sheet's COLORS note: background {bg}, legend {light}")
    sign["bg"] = bg
    return "; ".join(notes) + assumed

def sizes_in(spans):
    """Rows of the SIGN SIZE (inches) table: [(w, h)] with None for 'Var'. The accessibility text reads 'x' as 'multiply'."""
    rows = []; lines = {}
    for s in spans: lines.setdefault(round(s["bbox"].y0 / 3), []).append(s)
    for y, ss in sorted(lines.items()):
        text = " ".join(s["text"] for s in sorted(ss, key=lambda s: s["bbox"].x0))
        m = re.match(r"\s*(Var|VAR|\d{1,3})\s*(?:x|X|×|[Mm][Uu][Ll][Tt][Ii][Pp][Ll]\w*)\s*(Var|VAR|\d{1,3})\b", text)
        if m:
            w = None if m.group(1).lower() == "var" else float(m.group(1)); h = None if m.group(2).lower() == "var" else float(m.group(2))
            if (w is None or w < 200) and (h is None or h < 200) and (w, h) not in rows: rows.append((w, h))
    if rows: return rows
    # newer sheets: a dimension table whose first two columns are the sign's width and height in inches (no 'x')
    for y, ss in sorted(lines.items()):
        vals = [s["text"].strip() for s in sorted(ss, key=lambda s: s["bbox"].x0)]
        if len(vals) >= 4 and all(re.fullmatch(r"\d{1,3}(?:\.\d+)?[A-Z]?\*?", v) for v in vals[:3]) and ss[0]["bbox"].y0 > 0.4 * max(x["bbox"].y1 for x in spans):
            w, h = float(re.match(r"[\d.]+", vals[0]).group(0)), float(re.match(r"[\d.]+", vals[1]).group(0))
            if 8 <= w <= 200 and 8 <= h <= 200: rows.append((w, h))
    return rows

def choose_size(rows, pr):
    """First table row whose proportions match the drawing (a 'Var' side follows the drawing)."""
    if not rows: return None, ""
    asp = pr.width / pr.height
    def fit(r):
        w, h = r
        if w is None: w = h * asp
        if h is None: h = w / asp
        return abs((w / h) / asp - 1)
    best = min(rows, key=fit); w, h = best
    if w is not None and h is not None and fit(best) > 0.15:      # no row matches the drawing: take the first row's width, keep the drawn proportions
        w, h = rows[0][0], rows[0][0] / asp
        return (w, h), f"{int(rows[0][0])} x {int(rows[0][1])} in table row; proportions differ from the drawing, drawn proportions kept at width {int(w)} in — check"
    if w is None: w = h * asp
    if h is None: h = w / asp
    tag = f"{'Var' if best[0] is None else int(best[0])} x {'Var' if best[1] is None else int(best[1])} in"
    return (w, h), tag + (f"; other table sizes: " + ", ".join(f"{'Var' if a is None else int(a)} x {'Var' if b is None else int(b)}" for a, b in rows if (a, b) != best) if len(rows) > 1 else "")

def is_raster(page):
    """A scanned sheet: one image covering most of the page (usually with an OCR text layer)."""
    A = page.rect.get_area()
    if any(pymupdf.Rect(i["bbox"]).get_area() > 0.4 * A for i in page.get_image_info()): return True
    t = page.get_text()
    return len(t.strip()) < 50 or bool(re.search(r"S T A T E", t))

def main(limit=None):
    out = os.path.join(CA, "SVGs"); rows = []; seen = {}
    reg = [r for r in csv.DictReader(open(os.path.join(CA, "REGISTER.csv"))) if r["local"] and r["series"] in FAMILY]
    if limit: reg = reg[:limit]
    for i, r in enumerate(reg):
        pdf = os.path.join(CA, r["local"]); src = r["local"]; fam = FAMILY[r["series"]]
        code0 = re.sub(r"\s*\(PDF\)\s*$", "", r["text"]).strip(); name = code0
        doc = pymupdf.open(pdf); page = doc[0]
        if is_raster(page):
            rows.append([code0, "", fam, "", "", "scanned sheet (raster image); not drawn — needs a vector copy or tracing", src]); continue
        spans, F = SE.sheet_spans(pdf); region = ca_region(F, spans)
        mutcd, _ = header(spans); code = re.sub(r"\s*\(CA\)\s*", "", code0).replace(" ", "")
        if not mutcd:
            m = re.search(r"MUTCD\s*(?:CODE|NUMBER)\s*:?\s*([A-Za-z0-9-]+)", " ".join(s["text"] for s in spans)); mutcd = m.group(1) if m else ""
        mutcd_note = "" if not mutcd or re.match(r"^(none|non e|n|no)\b", mutcd, re.I) else f"MUTCD number {mutcd}"
        colours, ctext = colour_note(spans, region)
        legend = " ".join(s["text"] for s in spans if SE.SIGN_FONT.search(s["font"]) and region.contains(pymupdf.Point(s["origin"])))
        try: signs = SE.extract_page(pdf, 0)
        except Exception as ex:
            rows.append([code, code0, fam, "", "", f"extraction failed: {str(ex)[:120]}", src]); print("  !!", code, str(ex)[:100], flush=True); continue
        if not signs:
            rows.append([code, code0, fam, "", "", "no drawing found on the sheet", src]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        table = sizes_in(spans)
        nm = re.sub(r"[^A-Z0-9]+", "_", (legend or code0).upper()).strip("_")[:60] or "SIGN"; cd = re.sub(r"[^A-Za-z0-9-]+", "", code) or "SIGN"
        for vi, sgn in enumerate(signs):
            note = [sgn["note"]] if sgn["note"] and "no size found" not in sgn["note"] else []
            size, stag = choose_size(table, sgn["panel"])
            if size:
                pr = sgn["panel"]; land = pr.width >= pr.height; sw = max(size) if land else min(size)
                sgn["scale"] = sw / pr.width; note = [f"size from the sheet's SIGN SIZE table ({stag})"]
            elif "no size found" in (sgn["note"] or ""): note.append("no SIGN SIZE table read; drawn at 1:10 — check")
            cn = recolour(sgn, colours); note.append(cn if cn else "no COLORS note found; drawn in the sheet's black and white — check")
            dashes = sum(1 for f in sgn["fills"] if min(f["rect"].width, f["rect"].height) < 1.2 and not f.get("virtual"))
            if dashes >= 12: note.append("dashed placeholder outlines on the sheet (alternate panels / messages) partly kept as small marks — check")
            if mutcd_note: note.append(mutcd_note)
            svg, W, H = X.write_svg(sgn, fam)
            cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
            fn = f"{nm}_{cd}.svg" if vi == 0 and not cap else f"{nm}_{cap or 'VAR' + str(vi + 1)}_{cd}.svg"
            n = 2
            while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(cd) + r"\.svg$", f"_{n}_{cd}.svg", fn); n += 1
            seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
            rows.append([code, code0, fam, fn, f"{W:.0f}x{H:.0f} mm", "; ".join(note), src])
        if i % 25 == 0: print(f"{i + 1}/{len(reg)} {code} {legend[:40]}", flush=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
