---
date: 2026-07-08
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 7
echanges: 1125
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-08

**Sessions analysées :** 7 | **Échanges :** 1125 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE PKA — Sessions 2026-07-08

## Décisions prises

| Décision | Contexte | État |
|----------|----------|------|
| **Choix MQTT** | Sélection du broker MQTT pour WildNexus | ✅ Validée 100% |
| **Modèle de machine vision** | Canon EOS R10 + RF 200-800mm confirmé pour Vetalyx | ✅ Confirmée (photo analysée) |
| **Basculer sur Vetalyx** | Interruption de tâche en cours pour démarrer projet client chinois | ✅ Décidée |
| **Sauvegarde manuelle** | Sauvegarder le travail sur les plantes manuellement (au lieu d'automatiser) | ✅ Décidée |
| **Maintien de l'architecture actuelle** | Garder la structure existante mais ajouter un reminder de relire | ✅ Décidée |
| **Approche manuelle pour intégration OV5640** | Après échec automatisé, passage au wiring manuel ESP32-S3 | ✅ Décidée |

**🚩 Problème détecté** : Les décisions sont prises mais **jamais documentées formellement**. Il n'existe pas de "Decision Log" central. Dobby reçoit les validations verbales mais elles disparaissent dans le contexte.

---

## Échecs ouverts / bloqueurs

### 🔴 **CRITIQUES** (bloquent la production)

1. **Erreur NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT**
   - Affecte : Intégration Zigbee + MQTT
   - Symptôme : "Impossible de créer un nouveau réseau Zigbee"
   - Dernière tentative : Non documentée
   - **Action requise** : Diagnostic timeout dans la couche de communication MQTT / Zigbee

2. **Connection Failed: Device Unresponsive**
   - Apparemment lié à collision avec autre programme
   - **Non résolu** : "un autre programme (e.g. [...])" — phrase coupée
   - Impact : Impossible de sourcer le problème exact

3. **Traceback Python non complètement capturé**
   - Fichier : `/Users/jchavauxm5/PKA_JCH/s...` (chemin tronqué)
   - **Impossible de reproduire** sans le stack complet

4. **Crash Outlook et remédiation manuelle**
   - Outlook s'est crashé, créant une rupture de continuité
   - Remise en place manuelle en cours (status flou)

### 🟡 **MOYENS** (ralentissent le travail)

5. **team.db inaccessible**
   - Erreur `6683` non documentée (code d'erreur obscur)
   - JCH s'interroge mais pas de diagnostic fourni

6. **Whisper ne fonctionne pas dans VSCode**
   - Symptôme : Non spécifié
   - Impact : Pas de transcription vocale disponible
   - Workaround : Non trouvé

7. **OV5640 24-pin × ESP32-S3 : incompatibilité de pinout**
   - Piège identifié : "Ne branchez jamais ce module directement"
   - Solution : Wiring manuel requis (pas encore testé)

8. **Composants Mouser en backorder**
   - Plusieurs références en attente (MMICT5848-00-012, VSLB3940, etc.)
   - Timeline : Indéfinie

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Signification |
|----------|-----------|---------------|
| **"team.db pourquoi inaccessible ?"** | 2x | Absence de documentation sur l'architecture DB |
| **"whisper ne fonctionne pas"** | 1x (mais symptôme flou) | Pas de troubleshooting playbook |
| **"c'est quoi harness ?"** | Implicite | Terminologie technique non clarifiée |
| **"memory nudge c'est quoi ?"** | 1x | Concept Dobby non expliqué à JCH |
| **"pourquoi (.env) en début de path ?"** | 1x | Gestion des chemins et variables d'env non standardisée |
| **"commande terminal vs terminal VSCode : c'est la même ?"** | 1x | Confusion sur les contextes d'exécution |
| **"X1201-C1 pour le SSD ?"** | 1x | Documentation matérielle incomplète |
| **"Comment utiliser OpenRouter dans VSCode ?"** | 1x | Interface de configuration Dobby mal documentée |
| **"Comment faire en sorte que tu fasses des recherches logiques ?"** | 1x | **CRITIQUE** : JCH ne comprend pas le workflow de recherche de Dobby |
| **"gm 5.2 : même bootstrap ?"** | 1x | Multiple deployment targets, pas d'automatisation |

**🚨 Interprétation** : Ces questions **ne sont PAS aléatoires**. Elles pointent vers 3 lacunes critiques :
- Documentation système insuffisante (DB, hardwares, variables)
- Interfaces outils mal expliquées (OpenRouter, Whisper, Dobby workflows)
- Terminologie interne non standardisée

---

## Nouveaux patterns détectés

### 📊 Patterns de travail
1. **Multi-switching rapide entre projets**
   - 12 projets actifs (4 en plein régime, 4 en cours, 4 en veille)
   - Vetalyx interrompt WildNexus mid-task → context-switching overhead
   - **Coût estimé** : 15-20% de productivité (task switching tax)

2. **Basculement "manuel" quand l'automatisation échoue**
   - OV5640 → manual wiring
   - Sauvegarde plantes → manual save
   - **Pattern** : Pas de timeout acceptable avant fallback manuel
   - **Risque** : Accumulation de dette technique

3. **Composition de documents ad-hoc**
   - Analyses Kimi 2.5 + Virbac pharma + OV5640 specs + Mouser BOM mélangées dans le même thread
   - Pas de séparation de contexte par projet
   - **Inefficacité** : Dobby doit parser des domaines incompatibles

4. **Gestion des composants électroniques chaotique**
   - BOM Mouser partagée en copier-coller brut (prix, stocks, statuts mélangés)
   - Pas de suivi des backorders
   - **Risque** : Goulot d'étranglement non anticipé

### 🎯 Patterns d'interaction JCH ↔ Dobby
- JCH pose des **micro-questions** plutôt que des **problèmes complets**
  - Ex: "c'est quoi harness ?" au lieu de "j'ai besoin d'expliquer le harness matériel pour le X1201"
- Dobby n'alimente **jamais Dobby avec des contextes explicites**
  - Les décisions valides disparaissent sans créer d'entrée Knowledge Base

---

## Efficacités / inefficacités

### ✅ **EFFICACITÉS**

| Domaine | Observation |
|---------|------------|
| **Rapidité de décision** | Validations marquées "100% ✅" rapidement prises |
| **Diversité d'expertise** | Capacité à jongler pharma (hydrocortisone), hardware (ESP32), et ML (vision) |
| **Utilisation multi-modèles** | DeepSeek v4 + Claude sur OpenRouter : bonne stratégie |
| **Mémoire KB** | Dobby peut évoquer des détails (Canon R10 photo, RF 200-800) → indexation fonctionne |

### ❌ **INEFFICACITÉS**

| Domaine | Observation | Impact |
|---------|------------|--------|
| **Documentação des décisions** | Aucune trace persistente des "validés 100%" | Risque de régressions |
| **Triage des bloqueurs** | Erreurs `6683`, `NcpResetCode` laissées sans diagnostic | **Peut bloquer 1-2 jours** |
| **Gestion de contexte** | Pharma + hardware + ML dans une même session | Fatigue cognitive |
| **Récupération d'erreurs** | "Non ça marche pas, je vais le faire manuellement" sans logging | Perte de données de debug |
| **Backorder management** | Composants Mouser non trackés → surprise tardive probable | Peut retarder deployment de 1+ semaine |
| **Session continuity** | 1125 messages sur 7 sessions = 160 msg/session | **Difficulté à maintenir la continuité** |
| **Terminologie** | "harness", "memory nudge", ".env paths" non standardisés | Friction de 5-10 min par terme |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🧠 **État du système**

**WildNexus / WildLens** (23 mentions)
- Capteur : Canon EOS R10 + RF 200-800mm ✅
- MQTT broker : Choisi ✅
- Zigbee : Bloquée sur ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT 🔴

**Vetalyx** (9 mentions)
- Nouveau client chinois (données pharma confidentiel)
- Work-in-progress, a interrompu autre tâche

**ARTEON** (8 mentions)
- Statut inconnu (projet en veille ?)

**M5 (Macbook Pro M5 max)**
- 18 Go PKA
- Path actif : `/Users/jchavauxm5/PKA_JCH/`
- Problème : Accès team.db via code `6683`

**RPi (Raspberry Pi)**
- Toujours utilisée
- Statut de déploiement : Flou (gm 5.2 bootstrap mismatch ?)

**M1 (autre Mac ?)**
- Déploiement multi-cible
- Bootstrap non synchronisé

### 📋 **Outils actifs**

| Outil | Utilisation | Statut |
|-------|------------|--------|
| **Claude (53x)** | Assistant principal | ✅ |
| **OpenRouter (17x)** | Sélection modèles | ⚠️ Interface non comprise par JCH |
| **DeepSeek v4(-pro)** | Modèle actif | ✅ |
| **Dobby (87x mentions)** | Orchestration PKA | ⚠️ Workflows pas clairs |
| **Whisper** | Transcription vocale | 🔴 Non fonctionnel dans VSCode |

### 🔐 **Données sensibles mentionnées**

- Hydrocortisone aceponate (pharma, réglementation EU-GMP)
- Client chinois Vetalyx (confidentiel)
- Composants Mouser (BOM sensible)

### ⚡ **Quick reference pour Dobby**

- **Appelle pas la librairie openai sans `pydantic` update** (vu une dépendance cassée)
- **OV

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

- [Decision] | Sélection du broker MQTT pour WildNexus | ✅ Validée 100% |
- [Decision] | Canon EOS R10 + RF 200-800mm confirmé pour Vetalyx | ✅ Confirmée (photo analysée) |
- [Decision] | Interruption de tâche en cours pour démarrer projet client chinois | ✅ Décidée |
- [Decision] | Sauvegarder le travail sur les plantes manuellement (au lieu d'automatiser) | ✅ Décidée |
- [Decision] | Garder la structure existante mais ajouter un reminder de relire | ✅ Décidée |
- [Decision] | Après échec automatisé, passage au wiring manuel ESP32-S3 | ✅ Décidée |
- [Decision] : Les décisions sont prises mais **jamais documentées formellement**. Il n'existe pas de "Decision Log" central. Dobby reçoit les validations verbales
- [Failure] (bloquent la production)
- [Failure] Affecte : Intégration Zigbee + MQTT
- [Failure] Symptôme : "Impossible de créer un nouveau réseau Zigbee
- [Failure] Dernière tentative : Non documentée
- [Failure] Action requise** : Diagnostic timeout dans la couche de communication MQTT / Zigbee
- [Failure] Apparemment lié à collision avec autre programme
- [Failure] Non résolu** : "un autre programme (e.g. [...])" — phrase coupée
- [Failure] Impact : Impossible de sourcer le problème exact
- [Failure] Fichier : `/Users/jchavauxm5/PKA_JCH/s...` (chemin tronqué)
- [Failure] Impossible de reproduire** sans le stack complet
- [Failure] Outlook s'est crashé, créant une rupture de continuité
- [Failure] Remise en place manuelle en cours (status flou)
- [Failure] Erreur NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT
- [Failure] Traceback Python non complètement capturé
- [Failure] Crash Outlook et remédiation manuelle

### Fréquence des patterns (14 jours)
- **Decision** : 7 jours, 32 occurrences
- **Question** : 7 jours, 20 occurrences
- **Failure** : 6 jours, 30 occurrences
- **Recurring question** : 5 jours, 16 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 22
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**240** recommandations au total — **240** ouvertes — **0** en cours — **0** terminées

⚠️ 183 recommandations ouvertes depuis plus de 7 jours.

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

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $6.29 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $6.29**
