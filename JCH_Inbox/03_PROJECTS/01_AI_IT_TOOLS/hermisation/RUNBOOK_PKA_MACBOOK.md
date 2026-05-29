# Runbook PKA MacBook

Date : 2026-05-28
Statut : opérationnel, phase technique minimale

## 1. Rôle

Ce runbook décrit les commandes de santé, les services actifs/suspendus et les procédures minimales pour exploiter le MacBook PKA_JCH.

Il ne remplace pas la gouvernance :

- [[AI_System_Blueprint]]
- [[AI_Runtime_Audit]]
- [[AI_Data_Governance]]
- [[Runtime_Service_Register]]
- [[Phase_Tech_Minimal_MacBook_Audit]]
- [[Phase_Tech_Minimal_Backup_Audit]]
- [[TEAM/RESTORE_TEAM_DB]]

## 2. Règles de base

Ne pas lancer sans validation humaine :

- Hermes ;
- n8n ;
- Qdrant ;
- Redis ou PostgreSQL hors stack Plane existante ;
- agents persistants nouveaux ;
- restauration réelle de `TEAM/team.db` ;
- réactivation `email_digest.py` ;
- réactivation `outlook_gatekeeper.py`.

Ne pas inclure dans un commit technique minimal :

- changements Obsidian non liés ;
- imports VETALYX / WildNexus / vault massifs ;
- secrets, tokens, fichiers `.env`, logs sensibles ;
- backups SQLite.

## 3. Commandes de santé

Depuis la racine :

```sh
cd /Users/jchavauxm5/PKA_JCH
pwd
git branch --show-current
git remote -v
python3 --version
python3 -m pip --version
docker --version
docker info --format '{{.ServerVersion}} {{.OperatingSystem}} {{.Architecture}}'
code --version
tailscale version
python3 scripts/pka_security_audit.py
```

Tailscale, si le daemon répond :

```sh
tailscale status --self
tailscale ip -4
tailscale ping --timeout=5s --c 3 100.84.45.93
```

Backup :

```sh
ls -lt TEAM/backups/team_*.db | head
tail -n 20 TEAM/backups/backup.log
sqlite3 TEAM/team.db 'PRAGMA integrity_check;'
```

Docker / Plane :

```sh
docker ps --format '{{.Names}} {{.Status}} {{.Ports}}'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/
```

LaunchAgents :

```sh
launchctl print-disabled gui/$(id -u) | rg 'pka|dobby|jch'
launchctl print gui/$(id -u) | rg 'pka|dobby|jch'
```

Cron :

```sh
crontab -l
```

## 4. État attendu du socle

| Composant | État attendu |
|---|---|
| Git | installé |
| Python | 3.13.x |
| pip | disponible |
| Docker Desktop | installé, daemon actif |
| VS Code | installé, CLI `code` disponible |
| Tailscale | installé ; CLI `/usr/local/bin/tailscale` version `1.98.2` ; IP MacBook `100.108.55.44` |
| Repo | `/Users/jchavauxm5/PKA_JCH`, branche `main` |
| Security audit | `GREEN` |

## 5. Services actifs

| Service | Rôle | Commande / fréquence | Logs |
|---|---|---|---|
| `com.pka.dobby` | Bot Telegram [[Dobby]] | RunAtLoad + KeepAlive | `scripts/telegram-bot/dobby.log` |
| `com.jchytech.pka-dashboard` | Dashboard local | RunAtLoad + KeepAlive | voir plist |
| `com.jchytech.pka-dropbox-watch` | Surveillance Dropbox VETALYX | WatchPaths | `tmp/dropbox-watch.log` |
| `com.jchytech.pka-gmail-gatekeeper` | Scan Gmail | toutes les 20 min | `tmp/gmail-gatekeeper.log` |
| `com.jchytech.pka-plane-autostart` | Maintien Plane local | toutes les 5 min | `tmp/plane-autostart.launchd.log` |
| `com.jchytech.pka-system-check` | Rapport santé système | toutes les 6 h + RunAtLoad | `TEAM_Inbox/*_system_check.md` |
| `com.jchytech.pka-vault-maintenance` | Maintenance vault | 02:00 | `scripts/logs/vault_maintenance.log` |

## 6. Services suspendus ou retirés

| Service | État | Raison |
|---|---|---|
| `com.jchytech.pka-email-digest` | disabled | digest suspendu, token Google expiré/révoqué, ancien doublon cron retiré |
| `com.jchytech.pka-outlook-gatekeeper` | disabled | token Outlook expiré en boucle |
| `com.jch.pka.backup` | disabled + plist archivé | ancien chemin `Desktop/PKA _JCH`, doublon backup |

Archive :

```text
_local/disabled_launchagents/com.jch.pka.backup.plist.disabled
```

## 7. Cron actif

| Horaire | Script | Rôle |
|---|---|---|
| 08:00 quotidien | `scripts/backup_team_db.py` | backup `TEAM/team.db` |
| 22:00 quotidien | `scripts/sybil_journal.py` | journal [[Sybil]] |
| 23:00 quotidien | `scripts/dobby_retro.py` | rétrospective [[Dobby]] |
| 19:00 dimanche | `scripts/dobby_weekly_report.py` | rapport hebdo |

`email_digest.py` ne doit pas être présent dans le crontab tant qu'il n'est pas réautorisé.

## 8. [[Dobby]] Telegram

Statut :

- LaunchAgent : `com.pka.dobby`
- Script : `scripts/telegram-bot/bot.py`
- Python : `scripts/telegram-bot/venv/bin/python3`
- Log : `scripts/telegram-bot/dobby.log`

Voir l'état :

```sh
pgrep -fl 'scripts/telegram-bot/bot.py|com.pka.dobby'
tail -n 40 scripts/telegram-bot/dobby.log
launchctl print gui/$(id -u)/com.pka.dobby
```

Arrêter :

```sh
launchctl bootout gui/$(id -u)/com.pka.dobby
```

Redémarrer :

```sh
launchctl bootstrap gui/$(id -u) /Users/jchavauxm5/Library/LaunchAgents/com.pka.dobby.plist
```

Ne jamais journaliser un token Telegram en clair. Si un token apparaît dans un log :

1. considérer le token compromis ;
2. régénérer côté BotFather ;
3. purger les logs ;
4. vérifier le filtre de redaction dans `scripts/telegram-bot/bot.py`.

## 9. Backup TEAM DB

Backup manuel :

```sh
python3 scripts/backup_team_db.py
```

Backup manuel avec log :

```sh
python3 scripts/backup_team_db.py >> TEAM/backups/backup.log 2>&1
```

Vérifier le dernier backup :

```sh
latest=$(ls -t TEAM/backups/team_*.db | head -n 1)
stat -f '%Lp %z %N' "$latest"
sqlite3 "$latest" 'PRAGMA integrity_check;'
```

Restauration :

- suivre [[TEAM/RESTORE_TEAM_DB]] ;
- validation humaine obligatoire ;
- arrêt ou suspension des writers obligatoire.

## 10. Plane local

Statut :

- Compose : `_local/plane-community/plane-app/docker-compose.yaml`
- Env : `_local/plane-community/plane-app/plane.env`
- Proxy : `127.0.0.1:8088`, `127.0.0.1:4443`

Voir :

```sh
docker ps --format '{{.Names}} {{.Status}} {{.Ports}}'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/
```

Redémarrer le proxy uniquement :

```sh
docker compose -f _local/plane-community/plane-app/docker-compose.yaml --env-file=_local/plane-community/plane-app/plane.env up -d proxy
```

Règle :

Plane est un runtime existant. Ses Redis/PostgreSQL internes ne sont pas un socle pour Hermes.

## 11. Gmail et Dropbox

Gmail gatekeeper :

```sh
tail -n 80 tmp/gmail-gatekeeper.log
launchctl print gui/$(id -u)/com.jchytech.pka-gmail-gatekeeper
```

Dropbox watch :

```sh
tail -n 80 tmp/dropbox-watch.log
launchctl print gui/$(id -u)/com.jchytech.pka-dropbox-watch
```

Ces services manipulent des données sensibles. Ne pas modifier leurs règles sans validation.

## 12. Réactiver un service suspendu

Ne réactiver `email_digest` ou `outlook_gatekeeper` qu'après :

1. clarification du besoin ;
2. réauthentification token ;
3. test manuel ;
4. validation JCH ;
5. mise à jour de [[Runtime_Service_Register]].

Procédure générale :

```sh
launchctl enable gui/$(id -u)/SERVICE_LABEL
launchctl bootstrap gui/$(id -u) /Users/jchavauxm5/Library/LaunchAgents/SERVICE_LABEL.plist
```

## 13. Commit propre

Avant commit :

```sh
git status --short
python3 scripts/pka_security_audit.py
```

Inclure uniquement les fichiers de gouvernance/runtime validés.

Exclure :

- `.obsidian/` ;
- `TEAM/backups/team_*.db` ;
- logs ;
- `.env` ;
- fichiers importés non liés.

## 14. Incident rapide

Si comportement anormal :

1. ne pas lancer de nouvelle stack ;
2. vérifier `python3 scripts/pka_security_audit.py` ;
3. vérifier les logs du service concerné ;
4. arrêter le service fautif avec `launchctl bootout` si nécessaire ;
5. documenter dans `AI_Runtime_Audit.md` ou `Runtime_Service_Register.md`.

## 15. Tailscale

État validé le 2026-05-28 :

- CLI par défaut : `/usr/local/bin/tailscale`
- Version : `1.98.2`
- IP MacBook : `100.108.55.44`
- RPI `tkajch` : `100.84.45.93`
- Connectivité : `tailscale ping` OK

Le CLI Homebrew `1.96.4` a été délié avec :

```sh
brew unlink tailscale
```

Raison :

- éviter un mismatch entre le CLI Homebrew et le daemon fourni par Tailscale.app ;
- faire pointer `tailscale` vers le wrapper installé par Tailscale.app.

Vérifier :

```sh
type -a tailscale
tailscale version
tailscale status --self
tailscale ip -4
```
