---
date: 2026-07-17
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1204
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-17

**Sessions analysées :** 4 | **Échanges :** 1204 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE DES SESSIONS DU 2026-07-17

## Décisions prises

1. **Migration vers OpenRouter** : Abandon de Claude Code et Codex CLI pour utiliser OpenRouter afin de centraliser les appels API et éviter les frais supplémentaires.

2. **Passage sur lupo-rpi** : Tentative de stabilisation et freeze du setup du Raspberry Pi 5 (lupo-rpi) après une période d'instabilité.

3. **Utilisation d'Ollama avec SLM** : Recommandation validée (à 100%) pour déployer des Small Language Models quantisés (Q4_K_M en GGUF) sur le RPi 5 (8 Go) plutôt que des modèles full-size.

4. **Basculement manuel** : Après échec d'une automatisation, passage à une exécution manuelle du processus de configuration.

5. **Diagnostic pharmaceutique (Aenova)** : Intégration des données sur Aenova (8 sites industriels, expertise vétérinaire) et sur les CDMOs EU-GMP pour le projet Vetalyx.

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent le développement)

- **Erreur SQUASHFS sur NVMe** : `/mnt: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` → Le système ne peut pas booter, le disque est peut-être corrompu ou mal partitionné.

- **Instance Home Assistant dupliquée** : Message `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_install` → Deux instances de Home Assistant détectées (clonage/restauration de backup mal gérée). Empêche tout fonctionnement.

- **RPi 5 bloqué au démarrage hardware** : Le système "reste bloqué au tout début de la phase d'initialisation du matériel" sans progression visible.

- **Erreur de connexion SSH** : `upstream connect error or disconnect/reset before head` + `Broken pipe` → Impossible d'accéder au terminal RPi à distance.

### Sévères (dégradent fortement la productivité)

- **Whisper non fonctionnel** : Raison inconnue, détection nécessaire (est-ce un problème VSCode, d'installation locale ou d'API ?).

- **Ctrl+M ne fonctionne pas** : Raccourci clavier non opérationnel dans l'interface de travail.

- **team.db inaccessible** : Impossible d'accéder à la base de données, cause inconnue.

- **OpenRouter launcher dysfonctionnel** : La fonction de lancement affiche une erreur après clic, pas de dépannage appliqué.

---

## Questions récurrentes (signe de lacune documentaire)

1. **Comment configurer OpenRouter dans VSCode ?**
   - *Apparue 2+ fois* → Besoin d'une documentation interne claire sur l'intégration OpenRouter (choix de modèle, authentification, fallback).

2. **Pourquoi Whisper ne fonctionne pas en VSCode ?**
   - *Posée à plusieurs reprises* → Diagnostic incomplet, pas de solution trouvée, demande redondante.

3. **Comment accéder au terminal RPi depuis ma machine principale ?**
   - *Question récurrente dans le contexte des blocages SSH* → Manque de procédure de secours documentée, alternatives non explorées (SSH par IP, recovery mode, serial console).

4. **Pourquoi le RPi boot / ne boot pas ?**
   - *Vague et symptomatique* → Indique une compréhension fragmentaire du processus de démarrage et des étapes de diagnostic.

5. **Comment synchroniser le bootstrap entre M5 (gm 5.2) et RPi ?**
   - *Nouvelle question, non résolue* → Absence de documentation sur la gestion multi-machine.

---

## Nouveaux patterns détectés

### Patterns d'inefficacité

1. **Mode "trial-and-error" dominant** : Multiplicité de tentatives non documentées ("je vais essayer", "je vais le faire manuellement") sans capitalisation sur les tests antérieurs.

2. **Escalade de complexité sans consolidation** : Passage constant entre DeepSeek, Claude, OpenRouter, sans gouvernance claire des modèles à utiliser par domaine.

3. **Mémoire de session fragmentée** : Questions redondantes signalent que les insights précédents ne sont pas persisted correctement entre sessions.

4. **Déploiement multi-site complexe minimisé** : Aenova (8 sites industriels) mentionné en passant alors que cela devrait être un facteur dimensionnant du projet Vetalyx.

### Patterns positifs

- **Validation rapide** : Quand une solution fonctionne ("validé à 100%"), le feedback est clair et immédiat.
- **Expertise externe mobilisée** : JCH consulte des experts en amont (ex. recommandations LLM/hardware), ce qui réduit les essais stériles.
- **Pluralisme d'outils** : Capacité à mixer DeepSeek (performance), Claude (reasoning), OpenRouter (flexibilité).

---

## Efficacités / inefficacités

### ⚠️ Inefficacités majeures

| Symptôme | Coût | Cause probable |
|----------|------|---|
| Blocage SSH + accès terminal | 2–3h de downtime | Configuration réseau lupo-rpi instable, pas de plan B |
| Réinstallation Home Assistant (duplicate) | 1–2h | Pas de procédure de restauration sécurisée (UUID, staging) |
| Questions sur OpenRouter / VSCode posées 2x | 15–20min | Pas de wiki/runbook interne |
| Erreur SQUASHFS non résolue | Bloquant complet | Partitionnement / image ISO corruptée, diagnostic manque |
| Escalade DeepSeek→Claude→OpenRouter | 30min+ de contexte-switching | Absence de decision tree "quel modèle pour quel problème" |

### ✅ Points forts

- **Diagnostic d'expert mobilisé rapidement** : Les recommandations Ollama+Q4_K_M arrivent au bon moment.
- **Gestion du contexte** : Références claires aux projets (wildnexus, vetalyx, home assistant).
- **Décisions structurantes prises** : Migration OpenRouter est une bonne décision coût/flexibilité.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Bloqueurs à résoudre en priorité

1. **Réparer le lupo-rpi immédiatement** :
   - Tester l'image ISO (checksum)
   - Répartitionner le NVMe en fresh (risque perte de data)
   - Utiliser une serial console si SSH est mort
   - Alternative : rebrand sur une autre Pi/carte SD temporairement

2. **Supprimer la duplication Home Assistant** :
   - Identifier où l'instance "fantôme" tourne
   - Nettoyer les UUID/secrets en conflit
   - Documenter la procédure restore sécurisée

3. **Rétablir l'accès SSH** :
   - Vérifier hostname resolution (lupo-rpi.local)
   - Tester connexion par IP directe
   - Si mort : activer recovery mode SSH

### 🟡 Défis de connaissance à documenter

- **OpenRouter in VSCode** : Procédure pas-à-pas + config fichier `.vscode/settings.json`
- **Whisper debugging checklist** : Vérifier installation Ollama, permissions, port localhost:11434
- **M5/RPi bootstrap sync** : Comment partager la config d'amorçage entre machines

### 💾 Informations critiques à conserver

- **Aenova = 8 sites industriels vétérinaires approuvés** (facteur clé pour Vetalyx)
- **Ollama + Q4_K_M GGUF = solution validée** pour RPi 5 (8 Go)
- **OpenRouter = nouveau point central** pour API LLM (abandon Claude Code + Codex CLI)
- **RPi 5 setup = lupo-rpi.local**, SSH user: jchavaux
- **Modèles testés** : deepseek-v4, deepseek-v4-pro
- **Équipe mentionnée** : Dobby (orchestration), Forge (14x mentions), Argus

---

## Recommandations

### Court terme (24–48h)

1. **🚨 Créer une procédure de secours RPi** :
   - Documentation: "RPi SSH down? → Essayer [IP directe, serial, recovery mode, rebuild]"
   - Pré-configurer une image de fallback sur carte SD
   - Tester connexion SSH en mode offline (cable Ethernet direct)

2. **📋 Écrire un decision tree "Quel LLM utiliser ?"** :
   ```
   Tâche = code review → DeepSeek-v4-pro
   Tâche = brainstorm pharma → Claude (reasoning)
   Tâche = simple API call → OpenRouter + modèle léger
   Déploiement RPi → Ollama + SLM (Q4_K_M)
   ```

3. **🔧 Créer un wiki interne** avec :
   - OpenRouter + VSCode : step-by-step
   - Home Assistant restore sécurisé
   - Accès RPi troubleshooting (SSH, serial, network)
   - M5/RPi bootstrap sync

### Moyen terme (1–2 semaines)

4. **Consolidation du PKA (Personal Knowledge Archive)** :
   - Indexer les 1204 messages de session → extract patterns, decisions, questions
   - Créer des "memory tags" : `#vetalyx-pharmaceutical`, `#rpi-hardware`, `#openrouter-config`
   - Implémenter search_memory tool systématiquement

5. **Audit architectural du multi-machine** :
   - Valider la synchronisation M5 ↔ RPi ↔ Home Assistant
   - Documenter les points de défaillance unique (team.db, bootstrap, configs)
   - Plan de replication / backup sécurisé

6. **Valider la stack Ollama sur RPi** :
   - Déployer 2–3 SLM différents (Phi-3, Mistral 7B, Llama-2 7B)
   - Benchmarker latency + memory footprint
   - Documenter la config Ollama idéale pour production

### Long terme (> 2 semaines)

7. **Automatisation du déploiement** :
   - IaC pour lupo-rpi (Ansible / Docker Compose)
   - CI/CD pour validation image ISO avant deploy
   - Snapshots journaliers du team.db

8. **Réduction du multi-LLM** :
   - Migration complète → OpenRouter (économies + consistence)
   - Définir les modèles "cannonical" par JCH pour chaque domaine
   - Archiver DeepSeek TUI si OpenRouter couvre les besoins

---

## Synthèse exécutive

**État général** : Projet à forte valeur (Vetalyx pharma + WildNexus IoT) mais **bloqué par une infrastructure RPi instable** et **fragmenté par un tooling LLM non consolidé**.

**Risques immédiats** :
- Perte de productivité prolongée si lupo-rpi ne revient

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 42
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 39
- **Taux : 7.1%**

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

- [Decision] : Abandon de Claude Code et Codex CLI pour utiliser OpenRouter afin de centraliser les appels API et éviter les frais supplémentaires.
- [Decision] : Tentative de stabilisation et freeze du setup du Raspberry Pi 5 (lupo-rpi) après une période d'instabilité.
- [Decision] : Recommandation validée (à 100%) pour déployer des Small Language Models quantisés (Q4_K_M en GGUF) sur le RPi 5 (8 Go) plutôt que des modèles full-s
- [Decision] : Après échec d'une automatisation, passage à une exécution manuelle du processus de configuration.
- [Decision] : Intégration des données sur Aenova (8 sites industriels, expertise vétérinaire) et sur les CDMOs EU-GMP pour le projet Vetalyx.
- [Decision] Migration vers OpenRouter** : Abandon de Claude Code et Codex CLI pour utiliser OpenRouter afin de centraliser les appels API et éviter les frais supp
- [Decision] Passage sur lupo-rpi** : Tentative de stabilisation et freeze du setup du Raspberry Pi 5 (lupo-rpi) après une période d'instabilité.
- [Decision] Utilisation d'Ollama avec SLM** : Recommandation validée (à 100%) pour déployer des Small Language Models quantisés (Q4_K_M en GGUF) sur le RPi 5 (8 G
- [Decision] Basculement manuel** : Après échec d'une automatisation, passage à une exécution manuelle du processus de configuration.
- [Decision] Diagnostic pharmaceutique (Aenova)** : Intégration des données sur Aenova (8 sites industriels, expertise vétérinaire) et sur les CDMOs EU-GMP pour le
- [Failure] Erreur SQUASHFS sur NVMe** : `/mnt: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` → Le système ne peut pas booter, le disque est p
- [Failure] Instance Home Assistant dupliquée** : Message `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_install` → Deux insta
- [Failure] RPi 5 bloqué au démarrage hardware** : Le système "reste bloqué au tout début de la phase d'initialisation du matériel" sans progression visible.
- [Failure] Erreur de connexion SSH** : `upstream connect error or disconnect/reset before head` + `Broken pipe` → Impossible d'accéder au terminal RPi à distance

### Fréquence des patterns (14 jours)
- **Failure** : 9 jours, 56 occurrences
- **Decision** : 8 jours, 33 occurrences
- **Question** : 8 jours, 21 occurrences
- **Recurring question** : 7 jours, 20 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (3x) édente, échecs d'outils (ex: "L'API X a crashé hier avec l'erreur Y"), statuts d

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 14
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**302** recommandations au total — **302** ouvertes — **0** en cours — **0** terminées

⚠️ 245 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 260
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 4

### Plus récentes ouvertes

- [id=293] (2026-07-17) **Dobby** : 🚨 Créer une procédure de secours RPi** :
- [id=294] (2026-07-17) **Forge** : Documentation: "RPi SSH down? → Essayer [IP directe, serial, recovery mode, rebu
- [id=295] (2026-07-17) **Dobby** : Pré-configurer une image de fallback sur carte SD
- [id=296] (2026-07-17) **Dobby** : Tester connexion SSH en mode offline (cable Ethernet direct)
- [id=297] (2026-07-17) **Dobby** : 📋 Écrire un decision tree "Quel LLM utiliser ?"** :

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $24.85 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $24.85**
