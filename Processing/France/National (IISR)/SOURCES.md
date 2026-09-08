# Sources — France (Instruction interministérielle sur la signalisation routière, IISR)

Researched 2026-09-08 (SGN-079). Nothing built yet.

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
