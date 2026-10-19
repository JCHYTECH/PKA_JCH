---
date: 2026-10-06
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1182
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-06

**Sessions analysées :** 3 | **Échanges :** 1182 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE PKA - 2026-10-06

## Décisions prises

### Confirmées et documentées
- **Vetalyx (structure légale)** : Capital à 10.000€, DiaHo entre directement à 40% (pas de personne physique chinoise en opérationnel/management). Demande d'avis UCM confirmée.
- **Contrats Vetalyx/DiaHo** : Adaptation des articles 23 (année fiscale) et 33 (designation des directors) avant envoi. Consolidation v4 en cours.
- **Infrastructure M5/RPI** : Lupo reporté au 31 août. Reste à faire : SD endurance + silent blocs sur RPI.
- **Gestion fichiers** : Passer les drafts en validés prioritairement. Traitement screenshots inbox/sites par batch de 10.

### Implicites / mal formalisées
- **Acquisition matériel** : "Non on laisse tomber, je vais acheter un SSD 2To minimum" → **Pas de tracking de cette décision, pas de budget assigné, pas de deadline**.
- **Simulations**: "On va faire des simulations et je te reviens" → **État suspensif flou, pas de critères de validation définis**.
- **Factor form** : "Mal : facteur form une sphere parce qu'on va pas demander au gens de les fixer une à une" → **Décision conceptuelle non documentée**, raison métier floue.

---

## Échecs ouverts / bloqueurs

### Critiques
1. **API Key / Home Assistant config**
   - Van au niveau OFF, CAP ne fonctionne pas
   - "En dessous j'ai API key required"
   - **Statut** : "Vérifiez le bug HA" → **pas d'assignation, pas de deadline**

2. **Connexion sécurisée échouée**
   - "Secure connection to fail" sur flux réseau
   - **Cause inconnue**, **impact sur quel système unclear**

3. **Backup APFS / tmutil**
   - `tmutil startbackupVolume on disk8s2` → Encrypted and locked APFS Volume
   - **Bloqueur pour maintenance M5** (données?)

4. **Google Credentials vanroll**
   - Username/password Google Keyword ne fonctionnent pas
   - **Vanroll test ne donne plus de données** → regression?
   - **Action demandée** : "Tu ajoutes et tu vérifie pourquoi" → **non assignée clairement**

5. **Fiches vides (Dante)**
   - "Fiche Dante vide. Analyse le pourquoi pour savoir si c'est exceptionnel ou si correctif global nécessaire"
   - **3 fiches needs_review** → pas listées, pas priorisées

6. **Fichiers de states / Lupo**
   - "C'est quoi les states files ?" → **terminologique**, signe de documentation manquante

### Dégradations détectées
- **Facteur 3 d'erreur** sur une métrique non nommée : "Observe l'importance de ton erreur : un facteur 3. Cela peut tuer une decision sur un projet" → **Erreur non isolée, impact métier non quantifié**

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Contexte | Fréquence | Racine probable |
|----------|----------|-----------|-----------------|
| "C'est quoi le kit hardwire ?" | Contexte hardware RPI/Lupo | 2x | Glossaire projet manquant, doc hardware obsolète |
| "C'est quoi le ZH ?" | Context config/params | 1x+ | Acronyme non documenté dans AGENTS.md ou projet |
| "L(M) c'est quoi ?" | Notation dans logs/config | 2x | Convention locale non explicite dans working set |
| "C'est quoi les 3 fiches needs_review ?" | Triage inbox | 2x | Processus de review non formalisé |
| "C'est quoi les states files ?" | Lupo / IoT | 1x | Terminologie HA/Docker non normalisée |
| "Quelle est la différence entre lupo/assiette et esneux/iphone ?" | Instances HA | 1x | Architecture multi-instance non diagramée |
| "C'est quoi la synthèse de lecture propre ?" | Processing docs | 1x | Template/standard non défini |
| "Quel est le risque ISC à 175k€ d'endettement ?" | Vetalyx finances | 1x | Framework d'analyse financière ad-hoc |

**Insight** : 8 questions terminologiques / architecturales en ~1000 messages = **0.8% des échanges** en friction documentaire. Grave pour continuité.

---

## Nouveaux patterns détectés

### 1. **Décisions "jetables" sans trace**
- Mode : "oui on va essayer" → essayer quoi ? critères de succès ? revue quand ?
- Même pattern 3x minimum dans transcript
- **Perte d'institutional memory**

### 2. **Recherche d'information critiques par questions orales**
- IP M5, ports mosquitto, credentails → cherchés via grep/shell au lieu de doc centralisée
- Signale que `JCH_PRIVATE/credentials-central.md` existe mais **n'est pas source de vérité** pour l'équipe

### 3. **Géographie des problèmes non cartographiée**
- "S endroits exotiques ou peu visités mais exceptionnel. Peux tu faire une recherche pour l'Ombrie ?"
- Contexte complètement coupé, impossible de savoir projet/intention
- **Artefact de session fragmentée**

### 4. **Revues de fichiers incohérentes**
- "D'abord les drafts mets les en validés" 
- "Mets-moi le chemin des fichiers encore validés ?"
- Workflow de validation veille/nouvelle pas clarifié

### 5. **Métriques importantes non contextualisées**
- Facteur 3 mentionné comme "peut tuer une decision" mais **pas nommé, pas quantifié, pas lié à un projet**
- Pression iPhone, TTL 24h, endettement 175k€ → **nombres flottants sans modèle explicite**

---

## Efficacités / inefficacités

### ✅ Efficacités observées
1. **Utilisation multi-outils coordonnée** : DeepSeek + Claude + shell/grep workflow fluide
2. **Batch processing discipline** : "Traiter les skip après, batch de 10" → bonne scalabilité
3. **Reférenciation projet** : Vetalyx bien nommé, fichiers versionnés (v4-consolidee), archivés
4. **Escalade légale anticipée** : UCM consulté sur structure DiaHo avant signature
5. **Context awareness** : JCH fourni working set au début de session (AGENTS.md, CLAUDE.md)

### ❌ Inefficacités critiques
1. **Décisions orales non formalisées**
   - Temps perdu : prochaines sessions redemandent des clarifications
   - Coût : "Dobby, c'est quoi le kit hardwire ?" au lieu de lire doc
   - Multiplicateur : 3 sessions, 1182 échanges, 8+ questions répétées

2. **Bloqueurs sans assignation**
   - "Vérifiez le bug HA", "tu ajoutes et tu vérifie" → responsable unclear
   - Pas de deadline → drift de 2+ jours observé (31 août → 6 oct pour Lupo)

3. **Fragmentation documentaire**
   - IP M5 cherchée par grep au lieu de doc centralisée
   - Credentials-central.md existe mais pas consulté (ou outdated?)
   - AGENTS.md n'a pas les glossaires manquants

4. **Triage inbox ad-hoc**
   - "Mets-moi le chemin des fichiers encore validés" → relance manuelle
   - 3 fiches needs_review non listées automatiquement
   - "Ok on va travailler sur les screenshots" → pas de queue formelle

5. **Métriques flottantes**
   - Facteur 3 d'erreur → cause inconnue, impact inévalué
   - "Pression iPhone" → contexte coupé
   - ISC risk 175k€ → pas de framework d'évaluation explicite

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Priorité critique (affecte exécution)
1. **Bug HA : API Key + config CAP/OFF**
   - Bloque Vetalyx IoT downstream
   - Assigné à : ?? (à confirmer)
   - Deadline : jeudi prochain (2026-10-09)?
   
2. **Google Credentials Vanroll**
   - Regression détectée
   - Chercher: changelog Google Keyword auth, comparer avec config backup
   - Assigné à : ?? (à confirmer)

3. **Backup APFS M5 verrouillé**
   - Impacte maintenance infra
   - Solution : déverrouiller ou reconfigurer backup
   - Assigné à : JCH (M5 owner)

4. **Fiches Dante + needs_review triage**
   - 3 fiches non documentées
   - Requiert: audit du schema fichiers, correction globale si pattern
   - Assigné à : Dobby (auto-check)

### 🟡 Priorité moyenne (cesse la friction)
5. **Glossaire projet manquant**
   - Kit hardwire, ZH, L(M), states files → 8 questions répétées
   - Action : créer `JCH_Inbox/03_PROJECTS/GLOSSAIRE.md` avec termes IoT/Vetalyx
   - Assigné à : Dobby (collecte) + Renard/Jade (validation)

6. **Architecture instances HA non diagramée**
   - "Lupo/assiette vs esneux/iphone, c'est l'instance HA ?"
   - Créer : `JCH_Inbox/03_PROJECTS/11_IOT/HA-INSTANCES.md` avec schéma

7. **SSD 2To purchase**
   - Décision prise, pas tracée
   - Créer ticket : budget, fournisseur, deadline livraison
   - Assigné à : JCH (achat)

### 🟢 Priorité basse (bon à savoir)
8. **TTL 24h fluidité HTML**
   - "Comment utiliser cela avec fluidité, par exemple dans un HTML ?" → remise en contexte prochaine session
9. **Facteur 3 d'erreur**
   - À isoler et nommer dans prochaine retrospective si toujours pertinent
10. **Dimensions meuble tiroir**
    - 25-26cm requirement documenté mais pourquoi? (compatibilité banquette)
    - À valider dans specs Lupo final

---

## Recommandations

### 🎯 Court terme (cette semaine)
1. **Créer structure documentaire manquante** (2h)
   ```
   JCH_Inbox/03_PROJECTS/
   ├── GLOSSAIRE.md          (Kit hardwire, ZH, L(M), states files...)
   ├── 11_IOT/HA-INSTANCES.md (Lupo vs 

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 29
- Résolus automatiquement : 6
- Résolus manuellement : 0
- Encore ouverts : 23
- **Taux : 20.7%**

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

- [Decision] Vetalyx (structure légale)** : Capital à 10.000€, DiaHo entre directement à 40% (pas de personne physique chinoise en opérationnel/management). Demand
- [Decision] Contrats Vetalyx/DiaHo** : Adaptation des articles 23 (année fiscale) et 33 (designation des directors) avant envoi. Consolidation v4 en cours.
- [Decision] Infrastructure M5/RPI** : Lupo reporté au 31 août. Reste à faire : SD endurance + silent blocs sur RPI.
- [Decision] Gestion fichiers** : Passer les drafts en validés prioritairement. Traitement screenshots inbox/sites par batch de 10.
- [Failure] Van au niveau OFF, CAP ne fonctionne pas
- [Failure] En dessous j'ai API key required
- [Failure] Statut** : "Vérifiez le bug HA" → **pas d'assignation, pas de deadline
- [Failure] "Secure connection to fail" sur flux réseau
- [Failure] Cause inconnue**, **impact sur quel système unclear
- [Failure] `tmutil startbackupVolume on disk8s2` → Encrypted and locked APFS Volume
- [Failure] Bloqueur pour maintenance M5** (données?)
- [Failure] Username/password Google Keyword ne fonctionnent pas
- [Failure] Vanroll test ne donne plus de données** → regression?
- [Failure] Action demandée** : "Tu ajoutes et tu vérifie pourquoi" → **non assignée clairement
- [Failure] "Fiche Dante vide. Analyse le pourquoi pour savoir si c'est exceptionnel ou si correctif global nécessaire
- [Failure] 3 fiches needs_review** → pas listées, pas priorisées
- [Failure] "C'est quoi les states files ?" → **terminologique**, signe de documentation manquante
- [Failure] API Key / Home Assistant config
- [Failure] Connexion sécurisée échouée
- [Failure] Backup APFS / tmutil
- [Failure] Google Credentials vanroll
- [Failure] Fiches vides (Dante)
- [Failure] Fichiers de states / Lupo

### Fréquence des patterns (14 jours)
- **Failure** : 7 jours, 20 occurrences
- **Recurring question** : 7 jours, 17 occurrences
- **Question** : 6 jours, 22 occurrences
- **Decision** : 5 jours, 31 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 23
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**461** recommandations au total — **461** ouvertes — **0** en cours — **0** terminées

⚠️ 428 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 416
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=461] (2026-10-06) **Dobby** : Créer structure documentaire manquante** (2h)
- [id=456] (2026-10-03) **Dobby** : : Décisions avec conditions implicites ("on va attendre", "je vais essayer")
- [id=457] (2026-10-03) **Dobby** : Quoi** : [Action précise
- [id=458] (2026-10-03) **Dobby** : Condition/Deadline** :
- [id=459] (2026-10-03) **Dobby** : Dépendances** :

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
