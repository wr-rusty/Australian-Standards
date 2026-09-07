#!/usr/bin/env python3
"""uk_crawl.py — download the DfT 'Traffic signs working drawings (TSRGD 2016)' PDFs, one per diagram, from the fifteen
schedule publication pages on gov.uk, into Processing/United Kingdom/National (TSRGD 2016)/Original PDFs/Schedule NN/,
with REGISTER.csv (schedule, part, item, diagram, title, url, local).  python3 tools/uk_crawl.py"""
import os, re, csv, html as H, subprocess, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UK = os.path.join(ROOT, "Processing", "United Kingdom", "National (TSRGD 2016)")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0 Safari/537.36"
def get(url, dest=None):
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0: return True
    args = ["curl", "-sL", "-A", UA, url] + (["-o", dest] if dest else [])
    r = subprocess.run(args, capture_output=True, text=not dest); time.sleep(0.2)
    return (os.path.exists(dest) and os.path.getsize(dest) > 0) if dest else r.stdout
def main():
    rows = []
    for n in range(2, 17):
        page = get(f"https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-{n}")
        seen = set()
        for m in re.finditer(r'<a[^>]+href="(https://assets\.publishing\.service\.gov\.uk/[^"]+\.pdf)"[^>]*>(.*?)</a>', page, re.S):
            url, title = m.group(1), re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
            if url in seen: continue
            seen.add(url)
            fn = os.path.basename(url); mm = re.search(r"schedule-(\d+)-part-(\d+)-item-(\d+)-(.+)\.pdf", fn)
            sched, part, item, diag = (mm.group(1), mm.group(2), mm.group(3), mm.group(4)) if mm else (f"{n:02d}", "", "", fn[:-4])
            folder = os.path.join(UK, "Original PDFs", f"Schedule {int(sched):02d}"); os.makedirs(folder, exist_ok=True)
            dest = os.path.join(folder, fn); ok = get(url, dest)
            rows.append({"schedule": sched, "part": part, "item": item, "diagram": diag, "title": title, "url": url, "local": os.path.relpath(dest, UK) if ok else ""})
        print(f"schedule {n}: {len(seen)} drawings", flush=True)
    with open(os.path.join(UK, "REGISTER.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("done", len(rows), "with files", sum(1 for r in rows if r["local"]))
if __name__ == "__main__": main()
