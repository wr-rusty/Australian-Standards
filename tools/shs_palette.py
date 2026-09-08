#!/usr/bin/env python3
"""shs_palette.py — one colour value per MUTCD colour across the federal pack.

FHWA's Standard Highway Signs sheets were produced at different times and their PDFs carry different RGB values for
the same sign colour: the 2024 Edition sheets give yellow #ffd046, green #006f54, blue #005a9c, red #bf301a,
orange #f7921d, black #231f20; the 2004 Edition sheets give yellow #fff500, blue #007dc2, green #009140, red #d9261c,
orange #e8781a, black #1f1a17; the 2012 Supplement yellow #ffd24f, blue #005697, green #006f51. No sheet states a
colour specification (the MUTCD defines colours by chromaticity, not RGB). The pack uses the 2024 sheet values for
every sign, so a 2004-era sign sits next to a 2024 one in the same yellow. Special colours are left alone: scenic
byway blue (#291770/#2c286d), blank-out sign yellow (#fff200), electronic-toll green (#6abd45), fluorescent
yellow-green (#bed73d), purple (#6d276a), brown (#7d4803).   python3 tools/shs_palette.py [pack SVGs folder]"""
import os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "Complete", "USA", "Federal (MUTCD 2023)", "SVGs")
PALETTE = {  # sheet-edition variant -> 2024 Edition value
    "#fff500": "#ffd046", "#ffd24f": "#ffd046", "#fbcb30": "#ffd046", "#fed147": "#ffd046", "#fecd03": "#ffd046", "#f1d141": "#ffd046",
    "#007dc2": "#005a9c", "#005697": "#005a9c", "#4a5778": "#005a9c",
    "#009140": "#006f54", "#006f51": "#006f54", "#097054": "#006f54",
    "#d9261c": "#bf301a", "#ed1c24": "#bf301a",
    "#e8781a": "#f7921d", "#f5911d": "#f7921d",
    "#1f1a17": "#231f20", "#030505": "#231f20", "#030404": "#231f20", "#000000": "#231f20", "#221f20": "#231f20",
}

def main(pack=PACK):
    changed = 0; swaps = {}
    for f in glob.glob(os.path.join(pack, "**", "*.svg"), recursive=True):
        s = open(f).read()
        def sub(m):
            h = m.group(1).lower(); t = PALETTE.get(h, h)
            if t != h: swaps[h] = swaps.get(h, 0) + 1
            return f'fill="{t}"'
        s2 = re.sub(r'fill="(#[0-9a-fA-F]{6})"', sub, s)
        if s2 != s: open(f, "w").write(s2); changed += 1
    print(f"{changed} files recoloured; swaps: {swaps}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else PACK)
