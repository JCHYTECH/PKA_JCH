---
date: 2026-10-08
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1079
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-08

**Sessions analysées :** 3 | **Échanges :** 1079 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA - 2026-10-08

## Décisions prises

### Validées et clôturées
- **Vetalyx - Contrats légaux** : Fiches validées, adaptations contractuelles demandées (Articles 23, 33)
- **Infrastructure IoT-Van** : Décision d'acheter SSD 2To minimum (abandon de la solution alternative)
- **Lupo Hardware** : Installation Bluetti 100 V2 + charger v2 confirmée
- **Projet IoT-Van** : Décision de revenir au projet avec simulations en attente
- **Home Assistant** : "Bon travail" → passage en phase de test live annoncé

### Non finalisées
- **Vetalyx Belgique - Actionnariat chinois** : Question ouverte sur l'obligation de déclaration des actionnaires chinois (DiaHo 40% du capital)
  - Contexte : Capital 10.000€, pas de gestion opérationnelle chinoise
  - UCM Belgique consulté, réponse incomplète dans le transcript

---

## Échecs ouverts / bloqueurs

### Critiques
1. **macOS Backup (tmutil)** : `tmutil startbackupVolume on disk8s2` échoue
   - Raison : APFS Volume encrypté et verrouillé
   - Impact : Stratégie de sauvegarde compromise
   - **Status** : Non résolu

2. **Home Assistant - Van API** : 
   - Van en statut "off", CAP ne fonctionne pas
   - Erreur "API key required" en cascade
   - Impact : IoT-Van bloqué en production
   - **Status** : En investigation ("verifie le bug HA")

3. **Sécurité TLS** : "SSL error caused the secure connection to fail"
   - Contexte manquant, projet flou
   - **Status** : Non contextualisé

### Secondaires
- **Lupo Hardware** : Trois éléments en attente :
  - SD Endurance
  - Silent blocs sur RPI
  - **Status** : Configuration mineure, pas blocant

- **Risque ISC financier** : Seuil d'endettement Vetalyx à 175.000€
  - Question : C'est quoi le risque ISC ?
  - **Status** : Pas de réponse dans le transcript

---

## Questions récurrentes (signes de lacunes documentaires)

### Architecture / Configuration
- **"C'est quoi le ZH ?"** → Jamais défini/expliqué
- **"L(M) c'est quoi ?"** → Notation non documentée
- **"C'est quoi le kit hardwire ?"** → Terminologie floue
- **"State files" (Lupo)** → Non défini
- **"Les 3 fiches needs_review"** → ID manquant, processus unclear

### Procédures / Workflows
- **"Comment utiliser TTL 24h avec fluidité en HTML ?"** → Pas de pattern établi
- **"Comment garder en mémoire les procédures pour lancer via nom ?"** → Système de nommage/tagging absent ou défaillant
- **Dimension du tiroir 25-26cm** → Logique métier non documentée (pourquoi ce chiffre exactement ?)
- **"4 roues vs autre plus petit, avant/arrière"** → Classification vehicule non clarifiée

### Répétitions exactes (pattern pathologique)
```
- "oui tu ajoutes et tu verifie pourquoi vanroll test ne donne plus de données" (×2)
- Diagnostic des fiches vides (Dante) vs. correctif global (×2)
```
→ **Problème** : Même enquête lancée deux fois = inefficacité de tracking

---

## Nouveaux patterns détectés

### 1. **Mode "verification loop"**
JCH pose beaucoup de questions de vérification après chaque action :
- "verifie le bug HA"
- "analyse le pourquoi pour savoir si c'est exceptionnel ou correctif global"
- "checke pourquoi ce blocage"

→ **Interprétation** : Manque de confiance dans les rapports initiaux OU absence de système de vérification préalable = double travail

### 2. **Contextualisation fragmentée**
Les extraits du transcript sont très découpés :
- Contrats Vetalyx sur 3 sessions
- Problèmes IoT distribués (HA, Van, vanroll)
- Fiches cliniques parallèles à la logistique Lupo

→ **Interprétation** : Multi-tasking intensif = risque d'incohérence cross-projet

### 3. **Demandes floues d'info**
Beaucoup de "donne moi info" sans contexte clair :
- Pas de format spécifié
- Pas de scope défini
- Résultats probablement génériques

### 4. **Gestion d'inbox reactive**
- "il y a des dots dans inbox"
- "comment faire en sorte que tu gardes en mémoire"
- → Système de priorité/triage absent

---

## Efficacités / Inefficacités

### ✅ Efficacités détectées
1. **Décisions rapides et claires** : "non on laisse tomber. je vais acheter un SSD" → action immédiate
2. **Validation progressive** : Fiches validées progressivement, pas bloquage en masse
3. **Outils diversifiés** : DeepSeek (v4, v4-pro) + Claude en parallèle = couverture multi-modèles
4. **Escalade claire** : UCM consulté pour question juridique → bonne pratique

### ❌ Inefficacités critiques
1. **Pas de glossaire/lexique** → Perte temps sur définitions (ZH, L(M), etc.)
2. **Questions repetitives** → Même enquête lancée ×2 (vanroll, fiches vides)
3. **Backup en panne** → Zéro stratégie documentée pour APFS chiffré
4. **Contextualisation manquante** : "SSL error" sans projet associé
5. **TTL/HTML integration** → Jamais expliqué = questions futurs probables
6. **Notation dimensionelle floue** : "25-26cm" sans WHY documenté

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Projets actifs et leurs states
| Projet | Status | Prochaine action | Blocker |
|--------|--------|------------------|---------|
| **Vetalyx** | En cours contrats | Adapter Articles 23/33 ; Clarifier actionnariat chinois | Déclaration DiaHo? |
| **IoT-Van** | Réactivé + simulations | Tester en live | HA API key (van=off) |
| **Home Assistant** | Tests live annoncés | Vérifier bug CA/API | API key required |
| **Lupo Hardware** | 95% terminé | Ajouter SD + silent blocs | Minor |

### Informations critiques non clarifiées
- **ISC risk threshold** : 175.000€ endettement Vetalyx = quel risque exactement ?
- **SSL error context** : Quel projet/service ? Est-ce production ?
- **TTL 24h pattern** : Comment implémenter en HTML avec fluidité ?
- **File naming system** : Pourquoi "needs_review" sur 3 fiches ? Quel processus ?

### Entités clés à tracker
- **Membres** : Jade, Renard, Trace (rôles non définis dans transcript)
- **Machines** : M5, RPI - IP/credentials dans JCH_PRIVATE/credentials-central.md
- **Infrastructure** : Mosquitto, TailScale (réseau IoT)

---

## Recommandations

### 🔴 URGENT (semaine prochaine)
1. **Créer un GLOSSAIRE.md** : Définir ZH, L(M), ISC, kit hardwire, state files, needs_review workflow
   - Format : Terme | Contexte projet | Définition | Exemple
   - Objectif : Réduire questions de clarification de 70%

2. **Résoudre le backup APFS**
   - Rechercher : Alternative à tmutil (ex: Time Machine GUI, Migration Assistant)
   - Documenter : Procédure pour volumes chiffrés
   - Tester : Sur M5 avant mise en prod

3. **Déboguer HA van/API key**
   - Reproduire : Van=off + CAP=fail → stacktrace complet
   - Isoler : Est-ce HA ou integration externe ?
   - Documenter : Fix dans TEAM_Inbox/03_PROJECTS/11_IOT/BUGS.md

### 🟡 PRIORITÉ HAUTE (2-3 semaines)
4. **Clarifier Vetalyx actionnariat**
   - Action : Relancer UCM Belgique avec question précise : "Est-il obligatoire de déclarer DiaHo comme actionnaire ? Conformité fiscale ?"
   - Documenter : Réponse dans JCH_Inbox/03_PROJECTS/08_VETALYX/legal/

5. **Implémenter system de tagging pour procédures**
   - Créer : Tag index (ex: `@proc:ttl-html`, `@proc:vanroll-debug`)
   - Documenter : Whichproc pour chaque pattern récurrent
   - Intégrer : Dans prompt système d'IA ("Tu peux lancer @proc:X")

6. **Consolidation des "fiches vides"**
   - Audit : Dante fiche vide = bug systémique ou cas exceptionnel ?
   - If systémique → Fix template global
   - If exceptionnel → Documenter pourquoi
   - Décision à valider avant prochaine session

### 🟢 MAINTENANCE (mensuel)
7. **Retro bi-hebdo** : Sessions de 45min max pour éviter accumulation questions floues
8. **Inbox triage** : Protocole clair pour mails/Telegram → déduplication action
9. **Versioning contrats** : Vetalyx v5 attendue → numéroter clairement avant chaque cycle

---

## Signature
**Dobby** | 2026-10-08 | Pattern analysis v1.2

**À faire avant 2026-10-15** : ✓ GLOSSAIRE | ✓ Backup APFS fix | ✓ HA debug stacktrace

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 27
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 24
- **Taux : 11.1%**

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

- [Decision] Vetalyx - Contrats légaux** : Fiches validées, adaptations contractuelles demandées (Articles 23, 33)
- [Decision] Infrastructure IoT-Van** : Décision d'acheter SSD 2To minimum (abandon de la solution alternative)
- [Decision] Lupo Hardware** : Installation Bluetti 100 V2 + charger v2 confirmée
- [Decision] Projet IoT-Van** : Décision de revenir au projet avec simulations en attente
- [Decision] Home Assistant** : "Bon travail" → passage en phase de test live annoncé
- [Failure] : `tmutil startbackupVolume on disk8s2` échoue
- [Failure] Raison : APFS Volume encrypté et verrouillé
- [Failure] Impact : Stratégie de sauvegarde compromise
- [Failure] Status** : Non résolu
- [Failure] Van en statut "off", CAP ne fonctionne pas
- [Failure] Erreur "API key required" en cascade
- [Failure] Impact : IoT-Van bloqué en production
- [Failure] Status** : En investigation ("verifie le bug HA")
- [Failure] : "SSL error caused the secure connection to fail
- [Failure] Contexte manquant, projet flou
- [Failure] Status** : Non contextualisé
- [Failure] macOS Backup (tmutil)** : `tmutil startbackupVolume on disk8s2` échoue
- [Failure] Home Assistant - Van API** :
- [Failure] Sécurité TLS** : "SSL error caused the secure connection to fail

### Fréquence des patterns (14 jours)
- **Recurring question** : 8 jours, 18 occurrences
- **Decision** : 7 jours, 33 occurrences
- **Failure** : 7 jours, 19 occurrences
- **Question** : 6 jours, 23 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 19
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**472** recommandations au total — **472** ouvertes — **0** en cours — **0** terminées

⚠️ 449 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 426
- **Forge** : 33
- **Furet** : 7
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=462] (2026-10-08) **Dobby** : Créer un GLOSSAIRE.md** : Définir ZH, L(M), ISC, kit hardwire, state files, need
- [id=463] (2026-10-08) **Dobby** : Format : Terme | Contexte projet | Définition | Exemple
- [id=464] (2026-10-08) **Dobby** : Objectif : Réduire questions de clarification de 70%
- [id=465] (2026-10-08) **Dobby** : Résoudre le backup APFS
- [id=466] (2026-10-08) **Furet** : Rechercher : Alternative à tmutil (ex: Time Machine GUI, Migration Assistant)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
