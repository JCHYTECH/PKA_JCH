---
date: 2026-05-28
type: closure-report
status: draft
owner: "[[Dobby]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 1 — Cartographie, stabilisation, gouvernance"
source:
  - "[[AI_System_Blueprint]]"
  - "[[AI_Runtime_Audit]]"
  - "[[AI_Data_Governance]]"
  - "[[Runtime_Service_Register]]"
---

# Phase 1 Closure Report — PKA_JCH

## Décision

La Phase 1 est **clôturable**.

Le système [[PKA_JCH]] a été cartographié, les principaux risques runtime P0 ont été corrigés, et la gouvernance documentaire minimale est en place.

Décision de clôture :

> Ne pas ajouter d'infrastructure Hermes, n8n, Qdrant, Redis, PostgreSQL ou agents persistants avant validation explicite de la Phase technique minimale.

## 1. Livrables produits

| Livrable | Rôle | Statut |
|---|---|---|
| [[AI_System_Blueprint]] | Carte globale du système AI PKA : agents, dossiers, workflows, risques, autonomie. | Créé |
| [[AI_Runtime_Audit]] | Audit du runtime réel : launchd, cron, processus, ports, erreurs, remédiations. | Créé |
| [[AI_Data_Governance]] | Règles documentaires, runtime, secrets, validations humaines. | Créé |
| [[Runtime_Service_Register]] | Registre des services actifs, suspendus, obsolètes et conditions de rollback. | Créé |

## 2. Ce qui a été cartographié

| Domaine | Résultat |
|---|---|
| Agents | 28 membres actifs confirmés depuis `TEAM/team.db` : 27 spécialistes + [[Dobby]]. |
| Runtimes AI | Codex/GPT-5, Claude, Ollama, NVIDIA/DeepSeek, OpenAI, Google et autres providers configurés. |
| Dossiers | Zones critiques, runtime, archives, secrets, [[inbox]] et projets actifs identifiés. |
| Workflows | Inbox, sauvegarde, [[daily]], system check, Dropbox, Gmail, Telegram, Plane, WildNexus, VETALYX. |
| Services | LaunchAgents, cron, Docker/Plane, Ollama, Dropbox client. |
| Risques | Secrets/logs, ports exposés, doublons cron/launchd, token expiré, backups, roster drift. |

## 3. Remédiations P0 effectuées

| Élément | Action | Résultat |
|---|---|---|
| Bot Telegram [[Dobby]] | Rotation token côté JCH, purge logs, ajout d'un filtre de redaction dans `scripts/telegram-bot/bot.py`. | Bot actif, logs sans token détecté. |
| `email_digest.py` | Retrait des entrées cron, `bootout` et `disable` du LaunchAgent. | Service suspendu, plus de déclenchement automatique. |
| `outlook_gatekeeper.py` | `bootout` et `disable` du LaunchAgent. | Service suspendu, plus d'erreur token en boucle. |
| Logs/backups sensibles | `chmod 600` sur fichiers détectés. | Défauts de permissions corrigés. |
| Backup `TEAM/team.db` | Backup frais créé, `scripts/backup_team_db.py` corrigé pour créer en `0600`. | Backup à jour et conforme. |
| `TEAM/ROSTER.md` | Miroir synchronisé avec `TEAM/team.db`. | Audit sécurité sans roster drift. |
| Plane proxy | Ports Docker restreints à `127.0.0.1`; `plane.env` passé en `0600`. | Plane local-only sur `8088` et `4443`. |

## 4. État runtime actuel

### Actif

| Service | État |
|---|---|
| Dashboard PKA | Actif sur `127.0.0.1:8787`. |
| Gmail gatekeeper | Actif. |
| Bot Telegram [[Dobby]] | Actif. |
| Plane | Actif local-only sur `127.0.0.1:8088` et `127.0.0.1:4443`. |
| Ollama | Actif local-only sur `127.0.0.1:11434`. |
| Dropbox client | Actif hors PKA pur. |
| Cron backup/[[Sybil]]/retro/weekly | Actifs. |

### Suspendu

| Service | Raison |
|---|---|
| `email_digest.py` | Contradiction mémoire + token Google expiré + doublon cron/launchd. |
| `outlook_gatekeeper.py` | Token expiré en boucle. |

### Obsolète

| Service | Raison |
|---|---|
| `com.jch.pka.backup` | LaunchAgent pointant vers ancien chemin `Desktop/PKA _JCH`; retiré après validation JCH et plist archivé dans `_local/disabled_launchagents/`. |

## 5. Vérifications finales

| Vérification | Résultat |
|---|---|
| `python3 scripts/pka_security_audit.py` | GREEN — No findings. |
| Plane ports | `127.0.0.1:8088`, `127.0.0.1:4443`. |
| Plane racine | `curl http://127.0.0.1:8088/` retourne `200`. |
| Backup DB | `TEAM/backups/team_2026-05-28_2048.db` créé en `0600`. |
| Logs Telegram | Aucune occurrence token détectée après correction. |
| Documents Phase 1 | Pas de `TODO/TBD` détecté dans les livrables. |

## 6. Risques résiduels

| Risque | Gravité | Décision |
|---|---|---|
| LaunchAgent obsolète `com.jch.pka.backup` | Faible | Corrigé : retiré du runtime et archivé. |
| Gmail gatekeeper actif | Moyenne-Élevée | Garder surveillé; confirmer tokens et politique de tri. |
| Dropbox watch actif | Moyenne-Élevée | Garder surveillé; données VETALYX sensibles. |
| Plane stack complexe | Moyenne | Acceptée comme runtime existant; pas de réutilisation PostgreSQL/Redis pour Hermes. |
| Logs sans rotation formalisée | Moyenne | À traiter en Phase technique minimale ou maintenance runtime. |
| `JCH_Inbox/99_SYSTEM` contient credentials Google | Élevée | Zone L3; pas de copie; vérifier à terme migration hors vault si nécessaire. |

## 7. Conditions d'entrée en Phase technique minimale

La Phase technique minimale peut commencer si JCH valide les conditions suivantes :

1. Aucun nouveau framework d'orchestration.
2. Aucun Hermes pilote.
3. Aucun Qdrant, Redis, PostgreSQL additionnel.
4. Aucun n8n.
5. Aucun agent persistant nouveau.
6. Vérifier seulement l'existant : Git, Python, Docker Desktop, VS Code, Tailscale, backups.
7. Produire un rapport `Local_Infrastructure_Setup.md`.
8. Maintenir `python3 scripts/pka_security_audit.py` GREEN ou documenter explicitement toute exception.

## 8. Décision recommandée

Phase 1 peut être validée.

Prochaine phase recommandée :

> **Phase technique minimale MacBook** : audit d'installation et configuration de base, sans ajout de stack.

## Voir aussi

- [[AI_System_Blueprint]]
- [[AI_Runtime_Audit]]
- [[AI_Data_Governance]]
- [[Runtime_Service_Register]]
- [[Phase_Tech_Minimal_MacBook_Audit]]
- [[Phase_Tech_Minimal_Backup_Audit]]
- [[TEAM/RESTORE_TEAM_DB]]
- [[RUNBOOK_PKA_MACBOOK]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
- [[Corbeau]]
