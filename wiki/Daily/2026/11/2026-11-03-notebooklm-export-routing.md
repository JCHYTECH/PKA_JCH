---
date: 2026-11-03
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-03 — notebooklm-export-routing

## Session — 16:58 — notebooklm-export-routing

### Contexte
- Modèle : deepseek
- Projet : AI_IT_TOOLS

### Résumé
Export NotebookLM (Gemini Notebook) vers PKA : 32 fichiers telecharges via notebooklm-py, routes vers 6 projets.

### Actions
nlm (notebooklm-py) installe + authentification Google ; 32 artefacts telecharges (presentations, rapports, infographies, mind-maps, flashcards, audio) ; 19 dossiers notebook routes vers 03_WILDNEXUS (6), 07_TRAVELS (7), 08_VETALYX (2), 05_PHOTO_AI_JURY (1), 06_PHOTO_NATURE (2), 02_ARTEON (1) ; script scripts/notebooklm_export.py conserve.

### Décisions
Acces via notebooklm-py (reverse-engineer) car API NotebookLM Enterprise-only ; export = derniere version par type (limite CLI) ; dossier notebooklm/ par projet.

### Prochaines étapes
Recuperer manuellement les 2 artefacts 'file' (PDF non exportables via CLI) ; renommer le dossier 'lectricit-en-van-am-nag' ; verifier placement Gpi Marketing (02_ARTEON) et Langage des Vivants (06_PHOTO_NATURE).
