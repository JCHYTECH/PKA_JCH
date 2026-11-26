---
date: 2026-11-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-25 — Harnais PKA (cartographie + routage consolidé) et WildLens 3 sections

## Session — 00:52 — Harnais PKA (cartographie + routage consolidé) et WildLens 3 sections

### Contexte
- Modèle : deepseek
- Projet : AI_IT_TOOLS

### Résumé
Session dense sur le concept de harnais. (1) WildLens : 4 éditions restructurées en 3 sections (Cadre/Constat/Actualité technique, mots-clés en fin) après panel lecteurs ; anciennes versions archivées ; docs et script wildlens_weekly.py mis à jour. (2) M1 vérifié en direct (Wi-Fi, pas d'Ethernet), remonté à l'étage, Ollama opérationnel. (3) Hammerspoon étendu (déplacement fenêtre en plus du curseur). (4) Analyse du transcript 'Comprendre la puissance du Harnais' (Varoqueaux) -> knowledge + USER.md. (5) Cartographie du harnais (harnais-pka.md). (6) Routage modèles consolidé en source unique (models-routing.json + pka_model_router.py, model_config.json archivé). (7) Catalogue ~65 opérations (catalogue-operations.md) imprimé.

### Actions
- WildLens éditions 1-4 -> 3 sections (Cadre/Constat/Actualité technique), mots-clés en fin ; archive _archive/2026-11-24_avant-restructuration-3-sections/ ; docs ref (architecture-editoriale-v2.md v3, procedure-redaction-edition.md, INDEX.md) et scripts/wildlens_weekly.py mis à jour. - hardware-state.md : Hammerspoon (curseur + fenêtre) + état M1. - ~/.hammerspoon/init.lua : déplacement fenêtre ajouté. - TEAM_Inbox analyse harnais + routage 99_REFERENCES/harnais_2026-11-24/. - team.db knowledge #55 #56 + USER.md (section harnais). - docs/system/harnais-pka.md, models-routing.json v2 (source unique), pka_model_router.py, model_client.py re-pointé, model_config.json archivé, or_route.py noté. - docs/system/catalogue-operations.md (~65 opérations) imprimé (job EPSON 549).

### Décisions
- WildLens : 3 sujets par numéro (panel lecteurs 24/11) — Cadre / Constat / Actualité technique, mots-clés en fin. - PKA est un harnais ; seul maillon non possédé = runtime DeepSeek TUI (gardé). - Routage modèles : source unique docs/system/models-routing.json. - Interface : rester sur la vision dashboard web (Hub JCH).

### Prochaines étapes
- Câbler le Hub : snapshot -> radar + 5 boutons self-service (inbox/route, transcript, imprimer, recherche, save). - WildLens #3 : combler photo Cadre + Constat ; vérifier URLs FAO/UNEP (Constat #2). - M1 : brancher Ethernet (dialogue ASIX) + finaliser rotation secrets. - Brancher pka-snapshot au radar du Hub.
