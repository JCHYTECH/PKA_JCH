---
date: 2026-05-11
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-11 — Session [[Codex]]

## Session — 13:25 — Session [[Codex]]

### Résumé
tableau de board

### Actions
- Création du serveur local dashboard PKA sur http://127.0.0.1:8787.
- Ajout de la page modèles avec lancement Terminal par modèle.
- Ajout des couleurs PKA par modèle pour les boutons et fenêtres Terminal.
- Création du thème commun assets/pka-theme.css.
- Transformation du hub en début de poste de pilotage avec métriques dynamiques.
- Ajout des endpoints /api/health, /api/projects, /api/inbox, /api/latest.
- Ajout de scripts/pka_save.py et du bouton Sauver session dans le hub.

### Décisions
- Le dashboard local devient le point d'entrée opérationnel PKA.
- Les lancements de modèles passent par une allowlist serveur locale plutôt que par des fichiers .command depuis le navigateur.
- La palette PKA est centralisée dans un CSS commun.
- La sauvegarde [[Codex]] reste explicite et semi-manuelle, contrairement au /save [[Claude]].

### Prochaines étapes
- Rendre les cartes projets et derniers livrables dynamiques dans le hub.
- Améliorer l'ergonomie du bouton Sauver session si l'usage se confirme.
- Ajouter éventuellement une page dédiée aux derniers livrables TEAM_Inbox.
