# Sources — Western Australia (Main Roads WA)

* Signs Index in the Main Roads technical library: https://www.mainroads.wa.gov.au/technical-commercial/technical-library/signs-index/
  served by `/api/documents/search?nodeid=<node>`; crawled by `tools/wa_crawl.py` into `REGISTER.csv` and
  `Original PDFs/<Category>/<Series>/` (PDF design sheet and DWG per sign). Series: Regulatory MR-RA/RD/RE/RM/RV/RPK/RP/RS/RT,
  Warning MR-W*, Guide MR-G*, Service MR-S*, Tourist MR-V*, Temporary MR-T*, Multi Message MMS-*, Hazard Markers MR-HM,
  Electronic signs, and Category 2 (signs being phased out; not produced).
* The index supplements AS 1742; Main Roads signs take precedence over similar Australian Standard signs in WA.
* Licence: Main Roads WA material is © Main Roads Western Australia; check the technical library terms before commercial redistribution.

## Result (2026-09-06)

`SVGs/` is produced by `tools/wa_extract.py`: LibreDWG (dwg2dxf) → ezdxf (recovery reader) → sheet furniture stripped →
rendered 1 unit = 1 mm → Inkscape PDF → sheet extractor. 1,198 SVGs from 982 DWGs; 305 in `SVGs/intervene/` because
their legend is CAD text (needs setting in the AS 1744 face by hand); 142 DWGs gave no drawing once the furniture was
removed and 35 failed to convert (LibreDWG DXF faults). Colours: 300 signs from the sheet's COLOURS note, 615 from the
series default (regulatory black/white, warning and temporary black/yellow, guide white/green, service white/blue,
tourist white/brown, hazard red/white — "check"), 283 assumed black on white ("check"). Sizes from the sheet's 1:N scale
(588), the register size (52), true-size GuideSIGN exports, else 1:10 ("check"). Known faults: GuideSIGN-made drawings
(layers GSBWFILL/GSCOLORFILL, mostly the Multi Message series) lose some glyph blocks in LibreDWG's DXF (letters missing:
"ON SIDE ROAD" → "N IDE OAD"); their GSCOLORFILL layer carries the true colours and could replace the note/series
colouring; electronic (LED) sign faces come out as dot patterns.
