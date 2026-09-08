#!/usr/bin/env python3
"""uk_sizes.py — size figures from the DfT TSRGD 2016 working drawings, one OCR pass per sheet.

Each working drawing (Original PDFs/, from uk_crawl.py) states the drawn size of the sign and its permitted alternatives
beside the drawing: '600 (750) (900) (1200) (1500)' or '(400) 480 (560)', the unbracketed figure being the drawn one.
Direction-sign sheets are dimensioned in x-heights instead ('x-ht', '4x'). The sheet is OCR'd (tesseract) and the
figures recorded in Original PDFs/SIZES.csv: diagram, drawn size, alternatives, x-height flag, colours line, raw text.
Resumable: sheets already in the CSV are skipped.   python3 tools/uk_sizes.py [limit | reparse | retry]"""
import os, re, sys, csv, subprocess, tempfile, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UK = os.path.join(ROOT, "Processing", "United Kingdom", "National (TSRGD 2016)")
OUT = os.path.join(UK, "Original PDFs", "SIZES.csv")
FIELDS = ["diagram", "size", "alternatives", "xheight", "colours", "text"]

def ocr(page, dpi=170, psm="3"):
    pix = page.get_pixmap(dpi=dpi)
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "p.png"); pix.save(png)
        return subprocess.run(["tesseract", png, "stdout", "--psm", psm], capture_output=True, text=True).stdout

STANDARD = {150, 200, 250, 300, 350, 400, 450, 480, 500, 560, 600, 640, 700, 750, 800, 900, 1000, 1050, 1200, 1250, 1350, 1500, 1800, 2100, 2400}

def parse(text, diagram):
    """Drawn size and alternatives. The sheet lists the drawn size unbracketed next to the bracketed alternatives —
    '600 (750) (900) (1200) (1500)', '(400) 480 (560)' — often split over several lines, so: take the bracketed figures,
    then the unbracketed standard-size figure nearest the first of them. x-height flag when the sheet is dimensioned in x."""
    u = text.upper().replace("—", "-").replace("–", "-")
    dn = re.sub(r"\D", "", diagram.split("x")[0])
    toks = [(m.start(), int(m.group(2)), bool(m.group(1))) for m in re.finditer(r"(\(\s*)?\b(\d{3,4})\b\s*\)?", u)]
    toks = [(p, v, b) for p, v, b in toks if 100 <= v <= 5000 and str(v) != dn]
    br = [(p, v) for p, v, b in toks if b]
    size = ""; alts = ""
    if br:
        lo, hi = min(v for _, v in br), max(v for _, v in br)
        cands = [(abs(p - br[0][0]), p, v) for p, v, b in toks if not b and v in STANDARD and 0.3 * lo <= v <= 3 * hi and abs(p - br[0][0]) < 60]
        if cands:
            size = str(min(cands)[2]); alts = " ".join(str(v) for _, v in br)
    xh = bool(re.search(r"X\s*-?\s*H(?:EIGHT|T)\b|\b\d+(?:\.\d+)?\s*X\b(?!\s*\d)", u)) and not size
    cm = re.search(r"COLOURS?\s*[:\-]?\s*(.{0,200})", u, re.S)
    colours = re.sub(r"\s+", " ", cm.group(1).split("BEFORE USING")[0].split("NOTES")[0]).strip() if cm else ""
    return size, alts, xh, colours

def main(limit=None):
    done = {}
    if os.path.exists(OUT):
        done = {r["diagram"]: r for r in csv.DictReader(open(OUT))}
    rows = list(csv.DictReader(open(os.path.join(UK, "REGISTER.csv"))))
    todo = [r for r in rows if r["diagram"] not in done]; new = 0
    if limit == "reparse":
        for d in done.values():
            d["size"], d["alternatives"], xh, d["colours"] = parse(d["text"], d["diagram"]); d["xheight"] = "x" if xh else ""
        todo = []; limit = None
    if limit == "retry":   # sheets that gave neither a size nor an x-height flag: sparse-text OCR at a higher resolution
        by = {r["diagram"]: r for r in rows}
        for d in done.values():
            if d["size"] or d["xheight"]: continue
            text = ocr(pymupdf.open(os.path.join(UK, by[d["diagram"]]["local"]))[0], 300, "11")
            size, alts, xh, colours = parse(text, d["diagram"])
            if size or xh: d.update(size=size, alternatives=alts, xheight="x" if xh else "", colours=colours or d["colours"], text=re.sub(r"\s+", " ", text)[:1500]); new += 1
        todo = []; limit = None
    if limit: todo = todo[:limit]
    for r in todo:
        pdf = os.path.join(UK, r["local"])
        try:
            page = pymupdf.open(pdf)[0]; text = ocr(page)
        except Exception as ex:
            text = ""; print("OCR failed", r["diagram"], ex)
        size, alts, xh, colours = parse(text, r["diagram"])
        done[r["diagram"]] = {"diagram": r["diagram"], "size": size, "alternatives": alts, "xheight": "x" if xh else "", "colours": colours, "text": re.sub(r"\s+", " ", text)[:1500]}
        new += 1
        with open(OUT, "w", newline="") as fh:
            w = csv.DictWriter(fh, FIELDS); w.writeheader()
            for d in rows:
                if d["diagram"] in done: w.writerow(done[d["diagram"]])
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS); w.writeheader()
        for d in rows:
            if d["diagram"] in done: w.writerow(done[d["diagram"]])
    have = sum(1 for d in done.values() if d["size"]); xh = sum(1 for d in done.values() if d["xheight"])
    print(f"{new} sheets read this run; {len(done)}/{len(rows)} done; {have} with a size figure, {xh} x-height only, {len(done) - have - xh} neither")

if __name__ == "__main__":
    main((sys.argv[1] if sys.argv[1] in ("reparse", "retry") else int(sys.argv[1])) if len(sys.argv) > 1 else None)
