```yaml
---
date: 2026-06-05
type: journal
author: Sybil
tags: [infra, agents, documentation, systèmes, données]
---

# Journal du 5 juin 2026

## Infrastructure et Systèmes

Activité importante sur la pile technique. Dobby a subi une vérification d'état complète (`2026-06-05_dobby_system_check.md`), avec génération d'un rapport dans les archives d'équipe. Les logs de système révèlent une surveillance continue (`system_check_state.json`, `dropbox-watch.log`, `plane-autostart.log`).

Configuration Raspberry Pi et iPad mise à jour : documentation VNC centralisée (`docs/rpi-ipad-vnc-setup.md`) et guide Termius pour macOS/iPad (`docs/termius-mac-ipad.md`). L'infrastructure VNC semble être un point de travail stabilisation.

## Agents et Modèles

Révision documentaire complète des agents IA :
- `DEEPSEEK.md` — modifié
- `QWEN.md` — modifié
- `CLAUDE.md` — modifié
- `GEMINI.md` — modifié
- `AGENTS.md` — document de synthèse mis à jour

Plusieurs sessions de travail tracées (`session_20260605_110600.json`).

## Mémoire et Archivage

`MEMORY.md` mis à jour — central pour la continuité contextuelle. Wiki synchronisé (`wiki/index.md`, `wiki/log.md`).

## Données et Graphe

Génération complète du graphe de connaissance :
- `graphify-out/graph.html` — visualisation
- `graphify-out/graph.json` — données structurées
- `graphify-out/GRAPH_REPORT.md` — analyse

## Dobby (Modèle Local)

Entraînement actif du modèle LoRA Dobby sur M1 :
- Dataset segmenté : `dobby-dataset/train.jsonl`, `dobby-dataset/valid.jsonl`
- Checkpoint récent : `dobby-lora/0000150_adapters.safetensors`
- Log de sauvegarde : `backup_pka_m1.log`
- Configuration système : `com.dobby.retro.plist`
- Script d'installation/démarrage : `bin/install-dobby-retro.sh`

État : modèle en itération, snapshot d'entraînement capturé.

## Synchronisation Équipe

Base de données centralisée `TEAM/team.db` mise à jour. Monitoring Dropbox synchronisé (`dropbox_vetalyx_changes.log`, `dropbox_vetalyx_snapshot.json`). `.gitignore` ajusté pour filtrage des artefacts locaux.

## Tâches

Inbox personnel et collectif mis à jour : `JCH_Inbox/todo-jch.json` et `JCH_Inbox/todo-jch.html` reflètent l'état courant.

---

**Synthèse** : Jour d'intégration infrastructure — stabilisation des systèmes distribués (VNC, Dropbox, Dobby), mise à jour documentaire complète des agents IA, et progression continue sur l'entraînement local du modèle. Le graphe de connaissance a été régénéré.

```