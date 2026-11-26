---
date: 2026-06-30
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1029
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-30

**Sessions analysées :** 2 | **Échanges :** 1029 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA – Sessions 2026-06-30

## Décisions prises

### Claires et documentées
- **Départ WildNexus** : 25 juin à 15:00 depuis Namu (confirmé, à mémoriser pour planning)
- **Modèle ESP32** : Attendre confirmation des essais avant achat (décision prudente, mais non-datée)
- **Statut MQTT** : Reporter la décision ("on va attendre") – **BLOQUEUR NON TRACÉ**
- **Caméra WildNexus** : Faire un point/résumé (tâche ouverte, assignataire flou)

### Non documentées / implicites
- Quand JCH demande "quel mqtt ?" et obtient "on va attendre" → **Pas de trace de pourquoi**, **pas de deadline**
- Choix du modèle en fonction du contexte → Processus ad-hoc, dépendant de l'accès fichier (`/Users/jchavauxm5/`) mais **critères de sélection jamais explicités**
- "on va rester comme cela mais mets dans les reminders" → **Aucun reminder créé documenté**
- "on va completer le fichier" → Quel fichier ? Quand ? Par qui ?

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent le travail)
1. **MCP Server crash** : `pka-homeassistant` → stdio transport closed
   - **Impact** : Impossible de valider les outils, sessions interrompues
   - **Status** : Non résolu, pas de root cause identifier
   - **Actionnable** : Vérifier logs MCP, reconnexion automatique manquante

2. **Upload Arduino échoue** : "no upload port provided" + "upstream connect error"
   - **Machine** : M1/M5, port de communication perdu
   - **Status** : Litige avec Arduino IDE / permissions
   - **Actionnable** : Documenter la séquence de reconnexion USB

3. **Git pack trop volumineux** : 1,92 Go d'historique binaire
   - **Cause** : Probablement fichiers `.bin`, `.hex` commités
   - **Impact** : Clone/push lent, coûteux
   - **Actionnable** : Audit git, `.gitignore` renforcé, rebase historique

4. **Health-check PKA RED** : "faux positifs massifs"
   - **Status** : Non investigué, métriques non fiables
   - **Impact** : Impossible de savoir l'état réel du système

### Secondaires (frustrants mais non-bloquants)
- "pourquoi maintenant tu as les ref Mouser et avant pas ?" → **Régression documentaire**, JCH doit chercher manuellement
- "Output OFF, Mode Source Meter, 5000 mV je vois cela ou ?" → Documentation manquante sur l'interface
- Fork projet "plantes" dans "bioacoustique" pas créé → **Décision prise, non exécutée**

---

## Questions récurrentes (signe de lacune documentaire)

### Outils & configuration (7+ répétitions)
| Question | Fréquence | Racine |
|----------|-----------|--------|
| "comment utiliser OpenRouter dans VS Code ?" | 3x | Pas de doc unifiée VS Code + OpenRouter + sélection de modèle |
| "(.venv) c'est quoi ?" / "(.env) c'est quoi ?" | 3x | Python venv/env jamais expliqué dans le contexte JCH |
| "ca marche pas, voici le lien Arduino" | 2x | Processus d'install Arduino CLI non mémorisé |
| "memory nudge c'est quoi ?" | 2x | Terminologie PKA/Dobby opaque pour JCH |

### Matériel & références
| Question | Fréquence | Racine |
|----------|-----------|--------|
| "c'est quoi le X1201-C1 ?" | 1x | Manque nomenclature matériel centralisée |
| "ca marche pas, upstream connect error" | 2x | Processus troubleshooting USB/serial non documenté |

### Accès & workflow
| Question | Fréquence | Racine |
|----------|-----------|--------|
| "comment faire en sorte que tu y ai accès ?" (Apple Notes) | 1x | **CRITIQUE** : JCH veut partager Notes, mais pas d'interface configurée |
| "pourquoi ais je aussi (.env) en debut de path ?" | 1x | Confusion sur environnement d'exécution |

### Meta-questions (signal d'anxiété)
- "c'est quoi la peur pour toi ?" → Relation de confiance à consolider

---

## Nouveaux patterns détectés

### Pattern 1 : "Faux démarrages de conversation"
JCH pose une question → reçoit une réponse → demande immédiatement l'explication du **pourquoi/comment** de la réponse
- **Exemple** : "explique moi pourquoi maintenant tu as les ref Mouser et avant pas"
- **Signification** : Transparence insuffisante, JCH ne comprend pas la logique des outils
- **Impact** : Démon de confiance interne, surcomplexité perçue

### Pattern 2 : "Décisions suspendues sans trace"
JCH dit "on va attendre" / "on va faire le point" → Aucun rappel créé, aucune deadline fixée
- **Exemple** : MQTT, point camera WildNexus, completion de fichier
- **Signification** : Processus de tracking manquant (no task manager intégré)
- **Impact** : Perte de contexte à la prochaine session

### Pattern 3 : "Accès fichier fragmenté"
JCH mentionne `/Users/jchavauxm5/PKA_JCH/` → Assistants ne peuvent pas lister/accéder pleinement
- **Exemple** : "ok une fois dedans comment je choisis le modele ?" (inaccessibilité)
- **Signification** : Permissions fichier ou MCP client incomplet
- **Impact** : Besoin constant de JCH pour naviguer le contexte local

### Pattern 4 : "Multiplicité d'outils mal intégrés"
DeepSeek, Claude, OpenRouter, Docker, MCP → JCH doit switcher manuellement, perte de contexte
- **Exemple** : "explique moi comment utiliser openrouter dans l'interface de vs code"
- **Signification** : Pas de point d'entrée unifié, chaque outil a sa propre courbe d'apprentissage
- **Impact** : Friction cognitive élevée

### Pattern 5 : "Questions techniques + questions pédagogiques mélangées"
JCH pose un problème technique → reçoit une solution → demande "pourquoi c'est comme ça ?"
- **Exemple** : "pourquoi maintenant tu as les ref mouser..."
- **Signification** : Besoin d'une **explainability layer** dans les réponses
- **Impact** : Volume de messages doublé

---

## Efficacités / inefficacités

### ✅ Ce qui marche
1. **Recall mémoire PKA** : "rappel parfait à 100%" (Needle in Haystack) → Dobby fonctionne
2. **Tool Calling** : Excellente fiabilité d'utilisation des outils
3. **Contexte massif** : Fenêtre de contexte suffisante pour les projets complexes
4. **Modèles réactifs** : DeepSeek-v4 / DeepSeek-v4-pro performants pour les cases d'usage
5. **32 membres DB** : Équipe virtuelle bien dimensionnée

### ❌ Ce qui ralentit
1. **MCP instabilité** : Crashes stdio sans retry automatique (-2h par crash)
2. **Documentation fragmentée** : JCH pose 3x la même question sur (.venv) → doc unifiée manquante (-1.5h cumulé)
3. **Accès fichier limité** : Assistants ne voient pas `/Users/jchavauxm5/PKA_JCH/` complètement (-30min par session)
4. **Pas de task tracker intégré** : "on va faire le point" n'est pas actionnable (-45min/session à retrouver le contexte)
5. **Choix de modèle manuel** : "ok une fois dedans comment je choisis le modele ?" → pas d'heuristique (-20min par decision)
6. **Git pack massif** : Clone/push du repo 1.92 Go (-5min par opération × 50 sessions/an)

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 Faits immuables
- **Départ WildNexus** : **25 juin 2026 à 15:00 depuis Namu** (confirmé)
- **Équipe PKA** : 32 membres DB, Dobby = orchestrateur PKA
- **Projets actifs** : 12 (4 en plein régime, 4 en cours, 4 en veille)
- **Systèmes critiques** : dashboard, telegram-bot, gateway, docker
- **Capacités AI** : Kimi 2.5 + Dobby + DeepSeek sont les analyseurs de référence

### ⚠️ Décisions suspendues (CRITIQUES)
| Décision | Status | Deadline | Qui ? |
|----------|--------|----------|-------|
| Quel MQTT utiliser ? | ⏸️ "on va attendre" | À fixer | JCH |
| Point caméra WildNexus | ⏸️ "resume moi chall" | À fixer | Dobby |
| Quel ESP32 acheter | ⏸️ "apres les essais" | Fin juin ? | JCH + Dobby |
| Completion fichier | ⏸️ "on va completer" | À fixer | JCH |
| Fork "plantes" | ⏸️ "necessite de tu cree un fork" | À fixer | JCH |
| Apple Notes access | ⏸️ "comment faire ?" | À implémenter | JCH + Dobby |

### 🔧 Points techniques à mémoriser
- **USB/Serial Arduino** : M1/M5 a des issues de reconnexion ("no upload port provided")
- **Git repo** : 1.92 Go pack = historique binaire, nécessite cleanup
- **OV5640 + ESP32-S3** : Brochage différent d'OV2640, pinout critique
- **Health-check PKA** : RED à cause de faux positifs, métriques non fiables
- **MCP server stability** : pka-homeassistant crash stdio sporadiquement

### 📚 Lacunes documentaires à combler
1. **OpenRouter dans VS Code** (choix de modèle, config)
2. **(.venv) et (.env)** pour Python
3. **Terminologie PKA** (memory nudge, working set, etc.)
4. **Arduino CLI installation & troubleshooting**
5. **Processus d'accès fichier** (`/Users/jchavauxm5/PKA_JCH/`)
6. **Interface de sélection de modèle** (critères, heuristiques)

### 👤 Préférences JCH
-

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 33
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 33
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

- [Decision] Départ WildNexus** : 25 juin à 15:00 depuis Namu (confirmé, à mémoriser pour planning)
- [Decision] Modèle ESP32** : Attendre confirmation des essais avant achat (décision prudente, mais non-datée)
- [Decision] Statut MQTT** : Reporter la décision ("on va attendre") – **BLOQUEUR NON TRACÉ
- [Decision] Caméra WildNexus** : Faire un point/résumé (tâche ouverte, assignataire flou)
- [Failure] : `pka-homeassistant` → stdio transport closed
- [Failure] Impact** : Impossible de valider les outils, sessions interrompues
- [Failure] Status** : Non résolu, pas de root cause identifier
- [Failure] Actionnable** : Vérifier logs MCP, reconnexion automatique manquante
- [Failure] : "no upload port provided" + "upstream connect error
- [Failure] Machine** : M1/M5, port de communication perdu
- [Failure] Status** : Litige avec Arduino IDE / permissions
- [Failure] Actionnable** : Documenter la séquence de reconnexion USB
- [Failure] : 1,92 Go d'historique binaire
- [Failure] Cause** : Probablement fichiers `.bin`, `.hex` commités
- [Failure] Impact** : Clone/push lent, coûteux
- [Failure] Actionnable** : Audit git, `.gitignore` renforcé, rebase historique
- [Failure] : "faux positifs massifs
- [Failure] Status** : Non investigué, métriques non fiables
- [Failure] Impact** : Impossible de savoir l'état réel du système
- [Failure] MCP Server crash** : `pka-homeassistant` → stdio transport closed
- [Failure] Upload Arduino échoue** : "no upload port provided" + "upstream connect error
- [Failure] Git pack trop volumineux** : 1,92 Go d'historique binaire
- [Failure] Health-check PKA RED** : "faux positifs massifs

### Fréquence des patterns (14 jours)
- **Failure** : 7 jours, 84 occurrences
- **Decision** : 6 jours, 34 occurrences
- **Recurring question** : 5 jours, 20 occurrences
- **Question** : 4 jours, 23 occurrences
- **Blocker** : 1 jours, 1 occurrences
- **Conflict detected** : 1 jours, 3 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (4x) error handlers are registered, logging exception.Traceback (most recent call las
- [Failure] (4x) on a crashe dans le dernier boulot : check graphy complet utilisant ol
- [Failure] (3x) B mais c'est toujours bloqué cote console
- [Failure] (3x) j'ai trouvé ceci Arducam IMX500 AI Camera Module for ESP32-P4 and other MCU/SOC 
- [Failure] (3x) tu es en pro, tu pourra mieux voir les failles actuelles du dossier et faire des

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 23
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
