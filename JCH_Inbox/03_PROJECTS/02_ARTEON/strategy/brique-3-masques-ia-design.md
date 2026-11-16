---
date: 2026-11-16
source: dobby
domain: arteon
type: design
status: actif
lang: fr
---

# Brique 3 — Masques IA animaliers (design + brief Forge)

> Dobby 🦉 — 2026-11-16 · Suite P1, item 6. Design issu des 2 transcripts masquage (Simon d'Entremont,
> Steve Perry/Backcountry) + de la carte produit (`cartographie-fonctionnelle-presets.md`).
> Objectif : la seule brique que Ryan Wilkes / LSP ont et pas nous — celle qui justifie le prix premium.

---

## 1. Le constat qui justifie la brique

Les deux pros le disent : **« sélectionner le sujet » déborde** (le masque mord sur l'arrière-plan,
les ailes, l'espace entre les pattes). Personne ne vend un preset qui *tient compte de ce défaut*.
Notre différenciateur : livrer non pas des masques bruts, mais un **workflow de masques raffinés,
calibrés animalier**, avec recette par zone.

---

## 2. Les 4 masques cibles (ordre d'application)

| # | Masque | Sélection | Réglages par défaut | Usage animalier |
|---|--------|-----------|---------------------|-----------------|
| 1 | **Sujet** | « Sélectionner le sujet » → raffinage | +expo 0.2–0.5, +contraste (compense la perte de détail), −highlights | détacher l'animal du fond |
| 2 | **Œil** | sujet ∩ pinceau (ou ∩ luminance haute) | +expo, +clarté, +netteté | le point d'accroche du regard — oiseaux, mammifères |
| 3 | **Plumage / pelage** | sujet ∩ plage de luminance | +texture, +netteté, ±saturation ciblée | dompter les hautes lumières du plumage sans toucher le fond |
| 4 | **Arrière-plan** | « Sélectionner l'arrière-plan » | −expo, −texture, temp/tint (chaud/froid) | faire respirer le sujet, isoler |

**Le primitif clé = l'intersection** (`sujet ∩ X`) : c'est elle qui transforme un masque global
en masque localisé sans overspray (ex. héron : « sujet ∩ pinceau » pour les hautes du plumage).

---

## 3. Le workflow de raffinage (obligatoire, intégré)

1. Baisser l'**opacité de l'overlay** (réglages couleur) pour voir ce qui est réellement sélectionné.
2. Basculer **O** pour vérifier / masquer l'overlay.
3. **Soustraire au pinceau** les zones mordées (ailes, fond).
4. `AutoMask` (pinceau) pour rester « dans les lignes » sur les bords sujet/fond.
5. `Object mask` détourné pour isoler une partie du sujet.

---

## 4. Recettes naturalistes nommées (différenciateurs)

### 4.1 — « Plumage clair — anti-coulée » (la plus forte, absente du marché)
Tout oiseau blanc ou animal noir sous ciel bleu porte une dominante bleue (réflexion du ciel).
- Correctif : **masque plage de couleur** → désaturer le bleu → réinjecter un peu de jaune (au couchant).
- Pendant : « sujet sombre » (même cause sur les corvidés/rapaces).

### 4.2 — « Sculpture de lumière » (dodge & burn local)
Radial gradient **dupliqué** sur les zones moins éclairées (rochers, creux) — même effet, même force.
Sert à restituer « ce que l'œil a vu », pas à inventer de la lumière.

### 4.3 — « Œil vivant »
sujet ∩ pinceau sur l'œil → +expo +clarté +netteté. Le point qui fait « la photo animalière réussie ».

---

## 5. Contraintes SDK (à trancher AVANT de coder)

- La copie locale du MCP Lightroom est en **0.4.1** ; l'upstream est à **0.27.0** et a ajouté un
  toolset `masks`, un `create_develop_preset`, et les courbes de points.
- → **Évaluer la montée upstream 0.27.0** avant d'écrire des masques à la main. Cf. `2026-11-16_probleme-colorgrade-sdk-lightroom.md` (point d'attention connexe).
- Les masques IA ne sont pas livrables par `set_develop_settings` seul ; il faut le toolset masks
  ou `applyDevelopPreset` avec un XMP portant les masques.

---

## 6. Brief Forge (à planifier après feu vert JC)

**Livrable** : brique 3 = 4 masques + workflow de raffinage + 3 recettes nommées (§2–§4).

**Ordre conseillé** :
1. Monter le MCP upstream (0.4.1 → 0.27.0), vérifier le toolset `masks` + `create_develop_preset`.
2. Prototyper « sujet ∩ pinceau » sur une photo test (héron ou oiseau en vol), mesurer l'overspray résiduel.
3. Caler les réglages par défaut des 4 masques (§2) sur des RAW réels (pas de vote, pas de généralisation sans données).
4. Implémenter la recette « anti-coulée » (§4.1) comme preset de masque réutilisable.
5. Livrer un preset de masque par zone + la doc d'usage (ordre, raffinage, quand ne PAS l'appliquer).

**Garde-fous** :
- Toute modif du plugin exige Reload Plug-in + Start Server (ou redémarrage Lightroom).
- Ne pas dépendre de clés non documentées (API develop settings « experimental »).
- Réversibilité : tout doit rester annulable via git.
- Aucun achat ni montage — c'est du code, testé sur des photos déjà présentes.

**Spécialiste** : Forge (code) + Argus (calibration photo) + Dobby (orchestration).

---

*Découle de : `TEAM_Inbox/2026-11-16_dobby_synthese-enrichissement-xmp-plugin-animalier.md` (rec. 6).*
*Sources : transcripts masquage routés dans `02_ARTEON/99_REFERENCES/lightroom-technique_2026-11-16/`.*
