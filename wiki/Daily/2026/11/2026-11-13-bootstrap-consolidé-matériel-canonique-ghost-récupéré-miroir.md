---
date: 2026-11-13
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-13 — Bootstrap consolidé, matériel canonique, Ghost récupéré, miroir iCloud

## Session — 22:55 — Bootstrap consolidé, matériel canonique, Ghost récupéré, miroir iCloud

### Contexte
- Modèle : deepseek-v4-pro
- Projet : AI_IT_TOOLS

### Résumé
Session transverse : refonte du bootstrap en assembleur partagé (pka_bootstrap.py) + règle OUTIL ; listes canoniques photo-materiel.md et lupo-materiel.md ; nettoyage Docker HA sur M5 ; récupération du compte Ghost WildLens (pas de recréation) + édition #6 en brouillon ; miroir lecture-seule du PKA vers iCloud pour Obsidian sur l'iMac.

### Actions
- Bootstrap : scripts/pka_bootstrap.py (Config→State→TTD→Log→scans), qwen.py refactoré, dobby.sh (régénération + --quick + codex), AGENTS.md (règle OUTIL + bootstrap consolidé).
- Matériel : photo-materiel.md (R10→R7, Laowa 25mm, 90D conservé) et lupo-materiel.md créés, chargés au bootstrap.
- Infra HA : conteneurs homeassistant/mosquitto/zigbee2mqtt/flaresolverr supprimés, relais MCP lupo + bridge socat désactivés ; RPi HOME + Lupo vérifiés actifs (ping/HA/SSH).
- Ghost WildLens : compte récupéré (essai 14 j), titre+description posés, intégration API + scripts/ghost_import.py, Edition #6 en brouillon (slug wildlens-edition-6).
- iCloud : bin/pka-icloud-mirror (markdown seul, 2657 .md / 24 Mo) + launchd 15 min ; .git.bak-pre-filterrepo 88 Go purgé.

### Décisions
- Ghost : pas de recréation (décision 12/11 annulée) ; domaine final wildlens.arteon.be.
- Miroir Obsidian : lecture seule, pas d'édition depuis l'iMac (éviter les conflits).
- Impression : toujours via bin/pka-print (leçon règle OUTIL).

### Prochaines étapes
- JC : relire le brouillon Edition #6, choisir le plan Starter (~9 $/mois), brancher le domaine wildlens.arteon.be.
- Dobby : pousser les 5 autres éditions en brouillon après relecture.
- iMac : laisser la synchro iCloud se terminer.
