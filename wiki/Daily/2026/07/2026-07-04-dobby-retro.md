---
date: 2026-07-04
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1126
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-04

**Sessions analysées :** 3 | **Échanges :** 1126 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA — Sessions du 2026-07-04

## Décisions prises

| Décision | Statut | Notes |
|----------|--------|-------|
| **Migration OpenRouter pour Kimi** | ✅ Validée 100% | Passage exclusif OpenRouter validé. Reste à vérifier l'accès `/Users/jchavauxm5/` |
| **Choix du modèle dans VS Code** | ⏳ À documenter | Pas d'exemple concret fourni. JCH demande comment faire. |
| **Report délai capteurs IR/vidéo Belgique** | ✅ Appliquée | Nouveau délai : 30 juin (mais on est le 3 juillet → **incohérence temporelle**) |
| **Passage Zigbee + dongle HA** | ⏳ Partiellement appliquée | M5 arrêté, transition en cours. État du hardware flou. |
| **Utilisation manuelle pour tâche automatisée** | ❌ Fallback | "Ça marche pas, je vais le faire manuellement" → débat sur l'automatisation jamais fermé |
| **Vérification des effets en cascade** | 🔴 Non exécutée | JCH demande vérification, mais aucune trace de cette analyse dans les extraits |

**Problème critique** : Les décisions sont validées oralement mais **jamais tracées dans MEMORY.md** ou le système PKA. Aucune raison technique documentée.

---

## Échecs ouverts / bloqueurs

### 🔴 Bloqueurs hardware/réseau
1. **Connection timeout sur API** → Laissé en suspens (Yahoo)
2. **NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT** → Collision possible avec mqTT. **Jamais diagnostic approfondi**
3. **Device Unresponsive (Zigbee/HA)** → Cause inconnue. Autre programme interférant? **Non investigué**
4. **Upstream connect error before headers** → Crash réseau. Statut : "Ça marche pas"

### 🟡 Bloqueurs logiciels
1. **Git : 1,92 Go de pack binaire** → Health-check RED à cause de faux positifs. **À optimiser**
2. **Pointeurs multi-modèles dérives (12)** → PKA monitoring montre drift. **Aucune action corrective**
3. **Crash durant opération** → JCH demande "Tu as pu terminer avant le crash?" → **Pas de mécanisme de reprise**

### 🟡 Bloqueurs organisationnels
- **Photo Canon EOS R10 RF 200-800mm** → Validée pour projet WildNexus mais **statut du fork bioacoustique flou**
- **Accès Apple Notes** → Demandé 3x, jamais résolu. **Bridge manquant**
- **Variables d'environnement .venv/.env** → JCH pose la question 3x. **Documentation insuffisante ou mal intégrée**

---

## Questions récurrentes (signe de lacune documentaire)

### Même question posée 3+ fois
1. **".venv vs .env — c'est quoi la différence?"**
   - Asked: avant d'avoir .venv, maintenant pourquoi les deux?
   - **Cause racine** : Pas de guide "Environnement Python 101" accessible depuis le PKA
   
2. **"Comment accéder à Apple Notes?"**
   - Asked: 3x explicitement
   - **Cause racine** : Pas d'intégration bridge ; pas de fallback documenté (export JSON, sync iCloud, etc.)

3. **"Comment choisir un modèle dans VS Code avec OpenRouter?"**
   - Asked: Explicitement + implicitement lors de migration OpenRouter
   - **Cause racine** : Pas de screenshot/exemple ; doc OpenRouter ≠ VS Code integration

4. **"C'est quoi X (harness, memory nudge, X1201-C1)?"**
   - Termes techniques non définis localement
   - **Cause racine** : Pas de glossaire métier dans MEMORY.md ou AGENTS.md

### Déduction
**Ces questions reviennent car aucune réponse n'est tracée dans le système PKA.** À chaque session, JCH repose la même question, Dobby répond, rien n'est sauvegardé. **Loop infini**.

---

## Nouveaux patterns détectés

### 1. **Mode "Vérification asymétrique"**
   - JCH demande : "Verifie si X"
   - Réponse : "Validé 100%" ou silence
   - **Pattern** : Pas de trace écrite de la vérification. On ne sait pas ce qui a été checké, comment, ni pourquoi.

### 2. **Mélange projet/contexte sans transition**
   - Session démarre : PKA analysis (Kimi)
   - Bascule : Hydrocortisone (Virbac/pharma — projet Vetalyx?)
   - Puis : OV5640 ESP32 (hardware — WildLens?)
   - Puis : Composants Mouser (shopping list — même projet?)
   - **Pattern** : Aucun marqueur de contexte. Dobby doit deviner le projet actif.

### 3. **Utilisation des outils décorrélée des décisions**
   - JCH utilise DeepSeek pour analyse PKA
   - Puis bascule OpenRouter pour Kimi
   - Jamais expliqué : pourquoi ce split? Critères de choix?
   - **Pattern** : Outil choisi par commodité, pas par stratégie.

### 4. **Fallback manuel systématique**
   - "Ça marche pas. Je vais le faire manuellement."
   - **Compte** : 1x confirmé. Probable : plus.
   - **Pattern** : Aucune escalade, aucun débogage structuré avant fallback.

### 5. **Timestamps incohérents**
   - Report au 30 juin, mais session du 3 juillet
   - Fichiers datés 2026-07-04 vs 2026-07-03
   - **Pattern** : Pas de synchronisation calendrier PKA ↔ Dobby

---

## Efficacités / inefficacités

### ✅ **Points forts**
1. **Kimi 2.5 via OpenRouter** : Validation instantanée. JCH accepte d'emblée = gain de confiance.
2. **Utilisation de search_memory** : Lors de références passées, Dobby cherche (exemple : harness → contextualisation).
3. **Photo validation** : Canon EOS metadata extrait correctement, lié au projet WildNexus.

### ❌ **Points faibles (majeurs)**
1. **Zéro traçabilité des vérifications**
   - "Verifie attentivement" → Aucune trace
   - "Validé 100%" → Sur quoi exactement?
   - **Impact** : JCH ne peut pas auditer. Dobby peut halluciner une vérification.

2. **Pas de fallback intelligent pour erreurs matériel**
   - Timeout réseau → "Laissez Yahoo"
   - Device unresponsive → "Ça marche pas, manuel"
   - **Impact** : Perte d'itération, accumulation technique dept.

3. **Contexte projet jamais annoncé**
   - JCH saute entre 5-6 projets sans marqueur
   - Dobby doit déduire (failure rate inconnu)
   - **Impact** : Risque d'hallucination contexte, mélange d'analyses

4. **Questions récurrentes jamais clôturées**
   - Réponses données, jamais enregistrées
   - JCH devra re-demander prochaine session
   - **Impact** : Gaspillage token, frustration utilisateur

5. **Git repose sur binaires (1,92 Go)**
   - Health-check cassé par faux positifs
   - Aucune tentative de cleanup
   - **Impact** : Slow clone, monitoring infiable

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 **État critique du PKA**
- **Taille** : 18 Go (4 projets actifs, 8 en attente)
- **Équipe DB** : 32 membres ✅ (dont Dobby)
- **Health** : RED → faux positifs Git + drift multi-modèles (12)
- **Processus** : 4 actifs (dashboard, telegram-bot, gateway, docker)

### 📋 **Projets actifs + contexte**
| Projet | Statut | Notes | Outils |
|--------|--------|-------|--------|
| **WildNexus** | 🔥 Plein régime | Photo Canon + fork bioacoustique | Claude, DeepSeek |
| **WildLens** | 🔥 Plein régime | OV5640 ESP32-S3 (pinout critique) | DeepSeek |
| **Vetalyx** | ⏳ En cours | Hydrocortisone/Virbac, CDMO search | Claude |
| **Arteon** | ⏳ En cours | ? (flou) | ? |
| **PKA System** | ⏳ Monitoring | Analyse Kimi 2.5 en cours | Kimi via OpenRouter |

### 🔧 **Questions non résolues à escalader**
1. **Apple Notes access** : Chercher intégration ou export JSON
2. **.venv/.env confusion** : Créer glossaire Python + save dans MEMORY.md
3. **OpenRouter + VS Code UI** : Fournir screenshot/walkthrough
4. **Zigbee device unresponsive** : Diagnostic avant fallback manual
5. **Multi-modèle drift (12)** : Audit + correction des pointeurs

### ⚙️ **Décisions en attente de trace**
- [ ] OpenRouter OpenAPI migration pour Kimi (spécifier auth, endpoint)
- [ ] Zigbee dongle config (modèle, firmware, pair status)
- [ ] Photo Canon metadata usage (où stockée? qui y accède?)
- [ ] Effects cascade verification (quel cadre d'analyse?)

### 🚨 **Patterns à surveiller**
- Nouvelles bascules sans contexte → Demander `#PROJECT: nom`
- Fallback manual → Escalader, pas accepter
- "Validé" sans trace → Exiger détails
- Timestamps incohérents → Synchroniser avec Dobby's clock

---

## Recommandations

### **Immédiat (avant prochaine session)**

1. **Créer `GLOSSARY.md`** (5 min)
   ```markdown
   # Glossaire PKA — JCH + Dobby
   
   ## Python/Env
   - **.venv** : Virtual env local. Contient packages isolés. Créé via `python -m venv .venv`
   - **.env** : Secrets (API keys, paths). Chargé via `python-dotenv`. ≠ .venv
   - **(.venv) avant path** : Shell prompt indicant env activé. Normal.
   
   ## Hardware
   - **OV5640 24-pin** : Capteur image. Incompatible brochage OV2640. Voir section Pinout.
   - **X1201-C1** : [rechercher dans Mouser DB]
   

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 41
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 38
- **Taux : 7.3%**

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

- [Decision] | ✅ Validée 100% | Passage exclusif OpenRouter validé. Reste à vérifier l'accès `/Users/jchavauxm5/` |
- [Decision] | ⏳ À documenter | Pas d'exemple concret fourni. JCH demande comment faire. |
- [Decision] | ✅ Appliquée | Nouveau délai : 30 juin (mais on est le 3 juillet → **incohérence temporelle**) |
- [Decision] | ⏳ Partiellement appliquée | M5 arrêté, transition en cours. État du hardware flou. |
- [Decision] | ❌ Fallback | "Ça marche pas, je vais le faire manuellement" → débat sur l'automatisation jamais fermé |
- [Decision] | 🔴 Non exécutée | JCH demande vérification, mais aucune trace de cette analyse dans les extraits |
- [Decision] : Les décisions sont validées oralement mais **jamais tracées dans MEMORY.md** ou le système PKA. Aucune raison technique documentée.
- [Failure] → Laissé en suspens (Yahoo)
- [Failure] → Collision possible avec mqTT. **Jamais diagnostic approfondi
- [Failure] → Cause inconnue. Autre programme interférant? **Non investigué
- [Failure] → Crash réseau. Statut : "Ça marche pas
- [Failure] Connection timeout sur API** → Laissé en suspens (Yahoo)
- [Failure] Device Unresponsive (Zigbee/HA)** → Cause inconnue. Autre programme interférant? **Non investigué
- [Failure] Upstream connect error before headers** → Crash réseau. Statut : "Ça marche pas

### Fréquence des patterns (14 jours)
- **Decision** : 6 jours, 38 occurrences
- **Failure** : 6 jours, 36 occurrences
- **Question** : 6 jours, 18 occurrences
- **Recurring question** : 4 jours, 17 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 14
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**214** recommandations au total — **214** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 179
- **Forge** : 28
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=209] (2026-07-04) **Dobby** : 1. **Créer `GLOSSARY.md`** (5 min)
- [id=210] (2026-07-04) **Dobby** : .venv** : Virtual env local. Contient packages isolés. Créé via `python -m venv 
- [id=211] (2026-07-04) **Dobby** : .env** : Secrets (API keys, paths). Chargé via `python-dotenv`. ≠ .venv
- [id=212] (2026-07-04) **Dobby** : (.venv) avant path** : Shell prompt indicant env activé. Normal.
- [id=213] (2026-07-04) **Dobby** : OV5640 24-pin** : Capteur image. Incompatible brochage OV2640. Voir section Pino

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $14.94 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $14.94**
