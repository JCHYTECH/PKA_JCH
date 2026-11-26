---
date: 2026-08-07
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1081
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-08-07

**Sessions analysées :** 2 | **Échanges :** 1081 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE PKA - 2026-08-07

## Décisions prises

1. **Transfer vers modèle plus développé** : Face à des problèmes complexes (Whisper, RPI boot), décision de transférer vers DeepSeek v4-pro au lieu de rester sur la TUI basique.

2. **Validation et mise à jour documentaire** : "oui on valide mets à jours tous les fichiers utiles" → engagement de synchroniser l'état réel du système avec la PKA.

3. **Stratégie de déploiement LUPO** : 
   - Utiliser les modèles LLM quantisés (Q4_K_M en GGUF) sur RPI 5 via Ollama
   - Reporté au 31 août pour stabiliser le hardware

4. **Approche factor form** : Éviter de demander aux utilisateurs de fixer des composants un à un → préférer une sphère/assemblage intégré.

5. **Réinitialisation RPI minimale** : "on va reallume le lupo-rpi seul pour voir si tout redemarre" → boot isolé avant intégration réseau.

6. **Mémorisation des tests** : "ok mets cela en mémoire car on va faire des tests en reel dans quelques jours" → formaliser les configurations de test.

---

## Échecs ouverts / bloqueurs

### CRITIQUE
- **RPI 5 bloqué en initialisation hardware** : Reste figé au début du boot. Cause inconnue. Piste testée : restauration d'image Home Assistant OS conflictuelle.
- **AppManager.install bloqué** : `duplicate_os_instal` → détection d'une ancienne instance HA toujours active ou en arrière-plan.
- **Accès terminal RPI interrompu** : SSH déconnexion brutale ("Broken pipe"), empêchant diagnostics en direct.

### IMPORTANT
- **Whisper non fonctionnel dans VSCode** : Cause non identifiée. Pas de logs d'erreur exploitables.
- **team.db inaccessible** : Bloquerait la synchronisation d'état entre instances (lupo vs iphone/esneux).
- **Téléchargement image HA interrompu** : `haos_rpi5-15.1.img` → erreurs réseau (timeout), fichier incomplet.
- **Ctrl+M dans terminal rpi** : Affiche 'M' au lieu d'exécuter la commande → problème encodage/locale (LC_CTYPE=UTF-8 mal configuré).

### MOYEN
- **404 réseau** : Contexte flou, à clarifier.
- **Hardware LUPO incomplet** : SD card endurance et silent blocs manquants pour finaliser RPI.

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Apparitions | Implication |
|----------|------------|-----------|
| "c'est quoi les states files ?" | 2 | Absence de doc sur l'architecture HA (states vs config) |
| "pourquoi tu n'as pas acces au terminal rpi ?" | 2-3 | Perte répétée de SSH, pas de procédure de récupération documentée |
| "team.db pourquoi inaccessible ?" | 2 | Architecture de sync inconnue ou non opérationnelle |
| "whisper ne fonctionne pas ; vérifie pourquoi on est dans vscode ?" | 2 | Diagnostic incomplet, dépendance tool non claire |
| "pourquoi il boot ?" | 2 | Ambiguïté : "pourquoi il NE boot PAS ?" ou "pourquoi il boot encore ?" |
| "L(M) c'est quoi ?" | 1 | Notation non expliquée dans doc (format Q4_K_M ??) |
| "quelle est la différence entre lupo/assiette et esneux/iphone ?" | 1 | Instances HA non documentées, rôles flous |

**→ Urgent** : Créer un document `ARCHITECTURE_HA.md` avec :
- Vue d'ensemble des 3 instances (lupo, iphone/esneux, M5)
- Rôles de chacune (contrôle, monitoring, edge compute)
- Schema de sync (team.db, states files)
- Glossaire des formats/notations (Q4_K_M, L(M), etc.)

---

## Nouveaux patterns détectés

1. **Cycle d'attente → diagnostic incomplet → escalade modèle** :
   - Bloqueur hardware → "vérifie pourquoi" → transfert DeepSeek
   - Pas de logs systématiques capturés avant escalade
   - **Inefficace** : perte de contexte, re-diagnostic

2. **SSH comme SPOF (Single Point Of Failure)** :
   - Dès que SSH tombe, toute interaction RPI devient impossible
   - Pas de fallback (serial console, web admin, etc.)
   - Sessions fermées sans state snapshot

3. **Télécherchement de fichiers volumineux sans checksum** :
   - Image HA 347 Mo échouée 2x sans vérification intégrité
   - Pas de script de retry avec exponential backoff

4. **Décisions orales non formalisées** :
   - "mets cela en mémoire" → aucune trace dans PKA
   - Mémorisation = rétrospective Dobby, pas système durable
   - MEMORY.md probablement absent ou stalé

5. **Mélange d'instances sans clarté** :
   - "lupo vs iphone vs esneux vs M5" ? Quels rôles, quels workloads ?
   - Restauration HA crée conflits → besoin architecture explicitée

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Escalade intelligente vers modèle avancé** : Reconnaître les limites et passer à DeepSeek/Claude = bonne intuition.
- **Consultation expert externe** : Demander des recommandations LLM (Q4_K_M, Ollama) = approche pragmatique.
- **Mémorisation des décisions d'essai** : "ok mets cela en mémoire" montre souci de tracking.
- **Isolation du diagnostic** : "on va reallume le lupo-rpi seul" = bonne pratique scientifique (isoler variables).

### ❌ Inefficacités
- **Pas de capture préventive des logs** avant diagnostics → re-exploration après crash SSH.
- **Questions ambiguës** : "pourquoi tu n'as pas accès", "pourquoi il boot" → JCH ou assistant ne clarifient pas.
- **Dépendance SSH comme *unique* canal** : Fragile, interrompt workflow.
- **Télécharges sans checksum/retry auto** → gaspillage bande passante.
- **État du RPI 5 flou** : "bloqué au tout début de l'initialisation" mais on ne sait pas si c'est hang du kernel, HAT detecté, ou autre.
- **Trop de contexte par transcript** : 1081 échanges, mais patterns clés pas isolés pour relecture rapide.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 BLOQUEEURS À RÉSOUDRE EN PRIORITÉ
1. **RPI 5 boot hang** : Brancher serial console (UART), capturer early kernel logs avant tentative prochaine.
2. **SSH timeout** : Mettre en place watchdog ou cronjob SSH-keep-alive sur MAC.
3. **AppManager duplicate_os_instal** : Nettoyer `/etc/` et `/var/` de tout config HA avant restauration image.
4. **team.db access** : Vérifier permissions, localisation, et si c'est un fichier SQLite ou une API distante.

### 📋 DOCUMENTATION MANQUANTE (CRÉER)
- `ARCHITECTURE_HA.md` : instances, rôles, sync model
- `LUPO_SETUP.md` : checklist hardware (SD card, silent blocs, HAT PSU), procédure boot minimal
- `TERMINAL_RPI_RECOVERY.md` : fallback quand SSH mort (serial, web console, cron export)
- `GLOSSARY.md` : Q4_K_M, L(M), states files, duplicate_os_instal, etc.
- `MEMORY.md` : Mettre à jour avec décisions d'essai du 2026-08-07

### 🛠️ SETUP À FIGER
- **Ollama + Q4_K_M models** sur RPI 5 (RAM 8 Go) : configuration validée, template à réutiliser
- **Lupo-rpi bare minimum** : démarrer sans réseau, sans instances HA concurrentes
- **iPhone/esneux instance role** : clarifier (monitoring ? edge compute ? UI seulement ?)

### 🔧 PROCESSUS À METTRE EN PLACE
1. **Pré-diagnostic checklist** : avant chaque session RPI, capturer `uname -a`, free RAM, dmesg
2. **Checkpoint SSH** : hook de déconnexion qui sauvegarde `$LAST_STATE` dans PKA
3. **Télécherge robuste** : script bash pour retry image + checksum SHA256
4. **Escalade claire** : si > 15 min bloqué, documenter état et transférer modèle (ne pas rester muet)

### 📊 TRACKING ACTIF
- **Dobby** : ajouter extraction auto des "mets cela en mémoire" → PKA/MEMORY.md direct
- **etat-projets.md** : ajouter colonne "dépendances bloquantes" pour LUPO
- **TEAM_Inbox** : créer issue tracker pour SSH stability, RPI boot hang

---

## Recommandations

### IMMÉDIAT (avant 2026-08-10)
1. **Snapshot diagnostic RPI 5** :
   ```bash
   ssh lupo-rpi 'sudo systemctl status ha-supervisor; journalctl -xe | tail -100; free -h; lsblk'
   ```
   → Sauvegarder dans `JCH_Inbox/03_PROJECTS/11_IOT/lupo/diagnostic-2026-08-07.txt`

2. **Tester serial console** :
   - Brancher UART USB sur MAC
   - Capturer early boot logs lors du hang
   - → Fournira raison du boot bloqué

3. **Clarifier instances HA** :
   - Remplir tableau récapitulatif : lupo (rôle ?), iphone (rôle ?), esneux (rôle ?), M5 (rôle ?)
   - Synchroniser avec `etat-projets.md`

### COURT TERME (2026-08-10 à 2026-08-31)
4. **Créer ARCHITECTURE_HA.md** avec schéma ASCII réseau (3 instances + flows sync).
5. **Fixer LUPO hardware** : commander SD card endurance + silent blocs, valider montage.
6. **Automatiser télécherge** : script `bin/fetch-ha-image.sh` avec retry + checksum.
7. **Documenter Whisper + VSCode** : est-ce un plugin manquant ? Ollama pas connecté ? → debug et solutionner.

### MOYEN TERME
8. **Mettre en place fallback SSH** : cron watchdog, ou web console HA locale.
9. **Synchroniser MEMORY.md** : intégrer

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 28
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 0.0%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 194.1
- Échanges/session début fenêtre : 74.4
- Tendance globale : 160.9%
- Tendance 3j-3j : 443.5%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] : Face à des problèmes complexes (Whisper, RPI boot), décision de transférer vers DeepSeek v4-pro au lieu de rester sur la TUI basique.
- [Decision] : "oui on valide mets à jours tous les fichiers utiles" → engagement de synchroniser l'état réel du système avec la PKA.
- [Decision] Utiliser les modèles LLM quantisés (Q4_K_M en GGUF) sur RPI 5 via Ollama
- [Decision] Reporté au 31 août pour stabiliser le hardware
- [Decision] : Éviter de demander aux utilisateurs de fixer des composants un à un → préférer une sphère/assemblage intégré.
- [Decision] : "on va reallume le lupo-rpi seul pour voir si tout redemarre" → boot isolé avant intégration réseau.
- [Decision] : "ok mets cela en mémoire car on va faire des tests en reel dans quelques jours" → formaliser les configurations de test.
- [Decision] Transfer vers modèle plus développé** : Face à des problèmes complexes (Whisper, RPI boot), décision de transférer vers DeepSeek v4-pro au lieu de res
- [Decision] Validation et mise à jour documentaire** : "oui on valide mets à jours tous les fichiers utiles" → engagement de synchroniser l'état réel du système a
- [Decision] Stratégie de déploiement LUPO** :
- [Decision] Approche factor form** : Éviter de demander aux utilisateurs de fixer des composants un à un → préférer une sphère/assemblage intégré.
- [Decision] Réinitialisation RPI minimale** : "on va reallume le lupo-rpi seul pour voir si tout redemarre" → boot isolé avant intégration réseau.
- [Decision] Mémorisation des tests** : "ok mets cela en mémoire car on va faire des tests en reel dans quelques jours" → formaliser les configurations de test.
- [Failure] RPI 5 bloqué en initialisation hardware** : Reste figé au début du boot. Cause inconnue. Piste testée : restauration d'image Home Assistant OS conflic
- [Failure] AppManager.install bloqué** : `duplicate_os_instal` → détection d'une ancienne instance HA toujours active ou en arrière-plan.
- [Failure] Accès terminal RPI interrompu** : SSH déconnexion brutale ("Broken pipe"), empêchant diagnostics en direct.

### Fréquence des patterns (14 jours)
- **Failure** : 2 jours, 19 occurrences
- **Decision** : 1 jours, 11 occurrences
- **Question** : 1 jours, 13 occurrences
- **Recurring question** : 1 jours, 10 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 16
- Jours d'observation : 3
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**365** recommandations au total — **365** ouvertes — **0** en cours — **0** terminées

⚠️ 357 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 322
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=358] (2026-08-07) **Dobby** : Snapshot diagnostic RPI 5** :
- [id=359] (2026-08-07) **Dobby** : Tester serial console** :
- [id=360] (2026-08-07) **Dobby** : Brancher UART USB sur MAC
- [id=361] (2026-08-07) **Dobby** : Capturer early boot logs lors du hang
- [id=362] (2026-08-07) **Dobby** : → Fournira raison du boot bloqué

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
