---
date: 2026-05-28
type: runtime-service-register
status: draft
owner: "[[Dobby]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 1.3 — Gouvernance documentaire et runtime"
source:
  - "[[AI_Runtime_Audit]]"
  - "[[AI_Data_Governance]]"
---

# Runtime Service Register — PKA_JCH

## Statuts

| Statut | Sens |
|---|---|
| Actif | Service chargé ou processus observé. |
| Activé | Service configuré pour se lancer, même si non actif au moment de l'audit. |
| Suspendu | Service volontairement désactivé. |
| Obsolète | Service pointe vers un ancien chemin ou une ancienne architecture. |
| À valider | Nécessite décision JCH avant conservation ou modification. |

## Services launchd

| Service | Script | Owner | Fréquence | Statut | Inputs | Outputs / logs | Risque | Rollback |
|---|---|---|---|---|---|---|---|---|
| `com.jchytech.pka-dashboard` | `scripts/dashboard_server.py --host 127.0.0.1 --port 8787` | [[Forge]] | RunAtLoad + KeepAlive | Actif | Dashboards PKA | `tmp/dashboard.launchd.log`, port `127.0.0.1:8787` | Faible si local-only | `launchctl bootout gui/501/com.jchytech.pka-dashboard` |
| `com.jchytech.pka-gmail-gatekeeper` | `scripts/gmail_gatekeeper.py scan` | [[Pie]] + [[Forge]] | 1200 s | Actif | Gmail config, allowlist | `tmp/gmail-gatekeeper.log` | Données email, token Google | `launchctl bootout gui/501/com.jchytech.pka-gmail-gatekeeper` |
| `com.pka.dobby` | `scripts/telegram-bot/bot.py` | [[Dobby]] + [[Forge]] | RunAtLoad + KeepAlive | Actif | Telegram, `.env`, Anthropic/OpenAI APIs | `scripts/telegram-bot/dobby.log`, `conversation.db` | Token, conversation, API externe | `launchctl bootout gui/501/com.pka.dobby` |
| `com.jchytech.pka-dropbox-watch` | `scripts/dropbox_watch.py` | [[Forge]] + [[Vasco]] | WatchPaths Dropbox | Activé | `/Users/jchavauxm5/Dropbox/VETALYX` | `tmp/dropbox-watch.log`, snapshots | Données VETALYX | `launchctl bootout gui/501/com.jchytech.pka-dropbox-watch` |
| `com.jchytech.pka-system-check` | `scripts/pka_system_check.py --write-report` | [[Dobby]] + [[Castor]] | 21600 s + RunAtLoad | Activé | Vault, DB, configs | `TEAM_Inbox/*_system_check.md` | Bruit si non consolidé | `launchctl bootout gui/501/com.jchytech.pka-system-check` |
| `com.jchytech.pka-vault-maintenance` | `scripts/pka_vault_maintenance.py` | [[Forge]] + [[Corbeau]] | 02:00 | Activé | Vault Markdown | `scripts/logs/vault_maintenance.log` | Corrections automatiques | `launchctl bootout gui/501/com.jchytech.pka-vault-maintenance` |
| `com.jchytech.pka-plane-autostart` | `bin/plane-autostart.sh` | [[Forge]] | 300 s + RunAtLoad | Activé | Docker, Plane compose | `tmp/plane-autostart.log` | Docker local; ports restreints à loopback | `launchctl bootout gui/501/com.jchytech.pka-plane-autostart` |
| `com.jchytech.pka-email-digest` | `scripts/email_digest.py` | [[Pie]] | 09:00, 14:00, 20:00 | Suspendu | Gmail / digest config | `tmp/email-digest.log`, `scripts/email_digest.log` | Token expiré, doublon cron | `launchctl enable gui/501/com.jchytech.pka-email-digest` puis bootstrap validé |
| `com.jchytech.pka-outlook-gatekeeper` | `scripts/outlook_gatekeeper.py` | [[Pie]] + [[Forge]] | 900 s | Suspendu | Outlook token/config | `tmp/outlook-gatekeeper.log` | Token expiré en boucle | `launchctl enable gui/501/com.jchytech.pka-outlook-gatekeeper` puis bootstrap validé |
| `com.jch.pka.backup` | Ancien `Desktop/PKA _JCH/scripts/backup_team_db.py` | [[Castor]] | 259200 s | Retiré | Ancienne copie PKA | Ancien `Desktop/PKA _JCH/backups/backup.log` | Chemin cassé / doublon | `bootout` + `disable`; plist archivé dans `_local/disabled_launchagents/` |

## Cron

État observé après remédiation P0 : `email_digest.py` n'est plus présent dans le crontab.

| Horaire | Script | Owner | Statut | Rôle | Logs | Risque |
|---|---|---|---|---|---|---|
| 08:00 quotidien | `scripts/backup_team_db.py` | [[Castor]] | Actif | Backup `TEAM/team.db` | `TEAM/backups/backup.log` | Critique; backups doivent être `0600` |
| 22:00 quotidien | `scripts/sybil_journal.py` | [[Sybil]] | Actif | Journal quotidien | `scripts/sybil_journal.log` | Faible-moyen |
| 23:00 quotidien | `scripts/dobby_retro.py` | [[Dobby]] | Actif | Rétro quotidienne | `scripts/dobby_retro.log` | Faible-moyen |
| 19:00 dimanche | `scripts/dobby_weekly_report.py` | [[Dobby]] | Actif | Rapport hebdo | `scripts/dobby_weekly.log` | Faible-moyen |

## Docker / Plane

| Service | État | Ports | Owner | Risque | Décision requise |
|---|---|---|---|---|---|
| Plane stack Docker | Actif observé 2026-05-28 | `127.0.0.1:8088`, `127.0.0.1:4443` | [[Forge]] | Local-only après remédiation | Maintenir binding loopback; validation JCH requise pour LAN. |
| Plane PostgreSQL interne | Actif dans Docker | interne Docker `5432` | [[Forge]] | Ne pas confondre avec DB PKA | Garder séparé de `TEAM/team.db`. |
| Plane Redis interne | Actif dans Docker | interne Docker `6379` | [[Forge]] | Ne valide pas Redis pour Hermes | Pas de réutilisation sans phase technique. |
| Plane MinIO/MQ internes | Actifs dans Docker | internes Docker | [[Forge]] | Stack déjà complexe | Documenter sauvegarde/rollback Plane. |

## Services locaux non launchd

| Service | État | Port | Owner | Rôle | Risque |
|---|---|---:|---|---|---|
| Ollama | Actif | `127.0.0.1:11434` | [[Forge]] | Modèles locaux | Vérifier modèles disponibles. |
| Dropbox client | Actif | `127.0.0.1:17600`, `17603` | JCH | Sync fichiers | Données externes, hors PKA pur. |

## Services suspendus

| Service | Date suspension | Raison | Condition de réactivation |
|---|---|---|---|
| `email_digest.py` | 2026-05-28 | Contradiction avec `MEMORY.md`, token Google expiré/révoqué, doublon cron + launchd. | Décision JCH + OAuth valide + un seul scheduler + logs `0600`. |
| `outlook_gatekeeper.py` | 2026-05-28 | Token expiré en boucle toutes les 15 minutes. | Décision JCH + réauth Outlook + journalisation propre. |

## Remédiations runtime

| Date | Service | Action | Validation |
|---|---|---|---|
| 2026-05-28 | Plane proxy | Ajout de `host_ip: 127.0.0.1` sur les ports 80/443 publiés dans `_local/plane-community/plane-app/docker-compose.yaml`; recréation du proxy via Docker Compose; permission `0600` sur `plane.env`. | `docker ps` confirme `127.0.0.1:8088->80/tcp` et `127.0.0.1:4443->443/tcp`; `lsof` confirme loopback; `curl http://127.0.0.1:8088/` retourne `200`. |

## Règles d'entretien

- Tout nouveau service doit être ajouté ici avant activation.
- Toute suspension doit indiquer date, raison et condition de réactivation.
- Tout service touchant emails, secrets, Dropbox, Telegram ou réseau est au moins L2 et peut devenir L3.
- Toute exposition `0.0.0.0` doit être validée par JCH.
- Les logs de services sensibles doivent être `0600`.

## Voir aussi

- [[AI_Data_Governance]]
- [[AI_Runtime_Audit]]
- [[AI_System_Blueprint]]
- [[Phase_1_Closure_Report]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
- [[Pie]]
