#!/usr/bin/env python3
"""shs_organise.py — arrange the extracted SHS signs into family folders under MUTCD 2023/SVGs.
Precedence when a code appears in several editions: 2024 releases > 2012 supplement > 2004 edition.
Families by code prefix: R7/R8 Parking; other R Regulatory; W20–W25, G20 Temporary Traffic Control; other W Warning;
S School; M Route Markers; D/E/I/G Guide; OM Object Markers; EM Emergency Management."""
import os, re, csv, shutil, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "USA", "Federal (MUTCD 2023)", "SVGs")
SOURCES = [("2004 Edition", ["Regulatory Signs", "Warning Signs", "Guide Signs", "School Signs", "Emergency Management Signs", "Object Markers"]),
           ("2012 Supplement", ["2012 Supplement"]),
           ("2024 Edition", ["2024 Releases 1-4", "2024 Release 5 Guide", "2024 Release 6 Regulatory", "2024 Release 6 Guide"])]
def family(code):
    c = code.upper(); m = re.match(r"([A-Z]+)(\d*)", c); fam, num = m.group(1), m.group(2)
    n = int(num) if num else 0
    if fam == "R": return "Parking Signs" if n in (7, 8) else "Regulatory Signs"
    if fam == "W": return "Temporary Traffic Control Signs" if 20 <= n <= 25 else "Warning Signs"
    if fam == "G": return "Temporary Traffic Control Signs" if n == 20 else "Guide Signs"
    if fam == "S": return "School Signs"
    if fam == "M": return "Route Markers"
    if fam in ("D", "E", "I"): return "Guide Signs"
    if fam == "OM": return "Object Markers"
    if fam == "EM": return "Emergency Management Signs"
    return "Other Signs"
def main():
    chosen = {}   # (code, name) -> (edition_rank, edition, src_path, row)
    rank = {"2004 Edition": 0, "2012 Supplement": 1, "2024 Edition": 2}
    for edition, folders in SOURCES:
        for f in folders:
            man = os.path.join(OUT, f, "_extract_manifest.csv")
            if not os.path.exists(man): continue
            for row in csv.reader(open(man)):
                code, name, fn = row[0], row[1], row[2]; key = (code, name)
                src = os.path.join(OUT, "intervene", f, fn[len("intervene/"):]) if fn.startswith("intervene/") else os.path.join(OUT, f, fn)
                if not os.path.exists(src): continue
                if key not in chosen or rank[edition] >= chosen[key][0]: chosen[key] = (rank[edition], edition, src, row)
    # a newer edition supersedes ALL variants of a code from an older edition
    newest = {}
    for (code, name), (r, ed, src, row) in chosen.items(): newest[code] = max(newest.get(code, 0), r)
    final = {k: v for k, v in chosen.items() if v[0] == newest[k[0]]}
    tmp = os.path.join(OUT, "_organised"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    rows = []
    for (code, name), (r, ed, src, row) in sorted(final.items()):
        fam = family(code); iv = "/intervene/" in src
        d = os.path.join(tmp, "intervene", fam) if iv else os.path.join(tmp, fam); os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, os.path.basename(src))
        if os.path.exists(dst): dst = dst[:-4] + f"_{ed.split()[0]}.svg"
        shutil.copy2(src, dst); rows.append([code, name, ("intervene/" if iv else "") + fam, os.path.basename(dst), ed, row[3], row[6]])
    for edition, folders in SOURCES:
        for f in folders: shutil.rmtree(os.path.join(OUT, f), ignore_errors=True)
    shutil.rmtree(os.path.join(OUT, "intervene"), ignore_errors=True)
    for fam in os.listdir(tmp): shutil.move(os.path.join(tmp, fam), os.path.join(OUT, fam))
    os.rmdir(tmp)
    iv = [r for r in rows if r[2].startswith("intervene/")]
    if iv:
        with open(os.path.join(OUT, "intervene", "INTERVENE_LIST.md"), "w") as fh:
            fh.write("# Signs needing a manual check\n\n")
            for r in iv: fh.write(f"- {r[2][len('intervene/'):]}/{r[3]} ({r[0]}, {r[4]}): {r[6]}\n")
    with open(os.path.join(OUT, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "edition", "drawn_size", "notes"]); w.writerows(rows)
    import collections; print(len(rows), "signs organised:", dict(collections.Counter(r[2] for r in rows)))
    print("by edition:", dict(collections.Counter(r[4] for r in rows)))
if __name__ == "__main__": main()
