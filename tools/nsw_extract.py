#!/usr/bin/env python3
"""nsw_extract.py — Transport for NSW traffic sign register design plans into Australia/NSW/SVGs/<family>/<NAME>_<CODE>.svg
with MANIFEST.csv, via sheet_extract. Driven by Australia/NSW/REGISTER.csv (nsw_crawl.py).
Signs whose code also exists in the national AS 1743 set are still produced (NSW draws its own plans), and the manifest
says which are NSW-only ('n' suffix or a code absent from the national manifest).
  python3 tools/nsw_extract.py [limit]"""
import os, re, sys, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NSW = os.path.join(ROOT, "Australia", "NSW")
NATIONAL = os.path.join(ROOT, "Australia", "National (AS 1743)", "SVGs", "MANIFEST.csv")

def family(code):
    c = code.upper(); fam = re.match(r"[A-Z]+\d*", c); fam = fam.group(0) if fam else ""
    if fam.startswith("GE"): return "Freeway Signs"
    if fam == "G7": return "Service Signs"
    if fam == "G11": return "Tourist Signs"
    if fam.startswith("G"): return "Guide Signs"
    if fam in ("R5", "R6"): return "Parking Signs"
    if fam.startswith("R"): return "Regulatory Signs"
    if fam.startswith("W"): return "Warning Signs"
    if fam.startswith("T"): return "Temporary Signs"
    if fam.startswith("D"): return "Hazard Markers"
    if fam.startswith("S"): return "School Signs"
    return "Other Signs"

def national_codes():
    try: return {r["code"].upper().replace(" ", "") for r in csv.DictReader(open(NATIONAL))}
    except FileNotFoundError: return set()

def main(limit=None):
    out = os.path.join(NSW, "SVGs"); rows = []; seen = {}; nat = national_codes()
    reg = [r for r in csv.DictReader(open(os.path.join(NSW, "REGISTER.csv"))) if r["local"]]
    if limit: reg = reg[:limit]
    for i, r in enumerate(reg):
        code = (r["sign_no"] or os.path.splitext(os.path.basename(r["local"]))[0]).strip(); name = r["description"] or r["title"]
        fam = family(code); pdf = os.path.join(NSW, r["local"]); src = r["local"]
        try: signs = SE.extract_page(pdf, 0)
        except Exception as ex:
            rows.append([code, name, fam, "", "", f"extraction failed: {str(ex)[:120]}", src]); print("  !!", code, str(ex)[:100], flush=True); continue
        if not signs:
            rows.append([code, name, fam, "", "", "no drawing found on the sheet", src]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        nm = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")[:80] or "SIGN"; cd = code.replace(" ", "").replace("/", "-")
        nsw_only = "NSW-only code" if (cd.upper() not in nat) else "code also in the national AS 1743 set"
        for vi, sgn in enumerate(signs):
            svg, W, H = X.write_svg(sgn, fam)
            cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
            fn = f"{nm}_{cd}.svg" if vi == 0 and not cap else f"{nm}_{cap or 'VAR' + str(vi + 1)}_{cd}.svg"
            n = 2
            while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(cd) + r"\.svg$", f"_{n}_{cd}.svg", fn); n += 1
            seen[fn] = 1; open(os.path.join(folder, fn), "w").write(svg)
            rows.append([code, name, fam, fn, f"{W:.0f}x{H:.0f} mm", sgn["note"] + "; " + nsw_only, src])
        if i % 50 == 0: print(f"{i + 1}/{len(reg)} {code} {name[:40]}", flush=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
