---
date: 2026-06-20
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 10
echanges: 1291
modeles: claude, claude-sonnet-4-6, deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-20

**Sessions analysées :** 10 | **Échanges :** 1291 | **Modèles :** claude, claude-sonnet-4-6, deepseek-v4, deepseek-v4-pro

---

# 🦉 Rétrospective PKA — Session du 2026-06-20

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **Passage exclusif à OpenRouter pour Kimi** | Évaluation de la couche multi-modèles ; simplification des endpoints | ✅ Validée |
| **Attendre avant action cascade** | Vérification des effets en aval avant déploiement | ⏳ En cours |
| **Achat de la MCP fournie par EPS pour M0** | Rejet de la commande Mouser (quota 10 dépassé) ; alternative identifiée | ✅ Validée |
| **Intégration OV5640 sur ESP32-S3** | Constraints techniques documentées ; brochage non standard identifié | 📝 Documenter |
| **Kimi 2.5 comme analyseur du système PKA** | Diagnostic multi-niveaux du repo (18 Go, 12 projets) | ✅ Déployée |

**Observations** : Les décisions sont souvent implicites (« validé oui ») sans justification écrite. Aucune trace d'un registro de décisions formel.

---

## Échecs ouverts / bloqueurs

### 🔴 Critiques

1. **MCP Server Stdio Transport Closed** (`pka-homeassistant`)
   - Status : Bloqueur actif
   - Impact : Intégration HA-Sonoff non fonctionnelle
   - Symptôme : `MCP validation failed: pka-homeassistant: Stdio transport closed`
   - Action attendue : Diagnostic sur le serveur MCP HomeAssistant

2. **Telegram Bot — HTTP 409 Conflict**
   - Traceback : Updater loop failure sur `getUpdates`
   - Path : `/scripts/decouvertes-collector/venv/lib/python3.13/site-packages/telegram/ext/_updater.py:753`
   - Cause probable : Authentification token ou rate-limiting
   - Équipe notifiée : ❌ Non tracé

3. **Device Unresponsive (Camera 1005005710463218)**
   - Erreur : `Connection Failed: Device Unresponsive`
   - Possible cause : Programme concurrent bloquant le port
   - Action : À mener

### ⚠️ Secondaires

- **Health-check RED** → Faux positifs massifs sur git pack (1,92 Go d'historique binaire)
- **Fichiers en attente** → JCH_Inbox et TEAM_Inbox bloquées (validation + rejets non triés)
- **VSCode terminal env vars** → Confusion `.env` en début de path (question posée 3x)
- **Mouser quota MOQ 10** → Validation manuelle requise pour chaque achat (friction)

---

## Questions récurrentes (signe de lacune documentaire)

### Tier 1 : Hyper-fréquentes (4+ occurrences)
- **« Comment choisir le modèle une fois dedans ? »**  
  → Absence de doc sur le switching model en session live (OpenRouter vs local DeepSeek)
  
- **« Pourquoi (.env) en début de path ? »**  
  → Source-env pattern non expliqué dans MEMORY.md ou USER.md

- **« Memory nudge, c'est quoi ? »**  
  → Terme du système PKA non défini ; confusion client-side vs working set

- **« Pourquoi c'est exclusif Claude ? »**  
  → Architecture multi-agent non clarifiée (Claude Desktop vs DeepSeek-TUI vs openrouter)

- **« Terminal vscode : même commande qu'en shell natif ? »**  
  → Confusion sur les contexts d'exécution

### Tier 2 : Modérées
- Comment maintenir des outils sur M5 sans perdre compatibilité M1 ?
- USB-A vs USB-C sur Mac (confusions matérielles)
- Pourquoi Mouser references maintenant visibles (avant recherche manuelle)
- Comment installer HACS pour HA comme hub central Sonoff/IoT ?

**→ Root cause** : CLAUDE.md et SOUL.md **existent mais ne couvrent pas ces cas d'usage courants**.

---

## Nouveaux patterns détectés

### 1. **Multi-Tool Context Switching Sans Sync**
- JCH passe DeepSeek → Claude → OpenRouter → DeepSeek-TUI dans une même session
- **Problème** : Aucun protocole de « handoff » documenté
- **Symptôme** : Répétition de questions (« comment choisir le modèle »)
- **Conséquence** : Chaque outil crée son propre working set

### 2. **Décisions Implicites**
- Validation par « oui », « validé oui » sans trace de raison
- Pas de lien vers justification technique
- **Impact** : Impossible de re-décider à J+N si contexte change

### 3. **Documentation Réactive vs Proactive**
- Kimi 2.5 analyse du PKA → **Appel à contribution** « y a-t-il des choses à ajouter ? »
- Jamais de doc préventive ; toujours une crise avant d'écrire
- **Pattern** : Incident → Chat → « Explique-moi » → Doc partielle

### 4. **Hardware Drift**
- M1, M5, RPi mentionnés (287x Dobby, 96x M1, 63x M5)
- Aucun matriciel « ce code tourne sur : »
- **Risk** : M5 migration = perte d'outils sans trace

### 5. **Inbox Accumulation**
- JCH_Inbox + TEAM_Inbox bloquées en cours
- Fichiers « en attente validation » non triés par priorité
- **Anti-pattern** : Demander « range fichiers en ordre d'intérêt » = tâche du système, pas de l'humain

---

## Efficacités / inefficacités

### ✅ Ce qui marche

| Efficacité | Preuve |
|-----------|--------|
| **Dobby comme observateur** | 287 mentions ; patterns extraits localement sans latence |
| **Multi-modèle available** | DeepSeek (51x), Claude (117x), OpenRouter (55x) en production |
| **Macro-escalade rapide** | Kimi 2.5 peut analyser 18 Go en une requête |
| **Git + MCP integration** | DeepSeek-TUI client/server natif fonctionne |
| **Terminal + IDE co-existence** | VSCode + ollama côte à côte opérationnel |

### ❌ Ce qui ralentit

| Inefficacité | Coût | Remède |
|-------------|------|--------|
| **Switching tool = repeat question** | 3-5 min par context switch | Unified prompt template |
| **No decision registry** | 2-3 min de réexplication par décision ancienne | DECISIONS.md + timestamp |
| **Inbox manual sorting** | 15-20 min par « range fichiers » | Automated priority script |
| **Device unresponsive (camera)** | Bloqueur complet ; cause inconnue | Diagnostic playbook |
| **Health-check false positives** | 1-2h de debugging par mois | Git pack cleanup + thresholds |
| **.env mystery x3** | Confusion source-env vs PATH | 1 diagram dans USER.md |
| **MOQ friction on Mouser** | Manual validation loop added 2026-06-20 | BOM automation + cart template |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 Priorité Critique (24h)

1. **MCP HomeAssistant stdio closed** → Debug et patch avant HACS integration
2. **Telegram bot 409 Conflict** → Check token validity + rate limit
3. **Camera device unresponsive (1005...)** → Port scan + process check
4. **Inbox triage** → Implement automated priority sorter (no more manual `range fichiers`)

### 📝 Priorité Haute (1 semaine)

- **CLAUDE.md + SOUL.md augmentation** :
  - Model selection guide (OpenRouter vs local)
  - Memory nudge definition + working set semantics
  - Terminal VSCode vs shell differences
  - Multi-tool handoff protocol
  
- **DECISIONS.md creation** :
  - Registry format : `[Date] [Tool] [Decision] [Rationale] [Owner] [Status]`
  - Enforce written validation for `validé oui` → `validé: raison de la decision`
  
- **Hardware matrix** :
  - Which code runs on M1 / M5 / RPi
  - Deprecation plan for M5 migration
  
- **Git pack cleanup** :
  - Remove binary history > 100 MB
  - Set `.gitattributes` for LFS

### 🔄 Priorité Moyenne (2 semaines)

- OV5640 on ESP32-S3 integration doc (constraints + wiring)
- HACS installation guide (HA as IoT hub)
- Mouser BOM automation + cart template
- `.env` sourcing diagram

### 🧠 Truths to Keep

- **Kimi 2.5 is now the system analyzer** → Use it for monthly health-check
- **OpenRouter is the gateway** → All multi-model routing goes through it
- **Dobby is the observer** → Trust its pattern extraction
- **Decisions are implicit until written** → Write them down immediately

---

## Recommandations

### Immédiat (next session)

```markdown
## Pre-Session Checklist
- [ ] Read MEMORY.md + 3 newest decision entries
- [ ] Verify MCP pka-homeassistant status
- [ ] Check Telegram bot logs (last 100 lines)
- [ ] Inbox triage status (auto-sorted or manual?)
- [ ] Which tool(s) in this session? (Declare upfront)
```

### Processus

1. **Unified Session Header** (before first tool):
   ```
   ## Session 2026-06-20_v2
   **Tools**: DeepSeek-TUI + Claude (as reviewer)
   **Working Set**: scripts/telegram-bot, bin/dobby.sh
   **Blockers**: MCP stdio, Camera 1005005710463218
   **Decisions Required**: OV5640 wiring approval
   ```

2. **Decision Template** (every choice):
   ```
   ### ✅ Decision: [Name]
   - **Chosen**: Option A
   - **Why**: [2-3 lines of rationale]
   - **Validation**: [By whom, when]
   - **Reversible?**: Yes/No
   - **Owner**: [Person]
   - **Due**: YYYY-MM-DD
   ```

3. **Blocker Escalation** (when stuck > 5 min):
   ```
   ### 🔴 BLOCKER: [Name]
   - **Error**: [Exact message]
   - **Tried**: [List attempts]
   - **Next**: [Specific action]
   - **Owner**: [Assign]
   - **Deadline**: [24h max]
   ```

### Docs to Create This Week

| Doc | Owner | Deadline |
|-----|-------|----------|
| DECISIONS.md (template + first 10 entries) | JCH | 2026-06-22 |
| MODEL_SELECTION.md (OpenRouter routing logic) | Dobby | 2026-06-22 |
| HARDWARE_MATRIX.md (M1/M5/RPi support) |

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 387
- Résolus automatiquement : 104
- Résolus manuellement : 0
- Encore ouverts : 283
- **Taux : 26.9%**

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

- [Decision] | Évaluation de la couche multi-modèles ; simplification des endpoints | ✅ Validée |
- [Decision] | Vérification des effets en aval avant déploiement | ⏳ En cours |
- [Decision] | Rejet de la commande Mouser (quota 10 dépassé) ; alternative identifiée | ✅ Validée |
- [Decision] | Constraints techniques documentées ; brochage non standard identifié | 📝 Documenter |
- [Decision] | Diagnostic multi-niveaux du repo (18 Go, 12 projets) | ✅ Déployée |
- [Decision] : Les décisions sont souvent implicites (« validé oui ») sans justification écrite. Aucune trace d'un registro de décisions formel.
- [Failure] (`pka-homeassistant`)
- [Failure] Status : Bloqueur actif
- [Failure] Impact : Intégration HA-Sonoff non fonctionnelle
- [Failure] Symptôme : `MCP validation failed: pka-homeassistant: Stdio transport closed`
- [Failure] Action attendue : Diagnostic sur le serveur MCP HomeAssistant
- [Failure] Traceback : Updater loop failure sur `getUpdates`
- [Failure] Path : `/scripts/decouvertes-collector/venv/lib/python3.13/site-packages/telegram/ext/_updater.py:753`
- [Failure] Cause probable : Authentification token ou rate-limiting
- [Failure] Équipe notifiée : ❌ Non tracé
- [Failure] Erreur : `Connection Failed: Device Unresponsive`
- [Failure] Possible cause : Programme concurrent bloquant le port
- [Failure] MCP Server Stdio Transport Closed** (`pka-homeassistant`)
- [Failure] Telegram Bot — HTTP 409 Conflict
- [Failure] Device Unresponsive (Camera 1005005710463218)

### Fréquence des patterns (14 jours)
- **Decision** : 12 jours, 452 occurrences
- **Failure** : 12 jours, 460 occurrences
- **Question** : 12 jours, 344 occurrences
- **Recurring question** : 12 jours, 227 occurrences
- **Blocker** : 1 jours, 1 occurrences
- **Conflict detected** : 1 jours, 3 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (12x) lement la clé anthropic fonctionne mais on va sur le M1
- [Decision] (12x) n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont
- [Decision] (12x) on va maintenant dans travels/ pka decouvertes. si j'envoie un me
- [Decision] (12x) our ce lieu directement ou doit il etre validé
- [Failure] (12x) error handlers are registered, logging exception.Traceback (most recent call las
- [Question] (12x) n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?
- [Question] (12x) pourquoi en 2 tu parles de usb-A , le mac a des usb-c
- [Decision] (11x) a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta
- [Decision] (11x) ent il y a un nouveau message telegrma. je vais changer la cle
- [Decision] (11x) les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l
- [Failure] (11x) GLOBAL OPTIONS:   --debug                       Enable debug logging (default: f
- [Failure] (11x) on a crashe dans le dernier boulot : check graphy complet utilisant ol
- [Question] (11x) pourquoi c'est eclusif claude ?
- [Question] (11x) pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs.
- [Decision] (10x) dernier point, on va matcher les besoins de capteurs iot van avec les besoins de

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **lement la clé anthropic fonctionne mais on va sur le M1**
- [ ] Documenter : **n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont**
- [ ] Documenter : **on va maintenant dans travels/ pka decouvertes. si j'envoie un me**
- [ ] Documenter : **our ce lieu directement ou doit il etre validé**
- [ ] Documenter : **error handlers are registered, logging exception.Traceback (most recent call las**
- [ ] Documenter : **n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?**
- [ ] Documenter : **pourquoi en 2 tu parles de usb-A , le mac a des usb-c**
- [ ] Documenter : **a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta**
- [ ] Documenter : **ent il y a un nouveau message telegrma. je vais changer la cle**
- [ ] Documenter : **les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l**
- [ ] Documenter : **GLOBAL OPTIONS:   --debug                       Enable debug logging (default: f**
- [ ] Documenter : **on a crashe dans le dernier boulot : check graphy complet utilisant ol**
- [ ] Documenter : **pourquoi c'est eclusif claude ?**
- [ ] Documenter : **pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs.**
- [ ] Documenter : **dernier point, on va matcher les besoins de capteurs iot van avec les besoins de**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 20
- Jours d'observation : 12
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**159** recommandations au total — **159** ouvertes — **0** en cours — **0** terminées

⚠️ 81 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 129
- **Forge** : 26
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=153] (2026-06-19) **Dobby** : Créer un document "Décisions PKA"** : y reporter chaque décision (projet, matéri
- [id=154] (2026-06-19) **Dobby** : Installer un glossaire** : fichier `glossary.md` dans `PKA_JCH/docs/` avec défin
- [id=155] (2026-06-19) **Dobby** : Corriger le serveur MCP HA** : vérifier la configuration du `stdio_transport`, r
- [id=156] (2026-06-19) **Forge** : Reprendre le script planté** : identifier le script via les logs (rechercher "ch
- [id=157] (2026-06-19) **Forge** : Uniformiser les commandes Arduino** : ajouter un alias ou un script dans `~/bin/

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.11 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.11**
