---
date: 2026-06-11
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1064
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-11

**Sessions analysées :** 2 | **Échanges :** 1064 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE DES SESSIONS 2026-06-11 🦉

## Décisions prises

1. **Retour au choix Raspberry Pi (RPI)** comme infrastructure de base pour les projets IoT
   - Vérification des coûts réels demandée mais non documentée
   - Décision prise sans consensus apparent sur les paramètres de validation

2. **Consolidation des trois projets majeurs** : wildnexus, IoT, travels
   - Utilisation de NotebookLM pour la génération de rapports
   - Elimination de fichiers sources en double (md, notebook) dans directory structure

3. **Passage du browser externe à VS Code via NotebookLM**
   - Contournement de la nécessité d'accès externe sans documentation claire du workflow

4. **Matching capteurs IoT VAN** avec besoins spécifiques (en attente de validation)
   - Décision prise mais validation responsable non définie

**🚩 CRITIQUE** : Aucune de ces décisions n'a de trace d'implémentation, de propriétaire assigné, ou de deadline.

---

## Échecs ouverts / bloqueurs

### Critiques

1. **OAuth / macOS Keychain failure**
   ```
   OAuth error: Failed to save API key to macOS Keychain 
   (security: SecKeychainItem... Bootstrap failed: 5: Input/output error)
   ```
   - **Impact** : Impossible de persister les credentials, bloque l'automatisation
   - **Depuis** : Au moins 2026-06-09
   - **Propriétaire** : Indéfini

2. **Crash dans graphy complet (oleum?)**
   - Mentioned but **aucun détail fourni, pas de logs**
   - État critique indéterminé
   - Bloque potentiellement WildNexus

3. **HTTP/2 404 sur endpoint distant**
   ```
   HTTP/2 404 < date: Tue, 09 Jun 2026 18:05:07 GMT
   ```
   - Cause inconnue, source inconnue
   - Endpoint mort ou configuration réseau cassée?

4. **Remote port parsing failure**
   ```
   Failed to parse remote port from server output
   ```
   - Bloque déploiement sur RPI
   - Debug logging activé mais logs jamais partagés

### Secondaires

5. **Telegram Bot 409 Conflict** (decouvertes-collector)
   - Erreur HTTP 409 lors de `/getUpdates`
   - Bot peut être dupliqué ou rate-limité
   - Crash de updater non gracieux

6. **Locale settings warnings (Perl)**
   ```
   perl: warning: Setting locale failed
   ```
   - Symptôme bénin mais signe de mauvaise config système

---

## Questions récurrentes (signe de lacunes documentaires)

### Top 3 - Processus / Délégation (critiques)

```
"pourquoi tu ne le fais pas"
"pourquoi tu ne le fais pas"
"pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu proposes ?"
```

**Analyse** : JCH questionne pourquoi les assistants ne prennent pas d'initiative. **Ceci indique un manque de clarté sur les boundaries entre suggestion et exécution.**

```
"comment faire pour que cette instruction ne soit jamais oubliée quelquesoit le modele ?"
```

**Analyse** : Persistance des instructions système entre changements de modèles IA = **problème critique non résolu dans la prompt engineering PKA**.

### Top 2 - Syntaxe / Accès fichiers (confusion courante)

```
"c'est quoi ces quote et pourquoi l'acces fichiers impossible"
"c'est quoi ces quote et pourquoi l'acces fichiers impossible"
```

**Analyse** : Répétition exacte = **les quotes cassent l'accès fichiers. Jamais expliqué. Symptôme d'un shell wrapper défaillant.**

### Top 1 - Architecture / Outils

```
"esphome et home assistant quelle est la différence"
"pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs"
"ok parfait. derniere questions comment faire en sorte que l'html s'ouvre chez quelqu'un d'autres hors reseau jch ?"
```

**Analyse** : Questions répétées = **documentation manquante sur l'architecture IoT (esphome vs HA), la structure de projet, la distribution/sharing.**

---

## Nouveaux patterns détectés

### 1. **Oscillation décision / doute**
- Décision RPI prise → immédiatement vérification coûts → pas d'aboutissement
- Pattern : Décision rapide sans étude préalable, suivi d'une second-guessing

### 2. **Fragmentation des projets en parallèle**
- wildnexus, vetalyx, travels, iot, decouvertes-collector
- **5+ projets actifs** avec dependencies implicites
- Aucune matrice de priorité visible

### 3. **Multi-tool chaos**
- DeepSeek, Claude, Ollama, OpenRouter, Nvidia, NotebookLM
- Chaque outil = nouvelle configuration, nouvelle authentification
- OAuth failure = symptôme d'accumulation

### 4. **Machines multiples (M1, M5, RPI) sans SOP claire**
- `m1@FE:CC:48:61:DF:7F` vs `m1@MBP-de-M1` = même user, machines différentes?
- ifconfig + curl + apt-get = mix incompréhensible (macOS + Debian?)
- **Indique une infra multi-OS mal documentée**

### 5. **Questions de "comment ?" vs "pourquoi ?"**
- JCH demande rarement le *pourquoi* d'une solution
- Focus obsessionnel sur le *comment faire marcher* sans remise en question architectural
- Signe d'une accumulation de dette technique

---

## Efficacités / Inefficacités

### ✅ Efficacités

1. **Déploiement rapide sur RPI** (apt-get, jq install, ollama pulls)
   - Scripting shell maîtrisé
   - 9GB pulls exécutés sans supervision → autonomie relative

2. **Multi-model experimentation** (gemma3, mxbai-embed)
   - Flexibilité de basculer entre DeepSeek et Claude
   - Adaptabilité aux tâches différentes

3. **Telegram integration** (malgré le 409 Conflict)
   - Tentative d'automation décentralisée = bonne intention

### ❌ Inefficacités

1. **Perte d'informations massive**
   - Décisions sans trace → 2-3 semaines après, repose la même question
   - Aucune décision registry, pas de ADR (Architecture Decision Records)

2. **Debugging en aveugle**
   - Crashes mentionnés ("on a crashe dans le dernier boulot") sans reproduction steps
   - OAuth failure jamais root-caused
   - Logs capturés mais jamais analysés collectivement

3. **Cycle copie-colle / manuel exécution**
   - "Copier-coller commandes dans terminal" = perte de tracabilité, risque de erreurs
   - Pas de vrai CI/CD, pas d'idempotence

4. **Assistants trop suggestifs, pas assez directifs**
   - "pourquoi tu ne le fais pas ?" = JCH frustr é que les IA ne prennent pas le contrôle
   - Pattern : IA propose → JCH rejette → IA se rétracte → cycle infini

5. **Questions sur architecture posées in real-time**
   - "esphome vs homeassistant ?" devrait être dans un **Architecture.md** depuis longtemps
   - Chercher une réponse à chaque session = gaspillage de jetons

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Bloqueurs critiques (fix immédiat)

1. **macOS Keychain OAuth failure** 
   - Affecter un assistant pour root cause analysis
   - Contourner : utiliser `osascript` ou environment variables
   - Deadline : avant prochaine session

2. **graphy crash**
   - Demander logs complets (stderr, stdout, stack trace)
   - Reproduire isolément avant de continuer WildNexus

3. **Remote port parsing** (RPI deployment)
   - Vérifier exactement quelle commande génère cette sortie
   - Tester connectivity SSH/serial vers RPI

### 🟡 Processus à formaliser (avant prochaine sprint)

1. **Decision Log** → créer un fichier `DECISIONS.md` dans PKA root
   - Format : Date | Décision | Responsable | Status | Logs référencés
   - Exemple immédiat : RPI choice + cost validation

2. **Instruction persistence across models**
   - Créer un **System Prompt Vault** (JSON ou YAML)
   - Charger automatiquement pour tout nouveau modèle
   - Exemple : "Dobby envoie toujours les commandes, pas JCH"

3. **Project matrix**
   - Tabler les 5 projets actifs avec : priorité, propriétaire, deadline, blocker status
   - Éviter le context-switching constant

4. **Boundaries documentation**
   - Clarifier : quand un assistant *exécute* vs *suggère*
   - Répondre formellement à "pourquoi tu ne le fais pas ?" dans un SOP

5. **Architecture documentation quick-win**
   - Créer `ARCHITECTURE.md` avec schéma IoT (esphome vs HA, flows, capteurs)
   - Créer `INFRASTRUCTURE.md` (M1, M5, RPI, réseaux, credentials)

### 🟢 À préserver

1. **Résilience des deployments shell** (apt-get, ollama pulls fonctionnent)
2. **Multi-tool flexibility** (bien maintenir les credentials pour Claude, DeepSeek, Ollama)
3. **Volonté d'automation** (Telegram, cron, NotebookLM reports) ← bon signal

---

## Recommandations

### Phase 1 : Stabilisation (48h max)

1. **Créer emergency task board** avec les 3 bloqueurs critiques
   - Kanban simple : TODO | IN PROGRESS | BLOCKED | DONE
   - PairProgram Dobby (Claude Code) sur OAuth + graphy crash
   - Temps-box : 2h max par bloqueur

2. **Exécuter une session "decision archaeology"**
   - Rejouer la conversation RPI : coûts réels? validation criteria?
   - Documenter la décision finale dans `DECISIONS.md`
   - Assigner propriétaire pour follow-up coûts

3. **Fixer les boundaries IA**
   - Ajouter au prompt système Dobby : "Tu prépares + tu exécutes quand tu peux (Claude Code). Tu suggests quand tu ne peux pas."
   - Ajouter au prompt système autres IA : charger `INSTRUCTIONS.txt` en startup

### Phase 2 : Organisation (1 semaine)

4. **Consolidation projet**
   - Merger/prioritize les 5 projets (wildnexus is priority #1? OUI/NON)
   - Créer un `README.md` root avec structure claire
   - Naming convention : chaque projet a un dossier avec `src/`, `docs/`, `config/`

5. **Infrastructure as Code** 
   -

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 421
- Résolus automatiquement : 155
- Résolus manuellement : 0
- Encore ouverts : 266
- **Taux : 36.8%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 532.0
- Échanges/session début fenêtre : 74.4
- Tendance globale : 615.1%
- Tendance 3j-3j : 305.2%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] Retour au Raspberry Pi officiel** : JCH décide d'acheter le RPI officiel et son ventilateur actif, après avoir vérifié les coûts réels. La solution al
- [Decision] Passage dans Notebook** : Un élément non spécifié est basculé dans un notebook. JCH demande ce qui doit être documenté.
- [Decision] Mise à jour du mapping capteurs IoT** : Décision de matcher les besoins de capteurs IoT van avec les besoins des projets WildNexus, IoT et Travels.
- [Decision] Utilisation de Notebook LM pour les rapports** : JCH confie la création des rapports pour les trois projets à Notebook LM.
- [Decision] Validation du profil de poste IoT** : La description de fonction exhaustive est confrontée aux job descriptions de "Araignée" et "Chouette" (rôles PKA
- [Decision] comme infrastructure de base pour les projets IoT
- [Decision] Vérification des coûts réels demandée mais non documentée
- [Decision] Décision prise sans consensus apparent sur les paramètres de validation
- [Decision] : wildnexus, IoT, travels
- [Decision] Utilisation de NotebookLM pour la génération de rapports
- [Decision] Elimination de fichiers sources en double (md, notebook) dans directory structure
- [Decision] Contournement de la nécessité d'accès externe sans documentation claire du workflow
- [Decision] avec besoins spécifiques (en attente de validation)
- [Decision] Décision prise mais validation responsable non définie
- [Decision] : Aucune de ces décisions n'a de trace d'implémentation, de propriétaire assigné, ou de deadline.
- [Decision] Retour au choix Raspberry Pi (RPI)** comme infrastructure de base pour les projets IoT
- [Decision] Consolidation des trois projets majeurs** : wildnexus, IoT, travels
- [Decision] Passage du browser externe à VS Code via NotebookLM
- [Decision] Matching capteurs IoT VAN** avec besoins spécifiques (en attente de validation)
- [Failure] Échec de connexion SSH au serveur distant** : `Failed to issue method call: Access denied` et `Bootstrap failed: 5: Input/output error` sur `local-ser
- [Failure] Problème de locale sur le serveur** : `perl: warning: Setting locale failed` – erreur persistante non résolue.
- [Failure] Erreur 404 sur une requête HTTP** : `HTTP/2 404` – une ressource est introuvable, cause non identifiée.
- [Failure] Conflit Telegram Bot** : `HTTP/1.1 409 Conflict` sur `getUpdates` – le bot a un conflit de webhook/polling, non résolu.
- [Failure] Installation iPad bloquée** : JCH soupçonne que Tailscale VPN bloque l'installation sur iPad. Aucune solution trouvée.
- [Failure] Problème de quotes dans le terminal** : `quote> cquote>` – JCH est bloqué dans un état interactif inattendu, ne comprend pas pourquoi l'accès fichier 
- [Failure] Impact** : Impossible de persister les credentials, bloque l'automatisation
- [Failure] Depuis** : Au moins 2026-06-09
- [Failure] Propriétaire** : Indéfini
- [Failure] Mentioned but **aucun détail fourni, pas de logs
- [Failure] État critique indéterminé
- [Failure] Bloque potentiellement WildNexus
- [Failure] Cause inconnue, source inconnue
- [Failure] Endpoint mort ou configuration réseau cassée?
- [Failure] Bloque déploiement sur RPI
- [Failure] Debug logging activé mais logs jamais partagés
- [Failure] OAuth / macOS Keychain failure
- [Failure] Crash dans graphy complet (oleum?)
- [Failure] HTTP/2 404 sur endpoint distant
- [Failure] Remote port parsing failure

### Fréquence des patterns (14 jours)
- **Decision** : 5 jours, 273 occurrences
- **Failure** : 5 jours, 281 occurrences
- **Question** : 5 jours, 251 occurrences
- **Recurring question** : 5 jours, 140 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (5x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Failure] (5x) chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error
- [Failure] (5x) d strict checking.Host key verification failed.jchavauxm5@mac ~ %
- [Failure] (5x) générer du TypeScript/Vanilla CSS ou debugger tes scripts Python.   * Pour l'Ana
- [Failure] (5x) perl: warning: Setting locale failed.perl: warning: Please check that your local
- [Question] (5x) ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode
- [Question] (5x) e ce soit toi qui envoie les commandes. comment faire pour que cette instruction
- [Question] (5x) ok parfait. derniere questions comment faire en sorte que l'html s'ouvre chez qu
- [Question] (5x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?
- [Question] (5x) pourquoi modele clude ne premiere attention ?
- [Question] (5x) pourquoi tu ne le fais pas
- [Question] (5x) quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible
- [Question] (5x) ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces
- [Question] (5x) verifie d'abord pourquoi il n'a pas été regeneré
- [Decision] (4x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI**
- [ ] Documenter : **chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error**
- [ ] Documenter : **d strict checking.Host key verification failed.jchavauxm5@mac ~ %**
- [ ] Documenter : **générer du TypeScript/Vanilla CSS ou debugger tes scripts Python.   * Pour l'Ana**
- [ ] Documenter : **perl: warning: Setting locale failed.perl: warning: Please check that your local**
- [ ] Documenter : **ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode**
- [ ] Documenter : **e ce soit toi qui envoie les commandes. comment faire pour que cette instruction**
- [ ] Documenter : **ok parfait. derniere questions comment faire en sorte que l'html s'ouvre chez qu**
- [ ] Documenter : **ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?**
- [ ] Documenter : **pourquoi modele clude ne premiere attention ?**
- [ ] Documenter : **pourquoi tu ne le fais pas**
- [ ] Documenter : **quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible**
- [ ] Documenter : **ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces**
- [ ] Documenter : **verifie d'abord pourquoi il n'a pas été regeneré**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 39
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**74** recommandations au total — **74** ouvertes — **0** en cours — **0** terminées

### Répartition par assigné

- **Dobby** : 59
- **Forge** : 11
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=57] (2026-06-11) **Dobby** : Créer une règle "Exécution automatique"** : Tout assistant doit exécuter les com
- [id=58] (2026-06-11) **Dobby** : Diagnostiquer et résoudre le problème SSH** : `Access denied` sur `local-server-
- [id=59] (2026-06-11) **Dobby** : Résoudre le conflit Telegram** : Désactiver le webhook ou le polling pour reveni
- [id=60] (2026-06-11) **Dobby** : Ajouter un guide "Sortir des états interactifs"** : Expliquer comment quitter `q
- [id=61] (2026-06-11) **Dobby** : Mettre en place un processus de validation rapide** : Avant d'explorer une solut

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.0 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.0**
