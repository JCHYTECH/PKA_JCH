---
date: 2026-05-26
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-26 — session-obsidian-graph-vscode

## Session — 13:25 — session-obsidian-graph-vscode

### Contexte
- Modèle : codex-gpt-5
- Projet : PKA_JCH

### Résumé
Session de configuration [[Obsidian]] du vault PKA_JCH : installation du noyau de plugins, procedure de travail [[Obsidian]]/VS Code, puis recentrage de la vue Graphe sur les projets uniquement.

### Actions
- Installation et activation de Dataview, Templater, QuickAdd, Linter et [[Obsidian]] [[Git]].\n- Configuration [[Obsidian]] : notes par defaut vers JCH_Inbox/00_INBOX, attachments vers wiki/images, Daily Notes et templates PKA.\n- Creation de templates [[Obsidian]] pour Daily, Knowledge, SOP, Workstream et Inbox.\n- Creation du dashboard Dataview wiki/INDEX-dashboard.md.\n- Creation de SOP-006 pour travailler avec [[Obsidian]] et VS Code sans collision.\n- Modification de la vue Graphe globale : filtre projets uniquement path:JCH_Inbox/03_PROJECTS/ -path:JCH_Inbox/03_PROJECTS/[[archive]]/.\n- Masquage des liens non resolus pour retirer les noeuds gris fantomes.\n- Documentation dans GL-003 et sauvegardes des versions graph precedentes dans .[[Obsidian]]/backups/.

### Décisions
- [[Obsidian]] est le cockpit humain, VS Code l'atelier technique, [[Codex]]/[[Dobby]] l'operateur documentaire.\n- La vue Graph globale doit etre projets uniquement.\n- Les agents et outils IA restent dans le vault mais hors vue globale.\n- Linter reste installe mais sans lint automatique tant qu'il n'a pas ete teste sur un petit lot.

### Prochaines étapes
- Reload [[Obsidian]] si la configuration Graph ne se met pas a jour.\n- Inspecter visuellement la vue Graph projets uniquement.\n- Tester Dataview via wiki/INDEX-dashboard.md.\n- Tester Linter sur 5 notes non critiques avant usage large.
