"""vec.py — the sheet PDF's own vectors.
  vec.py list CODE [minsize_px]          drawings on the page: index, type, fill, stroke, bbox in 200-dpi px
  vec.py sym CODE symbol_id i,j,k[:colour] [i,j:colour ...] [--stroke]   write tools/symbols/<id>.svg from those items (px units), nonzero-normalised
CODE = Q-series code as in the title block (W5-Q11, W5-Q18_1) or p<pageindex>, or a TC pdf path."""
import sys, os, json, re, glob
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixwind import fix
V = os.path.dirname(os.path.abspath(__file__)); K = 200 / 72
ROOT = "/Users/russell/Local/GitHub/Australian-Standards"
def page_for(code):
    if code.lower().endswith(".pdf") or "@" in code:
        path, _, pg = code.partition("@"); return pymupdf.open(path)[int(pg or 0)]
    if code.startswith("TC"):
        import render
        base, _, pg = code.partition("_p")
        return pymupdf.open(render.find(base))[int(pg or 1) - 1]
    doc = pymupdf.open(os.path.join(ROOT, "Processing/Australia/QLD/Original PDFs/q-series.pdf"))
    if re.fullmatch(r"p\d+", code): return doc[int(code[1:])]
    idx = json.load(open(V + "/qidx.json"))
    for i, c in idx.items():
        if c == code: return doc[int(i)]
    raise SystemExit("no page for " + code)
def hexc(c): return "-" if c is None else "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)
def pts(d, M):
    """subpaths of a drawing as lists of segments in px"""
    subs = []; cur = None; last = None
    def P(p): q = pymupdf.Point(p) * M; return (q.x * K, q.y * K)
    for it in d["items"]:
        if it[0] == "re":
            r = it[1]; q = [P(r.tl), P(r.tr), P(r.br), P(r.bl)]
            if len(it) > 2 and it[2] < 0: q = q[::-1]
            subs.append([("M", q[0]), ("L", q[1]), ("L", q[2]), ("L", q[3])]); cur = None; last = None; continue
        if it[0] == "qu":
            qd = it[1]; q = [P(qd.ul), P(qd.ur), P(qd.lr), P(qd.ll)]
            subs.append([("M", q[0]), ("L", q[1]), ("L", q[2]), ("L", q[3])]); cur = None; last = None; continue
        a = P(it[1])
        if cur is None or last is None or abs(a[0] - last[0]) + abs(a[1] - last[1]) > 0.02:
            cur = [("M", a)]; subs.append(cur)
        if it[0] == "l": cur.append(("L", P(it[2]))); last = P(it[2])
        elif it[0] == "c": cur.append(("C", P(it[2]), P(it[3]), P(it[4]))); last = P(it[4])
    return subs
def dstr(subs, ox=0, oy=0):
    f = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
    out = []
    for s in subs:
        for seg in s:
            out.append(seg[0] + " ".join(f"{f(p[0] - ox)} {f(p[1] - oy)}" for p in seg[1:]))
        out.append("Z")
    return "".join(out)
def main(a):
    page = page_for(a[1]); M = page.rotation_matrix; ds = page.get_drawings()
    if a[0] == "list":
        mn = float(a[2]) if len(a) > 2 else 6
        for i, d in enumerate(ds):
            r = d["rect"] * M; r.normalize()
            if max(r.width, r.height) * K < mn: continue
            if "f" not in d["type"] or r.y0 * K > float(a[3] if len(a) > 3 else 1e9) or len(d["items"]) > 1 and False: continue
            if hexc(d.get("fill")) in ("#373435", "#201e1e") and d["type"] == "f" and len(d["items"]) == 3 and max(r.width, r.height) * K < 14: continue
            print(i, d["type"], hexc(d.get("fill")), hexc(d.get("color")), f"w{(d.get('width') or 0) * K:.1f}", "eo" if d.get("even_odd") else "nz",
                  f"[{r.x0 * K:.1f} {r.y0 * K:.1f} {r.x1 * K:.1f} {r.y1 * K:.1f}]", len(d["items"]))
    elif a[0] == "sym":
        sid = a[2]; layers = []; allp = []
        for g in a[3:]:
            if g.startswith("--"): continue
            idxs, _, colour = g.partition(":")
            subs = []
            for tok in idxs.split(","):
                if "-" in tok: lo, hi = tok.split("-"); rng = range(int(lo), int(hi) + 1)
                else: rng = [int(tok)]
                for i in rng: subs.append((ds[i], pts(ds[i], M)))
            layers.append((colour or "currentColor", subs))
            for _, ss in subs:
                for s in ss:
                    for seg in s: allp += list(seg[1:])
        # bbox from on-curve + control points is loose for curves; use svgpathtools bbox
        from svgpathtools import parse_path
        x0 = y0 = 1e9; x1 = y1 = -1e9
        for _, subs in layers:
            for _, ss in subs:
                for s in ss:
                    b = parse_path(dstr([s])).bbox(); x0 = min(x0, b[0]); x1 = max(x1, b[1]); y0 = min(y0, b[2]); y1 = max(y1, b[3])
        vb = [g for g in a[3:] if g.startswith("--vb=")]
        if vb: x0, y0, x1, y1 = [float(v) for v in vb[0][5:].split(",")]
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x1 - x0:.2f} {y1 - y0:.2f}">']
        for colour, subs in layers:
            for d, ss in subs:
                out.append(f'<path fill="{colour}" d="{fix(dstr(ss, x0, y0))}"/>')
        out.append("</svg>")
        open(os.path.join(ROOT, "tools/symbols", sid + ".svg"), "w").write("\n".join(out) + "\n")
        print(sid, f"px bbox [{x0:.1f} {y0:.1f} {x1:.1f} {y1:.1f}] size {x1 - x0:.1f} x {y1 - y0:.1f} px")
if __name__ == "__main__": main(sys.argv[1:])
