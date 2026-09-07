# Sources — Australian Capital Territory (Transport Canberra and City Services)

* `Original PDFs/MITS-14-Road-signs-1-0.pdf` — Municipal Infrastructure Technical Specification 14 Road signs (2019):
  a construction specification referencing AS 1742/1743 codes; it contains no ACT-specific sign drawings.
  The ACT pack is expected to be the national set; MIS-12 Guide signs and the TCCS drafting standard sign blocks remain to be checked.

* `Original PDFs/ACTSD/` — TCCS municipal design standard drawings for signs (ACTSD-3601–3630 positioning / posts /
  footings, 3701–3735 ACT standard parking signs, 3750–3751 directional signage), from
  https://www.cityservices.act.gov.au/plan-and-build/standards-codes-and-guidelines/municipal-design-standard-drawings.
  The parking-sign sheets (3701–3714, 3721–3735) are scans with an OCR layer; only 3720/3724 (pay parking) are vector and
  `tools/act_extract.py` draws those (5 SVGs, legends in FHWA fonts). The ACT-specific parking faces (R5-13/x, R5-15/x…)
  need the CAD originals from TCCS; everything else is the national AS 1743 set.
