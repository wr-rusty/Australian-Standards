#!/usr/bin/env python3
"""wa_extract.py — Main Roads WA Signs Index DWGs into Australia/WA/SVGs/<Category>/<NAME>_<CODE>.svg with MANIFEST.csv.

The DWG is converted with LibreDWG (dwg2dxf), loaded with ezdxf's recovery reader, stripped of its sheet furniture
(title block, logos, dimensions, notes, scale bars, text) and rendered true-size (1 drawing unit = 1 mm) to SVG with
ezdxf's drawing add-on, Inkscape turns that into a PDF, and the sheet extractor picks the sign drawings out of it. Closed
polylines on the letters layers (L25, L35 ...) that carry no hatch are filled solid, as the sign maker would.
  python3 tools/wa_extract.py [limit]      (WA_FILES=comma,separated,stems to run named drawings)"""
import os, re, sys, csv, glob, subprocess, collections, hashlib, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf, ezdxf
from ezdxf import recover, bbox
from ezdxf.addons.drawing import Frontend, RenderContext, svg, layout, config
import sheet_extract as SE, shs_extract as X
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = os.path.join(ROOT, "Australia", "WA")
CACHE = os.environ.get("WA_CACHE", os.path.join(os.path.dirname(SE.CACHE), ".wa_cache") if os.environ.get("SHEET_CACHE") else os.path.join(ROOT, ".wa_cache"))
INK = SE.INK
FURNITURE_BLOCKS = re.compile(r"^(A3BBLK|MR logo|State Logo|a3_in_vtblk|sca\d|.*DES$|SGNDIM|.*TITLE.*|.*LOGO.*|.*BORDER.*|.*NOTES?.*)$", re.I)
FURNITURE_LAYERS = re.compile(r"^(TBLK.*|DIMMARKS|COMMENTS|DEFPOINTS|DIM|T\d+|NOTES?|TEXT.*|TITLE.*|SCALE.*|VIEWPORT.*|HIDDEN.*)$", re.I)
DROP_TYPES = {"DIMENSION", "TEXT", "MTEXT", "ATTDEF", "ATTRIB", "POINT", "LEADER", "MLEADER", "VIEWPORT", "TOLERANCE", "IMAGE", "WIPEOUT"}

class Identity:
    """No page turning: the rendered drawing is already upright."""
    def __init__(self, page, spans_raw): self.M = pymupdf.Matrix(1, 0, 0, 1, 0, 0); self.rect = page.rect; self.turned = 0
    @classmethod
    def baked(cls, page, like): return cls(page, [])
    def P(self, p): return (p[0], p[1])
    def R(self, r): return pymupdf.Rect(r)
SE.Frame = Identity
SE.drawing_region = lambda F, spans: pymupdf.Rect(F.rect)      # no title block left after stripping: the whole page is drawing
COLOUR_WORDS = re.compile(r"FLUORESCENT\s+YELLOW[\s-]*GREEN|WHITE|BLACK|GREEN|BLUE|RED|BROWN|YELLOW|ORANGE|GREY|GRAY", re.I)
PALETTE = {"WHITE": "#ffffff", "BLACK": "#231f20", "YELLOW": "#ffe40d", "RED": "#ed1c24", "GREEN": "#00693c", "BLUE": "#0055a4", "BROWN": "#6f3f22", "ORANGE": "#f7921d", "FLUORESCENT YELLOW-GREEN": "#c4d600", "GREY": "#8a8d8f", "GRAY": "#8a8d8f"}

def hex2rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))

def legend_text(doc):
    r"""Text entities that look like sign legend (on letters layers L\d+ or GS* / colour layers, not notes or dimensions)."""
    out = []
    for space in [doc.modelspace()] + [b for b in doc.blocks if not b.name.startswith("*")]:
        for e in space:
            t = e.dxftype()
            if t not in ("TEXT", "MTEXT"): continue
            lay = (e.dxf.layer or "").upper(); txt = (e.dxf.text if t == "TEXT" else e.plain_text()).strip()
            if not txt or FURNITURE_LAYERS.match(lay) or re.match(r"^(panel|legend|sign|text|levels|version|width|height|margin|construct|chevron)", txt, re.I): continue
            if re.match(r"^L\d+$|^GS|^(RED|YELLOW|GREEN|BLUE|BROWN|WHITE|BLACK)", lay):
                if re.fullmatch(r"[\d.:x ]+|MR-.*|MMS-.*|\d+-\d+|\d+\s*mm|%%.*|\d+\..*|&.*|.*#.*|[A-Z]+TYPES|[A-Z]+LAYER|[A-Z]+STYLES", txt, re.I): continue
                out.append(txt[:30])
    return out

def sheet_text(doc):
    out = []
    for space in [doc.modelspace()] + [b for b in doc.blocks]:
        for e in space:
            t = e.dxftype()
            if t == "TEXT": out.append(e.dxf.text)
            elif t == "MTEXT": out.append(e.plain_text())
            elif t == "ATTDEF": out.append(getattr(e.dxf, "text", "") or "")
    return out

def sheet_scale(texts):
    """'1:N' on the sheet (scale bar / title block); the largest N wins (small ones label details)."""
    ns = [int(m.group(1)) for t in texts for m in re.finditer(r"\b1\s*:\s*(\d{1,3})\b", t)]
    ns = [n for n in ns if 1 <= n <= 100]
    return max(ns) if ns else None

def colour_note(texts):
    """{'legend': COLOUR, 'border': COLOUR, 'background': COLOUR} from a 'COLOURS: BLACK LEGEND & BORDER ON WHITE ... BACKGROUND' note."""
    for t in texts:
        u = re.sub(r"\s+", " ", t.upper())
        if "COLOUR" not in u and "COLOR" not in u: continue
        u = u.split("COLOUR", 1)[-1].split("COLOR", 1)[-1].lstrip("S:. ")
        out = {}
        parts = re.split(r"\bON\b", u, maxsplit=1)
        left = parts[0]; right = parts[1] if len(parts) > 1 else ""
        lc = [m.group(0).upper() for m in COLOUR_WORDS.finditer(left)]; rc = [m.group(0).upper() for m in COLOUR_WORDS.finditer(right)]
        if lc:
            if "LEGEND" in left or "SYMBOL" in left or not right: out["legend"] = lc[0]
            if "BORDER" in left: out["border"] = lc[-1] if "BORDER" in left.split(lc[0], 1)[-1] and len(lc) > 1 else lc[0]
        if rc: out["background"] = rc[0]
        if "BACKGROUND" in left and not rc: out["background"] = lc[-1]
        if out: return out
    return {}

def repair_dxf(path):
    """LibreDWG's DXF: INSERTs flagged 'attributes follow' (66/1) without ATTRIBs, and POLYLINEs whose VERTEX run ends
    without a SEQEND — clear the flag / insert the SEQEND so ezdxf's entity linker accepts the file. DXF is strict
    code/value line pairs, so walk it in pairs."""
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    pairs = [(lines[k].strip(), lines[k + 1]) for k in range(0, len(lines) - 1, 2)]
    out = []; fixed = 0; open_poly = False; entity = ""
    for idx, (code, val) in enumerate(pairs):
        v = val.strip()
        if code == "0":
            if open_poly and v not in ("VERTEX", "SEQEND"): out += [("0", "SEQEND"), ("8", "0")]; fixed += 1; open_poly = False
            if v == "POLYLINE": open_poly = True
            elif v == "SEQEND": open_poly = False
            entity = v
        if code == "66" and v == "1" and entity == "INSERT":
            nxt = next((pv.strip() for pc, pv in pairs[idx + 1:] if pc == "0"), "")
            if nxt != "ATTRIB": out.append(("66", "     0")); fixed += 1; continue
        out.append((code, val))
    if fixed:
        open(path, "w", encoding="utf-8").write("\n".join(f"{c:>3}\n{v}" if c.isdigit() and len(c) <= 3 else f"{c}\n{v}" for c, v in out) + "\n")
    return fixed

def dxf_of(dwg):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(os.path.abspath(dwg).encode()).hexdigest()[:8]
    out = os.path.join(CACHE, f"{os.path.splitext(os.path.basename(dwg))[0]}_{key}.dxf")
    if not os.path.exists(out):
        subprocess.run(["dwg2dxf", "-o", out, dwg], capture_output=True, timeout=600)
        if not os.path.exists(out): raise RuntimeError("dwg2dxf produced nothing")
        repair_dxf(out)
    return out

def supplement_blocks(doc, dwg):
    """LibreDWG's DXF writer drops the contents of some anonymous blocks (GuideSIGN glyphs). Its JSON reader keeps
    them: refill every empty *U block from the JSON entities owned by the same block-record handle."""
    import json
    jpath = dxf_of(dwg)[:-4] + ".dwg.json"
    if not os.path.exists(jpath):
        r = subprocess.run(["dwgread", "-O", "json", dwg], capture_output=True, text=True, timeout=600)
        if not r.stdout.strip(): return 0
        open(jpath, "w").write(r.stdout)
    try: objs = json.load(open(jpath)).get("OBJECTS", [])
    except Exception: return 0
    layers = {o["handle"][-1]: o.get("name", "0") for o in objs if o.get("object") == "LAYER" and o.get("handle")}
    by_owner = {}
    for o in objs:
        if "entity" in o and o.get("ownerhandle"): by_owner.setdefault(o["ownerhandle"][-1], []).append(o)
    added = 0
    for b in doc.blocks:
        if not b.name.startswith("*U") or len(list(b)) or not b.block_record.dxf.hasattr("handle"): continue
        ents = by_owner.get(int(b.block_record.dxf.handle, 16), [])
        for o in ents:
            lay = layers.get((o.get("layer") or [None])[-1], "0"); col = (o.get("color") or {}).get("index", 256)
            attribs = {"layer": lay, "color": col if isinstance(col, int) else 256}
            try:
                if o["entity"] == "LWPOLYLINE":
                    pts = o.get("points") or []; bul = o.get("bulges") or []
                    if len(pts) >= 2:
                        b.add_lwpolyline([(x, y, (bul[i] if i < len(bul) else 0.0)) for i, (x, y) in enumerate(pts)], format="xyb", close=bool((o.get("flag") or 0) & 512), dxfattribs=attribs); added += 1
                elif o["entity"] == "HATCH":
                    h = b.add_hatch(color=attribs["color"], dxfattribs={"layer": lay}); n = 0
                    for ph in o.get("paths") or []:
                        if ph.get("polyline_paths"):
                            pts = [(q["point"][0], q["point"][1], q.get("bulge", 0.0)) for q in ph["polyline_paths"]]
                            if len(pts) >= 2: h.paths.add_polyline_path(pts, is_closed=True, flags=ph.get("flag", 1)); n += 1
                        elif ph.get("segs"):
                            ep = h.paths.add_edge_path(flags=ph.get("flag", 1))
                            for sg in ph["segs"]:
                                t = sg.get("curve_type")
                                if t == 1: ep.add_line(tuple((sg.get("first_endpoint") or sg["start"])[:2]), tuple((sg.get("second_endpoint") or sg["end"])[:2]))
                                elif t == 2: ep.add_arc(tuple(sg["center"][:2]), sg["radius"], math.degrees(sg["start_angle"]), math.degrees(sg["end_angle"]), ccw=bool(sg.get("is_ccw", 1)))
                                elif t == 3: ep.add_ellipse(tuple(sg["center"][:2]), tuple(sg["endpoint"][:2]) if "endpoint" in sg else (sg.get("radius", 1), 0), sg.get("minor_major_ratio", sg.get("ratio", 1)), math.degrees(sg.get("start_angle", 0)), math.degrees(sg.get("end_angle", 6.283185)), ccw=bool(sg.get("is_ccw", 1)))
                                elif t == 4:
                                    cps = [tuple(c[:2]) for c in (sg.get("control_points") or sg.get("fit_points") or [])]
                                    for a, c in zip(cps, cps[1:]): ep.add_line(a, c)
                            n += 1
                    if n: added += 1
                    else: b.delete_entity(h)
            except Exception: pass
    return added

def strip_furniture(doc):
    """Remove sheet furniture and text; fill hatch-less closed polylines on letters layers. Returns notes."""
    notes = []
    named = {}
    for l in doc.layers:
        m = re.match(r"(RED|YELLOW|GREEN|BLUE|BROWN|ORANGE|WHITE|BLACK)(?![A-Z])", l.dxf.name.upper())
        if m:
            named[l.dxf.name] = m.group(1); h = PALETTE[m.group(1)]
            try: l.rgb = (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))   # so BYLAYER entities and nested block contents inherit the exact palette colour
            except Exception: pass
    def purge(space):
        for e in list(space):
            t = e.dxftype()
            if t == "INSERT":
                if FURNITURE_BLOCKS.match(e.dxf.name or ""): space.delete_entity(e)
                continue
            if t in DROP_TYPES or FURNITURE_LAYERS.match(e.dxf.layer or ""):
                space.delete_entity(e); continue
            if e.dxf.layer in named:   # a layer named after a colour states the sign colour: give it the palette RGB exactly
                h = PALETTE[named[e.dxf.layer]]; e.rgb = (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
            if t == "HATCH":            # curved hatch edges (arcs, splines) sometimes fail to render: flatten them
                try: e.paths.all_to_polyline_paths(num=48)
                except Exception: pass
    purge(doc.modelspace())
    for b in doc.blocks:
        if b.name.startswith("*"): continue
        purge(b)
    # letters drawn as closed outlines without a fill (small closed polylines; nested ones become the counters)
    ext_all = bbox.extents(doc.modelspace(), fast=True); limit = 0.15 * ext_all.size.x * ext_all.size.y if ext_all.has_data else 1e9
    for space in [doc.modelspace()] + [b for b in doc.blocks if not b.name.startswith("*")]:
        hatch_boxes = []
        for e in space:
            if e.dxftype() == "HATCH":
                try:
                    ext = bbox.extents([e], fast=True)
                    if ext.has_data: hatch_boxes.append(ext)
                except Exception: pass
        cands = []
        for e in list(space):
            if e.dxftype() not in ("LWPOLYLINE", "POLYLINE"): continue
            closed = e.closed if e.dxftype() == "LWPOLYLINE" else e.is_closed
            if not closed: continue
            try: ext = bbox.extents([e], fast=True)
            except Exception: continue
            if not ext.has_data or ext.size.x * ext.size.y > limit: continue
            if any(abs(hb.extmin.x - ext.extmin.x) < 0.5 and abs(hb.extmin.y - ext.extmin.y) < 0.5 and abs(hb.size.x - ext.size.x) < 1 and abs(hb.size.y - ext.size.y) < 1 for hb in hatch_boxes): continue
            pts = [(p[0], p[1]) for p in (e.get_points("xy") if e.dxftype() == "LWPOLYLINE" else [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices])]
            if len(pts) >= 3: cands.append((ext, pts, e.dxf.layer))
        cands.sort(key=lambda c: -(c[0].size.x * c[0].size.y)); used = [False] * len(cands); added = 0
        for i, (ext, pts, layer) in enumerate(cands):
            if used[i]: continue
            paths = [pts]; used[i] = True
            for j in range(i + 1, len(cands)):
                if not used[j] and ext.inside(cands[j][0].extmin) and ext.inside(cands[j][0].extmax): paths.append(cands[j][1]); used[j] = True
            h = space.add_hatch(color=7, dxfattribs={"layer": layer})
            for k, pp in enumerate(paths): h.paths.add_polyline_path(pp, is_closed=True, flags=1 if k == 0 else 0)
            for pp in paths: pass
            added += 1
        if added: notes.append(f"{added} closed letter outline(s) filled solid")
    return notes

def render_pdf(dwg):
    """PDF of the drawing without its sheet furniture, 1 drawing unit = 1 mm (cached); returns (pdf, info dict)."""
    import json
    dxf = dxf_of(dwg); pdf = dxf[:-4] + ".pdf"; meta = dxf[:-4] + ".json"
    if os.path.exists(pdf) and os.path.exists(meta): return pdf, json.load(open(meta))
    doc, aud = recover.readfile(dxf); texts = sheet_text(doc); refilled = supplement_blocks(doc, dwg)
    guidesign = any(l.dxf.name.upper() == "GSCOLORFILL" for l in doc.layers)
    if guidesign:   # GuideSIGN export: the colour level is the truth; drop the black-and-white and outline levels
        for space in [doc.modelspace()] + [b for b in doc.blocks]:
            for e in list(space):
                if (e.dxf.layer or "").upper() in ("GSBWFILL", "GSOUTLINE") and e.dxftype() != "INSERT": space.delete_entity(e)
    info = {"scale": sheet_scale(texts), "colours": colour_note(texts), "legend_text": legend_text(doc), "notes": strip_furniture(doc) + ([f"{refilled} glyph block(s) refilled from the DWG (LibreDWG's DXF dropped them)"] if refilled else []), "guidesign": guidesign, "layers": {l.dxf.name: l.color for l in doc.layers}}
    msp = doc.modelspace(); ext = bbox.extents(msp, fast=True)
    if not ext.has_data: raise RuntimeError("nothing left to draw")
    w, h = max(ext.size.x, 1), max(ext.size.y, 1); info["extents"] = [ext.extmin.x, ext.extmin.y, w, h]
    ctx = RenderContext(doc); backend = svg.SVGBackend()
    cfg = config.Configuration(background_policy=config.BackgroundPolicy.WHITE, color_policy=config.ColorPolicy.COLOR, lineweight_policy=config.LineweightPolicy.ABSOLUTE, min_lineweight=0.1)
    Frontend(ctx, backend, config=cfg).draw_layout(msp)
    mg = 0.2 * max(w, h)
    page = layout.Page(w + 2 * mg, h + 2 * mg, layout.Units.mm, margins=layout.Margins.all(mg))
    s = backend.get_string(page, settings=layout.Settings(scale=1.0, fit_page=False))
    svgp = dxf[:-4] + ".svg"; open(svgp, "w").write(s)
    r = subprocess.run([INK, svgp, "--export-type=pdf", f"--export-filename={pdf}"], capture_output=True, text=True, timeout=300)
    if not os.path.exists(pdf): raise RuntimeError("inkscape could not convert the render: " + r.stderr.strip()[-150:])
    json.dump(info, open(meta, "w")); return pdf, info

LIGHT = {"WHITE", "YELLOW", "TEAL"}
SERIES_DEFAULT = [(r"^MR-W|^MR-T", ("BLACK", "YELLOW")), (r"^MR-G", ("WHITE", "GREEN")), (r"^MR-S", ("WHITE", "BLUE")), (r"^MR-V", ("WHITE", "BROWN")), (r"^MR-HM", ("RED", "WHITE"))]

DARK_BG = {"BLUE", "GREEN", "BROWN", "RED", "BLACK"}
def recolour_true(sign, code):
    """GuideSIGN colour level: every fill's rendered colour is a real sign colour (nearest palette name); the panel's
    colour is the background, black/white legend follows the background's tone."""
    fills = sign["fills"]; real = [f for f in fills if not f.get("virtual")]
    top = max(real, key=lambda f: f["area"]) if real else None
    bg = X.colour_name(top["fill"]) if top else "WHITE"
    if bg not in PALETTE: bg = "WHITE"
    legend = "WHITE" if bg in DARK_BG else "BLACK"
    for f in fills:
        n = X.colour_name(f["fill"])
        if f.get("virtual"): f["fill"] = hex2rgb(PALETTE[bg])
        elif n in PALETTE and n not in ("BLACK", "WHITE"): f["fill"] = hex2rgb(PALETTE[n])
        elif n == "WHITE": f["fill"] = hex2rgb(PALETTE["WHITE"])
        else: f["fill"] = hex2rgb(PALETTE[legend])
    sign["bg"] = bg
    return f"colours from the drawing's GuideSIGN colour level: background {bg}, legend {legend}"

def recolour(sign, colours, code):
    """Drafting colours mean nothing, so the stacking tells the design: the last panel-sized fill (one that holds the
    others) is the background, panel-sized fills under it are legend colour (they show through its holes), small fills
    are legend colour unless they sit inside an earlier small legend fill (counters, inner panels: background/white).
    Fills on colour-named layers arrive as exact palette RGB and keep it. Colours come from the sheet's COLOURS note,
    else the series default (flagged)."""
    legend = colours.get("legend"); bg = colours.get("background"); how = "colours from the sheet's note"
    if not legend or not bg:
        for pat, (l, b) in SERIES_DEFAULT:
            if re.match(pat, code, re.I): legend, bg = legend or l, bg or b; how = f"no colour note on the sheet: {code.split('-')[0]}-{code.split('-')[1][:2] if '-' in code else ''} series default assumed — check colours"; break
        else: legend, bg = legend or "BLACK", bg or "WHITE"; how = "no colour note on the sheet: black legend on white assumed — check colours"
    fills = sign["fills"]; real = [f for f in fills if not f.get("virtual")]
    exact = {tuple(round(v, 3) for v in hex2rgb(h)): n for n, h in PALETTE.items()}
    big = max((f["area"] for f in real), default=0)
    def holds(f):
        others = [g for g in real if g is not f]
        return not others or sum(1 for g in others if f["rect"].contains(pymupdf.Point((g["rect"].x0 + g["rect"].x1) / 2, (g["rect"].y0 + g["rect"].y1) / 2))) >= 0.6 * len(others)
    def painted(g, pt):
        """Is the point inside the fill's painted area (even-odd over its subpaths)?"""
        n = 0
        for part in SE.subpaths(g["items"]):
            pts = X.item_points(part); k = len(pts); inside = False
            for a in range(k):
                x1, y1 = pts[a]; x2, y2 = pts[(a + 1) % k]
                if (y1 > pt[1]) != (y2 > pt[1]) and pt[0] < (x2 - x1) * (pt[1] - y1) / ((y2 - y1) or 1e-9) + x1: inside = not inside
            n += inside
        return n % 2 == 1
    def painted_fraction(f):
        """Even-odd painted area over the bbox area: a ring or a border-with-letters hatch is mostly empty."""
        from shapely.geometry import Polygon
        polys = []
        for part in SE.subpaths(f["items"]):
            pts = X.item_points(part)
            if len(pts) >= 3:
                try:
                    pg = Polygon(pts).buffer(0)
                    if pg.area > 0: polys.append(pg)
                except Exception: pass
        if not polys: return 1.0
        area = 0.0
        for pg in polys:
            depth = sum(1 for q in polys if q is not pg and q.area > pg.area and q.contains(pg.representative_point()))
            area += pg.area if depth % 2 == 0 else -pg.area
        return max(0.0, area) / max(f["area"], 1e-9)
    panels = [f for f in real if f["area"] >= 0.8 * big and holds(f) and painted_fraction(f) >= 0.6]
    top = panels[-1] if panels else None
    role = {}
    for f in real:
        key = tuple(round(v, 3) for v in f["fill"][:3])
        if key in exact: role[id(f)] = exact[key]; continue                       # colour-named layer: stated colour
        if f is top: role[id(f)] = bg
        elif f in panels: role[id(f)] = legend
        else:
            c = ((f["rect"].x0 + f["rect"].x1) / 2, (f["rect"].y0 + f["rect"].y1) / 2)
            inside = [g for g in real if g is not f and g not in panels and role.get(id(g)) == legend and g["rect"].contains(f["rect"]) and g["area"] > 1.05 * f["area"] and painted(g, c)]
            role[id(f)] = ("WHITE" if bg != "WHITE" else bg) if inside else legend
    for f in fills:
        if f.get("virtual"): f["fill"] = hex2rgb(PALETTE[bg])
        else: f["fill"] = hex2rgb(PALETTE[role[id(f)]])
    sign["bg"] = bg
    return f"{how}: legend {legend}, background {bg}" + (f", border {colours['border']}" if colours.get("border") else "")

def main(limit=None):
    out = os.path.join(WA, "SVGs"); rows = []; seen = {}
    reg0 = [r for r in csv.DictReader(open(os.path.join(WA, "REGISTER.csv"))) if any(p.lower().endswith(".dwg") for p in r["local"].split(" | "))]
    by_dwg = {}
    for r in reg0:   # the index lists most signs twice (drawing-number row and MR-code row) with the same files: keep the MR-code row
        d = [p for p in r["local"].split(" | ") if p.lower().endswith(".dwg")][0]
        if d not in by_dwg or re.match(r"(MR|MMS)-", r["title"]): by_dwg[d] = r
    reg = list(by_dwg.values())
    only = os.environ.get("WA_FILES")
    if only: reg = [r for r in reg if any(os.path.splitext(os.path.basename(p))[0] in only.split(",") for p in r["local"].split(" | "))]
    if limit: reg = reg[:limit]
    for i, r in enumerate(reg):
        dwg = [p for p in r["local"].split(" | ") if p.lower().endswith(".dwg")][0]; src = dwg
        code = r["code"] or os.path.splitext(os.path.basename(dwg))[0].upper(); name = r["title"]
        fam = re.sub(r"[^\w\- ]+", "", r["category"] or r["series"]).strip() or "Other"
        try:
            pdf, info = render_pdf(os.path.join(WA, dwg)); signs = SE.extract_page(pdf, 0, min_area_frac=0.0005); pre = info["notes"]
        except Exception as ex:
            rows.append([code, name, fam, "", "", f"conversion failed: {str(ex)[:120]}", src]); print("  !!", code, str(ex)[:100], flush=True); continue
        if not signs:
            rows.append([code, name, fam, "", "", "no drawing found after removing the sheet furniture", src]); continue
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        nm = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")[:80] or "SIGN"; cd = code.replace(" ", "").replace("/", "-")
        m = re.match(r"(\d+)\s*x\s*(\d+)", (r["size"] or "").replace(" ", ""))
        rw = rh = None
        if m: rw, rh = float(m.group(1)), float(m.group(2))
        if rw and len(signs) > 1:   # the register size picks the sign among several drawings on the sheet (details, alternatives)
            signs.sort(key=lambda s: abs((s["panel"].width / s["panel"].height) / (rw / rh) - 1))
        for vi, sgn in enumerate(signs):
            pr = sgn["panel"]; note = list(pre)
            ex = info.get("extents") or [0, 0, 0, 0]
            true_size = rw and abs(ex[2] - max(rw, rh)) < 0.06 * max(rw, rh) and abs(ex[3] - min(rw, rh)) < 0.06 * min(rw, rh)
            if info.get("scale"):
                sgn["scale"] = info["scale"] / 72; note.insert(0, f"size from the sheet scale 1:{info['scale']}")
            elif true_size:
                sgn["scale"] = 1 / 72; note.insert(0, "drawn true size (drawing extents equal the register size)")
            elif rw:
                land = pr.width >= pr.height; sw = max(rw, rh) if land else min(rw, rh); sgn["scale"] = (sw / pr.width) / 25.4; note.insert(0, f"size from the register ({r['size']} mm); no scale on the sheet")
            else:
                sgn["scale"] = 10 / 72; note.insert(0, "no scale on the sheet and no register size; drawn at 1:10 — check")
            W_mm, H_mm = pr.width * sgn["scale"] * 25.4, pr.height * sgn["scale"] * 25.4
            if rw and (abs(W_mm - rw) > 0.06 * rw or abs(H_mm - rh) > 0.06 * rh): note.append(f"register size {r['size']} mm differs from the drawing ({W_mm:.0f} x {H_mm:.0f} mm) — check")
            note.append(recolour_true(sgn, code) if info.get("guidesign") and not info.get("colours") else recolour(sgn, info.get("colours") or {}, code))
            intervene = not any(not f.get("virtual") for f in sgn["fills"])
            if intervene: note.append("line drawing only (outlines, no fills): needs drawing up by hand")
            if info.get("legend_text"):
                intervene = True; note.append(f"legend is CAD text on the sheet ({', '.join(info['legend_text'][:4])}{'…' if len(info['legend_text']) > 4 else ''}): needs setting in the AS 1744 face by hand")
            svg_s, W, H = X.write_svg(sgn, fam)
            cap = re.sub(r"[^A-Z0-9]+", "_", sgn.get("caption", "").upper()).strip("_")
            fn = f"{nm}_{cd}.svg" if vi == 0 and not cap else f"{nm}_{cap or 'VAR' + str(vi + 1)}_{cd}.svg"
            n = 2
            while fn in seen: fn = re.sub(r"(_\d+)?_" + re.escape(cd) + r"\.svg$", f"_{n}_{cd}.svg", fn); n += 1
            seen[fn] = 1
            if intervene:
                idir = os.path.join(out, "intervene", fam); os.makedirs(idir, exist_ok=True); open(os.path.join(idir, fn), "w").write(svg_s)
                rows.append([code, name, "intervene/" + fam, fn, f"{W:.0f}x{H:.0f} mm", "; ".join(note), src]); continue
            open(os.path.join(folder, fn), "w").write(svg_s)
            rows.append([code, name, fam, fn, f"{W:.0f}x{H:.0f} mm", "; ".join(note), src])
        if i % 25 == 0: print(f"{i + 1}/{len(reg)} {code} {name[:40]}", flush=True)
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes", "source"]); w.writerows(rows)
    print(len(rows), "rows;", sum(1 for r in rows if r[3]), "SVGs;", dict(collections.Counter(r[2] for r in rows if r[3])))

if __name__ == "__main__": main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
