---
date: 2026-05-29
type: infrastructure-reference
status: validated
owner: "[[Dobby]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 3 — Infrastructure locale minimale"
source:
  - "[[Phase_Tech_Minimal_MacBook_Audit]]"
  - "[[Phase_Tech_Minimal_Backup_Audit]]"
  - "[[RUNBOOK_PKA_MACBOOK]]"
---

# Local Infrastructure Setup — PKA_JCH

## Position dans la [[Hermisation]]

Ce document est le livrable formel de la **Phase 3 — Infrastructure locale minimale**.

Il synthétise les deux audits techniques conduits le 2026-05-28 et constitue la référence d'entrée pour la Phase 4 (Mémoire persistante).

> Condition d'entrée en Phase 4 : ce document validé + `python3 scripts/pka_security_audit.py` GREEN.

---

## 1. Socle validé

| Composant | Version | Chemin | Statut |
|-----------|---------|--------|--------|
| Git | `2.50.1 (Apple Git-155)` | `/usr/bin/git` | ✅ Validé |
| Python | `3.13.13` | `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | ✅ Validé |
| pip | `26.1.1` | — | ✅ Validé |
| Docker CLI | `29.4.3` | `/usr/local/bin/docker` | ✅ Validé |
| Docker Desktop | — | `/Applications/Docker.app` | ✅ Validé |
| VS Code | `1.121.0 arm64` | `/usr/local/bin/code` | ✅ Validé |
| Tailscale CLI | `1.98.2` | `/usr/local/bin/tailscale` | ✅ Validé (CLI aligné sur app) |
| Tailscale app | — | `/Applications/Tailscale.app` | ✅ Validé |

Aucune installation nouvelle n'a été effectuée. L'audit a confirmé l'existence et la cohérence du socle existant.

---

## 2. Réseau Tailscale

| Nœud | IP Tailscale | IP locale |
|------|-------------|-----------|
| MacBook | `100.108.55.44` | — |
| RPi `tkajch` | `100.84.45.93` | `192.168.1.48` |

Commandes de vérification :

```sh
tailscale status --self
tailscale ip -4
tailscale ping --timeout=5s --c 3 100.84.45.93
```

Point d'attention : ne pas lancer `tailscale up` sans validation humaine si une reconnexion ou autorisation de compte est demandée.

---

## 3. Docker — conteneurs actifs

| Conteneur | Ports publiés | Règle |
|-----------|--------------|-------|
| `plane-app-proxy-1` | `127.0.0.1:8088`, `127.0.0.1:4443` | Local-only — validé |
| Plane API / web / workers / db / redis / mq / minio | internes | Acceptés comme runtime existant |

**Règle ferme :** les composants internes de Plane (PostgreSQL, Redis) ne doivent pas être réutilisés comme socle Hermes. Toute Phase 4 déploiera ses propres conteneurs isolés.

---

## 4. Sauvegardes `TEAM/team.db`

| Élément | État |
|---------|------|
| Base active | `TEAM/team.db` — permissions `0600` |
| Dossier backups | `TEAM/backups/` — `0755` |
| Log cron | `TEAM/backups/backup.log` — `0600` |
| Intégrité | `PRAGMA integrity_check` → `ok` |
| Planification | Cron quotidien 08h00 via `scripts/backup_team_db.py` |
| Test restauration à blanc | Réussi (`tmp/restore_rehearsal/`) |

Procédure de restauration : [[TEAM/RESTORE_TEAM_DB]]

Risques résiduels acceptés :
- Backups uniquement locaux — à traiter en Phase 4 ou maintenance runtime (sauvegarde hors machine).
- Restauration automatisée interdite sans validation humaine.

---

## 5. Repo PKA_JCH

| Élément | État |
|---------|------|
| Racine | `/Users/jchavauxm5/PKA_JCH` |
| Branche active | `main` |
| Remote | `https://github.com/JCHYTECH/PKA_JCH.git` |

---

## 6. Services runtime au moment de la validation

### Actifs

| Service | Endpoint |
|---------|----------|
| Dashboard PKA | `127.0.0.1:8787` |
| Gmail gatekeeper | — |
| Bot Telegram [[Dobby]] | — |
| Plane | `127.0.0.1:8088` / `127.0.0.1:4443` |
| Ollama | `127.0.0.1:11434` |
| Dropbox client | — |
| Cron backup / [[Sybil]] / rétro / weekly | — |

### Suspendus

| Service | Raison |
|---------|--------|
| `email_digest.py` | Token Google expiré + doublon cron/launchd. Reprise sur amélioration + accord JCH uniquement. |
| `outlook_gatekeeper.py` | Token expiré en boucle. |

---

## 7. Conditions d'entrée en Phase 4

1. Ce document validé.
2. `python3 scripts/pka_security_audit.py` retourne GREEN.
3. Aucune installation de PostgreSQL, Redis, Qdrant, n8n, ni agent persistant nouveau en dehors de la Phase 4 définie.
4. `Persistent_Memory_Architecture.md` produit avant toute action technique.

---

## Voir aussi

- [[Phase_Tech_Minimal_MacBook_Audit]]
- [[Phase_Tech_Minimal_Backup_Audit]]
- [[RUNBOOK_PKA_MACBOOK]]
- [[Phase_1_Closure_Report]]
- [[AI_System_Blueprint]]
- [[AI_Data_Governance]]
- [[TEAM/RESTORE_TEAM_DB]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
