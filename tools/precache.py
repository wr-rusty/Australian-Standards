#!/usr/bin/env python3
"""precache.py — convert every sheet of the NSW, QLD and SA packs with Inkscape in parallel (fills sheet_extract's cache)
so the drivers then run quickly.  python3 tools/precache.py [workers]"""
import os, sys, csv, glob, subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def jobs():
    out = []
    nsw = os.path.join(ROOT, "Australia", "NSW")
    for r in csv.DictReader(open(os.path.join(nsw, "REGISTER.csv"))):
        if r["local"]: out.append((os.path.join(nsw, r["local"]), 0))
    sa = os.path.join(ROOT, "Australia", "SA")
    for r in csv.DictReader(open(os.path.join(sa, "REGISTER.csv"))):
        if r["local"] and r["hidden"] != "True": out.append((os.path.join(sa, r["local"]), 0))
    import qld_extract as Q, pymupdf
    for f in sorted(glob.glob(os.path.join(Q.SRC, "**", "*.pdf"), recursive=True)):
        if any(s in f.lower() for s in Q.SKIP_DIRS): continue
        out.append((f, 0))
    qs = os.path.join(ROOT, "Australia", "QLD", "Original PDFs", "q-series.pdf")
    if os.path.exists(qs):
        for p in range(pymupdf.open(qs).page_count): out.append((qs, p))
    return out

def one(job):
    import sheet_extract as SE
    try:
        SE.paths_pdf(*job)
        if os.environ.get("SHEET_MEMO"): SE.extract_page(*job)       # memoised extraction too
        return None
    except Exception as ex: return f"{job}: {ex}"

if __name__ == "__main__":
    js = jobs(); print(len(js), "sheets", flush=True); n = 0
    with ProcessPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as ex:
        for res in as_completed([ex.submit(one, j) for j in js]):
            n += 1; r = res.result()
            if r: print("  !!", r, flush=True)
            if n % 100 == 0: print(n, flush=True)
    print("done", flush=True)
