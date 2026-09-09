---
id: SGN-079
title: France national sign pack (IISR / arrêté de 1967)
status: open
priority: P1
area: sources
project: none
created: 2026-09-08
updated: 2026-09-09
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
- 2026-09-09 — inspection finished: every family rendered as a contact sheet on grey (Inkscape 150 px, PIL grid) and looked at; source-vs-output comparisons for the doubtful files. Found and fixed in `tools/fr_cerema.py`, all 530 rerun (`SVGs/` tidied of renamed files):
  - not faces → intervene (21 more, now **46**): J15a, J15b, K16 (perspective illustrations); Dc29_ex1/ex2, Dc43_ex1/ex2 (signposts on their post; the `_dc` faces stay); G1_bis, G1a_bis, G1b_bis, G1c_bis (cross with its R24 light and bell); K8, KC1_ex2, KD9_ex4, KR43, SR2, M3a1, M3a2, M3b1, M3b2 (two drawings on one sheet); M8ad (M8a+M8d assembly).
  - lost fills / stray paint: M6j body was left transparent because the unpainted test sampled inside its own 0.9 mm stroke → inset now clears the stroke; KS1 and KR41 were stretched by invisible white paint (a white guide line, a white pointer) → white shapes touching nothing else are dropped; J16's 320 hairline strokes (0.01 mm) are not carried and are counted.
  - wrong sizes: AB5 was 475×657 (drawn at half of AB3b) → 1:10, 950×1314; G1/G1A/G1B/G1C were half the IISR 2e partie sizes → 1:10 (1150×750, 1150×950, 750×1150, 750×1550); KD69a 500×200 → 1000×400 and KD43a_ex2 → 1300×400 per the 8e partie table; M9zex1cdr 1:10, M11b_ex1_dc/ex2_dc 1:15 (700×200 panonceau). Header arithmetic checked on 11 files across A/B/AB/C/M/K/G/ID/SC: all consistent.
  - names: `auou.svg` is the A13a children sign (aliased, code A13a); KX50 now carries its IISR code KXC50; eleven NAMES.csv rows fixed where the IISR parse had taken a size or half a sentence (KD43a/b, KD69a/b, M6a/b/c/f/j, B54, A9).
  - M1a: converts cleanly (385×112 mm, drawn 77×22.5 at 1:5) and has its row; the add() rejection in yesterday's log is not reproducible in the checked-in tool (there is no add() in it) — treated as an intermediate-version artefact. Its size is on the SIZE TO CHECK list (not a tabled panonceau width).
  - Final: 484 built (A 20, AB 9, B 79, C 20, CE 19, D 62, E/EB 13, G 4, H 11, ID 20, J 17, K 54, M 105, S 39, SR 12) + 46 intervene = 530 rows = 530 Cerema files; no `<text>`, no all-white file, 0 failures. SOURCES.md Build section written.
  - Unsure, for Russell: (1) **45 manifest rows say "SIZE TO CHECK"** — the legend-driven series (D/Dv/E/H/SR/KD/KC, the C60–C65 toll signs) have no fixed panel size in the IISR and Cerema drew several at scales other than 1:5 (the D64/D73/D74 motorway panels come out 267–302 mm wide, SR2/SR4/SR50 250–370 mm, the small M10/M11 examples 135–390 mm); they are left at 1:5 with the note rather than guessed. (2) G1–G1c are drawn on a light-grey panel by Cerema (kept); Dp1a/b bodies are grey as drawn. (3) Devices in elevation (K5, K1, K10, K15, KR lamps, J balises) are kept in the pack with a "not a sign face" note — remove if the pack should hold faces only. (4) The dropped hairline twin loses up to 1.8 mm of a panonceau's black border on a few files. (5) Attribution line proposed: "Source : Cerema, licence Etalab 2.0, 2025". (6) `tools/README.md` still has no France entry (not touched this session).
