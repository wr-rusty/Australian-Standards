"""auto.py — as-drawn spec builder for directly dimensioned, to-scale TMR sheets (vector artwork + live FHWA text).
build(code, name, W=None, ...) writes tools/specs/QLD/<code>.json and returns a report dict."""
import re, sys, os, json, colorsys, collections
from qb import *
import vec as _vec, pymupdf as _mu
from fixwind import fix
K = _vec.K
def cname(h):
    if h == "-": return None
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    if min(r, g, b) > 225: return "white"
    if max(r, g, b) < 0x62 and max(r, g, b) - min(r, g, b) < 36: return "black"
    hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); hue = hh * 360
    if s < 0.18: return "grey"
    if hue < 12 or hue > 340: return "red"
    if hue < 40: return "orange" if l > 0.42 else "brown"
    if hue < 70: return "yellow" if g > 150 else "brown"
    if hue < 100: return "yellowgreen"
    if hue < 175: return "green"
    if hue < 270: return "blue"
    return "red"
SER = [("AS1744LowerCase", "Emod"), ("FHWASeriesEm", "Emod"), ("SeriesB", "B"), ("SeriesC", "C"), ("SeriesD", "D"), ("SeriesE", "E"), ("SeriesF", "F")]
def series_of(font):
    for k_, v in SER:
        if k_ in font: return v
    return None
def dist(p, q): return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2])
def build(code, name, W=None, vcode=None, drawing=None, sign_box=None, which=0, notes_extra="", caps=None, family=None, legend=None, drop_text=(), vary=None, ymax=1700, keep_grey=False, drawn_value=None, text_fix=None, symbol_split=False, no_symbols=False, ground_override=None, lines=None, legend_fonts=(), series=None, union=False, add=None, drop_rows=(), fill_box=None, fill_series=None, box_mm=None, drop_small=0, no_strokes=False, diamond=None, hands=None, drawn_hand=None, table_note="", layer_mm=None):
    vcode = vcode or code; drawing = drawing or code
    page = _vec.page_for(vcode); M = page.rotation_matrix; ds = page.get_drawings()
    F = []
    for i, d in enumerate(ds):
        if "f" not in d["type"] or d.get("fill") is None: continue
        r = d["rect"] * M; r.normalize()
        F.append({"i": i, "hex": _vec.hexc(d["fill"]), "col": cname(_vec.hexc(d["fill"])), "b": (r.x0 * K, r.y0 * K, r.x1 * K, r.y1 * K), "n": len(d["items"]), "d": d})
    area = lambda f: (f["b"][2] - f["b"][0]) * (f["b"][3] - f["b"][1])
    if sign_box: outer = max((f for f in F if f["b"][0] >= sign_box[0] - 2 and f["b"][2] <= sign_box[2] + 2 and f["b"][1] >= sign_box[1] - 2 and f["b"][3] <= sign_box[3] + 2), key=area)
    else:
        cand = sorted((f for f in F if f["b"][1] < ymax and f["b"][3] < 1900 and f["n"] <= 16 and (f["b"][2] - f["b"][0]) > 150 and f["col"] != "grey"), key=area, reverse=True)
        outer = cand[which]
    ob = outer["b"]; pieces = [outer]
    if diamond:
        side_, r_ = diamond; W = round(side_ * R2, 2); ob = tuple(diamond_px(outer["b"], r_, side_))
    if union:
        grew = True
        while grew:
            grew = False
            for f in F:
                b_ = f["b"]
                if f in pieces or f["col"] == "grey" or f["n"] > 16: continue
                if abs(b_[0] - ob[0]) < 2.5 and abs(b_[2] - ob[2]) < 2.5 and (abs(b_[1] - ob[3]) < 2.5 or abs(b_[3] - ob[1]) < 2.5):
                    pieces.append(f); ob = (min(ob[0], b_[0]), min(ob[1], b_[1]), max(ob[2], b_[2]), max(ob[3], b_[3])); grew = True
    # live text
    TX = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                t = sp["text"].strip()
                if not t: continue
                r = _mu.Rect(sp["bbox"]) * M; r.normalize()
                TX.append({"t": t, "font": sp["font"], "size": sp["size"] * K, "b": (r.x0 * K, r.y0 * K, r.x1 * K, r.y1 * K), "color": sp.get("color", 0)})
    base_leg = lambda t: "FHWA" in t["font"] or "AS1744" in t["font"] or t["font"] in legend_fonts
    lsz = sorted(t["size"] for t in TX if not base_leg(t)); typ = lsz[len(lsz) // 2] if lsz else 30
    def is_leg(t):
        if base_leg(t): return True
        b_ = t["b"]
        return (b_[0] > ob[0] and b_[2] < ob[2] and b_[1] > ob[1] and b_[3] < ob[3] and t["size"] > 1.5 * typ and re.fullmatch(r"[A-Z0-9/&\-.,'() ]+|k?m|t|km/h", t["t"]) is not None)
    labels = [t for t in TX if not is_leg(t)]
    if W is None:
        best = None
        for t in labels:
            m = re.fullmatch(r"(\d{3,4})", t["t"])
            cx = (t["b"][0] + t["b"][2]) / 2
            if m and t["b"][3] <= ob[1] + 2 and ob[0] < cx < ob[2] and abs(cx - (ob[0] + ob[2]) / 2) < 0.25 * (ob[2] - ob[0]):
                dy = ob[1] - t["b"][3]
                if best is None or dy > best[0]: best = (dy, int(m.group(1)))   # the farthest label above = the overall width
        if best is None: raise SystemExit(f"{code}: no width label")
        W = best[1]
    k = (ob[2] - ob[0]) / W; H = (ob[3] - ob[1]) / k; edge_inferred = 0
    if outer["col"] == "black" and len(pieces) == 1:
        hl = sorted({int(t["t"]) for t in labels if re.fullmatch(r"\d{3,4}", t["t"]) and (t["b"][2] < ob[0] or t["b"][0] > ob[2]) and ob[1] - 50 < (t["b"][1] + t["b"][3]) / 2 < ob[3] + 50 and H < int(t["t"]) < 1.06 * H})
        if hl and abs(hl[0] - H) > 0.002 * H:
            a_ = (ob[2] - ob[0]) / (ob[3] - ob[1]); e_ = (W - a_ * hl[0]) / (2 * (1 - a_)) if abs(1 - a_) > 0.02 else (hl[0] - H) / 2
            if 0 < e_ < 0.04 * W:
                e_ = round(e_) if abs(e_ - round(e_)) < 0.6 else round(e_, 1); k = (ob[2] - ob[0]) / (W - 2 * e_)
                ob = (ob[0] - e_ * k, ob[1] - e_ * k, ob[2] + e_ * k, ob[3] + e_ * k); H = (ob[3] - ob[1]) / k; edge_inferred = e_
    Hr = round(H / 5) * 5 if abs(H - round(H / 5) * 5) < 0.012 * H else round(H, 1)
    if diamond: Hr = W; H = W
    ppx = list(ob)
    mmb = lambda b: ((b[0] - ob[0]) / k, (b[1] - ob[1]) / k, (b[2] - ob[0]) / k, (b[3] - ob[1]) / k)
    inside = lambda b, tol=1.5: b[0] >= ob[0] - tol and b[2] <= ob[2] + tol and b[1] >= ob[1] - tol and b[3] <= ob[3] + tol
    IN = [f for f in F if inside(f["b"]) and (keep_grey or f["col"] != "grey") and (f["i"] != outer["i"] or len(pieces) > 1)]
    def junk(f):   # leader arrowheads in the corners and the dashes of a variable-legend box
        m = mmb(f["b"]); w, h = m[2] - m[0], m[3] - m[1]
        if max(w, h) < 0.02 * W and f["n"] <= 4 and min(w, h) < 0.012 * W: return True
        if max(w, h) < 0.03 * max(W, H) and f["n"] <= 7 and (m[0] < 0.06 * W or m[2] > 0.94 * W) and (m[1] < 0.06 * H or m[3] > 0.94 * H): return True
        return False
    dashed = []
    for d in ds:
        if d["type"] == "s" and d.get("dashes") and d["dashes"] not in ("[] 0", ""):
            r = d["rect"] * M; r.normalize(); dashed.append((r.x0 * K, r.y0 * K, r.x1 * K, r.y1 * K))
    def on_dash(f):
        b_ = f["b"]
        if max(b_[2] - b_[0], b_[3] - b_[1]) > 0.08 * (ob[2] - ob[0]): return False
        for q in dashed:
            if b_[0] >= q[0] - 4 and b_[2] <= q[2] + 4 and b_[1] >= q[1] - 4 and b_[3] <= q[3] + 4 and (min(abs(b_[0] - q[0]), abs(b_[2] - q[2]), abs(b_[1] - q[1]), abs(b_[3] - q[3])) < 4): return True
        return False
    def hinge(f):
        m = mmb(f["b"]); return (m[2] - m[0]) > 0.9 * W and (m[3] - m[1]) < 8 and f["col"] in ("white", "grey") and 0.1 * H < m[1] < 0.9 * H
    def tiny_only(f):
        try: subs = _vec.pts(f["d"], M)
        except Exception: return False
        if len(subs) < 2: return False
        for s_ in subs:
            xs_ = [p[0] for seg in s_ for p in seg[1:]]; ys_ = [p[1] for seg in s_ for p in seg[1:]]
            w_, h_ = (max(xs_) - min(xs_)) / k, (max(ys_) - min(ys_)) / k
            if not (min(w_, h_) < 0.006 * W and max(w_, h_) < 0.06 * W): return False
        return True
    IN = [f for f in IN if not junk(f) and not on_dash(f) and not hinge(f) and not tiny_only(f)]
    if layer_mm: IN = [f for f in IN if not ((f["b"][2] - f["b"][0]) > 0.85 * (outer["b"][2] - outer["b"][0]) and (f["b"][3] - f["b"][1]) > 0.85 * (outer["b"][3] - outer["b"][1]))]
    if diamond:
        e_all = 0.06 * W * k
        IN = [f for f in IN if inside_diamond(f["b"], ob, 0) or (f["n"] <= 40 and abs((f["b"][2] - f["b"][0]) - (f["b"][3] - f["b"][1])) < 2 and (f["b"][2] - f["b"][0]) > 0.8 * (outer["b"][2] - outer["b"][0]))]
    if drop_small: IN = [f for f in IN if max(mmb(f["b"])[2] - mmb(f["b"])[0], mmb(f["b"])[3] - mmb(f["b"])[1]) >= drop_small]
    if edge_inferred: IN = [f for f in IN if not f["i"] < outer["i"]]
    boxes = [mmb(q) for q in dashed if q[0] >= ob[0] and q[2] <= ob[2] and q[1] >= ob[1] and q[3] <= ob[3]]
    # concentric layers
    layers = [(outer["col"], 0.0)]; used = {outer["i"]}; cur = ob
    if edge_inferred: layers = [("white", 0.0), (outer["col"], float(edge_inferred))]; cur = outer["b"]
    if len(pieces) > 1: layers = [("none", 0.0)]; used = set()
    for f in (sorted(IN, key=area, reverse=True) if len(pieces) == 1 else []):
        b = f["b"]; ob_ = outer["b"] if diamond else ob; ins = [b[0] - ob_[0], b[1] - ob_[1], ob_[2] - b[2], ob_[3] - b[3]]
        if max(ins) - min(ins) < 1.2 and f["n"] <= (40 if diamond else 16) and min(ins) / k < 0.2 * min(W, H) and min(ins) > (cur[0] - (outer["b"][0] if diamond else ob[0])) + 0.5 and len(layers) < 3 and f["i"] > outer["i"]:
            layers.append((f["col"], sum(ins) / 4 / k)); used.add(f["i"]); cur = b
        elif len(layers) >= 3: break
    rd = lambda v: round(v) if abs(v - round(v)) < 0.35 else round(v, 1)
    stroke_els = []
    spec_kw = {}
    if len(layers) == 3: spec_kw = {"edge": {"colour": layers[0][0], "width": rd(layers[1][1])}, "border": {"colour": layers[1][0], "width": rd(layers[2][1] - layers[1][1])}, "ground": layers[2][0]}
    elif len(layers) == 2 and edge_inferred: spec_kw = {"edge": {"colour": "white", "width": edge_inferred}, "ground": "black"}
    elif len(layers) == 2: spec_kw = {"border": {"colour": layers[0][0], "width": rd(layers[1][1])}, "ground": layers[1][0]}
    else: spec_kw = {"ground": layers[0][0]}
    if layer_mm: spec_kw = {"edge": {"colour": layer_mm[0], "width": layer_mm[1]}, "border": {"colour": layer_mm[2], "width": layer_mm[3]}, "ground": layer_mm[4]}
    if ground_override: spec_kw["ground"] = ground_override
    # radius from label
    radius = 0
    if diamond: radius = diamond[1]
    for t in ([] if diamond else labels):
        m = re.fullmatch(r"[rR]\s?(\d+)", t["t"])
        if m and t["b"][1] < ob[3] and t["b"][3] > ob[1] - 200: radius = int(m.group(1)); break
    if not radius and len(pieces) == 1 and not diamond:
        try:
            P_ = [seg[-1] for s_ in _vec.pts(outer["d"], M) for seg in s_]
            topx = [p[0] for p in P_ if abs(p[1] - outer["b"][1]) < 0.3 and p[0] < (outer["b"][0] + outer["b"][2]) / 2]
            if topx and min(topx) - outer["b"][0] > 1:
                rg = (min(topx) - outer["b"][0]) / k + (edge_inferred or 0); radius = round(rg / 5) * 5 if abs(rg - round(rg / 5) * 5) < 2 else round(rg)
        except Exception: pass
    # solid stroked lines / curves inside the sign that are part of the face (rules, hill profiles, dimension-style bars) -> filled outlines
    from shapely.geometry import LineString
    from svgpathtools import parse_path as _pp
    for i_, d in enumerate(ds):
        if no_strokes or d["type"] != "s" or d.get("dashes") not in (None, "", "[] 0"): continue
        colr = cname(_vec.hexc(d.get("color"))); wd = (d.get("width") or 0) * K / k
        if colr in (None, "grey") or wd < 0.0025 * W: continue
        try: subs = _vec.pts(d, M)
        except Exception: continue
        m_ = min(layers[-1][1] if len(layers) > 1 else 0, 0.05 * W)
        for s_ in subs:
            sm = [(seg[0],) + tuple(((p[0] - ob[0]) / k, (p[1] - ob[1]) / k) for p in seg[1:]) for seg in s_]
            allp = [p for seg in sm for p in seg[1:]]
            if not all(m_ < p[0] < W - m_ and m_ < p[1] < H - m_ for p in allp): continue
            dd = _vec.dstr([sm])[:-1]   # open path
            try: P_ = _pp(dd)
            except Exception: continue
            ptsl = []
            for seg in P_:
                n_ = 1 if seg.__class__.__name__ == "Line" else 24
                for j in range(n_): q = seg.point(j / n_); ptsl.append((q.real, q.imag))
            q = P_[-1].point(1); ptsl.append((q.real, q.imag))
            if len(ptsl) < 2: continue
            ls = LineString(ptsl)
            if ls.length < 2 * wd: continue
            poly = ls.buffer(wd / 2, cap_style=2, join_style=2)
            geoms = [poly] if poly.geom_type == "Polygon" else list(poly.geoms)
            for g_ in geoms:
                dpath = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in list(g_.exterior.coords)[:-1]) + "Z"
                for hole in g_.interiors: dpath += "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in list(hole.coords)[:-1]) + "Z"
                e_ = {"type": "path", "d": dpath, "colour": colr}
                if g_.interiors: e_["fill_rule"] = "evenodd"
                stroke_els.append(e_)
    # remaining fills -> panel paths or symbol items
    els = []; symitems = []; trep = []; text_els = []; variable = []
    def pathd(f):
        subs = _vec.pts(f["d"], M)
        sm = [[(seg[0],) + tuple(((p[0] - ob[0]) / k, (p[1] - ob[1]) / k) for p in seg[1:]) for seg in s] for s in subs]
        return fix(_vec.dstr(sm))
    for f in IN:
        if f["i"] in used: continue
        m = mmb(f["b"]); w, h = m[2] - m[0], m[3] - m[1]
        simple = f["n"] <= 14 and max(w, h) >= 12 and not (f["d"].get("even_odd") and f["n"] > 8)
        if simple:   # panel shapes: exact paths in mm
            if f["n"] == 1 and f["d"]["items"][0][0] == "re": els.append({"type": "rect", "x": rd(m[0]), "y": rd(m[1]), "w": rd(w), "h": rd(h), "colour": f["col"]})
            else: els.append({"type": "path", "d": pathd(f), "colour": f["col"]})
        else: symitems.append(f)
    symbols = {}; sym_note = ""; rowrep = []
    # ---- contours of the remaining fills (letters outlined on the TC sheets, and symbol artwork)
    from svgpathtools import parse_path
    CT = []
    for f in symitems:
        subs = _vec.pts(f["d"], M)
        for s_ in subs:
            sm = [(seg[0],) + tuple(((p[0] - ob[0]) / k, (p[1] - ob[1]) / k) for p in seg[1:]) for seg in s_]
            try: bb = parse_path(_vec.dstr([sm])).bbox()
            except Exception: continue
            thin_ = min(bb[1] - bb[0], bb[3] - bb[2]) < 0.004 * W and max(bb[1] - bb[0], bb[3] - bb[2]) < 0.05 * W
            CT.append({"f": f, "sm": sm, "b": (bb[0], bb[2], bb[1], bb[3]), "col": f["col"], "kids": [], "thin": thin_})
    nthin = collections.Counter(id(c["f"]) for c in CT if c["thin"])
    CT = [c for c in CT if not (c["thin"] and nthin[id(c["f"])] >= 6)]
    par = []
    for c in sorted(CT, key=lambda c: -(c["b"][2] - c["b"][0]) * (c["b"][3] - c["b"][1])):
        host = next((p for p in par if p["f"] is c["f"] and p["b"][0] <= c["b"][0] + 0.3 and p["b"][1] <= c["b"][1] + 0.3 and p["b"][2] >= c["b"][2] - 0.3 and p["b"][3] >= c["b"][3] - 0.3), None)
        if host: host["kids"].append(c)
        else: par.append(c)
    par.sort(key=lambda c: (c["b"][1], c["b"][0])); rows_ = []
    for c in par:
        h = c["b"][3] - c["b"][1]; placed = False
        for r in rows_:
            ov = min(c["b"][3], r["y1"]) - max(c["b"][1], r["y0"])
            if ov > 0.5 * min(h, r["y1"] - r["y0"]): r["c"].append(c); r["y0"] = min(r["y0"], c["b"][1]) if h > 0.5 * (r["y1"] - r["y0"]) else r["y0"]; r["y1"] = max(r["y1"], c["b"][3]) if h > 0.5 * (r["y1"] - r["y0"]) else r["y1"]; placed = True; break
        if not placed: rows_.append({"y0": c["b"][1], "y1": c["b"][3], "c": [c]})
    rows_.sort(key=lambda r: r["y0"])
    rows_ = [r for n_, r in enumerate(rows_) if n_ not in drop_rows]
    lab_series = []
    for t in sorted(labels, key=lambda t: t["b"][1]):
        m_ = re.match(r"(\d{2,3})\s?(Mod\s?E|[B-F])", t["t"])
        if m_ and t["b"][1] < ob[3] + 60 and t["b"][3] > ob[1] - 60: lab_series.append((int(m_.group(1)), "E" if m_.group(2).startswith("Mod") else m_.group(2), t["t"]))
    lab_all = sorted({int(x) for t in labels for x in re.findall(r"(\d{2,3})\s?(?:Mod\s?E|[B-F]|LC|lc|Em|EM)", t["t"])})
    art = []; legend_parts = []
    def words_of(r):
        cs = sorted(r["c"], key=lambda c: c["b"][0]); hs = sorted(c["b"][3] - c["b"][1] for c in cs); cap = hs[-1]
        ws = [[cs[0]]]
        for c in cs[1:]:
            right = max(x["b"][2] for x in ws[-1])
            if c["b"][0] - right > 0.42 * cap: ws.append([c])
            else: ws[-1].append(c)
        return ws
    if lines is None:
        for n_, r in enumerate(rows_):
            ws = words_of(r)
            rowrep.append((n_, "y %.0f-%.0f" % (r["y0"], r["y1"]), "h %.0f" % (r["y1"] - r["y0"]), "x %.0f-%.0f" % (min(c["b"][0] for c in r["c"]), max(c["b"][2] for c in r["c"])), [len(w) for w in ws], sorted({c["col"] for c in r["c"]})))
        art = [c for r in rows_ for c in r["c"]] if rows_ else []
    else:
        if len(lines) != len(rows_): raise SystemExit(f"{code}: {len(rows_)} rows detected, {len(lines)} lines given")
        ti = 0; ntext = sum(1 for l in lines if l)
        for r, ln in zip(rows_, lines):
            if not ln: art += r["c"]; continue
            forced = None
            if isinstance(ln, tuple): ln, forced = ln
            toks = ln.split(" "); ws = words_of(r)
            real = [t_ for t_ in toks if not t_.startswith("@")]
            if len(ws) != len(real):
                raise SystemExit(f"{code}: row '{ln}': {len(ws)} word clusters {[round(min(c['b'][0] for c in w)) for w in ws]} for {len(real)} words")
            ser = forced or (lab_series[ti][1] if len(lab_series) == ntext else None)
            if ser is None: raise SystemExit(f"{code}: series for '{ln}' not resolved: labels {lab_series} vs {ntext} text rows; give (text, series)")
            ti += 1
            meas = []; wi = 0
            for t_ in toks:
                if t_.startswith("@") or t_ == "*": meas.append(None if t_.startswith("@") else "art"); 
                if t_.startswith("@"): continue
                w = ws[wi]; wi += 1
                if t_ == "*": art += w; continue
                x0_ = min(c["b"][0] for c in w); x1_ = max(c["b"][2] for c in w); tall = [c for c in w if c["b"][3] - c["b"][1] > 0.6 * max(c2["b"][3] - c2["b"][1] for c2 in w)]
                y0_ = min(c["b"][1] for c in tall); y1_ = max(c["b"][3] for c in tall); hh = y1_ - y0_
                lower = not re.search(r"[A-Z0-9]", t_)
                if lower:
                    cap = hh if re.search(r"[bdfhklt]", t_) else hh / 0.75; s2 = "Emod"; top = y1_ - cap
                else:
                    med = sorted(c["b"][3] - c["b"][1] for c in tall)[len(tall) // 2]
                    near = [h_ for h_ in lab_all if abs(h_ - med) < 0.07 * med]
                    cap = min(near, key=lambda h_: abs(h_ - med)) if near else round(med / 5) * 5; s2 = ser; top = y0_ if not re.search(r"[a-z]", t_) else y1_ - cap
                    if abs(cap - med) > 0.07 * med: trep.append((t_, "cap label mismatch", round(med, 1), cap))
                meas.append({"t": t_, "x0": x0_, "x1": x1_, "top": top, "cap": round(cap, 2) if lower else cap, "ser": s2, "col": w[0]["col"], "ratio": (x1_ - x0_) / max(1, width(t_, s2, cap))})
            real_m = [m_ for m_ in meas if isinstance(m_, dict)]
            # placeholders: centred in the gap between their neighbours
            out_tokens = []
            idx = 0
            for j, t_ in enumerate(toks):
                if t_ == "*": continue
                if t_.startswith("@"):
                    prev = next((m_ for m_ in reversed(out_tokens) if "x1" in m_), None)
                    nxt = None; cnt = 0
                    for t2 in toks[j + 1:]:
                        if t2.startswith("@") or t2 == "*": continue
                        nxt = real_m[sum(1 for q in toks[:j] if not q.startswith("@") and q != "*") + cnt]; break
                    lo = prev["x1"] if prev else (nxt["x0"] - 2.2 * nxt["cap"]); hi = nxt["x0"] if nxt else (prev["x1"] + 2.2 * prev["cap"])
                    ref = prev or nxt; capn = max(m_["cap"] for m_ in real_m if m_["ser"] != "Emod") if any(m_["ser"] != "Emod" for m_ in real_m) else ref["cap"]
                    out_tokens.append({"t": t_[1:], "cx": (lo + hi) / 2, "top": min(m_["top"] for m_ in real_m), "cap": capn, "ser": ser, "col": ref["col"], "ph": True})
                else:
                    out_tokens.append(real_m[sum(1 for q in toks[:j] if not q.startswith("@") and q != "*")])
            uniform = len({(m_["cap"], m_["ser"], round(m_["top"])) for m_ in out_tokens}) == 1 and not any(m_.get("ph") for m_ in out_tokens)
            if uniform and len(out_tokens) > 1:
                g = [round(out_tokens[i + 1]["x0"] - out_tokens[i]["x1"]) for i in range(len(out_tokens) - 1)]
                e = TW([m_["t"] for m_ in out_tokens], out_tokens[0]["ser"], out_tokens[0]["cap"], rd(out_tokens[0]["top"]), g[0] if len(set(g)) == 1 else g)
                c = (out_tokens[0]["x0"] + out_tokens[-1]["x1"]) / 2
                if abs(c - W / 2) > 0.004 * W + 3: e["cx"] = rd(c)
                if out_tokens[0]["col"] != "black": e["colour"] = out_tokens[0]["col"]
                text_els.append(e)
            else:
                for m_ in out_tokens:
                    c = m_["cx"] if m_.get("ph") else (m_["x0"] + m_["x1"]) / 2
                    e = T(m_["t"], m_["ser"], m_["cap"], rd(m_["top"]))
                    if abs(c - W / 2) > 0.004 * W + 3: e["cx"] = rd(c)
                    if m_["col"] != "black": e["colour"] = m_["col"]
                    text_els.append(e)
            legend_parts.append(" ".join(m_["t"] for m_ in out_tokens))
            trep.append((ln, ser, [(m_["t"], m_["cap"], "top %.1f" % m_["top"], "" if m_.get("ph") else "r%.3f" % m_["ratio"]) for m_ in out_tokens]))
    if art and not no_symbols:
        sid = "qld_" + code.lower().replace("_", "-") + "_artwork"
        ax0 = min(c["b"][0] for c in art); ay0 = min(c["b"][1] for c in art); ax1 = max(c["b"][2] for c in art); ay1 = max(c["b"][3] for c in art)
        out_ = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ax1 - ax0:.2f} {ay1 - ay0:.2f}">']
        order = {id(c): n_ for n_, c in enumerate(CT)}
        for c in sorted(art, key=lambda c: (c["f"]["i"], order[id(c)])):
            sm = [[(seg[0],) + tuple((p[0] - ax0, p[1] - ay0) for p in seg[1:]) for seg in x["sm"]] for x in [c] + c["kids"]]
            fillc = "currentColor" if c["col"] == "black" else G.COLOURS.get(c["col"], "#000")
            out_.append(f'<path fill="{fillc}" d="{fix(_vec.dstr(sm))}"/>')
        out_.append("</svg>")
        open(ROOT + "/tools/symbols/" + sid + ".svg", "w").write("\n".join(out_) + "\n")
        m = [round(ax0, 1), round(ay0, 1), round(ax1 - ax0, 1), round(ay1 - ay0, 1)]
        els.append(S(sid, *m)); cols = sorted({c["col"] for c in art})
        symbols = symentry(sid, drawing, f"the sign's symbol artwork: {len(art)} vector outlines of the sheet PDF ({', '.join(cols)})", cols)
        sym_note = f" Symbol artwork: the sheet PDF's own vector outlines (tools/symbols/{sid}.svg, {len(art)} outlines), placed as drawn: {m[2]} x {m[3]} at x {m[0]}, y {m[1]}."
    els += text_els
    # text
    im = Image.open(PNG + drawing + ".png").convert("RGB")
    lab_h = []
    for t in labels:
        for m_ in re.finditer(r"(\d{2,3})\s?(?:Mod\s?E|[B-F](?:[NMW]|M)?\b|EM|Em|LC|lc|ModE)", t["t"]): lab_h.append(int(m_.group(1)))
    FT = sorted([t for t in TX if is_leg(t) and inside(t["b"], 6)], key=lambda t: (round(t["b"][1] / (0.03 * (ob[3] - ob[1]))), t["b"][0]))
    for t in FT:
        if t["t"] in drop_text: continue
        ser = series_of(t["font"]); b = t["b"]
        # the dimension label level with this line (right or left of the sign): series letter and heights
        cy = (b[1] + b[3]) / 2; near = sorted((l_ for l_ in labels if re.search(r"\d{2,3}\s?(Mod\s?E|[B-F]|LC|lc)", l_["t"]) and (l_["b"][0] > ob[2] or l_["b"][2] < ob[0])), key=lambda l_: abs((l_["b"][1] + l_["b"][3]) / 2 - cy))
        row_lab = [l_ for l_ in near[:3] if abs((l_["b"][1] + l_["b"][3]) / 2 - cy) < 0.75 * (b[3] - b[1])]
        row_txt = " ".join(l_["t"] for l_ in row_lab)
        if ser is None:
            m_ = re.search(r"\d{2,3}\s?(Mod\s?E|[B-F])", row_txt)
            ser = (series or {}).get(t["t"]) or ("Emod" if not re.search(r"[A-Z0-9]", t["t"]) else (("E" if m_.group(1).startswith("Mod") else m_.group(1)) if m_ else None))
            if ser is None: trep.append((t["t"], "NO SERIES")); continue
        if (series or {}).get(t["t"]): ser = series[t["t"]]
        row_h = [int(x) for x in re.findall(r"(\d{2,3})\s?(?:Mod\s?E|[B-F]|LC|lc|Em|EM)", row_txt)]
        # background = most common colour in the bbox; ink = far from it
        x0, y0, x1, y1 = int(b[0]) + 1, int(b[1] - 2), int(b[2]), int(b[3] + 2)
        ext = int(0.6 * (y1 - y0)); y0e, y1e = y0 - ext, y1 + ext
        crop = im.crop((x0, y0e, x1, y1e)); px = crop.load()
        cnt = collections.Counter(im.crop((x0, y0, x1, y1)).getdata()); bg = cnt.most_common(1)[0][0]
        fg = [c for c, n in cnt.most_common(6) if dist(c, bg) > 150]
        inkc = fg[0] if fg else None
        isink = (lambda p: dist(p, inkc) < 110) if inkc else (lambda p: dist(p, bg) > 150)
        rowink = [sum(1 for x in range(crop.width) if isink(px[x, y])) >= 2 for y in range(crop.height)]
        mid = [y for y in range(ext, crop.height - ext) if rowink[y]]
        if mid and not re.search(r"[A-Z0-9bdfhklt]", t["t"]): ys = [mid[0], mid[-1]]
        elif mid:
            ya, yb = mid[0], mid[-1]
            while ya > 0 and rowink[ya - 1]: ya -= 1
            while yb < crop.height - 1 and rowink[yb + 1]: yb += 1
            ys = [ya, yb]
        else: ys = []
        xs = [x for x in range(crop.width) if ys and any(isink(px[x, y]) for y in range(ys[0], ys[-1] + 1))]
        y0 = y0e
        txt = t["t"]
        if text_fix and txt in text_fix: txt = text_fix[txt]
        est = t["size"] / k * 0.722
        if not ys or not xs:
            trep.append((txt, "NO INK")); continue
        it, ib = (y0 + ys[0] - ob[1]) / k, (y0 + ys[-1] + 1 - ob[1]) / k; il, ir = (x0 + xs[0] - ob[0]) / k, (x0 + xs[-1] + 1 - ob[0]) / k
        lower_only = not re.search(r"[A-Z0-9]", txt)
        if lower_only:
            cap = (ir - il) / (width(txt, "Emod", 100) / 100)      # from the ink width (the span box clips the glyphs)
            cc = [h for h in row_h + lab_h] + [round(h / 0.75, 2) for h in row_h + lab_h]
            nearc = sorted((h for h in cc if abs(h - cap) < 0.08 * cap), key=lambda h: abs(h - cap)); cap = nearc[0] if nearc else round(cap, 1); top = ib - cap
            if abs(top - round(top / 5) * 5) < 1.6: top = round(top / 5) * 5
        else:
            capm = (ib - it)
            cands = [h for h in (row_h or lab_h) if abs(h - capm) < 0.09 * capm] or [h for h in lab_h if abs(h - capm) < 0.06 * capm]
            est = capm
            cap = min(cands, key=lambda h: abs(h - est)) if cands else round(est / 5) * 5
            top = it + max(0, min(capm - cap, 0.07 * cap)) / 2 if not re.search(r"[Q,;]", txt) else it + 0.02 * cap
            if re.search(r"[a-z]", txt) and not re.match(r"[A-Z0-9bdfhklt]", txt): top = ib - cap
            if abs(top - round(top / 5) * 5) < 1.6: top = round(top / 5) * 5
        col = cname("#%02x%02x%02x" % inkc) if inkc else "black"
        inkn = sum(1 for y in range(ys[0], ys[-1] + 1) for x in range(xs[0], xs[-1] + 1) if isink(px[x, y]))
        dotted = inkn / max(1, (ys[-1] - ys[0] + 1) * (xs[-1] - xs[0] + 1)) < 0.16 and re.fullmatch(r"[\d.:\- ]+", txt) is not None
        if dotted: variable.append(txt); col = [c_ for c_ in (e_.get("colour", "black") for e_ in els if e_["type"] == "text")][-1] if any(e_["type"] == "text" for e_ in els) else "black"
        if (caps or {}).get(txt): cap = caps[txt]
        words = txt.split(" ")
        e = {"type": "text", "series": ser, "height": cap, "top": rd(top)}
        tot = sum(width(w_, ser, cap) for w_ in words if w_)
        words = [w_ for w_ in words if w_]
        if len(words) == 1: e["text"] = words[0]; g = []
        else:
            # word gaps: split the ink columns at gaps > 0.42 cap
            segs = []; st = pv = xs[0]
            for x in xs[1:]:
                if (x - pv) / k > 0.42 * cap: segs.append((st, pv)); st = x
                pv = x
            segs.append((st, pv))
            if len(segs) == len(words): g = [round((segs[i + 1][0] - segs[i][1]) / k) for i in range(len(segs) - 1)]
            else: g = [round(max(0.45 * cap, (ir - il - tot) / (len(words) - 1)))] * (len(words) - 1); trep.append((txt, "gap fallback", len(segs)))
            e["words"] = words; e["gap"] = g[0] if len(set(g)) == 1 else g
        c = (il + ir) / 2
        if abs(c - W / 2) > 0.004 * W + 3: e["cx"] = rd(c)
        if col != "black": e["colour"] = col
        els.append(e); legend_parts.append(txt)
        trep.append((txt, ser, cap, "est %.0f" % est, "top %.1f" % top, "drawn/AS %.3f" % ((ir - il - sum(g)) / tot if tot else 0), col))
    if fill_box is not None:
        # every numeral box without a legend in it takes the vary placeholder, sized and seated as the capital line beside it
        txt_e = [e for e in els if e["type"] == "text" and "series" in e]
        for q in (box_mm or boxes):
            cyq = (q[1] + q[3]) / 2; cxq = (q[0] + q[2]) / 2
            row = [e for e in txt_e if e["top"] - 5 <= cyq <= e["top"] + e["height"] + 5 and e["series"] != "Emod"]
            if any(abs(e.get("cx", W / 2) - cxq) < 0.3 * (q[2] - q[0]) for e in row): continue
            ref = min(row, key=lambda e: abs(e.get("cx", W / 2) - cxq)) if row else None
            if ref is None: trep.append(("box", q, "NO REFERENCE LINE")); continue
            e = T(fill_box, fill_series or ref["series"], ref["height"], ref["top"], cx=rd(cxq))
            if ref.get("colour"): e["colour"] = ref["colour"]
            els.append(e); trep.append(("box filled", q, e["series"], e["height"], e["top"]))
    els += stroke_els
    if add: els += add
    lab_txt = " | ".join(t["t"] for t in sorted(labels, key=lambda t: (t["b"][0] > ob[2], t["b"][1])) if t["b"][1] < ob[3] + 120 and t["b"][3] > ob[1] - 160 and len(t["t"]) < 14 and re.search(r"\d", t["t"]))
    title = title_of(page)
    notes = (f"TMR Queensland design sheet {code.replace('_p', ' page ')} '{title}', directly dimensioned and drawn to scale (the drawn outline is {W} x {H:.0f} by the sheet's own width label); built from the sheet PDF itself: panel geometry and artwork are the sheet's vectors, legend lines are the sheet's live text placed where the sheet draws them (cap tops and centres measured on the 200 dpi render), letter heights from the sheet's labels, AS 1744 (plus0) spacing ('DN' / 'DM' / 'EN' / 'CN' etc. read as the plain series). "
             f"Size {W} x {Hr}" + (f", R{radius}" if radius else "") + f"; layers from the vectors: {', '.join(f'{c} from {rd(i)}' for c, i in layers)}. Sheet labels: {lab_txt}." + sym_note + (f" Variable legend (drawn dotted in a dashed box on the sheet): {', '.join(variable)} - the sheet's example value is generated." if variable else "") + (" " + notes_extra if notes_extra else ""))
    if diamond: kw_shape = {"shape": "diamond"}
    else: kw_shape = {}
    kw = dict(panel_px=ppx, drawing=drawing, base=False, **spec_kw, **kw_shape)
    if hands: kw["hands"] = hands; kw["drawn_hand"] = drawn_hand or hands[0]
    if table_note: notes = notes.replace("directly dimensioned and drawn to scale (the drawn outline is", "with a lettered size table: " + table_note + " The drawing is to scale for that size (the drawn outline scales to")
    if radius: kw["radius"] = radius
    if symbols: kw["symbols"] = symbols
    if family: kw["folder"] = family
    if vary: kw["vary"] = vary
    if drawn_value is not None: kw["drawn_value"] = drawn_value
    leg = legend or " ".join(legend_parts)
    if name is None:
        wds = re.sub(r"[^A-Za-z0-9.\- ]", "", leg).upper().split()
        asp = W / Hr; shape = "SQUARE" if 0.9 < asp < 1.1 else "TALL" if asp < 0.9 else "LONG" if 1.8 < asp < 2.3 else "WIDE" if 2.7 < asp < 3.4 else "LONG_SKINNY" if 3.6 < asp < 4.6 else "WIDE_SKINNY" if asp > 5.4 else ""
        base_ = "_".join(wds)
        while len(base_) > 70 and "_" in base_: base_ = base_.rsplit("_", 1)[0]
        name = "_".join(x for x in (base_, (spec_kw.get("ground") or "").upper(), shape) if x)
    mk(code, name, leg, [W, Hr], els, notes, **kw)
    return {"code": code, "name": name, "boxes": [[round(v) for v in q] for q in boxes], "variable": variable, "size": (W, round(H, 1)), "layers": layers, "radius": radius, "text": trep, "nsym": len(symitems), "rows": rowrep, "labels": lab_txt, "title": title, "strokes": len(stroke_els), "panels": sum(1 for e in els if e["type"] in ("rect", "path")) - len(stroke_els)}
def title_of(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            r = _mu.Rect(l["bbox"]) * page.rotation_matrix; r.normalize()
            t = " ".join(sp["text"].strip() for sp in l["spans"]).strip()
            if r.y0 * K > 1880 and r.x0 * K > 700 and t and not re.search(r"APPROVED|ENGINEER|Date|Traffic Eng|^\d\d/\d\d/\d\d|^[A-G]$|MANAGER|OFFICIAL|Page|^TC\d", t): out.append(t)
    return " ".join(out)[:120]
def report(r):
    print(f"## {r['code']} {r['name']} var={r['variable']} {r['size']} R{r['radius']} layers {[(c, round(i, 1)) for c, i in r['layers']]} panels {r['panels']} strokes {r['strokes']} symitems {r['nsym']}")
    print("   title:", r["title"]); print("   labels:", r["labels"])
    if r["boxes"]: print("   dashed boxes (mm):", r["boxes"])
    for t in r["rows"]: print("   row", t)
    for t in r["text"]: print("   ", t)
