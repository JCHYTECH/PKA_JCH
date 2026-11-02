---
date: 2026-10-25
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1057
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-25

**Sessions analysées :** 2 | **Échanges :** 1057 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-10-25
## JCH × Assistants IA (DeepSeek, Claude)

---

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **LUPO VAN** : Installation Bluetti 100 V2 + chargeur 2 | Équipement van (JCH) | ✅ Validée |
| **Standardisation 12V** | Faciliter procurement WILDNEXUS | ✅ Validée |
| **Vetalyx - capital 10k€** | Structure belgique avec DiaHo 40% | ✅ Prise (en attente confirmations UCM) |
| **Traitement batch skip** | Procédure : par lots de 10 | ✅ Spécifiée |
| **Draft→Validé workflow** | Ordre de traitement : d'abord les drafts | ✅ Spécifiée |
| **Distribution WILDNEXUS** | À redéfinir (question lancée, pas de réponse capturée) | ⚠️ Bloquée |
| **Procédure fiches spots** | Stationnement / localisation | ⏳ En conception |

**Problème identifié** : La décision de distribution WILDNEXUS est relancée de manière circulaire → aucune documentation trouvée. Indicateur de perte d'information ou d'absence d'ADR.

---

## Échecs ouverts / bloqueurs

### 🔴 CRITIQUES

1. **WILDNEXUS - Distribution channel perdu**
   - Question récurrente : "rappele moi comment on voulait distribuer wildlens ?"
   - Aucune ADR ou doc référencée
   - **Impact** : Décision à reprendre depuis zéro

2. **Vetalyx - Statut fiscal DiaHo flou**
   - Changement : DiaHo entre au capital 40% (entité chinoise)
   - Question ouverte : Obligation de déclaration ?
   - UCM Belgique interrogée, réponse partielle capturée
   - **Impact** : Blocage administratif potentiel avant constitution

3. **Erreurs API / HA (Home Assistant)**
   - `van à niveau off, cap ne fonctionne pas` + `API key required`
   - `Erreur 403 access blocked`
   - `Erreur 1007 (invalid frame payload data) realtime_input`
   - **État** : Bloqueur technique non résolu, requiert debug

4. **VanRoll Test - données manquantes**
   - "pourquoi vanroll test ne donne plus de données"
   - Analyse requise : cas particulier ou bug global ?
   - **Impact** : Incertitude sur data pipeline

### 🟡 MAJEURS

5. **Dante - Fiche vide**
   - À analyser : exception ou pattern systémique ?
   - Requiert investigation root cause

6. **Intégration KIRO**
   - JCH a partagé lien Kiro (interface IA locale) + contenu page
   - Demande : "peut-on l'intégrer à notre routine ?"
   - **Pas d'analyse de faisabilité capturée**
   - Reste en pending

---

## Questions récurrentes (signe de lacune documentaire)

### Hochement de tête du problème 🚩

| Question | Fréquence | Racine probable |
|----------|-----------|-----------------|
| Specs VAN (roues avant/arrière, dimensions 25-26cm tiroir) | 2+ | Pas de schéma de cotation centralisé ; specs éparses |
| État des données VANROLL/DANTE | 2+ | Pas de monitoring / alerting sur data quality |
| "C'est quoi le ZH ?" / "L(M) ?" / "state files ?" | 3+ | **Vocabulaire technique non standardisé** ou absent de la wiki |
| TTL 24h + HTML button usage | 2+ | Doc de pattern réutilisable manquante |
| Procédures via telegram vs inbox | 2+ | Pas de système de commandes procédurales unifié |
| "Comment tu gardes en mémoire les procédures ?" | 2+ | **Besoin d'un registre de procédures déclenchables par nom** |

### ⚠️ Diagnostic
**Le PKA souffre d'une fragmentation documentaire.**
- Vocabulaire ad-hoc non défini (ZH, L(M), state files)
- Procédures techniques répétées dans plusieurs canaux (telegram, inbox)
- Pas de registre de procédures typées
- Spécifications hardware éparses (VAN)

---

## Nouveaux patterns détectés

### 1. **Cycle "rappelle-moi"**
JCH relance régulièrement des questions sur des décisions antérieures (WILDNEXUS distrib, specs VAN).
- **Signe** : ADR ou décisions ne sont pas :
  - Assez visibles dans le PKA
  - Assez bien indexées
  - Assez mnémoniques (titres trop génériques ?)

### 2. **Zigzag administratif Vetalyx**
JCH navigue entre :
- Contrats (statuts, directors, articles)
- Fiscal (endettement 175k€, risque ISC, DiaHo 40%)
- Humain (rôles opératifs vs actionnaires)

**Pattern** : Pas de canvas global "Vetalyx incorporation checklist". Chaque aspect revient séparé.

### 3. **Multi-tool async avec perte de context**
- DeepSeek TUI pour local reasoning
- Claude/Composer pour édition riche
- Telegram pour urgences
- Inbox pour suivi

**Pattern** : Aucune synchronisation capturée entre les flux. Questions lancées dans un outil, réponses potentiellement perdues dans un autre.

### 4. **Tests/validation sans critères explicites**
- "en cours de test et seuls les testeurs approuvés par le développeur y ont accès"
- Pas de test matrix, de sign-off criteria
- VanRoll/Dante data issues → analyse requise, mais sans framework

**Pattern** : Tests informels, causels → débordements et découvertes tardives.

### 5. **Procédures matérialisées dans l'oralité**
- Batch de 10 pour skip
- Fiches spots pour parking
- 25-26 cm pour tiroir (car banquette passager reste en place)

**Pattern** : Règles métier non codifiées → répétition, oublis, réinterprétations.

---

## Efficacités / Inefficacités

### ✅ Efficacités détectées

1. **Clarté des constraints matériels**
   - JCH énonce clairement : "on va rester tout en 12V" → décision d'architecture immédiate et propagable
   
2. **Utilisation multi-outils réfléchie**
   - DeepSeek TUI pour le local
   - Claude Composer pour les formats riches (contrats, docs)
   - Bonne séparation logique

3. **Suivi des blockers signalés**
   - Erreurs HA, API 403, frames invalides sont nommées explicitement
   - JCH demande analyses (VanRoll, Dante)

### ❌ Inefficacités détectées

1. **Perte d'ADR/décisions historiques**
   - Distribution WILDNEXUS = question en boucle
   - Aucune référence à un ADR-001, ADR-002 existant ?
   - (On voit ADR-003 en path active, mais pas ADR-001/002 capturés)

2. **Pas de triage / priorité explicite**
   - Vetalyx fiscal urgente ?
   - LUPO batterie urgente ?
   - Bug HA bloqueur ?
   - → Aucun tri n'apparaît

3. **Questions sans owner assigné**
   - "analyse le pourquoi" (Dante fiche vide) → qui le fait ? quand ?
   - "verifie le bug HA" → qui escalade si plus grave ?

4. **Accumulation de petites inconnues**
   - ZH, L(M), state files, ISC risk, cap/van config
   - Chacun dilapide cognitive load à chaque session
   - Pas de glossaire

5. **Validation procédurales ad-hoc**
   - Batch de 10 : décidé oralement
   - Fiches spots : procédure en design, pas encore exécutée
   - Pas de "testée", "validée en prod", "à revoir"

6. **Latence capturée**
   - "constat en un fichier quand les chinois auront répondu" → on attend. Pas de suivi visible.
   - "d'abord on va leur poser des questions polies" → quand ? qui ? where's the task ?

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🧠 Context persistant requis

1. **WILDNEXUS**
   - Statut : En phase d'architecture LPWAN (ADR-003 choix radio détecté)
   - Dataset : InsectSet459 (459 insectes annotés pour acoustic)
   - Décision 12V imposée → impact procurement
   - **Question ouverte** : Distribution channel (à reconstruire)
   - Mouser engagement attendu (fichier `2026-10-25_dobby_conseil_wildnexus-mouser.md` créé)

2. **VETALYX (Belgique)**
   - Capital : 10k€
   - Acteurs : JCH (et qui ? Mélanie ?), DiaHo 40%, + tiers ?
   - Statut fiscal/admin : En attente confirmations UCM
   - Articles clés : 23 (fiscal year) et 33 (directors) non finalisés
   - **Risque ISC** : À clarifier
   - **Changement major** : DiaHo entre comme actionnaire, pas ressortissants physiques chinois en ops
   - **Deadline** : À spécifier (avant ? after ? quand ?)

3. **LUPO VAN**
   - Battery : Bluetti 100 V2 + chargeur 2
   - Config à valider : Specs roues (avant/arrière), tiroir 25-26cm
   - Integration avec HA (bug en cours, see bloqueur)
   - Statut test : Approbation développeur requise avant accès

4. **Glossaire technique manquant**
   - ZH = ?
   - L(M) = ?
   - State files = ?
   - ISC risk = ?
   - cap = ?
   - **Action** : Ajouter à wiki ou AGENTS.md

5. **Procédures non codifiées**
   - Batch skip : par 10
   - Fiches spots : en conception
   - Procédures via telegram + inbox : requiert registre centralisé
   - **Action** : Créer bin/procedures.sh ou wiki/PROCEDURES.md

---

## Recommandations

### 🎯 Court terme (cette semaine)

1. **Reconstruire ADR WILDNEXUS distribution**
   - Session dédiée 30 min
   - Résultat : ADR-001 ou ADR-002 redécouvert ou créé
   - Output : 1 fichier `WILDNEXUS_02_DECISIONS/ADR-00X-distribution-channel.md`

2. **Créer glossaire

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 31
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 9.7%**

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

- [Decision] : Installation Bluetti 100 V2 + chargeur 2 | Équipement van (JCH) | ✅ Validée |
- [Decision] | Faciliter procurement WILDNEXUS | ✅ Validée |
- [Decision] capital 10k€** | Structure belgique avec DiaHo 40% | ✅ Prise (en attente confirmations UCM) |
- [Decision] | Procédure : par lots de 10 | ✅ Spécifiée |
- [Decision] | Ordre de traitement : d'abord les drafts | ✅ Spécifiée |
- [Decision] | À redéfinir (question lancée, pas de réponse capturée) | ⚠️ Bloquée |
- [Decision] | Stationnement / localisation | ⏳ En conception |
- [Decision] : La décision de distribution WILDNEXUS est relancée de manière circulaire → aucune documentation trouvée. Indicateur de perte d'information ou d'abse
- [Failure] Distribution channel perdu
- [Failure] Question récurrente : "rappele moi comment on voulait distribuer wildlens ?
- [Failure] Aucune ADR ou doc référencée
- [Failure] Impact** : Décision à reprendre depuis zéro
- [Failure] Statut fiscal DiaHo flou
- [Failure] Changement : DiaHo entre au capital 40% (entité chinoise)
- [Failure] Question ouverte : Obligation de déclaration ?
- [Failure] UCM Belgique interrogée, réponse partielle capturée
- [Failure] Impact** : Blocage administratif potentiel avant constitution
- [Failure] `van à niveau off, cap ne fonctionne pas` + `API key required`
- [Failure] `Erreur 403 access blocked`
- [Failure] `Erreur 1007 (invalid frame payload data) realtime_input`
- [Failure] État** : Bloqueur technique non résolu, requiert debug
- [Failure] pourquoi vanroll test ne donne plus de données
- [Failure] Analyse requise : cas particulier ou bug global ?
- [Failure] Impact** : Incertitude sur data pipeline
- [Failure] WILDNEXUS - Distribution channel perdu
- [Failure] Vetalyx - Statut fiscal DiaHo flou
- [Failure] Erreurs API / HA (Home Assistant)
- [Failure] VanRoll Test - données manquantes

### Fréquence des patterns (14 jours)
- **Decision** : 5 jours, 29 occurrences
- **Failure** : 5 jours, 17 occurrences
- **Recurring question** : 5 jours, 15 occurrences
- **Question** : 4 jours, 23 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 28
- Jours d'observation : 7
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**529** recommandations au total — **529** ouvertes — **0** en cours — **0** terminées

⚠️ 485 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 476
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 6
- **Renard** : 3
- **Sybil** : 2

### Plus récentes ouvertes

- [id=525] (2026-10-25) **Dobby** : Reconstruire ADR WILDNEXUS distribution
- [id=526] (2026-10-25) **Dobby** : Session dédiée 30 min
- [id=527] (2026-10-25) **Dobby** : Résultat : ADR-001 ou ADR-002 redécouvert ou créé
- [id=528] (2026-10-25) **Dobby** : Output : 1 fichier `WILDNEXUS_02_DECISIONS/ADR-00X-distribution-channel.md`
- [id=529] (2026-10-25) **Dobby** : Créer glossaire

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.28 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.28**
