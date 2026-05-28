---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — Skills inventory cross-runtime

## Session — 09:57 — Skills inventory cross-runtime

### Contexte
- Modèle : [[Codex]] CLI / GPT-5
- Projet : PKA

### Résumé
Inventaire des skills locales: dossier AI_IT_TOOLS/internal-agent-governance/skills, plusieurs SKILL.md WildNexus, et bundle .[[Claude]]/claude-video. Aucun skill trouve sous .gemini.

### Actions
- AI_IT_TOOLS contient un registre de skills internes (draft/approved/active).\n- WildNexus contient des SKILL.md d'agents locaux, dont wildnexus-bioacoustics-dsp.\n- .[[Claude]]/claude-video expose une skill autonome pour l'analyse video.\n- .gemini n'a pas de skill detectee dans le scan courant.

### Décisions
Les skills sont dispersées par runtime/projet, donc il faut les inventorier explicitement pour éviter les doublons et les oublis de découverte.

### Prochaines étapes
Si un runtime tiers doit réutiliser une skill PKA, créer soit un mirror, soit une note d'index commune indiquant où elle vit et dans quel contexte elle est valide.
