---
date: 2026-11-16
source: dobby
domain: arteon
type: synthèse
status: actif
lang: fr
corpus: 7 transcripts NoteGPT Lightroom (00_INBOX) + 3 livrables sous-agents
---

# Synthèse — Enrichissement de la proposition XMP/plugin animalier WildLens/ARTEON

> Dobby 🦉 — 2026-11-16 · Lecture des 7 transcripts Lightroom + confrontation à la proposition actuelle
> (pack « Naturaliste » 36 XMP, curseur proportionnel 3 piliers, brique 3 masques IA, brique 4 `/recommend`).
> Convention `[ÉTABLI]` = technique standard vérifiable · `[AFFIRMÉ]` = opinion d'auteur · `[NON PROUVÉ]` = plausible sans preuve.

---

## 0. Le corpus et sa pertinence

| # | Transcript | Auteur | Domaine | Pertinence pour nous |
|---|-----------|--------|---------|----------------------|
| 1 | Masking Tricks and Hacks | **Simon d'Entremont** (animalier CA) | Masquage | 🔴 directe — brique 3 |
| 2 | Masking Finally Made Easy | **Steve Perry** (Backcountry) | Masquage | 🔴 directe — brique 3 |
| 3 | Stupid Trick Color Grades | créateur solo | Grading | 🟡 pilier grading |
| 4 | Don't Fall For THIS (Presets) | créateur solo | Critique presets | 🟡 positionnement |
| 5 | How I edit after 10 years | paysagiste (1 oiseau) | Workflow | 🟡 /recommend |
| 6 | 10 step RAW process | **Simon d'Entremont** | Workflow animalier | 🟡 /recommend + looks |
| 7 | 12-step Masterclass | **Simon d'Entremont** | Workflow animalier | 🟡 /recommend + looks |

**Signal fort : 3/7 des transcripts sont du même photographe animalier pro (Simon d'Entremont, Canada)** — c'est le corpus le plus pertinent qu'on ait eu sur le workflow animalier réel. Les 2 transcripts masquage sont directement sur notre brique premium (masques IA).

---

## 1. Ce que le corpus confirme de notre proposition (à garder)

1. **L'ordre canonique d'édition est stable** et correspond à ce que notre plugin devrait guider :
   `crop → corrections de base (WB/expo/shadows/highlights) → courbe → grading → TSL → détail → masques en dernier`. Les 3 auteurs workflow convergent. `[ÉTABLI]`
2. **Le masquage est LA compétence premium** — les 2 auteurs masquage le présentent comme ce qui sépare l'amateur du pro (« the most powerful tool », « the truth is most people underutilize masking »). Valide notre pari brique 3. `[ÉTABLI]`
3. **La séparation des couleurs (ombres froides / hautes chaudes)** est une technique nommée et revendiquée par les auteurs workflow — c'est notre signature « indigo/doré ». `[ÉTABLI]`
4. **Le positionnement anti-« filtre »** : le transcript presets dénonce exactement ce que nous voulons éviter (promesses « un clic », presets génériques, WB cassé). Notre axe « méthode + regard, pas filtre » est la bonne réponse.

---

## 2. Trois défauts RÉELS trouvés dans nos XMP (à corriger, pas cosmétique)

Vérification faite par le sous-agent grading contre les 36 fichiers `presets-naturaliste/*.xmp` :

### 2.1 — La balance des blancs est bakée en dur dans les 36 XMP ❌
Les XMP portent `ColorTemperature` (5400–6250 K) + `Tint`. Or c'est **précisément le piège n°1 dénoncé par la critique du marché** : un preset qui réécrit la WB « casse » sur les RAW dont la lumière diffère. Notre propre mode d'emploi (étape 2) dit « ajuster la WB à *votre* image » — la doc reconnaît le défaut que le fichier crée.
→ **Sortir WB/tint/expo des XMP de look** (« As Shot »), ou scinder `Look-*` vs `Base-*` optionnel. Effort ~1 h + re-export.

### 2.2 — Notre grading n'a que 2 roues, pas 3 ❌
Aucun `ColorGradeMidtone*` ni `ColorGrade*Lum` dans les 36 fichiers. C'est un **split toning à 2 points**, pas le grading 3 roues décrit par les transcripts. Conséquences :
- impossible de finir par les midtones (règle d'atelier récurrente) ;
- pas de slider Luminance pour rattraper l'« effet filtre » ;
- 30 des 36 fichiers utilisent **la même teinte d'ombres (220°)** — `Golden hour`, `Signature` et `Nocturne` ne diffèrent que de 2–5° de teinte. Au prix d'un pack, c'est mince.
→ **Ajouter la 3ᵉ roue (midtones) + Luminance + faire varier Blending/Balance par look.** Attention : le SDK ne remonte que `SplitToning*` (midtones/Luminance sans équivalent legacy) → portables dans le XMP mais invisibles au plugin. Acceptable : le XMP est l'unité de revenu.

### 2.3 — La landing revendique « indigo », le fichier contient « bleu acier » ❌
`SplitToningShadowHue="220"` = azur/acier (~250–270° serait l'indigo). Les hautes lumières (38–40° = doré) sont, elles, correctes.
→ Trancher : renommer en « bleu acier » **ou** pousser les ombres à 250–265° pour mériter le mot. Ne pas laisser l'écart mot↔fichier : c'est vérifiable à l'œil en 5 s.

---

## 3. Enrichissement brique 3 — masques IA (le premium)

Les 2 transcripts masquage donnent la recette exacte de ce qu'il faut livrer :

### 3.1 — Le masque « sélectionner le sujet » déborde (les 2 auteurs le disent)
Lightroom sélectionne le sujet **mais** mord sur l'arrière-plan et les ailes (oiseaux). Le workflow de raffinage est donc **obligatoire** dans la brique :
1. baisser l'**opacité de l'overlay** (réglages couleur) pour voir ce qui est sélectionné ;
2. bascule **O** pour vérifier ;
3. **soustraire au pinceau** les zones mordées.
→ Notre brique 3 ne peut pas se contenter de « masque sujet » : il faut un guide de raffinage intégré, sinon on vend le défaut que les deux pros dénoncent.

### 3.2 — Intersect = le primitif clé (sujet ∩ pinceau / ∩ luminance / ∩ couleur)
Exemple héron : « sujet ∩ pinceau » pour dompter les hautes lumières du plumage **sans overspray** sur le fond. C'est **exactement** la sémantique de nos 4 masques (sujet / œil / plumage / arrière-plan) :
- **œil** = sujet ∩ pinceau + exto + clarté + netteté ;
- **plumage** = sujet ∩ plage de luminance (pour ne toucher que les hautes du plumage) ;
- **arrière-plan** = sélection arrière-plan + -expo -texture + temp/tint.

### 3.3 — Recette spécifique animalière : la coulée bleue sur plumages blancs/noirs
Les 2 auteurs : tout **oiseau blanc** ou **animal noir** photographié sous ciel bleu porte une dominante bleue (réflexion du ciel). Correctif = **masque plage de couleur** (désaturer le bleu) puis réinjecter un peu de jaune (au couchant). C'est LA recette naturaliste récurrente, absente de nos 12 looks → **candidate idéale pour un preset de masque dédié « Plumage clair — anti-coulée »** (et son pendant « sujet sombre »).

### 3.4 — Automask + object mask
- **Automask** (pinceau) = « rester dans les lignes » sur les bords sujet/fond.
- **Object mask** détourné pour sélectionner une partie du sujet.
- **Radial gradient dupliqué** = dodge & burn local pour sculpter la lumière.
→ Autant de briques de base à exposer dans le plugin, pas seulement les 4 masques IA.

---

## 4. Enrichissement brique 4 — `/recommend`

### 4.1 — Les signaux EXIF/photo qui déterminent le choix d'un look (recoupés des 3 workflow)
| Signal | Décision |
|--------|----------|
| Heure / lumière (lever, coucher, nuit, neige, sous-bois) | scénario → `Golden hour`, `Nocturne`, `Contre-jour/brume`… |
| Sujet clair vs sombre (blanc = héron, noir = corvidé/rapace) | `Plumage clair` vs `Plumage sombre` + recette coulée bleue |
| Fond (neige, verdure, eau, ciel) | `Paysage`/`Contre-jour` + temp/tint du fond |
| ISO élevé (oiseau en vol, crépuscule) | `Action/vol` (bruit maîtrisé) |
| Distance/format (macro vs télé) | `Macro` vs `Mammifères`/`Plumage` |

### 4.2 — Les astuces de diagnostic à embarquer dans le plugin (valeur UX gratuite)
- **« Crank contrast »** : pousser le contraste à fond pour révéler structure et défauts avant de choisir quoi retoucher. `[AFFIRMÉ]`
- **Alt + slider** (noirs/blancs) : montre où ça clippe — réglage non destructif de la dynamique. `[ÉTABLI]`
- **WB à l'œil** : pousser vibrance+saturation à 100 % pour révéler la dominante, puis corriger. `[AFFIRMÉ]`
→ Trois « diagnostics guidés » différenciants, intraçables par les packs XMP statiques.

---

## 5. Trous dans la couverture des 12 looks

1. **Neige / hiver** — absent de nos 12 looks, alors que **c'est le créneau Munier revendiqué** (neige, atmosphère). Simon d'Entremont édite un hibou des marais sous neige ; le fond neigeux est un scénario à part entière. → **Look manquant n°1.**
2. **Automne** — le paysagiste utilise des presets « automne » dédiés ; le fauve/roux des mammifères et le feuillage d'automne ne sont couverts ni par `Mammifères` ni par `Paysage`. → **Look manquant n°2** (à trancher, cf. 6.1).
3. **Heure bleue** — glow crépusculaire (cité comme preset de masque par le transcript presets).

---

## 6. Recommandations priorisées

### P0 — corriger avant tout lancement (défauts réels)
1. **Découpler WB/tint/expo des 36 XMP de look** (2.1) — sinon on vend le défaut dénoncé par la concurrence.
2. **Trancher « indigo » vs « bleu acier »** (2.3) — mot ↔ fichier cohérents.
3. **Corriger le décompte doc** : le mode d'emploi dit « 12 fichiers » pour 36 XMP ; la landing dit « 12 presets ». Formuler « 12 looks × 3 forces = 36 fichiers » partout.

### P1 — renforcer le produit (différenciation réelle)
4. **Ajouter la 3ᵉ roue (midtones) + Luminance + varier Blending/Balance par look** (2.2) — rend les 12 looks réellement distincts.
5. **Redéfinir le contrat d'un look = `{ forme d'harmonie, plage d'ancrage, amplitude }`** au lieu d'une teinte fixe. Le XMP livre l'instance par défaut ; `/recommend` livre l'instance adaptée (dominante mesurée). Transforme « un preset est aveugle » en argument : *le preset seul est aveugle, le pack + `/recommend` ne l'est plus.*
6. **Brique 3 : livrer le workflow de raffinage + les 4 masques + la recette coulée bleue** (3.1–3.4). C'est ce qui justifie le prix premium ($55+, cf. Ryan Wilkes).

### P2 — enrichir la couverture et la doc
7. **Ajouter un look « Neige/hiver »** (et évaluer « Automne ») — cohérence avec le positionnement Munier. À décider *après* 4 (ne pas gonfler le catalogue sans traiter les roues).
8. **Section « ce que ces presets ne font PAS »** (ni WB, ni expo, ni débruitage IA boîtier, ni rattrapage flou) — désarme la critique « presets = arnaque », signal de confiance qu'aucun concurrent ne donne.
9. **Preuve avant/après falsifiable** : 1 RAW réel par look, boîtier + objectif + ISO documentés, même preset sur 2 boîtiers — répond au « tous boîtiers » non testé de la FAQ.
10. **Documenter forme + ordre d'exécution** de chaque look (colonne « Forme / ancre » + procédure « dominante → look → midtones en dernier »).

---

## 7. Garde-fous (ne pas sur-interpréter)

- **Aucune source ne parle d'indigo/doré** : notre signature chromatique est nôtre, ni validée ni invalidée. C'est un actif, pas une preuve.
- **La thèse « les presets cassent sur certains RAW » reste NON PROUVÉE** par ces vidéos — elle doit venir de nos tests (boîtiers/profils/Process Version), pas du discours marketing d'un créateur solo.
- **Le transcript « Don't Fall For THIS » a un intérêt éditorial** à dénigrer le marché (il vend son alternative) ; le transcript grading vend une ressource en description. Deux `[AFFIRMÉ]`, pas des sources techniques.
- **Le transcript grading ne mesure rien** (pas de test en aveugle) : sa valeur est pédagogique (vocabulaire + ordre + garde-fous), pas normative.

---

## Livrables associés
- `TEAM_Inbox/2026-11-16_dobby_analyse-transcript-lightroom-grading-presets.md` (12 recommandations détaillées, vérif contre les 36 XMP)
- `TEAM_Inbox/2026-11-16_dobby_analyse-transcript-lightroom-masquage.md` / `-workflow.md` (non écrits — canal sous-agent défaillant, analyse faite en direct par Dobby)

## Routing
- 7 transcripts → `02_ARTEON/99_REFERENCES/lightroom-technique_2026-11-16/`
- Prochaine action produit : trancher P0-1 (découplage WB) avec JC, puis Forge sur le re-export des 36 XMP.
