# Sources — France (Instruction interministérielle sur la signalisation routière, IISR)

Researched 2026-09-08 (SGN-079); built 2026-09-08, inspected and finished 2026-09-09 — see **Build** at the end.

## The regulation

* **Arrêté du 24 novembre 1967 relatif à la signalisation des routes et des autoroutes** (consolidated on Légifrance,
  https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006075080). Art. 1 delegates the detail to the *Instruction
  interministérielle sur la signalisation routière* (IISR), nine parts taken by joint arrêté (transport + interior).
  The arrêté text on Légifrance names the sign classes and shapes but does not carry the figures; the figures live
  in the IISR parts.
* **IISR, parties 1–9** (1re Généralités; 2e Signalisation de danger; 3e Intersections et régimes de priorité;
  4e Signalisation de prescription; 5e Signalisation d'indication, des services et de repérage; 6e Feux de
  circulation permanents; 7e Marques sur chaussée; 8e Signalisation temporaire; 9e Signalisation dynamique).
  Official value only for the versions published in the JO / Bulletin officiel; the ministry and Cerema publish
  consolidated "versions consolidées" as PDFs.
* Numbering: family letter + number + variant letter — A (danger), AB (intersections/priorité), B (prescription),
  C (indication), CE (services), D (direction), E/EB (localisation, entrée/sortie d'agglomération), G (passages à
  niveau), H (information), J (balises), K/AK/KC/KD (temporaire), M (panonceaux), SR (sécurité routière), plus the
  symbol sets SC, SI, SU/SE and the ideograms ID. Roughly 500 panel types before variants (fr.wikipedia
  "Panneau de signalisation routière en France": A 29, AB 9, B 88, C 55, CE 39, D 56, E 26, EB 2, G 10, H 10,
  J 13, K 35, M 59, SR 5).

## Artwork: `Original SVG (Cerema)/` — official vector, the pack should be built from these

* Cerema (Centre d'études et d'expertise sur les risques, l'environnement, la mobilité et l'aménagement — the
  state agency that edits the IISR consolidations) publishes **"Signaux au format SVG (pour le web)"**,
  https://equipementsdelaroute.cerema.fr/signaux-au-format-svg-a654.html (published 2025-01-16, updated
  2025-01-27), pointing to a Box share https://cerema.app.box.com/v/signauxroutiers (owner "Admin Cerema",
  uploaded by Christophe Damas, Cerema's signalisation lead, October 2023).
* Downloaded 2026-09-08 with `tools/fr_cerema_box.py` (the Box page
  embeds the folder listing as JSON and files download via
  `index.php?rm=box_download_shared_file&shared_name=dwrf655fhaolonqcspo0z0gvb06ms0n7&file_id=f_<id>`).
  `BOX_MANIFEST.csv` lists every file with its Box id. **530 SVGs**, 10 MB:

  | folder | files | folder | files |
  |---|---|---|---|
  | Panneaux_A | 20 | Panneaux_H | 11 |
  | Panneaux_AB | 9 | panneaux_K (temporaire) | 63 |
  | Panneaux_B (Interdiction / Fin_interdiction / Obligation / Fin_obligation …) | 79 | Panonceaux_M (Type_M1 … M12) | 110 |
  | Panneaux_C | 20 | Panneaux_SR | 14 |
  | Panneaux_CE | 20 | Symboles_SC | 17 |
  | Panneaux_D | 72 | Symboles_SI | 15 |
  | Panneaux_E_EB | 22 | Symboles_SU_SE | 9 |
  | Panneaux_G_balises_J | 29 | Ideogrammes_ID | 20 |

* Format: LibreOffice/OpenOffice Draw SVG exports (`xmlns:ooo`), sized in mm (e.g. M1a 76.98 × 22.5 mm — the
  files carry a real size, at 1:10 of a typical panel). 510 of 530 have no live text (legends are paths);
  20 keep `<text>` with fonts Arial, AvantGarde Bk/Md BT and `alphabl1`/`alphabl4` (the L1/L4 road alphabets) —
  those need outlining with the proper alphabet (Caractères L1/L4 are available as free fonts from Cerema/SETRA;
  to check) or re-setting.
* Coverage gaps to check against the IISR: KC/KD (temporary direction) and the D-family variants are present
  as examples; no X (special) or dynamic (9e partie) signs; part 7 markings are not signs.
* **Licence:** the Cerema site states "Sauf mention contraire, tous les contenus de ce site sont sous licence
  etalab-2.0" (Licence Ouverte 2.0, https://github.com/etalab/licence-ouverte/blob/master/LO.md): free reuse,
  commercial included, worldwide, on condition of attribution ("Cerema") and the date of last update. No contrary
  mention appears on the SVG page or in the Box share. The sign designs themselves are set by arrêté (official
  act) and the IISR; the SVG files are Cerema's public-sector information.

## Specs: `Original PDFs (IISR)/`

* The nine IISR parts, versions consolidées at 9 January 2019 (arrêté du 12 décembre 2018, JO 9 janvier 2019),
  from the Maison de la Sécurité Routière du Doubs (a prefecture site, etalab-2.0 footer):
  https://www.msr25.doubs.developpement-durable.gouv.fr/reglementation-en-matiere-de-signalisation-a606.html
  — `iisr_1ere_partie_generalites.pdf` (59 pp), `…2eme…danger` (26), `…3eme…priorite` (45), `…4eme…prescription`
  (42), `…5eme…services_et_de_reperage` (112), `…6eme…feux` (36), `…7eme…marques` (81), `…8eme…temporaire` (54),
  `…9eme…dynamique` (51). Produced with PDFCreator; the sign figures inside are **raster** (pdfimages lists
  125 images in part 2, 188 in part 4), so these PDFs are for dimensions, colours and the sign list, not for
  tracing.
* Newer consolidations exist on Cerema's site (e.g. `IISR_1ePARTIE_VC_20160215_cle2e3a4d.pdf`, 9e partie VC
  2024-03-15 at https://equipementsdelaroute.cerema.fr/IMG/pdf/2025_09_03_iisr_9epartie_vc_20240315_relu_jcb_cle2cdd1b.pdf)
  and later modifying arrêtés on Légifrance; check the latest before finalising sizes.
* Légifrance content is reusable under Licence Ouverte 2.0 (arrêté du 24 juin 2014 on free reuse of DILA's
  legal databases, https://www.legifrance.gouv.fr/contenu/pied-de-page/open-data-et-api).

## Fallbacks (third party, not authoritative)

* Wikimedia Commons "Category:Diagrams of road signs of France" (19 subcategories, e.g. motorway exit 163 files,
  temporary 108 files): redrawings by Commons users (e.g. `France_road_sign_A13a.svg`, author Roulex 45, "own
  work", GFDL / CC BY-SA 3.0). CC BY-SA is share-alike — usable only with attribution and licence notice; not
  needed given the Cerema set.

## Recommended route

Official vector artwork → convert: normalise the 530 Cerema SVGs (strip OOo wrappers, outline the 20 with live
text, set real sizes from the IISR parts), family folders by letter, MANIFEST.csv. Same route as the UK pack.

## Build (2026-09-08/09, `tools/fr_cerema.py`)

* **Input:** the 530 Cerema SVGs (LibreOffice Draw exports, 0.01 mm units). Every filled shape is kept exactly;
  LibreOffice's hairline twin round each fill is dropped (it loses at most the outer half of a 0.36 mm page stroke,
  1.8 mm real, on a few panonceau borders); genuine stroked line-work is outlined with Inkscape so the output is
  fills only; closed unfilled outlines that sit on unpainted page (panonceau bodies, balise bodies) get a white fill
  after sampling a rasterisation of the source, inset clear of the outline's own stroke. White paint that touches
  nothing else (invisible on the white page: a stray pointer in KR41, a guide line that stretched KS1) and strokes
  under 0.03 mm (J16's hatched head, 320 of them) are not carried. The one gradient (J14a) is flattened, the one raster
  (K14) dropped, fill-opacity ignored. No `<text>` survives: strings in the L1/L4 road alphabets send the file to
  intervene/ (no licensed digitisation of Caractères L1/L4 exists); Arial/AvantGarde strings are the drawings' own
  annotations and are dropped. Names: `NAMES.csv` (IISR text and the Wikipedia lists; eleven rows fixed by hand on
  2026-09-09 where the IISR parse had taken a size or half a sentence — KD43a/b, KD69a/b, M6a/b/c/f/j, B54, A9).
* **Scale:** 1:5 for the fixed-size series, verified on the gamme normale (A triangle 190 → 950×824 with rounded
  corners, B disc 170 → 850, AB4 octagon 160 → 800, C square 140 → 700, M9z 180×100 → 900×500) and on the header
  arithmetic of eleven files across the series. Exceptions set from IISR sizes: K5 devices 1:10 (8e partie heights),
  AB5 1:10 (its triangle is half of AB3b's), G1/G1a/G1b/G1c 1:10 (2e partie: 1150×750, 1150×950, 750×1150, 750×1550),
  KD69a and KD43a_ex2 1:10 (8e partie: 1000×400, 1300×400), M9zex1cdr 1:10 and M11b_ex1_dc/ex2_dc 1:15 (they give the
  tabled 700×200 panonceau). The legend-driven series (D, Dv, Dc, Dp, E, H, SR, KD, KC, C60–C65) have no fixed panel
  size in the IISR; their manifest rows say the size is Cerema's example at 1:5, and **45 rows carry "SIZE TO CHECK"**
  where the letter heights or an IISR size show the file cannot be 1:5 but the scale is not certain: D64, D73, D74a/b
  (motorway panels with 50–80 mm legends at 1:5), Dv44, SR2a/b/c, SR3_18_12/24_16/36_24 (the suffix reads as a size),
  SR4_ex1_dc/ex2_dc, SR50_ex1/ex2, M1a, M2_ex4, M10a_ex1/ex2, M10b, M10c1/2/3, M11a, M11b_ex2, E53c_ex2, E_46_dc and the
  remaining KD/KC1 files. Header as the other packs: viewBox in pt at 1 pt = 1 cm, width/height in mm at 72 pt/in.
* **Output:** `SVGs/<family>/<NAME>_<CODE>.svg`, **484 signs** + `SVGs/MANIFEST.csv` (530 rows, one per Cerema file):
  A Danger 20, AB Intersections et priorité 9, B Prescription 79, C Indication 20, CE Services 19, D Direction 62,
  E/EB Localisation 13, G Passages à niveau 4, H Information touristique 11, ID Idéogrammes 20, J Balises 17,
  K Temporaire 54, M Panonceaux 105, S Symboles (SC/SI/SU/SE) 39, SR Sécurité routière 12. Cerema file names mapped to
  IISR codes: `auou.svg` = A13a, `KX50` = KXC50. Devices the catalogue draws in elevation (K5a/b/c/d, K1, K10, K15,
  K2_ex2, KR1/KR2/KR11/KR41, J1/J3/J7/J10/J11/J12/J13/J16) are kept with the note "device drawn in elevation, not a
  sign face". G1–G1c are drawn on a light-grey panel by Cerema (kept as drawn); KD44a/b_ex2 have a pale-yellow ground
  as drawn.
* **`SVGs/intervene/` — 46 files, each with the reason in its manifest row:**
  live L1/L4 text (9): SC8_19, Dc29_ex2_dc, Dc43_ex2_dc, Dp1a, Dp1b, Dv61_ex1, Dv61_ex2, E52b_ex2, (K14 also has a raster);
  dimensioned drawings (4): E52c_ex1, E52c_ex2, SU1, SU3;
  several drawings on one sheet (14): G2, G3, KM, SR2, SR4, K2_ex1, K8, KC1_ex2, KD9_ex4, KR42, KR43, M3a1, M3a2, M3b1, M3b2;
  front-and-side borne drawings (5): E52a_ex3, E53a_ex2, E53b_ex2, E54a_ex, E54b_ex2; assemblies (10): EB10, M8ad,
  Dc29_ex1, Dc29_ex2, Dc43_ex1, Dc43_ex2 (signposts on their post), G1_bis, G1a_bis, G1b_bis, G1c_bis (cross with its
  R24 light and bell); perspective illustrations (3): J15a, J15b, K16; raster (1): K14.
* **Attribution (Licence Ouverte 2.0 asks for the source and the date of last update):** proposed platform line
  "Source : Cerema, licence Etalab 2.0, 2025" (Cerema's SVG page: published 2025-01-16, updated 2025-01-27; the Box
  files date from October 2023). Russell decides the wording.
* **Not done / to decide:** the 45 SIZE TO CHECK scales (needs the IISR 5e/8e partie figures read sign by sign, or
  Cerema asked what page scale the direction-sign examples use); the KC/KD temporary-direction and 9e partie dynamic
  signs missing from the Cerema set; the L1/L4 alphabets for the 9 text files; `tools/README.md` has no France entry
  yet.
