---
date: 2026-06-21
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1115
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-21

**Sessions analysées :** 3 | **Échanges :** 1115 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA — Sessions 2026-06-21

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **Rester sur le working set actuel** | Stabilisation du repo PKA | ✅ Validée avec reminders |
| **OpenRouter comme seul routeur pour Kimi** | Migration depuis Anthropic (M1 → OpenRouter) | ⏳ En cours de vérification |
| **Supprimer les répertoires `notebook_sources` et `.md` redondants** | Nettoyage du vault | ⏳ À localiser et exécuter |
| **Passer exclusivement à OpenRouter** (vs. Anthropic key) | Simplification des credentials | ⏳ À vérifier sur M1 |

**Problème majeur** : Les décisions ne sont pas explicitement tracées avec raison/impact. Tu dis souvent "ok on va faire X" mais sans documenter *pourquoi* ni *où ça affecte l'aval*.

---

## Échecs ouverts / bloqueurs

### 🔴 Critiques

1. **Crash non résolu du dernier job**
   - Message : `Traceback (most recent call last): File "/Users/jchavauxm5/PKA_JCH/s...`
   - Scope : "graphy complet utilisant ol" (incomplet dans logs)
   - **Action manquante** : Root cause analysis jamais complétée

2. **Camera WildNexus bloquée**
   - Référence : `1005005710463218` (caméra Arducam IMX500 AI pour ESP32-P4)
   - État : "faire le point sur la camera de wildnexus" → jamais fait
   - **Décision suspendue** : USB-A vs. USB-C, harness, type de connecteur

3. **Terminal crash avec vault incomplet**
   - `regarde ce qui a été fait et ce qui reste à faire` → Diagnostic jamais livré
   - État fichiers : inbox équipe bloquée, rejets non triés

4. **Télégram-bot HTTP 409 Conflict**
   - Fichier : `/scripts/telegram-bot/bot.py`
   - Erreur : `No error handlers are registered`
   - **Impact** : Processus actif #4 en échec silencieux

5. **Git pack bloated (1,92 Go)**
   - "Health-check auto RED à cause de faux positifs massifs"
   - Historique binaire non optimisé
   - **Risk** : Clone/pull lents, CI/CD ralenti

### ⚠️ Non-bloqueurs mais irritants

- **Polyvalence des références Mouser** : Tu vas chercher manuellement les références au lieu de les récupérer via API/scraping
- **Confusion Claude/DeepSeek exclusivité** : Répond à la question 3 fois sans clarifier pourquoi c'est exclusif à Claude (MCP vs. API?)
- **Notes Apple inaccessibles** : "Comment faire en sorte que tu y ai accès?" → Jamais explorée

---

## Questions récurrentes (signe de lacune documentaire)

### Pattern détecté : **Portabilité et maintenance outillage**

1. **"Comment je maintiens mon outil quand je passe du M5 au M1?"**
   - Revient 3x sous formes différentes
   - **Manque** : Documentation sur venv, .env, Python path isolation
   - **Root cause** : Pas de "Setup Playbook" pour migration machine

2. **"Terminal vs. VSCode terminal — c'est la même commande?"**
   - Posée 2x (token `urn_meta>`)
   - **Manque** : Doc sur PATH, shell sourcing, isolation d'environnement
   - **Symptôme** : Tu ne sais pas si c'est un problème shell ou Python

3. **"Pourquoi maintenant tu as les ref Mouser et avant non?"**
   - Frustration visible
   - **Manque** : Changelog des changements d'API/scraping
   - **Impact** : Tu dois re-tester chaque fois au lieu de faire confiance

4. **"C'est quoi (.venv) / (.env)?"**
   - Basique mais posée comme urgente
   - **Symptôme** : Dobby/assistants ne prennent pas 5 min pour expliquer
   - **Impact** : Tu bloques sur des triviaux

### Pattern détecté : **Décisions en cascade non documentées**

- "Est-ce que ce qu'on va faire a des effets cascades en aval?" → Posée mais réponse jamais tracée
- **Manque** : Impact map ou dependency graph

---

## Nouveaux patterns détectés

### 1. **Mode "Rapid Fire"**
Tu poses 8–12 questions/décisions par minute, en sautant entre contextes (caméra → fichiers → modèles → shopping).
- **Risque** : Les réponses partielles s'accumulent, créant des "bulles" de semi-connaissance
- **Exemple** : WildNexus camera suspendue depuis 3 sessions

### 2. **Approche "Verify After" (inverse du planning)**
- "Vérifie attentivement si c'est correct"
- "Regarde ce qui a été fait"
- "Vérifie ou il sont [les fichiers]"

Au lieu d'un plan A → validate → execute, tu fais execute → verify → patch.
- **Coût** : Chaque vérification relance une session complète

### 3. **Outils = Entropia**
Tu utilises 3–4 interfaces en parallèle : DeepSeek TUI, Claude Code, Codex CLI, Composer (?) sans schéma clair.
- "Ok une fois dedans comment je choisis le modele?"
- Pas de routing logic transparent → trust/uncertainty

### 4. **Documentation dans l'action, pas en amont**
- "Mets dans les reminders de me le pro[poser]" (future-proofing via voice memo)
- **Symptôme** : Tu délégues la documentation à des rappels plutôt que de la structurer

---

## Efficacités / inefficacités

### ✅ Efficace

| What | Why |
|------|-----|
| **Working set focus** | Tu relis les paths à chaque session → limite la pollution cognitive |
| **Multi-model testing** | DeepSeek + Claude = validation croisée rapide |
| **Rapid hypothesis** | "Comment faire X?" → "Essaye Y" → fast feedback loop |
| **Extraction de patterns (Dobby)** | Détecte les silences documentaires auto → utile pour cette retro |

### ❌ Inefficace

| What | Why | Cost |
|------|-----|------|
| **Pas de decision log** | Décisions perdues après session → même Q posée 3x | Temps perdu, frustration |
| **Crash non-rootcaused** | "On a crashé" → pas de Traceback complet → même erreur possible demain | Risk de régressions |
| **Référence shopping manuel** | Tu tapes "Mouser" + recherche au lieu de BOM importable | 15 min/achat perdues |
| **Confusion CLI vs. CodeUI** | "C'est la même commande?" → oui/non/depends pas clair | Tu doutes de chaque script |
| **Camera WildNexus gelée 3 sessions** | Pas de "Next Step" assignée → implicit priority=0 | Scope creep |
| **Venv/env vocabulary absent** | Posée comme urgente mais jamais expliquée au niveau "mental model" | Tu ne peux pas troubleshoot seul |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🧠 État du système (2026-06-21)

**Healthy :**
- Working set stable (AGENTS.md, CLAUDE.md, bin/dobby.sh)
- 12 projets actifs (4 prod, 4 en cours, 4 veille)
- Équipe DB : 32 membres + Dobby

**At Risk :**
- Crash terminal non-rootcaused (jobs "graphy" incomplets)
- Camera WildNexus : décision suspendue (OV5640 DVP 24-pin → brochage ESP32-S3 mismatch?)
- Telegram-bot 409 Conflict (unhandled error)
- Git pack 1,92 Go (historique binaire)

**In Flux :**
- Authentification Anthropic → OpenRouter (en cours, M1)
- Nettoyage vault (`notebook_sources`, `.md` redundants)
- Notes Apple integration (demandée, pas exploré)

### 📋 Questions qui vont revenir

1. **Portabilité M5 → M1** → Fais un **SETUP.md** dans le repo (Python path, venv activation, alias shell)
2. **Terminal vs. VSCode** → Ajoute à CLAUDE.md une section "Shell Context"
3. **Mouser refs** → Documente le changement API ou intègre un scraper persistent (BOM importer)
4. **"C'est exclusif Claude?"** → Clarify MCP architecture dans AGENTS.md

### 🔧 Dettes techniques à tracker

- [ ] Crash "graphy complet" — ouvrir issue avec Traceback complet
- [ ] Camera WildNexus — Décider USB pinout (A vs. C), commander, fermer issue
- [ ] Telegram-bot error handler — Ajouter try/catch + logging
- [ ] Git pack optimization — `git gc --aggressive` + document résultat
- [ ] Venv vocabulary — 5-min explainer video ou doc

---

## Recommandations

### Immédiat (prochaine session)

1. **Ouvre un "Decision Checkpoint" workflow**
   ```markdown
   ## Decision: [NAME]
   - What: [Action]
   - Why: [Rationale]
   - Impact: [Downstream effects]
   - Verified: [YES/NO/PENDING]
   - Date: [YYYY-MM-DD]
   ```
   Ajoute aux reminders → force cette structure *avant* de cliquer "ok"

2. **Rootcause le crash terminal**
   - Récupère le `Traceback` complet du job "graphy"
   - Ouvre issue dans `/tests/crashes/` avec reproduction steps
   - Assign Dobby pour suivre jusqu'à fix

3. **Close WildNexus camera decision**
   - Choose : OV5640 ou Arducam IMX500?
   - Order → document harness/USB pinout dans WIKI
   - Test on ESP32-S3

### Court terme (2–3 sessions)

4. **Create 3 Quick Docs** (chacun <5min read)
   - `SETUP_NEW_MACHINE.md` (venv, .env, path, alias)
   - `AGENT_ROUTING.md` (quand utiliser DeepSeek vs. Claude vs. OpenRouter)
   - `VIM_GLOSSARY.md` (CLI commands demystified)

5. **Fix Telegram-bot**
   - Add error handler to `/scripts/telegram-bot/bot.py` line 753
   - Test 409 conflict scenario
   - Document what triggers it

6. **Optimize Git pack**
   - Run `git gc --aggressive --prune=now`
   - Measure before/after size
   - Document in MEMORY.md

7. **Implement BOM scraper**
   - Auto-fetch Mouser references from parts list
   - Cache in `scripts/mouser-bom/`
   - Integrate with shopping workflow

### Medium term

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 357
- Résolus automatiquement : 84
- Résolus manuellement : 0
- Encore ouverts : 273
- **Taux : 23.5%**

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

- [Decision] | Stabilisation du repo PKA | ✅ Validée avec reminders |
- [Decision] | Migration depuis Anthropic (M1 → OpenRouter) | ⏳ En cours de vérification |
- [Decision] | Nettoyage du vault | ⏳ À localiser et exécuter |
- [Decision] (vs. Anthropic key) | Simplification des credentials | ⏳ À vérifier sur M1 |
- [Decision] : Les décisions ne sont pas explicitement tracées avec raison/impact. Tu dis souvent "ok on va faire X" mais sans documenter *pourquoi* ni *où ça affe
- [Failure] Message : `Traceback (most recent call last): File "/Users/jchavauxm5/PKA_JCH/s...`
- [Failure] Scope : "graphy complet utilisant ol" (incomplet dans logs)
- [Failure] Action manquante** : Root cause analysis jamais complétée
- [Failure] Référence : `1005005710463218` (caméra Arducam IMX500 AI pour ESP32-P4)
- [Failure] État : "faire le point sur la camera de wildnexus" → jamais fait
- [Failure] Décision suspendue** : USB-A vs. USB-C, harness, type de connecteur
- [Failure] `regarde ce qui a été fait et ce qui reste à faire` → Diagnostic jamais livré
- [Failure] État fichiers : inbox équipe bloquée, rejets non triés
- [Failure] Fichier : `/scripts/telegram-bot/bot.py`
- [Failure] Erreur : `No error handlers are registered`
- [Failure] Impact** : Processus actif #4 en échec silencieux
- [Failure] "Health-check auto RED à cause de faux positifs massifs
- [Failure] Historique binaire non optimisé
- [Failure] Risk** : Clone/pull lents, CI/CD ralenti
- [Failure] Crash non résolu du dernier job
- [Failure] Camera WildNexus bloquée
- [Failure] Terminal crash avec vault incomplet
- [Failure] Télégram-bot HTTP 409 Conflict
- [Failure] Git pack bloated (1,92 Go)

### Fréquence des patterns (14 jours)
- **Decision** : 13 jours, 472 occurrences
- **Failure** : 13 jours, 480 occurrences
- **Question** : 13 jours, 360 occurrences
- **Recurring question** : 13 jours, 237 occurrences
- **Blocker** : 1 jours, 1 occurrences
- **Conflict detected** : 1 jours, 3 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (13x) lement la clé anthropic fonctionne mais on va sur le M1
- [Decision] (13x) n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont
- [Decision] (13x) on va maintenant dans travels/ pka decouvertes. si j'envoie un me
- [Decision] (13x) our ce lieu directement ou doit il etre validé
- [Failure] (13x) error handlers are registered, logging exception.Traceback (most recent call las
- [Question] (13x) n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?
- [Question] (13x) pourquoi en 2 tu parles de usb-A , le mac a des usb-c
- [Decision] (12x) ent il y a un nouveau message telegrma. je vais changer la cle
- [Failure] (12x) GLOBAL OPTIONS:   --debug                       Enable debug logging (default: f
- [Failure] (12x) on a crashe dans le dernier boulot : check graphy complet utilisant ol
- [Question] (12x) pourquoi c'est eclusif claude ?
- [Decision] (11x) a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta
- [Decision] (11x) les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l
- [Failure] (11x) d'attent garde fichiers ne inbox equipe bloquée et en cours. en attente validati
- [Question] (11x) pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs.

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **lement la clé anthropic fonctionne mais on va sur le M1**
- [ ] Documenter : **n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont**
- [ ] Documenter : **on va maintenant dans travels/ pka decouvertes. si j'envoie un me**
- [ ] Documenter : **our ce lieu directement ou doit il etre validé**
- [ ] Documenter : **error handlers are registered, logging exception.Traceback (most recent call las**
- [ ] Documenter : **n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?**
- [ ] Documenter : **pourquoi en 2 tu parles de usb-A , le mac a des usb-c**
- [ ] Documenter : **ent il y a un nouveau message telegrma. je vais changer la cle**
- [ ] Documenter : **GLOBAL OPTIONS:   --debug                       Enable debug logging (default: f**
- [ ] Documenter : **on a crashe dans le dernier boulot : check graphy complet utilisant ol**
- [ ] Documenter : **pourquoi c'est eclusif claude ?**
- [ ] Documenter : **a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta**
- [ ] Documenter : **les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l**
- [ ] Documenter : **d'attent garde fichiers ne inbox equipe bloquée et en cours. en attente validati**
- [ ] Documenter : **pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs.**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 24
- Jours d'observation : 13
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**172** recommandations au total — **172** ouvertes — **0** en cours — **0** terminées

⚠️ 96 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 141
- **Forge** : 26
- **Corbeau** : 3
- **Furet** : 2

### Plus récentes ouvertes

- [id=160] (2026-06-21) **Dobby** : Ouvre un "Decision Checkpoint" workflow
- [id=161] (2026-06-21) **Dobby** : Why: [Rationale
- [id=162] (2026-06-21) **Dobby** : Impact: [Downstream effects
- [id=163] (2026-06-21) **Dobby** : Verified: [YES/NO/PENDING
- [id=164] (2026-06-21) **Dobby** : Date: [YYYY-MM-DD

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.11 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.11**
