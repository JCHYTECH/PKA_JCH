---
date: 2026-11-15
source: dobby
domain: arteon
type: cartographie
status: actif
lang: fr
---

# Cartographie fonctionnelle — presets animaliers relevés

> On ne compare pas les presets par la marque, mais par **ce qu'ils font**. Trois dimensions suffisent :
> **(1) registre technique** (ce qu'ils touchent), **(2) ciblage** (sur quoi ils sont calibrés), **(3) vecteur** (comment ils se livrent).

---

## Dimension 1 — Registre technique (ce que le preset modifie)

| Registre | Effet concret | Presets relevés |
|----------|---------------|-----------------|
| **Ton** | contraste, exposition, lift des noirs, compression des hautes | Cinematic Wildlife, Contrast/HDR Bird, Ansel Adams, Low Key |
| **Couleur** | TSL, vibrance, saturation ciblée | Vivid/Colorful Bird, Saturation Pop, Serge Ramelli |
| **Ambiance** | grading, température, dehaze, grain | Moody Forest, Green Moody Bird, Cool/Blue Bird, **Vincent Munier** |
| **Monochrome** | N&B, split toning, sépia | Vintage Wildlife, Noir & Blanc argentique, Low Key |
| **Local** | pinceau / radial / dégradé ciblé | Feather Detailer, Perch Detailer (Craig Rogers) |
| **IA adaptatif** | masque sujet/ciel/neige/pluie intégré | Wild Edits « Adaptive », LSP (88 masques) |

---

## Dimension 2 — Ciblage (sur quoi c'est calibré)

| Ciblage | Logique | Presets relevés |
|---------|---------|-----------------|
| **Générique** | aucun calibrage, look passe-partout | PSD Stack, mhrcreator |
| **Mood** | une émotion (cinematic, moody, vintage, HDR) | Presetpedia (50 Wildlife), Pose Nature |
| **Scénario** | une situation (golden, nocturne, macro, vol, brume) | **Nos 12 Naturaliste** |
| **Taxon** | une espèce (plumage, fourrure, yeux) | birdpack™ (190+ presets / 24 taxons) |
| **Localisé** | une zone de l'image (œil, plumage, perchoir) | Craig Rogers (brush) |

---

## Dimension 3 — Vecteur (comment il se livre)

| Vecteur | Caractéristique | Presets relevés |
|---------|-----------------|-----------------|
| **Statique** | XMP figé, tout ou rien | Presetpedia, PSD Stack, birdpack, Woodland |
| **Adaptatif** | masques IA intégrés, se recale sur la photo | Ryan Wilkes, LSP |
| **Interactif** | curseur d'intensité | Pose Nature (« quantity slider »), **notre slider paramétrique** |
| **Pinceau** | s'applique au pinceau, pas à l'image | Craig Rogers |

---

## La carte — où chacun se place

```
REGISTRE →     Ton        Couleur     Ambiance    Mono     Local     IA
Ciblage ↓
Générique      PSD/mhr    PSD         PSD         PSD      —         —
Mood           Presetpedia Presetpedia Presetpedia Presetpedia —      —
               PoseNat.   PoseNat.    PoseNat.*   PoseNat. —         —
Scénario       ARTECON    ARTEON      ARTEON      ARTEON   —         —
Taxon          birdpack   birdpack    birdpack     birdpack —         —
Localisé       —          Craig       Craig        —        Craig     —
Adaptatif      Ryan       Ryan        Ryan         Ryan     Ryan      Ryan
Interactif     PoseNat.   PoseNat.    PoseNat.     PoseNat. —         —
               ARTECON    ARTEON      ARTEON       ARTEON   —         —

* Vincent Munier (Pose Nature) = registre Ambiance / ciblage Mood — le créneau ARTEON.
```

---

## Ce que la carte révèle (lecture stratégique)

**1. Le quadrant bas-gauche (Ton/Couleur/Mood génériques) est saturé.** Presetpedia, PSD Stack, Pose Nature s'y battent à coup de volume. Aucune barrière d'entrée, aucune crédibilité. **On n'y va pas.**

**2. Le quadrant haut-droit (Scénario + IA + Interactif) est presque vide.** Personne ne combine : ciblage **scénario zoologiste** × registre **complet (ton+couleur+ambiance+mono)** × vecteur **interactif proportionnel** × **éthique documentée**. C'est notre case.

**3. Trois positions sont occupées par un seul acteur :**
- **Par taxon** → birdpack (seul). Mais c'est du « workflow ornitho », pas du « regard naturaliste ».
- **Local/brush** → Craig Rogers (seul). Complémentaire, pas concurrent (ça s'ajoute à nos presets).
- **Interactif** → Pose Nature (curseur de quantité) — **mais cassé sur la courbe** (le Amount natif ne scale pas le grading/TSL). Notre slider paramétrique fait mieux sur la même case.

**4. Le trou premium que personne ne sert :**
```
Scénario naturaliste (zoologiste)  ×  Adaptatif (masques IA)  ×  Interactif (curseur proportionnel)
```
Ryan Wilkes a l'adaptatif sans le scénario naturaliste ni le curseur proportionnel.
Pose Nature a le curseur sans l'adaptatif ni la crédibilité zoologiste.
birdpack a le taxon sans l'adaptatif ni l'éthique.
→ **Notre position = la combinaison des trois, sur le créneau « Munier » (poétique, éthique).**

---

## Feuille de route produit (découlée de la carte)

1. **Maintenant** : les 12 presets Scénario (fait) + le **curseur proportionnel** (fait — à documenter comme innovation). ✅ **Validé 16/11** : les 3 piliers (courbe paramétrique + grading + TSL) scalent proportionnellement en production. Le grading passe par les clés legacy `SplitToning*` (le SDK droppe `ColorGrade*`), substituées dans `looks.mjs` — vérifié catalogue + visuel.
2. **Brique 2** : le sélecteur des 12 looks dans le slider (brancher le curseur sur tous les scénarios, pas seulement Fin Art).
3. **Brique 3 (le premium)** : les **masques IA** (sujet/œil/plumage/arrière-plan) — la seule brique que Ryan Wilkes/LSP ont et pas nous. C'est là que se paie le vrai prix ($55+).
4. **Différenciation durable** : la **crédibilité zoologiste + éthique** — intraçable pour les concurrents génériques.
