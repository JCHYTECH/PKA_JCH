---
date: 2026-05-30
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-30 — session-deepseek-dropbox-sync

## Session — 22:55 — session-deepseek-dropbox-sync

### Contexte
- Modèle : deepseek
- Projet : PKA_SYSTEM

### Résumé
Copie complète du vault vers Dropbox (ditto 2.8 GB). Correction permissions post-sudo (chown). Exclusions Obsidian pour INSECTNET (audio/segments/spectrograms). Décision: Dropbox plutôt qu'iCloud pour stabilité synchro.

### Actions
Copié vault vers ~/Dropbox/PKA_JCH via ditto; chown -R post-sudo; ajout userIgnoreFilters dans .obsidian/app.json; leçon: cp -a incomplet, ditto + sudo requis, Norton a bloqué un exe externe
