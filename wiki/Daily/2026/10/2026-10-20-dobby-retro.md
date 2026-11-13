---
date: 2026-10-20
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1087
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-20

**Sessions analysées :** 2 | **Échanges :** 1087 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA - Session 2026-10-20

## Décisions prises

### Confirmées et actionnées
- **Stockage M5** : Abandon du "tout en 12" → achat SSD 2To minimum (décision logistique/procurement)
- **Van Lupo** : Installation Bluetti 100 V2 + charger 2 (config énergétique fixée)
- **Gestion Inbox** : Passage des drafts en "validés" (workflow de validation)
- **Projet IoT-Van** : Résurrection confirmée → demande de résumé lancée
- **Priorité P2** : Mise en attente (dépendance de position d'autres éléments)

### À clarifier / Incomplètes
- "on va choisir le niveau disponible dans l'iphone. peut on envoyer" → **quoi envoyer ? Où ?** Décision tronquée.
- "on va tester en life et je te reviens" → **quoi tester exactement ?** Pas de trace du contexte.

## Échecs ouverts / bloqueurs

### Critiques système
| Bloqueur | Contexte | Impact |
|----------|----------|--------|
| **SSL/TLS failure** | "secure connection ro fail" | Impossible de déterminer le service affecté |
| **403 Access Blocked** | Aucun endpoint précisé | Authentification ou permissions manquantes |
| **WebSocket 1007** | "invalid frame payload data" realtime_input.m | IoT-Van telemetry probablement affectée |
| **APFS mount failure** | tmutil on disk8s2, volume chiffré et verrouillé | Backup automatique bloqué |

### Fonctionnels
- **vanroll test** : Plus de données remontées → Cause inconnue, correction demandée mais pas faite
- **Home Automation** : Van à niveau "off" → CAP non fonctionnel ; "API key required" en dessous
- **HA Bug** : Signalé mais jamais triagé ("verifie le bug HA")

### Métier
- **VETALYX Belgique** : Articles 23 & 33 du statut à fixer AVANT envoi (directors, année fiscale)
- **Contrat VETALYX** : Modification majeure (Article 6+) vs. contrat Zheda → Réconciliation nécessaire
- **DiaHo/actionnariat chinois** : UCM consulté mais réponse tronquée dans transcript

## Questions récurrentes (signe de lacune documentaire)

### Terminologie technique non définie
| Terme | Mentions | Status |
|-------|----------|--------|
| **ZH** | 1x | Jamais expliqué → Acronyme flottant |
| **States files** | 1x | Relation à Lupo (31 août) inconnue |
| **L(M)** | 2x | Notation scientifique ou convention locale ? |
| **Kit hardwire** | 1x | Contexte vanroll/IoT-Van manquant |
| **"Synthèse de lecture propre"** | 1x | Processus documentaire vague |

### Procédurales / Organisationnelles
- **3 fiches needs_review** : Jamais mentionnées, pas tracées
- **Pourquoi les dimensions du tiroir 25-26 cm ?** : Demandé 2x, réponse partielle ("meuble en place quand banquette passager")
- **Différence 4 roues vs. roues petites/avant/arrière** : Contexte véhicule manquant

### Gestion mémoire / Procédures
- Comment lancer des procédures via **"un nom"** au lieu de détailler via Inbox + Telegram ?
- **Pourquoi vanroll ne donne plus de données ?** Demandé + verificaton assignée mais jamais rapportée

## Nouveaux patterns détectés

### 1. **Fragmentation des contexts critiques**
Les décisions métier (VETALYX, Lupo, IoT-Van) et techniques (SSL, WebSocket, HA) sont entrelacées sans séparation claire.
- Chaque projet a son propre status scattered (drafts, validés, archived)
- Pas de single source of truth par projet

### 2. **Backward incompleteness**
Les demandes de vérification/analyse ("verifie pourquoi X", "analyse le pourquoi pour Y") ne sont jamais retournées avec un verdict.
Exemple : vanroll test, bug HA, fiches Dante vides.

### 3. **Tool-switching overhead**
Utilisation parallèle : DeepSeek TUI (21x), Claude Code (42x), Codex CLI.
→ **Les métadonnées de contexte ne suivent pas** (turn_meta répétées, working set identique 4x d'affilée)

### 4. **Inbox = vortex**
Référence récurrente à `JCH_Inbox/00_INBOX/` mais structure interne opaque.
- Validation workflow ("drafts → validés") existe mais critères de validation absents
- "00_INBOX" vs. "03_PROJECTS" vs. "04_PILOTAGE_STRATEGIQUE" : hiérarchie floue

### 5. **Credentials management fragile**
`credentials-central.md` accédé lors de diagnostics IPv4 → risque d'exposition en transcript si perte de contexte

## Efficacités / Inefficacités

### ✅ Efficacités
- **Décisions rapides** : "on va rester tout en 12" → "non" → SSD 2To décidé en < 1 échange
- **Multi-projet parallelization** : VETALYX, IoT-Van, Lupo gérés simultanément sans deadlock apparent
- **Tool selection adaptive** : Claude pour statuts complexes, DeepSeek pour patterns, Codex pour shell

### ❌ Inefficacités
- **No closure on verification tasks** : "verifie X", "analyse Y" assigné mais jamais rapporté back
- **Acronym inflation** : ZH, L(M), states files, kit hardwire jamais définis → demandes répétées
- **Transcript pollution** : Métadonnées `turn_meta` dupliquées 4x, working set identique = token waste
- **Inbox state ambiguity** : "met en validés", "chemin des fichiers à encore validé" → critères flous
- **Incomplete decision captures** : "peut on envoyer ?" sans objet ; "tester en life" sans spec
- **HA monitoring dead** : Bug signalé, jamais triagé → production health blind spot

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Projets en cours
1. **VETALYX** (Belgique, capital 10k€, DiaHo 40% actionnaire chinois)
   - Status Articles 23 & 33 MUST être fixés avant envoi
   - Contrat commercial modifié vs. draft Zheda → réconciliation obligatoire
   - Fiscal solidity check de DiaHo en attente

2. **IoT-Van** (Ressuscité le 2026-10-20)
   - Hardware : Bluetti 100 V2 + charger 2 commandés
   - Monitoring : vanroll test en panne (cause TBD)
   - HA bug : Van level "off" → CAP non-fonctionnel
   - WebSocket 1007 sur realtime_input.m

3. **Lupo Van** (reporté au 31 août)
   - Dimensions tiroir : 25-26 cm (pourquoi ? réponse partielle)
   - "States files" ? (définition manquante)

4. **Hardware M5**
   - SSD 2To minimum → procurement en cours

### Blockers actifs
| Bloqueur | Owner | DueDate |
|----------|-------|---------|
| vanroll test ne remonte plus de données | ? | ? |
| HA bug : level off → CAP broken | ? | ? |
| Articles 23 & 33 VETALYX fixation | ? | Pre-send |
| VETALYX/Zheda contrat reconciliation | ? | ? |
| tmutil backup APFS mount error | ? | ? |
| Définir : ZH, L(M), states files, kit hardwire | Dobby | ASAP |

### Mémoire procédurale
- Inbox workflow : drafts → validés (critères TBD)
- Procédures nommées : demande pour lancer via "nom" au lieu de filepath
- Telegram + Inbox dual ingestion → unification?

## Recommandations

### 🔴 Urgent (< 48h)
1. **Triage bloquers** : Créer ticket HA bug, websocket 1007, APFS mount avec stack traces complètes
2. **Closure sur vérifications** : "vanroll test", "bug HA" → rapport investigation concis ou escalade
3. **VETALYX legal checkpoint** : Articles 23/33 statut + contrat Zheda → document de signature pré-validé

### 🟡 Court terme (semaine)
4. **Terminer définitions** : Documenter ZH, L(M), states files, kit hardwire dans un glossaire projet (lien dans AGENTS.md)
5. **Inbox taxonomy** : Clarifier "drafts vs. validés" → checklist de validation visible
6. **Lupo dimensions** : Question "pourquoi 25-26 cm" → réponse complète en wiki ou BAM
7. **Procédures nommées** : Si demande fréquente, créer launcher CLI (`dobby proc:lanciomar <nom>`)

### 🟢 Moyen terme
8. **Turn_meta dedup** : DeepSeek repetait working set identique 4x → caching ou session state across messages
9. **Credentials rotation** : credentials-central.md accédé en diagnostic → audit access logs
10. **IoT-Van monitoring** : Remplacer "test en life + je te reviens" par telemetry dashboard ou webhook
11. **Inbox → Git?** : Si validation workflow critique, tracker dans `.github/VALIDATION.md` ou branch strategy

### 🏗️ Structural
12. **Decide on single source of truth per project** : VETALYX status → Google Sheets? Notion? Markdown? (Actuellement scattered across composer_history)
13. **Tool handoff protocol** : DeepSeek → Claude → output format strict (JSON + markdown) pour eviter perte de contexte
14. **Retrospective cadence** : Sessions identifiées = 2 sur 2026-10-20 → fixer si daily/weekly review existe

---

### Meta-observation finale
**Le système PKA fonctionne mais a atteint la limite de "conversational state".**  
JCH jongle 3+ projets complexes (tech + légal + hardware) avec 4 outils parallèles.  
Sans documentation centralisée des décisions et sans closure protocol sur les vérifications, chaque session accumule de la "dette cognitive".  
Les prochaines sessions risquent de re-poser les mêmes questions (ZH, states files, kit hardwire) jusqu'à centralisation.

**Priority absolue : Glossaire + Inbox taxonomy + Closure protocol.**

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 22
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 22
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

- [Decision] Stockage M5** : Abandon du "tout en 12" → achat SSD 2To minimum (décision logistique/procurement)
- [Decision] Van Lupo** : Installation Bluetti 100 V2 + charger 2 (config énergétique fixée)
- [Decision] Gestion Inbox** : Passage des drafts en "validés" (workflow de validation)
- [Decision] Projet IoT-Van** : Résurrection confirmée → demande de résumé lancée
- [Decision] Priorité P2** : Mise en attente (dépendance de position d'autres éléments)
- [Failure] | "secure connection ro fail" | Impossible de déterminer le service affecté |
- [Failure] | Aucun endpoint précisé | Authentification ou permissions manquantes |
- [Failure] | "invalid frame payload data" realtime_input.m | IoT-Van telemetry probablement affectée |
- [Failure] | tmutil on disk8s2, volume chiffré et verrouillé | Backup automatique bloqué |

### Fréquence des patterns (14 jours)
- **Decision** : 5 jours, 27 occurrences
- **Failure** : 3 jours, 13 occurrences
- **Question** : 2 jours, 19 occurrences
- **Recurring question** : 2 jours, 11 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 9
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**502** recommandations au total — **502** ouvertes — **0** en cours — **0** terminées

⚠️ 472 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 450
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 5
- **Renard** : 3
- **Sybil** : 2

### Plus récentes ouvertes

- [id=500] (2026-10-20) **Dobby** : Triage bloquers** : Créer ticket HA bug, websocket 1007, APFS mount avec stack t
- [id=501] (2026-10-20) **Sybil** : Closure sur vérifications** : "vanroll test", "bug HA" → rapport investigation c
- [id=502] (2026-10-20) **Renard** : VETALYX legal checkpoint** : Articles 23/33 statut + contrat Zheda → document de
- [id=486] (2026-10-19) **Dobby** : Créer PROCEDURES.md** (ou PATTERNS.md)
- [id=487] (2026-10-19) **Dobby** : Documenter toute procédure réutilisable

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.35 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.35**
