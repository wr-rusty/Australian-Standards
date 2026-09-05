# Sources — California (Caltrans)

* `Original PDFs/<series>/` — Caltrans California Sign Specification Drawings (CA-coded signs: G, SG, S, R, SR, C, SC, W, SW
  series plus cross-reference and deleted-sign lists), one PDF per sign from https://dot.ca.gov/programs/safety-programs/sign-specs
  (`REGISTER.csv` lists every link). Roughly half the sheets are vector drawings; the rest are scanned images with an OCR
  text layer, which the sheet extractor cannot use (they would need tracing or a vector copy from Caltrans).
* National (MUTCD-coded) signs used in California are in `USA/Federal (MUTCD 2023)`.
* Licence: California state publications; Caltrans sign specs are published for public use.

## Result (2026-09-05)

`SVGs/` is produced by `tools/ca_extract.py` (the sheet extractor with Caltrans rules): 245 SVGs from the 246 vector
sheets; the 228 scanned sheets are listed in `SVGs/MANIFEST.csv` without a file. Older Caltrans sheets are drawn in two
tones (white panel, black legend) with the real colours in a COLORS note, so the driver recolours them from that note
(light background: white → background colour, black → legend colour; dark background: black → background colour, white
stays white); newer sheets are drawn in colour and kept as drawn. Sizes come from the SIGN SIZE (inches) table row that
matches the drawing's proportions ("Var" widths follow the drawing); sheets without a readable table are drawn at 1:10
and marked "check" (200 rows carry a check note). Known faults to review: sheets with several drawings also yield their
detail drawings (R10-3e, S34 pavement marking); multi-panel service signs (SG42-x) keep fragments of their dashed
placeholder outlines; signs with three or more colours on a two-tone sheet cannot be told apart (noted).
