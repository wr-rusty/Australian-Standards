#!/usr/bin/env python3
"""nz_sweep.py — sweep the NZTA sign-specifications register by entry id (view/1 … view/N) and add every entry the
category listings did not show (the core regulatory signs: speed limits, stop, give way …) to REGISTER.csv, downloading
their EPS and non-labelled GIF. Needs NZTA_COOKIE / NZTA_UA from a browser session that has passed the Imperva check.
  python3 tools/nz_sweep.py [max_id]"""
import os, re, sys, csv, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nz_crawl as C
CAT_BY_RULE = {"R": "Regulatory", "W": "Permanent warning", "T": "Temporary warning", "A": "General advisory", "M": "Motorist service",
               "V": "Tourist", "G": "Guide", "S": "Symbol", "P": "Parking"}
CAT_BY_CODE = {"RS": "Regulatory", "RG": "Regulatory", "RP": "Parking", "RL": "Regulatory", "RJ": "Regulatory", "RD": "Regulatory", "RB": "Regulatory", "RH": "Regulatory",
               "WB": "Permanent warning", "WC": "Permanent warning", "PW": "Permanent warning", "TW": "Temporary warning", "AB": "General advisory", "AU": "General advisory",
               "MS": "Motorist service", "VI": "Tourist", "VJ": "Tourist", "GA": "Guide", "GB": "Guide", "GC": "Guide", "ST": "Symbol", "SG": "Symbol", "SA": "Symbol"}

def parse(vid):
    page = C.get(f"{C.REG}/view/{vid}")
    if "traffic-sign-detail" not in page: return None
    main = page.split("<main", 1)[1] if "<main" in page else page
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", "", main, flags=re.S); txt = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", txt)))
    m = re.search(r"Back to traffic signs\s*(.*?)\s*(?:All dimensions|Details)", txt); title = (m.group(1) if m else "").strip()
    title, _, variant = title.partition(" — ")
    def field(name):
        m = re.search(rf"\b{name}\s+(.+?)\s+(?=Code\b|Rule\b|MoTSaM\b|EPS image\b|Non-labeled image\b|Last updated\b|Dimensions\b|Colours\b)", txt)
        return m.group(1).strip() if m else ""
    code, rule, motsam, updated = field("Code"), field("Rule"), field("MoTSaM"), field("Last updated")
    dims = re.search(r"Dimensions\s+(.*?)\s+Colours", txt); cols = re.search(r"Colours\s+(.*?)\s+(?:About Careers|Back to traffic signs|$)", txt)
    files = re.findall(r'href="([^"]+\.(?:eps|pdf|dxf|dwg|zip|ai|svg|gif|png))"', main, re.I)
    files = [f if f.startswith("http") else C.BASE + f for f in dict.fromkeys(files)]
    cat = CAT_BY_CODE.get(code[:2].upper()) or CAT_BY_RULE.get(rule[:1].upper(), "Regulatory")
    return {"category": cat, "id": str(vid), "rule": rule, "code": code, "motsam": motsam, "title": (title + (f" ({variant})" if variant and variant.lower() != "standard" else "")).strip(),
            "updated": updated, "heading": title, "dimensions": dims.group(1).strip() if dims else "", "colours": cols.group(1).strip() if cols else "", "files": " | ".join(files), "local": ""}

def main(max_id=1400):
    reg_path = os.path.join(C.NZ, "REGISTER.csv"); rows = list(csv.DictReader(open(reg_path))); have = {r["id"] for r in rows}
    fields = list(rows[0].keys()); added = 0
    for vid in range(1, max_id + 1):
        if str(vid) in have: continue
        try: e = parse(vid)
        except RuntimeError as ex: print("  !!", vid, ex, flush=True); continue
        if not e: continue
        local = []; folder = os.path.join(C.NZ, "Original EPS", e["category"]); os.makedirs(folder, exist_ok=True)
        for url in e["files"].split(" | "):
            if not url: continue
            fn = os.path.basename(url.split("?")[0]); dest = os.path.join(folder, fn)
            try: C.get(url, dest=dest); local.append(os.path.relpath(dest, C.NZ))
            except RuntimeError as ex: print("  !!", vid, fn, ex, flush=True)
        e["local"] = " | ".join(local); rows.append(e); added += 1
        print(f"{vid}: {e['code']} {e['rule']} {e['title'][:50]} [{e['category']}] files={len(local)}", flush=True)
    with open(reg_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print("added", added, "entries; register now", len(rows), flush=True)

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else 1400)
