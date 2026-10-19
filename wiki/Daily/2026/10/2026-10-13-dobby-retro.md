---
date: 2026-10-13
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1085
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-13

**Sessions analysées :** 3 | **Échanges :** 1085 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-10-13
## Dobby's Analysis

---

## Décisions prises

1. **Approche relationnelle prioritaire** : D'abord poser des questions polies pour comprendre avant d'agir (contexte : probablement relationnel B2B avec DiaHo/Zheda)

2. **Versionning stratégique** : Travailler uniquement en version française pour les documents commerciaux (Vetalyx)

3. **Infrastructure disque** : Abandonner les solutions logicielles, acheter un SSD 2To minimum (vs. autres approches testées)

4. **Hardware design - facteur forme** : Abandonner les sphères fixables individuellement → approche globale pour éviter de demander aux utilisateurs de manipulations répétitives

5. **Validation procédurale** : Fiches spots finalisées et validées, prêtes pour tests réels "dans quelques jours"

6. **Tests en conditions réelles** : Transition planifiée de simulation vers "live" (timing flou : "je te reviens")

7. **Vetalyx - Structure actionnariale** : Intégration directe du capital chinois à 40% via DiaHo (pas de personnes physiques chinoises en rôles opératifs/management)

---

## Échecs ouverts / bloqueurs

### Critiques (bloquent progression)
- **API Key / Authentification** : "cap ne fonctionne pas" + "API key required" → **pas de resolution documentée**
- **Connexion sécurisée** : "error caused the secure connection to fail" → pas de contexte, pas de solution
- **Volume APFS chiffré/verrouillé** : `tmutil startbackupVolume on disk8s2` échoue sur volume encrypted/locked → commande incorrecte ou processus incomplet
- **HA Bug** : "verifie le bug HA" → rappel mémoïque, pas de détail technique

### Ambigus (clarification nécessaire)
- **Seuil d'endettement Vetalyx** : Fixé à 175.000€, mais "c'est quoi le risque ISC ?" → **métrique de risque non définie**
- **Données manquantes vanroll test** : "pourquoi vanroll test ne donne plus de données ?" → régression ? changement de config ?
- **Fiche vide Dante** : "la fiche est vide. analyse le pourquoi" → correction globale nécessaire ou cas isolé ?

### Hardware incomplet
- **Lupo hardware** : "reporté au 31 aout" (date du passé?), SD endurance + silent blocs RPi en attente

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Récurrence | Implication |
|----------|-----------|-------------|
| "C'est quoi L(M) ?" | 1+ mention | Notation technique non documentée pour le projet van/M5 |
| "C'est quoi les 3 fiches needs_review ?" | 2x | Métadonnée de workflow pas clairement liée au contexte |
| "La synthese de lecture propre c'est quoi ?" | 2x | Terme métier/interne non expliqué → **doc MEMORY insuffisante** |
| "C'est quoi les state files ?" | 1x | Configuration HA/Lupo non documentée |
| "C'est quoi le ZH ?" | 1x | Sigle non défini (Zigbee Hub ? Zone Home ?) |
| "Quelle est la différence lupo/assiette vs esneux/iphone ?" | 1x | Architecture d'instances HA confuse → **besoin schéma d'infra** |
| "C'est quoi le kit hardwire ?" | 1x | Composant/projet mal nommé ou mal indexé |
| "TTL 24h — comment utiliser avec fluidité HTML ?" | 1x | Implémentation technique fragmentée |
| "Pourquoi les dimensions du tiroir 25-26cm ?" | 2x | Constraint mécanique expliquée mais oubliée → **doc vanlife insuffisante** |

**Pattern dominant** : Questions qui reviennent = **absence de documentation centralisée** ou doc de trop mauvaise qualité pour être retrouvée.

---

## Nouveaux patterns détectés

### 1. **Oscillation décision / simulation / live**
JCH dit "on va faire des simulations" puis "on va tester en live" puis "revenez quand c'est fait" → **pas de milestone clair, testing ad-hoc**. Timing estimé : "dans quelques jours" (vague).

### 2. **Multi-contexte sans isolation**
**Dans une même session** : vetalyx (finance/légal belgique), van/lupo (hardware CAO), home assistant (infra IoT), wildlens/wildnexus (vision?), dossiers voyage Ombrie → **context switching coûteux**, risque de confusion actionnariale ↔ dimensionnement tiroir.

### 3. **Décisions polies mais non tracées**
"D'abord poser des questions polies" = bonne pratique relationnelle, mais **aucune trace des réponses attendues ou de qui demande quoi à qui** (DiaHo ? Zheda ? UCM ?).

### 4. **Dobby travaille sans expert**
**Question directe** : "explique moi pourquoi dobby travaille sans s'appuyer sur les experts. sont ils inutiles ou dobby préf[ere] ?" 
→ **Rôles d'équipe flous** (Trace, Jade, Renard mentionnés 6x chacun, mais peu visible dans actions).

### 5. **Chaîne de correction procédurale cassée**
"Verifie le bug HA → cherche la cause → améliore la procedure" → **pas de feedback loop documentée** après fix.

---

## Efficacités / inefficacités

### ✅ Efficace
- **Usage des outils** : DeepSeek CLI + Claude Code utilisés correctement pour recherche fichiers, exécution shell, lecture contexte
- **Décisions binaires rapides** : "on laisse tomber" → action immédiate sans regret (SSD example)
- **Fiches de spécification** : Workflow "spots → validation → live" semble éprouvé pour hardware

### ❌ Inefficace
- **Transitions oubliées** : Décisions prises ("P2 on va attendre position des autres") mais jamais revues → dead letters
- **Contextes non isolés** : Même session mélange Belgique/légal + CAO/van + infra IoT → fatigue cognitive, erreurs cross-project
- **Feedback loop HS** : "je te reviens" = fin de session, pas de suivi tracé → regrets oubliés à la prochaine session
- **Clarification retardée** : "c'est quoi le ZH ?" demandé mais réponse non fournie → continue sans comprendre
- **Dobby seul** : Experts (Trace, Jade, Renard) peu visibles → délégation non-optimale ou désaccord non-surfacé

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Décisions critiques actives
1. **Vetalyx** 
   - Capital 10.000€, DiaHo 40%, structure chinoise sans opératifs locaux
   - À faire : fixer année fiscale + directors avant envoi
   - Risque ISC à 175k€ = **métrique flou, clarifier**
   - UCM belge a répondu sur déclaration actionnaires → vérifier conformité

2. **Lupo vanlife**
   - Meuble banquette 104×55×25cm, 3 tiroirs, trappe 180° basculante
   - Dimensionnement 25-26cm = contrainte banquette passager restant en place
   - **Hard stop 31 aout** (?) pour hardware : SD endurance + silent blocs RPi
   - Tests hardware imminents ("quelques jours")

3. **HA / Infra IoT**
   - Bug HA non résolu : état à confirmer
   - vanroll test : données manquantes depuis X → régression
   - Instances lupo/assiette vs esneux/iphone = architecture confuse

### Lacunes documentaires urgentes
- **MEMORY.md** : ajouter définitions : L(M), ZH, kit hardwire, synthese_lecture_propre, state_files
- **Infra HA** : créer schéma instances + différences assiette/esneux/iphone
- **Van CAO specs** : doc constraints mécaniques (25-26cm → banquette)
- **Workflow validation** : tracer "needs_review → fiches → live" avec responsables
- **Vetalyx financier** : documenter risques ISC, seuils d'alerte

### Bascules en suspens
- P2 : attendre position des autres → **sur qui ? à quelle deadline ?**
- Procedure spots : tests en live → date précise ?
- Fiche Dante vide : correction globale ou isolée ?

---

## Recommandations

### 🎯 Immédiat (avant prochaine session)
1. **Isoler les contextes** 
   - Créer 3 sessions distinctes : Vetalyx (légal/financier), Van (CAO/hardware), HA (infra)
   - Éviter mix dans même conversation → cognitive load ↓, décisions meilleures

2. **Documenter les définitions floues**
   ```markdown
   # GLOSSAIRE SESSION 2026-10-13
   - L(M) : [définition JCH]
   - ZH : [définition JCH]
   - Kit hardwire : [définition JCH]
   - Synthese lecture propre : [définition JCH]
   - State files (HA) : [définition JCH]
   - ISC risk 175k : [métrique exacte et formule]
   ```
   → Ajouter à MEMORY.md avant fin session +1

3. **Clarifier les rôles d'experts**
   - **Question directe à JCH** : Pourquoi Dobby travaille seul ? (Trace, Jade, Renard pourraient-ils prendre 20% de la charge ?)
   - Documenter : "Trace = ? | Jade = ? | Renard = ?"

### 📋 Court terme (1-2 sessions)
4. **Tracer les "P2" et "je te reviens"**
   - Créer section "SUSPENDS" dans MEMORY avec deadline explicite
   - Exemple: `[P2] Attendre position [QUI?] sur [SUJET?] → deadline [DATE]`

5. **Valider les blockers**
   - API Key + cap error : 30min diagnostic avec DeepSeek (logs? config?)
   - HA bug : 1 session dédiée HA, isolée
   - vanroll data : vérifier git history, config changes

6. **Documenter Vetalyx financier**
   - Créer: `Vetalyx/STRUCTURE_ACTIONNARIALE.md` avec UCM response, risques, timeline
   - Risque ISC 175k = seuil de quoi exactement ? → clarifier formule

7. **Milestone explicite van**
   - "Tests hardware imminents" → date précise (31 aout ?)
   - Checklist pré-live : quelle est-elle ?

### 🏗️ Moyen terme (après stabilisation)
8. **Refactoriser MEMORY.md**
   - Actuellement : trop

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 20
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 20
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

- [Decision] : D'abord poser des questions polies pour comprendre avant d'agir (contexte : probablement relationnel B2B avec DiaHo/Zheda)
- [Decision] : Travailler uniquement en version française pour les documents commerciaux (Vetalyx)
- [Decision] : Abandonner les solutions logicielles, acheter un SSD 2To minimum (vs. autres approches testées)
- [Decision] facteur forme** : Abandonner les sphères fixables individuellement → approche globale pour éviter de demander aux utilisateurs de manipulations répéti
- [Decision] : Fiches spots finalisées et validées, prêtes pour tests réels "dans quelques jours
- [Decision] : Transition planifiée de simulation vers "live" (timing flou : "je te reviens")
- [Decision] Structure actionnariale** : Intégration directe du capital chinois à 40% via DiaHo (pas de personnes physiques chinoises en rôles opératifs/management
- [Decision] Approche relationnelle prioritaire** : D'abord poser des questions polies pour comprendre avant d'agir (contexte : probablement relationnel B2B avec D
- [Decision] Versionning stratégique** : Travailler uniquement en version française pour les documents commerciaux (Vetalyx)
- [Decision] Infrastructure disque** : Abandonner les solutions logicielles, acheter un SSD 2To minimum (vs. autres approches testées)
- [Decision] Hardware design - facteur forme** : Abandonner les sphères fixables individuellement → approche globale pour éviter de demander aux utilisateurs de ma
- [Decision] Validation procédurale** : Fiches spots finalisées et validées, prêtes pour tests réels "dans quelques jours
- [Decision] Tests en conditions réelles** : Transition planifiée de simulation vers "live" (timing flou : "je te reviens")
- [Decision] Vetalyx - Structure actionnariale** : Intégration directe du capital chinois à 40% via DiaHo (pas de personnes physiques chinoises en rôles opératifs/
- [Failure] API Key / Authentification** : "cap ne fonctionne pas" + "API key required" → **pas de resolution documentée
- [Failure] Connexion sécurisée** : "error caused the secure connection to fail" → pas de contexte, pas de solution
- [Failure] Volume APFS chiffré/verrouillé** : `tmutil startbackupVolume on disk8s2` échoue sur volume encrypted/locked → commande incorrecte ou processus incompl
- [Failure] HA Bug** : "verifie le bug HA" → rappel mémoïque, pas de détail technique

### Fréquence des patterns (14 jours)
- **Decision** : 6 jours, 29 occurrences
- **Failure** : 5 jours, 17 occurrences
- **Question** : 5 jours, 21 occurrences
- **Recurring question** : 5 jours, 14 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 18
- Jours d'observation : 7
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**485** recommandations au total — **485** ouvertes — **0** en cours — **0** terminées

⚠️ 460 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 438
- **Forge** : 33
- **Furet** : 7
- **Corbeau** : 5
- **Renard** : 1
- **Sybil** : 1

### Plus récentes ouvertes

- [id=473] (2026-10-13) **Dobby** : Isoler les contextes
- [id=474] (2026-10-13) **Renard** : Créer 3 sessions distinctes : Vetalyx (légal/financier), Van (CAO/hardware), HA 
- [id=475] (2026-10-13) **Dobby** : Éviter mix dans même conversation → cognitive load ↓, décisions meilleures
- [id=476] (2026-10-13) **Dobby** : Documenter les définitions floues
- [id=477] (2026-10-13) **Dobby** : L(M) : [définition JCH

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
