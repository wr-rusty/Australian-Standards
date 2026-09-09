# Sources — South Australia (Department for Infrastructure and Transport)

* Standard Road Sign Index: https://signindex.dit.sa.gov.au (Angular app over an API at
  d2pagjgnt5.execute-api.ap-southeast-2.amazonaws.com/Production/api/v1: `/signs`, `/series`, `/references`).
  `Original/signindex_signs.json` is the full `/signs` response (1,211 signs with series, codes and sizes);
  `REGISTER.csv` summarises it; `Original PDFs/<id>.pdf` are the sign PDFs at `assets/signs/pdf/<id>.pdf`
  (vector, legends outlined). SA-specific codes carry "SA" (for example G7-SA121-3).
* Licence: the site is published under Creative Commons Attribution 3.0 Australia.

## Generated set (spec-driven, 2026-09-09)

* `SVGs (generated)/` is built by `tools/signgen.py` from `tools/specs/SA/*.json` (pack `SA` in `PACKS`), one spec per DIT sheet at the
  sheet's illustrated size, every dimension from the sheet (letter series and heights, margins, ink widths; "= offset / = gap" resolved on
  the drawing), AS 1744 plus0 spacing, symbols traced to `tools/symbols/sa_*` or reused from the national set where the sheet cites an
  AS 1743 sign. `MANIFEST.csv` there lists every spec: files built, `SKIPPED:` rows with the reason.
* The sheets are rendered to `Original PNGs/<first code>.png` (200 dpi, upright); specs whose sheet carries several codes name it with
  `"drawing"`. `SVGs/` (the 2026-09-06 extraction) is kept as source material only.
* Only SA-specific signs are drawn: sheets that are AS 1743 codes at an A/B size (R2-5A, R9-1-1A …) are skip rows pointing at
  `Complete/Australia/National (AS 1743)`.
* Status: Regulatory family (R2, R3, R4, R6, R8, R9, RM4, RM9) — 45 specs built (75 SVGs), 16 skips; R3-SA58, R6-SA109/110/111 still to
  do (pictograms); Parking, Warning, Temporary, Service, Hazard markers not started. Progress in `Tickets/SGN-005-australia-sa-state-sign-pack.md`.
* Licence for the generated set as for the sheets: CC BY 3.0 AU, credit "© Government of South Australia (Department for Infrastructure and Transport)".
