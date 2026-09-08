#!/usr/bin/env python3
"""de_bast.py — Germany (StVO / VzKat) from the free official BASt vector artwork.

Sources (Processing/Germany/National (StVO)/Original Vector (BASt, post-2017)/, unzipped beside the ZIPs):
  Vz2017/               signs added since the VzKat 2017 (DVK + DXF + EPS per variant, some CorelDRAW EPS)
  VLT 2021/             Verkehrslenkungstafeln 501–551 of the VwV-StVO 2021
  Sinnbilder und Symbole/  StVO § 39 Abs. 7 and Abs. 8 Sinnbilder, RWB 2000 and RWBA 2000 pictograms
  Musterdateien/        six DVKAZ format samples with their EPS (101, 264-2.3, 314-50, 515-11, 605-11, 1010-65)
Every EPS is drawn at 1:1 (1 pt = 25.4/72 mm): the DV-Vision exports of the DVKAZ files (whose DA 11 extent is in cm,
STVOKAZ-Beschreibung.pdf) and the CorelDRAW exports alike — 60 cm = 1702 pt, checked against the DVK extents and the
VzKat sizes (Z 101: 900 mm triangle → 841.4 × 739.4 mm with 40 mm corner radius; Z 264: 600 mm disc; Z 230: 600 × 900).
Pipeline as tools/uk_eps.py: Ghostscript EPS → PDF, fills lifted exactly (no live text in these files), strokes of a
visible width outlined with Inkscape, a white page rectangle behind a non-rectangular face dropped.
Names come from the official list bezeichnung-der-vz.pdf (Original JPG (BASt)/), else from the DVK's "Bezeichnung:"
comment, else the file name. Output: SVGs/<family>/<NAME>_<CODE>.svg, SVGs/MANIFEST.csv and REGISTER.csv (every entry
of the official list + the vector-only codes, with vector / JPG / SVG presence).
  python3 tools/de_bast.py [limit]          DE_CACHE=<dir> for the EPS→PDF cache (default <pack>/.pdfcache)
  python3 tools/de_bast.py sheets <dir>     contact sheets of the SVGs (Inkscape PNG + PIL grid) into <dir>"""
import os, re, sys, csv, hashlib, subprocess, collections, unicodedata, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shs_extract as X
import uk_eps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DE = os.path.join(ROOT, "Processing", "Germany", "National (StVO)")
VEC = os.path.join(DE, "Original Vector (BASt, post-2017)")
JPG = os.path.join(DE, "Original JPG (BASt)")
NAMES_PDF = os.path.join(JPG, "bezeichnung-der-vz.pdf")
INK = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
MM_PER_PT = 25.4 / 72          # every BASt EPS is at 1:1 (see module docstring)
SETS = [("Vz2017", "Vz2017"), ("VLT 2021", "VLT 2021"), ("Musterdateien", "Musterdateien/eps"),
        ("StVO § 39 Abs. 7", "Sinnbilder und Symbole/StVO §39 Abs 7"), ("StVO § 39 Abs. 8", "Sinnbilder und Symbole/StVO §39 Abs 8"),
        ("RWB 2000", "Sinnbilder und Symbole/RWB 2000"), ("RWBA 2000", "Sinnbilder und Symbole/RWBA 2000")]
SYMBOL_PREFIX = {"StVO § 39 Abs. 7": "SB", "StVO § 39 Abs. 8": "SB", "RWB 2000": "RWB", "RWBA 2000": "RWBA", "Vz2017": "SB"}
FAMILIES = [(100, 199, "Gefahrzeichen (warning)"), (200, 299, "Vorschriftzeichen (regulatory)"), (300, 599, "Richtzeichen (guide)"),
            (600, 799, "Verkehrseinrichtungen (traffic devices)"), (1000, 1099, "Zusatzzeichen (supplementary plates)")]
SYMBOL_FAMILY = "Sinnbilder und Symbole (pictograms)"
TITLE_FIX = {"PLAKETTE-CARSHARING": "Carsharing-Plakette (mit Hologramm)",          # CorelDRAW file, no DVK comment
             "RWBA-NOTRUFSAEULE": "Notrufsäule",                                    # its DVK comment says "Fernsprecher" (copied from that symbol)
             "SB-EKFZ": "Elektrokleinstfahrzeuge im Sinne der Elektrokleinstfahrzeuge-Verordnung"}   # DVK comment has a typo
CODE_RE = re.compile(r"^(\d{3,4}(?:\.\d)?(?:-\d{1,2}(?:[.,]\d)?)?)(?![\d.])")

def fold(s):
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue").replace("ß", "ss")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()

def slug(s, sep="_", n=70): return re.sub(r"[^A-Z0-9]+", sep, fold(s).upper()).strip(sep)[:n] or "SIGN"

def family_of(code):
    m = re.match(r"(\d{3,4})", code)
    if not m: return SYMBOL_FAMILY
    n = int(m.group(1))
    return next((f for lo, hi, f in FAMILIES if lo <= n <= hi), SYMBOL_FAMILY)

def parse_register(pdf=NAMES_PDF):
    """(code, title, section) for every numbered entry of the 'Liste der amtlichen Bezeichnungen'."""
    rows = []; section = ""
    for page in pymupdf.open(pdf):
        cont = False; lines = collections.defaultdict(list)
        for w in page.get_text("words"): lines[round(w[1])].append(w)
        for y in sorted(lines):
            ws = sorted(lines[y], key=lambda w: w[0]); text = " ".join(w[4] for w in ws)
            if y < 90:
                if 60 < y: section = text
                continue
            if y > 785 or text.startswith("Nr.:"): continue
            if abs(ws[0][0] - 71) < 3 and re.match(r"\d{3,4}", ws[0][4]):
                rows.append([ws[0][4].strip(), " ".join(w[4] for w in ws[1:]).strip(), section]); cont = True
            elif abs(ws[0][0] - 71) < 3:                      # a section heading mid-page, or a sub-heading ("Allgemeine Zusatzzeichen")
                cont = False
                if re.search(r"nach (Anlage|§)|Sonstige Zeichen", text): section = text
            elif cont and ws[0][0] > 100: rows[-1][1] = (rows[-1][1] + " " + text).strip()   # wrapped title (never across a page)
    return rows

def dvk_meta(folder, stem=None):
    """Name and extent (cm) from the DVK comment block beside an EPS (the DVK named <stem> when given), if any."""
    name = ""; extent = ""
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith(".dvk") or (stem and f.lower() != stem.lower() + ".dvk"): continue
        raw = open(os.path.join(folder, f), "rb").read()
        lines = raw.decode("cp850" if any(0x80 <= b <= 0x9F or b == 0xE1 for b in raw) else "latin1").splitlines()
        for i, ln in enumerate(lines):
            if ln.startswith("99") and "Bezeichnung:" in ln:
                parts = [ln.split("Bezeichnung:", 1)[1].strip()]
                for nxt in lines[i + 1:]:
                    t = nxt[2:].strip() if nxt.startswith("99") else ""
                    if not t or not nxt.startswith("99") or re.match(r"(Eingeführt|Ausdehnung|\d+\.\s*(StVR|Verordnung)|VwV|\*{5})", t): break
                    parts.append(t)
                name = " ".join(p for p in parts if p)
            m = re.match(r"11\s+(-?\d+\.?\d*)\s*(-?\d+\.?\d*)\s*(-?\d+\.?\d*)\s*(-?\d+\.?\d*)", ln)
            if m and not extent:
                v = [float(x) for x in m.groups()]; extent = f"{v[1] - v[0]:g} x {v[3] - v[2]:g} cm"
        break
    return name, extent

def eps_files():
    """(set, eps path) in priority order, one per distinct file content (the pictogram sets share files)."""
    out = []; seen = {}
    for label, sub in SETS:
        base = os.path.join(VEC, sub)
        for root, _, files in sorted(os.walk(base)):
            for f in sorted(files):
                if not f.lower().endswith(".eps"): continue
                p = os.path.join(root, f); h = hashlib.md5(open(p, "rb").read()).hexdigest()
                if h in seen: seen[h][2].append((label, f)); continue
                seen[h] = (label, p, []); out.append(seen[h])
    return out

def sign_code(label, path, dvk_name):
    """Zeichen number from the file name (230-10, 244.3, 455.1-13 …); pictograms get PREFIX-<BASt's short file name>."""
    stem = os.path.splitext(os.path.basename(path))[0]
    m = CODE_RE.match(re.sub(r"^(Zz|ZZ|Z)[-.]", "", stem))
    if m: return m.group(1).replace(",", "."), False
    base = os.path.basename(os.path.dirname(path)) if stem.lower() == "so-22" else stem     # so-22 = Gespannfuhrwerk
    base = re.sub(r"^(Sinnbild|Sinnbildf|Aufkleber|Plakette)[- ]|-sym$|-Hologramm$", "", base, flags=re.I)
    low = stem.lower()
    pre = "AUFKLEBER" if "aufkleber" in low else "PLAKETTE" if "plakette" in low else SYMBOL_PREFIX.get(label, "SYM")
    return pre + "-" + slug(base, "-", 30), True

def jpg_index():
    idx = collections.defaultdict(list)
    for f in sorted(os.listdir(JPG)):
        if f.lower().endswith(".jpg"):
            m = CODE_RE.match(f[:-4]); idx[m.group(1).replace(",", ".") if m else f].append(f)
    return idx

def build(limit=None):
    cache = os.environ.get("DE_CACHE", os.path.join(DE, ".pdfcache"))
    out = os.path.join(DE, "SVGs"); os.makedirs(out, exist_ok=True)
    register = parse_register(); names = {c: t for c, t, _ in register}
    manifest = []; built = {}; seen_fn = set(); n = 0; vector_codes = collections.OrderedDict()
    for label, eps, dupes in eps_files():
        if label == "Musterdateien":   # the six samples share one dvkaz folder
            dvk_name, extent = dvk_meta(os.path.join(VEC, "Musterdateien", "dvkaz"), os.path.splitext(os.path.basename(eps))[0])
        else: dvk_name, extent = dvk_meta(os.path.dirname(eps))
        code, is_symbol = sign_code(label, eps, dvk_name)
        creator = "CorelDRAW" if b"CorelDRAW" in open(eps, "rb").read(600) else "DV-Vision"
        title = names.get(code) or TITLE_FIX.get(code) or re.sub(r"^Sinnbild[- ]", "", dvk_name).strip('" ') or os.path.splitext(os.path.basename(eps))[0]
        title = title[0].upper() + title[1:]
        src = "official list" if code in names else ("DVK comment" if dvk_name else "file name")
        fam = SYMBOL_FAMILY if is_symbol else family_of(code)
        vector_codes.setdefault(code, (label, os.path.relpath(eps, VEC), title))
        try:
            sign, note = uk_eps.extract(uk_eps.eps_to_pdf(eps, cache))
        except RuntimeError as ex:
            sign, note = None, str(ex)
        if sign is None:
            manifest.append([code, title, fam, "", "", f"{label}: {os.path.relpath(eps, VEC)}; {note}"]); continue
        sign["scale"] = MM_PER_PT / 25.4; sign["diamond"] = False; sign["bg"] = X.colour_name(sign["fills"][0]["fill"])
        svg, W, H = X.write_svg(sign, fam)
        folder = os.path.join(out, fam); os.makedirs(folder, exist_ok=True)
        fn = f"{slug(title)}_{code}.svg"; k = 2
        while fn in seen_fn: fn = f"{slug(title)}_{k}_{code}.svg"; k += 1
        seen_fn.add(fn); open(os.path.join(folder, fn), "w").write(svg); n += 1; built[code] = fn
        doc = pymupdf.open(uk_eps.eps_to_pdf(eps, cache)); imgs = len(doc[0].get_images())
        notes = [f"{label}: {os.path.relpath(eps, VEC)}", f"{creator} EPS at 1:1 (1 pt = 0.3528 mm)" + (f", DVK extent {extent}" if extent else ""), f"name from {src}"]
        if note: notes.append(note)
        if imgs: notes.append(f"{imgs} embedded raster image(s) in the EPS not carried (vector fills only)")
        f0 = sign["fills"][0]
        if is_symbol and X.colour_name(f0["fill"]) == "WHITE" and f0["rect"].width > 0.97 * sign["panel"].width and f0["rect"].height > 0.97 * sign["panel"].height:
            notes.append("drawn on its white symbol field as BASt supplies it")
        if code == "342": notes.append("catalogue illustration of the marking on a grey carriageway plan, not a sign face")
        for dl, df in dupes:
            dcode = sign_code(dl, df, "")[0]
            if dcode == code or not re.match(r"\d", dcode): notes.append(f"identical EPS also shipped as {dl}: {df}"); continue
            # a different Zeichen shipped as a byte-identical file: BASt's error, do not build a wrong sign from it
            manifest.append([dcode, names.get(dcode, dcode), family_of(dcode), "", "", f"{dl}: {df} is byte-identical to {os.path.basename(eps)} ({code}); not built until BASt ships the right file"])
        manifest.append([code, title, fam, fn, f"{W:.0f}x{H:.0f} mm", "; ".join(notes)])
        if limit and n >= limit: break
    with open(os.path.join(out, "MANIFEST.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "name", "family", "file", "size", "notes"]); w.writerows(manifest)
    # REGISTER: the official list + vector-only codes, with what exists for each
    jpgs = jpg_index(); reg_rows = []
    for code, title, section in register:
        v = vector_codes.get(code)
        reg_rows.append([code, title, section, family_of(code), v[0] if v else "", v[1] if v else "", ";".join(jpgs.get(code, [])), built.get(code, "")])
    listed = {c for c, _, _ in register}
    for code, (label, rel, title) in vector_codes.items():
        if code not in listed:
            reg_rows.append([code, title, "(not in the November 2021 list)", SYMBOL_FAMILY if not re.match(r"\d", code) else family_of(code), label, rel, ";".join(jpgs.get(code, [])), built.get(code, "")])
    for code, fs in jpgs.items():
        if code not in listed and code not in vector_codes:
            parent = names.get(code.split("-")[0], "")
            reg_rows.append([code, (parent + " (Unternummer)").strip(), "(not in the November 2021 list)", family_of(code), "", "", ";".join(fs), ""])
    with open(os.path.join(DE, "REGISTER.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "title", "section", "family", "vector_set", "eps", "jpg", "svg"]); w.writerows(reg_rows)
    fam_n = collections.Counter(m[2] for m in manifest if m[3])
    print(f"{n} SVGs written; {sum(1 for m in manifest if not m[3])} EPS without artwork; families: {dict(fam_n)}")
    print(f"register: {len(register)} listed entries; vector-only codes: {sum(1 for r in reg_rows if r[2].startswith('(not'))}; "
          f"listed with vector: {sum(1 for r in reg_rows[:len(register)] if r[4])}; listed with JPG: {sum(1 for r in reg_rows[:len(register)] if r[6])}")
    unmatched = [f for c, fs in jpgs.items() if c not in listed for f in fs]
    if unmatched: print(f"{len(unmatched)} JPGs whose code is not in the list:", unmatched)

def sheets(outdir, cols=8, tile=200):
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True); svgs = []
    for root, _, files in sorted(os.walk(os.path.join(DE, "SVGs"))):
        svgs += [os.path.join(root, f) for f in sorted(files) if f.endswith(".svg")]
    pngdir = os.path.join(outdir, "png"); os.makedirs(pngdir, exist_ok=True)
    todo = [s for s in svgs if not os.path.exists(os.path.join(pngdir, os.path.basename(s)[:-4] + ".png"))]
    for i in range(0, len(todo), 40):
        subprocess.run([INK, "--export-type=png", f"--export-width={tile - 10}", "--export-background=#c8c8c8", "--export-background-opacity=1", "--export-area-page"]
                       + todo[i:i + 40], capture_output=True, text=True, timeout=600)
        for s in todo[i:i + 40]:   # Inkscape writes beside the SVG; move into the scratch folder
            p = s[:-4] + ".png"
            if os.path.exists(p): os.replace(p, os.path.join(pngdir, os.path.basename(p)))
    by_fam = collections.defaultdict(list)
    for s in svgs: by_fam[os.path.basename(os.path.dirname(s))].append(s)
    for fam, fs in by_fam.items():
        per = cols * 6
        for part in range(0, len(fs), per):
            chunk = fs[part:part + per]; rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tile, rows * (tile + 28)), (235, 235, 235)); d = ImageDraw.Draw(sheet)
            for i, s in enumerate(chunk):
                p = os.path.join(pngdir, os.path.basename(s)[:-4] + ".png")
                if os.path.exists(p):
                    im = Image.open(p).convert("RGB"); im.thumbnail((tile - 10, tile - 10))
                    sheet.paste(im, ((i % cols) * tile + 5, (i // cols) * (tile + 28) + 5))
                d.text(((i % cols) * tile + 4, (i // cols) * (tile + 28) + tile - 2), os.path.basename(s)[:-4][-30:], fill=(0, 0, 0))
            sheet.save(os.path.join(outdir, f"{slug(fam)}_{part // per + 1}.png"))
    print(f"{len(svgs)} SVGs on sheets in {outdir}")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "sheets": sheets(sys.argv[2])
    else: build(int(sys.argv[1]) if len(sys.argv) > 1 else None)
