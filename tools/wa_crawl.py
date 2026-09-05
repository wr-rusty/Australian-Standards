#!/usr/bin/env python3
"""wa_crawl.py — crawl the Main Roads WA Signs Index (technical library) and download every sign's PDF and DWG.

The library is served by /api/documents/search?nodeid=<node>; the Signs Index node tree (series such as
'Speed Series (MR-RS)') comes from the same API. Writes Australia/WA/REGISTER.csv (series, title, summary with size and
MR code, files) and downloads into Australia/WA/Original PDFs/<Category>/<Series>/.
  python3 tools/wa_crawl.py"""
import os, re, sys, csv, json, time, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = os.path.join(ROOT, "Australia", "WA")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0 Safari/537.36"
API = "https://www.mainroads.wa.gov.au/api/documents/search"
SIGNS_INDEX = "11489_745"

def get_json(url):
    for attempt in range(3):
        r = subprocess.run(["curl", "-s", "-A", UA, "-H", "Accept: application/json", url], capture_output=True, text=True)
        try: return json.loads(r.stdout)
        except json.JSONDecodeError: time.sleep(3)
    raise RuntimeError("no JSON from " + url)

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0: return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = subprocess.run(["curl", "-sL", "-A", UA, "-o", dest, "-w", "%{http_code}", url], capture_output=True, text=True); time.sleep(0.3)
    if r.stdout.strip() != "200" or os.path.getsize(dest) == 0:
        if os.path.exists(dest): os.remove(dest)
        return False
    return True

def leaves(node, path):
    kids = node.get("children") or []
    if not kids: yield node, path
    for k in kids: yield from leaves(k, path + [node["name"]])

def main():
    tree = get_json(f"{API}?q=&take=1&page=1&sectionFilter=731")["nodeTree"]
    def find(nodes):
        for n in nodes:
            if n["id"] == SIGNS_INDEX: return n
            r = find(n.get("children") or [])
            if r: return r
    root = find(tree)
    if not root: sys.exit("Signs Index node not found")
    rows = []
    for leaf, path in leaves(root, []):
        cat = " / ".join(p for p in path[1:]) or leaf["name"]; series = leaf["name"]
        page = 1; n = 0
        while True:
            d = get_json(f"{API}?q=&take=50&page={page}&sectionFilter=731&sort=atoz&nodeid={leaf['id']}")
            items = d.get("items") or []
            for it in items:
                summary = re.sub(r"\s+", " ", it.get("summary") or "").strip()
                m = re.search(r"\b(MR-[A-Z]+-\d+[A-Z]?|MMS-[A-Z]+-\d+[A-Z]?)\b", " ".join([it["title"], summary] + [f.get("name", "") for f in it.get("files", [])]))
                code = m.group(1) if m else ""
                size = re.search(r"Size:?\s*([\d\s]+x[\d\s]+)", summary); size = size.group(1).replace(" ", "") if size else ""
                folder = os.path.join(WA, "Original PDFs", re.sub(r"[^\w\- ]+", "", (path[1] if len(path) > 1 else leaf["name"])).strip(), re.sub(r"[^\w\- ]+", "", series).strip())
                local = []
                for f in it.get("files", []):
                    href = f.get("href"); ft = (f.get("filetype") or "").lower()
                    if not href or ft not in ("pdf", "dwg", "dxf"): continue
                    fn = os.path.basename(href.split("?")[0]); dest = os.path.join(folder, fn)
                    if download(href, dest): local.append(os.path.relpath(dest, WA))
                    else: print("  !!", it["title"][:50], href[-60:], flush=True)
                rows.append({"category": path[1] if len(path) > 1 else "", "series": series, "node": leaf["id"], "title": it["title"], "code": code, "size": size, "summary": summary[:200],
                             "type": it.get("documentType", ""), "updated": it.get("lastUpdated", ""), "files": " | ".join(f.get("href", "") for f in it.get("files", [])), "local": " | ".join(local)})
                n += 1
            if len(items) < 50: break
            page += 1
        print(f"{series}: {n}", flush=True)
    with open(os.path.join(WA, "REGISTER.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("done", len(rows), "items;", sum(1 for r in rows if r["local"]), "with files")

if __name__ == "__main__": main()
