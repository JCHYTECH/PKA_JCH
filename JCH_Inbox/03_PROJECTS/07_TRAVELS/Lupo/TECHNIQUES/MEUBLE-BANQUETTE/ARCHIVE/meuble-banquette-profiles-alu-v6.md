# Meuble banquette — v6 Profilés aluminium (T-slot 2020)

> **Statut :** SUPERSÉDÉ par le **v7** (sans tiroir · volets rabattables · table coulissante). Conservé pour l'historique.
> **Empreinte :** 92 × 54 cm · **Hauteur hors tout : 25,6 cm** (contrainte lit banquette passager — inchangée).
> **Matériau :** ossature **profilé aluminium T-slot 20×20 (2020)** + panneaux **Dibond 3 mm** + assise **HPL compact 12 mm** (insensible humidité).
> **Principe :** 3 modules « cage » boulonnés (écosystème type imprimante 3D), chacun avec un **tiroir sur coulisses double sens (R28DD 500 mm)** conservé. **Accès double sens** (intérieur OU extérieur) et **assise** conservés.
> **Charge :** **15 kg max / tiroir** (inchangé). **Assise 80 kg** ponctuel (inchangé).

---

## 1. Analyse du modèle existant (v5 bois, clôturé 2026-10-19)

**Ce que le v5 a de juste (à conserver absolument) :**
- **Accès double sens** — c'est la fonction cœur : le même tiroir sert côté intérieur (vie à bord) ET côté extérieur (porte coulissante / hayon). Coulisses **Chambrelan R28DD 500 mm**, extension ~330 mm/côté (~61 %), 85 kg/paire.
- **Assise** — couvercle qui supporte ~80 kg ponctuel, affleurant, **simplement déposé** (amovible).
- **Asymétrie 1 large + 2 étroits** — A utile 320 mm, B/C utile 264 mm (empreinte 92 cm contrainte par le passage de roue / lit).
- **Charge 15 kg/tiroir**, hauteur tiroir 210 mm, traverse anti-rack, prises ovales 90×60.

**Ce que le v5 a de lourd (pourquoi passer à l'alu) :**
- **Panneaux HPL 10,5 mm** → découpe CNC précise (service de coupe), **chants à plaquer** (mélaminé), **rainurage + collage** des extrémités/fond.
- **Cadre en L bois dur** (profilé L 15×20) → usinage de bois dur.
- **Perçages M4 des coulisses** → à relever et percer précisément dans le bois (sans entraxe fourni).
- **9 pièces bois dur** (6 rails cadre L + 3 traverses) → usinage supplémentaire.
- Assemblage **collé + vissé** → irréversible, sensible à l'humidité et aux vibrations du van.

**Bilan :** un meuble juste sur le plan fonctionnel, mais dont la **fabrication** dépend d'une CNC + d'un service de coupe + de chants à plaquer. C'est exactement ce que l'aluminium supprime.

---

## 2. Objectif du v6 aluminium

Remplacer **caisson + tiroir en bois** par une **ossature aluminium T-slot boulonnée + panneaux insérés en rainure**, en conservant : empreinte, hauteur, accès double sens, assise, coulisses R28DD.

| Critère | v5 bois | v6 alu |
|---|---|---|
| Découpe panneaux | CNC / service de coupe | Panneaux rectangles simples (Dibond) |
| Chants | À plaquer | Aucun (Dibond = sandwich alu/poly) |
| Assemblage | Collé + vissé (irréversible) | Boulonné T-nuts + équerres (démontable) |
| Perçage coulisses | M4 précis dans le bois | **T-nuts coulissants dans la rainure** (réglable, sans perçage) |
| Rigidité | Bois + contreventement | **Panneaux en rainure = sandwich rigidifiant** |
| Humidité / vibration | Sensible (gonflement, collage) | Insensible (alu + Dibond) |
| Versatilité | Fixe | **Reconfigurable** (accessoires 2020, position réglable, démontable) |

---

## 3. Choix du profilé

**Recommandé : 2020 (20 × 20 mm) T-slot, rainure 6 mm, visserie M5 (équerres) + M4 (coulisses via T-nuts).**

- C'est le standard des châssis d'imprimantes 3D : barres à ~3–5 €/m, équerres, T-nuts et accessoires en masse.
- **Rigidité suffisante** pour l'assise (80 kg) grâce au cadre 4 rails + panneau d'assise, sans besoin de 20×40.
- Le **MakerBeam 10×10 / XL 15×15** (M3) évoqué avec ChatGPT est **trop léger** pour une assise portée à 80 kg et des tiroirs de 15 kg dans un van qui vibre → **déconseillé ici**.
- **Option de renfort** (si flèche d'assise trop visible à l'usage) : rails hauts en **20×40 (2040)** sur les 2 côtés porteurs, sans rien changer d'autre.

---

## 4. Architecture — par module (12 arêtes + panneaux)

Chaque module est une **cage rectangulaire** (le même motif que le caisson d'imprimante 3D décrit avec ChatGPT, transposé aux dimensions banquette) :

```
        ┌───────────── 4 rails HAUT (assise) ─────────────┐
        │                                                 │
   4 MONTANTS                                      panneaux
   (216 mm)                                        côtés
        │                                                 │
        └───────────── 4 rails BAS (fond) ────────────────┘
   Faces AVANT / ARRIÈRE = OUVERTES (accès tiroir double sens)
```

- **Caisson** = 4 rails haut + 4 rails bas + 4 montants verticaux, assemblés par **équerres d'angle** (8 par module) + T-nuts M5. Panneaux **fond + 2 côtés** en Dibond 3 mm insérés dans les rainures.
- **Assise** = panneau **contreplaqué 15 mm** (ou HPL 12 mm) **simplement posé** sur les 4 rails hauts, dans le creux (affleure, amovible). Support à 4 côtés → meilleur que le cadre en L 2 rails du v5.
- **Tiroir** = **cadre 2020 (4 rails)** + panneaux (2 côtés + 2 extrémités + 1 fond) fixés dessous, monté sur les coulisses R28DD.
- **Coulisses R28DD** : rail fixe monté sur les **rails latéraux du caisson** (rainure interne), rail mobile sur les **rails latéraux du tiroir** — via **T-nuts M4 coulissants** (aucun perçage, position réglable en continu).

---

## 5. Dimensions (v6)

### Modules — extérieur inchangé

| Module | Extérieur (L × P × H) | Utile intérieur | Tiroir (larg.) |
|--------|----------------------|-----------------|----------------|
| **A** | 344 × 540 × 256 mm | **304 mm** (−16 vs bois) | **280 mm** |
| **B / C** | 288 × 540 × 256 mm | **248 mm** (−16 vs bois) | **225 mm** |

> ⚠️ **Perte de 16 mm d'utile** par rapport au bois (20 mm de profilé contre 10,5 mm de panneau, ×2 côtés). Si tu veux la récupérer : **mutualiser les montants entre modules adjacents** (un seul montant central A/B et B/C) → on regagne ~20 mm par interface. À arbitrer (point ouvert §11).

### Détail des arêtes (caisson)

| Élément | Longueur | Qté / module |
|---------|----------|--------------|
| Rail haut (profondeur) | 540 mm | 2 |
| Rail haut (largeur) | 344 (A) / 288 (B/C) | 2 |
| Rail bas (profondeur) | 540 mm | 2 |
| Rail bas (largeur) | 344 (A) / 288 (B/C) | 2 |
| Montant vertical | **216 mm** (256 − 2×20) | 4 |

### Tiroir (cadre 2020 + panneaux suspendus)

| Élément | A | B / C |
|---------|---|-------|
| Rail latéral (profondeur) | 540 mm ×2 | 540 mm ×2 |
| Rail extrémité (largeur) | 280 mm ×2 | 225 mm ×2 |
| Hauteur utile tiroir | **210 mm** (panneaux suspendus sous le cadre) | 210 mm |

### Assise (panneau posé, affleurant)

| Module | Panneau assise |
|--------|----------------|
| A | **300 × 540 mm** (HPL compact 12 mm) |
| B / C | **244 × 540 mm** (HPL compact 12 mm) |

---

## 6. Liste de coupes profilés — TOTAUX (2020)

| Pièce | Longueur | Qté | Total |
|-------|----------|-----|-------|
| Rail profondeur (caisson haut + bas) | 540 mm | 12 | 6 480 mm |
| Rail largeur A (haut + bas) | 344 mm | 4 | 1 376 mm |
| Rail largeur B/C (haut + bas) | 288 mm | 8 | 2 304 mm |
| Montant vertical | 216 mm | 12 | 2 592 mm |
| Rail tiroir profondeur | 540 mm | 6 | 3 240 mm |
| Rail tiroir largeur A | 280 mm | 2 | 560 mm |
| Rail tiroir largeur B/C | 225 mm | 4 | 900 mm |
| **TOTAL** | | **44 pièces** | **≈ 17,5 m** |

> Les barres de 2020 s'achètent en longueurs de 1 m ou 2 m et se coupent à la **scie à métaux** (ou mini-meuleuse) — aucune découpe CNC. Un trait de scie droit suffit, les équerres absorbent les ±1 mm.

---

## 7. Panneaux (Dibond 3 mm — alu composite)

| Panneau | Qté | Dimensions (mm) |
|---------|-----|-----------------|
| Côté caisson | 6 | 540 × 216 |
| Fond caisson A | 1 | 304 × 540 |
| Fond caisson B/C | 2 | 248 × 540 |
| Côté tiroir | 6 | 540 × 210 |
| Extrémité tiroir A | 2 | 280 × 210 |
| Extrémité tiroir B/C | 4 | 225 × 210 |
| Fond tiroir A | 1 | 280 × 540 |
| Fond tiroir B/C | 2 | 225 × 540 |
| **Assise** (HPL compact 12) | A 1 + B/C 2 | 300/244 × 540 |

> **Dibond 3 mm** se coupe au cutter (entaille + pliage) ou à la scie — pas de chant, étanche, coloré à cœur (gris/blanc au choix). **Assise en HPL compact 12 mm** — coloré à cœur, insensible à l'humidité (van inutilisé = condensation), pas de chant ; rectangle à découper, chants légèrement poncés.

---

## 8. Quincaillerie (BOM)

| # | Élément | Qté | Spécification | Indicatif |
|---|---------|-----|---------------|-----------|
| 1 | **Coulisses Chambrelan R28DD** | 6 (3 paires) | 500 mm, double développement, 85 kg/paire, M4 | ~150–270 € (poste principal, inchangé) |
| 2 | Profilé 2020 (20×20) | ~17,5 m | T-slot, rainure 6 mm | ~55–90 € |
| 3 | Équerre d'angle 2020 | ~40 | L 2 trous, M5 | ~20–50 € |
| 4 | T-nuts M5 (équerres) | ~80 | Écrou à coulisse pour rainure 6 mm | ~8 € |
| 5 | T-nuts M4 (coulisses) | ~24 | Montage coulisses réglable | ~3 € |
| 6 | Visserie M5 (bouton + fraisée) | ~120 | Inox, longueurs 8–10 mm | ~10 € |
| 7 | Visserie M4 (coulisses) | lot | Selon perçages R28DD | ~5 € |
| 8 | Dibond 3 mm | ~2,5 m² | Faces gris/blanc | ~25–45 € |
| 9 | Assise contreplaqué 15 mm | ~1,4 m² | Bouleau, huilé | ~20–30 € |
| 10 | Prise ovale 90×60 | 6 | 1 par extrémité de tiroir | ~12–24 € |
| 11 | Sangle à came 2,5 m | 1 | Maintien en conduite | ~8–15 € |
| 12 | Chevilles + loquets (solidarisation) | 4 + 2 | Inchangé | ~8–16 € |

**Total estimatif :** ~**200–330 €** (dominé par les coulisses R28DD, qui restent la dépense incompressible). Le **reste de la structure revient à ~90–190 €** et se monte sans outil de menuiserie.

---

## 9. Montage (par module, ~1 h sans outil spécialisé)

1. **Couper** les 12 arêtes du caisson (scie à métaux) + les 4 rails du tiroir.
2. **Assembler** la cage caisson : 8 équerres d'angle + T-nuts M5 (haut et bas). Vérifier l'équerre sur un coin.
3. **Insérer** les panneaux fond + côtés (Dibond) dans les rainures des rails.
4. **Monter les coulisses** : fixer les rails fixes R28DD sur les rails latéraux internes du caisson via **T-nuts M4** (coulissants — alignement sans perçage), les rails mobiles sur les rails latéraux du tiroir.
5. **Assembler le tiroir** : cadre 2020 (4 rails + équerres) + panneaux suspendus dessous (côtés, extrémités, fond). Monter sur les coulisses.
6. **Poser l'assise** : panneau 15 mm simplement déposé dans le cadre haut (amovible).
7. **Solidariser** les 3 modules : chevilles Ø8 + loquets à bascule (inchangé).

> **Réglage des coulisses = le point fort** : les T-nuts M4 coulissent dans la rainure → on règle la hauteur et l'alignement des deux coulisses **à la main**, là où le bois imposait de percer juste du premier coup.

---

## 10. Comparatif bois (v5) vs alu (v6)

| | v5 bois | v6 alu |
|---|---|---|
| **Faisabilité DIY** | CNC + service de coupe + chants + rainurage | Scie à métaux + clé Allen + cutter |
| **Outillage** | Défonceuse, plaqueuse de chants, presse | Clé Allen, scie à métaux, cutter, perceuse (option) |
| **Poids** | ~25–28 kg | ~18–22 kg (alu + Dibond, assise incluse) |
| **Rigidité assise** | 1,7 mm de flèche à 80 kg | ≤ 1,5 mm (cadre 4 côtés + panneau 15 mm) |
| **Humidité / vibration** | Sensible | Insensible |
| **Réversibilité** | Collé (non) | Boulonné (démontable, reconfigurable) |
| **Versatilité** | Fixe | Accessoires 2020 (crochets, rails, charnières) |
| **Coût structure** | ~185–330 € (dont coulisses) | ~200–330 € (dont coulisses) |

---

## 11. Arbitrages (Dobby 🦉 — à confirmer JC)

1. **Perte de 16 mm d'utile → ACCEPTÉE (modules indépendants).** On garde 3 cages identiques et autonomes. Tiroir A 280 mm (vs 297 bois), B/C 225 mm (vs 241) — perte mineure. Le caractère « LEGO » et la simplicité de 3 boîtes identiques priment. *Alternative si la largeur devient critique : mutualiser les montants intermédiaires (récupère ~40 mm au total).*
2. **Assise → HPL compact 12 mm.** Insensible à l'humidité (van inutilisé = condensation, écarts de T°), coloré à cœur sans chant, très rigide. Le contreplaqué, même huilé, reste sensible aux reprises d'humidité → écarté.
3. **Équerres → cubes 3 voies (corner cube) aux 8 sommets du caisson**, équerres L simples pour le tiroir (plus léger). Les cubes rigidifient les angles dans 3 axes — indispensable en van.
4. **Panneaux tiroir → Dibond 3 mm partout** (décision JC). La structure est portée par le cadre 2020 (rails + coulisses), les panneaux ne sont qu'enveloppe. *Caveat : le fond 3 mm peut fléchir légèrement sous charge concentrée 15 kg — une entretoise 2020 centrale en plus le corrige si besoin.*
5. **Base → 3 fonds indépendants (pas de rail continu).** Préserve le caractère modulaire/démontable. La mise à niveau au sol se gère par cales.

---

*Proposition v6 rédigée le 2026-11-06 par Dobby 🦉, dérivée de la réflexion ChatGPT « Profilés aluminium 10×10 » + du v5 bois. À valider par JC avant BOM définitif et plan SVG.*
