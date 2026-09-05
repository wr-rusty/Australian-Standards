#!/usr/bin/env python3
"""sa_extract.py — South Australian Standard Road Sign Index PDFs into Australia/SA/SVGs/<series>/<NAME>_<CODE>.svg with
MANIFEST.csv, via sheet_extract. The sign's size comes from the register (the sheets' dimension figures are outlined),
so the drawing is scaled to the register's first listed size for its code.
  python3 tools/sa_extract.py [limit]"""
import os, re, sys, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SA = os.path.join(ROOT, "Australia", "SA")

def main(limit=None):
    out = os.path.join(SA, "SVGs"); rows = []; seen = {}; sheet_of = {}
    reg = [r for r in csv.DictReader(open(os.path.join(SA, "REGISTER.csv"))) if r["local"] and r["hidden"] != "True"]
    if limit: reg = reg[:limit]
    import hashlib
    for i, r in enumerate(reg):
        digest = hashlib.md5(open(os.path.join(SA, r["local"]), "rb").read()).hexdigest()
        if digest in sheet_of:   # the same sheet serves several register entries (symbol sets): drawn once
            rows.append([(r["codes"].split(" | ") or [""])[0], r["name"], "", "", "", f"same sheet as {sheet_of[digest]}; its drawings are filed there (symbols not told apart on an all-outlined sheet — check)", r["local"]]); continue
        sheet_of[digest] = (r["codes"].split(" | ") or [""])[0] or f"SA{r['id']}"
        codes = [c for c in r["codes"].split(" | ") if c]; sizes = [s for s in r["sizes"].split(" | ") if s]
        code = codes[0] if codes else f"SA{r['id']}"; name = r["name"]
        fam = re.sub(r"^[A-Z]+\d*\s*", "", r["series"]).title() or "Other"; fam = " ".join(w if w.isupper() else w.capitalize() for w in r["series"].title().split())
        pdf = os.path.join(SA, r["local"]); src = r["local"]
        try: signs = SE.extract_page(pdf, 0)
        except Exception as ex:
            rows.append([code, name, fam, "", "", f"extraction failed: {str(ex)[:120]}", src]); print("  !!", code, str(ex)[:100], flush=True); continue
        if not signs:
            rows.append([code, name, fam, "", "", "no drawing found on the sheet", src]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        nm = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")[:80] or "SIGN"
        # a sheet drawing several codes (symbol sets): pair drawings with codes in reading order
        paired = len(codes) > 1 and len(signs) == len(codes)
        if paired: signs = sorted(signs, key=lambda s: (round(s["panel"].y0 / 40), s["panel"].x0))
        for vi, sgn in enumerate(signs):
            note = sgn["note"]
            greys = [f for f in sgn["fills"] if abs(f["fill"][0] - 0.6) < 0.05 and abs(f["fill"][1] - 0.6) < 0.05 and abs(f["fill"][2] - 0.6) < 0.05]
            for f in greys: f["fill"] = (1.0, 1.0, 1.0)     # SA sheets draw white retroreflective areas in 60% grey (colour legend)
            if greys: note = (note + "; " if note else "") + "60% grey on the sheet rendered as white (sheet's colour legend convention)"
            code = codes[vi] if paired else (codes[0] if codes else f"SA{r['id']}"); cd = code.replace(" ", "").replace("/", "-")
            size_i = sizes[vi] if paired and vi < len(sizes) else (sizes[0] if sizes else "")
            m = re.match(r"(\d+)x(\d+)", size_i) if size_i else None
            if m and (vi == 0 or paired):   # register size wins over the sheet's (outlined) figures
                w_mm, h_mm = float(m.group(1)), float(m.group(2)); pr = sgn["panel"]
                land = pr.width >= pr.height; sw = max(w_mm, h_mm) if land else min(w_mm, h_mm)
                sgn["scale"] = (sw / pr.width) / 25.4
                note = f"size from the register ({size_i} mm{'; other listed sizes: ' + ', '.join(sizes[1:]) if len(sizes) > 1 and not paired else ''})" + ("; drawings paired with codes in reading order" if paired else "")
                if abs(pr.height * sw / pr.width - (min(w_mm, h_mm) if land else max(w_mm, h_mm))) > 0.06 * max(w_mm, h_mm): note += "; drawn proportions differ from the register size — check"
            svg, W, H = X.write_svg(sgn, fam)
            cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
            fn = f"{nm}_{cd}.svg" if (vi == 0 or paired) and not cap else f"{nm}_{cap or 'VAR' + str(vi + 1)}_{cd}.svg"
            n = 2
            while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(cd) + r"\.svg$", f"_{n}_{cd}.svg", fn); n += 1
            seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
            rows.append([code, name, fam, fn, f"{W:.0f}x{H:.0f} mm", note + ("; codes on this sheet: " + ", ".join(codes) if len(codes) > 1 and not paired else ""), src])
        if i % 50 == 0: print(f"{i + 1}/{len(reg)} {code} {name[:40]}", flush=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
