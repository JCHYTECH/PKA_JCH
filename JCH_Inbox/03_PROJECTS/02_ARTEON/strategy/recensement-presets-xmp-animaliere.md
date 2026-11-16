---
date: 2026-11-15
source: dobby
domain: arteon
type: recensement
status: actif
lang: fr
---

# Recensement — Presets XMP photo animalière (marché)

> Scan large des sources de presets Lightroom dédiés à la photo animalière/nature.
> Objectif : cartographier la concurrence, repérer les différenciateurs, et identifier ce qui est réutilisable (avec licence) ou à éviter.

---

## 1. Sources gratuites (XMP/DNG téléchargeables)

| Source | Contenu | Format | Licence réelle | URL |
|--------|---------|--------|----------------|-----|
| **Presetpedia** | 50 Wildlife + 50 Bird presets (Natural Warmth, Vivid, Moody Forest, Cinematic, Vintage, Dark/Night ; Airy/Vivid/Moody Bird…) | XMP | « usage personnel », redistribution non autorisée | presetpedia.com/wildlife-lightroom-presets |
| **PSD Stack (Bunty Pundir)** | 311+ presets gratuits, dont 1 « Wildlife » | XMP + DNG + LRTemplate | usage personnel | psdstack.com |
| **Northlandscapes (J. E. Waider)** | 40+ presets paysage (7 commandés par Adobe Create) | XMP | gratuit, usage perso | northlandscapes.com |
| **mhrcreator / YouTube** | presets gratuits à mot de passe (DNG/XMP) | DNG/XMP | faible qualité, spammy | à éviter |

→ **Constats** : abondance de presets « animalier générique » gratuits, mais aucun n'est *curé par un zoologiste*, aucun ne documente la courbe tonalité / TSL / grading. Qualité inégale, pas d'éthique, pas de taxonomie.

---

## 2. Sources payantes (premium)

| Produit | Prix | Contenu | Différenciateur |
|---------|------|---------|-----------------|
| **Wild Edits — Ryan Wilkes** | 55 $ | 30 presets dont **15 « Adaptive » avec masques IA intégrés** | Masques IA = la vraie valeur premium |
| **birdpack™ — birdspot** | ~50-80 $ | **190+ presets par espèce** (24 taxons) + 40 « Moods » | Approche **par taxon** (Kingfishers, Owls, Raptors…) |
| **Pose Nature (FR)** | ~30-60 € | 50 presets wildlife, styles **Vincent Munier / Ansel Adams / Serge Ramelli**, avec **« curseur de quantité »** | **Slider d'intensité** + référence FR |
| **Wild Spirit — LSP Actions** | ~40-80 $ | **330 presets + 88 masques** | Volume + masques |
| **Woodland Presets** | 219 $ (méga bundle 184 packs) | bundles massifs nature/faune | Volume, low-cost par preset |
| **Craig Rogers Photography** | 20 €/pack | **20 Brush presets** oiseaux (Feather Detailer, Perch Detailer, Saturation Pop) | Presets **pinceau** (localisés), pas globaux |

---

## 3. Le signal Vincent Munier

**Munier** = la référence absolue de la photo animalière française « poétique » : neige, atmosphère, animal intégré au paysage, lenteur, respect du sujet (Eric Hosking Award ×3).

→ Pose Nature vend un preset « Style Vincent Munier ». C'est **exactement le créneau esthétique d'ARTEON** (naturaliste poétique, « Fin Art », l'animal dans son milieu, pas le trophée). Ce créneau a une **demande nommée**, mais personne ne le sert avec :
1. une vraie **crédibilité zoologiste** (taxonomie, comportement),
2. un **curseur global proportionnel** qui fonctionne (voir §4),
3. une **éthique documentée** (pas d'appâtage, pas d'IA).

---

## 4. Implication pour ARTEON — le différenciateur

**Le « curseur de force globale » n'est PAS unique** : Pose Nature commercialise déjà un « quantity slider ». ⚠️ **Corrigé 16/11** : le curseur Amount natif scale en réalité les réglages de base, la TSL, le grain **et la saturation du grading** (mesuré, `SplitToningShadowSaturation 10→5→0→20`) — il ne fige que la **teinte** du grading et la **courbe de points**. La « supériorité sur le Amount natif » ne tient donc pas sur le grading (il le scale aussi) : notre vraie distinction est (1) une **courbe paramétrique scalable** (le Amount fige la courbe de points) et (2) un **invariant documenté et contrôlable**, pas une boîte noire. ✅ **Vérifié 16/11** : le grading est livré par les clés legacy `SplitToning*` (le SDK droppe les roues `ColorGrade*`) — substitution dans `looks.mjs`, confirmée en catalogue + visuel. Les 3 piliers (courbe paramétrique + grading + TSL) sont mesurés.

**Ce qu'on peut faire sans risque de licence :**
- Étudier la *structure* des packs (par taxon, par mood, par scénario) → on l'a déjà (12 scénarios).
- S'inspirer des *noms de looks* qui marchent (Cinematic, Moody, Vivid, Golden) → on les a déjà.

**Ce qu'on ne peut PAS faire sans accord écrit :**
- Inclure des XMP tiers dans notre plugin/pack (Presetpedia, PSD Stack, Pose Nature, Ryan Wilkes, Birdpack sont tous propriétaires — « usage personnel, pas de redistribution »).
- Seul un XMP sous licence explicite (CC0, CC-BY) ou un accord d'auteur écrit le permettrait. → **Renard** pour le cadrage si on veut en intégrer.

---

## 5. Recommandation

1. **Ne pas réutiliser de XMP tiers** — notre différenciation est précisément le regard zoologiste curé, pas l'agrégation de presets génériques.
2. **Garder l'angle « Munier »** comme positionnement nommé (poétique, neige, atmosphère) — c'est le créneau premium non servi.
3. **Protéger le curseur proportionnel** comme innovation (le slider Amount natif est cassé pour la courbe — nous on le fait bien).
4. **Le premium se joue sur les masques** (Ryan Wilkes, LSP) — prochaine brique produit après le slider.
