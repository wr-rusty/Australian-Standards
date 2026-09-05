#!/usr/bin/env python3
"""act_extract.py — ACT (TCCS) municipal standard drawings for signs (ACTSD-36xx/37xx) into Australia/ACT/SVGs/<family>/
with MANIFEST.csv via sheet_extract. Scanned sheets (most of the parking-sign series) are listed without a file.
  python3 tools/act_extract.py"""
import os, re, sys, csv, glob, collections, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACT = os.path.join(ROOT, "Australia", "ACT")
TITLES = {"3601": "Vertical and lateral sign positioning", "3602": "Endorsed sign systems", "3610": "School zone sign details", "3611": "Refuge island sign details",
          "3620": "Finger board sign details", "3630": "Signpost and footing details", "3750": "Park and Ride directional signage", "3751": "Directional signage - electric vehicle charging"}
def family(n):
    n = int(n)
    if 3700 <= n < 3750: return "Parking Signs"
    if n in (3750, 3751): return "Guide Signs"
    if n in (3610, 3611): return "Regulatory Signs"
    if n == 3620: return "Guide Signs"
    return "Other"
def is_raster(page):
    A = page.rect.get_area()
    return any(pymupdf.Rect(i["bbox"]).get_area() > 0.4 * A for i in page.get_image_info()) and len(page.get_drawings()) < 200
def main():
    out = os.path.join(ACT, "SVGs"); rows = []; seen = {}
    for pdf in sorted(glob.glob(os.path.join(ACT, "Original PDFs", "ACTSD", "*.pdf"))):
        n = re.search(r"ACTSD-(\d{4})", pdf).group(1); src = os.path.relpath(pdf, ACT); fam = family(n)
        page = pymupdf.open(pdf)[0]; text = page.get_text(); title = TITLES.get(n, "ACT standard parking signs" if fam == "Parking Signs" else "")
        if n in ("3601", "3602", "3630"):
            rows.append([f"ACTSD-{n}", title, "Other", "", "", "post, footing and positioning details — no sign face", src]); continue
        codes = sorted(set(re.findall(r"\bR\d-\d+(?:/\d+(?:-\d+)?)?\b", text)))
        title = TITLES.get(n, "ACT standard parking signs" if fam == "Parking Signs" else "")
        if is_raster(page):
            rows.append([f"ACTSD-{n}", title, fam, "", "", "scanned sheet (raster image with OCR text); sign faces not drawn — needs the CAD original from TCCS" + (f"; codes on the sheet: {', '.join(codes[:12])}" if codes else ""), src]); continue
        try: signs = SE.extract_page(pdf, 0)
        except Exception as ex: rows.append([f"ACTSD-{n}", title, fam, "", "", f"extraction failed: {str(ex)[:100]}", src]); continue
        if not signs: rows.append([f"ACTSD-{n}", title, fam, "", "", "vector sheet but no sign face drawing found (assembly / detail drawing)", src]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        for vi, sgn in enumerate(signs):
            svg, W, H = X.write_svg(sgn, fam)
            cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
            nm = re.sub(r"[^A-Z0-9]+", "_", (cap or title or "SIGN").upper()).strip("_")[:60]
            fn = f"{nm}_ACTSD-{n}.svg" if vi == 0 else f"{nm}_{cap or 'VAR' + str(vi + 1)}_ACTSD-{n}.svg"
            k = 2
            while fn in seen: fn = re.sub(r"(_\d+)?_ACTSD-" + n + r"\.svg$", f"_{k}_ACTSD-{n}.svg", fn); k += 1
            seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
            rows.append([f"ACTSD-{n}", title, fam, fn, f"{W:.0f}x{H:.0f} mm", sgn["note"], src])
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))
if __name__ == "__main__": main()
