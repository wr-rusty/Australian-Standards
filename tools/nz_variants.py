#!/usr/bin/env python3
"""
nz_variants.py — time-limit variants of the NZ (TCD Manual) parking signs, ticket SGN-068.

NZTA's register draws each time-restricted parking family once (P30, or P60/P120 for zones) and lists the
numerals as a component ("Numerals 75D", i.e. AS 1744 Series D at 75 mm cap). This tool composes the other
time limits from the NZTA artwork itself: every path of the base SVG (border, background, `P` 100E, class
symbol, Transport Medium legend, arrow) is kept verbatim; only the numeral outlines are replaced by the same
digits set in the repo's Series D face at 75 mm, on the base artwork's own baseline and centred where the
artwork centres them. One-line layouts (`P120 Zone`) keep the artwork's P-to-numeral gap and re-centre the
P + numerals group as the artwork does. Nothing is invented: sizes, colours and positions are the base sign's.

Time-limit set: 5, 10, 15, 30, 60, 120, 180, 240 minutes (see the SGN-068 ticket for the evidence).

Usage: nz_variants.py [--dry-run] [--sheet DIR]
Writes: <NZ>/SVGs/Parking Signs/<TITLE>_P<VALUE>_<CODE>.svg (never overwrites; existing files are skipped)
        <NZ>/SVGs/MANIFEST.csv (one row appended per new file)
"""
import os, re, sys, csv, glob, subprocess, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import signgen
from svgpathtools import parse_path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NZ = os.path.join(ROOT, "Complete", "New Zealand", "National (TCD Manual)")
SVGS = os.path.join(NZ, "SVGs")
FAMILY = "Parking Signs"
MANIFEST = os.path.join(SVGS, "MANIFEST.csv")
INKSCAPE = "/Applications/Inkscape.app/Contents/MacOS/inkscape"

VALUES = [5, 10, 15, 30, 60, 120, 180, 240]
NUM_H = 75.0            # register: Numerals 75D
SERIES = "D"

# (base file, register code, base value, values to build, register title of the base)
# The base files are NZTA's own artwork as extracted by nz_extract.py; titles are the register's.
FAMILIES = [
    # R6-30 time restricted, standard hours (PP21, 300x300)
    ("TIME_RESTRICTED_STANDARD_HOURS_P30_WITH_SINGLE_ARROW_POINTING_RIGHT_P30_PP21.svg", "PP21", 30, [5, 10, 15, 180, 240],
     "Time restricted, standard hours, P30 with single arrow pointing right (P30)"),
    ("TIME_RESTRICTED_STANDARD_HOURS_P30_WITH_SINGLE_ARROW_POINTING_LEFT_P30_PP21.svg", "PP21", 30, [5, 10, 15, 180, 240],
     "Time restricted, standard hours, P30 with single arrow pointing left (P30)"),
    ("TIME_RESTRICTED_STANDARD_HOURS_P30_WITH_DOUBLE_ARROW_P30_PP21.svg", "PP21", 30, [5, 10, 15, 180, 240],
     "Time restricted, standard hours, P30 with double arrow (P30)"),
    # R6-31 non-standard hours (PP22, 300x360, `Mon-Fri` legend as drawn)
    ("TIME_RESTRICTED_NON_STANDARD_HOURS_P30_SINGLE_ARROW_POINTING_RIGHT_NON_STANDARD_HOURS_PP22.svg", "PP22", 30, None,
     "Time restricted non-standard hours P30 single arrow pointing right (Non-standard hours)"),
    ("TIME_RESTRICTED_NON_STANDARD_HOURS_P30_SINGLE_ARROW_POINTING_LEFT_NON_STANDARD_HOURS_PP22.svg", "PP22", 30, None,
     "Time restricted non-standard hours P30 single arrow pointing left (Non-standard hours)"),
    ("TIME_RESTRICTED_NON_STANDARD_HOURS_P30_DOUBLE_ARROW_NON_STANDARD_HOURS_PP22.svg", "PP22", 30, None,
     "Time restricted non-standard hours P30 double arrow (Non-standard hours)"),
    # R6-32 other times (PP22, 300x360)
    ("TIME_RESTRICTED_OTHER_TIMES_P30_SINGLE_ARROW_POINTING_RIGHT_OTHER_TIMES_PP22.svg", "PP22", 30, None,
     "Time restricted, other times, P30 single arrow pointing right (Other times)"),
    ("TIME_RESTRICTED_OTHER_TIMES_P30_SINGLE_ARROW_POINTING_LEFT_OTHER_TIMES_PP22.svg", "PP22", 30, None,
     "Time restricted, other times, P30 single arrow pointing left (Other times)"),
    ("TIME_RESTRICTED_OTHER_TIMES_P30_DOUBLE_ARROW_OTHER_TIMES_PP22.svg", "PP22", 30, None,
     "Time restricted, other times, P30 double arrow (Other times)"),
    # R6-53.2 bus parking time restricted (PP3 300x400, PP31 300x450)
    ("CLASS_RESTRICTED_BUS_PARKING_TIME_RESTRICTED_P30_STANDARD_TIME_RESTRICTED_PP3.svg", "PP3", 30, None,
     "Class restricted bus parking time restricted P30 standard (Time restricted)"),
    ("CLASS_RESTRICTED_BUS_PARKING_TIME_RESTRICTED_P30_ARROW_POINTING_RIGHT_TIME_RESTRICTED_PP31.svg", "PP31", 30, None,
     "Class restricted bus parking time restricted P30 arrow pointing right (Time restricted)"),
    ("CLASS_RESTRICTED_BUS_PARKING_TIME_RESTRICTED_P30_ARROW_POINTING_LEFT_TIME_RESTRICTED_PP31.svg", "PP31", 30, None,
     "Class restricted bus parking time restricted P30 arrow pointing left (Time restricted)"),
    ("CLASS_RESTRICTED_BUS_PARKING_TIME_RESTRICTED_P30_DOUBLE_ARROW_TIME_RESTRICTED_PP31.svg", "PP31", 30, None,
     "Class restricted bus parking time restricted P30 double arrow (Time restricted)"),
    # R6-54.2 shuttle parking time restricted
    ("CLASS_RESTRICTED_SHUTTLE_PARKING_TIME_RESTRICTED_P30_STANDARD_TIME_RESTRICTED_PP3.svg", "PP3", 30, None,
     "Class restricted shuttle parking time restricted P30 standard (Time restricted)"),
    ("CLASS_RESTRICTED_SHUTTLE_PARKING_TIME_RESTRICTED_P30_ARROW_POINTING_RIGHT_TIME_RESTRICTED_PP31.svg", "PP31", 30, None,
     "Class restricted shuttle parking time restricted P30 arrow pointing right (Time restricted)"),
    ("CLASS_RESTRICTED_SHUTTLE_PARKING_TIME_RESTRICTED_P30_ARROW_POINTING_LEFT_TIME_RESTRICTED_PP31.svg", "PP31", 30, None,
     "Class restricted shuttle parking time restricted P30 arrow pointing left (Time restricted)"),
    ("CLASS_RESTRICTED_SHUTTLE_PARKING_TIME_RESTRICTED_P30_DOUBLE_ARROW_TIME_RESTRICTED_PP31.svg", "PP31", 30, None,
     "Class restricted shuttle parking time restricted P30 double arrow (Time restricted)"),
    # R6-50 loading zone (P5 drawn; "Numeral 75D" is a register component) — council practice: P10, P15, P30
    ("CLASS_RESTRICTED_LOADING_ZONE_STANDARD_LOADING_ZONE_PP21.svg", "PP21", 5, [10, 15, 30],
     "Class restricted Loading zone standard (Loading Zone)"),
    ("CLASS_RESTRICTED_LOADING_ZONE_ARROW_POINTING_RIGHT_LOADING_ZONE_PP22.svg", "PP22", 5, [10, 15, 30],
     "Class restricted Loading Zone arrow pointing right (Loading Zone)"),
    ("CLASS_RESTRICTED_LOADING_ZONE_ARROW_POINTING_LEFT_LOADING_ZONE_PP22.svg", "PP22", 5, [10, 15, 30],
     "Class restricted Loading Zone arrow pointing left (Loading Zone)"),
    ("CLASS_RESTRICTED_LOADING_ZONE_DOUBLE_ARROW_LOADING_ZONE_PP22.svg", "PP22", 5, [10, 15, 30],
     "Class restricted Loading Zone double arrow (Loading Zone)"),
    # Parking zone signs (PZ series; "Numerals 75D"), zone limits 30/60/120/180/240
    ("E_G_P_60_ZONE_PZ21.svg", "PZ21", 60, [30, 120, 180, 240], "e.g. P / 60 / ZONE"),
    ("E_G_P_60_MON_FRI_ZONE_PZ22.svg", "PZ22", 60, [30, 120, 180, 240], "e.g. P / 60 / Mon – Fri / ZONE"),
    ("E_G_P_120_MON_FRI_ZONE_PZ12.svg", "PZ12", 120, [30, 60, 180, 240], "e.g. P 120 / Mon - Fri / ZONE"),
    ("E_G_P_120_MON_FRI_ZONE_BEGINS_PZ13.svg", "PZ13", 120, [30, 60, 180, 240], "e.g. P 120 / Mon – Fri / ZONE /BEGINS"),
    ("E_G_P_120_ZONE_ENDS_PZ22.svg", "PZ22", 120, [30, 60, 180, 240], "e.g. P / 120 / ZONE / ENDS"),
    ("E_G_P_120_9AM_4PM_MON_FRI_ZONE_PZ23.svg", "PZ23", 120, [30, 60, 180, 240], "e.g. P / 120 / 9am – 4pm / Mon – Fri / ZONE"),
]

PATH_RE = re.compile(r'<path fill="([^"]+)"( fill-rule="evenodd")?(?: transform="[^"]+")? d="([^"]+)"/>')
fmt = signgen.fmt

def read_paths(svg):
    """[(match_start, match_end, fill, evenodd, d, bbox(x0,x1,y0,y1))] in paint order."""
    out = []
    for m in PATH_RE.finditer(svg):
        b = parse_path(m.group(3)).bbox()
        out.append(dict(span=m.span(), fill=m.group(1), eo=bool(m.group(2)), d=m.group(3), bbox=b))
    return out

def overshoot(fc, ch, H):
    """How far a digit's ink drops below the baseline (round-bottomed digits), in mm."""
    n = fc.glyph(ch)[0]; b = fc.bounds(n)
    return max(0.0, -b[1]) * H / signgen.CAP

def analyse(paths, base_value, legend):
    """Find the `P` (100E, 100 mm tall) and the numeral outlines (75D, 75-78 mm tall) of a base sign."""
    sign = max(paths, key=lambda p: (p["bbox"][1] - p["bbox"][0]) * (p["bbox"][3] - p["bbox"][2]))
    x0, x1, y0, y1 = sign["bbox"]
    P = [p for p in paths if p["fill"] == legend and abs((p["bbox"][3] - p["bbox"][2]) - 100) < 1.5 and 70 < p["bbox"][1] - p["bbox"][0] < 90]
    nums = [p for p in paths if p["fill"] == legend and 74 <= p["bbox"][3] - p["bbox"][2] <= 79 and p["bbox"][1] - p["bbox"][0] <= 60]
    digits = str(base_value)
    if len(P) != 1 or len(nums) != len(digits):
        raise SystemExit(f"cannot read base: {len(P)} P paths, {len(nums)} numeral paths for {digits}")
    nums.sort(key=lambda p: p["bbox"][0])
    fc = signgen.face(SERIES)
    baseline = max(p["bbox"][3] - overshoot(fc, ch, NUM_H) for p, ch in zip(nums, digits))
    P = P[0]
    one_line = nums[0]["bbox"][2] < P["bbox"][3] - 50      # numerals beside the P, not under it
    return dict(sign=(x0, x1, y0, y1), P=P, nums=nums, baseline=baseline, one_line=one_line)

def numeral_paths(text, x_ink_left, baseline):
    fc = signgen.face(SERIES)
    return fc.path(text, NUM_H, x_ink_left, baseline)

def compose(svg, info, value, legend):
    """Return the variant SVG text: base paths verbatim, numerals replaced, P re-centred on one-line layouts."""
    fc = signgen.face(SERIES)
    text = str(value)
    nums, P = info["nums"], info["P"]
    ink_w = fc.ink_width(text, NUM_H)
    group_c = (nums[0]["bbox"][0] + nums[-1]["bbox"][1]) / 2         # where the artwork centres the numerals
    p_shift = 0.0
    if info["one_line"]:
        gap = nums[0]["bbox"][0] - P["bbox"][1]                        # artwork's P-ink to first-numeral-ink gap
        group_c = (P["bbox"][0] + nums[-1]["bbox"][1]) / 2             # artwork centres P + numerals together
        new_w = (P["bbox"][1] - P["bbox"][0]) + gap + ink_w
        p_left = group_c - new_w / 2
        p_shift = p_left - P["bbox"][0]
        x_left = p_left + (P["bbox"][1] - P["bbox"][0]) + gap
    else:
        x_left = group_c - ink_w / 2
    d = numeral_paths(text, x_left, info["baseline"])
    new_num = f'  <path fill="{legend}" d="{d}"/>'
    # the file is one path per line: the first numeral line takes the new numerals, the other numeral lines go,
    # the P line gets a translate on one-line layouts, everything else is copied verbatim
    num_d = {p["d"] for p in nums}; first_d = nums[0]["d"]
    out = []
    for line in svg.split("\n"):
        m = PATH_RE.search(line)
        if m and m.group(3) in num_d:
            if m.group(3) == first_d: out.append(new_num)
            continue
        if m and p_shift and m.group(3) == P["d"]:
            out.append(f'  <path fill="{P["fill"]}"{" fill-rule=\"evenodd\"" if P["eo"] else ""} transform="translate({fmt(round(p_shift, 2))} 0)" d="{P["d"]}"/>')
            continue
        out.append(line)
    return "\n".join(out)

def variant_filename(base, code, base_value, value):
    stem = base[:-4]
    stem = re.sub(rf"_{code}$", "", stem)
    stem = re.sub(rf"_P?{base_value}(?=_|$)", "", stem)
    return f"{stem}_P{value}_{code}.svg"

def variant_title(title, base_value, value):
    return re.sub(rf"(?<!\d)(P ?/? ?){base_value}(?!\d)", lambda m: m.group(1) + str(value), title)

def manifest_rows():
    with open(MANIFEST, newline="") as fh:
        r = csv.DictReader(fh); return r.fieldnames, list(r)

def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sheet", help="directory for PNG renders + contact sheet of what was written")
    a = ap.parse_args(argv)
    fields, rows = manifest_rows()
    by_file = {r["file"]: r for r in rows}
    new_rows, written, skipped = [], [], []
    for base, code, base_value, values, title in FAMILIES:
        path = os.path.join(SVGS, FAMILY, base)
        if not os.path.exists(path): raise SystemExit(f"missing base {base}")
        svg = open(path).read()
        paths = read_paths(svg)
        legend = "#ffffff"
        info = analyse(paths, base_value, legend)
        base_row = by_file.get(base, {})
        for v in (values or [x for x in VALUES if x != base_value]):
            fn = variant_filename(base, code, base_value, v)
            out = os.path.join(SVGS, FAMILY, fn)
            if os.path.exists(out): skipped.append(fn); continue
            text = compose(svg, info, v, legend)
            note = (f"SGN-068 variant of {base}: NZTA artwork kept verbatim (border, background, P 100E, symbol, legend, arrow); "
                    f"numerals '{v}' set in AS 1744 Series D at 75 mm (register: Numerals 75D) on the artwork's numeral baseline "
                    f"({fmt(round(info['baseline'], 1))} mm), " +
                    ("P + numerals re-centred as a group with the artwork's P-to-numeral gap" if info["one_line"] else "centred as the artwork's numerals") +
                    "; time-limit set 5/10/15/30/60/120/180/240 min per ticket evidence")
            row = {"code": code, "name": variant_title(title, base_value, v), "family": FAMILY, "file": fn,
                   "size": base_row.get("size", ""), "register_dimensions": base_row.get("register_dimensions", ""), "notes": note}
            if not a.dry_run:
                with open(out, "w") as fh: fh.write(text)
            new_rows.append(row); written.append(out)
    if not a.dry_run and new_rows:
        with open(MANIFEST, "a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields); [w.writerow(r) for r in new_rows]
    print(f"{len(written)} variants {'would be ' if a.dry_run else ''}written, {len(skipped)} already present")
    if a.sheet and written and not a.dry_run: sheet(written, a.sheet)

def sheet(files, outdir):
    from PIL import Image, ImageDraw
    os.makedirs(outdir, exist_ok=True); pngs = []
    for f in files:
        png = os.path.join(outdir, os.path.basename(f)[:-4] + ".png")
        subprocess.run([INKSCAPE, f, "--export-type=png", "--export-height=260", "--export-background=#888888",
                        f"--export-filename={png}"], capture_output=True)
        if os.path.exists(png): pngs.append(png)
    cw, ch, cols = 200, 300, 12
    rows = (len(pngs) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw, rows * ch), (60, 60, 60)); d = ImageDraw.Draw(im)
    for k, p in enumerate(pngs):
        t = Image.open(p).convert("RGB"); t.thumbnail((190, 260))
        x, y = (k % cols) * cw, (k // cols) * ch
        im.paste(t, (x + 5, y + 20)); d.text((x + 5, y + 5), os.path.basename(p)[:30], fill=(255, 255, 255))
    im.save(os.path.join(outdir, "variants_sheet.png")); print("sheet:", os.path.join(outdir, "variants_sheet.png"))

if __name__ == "__main__":
    main(sys.argv[1:])
