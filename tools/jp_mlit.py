#!/usr/bin/env python3
"""
jp_mlit.py — lift every sign face from the Japanese road-sign list (MLIT 道路標識一覧, one A3 vector page).

The sheet shows about 250 sign faces in five classes, each under a label such as "(301)通行止め" or
"(329-A)徐行". For every label:
  * the page's vector paths and live text are grouped into faces by proximity (the faces are well separated on the
    sheet; a face's parts overlap or touch), and each face goes to the label above it in its cell
  * a label with several example panels gives one file per panel (suffix _1, _2 … in reading order)
  * consecutive labels that share one face (e.g. (305) and (305の2)) give one file; all codes are in the manifest
  * fills are kept as drawn; stroked paths are outlined (curves flattened to 0.01 pt of the sheet); live text is
    outlined from the sheet's embedded TrueType subsets by glyph id; a face with a glyph that cannot be outlined
    goes to SVGs/intervene/ with the reason
  * section headers, cell rules, the title and the labels themselves are dropped
  * the sheet is not to scale: real sizes come from the sign order (標識令 別表第二) figures where they give
    one (SIZES below, source clause in the manifest); otherwise the face is kept at a nominal scale ("size nominal")
Output: Processing/Japan/National (MLIT)/SVGs/<family>/<NAME>_<CODE>.svg + SVGs/MANIFEST.csv, in the library's
SVG convention (viewBox 1 pt = 1 cm of sign, width/height in mm at 72 pt/in, one <g transform="scale(0.1)">).

Usage: jp_mlit.py [--debug DIR]     (--debug writes an overlay of faces and label assignments)
"""
import os, re, sys, io, csv, math, shutil, unicodedata
import pymupdf
from shapely.geometry import LineString, LinearRing, Polygon, MultiPolygon
from shapely.ops import unary_union, substring

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "Processing", "Japan", "National (MLIT)")
PDF = os.path.join(PACK, "Original PDFs", "ichiran.pdf")
OUT = os.path.join(PACK, "SVGs")
FAMILIES = {"1": "Guide Signs", "2": "Warning Signs", "3": "Regulatory Signs", "4": "Instruction Signs", "5": "Supplementary Signs"}
CODE_RE = re.compile(r"\(\s*(\d{3})(?:(?:の|-)(\d+))?(?:の(\d+))?(?:-([A-Z]))?\s*\)")      # after NFKC; the sheet writes 310の2 as "310-2"
LABEL_FONT, LABEL_MAX = "MS-Gothic", 5.2      # labels: MS Gothic, under 5.2 pt, dark grey
NOMINAL = 10.0                                 # mm of sign per sheet point where the order gives no size
# English names by first code of a label (the Japanese title stays in the manifest)
NAMES = {
    "101": "MUNICIPALITY", "102-A": "PREFECTURE", "102-B": "PREFECTURE", "103-A": "EXPRESSWAY ENTRANCE DIRECTION", "103-B": "EXPRESSWAY ENTRANCE DIRECTION",
    "104": "EXPRESSWAY ENTRANCE AHEAD", "105-A": "DESTINATION DIRECTION AND DISTANCE", "105-B": "DESTINATION DIRECTION AND DISTANCE",
    "105-C": "DESTINATION DIRECTION AND DISTANCE", "106-A": "DESTINATION AND DISTANCE", "106-B": "DESTINATION AND DISTANCE", "106-C": "DESTINATION AND DISTANCE",
    "107-A": "DESTINATION AND LANE", "107-B": "DESTINATION AND LANE", "108-A": "DESTINATION AND DIRECTION AHEAD", "108-B": "DESTINATION AND DIRECTION AHEAD",
    "108-2-A": "DESTINATION AND DIRECTION", "108-2-B": "DESTINATION AND DIRECTION", "108-2-C": "DESTINATION AND DIRECTION", "108-2-D": "DESTINATION AND DIRECTION",
    "108-2-E": "DESTINATION AND DIRECTION", "108-3": "DESTINATION DIRECTION AND ROAD NAME AHEAD", "108-4": "DESTINATION DIRECTION AND ROAD NAME",
    "109": "EXIT AHEAD", "110-A": "DESTINATION AND EXIT AHEAD", "110-B": "DESTINATION AND EXIT AHEAD", "111-A": "DESTINATION LANE AND EXIT AHEAD",
    "111-B": "DESTINATION LANE AND EXIT AHEAD", "112-A": "DESTINATION AND EXIT", "112-B": "DESTINATION AND EXIT", "113-A": "EXIT", "113-B": "EXIT",
    "114-A": "NOTED PLACE", "114-B": "NOTED PLACE", "114-C": "NOTED PLACE", "114-2-A": "MAIN POINT", "114-2-B": "MAIN POINT", "115": "TOLL GATE",
    "116": "SERVICE AREA ROADSIDE STATION AND DISTANCE", "116-2-A": "SERVICE AREA ROADSIDE STATION AHEAD", "116-2-B": "SERVICE AREA ROADSIDE STATION AHEAD",
    "116-2-C": "SERVICE AREA ROADSIDE STATION AHEAD", "116-3-A": "SERVICE AREA", "116-3-B": "SERVICE AREA", "116-4": "EMERGENCY TELEPHONE",
    "116-5": "PASSING PLACE", "116-6": "EMERGENCY PARKING BAY", "117-A": "PARKING", "117-B": "PARKING",
    "117-2": "ENTRANCE TO MAIN ROAD FROM SERVICE AREA OR PARKING", "117-3-A": "CLIMBING LANE", "117-3-B": "CLIMBING LANE",
    "118-A": "NATIONAL ROUTE NUMBER", "118-B": "NATIONAL ROUTE NUMBER", "118-C": "NATIONAL ROUTE NUMBER", "118-2-A": "PREFECTURAL ROUTE NUMBER",
    "118-2-B": "PREFECTURAL ROUTE NUMBER", "118-2-C": "PREFECTURAL ROUTE NUMBER", "118-3": "EXPRESSWAY NUMBER",
    "118-4-A": "GROSS WEIGHT LIMIT RELAXED DESIGNATED ROAD", "118-4-B": "GROSS WEIGHT LIMIT RELAXED DESIGNATED ROAD",
    "118-5-A": "HEIGHT LIMIT RELAXED DESIGNATED ROAD", "118-5-B": "HEIGHT LIMIT RELAXED DESIGNATED ROAD", "118-5-C": "HEIGHT LIMIT RELAXED DESIGNATED ROAD",
    "118-5-D": "HEIGHT LIMIT RELAXED DESIGNATED ROAD", "119-A": "ROAD NAME", "119-B": "ROAD NAME", "119-C": "ROAD NAME", "119-D": "ROAD NAME",
    "120-A": "DETOUR", "120-B": "DETOUR", "121-A": "ELEVATOR", "122-A": "ESCALATOR", "123-A": "RAMP", "124-A": "BUS STOP", "125-A": "TRAM STOP", "126-A": "TOILET",
    "201-A": "CROSSROADS", "201-B": "SIDE ROAD JUNCTION", "201-C": "T JUNCTION", "201-D": "Y JUNCTION", "201-2": "ROUNDABOUT", "202": "BEND",
    "203": "SHARP BEND", "204": "REVERSE BEND", "205": "SHARP REVERSE BEND", "206": "WINDING ROAD", "207-A": "RAILWAY CROSSING", "207-B": "RAILWAY CROSSING",
    "208": "SCHOOL KINDERGARTEN NURSERY", "208-2": "TRAFFIC SIGNALS", "209": "SLIPPERY", "209-2": "FALLING ROCKS", "209-3": "UNEVEN ROAD", "210": "MERGING TRAFFIC",
    "211": "LANE REDUCTION", "212": "ROAD NARROWS", "212-2": "TWO WAY TRAFFIC", "212-3": "STEEP ASCENT", "212-4": "STEEP DESCENT", "213": "ROAD WORKS",
    "214": "CROSSWIND", "214-2": "ANIMALS CROSSING", "215": "OTHER DANGER",
    "301": "ROAD CLOSED", "302": "CLOSED TO VEHICLES", "303": "NO ENTRY", "304": "CLOSED TO MOTOR VEHICLES EXCEPT MOTORCYCLES",
    "305": "CLOSED TO LARGE GOODS VEHICLES", "306": "CLOSED TO LARGE PASSENGER VEHICLES", "307": "CLOSED TO MOTORCYCLES AND MOPEDS",
    "308": "CLOSED TO LIGHT VEHICLES EXCEPT BICYCLES", "309": "CLOSED TO SPECIFIED SMALL MOPEDS AND BICYCLES", "310": "CLOSED TO VEHICLES COMBINATION",
    "310-2": "NO TWO UP RIDING ON MOTORCYCLES", "310-3": "CLOSED TO VEHICLES WITHOUT TYRE CHAINS",
    "311-A": "PROCEED ONLY IN DESIGNATED DIRECTIONS", "311-B": "PROCEED ONLY IN DESIGNATED DIRECTIONS", "311-C": "PROCEED ONLY IN DESIGNATED DIRECTIONS",
    "311-D": "PROCEED ONLY IN DESIGNATED DIRECTIONS", "311-E": "PROCEED ONLY IN DESIGNATED DIRECTIONS", "311-F": "PROCEED ONLY IN DESIGNATED DIRECTIONS",
    "312": "NO CROSSING BY VEHICLES", "313": "NO U TURN", "314": "NO OVERTAKING", "315": "NO STOPPING OR PARKING", "316": "NO PARKING",
    "318": "TIME LIMITED PARKING ZONE", "319": "CLOSED TO VEHICLES CARRYING DANGEROUS GOODS", "320": "WEIGHT LIMIT", "321": "HEIGHT LIMIT", "322": "MAXIMUM WIDTH",
    "323": "MAXIMUM SPEED", "324": "MINIMUM SPEED", "325": "MOTOR VEHICLES ONLY", "325-2": "SPECIFIED SMALL MOPEDS AND BICYCLES ONLY",
    "325-3": "BICYCLES AND PEDESTRIANS ONLY", "325-4": "PEDESTRIANS ONLY", "325-5-A": "PERMITTED VEHICLES ONLY", "325-5-B": "PERMITTED VEHICLES ONLY",
    "325-5-C": "PERMITTED VEHICLES ONLY", "325-6": "PERMITTED VEHICLES COMBINATION ONLY", "325-7": "WIDE AREA DISASTER RESPONSE VEHICLES ONLY",
    "326-A": "ONE WAY", "326-B": "ONE WAY", "326-2-A": "ONE WAY FOR SPECIFIED SMALL MOPEDS AND BICYCLES", "326-2-B": "ONE WAY FOR SPECIFIED SMALL MOPEDS AND BICYCLES",
    "327": "VEHICLE LANE CLASSIFICATION", "327-2": "LANE FOR SPECIFIED VEHICLE TYPES", "327-3": "EXPRESSWAY LANE FOR TOWING VEHICLES", "327-4": "EXCLUSIVE LANE",
    "327-4-2": "BICYCLE EXCLUSIVE LANE", "327-5": "ROUTE BUS PRIORITY LANE", "327-6": "MOTORWAY FIRST LANE DESIGNATED SECTION FOR TOWING VEHICLES",
    "327-7-A": "LANE USE BY DIRECTION", "327-7-B": "LANE USE BY DIRECTION", "327-7-C": "LANE USE BY DIRECTION", "327-7-D": "LANE USE BY DIRECTION",
    "327-8": "MOPED RIGHT TURN TWO STAGE", "327-9": "MOPED RIGHT TURN DIRECT", "327-10": "ROUNDABOUT CLOCKWISE TRAFFIC", "327-11": "PARALLEL PARKING",
    "327-12": "PERPENDICULAR PARKING", "327-13": "ANGLE PARKING", "328": "SOUND HORN", "329-A": "SLOW", "329-B": "SLOW", "330-A": "STOP", "330-B": "STOP",
    "331": "CLOSED TO PEDESTRIANS", "332": "NO PEDESTRIAN CROSSING",
    "401": "RIDING ABREAST PERMITTED", "402": "DRIVING ON TRAMWAY PERMITTED", "402-2": "PARKING PERMITTED", "403-2": "STOPPING PERMITTED", "405": "PRIORITY ROAD",
    "406": "CENTRE LINE", "406-2": "STOP LINE", "407-A": "PEDESTRIAN CROSSING", "407-B": "PEDESTRIAN CROSSING", "407-2": "BICYCLE CROSSING",
    "407-3": "PEDESTRIAN AND BICYCLE CROSSING", "408": "SAFETY ZONE", "409-A": "ADVANCE NOTICE OF REGULATION", "409-B": "ADVANCE NOTICE OF REGULATION",
    "501": "DISTANCE OR AREA", "502": "DAY OR TIME", "503-A": "VEHICLE TYPE", "503-B": "VEHICLE TYPE", "503-C": "VEHICLE TYPE", "503-D": "VEHICLE TYPE",
    "503-2": "REMOTE OPERATED SMALL VEHICLE", "504": "PARKING CLEARANCE", "504-2": "PARKING TIME LIMIT", "505-A": "BEGINS", "505-B": "BEGINS", "505-C": "BEGINS",
    "506": "WITHIN SECTION", "506-2": "WITHIN ZONE", "507-A": "ENDS", "507-B": "ENDS", "507-C": "ENDS", "507-D": "ENDS", "508": "SCHOOL ROUTE", "508-2": "NO OVERTAKING",
    "509": "PRIORITY ROAD AHEAD", "509-2": "RAILWAY CROSSING CAUTION", "509-3": "CROSSWIND CAUTION", "509-4": "ANIMALS CAUTION", "509-5": "CAUTION", "510": "ADVISORY",
    "510-2": "REASON FOR REGULATION", "511": "DIRECTION", "512": "PLACE NAME", "513": "START POINT", "514": "END POINT",
}
# Sizes read from the figures of the sign order (標識令 別表第二, e-Gov law 335M50004002003, figures in Original PDFs/sign-order-figures/).
# (dimension, cm, clause): 'w' width, 'h' height, 'side' side of a point-up square. A bracketed "(a×b)" under a figure is (height × width).
# None = the figure gives no outer size that could be read; the face stays nominal. "CODE#n" addresses example panel n of a label.
_O = "標識令 別表第二 "
SIZES = {
    "116-4": ("w", 60, _O + "(116の4) 図示 (90×60)"), "116-5": ("w", 60, _O + "(116の5) 図示 (90×60)"), "116-6": ("w", 60, _O + "(116の6) 図示 (90×60)"),
    "117-A": ("w", 60, _O + "(117-A) 図示 (60×60)"), "117-B": ("w", 60, _O + "(117-B) 図示 (90×60)"),
    "118-A": ("w", 45, _O + "(118-A) 図示 横 45"), "118-B": ("w", 80, _O + "(118-B) 図示 横 80"), "118-C": ("w", 80, _O + "(118-C) 図示 横 80"),
    "118-2-B": ("w", 80, _O + "(118の2-B) 図示 横 80"), "118-2-C": ("w", 80, _O + "(118の2-C) 図示 横 80"),
    "118-4-A": ("w", 100, _O + "(118の4-A) 図示 横 100"), "118-4-B": ("w", 100, _O + "(118の4-B) 図示 横 100"),
    "118-5-A": ("w", 100, _O + "(118の5-A) 図示 横 100"), "118-5-B": ("w", 100, _O + "(118の5-B) 図示 横 100"),
    "118-5-C": ("w", 100, _O + "(118の5-C) 図示 横 100"), "118-5-D": ("w", 100, _O + "(118の5-D) 図示 横 100"),
    "119-A": ("w", 80, _O + "(119-A) 図示 横 80"), "119-B": ("w", 80, _O + "(119-B) 図示 横 80"), "119-C": ("h", 80, _O + "(119-C) 図示 縦 80"),
    "119-D": ("w", 90, _O + "(119-D) 図示 横 90"), "120-A": ("w", 45, _O + "(120-A) 図示 (30×45)"),
    "326-A": ("w", 60, _O + "(326-A) 図示 (30×60)"), "326-B": ("w", 35, _O + "(326-B) 図示 横 35, 縦 60 以上"),
    "326-2-A": None, "326-2-B": None,
    "327": ("w", 120, _O + "(327) 図示 横 120 以上 (minimum)"), "327-2": ("w", 120, _O + "(327の2) 図示 横 120 以上 (minimum)"),
    "327-3": ("w", 90, _O + "(327の3) 図示 横 90 以上 (minimum)"), "327-4": None, "327-4-2": ("w", 60, _O + "(327の4の2) 図示 横 60 以上 (minimum)"),
    "327-5": ("w", 90, _O + "(327の5) 図示 横 90"), "327-6": ("w", 90, _O + "(327の6) 図示 横 90"),
    "327-7-A": ("w", 120, _O + "(327の7-A) 図示 横 120 以上 (minimum)"), "327-7-B": ("w", 90, _O + "(327の7-B) 図示 (90×90)"), "327-7-C": None, "327-7-D": None,
    "327-11": ("w", 60, _O + "(327の11) 図示 横 60"), "327-12": ("w", 60, _O + "(327の12) 図示 横 60"), "327-13": ("w", 60, _O + "(327の13) 図示 横 60"),
    "329-A": ("tri", 80, _O + "(329-A) 図示 一辺 80, R=5"), "329-B": ("tri", 80, _O + "(329-B) 図示 一辺 80, R=5"),
    "330-A": ("tri", 80, _O + "(330-A) 図示 一辺 80, R=5"), "330-B": ("tri", 80, _O + "(330-B) 図示 一辺 80, R=5"),
    "331": None, "332": None,
    "409-A": ("w", 60, _O + "(409-A) 図示 (90×60)"), "409-B": ("w", 90, _O + "(409-B) 図示 横 90 以上 (minimum)"),
    "507-D": ("w", 40, _O + "(507-D) 図示 直径 40"), "510#2": ("w", 30, _O + "(510) 図示 (30×30)"),
}
CLASS_SIZE = {      # the class figure "本標識板及び柱の規格" at the head of each table
    "Warning Signs": ("side", 45, _O + "警戒標識 本標識板の規格 一辺 45"),
    "Regulatory Signs": ("w", 60, _O + "規制標識 本標識板の規格 直径 60"),
    "Instruction Signs": ("w", 60, _O + "指示標識 本標識板の規格 60×60"),
}
SKIP = set()

GUIDE_Y1, PANEL_GAP = 420.0, 1.6               # guide signs sit above y = 420 pt; panels of one guide assembly are under 1.6 pt apart
JOIN = 0.9                                     # parts of one face are at most this far apart on the sheet (pt)

def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def hexcol(c): return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v * 255)))) for v in c[:3])
def is_dark(c): return c is not None and max(c[:3]) < 0.25

# ---------------------------------------------------------------- geometry

def bez_points(p0, p1, p2, p3, tol=0.01):
    """Flatten one cubic to points (excluding p0), fine enough for stroking and extents."""
    d = max(math.hypot(p1[0] - p0[0], p1[1] - p0[1]), math.hypot(p2[0] - p1[0], p2[1] - p1[1]), math.hypot(p3[0] - p2[0], p3[1] - p2[1]))
    n = max(4, min(64, int(math.sqrt(d / tol) * 1.2) + 1))
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        out.append((u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
                    u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]))
    return out

def subpaths(items, close=False):
    """PyMuPDF drawing items -> list of (segments, closed); a segment is ('l', p, q) or ('c', p0, p1, p2, p3)."""
    subs = []; cur = []; last = None
    def flush():
        nonlocal cur
        if cur:
            a = cur[0][1]; b = cur[-1][-1]
            subs.append((cur, math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-4))
        cur = []
    for it in items:
        k = it[0]
        if k == "re":
            flush(); r = it[1]; pts = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
            subs.append(([("l", pts[i], pts[(i + 1) % 4]) for i in range(4)], True)); last = None; continue
        if k == "qu":
            flush(); q = it[1]; pts = [tuple(q.ul), tuple(q.ur), tuple(q.lr), tuple(q.ll)]
            subs.append(([("l", pts[i], pts[(i + 1) % 4]) for i in range(4)], True)); last = None; continue
        seg = (k,) + tuple((float(p[0]), float(p[1])) for p in it[1:])
        if last is not None and math.hypot(seg[1][0] - last[0], seg[1][1] - last[1]) > 1e-4: flush()
        cur.append(seg); last = seg[-1]
    flush()
    if close and subs and not subs[-1][1]:
        segs, _ = subs[-1]; segs.append(("l", segs[-1][-1], segs[0][1])); subs[-1] = (segs, True)
    return subs

def flat(segs):
    pts = [segs[0][1]]
    for s in segs:
        if s[0] == "l": pts.append(s[2])
        else: pts += bez_points(*s[1:])
    out = [pts[0]]
    for p in pts[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-6: out.append(p)
    return out

def subs_d(subs, T, closed_all=False):
    d = []
    for segs, closed in subs:
        a = T(segs[0][1]); d.append(f"M{fmt(a[0])} {fmt(a[1])}")
        for s in segs:
            if s[0] == "l": q = T(s[2]); d.append(f"L{fmt(q[0])} {fmt(q[1])}")
            else:
                b, c, e = T(s[2]), T(s[3]), T(s[4]); d.append(f"C{fmt(b[0])} {fmt(b[1])} {fmt(c[0])} {fmt(c[1])} {fmt(e[0])} {fmt(e[1])}")
        if closed or closed_all: d.append("Z")
    return "".join(d)

def poly_subs(geom):
    """Shapely (multi)polygon -> closed line subpaths."""
    out = []
    polys = [geom] if isinstance(geom, Polygon) else [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon)]
    for pg in polys:
        for ring in [pg.exterior] + list(pg.interiors):
            pts = list(ring.coords)[:-1]
            if len(pts) >= 3: out.append(([("l", pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))], True))
    return out

def stroke_outline(dr):
    """Outline of a stroked path as a polygon (cap, join, mitre limit and dashes as drawn)."""
    w = dr.get("width") or 0
    if w <= 0: return None
    cap = {0: "flat", 1: "round", 2: "square"}.get((dr.get("lineCap") or (0,))[0], "flat")
    join = {0: "mitre", 1: "round", 2: "bevel"}.get(int(dr.get("lineJoin") or 0), "mitre")
    dash = [float(v) for v in re.findall(r"[\d.]+", (dr.get("dashes") or "").split("]")[0])]
    parts = []
    for segs, closed in subpaths(dr["items"], dr.get("closePath")):
        pts = flat(segs)
        if len(pts) < 2: continue
        if closed and len(pts) > 3 and not dash: line = LinearRing(pts)
        else: line = LineString(pts)
        lines = [line]
        if dash and sum(dash) > 0:
            lines = []; pos = 0.0; i = 0; L = line.length
            if len(dash) % 2: dash = dash * 2
            while pos < L:
                if i % 2 == 0: lines.append(substring(line, pos, min(L, pos + dash[i % len(dash)])))
                pos += dash[i % len(dash)]; i += 1
        for ln in lines:
            if ln.length == 0: continue
            parts.append(ln.buffer(w / 2, cap_style=cap, join_style=join, mitre_limit=10, quad_segs=16))
    if not parts: return None
    return unary_union(parts)

# ---------------------------------------------------------------- fonts

class Fonts:
    """The sheet's embedded TrueType subsets; glyphs are addressed by glyph id (from the text trace)."""
    def __init__(self, doc, page):
        from fontTools.ttLib import TTFont
        self.by_name = {}
        for xref, ext, typ, name, *_ in page.get_fonts():
            base = name.split("+")[-1]
            try:
                _, fext, _, buf = doc.extract_font(xref)
                tt = TTFont(io.BytesIO(buf), lazy=False)
                self.by_name.setdefault(base, []).append({"tt": tt, "gs": tt.getGlyphSet(), "order": tt.getGlyphOrder(), "upm": tt["head"].unitsPerEm,
                                                         "hmtx": tt["hmtx"].metrics if "hmtx" in tt else {}, "type0": typ == "Type0"})
            except Exception as e:
                print("font not readable:", name, e)

    def glyph(self, font, gid, origin, size, adv_pt):
        """Outline one glyph as segments in page coordinates; None if no embedded font has it.
        Two subsets can share a name (a composite and a simple font): the one whose advance matches the drawn advance wins."""
        from fontTools.pens.recordingPen import DecomposingRecordingPen
        best = None
        for f in self.by_name.get(font, []):
            if gid >= len(f["order"]): continue
            gn = f["order"][gid]
            adv = f["hmtx"].get(gn, (f["upm"], 0))[0] / f["upm"] * size
            pen = DecomposingRecordingPen(f["gs"])
            try: f["gs"][gn].draw(pen)
            except Exception: continue
            if not pen.value: continue
            err = abs(adv - adv_pt) if adv_pt else 0
            if best is None or err < best[0]: best = (err, f, pen.value, adv)
        if best is None: return None
        _, f, ops, adv = best
        hs = (adv_pt / adv) if (adv_pt and adv and abs(adv_pt / adv - 1) > 0.03) else 1.0     # horizontally scaled text
        k = size / f["upm"]; ox, oy = origin
        def P(pt): return (ox + pt[0] * k * hs, oy - pt[1] * k)
        subs = []; segs = []; cur = start = None
        for op, args in ops:
            if op == "moveTo":
                if segs: subs.append((segs, True)); segs = []
                cur = start = P(args[0])
            elif op == "lineTo": q = P(args[0]); segs.append(("l", cur, q)); cur = q
            elif op == "curveTo":
                a, b, c = [P(v) for v in args]; segs.append(("c", cur, a, b, c)); cur = c
            elif op == "qCurveTo":
                pts = [P(a) for a in args if a is not None]
                if args[-1] is None:      # no on-curve point: closed quadratic spline
                    on = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2); cur = start = on; pts = pts + [on]
                for i in range(len(pts) - 1):
                    c1 = pts[i]
                    end = pts[-1] if i == len(pts) - 2 else ((c1[0] + pts[i + 1][0]) / 2, (c1[1] + pts[i + 1][1]) / 2)
                    b1 = (cur[0] + 2 / 3 * (c1[0] - cur[0]), cur[1] + 2 / 3 * (c1[1] - cur[1]))
                    b2 = (end[0] + 2 / 3 * (c1[0] - end[0]), end[1] + 2 / 3 * (c1[1] - end[1]))
                    segs.append(("c", cur, b1, b2, end)); cur = end
            elif op in ("closePath", "endPath"):
                if cur and start and cur != start: segs.append(("l", cur, start))
                cur = start
        if segs: subs.append((segs, True))
        return subs

# ---------------------------------------------------------------- page model

def extents(subs):
    xs = []; ys = []
    for segs, _ in subs:
        for p in flat(segs): xs.append(p[0]); ys.append(p[1])
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None

def is_sheet_furniture(dr):
    """Section header bars (a flat coloured bar 16 pt high), horizontal cell rules and vertical cell dividers."""
    r = dr["rect"]
    if dr["type"] == "s" and len(dr["items"]) == 1 and dr["items"][0][0] == "l" and is_dark(dr.get("color")) and (r.width > 100 or r.height > 60) and min(r.width, r.height) < 0.01: return True
    if dr["type"] == "f" and r.width > 100 and 15.5 < r.height < 17 and len(dr["items"]) == 1 and dr["items"][0][0] == "re": return True
    return False

def load(doc, page):
    """All painted things on the page in paint order: {'kind','seq','bbox','paint':[(fill, evenodd, subs)], ...}."""
    fonts = Fonts(doc, page); things = []; labels = []; W = page.rect.width
    for dr in page.get_drawings():
        r = dr["rect"]; t = dr["type"]
        if t not in ("f", "s", "fs"): continue
        if is_sheet_furniture(dr): continue                                 # section header bars, cell rules and dividers
        paint = []
        if "f" in t and dr.get("fill") is not None:
            paint.append((dr["fill"], bool(dr.get("even_odd")), subpaths(dr["items"])))
        if "s" in t and dr.get("color") is not None:
            geom = stroke_outline(dr)
            if geom is not None and not geom.is_empty: paint.append((dr["color"], False, poly_subs(geom)))
        paint = [p for p in paint if p[2]]
        if not paint: continue
        bbs = [extents(p[2]) for p in paint]
        bb = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
        things.append({"kind": "path", "seq": dr["seqno"], "bbox": bb, "paint": paint, "stroke_only": t == "s", "width": dr.get("width") or 0,
                       "colour": dr.get("color") if t == "s" else dr.get("fill")})
    for sp in page.get_texttrace():
        txt = "".join(chr(c[0]) for c in sp["chars"])
        if not txt.strip(): continue
        col = tuple(sp["color"]) if len(sp["color"]) == 3 else (sp["color"][0],) * 3
        if sp["font"] == LABEL_FONT and sp["size"] <= LABEL_MAX and is_dark(col):
            for uc, gid, origin, cb in sp["chars"]:
                if chr(uc).strip(): labels.append({"c": chr(uc), "x": origin[0], "y": origin[1], "x1": cb[2], "top": cb[1]})
            continue
        if sp["size"] >= 11.5 and sp["font"] in ("HGGothicE", "HGPSoeiKakugothicUB"): continue      # section headers, sheet title
        paint = []; missing = []
        chars = sp["chars"]
        for i, (uc, gid, origin, cb) in enumerate(chars):
            if not chr(uc).strip(): continue
            adv = cb[2] - cb[0]
            subs = fonts.glyph(sp["font"], gid, origin, sp["size"], adv)
            if subs is None: missing.append(chr(uc)); continue
            if sp["type"] == 1:      # stroked text: outline of the stroke along each contour
                lw = sp.get("linewidth") or 0
                rings = [LinearRing(flat(segs)).buffer(lw / 2, join_style="mitre", mitre_limit=10) for segs, _ in subs if len(flat(segs)) > 3 and lw > 0]
                subs = poly_subs(unary_union(rings)) if rings else []
                if not subs: continue
            paint.append((col, False, subs))
        bb = sp["bbox"]
        if paint:
            bbs = [extents(p[2]) for p in paint]
            bb = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
        things.append({"kind": "text", "seq": sp["seqno"], "bbox": bb, "paint": paint, "text": txt, "font": sp["font"], "size": sp["size"],
                       "missing": missing, "stroked": sp["type"] == 1, "colour": col})
    things.sort(key=lambda t: t["seq"])
    # a white fill that nothing else is drawn on is invisible on the sheet (a leftover blank box): drop it
    def lone_white(t):
        if t["kind"] != "path" or t["stroke_only"] or len(t["paint"]) != 1 or min(t["colour"][:3]) < 0.99: return False
        a = t["bbox"]
        for o in things:
            if o is t: continue
            b = o["bbox"]
            if min(a[2], b[2]) - max(a[0], b[0]) > 1.0 and min(a[3], b[3]) - max(a[1], b[1]) > 1.0: return False
        return True
    things = [t for t in things if not lone_white(t)]
    return things, labels

def cluster(things):
    """Group things whose boxes touch (within JOIN) into faces."""
    n = len(things); parent = list(range(n))
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    order = sorted(range(n), key=lambda i: things[i]["bbox"][0])
    for ii, i in enumerate(order):
        a = things[i]["bbox"]
        for j in order[ii + 1:]:
            b = things[j]["bbox"]
            if b[0] > a[2] + JOIN: break
            if b[1] <= a[3] + JOIN and a[1] <= b[3] + JOIN: parent[find(i)] = find(j)
    groups = {}
    for i in range(n): groups.setdefault(find(i), []).append(things[i])
    def aligned(a, b):      # stacked or side-by-side panels of one guide-sign assembly: a narrow gap and equal extents
        if a[3] > GUIDE_Y1 or b[3] > GUIDE_Y1: return False
        dx = max(a[0], b[0]) - min(a[2], b[2]); dy = max(a[1], b[1]) - min(a[3], b[3])
        if 0 < dy < PANEL_GAP and abs(a[0] - b[0]) < 1 and abs(a[2] - b[2]) < 1: return True
        if 0 < dx < PANEL_GAP and abs(a[1] - b[1]) < 1 and abs(a[3] - b[3]) < 1: return True
        return False
    def boxes():
        gs = {}
        for i in range(n): gs.setdefault(find(i), []).append(things[i])
        return {k: (min(t["bbox"][0] for t in g), min(t["bbox"][1] for t in g), max(t["bbox"][2] for t in g), max(t["bbox"][3] for t in g)) for k, g in gs.items()}
    bx = boxes(); keys = list(bx)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if aligned(bx[a], bx[b]): parent[find(a)] = find(b)
    groups = {}
    for i in range(n): groups.setdefault(find(i), []).append(things[i])
    faces = []
    for g in groups.values():
        bb = (min(t["bbox"][0] for t in g), min(t["bbox"][1] for t in g), max(t["bbox"][2] for t in g), max(t["bbox"][3] for t in g))
        faces.append({"things": sorted(g, key=lambda t: t["seq"]), "bbox": bb})
    return faces

def read_labels(chars, bands):
    """Label characters -> labels {'codes': [(code, title)], 'x0','y0','y1','band'}.
    The sheet sets labels as loose runs of characters, so they are rebuilt from character positions: characters on one
    baseline with no gap form a run; a run starting "(NNN" is a label; any other run continues the label above it."""
    chars = sorted(chars, key=lambda c: (c["y"], c["x"]))
    rows = []
    for c in chars:
        for r in rows:
            if abs(r[0]["y"] - c["y"]) < 0.6: r.append(c); break
        else: rows.append([c])
    runs = []
    for r in rows:
        r.sort(key=lambda c: c["x"]); cur = None
        for c in r:
            text_so_far = unicodedata.normalize("NFKC", "".join(k["c"] for k in cur["chars"])) if cur else ""
            new_code = c["c"] in "(（" and cur and not re.search(r"[形は]$", text_so_far) and len(text_so_far) > 4
            if cur is None or c["x"] - cur["x1"] > 1.3 or new_code:
                cur = {"chars": [], "x0": c["x"], "x1": c["x1"], "y": c["y"], "top": c["top"]}; runs.append(cur)
            cur["chars"].append(c); cur["x1"] = max(cur["x1"], c["x1"]); cur["top"] = min(cur["top"], c["top"])
    for r in runs: r["text"] = unicodedata.normalize("NFKC", "".join(c["c"] for c in r["chars"])).strip()
    runs = [r for r in runs if r["text"]]
    def band(x, y):
        best = None
        for (y0, y1, x0, x1) in bands:
            if x0 - 2 <= x <= x1 + 2 and y1 <= y + 0.5 and (best is None or y1 > best): best = y1
        return best
    labels = []; rest = []
    for r in sorted(runs, key=lambda r: (r["y"], r["x0"])):
        if re.match(r"\(\d{3}", r["text"]) or r["text"].startswith("<"):
            labels.append({"lines": [r], "x0": r["x0"], "x1": r["x1"], "y0": r["top"], "y1": r["y"], "ay": r["y"], "ax1": r["x1"], "band": band(r["x0"] + 1, r["top"])})
        else: rest.append(r)
    split = []
    for r in rest:      # a second line can run into the neighbouring cell's second line: cut it where a label above starts
        b = band(r["x0"] + 1, r["top"])
        cuts = sorted(lb["x0"] for lb in labels if lb["band"] == b and r["x0"] + 3 < lb["x0"] < r["x1"] and 0 < r["y"] - lb["y1"] < 7.5)
        parts = [[]]
        for c in r["chars"]:
            if cuts and c["x"] >= cuts[0] - 0.5: cuts.pop(0); parts.append([])
            parts[-1].append(c)
        for cs in parts:
            if cs: split.append({"chars": cs, "x0": cs[0]["x"], "x1": cs[-1]["x1"], "y": r["y"], "top": r["top"], "text": unicodedata.normalize("NFKC", "".join(c["c"] for c in cs)).strip()})
    stray = []
    for r in sorted(split, key=lambda r: (r["y"], r["x0"])):      # continuation lines, top to bottom
        b = band(r["x0"] + 1, r["top"])
        cands = [lb for lb in labels if lb["band"] == b and lb["x0"] - 1.5 <= r["x0"] and 0 <= r["y"] - lb["y1"] < 7.5]
        same = [lb for lb in labels if lb["band"] == b and abs(lb["ay"] - r["y"]) < 0.6 and 0 <= r["x0"] - lb["ax1"] < 6]
        if same: lb = max(same, key=lambda lb: lb["x0"]); lb["ax1"] = r["x1"]
        elif cands: lb = max(cands, key=lambda lb: (lb["x0"], lb["y1"]))
        else: stray.append(r); continue
        lb["lines"].append(r); lb["y1"] = max(lb["y1"], r["y"]); lb["x1"] = max(lb["x1"], r["x1"])
    for lb in labels:
        text = "".join(r["text"] for r in sorted(lb["lines"], key=lambda r: (round(r["y"]), r["x0"]))); lb["text"] = text
        ms = list(CODE_RE.finditer(text)); lb["codes"] = []
        for i, m in enumerate(ms):
            if i and m.start() > ms[i - 1].end() and not re.match(r"\(\d{3}", text[m.start():]): continue
            title = text[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(text)].strip()
            code = "-".join(g for g in m.groups() if g)
            lb["codes"].append((code, title))
    return labels, stray

def rules(page):
    """y of the horizontal cell rules and header bars (bands between them are rows of cells), with their x range."""
    out = []
    for dr in page.get_drawings():
        r = dr["rect"]
        if is_sheet_furniture(dr) and r.width > 100: out.append((r.y0, r.y1, r.x0, r.x1))
    return out

def dividers(page):
    """Vertical cell dividers of the guide-sign rows: (x, y0, y1)."""
    out = []
    for dr in page.get_drawings():
        r = dr["rect"]
        if is_sheet_furniture(dr) and r.height > 60: out.append((r.x0, r.y0, r.y1))
    return out

def assign(faces, labels, bands, divs):
    """Each face goes to the label above it in its cell: same band, label starts left of the face's centre, nearest column, nearest above."""
    def band(x, y):
        best = None
        for (y0, y1, x0, x1) in bands:
            if x0 - 2 <= x <= x1 + 2 and y1 <= y + 0.5 and (best is None or y1 > best): best = y1
        return best
    def cell(x, y): return sum(1 for (dx, y0, y1) in divs if y0 - 1 <= y <= y1 + 1 and dx < x)
    for lb in labels: lb["faces"] = []; lb["cell"] = cell(lb["x0"] + 1, lb["y0"])
    loose = []
    for f in faces:
        bb = f["bbox"]; cx = (bb[0] + bb[2]) / 2; b = band(cx, bb[1])
        incell = [lb for lb in labels if lb["band"] == b and lb["cell"] == cell(cx, bb[1]) and lb["y0"] < bb[1] + 2]
        cands = [lb for lb in incell if lb["x0"] - 3 <= cx]
        if not cands:      # a label centred over a group of panels starts right of the first panel: the cell's first label
            if not incell: loose.append(f); continue
            cands = [min(incell, key=lambda lb: lb["x0"])]
        mx = max(lb["x0"] for lb in cands)
        col = [lb for lb in cands if lb["x0"] > mx - 12]
        lb = max(col, key=lambda lb: lb["y0"]); lb["faces"].append(f); f["label"] = lb
    return loose

# ---------------------------------------------------------------- output

def face_svg(face, mm_per_pt):
    bb = face["bbox"]; k = mm_per_pt
    W, H = (bb[2] - bb[0]) * k, (bb[3] - bb[1]) * k
    def T(p): return ((p[0] - bb[0]) * k, (p[1] - bb[1]) * k)
    body = []
    for t in face["things"]:
        if t["kind"] == "text":
            d = "".join(subs_d(p[2], T) for p in t["paint"])
            if d: body.append(f'<path fill="{hexcol(t["colour"])}" d="{d}"/>')
            continue
        for fill, eo, subs in t["paint"]:
            body.append(f'<path fill="{hexcol(fill)}"{" fill-rule=\"evenodd\"" if eo else ""} d="{subs_d(subs, T, closed_all=True)}"/>')
    OW, OH = W * 0.1, H * 0.1
    svg = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{fmt(OW * 25.4 / 72)}mm" height="{fmt(OH * 25.4 / 72)}mm" viewBox="0 0 {fmt(OW)} {fmt(OH)}">',
           '<g transform="scale(0.1)">'] + ["  " + b for b in body] + ["</g>", "</svg>"]
    return "\n".join(svg) + "\n", W, H

def diamond_side(face):
    """Side of a point-up square face on the sheet (pt): extent of the outline along the edge normal."""
    v = []
    for t in face["things"]:
        for _, _, subs in t["paint"]:
            for segs, _ in subs:
                for p in flat(segs): v.append((p[0] + p[1]) / math.sqrt(2))
    return max(v) - min(v)

def size_for(code, family, face, n_faces, idx):
    """(mm per sheet point, note). SIZES[code] = (dimension, cm, clause) with dimension in 'w' (width), 'h' (height), 'side' (point-up square)."""
    bb = face["bbox"]; w = bb[2] - bb[0]; h = bb[3] - bb[1]
    key = f"{code}#{idx}" if f"{code}#{idx}" in SIZES else code
    spec = SIZES[key] if key in SIZES else CLASS_SIZE.get(family)
    if spec is None: return NOMINAL, f"no size given for this face in the sign order; artwork kept at 1 pt = {fmt(NOMINAL)} mm (proportions as on the sheet, size nominal)"
    dim, cm, clause = spec
    if dim == "tri":      # triangle side between the sharp corners; the corners are rounded R = 5 cm, which shortens the outline by 2 x 3.66 cm
        return (cm - 2 * 5 * (math.sqrt(3) - 1)) * 10 / w, f"side {fmt(cm * 10)} mm between sharp corners, outline {fmt((cm - 2 * 5 * (math.sqrt(3) - 1)) * 10)} mm wide after the R 50 mm corners ({clause}); proportions as on the sheet"
    ref = {"w": w, "h": h, "side": diamond_side(face) if dim == "side" else None}[dim]
    what = {"w": "width", "h": "height", "side": "side"}[dim]
    return cm * 10 / ref, f"{what} {fmt(cm * 10)} mm ({clause}); proportions as on the sheet"

def ascii_name(s): return re.sub(r"_+", "_", re.sub(r"[^A-Z0-9]+", "_", s.upper())).strip("_")

def main(debug=None):
    doc = pymupdf.open(PDF); page = doc[0]
    things, spans = load(doc, page)
    faces = cluster(things)
    bands = rules(page)
    labels, stray = read_labels(spans, bands)
    loose = assign(faces, labels, bands, dividers(page))
    # consecutive labels sharing one face: a label without faces joins the label directly above (or below) it in its column
    coded = [lb for lb in labels if lb["codes"] or lb["text"].startswith("<")]
    for lb in coded:
        if lb["faces"] or not lb["codes"]: continue
        near = [o for o in coded if o is not lb and o["band"] == lb["band"] and abs(o["x0"] - lb["x0"]) < 12 and o["faces"] and abs(o["y0"] - lb["y0"]) < 12]
        if near:
            o = min(near, key=lambda o: abs(o["y0"] - lb["y0"])); lb["merged"] = True
            o["codes"] = (lb["codes"] + o["codes"]) if lb["y0"] < o["y0"] else (o["codes"] + lb["codes"])
    if debug:
        os.makedirs(debug, exist_ok=True)
        sh = page.new_shape()
        for f in faces:
            sh.draw_rect(pymupdf.Rect(f["bbox"])); sh.finish(color=(1, 0, 1) if "label" in f else (1, 0, 0), width=0.3)
            if "label" in f:
                lb = f["label"]; sh.draw_line((lb["x0"], lb["y1"]), (f["bbox"][0], f["bbox"][1])); sh.finish(color=(0, 0.7, 0), width=0.3)
        for lb in labels:
            sh.draw_rect(pymupdf.Rect(lb["x0"], lb["y0"], lb["x1"], lb["y1"])); sh.finish(color=(0, 0.6, 0) if lb["codes"] else (1, 0.5, 0), width=0.2)
        sh.commit(); page.get_pixmap(dpi=200).save(os.path.join(debug, "overlay.png"))
        doc = pymupdf.open(PDF); page = doc[0]
        with open(os.path.join(debug, "labels.txt"), "w") as fh:
            for lb in labels:
                fh.write(f'{lb["x0"]:7.1f} {lb["y0"]:7.1f} band={lb["band"]} faces={len(lb["faces"])} {"MERGED " if lb.get("merged") else ""}{lb["codes"]} | {lb["text"]}\n')
            for r in stray: fh.write(f'STRAY RUN {r["x0"]:.1f} {r["y"]:.1f} {r["text"]}\n')
            for f in loose: fh.write(f'LOOSE {tuple(round(v, 1) for v in f["bbox"])} {[t.get("text", t["kind"]) for t in f["things"]][:6]}\n')
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    rows = []; counts = {}; interv = []
    for lb in sorted(coded, key=lambda lb: (lb["codes"][0][0] if lb["codes"] else "999", lb["y0"], lb["x0"])):
        if lb.get("merged") or not lb["codes"]: continue
        code0, title0 = lb["codes"][0]
        family = FAMILIES[code0[0]]
        fs = sorted(lb["faces"], key=lambda f: (round(f["bbox"][1] / 6), f["bbox"][0]))
        fs = [f for i, f in enumerate(fs) if f"{code0}#{i + 1}" not in SKIP]
        codes = "; ".join(c for c, _ in lb["codes"]); name_ja = "; ".join(t for _, t in lb["codes"] if t)
        name_en = NAMES.get(code0)
        if not name_en: print("no English name:", code0, name_ja); name_en = "SIGN"
        if not fs: print("label without a face:", codes, name_ja); continue
        for i, f in enumerate(fs, 1):
            suffix = f"_{i}" if len(fs) > 1 else ""
            k, note = size_for(code0, family, f, len(fs), i)
            svg, W, H = face_svg(f, k)
            missing = sorted({f'{t["font"]} "{c}"' for t in f["things"] if t["kind"] == "text" for c in t["missing"]})
            stroked = [t["text"] for t in f["things"] if t["kind"] == "text" and t["stroked"]]
            notes = [note]
            if len(lb["codes"]) > 1: notes.append("one face on the sheet for codes " + codes)
            if len(fs) > 1: notes.append(f"example panel {i} of {len(fs)} under this label")
            legend = "".join(t["text"] for t in f["things"] if t["kind"] == "text").strip()
            if legend: notes.append("live text outlined from the sheet's embedded fonts")
            folder = family
            if missing: folder = "intervene"; notes.insert(0, "INTERVENE: glyphs not outlined: " + ", ".join(missing)); interv.append(code0 + suffix)
            fn = f"{ascii_name(name_en)}_{code0}{suffix}.svg"
            os.makedirs(os.path.join(OUT, folder), exist_ok=True)
            with open(os.path.join(OUT, folder, fn), "w") as fh: fh.write(svg)
            rows.append([codes + (f" ({i})" if suffix else ""), name_ja, name_en, family, (folder + "/" if folder == "intervene" else "") + fn, f"{round(W)}x{round(H)} mm", "; ".join(notes)])
            counts[folder] = counts.get(folder, 0) + 1
            f["file"] = os.path.join(OUT, folder, fn)
    with open(os.path.join(OUT, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name_ja", "name_en", "family", "file", "size", "notes"]); w.writerows(rows)
    print(len(rows), "SVGs;", counts, "; loose faces:", len(loose), "; intervene:", interv)
    return faces, labels, loose

if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--debug") + 1] if "--debug" in sys.argv else None)
