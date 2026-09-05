#!/usr/bin/env python3
"""nz_crawl.py — crawl the NZTA sign-specifications register and download every sign's files.

The site sits behind Imperva; a session cookie from a browser that has passed the check is required:
  NZTA_COOKIE='incap_ses_...=...' NZTA_UA='Mozilla/5.0 ...' python3 tools/nz_crawl.py
Writes NZ TCD Manual/REGISTER.csv (one row per sign: category, view id, rule, code, MoTSaM, title, updated,
dimensions, colours, files) and downloads the EPS and non-labelled GIF into NZ TCD Manual/Original EPS/<category>/.
HTML is cached under the scratch dir so re-runs do not re-fetch."""
import os, re, sys, csv, time, subprocess, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NZ = os.path.join(ROOT, "New Zealand", "National (TCD Manual)")
BASE = "https://www.nzta.govt.nz"
REG = "/resources/traffic-control-devices-manual/sign-specifications"
CATS = {677: "Regulatory", 734: "Permanent warning", 835: "Temporary warning", 923: "Symbol", 924: "Parking",
        966: "General advisory", 1031: "Motorist service", 1032: "Tourist", 1033: "Guide", 1034: "Arrow"}
CACHE = os.environ.get("NZTA_CACHE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".nz_cache"))
COOKIE, UA = os.environ["NZTA_COOKIE"], os.environ["NZTA_UA"]

def get(path, binary=False, dest=None):
    url = BASE + path if path.startswith("/") else path
    key = re.sub(r"[^A-Za-z0-9._-]+", "_", path)[-150:]
    cpath = dest or os.path.join(CACHE, key)
    if os.path.exists(cpath) and os.path.getsize(cpath) > 0:
        return None if dest else open(cpath, "rb").read().decode("utf-8", "replace")
    os.makedirs(os.path.dirname(cpath), exist_ok=True)
    r = subprocess.run(["curl", "-sL", "-A", UA, "-H", f"Cookie: {COOKIE}", "-o", cpath, "-w", "%{http_code}", url], capture_output=True, text=True)
    time.sleep(0.4)
    if r.stdout.strip() != "200":
        if os.path.exists(cpath): os.remove(cpath)
        raise RuntimeError(f"{r.stdout.strip()} for {url}")
    return None if dest else open(cpath, "rb").read().decode("utf-8", "replace")

def text(s): return H.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")
def clean(s): return re.sub(r"\s+", " ", text(s)).strip()

def listing(cid):
    rows = []
    for start in range(0, 400, 10):
        page = get(f"{REG}?category={cid}&start={start}")
        body = page.split("<tbody", 1)[1] if "<tbody" in page else ""
        trs = re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S)
        if not trs: break
        for tr in trs:
            tds = [clean(td) for td in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            m = re.search(r"/view/(\d+)", tr)
            if m and len(tds) >= 6: rows.append({"category": CATS[cid], "id": m.group(1), "rule": tds[0], "code": tds[2], "motsam": tds[3], "title": tds[4], "updated": tds[5]})
        if len(trs) < 10: break
    return rows

def entry(vid):
    page = get(f"{REG}/view/{vid}")
    main = page.split("<main", 1)[1] if "<main" in page else page
    files = re.findall(r'href="([^"]+\.(?:eps|pdf|dxf|dwg|zip|ai|svg|gif|png))"', main, re.I)
    files = [f if f.startswith("http") else BASE + f for f in dict.fromkeys(files)]
    def section(name):
        m = re.search(rf"{name}\s*</h\d>(.*?)(?:<h\d|</main)", main, re.S)
        if not m: return ""
        items = re.findall(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", m.group(1), re.S)
        return "; ".join(f"{clean(k)} {clean(v)}" for k, v in items) if items else clean(m.group(1))[:400]
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", main, re.S)
    return {"heading": clean(heading.group(1)) if heading else "", "dimensions": section("Dimensions"), "colours": section("Colours"), "files": files}

def main():
    os.makedirs(NZ, exist_ok=True); rows = []
    for cid in CATS:
        rs = listing(cid); print(CATS[cid], len(rs), flush=True); rows += rs
    out = []
    for i, r in enumerate(rows):
        try: e = entry(r["id"])
        except RuntimeError as ex: print("  !!", r["code"], ex, flush=True); e = {"heading": "", "dimensions": "", "colours": "", "files": []}
        r.update(e); local = []
        folder = os.path.join(NZ, "Original EPS", r["category"]); os.makedirs(folder, exist_ok=True)
        for f in e["files"]:
            fn = os.path.basename(f)
            if not re.search(r"\.(eps|pdf|dxf|dwg|zip|ai|svg)$", fn, re.I) and "no-label" not in fn.lower() and "nolabel" not in fn.lower(): continue
            dest = os.path.join(folder, fn)
            try: get(f, dest=dest); local.append(os.path.relpath(dest, NZ))
            except RuntimeError as ex: print("  !!", r["code"], ex, flush=True)
        r["local"] = " | ".join(local); r["files"] = " | ".join(e["files"]); out.append(r)
        if i % 25 == 0: print(f"{i + 1}/{len(rows)} {r['code']} {r['title'][:40]}", flush=True)
    with open(os.path.join(NZ, "REGISTER.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["category", "id", "rule", "code", "motsam", "title", "updated", "heading", "dimensions", "colours", "files", "local"])
        w.writeheader(); w.writerows(out)
    print("done", len(out))

if __name__ == "__main__": main()
