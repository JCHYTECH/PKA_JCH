---
date: 2026-11-16
source: dobby
domain: arteon
type: analyse-transcript
status: actif
lang: fr
corpus: 2 transcripts NoteGPT (The Stupid Trick To Perfect Color Grades In Lightroom ; Don't Fall For THIS (Lightroom Presets)!)
---

# Analyse — Color grading par les formes & critique du marché des presets

> Dobby 🦉 — 2026-11-16 · Lecture intégrale des 2 transcripts + vérification contre nos XMP réels (`02_ARTEON/presets-naturaliste/`).
> Objet : ce que ces 2 sources changent dans la proposition « Pack Naturaliste » (grading, 36 XMP, doc, marketing).

**Convention de statut** : `[ÉTABLI]` = technique/propriété standard, vérifiable hors auteur · `[AFFIRMÉ]` = opinion de l'auteur, non mesurée · `[NON PROUVÉ]` = plausible mais aucune preuve dans le transcript.

---

## 1. Synthèse — Transcript A « The Stupid Trick To Perfect Color Grades In Lightroom » (12:20)

**Thèse** : le color grading de Lightroom n'est pas un exercice de devinette, c'est un exercice de **forme géométrique**. Les 3 roues (ombres / tons moyens / hautes lumières) sont projetées sur un seul cercle chromatique ; la figure que forment les 3 points sur ce cercle EST l'harmonie colorée. L'auteur substitue aux noms d'harmonies (triade, complémentaire divisée, monochrome…) un mnémonique de 4 formes : **« trois / ligne / Y / triangle »** (« three-Y-line-tri rule »).

**Ce que le transcript dit vraiment (et rien de plus)** :

1. **4 formes = 4 harmonies** — « trois » (triade équilibrée), « ligne » (analogue/monochrome, les 3 points alignés), « Y » (complémentaire divisée : 2 couleurs d'un côté, 1 à l'opposé), « triangle » (triade). `[ÉTABLI]` pour la théorie des harmonies ; `[AFFIRMÉ]` pour l'équivalence avec les 3 plages de Lightroom (interprétation cohérente, pas une propriété du logiciel).
2. **Ordre d'exécution** (01:10) : commencer par la plage **dominante** de la scène, **finir par les tons moyens** — jamais l'inverse, parce que les tons moyens « font l'équilibrage ». `[AFFIRMÉ]` : règle d'atelier, aucune mesure ; logique défendable (les midtones sont les plus visibles à l'œil).
3. **Raccourcis = le cœur opératoire** (01:33–02:47) : `Shift` + glisser = **verrouille la teinte, libère la saturation** ; `Cmd/Ctrl` + glisser = **verrouille la saturation, libère la teinte**. `[ÉTABLI]` (comportement documenté de Lightroom).
4. **« Effet filtre » = signal d'erreur** : quand le virage ressemble à un filtre posé sur l'image (« washed out color going over your photo »), le correctif est le **slider Luminance de la plage concernée** (assombrir la couleur des ombres sans changer sa teinte), puis **Blending** (dureté de la transition ombre → haute lumière) et **Balance** (biais vers les hautes lumières ou vers les ombres). `[ÉTABLI]` pour l'existence des contrôles ; `[AFFIRMÉ]` pour la primauté du correctif ; l'auteur concède lui-même : « there is no exact science to this part ».
5. **Deux règles de dosage, les plus utiles pour nous** :
   - « You can choose colors that compete with the existing colors, but you will have an easier time **moving your colors in a direction that your photo already has** » (05:28) → le grade **accentue**, il ne réécrit pas.
   - Quand une couleur est déjà dominante (cas du bleu, 08:58), il **ancre à l'opposé depuis les ombres** et laisse les hautes lumières tranquilles ; et si c'est encore trop : « **barely add a color at all or just skip an exposure range** » (10:17) — l'abstention est une option légitime.
6. **Aveux de faiblesse** : au départ il « bougeait les roues au hasard » puis « reset everything and pretend this tool doesn't exist » ; la méthode est un garde-fou anti-errance, pas un modèle prédictif. `[NON PROUVÉ]` : aucune comparaison avant/après mesurée, aucun test en aveugle, aucune validation par des tiers.

**Ce que le transcript A ne dit PAS** (pour ne pas sur-attribuer) : il ne prescrit **aucun couple de teintes fixe** type « indigo dans les ombres / doré dans les hautes ». Le teal-orange n'est qu'une des figures possibles (ligne ou Y), et il est explicitement conditionné à la dominante de l'image. **Notre revendication marketing actuelle n'est donc pas confirmée par cette source : elle est relativisée.**

---

## 2. Synthèse — Transcript B « Don't Fall For THIS (Lightroom Presets)! » (6:49)

**Thèse en deux temps** : réponse courte — « presets are a scam », n'achetez pas ; réponse longue — certains réglages se transportent très bien, d'autres jamais, et le tri dépend de la **nature du réglage**, pas de la qualité du preset.

1. **Loi de transfert** : « the more you edit an image, the less these settings can be applied to other shots » (00:36). Plus un look est construit sur des corrections spécifiques à l'image, moins il est portable. `[ÉTABLI]` en pratique : un preset est un delta absolu, pas relatif.
2. **Taxonomie explicite — ce qui ne se transporte PAS** : exposition, **balance des blancs**, **masquage** ; et dans son énumération du workflow, le **color grading** figure aussi parmi les étapes « spécifiques à cette image » (01:13). Motif : « because the light is different, I might have used other camera settings ». `[AFFIRMÉ]` mais argumenté — c'est l'avertissement le plus directement applicable à nos fichiers.
3. **Ce qui se transporte bien** : **débruitage, netteté, texture, clarté, et « to some degree » le dehaze** (01:49). `[AFFIRMÉ]` — cohérent avec la pratique (réglages de rendu de détail, peu dépendants de l'exposition).
4. **Recette de netteté standard** (répétée sur chaque image) : baisser le **rayon**, monter le **détail**, ajouter du **masquage**, doser le **montant**. `[ÉTABLI]` — c'est le réglage de netteté d'usage courant.
5. **Les presets de masque existent et sont le vrai gain** : exemple « glow » en heure bleue = exposition ↑, noirs ↑, température ↑, dehaze ↓, sauvegardé comme preset de masque, réappliqué sur une autre image à source lumineuse artificielle (03:43–04:48). `[ÉTABLI]` (fonctionnalité Lightroom) et **directement pertinent pour la brique 3**.
6. **Un preset reste éditable après application** — point de départ, pas résultat. `[ÉTABLI]`.
7. **Le seul cas où il recommande d'acheter/faire des presets** : mariage, événement, immobilier — volume élevé, conditions stables, pas de temps pour l'image-par-image. `[AFFIRMÉ]`, et **mauvaise nouvelle assumée pour notre niche** : il cite explicitement le paysage et l'animalier comme les cas où il édite manuellement, image par image (04:56).
8. **Verdict commercial** : « they almost never achieve what is promised » ; pour un débutant, « you won't learn much from using presets » (05:28). `[AFFIRMÉ]` — opinion sans données, mais c'est **le discours dominant du marché** ; notre copy doit y répondre frontalement.
9. **Non traité par le transcript** : la casse technique des presets sur certains RAW (profils boîtier, DNG vs CR3/NEF, Process Version). Le transcript parle de « light is different / camera settings », pas de compatibilité de format. **Toute affirmation de notre part sur ce point devra venir de nos propres tests**, pas de cette source.

---

## 3. Techniques et pièges exploitables (tableau de tri)

| # | Élément | Statut | Exploitation ARTEON |
|---|---------|--------|---------------------|
| T1 | 4 formes d'harmonie (triade / ligne / Y / triangle) comme substitut aux noms | `[ÉTABLI]` théorie + `[AFFIRMÉ]` mapping | **Vocabulaire des 12 looks** : nommer la forme, pas seulement la teinte |
| T2 | Ordre : plage dominante d'abord, midtones en dernier | `[AFFIRMÉ]` | Procédure du mode d'emploi (3 étapes reproductibles) |
| T3 | `Shift` = teinte verrouillée / `Cmd` = saturation verrouillée | `[ÉTABLI]` | Justifie le **curseur proportionnel** : faire varier la saturation, jamais la teinte |
| T4 | Correctif anti « effet filtre » = sliders **Luminance** par plage | `[AFFIRMÉ]` | **Absent de nos XMP** (aucun `ColorGrade*Lum`) → à ajouter |
| T5 | Blending (dureté de transition) + Balance (biais ombres/hautes) | `[ÉTABLI]` | Blending=50 et Balance=−20 **figés dans les 36 fichiers** → devraient varier par look |
| T6 | Accentuer la direction chromatique existante, pas la contredire | `[AFFIRMÉ]`, solide en pratique | **Argument central du positionnement naturaliste** (éthique = ne pas réécrire la scène) |
| T7 | « Skip an exposure range » / « barely add a color » | `[AFFIRMÉ]` | Un look doit pouvoir **s'auto-annuler** sur une image incompatible |
| T8 | Seuls les réglages de rendu (bruit, netteté, texture, clarté, dehaze) sont portables | `[AFFIRMÉ]` | **Nos XMP violent la règle** : WB + expo bakés (cf. §4.1) |
| T9 | Presets de masque (glow heure bleue) = gain de temps réel | `[ÉTABLI]` | Livrable additionnel de la brique 3, précédent crédible |
| T10 | Le marché promet la transformation magique du RAW terne | `[AFFIRMÉ]` (observation de marché) | **Anti-positionnement disponible** : promesse falsifiable + limites publiées |
| P1 | Piège : presets « universels » vendus comme passe-partout | `[AFFIRMÉ]` | Nous vendons 12 looks → risque de reproduire le travers (cf. §4.6) |
| P2 | Piège : le preset applique des **valeurs absolues** (WB, expo) → casse dès que la lumière change | `[ÉTABLI]` techniquement | Bug réel chez nous (§4.1) |
| P3 | Piège : « tu n'apprends rien » — le preset comme substitut de compétence | `[AFFIRMÉ]` | Réponse : le pack **enseigne la décision** (quel look, pourquoi, quand s'abstenir) |
| P4 | Piège : l'auteur lui-même n'utilise pas de presets en animalier | `[AFFIRMÉ]` | Objection n°1 en vente → à traiter de face, pas en note de bas de page |

---

## 4. Implication ARTEON

### 4.0 — Ce que ces 2 sources ne changent PAS

Le socle produit tient : 12 looks × 3 forces, courbe paramétrique + grading + TSL, masques IA en premium. Aucun des deux transcripts ne remet en cause l'architecture. **Ce qu'ils remettent en cause, c'est (a) le contenu exact de nos roues, (b) ce que nos XMP forcent, (c) la promesse commerciale.** Rien ici ne justifie de toucher au nombre de looks.

### 4.1 — CORRIGER (bloquant) : les 36 XMP bakent la balance des blancs

**Constat sur nos fichiers** : les 36 XMP contiennent `crs:WhiteBalance="Custom"` + une température fixe + un tint + une exposition.

- `presets-naturaliste/Plumage colore - Doux.xmp:10-13` → `WhiteBalance="Custom"`, `ColorTemperature="5400"`, `Tint="+0.80"`, `Exposure2012="+0.04"`
- `presets-naturaliste/Golden hour.xmp:10-12` → 6250 K / tint −1
- `presets-naturaliste/Nocturne.xmp:10-12` → 6000 K / tint +2
- `presets-naturaliste/Signature Fin Art Cinematique.xmp:10-12` → 5600 K / tint +4
- 36/36 fichiers concernés (`grep -l 'crs:WhiteBalance="Custom"' *.xmp` → 36)

**Pourquoi c'est grave** : c'est **exactement** le piège P2 du transcript B (« if I would put the white balance, exposure into a preset and copy them onto another image, it would most likely make the picture worse », 01:13). Une photo de martin-pêcheur prise à 4800 K en sous-bois reçoit 5400 K + tint +0.80 : le preset **détruit la neutralité** avant que l'utilisateur n'ait rien fait. Pire, notre `mode-emploi-naturaliste.md` (étape 2) dit « Ajuster exposition et balance des blancs à *votre* image » : **la doc reconnaît le problème que le fichier crée**.

**Recommandation** : sortir `WhiteBalance`, `ColorTemperature`, `Tint`, `Exposure2012` des XMP de look (laisser « As Shot »), ou scinder en `Look-*` (courbe + grading + TSL + détail) et `Base-*` explicitement optionnel. À défaut, un seul look « Signature » peut porter un parti-pris WB — pas les 36.
**Test de recette** : 3 RAW (ombre froide / plein soleil / nuit) × 3 looks ; le preset ne doit déplacer le WB d'aucun des 3.

### 4.2 — NUANCER : « indigo » n'est pas ce que le fichier contient

La landing (`landing-presets-naturaliste.html:82-83`) revendique « Ombres : veloutées, teintées indigo » / « Hautes lumières : dorées, comprimées ». L'artefact dit : `SplitToningShadowHue="220"` (plage 220–230 selon les looks), `SplitToningHighlightHue="38"` (35–40).

- **Hautes lumières** : 38–40° = orange/doré → **revendication correcte, confirmée**.
- **Ombres** : 220° = **bleu acier / azur**, pas indigo (~250–270°). Deux options honnêtes : assumer « bleu froid / acier » dans le copy, ou pousser la teinte vers 250–265 pour mériter le mot. Ne pas laisser l'écart entre le mot et le fichier : c'est le type d'écart qu'un client vérifie à l'œil en 5 secondes, et c'est exactement le reproche du transcript B (« they almost never achieve what is promised »).

### 4.3 — ENRICHIR : passer de 2 roues à 3 (et ajouter les sliders Luminance)

Constat : **aucun** fichier ne contient `ColorGradeMidtone*` (`grep -l ColorGradeMidtone *.xmp` → 0) ni de `ColorGrade*Lum`. Notre grading est un **split toning à 2 points** — pas le grading à 3 roues que décrit le transcript A. Conséquences concrètes :

- La règle T2 (finir par les midtones) est **structurellement impossible** avec nos presets actuels.
- Le correctif T4 (anti « effet filtre ») est **inopérant** : pas de slider Luminance pour rattraper une couleur qui délave les ombres.
- Les 4 formes de T1 supposent 3 points : avec 2 points on ne peut produire qu'une **ligne** ou un **Y dégénéré**. Le vocabulaire de formes reste donc décoratif tant que la 3ᵉ roue n'existe pas.
- **À vérifier** (non prouvé) : l'absence de `ColorGradeBalance` (on n'a que le legacy `SplitToningBalance="-20"`) — exporter un XMP depuis Lightroom 15 avec la Balance réglée et comparer les clés. Si la clé manque, notre Balance n'est lue que par le chemin legacy.
- **Contrainte à trancher** : le SDK ne remonte que `SplitToning*` (cf. `2026-11-16_dobby_conseil_colorgrade-A-vs-B.md`). Les midtones et les Luminance n'ont **pas** d'équivalent legacy → elles seront portables dans le XMP mais **invisibles au plugin**. C'est acceptable : le XMP est l'unité de revenu, le plugin n'a pas à connaître chaque roue. Ne pas retomber dans le débat A/B pour ça.

### 4.4 — REDÉFINIR le contrat d'un look : (forme + ancrage + amplitude), pas (teinte fixe)

C'est le point le plus structurant, et il vient du croisement des deux transcripts : A dit « pars de la dominante de l'image », B dit « le grading fait partie de ce qui ne se transporte pas ». Un XMP ne peut pas « partir de la dominante » — il applique des valeurs fixes. **D'où la contradiction à résoudre** : soit on assume que les 12 looks sont des partis-pris (et on le dit), soit on encode le look comme une règle et c'est la brique 4 `/recommend` qui l'instancie.

Proposition : chaque look = triplet documenté
`{ forme d'harmonie, plage d'ancrage, amplitude }` — ex. « Y : ancre ombres à l'opposé de la dominante détectée, doré en hautes, midtones en équilibrage ». L'XMP livre une **instance par défaut** de ce triplet ; `/recommend` en livre une **instance adaptée** (dominante mesurée sur l'image). Cela transforme une faiblesse (« un preset ne peut pas lire l'image ») en argument produit : *le preset seul est aveugle, le pack + `/recommend` ne l'est plus*.

### 4.5 — Recommandations concrètes, numérotées (par ordre de priorité)

1. **Découpler WB/expo du XMP de look** (§4.1). Sans ça, tout le reste est cosmétique : on vend le défaut que la concurrence est accusée d'avoir. Effort ≈ 1 h de script + re-export des 36.
2. **Trancher « indigo »** : soit renommer en « bleu acier », soit passer les ombres à 250–265° sur les looks qui le revendiquent. Effort ≈ 30 min, décision de goût.
3. **Ajouter la 3ᵉ roue (midtones) + les 3 sliders Luminance** à chaque look. Effort ≈ 2 h ; c'est ce qui rend les 12 looks **réellement distincts** au lieu de 12 variations du même teal-orange. Mesure : les 36 fichiers n'utilisent que **3 valeurs de teinte** — ombres 210 (3 fichiers), 220 (**30**), 230 (3) ; hautes lumières 35 (3), 38 (**30**), 40 (3). `Golden hour` (220/10, 40/7), `Signature` (220/10, 38/6) et `Nocturne` (230/10, 35/6) ne diffèrent donc que de 2–5° de teinte : au prix d'un pack, c'est mince, et ce n'est pas la 3ᵉ roue qui le corrigera toute seule — c'est la combinaison forme + luminance + blending.
4. **Faire varier Blending et Balance par look** (aujourd'hui 50 et −20 partout, `*.xmp:57` et `:52`). C'est le seul levier « douceur/dureté » gratuit : `Contre-jour/brume` doit être très fondu, `Noir & blanc` net, `Action/vol` plus sec. Effort ≈ 15 min.
5. **Curseur proportionnel = variation de saturation uniquement, teinte constante** — c'est la sémantique des raccourcis `Shift` (T3) et c'est aussi ce que fait `presetAmount`. Deux conséquences : (a) interdire dans le script toute modification de `Hue` entre `- Doux`, base et `- Fort` (à vérifier : aucune règle ne l'impose aujourd'hui) ; (b) `Crs:SupportsAmount="True"` est déjà présent (`Plumage colore - Doux.xmp:80`) → le curseur « Amount » natif de Lightroom existe ; l'exposer dans la doc plutôt que d'en inventer un. **À confirmer en UI** (1 min) : le slider Amount apparaît-il bien sur nos presets importés ?
6. **Documenter la forme de chaque look + l'ordre d'exécution** dans le mode d'emploi : ajouter une colonne « Forme / ancre » au tableau des 12 looks, et une procédure « 1) regarde la dominante, 2) choisis le look, 3) corrige les midtones en dernier ». Coût quasi nul, valeur pédagogique = réponse directe au piège P3 (« on n'apprend rien »).
7. **Section « ce que ces presets ne font PAS »** dans le mode d'emploi **et** la landing : ni WB, ni exposition, ni débruitage IA dépendant du boîtier, ni rattrapage d'une photo floue ou sous-exposée de 3 IL. C'est le seul moyen crédible de désarmer P1/P2/P4 — et c'est un signal de confiance qu'aucun concurrent ne donne.
8. **Corriger l'incohérence documentaire** : le mode d'emploi dit « Sélectionner les **12** fichiers `.xmp` » alors que le pack en contient **36** (`ls *.xmp | wc -l` → 36) ; la landing dit « 12 presets XMP · PDF mode d'emploi ». Choisir une formulation unique et exacte : « 12 looks × 3 forces = 36 fichiers ».
9. **Preuve avant/après falsifiable** : pour chaque look, 1 RAW réel + le nom du boîtier + l'objectif + ISO, et le même preset appliqué sur 2 boîtiers différents. Répond au « presets génériques, aucun profil boîtier requis » de la FAQ, qui est aujourd'hui une affirmation **non testée** et en tension directe avec la critique du transcript B.
10. **Brique 3 : livrer aussi des presets de masque** (glow heure bleue, plumage en contre-jour, œil). Précédent documenté par l'auteur du transcript B (T9) ; c'est le complément naturel des masques IA et ça matérialise le premium sans nouvelle architecture.
11. **Positionnement « Munier » — reformulation** : la critique la plus dangereuse n'est pas « les presets sont mauvais », c'est « **en animalier, on n'utilise pas de presets** ». La réponse n'est pas de nier, c'est de déplacer l'objet vendu : *on ne vend pas un filtre, on vend un regard + une méthode de décision* (quel look, pourquoi celui-là, et **quand ne pas l'appliquer** — T7). C'est exactement le créneau poétique/éthique, et c'est la seule réponse qui rend la crédibilité zoologiste pertinente : le zoologiste sait quelle lumière est *vraie* pour l'espèce et le milieu.
12. **Ce qu'il ne faut PAS revendiquer** : « transforme vos RAW ternes en chefs-d'œuvre » (T10), « un seul clic », « compatible tous RAW sans test », « indigo » tant que 220°. Le transcript B nomme ces promesses comme le marqueur du marché douteux ; s'en écarter est un différenciateur à coût nul.

### 4.6 — Décision de scope : ne pas ajouter de looks

La tentation serait d'ajouter des looks « heure bleue », « pluie », « neige » après lecture. **Non** : le transcript A montre que la différenciation vient du **dosage** (forme, luminance, blending), pas du nombre de recettes. 12 looks × 3 forces = 36 fichiers ; passer à 16 looks sans traiter 4.1 et 4.3 ne ferait qu'augmenter le nombre de variations indistinctes. Investir dans les roues, pas dans le catalogue.

---

## 5. Points à ne pas sur-interpréter (garde-fous)

- **Aucune des deux sources ne parle d'indigo/doré** : notre signature chromatique est **nôtre**, elle n'est ni validée ni invalidée par ce corpus. C'est un actif, pas une preuve.
- **Le transcript B ne mentionne jamais la casse par format RAW** : la thèse « les presets cassent sur certains RAW » reste **non prouvée** à ce stade ; elle doit venir de nos tests (boîtiers, profils, Process Version), pas de ces vidéos.
- **Les deux auteurs sont des créateurs solo** vendant (ou refusant de vendre) des presets : le transcript B a un intérêt éditorial à dénigrer le marché, le transcript A à proposer une ressource gratuite en description. Les deux sont des `[AFFIRMÉ]` de qualité variable, pas des sources techniques.
- **Le transcript A ne mesure rien** : ni test en aveugle, ni comparaison inter-observateurs. Sa valeur est pédagogique (vocabulaire + ordre + garde-fous), pas normative.
