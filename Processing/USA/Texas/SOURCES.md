# Sources — Texas (TxDOT)

* `Original PDFs/shsd-2012-section1..13.pdf` — Standard Highway Sign Designs for Texas, 2012 Edition Revision 4 (May 2021),
  from https://www.txdot.gov/business/resources/traffic-design-standards/highway-sign-designs.html
  (section PDFs on ftp.dot.state.tx.us/pub/txdot-info/trf/shsd/2012/). Vector sheets in the FHWA SHS layout: several
  signs per page with lettered dimensions, size tables, code labels (R1-2bTP, R7-107R (L,DBL)) and colour notes.
* Licence: TxDOT publications are public records of the State of Texas; no copyright restriction is asserted on the SHSD.

`SVGs/` is produced by `tools/tx_extract.py` (the MUTCD extractor `tools/shs_extract.py` with Texas code patterns);
`SVGs/MANIFEST.csv` records the size row used and anything to check.

## Result (2026-09-05)

1,870 SVGs in 13 family folders (`Symbols and Arrows/` holds section 11's standard arrow and symbol details, useful as
artwork but not signs). Legends set in Clearview / Highway *Plus fonts are outlined from the sheets' embedded font
programs. 30 files sit in `SVGs/intervene/…` (fonts the sheet does not embed, or FHWA-style artwork faults) and 594 rows
carry a "check" note, mostly size (no conventional-road marker in the size table, so the smallest row is used). Known
faults to review: symbol placeholders drawn as black blocks on sheets that say "see Symbol section"; a few sheets with
dimension figures outlined inside the panel (e.g. R4-10); outline-less square signs (e.g. R5-1) rendered without their
white background.
