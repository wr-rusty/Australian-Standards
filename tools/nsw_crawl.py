#!/usr/bin/env python3
"""nsw_crawl.py — crawl the Transport for NSW traffic sign register and download every sign design plan.

  python3 tools/nsw_crawl.py
Writes Australia/NSW/REGISTER.csv (sign no, description, standard sign?, use by council, legislative reference,
technical references, image, design plan URL, local file) and downloads the design plan PDFs into
Australia/NSW/Original PDFs/. HTML is cached under NSW_CACHE (default .nsw_cache/) so re-runs do not re-fetch."""
import os, re, sys, csv, time, subprocess, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NSW = os.path.join(ROOT, "Australia", "NSW")
BASE = "https://www.transport.nsw.gov.au"
REG = "/operations/roads-and-waterways/traffic-signs"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0 Safari/537.36"
CACHE = os.environ.get("NSW_CACHE", os.path.join(ROOT, ".nsw_cache"))

def get(path, dest=None):
    url = BASE + path if path.startswith("/") else path
    cpath = dest or os.path.join(CACHE, re.sub(r"[^A-Za-z0-9._-]+", "_", path)[-150:])
    if os.path.exists(cpath) and os.path.getsize(cpath) > 0:
        return None if dest else open(cpath, "rb").read().decode("utf-8", "replace")
    os.makedirs(os.path.dirname(cpath), exist_ok=True)
    for attempt in range(3):
        r = subprocess.run(["curl", "-sL", "-A", UA, "-o", cpath, "-w", "%{http_code}", url], capture_output=True, text=True)
        time.sleep(0.3)
        if r.stdout.strip() == "200": break
        time.sleep(3)
    else:
        if os.path.exists(cpath): os.remove(cpath)
        raise RuntimeError(f"{r.stdout.strip()} for {url}")
    return None if dest else open(cpath, "rb").read().decode("utf-8", "replace")

def clean(s): return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def listing():
    slugs = []
    for page in range(0, 400):
        htm = get(f"{REG}?page={page}")
        found = list(dict.fromkeys(re.findall(r'href="/operations/roads-and-waterways/traffic-signs/([^"?#]+)"', htm)))
        if not found: break
        new = [s for s in found if s not in slugs]
        if not new: break
        slugs += new
        print(f"page {page}: {len(new)} signs (total {len(slugs)})", flush=True)
    return slugs

def entry(slug):
    htm = get(f"{REG}/{slug}")
    main = re.search(r"<main.*?</main>", htm, re.S); main = main.group(0) if main else htm
    txt = clean(re.sub(r"<script.*?</script>|<style.*?</style>", "", main, flags=re.S))
    def field(label, nxt):
        m = re.search(re.escape(label) + r"\s*(.*?)\s*(?=" + "|".join(re.escape(n) for n in nxt) + r")", txt)
        return m.group(1).strip() if m else ""
    labels = ["Sign No:", "Descriptions", "Standard sign?", "Use by council", "Legislative Reference", "Primary Technical Reference", "Additional Primary Technical References", "Sign Design Image", "Notes:", "Sign Design Plan", "Share via"]
    def after(label):
        i = labels.index(label); return field(label, labels[i + 1:] or ["Share via"])
    title = re.search(r"<h1[^>]*>(.*?)</h1>", main, re.S)
    pdf = re.findall(r'href="([^"]+/signage/trafficsigns/pdf/[^"]+\.pdf)"', main, re.I)
    img = re.findall(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', main)
    img = [s for s, a in img if "trafficsigns" in s or "sign" in a.lower()]
    return {"slug": slug, "title": clean(title.group(1)) if title else "", "sign_no": after("Sign No:"), "description": after("Descriptions"),
            "standard": after("Standard sign?"), "council": after("Use by council"), "legislation": after("Legislative Reference"),
            "reference": after("Primary Technical Reference"), "references2": after("Additional Primary Technical References"),
            "notes": after("Notes:"), "plan": after("Sign Design Plan"), "pdf": (BASE + pdf[0] if pdf[0].startswith("/") else pdf[0]) if pdf else "", "image": img[0] if img else ""}

def main():
    os.makedirs(os.path.join(NSW, "Original PDFs"), exist_ok=True)
    slugs = listing(); out = []
    for i, slug in enumerate(slugs):
        try: e = entry(slug)
        except RuntimeError as ex: print("  !!", slug, ex, flush=True); e = {"slug": slug, "pdf": ""}
        local = ""
        if e.get("pdf"):
            fn = os.path.basename(e["pdf"].split("?")[0]); dest = os.path.join(NSW, "Original PDFs", fn)
            try: get(e["pdf"], dest=dest); local = os.path.relpath(dest, NSW)
            except RuntimeError as ex: print("  !!", slug, ex, flush=True)
        e["local"] = local; out.append(e)
        if i % 50 == 0: print(f"{i + 1}/{len(slugs)} {e.get('sign_no', '')} {e.get('description', '')[:40]}", flush=True)
    keys = ["sign_no", "description", "title", "standard", "council", "legislation", "reference", "references2", "notes", "plan", "image", "pdf", "local", "slug"]
    with open(os.path.join(NSW, "REGISTER.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(out)
    print("done", len(out), "signs;", sum(1 for e in out if e["local"]), "plans downloaded")

if __name__ == "__main__": main()
