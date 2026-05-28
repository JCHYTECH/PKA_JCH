---
date: 2026-05-29
type: architecture-evaluation
status: validated
owner: "[[Dobby]]"
author: "[[Atlas]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 5 — Orchestration légère"
source:
  - "[[Persistent_Memory_Architecture]]"
  - "[[Local_Infrastructure_Setup]]"
  - "[[AI_Runtime_Audit]]"
  - "[[Runtime_Service_Register]]"
  - "[[Hermisation]]"
---

# Workflow Orchestration — PKA_JCH

## Position dans la Hermisation

Ce document est le livrable formel de la **Phase 5 — Orchestration légère**.

Il évalue n8n, les queues et les outils de monitoring au regard des workflows réels du système PKA_JCH, et définit l'architecture d'orchestration à adopter.

> Règle de phase : aucune installation technique avant que ce document soit validé par JCH.

---

## 1. État de l'orchestration actuelle

### Workflows automatisés actifs

| Service | Déclencheur | Script | Statut |
|---------|-------------|--------|--------|
| Backup `team.db` | Cron 08h00 quotidien | `scripts/backup_team_db.py` | ✅ Actif |
| Journal Sybil | Cron 22h00 quotidien | `scripts/sybil_journal.py` | ✅ Actif |
| Rétro Dobby | Cron 23h00 quotidien | `scripts/dobby_retro.py` | ✅ Actif |
| Rapport hebdomadaire | Cron 19h00 dimanche | `scripts/dobby_weekly_report.py` | ✅ Actif |
| Dashboard PKA | LaunchAgent (PID 906) | `scripts/dashboard_server.py` | ✅ Actif |
| Gmail gatekeeper | LaunchAgent (PID 914) | `scripts/gmail_gatekeeper.py` | ✅ Actif |
| Bot Telegram Dobby | LaunchAgent (PID 5377) | `scripts/telegram-bot/bot.py` | ✅ Actif |
| Dropbox watch | LaunchAgent (chargé, inactif) | `scripts/dropbox_watch.py` | ⚠️ Chargé sans PID |
| Vault maintenance | LaunchAgent (chargé, inactif) | `scripts/vault_maintenance/` | ⚠️ Chargé sans PID |
| System check | LaunchAgent (chargé, inactif) | — | ⚠️ Chargé sans PID |
| Plane autostart | LaunchAgent (chargé, inactif) | — | ⚠️ Chargé sans PID |

### Workflows suspendus

| Service | Raison |
|---------|--------|
| `email_digest.py` | Token Google expiré + doublon cron/launchd |
| `outlook_gatekeeper.py` | Token expiré en boucle |

### Problèmes identifiés

1. **Aucun audit log unifié** — chaque script écrit dans son propre `.log`. Impossible de voir d'un coup ce qui a tourné, réussi ou échoué.
2. **4 LaunchAgents chargés sans PID** — Dropbox watch, vault maintenance, system check, plane autostart : chargés dans launchd mais sans processus actif. Cause inconnue, non bloquante mais non documentée.
3. **Aucune alerte en cas d'échec silencieux** — un cron qui échoue laisse une trace dans son log mais personne ne le lit.
4. **Workflows manuels non tracés** — les tâches Dobby (briefs, analyses, livrables) ne sont pas comptabilisées comme des exécutions d'orchestration.

---

## 2. Évaluation des technologies

### 2.1 n8n

**Besoin adressé :** orchestration visuelle de workflows multi-étapes avec conditions, webhooks, intégrations tierces (Gmail, Slack, Telegram, GitHub, Notion, Airtable…).

**Réalité PKA :**
- Les workflows actuels sont des scripts Python autonomes, tous mono-service.
- Aucun workflow n'implique aujourd'hui plus de 2 services simultanément avec logique conditionnelle.
- n8n nécessite un conteneur Docker supplémentaire + base de données persistante propre.
- La valeur de n8n apparaît quand : (a) un workflow relie ≥3 services externes, (b) un utilisateur non-développeur doit modifier les conditions, (c) les scripts Python deviennent trop nombreux à maintenir.

**Verdict : 🟡 Pertinent, mais prématuré.**

n8n devient justifié si un workflow doit relier Gmail + Telegram + team.db + Plane avec logique conditionnelle et sans développement Python. Aucun workflow actuel ne remplit ces critères.

---

### 2.2 Queues (RabbitMQ, Redis Streams…)

**Besoin adressé :** découplage producteur/consommateur, traitement asynchrone, retry automatique.

**Réalité PKA :**
- Aucun producteur concurrent. Les scripts s'exécutent séquentiellement via cron/launchd.
- Aucun besoin de retry automatique (les scripts ont leur propre gestion d'erreur).
- Pas de charge à absorber.

**Verdict : ❌ Non justifié.**

À reconsidérer uniquement si plusieurs agents autonomes émettent des tâches en parallèle (Phase 6+).

---

### 2.3 Monitoring (Prometheus/Grafana, Uptime Kuma…)

**Besoin adressé :** visibilité sur l'état des services, alertes, historique de performance.

**Réalité PKA :**
- Le dashboard PKA sur `127.0.0.1:8787` couvre déjà une partie de la visibilité.
- Les logs sont éparpillés dans 5+ fichiers `.log` individuels.
- Prometheus/Grafana = stack lourde pour un système mono-utilisateur local.

**Verdict : 🟡 Besoin réel, solution légère suffisante.**

La bonne réponse n'est pas Prometheus — c'est un **audit log centralisé dans `memory_log`** + un endpoint `/api/automation` dans `dashboard_server.py`. Zéro infrastructure supplémentaire.

---

## 3. Architecture retenue — Phase 5a (maintenant)

### Principe

> Centraliser les traces, pas les outils.

Tous les scripts automatisés écrivent dans `memory_log` à chaque exécution (succès ou échec). Le dashboard expose ces traces. Aucun nouveau conteneur.

### Actions Phase 5a

| Action | Support | Responsable |
|--------|---------|-------------|
| Ajouter un appel `memory_log` en fin de chaque script cron (backup, sybil, retro, weekly) | `team.db` → `memory_log` | [[Forge]] |
| Créer `/api/automation` dans `dashboard_server.py` — retourne les 20 dernières entrées `memory_log` de type `cron` | `dashboard_server.py` | [[Forge]] |
| Ajouter un bloc "Dernières exécutions" dans `hub.html` alimenté par `/api/automation` | `hub.html` | [[Forge]] |
| Diagnostiquer les 4 LaunchAgents chargés sans PID | launchd | [[Forge]] |
| Documenter la cause dans `Runtime_Service_Register.md` | — | [[Dobby]] |

### Critères de passage Phase 5b

| Seuil | Condition |
|-------|-----------|
| Workflow ≥3 services externes avec logique conditionnelle identifié | Évaluer n8n |
| ≥3 scripts cron en erreur silencieuse non détectée sur 30 jours | Implémenter alertes Telegram |
| Agents autonomes multiples en parallèle | Évaluer queues |

---

## 4. Architecture Phase 5b — conditionnelle (n8n)

> À ne déployer que si les seuils ci-dessus sont atteints.

### Composants

| Composant | Rôle | Infrastructure |
|-----------|------|---------------|
| n8n | Orchestration visuelle de workflows multi-services | 1 conteneur Docker, port `127.0.0.1:5678` |
| SQLite (existant) | Persistence des états workflow via `memory_log` | Déjà actif |

### Workflows candidats à migrer vers n8n

| Workflow | Services impliqués | Priorité |
|----------|--------------------|----------|
| Ingestion inbox → classification → team.db | Dropbox/filesystem + Python + SQLite | Haute |
| Alerte échec cron → Telegram | cron + Telegram bot | Moyenne |
| Digest email → résumé → daily note | Gmail + Python + Obsidian | Faible (suspendu) |

### Règles

- n8n stocke ses données dans un volume Docker isolé.
- Aucune réutilisation du PostgreSQL ou Redis de Plane.
- Rollback : `docker stop n8n && docker rm n8n` — aucun effet sur `team.db`.

---

## 5. Ordre d'exécution Phase 5a

1. **Diagnostic LaunchAgents inactifs** — comprendre pourquoi 4 agents sont chargés sans PID.
2. **Audit log cron** — brancher les 4 scripts cron sur `memory_log`.
3. **Endpoint `/api/automation`** — exposer les traces dans le dashboard.
4. **Dashboard bloc "Exécutions"** — rendre les traces visibles dans `hub.html`.

---

## 6. Conditions d'entrée dans les Pilotes

La Phase 5a complète ouvre la voie aux **3 pilotes** définis dans `PILOT_SCOPE.md` :

- **Pilote 1** — Gouvernance documentaire (Corbeau + Forge) : classifier notes, valider YAML, maintenir index Obsidian.
- **Pilote 2** — Architecture système (Forge + Castor) : câbler concrètement les couches mémoire définies en Phase 4.
- **Pilote 3** — Wildlife / Bioacoustique (Chouette + Clio + Forge + Corbeau) : connecter BirdNET, RPi, ESP32, datasets audio à la mémoire PKA.

---

## Voir aussi

- [[Persistent_Memory_Architecture]]
- [[Local_Infrastructure_Setup]]
- [[AI_Runtime_Audit]]
- [[Runtime_Service_Register]]
- [[Hermisation]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
- [[Corbeau]]
- [[Atlas]]
