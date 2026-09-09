#!/usr/bin/env python3
"""fr_cerema.py — the France national pack from Cerema's official sign artwork ("Signaux au format SVG", Licence
Ouverte 2.0): Processing/France/National (IISR)/Original SVG (Cerema)/<series folder>/<CODE>.svg, 530 LibreOffice Draw
exports in 0.01 mm user units.

What the converter does with each file:
* keeps every filled shape exactly (coordinates scaled to real mm); the hairline stroke LibreOffice draws round every
  filled shape (a duplicate of the fill's outline, 0.03-0.08 mm on paper) is dropped;
* outlines the genuine stroked line-work (dimension-free line shapes, arrows, posts: 1,213 paths in ~190 files) with
  Inkscape object-stroke-to-path so the output is fills only;
* a closed outline that has no fill (panonceau borders, balise bodies, cone bands) reads as white only because the page
  is white: the source is rasterised and the outline's interior sampled; where it is unpainted the shape gets a white
  fill (noted in the manifest), where it already sits on paint it is left alone;
* the one gradient (J14a) is flattened to its most saturated stop, the one raster (K14, a photo of red/white tape) is
  dropped and the sign sent to intervene/; fill-opacity (four KD44 files, 0.85-0.99) is ignored;
* live <text> is never faked: strings in the road alphabets (Caractères L1/L4, alphabl1/alphabl4 — no free licensed
  digitisation exists, see SOURCES.md) mean the sign goes to SVGs/intervene/<family>/ with the strings in the manifest;
  strings in Arial/AvantGarde are the drawing's own annotations (sizes, "exemple", "Avers/Envers") and are dropped;
* composite or dimensioned drawings (several examples on one sheet, a sign with its panonceau at 1/10, cotation),
  signpost assemblies, perspective illustrations (J15a, J15b, K16) and sign-plus-light assemblies (G1*_bis) go to
  intervene/ as well, listed in COMPOSITE;
* white paint that touches nothing else is invisible on Cerema's white page (a stray white pointer in KR41, a white
  guide line in KS1 that stretched the drawing) and is not carried; strokes thinner than 0.03 mm (J16's hatched head) are
  not carried either; both are counted in the manifest;
* devices the catalogue draws in elevation (cones, piquets, balises, lamps, barriers, the K15 portal) are kept as drawn
  with a manifest note that they are not sign faces (DEVICE).

Scale: the panels are drawn at 1:5 (IISR 1re partie art. 5-3 gamme normale: triangle 1000, disc 850, octagon 800,
square 700 mm — the files measure 185/170/160/140 mm; panonceaux M9z 900x500 -> 180x100 mm). Exceptions, each checked
against an IISR size (SCALE / SCALE_WHY): the K5 devices 1:10 (K5a 750 mm high -> 75 mm file, K5b 1100 -> 110, K5d
800 -> 80; K5c fits 1:5), AB5 1:10 (its AB3a triangle is half the size of AB3b's), G1/G1a/G1b/G1c 1:10 (IISR 2e partie
1150x750, 1150x950, 750x1150, 750x1550), KD69a and KD43a_ex2 1:10 (IISR 8e partie 1000x400, 1300x400), M9zex1cdr 1:10 and
M11b_ex1_dc/ex2_dc 1:15 (they give the tabled 700x200 mm panonceau). Legend-driven series (D, Dv, Dc, Dp, E, H, SR, KD, KC,
the C60-C65 toll signs) have no fixed panel size in the IISR — the manifest says so — and the files whose letter heights
or IISR size cannot be 1:5 but whose scale is not certain carry a "SIZE TO CHECK" note (SIZE_DOUBT, 45 files: D64/D73/D74
motorway panels, Dv44, SR2/SR3/SR4/SR50, the small M10/M11 examples, the remaining KD files). Output header as the other
packs: viewBox in pt at 1 pt = 1 cm of sign, width/height in mm at 72 pt/in, one <g transform="scale(0.1)"> with the
paths in real mm. Cerema's odd file names are mapped to IISR codes in ALIAS (auou.svg = A13a, KX50 = KXC50).
The output folder is not cleaned by this tool: after a rerun delete SVGs/ files the manifest no longer lists.
  python3 tools/fr_cerema.py [limit|pattern]     FR_CACHE=<dir> for the Inkscape PNG/stroke cache"""
import os, re, sys, csv, json, math, subprocess, unicodedata, collections, tempfile
from lxml import etree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR = os.path.join(ROOT, "Processing", "France", "National (IISR)")
SRC = os.path.join(FR, "Original SVG (Cerema)")
OUT = os.path.join(FR, "SVGs")
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
NS = "{http://www.w3.org/2000/svg}"; XL = "{http://www.w3.org/1999/xlink}"
PX_PER_MM = 4                 # rasterisation used to test whether an unfilled outline sits on unpainted page
BG = (0xc0, 0xc0, 0xff)       # the colour that rasterisation paints where nothing is drawn
FAMILY = [("Panneaux_A/", "A Danger"), ("Panneaux_AB/", "AB Intersections et priorite"), ("Panneaux_B/", "B Prescription"),
          ("Panneaux_C/", "C Indication"), ("Panneaux_CE/", "CE Services"), ("Panneaux_D/", "D Direction"),
          ("Panneaux_E_EB/", "E EB Localisation"), ("Panneaux_G_balises_J/Signaux_G/", "G Passages a niveau"),
          ("Panneaux_G_balises_J/Balises_J/", "J Balises"), ("Panneaux_H/", "H Information touristique"),
          ("panneaux_K/", "K Temporaire"), ("Panonceaux_M/", "M Panonceaux"), ("Panneaux_SR/", "SR Securite routiere"),
          ("Symboles_", "S Symboles"), ("Ideogrammes_ID/", "ID Ideogrammes")]
# real mm per file mm; the panels are 1:5, the K5 devices (checked against IISR 8e partie heights) 1:10 except K5c
SCALE = {"K5A": 10, "K5B": 10, "K5D": 10,
         "AB5": 10,                                                     # same AB3a triangle as AB3b, drawn at half its size
         "G1": 10, "G1_bis": 10, "G1A": 10, "G1a_bis": 10, "G1B": 10, "G1b_bis": 10, "G1C": 10, "G1c_bis": 10,
         "M9zex1cdr": 10, "M11b_ex1_dc": 15, "M11b_ex2_dc": 15,
         "KD69a": 10, "KD43a_ex2": 10}                               # IISR 8e partie sizes: KD69a 1000x400, KD43a with KS1 1300x400
SCALE_WHY = {"K5A": "K5 device; IISR 8e partie heights K5a 750, K5b 1100, K5d 800 mm", "K5B": "K5 device; IISR 8e partie heights K5a 750, K5b 1100, K5d 800 mm",
             "K5D": "K5 device; IISR 8e partie heights K5a 750, K5b 1100, K5d 800 mm",
             "AB5": "the AB3a triangle in this file is 95 mm against 190 mm in AB3b (both the 1000 mm gamme normale)",
             "G1": "IISR 2e partie annexe: G1 and G1b 1150x750, G1a 1150x950, G1c 1550x750 mm; the files are drawn at half of that",
             "M9zex1cdr": "x2 gives the 700x200 mm panonceau of the IISR 1re partie table (700x204)",
             "M11b_ex1_dc": "x3 gives the 700x200 mm panonceau of the IISR 1re partie table (702x198)"}
for _k in ("G1_bis", "G1A", "G1a_bis", "G1B", "G1b_bis", "G1C", "G1c_bis"): SCALE_WHY[_k] = SCALE_WHY["G1"]
SCALE_WHY["M11b_ex2_dc"] = SCALE_WHY["M11b_ex1_dc"]
SCALE_WHY["KD69a"] = "IISR 8e partie: KD69a is 1000x400 mm; the file is 100x40"
SCALE_WHY["KD43a_ex2"] = "IISR 8e partie: KD43a with the KS1 symbol is 1300x400 mm; the file is 129.6x40"
DEFAULT_SCALE = 5
# legend-driven series: the IISR fixes the letter heights, not the panel; the size in the manifest is Cerema's example at 1:5
LEGEND_DRIVEN = ("D", "Da", "DA", "Dc", "Dp", "Dv", "E", "EB", "H", "SR", "KD", "KC", "KM", "C60", "C61", "C63", "C64", "C65")
# files whose drawn size cannot be 1:5 (letter heights or the IISR size table say a smaller scale) but whose scale is not certain
SIZE_DOUBT = {"D64": "the '17 km' legend is 50-80 mm at 1:5; a motorway D64 uses Hc 250-400 mm, so the file is at a smaller scale (1:20-1:50), which one is not certain",
              "D73": "legends 40-60 mm at 1:5; a motorway D73 uses Hc >= 250 mm, so the file is at a smaller scale, which one is not certain",
              "D74a": "legends 50-80 mm at 1:5; a motorway D74 uses Hc >= 250 mm, so the file is at a smaller scale, which one is not certain",
              "D74b": "legends 50-80 mm at 1:5; a motorway D74 uses Hc >= 250 mm, so the file is at a smaller scale, which one is not certain",
              "Dv44": "letters 40/60 mm at 1:5 against 50/100 mm in the other Dv43/Dv44 drawings: smaller scale, which one is not certain",
              "SR2a": "332 mm wide at 1:5 for a motorway sign; scale not certain", "SR2b": "331 mm wide at 1:5 for a motorway sign; scale not certain",
              "SR2c": "330 mm wide at 1:5 for a motorway sign; scale not certain",
              "SR3_18_12": "the file-name suffix reads as a size (18_12, 24_16, 36_24) that 1:5 does not give (404x605); scale not certain",
              "SR3_24_16": "the file-name suffix reads as a size (18_12, 24_16, 36_24) that 1:5 does not give (533x800); scale not certain",
              "SR3_36_24": "the file-name suffix reads as a size (18_12, 24_16, 36_24) that 1:5 does not give (800x1200); scale not certain",
              "SR4_ex1_dc": "letters 110 mm at 1:5 for a motorway message; scale not certain", "SR4_ex2_dc": "letters 110 mm at 1:5 for a motorway message; scale not certain",
              "SR50_ex1": "letters 150 mm at 1:5 for a motorway message; scale not certain", "SR50_ex2": "letters 150 mm at 1:5 for a motorway message; scale not certain",
              "M10c1": "135x41 mm at 1:5 is no panonceau size (IISR table: 350/500/700 x 150-700); scale not certain",
              "M10c2": "135x41 mm at 1:5 is no panonceau size (IISR table: 350/500/700 x 150-700); scale not certain",
              "M10c3": "136x41 mm at 1:5 is no panonceau size (IISR table: 350/500/700 x 150-700); scale not certain",
              "M10a_ex1": "387x113 mm at 1:5 is no panonceau size of the IISR table; scale not certain", "M10a_ex2": "347x101 mm at 1:5 is no panonceau size of the IISR table; scale not certain",
              "M10b": "306x154 mm at 1:5 against 700x350 for M10BL; scale not certain", "M1a": "385x112 mm at 1:5 is no panonceau size of the IISR table; scale not certain",
              "M11a": "304x152 mm at 1:5 is no panonceau size of the IISR table; scale not certain", "M11b_ex2": "274x164 mm at 1:5 is no panonceau size of the IISR table; scale not certain",
              "M2_ex4": "512x143 mm at 1:5 is no panonceau size of the IISR table; scale not certain",
              "E53c_ex2": "125x135 mm at 1:5 against 251x251 for the E53c_dc plaque; scale not certain", "E_46_dc": "125x62 mm at 1:5 for an E46 cartouche; scale not certain",
              }
for _k in ("KD62", "KD69b", "KD79a", "KD79b", "KD43d", "KD8_ex1", "KD8_ex2", "KD8_ex3", "KD8_ex4", "KD8_ex5", "KD8_ex6", "KD44a", "KD44b", "KD44c",
           "KD44a_ex2", "KD44b_ex2", "KD44b", "KC1_ex1", "KC1_ex3"):
    SIZE_DOUBT[_k] = "KD69a and KD43a_ex2 are drawn at 1:10 against the IISR 8e partie sizes; this file may be too (the IISR gives it no fixed size); scale not certain"
# devices the catalogue draws in elevation: kept as drawn, they are not sign faces
DEVICE = {"K5A", "K5B", "K5c", "K5D", "K1", "K10", "K15_ex1", "K15_ex2", "K2_ex2", "KR1", "KR2", "KR11j", "KR11v", "KR41",
          "J1", "J1_bis", "J3", "J7", "J10-d", "J10-g", "J11", "J12", "J13", "J16"}
HAIRLINE = 3                  # stroke-only paths thinner than 0.03 mm on the page (J16's hatched head, 320 of them) are not carried
ROAD_FONTS = ("caracteres l", "alphabl")
COMPOSITE = {"E52c_ex1": "dimensioned drawing of the E52c plaque (cotes, notes), not a sign face",
             "E52c_ex2": "dimensioned drawing of the E52c plaque (cotes, notes), not a sign face",
             "SU1": "dimensioned drawing of the SU1 symbol (Hc cotes), not a sign face",
             "SU3": "dimensioned drawing of the SU3 symbol (Hc cotes), not a sign face",
             "G2": "sign drawn with its associated M9z panonceau at 1/10 and a caption: two scales on one sheet",
             "G3": "portique drawn with its associated M9 panonceau at 1/10 and a caption: two scales on one sheet",
             "KM": "four captioned examples (KM1, KM2, KM9 x2) on one sheet; each exists as its own file (KM1_cd, KM2_cd, KM9_ex1_cd, KM9_ex2_cd)",
             "SR4": "two captioned examples on one sheet; each exists as its own file (SR4_ex1_dc, SR4_ex2_dc)",
             "K2_ex1": "front and back of the K2 barrier captioned Avers/Envers on one sheet",
             "KR42": "two arrow-board examples on one sheet; each exists as its own file (KR42_ex1_cd, KR42ex2_dc)",
             "EB10": "three sign assemblies (EB10 with cartouche and E31/E32 plates) on one sheet",
             "K14": "the twisted red/white tape is a raster image (300x74 px PNG) in the source; dropped, only the vector parts remain",
             "E52a_ex3": "front and side faces of the borne drawn side by side (the single-face drawing is E52a_ex2)",
             "E53a_ex2": "front and side faces of the borne drawn side by side (the single-face drawing is E53a_ex1)",
             "E53b_ex2": "front and side faces of the borne drawn side by side (the single-face drawing is E53b_ex1)",
             "E54a_ex": "front and side faces of the borne drawn side by side",
             "E54b_ex2": "front and side faces of the borne drawn side by side (the single-face drawing is E54b_ex1)",
             "J15a": "perspective rendering of the J15a kerb balise (3D illustration), not a face",
             "J15b": "perspective rendering of the J15b dome balise on its base (3D illustration), not a face",
             "K16": "perspective rendering of the K16 modular separators (3D illustration), not a face",
             "Dc29_ex1": "signpost assembly drawn on its post (the face alone is Dc29_ex1_dc)",
             "Dc29_ex2": "signpost assembly drawn on its post (the face alone is Dc29_ex2_dc)",
             "Dc43_ex1": "signpost assembly drawn on its post (the face alone is Dc43_ex1_dc)",
             "Dc43_ex2": "signpost assembly drawn on its post (the face alone is Dc43_ex2_dc)",
             "K8": "two drawings on one sheet: the K8 chevron bar and a single K8 chevron panel",
             "KD9_ex4": "two KD9 lane-allocation examples on one sheet",
             "KC1_ex2": "two KC1 examples ('CIRCULATION ALTERNEE', 'BARRIERE DE DEGEL') on one sheet",
             "KR43": "two arrow-board examples on one sheet; the single drawing is KR43ex1_dc",
             "M3a1": "two drawings on one sheet: the arrow alone and the arrow on its rounded panonceau",
             "M3a2": "two drawings on one sheet: the filled arrow panonceau and an outline-only version",
             "M3b1": "two drawings on one sheet: the filled arrow panonceau and an outline-only version",
             "M3b2": "two drawings on one sheet: the filled arrow panonceau and an outline-only version",
             "M8ad": "the M8a and M8d panonceaux drawn together as an assembly (each exists as its own file)",
             "SR2": "SR2a, SR2b and SR2c on one sheet; each exists as its own file",
             "G1_bis": "G1 drawn with its R24 flashing light and bell housing: the level-crossing assembly, not the sign alone (G1 is its own file)",
             "G1a_bis": "G1a drawn with its R24 flashing light and bell housing: the level-crossing assembly, not the sign alone (G1A is its own file)",
             "G1b_bis": "G1b drawn with its R24 flashing light and bell housing: the level-crossing assembly, not the sign alone (G1B is its own file)",
             "G1c_bis": "G1c drawn with its R24 flashing light and bell housing: the level-crossing assembly, not the sign alone (G1C is its own file)"}
NOTE = {"G1": "the 1150x750 panel is drawn light grey by Cerema, kept as drawn", "G1A": "the 1150x950 panel is drawn light grey by Cerema, kept as drawn",
        "G1B": "the 750x1150 panel is drawn light grey by Cerema, kept as drawn", "G1C": "the 750x1550 panel is drawn light grey by Cerema, kept as drawn",
        "M6j": "the panonceau body is drawn grey by Cerema (an unfilled outline on the page); filled white here like the other panonceaux",
        "KD44a_ex2": "pale yellow background as drawn by Cerema", "KD44b_ex2": "pale yellow background as drawn by Cerema"}
GENERIC = [("AK", "Panneau de danger temporaire"), ("AB", "Panneau d'intersection et de priorite"), ("A", "Panneau de danger"),
           ("B", "Panneau de prescription"), ("CE", "Panneau de services"), ("C", "Panneau d'indication"),
           ("Da", "Panneau de direction avec affectation de voies"), ("DA", "Panneau de direction avec affectation de voies"), ("Dc", "Panneau d'information locale"),
           ("Dp", "Panneau de signalisation pietonne"), ("Dv", "Panneau de direction cyclable"), ("D", "Panneau de direction"),
           ("EB", "Panneau d'entree ou de sortie d'agglomeration"), ("E", "Panneau de localisation"), ("G", "Signal de passage a niveau"),
           ("H", "Panneau d'information touristique"), ("J", "Balise"), ("KC", "Panneau d'indication temporaire"), ("KD", "Panneau de direction temporaire"),
           ("KM", "Panonceau temporaire"), ("KR", "Signal lumineux temporaire"), ("KX", "Signal temporaire"), ("KS", "Symbole temporaire"), ("K", "Signal temporaire"),
           ("M", "Panonceau"), ("SR", "Panneau de securite routiere"), ("SC", "Symbole"), ("SI", "Symbole"), ("SU", "Symbole"), ("SE", "Symbole"), ("ID", "Ideogramme")]

def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

# ---------- transforms and path data ----------
def parse_transform(s):
    m = [1, 0, 0, 1, 0, 0]
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        a = [float(v) for v in re.split(r"[\s,]+", args.strip()) if v]
        if name == "translate": t = [1, 0, 0, 1, a[0], a[1] if len(a) > 1 else 0]
        elif name == "scale": t = [a[0], 0, 0, a[1] if len(a) > 1 else a[0], 0, 0]
        elif name == "matrix": t = a
        else: raise ValueError("unsupported transform " + name)
        m = mul(m, t)
    return m

def mul(m, t):   # m then t applied inside (m * t as column-vector matrices: p' = m(t(p)))
    a, b, c, d, e, f = m; A, B, C, D, E, F = t
    return [a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f]

def apply(m, x, y): return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])

NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
def parse_path(d):
    """Absolute segments: ('M',x,y) ('L',x,y) ('C',x1,y1,x2,y2,x,y) ('Q',x1,y1,x,y) ('A',rx,ry,rot,laf,sf,x,y) ('Z',)."""
    toks = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]|" + NUM.pattern, d)
    segs = []; i = 0; cx = cy = sx = sy = 0.0; cmd = None; last_c = None; last_q = None
    def nums(n):
        nonlocal i
        v = [float(t) for t in toks[i:i + n]]; i += n; return v
    while i < len(toks):
        t = toks[i]
        if re.match(r"[A-Za-z]", t): cmd = t; i += 1
        elif cmd is None: raise ValueError("path without command")
        rel = cmd.islower(); c = cmd.upper()
        if c == "Z": segs.append(("Z",)); cx, cy = sx, sy; last_c = last_q = None; continue
        if c == "M":
            x, y = nums(2)
            if rel: x += cx; y += cy
            segs.append(("M", x, y)); cx, cy = sx, sy = x, y; cmd = "l" if rel else "L"; last_c = last_q = None
        elif c == "L":
            x, y = nums(2)
            if rel: x += cx; y += cy
            segs.append(("L", x, y)); cx, cy = x, y; last_c = last_q = None
        elif c == "H":
            x, = nums(1)
            if rel: x += cx
            segs.append(("L", x, cy)); cx = x; last_c = last_q = None
        elif c == "V":
            y, = nums(1)
            if rel: y += cy
            segs.append(("L", cx, y)); cy = y; last_c = last_q = None
        elif c == "C":
            x1, y1, x2, y2, x, y = nums(6)
            if rel: x1 += cx; y1 += cy; x2 += cx; y2 += cy; x += cx; y += cy
            segs.append(("C", x1, y1, x2, y2, x, y)); cx, cy = x, y; last_c = (x2, y2); last_q = None
        elif c == "S":
            x2, y2, x, y = nums(4)
            if rel: x2 += cx; y2 += cy; x += cx; y += cy
            x1, y1 = (2 * cx - last_c[0], 2 * cy - last_c[1]) if last_c else (cx, cy)
            segs.append(("C", x1, y1, x2, y2, x, y)); cx, cy = x, y; last_c = (x2, y2); last_q = None
        elif c == "Q":
            x1, y1, x, y = nums(4)
            if rel: x1 += cx; y1 += cy; x += cx; y += cy
            segs.append(("Q", x1, y1, x, y)); cx, cy = x, y; last_q = (x1, y1); last_c = None
        elif c == "T":
            x, y = nums(2)
            if rel: x += cx; y += cy
            x1, y1 = (2 * cx - last_q[0], 2 * cy - last_q[1]) if last_q else (cx, cy)
            segs.append(("Q", x1, y1, x, y)); cx, cy = x, y; last_q = (x1, y1); last_c = None
        elif c == "A":
            rx, ry, rot, laf, sf, x, y = nums(7)
            if rel: x += cx; y += cy
            segs.append(("A", rx, ry, rot, laf, sf, x, y)); cx, cy = x, y; last_c = last_q = None
    return segs

def transform_segs(segs, m):
    uniform = abs(m[1]) < 1e-9 and abs(m[2]) < 1e-9 and abs(m[0] - m[3]) < 1e-9
    out = []
    for s in segs:
        if s[0] == "Z": out.append(s)
        elif s[0] == "A":
            if not uniform: raise ValueError("arc under a non-uniform transform")
            x, y = apply(m, s[6], s[7]); out.append(("A", s[1] * abs(m[0]), s[2] * abs(m[0]), s[3], s[4], s[5], x, y))
        else:
            pts = [apply(m, s[k], s[k + 1]) for k in range(1, len(s), 2)]
            out.append((s[0],) + tuple(v for p in pts for v in p))
    return out

def segs_d(segs):
    parts = []
    for s in segs:
        if s[0] == "Z": parts.append("Z")
        elif s[0] == "A": parts.append(f"A{fmt(s[1])} {fmt(s[2])} {fmt(s[3])} {int(s[4])} {int(s[5])} {fmt(s[6])} {fmt(s[7])}")
        else: parts.append(s[0] + " ".join(fmt(v) for v in s[1:]))
    return "".join(parts)

def segs_bbox(segs):
    xs = []; ys = []
    for s in segs:
        if s[0] == "Z": continue
        pts = s[6:] if s[0] == "A" else s[1:]
        xs += pts[0::2]; ys += pts[1::2]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None

def is_closed(segs): return any(s[0] == "Z" for s in segs) or (len(segs) > 2 and segs[0][0] == "M" and abs(segs[0][1] - segs[-1][-2]) < 1 and abs(segs[0][2] - segs[-1][-1]) < 1)

def rect_segs(el):
    x, y, w, h = (float(el.get(k, "0")) for k in ("x", "y", "width", "height"))
    return [("M", x, y), ("L", x + w, y), ("L", x + w, y + h), ("L", x, y + h), ("Z",)]

# ---------- colours ----------
def norm_colour(c, root):
    c = (c or "").strip()
    m = re.match(r"url\(#([^)]+)\)", c)
    if m:
        g = root.find(f".//*[@id='{m.group(1)}']")
        stops = []
        for st in (g.iter(NS + "stop") if g is not None else []):
            col = st.get("stop-color") or re.search(r"stop-color:\s*([^;]+)", st.get("style", "") or "")
            col = col if isinstance(col, str) else (col.group(1) if col else None)
            if col: stops.append(col.strip())
        if not stops: return "#000000", "gradient with no stops read"
        def sat(h):
            r, g_, b = (int(h[i:i + 2], 16) for i in (1, 3, 5)); return max(r, g_, b) - min(r, g_, b)
        best = max((norm_colour(s, root)[0] for s in stops), key=sat)
        return best, f"gradient fill flattened to its most saturated stop {best}"
    if re.match(r"#[0-9a-fA-F]{6}$", c): return c.lower(), ""
    if re.match(r"#[0-9a-fA-F]{3}$", c): return "#" + "".join(ch * 2 for ch in c[1:]).lower(), ""
    names = {"black": "#000000", "white": "#ffffff", "red": "#ff0000", "blue": "#0000ff", "green": "#008000", "yellow": "#ffff00", "none": None}
    if c.lower() in names: return names[c.lower()], ""
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", c)
    if m: return "#%02x%02x%02x" % tuple(int(v) for v in m.groups()), ""
    raise ValueError("colour " + c)

def style_get(el, key):
    v = el.get(key)
    if v is None:
        m = re.search(r"(?:^|;)\s*" + key + r"\s*:\s*([^;]+)", el.get("style", "") or "")
        v = m.group(1).strip() if m else None
    return v

# ---------- reading a Cerema file ----------
def read_source(path):
    root = etree.parse(path).getroot()
    vb = [float(v) for v in root.get("viewBox").split()]
    file_mm = (float(root.get("width").rstrip("m")), float(root.get("height").rstrip("m")))
    units_per_mm = vb[2] / file_mm[0]
    slide = next((g for g in root.iter(NS + "g") if g.get("class") == "SlideGroup"), None)
    if slide is None: raise ValueError("no SlideGroup")
    items = []; texts = []; images = 0; notes = []
    def walk(el, m):
        for ch in el:
            if not isinstance(ch.tag, str): continue
            tag = ch.tag.replace(NS, "")
            mm = mul(m, parse_transform(ch.get("transform"))) if ch.get("transform") else m
            if tag == "g": walk(ch, mm); continue
            if tag == "text":
                for ts in ch.iter(NS + "tspan"):
                    if ts.text and ts.text.strip():
                        fam = "?"; anc = ts
                        while anc is not None and fam == "?":   # LibreOffice puts the font on the paragraph tspan
                            fam = style_get(anc, "font-family") or "?"; anc = anc.getparent()
                        texts.append((ts.text.strip(), fam.strip("'\"")))
                continue
            if tag == "image": nonlocal images; images += 1; continue
            if tag not in ("path", "rect", "polygon", "polyline", "line", "circle", "ellipse"): continue
            if ch.get("class") == "BoundingBox": continue
            if tag == "rect": segs = rect_segs(ch)
            elif tag == "path": segs = parse_path(ch.get("d", ""))
            else: raise ValueError("shape " + tag)
            if not segs: continue
            segs = transform_segs(segs, mm)
            fill = style_get(ch, "fill"); stroke = style_get(ch, "stroke")
            fill_c, n1 = norm_colour(fill if fill is not None else "black", root)
            stroke_c, _ = norm_colour(stroke or "none", root)
            if n1: notes.append(n1)
            if style_get(ch, "fill-opacity") not in (None, "1"): notes.append("fill-opacity ignored")
            sw = float(style_get(ch, "stroke-width") or 1)
            items.append({"segs": segs, "fill": fill_c, "stroke": stroke_c, "sw": sw, "cap": style_get(ch, "stroke-linecap") or "butt",
                          "join": style_get(ch, "stroke-linejoin") or "miter", "group": ch.getparent(), "d": ch.get("d")})
    walk(slide, parse_transform(slide.get("transform")))   # the SlideGroup carries the page offset
    # drop the hairline twin LibreOffice draws round each filled shape (same d, same group, fill none)
    kept = []
    for it in items:
        if it["fill"] is None and it["stroke"]:
            twin = any(o is not it and o["group"] is it["group"] and o["fill"] and o["d"] == it["d"] for o in items)
            if twin: continue
        if it["fill"] is None and not it["stroke"]: continue
        kept.append(it)
    return {"root": root, "vb": vb, "file_mm": file_mm, "upm": units_per_mm, "items": kept, "texts": texts, "images": images, "notes": sorted(set(notes))}

# ---------- strokes -> fills with Inkscape ----------
def outline_strokes(src_items, cache_key, cache):
    """Outline the stroke-only items with Inkscape; returns {index: (fill colour, segs)} in file units."""
    idx = [i for i, it in enumerate(src_items) if it["fill"] is None and it["stroke"] and it["sw"] >= HAIRLINE]
    if not idx: return {}
    tmp = os.path.join(cache, cache_key + "_strokes.svg"); out = os.path.join(cache, cache_key + "_outlined.svg")
    if not os.path.exists(out):
        body = []
        for i in idx:
            it = src_items[i]
            body.append(f'<path id="s{i}" fill="none" stroke="{it["stroke"]}" stroke-width="{it["sw"]}" stroke-linecap="{it["cap"]}" stroke-linejoin="{it["join"]}" d="{segs_d(it["segs"])}"/>')
        open(tmp, "w").write('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 100000 100000">' + "".join(body) + "</svg>")
        r = subprocess.run([INK, tmp, "--actions=select-all;object-stroke-to-path;export-plain-svg;export-filename:" + out + ";export-do"], capture_output=True, text=True, timeout=600)
        if not os.path.exists(out): raise RuntimeError("inkscape stroke-to-path failed: " + r.stderr.strip()[-200:])
    root = etree.parse(out).getroot(); res = {}
    def walk(el, m):
        for ch in el:
            if not isinstance(ch.tag, str): continue
            mm = mul(m, parse_transform(ch.get("transform"))) if ch.get("transform") else m
            if ch.tag == NS + "g": walk(ch, mm); continue
            if ch.tag == NS + "path" and (ch.get("id") or "").startswith("s"):
                i = int(ch.get("id")[1:]); fill = style_get(ch, "fill")
                res[i] = (norm_colour(fill or src_items[i]["stroke"], root)[0], transform_segs(parse_path(ch.get("d")), mm))
    walk(root, [1, 0, 0, 1, 0, 0])
    return {i: v for i, v in res.items() if i in idx}   # a cached outline file may hold hairlines from an earlier run

# ---------- unpainted test for closed unfilled outlines ----------
def raster(path, src, cache_key, cache):
    png = os.path.join(cache, cache_key + ".png")
    if not os.path.exists(png):
        w = max(8, int(round(src["file_mm"][0] * PX_PER_MM)))
        subprocess.run([INK, path, "--export-type=png", "--export-filename=" + png, f"--export-width={w}", "--export-background=#%02x%02x%02x" % BG, "--export-background-opacity=1"], capture_output=True, text=True, timeout=300)
    from PIL import Image
    return Image.open(png).convert("RGB")

def unpainted_fraction(segs, src, img, sw=0.0):
    """Sample the interior of a closed outline (inset from its edge and clear of its own stroke) in the rasterised source; 1.0 = all unpainted."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from svgpathtools import parse_path as sp
    rings = []; cur = []
    for s in segs:
        if s[0] == "M":
            if len(cur) > 2: rings.append(cur)
            cur = [(s[1], s[2])]
        elif s[0] == "Z": continue
        elif s[0] == "L": cur.append((s[1], s[2]))
        else:
            try:
                p = sp(segs_d([("M", cur[-1][0], cur[-1][1]), s]))
                cur += [(p.point(t).real, p.point(t).imag) for t in (0.25, 0.5, 0.75, 1.0)]
            except Exception: cur.append((s[-2], s[-1]))
    if len(cur) > 2: rings.append(cur)
    polys = [Polygon(r).buffer(0) for r in rings if len(r) > 2]
    polys = [p for p in polys if not p.is_empty and p.area > 0]
    if not polys: return 0.0
    poly = unary_union(polys)
    inset = poly.buffer(-max(30.0, 2.0 * 100 / PX_PER_MM, sw / 2 + 10))   # 0.3 mm of paper, two pixels or half the stroke, whichever is more
    if inset.is_empty: inset = poly.buffer(-min(10.0, math.sqrt(poly.area) / 6))
    if inset.is_empty: return 0.0
    pts = []
    geoms = list(inset.geoms) if hasattr(inset, "geoms") else [inset]
    for g in geoms:
        ext = g.exterior; n = 24
        pts += [ext.interpolate(k / n, normalized=True) for k in range(n)]
        pts.append(g.representative_point())
    vb = src["vb"]; sx = img.size[0] / vb[2]; sy = img.size[1] / vb[3]; hit = 0
    for p in pts:
        px = int((p.x - vb[0]) * sx); py = int((p.y - vb[1]) * sy)
        if 0 <= px < img.size[0] and 0 <= py < img.size[1]:
            r, g_, b = img.getpixel((px, py))
            if abs(r - BG[0]) < 24 and abs(g_ - BG[1]) < 24 and abs(b - BG[2]) < 24: hit += 1
    return hit / max(1, len(pts))

# ---------- names ----------
def load_names():
    p = os.path.join(FR, "NAMES.csv")
    if not os.path.exists(p): return {}
    return {r["code"]: (r["name"], r["source"]) for r in csv.DictReader(open(p, encoding="utf-8"))}

ALIAS = {"KX50": "KXC50", "auou": "A13a"}   # Cerema file name -> IISR code (auou.svg is the A13a children sign)

def base_code(stem):
    s = ALIAS.get(stem, stem)
    s = re.sub(r"^([A-Za-z]+)_(\d)", r"\1\2", s)               # E_46 -> E46
    for _ in range(2): s = re.sub(r"[_-]?(ex\d*|dc|cd|cdr|ancien|bis|C)$", "", s)
    s = re.sub(r"_\d+(_\d+)*$", "", s)                          # B33_110 -> B33
    return s

def lookup_name(stem, names):
    """The title of the stem's code, else of its parent code (M3b3 -> M3b, Da31a -> Da31), else the series' generic title."""
    b = base_code(stem); low = {k.lower(): v for k, v in names.items()}
    cands = [stem, b]; s = b
    while len(s) > 1 and not re.fullmatch(r"[A-Za-z]+\d+", s):
        s = s[:-1]; cands.append(s)
    for cand in cands:
        if cand.lower() in low: return low[cand.lower()]
    m = re.match(r"[A-Za-z]+", b)
    pre = m.group(0) if m else ""
    for p, g in GENERIC:
        if pre.lower() == p.lower() or (len(pre) > len(p) and pre.lower().startswith(p.lower()) and p in ("K", "D", "S")):
            return g, "generic"
    for p, g in GENERIC:
        if pre.upper().startswith(p.upper()): return g, "generic"
    return "Signal", "generic"

def ascii_upper(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Z0-9]+", "_", s.upper()).strip("_")
    if len(s) > 60: s = s[:60].rsplit("_", 1)[0]      # cut long descriptions at a word boundary
    return s or "SIGNAL"

# ---------- writer ----------
def write_svg(fills, bbox, mm_per_unit):
    x0, y0, x1, y1 = bbox; W = (x1 - x0) * mm_per_unit; H = (y1 - y0) * mm_per_unit
    m = [mm_per_unit, 0, 0, mm_per_unit, -x0 * mm_per_unit, -y0 * mm_per_unit]
    body = []
    for f in fills:
        rule = ' fill-rule="evenodd"' if f.get("evenodd") else ""
        body.append(f'<path fill="{f["fill"]}"{rule} d="{segs_d(transform_segs(f["segs"], m))}"/>')
    OW, OH = W * 0.1, H * 0.1
    svg = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{fmt(OW * 25.4 / 72)}mm" height="{fmt(OH * 25.4 / 72)}mm" viewBox="0 0 {fmt(OW)} {fmt(OH)}">',
           '<g transform="scale(0.1)">'] + ["  " + b for b in body] + ["</g>", "</svg>"]
    return "\n".join(svg) + "\n", W, H

def family_of(rel):
    for pre, fam in FAMILY:
        if rel.startswith(pre): return fam
    raise ValueError("no family for " + rel)

def convert(rel, cache, names):
    path = os.path.join(SRC, rel); stem = os.path.splitext(os.path.basename(rel))[0]
    src = read_source(path); notes = list(src["notes"]); reasons = []
    key = re.sub(r"[^A-Za-z0-9]+", "_", rel[:-4])
    outlined = outline_strokes(src["items"], key, cache)
    fills = []; backing = []; img = None; empty = 0
    boxes = [segs_bbox(it["segs"]) for it in src["items"]]
    def touches(i):
        a = boxes[i]
        return any(j != i and b and not (b[2] < a[0] or b[0] > a[2] or b[3] < a[1] or b[1] > a[3]) for j, b in enumerate(boxes))
    for i, it in enumerate(src["items"]):
        if it["fill"]:
            fills.append({"fill": it["fill"], "segs": it["segs"], "evenodd": True}); continue
        if i not in outlined: continue
        if is_closed(it["segs"]) and not touches(i):   # an empty frame with nothing drawn in or across it: annotation, not sign
            empty += 1; continue
        if is_closed(it["segs"]):
            if img is None: img = raster(path, src, key, cache)
            if unpainted_fraction(it["segs"], src, img, it["sw"]) >= 0.15:   # painted at the back: shows only where nothing else paints
                backing.append({"fill": "#ffffff", "segs": it["segs"], "evenodd": True})
        col, segs = outlined[i]
        fills.append({"fill": col, "segs": segs, "evenodd": False})
    whitened = len(backing); fills = backing + fills
    hair = sum(1 for it in src["items"] if it["fill"] is None and it["stroke"] and it["sw"] < HAIRLINE)
    # white paint that touches nothing else is invisible on the white page (stray pointers, guide lines): not carried
    fb = [segs_bbox(f["segs"]) for f in fills]
    dark = [b for f, b in zip(fills, fb) if b and f["fill"] not in ("#ffffff", "#fefefe")]
    def meets(a):
        return any(not (b[2] < a[0] - 50 or b[0] > a[2] + 50 or b[3] < a[1] - 50 or b[1] > a[3] + 50) for b in dark)
    if dark:
        keep = [f for f, b in zip(fills, fb) if f["fill"] not in ("#ffffff", "#fefefe") or (b and meets(b))]
        invisible = len(fills) - len(keep); fills = keep
    else: invisible = 0
    if outlined: notes.append(f"{len(outlined)} stroked path(s) outlined with Inkscape")
    if whitened: notes.append(f"{whitened} unfilled closed outline(s) filled white (drawn on a white page)")
    if empty: notes.append(f"{empty} empty outline frame(s) with nothing drawn inside dropped")
    if hair: notes.append(f"{hair} hairline stroke(s) under 0.03 mm not carried")
    if invisible: notes.append(f"{invisible} white shape(s) touching nothing else (invisible on the white page) dropped")
    road = [t for t, f in src["texts"] if f.lower().startswith(ROAD_FONTS)]
    other = [t for t, f in src["texts"] if not f.lower().startswith(ROAD_FONTS)]
    if road:
        reasons.append("live text in the L1/L4 road alphabet, font not available: " + " / ".join(f"'{t}'" for t in road))
    if other:
        fonts = sorted(set(f for _, f in src["texts"] if not f.lower().startswith(ROAD_FONTS)))
        notes.append("drawing annotation text dropped (" + ", ".join(fonts) + "): " + " / ".join(f"'{t}'" for t in other)[:200])
    if src["images"]: reasons.append(f"{src['images']} raster image(s) in the source dropped")
    if stem in COMPOSITE: reasons.append(COMPOSITE[stem])
    if not fills: raise ValueError("nothing to draw")
    bb = None
    for f in fills:
        b = segs_bbox(f["segs"])
        if b: bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    scale = SCALE.get(stem, DEFAULT_SCALE)
    mm_per_unit = scale / src["upm"]
    svg, W, H = write_svg(fills, bb, mm_per_unit)
    name, nsrc = lookup_name(stem, names)
    fam = family_of(rel)
    fw, fh = (bb[2] - bb[0]) / src["upm"], (bb[3] - bb[1]) / src["upm"]
    size_note = f"drawn {fw:.1f}x{fh:.1f} mm at 1:{scale}"
    if scale != DEFAULT_SCALE: size_note += f" ({SCALE_WHY[stem]})"
    code = ALIAS.get(stem, stem)
    if code != stem: notes.append(f"Cerema file name {stem}.svg")
    pre = re.match(r"[A-Za-z]+", base_code(stem)).group(0)
    if stem in SIZE_DOUBT: notes.append("SIZE TO CHECK: " + SIZE_DOUBT[stem])
    elif pre in LEGEND_DRIVEN or stem.startswith(("C60", "C61", "C63", "C64", "C65")):
        notes.append("legend-driven sign: the IISR fixes letter heights, not the panel; size is Cerema's example at 1:5")
    if stem in DEVICE: notes.append("device drawn in elevation as in the Cerema catalogue, not a sign face")
    if stem in NOTE: notes.append(NOTE[stem])
    if nsrc == "generic": notes.append("name is the series' generic title (no sign title found in the IISR text or the Wikipedia lists)")
    elif nsrc: notes.append(f"name from {nsrc}")
    return {"stem": stem, "code": code, "name": name, "family": fam, "svg": svg, "W": W, "H": H, "notes": [size_note] + notes, "reasons": reasons, "rel": rel}

def main(arg=None):
    cache = os.environ.get("FR_CACHE", os.path.join(FR, ".cache")); os.makedirs(cache, exist_ok=True)
    names = load_names()
    files = []
    for root, _, fs in os.walk(SRC):
        for f in fs:
            if f.lower().endswith(".svg"): files.append(os.path.relpath(os.path.join(root, f), SRC))
    files.sort(key=lambda r: (family_of(r), r.lower()))
    limit = None
    if arg and arg.isdigit(): limit = int(arg)
    elif arg: files = [f for f in files if re.search(arg, f)]
    manifest = []; seen = set(); n = 0; fails = []
    for rel in files:
        try:
            s = convert(rel, cache, names)
        except Exception as ex:
            fails.append((rel, str(ex))); manifest.append([os.path.splitext(os.path.basename(rel))[0], "", family_of(rel), "", "", rel, "FAILED: " + str(ex)[:150]]); continue
        folder = os.path.join(OUT, "intervene", s["family"]) if s["reasons"] else os.path.join(OUT, s["family"])
        os.makedirs(folder, exist_ok=True)
        fn = f"{ascii_upper(s['name'])}_{s['code']}.svg"; k = 2
        while fn.lower() in seen: fn = f"{ascii_upper(s['name'])}_{k}_{s['code']}.svg"; k += 1
        seen.add(fn.lower())
        open(os.path.join(folder, fn), "w").write(s["svg"]); n += 1
        notes = "; ".join(s["reasons"] + s["notes"])
        manifest.append([s["code"], s["name"], s["family"], os.path.relpath(os.path.join(folder, fn), OUT), f"{s['W']:.0f}x{s['H']:.0f} mm", rel, notes])
        if limit and n >= limit: break
    with open(os.path.join(OUT, "MANIFEST.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "source", "notes"]); w.writerows(manifest)
    fams = collections.Counter(m[2] for m in manifest if m[3] and not m[3].startswith("intervene"))
    inter = [m for m in manifest if m[3].startswith("intervene")]
    print(f"{n} SVGs written ({len(inter)} in intervene/); {len(fails)} failed; families: {dict(fams)}")
    for f in fails: print("  FAIL", f)
    for m in inter: print("  intervene", m[0], "-", m[6][:110])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
