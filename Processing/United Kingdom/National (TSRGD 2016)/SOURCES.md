# Sources — United Kingdom (Department for Transport, TSRGD 2016)

## Artwork: `Original EPS/` (the pack is built from these)

* The DfT's own coloured sign artwork, "Traffic sign images" on GOV.UK
  (https://www.gov.uk/guidance/traffic-sign-images): 18 EPS packs by sign group (warning, regulatory, speed limit,
  motorway, direction and tourist, on-street parking, …), 702 EPS files (661 distinct signs; a few are shipped in two
  packs), plus the index spreadsheet `traffic-signs-images-image-details.xls` (category, description, shape, colours,
  diagram number, file names). Crown copyright, Open Government Licence v3: "You may reproduce traffic-sign images free
  of charge and without having to seek permission, but you must reproduce them accurately and not in a misleading
  context … include a statement that these images are Crown copyright."
* The EPS files are Illustrator artwork (1995–2010): legends already outlined in the Transport alphabet, no live text,
  correct colours. Two are raster (Photoshop EPS: 530, 543) and have no SVG.
* `tools/uk_eps.py` → `SVGs/<category>/<DESCRIPTION>_<DIAGRAM>.svg` + `SVGs/MANIFEST.csv`. Ghostscript converts each
  EPS to PDF; the fills are lifted exactly; a white artboard rectangle left behind a triangle/disc/octagon is dropped so
  the outside of the sign is transparent; thin borders drawn as stroked paths are outlined with Inkscape.

## Sizes: `Original PDFs/` + `SIZES.csv`

* The EPS files carry no scale. Real sizes come from the DfT "Traffic signs working drawings (TSRGD 2016)", one PDF per
  diagram, 611 drawings from https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-N
  (N = 2…16), crawled by `tools/uk_crawl.py` into `REGISTER.csv`. `tools/uk_sizes.py` OCRs each sheet (tesseract) for the
  size figures — '600 (750) (900) (1200) (1500)', the unbracketed one being the drawn size — into `Original PDFs/SIZES.csv`.
* The drawn size is applied to the sign's longer side (triangle side, disc diameter, panel width). Where the working
  drawing is dimensioned in x-heights only (direction, motorway, most rectangular signs), or no drawing exists for the
  diagram, the SVG keeps the artwork's proportions at 1 pt = 10 mm and the manifest says so ("size nominal").
* The earlier attempt to build the pack from the line-work drawings themselves (`tools/uk_extract.py`) was rejected on
  2026-09-08 and is superseded by the EPS route; the tool is kept only for reference.

## Status (2026-09-08)

658 SVGs in 18 DfT categories, awaiting Russell's review before moving to `Complete/`. Open points: sizes are nominal
for the x-height signs (SGN-060); 530 and 543 are raster only; Northern Ireland uses its own regulations (not covered).
