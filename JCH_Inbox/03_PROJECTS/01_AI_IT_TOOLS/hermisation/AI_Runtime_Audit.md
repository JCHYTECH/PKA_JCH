---
date: 2026-05-28
type: runtime-audit
status: draft
owner: "[[Dobby]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 1.2 — Audit Runtime Minimal"
source:
  - "[[AI_System_Blueprint]]"
  - "[[TEAM/team.db]]"
  - "macOS launchd"
  - "crontab"
  - "process list"
---

# AI Runtime Audit — PKA_JCH

## Objectif

Cartographier le runtime réel de [[PKA_JCH]] avant toute nouvelle infrastructure.

Cette mission répond à une question simple :

> Qu'est-ce qui tourne vraiment, qu'est-ce qui est seulement configuré, et qu'est-ce qui est à risque ?

## Portée

Audit en lecture seule réalisé le 2026-05-28.

Commandes utilisées :

- `pgrep -fl ...`
- `crontab -l`
- `lsof -iTCP -sTCP:LISTEN -n -P`
- inspection des LaunchAgents dans `~/Library/LaunchAgents/`
- lecture de logs récents
- `docker ps --format ...`
- vérification de permissions avec `stat`

Limite : `launchctl list` n'a pas retourné de sortie exploitable dans cette session. L'audit combine donc fichiers LaunchAgents installés, processus actifs, ports et logs.

## Résumé exécutif

Le système PKA n'est pas seulement documentaire : plusieurs automatisations tournent déjà réellement.

Points critiques :

1. `email_digest.py` est encore planifié en cron et en LaunchAgent alors que `MEMORY.md` indique que le digest est suspendu.
2. `email_digest.py` échoue avec un token Google expiré/révoqué.
3. `outlook_gatekeeper` tourne toutes les 15 minutes mais signale un token expiré en boucle.
4. Le bot Telegram [[Dobby]] tourne et ses logs exposent des requêtes contenant le token du bot en clair. Le token doit être considéré comme compromis.
5. Plane tourne via Docker et expose `8088` et `4443` sur toutes les interfaces (`0.0.0.0`), ce qui contredit la préférence sécurité "local-only" sauf validation explicite.
6. Des logs et backups récents ont des permissions `0644`, alors que la politique exige `0600`.
7. Le LaunchAgent backup qui pointait vers `Desktop/PKA _JCH` a été retiré après validation JCH.

## 1. Services et LaunchAgents

### 1.1 LaunchAgents PKA installés

| Label | Programme | Fréquence | État observé | Classification | Criticité |
|---|---|---:|---|---|---|
| `com.jchytech.pka-dashboard` | `scripts/dashboard_server.py --host 127.0.0.1 --port 8787` | RunAtLoad + KeepAlive | Processus actif PID 906, port `127.0.0.1:8787` | Actif | Moyenne |
| `com.jchytech.pka-dropbox-watch` | `scripts/dropbox_watch.py` | WatchPaths Dropbox | Log récent "Logged 4 changes" | Actif ou déclenché récemment | Élevée |
| `com.jch.pka.backup` | Ancien chemin `Desktop/PKA _JCH/scripts/backup_team_db.py` | 259200 s | Retiré du domaine launchd; plist archivé | Corrigé | Faible |
| `com.jchytech.pka-system-check` | `scripts/pka_system_check.py --write-report` | 21600 s + RunAtLoad | Rapport du 2026-05-28 généré | Actif | Élevée |
| `com.jchytech.pka-plane-autostart` | `bin/plane-autostart.sh` | 300 s + RunAtLoad | Logs actifs toutes les 5 min | Actif | Élevée |
| `com.jchytech.pka-gmail-gatekeeper` | `scripts/gmail_gatekeeper.py scan` | 1200 s + RunAtLoad | Processus actif PID 914 | Actif | Élevée |
| `com.pka.dobby` | `scripts/telegram-bot/bot.py` | RunAtLoad + KeepAlive | Processus actif PID 1853 | Actif, sensible | Élevée |
| `com.jchytech.pka-outlook-gatekeeper` | `scripts/outlook_gatekeeper.py` | 900 s | Logs token expiré répétés | Actif mais non fonctionnel | Élevée |
| `com.jchytech.pka-email-digest` | `scripts/email_digest.py` | 09:00, 14:00, 20:00 | Doublon avec cron, erreur token Google | À désactiver ou corriger | Élevée |

## 2. Cron

`crontab -l` contient 7 entrées PKA.

| Horaire | Script | Classification | Commentaire |
|---|---|---|---|
| 09:00, 14:00, 20:00 | `scripts/email_digest.py` | Contradictoire / à risque | Digest indiqué comme suspendu dans `MEMORY.md`; doublon avec LaunchAgent. |
| 08:00 | `scripts/backup_team_db.py` | Critique | Dernier log backup local observé : 2026-05-26. |
| 22:00 | `scripts/sybil_journal.py` | Actif utile | Journalisation quotidienne. |
| 23:00 | `scripts/dobby_retro.py` | Actif utile | Rétro quotidienne. |
| Dimanche 19:00 | `scripts/dobby_weekly_report.py` | Actif utile | Rapport hebdomadaire. |

## 3. Processus actifs observés

| PID | Processus | Rôle | Classification |
|---:|---|---|---|
| 906 | `dashboard_server.py --host 127.0.0.1 --port 8787` | Dashboard local PKA | Actif, local-only |
| 914 | `gmail_gatekeeper.py scan` | Gatekeeper Gmail | Actif |
| 1853 | `telegram-bot/bot.py` | Bot Telegram [[Dobby]] | Actif, sensible |
| 1299 | Docker Desktop | Support Plane / Docker | Actif |
| 951+ | Dropbox | Synchronisation Dropbox | Actif externe |
| 972 | Ollama | Modèles locaux | Actif, local-only `127.0.0.1:11434` |

## 4. Ports ouverts

### 4.1 Ports PKA ou liés à PKA

| Port | Binding | Service | Risque |
|---:|---|---|---|
| 8787 | `127.0.0.1` | Dashboard PKA | Correct, local-only |
| 11434 | `127.0.0.1` | Ollama | Correct, local-only |
| 8088 | `0.0.0.0` / IPv6 | Plane proxy Docker | À risque si non validé |
| 4443 | `0.0.0.0` / IPv6 | Plane proxy Docker TLS | À risque si non validé |
| 17600, 17603 | `127.0.0.1` | Dropbox | Externe mais local-only |

### 4.2 Autres ports non classés PKA

Ports observés : `5000`, `7000`, `2968`, ports Adobe, OneDrive, Code Helper, digipass. Non classés PKA dans cet audit.

## 5. Docker / Plane

Docker est actif. Plane tourne avec les conteneurs suivants :

- `plane-app-proxy-1`
- `plane-app-api-1`
- `plane-app-worker-1`
- `plane-app-beat-worker-1`
- `plane-app-web-1`
- `plane-app-admin-1`
- `plane-app-space-1`
- `plane-app-live-1`
- `plane-app-plane-db-1`
- `plane-app-plane-redis-1`
- `plane-app-plane-minio-1`
- `plane-app-plane-mq-1`

Observation importante : Plane utilise déjà PostgreSQL, Redis, MinIO et MQ dans Docker. Cela ne doit pas être confondu avec une validation d'infrastructure Hermes. C'est un runtime existant à gouverner, pas une permission d'ajouter une nouvelle stack.

## 6. Logs et erreurs

| Log | Observation | Classification |
|---|---|---|
| `scripts/email_digest.log` | Erreur Google OAuth `invalid_grant`, token expiré/révoqué. | P0 |
| `tmp/email-digest.log` | Exécution récente à 14:00. | P0 |
| `tmp/outlook-gatekeeper.log` | Messages répétés "Token expire" toutes les 15 minutes. | P0 |
| `tmp/gmail-gatekeeper.log` | Scans réussis : `allowed_existing: 1`, pas d'erreur récente. | P1 |
| `tmp/plane-autostart.log` | Plane relancé/vérifié toutes les 5 minutes, API reachable. | P1 |
| `scripts/telegram-bot/dobby.log` | Requêtes Telegram avec token visible dans les URLs de log. | P0 sécurité |
| `scripts/telegram-bot/bot.log` | Ancien conflit `getUpdates`, possible double instance historique. | P1 |

## 7. Permissions sensibles

### 7.1 Conformes

- `TEAM/team.db` : `0600`
- anciens backups DB principaux : `0600`
- `scripts/telegram-bot/.env` : `0600`
- `scripts/telegram-bot/*.log` : `0600`
- plusieurs logs PKA : `0600`

### 7.2 Non conformes

| Fichier | Mode observé | Mode attendu | Priorité |
|---|---:|---:|---|
| `TEAM/backups/team_2026-05-25_0800.db` | `0644` | `0600` | P0 |
| `TEAM/backups/team_2026-05-26_0800.db` | `0644` | `0600` | P0 |
| `tmp/dropbox-watch.log` | `0644` | `0600` | P0 |
| `tmp/email-digest.log` | `0644` | `0600` | P0 |
| `tmp/outlook-gatekeeper.log` | `0644` | `0600` | P0 |

## 8. Contradictions

| Sujet | Source A | Source B | Décision recommandée |
|---|---|---|---|
| Email digest | `MEMORY.md` : digest suspendu depuis 2026-05-11 | Cron + LaunchAgent encore actifs | Désactiver ou clarifier immédiatement. |
| Backup DB | Cron actuel `scripts/backup_team_db.py` | Ancien LaunchAgent obsolète `Desktop/PKA _JCH` | Corrigé le 2026-05-28 : ancien LaunchAgent retiré et archivé. |
| Plane sécurité | Politique : dashboards en `127.0.0.1` par défaut | Plane exposait `0.0.0.0:8088/4443` lors de l'audit initial | Corrigé le 2026-05-28 : binding restreint à `127.0.0.1`. |
| Telegram sécurité | Secrets hors Markdown et logs | Logs contiennent token Telegram dans URL | Rotation token + purge logs + filtrage logging. |

## 9. Classification actionnable

### P0 — À traiter avant toute phase technique

1. Décider du statut réel de `email_digest.py` : suspendre vraiment ou réauthentifier.
2. Supprimer le doublon cron/LaunchAgent pour `email_digest.py`.
3. Réauthentifier ou désactiver `outlook_gatekeeper`.
4. Considérer le token Telegram comme compromis : le régénérer, purger les logs, modifier le logging pour masquer les URLs contenant le token.
5. Corriger permissions `0644` sur logs/backups sensibles.
6. Vérifier si Plane doit être accessible LAN ; sinon restreindre à `127.0.0.1`.
7. Supprimer ou corriger le LaunchAgent backup pointant vers `Desktop/PKA _JCH`, après validation humaine. **Fait le 2026-05-28.**

### P1 — Gouvernance runtime

1. Créer un registre `Runtime_Service_Register.md`.
2. Ajouter pour chaque service : owner, fréquence, inputs, outputs, logs, rollback.
3. Ajouter une règle : tout nouveau LaunchAgent doit passer par validation JCH.
4. Ajouter rotation et redaction de logs.
5. Vérifier la disponibilité réelle des modèles Ollama configurés.

### P2 — Nettoyage documentaire

1. Aligner `MEMORY.md`, LaunchAgents et cron.
2. Ajouter les statuts `actif`, `suspendu`, `retiré`, `obsolète`.
3. Consolider les rapports système dans une vue unique.

## 10. Décision Phase 1.2

Le système existant est déjà assez automatisé pour justifier une stabilisation avant toute nouvelle couche.

Conclusion :

> Ne pas ajouter Hermes, n8n, Redis, Qdrant ou nouvelle orchestration tant que les P0 runtime ne sont pas résolus.

Les règles de conservation et d'évolution de ce runtime sont formalisées dans [[AI_Data_Governance]] et [[Runtime_Service_Register]].

## 11. Remédiations effectuées

| Date | Élément | Action | Validation |
|---|---|---|---|
| 2026-05-28 | Bot Telegram [[Dobby]] | Ajout d'un filtre de logs dans `scripts/telegram-bot/bot.py` pour masquer les tokens Telegram, purge des logs, redémarrage du LaunchAgent. | Processus actif, log de démarrage propre, aucune occurrence token détectée après purge. |
| 2026-05-28 | `email_digest.py` | Suppression des trois entrées cron `09:00`, `14:00`, `20:00`; `launchctl bootout` du LaunchAgent; `launchctl disable gui/501/com.jchytech.pka-email-digest`. | `crontab -l` ne contient plus `email_digest.py`; service absent du domaine launchd; `print-disabled` indique `disabled`; aucun processus `email_digest.py`. |
| 2026-05-28 | `outlook_gatekeeper.py` | `launchctl bootout` du LaunchAgent; `launchctl disable gui/501/com.jchytech.pka-outlook-gatekeeper`. | Service absent du domaine launchd; `print-disabled` indique `disabled`; aucun processus `outlook_gatekeeper.py` ou `outlook_imap.py`. |
| 2026-05-28 | Permissions logs/backups sensibles | `chmod 600` sur `TEAM/backups/team_2026-05-25_0800.db`, `TEAM/backups/team_2026-05-26_0800.db`, `tmp/dropbox-watch.log`, `tmp/email-digest.log`, `tmp/outlook-gatekeeper.log`, `TEAM_Inbox/dropbox_vetalyx_changes.log`. | `stat` confirme `0600`; `pka_security_audit.py` ne signale plus de défaut de permissions. |
| 2026-05-28 | Backup `TEAM/team.db` | Exécution manuelle de `scripts/backup_team_db.py`; correction du script pour appliquer `0600` aux nouveaux backups. | Backup frais `TEAM/backups/team_2026-05-28_2048.db` en `0600`; audit sécurité passé de RED à ORANGE. |
| 2026-05-28 | Plane proxy | Restriction des ports publiés à `127.0.0.1` dans `_local/plane-community/plane-app/docker-compose.yaml`; recréation du proxy; `chmod 600` sur `plane.env`. | `docker ps` confirme `127.0.0.1:8088` et `127.0.0.1:4443`; `lsof` confirme loopback; page racine Plane répond `200`; audit sécurité GREEN. |
| 2026-05-28 | LaunchAgent backup obsolète | `launchctl bootout gui/501/com.jch.pka.backup`; `launchctl disable gui/501/com.jch.pka.backup`; archivage du plist hors `~/Library/LaunchAgents`. | Le backup valide reste assuré par cron à 08:00; l'ancien plist est conservé dans `_local/disabled_launchagents/com.jch.pka.backup.plist.disabled`. |

Sauvegardes crontab :

- `tmp/crontab_before_email_digest_suspend_2026-05-28.txt`
- `tmp/crontab_without_email_digest_2026-05-28.txt`

## Voir aussi

- [[AI_System_Blueprint]]
- [[AI_Data_Governance]]
- [[Runtime_Service_Register]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
- [[Sybil]]
- [[JCH_Inbox/99_SYSTEM/security/policy|PKA Security Policy]]
