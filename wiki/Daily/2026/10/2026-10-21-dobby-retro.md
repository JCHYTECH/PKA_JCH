---
date: 2026-10-21
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1099
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-21

**Sessions analysées :** 3 | **Échanges :** 1099 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-10-21
## Jean-Claude Havaux × Assistants IA

---

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| Traiter les screenshots dans `inbox/sites` | Triage de contenu visuel | À documenter |
| Utiliser exclusivement la version française | Standardisation linguistique | Confirmé |
| Acheter un SSD 2To minimum | Infrastructure locale | Décision d'équipement |
| Discuter avec Alain Bosseloir (partenaire) | Escalade externe | En attente feedback |
| Procédure de fiches spots pour stationnement | Nouveau workflow | À formaliser |
| Ajouter tiroirs aux caissons (coulisse standard) | Design de meuble | Spécification technique |
| Rester en "12" pour procurement | Standardisation de composants | Décision logistique |
| Test en live du système | Passage en production | À planifier |

**Problème identifié** : Aucune de ces décisions n'est tracée dans un registre de décisions (ADR/decision log). Les raisons justificatives sont absentes. Impossible de faire une rétro sur les hypothèses.

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent avancement)

1. **Bug HA non résolu**
   - Message d'erreur : `API key required` + état "off" → "CAP ne fonctionne pas"
   - **Cause inconnue** : À vérifier
   - **Impact** : La session entière a pivoté pour enquêter

2. **Erreur WebSocket realtime_input**
   - `received 1007 (invalid frame payload data)` dans realtime_input.m
   - **Contexte** : Intégration IA temps réel
   - **Non résolu**, non escaladé

3. **Montage de volume APFS échoué**
   - `tmutil startbackupVolume on disk8s2 failed to mountThis is an encrypted and locked APFS Volume`
   - **Impact** : Backup système bloqué
   - **Action prise** : Aucune (noter : décision SSD 2To liée?)

4. **Erreur 403 Access Blocked**
   - Requête refusée sur endpoint HA
   - **Contexte** : Orchestration de configuration ou API externe

5. **Erreur SSL/TLS**
   - `secure connection ro fail` [sic]
   - **Absence de trace** : Pas d'URL, pas de certificat impliqué

### Mineurs / À clarifier

- Question sur risque ISC avec seuil d'endettement à 175k€ (VetaLyx) → pas de réponse documentée
- Recherche sur l'Ombrie (lieux exotiques/peu visités) → contexte absent du transcript

**Point critique** : Aucun de ces bloqueurs n'a de ticket, pas de priorité, pas de responsable assigné.

---

## Questions récurrentes (signe de lacune documentaire)

### Lacunes majeures identifiées

| Question | Fréquence | Implication |
|----------|-----------|------------|
| "C'est quoi les states files ?" | 1× min | Concept clé non documenté (LUPO?) |
| "Quelle est la différence entre LUPO/assiette et ESNEUX/iPhone ?" | 1× min | Architecture HA non formalisée |
| "C'est quoi Warn Invalid request (400)?" | Répétée | Logs d'erreur non interprétés |
| "C'est quoi L(M) ?" | 1× min | Notation technique non explicitée |
| "C'est quoi le kit hardwire ?" | 1× min | Spécification hardware manquante |
| "Pourquoi 25-26 cm pour le tiroir ?" | 1× min | Ratios de design non justifiés par écrit |
| "C'est quoi le ZH ?" | 1× min | Acronyme non défini |
| "C'est quoi la synthèse de lecture propre ?" | 1× min | Processus de documentation absent |
| "C'est quoi les 3 fiches needs_review ?" | 1× min | Workflow de validation opaque |

### Root cause

**Absence d'une wiki/glossaire/FAQ**. JCH pose des questions déjà répondues ailleurs, ou les assistants répètent sans référencer une source canonique.

---

## Nouveaux patterns détectés

### 1. **Alternance d'univers de travail sans contexte clair**
   - Sessions mélangent VetaLyx (legal/finance Belgique), WildNexus (IoT/simulation), infrastructure locale (backup, SSD, HA)
   - **Aucun signalement explicite du changement de contexte**
   - Les assistants doivent inférer du contenu ; risque de cross-contamination

### 2. **Deepseek TUI génère des `<turn_meta>` répétitifs sans exploitation**
   - Même "Repo Working Set" dupliqué 5 fois dans le transcript
   - **Efet** : Bruit, consommation de tokens, pas d'action produite
   - Suggère une boucle de diagnostic inutile

### 3. **Requêtes de recherche / exploration sans hypothèse**
   - Ex : "Ombrie : lieux exotiques/peu visités, fais une recherche"
   - Pas de use case explicitée (pourquoi Ombrie? WildNexus? VetaLyx? Loisir?)
   - **Pattern** : JCH utilise les assistants comme moteur de recherche, pas comme sparring-partner

### 4. **Décisions partiales ("on va", "je vais")**
   - Formulations au futur sans deadline, sans success criteria
   - "on va tester en life et je te reviens" → aucun checkpoint
   - **Aucun suivi de l'exécution**

### 5. **Escalade informelle**
   - "Je vais en discuter avec Alain" → pas de feuille de route, pas de retour prévu
   - Parallèlement, Dobby continue sans attendre

### 6. **Configuration instance HA fragmentée**
   - Plusieurs états mentionnés : "van à niveau off", "CAP ne fonctionne pas", "API key required"
   - **Pas de vue d'état global** ⇒ corriger une chose casse une autre

---

## Efficacités / inefficacités

### ⚡ Efficacités

- **Rapidité de pivot** : JCH bascule entre projets sans perdre le fil
- **Utilisation multi-outil** : DeepSeek + Claude + CLI shell (approprié pour le contexte)
- **Tracabilité d'intention** : Patterns locaux extraits correctement par Dobby
- **Volumétrie** : 1048 messages utilisateur en 3 sessions = rythme soutenu, focus maintenu

### ⚠️ Inefficacités majeures

1. **Token waste via redondance**
   - `<turn_meta>` dupliqué 5× = ~200-300 tokens perdus
   - Aucun post-processing de logs pour éliminer le bruit
   - **Coût/session** : ~10% de surcharge

2. **Pas de mémoire structurée entre sessions**
   - Chaque session repart zéro sur le context (JCH doit rejouer les infos)
   - Questions déjà posées réapparaissent (ex : "states files")
   - **Inefficacité cumulative** : T²

3. **Diagnostic sans conclusion**
   - Bug HA vérifié 3+ fois, aucune root cause hypothesis documentée
   - "Vérifie le bug HA" → 10 échanges → "ok on reste en 12" (pivot sans résolution)

4. **Absence de checklist**
   - Décisions sans conditions d'acceptation
   - Test en live sans plan de rollback
   - **Risque** : échecs silencieux

5. **Demandes d'assistance vagues**
   - "explique moi pourquoi dobby travaille sans s'appuyer sur les experts"
   - **Aucune réponse tracée** ; question récurrente qui signale une friction non résorbée

6. **Oublis de contexte**
   - Recherche Ombrie lancée sans use case ⇒ assistants doivent deviner
   - Design meuble (tiroir 25-26cm) avec justification in-line, pas en spec

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Contexte stratégique

- **VetaLyx (Belgique)** : Capital 10k€, actionnaire chinois (DIaho) 40%, structure sans ressortissants chinois opératifs. Questions légales en cours : déclaration obligatoire? Fiscal?
- **WildNexus** : Simulation, engineering P0, problèmes WebSocket realtime_input
- **Infrastructure JCH** : M5 (machine locale), RPI, HA instable (API key, CAP off), backup APFS gelé, SSD 2To à acheter
- **Partenaires clés** : Alain Bosseloir (discussion prévue), UCM Belgique (avis reçu sur DIaho)

### Bloqueurs persistants à checker d'office

1. HA API key + CAP state (avant prochain test live)
2. Backup APFS/tmutil (infrastructure critique)
3. WebSocket 1007 errors (realtime_input.m)
4. 3 fiches needs_review (quel statut?)

### Decisions en attente de feedback

- Achat SSD 2To (décision coût/planning?)
- Discussion Alain Bosseloir (quand? Agenda?)
- Test live du système (date prévue?)
- Design tiroir (approuvé ou itération?)

### Vocabulaire interne à standardiser

- **states files** (LUPO?)
- **LUPO vs ESNEUX/iPhone** (architecture HA)
- **L(M)** (notation technique?)
- **kit hardwire** (specs?)
- **ZH** (?)
- **needs_review** (workflow validation)

---

## Recommandations

### 🔴 URGENT (Avant prochaine session)

1. **Créer un Decision Log** (format ADR simple)
   - Template : `[date] Décision: X | Contexte: Y | Hypotèse: Z | Owner: | Deadline: | Status:`
   - Rétro-remplir les 8 décisions de cette session
   - Lier à chaque décision son bloqueur/risque

2. **Résoudre ou documenter les 5 bugs critiques**
   - Créer 1 ticket par erreur : `HA_API_KEY_CAP_OFF`, `WEBSOCKET_1007`, `APFS_MOUNT_FAIL`, etc.
   - Root cause analysis obligatoire (ou "Not reproducible", pas de silence)
   - Assign owner + deadline

3. **Créer une Wiki interne : Glossaire + Architecture**
   - Minimum 20 entrées (states files, L(M), kit hardwire, ZH, CAP, needs_review, etc.)
   - Diagramme HA (LUPO vs ESNEUX vs iPhone)
   - Specs design meuble (pourquoi 25-26cm?)

### 🟡 IMPORTANT (Plan sur 1-2 semaines)

4. **Structurer les sessions

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 23
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 23
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

- [Decision] : Aucune de ces décisions n'est tracée dans un registre de décisions (ADR/decision log). Les raisons justificatives sont absentes. Impossible de faire
- [Failure] Message d'erreur : `API key required` + état "off" → "CAP ne fonctionne pas
- [Failure] Cause inconnue** : À vérifier
- [Failure] Impact** : La session entière a pivoté pour enquêter
- [Failure] `received 1007 (invalid frame payload data)` dans realtime_input.m
- [Failure] Contexte** : Intégration IA temps réel
- [Failure] Non résolu**, non escaladé
- [Failure] `tmutil startbackupVolume on disk8s2 failed to mountThis is an encrypted and locked APFS Volume`
- [Failure] Impact** : Backup système bloqué
- [Failure] Action prise** : Aucune (noter : décision SSD 2To liée?)
- [Failure] Requête refusée sur endpoint HA
- [Failure] Contexte** : Orchestration de configuration ou API externe
- [Failure] `secure connection ro fail` [sic]
- [Failure] Absence de trace** : Pas d'URL, pas de certificat impliqué
- [Failure] Erreur WebSocket realtime_input
- [Failure] Montage de volume APFS échoué

### Fréquence des patterns (14 jours)
- **Decision** : 4 jours, 26 occurrences
- **Failure** : 3 jours, 13 occurrences
- **Recurring question** : 3 jours, 12 occurrences
- **Question** : 2 jours, 21 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 16
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**514** recommandations au total — **514** ouvertes — **0** en cours — **0** terminées

⚠️ 485 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 461
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 6
- **Renard** : 3
- **Sybil** : 2

### Plus récentes ouvertes

- [id=503] (2026-10-21) **Dobby** : Créer un Decision Log** (format ADR simple)
- [id=504] (2026-10-21) **Dobby** : Template : `[date] Décision: X | Contexte: Y | Hypotèse: Z | Owner: | Deadline: 
- [id=505] (2026-10-21) **Dobby** : Rétro-remplir les 8 décisions de cette session
- [id=506] (2026-10-21) **Dobby** : Lier à chaque décision son bloqueur/risque
- [id=507] (2026-10-21) **Dobby** : Résoudre ou documenter les 5 bugs critiques

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.35 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.35**
