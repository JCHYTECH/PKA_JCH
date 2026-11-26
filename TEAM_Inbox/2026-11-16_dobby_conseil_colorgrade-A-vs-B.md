# Conseil — ColorGrade : option A vs option B

> Dobby 🦉 — 2026-11-16 · Conseil complet (6 stances : Contrarian, Premiers Principes, Expansionniste, Outsider, Prémortem, Méthodologiste) en parallèle.
> Décision : grading (ColorGrade) ignoré par le SDK Lightroom — (A) assumer 2 piliers/3, ou (B) récupérer le 3ᵉ via applyDevelopPreset + presetAmount / presets XMP.

---

## VERDICT

**Recommandation : CONDITIONNEL — A par défaut, MAIS exécuter d'abord 2 tests falsifiables à 15 min qui peuvent basculer vers B.**

**Arguments pour A (le défaut) :**
1. B repose sur une chaîne non vérifiée (preset XMP → applyDevelopPreset → moteur) ; la preuve « 0/9 828 » mesure le pipeline entier, pas la capacité du SDK.
2. `presetAmount` (0–200) est un fondu **global**, pas un axe paramétrique → double comptage avec notre scale par clé ; le curseur deviendrait un interrupteur à crans.
3. Fork (0.4.1 vs 0.27.0) + SDK « expérimental » = bus factor 1, échec silencieux.
4. Le premium réel = **masques IA (brique 3)**, pas le grading.

**Arguments contre A / pour tester B :**
1. Le grading peut être « déplacé » dans le preset XMP (interprété nativement par Lightroom, hors getters/setters) — vérifiable par `grep crs:ColorGrade` en 2 min.
2. Retirer un pilier sur une preuve qui confond pipeline et SDK = risquer de jeter un pilier pour un bug de mapping local.
3. `presetAmount` est conceptuellement le bon opérateur (scaling de bloc entier = la sémantique du curseur).

**Objection la plus forte :** Méthodologiste — « la preuve 0/9 828 confond pipeline et SDK ; on risque de retirer un pilier pour un bug local ». **Réponse :** acceptée — 2 tests d'isolation avant toute suppression de clé.

**Résidu de risque (A) :** même en A, il faut un test anti-régression qui échoue si `ColorGrade*` réapparaît (Contrarian) + corriger la communication « 3 piliers » (Premiers Principes : on promet un invariant — curseur monotone réversible — pas trois widgets).

**Dissent :** Expansionniste maintient que B change la nature du produit — les presets XMP sont **portables**, découplés du plugin, et deviennent l'unité de revenu (packs par genre) ; B mérite un *spike*, pas un fork.

---

## Actions immédiates (découlées du conseil)

1. `grep crs:ColorGrade` sur un preset XMP exporté — le grading est-il dans le preset ? (2 min)
2. Isolation : `applyDevelopSettings` avec `ColorGrade*` sur un catalogue jetable à 1 photo + relecture — le SDK droppe-t-il vraiment ? (1 h)
3. Décider la montée upstream **0.27.0** (masks IA = brique 3) **séparément** du chantier grading.
4. Si B est confirmé → exposer `presetAmount` ou utiliser `apply_develop_preset` (pas un fork complet).

---

*Verrouillé par Dobby 🦉 — les critiques conseillent, Dobby tranche. Pas de débat entre stances.*

---

## RÉSOLUTION (16/11 — exécution du verdict)

Les 2 tests falsifiables exécutés → **B est confirmé, en version triviale (ni fork ni presetAmount)** :

1. `grep crs:ColorGrade` sur nos presets XMP : le grading est **déjà encodé deux fois** — clés `ColorGrade*` (droppées par le SDK) **et** clés `SplitToning*` (legacy, dans l'allowlist SDK), avec les mêmes valeurs (220/10, 38/6).
2. Isolation live : `set_develop_settings` avec `SplitToningShadowHue/Saturation` + `SplitToningHighlightHue/Saturation` → le **catalogue les enregistre** (count 4→5, valeurs exactes 220/10/38/6), alors que `ColorGradeShadowSat/Hue` restent à 0.

**Correctif appliqué à `scripts/looks.mjs`** : `ColorGradeShadowHue/Sat` → `SplitToningShadowHue/Saturation`, `ColorGradeHighlightHue/Sat` → `SplitToningHighlightHue/Saturation`, `SCALE_KEYS` mis à jour. `ColorGradeBlending` conservé (fonctionnel). Le look émet désormais les clés SplitToning, qui passent le SDK.

**Verdict final :** le 3ᵉ pilier (grading) est récupéré par une simple substitution de clés. Reste (optionnel) une confirmation visuelle que les roues Color Grading reflètent bien les valeurs SplitToning dans l'UI Lightroom 15.
