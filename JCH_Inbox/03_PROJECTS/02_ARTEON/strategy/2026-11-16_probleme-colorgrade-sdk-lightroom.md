# Prompt — Problème ColorGrade du SDK Lightroom & objectif de départ

> ✅ **RÉSOLU le 16/11** — le grading est récupéré par substitution `ColorGrade*` → `SplitToning*` (clés legacy supportées par le SDK). `looks.mjs` corrigé, vérifié en catalogue + visuel. Voir § Résolution en fin de document.

> Dobby 🦉 — 2026-11-16 · Prompt de travail issu de la **proposition 1** (test falsifiable du curseur proportionnel).
> Destinataire : Forge / Argus (ou tout modèle/session reprenant le chantier).
> Contexte projet : stratégie plugin Lightroom ARTEON/WildLens — presets « Naturaliste » + curseur paramétrique MCP.

---

## Contexte

La brique 1 de la stratégie presets revendique un « curseur proportionnel » qui scalerait
**la courbe, le grading et la TSL** là où le Amount natif de Lightroom ne le ferait pas.
La proposition 1 a mesuré cette revendication en production (copie virtuelle d'un geai,
3 looks × 7 forces, relecture SDK complète).

## Le problème

Le scaling proportionnel fonctionne **pour 2 des 3 piliers**, et est **cassé pour le 3ᵉ** :

1. ✅ **Courbe paramétrique** (`ParametricShadows/Darks/Lights/Highlights`) : scale exactement base×force, appliquée fidèlement.
2. ✅ **TSL** (`HueAdjustment*`, `SaturationAdjustment*`, `LuminanceAdjustment*`) : idem, proportionnel et fidèle.
3. ❌ **Grading (ColorGrade, les roues)** : `ColorGradeShadowSat`, `ColorGradeShadowHue`, `ColorGradeHighlightSat`,
   `ColorGradeHighlightHue` sont **ignorées silencieusement** par `set_develop_settings` → `applyDevelopSettings()`.
   Seul `ColorGradeBlending` (un paramètre de mélange, sans effet sans roues) survit.

**Preuves :**
- Relecture `getDevelopSettings()` : les 4 clés roues absentes, seul `ColorGradeBlending` revient.
- Catalogue Lightroom (9 828 photos) : `ColorGradeShadowSat/Hue/HighlightSat` = **0 occurrence**,
  alors que `ColorGradeMidtoneSat/GlobalSat/Blending` = 9 828 (défauts stockés partout).
  → `applyDevelopSettings()` droppe les roues ombre/haute lumière.

## Analyse élargie — le problème est-il déjà connu ?

**Oui, c'est une limite connue et documentée du SDK Adobe, pas un bug de notre code :**

- Adobe marque l'API develop settings comme **expérimentale** : « You should not depend on the
  contents of the settings table remaining compatible in future versions. The definitive list is
  the one shown in the UI. » (doc `LrPhoto:getDevelopSettings()`).
- Le changelog officiel « Changes to the Lightroom SDK 11 » (johnrellis, forums Adobe) ne mentionne
  **aucune** clé ColorGrade par roue — ni ajout, ni retrait.
- La liste reverse-engineered de référence (kevinkiklee/adobe-plugin-skills) n'expose que la **roue
  globale** (`ColorGradeGlobalSat`, `ColorGradeGlobalLum`, `ColorGradeBlending`) — pas les roues
  ombre / ton moyen / haute lumière.
- Dans le repo upstream `Automaat/lightroom-mcp` : **0 issue** contenant « ColorGrade », mais
  **88 issues** sur « develop settings » (le domaine est actif et connu comme limité).

**Point d'attention connexe :** notre copie locale du MCP est **0.4.1**, alors que l'upstream est
à **0.27.0** et a ajouté un toolset `masks` (masques IA), un outil `create_develop_preset`, et la
gestion des courbes de points (`ToneCurvePV2012` en tableau plat). Avant tout correctif lourd,
vérifier si une mise à niveau upstream règle déjà une partie du problème.

**Piste de traitement identifiée :** le SDK expose
`catalog:applyDevelopPreset(photos, preset, plugin, presetAmount 0–200, updateAISettings)` — c'est-à-dire
un **`presetAmount`** (le « Amount » natif) **et** la possibilité d'appliquer un preset XMP complet
(qui, lui, peut porter le grading). Or l'outil MCP `apply_develop_preset` n'expose que
`photo_ids` + `preset_name`. → Le grading est peut-être livrable par preset, mais **pas** par
`set_develop_settings`.

## Objectif de départ

Trancher puis exécuter, dans cet ordre :

1. **Décider A vs B** :
   - **A — Assumer 2 piliers sur 3.** Retirer les clés `ColorGrade*` de `scripts/looks.mjs`,
     repositionner la revendication sur « courbe paramétrique + TSL proportionnelles »,
     documenter l'absence de grading.
   - **B — Récupérer le 3ᵉ pilier.** Vérifier si `apply_develop_preset` (+ `presetAmount`) livre
     le grading et/ou le Amount natif, puis exposer ce paramètre dans le MCP.
2. **Évaluer la mise à niveau upstream** (0.4.1 → 0.27.0) et ses implications (masques IA, courbes
   de points) avant d'investir du code dans la copie locale.
3. **Livrer une décision argumentée**, pas un correctif silencieux : le verdict alimente le
   repositionnement produit (cf. conseil du 2026-11-16).

## Contraintes / garde-fous

- Ne pas dépendre de clés non documentées : l'API develop settings est « experimental », le définitif est l'UI.
- Ne pas réinventer : tester d'abord `applyDevelopPreset(presetAmount)` et la mise à niveau upstream.
- Toute modification du plugin exige Reload Plug-in + Start Server (ou redémarrage Lightroom).
- Ne pas conclure sur une seule valeur : recouper read-back SDK + catalogue `.lrcat` + XMP.
- Réversibilité : les modifications de `looks.mjs` et du plugin doivent rester annulables via git.

## Résolution (16/11)

Le problème est **résolu en faveur de B, version triviale** :

1. **Diagnostic exact** : le SDK Lightroom droppe les roues `ColorGrade*` (shadow/highlight hue+sat), mais **applique** les clés legacy `SplitToning*` (qui désignent les mêmes roues en interne). Nos presets XMP portaient déjà le grading deux fois — `crs:ColorGrade*` et `crs:SplitToning*`, mêmes valeurs.
2. **Correctif** : substitution dans `scripts/looks.mjs` — `ColorGradeShadowHue/Sat` → `SplitToningShadowHue/Saturation`, `ColorGradeHighlightHue/Sat` → `SplitToningHighlightHue/Saturation`, `SCALE_KEYS` mis à jour ; `ColorGradeBlending` conservé (fonctionnel).
3. **Vérification** : isolation live (catalogue 4→5, valeurs exactes 220/10/38/6) + confirmation visuelle des roues Color Grading par JC.
4. **Verdict produit** : différenciateur repositionné sur **3 piliers complets** (courbe paramétrique + grading + TSL), mesurés en production. Reste en suspens : partie C (test du Amount natif, manuelle) et la montée upstream 0.27.0 (masks IA, brique 3), orthogonales.

## Références utiles

- Résultat de la proposition 1 : `_local/lightroom-mcp/tests/strength-sweep/README.md`
- Mesure brute : `_local/lightroom-mcp/tests/strength-sweep/out/sweep-2026-11-16T08-38-18-614Z.json`
- Audit math : `_local/lightroom-mcp/tests/strength-sweep/audit-scale.mjs`
- Conseil stratégique : `TEAM_Inbox/2026-11-16_dobby_conseil_wildlens-plugin-lightroom.md`
- Doc SDK (experimental) : `LrPhoto:getDevelopSettings()` — Lightroom SDK API Reference
- Liste reverse-engineered : github.com/kevinkiklee/adobe-plugin-skills → `lrc-sdk.md`
