# Sources — United Kingdom (Department for Transport, TSRGD 2016)

* `Original PDFs/Schedule NN/` — the DfT "Traffic signs working drawings (TSRGD 2016)", one PDF per diagram, 611
  drawings from the fifteen schedule pages at
  https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-N (N = 2…16),
  crawled by `tools/uk_crawl.py` into `REGISTER.csv`. Crown copyright, Open Government Licence v3.
* The drawings are black line work only: every legend is outlined, there are no text objects, and the sign's colours
  and sizes appear only in the (outlined) notes. `tools/uk_extract.py` OCRs the notes (tesseract), chains the plotted
  dots into curves, polygonises the line work and colours the faces by nesting depth.

## Status (2026-09-08): NOT USABLE

`SVGs/` holds a partial run (458 of 611) that Russell reviewed and rejected: symbol-only drawings come out with no
panel behind them, multi-panel and multi-colour signs get their depth colours wrong, and OCR-guessed colours are
unreliable. Kept only as a record of the attempt; do not upload. A different route (generation from specs with the
Transport alphabet, or a coloured source) is needed.
