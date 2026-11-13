---
date: 2026-06-15
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1185
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-15

**Sessions analysées :** 3 | **Échanges :** 1185 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Session 2026-06-15 - Dobby PKA

## Décisions prises

- **Retour au choix RPI** : Validation en cours des coûts réels après exploration d'alternatives (M1, iPad).
- **Utilisation de Notebook LM** : Pour générer les rapports des trois projets prioritaires (WildNexus, IoT, Travels).
- **Migration de clé API** : Passage de la clé Anthropic à un setup alternatif suite à changement de message Telegram.
- **Validation des paramètres de performance** : Seuil fixé à 3% minimum de gain (en dessous = non implémenté).
- **Stockage des rappels** : Mise en place d'un système pour conserver les tâches à re-explorer (en particulier sur M5).
- **Sélection MQTT non finalisée** : Question ouverte « je choisis quel mqtt ? » → décision reportée.

**Problème** : Décisions fragmentées, certaines non documentées dans des tickets formels.

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent les projets)

1. **iPad + VPN Tailscale : installation impossible**
   - VPN connecté, mais console bloque toujours
   - Suspect : restriction côté système ou configuration incomplète
   - **Impact** : WildLens n'est pas portable sur iPad
   - **Statut** : Non résolu

2. **Container Docker HTTP/2 404**
   - Erreur : `HTTP/2 404` sur endpoint localhost
   - **Impact** : Déploiement stagné
   - Conseil donné : « Debug avec Gordon » (container error fix)

3. **Crash graphique non documenté**
   - Mention : « on a crashe dans le dernier boulot : check graphy complet »
   - Contexte flou, pas de trace complète
   - **Risque** : Récurrence silencieuse

4. **Device Unresponsive (M5 / ESP32-P4)**
   - Erreur : `Connection Failed: Device Unresponsive`
   - Cause possible : autre programme utilise le port
   - **Impact** : Tests IoT bloqués

5. **Telegram API Conflict (409)**
   - Erreur : `HTTP/1.1 409 Conflict` sur `getUpdates`
   - Trace incomplète dans logs
   - **Impact** : découvertes-collector en panne

### Moyen (entravent la productivité)

- **Arduino CLI installation** : référence donnée (lien docs.arduino.cc) mais pas intégré au workflow
- **SSH key negotiation** : trace `ssh-ed25519 SHA256:...` → configuration instable potentielle
- **Accès aux Apple Notes** : JCH demande comment donner l'accès à ses assistants → pas de solution proposée

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Signification |
|----------|-----------|---------------|
| « Pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu proposes ? » | 2x | Assistants pas assez directifs ; manque de validation avant d'explorer |
| « Comment maintenir l'outil si je migre de M5 ? » | 2x | Pas de stratégie de pérennité documentée pour les outils dépendants |
| « Pourquoi c'est exclusif Claude ? » | 1x (récurrente?) | Confusion sur les capacités Claude vs DeepSeek vs OpenRouter |
| « Pourquoi tu proposes USB-A quand j'ai USB-C ? » | 1x | Manque de contexte machine (M1 MacBook specs) en mémoire |
| « (.venv) c'est quoi ? » | 1x | Pas de onboarding virtualenv expliqué |
| « Comment faire pour que tu accèdes à Apple Notes ? » | 1x | Pas de solution systématique pour l'intégration des sources perso |
| « Pourquoi tu as les réfs Mouser maintenant et avant non ? » | 1x | Assistants inconsistants sur les sources de référence ; manque de mémorisation |
| « C'est quoi la peur pour toi ? » | 1x | Question philosophique → signe de fatigue ou frustration envers les assistants |
| « Comment installer HACS pour que HA soit le carrefour des produits Sonoff ? » | 1x | Manque de guide intégration Home Assistant + HACS |

**Diagnostic** : Besoin urgent de **documentation interne** (onboarding, troubleshooting, architecture globale).

---

## Nouveaux patterns détectés

1. **Ping-pong multi-outils sans convergence**
   - JCH bascule DeepSeek → Claude → OpenRouter sans décision claire
   - Chaque outil propose une solution différente → frustration
   - **Cause** : Pas de "playbook" par type de tâche

2. **Contexte machine fragmenté**
   - M5, M1 MacBook, iPad, RPI mentionnés sans fil rouge
   - Décisions prises isolément par machine (ex: clé API sur M1)
   - **Symptôme** : Coûts, maintenance, pérennité non consolidés

3. **Projets entrelacés sans séparation claire**
   - WildNexus, WildLens, IoT, Travels, Vetalyx = 5 contextes distincts
   - Questions mélangées (« t maitenant avant j'avais pas (.venv) » = problème général IoT)
   - **Besoin** : Matrix RACI projet ↔ outil ↔ machine

4. **Validation de performance implicite**
   - Seuil 3% fixé oralement, pas dans les reminders
   - Risque oubli ou incohérence future

5. **Gestion des secrets chaotique**
   - Clés API changées ad-hoc (Anthropic → autre)
   - Pas de vault centralisé mentionné
   - Logs montrent tokens en clair (Telegram bot ID)

---

## Efficacités / inefficacités

### ❌ Inefficacités majeures

| Inefficacité | Coût estimé | Remède |
|---|---|---|
| Assistants proposent solutions sans validation contexte machine | 30+ min/session | Créer checksheet : « As-tu vérifié les specs de : M1/M5/RPI/iPad ? » |
| Questions récurrentes = manque de wiki interne | 15 min/session | Créer `FAQ_PKA.md` + index des tâches par projet |
| Changements de clé API improvisés | Risque sécurité | Vault centralisé (1Password/Bitwarden) + reminders synchronisés |
| Crashes graphiques non tracés | Inconnu (peut-être 1h+/semaine) | Logging structuré + alertes Telegram |
| Pas d'accès Apple Notes → recherche manuelle | 5-10 min/jour | API Apple Notes ou export structuré (Zapier?) |

### ✅ Efficacités à conserver

- **Notebook LM pour synthèse rapide** : Décision bonne, à documenter
- **Référence Mouser depuis DeepSeek** : Quand utilisé, c'est fluide
- **Tailscale VPN** : Infrastructure réseau fiable (malgré bugs d'install)
- **Modèle DeepSeek-v4-pro** : Apparemment stable pour coding

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Architectures décidées
- **RPI est le choix de base** (coûts validés) → ne pas relancer le débat M1 sans raison
- **Notebook LM = outil de synthèse** pour WildNexus, IoT, Travels
- **Seuil performance 3%** : Applique-le systématiquement

### Blockers à résoudre en priorité
1. **iPad + Tailscale** : Réassigner à [Pie?] avec deadline
2. **Docker 404** : Lancer `docker ai "help me fix..."` avec Gordon
3. **Telegram 409 Conflict** : Logs incomplets → réenclencher avec traceback complet
4. **Device Unresponsive M5** : Script de test automatique pour isoler le port bloquant

### Contexte machines à mémoriser
- **M1 MacBook** : USB-C seulement, Ollama sur /Users/jchavauxm5, (~/.venv) standard
- **M5** : Arducam IMX500 AI Camera Module en expérimentation
- **RPI** : Coûts validés, performances à confirmer
- **iPad** : Pour maintenant = non-viable (VPN issue)

### Dettes de documentation urgentes
- `FAQ_VIRTUALENV.md` : Qu'est-ce que .venv et pourquoi
- `MOUSER_WORKFLOW.md` : Comment importer liste BOM
- `HACS_HA_INTEGRATION.md` : Installer HACS + Sonoff dans Home Assistant
- `APPLE_NOTES_SYNC.md` : Solution pour accès à Notes
- `PROJECT_MATRIX.md` : Quelle tâche → quel projet → quelle machine → quel outil

### Secrets et infra
- **Clés API** : Centraliser dans vault, ne pas changer sans notifier Dobby
- **SSH keys** : Vérifier stabilité de la clé ed25519
- **Telegram bot** : Fixer le 409 Conflict ASAP (bloque collector)

---

## Recommandations

### 🎯 Court terme (3-5 jours)

1. **Créer `MEMORY.md` structuré** 
   - Format : Projets | Machines | Outils | Décisions | Blockers
   - Dobby l'ingère au début de chaque session
   - Évite les questions « pourquoi USB-A » x3

2. **Tier les 5 bloqueurs**
   ```
   CRITIQUE : Telegram 409 (+ Docker 404)
   HAUTE   : iPad + Tailscale
   MOYENNE : M5 Device Unresponsive
   BASSE   : Apple Notes sync
   ```

3. **Documenter seuil 3%** dans reminders Dobby
   - Trigger : chaque fois qu'une optimisation est proposée

4. **Créer checksheet** pour assistants
   ```markdown
   Avant de proposer une solution IoT, vérifier :
   - [ ] Sur quel appareil? (M1/M5/RPI/iPad)
   - [ ] Quel projet? (WildNexus/Travels/etc)
   - [ ] Coûts réels validés?
   - [ ] Pérennité si migration M5?
   ```

### 📋 Moyen terme (1-2 semaines)

5. **Wiki PKA minimal** (5 fichiers)
   - `VIRTUALENV_101.md`
   - `MOUSER_BOM_IMPORT.md`
   - `HACS_SONOFF_SETUP.md`
   - `MACHINE_SPECS.md` (specs M1/M5/RPI/iPad)
   - `VAULT_STRATEGY.md` (gestion secrets)

6. **Système de reminders** pour M5 migration
   - Question : « Es-tu sûr que cet outil survit à un départ de M5 ? »
   - Automatisé dans Dobby

7. **Analyser crash graphique**
   - Récupérer logs complets
   -

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 420
- Résolus automatiquement : 132
- Résolus manuellement : 0
- Encore ouverts : 288
- **Taux : 31.4%**

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

- [Decision] Retour au choix RPI** : validation des coûts réels pour le projet IoT (probablement WildLens/Nexus).
- [Decision] Attente sur le volet A, exécution du B et processing du C** : décision de priorisation claire non documentée ailleurs.
- [Decision] Validation des paramètres "du moment"** : abandon d'une optimisation fine jugée non rentable (gain de 3% jugé insuffisant).
- [Decision] Utilisation de Notebook LM pour les rapports WildNexus, IoT et Travels** : outil imposé sans alternative documentée.
- [Decision] Focus sur le working set** : recentrage après dispersion (suite à des erreurs de terminal).
- [Decision] Choix d'un client MQTT** : question restée ouverte (pas de décision finale visible).
- [Decision] Retour au choix RPI** : Validation en cours des coûts réels après exploration d'alternatives (M1, iPad).
- [Decision] Utilisation de Notebook LM** : Pour générer les rapports des trois projets prioritaires (WildNexus, IoT, Travels).
- [Decision] Migration de clé API** : Passage de la clé Anthropic à un setup alternatif suite à changement de message Telegram.
- [Decision] Validation des paramètres de performance** : Seuil fixé à 3% minimum de gain (en dessous = non implémenté).
- [Decision] Stockage des rappels** : Mise en place d'un système pour conserver les tâches à re-explorer (en particulier sur M5).
- [Decision] Sélection MQTT non finalisée** : Question ouverte « je choisis quel mqtt ? » → décision reportée.
- [Decision] : Décisions fragmentées, certaines non documentées dans des tickets formels.
- [Failure] Crash de terminal récurrent** (`The terminal process failed to launch` sur `/Users/jchavauxm5/PK...`) : cause non résolue, le vault n'a pas pu être vé
- [Failure] Erreur 404 sur HTTP** (`HTTP/2 404` lors d'envoi de données) : service indisponible, aucune action corrective tracée.
- [Failure] Connexion SSH échouée** (`Connection Failed: Device Unresponsive`) : le M5 n'a pas répondu, probable problème de réseau ou de configuration.
- [Failure] Erreur conteneur Docker** (`docker ai "help me fix t...`) : debug demandé mais pas de résolution dans le transcript.
- [Failure] Log Telegram bloqué** (`HTTP/1.1 409 Conflict`, `No error handlers are registered`) : bot Telegram en conflit, pas de correction apportée.
- [Failure] Arducam IMX500** : trouvée mais pas de décision d'intégration.
- [Failure] VPN connecté, mais console bloque toujours
- [Failure] Suspect : restriction côté système ou configuration incomplète
- [Failure] Impact** : WildLens n'est pas portable sur iPad
- [Failure] Statut** : Non résolu
- [Failure] Erreur : `HTTP/2 404` sur endpoint localhost
- [Failure] Impact** : Déploiement stagné
- [Failure] Conseil donné : « Debug avec Gordon » (container error fix)
- [Failure] Mention : « on a crashe dans le dernier boulot : check graphy complet »
- [Failure] Contexte flou, pas de trace complète
- [Failure] Risque** : Récurrence silencieuse
- [Failure] Erreur : `Connection Failed: Device Unresponsive`
- [Failure] Cause possible : autre programme utilise le port
- [Failure] Impact** : Tests IoT bloqués
- [Failure] Erreur : `HTTP/1.1 409 Conflict` sur `getUpdates`
- [Failure] Trace incomplète dans logs
- [Failure] Impact** : découvertes-collector en panne
- [Failure] iPad + VPN Tailscale : installation impossible
- [Failure] Container Docker HTTP/2 404
- [Failure] Crash graphique non documenté
- [Failure] Device Unresponsive (M5 / ESP32-P4)
- [Failure] Telegram API Conflict (409)

### Fréquence des patterns (14 jours)
- **Decision** : 9 jours, 433 occurrences
- **Failure** : 9 jours, 441 occurrences
- **Question** : 9 jours, 379 occurrences
- **Recurring question** : 9 jours, 220 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (8x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Decision] (8x) foramnce par exemple de 3% cela ne vaut pas la peine
- [Failure] (8x) /LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running
- [Failure] (8x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Failure] (8x) What's next:    Debug this container error with Gordon → docker ai "help me fix 
- [Failure] (8x) failed to connect
- [Question] (8x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?
- [Question] (8x) pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu propo
- [Question] (8x) verifie d'abord pourquoi il n'a pas été regeneré
- [Decision] (7x) a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta
- [Decision] (7x) dernier point, on va matcher les besoins de capteurs iot van avec les besoins de
- [Decision] (7x) ent il y a un nouveau message telegrma. je vais changer la cle
- [Decision] (7x) je vais acheter l'officiel et aussi le ventilateur actif. pour celu
- [Decision] (7x) le A on va ttendre, le B on fait et le C processer
- [Decision] (7x) lement la clé anthropic fonctionne mais on va sur le M1

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution**
- [ ] Documenter : **foramnce par exemple de 3% cela ne vaut pas la peine**
- [ ] Documenter : **/LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running**
- [ ] Documenter : **OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI**
- [ ] Documenter : **What's next:    Debug this container error with Gordon → docker ai "help me fix **
- [ ] Documenter : **failed to connect**
- [ ] Documenter : **ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?**
- [ ] Documenter : **pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu propo**
- [ ] Documenter : **verifie d'abord pourquoi il n'a pas été regeneré**
- [ ] Documenter : **a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta**
- [ ] Documenter : **dernier point, on va matcher les besoins de capteurs iot van avec les besoins de**
- [ ] Documenter : **ent il y a un nouveau message telegrma. je vais changer la cle**
- [ ] Documenter : **je vais acheter l'officiel et aussi le ventilateur actif. pour celu**
- [ ] Documenter : **le A on va ttendre, le B on fait et le C processer**
- [ ] Documenter : **lement la clé anthropic fonctionne mais on va sur le M1**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 40
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**120** recommandations au total — **120** ouvertes — **0** en cours — **0** terminées

⚠️ 22 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 98
- **Forge** : 18
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=103] (2026-06-15) **Dobby** : Créer une fiche "Décisions"** dans le vault project (PKA_JCH) avec la date, la d
- [id=104] (2026-06-15) **Forge** : Automatiser la vérification du terminal** avant chaque session : tester le réper
- [id=105] (2026-06-15) **Dobby** : Définir un processus de choix d'outil** : si un assistant propose une solution, 
- [id=106] (2026-06-15) **Forge** : Standardiser les exports de composants** : utiliser un template BOM vérifié (col
- [id=107] (2026-06-15) **Dobby** : Documenter l'architecture MCP** : comment DeepSeek-TUI, Claude et les outils Doc

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.99 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.99**
