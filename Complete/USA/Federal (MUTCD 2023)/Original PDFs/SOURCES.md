# Sources (FHWA, public domain)

All files here are downloaded from the FHWA MUTCD site (https://mutcd.fhwa.dot.gov/):

* `SHS 2004 Edition/` — Standard Highway Signs, 2004 Edition chapters (Regulatory, Warning, Guide, School, EM, Object Markers,
  Pavement Markings, Standard Alphabets, Design Guidelines, Appendix, Blank Standards): https://mutcd.fhwa.dot.gov/ser-shs_millennium_eng.htm
* `SHS 2012 Supplement/` — 2012 Supplement to the 2004 Edition (signs added/revised in the 2009 MUTCD).
* `SHS 2009 Interim Vector/` — PDF + EPS full-size layouts for the 2009 MUTCD's new signs: https://mutcd.fhwa.dot.gov/shsm_interim/
* `SHS 2024 Releases/` — 2024 Edition of SHS (11th Edition MUTCD) phased releases 1–6: design-detail PDFs, dimension
  appendices, and vector graphics ZIPs (PDF/EPS/SVG): https://mutcd.fhwa.dot.gov/kno-shs_2024-release-status/index.htm

Vector ZIPs larger than GitHub's limits are kept locally only (see .gitignore).

## Colours (2026-09-08)

The sheet PDFs carry different RGB values for the same MUTCD colour depending on when FHWA produced them (2004 Edition yellow #fff500 and blue #007dc2; 2012 Supplement yellow #ffd24f; 2024 Edition yellow #ffd046, blue #005a9c, green #006f54, red #bf301a, orange #f7921d, black #231f20). No sheet states a colour specification; the MUTCD defines sign colours by chromaticity, not RGB. `tools/shs_palette.py` maps every sign to the 2024 Edition values so the pack is uniform; special colours (scenic byway blue, blank-out yellow, toll green, fluorescent yellow-green, purple, brown) are kept as drawn.
