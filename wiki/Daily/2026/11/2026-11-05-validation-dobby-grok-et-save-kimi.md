---
date: 2026-11-05
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-05 — validation-dobby-grok-et-save-kimi

## Session — 10:18 — validation-dobby-grok-et-save-kimi

### Contexte
- Modèle : kimi-code
- Projet : 01_AI_IT_TOOLS

### Résumé
Validation du noyau Dobby local avec Grok 4.7 via Codex CLI et OpenRouter, analyse du chantier Instagram/WildLens et création du rituel /save pour Kimi raccordé à la mémoire PKA.

### Actions
Lanceur bin/lancer-grok.command et MCP configurés ; mémoire isolée, délégation et graphify validés ; documentation docs/system/launch-command.md mise à jour et artefacts temporaires supprimés. Accès Instagram/Ghost analysés ; e-mail support envoyé par JC puis chantier mis en pause. Skill Kimi .agents/skills/save/SKILL.md créé, revu indépendamment et chargé avec succès en dry-run.

### Décisions
Grok reste un lanceur séparé et bin/dobby.sh reste inchangé. La mémoire Dobby partagée, et non les transcripts bruts, sert de pont entre runtimes. Le chantier Instagram/Ghost reste en pause dans l’attente du support.

### Prochaines étapes
Essayer le double-clic et le TUI interactif Grok ainsi que l’invocation utilisateur /save dans Kimi. Reprendre Ghost après réponse du support.
