---
date: 2026-06-03
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-06-03 — Correction clé DeepSeek TUI

## Session — 23:18 — Correction clé DeepSeek TUI

### Contexte
- Modèle : codex
- Projet : AI_IT_TOOLS

### Résumé
Diagnostic de deepseek-tui après erreur de clé API invalide. La clé exportée dans ~/.zshrc était obsolète, tandis qu'une clé valide existait déjà dans ~/.config/pka-jch/api_keys.

### Actions
Test deepseek-tui doctor; tests API DeepSeek /models, /chat/completions et /user/balance; remplacement du chargement DeepSeek dans ~/.zshrc par le fichier secret existant; bascule du modèle par défaut vers deepseek-v4-flash dans ~/.deepseek/config.toml, bin/dobby.sh et scripts/deepseek_chat.py; vérification finale doctor et lancement scripts/deepseek_chat.py.

### Décisions
Ne plus stocker la clé DeepSeek en clair dans ~/.zshrc; utiliser ~/.config/pka-jch/api_keys comme source locale; préférer deepseek-v4-flash à deepseek-chat car l'alias deepseek-chat est annoncé comme retiré le 2026-07-24.

### Prochaines étapes
Relancer deepseek-tui depuis un nouveau Terminal si besoin; surveiller les futurs changements de modèles DeepSeek; garder les sauvegardes ~/.zshrc.bak-20260603-deepseek-key et ~/.deepseek/config.toml.bak-20260603-deepseek-chat jusqu'à confirmation durable.
