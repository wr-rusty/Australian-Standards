---
id: SGN-078
title: Germany national sign pack (StVO / VzKat)
status: open
priority: P1
area: sources
project: none
created: 2026-09-08
updated: 2026-09-08
source: manual
---

## Summary

(what is wrong and why it matters)

## Evidence

- (sources, URLs, files — verified)

## Fix

(the concrete change)

## Verify

(how we know it is done)

## Log

- 2026-09-08 — filed.
- 2026-09-08 — First build from the free BASt vector sets (`tools/de_bast.py`, uk_eps pipeline): 242 EPS unzipped
  (Vz2017 69, VLT 2021 102, Sinnbilder/RWB/RWBA 65, Musterdateien 6), 232 distinct → **232 SVGs**: Gefahrzeichen 1,
  Vorschriftzeichen 13, Richtzeichen 130, Verkehrseinrichtungen 2, Zusatzzeichen 22, Sinnbilder und Symbole 64
  (`SVGs/MANIFEST.csv`). 551-28.eps is byte-identical to 551-27.eps (BASt error) — not built, row in the manifest.
  Scale: every EPS is 1:1 (1 pt = 25.4/72 mm) — DVK extents are in cm and the EPS BoundingBox is 28.35 pt/cm;
  checked Z 101 → 841.4 × 739.4 mm (900 mm triangle, r 40), Z 264-2.3 → 600 mm disc, Z 230 → 600 × 900, 1010-71 →
  600 × 330. Names from `bezeichnung-der-vz.pdf` → `REGISTER.csv` (1,161 entries; sections match the number
  ranges). **Gap:** 165 of 1,161 listed Zeichen have official vector; 644 have only the 1:10 JPG; 352 have neither
  (per family in SOURCES.md "Build") — the stick or generation must cover 996 entries. Contact sheets inspected:
  faces, colours and proportions correct; Z 342 is a plan illustration of the marking (grey road), the Carsharing
  Plakette lacks its raster hologram, RWB/RWBA pictograms keep their white 150 mm symbol field. Unsure: whether
  the pictogram set belongs in the sign pack at all, and whether 720 (Grünpfeil, JPG only) should sit with the
  Verkehrseinrichtungen. Housekeeping: the 670 unzipped JPGs (2.1 GB) are **not** covered by `.gitignore` (only
  the ZIPs are) — needs an ignore line before the next commit; not changed here (out of scope for this build).

## Sources found

Researched 2026-09-08; full detail in `Processing/Germany/National (StVO)/SOURCES.md`.

- **Authority:** StVO Anlagen 1–4 (binding sign images, Zeichen 101…, 201…, 301…, 600…) and the
  Verkehrszeichenkatalog 2017 (VzKat, Anlagen 1–8 VwV-StVO, current to 10.04.2025), maintained by BASt Referat V1
  for the BMDV; browsable at vzkat.de. Official list of names: `bezeichnung-der-vz.pdf` — **1,161 numbered
  entries** (Nov 2021). Guide-sign composition rules RWB 2000 / RWBA 2000 / RTB are FGSV publications (paid,
  copyrighted); their pictograms are free from BASt.
- **Artwork, free (downloaded):** 670 colour JPGs of the whole VzKat 2017 (300 dpi, 1:10, six ZIPs, 919 MB) in
  `Original JPG (BASt)/`; **official vector (DVK + DXF + EPS)** for every sign added since 2017 (51 ZIPs, 166
  variants), the 2021 Verkehrslenkungstafeln (31 ZIPs), the StVO § 39 Sinnbilder and the RWB/RWBA pictograms
  (65 ZIPs) in `Original Vector (BASt, post-2017)/`; DVKAZ/EPS/DXF sample files + format description.
- **Artwork, paid:** the complete set (~1,000 signs and symbols, DVKAZ at 1/10,000 mm, plus DIN 1451 glyphs) on
  a USB stick with the Windows converter DV-Vision (→ EPS Level 2 with colours, or DXF): **250 € + 19 % MwSt =
  297.50 €**, signed order form to Ref-V1@bast.de. No extra licence terms.
- **Licence:** BASt: "Verkehrszeichen unterliegen keinem Urheberrechtsschutz." § 5 Abs. 1 UrhG — Verordnungen and
  amtliche Erlasse (StVO Anlagen, VwV-StVO/VzKat) have no copyright. Commercial use fine; Commons uses
  `PD-VzKat`.
- **Fallback:** Wikimedia Commons "Diagrams of road signs of Germany" (249 files + 34 subcategories, PD-VzKat) —
  volunteer redrawings, not the official geometry.
- **Recommended route: official vector artwork → convert.** Step 1 now: run the UK EPS pipeline
  (`tools/uk_eps.py` pattern) over the free BASt EPS (post-2017 signs, VLT, pictograms). Step 2: buy the BASt
  stick, convert the ~1,000 DVKAZ files with DV-Vision in a Windows VM, and run the same pipeline over the full
  catalogue; JPGs serve as the visual check and for anything the stick lacks.
- **Russell decides:** (a) buy the BASt data stick (297.50 €) and provide a Windows VM/PC for DV-Vision, or
  (b) generate the pre-2017 signs from the VzKat sizes + JPGs / Commons SVGs instead; (c) whether RWB/RWBA
  composed guide signs are in scope (the FGSV rules would have to be bought and only the pictograms are free).
