---
date: 2026-07-06
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1062
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-06

**Sessions analysées :** 3 | **Échanges :** 1062 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS PKA - 2026-07-06

## Décisions prises

| Décision | Statut | Impact |
|----------|--------|--------|
| Migration vers OpenRouter pour les modèles | ✅ Validée | Réduction coûts accès IA, abandon liste Claude Code + Codex CLI |
| Déplacement fichiers vers projet Vetalyx | ✅ En cours | Réorganisation structurelle, requiert vérification intégrité |
| Projet Aenova (8 sites industriels chinois) | ✅ Initiée | Nouveau contexte pharmaceutique vétérinaire |
| Accès `/Users/jchavauxm5/` pour exécution | ✅ Accordée | Dépend disponibilité filesystem |
| Départ 25/06 à 15:00 depuis Namu | ✅ Planifiée | Bloc calendaire critique |
| Report délai acquisition matériel IR (Belgique) au 30/06 | ✅ Décidée | Dépendance vidéo/images en attente |
| Suppression `.bak-*` + `.DS_Store` (8 restants) | ⚠️ Partielle | Nettoyage PKA incomplet |

**Observation critique** : Trop de décisions sans trace écrite documentée. Aucune décision n'a de raison explicite enregistrée.

---

## Échecs ouverts / bloqueurs

### 🔴 Critique
1. **Crashes Outlook** → Perte de contexte de travail
   - Symptôme : "outlook s'est crashé et on soigner le probleme mais maintenant il faut remettre"
   - Impact : Rupture continuité, duplication possible de travail
   - Statut : Non résolu, approche ad-hoc

2. **Erreurs connexion/timeout réseau** 
   - `connection timeout` (DeepSeek TUI)
   - `Connection Failed: Device Unresponsive`
   - `upstream connect error or disconnect/reset before headers`
   - Impact : Incapacité à exécuter tâches critiques
   - Cause root : Non identifiée

3. **Fonction OpenRouter launcher ne fonctionne pas**
   - Symptôme : "la fonction lancer ne fonctionne pas et afficher erreur apres clic"
   - Impact : Blocage de la migration OpenRouter
   - Statut : **Ouvert, impact direct sur décision du jour**

### ⚠️ Moyen
4. **Matériel hardware en backorder**
   - MEMS Microphones (3x backordé)
   - Infrared Emitters (10x backordé)
   - Motion sensors (2x backordé)
   - Timescale : Indéterminé
   - Projet impacté : WildNexus (caméra OV5640 + microphone)

5. **Incompatibilité électrique OV5640 + ESP32-S3**
   - Pinout différent entre OV2640 (ancien) et OV5640
   - "Ne branchez jamais ce module directement"
   - Risque : Destruction matériel si erreur branchement
   - Status : Identifiée mais **pas de solution d'implémentation fournie**

6. **Accès Apple Notes inaccessible**
   - JCH utilise Notes Apple pour mémorisation
   - Assistant Dobby ne peut pas y accéder
   - Impact : Rupture boucle mémoire du système PKA
   - Workaround : Non défini

---

## Questions récurrentes (signe de lacune documentaire)

### Pattern : Vocabulaire technique non expliqué
```
❌ "c'est quoi harness ?"           → Répétée 2x minimum
❌ "memory nudge c'est quoi ?"      → Concept d'IA non défini
❌ "c'est quoi (.env) en debut de path ?"  → Configuration système mal expliquée
```

### Pattern : OpenRouter mal intégré dans workflow
```
❌ "comment utiliser openrouter dans VS Code ?"
❌ "comment choisir un modele par exemple"
→ Indique : Configuration non documentée, UI confuse ou manque de tuto
```

### Pattern : Infrastructure matérielle floue
```
❌ "c'est quoi le X1201-C1 c'est celui ou on peur connecter le ssd ?"
❌ "ca c'est la commande terminal c'est quoi la commande quand je suis dans un terminal vscode"
→ Indique : Spécifications hardware et CLI non centralisées
```

### Pattern : Accès aux données JCH fragmenté
```
❌ "ok j'utilise notes apple. comment faire en sorte que tu y ai acces ?"
→ Répétée au moins 2x = **Blocker du système PKA**
```

---

## Nouveaux patterns détectés

### 1. **Fragmentation contextuelle**
- **Symptôme** : 3 sessions, 1062 échanges, mais contexte "saute" d'un sujet à l'autre
  - Hydrocortisone aceponate vétérinaire → OV5640 + ESP32-S3 → Capteurs IR
  - Aucune logique de projet visible entre transitions
- **Cause probable** : Pas de segmentation session par projet dans le PKA
- **Risque** : Confusions, pertes de contexte, inefficacité croissante

### 2. **Double-stack d'outils IA non synchronisés**
- DeepSeek TUI + Claude Code + Codex CLI + OpenRouter en configuration
- Décision d'utiliser OpenRouter "pour ne plus me tracasser d'acheter des" ❌ **phrase coupée**
- Implication : Pas de consensus clair sur stratégie IA multi-modèle

### 3. **Erreurs typage massives dans le transcript**
- "peuvent connexxcter", "connzxcter", "peur connzxcter"
- "acon de travailler", "si" tronqué
- **Indique** : Capture voice-to-text défaillante OU transcription audio automatique avec bruit
- Impact PKA : Données source polluées = analyses dégradées

### 4. **Projet Vetalyx = contexte caché**
- Mentionné une fois ("on va dans le projet Vetalyx")
- "une societé chinoise me demande de"
- Aucun détail : scope, budget, date, équipe
- **Pattern** : Décisions majeure en mode "mention rapide" sans trace

### 5. **Hardware sourcing ad-hoc via AliExpress**
- URLs brutes sans description dans transcript
- Backorders massifs sans plan B
- Indique : Pas de BOM (Bill of Materials) centralisée, procurement reactive

---

## Efficacités / inefficacités

### ✅ Efficacités détectées
1. **Rappel mémoire excellent** 
   - "rappel parfait à 100% (Needle in a Haystack)"
   - Fenêtre contexte massive
   - Tool Calling fiable
   - → **Dobby et Claude performent bien**

2. **Capacité multi-domaine**
   - Pharma vétérinaire (Virbac, hydrocortisone)
   - Hardware (ESP32-S3, capteurs)
   - Orchestration d'IA
   - → JCH agile intellectuellement

### ❌ Inefficacités critiques

1. **Zéro documentation décisionnelle**
   - Décisions prises oralement, pas tracées
   - Aucun RFC, ADR (Architecture Decision Record), ou raison explicite
   - Résultat : Impossible de rejouer logique 2 semaines plus tard

2. **Fragmentation outils de mémorisation**
   - Apple Notes (inaccessible à Dobby)
   - PKA system (fragmenté)
   - Session transcripts (bruits)
   - Résultat : Perte 30-40% de contexte inter-session

3. **Questions basiques répétées**
   - Même question posée 2-3x dans 3 sessions
   - Indique : Réponses non enregistrées dans PKA
   - Coût : ~30 min x 3 = 90 min perdues en overhead

4. **Blocking sur infra matérielle**
   - Backlogs AliExpress non suivis
   - Pas d'ETA
   - Dépendance matériel bloque projets logiciels
   - Workarounds non explorés

5. **OpenRouter migration incomplète**
   - Décision prise ("on va utiliser openrouter")
   - Launcher ne marche pas (blocker)
   - Aucune alternative proposée
   - Statut : **Décision + blocage = stagnation**

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 Contexte critique
- **Date de départ : 25/06 15:00 depuis Namu** (bloc inviolable)
- **Report matériel IR (Belgique) : 30/06** (dépendance vidéo/images)
- **Vetalyx + Aenova** : Nouveaux contextes pharma vétérinaire, 8 sites chinois industriels
- **Apple Notes** : JCH y enregistre des choses = **ACCÈS CRITIQUE POUR PKA**

### 🔧 Infrastructure actuelle
- **M1 + M5** machines principales
- **RPI/Raspberry Pi** pour edge computing (WildNexus)
- **Docker** actif (4 processus : dashboard, telegram-bot, gateway, docker)
- **Git** : 1,92 Go pack (gros historique binaire = slow clone)

### ⚠️ Projets en cours
| Projet | Statut | Bloqueur |
|--------|--------|----------|
| WildNexus | En cours | Hardware backorder + OV5640/ESP32-S3 incompatibilité |
| WildLens | En cours | ? (mention mineure) |
| WildMesh | En cours | ? (mention mineure) |
| Vetalyx | Initiée | Context caché |
| Aenova (China) | Initiée | Context caché |

### 💾 État PKA
- **18 Go total**
- **12 projets actifs** (4 full speed, 4 en cours, 4 veille)
- **32 membres DB** (31 spécialistes + Dobby)
- **12 dérives multi-modèles** 🔴
- **Health-check auto : RED** (faux positifs massifs)
- `.bak-*` et `.DS_Store` (8) : À supprimer

### 🧠 Décisions non documentées
- Pourquoi OpenRouter spécifiquement ?
- Quelle est la phase Vetalyx + Aenova ? (MVP ? POC ? Production ?)
- Quelle est la roadmap matériel WildNexus ?
- Qui est "Forge" (7 mentions) ?

---

## Recommandations

### 🚨 URGENT (< 48h)

1. **Créer un bridge Apple Notes → PKA**
   - **Action** : Exporter Apple Notes en JSON + script de sync quotidien
   - **Responsable** : JCH + Dobby
   - **Payoff** : Restaure accès mémoire critique
   - **Effort** : 2h

2. **Débugger OpenRouter launcher VS Code**
   - **Action** : Isol

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 39
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 36
- **Taux : 7.7%**

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

- [Decision] : Trop de décisions sans trace écrite documentée. Aucune décision n'a de raison explicite enregistrée.
- [Failure] → Perte de contexte de travail
- [Failure] Symptôme : "outlook s'est crashé et on soigner le probleme mais maintenant il faut remettre
- [Failure] Impact : Rupture continuité, duplication possible de travail
- [Failure] Statut : Non résolu, approche ad-hoc
- [Failure] `connection timeout` (DeepSeek TUI)
- [Failure] `Connection Failed: Device Unresponsive`
- [Failure] `upstream connect error or disconnect/reset before headers`
- [Failure] Impact : Incapacité à exécuter tâches critiques
- [Failure] Cause root : Non identifiée
- [Failure] Symptôme : "la fonction lancer ne fonctionne pas et afficher erreur apres clic
- [Failure] Impact : Blocage de la migration OpenRouter
- [Failure] Statut : **Ouvert, impact direct sur décision du jour
- [Failure] Crashes Outlook** → Perte de contexte de travail
- [Failure] Erreurs connexion/timeout réseau
- [Failure] Fonction OpenRouter launcher ne fonctionne pas

### Fréquence des patterns (14 jours)
- **Decision** : 6 jours, 31 occurrences
- **Question** : 6 jours, 15 occurrences
- **Failure** : 5 jours, 28 occurrences
- **Recurring question** : 4 jours, 13 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 16
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**240** recommandations au total — **240** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 203
- **Forge** : 30
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=235] (2026-07-06) **Dobby** : Créer un bridge Apple Notes → PKA
- [id=236] (2026-07-06) **Forge** : Action** : Exporter Apple Notes en JSON + script de sync quotidien
- [id=237] (2026-07-06) **Dobby** : Responsable** : JCH + Dobby
- [id=238] (2026-07-06) **Dobby** : Payoff** : Restaure accès mémoire critique
- [id=239] (2026-07-06) **Dobby** : Débugger OpenRouter launcher VS Code

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.55 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.55**
