# Sources — Italy (Codice della Strada, D.Lgs. 285/1992; Regolamento di esecuzione, D.P.R. 495/1992)

Researched 2026-09-08 (SGN-080). Nothing built yet.

## The regulation

* **D.Lgs. 30 aprile 1992, n. 285 (Nuovo codice della strada)**, art. 38–45 on signals; art. 39 (segnali
  verticali) delegates shapes, colours, sizes and figures to the regulation.
* **D.P.R. 16 dicembre 1992, n. 495 (Regolamento di esecuzione e di attuazione del nuovo codice della strada)**,
  Titolo II, art. 74–195; the sign drawings are the annexed **Figure II 1 … II 482** (plus /a /b … variants),
  each captioned "Figura II n Art. m" with name and meaning. Later amendments (D.P.R. 610/1996 and later
  decrees) replaced or added figures; the consolidated text is on Normattiva
  (https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1992-12-16;495!vig=, updated
  2025-02-24) but Normattiva shows only the text and links the original Gazzetta PDF for the annex.
* Classes: pericolo (triangles), precedenza, divieto, obbligo, indicazione (urban white, extra-urban blue,
  motorway green, tourist brown), servizi, complementari, temporanei (yellow), pannelli integrativi (Modelli).
  Fonts: Alfabeto Normale / Alfabeto Stretto (art. 125 of the regolamento).

## Official artwork: `Original PDFs (Gazzetta Ufficiale)/`

* `GU-1992-12-28-n303-SO134-DPR-495-1992.pdf` — Gazzetta Ufficiale, Serie Generale n. 303 del 28-12-1992,
  Supplemento Ordinario n. 134, from https://www.gazzettaufficiale.it/eli/gu/1992/12/28/303/so/134/sg/pdf
  (Istituto Poligrafico e Zecca dello Stato), 12.5 MB, 446 pages A4. It is the **original 1992 annex with all
  figures**, but it is a **bilevel scan at 200 dpi** (JBIG2, "copia tratta da Guritel — Gazzetta Ufficiale
  on-line", no text layer): black-and-white halftones, roughly 800 px per sign. Good enough to read shapes,
  captions and numbers, not to trace. Figures amended after 1992 are in later GU issues, not in this file.
* MIT's normativa page for the decree (https://www.mit.gov.it/normativa/decreto-del-presidente-della-repubblica-numero-495-del-16121992)
  links only the text. No ministry download of the figures as vector or high-resolution images was found;
  MIT publishes DWG/DXF only for temporary-works schemes (D.I. 22 gennaio 2019) and similar guides.
* Colour and dimension tables are in the regolamento text (art. 79–80 sizes, art. 78 colours: Tabella II 1 …).

## Licence

* Art. 5 L. 22 aprile 1941 n. 633: "Le disposizioni di questa legge non si applicano ai testi degli atti
  ufficiali dello Stato e delle Amministrazioni pubbliche, sia italiane che straniere." The figures are an
  integral annex of a D.P.R. published in the Gazzetta, so they are not protected; gazzettaufficiale.it's own
  note allows reproduction of the electronic texts with mention of the source and of their non-authentic
  nature. Commons tags the Italian signs both PD-ItalyGov ("part of a text of official act published … by the
  Italian State") and CC BY-SA for the redrawing.

## Fallbacks (third party, not authoritative)

* Wikimedia Commons "Category:Diagrams of road signs of Italy" (20 subcategories: motorway exit 99 files,
  markings 55, indication 34, motorway 35, luminous 29, historic 30 …), e.g.
  `Italian_traffic_signs_-_dare_precedenza.svg` (author "F l a n k e r", traced from codicestradainfantillo.it;
  dual PD-ItalyGov / CC BY-SA 3.0). Comprehensive and clean, but redrawn by volunteers.
* Commercial consolidated editions with the figures (Maggioli, Legislazione Tecnica "Allegati al Titolo II" —
  https://legislazionetecnica.it/bcksistemone/files/regulations/pdf/DPR4951992_P02.pdf, returns 403 to scripts)
  and sign-maker catalogues (3G Segnaletica) reproduce the figures at print quality; their layout/edition is
  theirs, the figures are the State's.

## Recommended route

Drawings/spec only → **generate**: no official vector exists. Build the figures from the regolamento's shapes,
sizes, colours and the Alfabeto Normale/Stretto (art. 125), using the GU scan as the visual reference and the
Commons SVGs as a check (or, if Russell accepts third-party redrawings for a first pass, normalise the Commons
set under its CC BY-SA terms and replace progressively). Budget: ~500 figures with variants (II 1 – II 482 plus 48+ /a /b variants).
`Original PDFs (Gazzetta Ufficiale)/FIGURES-OCR.csv` is a tesseract pass over the scan (150 dpi, Italian):
322 caption hits, 299 of the 482 base numbers read, with the GU PDF page for each — a partial index, to be
completed by hand or from the Normattiva text (which lists every "Fig. II n" in the articles).
