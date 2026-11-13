---
date: 2026-06-29
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1017
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-29

**Sessions analysées :** 2 | **Échanges :** 1017 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE PKA — Session 2026-06-29

## Décisions prises

1. **Migration Home Assistant + Zigbee Dongle**
   - Utilisation de HA avec dongle Zigbee (M5 arrêté)
   - Statut : validé, en attente de sauvegarde complète du travail sur les plantes

2. **Attente stratégique (2 décisions)**
   - Caméra Wildnexus : en suspend (point à refaire)
   - Composants matériels supplémentaires : en suspend (attendre clarification)

3. **Modèle spécialisé pour problèmes récurrents**
   - Mise en place d'un modèle dédié pour les débogages (pattern détecté : même type d'erreur revient)

4. **Vérification des effets en cascade**
   - Validation obligatoire avant déploiement (demande explicite)

**⚠️ Critique** : Aucune traçabilité temporelle. Les décisions manquent de dates de revue et d'owner assigné.

---

## Échecs ouverts / bloqueurs

### Bloqueurs techniques critiques
1. **Caméra Wildnexus**
   - Reference : `camera 1005005710463218`
   - Problème : incompatibilité OV5640 DVP 24-pin / ESP32-S3
   - Pivot testé : Arducam IMX500 (trouvé, non validé)
   - Status : **À trancher** (OV5640 vs IMX500)

2. **Arduino CLI installation**
   - Erreur : upstream connect error / no upload port provided
   - Documentation : référence officielle existante mais non appliquée
   - Status : **Bloquer** jusqu'à installation complète

3. **ESP32 Memory overflow**
   - Erreur : "Maximum is 327680 bytes"
   - Cause : code trop volumineux pour la RAM disponible
   - Status : **À optimiser** (compression ou refactoring nécessaire)

4. **Connection ESP32 Device Unresponsive**
   - Erreur : Connection Failed, possible autre programme en conflit
   - Diagnostic partiel seulement
   - Status : **À investiguer** (processus fantômes ?)

### Bloqueurs secondaires
5. **Outlook crash** → à remise en place (non détaillé comment)
6. **Dotfiles/environnement fragile** → Path (.env) + (.venv) confusion récurrente

---

## Questions récurrentes (signe de lacune documentaire)

### Manque d'explications fondamentales
| Question | Apparitions | Racine probable |
|----------|------------|-----------------|
| "c'est quoi (.venv) ?" | 3+ | Pas de doc Python/venv dans PKA |
| "c'est quoi (.env) ?" | 2+ | Dotenv non expliqué (utilisé implicitement) |
| "comment faire accéder Dobby à Notes Apple ?" | 2+ | **Vrai problème système** : pas d'intégration écosystème Apple |
| "ca c'est quoi harness ?" | 2+ | Jargon technique non défini (test harness ? hardware harness ?) |
| "memory nudge c'est quoi ?" | 1 | Terme propre à PKA, jamais documenté formellement |
| "terminal vscode vs terminal system ?" | 2+ | Confusion shell/PATH non clarifiée |
| "pourquoi maintenant j'ai des refs Mouser et pas avant ?" | 2+ | **Manque de traçabilité des décisions** d'outils |

### Feedback pattern
JCH pose **deux fois la même question** = absence de documentation persistante + pas de lien vers réponse précédente dans mémoire.

---

## Nouveaux patterns détectés

### 1. **Cycle de débogage inefficace**
```
Erreur technique → Recherche ad-hoc → Lien externe → Test manuel → Oubli de documenter
```
**Exemple** : Arduino CLI error → lien docs.arduino.cc → "ca marche pas" → pas d'ajout à knowledge base

### 2. **Paralysie décisionnelle sur matériel**
- OV5640 vs IMX500 : deux semaines en suspend ?
- Cause : surcharge cognitive (12 projets actifs, 4 en full steam)
- Symptôme : "on va attendre" revient 3x

### 3. **Toolchain fragmentation**
- DeepSeek-TUI + Claude Code + Codex CLI = 3 surfaces d'API
- Chacun avec contexte partiel
- Manque : orchestration MCP centralisée (mentionnée mais pas implémentée)

### 4. **Perte de contexte entre sessions**
- Dobby doit redemander des infos de session précédente (oublis)
- 2 sessions = 1017 échanges = **mémoire non persistante efficace**

### 5. **Approche par recherche plutôt que par mémoire**
- JCH envoie souvent des extraits Google/docs
- Dobby ne relie pas à la base PKA existante
- Cause : pas de search_memory systématique

---

## Efficacités / Inefficacités

### ✅ Ce qui marche bien
1. **Needle in Haystack recall** (100% selon Kimi)
   - Dobby retrouve les infos passées
   - Contexte massif bien géré

2. **Tool Calling fiable**
   - DeepSeek / Claude alternance sans friction
   - Imports/exports entre outils réussis

3. **Décisions rapides quand contexte clair**
   - Migration HA + Zigbee : décidé et avancé en même session

### ❌ Inefficacités majeures

| Inefficacité | Impact | Cause racinaire |
|-------------|--------|-----------------|
| **Redocumentation de basics** | 3-4 échanges perdus par session | Pas de onboarding persistent |
| **Attente passive** | Bloqueurs non actifs | Pas de timeout / follow-up systématique |
| **Recherche Mouser/composants** | 2-3 aller-retours | Pas de BOM parser intégré à Dobby |
| **Gestion Notes Apple** | Inaccessible pour Dobby | Limitation système non contournée |
| **Overhead de 18 Go** | Lenteurs potentielles | Binaires historiques non purgés |

### Coût d'opportunité identifié
- **1017 messages** = ~5-6 heures d'interaction
- **Estimé : 20% perdu** en clarifications / redites = **60 min gaspillées**

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 État des projets (snapshot 2026-06-29)
- **Wildnexus** : caméra bloquée (OV5640 vs IMX500), décision en suspend
- **HA + Zigbee** : GO, en cours de finalisation
- **Work sur plantes** : à sauvegarder + valider cascades
- **M5** : arrêté (migration HA complète)
- **Outlook** : crashé, remise en place partielle

### 📋 Décisions validées à ne pas rediscuter
1. HA avec dongle Zigbee = architecture cible
2. Modèle spécialisé pour débogages = à créer
3. Vérification cascades obligatoire = politique de déploiement

### ⚠️ Bloqueurs actifs à suivre
1. **Arduino CLI** → finish installation avant prochain test ESP32
2. **Caméra Wildnexus** → arbitrer OV5640 vs IMX500 (deadline ?)
3. **Memory bloat (18 Go)** → audit + nettoyage Git recommended

### 📚 Documentation à produire immédiatement
- [ ] `.venv` vs `.env` expliqué + lié au gitignore
- [ ] "Harness" défini (test harness ? hardware harness ?)
- [ ] "Memory nudge" expliqué (PKA-specific glossaire)
- [ ] Commandes terminal MacBook vs VSCode terminal (PATH clarification)
- [ ] Notes Apple integration strategy (limitation vs workaround)

### 🧠 Points de vigilance cognitif
- **Paralysie décisionnelle** sur Wildnexus : JCH tend à "attendre" quand incertitude matériel
- **Context switching coûteux** : 12 projets actifs → créer des "focus windows"
- **Recherche plutôt que mémoire** : instruire Dobby à proposer liens vers session antérieures

---

## Recommandations

### Phase 1 : Immédiat (< 24h)
1. **Trancher Wildnexus**
   - Décision OV5640 vs IMX500 : table à décision (cout/délai/perf)
   - Actioner la commande (AliExpress link exists)
   - Timeline : GPS si critical path

2. **Documenter les basics**
   - Template 1-page : `.venv`, `.env`, harness, memory nudge
   - Lien dans PKA index + Dobby reminder on mention

3. **Audit Arduino CLI**
   - Reproduire l'erreur en session partagée
   - Créer script setup automatisé (Docker ou shell)
   - Sauvegarder résolution dans runbooks

### Phase 2 : Court terme (1-2 semaines)
4. **Implémenter search_memory systématique**
   - Dobby : avant chaque réponse, si ambiguité → `search_memory` auto
   - Ajouter traçabilité : "référence à session XYZ du DATE"

5. **Créer "Decision Log" persistent**
   - Capture : QUI/QUOI/QUAND/POURQUOI sur chaque bifurcation
   - Format : [decision.log] dans PKA root
   - Dobby propose ré-évaluation tous les 2 semaines sur "attentes"

6. **Refactor toolchain**
   - MCP centralisé (DeepSeek-TUI as hub) = démontrer faisabilité
   - Évite context loss entre Claude / DeepSeek

### Phase 3 : Moyen terme (1 mois)
7. **Système de timeboxing décision**
   - Wildnexus : "decision deadline = 2026-07-06"
   - Si pas de clarification, escalade → JCH call
   - Évite la dérive "on va attendre"

8. **Intégration Notes Apple**
   - Option A : exporteur periodic vers markdown (sync)
   - Option B : accepter limitation, créer "capture protocol" alternatif
   - Dobby ne peut pas y accéder = limiter promesses

9. **Git cleanup**
   - Audit 18 Go : identifier binaires historiques
   - Archive old packs, shallow clone setup
   - Gain : accélération requête mémoire

10. **Glossaire PKA vivant**
    - Wiki interne : tous les jargons ("harness", "nudge", "cascades effect")
    - Dobby : link automatique si terme spécialisé détecté

### Insight psychologique (mode froid)
**JCH tend à procrastiner sur décisions matériel = charge décisionnelle trop haute.**
- Paliatif : créer **decision templates** (arbre OV5640 vs IMX500 pre-filled)
-

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 30
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 30
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

- [Decision] Utilisation de HA avec dongle Zigbee (M5 arrêté)
- [Decision] Statut : validé, en attente de sauvegarde complète du travail sur les plantes
- [Decision] Caméra Wildnexus : en suspend (point à refaire)
- [Decision] Composants matériels supplémentaires : en suspend (attendre clarification)
- [Decision] Mise en place d'un modèle dédié pour les débogages (pattern détecté : même type d'erreur revient)
- [Decision] Validation obligatoire avant déploiement (demande explicite)
- [Decision] : Aucune traçabilité temporelle. Les décisions manquent de dates de revue et d'owner assigné.
- [Decision] Migration Home Assistant + Zigbee Dongle
- [Decision] Attente stratégique (2 décisions)
- [Decision] Modèle spécialisé pour problèmes récurrents
- [Decision] Vérification des effets en cascade
- [Failure] Reference : `camera 1005005710463218`
- [Failure] Problème : incompatibilité OV5640 DVP 24-pin / ESP32-S3
- [Failure] Pivot testé : Arducam IMX500 (trouvé, non validé)
- [Failure] Status : **À trancher** (OV5640 vs IMX500)
- [Failure] Erreur : upstream connect error / no upload port provided
- [Failure] Documentation : référence officielle existante mais non appliquée
- [Failure] Status : **Bloquer** jusqu'à installation complète
- [Failure] Erreur : "Maximum is 327680 bytes
- [Failure] Cause : code trop volumineux pour la RAM disponible
- [Failure] Status : **À optimiser** (compression ou refactoring nécessaire)
- [Failure] Erreur : Connection Failed, possible autre programme en conflit
- [Failure] Diagnostic partiel seulement
- [Failure] Status : **À investiguer** (processus fantômes ?)
- [Failure] Arduino CLI installation
- [Failure] ESP32 Memory overflow
- [Failure] Connection ESP32 Device Unresponsive

### Fréquence des patterns (14 jours)
- **Failure** : 7 jours, 106 occurrences
- **Decision** : 6 jours, 35 occurrences
- **Question** : 4 jours, 21 occurrences
- **Recurring question** : 4 jours, 19 occurrences
- **Blocker** : 1 jours, 1 occurrences
- **Conflict detected** : 1 jours, 3 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (5x) error handlers are registered, logging exception.Traceback (most recent call las
- [Failure] (5x) on a crashe dans le dernier boulot : check graphy complet utilisant ol
- [Failure] (4x) B mais c'est toujours bloqué cote console
- [Failure] (4x) j'ai trouvé ceci Arducam IMX500 AI Camera Module for ESP32-P4 and other MCU/SOC 
- [Failure] (4x) tu es en pro, tu pourra mieux voir les failles actuelles du dossier et faire des
- [Failure] (3x) .  Errors may be dropped.[16:24:26.399] Failed to parse remote port from server 
- [Failure] (3x) 39407782&ds_e_product_merchant_id=5716905007&ds_e_product_country=BE&ds_e_produc
- [Failure] (3x) awned 24778[16:24:26.141] Using connect timeout of 17 seconds[16:24:26.199] > lo
- [Failure] (3x) comment ne pas etre bloqué par les demandes d'approbation ou je dis tjrs approve
- [Failure] (3x) dnexus en lui demandant d'y trouver des failles
- [Failure] (3x) logique erreur The terminal process failed to launch: Starting directory (cwd) "
- [Failure] (3x) ssh, pid=24786[16:24:26.336] stderr> debug1: Server host key: ssh-ed25519 SHA256

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **error handlers are registered, logging exception.Traceback (most recent call las**
- [ ] Documenter : **on a crashe dans le dernier boulot : check graphy complet utilisant ol**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 27
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**183** recommandations au total — **183** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 151
- **Forge** : 27
- **Corbeau** : 3
- **Furet** : 2

### Plus récentes ouvertes

- [id=173] (2026-06-29) **Dobby** : Trancher Wildnexus
- [id=174] (2026-06-29) **Dobby** : Décision OV5640 vs IMX500 : table à décision (cout/délai/perf)
- [id=175] (2026-06-29) **Dobby** : Actioner la commande (AliExpress link exists)
- [id=176] (2026-06-29) **Dobby** : Timeline : GPS si critical path
- [id=177] (2026-06-29) **Dobby** : Documenter les basics

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $8.98 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $8.98**
