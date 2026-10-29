# Phase Technique Minimale — Audit Socle MacBook

Date : 2026-05-28
Statut : socle présent ; Tailscale corrigé ; étape backup validée séparément

## 1. Résumé

La première étape de la phase technique minimale a été exécutée en audit seulement.

Décision :

- Git : OK.
- Python : OK.
- Docker Desktop : OK.
- VS Code : OK.
- Tailscale : OK après réalignement du CLI sur Tailscale.app.
- Repo `PKA_JCH` : OK, branche `main`, remote GitHub configuré.

Cette étape ne déclenche aucune installation lourde et ne débloque pas encore Hermes, n8n, Qdrant, Redis, PostgreSQL ou agents persistants.

## 2. Versions et chemins

| Composant | État | Version / chemin observé | Décision |
|---|---|---|---|
| Git | OK | `git version 2.50.1 (Apple Git-155)` ; `/usr/bin/git` | Socle valide |
| Python | OK | `Python 3.13.13` ; `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | Socle valide |
| pip | OK | `pip 26.1.1` pour Python 3.13 | Socle valide |
| Docker CLI | OK | `Docker version 29.4.3` ; `/usr/local/bin/docker` | Socle valide |
| Docker Desktop | OK | `/Applications/Docker.app` présent ; daemon `Docker Desktop aarch64` | Socle valide |
| VS Code | OK | `1.121.0`, `arm64` ; `/usr/local/bin/code` ; app présente | Socle valide |
| Tailscale CLI | OK | `1.98.2` ; `/usr/local/bin/tailscale` | Socle valide |
| Tailscale app | OK | `/Applications/Tailscale.app` | App lancée, CLI aligné |

## 3. Docker

Docker Desktop est fonctionnel.

État du daemon :

```text
29.4.3 Docker Desktop aarch64
```

Conteneurs runtime observés :

| Service | État |
|---|---|
| `plane-app-proxy-1` | Actif, ports publiés uniquement sur `127.0.0.1:8088` et `127.0.0.1:4443` |
| Plane API / web / workers / db / redis / mq / minio | Actifs dans le runtime Plane existant |

Décision :

- Plane est accepté comme runtime existant.
- Ses composants internes ne doivent pas être réutilisés comme socle Hermes.
- Aucun nouveau conteneur n'est à ajouter à ce stade.

## 4. Tailscale

Version CLI après correction :

```text
1.98.2
```

Constat initial :

- l'application Tailscale est installée ;
- un processus Tailscale est visible ;
- la commande `tailscale` pointait vers le CLI Homebrew `1.96.4` dans `/opt/homebrew/bin/tailscale`, non aligné avec le daemon de l'app ;
- le CLI affichait une erreur de daemon ou un avertissement de version selon le contexte.

Correction appliquée :

- test hors sandbox du CLI app : OK ;
- `brew unlink tailscale` pour retirer les symlinks Homebrew ;
- la commande `tailscale` résout maintenant vers `/usr/local/bin/tailscale` ;
- version CLI alignée avec Tailscale.app : `1.98.2`.

État validé :

```text
MacBook Tailscale IP: 100.108.55.44
RPI tkajch: 100.84.45.93
tailscale ping tkajch: pong via 192.168.1.48:41641 in 11ms
```

Commandes de vérification :

```sh
tailscale status --self
tailscale ip -4
tailscale ping --timeout=5s --c 3 100.84.45.93
```

Ne pas lancer `tailscale up` sans validation humaine si une reconnexion ou une autorisation de compte est demandée.

## 5. Repo PKA_JCH

| Élément | État |
|---|---|
| Racine Git | `/Users/jchavauxm5/PKA_JCH` |
| Branche | `main` |
| Remote | `https://github.com/JCHYTECH/PKA_JCH.git` |

Fichiers Phase 1 actuellement concernés par les changements de clôture :

- `AI_System_Blueprint.md`
- `AI_Runtime_Audit.md`
- `AI_Data_Governance.md`
- `Runtime_Service_Register.md`
- `Phase_1_Closure_Report.md`
- `TEAM/ROSTER.md`
- `scripts/backup_team_db.py`
- `scripts/telegram-bot/bot.py`
- `_local/disabled_launchagents/com.jch.pka.backup.plist.disabled`

Note :

Le worktree contient beaucoup d'autres changements préexistants non liés à cette phase. Ils ne doivent pas être inclus dans un commit Phase 1 sans revue séparée.

## 6. Verdict

Le socle MacBook est suffisamment présent pour continuer vers l'étape 2 : stabilisation des sauvegardes et procédure de restauration.

Blocage mineur corrigé :

- Tailscale est fiable côté CLI pour l'administration distante et les tests RPI.

Étape suivante exécutée :

- [[Phase_Tech_Minimal_Backup_Audit]]
- [[TEAM/RESTORE_TEAM_DB]]
- [[RUNBOOK_PKA_MACBOOK]]

Prochaine étape recommandée après runbook :

> Préparer le commit propre Phase 1 + phase technique minimale.
