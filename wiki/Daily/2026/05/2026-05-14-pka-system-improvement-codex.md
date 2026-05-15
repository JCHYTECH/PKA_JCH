---
date: 2026-05-14
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-14 — pka-system-improvement-codex

## Session — 13:04 — pka-system-improvement-codex

### Résumé
Mise en place du socle transversal d'amélioration PKA: audit système dédié, enrichissement skills, source canonique des pointeurs multi-outils, hook PreToolUse léger, couche instincts, profils de contexte projet, check global consolidé, et promotion semi-automatique instincts->skills avec config et rapport.

### Actions
- Analyse du repo Everything Claude Code et extraction des patterns utiles pour PKA.
- Création du script pka_system_improvement_audit.py avec tests.
- Extension de la table skills et mise à jour de skill_search.py / skill_write.py.
- Enregistrement du skill pka-system-improvement.
- Ajout du hook PreToolUse via pka_pretool_guidance.py.
- Mise en place d'une source canonique pour AGENTS.md / GEMINI.md / DEEPSEEK.md et bloc canonique géré dans CLAUDE.md.
- Création du check global pka_system_check.py.
- Ajout de la couche instincts, des profils de contexte projet, et du job launchd de system check.
- Ajout du promoteur instincts->skills, de sa configuration, et du rapport de promotion.
- Vérifications fraîches répétées jusqu'à obtenir GREEN sur le check global.

### Décisions
- Approche retenue: évolution intermédiaire plutôt qu'architecture lourde type framework complet.
- Les surfaces multi-outils fines sont générées depuis une source canonique unique.
- CLAUDE.md garde son contenu riche mais reçoit un bloc canonique géré.
- La promotion automatique est introduite par petits incréments: d'abord config + rapport, puis visibilité dans le check global.
- Le check global doit rester read-only: il évalue la promotion potentielle sans muter la base.

### Prochaines étapes
- Étape suivante recommandée: brancher la promotion config-driven sur un launchd dédié, séparément.
- Ensuite: envisager décroissance/révision des instincts obsolètes ou contredits.
- En cas de reprise, commencer par relire le dernier rapport instinct_promotion et lancer pka_system_check.py.
