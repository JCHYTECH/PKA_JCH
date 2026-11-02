---
date: 2026-10-19
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1199
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-19

**Sessions analysées :** 3 | **Échanges :** 1199 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Sessions 2026-10-19 - Dobby

## Décisions prises

1. **Vetalyx (projet business Belgique)** :
   - Capital fixé à 10 000 EUR
   - Structure actionnariat : DiaHo (chinois) entre à 40% directement au capital, sans personnel opérationnel/management chinois physiquement présent
   - Article 23 : année fiscale à fixer entre associés avant envoi
   - Article 33 : "directors" à désigner avant envoi
   - Contrats commerciaux à adapter suite aux retours UCM Belgique

2. **Vanlife (Lupo Bianco - projet IOT van)** :
   - Meuble banquette multi-tiroirs : 104cm (L) × 55cm (P) × 25cm (H)
   - Configuration : 3 tiroirs ouvrants côté interne + externe via glissières
   - Trappe supérieure avec pivot 180° externe
   - Dimension critique des tiroirs : 25-26cm (contrainte meuble en place avec banquette passager)
   - Reste en 12V (tous composants standardisés pour simplifier procurement)
   - RPI à allumer pour tests réels en quelques jours

3. **Procédures/Process** :
   - Procédure "fiches spots" pour stationnement à créer
   - Traitement des "skip" reporté (batch de 10)
   - Brouillons à valider avant promotion
   - Pattern mémoire à documenter pour lancer via noms de procédures (inbox + Telegram)

4. **Méthodologie** :
   - Arrêt des sessions "en rond" → documentation markdown immédiate
   - Tests en réel planifiés (quelques jours)
   - Simulations avant déploiement

---

## Échecs ouverts / bloqueurs

### Critiques (non résolvables)
1. **Erreur 403 Access Blocked** (×2 occurrences) : contexte flou, pas de service/URL identifiée. Nécessite clarification.
2. **Erreur WebSocket 1007** (realtime_input.m) : payload invalide, cause inconnue, bloque communication temps réel.
3. **tmutil backup failure** (disk8s2) : volume APFS chiffré + verrouillé, dépend d'autorisation macOS.

### Business/Risques
1. **Seuil d'endettement Vetalyx** : JCH mentionne 175 000 EUR mais questionne le "risque ISC" → **gap légal/financier non documenté**. À clarifier avec expert comptable.
2. **Solidité financière de DiaHo** : demande potentielle de documents fiscaux pour démontrer solvabilité avant signature. **Status UCM Belgique incomplet** dans transcript.

### Techniques/Data
1. **vanroll test** : ne retourne plus de données (cause inconnue). À investiguer.
2. **API key missing** (sous-niveau HA) : credentials manquants ou configuration cassée.
3. **HAProxy/reverse proxy** : "cap ne fonctionne pas" à niveau "off" → déploiement incomplet.

### Documentaires
1. **Fiches spots vides** : exemple Dante (fiche vide). Unclear si bug global ou cas exceptionnels → procédure de correction manquante.
2. **States files** : Lupo reporté au 31/08, question "c'est quoi les states files?" sans réponse → concept undefined.

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Récurrences | Implication |
|----------|-------------|------------|
| C'est quoi le ZH ? | 1+ | Acronyme non défini (Zurich? Zone? Système?) |
| L(M) - notation technique ? | 1+ | Notation interne mal documentée |
| Kit hardwire ? | 1 | Composant ou procédure? Contexte vanlife flou |
| States files (Lupo) ? | 1+ | Concept HA/IoT mal expliqué |
| Différence lupo/assiette vs esneux/iphone ? | 1 | Instances HA confuses, mapping non documenté |
| Avant/arrière (4 roues + plus petit) ? | 2+ | **Pattern véhicule Lupo : géométrie/axles non clarifiée** |
| Dimension tiroir 25-26cm pourquoi ? | 2 | Formulé en "pourquoi?" = question pédagogique, pas de doc |
| Fiches needs_review (3 fiches) ? | 1+ | Statut/contenu indéfini |
| "Synthèse de lecture propre" ? | 1 | Jargon maison sans définition |
| vanroll ne donne plus de données ? | 1+ | Service/script/cron? Pas d'investigation approfondie |

**Impact** : Plus de 7 questions sans réponse directe → **documentation interne critique manquante** (wiki ou AGENTS.md incomplet).

---

## Nouveaux patterns détectés

1. **Contexte mélangé (Business + IoT + Vanlife)** :
   - 3 projects majeurs en parallèle (Vetalyx, Wildnexus, Lupo-van-IOT)
   - Pas de séparation claire entre sessions
   - Risque de confusion d'instructions

2. **Débits d'information non structurés** :
   - Décisions verbales (pas de commit/PR)
   - Courtes phrases, code implicite
   - Demandes de clarification → rejet par fatigue ("on va arrêter là, on tourne en rond")

3. **Checklists implicites non finalisées** :
   - "adapte les contrats" (Vetalyx)
   - "valide les drafts"
   - "checke pourquoi ce blocage"
   - **→ Pas d'issue tracker ou TODO.md central**

4. **Dépendances cross-tools non gérées** :
   - DeepSeek + Claude + Codex utilisés en parallèle
   - Chacun maîtrise un contexte subset
   - État global du workspace opaque

5. **Procédures réutilisables non versionnées** :
   - "garder en mémoire les procédures pour lancer via un nom"
   - Actuellement ad-hoc
   - Suggestion (JCH) : système de noms (inbox + Telegram)
   - **→ Pas de registry (PROCEDURES.md?) existant**

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Décisions rapides** : capital Vetalyx, dimensions vanlife définies en une session
- **Context awareness** : assistants savent naviguer workspace multiples (JCH_Inbox, JCH_PRIVATE, TEAM)
- **Tool switching agile** : DeepSeek ↔ Claude sans friction (transitions transparentes)
- **Prototypage physique** : Lupo meuble = specs + test réel = validation complète

### ❌ Inefficacités
1. **Boucles de clarification** : questions "c'est quoi?" répétées = temps perdu
2. **Pas de documentation immédiate** : décisions verbales → oubli/redondance
3. **Erreurs non investigées** : 403, 1007 WebSocket, vanroll mentionnés mais non rootcause
4. **Fatigue décisionnelle** : "on tourne en rond, créé un fichier .md" = abandon de sessions sans closure
5. **Credentials / secrets sprawl** : grep credentials-central.md en contexte multi-tool = risque exposition
6. **Batch de 10 (skip)** : décision de report sans raison documentée
7. **Context switching** : Vetalyx (juridique/finance) → Lupo (meuble) → HA/IoT en même session

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Vetalyx (Business)
- **Capital** : 10 000 EUR
- **Actionnariat** : DiaHo 40% (via société, pas physique)
- **Blockers légaux** : Article 23 (année fiscale), Article 33 (directors)
- **Risque ISC** : seuil 175 000 EUR (À CLARIFIER : sens et origine)
- **Deadline** : UCM Belgique a répondu, attendre signature

### Lupo Bianco Vanlife
- **Meuble banquette** : 104×55×25cm, 3 tiroirs
- **Voltage** : 12V standard (procurement simplifié)
- **RPI** : allumer bientôt pour tests réels
- **Tests** : dans quelques jours en réel
- **Procédure spots** : À créer

### État système
- **Instances HA** : lupo/assiette vs esneux/iphone (mapping flou, À clarifier)
- **Issues ouvertes** :
  - vanroll test (data loss)
  - HAProxy "cap" (off, non fonctionnel)
  - Volume APFS backup (permissions)
  - Erreur 403 (contexte?)
  - WebSocket 1007 (payload)

### Procédures/Mémoire
- **Pattern à documenter** : lancer procédures via noms (inbox + Telegram)
- **Fiches vides** : investiguer si bug global (Dante example)
- **States files** : Lupo, définition manquante

---

## Recommandations

### Immédiat (prochaine session)

1. **Créer PROCEDURES.md** (ou PATTERNS.md)
   - Documenter toute procédure réutilisable
   - Format : `## [NOM] - Description`
   - Linking : inbox → reference procédure
   - Exemple : `PROCEDURE_VANROLL_INSPECT`, `PROCEDURE_FICHES_VALIDATION`

2. **Écrire CLARIFICATIONS.md** pour questions récurrentes
   ```markdown
   ## ZH
   Définition : [À compléter]
   Contexte : [À compléter]
   
   ## L(M)
   Notation : [À compléter]
   ...
   ```

3. **Ouvrir un BLOCKERS.md central**
   - Erreur 403 : contexte? service? URL?
   - WebSocket 1007 : reproduire + logs
   - vanroll : dernière exécution réussie? cron log?
   - HAProxy "cap" : config current + attendue?

4. **Séparer sessions par projet**
   - Session Vetalyx (juridique/finance) ≠ Session Lupo (hardware) ≠ Session Wildnexus (technique)
   - Chacune a sa propre piste d'audit

### Court terme (3-4 sessions)

5. **Documenter Vetalyx finalization**
   - Articles 23, 33 : qui signe quoi? Deadline?
   - ISC risk : sens exact + mitigation
   - DiaHo docs : collectés? vérifiés?

6. **Tests Lupo réels** (planifiés "dans quelques jours")
   - RPI startup → documented outcome
   - Meuble prototype → photos/CAD validation
   - Checklist de tests (dimensions, glissières, trappe)

7. **Mapper instances HA proprement**
   - lupo/assiette ↔ esneux/iphone : qui parle à qui?
   - Créer diagram ou table YAML

8. **Investiguer vanroll regression**
   - Dernière version fonctionnelle?
   - Cron logs? API logs?

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 23
- Résolus automatiquement : 1
- Résolus manuellement : 0
- Encore ouverts : 22
- **Taux : 4.3%**

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

- [Decision] Capital fixé à 10 000 EUR
- [Decision] Structure actionnariat : DiaHo (chinois) entre à 40% directement au capital, sans personnel opérationnel/management chinois physiquement présent
- [Decision] Article 23 : année fiscale à fixer entre associés avant envoi
- [Decision] Article 33 : "directors" à désigner avant envoi
- [Decision] Contrats commerciaux à adapter suite aux retours UCM Belgique
- [Decision] Meuble banquette multi-tiroirs : 104cm (L) × 55cm (P) × 25cm (H)
- [Decision] Configuration : 3 tiroirs ouvrants côté interne + externe via glissières
- [Decision] Trappe supérieure avec pivot 180° externe
- [Decision] Dimension critique des tiroirs : 25-26cm (contrainte meuble en place avec banquette passager)
- [Decision] Reste en 12V (tous composants standardisés pour simplifier procurement)
- [Decision] RPI à allumer pour tests réels en quelques jours
- [Decision] Procédure "fiches spots" pour stationnement à créer
- [Decision] Traitement des "skip" reporté (batch de 10)
- [Decision] Brouillons à valider avant promotion
- [Decision] Pattern mémoire à documenter pour lancer via noms de procédures (inbox + Telegram)
- [Decision] Arrêt des sessions "en rond" → documentation markdown immédiate
- [Decision] Tests en réel planifiés (quelques jours)
- [Decision] Simulations avant déploiement
- [Decision] Vetalyx (projet business Belgique)** :
- [Decision] Vanlife (Lupo Bianco - projet IOT van)** :
- [Decision] Procédures/Process** :
- [Failure] (×2 occurrences) : contexte flou, pas de service/URL identifiée. Nécessite clarification.
- [Failure] (realtime_input.m) : payload invalide, cause inconnue, bloque communication temps réel.
- [Failure] (disk8s2) : volume APFS chiffré + verrouillé, dépend d'autorisation macOS.
- [Failure] Erreur 403 Access Blocked** (×2 occurrences) : contexte flou, pas de service/URL identifiée. Nécessite clarification.
- [Failure] Erreur WebSocket 1007** (realtime_input.m) : payload invalide, cause inconnue, bloque communication temps réel.
- [Failure] tmutil backup failure** (disk8s2) : volume APFS chiffré + verrouillé, dépend d'autorisation macOS.

### Fréquence des patterns (14 jours)
- **Decision** : 5 jours, 27 occurrences
- **Failure** : 3 jours, 15 occurrences
- **Question** : 3 jours, 20 occurrences
- **Recurring question** : 3 jours, 12 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 27
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**499** recommandations au total — **499** ouvertes — **0** en cours — **0** terminées

⚠️ 472 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 449
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 5
- **Renard** : 2
- **Sybil** : 1

### Plus récentes ouvertes

- [id=486] (2026-10-19) **Dobby** : Créer PROCEDURES.md** (ou PATTERNS.md)
- [id=487] (2026-10-19) **Dobby** : Documenter toute procédure réutilisable
- [id=488] (2026-10-19) **Forge** : Format : `## [NOM] - Description`
- [id=489] (2026-10-19) **Dobby** : Linking : inbox → reference procédure
- [id=490] (2026-10-19) **Dobby** : Exemple : `PROCEDURE_VANROLL_INSPECT`, `PROCEDURE_FICHES_VALIDATION`

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.35 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.35**
