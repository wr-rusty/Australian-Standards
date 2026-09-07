# Sources — New South Wales (Transport for NSW)

* Register: https://www.transport.nsw.gov.au/operations/roads-and-waterways/traffic-signs — 1,662 signs (`REGISTER.csv`,
  crawled by `tools/nsw_crawl.py`), one page per sign with sign number, description, whether it is a standard sign,
  council use, legislative and technical references, and a design plan PDF for most (`Original PDFs/<code>.pdf`,
  A3 CAD sheets, usually 1:5, FHWA Series fonts embedded; older sheets have all text outlined).
* Signs whose number ends in "n" are NSW designs; others are the NSW plan of a national (AS 1743) sign.
* Licence: Transport for NSW content is Creative Commons Attribution 4.0 unless otherwise stated; attribute
  "© State of New South Wales (Transport for NSW)".

`SVGs/` is produced by `tools/nsw_extract.py` via `tools/sheet_extract.py`; `SVGs/MANIFEST.csv` records the size source
and anything to check.
