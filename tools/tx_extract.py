#!/usr/bin/env python3
"""tx_extract.py — Standard Highway Sign Designs for Texas (TxDOT SHSD 2012 rev 4, section PDFs) into
USA/Texas/SVGs/<family>/ with MANIFEST.csv. The sheets follow the FHWA SHS layout, so shs_extract does the work with a
wider code pattern (R1-2bTP, R7-107R (L,DBL)) and 11 pt labels.
  python3 tools/tx_extract.py [section]"""
import os, re, sys, csv, glob, collections
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X, shs_organise as O
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TX = os.path.join(ROOT, "USA", "Texas")
X.CODE_RE = re.compile(r"^([A-Z]{1,2}\d{0,2}-\d{1,3}[a-zA-Z]{0,3}(?:\s?[LRVHC])?(?:\s?\([^)]*\))?)$"); X.LABEL_MIN_SIZE = 11

def main(section=None):
    out = os.path.join(TX, "SVGs"); rows = []; seen = {}
    pdfs = sorted(glob.glob(os.path.join(TX, "Original PDFs", "shsd-2012-section*.pdf")), key=lambda f: int(re.search(r"section(\d+)", f).group(1)))
    if section: pdfs = [f for f in pdfs if f.endswith(f"section{section}.pdf")]
    for pdf in pdfs:
        doc = pymupdf.open(pdf); sec = re.search(r"section(\d+)", pdf).group(1); n = 0
        for pno in range(len(doc)):
            try: signs = X.extract_page(doc, pno, "Texas")
            except Exception as ex: print("  !!", sec, pno + 1, str(ex)[:80], flush=True); continue
            for s in signs:
                code = s["code"].replace(" ", ""); fam = O.family(code)
                svg, W, H = X.write_svg(s, fam)
                name = re.sub(r"[^A-Z0-9]+", "_", s["name"].upper()).strip("_") or "SIGN"
                variant = s.get("variant", "")
                fn = f"{name}_{variant}_{code}.svg" if variant else f"{name}_{code}.svg"; fn = fn.replace("(", "").replace(")", "").replace(",", "-")
                k = 2
                while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(code.replace("(", "").replace(")", "").replace(",", "-")) + r"\.svg$", f"_{k}_{code}.svg", fn); k += 1
                seen[fn] = 1; folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
                if s.get("intervene"): folder = os.path.join(out, "intervene", fam); os.makedirs(folder, exist_ok=True)
                open(os.path.join(folder, fn), "w").write(svg); n += 1
                rows.append([code, s["name"], ("intervene/" if s.get("intervene") else "") + fam, fn, f"{W/25.4:.1f}x{H/25.4:.1f} in", s.get("intervene") or s["note"], f"Original PDFs/shsd-2012-section{sec}.pdf#page={pno + 1}"])
        print(f"section {sec}: {len(doc)} pages, {n} signs", flush=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "signs;", dict(collections.Counter(r[2] for r in rows)))

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else None)
