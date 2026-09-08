---
id: SGN-080
title: Italy national sign pack (Codice della Strada, DPR 495/1992)
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

Researched 2026-09-08; full detail in `Processing/Italy/National (Codice della Strada)/SOURCES.md`.

- **Authority:** D.Lgs. 285/1992 (Codice della Strada, art. 38–45) and D.P.R. 495/1992 (Regolamento di
  esecuzione, Titolo II art. 74–195) with the annexed drawings **Figura II 1 … II 482** (+ /a /b variants,
  ~500 figures), captioned "Figura II n Art. m". Consolidated text on Normattiva (updated 24.02.2025) — text only,
  it links the 1992 Gazzetta PDF for the annex. Later decrees (D.P.R. 610/1996 …) amended figures in later GU
  issues.
- **Artwork, official (downloaded):** Gazzetta Ufficiale n. 303 del 28-12-1992, S.O. n. 134 — the original annex
  with all figures, `Original PDFs (Gazzetta Ufficiale)/GU-1992-12-28-n303-SO134-DPR-495-1992.pdf` (446 pp,
  12.5 MB). It is a **200-dpi bilevel scan** (JBIG2, no text layer): shapes and captions are legible, but it is
  not vector and not traceable to production quality. `FIGURES-OCR.csv` = partial tesseract index (299/482
  base numbers with GU page). **No vector or high-resolution figure set is published by MIT or the Gazzetta**;
  MIT's normativa page links only the text.
- **Licence:** art. 5 L. 633/1941 — "Le disposizioni di questa legge non si applicano ai testi degli atti
  ufficiali dello Stato e delle Amministrazioni pubbliche"; the figures are the annex of a D.P.R., so
  unprotected. gazzettaufficiale.it allows reproduction of the electronic texts with source mention.
- **Fallback:** Wikimedia Commons "Diagrams of road signs of Italy" (20 subcategories; motorway exit 99,
  markings 55, indication 34, motorway 35 …) — redrawn by volunteers, dual PD-ItalyGov / CC BY-SA 3.0. Commercial
  consolidated editions (Legislazione Tecnica "Allegati al Titolo II", Maggioli) and sign-maker catalogues
  (3G Segnaletica) reproduce the figures at print quality but are not downloadable/licensed.
- **Recommended route: drawings/spec only → generate.** Build the ~500 figures from the regolamento's shapes,
  sizes (art. 79–80), colours (Tabella II) and the Alfabeto Normale/Stretto (art. 125), with the GU scan as the
  visual reference and the Commons SVGs as a check, as was done for AS 1743.
- **Russell decides:** whether a first pass may normalise the Commons SVGs (CC BY-SA share-alike → attribution
  and licence notice on the platform) while the generated set is built; whether to buy a consolidated printed
  edition with current figures (Maggioli/Legislazione Tecnica, ~50–100 €) as the reference for post-1992
  changes; the Alfabeto Normale/Stretto font source (free redrawings exist, e.g. on Commons "Technical measures
  and font of road signs").
