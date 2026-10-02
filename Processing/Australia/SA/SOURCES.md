# Sources — South Australia (Department for Infrastructure and Transport)

* Standard Road Sign Index: https://signindex.dit.sa.gov.au (Angular app over an API at
  d2pagjgnt5.execute-api.ap-southeast-2.amazonaws.com/Production/api/v1: `/signs`, `/series`, `/references`).
  `Original/signindex_signs.json` is the full `/signs` response (1,211 signs with series, codes and sizes);
  `REGISTER.csv` summarises it; `Original PDFs/<id>.pdf` are the sign PDFs at `assets/signs/pdf/<id>.pdf`
  (vector, legends outlined). SA-specific codes carry "SA" (for example G7-SA121-3).
* Licence: the site is published under Creative Commons Attribution 3.0 Australia.

## Generated set (spec-driven, 2026-09-09, extended 2026-10-02)

* `SVGs (generated)/` is built by `tools/signgen.py` from `tools/specs/SA/*.json` (pack `SA` in `PACKS`), one spec per DIT sheet at the
  sheet's illustrated size, every dimension from the sheet (letter series and heights, margins, ink widths; "= offset / = gap" resolved on
  the drawing), AS 1744 plus0 spacing, symbols traced to `tools/symbols/sa_*` or reused from the national set where the sheet cites an
  AS 1743 sign. `MANIFEST.csv` there lists every spec: files built, `SKIPPED:` rows with the reason.
* The sheets are rendered to `Original PNGs/<first code>.png` (200 dpi, upright); specs whose sheet carries several codes name it with
  `"drawing"`. `SVGs/` (the 2026-09-06 extraction) is kept as source material only.
* Only SA-specific signs are drawn: sheets that are AS 1743 codes at an A/B size (R2-5A, R9-1-1A …) are skip rows pointing at
  `Complete/Australia/National (AS 1743)`.
* Status (2026-10-02): 606 specs, 565 SVGs, 210 skip rows. Families: Regulatory Signs 103, Speed Signs 28, Parking Signs 42, Warning Signs 122,
  Temporary Signs 177, Hazard Markers 16, Service Signs 41, Symbols 36 (the DIT Symbol Series: S / TS / WS / IS plates published as their own drawings).
  Guide and Freeway families are excluded; the "Other" series (31 sheets) is not done. Skips: AS 1743 codes at another size or placeholder sheets
  (→ national pack), G7 templates with empty symbol boxes or site names, superseded sheets, composites without letter sizes, figures.
* Two ways of building, said in each spec's notes: (1) from the sheet's stated dimensions (Regulatory, Parking, first Warning batches);
  (2) from the sheet's own filled vector artwork — rendered without the dimension line-work at 1200 dpi, legend matched word by word to the FHWA
  series and set at AS 1744 plus0, symbols traced at 1000 dpi (most of Warning, Temporary, Hazard, Service, Symbols). Every sign is overlay-checked
  against its sheet.
* `Original PNGs/<code>_upright.png` (12 files) are upright re-renders of sheets whose first render was sideways; specs name them in `"drawing"`.
* Variant values ("varies" legends) are stated in the notes and are not confirmed against SA practice. Progress and open points in
  `Tickets/SGN-005-australia-sa-state-sign-pack.md`.
* Licence for the generated set as for the sheets: CC BY 3.0 AU, credit "© Government of South Australia (Department for Infrastructure and Transport)".
