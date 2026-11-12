---
date: 2026-11-07
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-07 — Veille DeepSeek V4 et evolution du systeme PKA

## Session — 12:26 — Veille DeepSeek V4 et evolution du systeme PKA

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 01_AI_IT_TOOLS

### Résumé
Session multi-projets. (1) Analyse transcript TV privacy (Samsung/ACR/Clean Your TV) puis integration complete : routing vers 01_AI_IT_TOOLS, 6 connaissances capturees dans team.db, decision 'pas de TV dans Lupo', pointers NEXUS_ACOUSTIC et WILDNEXUS_DEVICE, creation du skill analyse-transcript. (2) Veille DeepSeek : V4 = pro + flash, fin des alias deepseek-chat/reasoner au 24/07/2026, endpoint natif Search/Fetch a 0,75$/1k. Actions : matrice-modeles mise a jour, alias corriges dans 4 fichiers, creation de bin/pka-search (teste), regles AGENTS.md mises a jour (recherche native + sous-agents v4-flash), Tavily marque a reevaluer. (3) Preparation inventaire magazine Photo (projet 12) : CSV + mode d'emploi crees, canal eBay France retenu.

### Actions
- Skill analyse-transcript cree + indexe (skills/INDEX.md)
- Transcript TV privacy route + 6 connaissances team.db + livrable TEAM_Inbox
- Decision 'pas de TV dans Lupo' + pointers NEXUS_ACOUSTIC/WILDNEXUS_DEVICE
- matrice-modeles.md : V4 pro/flash, Qwen 3.6 Plus, recherche native, off-peak
- Alias deepseek-chat/reasoner -> deepseek-v4-pro (config, DEEPSEEK.md, 2 scripts)
- bin/pka-search cree et teste (endpoint natif Search/Fetch)
- AGENTS.md : recherche native + sous-agents v4-flash ; Tavily a reevaluer
- Analyse 3 transcripts SuperAgent -> livrable + 3 connaissances
- Inventaire magazine Photo : CSV + MD prepares (projet 12)

### Décisions
- Pas de TV connectee dans Lupo (local-first)
- Recherche scriptee -> DeepSeek natif (bin/pka-search) ; Tavily conserve pour l'interactif TUI
- Sous-agents -> deepseek-v4-flash (orchestrateur reste en v4-pro)
- Vente Photo : eBay France, etat Bon, pepites a determiner par Dobby

### Prochaines étapes
- Remplir inventaire-photo-magazine.csv (n+annee+etat) -> matrice de prix + strategie vente
- Confirmer poids d'un numero (~350g) et nombre total de numeros
- P1 a trancher : ajouter un mode observation/dry-run aux watch loops (inspire SuperAgent)
