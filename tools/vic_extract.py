#!/usr/bin/env python3
"""vic_extract.py — Victoria's DTP Supplement to AS 1743 (TEM Vol 2 Part 2.17, one V-series sign drawing per page) and
TEM Vol 3 Part 2.12 (tourist and service signs) into Australia/VIC/SVGs/<family>/<NAME>_<CODE>.svg with MANIFEST.csv,
via sheet_extract page by page. Names come from the books' index tables (Sign No. / Description / Drawing No.).
  python3 tools/vic_extract.py [limit]"""
import os, re, sys, csv, glob, collections, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIC = os.path.join(ROOT, "Australia", "VIC")
BOOKS = ["TEM-Vol-2-Part-2.17-AS1743-Road-Signs-Specifications-_v2_.pdf", "TEM-Vol-3-Part-2.12-Tourist-and-Services-Signs.pdf"]
CODE = re.compile(r"\b([A-Z]{1,2})\s?(\d{1,2})\s?-\s?V\s?(\d{1,3})\s?([A-Z]?)(?:\s?-\s?(\d))?\b")
SYM = re.compile(r"\bS\s?-\s?V\s?(\d{2,3})\b")

class Turned(SE.Frame):
    """The book's sheets are drawn reading up the page: turn every page 90 degrees."""
    def __init__(self, page, spans_raw):
        M = page.rotation_matrix; R = M * pymupdf.Matrix(90); base = (page.rect * page.derotation_matrix).normalize(); pr = (base * R).normalize()
        self.M = R * pymupdf.Matrix(1, 0, 0, 1, -pr.x0, -pr.y0); self.rect = (base * self.M).normalize(); self.turned = 90
SE.Frame = Turned
SE.drawing_region = lambda F, spans: pymupdf.Rect(0, 0, F.rect.width, 0.82 * F.rect.height)   # title block: the band along the bottom once turned

def family(code):
    c = code.upper(); fam = re.match(r"[A-Z]+\d*", c); fam = fam.group(0) if fam else ""
    if c.startswith("S-V"): return "Symbols"
    if fam.startswith("GE"): return "Freeway Signs"
    if fam == "G7": return "Service Signs"
    if fam == "G11": return "Tourist Signs"
    if fam.startswith("G"): return "Guide Signs"
    if fam in ("R5", "R6"): return "Parking Signs"
    if fam.startswith("R"): return "Regulatory Signs"
    if fam.startswith("W"): return "Warning Signs"
    if fam.startswith("T"): return "Temporary Signs"
    if fam.startswith("D"): return "Hazard Markers"
    return "Other Signs"

def norm(m): return f"{m[0]}{m[1]}-V{m[2]}{m[3]}" + (f"-{m[4]}" if m[4] else "")

def index_names(doc):
    """code -> description from the index tables (a code line, a description line, a drawing-number line)."""
    names = {}
    for p in doc:
        t = p.get_text()
        if "Sign No." not in t or "Drawing No" not in t: continue
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        for i, l in enumerate(lines[:-1]):
            m = CODE.fullmatch(l.replace(" ", "")) or CODE.fullmatch(l)
            if m and not re.fullmatch(r"\d{5,7}", lines[i + 1]): names.setdefault(norm(m.groups()), lines[i + 1])
    return names

def main(limit=None):
    out = os.path.join(VIC, "SVGs"); rows = []; seen = {}; n = 0
    for book in BOOKS:
        pdf = os.path.join(VIC, "Original PDFs", book)
        if not os.path.exists(pdf): continue
        doc = pymupdf.open(pdf); names = index_names(doc); print(book, "index names:", len(names), flush=True)
        for pno in range(doc.page_count):
            if limit and n >= limit: break
            page = doc[pno]; text = page.get_text()
            if "Sign No." in text and "Drawing No" in text: continue                      # index page
            if len(page.get_drawings()) < 40: continue                                        # prose page
            codes = list(dict.fromkeys(norm(m) for m in CODE.findall(text))) or [f"S-V{m}" for m in dict.fromkeys(SYM.findall(text))]
            if not codes or len(codes) >= 4: continue                                         # index / list pages name many codes
            code = codes[0]; name = names.get(code, "") or names.get(re.sub(r"-\d$", "", code), ""); fam = family(code); src = f"Original PDFs/{book}#page={pno + 1}"
            try: signs = SE.extract_page(pdf, pno)
            except Exception as ex:
                rows.append([code, name, fam, "", "", f"extraction failed: {str(ex)[:100]}", src]); print("  !!", code, str(ex)[:80], flush=True); continue
            if not signs: rows.append([code, name, fam, "", "", "no drawing found on the page", src]); continue
            folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
            nm = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")[:80] or "SIGN"; cd = code.replace("/", "-")
            for vi, sgn in enumerate(signs):
                svg, W, H = X.write_svg(sgn, fam)
                cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
                fn = f"{nm}_{cd}.svg" if vi == 0 and not cap else f"{nm}_{cap or 'VAR' + str(vi + 1)}_{cd}.svg"
                k = 2
                while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(cd) + r"\.svg$", f"_{k}_{cd}.svg", fn); k += 1
                seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
                rows.append([code, name, fam, fn, f"{W:.0f}x{H:.0f} mm", sgn["note"] + ("; other codes on the page: " + ", ".join(codes[1:]) if len(codes) > 1 else ""), src])
            n += 1
            if n % 25 == 0: print(f"{n} pages -> {code} {name[:40]}", flush=True)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
