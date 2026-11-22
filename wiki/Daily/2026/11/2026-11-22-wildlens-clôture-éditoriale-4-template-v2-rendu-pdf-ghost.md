---
date: 2026-11-22
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-22 — WildLens — clôture éditoriale #4 + template v2 + rendu PDF Ghost

## Session — 14:14 — WildLens — clôture éditoriale #4 + template v2 + rendu PDF Ghost

### Contexte
- Modèle : deepseek
- Projet : ARTEON

### Résumé
Session ARTEON/WildLens : réconciliation du template éditorial v2 (4 sections Cadre/Virage/Objectif/Constat), correction du script hebdo (fausse alerte), création de la procédure de rédaction + règle double-check Ghost/Markdown, rédaction de l'édition #4 (pigeon ramier, contre-plongée, Constat tourterelle des bois), correction des éditions #2/#3, outil bin/wildlens-ghost-pdf + impression des 4 éditions et du plan d'action. En parallèle : filtre éthique Argus rendu non-bloquant (risque d'artificialité signalé, analyse poursuivie).

### Actions
- Corrigé scripts/wildlens_weekly.py : statut lu depuis le frontmatter, URL Ghost self-host.
- Créé ref/procedure-redaction-edition.md : template Markdown + rôles des sections + double-check Ghost/Markdown.
- Rédigé l'édition #4 (pigeon ramier) : 4 sections, Constat tourterelle des bois (sources Conseil d'État/Légifrance/FACE).
- Corrigé l'édition #2 (mots-clés en tête, crédit espèce, sources section ③).
- Créé bin/wildlens-ghost-pdf (rendu PDF style Ghost) + généré les 4 PDF.
- Imprimé les 4 éditions + le plan d'action (EPSON, recto).
- Mis à jour wildlens/INDEX.md + strategy/plan-action-wildlens.md.
- Modifié le filtre éthique Argus : captive_animal → warning non-bloquant (artificiality_risk transmis à l'analyse).

### Décisions
- Le Constat (④) devient systématique (angle pro-nature / anti-spécisme).
- L'édition #3 (ai-autofocus) reste sur l'ancienne structure 5 sections (assumée telle quelle).
- Template : photo en tête = feature image Ghost, sommaire cliquable = TOC thème — hors Markdown. Double-check Ghost/Markdown obligatoire.
- Rôles des sections : Le Virage = innovation technologique, L'Objectif = sujet technique.
- Argus : le risque d'artificialité est signalé mais ne bloque plus l'analyse.

### Prochaines étapes
- Valider l'édition #4 (JC) → draft → scheduled (cible 12/12) + poser la photo en feature image Ghost.
- Reprendre la cadence hebdo WildLens (samedi).
- Argus : lancer la prochaine fournée d'analyses photo après décision explicite de JC.
