---
date: 2026-11-20
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-20 — WildLens passe en francais + clipper iPad

## Session — 12:16 — WildLens passe en francais + clipper iPad

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 02_ARTEON

### Résumé
Deux chantiers menés. (1) ARTEON/WildLens : renumérotation Ghost éclaircie (#4→#1, #1→#3, ancienne #3 supprimée), structure 02_ARTEON nettoyée (editions/final/ + fr/, datés archivés, passe-utile routé, credentials et INDEX à jour), thèmes+keywords harmonisés, puis pivot stratégique : WildLens bascule en français (audience francophone première cible). 3 éditions traduites FR et réimportées dans Ghost, thème FR déployé sur le VPS, locale fr + dates françaises, légende Instagram FR. (2) AI_IT_TOOLS : chaîne clipper iPad → vault iCloud « PKA Capture » → pull M5 (bin/pka-clip-pull, launchd 15 min).

### Actions
- Résolu la renumérotation WildLens (renumber_wildlens.py) : #4→#1, #1→#3, ancienne #3 supprimée
- Nettoyé 02_ARTEON : editions/final/ (3 fichiers alignés Ghost) + fr/, datés archivés, passe-utile routé (Argus→05_PHOTO_AI_JURY, notebooklm→99_REFERENCES), clé Ghost obsolète marquée, INDEX + photos README à jour
- Harmonisé : ligne Theme sous la photo, keywords en fin d'édition, français résiduel corrigé
- Traduit les 3 éditions EN→FR (fr/), réimporté dans Ghost (titres « Édition #N »)
- Déployé le thème FR sur le VPS (deploy@2.25.8.208), locale fr, description « sans fard »
- Légende Instagram FR (édition manuelle — l'API Graph ne permet pas la modification de légende publiée)
- Créé bin/pka-clip-pull + launchd 15 min (clipper iPad → inbox)

### Décisions
- Pivot WildLens → tout en français : FR pour le lancement, EN en réserve, IT plus tard ; pas de compte Instagram séparé par langue tant que pas de traction
- Renumérotation éditions : #1=rouge-gorge, #2=gannet, #3=AI autofocus ; provenance « Was this real? » retirée
- Garder la citation FR « modestement, recoudre » comme marqueur d'identité ARTEON
- Clipper iPad : vault iCloud « PKA Capture » + pull one-way (miroir lecture seule), pas de synchro bidirectionnelle

### Prochaines étapes
- Recoller le hashtag #photographyethics (coupé au collage Instagram) d'un bloc
- Renouveler le token Instagram avant le 04/01/2026 (60 j)
- FR/IT (Jade) différé ; changeur de langue non prioritaire (tout-FR pour l'instant)
- Relecture JC des éditions #2 (05/12) et #3 (28/11) avant publication
