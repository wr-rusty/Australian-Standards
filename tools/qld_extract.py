#!/usr/bin/env python3
"""qld_extract.py — Queensland TC signs (TMR 'officially approved' traffic control signs) into
Australia/QLD/SVGs/<category>/<NAME>_<CODE>.svg with MANIFEST.csv, via sheet_extract. Superseded sheets are skipped.
  python3 tools/qld_extract.py [limit]"""
import os, re, sys, csv, glob, collections, traceback
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QLD = os.path.join(ROOT, "Australia", "QLD")
SRC = glob.glob(os.path.join(QLD, "Original PDFs", "TC signs", "TC Signs_*"))[0]
SKIP_DIRS = ("superseded", "tc signs index", "qld govt logo", "signing & pavement marking layouts")

def title_block(pdf):
    """(code, type line, name) from the sheet's title block: the largest texts below the drawing region."""
    spans, F = SE.sheet_spans(pdf); region = SE.drawing_region(F, spans)
    tb = [s for s in spans if s["bbox"].y0 > region.y1 and s["size"] >= 13 and not any(w.lower() in s["text"].lower() for w in ("approved", "issued", "queensland", "department", "division", "section", "principal", "director"))]
    code = next((s["text"].strip() for s in tb if re.fullmatch(r"(TC|ETM|ENV|Q)?[A-Z]*\d{2,5}(_\d+)?[A-Z]?", s["text"].strip())), "")
    lines = sorted([s for s in tb if s["text"].strip() != code and not re.fullmatch(r"[A-Z]", s["text"].strip())], key=lambda s: (round(s["bbox"].y0), s["bbox"].x0))
    texts = [s["text"].strip() for s in lines]
    kind = texts[0] if texts else ""
    quoted = " ".join(t for t in texts if "“" in t or "”" in t or '"' in t).replace("“", "").replace("”", "").replace('"', "").strip()
    name = quoted or " ".join(texts[1:]) or kind
    return code, kind, name

def main(limit=None):
    out = os.path.join(QLD, "SVGs"); rows = []; seen = {}
    files = sorted(glob.glob(os.path.join(SRC, "*", "*.pdf")))
    files = [f for f in files if os.path.basename(os.path.dirname(f)).lower() not in SKIP_DIRS]
    if limit: files = files[:limit]
    for i, f in enumerate(files):
        cat = os.path.basename(os.path.dirname(f)); fam = " ".join(w.capitalize() for w in re.split(r"[\s_]+", cat.replace("&", "and"))).replace(",", "")
        stem = os.path.splitext(os.path.basename(f))[0]
        try:
            code, kind, name = title_block(f); code = (code or stem).upper().replace("_1", ""); code = re.sub(r"_\d+$", "", code)
            doc = pymupdf.open(f)
            if len(doc) > 1: pass
            signs = SE.extract_page(f, 0)
        except Exception as ex:
            rows.append([stem.upper(), "", fam, "", "", f"extraction failed: {str(ex)[:120]}", os.path.relpath(f, QLD)]); print("  !!", stem, str(ex)[:100], flush=True); continue
        if not signs:
            rows.append([code, name, fam, "", "", "no drawing found on the sheet", os.path.relpath(f, QLD)]); continue
        if signs[0]["superseded"]:
            rows.append([code, name, fam, "", "", "sheet stamped SUPERSEDED; not produced", os.path.relpath(f, QLD)]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        nm = re.sub(r"[^A-Z0-9]+", "_", (name or kind or stem).upper()).strip("_")[:80] or "SIGN"
        for vi, sgn in enumerate(signs):
            svg, W, H = X.write_svg(sgn, fam)
            cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
            fn = f"{nm}_{code}.svg" if vi == 0 and not cap else f"{nm}_{cap or 'VAR' + str(vi + 1)}_{code}.svg"
            n = 2
            while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(code) + r"\.svg$", f"_{n}_{code}.svg", fn); n += 1
            seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
            rows.append([code, name, fam, fn, f"{W:.0f}x{H:.0f} mm", sgn["note"] + (f"; type: {kind}" if kind else ""), os.path.relpath(f, QLD)])
        if i % 50 == 0: print(f"{i + 1}/{len(files)} {code} {name[:40]}", flush=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
