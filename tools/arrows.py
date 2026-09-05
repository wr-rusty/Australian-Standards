#!/usr/bin/env python3
"""
arrows.py — geometric arrows for AS 1743 signs, drawn from the drawings' stated dimensions.

An arrow is a constant-width shaft along a centreline plus a head at the end.
Centreline elements (walked from the tail, local x = heading direction):
  {"line": L}                                   straight length L
  {"arc": {"r_inner": R, "sweep": deg, "turn": "left"|"right"}}   (or "r_outer" / "r" = centreline radius)
  {"corner": {"turn": "left"|"right", "angle": 90, "r_outer": Ro, "r_inner": Ri}}   sharp bend with fillets
Head (at the end of the centreline):
  {"length": HL,        barb line to tip
   "width": HW,         barb tip to barb tip (outer extremes, radii included)
   "notch": ND,         how far ahead of the barb line the head base meets the shaft (0 = flat base; negative = base behind the barb line)
   "barb_step": s,      short edge at each barb, from the barb tip corner inward (perpendicular to the axis) before the base line
   "tip_r": Rt, "barb_r": Rb, "step_r": Rs, "tip_flat": f}
Element in a spec:
  {"type":"arrow","width":110,"path":[...],"head":{...},"heading":-90,"x":..,"y":..,"w":..,"h":..,"fit":"center"}
Tapered straight shaft (guide-sign block arrows): add "width_head" (shaft width where it meets the head) and
optionally "tail_r" (radius at the tail corners); allowed only with a single {"line": L} path.
`heading` in degrees, 0 = pointing right, -90 = up, 180 = left, -45 = up-right.  The finished outline is fitted into
the box (x,y,w,h) by centring (fit "center"), or anchored at the box's top-left ("topleft"); a size mismatch > 2 % is reported.
Returns SVG path data in sign mm.
"""
import math

def fmt(v):
    if isinstance(v, float): return f"{v:.2f}".rstrip("0").rstrip(".") or "0"
    return str(v)

# ---------------------------------------------------------------- centreline walk
def _walk(path_els, width):
    """Return list of primitives with absolute local coords: ('line', p0, p1) and
    ('arc', centre, r_centre, a0, a1, turn) plus corner markers ('corner', turn, angle, ro, ri) between lines."""
    prims = []; pos = (0.0, 0.0); hd = 0.0
    for el in path_els:
        if "line" in el:
            L = float(el["line"]); p1 = (pos[0] + L * math.cos(hd), pos[1] + L * math.sin(hd))
            prims.append(("line", pos, p1)); pos = p1
        elif "arc" in el:
            a = el["arc"]; turn = a.get("turn", "left"); sweep = math.radians(float(a["sweep"]))
            if "r" in a: R = float(a["r"])
            elif "r_inner" in a: R = float(a["r_inner"]) + width / 2
            else: R = float(a["r_outer"]) - width / 2
            sgn = -1 if turn == "left" else 1          # y down: left turn = decreasing angle (counter-clockwise on screen)
            nx, ny = -math.sin(hd), math.cos(hd)       # left normal in y-down coords is (sin, -cos)... define explicitly:
            # left-hand normal (screen): rotate heading by -90deg
            lx, ly = math.sin(hd), -math.cos(hd)
            cx, cy = (pos[0] + lx * R, pos[1] + ly * R) if turn == "left" else (pos[0] - lx * R, pos[1] - ly * R)
            a0 = math.atan2(pos[1] - cy, pos[0] - cx); a1 = a0 + sgn * sweep
            prims.append(("arc", (cx, cy), R, a0, a1, turn))
            pos = (cx + R * math.cos(a1), cy + R * math.sin(a1)); hd = hd + sgn * sweep
        elif "corner" in el:
            c = el["corner"]; turn = c.get("turn", "left"); ang = math.radians(float(c.get("angle", 90)))
            prims.append(("corner", turn, ang, float(c.get("r_outer", 0)), float(c.get("r_inner", 0))))
            hd = hd + (-ang if turn == "left" else ang)
    return prims, pos, hd

def _offset_side(prims, width, side):
    """side = +1 for the left edge (screen-left of heading), -1 for the right edge. Returns list of
    ('L', p) / ('A', r, sweepflag, p) segments starting with ('M', p)."""
    d = width / 2
    segs = []
    def left_normal(p0, p1):
        vx, vy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(vx, vy)
        return (vy / L, -vx / L)
    # first pass: build segments; corners handled by trimming neighbouring lines
    i = 0; out = []
    while i < len(prims):
        pr = prims[i]
        if pr[0] == "line":
            _, p0, p1 = pr; n = left_normal(p0, p1)
            q0 = (p0[0] + side * d * n[0], p0[1] + side * d * n[1]); q1 = (p1[0] + side * d * n[0], p1[1] + side * d * n[1])
            out.append(["line", q0, q1])
        elif pr[0] == "arc":
            _, c, R, a0, a1, turn = pr
            r = R - d if (turn == "left") == (side == 1) else R + d
            out.append(["arc", c, r, a0, a1])
        else:
            out.append(list(pr))
        i += 1
    # apply corners: between line k-1 and line k+1 with corner at k
    for k, o in enumerate(out):
        if o[0] != "corner": continue
        _, turn, ang, ro, ri = o
        inner = (turn == "left") == (side == 1)
        r = ri if inner else ro
        prev, nxt = out[k - 1], out[k + 1]
        if r <= 0 or prev[0] != "line" or nxt[0] != "line":
            # sharp: intersect the two offset lines
            P = _intersect(prev[1], prev[2], nxt[1], nxt[2]); prev[2] = P; nxt[1] = P; o[:] = ["skip"]; continue
        P = _intersect(prev[1], prev[2], nxt[1], nxt[2])
        t = r / math.tan(ang / 2)
        u1 = _unit(prev[1], P); u2 = _unit(P, nxt[2])
        A = (P[0] - u1[0] * t, P[1] - u1[1] * t); B = (P[0] + u2[0] * t, P[1] + u2[1] * t)
        prev[2] = A; nxt[1] = B
        cross = u1[0] * u2[1] - u1[1] * u2[0]
        o[:] = ["fillet", r, 1 if cross > 0 else 0, B]
    for o in out:
        if o[0] == "line":
            if not segs: segs.append(("M", o[1]))
            segs.append(("L", o[2]))
        elif o[0] == "arc":
            c, r, a0, a1 = o[1], o[2], o[3], o[4]
            p0 = (c[0] + r * math.cos(a0), c[1] + r * math.sin(a0)); p1 = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1))
            if not segs: segs.append(("M", p0))
            sweepflag = 1 if a1 > a0 else 0; large = 1 if abs(a1 - a0) > math.pi else 0
            samples = [(c[0] + r * math.cos(a0 + (a1 - a0) * k / 12), c[1] + r * math.sin(a0 + (a1 - a0) * k / 12)) for k in range(1, 12)]
            segs.append(("A", r, large, sweepflag, p1, samples))
        elif o[0] == "fillet":
            segs.append(("A", o[1], 0, o[2], o[3]))
    return segs

def _unit(p, q):
    L = math.hypot(q[0] - p[0], q[1] - p[1]); return ((q[0] - p[0]) / L, (q[1] - p[1]) / L)

def _intersect(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9: return p2
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

# ---------------------------------------------------------------- head
def _head_polygon(width, head):
    """Head polygon in local coords with barb line at x=0, tip at +x. Returns (points, radii)."""
    HL = float(head["length"]); HW = float(head["width"]); ND = float(head.get("notch", 0))
    step = float(head.get("barb_step", 0)); Rt = float(head.get("tip_r", 0)); Rb = float(head.get("barb_r", 0))
    Rs = float(head.get("step_r", 0)); flat = float(head.get("tip_flat", 0)); sw = width / 2
    pts = []; rad = []
    # tip
    if flat > 0:
        pts += [(HL, -flat / 2), (HL, flat / 2)]; rad += [Rt, Rt]
    else:
        pts.append((HL, 0)); rad.append(Rt)
    # right barb (screen +y), then base to shaft, then across to the other side
    pts.append((0, HW / 2)); rad.append(Rb)
    if step > 0: pts.append((0, HW / 2 - step)); rad.append(Rs)
    pts.append((ND, sw)); rad.append(0)
    pts.append((ND, -sw)); rad.append(0)
    if step > 0: pts.append((0, -HW / 2 + step)); rad.append(Rs)
    pts.append((0, -HW / 2)); rad.append(Rb)
    return pts, rad

def rounded_polygon_path(pts, radii):
    n = len(pts); out = []
    for i in range(n):
        r = radii[i]; p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*v1); l2 = math.hypot(*v2); u1 = (v1[0] / l1, v1[1] / l1); u2 = (v2[0] / l2, v2[1] / l2)
        theta = math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])))
        t = r / math.tan(theta / 2) if r > 0 and theta > 1e-6 else 0
        t = min(t, l1 / 2, l2 / 2)
        a = (p1[0] + u1[0] * t, p1[1] + u1[1] * t); b = (p1[0] + u2[0] * t, p1[1] + u2[1] * t)
        rr = t * math.tan(theta / 2)
        out.append((a, b, 0 if (u1[0] * u2[1] - u1[1] * u2[0]) > 0 else 1, rr))
    d = f"M{fmt(out[0][0][0])} {fmt(out[0][0][1])}"
    for i in range(n):
        a, b, sw, rr = out[i]
        if rr > 0: d += f"A{fmt(rr)} {fmt(rr)} 0 0 {sw} {fmt(b[0])} {fmt(b[1])}"
        na = out[(i + 1) % n][0]; d += f"L{fmt(na[0])} {fmt(na[1])}"
    return d + "Z"

def rounded_extents(pts, radii):
    """Bounding box of the rounded polygon (arcs sampled)."""
    n = len(pts); xs = []; ys = []
    for i in range(n):
        r = radii[i]; p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*v1); l2 = math.hypot(*v2); u1 = (v1[0] / l1, v1[1] / l1); u2 = (v2[0] / l2, v2[1] / l2)
        theta = math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])))
        t = r / math.tan(theta / 2) if r > 0 and theta > 1e-6 else 0
        t = min(t, l1 / 2, l2 / 2); rr = t * math.tan(theta / 2)
        if rr <= 0: xs.append(p1[0]); ys.append(p1[1]); continue
        a = (p1[0] + u1[0] * t, p1[1] + u1[1] * t); b = (p1[0] + u2[0] * t, p1[1] + u2[1] * t)
        bis = (u1[0] + u2[0], u1[1] + u2[1]); bl = math.hypot(*bis); bis = (bis[0] / bl, bis[1] / bl)
        c = (p1[0] + bis[0] * rr / math.sin(theta / 2), p1[1] + bis[1] * rr / math.sin(theta / 2))
        a0 = math.atan2(a[1] - c[1], a[0] - c[0]); a1 = math.atan2(b[1] - c[1], b[0] - c[0])
        da = a1 - a0
        while da > math.pi: da -= 2 * math.pi
        while da < -math.pi: da += 2 * math.pi
        for k in range(13):
            ang = a0 + da * k / 12; xs.append(c[0] + rr * math.cos(ang)); ys.append(c[1] + rr * math.sin(ang))
    return min(xs), min(ys), max(xs), max(ys)

def head_polygon_fitted(width, head):
    """Head polygon whose ROUNDED outline spans exactly head.length (rear extreme to tip) and head.width,
    as the drawings dimension them; the rear extreme sits on x = 0 (the barb line)."""
    HL = float(head["length"]); HW = float(head["width"])
    if head.get("dims") == "vertices": return _head_polygon(width, head)
    h2 = dict(head); L, Wd = HL, HW
    for _ in range(6):
        h2["length"] = L; h2["width"] = Wd
        pts, rad = _head_polygon(width, h2)
        x0, y0, x1, y1 = rounded_extents(pts, rad)
        L += HL - (x1 - x0); Wd += HW - (y1 - y0)
    pts, rad = _head_polygon(width, h2)
    x0, y0, x1, y1 = rounded_extents(pts, rad)
    return [(x - x0, y) for x, y in pts], rad

# ---------------------------------------------------------------- assemble
def build(el):
    """Return (path_d, bbox (minx,miny,maxx,maxy)) in sign mm for an arrow element."""
    width = float(el["width"]); heading = math.radians(float(el.get("heading", 0)))
    path_els = list(el.get("path", []))
    prims, end, hd = _walk(path_els, width)
    if el.get("head") and float(el["head"].get("notch", 0)) > 0 and path_els:
        # run the shaft on into the head as far as the notch so there is no gap behind the head base
        prims, _, _ = _walk(path_els + [{"line": float(el["head"]["notch"])}], width)
    subpaths = []; pts_all = []
    def T(p):  # local -> rotated by heading (about origin)
        c, s = math.cos(heading), math.sin(heading)
        return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)
    def seg_to_d(segs):
        d = ""
        for sgm in segs:
            if sgm[0] == "M": p = T(sgm[1]); pts_all.append(p); d += f"M{fmt(p[0])} {fmt(p[1])}"
            elif sgm[0] == "L": p = T(sgm[1]); pts_all.append(p); d += f"L{fmt(p[0])} {fmt(p[1])}"
            elif sgm[0] == "A":
                p = T(sgm[4]); pts_all.append(p); d += f"A{fmt(sgm[1])} {fmt(sgm[1])} 0 {sgm[2]} {sgm[3]} {fmt(p[0])} {fmt(p[1])}"
                if len(sgm) > 5: pts_all.extend(T(q) for q in sgm[5])
        return d
    wh = float(el.get("width_head", width))
    if el.get("width_head") is not None and len(path_els) == 1 and "line" in path_els[0]:
        # tapered straight shaft: width at the tail -> width_head where it meets the head (at the notch)
        L = float(path_els[0]["line"]) + (float(el["head"].get("notch", 0)) if el.get("head") else 0)
        tr_ = float(el.get("tail_r", 0))
        poly = [(0, -width / 2), (L, -wh / 2), (L, wh / 2), (0, width / 2)]
        poly = [T(p) for p in poly]
        ex0, ey0, ex1, ey1 = rounded_extents(poly, [tr_, 0, 0, tr_]); pts_all += [(ex0, ey0), (ex1, ey1)]
        subpaths.append(rounded_polygon_path(poly, [tr_, 0, 0, tr_]))
        prims = []
    if prims:
        left = _offset_side(prims, width, +1); right = _offset_side(prims, width, -1)
        # shaft outline: left edge forward, straight across the head base to the right edge's end, right edge backward
        d = seg_to_d(left)
        pts = [right[0][1]] + [sg[4] if sg[0] == "A" else sg[1] for sg in right[1:]]   # right-edge vertices in forward order
        rev = [("L", pts[-1])]
        for i in range(len(right) - 1, 0, -1):
            sg = right[i]; target = pts[i - 1]
            if sg[0] == "L": rev.append(("L", target))
            else: rev.append(("A", sg[1], sg[2], 1 - sg[3], target) + ((sg[5],) if len(sg) > 5 else ()))
        d += seg_to_d(rev)
        subpaths.append(d + "Z")
    # head at the end, in local frame rotated by hd
    if el.get("head"):
        hp, hr = head_polygon_fitted(wh, el["head"])
        c, s = math.cos(hd), math.sin(hd)
        hp2 = [(end[0] + x * c - y * s, end[1] + x * s + y * c) for x, y in hp]
        hp3 = [T(p) for p in hp2]
        ex0, ey0, ex1, ey1 = rounded_extents(hp3, hr); pts_all += [(ex0, ey0), (ex1, ey1)]   # extents of the rounded outline
        subpaths.append(rounded_polygon_path(hp3, hr))
    # bbox from points (plus arc bulge approximation: include arc midpoints)
    minx = min(p[0] for p in pts_all); maxx = max(p[0] for p in pts_all); miny = min(p[1] for p in pts_all); maxy = max(p[1] for p in pts_all)
    return " ".join(subpaths), (minx, miny, maxx, maxy)

def place(el, W=None):
    """Build and translate into the element's box. Returns (d, warning or '')."""
    d, (x0, y0, x1, y1) = build(el)
    bw, bh = x1 - x0, y1 - y0
    fit = el.get("fit", "center")
    if fit == "topleft": tx, ty = el["x"] - x0, el["y"] - y0
    else: tx, ty = el["x"] + el["w"] / 2 - (x0 + x1) / 2, el["y"] + el["h"] / 2 - (y0 + y1) / 2
    warn = ""
    if abs(bw - el["w"]) > 0.02 * el["w"] or abs(bh - el["h"]) > 0.02 * el["h"]:
        warn = f"arrow size {bw:.1f}x{bh:.1f} vs box {el['w']}x{el['h']}"
    return _translate(d, tx, ty), warn

def _translate(d, tx, ty):
    import re
    out = []; i = 0
    toks = re.findall(r"[MLAZ]|-?\d+\.?\d*", d)
    while i < len(toks):
        t = toks[i]
        if t in "ML": out.append(f"{t}{fmt(float(toks[i+1]) + tx)} {fmt(float(toks[i+2]) + ty)}"); i += 3
        elif t == "A": out.append(f"A{toks[i+1]} {toks[i+2]} {toks[i+3]} {toks[i+4]} {toks[i+5]} {fmt(float(toks[i+6]) + tx)} {fmt(float(toks[i+7]) + ty)}"); i += 8
        elif t == "Z": out.append("Z"); i += 1
        else: i += 1
    return "".join(out)

if __name__ == "__main__":
    import json, sys
    el = json.loads(sys.argv[1]); print(place(el))
