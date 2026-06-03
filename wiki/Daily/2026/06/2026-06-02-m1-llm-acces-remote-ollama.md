---
date: 2026-06-02
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-06-02 — m1-llm-acces-remote-ollama

## Session — 20:29 — m1-llm-acces-remote-ollama

### Contexte
- Modèle : GPT-5
- Projet : AI_IT_TOOLS

### Résumé
Session centrée sur l'accès distant au Mac M1 dédié LLM locaux et la documentation des connexions machines.

### Actions
Accès SSH au M1 validé via m1@100.73.212.110 ; Partage d'écran VNC validé via open vnc://100.73.212.110 ; Ollama vérifié localement sur le M1 ; test d'inférence llama3.2:3b OK ; PATH Ollama configuré dans ~/.zshenv ; création de CONNEXIONS.md et MODE_EMPLOI_M1_LLM.md ; mise à jour M1_LLM_ACCESS.md et INDEX.md.

### Décisions
Le M1 reste administré via SSH, VNC/Tailscale et VS Code Remote-SSH ; Ollama n'est pas exposé directement sur Tailscale, usage recommandé via SSH ou tunnel local ; pour le RPi, JCH privilégie iPad + Raspberry Pi Connect pour l'accès visuel, et SSH/web pour l'administration depuis M5.

### Prochaines étapes
Tester VS Code Remote-SSH vers m1@100.73.212.110 en usage réel ; ajouter une note Raspberry Pi Connect dans CONNEXIONS.md si JCH confirme la procédure iPad ; maintenir les fiches d'accès sans secrets en clair.
