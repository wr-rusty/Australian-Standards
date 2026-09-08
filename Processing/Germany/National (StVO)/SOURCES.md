# Sources — Germany (StVO Anlagen 1–4, Verkehrszeichenkatalog VzKat 2017)

Researched 2026-09-08 (SGN-078). First build from the free vector sets the same day (see **Build** at the end).

## The regulation

* **Straßenverkehrs-Ordnung (StVO)** § 39–43 and Anlage 1 (Gefahrzeichen, zu § 40), Anlage 2 (Vorschriftzeichen,
  zu § 41), Anlage 3 (Richtzeichen, zu § 42), Anlage 4 (Verkehrseinrichtungen, zu § 43) — the legally binding
  sign images with their Zeichen numbers (101 …, 201 …, 301 …, 600 …), https://www.gesetze-im-internet.de/stvo_2013/.
* **Verkehrszeichenkatalog (VzKat 2017)** — Anlagen 1–8 of the VwV-StVO (Allgemeine Verwaltungsvorschrift zur
  StVO, 26.01.2011 i.d.F. 22.05.2017, kept current through the VwV-StVO amendments of 2020, 2021, 2024, latest
  10.04.2025, BAnz AT 09.04.2025 B2). It is the complete official catalogue including every numbered variant
  (`101-10` Flugbetrieb rechts, `108-4` Gefälle 4 % …) and the Zusatzzeichen 1000–1060. Maintained for the BMDV by
  the **Bundesanstalt für Straßenwesen (BASt)**, Referat V1 (Ref-V1@bast.de). Browsable at https://www.vzkat.de/
  (Teile 1–7 + Anhang, "Stand 10.04.2025"); FGSV Verlag sells it as R 070 inside the FGSV WebReader (no vector
  files there).
* Numbering: `Zeichen NNN` (three digits, class by hundreds), `NNN-VV` for variants (10–19 right, 20–29 left,
  50–59 special legends), `NNN.N` for later insertions (244.3, 277.1, 350.1), Zusatzzeichen 1000–1060 with
  two-digit suffixes (1010-68 …). `Original JPG (BASt)/bezeichnung-der-vz.pdf` (37 pp, Stand November 2021) is
  the official "Liste der amtlichen Bezeichnungen": **1,161 numbered entries**.
* Guide signs: the sign faces themselves (Zeichen 401–460 Wegweiser, 415–453) are in the VzKat; the design rules
  for composing them are the **RWB 2000** (Richtlinien für die wegweisende Beschilderung außerhalb von Autobahnen,
  ARS 27/1999) and **RWBA 2000** (… auf Autobahnen, ARS 26/2000), and RTB for tourist signing — FGSV publications,
  copyright FGSV, paid (https://www.fgsv-verlag.de/rwb-2000). Their pictograms are free from BASt (below).
  Legend font: DIN 1451 Teil 2 Mittelschrift/Engschrift (glyph data on the BASt data stick, and as fonts).

## Official artwork

### `Original JPG (BASt)/` — complete VzKat 2017, raster

* BASt "Verkehrszeichenkatalog 2017 — Download",
  https://www.bast.de/DE/Themen/Sicherheit/HF_2/Massnahmen/verkehrszeichen/vz-download.html: six ZIPs
  (`100-199.zip`, `200-299.zip`, `300-499.zip`, `500-599.zip`, `600-720.zip`, `1000-1099.zip`, 919 MB), **670
  JPGs** ("von jedem Zeichen ist mindestens eine Variante enthalten"), 300 dpi at 1:10 of the standard size
  (e.g. 101-10 = 998 × 878 px), dated 2017-11, in colour. Downloaded 2026-09-08.
* Changes 1992 → 2017 (withdrawn/altered signs) are shown inline on
  https://www.bast.de/DE/Themen/Sicherheit/Daten/V1-VzKat-Aenderungen-1992-2017.html (lightbox JPGs, no ZIP).

### `Original Vector (BASt, post-2017)/` — official vector for the new signs, pictograms and symbols

* `Vz2017/` — 51 ZIPs from "Neue Verkehrszeichen nach der Einführung des Verkehrszeichenkatalogs 2017",
  https://www.bast.de/DE/Themen/Sicherheit/HF_2/Massnahmen/verkehrszeichen/unterseiten/Neue-Vz-nach-2017.html:
  every sign added by the StVO amendments 2020/2024 (230 Ladebereich, 244.3/244.4, 257-59, 277.1/281.1, 311.1,
  314-31, 342 Haifischzähne, 350.1/350.2, 365-69…71, 442-14…33, 448, 455.1, 460, 721, Zusatzzeichen 1006-32,
  1010-68…72, 1012-54…57, 1022-16/17, 1024-21/22, 1040-37, 1050-31, 1053-54…57, 1060-34, Sinnbilder Lastenfahrrad,
  Wohnmobil, E-Kleinstfahrzeug, Carsharing, Plaketten/Aufkleber). Each ZIP holds `.DVK` + `.dxf` + `.eps` per
  variant (166 of each) plus JPG/WMF; the EPS are DV-Vision exports (Adobe Illustrator 3 prolog, colour, freely
  scalable).
* `VLT 2021/` — 31 ZIPs, the Verkehrslenkungstafeln introduced with VwV-StVO 2021 (501, 511–514, 527–529, 531,
  533-2/-6, 538, 541, 542, 550, 551), same formats.
* `Sinnbilder und Symbole/` — 65 ZIPs (`.dvk` + `.eps` (+ `.gif`/`.dxf`)): Sinnbilder StVO § 39 Abs. 7 (15,
  vehicle classes) and Abs. 8 (9), **RWB 2000 symbols** (18: Informationsstelle, Parkplatz, Bahnhof, Flughafen,
  Hafen, Autohof …) and **RWBA 2000 symbols** (23: Tankstelle, Gasthaus, Motel, Notrufsäule, Autobahnkreuz …),
  from https://www.bast.de/DE/Themen/Sicherheit/HF_2/Massnahmen/verkehrszeichen/sinnbilder-symbole.html and its
  sub-pages. Abs. 10 and RTB pages list symbols without downloads.
* `Musterdateien/` — `dvkaz.zip` (6 sample signs in the DVKAZ format + `STVOKAZ-Beschreibung.pdf`, the format
  description), `eps.zip`, `dxf.zip` from https://www.bast.de/DE/Themen/Sicherheit/HF_2/Massnahmen/verkehrszeichen/vz-daten.html.

### The complete vector set — paid, from BASt

* "Die vollständigen digitalen Daten der Verkehrszeichen können bei der BASt gegen Entgelt bezogen werden":
  a USB stick with **all valid signs in DVKAZ format (circa 1,000 Verkehrszeichen und Symbole, resolution
  1/10,000 mm)** plus the DIN 1451 Teil 2 glyphs and the Windows converter **DV-Vision** that writes EPS Level 2
  (with colours, freely scalable; Illustrator on Mac reads them) or DXF (no colours, curves flattened).
  **Price: 250 € + 19 % MwSt (297.50 €)**, "nur komplett inklusive Konvertierungsprogramm", order by signed PDF
  form to Ref-V1@bast.de or fax +49 2204 43-4150
  (https://www.bast.de/DE/Themen/Sicherheit/HF_2/Massnahmen/verkehrszeichen/unterseiten/Bestellung/vz-bestellung_node.html).
  No further licence terms ("weitergehende Zusatzvereinbarungen … können nicht anerkannt werden"). The converter
  is Windows-only; the free `Musterdateien` are there to test the workflow first.

## Licence

* BASt on every download page: **"Verkehrszeichen unterliegen keinem Urheberrechtsschutz."** The sign images are
  part of the StVO Anlagen (a Verordnung) and the VwV-StVO/VzKat (amtlicher Erlass), so § 5 Abs. 1 UrhG applies:
  "Gesetze, Verordnungen, amtliche Erlasse und Bekanntmachungen … genießen keinen urheberrechtlichen Schutz."
  § 5 Abs. 2 (other official works) would at most add the change-prohibition/source rules of §§ 62–63. Free for
  commercial use; no attribution required by law (we will cite BASt/BMDV anyway).
* The paid DVKAZ stick is sold without extra licence terms; the data are the same public-domain sign images.
  RWB/RWBA/RTB documents (FGSV) are copyrighted — do not copy the documents; the pictograms are official and
  provided free by BASt.
* Commons tags German sign SVGs `PD-VzKat` (current) / `PD-Vz historisch`.

## Fallbacks (third party, not authoritative)

* Wikimedia Commons "Category:Diagrams of road signs of Germany" (249 files, 34 subcategories; the SVG set
  covers the whole VzKat with variants): volunteer redrawings, public domain under § 5 UrhG (`PD-VzKat`).
  Clean and complete, but not the official geometry.
* verkehrszeichen-online.org and sign-maker PDF catalogues (wolkdirekt.com) reproduce the catalogue.

## Recommended route

Official vector artwork → convert, in two steps: (1) build now from the free BASt EPS (Vz2017 + VLT 2021 +
Sinnbilder/RWB/RWBA symbols) with the UK EPS pipeline, and the 670 JPGs only as a visual check; (2) buy the
BASt data stick (297.50 €) and convert the ~1,000 DVKAZ signs to EPS with DV-Vision (needs a Windows VM), then
run the same pipeline over the whole catalogue. If Russell does not want to buy, the alternative for the
pre-2017 signs is "drawings/spec only → generate" from the VzKat sizes plus the JPGs, or the Commons SVGs.

## Build (2026-09-08, `tools/de_bast.py`)

* **Input:** every EPS of the free BASt vector sets, unzipped beside their ZIPs in `Original Vector (BASt, post-2017)/`
  (the ZIPs are kept): Vz2017 69 EPS, VLT 2021 102, Sinnbilder und Symbole 65, Musterdateien 6 = 242 files, 232
  distinct by content (the pictogram sets ship ten symbols twice — Flughafen, Information, Bus, Lkw/Pkw mit Anhänger,
  Erste Hilfe, Polizei, Parkplatz, Autohof — and **551-27.eps and 551-28.eps are byte-identical**, so 551-28 is not
  built; its manifest row says so). The `442.zip`, `455.1.zip`, `460.zip` and the unprefixed VLT ZIPs hold only
  thumbnail JPGs. 219 EPS are DV-Vision exports of the DVKAZ files, 23 are CorelDRAW 2020/X7 exports (230 series,
  1006-32, 1012-55…57, 1024-22, 1040-37, 1050-31, 1053-55…57, 1060-34, 257-59, 311.1, 342, 448, Plakette).
* **Scale — every EPS is at 1:1, 1 pt = 25.4/72 mm.** Evidence: the DVKAZ format (`STVOKAZ-Beschreibung.pdf`) states
  all lengths in cm and each DVK's DA 11 record gives the extent; the EPS BoundingBox is that extent × 28.35 pt/cm
  (60 cm = 1702 pt on 150 of 160 files with a DVK; the VLT DVKs 511-28, 513-14 … carry a stale 125 cm extent while
  their EPS is 160 cm, and so-22 (Gespannfuhrwerk) says 230 × 200 cm for a 39 × 20 cm drawing — the EPS is trusted).
  Verified on signs of known VzKat size after conversion: Z 101 (Regelgröße 900 mm triangle, 40 mm corner radius)
  → 841.4 × 739.4 mm; Z 264-2.3 (600 mm disc) → 600.0 mm; Z 230 (600 × 900 mm) → 600 × 900; Z 1010-71 Zusatzzeichen
  → 600 × 330; VLT 501-19 → 1600 × 1600. Sizes are therefore whatever BASt drew (Größe 2 where a size series exists),
  one size per sign; the manifest records the DVK extent per sign.
* **Pipeline:** `uk_eps.py` functions — Ghostscript EPS → PDF, fills lifted exactly, `write_svg` header convention.
  No live text and no artboard rectangles in these files (DV-Vision draws the sign's own white face/border as the
  first fill). Strokes: the CorelDRAW files carry a 0.03 pt hairline on the outer fill (ignored, below the 0.3 pt
  threshold); Z 342 Haifischzähne has fourteen 1 pt strokes, outlined with Inkscape. Z 342 is the catalogue's
  plan illustration of the marking on a grey carriageway, not a sign face (noted in the manifest). The Carsharing
  Plakette EPS embeds three raster images (hologram) that are not carried. Colours are the EPS values (black
  #231f20, red #ed1c24, blue #0066b3 / #0067b4 Corel, yellow #fff200, orange #f7941d, green #009856, grey #828487).
* **Names:** `bezeichnung-der-vz.pdf` (1,161 entries, parsed into `REGISTER.csv`); codes not in that list (264-2.3,
  the pictograms) use the DVK's `Bezeichnung:` comment (older DVKs are DOS cp850, newer latin1); three fixed by hand
  (Plakette has no DVK, the Notrufsäule DVK says "Fernsprecher", the eKF DVK has a typo). Pictogram codes are
  `SB-<BASt file name>` (StVO § 39 Sinnbilder), `RWB-…`, `RWBA-…`, `AUFKLEBER-…`, `PLAKETTE-…`. RWB/RWBA symbols
  come on their white 150 × 150 mm symbol field (kept, as drawn); the § 39 Abs. 7/8 Sinnbilder are bare black shapes.
* **Output:** `SVGs/<family>/<NAME>_<CODE>.svg`, 232 files + `SVGs/MANIFEST.csv`: Gefahrzeichen 1 (Z 101 sample),
  Vorschriftzeichen 13, Richtzeichen 130 (incl. the 102 VLT 501–551 and the 442/455.1/460 Kreisverkehr sets),
  Verkehrseinrichtungen 2 (605-11 sample, 721), Zusatzzeichen 22, Sinnbilder und Symbole 64. Families follow the
  Zeichen number ranges (720/721 "Sonstige Zeichen" sit with the Verkehrseinrichtungen).
* **Gap (`REGISTER.csv`, one row per listed Zeichen + 74 extra rows for vector-only pictograms and JPG-only
  Unternummern):** of the 1,161 listed entries 165 have official vector (built), 644 have only the 1:10 JPG, 352 have
  neither (only a name). Per family — Gefahrzeichen 117 listed: 1 vector / 102 JPG only / 14 neither;
  Vorschriftzeichen 172: 12 / 133 / 27; Richtzeichen 527: 130 / 201 / 196; Verkehrseinrichtungen 95: 2 / 20 / 73;
  Zusatzzeichen 250: 20 / 188 / 42. The 996 unbuilt entries need either the BASt stick (DVKAZ → DV-Vision EPS →
  this tool unchanged) or generation from the VzKat sizes with the JPGs as reference; the 352 "neither" entries are
  mostly percentage/number series (108-4…, 274-5…, 1004-…) and lane-count variants that the JPG set shows once.
