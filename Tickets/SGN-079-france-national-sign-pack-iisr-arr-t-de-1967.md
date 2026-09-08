---
id: SGN-079
title: France national sign pack (IISR / arrêté de 1967)
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

## Sources found

Researched 2026-09-08; full detail in `Processing/France/National (IISR)/SOURCES.md`.

- **Authority:** Arrêté du 24 novembre 1967 relatif à la signalisation des routes et des autoroutes (Légifrance
  LEGITEXT000006075080) and the Instruction interministérielle sur la signalisation routière (IISR), parties 1–9,
  whose consolidated PDFs carry the sign figures. Numbering A/AB/B/C/CE/D/E/EB/G/H/J/K/M/SR + symbols SC/SI/SU/SE
  and ideograms ID; roughly 500 panel types before variants (A 29, AB 9, B 88, C 55, CE 39, D 56, E 26, G 10,
  H 10, J 13, K 35, M 59, SR 5).
- **Artwork, official vector (downloaded):** Cerema's "Signaux au format SVG (pour le web)"
  (equipementsdelaroute.cerema.fr, Jan 2025, Box share `cerema.app.box.com/v/signauxroutiers`, uploaded by
  Cerema's signalisation lead Oct 2023): **530 SVGs**, 16 folders (A 20, AB 9, B 79, C 20, CE 20, D 72, E/EB 22,
  G+J 29, H 11, K 63, M 110, SR 14, SC 17, SI 15, SU/SE 9, ID 20) in
  `Original SVG (Cerema)/` with `BOX_MANIFEST.csv`. LibreOffice Draw exports sized in mm; 510 have outlined
  legends, 20 keep live text (Arial, AvantGarde, alphabl1/alphabl4 = L1/L4 alphabets) to outline.
- **Specs (downloaded):** the nine IISR parts, versions consolidées 9 Jan 2019 (Doubs prefecture site, 506 pp
  total) in `Original PDFs (IISR)/`; figures inside are raster, use them for sizes/colours. Newer consolidations
  on Cerema's site (part 1 2016, part 9 2024) to check.
- **Licence:** Cerema site footer "Sauf mention contraire, tous les contenus de ce site sont sous licence
  etalab-2.0" — Licence Ouverte 2.0: free commercial reuse worldwide with attribution (Cerema) and date. Légifrance
  content likewise Licence Ouverte 2.0 (arrêté du 24 juin 2014). No paid product: Cerema does not sell the vector
  files, it gives them away.
- **Fallback:** Wikimedia Commons "Diagrams of road signs of France" (19 subcategories) — own-work redrawings
  under GFDL/CC BY-SA 3.0 (share-alike); not needed.
- **Recommended route: official vector artwork → convert.** Normalise the 530 Cerema SVGs (strip OOo wrappers,
  outline the 20 text files with the L1/L4 alphabets, apply IISR sizes), families by letter, MANIFEST.csv — the
  UK route with SVG instead of EPS input.
- **Russell decides:** attribution line for the platform ("Source : Cerema, licence Etalab 2.0, 2025"); whether
  the dynamic (9e partie) and temporary-direction (KC/KD) signs missing from the Cerema set are generated or
  left out; nothing to buy.

- 2026-09-08 13:30 — build stopped at Russell's hard stop before the agent finished its contact-sheet inspection: 530 SVGs written (25 in intervene), tool tools/fr_cerema.py, MANIFEST.csv complete. Still to do: inspect all contact sheets (a random 48 looked right; J15a balise and Dc29 local-information example are Cerema illustrations, not faces — move to intervene), resolve the M1a row the agent was debugging, decide the attribution line.
