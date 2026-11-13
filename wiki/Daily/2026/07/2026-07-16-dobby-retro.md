---
date: 2026-07-16
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1258
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-16

**Sessions analysées :** 4 | **Échanges :** 1258 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS DU 2026-07-16
## JCH + Assistants IA (DeepSeek TUI, Claude Code, Codex CLI)

---

## Décisions prises

1. **Retour à lupo-rpi pour figer le setup** → Priorisation du matériel RPi 5 (8 Go) avec SSD NVMe comme base stable.
2. **Migration vers OpenRouter** → Abandon de la gestion des crédits API directs (Claude/DeepSeek), utilisation d'OpenRouter comme agrégateur pour réduire la friction opérationnelle.
3. **Abandon de la synchronisation bootstrap manuelle** → "Je vais le faire manuellement" indique un échec de l'automatisation pour GM 5.2 ↔ RPi ; décision de contourner plutôt que de corriger.
4. **Départ camping 25/07 à 15:00 depuis Namu** → Engagement calendaire ferme, impact potentiel sur continuité de développement.
5. **Validation et mise à jour des fichiers (plantes/bioacoustique)** → Décision de créer un fork du projet bioacoustique pour isoler le travail.

**⚠️ Problème critique** : Les décisions sont **parsemées dans le flux conversationnel**, jamais formalisées en "checkpoint de décision". Impossible de tracer *pourquoi* OpenRouter plutôt qu'une alternative, ou *quand* lupo-rpi sera considéré "figé".

---

## Échecs ouverts / bloqueurs

### Matériel / Infrast structure
- **SQUASHFS superblock error** (`/mnt: fsconfig() failed`) → Corruption NVMe probable ; état du SSD unclear.
- **Whisper ne fonctionne pas en VSCode** → Repeated 3 times ; root cause jamais diagnostiquée (environnement locale vs. conteneur ?)
- **Terminal RPI inaccessible** → "pourquoi tu n'as pas acces au terminal rpi ?" → Tailscale/SSH ? Permission ? State inconnu.
- **Hardware lupo-rpi "presque prêt"** → SD endurance + silent bloc manquants, mais pas de timeline affectée.

### Réseau / Services
- **NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT** → MQTT/Zigbee stack instability détectée mais non résolue.
- **HTTP 404 cascadé** → "404: haos_*.xz", "upstream connect error or disconnect/reset before head" → Téléchargement/restoration Home Assistant bloqué.
- **Conflits Home Assistant OS** → Instance dupliquée détectée (UUID duplicate, réseau/disque). Cause : restauration sauvegarde non nettoyée.

### Logiciel
- **Ctrl+M affiche "m" au lieu de fonctionnalité** → Binding VSCode cassé, symptomatique de configuration fragmentée.
- **team.db inaccessible** → "pourquoi inaccessible ?" → Pas de résolution documentée.

**🔴 Pattern dangereux** : Les bloqueurs s'accumulent sans escalade. JCH essaie des contournements ("je vais le faire manuellement") plutôt que de déboguer structurellement.

---

## Questions récurrentes (signe de lacune documentaire)

1. **"Comment configurer OpenRouter dans VSCode ?"** (×2 minimum)
   - → **Lacune** : Pas de doc "OPENROUTER_SETUP.md" accessible.
   - → **Impact** : Réinstruction à chaque session, friction cognitive.

2. **"Pourquoi Whisper ne marche pas ?"** (×3)
   - → **Lacune** : Absence de checklist diagnostic (env vars, dépendances Python, conteneur vs. host).
   - → **Impact** : Boucle infinie de débogage superficiel.

3. **"Pourquoi pas d'accès terminal RPI ?"** (×2)
   - → **Lacune** : État de la connexion Tailscale/SSH jamais documté ; pas de health check proactif.
   - → **Impact** : Dépend de l'assistant pour diagnostiquer à chaque fois.

4. **"C'est quoi le X1201-C1 ?"**
   - → **Lacune** : Composants matériels non catalogués dans la liste de pièces (BOM).
   - → **Impact** : Confusion lors de l'assemblage, décisions d'achat non tracées.

**💡 Signal** : Ces questions révèlent **3 documents manquants critiques** :
- `OPENROUTER_INTEGRATION.md`
- `WHISPER_TROUBLESHOOTING.md`
- `HARDWARE_BOM.md` avec cross-ref composants

---

## Nouveaux patterns détectés

### 1. **"Mélange domaines" sans séparation claire**
- Session bascule : **pharma vétérinaire** (hydrocortisone aceponate Virbac) → **domotique** (Home Assistant) → **bioacoustique** (plantes) → **électronique** (MEMS mic, IR sensors).
- Cause probable : PKA unique pour tous les projets, pas de segmentation par contexte.
- **Risque** : Contamination cognitive, confusion d'outils/configs entre domaines.

### 2. **"Transcripts polluées par du contenu copié/pasted"**
- Extraits comme "The primary pharmaceutical producer..." sont clairement du résultat d'une recherche web copiée, pas du context du projet JCH.
- → Suggests : Assistants importent du contexte de session précédente sans filtrer.
- → **Action requise** : Nettoyer la base de context ; segmenter par projet.

### 3. **"Validation sans persistence"**
- "oui on valide mets à jours tous les fichihers" → Mais aucune trace que ces fichiers ont été **actuellement** sauvegardés ou commitées.
- Git commit hash ? Pas mentionné. État de `MEMORY.md` ? Inconnu.

### 4. **"Escalade manuelle > automatisation"**
- Whisper failure → Contournement vs. diagnostic.
- Bootstrap GM 5.2 → Manual vs. Script.
- **Symptôme** : Incoming débit technique supérieur à capacité de JCH solo.

### 5. **"Date limite externe (camping 25/07)"**
- Crée urgence artificiële ; risque de décisions de "quick fix".
- Aucune checkpoint de "ce qui doit être fait avant 25/07".

---

## Efficacités / inefficacités

### ✅ Efficacités
- **OpenRouter decision** → Réduit friction API management, permet rotation de modèles sans refactoring.
- **Photo diagnostic** (Canon EOS R10 + RF 200-800mm) → Rapidement confirmée par Dobby, good for hardware tracking.
- **Expert consultation** (recommandations SLM/Ollama) → Apporte structure, évite du trial-and-error.

### ❌ Inefficacités (majeures)
1. **Pas de triaging de bloqueurs** → 8 issues concurrentes, aucune priorisation.
2. **Questions répétées** → Signale PKA non persistant ou non accessible pendant session.
3. **Transcript non-structuré** → Décisions, bloqueurs, décisions imbriquées ; difficile à extraire.
4. **Pas de state machine** → "Terminal inaccessible" devrait triggerautomatique fallback, pas être redécouverte.
5. **Timeboxing absent** → Session à 4 turn sur 4 jours; pas de limite de déperdition.
6. **Conteneurisation confuse** → VSCode local vs. remote RPi vs. container ; state d'où tourne quoi est flou.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 État Critique
- **lupo-rpi** : Hardware "presque figé", NVMe peut être corrompue (SQUASHFS error), pas encore de SD endurance/silent bloc.
- **Home Assistant** : Instance dupliquée, restoration bloquée (404), UUID conflict → Besoin de full reset + sauvegarde nettoyée.
- **Terminal RPI** : Inaccessible, cause unknown → Priorité diagnostic n°1 avant continuation domotique.

### 🟡 État Suspendu
- **Whisper** : Ne fonctionne pas, diagnostic jamais complété. Check : env Python, dépendances, host vs. container.
- **Synchronisation Bootstrap** : GM 5.2 ↔ RPi non automatisée, contournement manuel utilisé temporairement.
- **X1201-C1 & BOM** : Composants non catalogués, risque d'erreur d'assemblage.

### 🟢 Points d'Ancrage
- **OpenRouter choisi** → Documenter config VSCode OpenRouter rapidement (template prêt pour prochaine session).
- **Expert consulté** → Recommandations SLM/Ollama pour RPi 5 (8 Go) restent valables.
- **Projets segments** :
  - Domotique (Home Assistant + Zigbee2mqtt)
  - Bioacoustique (fork en cours)
  - Pharma vétérinaire (recherche, pas de dev)

### 📅 Contrainte Externe
- **Départ 25/07 à 15:00 depuis Namu** → ~9 jours restants ; prioriser lupo-rpi stabilité + camping offline prep.

---

## Recommandations

### 🎯 Immédiates (avant prochaine session)

1. **Créer `DECISION_LOG.md`** dans `/JCH_Inbox/`
   - Format : `[Date] [Projet] [Décision] → [Raison] → [État: Open/Closed]`
   - Exemple : `[2026-07-16] [Domotique] Utiliser OpenRouter → Réduire friction API → Open`
   - → Permet recherche rapide et continuité.

2. **Diagnostic terminal RPI (30 min)**
   ```bash
   # Ajouter à MEMORY.md :
   - État Tailscale : [A vérifier]
   - SSH public key sur RPi : [A vérifier]
   - Ping RPi via Tailscale : [A vérifier]
   ```
   → Bloqueur #1, doit être résolu avant domotique continue.

3. **Isoler Whisper dans conteneur diagnostic**
   ```dockerfile
   # Créer : /docs/docker-compose.whisper.yml
   # Teste Whisper en isolation (env contrôlé)
   # Documenter: quelle version, quelle config réussit
   ```
   → Évite contamination VSCode local.

4. **Créer `OPENROUTER.md`** (15 min)
   - APIkey storage (Tailscale secret ?)
   - VSCode extension config
   - Model selection logic
   - → Évite la question récurrente #1.

5. **Home Assistant reset planning**
   - Avant 25/07 : Snapshots à jour + vérifier UUID conflicts
   - Restore plan documenté dans `HOMEASSISTANT_RESTORE.md`
   - → Bloqueur #2, doit être *terminé* avant camping (offline mode).

### 📋 Court Terme (semaine)

6. **Segmenter PKA par projet** dans `/TEAM/`
   - `DOMOTIQUE_PKA.md` (Home

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 49
- Résolus automatiquement : 13
- Résolus manuellement : 0
- Encore ouverts : 36
- **Taux : 26.5%**

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

- [Decision] → Priorisation du matériel RPi 5 (8 Go) avec SSD NVMe comme base stable.
- [Decision] → Abandon de la gestion des crédits API directs (Claude/DeepSeek), utilisation d'OpenRouter comme agrégateur pour réduire la friction opérationnelle.
- [Decision] → "Je vais le faire manuellement" indique un échec de l'automatisation pour GM 5.2 ↔ RPi ; décision de contourner plutôt que de corriger.
- [Decision] → Engagement calendaire ferme, impact potentiel sur continuité de développement.
- [Decision] → Décision de créer un fork du projet bioacoustique pour isoler le travail.
- [Decision] : Les décisions sont **parsemées dans le flux conversationnel**, jamais formalisées en "checkpoint de décision". Impossible de tracer *pourquoi* OpenR
- [Decision] Retour à lupo-rpi pour figer le setup** → Priorisation du matériel RPi 5 (8 Go) avec SSD NVMe comme base stable.
- [Decision] Migration vers OpenRouter** → Abandon de la gestion des crédits API directs (Claude/DeepSeek), utilisation d'OpenRouter comme agrégateur pour réduire 
- [Decision] Abandon de la synchronisation bootstrap manuelle** → "Je vais le faire manuellement" indique un échec de l'automatisation pour GM 5.2 ↔ RPi ; décision
- [Decision] Départ camping 25/07 à 15:00 depuis Namu** → Engagement calendaire ferme, impact potentiel sur continuité de développement.
- [Decision] Validation et mise à jour des fichiers (plantes/bioacoustique)** → Décision de créer un fork du projet bioacoustique pour isoler le travail.
- [Failure] SQUASHFS superblock error** (`/mnt: fsconfig() failed`) → Corruption NVMe probable ; état du SSD unclear.
- [Failure] Whisper ne fonctionne pas en VSCode** → Repeated 3 times ; root cause jamais diagnostiquée (environnement locale vs. conteneur ?)
- [Failure] Terminal RPI inaccessible** → "pourquoi tu n'as pas acces au terminal rpi ?" → Tailscale/SSH ? Permission ? State inconnu.
- [Failure] Hardware lupo-rpi "presque prêt"** → SD endurance + silent bloc manquants, mais pas de timeline affectée.

### Fréquence des patterns (14 jours)
- **Decision** : 8 jours, 32 occurrences
- **Failure** : 8 jours, 53 occurrences
- **Question** : 8 jours, 22 occurrences
- **Recurring question** : 7 jours, 20 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (3x) édente, échecs d'outils (ex: "L'API X a crashé hier avec l'erreur Y"), statuts d

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 15
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**292** recommandations au total — **292** ouvertes — **0** en cours — **0** terminées

⚠️ 240 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 252
- **Forge** : 32
- **Corbeau** : 4
- **Furet** : 4

### Plus récentes ouvertes

- [id=275] (2026-07-16) **Dobby** : Créer `DECISION_LOG.md`** dans `/JCH_Inbox/`
- [id=276] (2026-07-16) **Dobby** : Format : `[Date] [Projet] [Décision] → [Raison] → [État: Open/Closed]`
- [id=277] (2026-07-16) **Dobby** : Exemple : `[2026-07-16] [Domotique] Utiliser OpenRouter → Réduire friction API →
- [id=278] (2026-07-16) **Furet** : → Permet recherche rapide et continuité.
- [id=279] (2026-07-16) **Dobby** : Diagnostic terminal RPI (30 min)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $24.85 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $24.85**
