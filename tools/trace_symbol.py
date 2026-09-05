#!/usr/bin/env python3
"""
trace_symbol.py — trace a symbol from an AS 1743 drawing into tools/symbols/<id>.svg (mm units).

The drawing shows the finished sign in colour. We find the sign's ground by colour, map the
spec's mm box onto it, crop, upsample, threshold the black symbol, trace with potrace and
re-emit the outline as an absolute SVG path whose viewBox is the symbol's ink extent in mm.

  python3 tools/trace_symbol.py --spec tools/specs/TM/TM10-1A.json           # all symbols in a spec
  python3 tools/trace_symbol.py --drawing TM10-1A --ground yellow --inset 25 --box 250 100 100 400 --id tm10-1a_up_arrow
Add --force to overwrite, --show to also write a PNG preview next to the crop in the scratch dir.
"""
import argparse, glob, json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG_DIR = os.path.join(ROOT, "Australia", "National (AS 1743)", "Original PNGs")
SYM_DIR = os.path.join(ROOT, "tools", "symbols")
UPSCALE = 6

def base_code(code): return code.split("(")[0]
def resolve_png(code):
    """Drawing file for a code: exact name, else a file named <base>(...).png (handed drawings)."""
    exact = os.path.join(PNG_DIR, code + ".png")
    if os.path.exists(exact): return exact
    b = base_code(code)
    for f in sorted(os.listdir(PNG_DIR)):
        if (f.startswith(b + "(") or f == b + ".png") and f.endswith(".png"): return os.path.join(PNG_DIR, f)
    raise SystemExit(f"no drawing for {code}")

def reference_inset(spec):
    """mm inset (from the drawn outline) of the region the tracer detects. Coloured grounds: the
    ground itself, i.e. inside every edge/border layer (thin same-coloured edge strips are separate
    components and are dropped). White grounds: the outer edge of the black ring, i.e. inside any
    white layers outside it. Diamonds: the rounded tips pull the bbox in by r*(sqrt2-1)."""
    layers = []
    if spec.get("edge"): layers.append((spec["edge"]["colour"], spec["edge"]["width"], 0))
    for b in spec.get("borders", [spec["border"]] if spec.get("border") else []): layers.append((b["colour"], b["width"], b.get("inset", 0)))
    inset = 0.0
    if spec["ground"] == "white":
        for colour, w, extra in layers:
            if colour == "white": inset += w + extra
            else: break
    else:
        inset = sum(w + extra for _, w, extra in layers)
    if spec.get("shape") == "diamond":
        r = max(0, spec.get("radius", 0) - inset); inset += r * (2 ** 0.5 - 1)
    return inset

def ground_inset(spec):
    """mm from the outline to the ground (all edge/border layers), ignoring diamond tip rounding."""
    layers = []
    if spec.get("edge"): layers.append(spec["edge"]["width"])
    for b in spec.get("borders", [spec["border"]] if spec.get("border") else []): layers.append(b["width"] + b.get("inset", 0))
    return float(sum(layers))

def is_ground(px, ground):
    r, g, b = px[:3]
    return {
        "yellow": r > 200 and g > 170 and b < 120,
        "orange": r > 200 and 90 < g < 190 and b < 90,
        "red":    r > 180 and g < 90 and b < 90,
        "green":  g > 90 and r < 90 and b < 120,
        "blue":   b > 120 and r < 110 and g < 130,
        "brown":  100 < r < 190 and 50 < g < 120 and b < 90,
        "yellowgreen": r > 150 and g > 190 and b < 120,
        "white":  r > 235 and g > 235 and b > 235,
        "black":  r < 60 and g < 60 and b < 60,
    }[ground](0) if False else {
        "yellow": r > 200 and g > 170 and b < 120,
        "orange": r > 200 and 90 < g < 190 and b < 90,
        "red":    r > 180 and g < 90 and b < 90,
        "green":  g > 90 and r < 90 and b < 120,
        "blue":   b > 120 and r < 110 and g < 130,
        "brown":  100 < r < 190 and 50 < g < 120 and b < 90,
        "yellowgreen": r > 150 and g > 190 and b < 120,
        "white":  r > 235 and g > 235 and b > 235,
        "black":  r < 60 and g < 60 and b < 60,
    }[ground]

INK_HEX = {"black": "#000", "red": "#ed1c24", "green": "#0b804c", "blue": "#3a53a4", "white": "#fff",
           "yellow": "#ffe40d", "orange": "#f58020", "brown": "#754c24"}
def is_ink(px, colour):
    r, g, b = px[:3]
    return {"black": r < 110 and g < 110 and b < 110,
            "red": r > 150 and g < 110 and b < 110,
            "green": g > 80 and r < 120 and b < 130 and g > r + 20,
            "blue": b > 110 and r < 120 and g < 140 and b > r + 30,
            "white": r > 200 and g > 200 and b > 200,
            "yellow": r > 200 and g > 170 and b < 120,
            "orange": r > 200 and 90 < g < 190 and b < 90,
            "brown": 100 < r < 190 and 50 < g < 120 and b < 90}[colour]

def find_panel(img, ground, which=0):
    """Pixel bbox of the `which`-th ground-coloured connected region, ordered top-to-bottom then
    left-to-right (drawings that show (L) and (R) contain two panels). Only coloured grounds."""
    w, h = img.size; px = img.load()
    mask = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            if is_ground(px[x, y], ground): mask[y * w + x] = 1
    seen = bytearray(w * h); comps = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[i] or seen[i]: continue
            stack = [i]; seen[i] = 1; n = 0; x0 = x1 = x; y0 = y1 = y
            while stack:
                j = stack.pop(); n += 1; jy, jx = divmod(j, w)
                x0 = min(x0, jx); x1 = max(x1, jx); y0 = min(y0, jy); y1 = max(y1, jy)
                for k in (j - 1, j + 1, j - w, j + w):
                    if 0 <= k < w * h and mask[k] and not seen[k] and abs((k % w) - jx) <= 1: seen[k] = 1; stack.append(k)
            if n > 400: comps.append((n, x0, y0, x1, y1))
    if not comps: raise SystemExit("ground colour not found")
    big = max(c[0] for c in comps)
    comps = [c for c in comps if c[0] > big * 0.02]          # drop legend swatches, grid insets
    # cluster: start from the largest, absorb components whose bbox lies near the cluster (sub-panels
    # of one sign separated by white dividers); handed drawings stay separate clusters
    clusters = []
    for c in sorted(comps, key=lambda c: -c[0]):
        n, x0, y0, x1, y1 = c; placed = False
        for cl in clusters:
            gap = 0.08 * max(cl[3] - cl[1], cl[4] - cl[2])
            if x0 <= cl[3] + gap and x1 >= cl[1] - gap and y0 <= cl[4] + gap and y1 >= cl[2] - gap:
                cl[0] += n; cl[1] = min(cl[1], x0); cl[2] = min(cl[2], y0); cl[3] = max(cl[3], x1); cl[4] = max(cl[4], y1); placed = True; break
        if not placed: clusters.append([n, x0, y0, x1, y1])
    clusters = [cl for cl in clusters if cl[0] > big * 0.25]
    clusters.sort(key=lambda c: (c[2] // 50, c[1]))             # top-to-bottom, then left-to-right
    n, x0, y0, x1, y1 = clusters[min(which, len(clusters) - 1)]
    return x0, y0, x1, y1

def find_white_panel(img, which=0):
    """White-ground signs: bbox of the dark border ring (largest dark component by bbox area),
    trimmed to its long straight runs so touching dimension lines don't widen it."""
    for dark in (90, 170):
        try: return _find_white_panel(img, which, dark)
        except SystemExit: pass
    raise SystemExit("no border ring found")

def _find_white_panel(img, which, dark):
    w, h = img.size; px = img.load()
    mask = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if r < dark and g < dark and b < dark: mask[y * w + x] = 1
    seen = bytearray(w * h); comps = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[i] or seen[i]: continue
            stack = [i]; seen[i] = 1; pts = []
            while stack:
                j = stack.pop(); pts.append(j); jy, jx = divmod(j, w)
                for k in (j - 1, j + 1, j - w, j + w):
                    if 0 <= k < w * h and mask[k] and not seen[k] and abs((k % w) - jx) <= 1: seen[k] = 1; stack.append(k)
            if len(pts) < 2000: continue
            xs = [q % w for q in pts]; ys = [q // w for q in pts]
            comps.append(((max(xs) - min(xs)) * (max(ys) - min(ys)), pts, min(ys)))
    if not comps: raise SystemExit("no border ring found")
    comps.sort(key=lambda c: -c[0]); big = comps[0][0]
    cands = [c for c in comps if c[0] > big * 0.3]; cands.sort(key=lambda c: c[2])
    pts = cands[min(which, len(cands) - 1)][1]
    rows = {}; cols = {}
    for q in pts:
        y, x = divmod(q, w); rows[y] = rows.get(y, 0) + 1; cols[x] = cols.get(x, 0) + 1
    rmax = max(rows.values()); cmax = max(cols.values())
    ry = [y for y, n in rows.items() if n >= 0.5 * rmax]; cx = [x for x, n in cols.items() if n >= 0.5 * cmax]
    return min(cx), min(ry), max(cx), max(ry)

def drop_edge_specks(bw):
    """Remove dark components that are small (< 4% of the largest) and lie within 10% of the crop edge:
    the drawings' corner brackets and dashed reference boxes around a symbol."""
    w, h = bw.size; px = bw.load()
    mask = bytearray(1 if px[x, y] == 0 else 0 for y in range(h) for x in range(w))
    seen = bytearray(w * h); comps = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[i] or seen[i]: continue
            stack = [i]; seen[i] = 1; pts = []
            while stack:
                j = stack.pop(); pts.append(j); jy, jx = divmod(j, w)
                for k in (j - 1, j + 1, j - w, j + w):
                    if 0 <= k < w * h and mask[k] and not seen[k] and abs((k % w) - jx) <= 1: seen[k] = 1; stack.append(k)
            comps.append(pts)
    if not comps: return bw
    big = max(len(c) for c in comps); ex, ey = 0.1 * w, 0.1 * h
    for c in comps:
        if len(c) < 0.04 * big:
            xs = [q % w for q in c]; ys = [q // w for q in c]
            if min(xs) < ex or max(xs) > w - ex or min(ys) < ey or max(ys) > h - ey:
                for q in c: px[q % w, q // w] = 255
    return bw

def parse_potrace(svg_text):
    """Return list of subpaths as lists of (x,y) cubic-bezier control tuples, in potrace units (y up)."""
    m = re.search(r'transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([-\d.]+),([-\d.]+)\)"', svg_text)
    tx, ty, sx, sy = map(float, m.groups())
    out = []
    for d in re.findall(r'<path d="([^"]+)"', svg_text):
        toks = re.findall(r'[MmCcLlZz]|-?\d+\.?\d*', d); i = 0; cur = None; start = None; cmd = None
        segs = []  # list of ('M',x,y) / ('C',x1,y1,x2,y2,x,y) / ('L',x,y) / ('Z',)
        def T(x, y): return (tx + sx * x, ty + sy * y)
        while i < len(toks):
            if toks[i].isalpha(): cmd = toks[i]; i += 1; continue
            if cmd == 'M':
                x, y = float(toks[i]), float(toks[i + 1]); i += 2; cur = (x, y); start = cur; segs.append(('M',) + T(x, y)); cmd = 'L'
            elif cmd == 'm':
                x, y = cur[0] + float(toks[i]), cur[1] + float(toks[i + 1]); i += 2; cur = (x, y); start = cur; segs.append(('M',) + T(x, y)); cmd = 'l'
            elif cmd in 'Cc':
                v = list(map(float, toks[i:i + 6])); i += 6
                if cmd == 'c': v = [v[0] + cur[0], v[1] + cur[1], v[2] + cur[0], v[3] + cur[1], v[4] + cur[0], v[5] + cur[1]]
                segs.append(('C',) + T(v[0], v[1]) + T(v[2], v[3]) + T(v[4], v[5])); cur = (v[4], v[5])
            elif cmd in 'Ll':
                x, y = float(toks[i]), float(toks[i + 1]); i += 2
                if cmd == 'l': x += cur[0]; y += cur[1]
                segs.append(('L',) + T(x, y)); cur = (x, y)
            elif cmd in 'Zz':
                segs.append(('Z',)); cur = start; i += 0
                if i < len(toks) and not toks[i].isalpha(): pass
        out.append(segs)
    return out

def trace(drawing, ground, inset, box, sid, panel=None, force=False, show=False, threshold=110, invert=False, which=0, colours=None, mask=None, open_px=0):
    outp = os.path.join(SYM_DIR, sid + ".svg")
    if os.path.exists(outp) and not force: return "exists"
    img = Image.open(resolve_png(drawing)).convert("RGB")
    if panel: x0, y0, x1, y1 = panel
    elif ground == "white": x0, y0, x1, y1 = find_white_panel(img, which)
    else: x0, y0, x1, y1 = find_panel(img, ground, which)
    # the ground region corresponds to the mm rect inset by (edge+border) on every side
    Wmm = box[4] if len(box) > 4 else None
    return _trace_from_panel(img, (x0, y0, x1, y1), inset, box, sid, outp, show, threshold, invert, colours, mask, open_px)

def _trace_from_panel(img, ppx, inset, box, sid, outp, show, threshold, invert, colours=None, mask=None, open_px=0):
    x0, y0, x1, y1 = ppx
    bx, by, bw, bh, Wmm, Hmm = box
    kx = (x1 - x0 + 1) / (Wmm - 2 * inset); ky = (y1 - y0 + 1) / (Hmm - 2 * inset)   # px per mm
    cx0 = x0 + (bx - inset) * kx; cy0 = y0 + (by - inset) * ky; cx1 = cx0 + bw * kx; cy1 = cy0 + bh * ky
    pad = max(2, int(0.02 * max(cx1 - cx0, cy1 - cy0)))
    crop = img.crop((int(cx0) - pad, int(cy0) - pad, int(cx1) + pad + 1, int(cy1) + pad + 1))
    if mask:   # paint everything outside the sign's ground shape white (border corners on diamonds/circles)
        shape, Wm, Hm, gin = mask; cp = crop.load(); ox, oy = int(cx0) - pad, int(cy0) - pad; margin = 4.0
        for yy in range(crop.height):
            for xx in range(crop.width):
                mx = inset + (ox + xx - x0) / kx; my = inset + (oy + yy - y0) / ky   # mm in sign coords
                if shape == "diamond": inside = abs(mx - Wm / 2) + abs(my - Hm / 2) <= Wm / 2 - gin * 1.41421 - margin
                elif shape == "circle": inside = ((mx - Wm / 2) ** 2 + (my - Hm / 2) ** 2) ** 0.5 <= Wm / 2 - gin - margin
                elif shape == "octagon": inside = max(abs(mx - Wm / 2), abs(my - Hm / 2), (abs(mx - Wm / 2) + abs(my - Hm / 2)) / 1.41421) <= Wm / 2 - gin - margin
                else: inside = gin + margin <= mx <= Wm - gin - margin and gin + margin <= my <= Hm - gin - margin
                if not inside: cp[xx, yy] = (255, 255, 255)
    bigc = crop.resize((crop.width * UPSCALE, crop.height * UPSCALE), Image.LANCZOS).convert("RGB")
    layers = []   # (hex fill, 1-bit image)
    if colours:
        cp = bigc.load(); w_, h_ = bigc.size
        for colour in colours:
            m = Image.new("1", bigc.size, 255); mp = m.load()
            for yy in range(h_):
                for xx in range(w_):
                    if is_ink(cp[xx, yy], colour): mp[xx, yy] = 0
            layers.append((INK_HEX[colour], drop_edge_specks(m)))
    else:
        big = bigc.convert("L")
        if invert: big = ImageOps.invert(big)
        if open_px:   # morphological opening: removes hairlines (drawing centre lines) thinner than open_px (upscaled px)
            k = open_px | 1; big = big.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))
        layers.append(("currentColor", drop_edge_specks(big.point(lambda v: 0 if v < threshold else 255, "1"))))
    kx_mm = 1 / (UPSCALE * kx); ky_mm = 1 / (UPSCALE * ky)
    allpaths = []   # (fill, segs list)
    for fill, bw_img in layers:
        with tempfile.TemporaryDirectory() as td:
            pbm = os.path.join(td, "s.pbm"); bw_img.save(pbm)
            svg = subprocess.run(["potrace", "-s", "-t", "8", "-a", "1.0", "-O", "0.2", "-u", "100", "-o", "-", pbm], capture_output=True, text=True, check=True).stdout
        for segs in parse_potrace(svg): allpaths.append((fill, segs))
    if not allpaths: raise SystemExit(f"{sid}: nothing traced")
    pts = [(sg[j], sg[j + 1]) for _, segs in allpaths for sg in segs for j in range(1, len(sg), 2)]
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts); miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    sx, sy = kx_mm, ky_mm
    def f(v): return f"{v:.2f}".rstrip("0").rstrip(".") or "0"
    def X(x): return f((x - minx) * sx)
    def Y(y): return f((y - miny) * sy)
    def path_d(segs):
        d = []
        for sg in segs:
            if sg[0] == 'M': d.append(f"M{X(sg[1])} {Y(sg[2])}")
            elif sg[0] == 'L': d.append(f"L{X(sg[1])} {Y(sg[2])}")
            elif sg[0] == 'C': d.append(f"C{X(sg[1])} {Y(sg[2])} {X(sg[3])} {Y(sg[4])} {X(sg[5])} {Y(sg[6])}")
            else: d.append("Z")
        return " ".join(d)
    vw = (maxx - minx) * sx; vh = (maxy - miny) * sy
    os.makedirs(SYM_DIR, exist_ok=True)
    body = []
    for fill, _ in layers:
        ds = " ".join(path_d(segs) for fl, segs in allpaths if fl == fill)
        if ds: body.append(f'<path fill="{fill}" fill-rule="evenodd" d="{ds}"/>')
    with open(outp, "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(vw)} {f(vh)}">\n' + "\n".join(body) + "\n</svg>\n")
    if show:
        crop.save(os.path.join(show, sid + "_crop.png"))
    warn = " WARNING: traced extent differs from box by >4% - check the box in the spec" if abs(vw - bw) > 0.04 * bw or abs(vh - bh) > 0.04 * bh else ""
    return f"traced {f(vw)} x {f(vh)} mm (box {bw} x {bh}){warn}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--drawing"); ap.add_argument("--ground"); ap.add_argument("--inset", type=float, default=0)
    ap.add_argument("--box", nargs=4, type=float); ap.add_argument("--size", nargs=2, type=float); ap.add_argument("--id")
    ap.add_argument("--panel", nargs=4, type=int); ap.add_argument("--force", action="store_true"); ap.add_argument("--show")
    ap.add_argument("--threshold", type=int, default=110); ap.add_argument("--invert", action="store_true"); ap.add_argument("--which", type=int, default=0)
    a = ap.parse_args()
    if a.spec:
        specs = [json.load(open(sp)) for sp in sorted(glob.glob(a.spec))]
        done = set()
        # pass 0: specs whose code equals a symbol's source exactly; pass 1: base-code matches (handed drawings);
        # pass 2: report reuses. An id is traced at most once per run (first definer wins).
        for reuse_pass in (0, 1, 2):
            for spec in specs:
                if spec.get("skip") or not spec.get("symbols"): continue
                inset = reference_inset(spec)
                for el in spec.get("elements", []):
                    if el.get("type") != "symbol": continue
                    meta = spec["symbols"].get(el["id"], {})
                    src = meta.get("source", spec["code"])
                    exact = src == spec["code"]; own = base_code(src) == base_code(spec["code"])
                    if reuse_pass == 0 and not exact: continue
                    if reuse_pass == 1 and (exact or not own): continue
                    if reuse_pass == 2:
                        if own: continue
                        print(spec["code"], el["id"], "reuse of", src, "(ok)" if os.path.exists(os.path.join(SYM_DIR, el["id"] + ".svg")) else "MISSING - source spec has no such symbol"); continue
                    if el["id"] in done: print(spec["code"], el["id"], "already traced this run (first definer wins)"); continue
                    done.add(el["id"])
                    try:
                        r = trace(src, meta.get("ground", spec["ground"]), meta.get("inset", inset), (el["x"], el["y"], el["w"], el["h"], spec["size"][0], spec["size"][1]), el["id"],
                                  panel=meta.get("panel_px"), force=a.force, show=a.show, threshold=meta.get("threshold", a.threshold),
                                  invert=meta.get("invert", meta.get("ground", spec["ground"]) == "black"), which=meta.get("which", 0), colours=meta.get("colours"),
                                  mask=None if meta.get("nomask") else (spec.get("shape", "rect"), spec["size"][0], spec["size"][1], ground_inset(spec)), open_px=meta.get("open", 0))
                    except SystemExit as e: r = f"FAILED: {e}"
                    except Exception as e: r = f"FAILED: {type(e).__name__} {e}"
                    print(spec["code"], el["id"], r)
    else:
        print(trace(a.drawing, a.ground, a.inset, tuple(a.box) + tuple(a.size), a.id, panel=a.panel, force=a.force, show=a.show, threshold=a.threshold, invert=a.invert, which=a.which))

if __name__ == "__main__":
    main()
