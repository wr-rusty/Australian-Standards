#!/usr/bin/env python3
"""dedupe_pack.py — drop from a jurisdiction pack every sign whose code already exists in its base pack (the national
AS 1743 set for Australian states, the federal MUTCD set for US states): the SVG is deleted and the manifest row keeps
the code with a pointer to the base file, so the platform loads each sign once.
  python3 tools/dedupe_pack.py <pack_dir> <base_pack_dir>"""
import os, sys, csv, collections

def norm(c): return c.upper().replace(" ", "").strip()

def main(pack, base):
    base_rows = list(csv.DictReader(open(os.path.join(base, "SVGs", "MANIFEST.csv"))))
    base_files = {}
    for r in base_rows:
        f = r.get("file") or r.get("svg") or ""
        if f and norm(r["code"]) not in base_files: base_files[norm(r["code"])] = f
    man = os.path.join(pack, "SVGs", "MANIFEST.csv"); rows = list(csv.DictReader(open(man))); fields = list(rows[0].keys())
    removed = 0; codes = collections.Counter()
    for r in rows:
        key = norm(r["code"])
        if key in base_files and r["file"]:
            p = os.path.join(pack, "SVGs", r["family"], r["file"])
            if os.path.exists(p): os.remove(p); removed += 1
            codes[r["code"]] += 1
            r["file"] = ""; r["size"] = ""; r["notes"] = f"same code as the base pack: use {os.path.basename(base)}/SVGs/{base_files[key]}" + (f" (was: {r['notes']})" if r["notes"] else "")
    for d, _, fs in list(os.walk(os.path.join(pack, "SVGs"))):
        if not fs and not os.listdir(d): os.rmdir(d)
    with open(man, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"{os.path.basename(pack)}: {removed} SVGs removed ({len(codes)} codes shared with {os.path.basename(base)}); {sum(1 for r in rows if r['file'])} SVGs kept")

if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
