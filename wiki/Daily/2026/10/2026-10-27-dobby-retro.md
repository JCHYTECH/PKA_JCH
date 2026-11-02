---
date: 2026-10-27
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1183
modeles: deepseek-v4, deepseek-v4-flash, deepseek-v4-pro
---

# Rétrospective — 2026-10-27

**Sessions analysées :** 4 | **Échanges :** 1183 | **Modèles :** deepseek-v4, deepseek-v4-flash, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-10-27
## Dobby Analysis Report

---

## Décisions prises

### Confirmées et documentées
- **WILDNEXUS** : rester en **français uniquement** pour la documentation
- **Caissons** : équiper d'un **tiroir avec coulisses** (dimensions finalisées : 25-26 cm)
- **Procurement** : rester au **niveau 12** pour homogénéiser la chaîne d'approvisionnement
- **Distribution WILDLENS** : décision en cours de clarification (question récurrente = pas finalisée)
- **Vetalyx/Belgique** : accepter l'entrée du capital chinois à **40% via DiaHo** sans représentant physique

### Partiellement documentées
- Validation des fiches (nombre précis des `needs_review` : **3 fiches** mais pas clairement identifiées)
- Tests en cours avec accès restreint aux testeurs approuvés (procédure floue)
- Activation d'un constat en fichier "quand les chinois auront répondu" (pas de deadline, pas de trigger clairement défini)

### Floues / à clarifier
- Stratégie WILDNEXUS vs WILDNEXUS vs WildNexus (3 variantes orthographiques = confusion)
- Procédure de lancement de tâches par nom via Telegram/Inbox (question posée mais sans réponse documentée)

---

## Échecs ouverts / bloqueurs

### Techniques critiques
1. **Backup chiffré échoué** : `tmutil startbackupVolume on disk8s2` → Volume APFS chiffré verrouillé
   - Statut : non résolu, aucune tentative de contournement documentée
   
2. **WebSocket frame payload error** : `received 1007 (invalid frame payload data)` dans `realtime_input.m`
   - Cause : pas d'investigation complète
   - Impact : affecte la connexion temps réel (outil DeepSeek TUI ?)
   
3. **Connexion sécurisée échouée** : "secure connection failed"
   - Contexte : flou dans le transcript
   - Procédure de debug : mentionnée mais pas exécutée

4. **Home Assistant** : "van à niveau off, cap ne fonctionne pas et en dessous j'ai API key required"
   - Bug non identifié, niveau d'abstraction confus
   - Demande : "vérifie le bug HA" → non suivi

5. **VanRoll test** : "ne donne plus de données"
   - Demandé une vérification mais pas de rapport de retour

### Méthodologiques
- **Recherche Ombrie** : demandée pour lieux "exotiques peu visités mais exceptionnels" → pas de résultat visible
- **Synthèse de lecture** : concept mentionné mais jamais défini ("c'est quoi la synthese de lecture propre ?")

### Bloqueurs en attente externe
- Réponse des partenaires chinois (DiaHo) sur la structuration de Vetalyx → calendrier flou

---

## Questions récurrentes (signe de lacune documentaire)

### TOP 3 - Symptôme de documentation absente
1. **"c'est quoi les 3 fiches needs_review ?"** (posée 2x minimum)
   - Aucun fichier référençant ces 3 fiches
   - Dobby ne peut pas tracer la réponse
   
2. **"L(M) c'est quoi ?"** (posée 2x)
   - Notation ambiguë : Loss(Model) ? Level(Meta) ? Jamais clarifiée
   
3. **"Comment faire en sorte que tu gardes en mémoire les procédures pour lancer via un nom ?"**
   - Démontre une friction entre Inbox/Telegram et la mémoire système
   - Pas de solution implémentée

### Questions de compréhension conceptuelle
- "states files" : fichiers de synchronisation HA ? Git ? Autre ?
- "risque isc" : ISC = risque de financement ? Sécurité ? Non défini
- "ZH" : acronyme totalement inexpliqué
- "lupo vs assiette/esneux/iphone" : la différence entre instances HA reste floue après la question

### Questions de processus
- "pourquoi Dobby travaille sans s'appuyer sur les experts ?" → révèle une tension architecture (Dobby autonome vs. experts comme référence)
- "TTL 24h : comment utiliser cela avec fluidité ?" → vague, pas de cas d'usage concret

---

## Nouveaux patterns détectés

### Pattern 1 : Décisions orales non documentées immédiatement
**Symptôme** : fiches finalisées, caissons avec tiroir, niveau 12 → détectées après-coup via extraction
**Cause** : pas de protocole de validation-capture entre JCH et assistants
**Risque** : perte si les participants oublient les détails

### Pattern 2 : Questions posées en cascade sans résolution
**Exemple** : "comment faire en sorte que tu gardes en mémoire..." → réponse attendue = silence → question reprise 3 sessions plus tard
**Diagnostic** : soit l'IA n'a pas su répondre, soit la réponse n'a pas été convertie en procédure actionnable

### Pattern 3 : Confusion entre projets et sous-projets
**Evidence** : 
- WILDNEXUS (50x), WildNexus (10x), WILDNEXUS (8x) — variations orthographiques
- Vetalyx (20x), VETALYX (8x), Vetalyx (16x)
- Aucun document de clarification "naming convention"

### Pattern 4 : Outils en parallèle, mémoire fragmentée
**Setup actuel** : Claude (74x), DeepSeek (14x), Tailscale (42x), Ollama (9x)
- Chaque outil vit dans son contexte
- Pas de synchronisation Inbox ↔ Telegram ↔ PKA
- JCH demande : "comment faire en sorte que tu mémorises ?" → indique qu'il n'y a PAS de mémorisation unifiée

### Pattern 5 : Tests en cours = documentation gelée
**Exemple** : "en cours de test et seuls les testeurs approuvés par le développeur y ont accès"
- Pas de rapport de test visible
- Pas de critères de sortie du test
- Bloque potentiellement les décisions dépendantes

### Pattern 6 : Micro-décisions techniques sans tracabilité
**Exemple** : dimensions du tiroir (25-26 cm) + justification ("on peut laisser le meuble en place") → aucun ticket, aucun ADR
- WILDNEXUS a un ADR-003 mais pas pour les tiroirs
- Pattern : décisions de design physique = orales, décisions techniques logicielles = ADR → **inconsistant**

---

## Efficacités / inefficacités

### ✅ Ce qui marche
1. **Claude + DeepSeek en tandem** : répartition claire (74 vs 14 mentions)
   - Claude = tâches complexes/raisonnement
   - DeepSeek = TUI/CLI rapide
   - Aucun conflit rapporté

2. **Tailscale** : backbone stable (42 mentions)
   - Connecte les machines M1/M5/RPI sans friction
   - Pas d'erreur de connexion rapportée (sauf HA ambigüe)

3. **Décisions opérationnelles rapides** : fiches validées, caissons équipés, niveau procurement fixé
   - Execution time : court
   - Consensus : acquis rapidement

### ❌ Ce qui traîne
1. **Lacune architecturale majeure** : pas de "single source of truth" pour les procédures
   - JCH demande "comment faire en sorte que..." = architecture absente
   - Dobby travaille en standalone, experts non impliqués systématiquement
   - Risque : décisions sous-optimales, expertise ignorée

2. **Bloqueurs techniques non priorisés**
   - Backup échoué (données critiques ?) → pas de deadline
   - WebSocket 1007 (realtime brané) → pas d'escalade
   - HA bug (smart home ?) → demandé mais pas suivi
   - **Verdict** : aucun triage urgence/importance

3. **Questions non résolues = accumulation**
   - L(M), states files, ZH, risque ISC, synthèse de lecture
   - 5+ questions "what is X ?" en 4 sessions = ROI documentaire très faible
   - **Coût d'opportunité** : temps dépensé à re-expliquer vs. créer

4. **Processus test opaque**
   - "testeurs approuvés par le développeur" → qui ? critères ?
   - Pas de rapport → pas de validation possible

5. **Configuration multi-instance fragmentée**
   - lupo/assiette vs esneux/iphone
   - "c'est l'instance HA ?" → flou après la question
   - Pas de topology document

### ⚡ Inefficacité majeure : la boucle Dobby
**Symptôme direct dans le transcript** :
> "explique moi pourquoi dobby travaille sans s'appuyer sur les experts. sont ils inutiles ou dobby préfère ?"

**Interprétation** : JCH détecte que Dobby fonctionne en vase clos
- Dobby : analyse locale, pas d'appel aux experts
- Experts (CLAUDE.md, AGENTS.md) : existent mais ne sont pas invoqués
- Résultat : perte de sagesse distribuée

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 Décisions verrouillées (à respecter)
1. **Français only** pour WILDNEXUS doc
2. **Niveau 12** pour procurement (pas de négociation)
3. **Caisson + tiroir** 25-26 cm (constraint client : banquette passager)
4. **Vetalyx** : capital 40% DiaHo (chinois), pas de représentant physique, capital = 10k EUR
5. **Fiches : 3 en needs_review** (identifier lesquelles !)

### ⚠️ Points d'attention
- Chinois répondront à la demande capitalistique → activation manuel d'un constat en fichier
- VanRoll test : ne donne plus de données (root cause à identifier)
- Home Assistant : "cap ne fonctionne pas" + "API key required" (à trier)
- Backup APFS chiffré : bloquerait une restauration d'urgence

### 📚 Lacunes documentaires critiques
| Concept | Status | Impact |
|---------|--------|--------|
| L(M) | Undefined | Affects specs/communication |
| States files | Unclear | HA integration risk |
| ZH | No context | 3 mentions, toujours mystère |
| Synthèse de lecture | Mentioned but never defined | Training/QA process unclear |
| Risque ISC | Floating number (175k EUR) | Vetalyx financial modeling |
| WILDNEXUS naming | 3 orthographes différentes | Searchability broken |
| Testeurs approuvés | Criteria unknown | Test governance absent |
| Procédure par nom (Inbox/Telegram) | Requested but not implemented | UX friction ongoing |

### 🔗 

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 30
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 6.7%**

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

- [Decision] WILDNEXUS** : rester en **français uniquement** pour la documentation
- [Decision] Caissons** : équiper d'un **tiroir avec coulisses** (dimensions finalisées : 25-26 cm)
- [Decision] Procurement** : rester au **niveau 12** pour homogénéiser la chaîne d'approvisionnement
- [Decision] Distribution WILDLENS** : décision en cours de clarification (question récurrente = pas finalisée)
- [Decision] Vetalyx/Belgique** : accepter l'entrée du capital chinois à **40% via DiaHo** sans représentant physique
- [Failure] : `tmutil startbackupVolume on disk8s2` → Volume APFS chiffré verrouillé
- [Failure] Statut : non résolu, aucune tentative de contournement documentée
- [Failure] : `received 1007 (invalid frame payload data)` dans `realtime_input.m`
- [Failure] Cause : pas d'investigation complète
- [Failure] Impact : affecte la connexion temps réel (outil DeepSeek TUI ?)
- [Failure] : "secure connection failed
- [Failure] Contexte : flou dans le transcript
- [Failure] Procédure de debug : mentionnée mais pas exécutée
- [Failure] : "van à niveau off, cap ne fonctionne pas et en dessous j'ai API key required
- [Failure] Bug non identifié, niveau d'abstraction confus
- [Failure] Demande : "vérifie le bug HA" → non suivi
- [Failure] : "ne donne plus de données
- [Failure] Demandé une vérification mais pas de rapport de retour
- [Failure] Backup chiffré échoué** : `tmutil startbackupVolume on disk8s2` → Volume APFS chiffré verrouillé
- [Failure] WebSocket frame payload error** : `received 1007 (invalid frame payload data)` dans `realtime_input.m`
- [Failure] Connexion sécurisée échouée** : "secure connection failed
- [Failure] Home Assistant** : "van à niveau off, cap ne fonctionne pas et en dessous j'ai API key required
- [Failure] VanRoll test** : "ne donne plus de données

### Fréquence des patterns (14 jours)
- **Decision** : 5 jours, 29 occurrences
- **Recurring question** : 5 jours, 15 occurrences
- **Failure** : 4 jours, 18 occurrences
- **Question** : 3 jours, 23 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 23
- Jours d'observation : 7
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**529** recommandations au total — **529** ouvertes — **0** en cours — **0** terminées

⚠️ 499 recommandations ouvertes depuis plus de 7 jours.

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

- OpenRouter   🟢 $17.27 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.27**
