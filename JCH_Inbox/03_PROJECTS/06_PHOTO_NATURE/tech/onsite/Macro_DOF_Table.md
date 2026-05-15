# Macro DOF Table

**Created:** 2026-03-14 06:45  
**Updated:** 2026-03-14 07:09  
**Messages:** 17

---

## Human
*2026-03-14 06:45*

I need you to generate a table showing the value of depth of field (in micron and mm) when using a canon 100mm macro lens at different magnifcation. Create a standardtable that will be used for all the lenses that I have in macro photography : Venus Laowa 24mm f/14 2x Macro Probe and Laowa 25mm F2.8 2.5-5x Ultra Macro

---

## Assistant
*2026-03-14 06:45*

Je calcule une table normalisée de profondeur de champ par grandissement, de façon réutilisable pour vos trois optiques macro. Je vais m’appuyer sur une formule cohérente et préciser les hypothèses, car la valeur change selon l’ouverture et le cercle de confusion choisi.

---

## Assistant
*2026-03-14 06:48*

Here is a normalized macro depth-of-field reference table for your Canon APS-C bodies such as the R10 or 90D, using Canon’s APS-C circle of confusion value of 0.019 mm. I assumed your Canon 100mm macro is a 1:1 model; Canon lists 1x maximum magnification for the EF 100mm Macro, Laowa lists 2x for the 24mm f/14 Probe, and 2.5x to 5x for the 25mm Ultra Macro. The calculation used is the standard close-up approximation: **DOF ≈ 2 × N × c × (1 + m) / m²**, where **N** is the f-number, **c** the circle of confusion, and **m** the magnification. Under this approximation, one standard table can serve all three lenses because DOF depends mainly on aperture and magnification; the lens mainly determines which magnification rows are available. Photopills notes that pupil magnification can make some long-focal-length macro lenses deviate slightly from this simplified model. citeturn379094search1turn984420search4turn984420search1turn984420search2turn355228search0turn355228search6

| Magnification | f/2.8 | f/4 | f/5.6 | f/8 | f/11 | f/14 | f/16 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.25x | 2128 µm / 2.128 mm | 3040 µm / 3.040 mm | 4256 µm / 4.256 mm | 6080 µm / 6.080 mm | 8360 µm / 8.360 mm | 10640 µm / 10.640 mm | 12160 µm / 12.160 mm |
| 0.50x | 638 µm / 0.638 mm | 912 µm / 0.912 mm | 1277 µm / 1.277 mm | 1824 µm / 1.824 mm | 2508 µm / 2.508 mm | 3192 µm / 3.192 mm | 3648 µm / 3.648 mm |
| 0.75x | 331 µm / 0.331 mm | 473 µm / 0.473 mm | 662 µm / 0.662 mm | 946 µm / 0.946 mm | 1300 µm / 1.300 mm | 1655 µm / 1.655 mm | 1892 µm / 1.892 mm |
| 1.0x | 213 µm / 0.213 mm | 304 µm / 0.304 mm | 426 µm / 0.426 mm | 608 µm / 0.608 mm | 836 µm / 0.836 mm | 1064 µm / 1.064 mm | 1216 µm / 1.216 mm |
| 1.5x | 118 µm / 0.118 mm | 169 µm / 0.169 mm | 236 µm / 0.236 mm | 338 µm / 0.338 mm | 464 µm / 0.464 mm | 591 µm / 0.591 mm | 676 µm / 0.676 mm |
| 2.0x | 80 µm / 0.080 mm | 114 µm / 0.114 mm | 160 µm / 0.160 mm | 228 µm / 0.228 mm | 314 µm / 0.314 mm | 399 µm / 0.399 mm | 456 µm / 0.456 mm |
| 2.5x | 60 µm / 0.060 mm | 85 µm / 0.085 mm | 119 µm / 0.119 mm | 170 µm / 0.170 mm | 234 µm / 0.234 mm | 298 µm / 0.298 mm | 340 µm / 0.340 mm |
| 3.0x | 47 µm / 0.047 mm | 68 µm / 0.068 mm | 95 µm / 0.095 mm | 135 µm / 0.135 mm | 186 µm / 0.186 mm | 236 µm / 0.236 mm | 270 µm / 0.270 mm |
| 4.0x | 33 µm / 0.033 mm | 48 µm / 0.048 mm | 66 µm / 0.067 mm | 95 µm / 0.095 mm | 131 µm / 0.131 mm | 166 µm / 0.166 mm | 190 µm / 0.190 mm |
| 5.0x | 26 µm / 0.026 mm | 36 µm / 0.036 mm | 51 µm / 0.051 mm | 73 µm / 0.073 mm | 100 µm / 0.100 mm | 128 µm / 0.128 mm | 146 µm / 0.146 mm |

Use the table like this: for the Canon 100mm macro, the most relevant rows are **0.25x to 1.0x**; for the Laowa 24mm Probe, **0.5x to 2.0x**; for the Laowa 25mm Ultra Macro, **2.5x to 5.0x**. citeturn984420search4turn984420search1turn984420search2

One practical note: this is a **geometric DOF table**, so for critical focus stacking you would usually choose a step size smaller than the listed DOF, not equal to it. Generated at 07:48, Brussels time.

I can also turn this into a clean printable A4 reference sheet.

---

## Human
*2026-03-14 06:51*

Ok for a  sheet could you add a column to determine value in mucron of steps to use in focus stacking mode ?

---

## Assistant
*2026-03-14 06:51*

Le pas de stacking dépend aussi de l’ouverture, donc une seule colonne universelle serait trompeuse. Je vais vous donner une version de feuille propre avec une règle standard de calcul du pas et, pour qu’elle soit utilisable sur le terrain, une table de pas recommandés directement dérivés de la DOF.

---

## Assistant
*2026-03-14 06:52*

Je transforme cela en fiche A4 imprimable, avec une colonne pratique pour le pas de stacking. Je vais utiliser une règle conservatrice adaptée au macro stacking de terrain.

---

## Assistant
*2026-03-14 06:57*

Done.

I added a dedicated focus-stacking step table in microns, based on a conservative rule of 50% of the calculated DOF, which is the safest general-purpose setting for macro work.

Files:
[Printable PDF sheet](sandbox:/mnt/data/rendered_macro_sheet/macro_dof_focus_stacking_sheet.pdf)
[Editable DOCX sheet](sandbox:/mnt/data/macro_dof_focus_stacking_sheet.docx)

Time: 07:57

For very flat subjects you can usually increase the step to about 60-70% of DOF. For difficult 3D subjects, reflective insects, or critical high-resolution stacks, reducing to 30-40% is safer.

---

## Human
*2026-03-14 06:58*

In your competence in photography and computing, do you have suggestions to enhance the table information or/and simplication , by ex use on ly micron to gain place

---

## Assistant
*2026-03-14 06:58*

Je vais vous proposer une version plus “terrain”, plus compacte et plus lisible, sans refaire tout le document pour l’instant. Le vrai gain vient surtout de la hiérarchisation: mettre le pas de stacking au centre, et reléguer la DOF au second plan.

---

## Assistant
*2026-03-14 06:58*

Yes. The table can be improved quite a lot, and your idea of using only microns is one of the best simplifications.

My recommendation would be this:

Use only µm in the table body. In macro stacking, the working unit is usually the micron, and switching between µm and mm adds visual clutter. A value like 0.314 mm is immediately clearer as 314 µm when you are setting rail steps.

Make the stacking step the primary value, not the DOF. In practice, when shooting, you mostly need:
magnification → aperture → recommended step.
The DOF is useful, but secondary. So the best compact table is often:
Magnification | f/4 | f/5.6 | f/8 | f/11 | f/16
with each cell showing the recommended step in µm, and optionally the DOF in smaller text or in brackets.

Round values. Exact numbers look scientific, but they slow reading. For field use, rounded values are better:
below 100 µm: round to nearest 5 µm
100–500 µm: round to nearest 10 µm
above 500 µm: round to nearest 25 or 50 µm
This makes the sheet much faster to use.

Reduce the number of aperture columns. For a practical sheet, you do not need every aperture. A very efficient set would be:
f/4, f/5.6, f/8, f/11, f/16
You can drop f/2.8 unless you really use it often for the 100 mm or the Laowa 25 mm. You may also keep f/14 only in a lens-specific appendix for the Probe lens.

Separate the table into two versions:
a “field sheet” with only recommended step in µm,
and a “reference sheet” with DOF + step.
That is usually the best compromise between speed and completeness.

Group the magnification rows by lens usability. For example:
Canon 100 mm macro: 0.25x, 0.5x, 0.75x, 1x
Laowa Probe: 0.5x, 1x, 1.5x, 2x
Laowa 25 mm Ultra Macro: 2.5x, 3x, 4x, 5x
This avoids scanning useless rows.

Use one fixed rule for step size and print it in the header. For example:
Recommended step = 50% of DOF
Then every number in the table has an immediate logic. You can also add a small note:
Flat subject: 60–70% of DOF
General subject: 50% of DOF
Difficult 3D insect subject: 30–40% of DOF

A very compact layout would be this:

Lens / Range | Magnification | f/4 | f/5.6 | f/8 | f/11 | f/16
and in each cell only one value, for example:
114
160
228
314
456

meaning recommended step in µm.

Then, at the bottom:
All values in µm.
Step rule = 50% of calculated DOF.
APS-C CoC = 0.019 mm.

That would probably be the most efficient version.

My judgment is:
for real use, the best simplification is:
1. only µm
2. only recommended step in cells
3. DOF moved to a note or a second sheet
4. rounded values
5. reduced aperture columns

So yes, using only microns is not just a way to save space; it is actually the better operational format.

Time: 08:01

I can now rebuild the sheet in a much cleaner “field version” with this compact logic.

---

## Human
*2026-03-14 07:00*

Ok field version

---

## Assistant
*2026-03-14 07:01*

I’m rebuilding it as a compact field sheet: microns only, stacking step as the main value, and fewer aperture columns so it is faster to read at the rail.

---

## Assistant
*2026-03-14 07:01*

I have the compact structure now: one landscape A4 page, one unit only (µm), and the table centered on the usable setting in the field — the rail step, not the theoretical DOF.

---

## Assistant
*2026-03-14 07:05*

Done.

Files:
[Field sheet PDF](sandbox:/mnt/data/macro_field_render/macro_field_sheet.pdf)
[Field sheet DOCX](sandbox:/mnt/data/macro_field_sheet.docx)

I simplified it to the operational format:
all values in µm, reduced aperture set, and recommended stacking step as the main information.

Time: 08:04

A next refinement that could be useful would be a second ultra-compact version with only the magnifications you actually use most often on each lens.

---

## Human
*2026-03-14 07:08*

Which font did you use ?

---

## Assistant
*2026-03-14 07:08*

I’m checking the generated file directly so I can tell you the actual font used rather than guessing from the template.

---

## Assistant
*2026-03-14 07:08*

The generated sheet uses **Aptos**.

More precisely:
- **Title, subtitle, and table text:** Aptos
- The DOCX theme still contains older Office theme defaults like **Calibri/Cambria**, but the actual visible text in the document is explicitly set to **Aptos**

On a Mac, if Aptos is not available in the app you use, it may be substituted automatically by another sans-serif font.

Time: 08:06

---
