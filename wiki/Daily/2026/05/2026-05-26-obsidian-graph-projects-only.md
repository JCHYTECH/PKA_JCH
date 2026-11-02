---
date: 2026-05-26
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-26 — obsidian-graph-projects-only

## Session — 12:37 — obsidian-graph-projects-only

### Contexte
- Modèle : codex-gpt-5
- Projet : PKA_JCH

### Résumé
Ajustement de la vue Graphe [[Obsidian]] pour n'afficher que les projets actifs PKA_JCH.

### Actions
- Filtre Graph remplace par path:JCH_Inbox/03_PROJECTS/ -path:JCH_Inbox/03_PROJECTS/[[archive]]/.\n- Conservation des groupes couleur par projet.\n- Masquage maintenu des orphelins.\n- Sauvegarde de la version intermediaire dans .[[Obsidian]]/backups/2026-05-26-graph-project-view/graph-before-projects-only.json.\n- Mise a jour de GL-003 et de wiki/index.md.

### Décisions
La vue Graph globale doit etre strictement projet-only. Les agents, outils IA, Daily, SOPs et autres zones restent disponibles dans le vault mais hors de cette vue.

### Prochaines étapes
Reload [[Obsidian]] et inspecter si certains fichiers non projet restent visibles via liens non resolus ; ajuster hideUnresolved si necessaire.
