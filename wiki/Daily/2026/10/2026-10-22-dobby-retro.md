---
date: 2026-10-22
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1152
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-22

**Sessions analysées :** 2 | **Échanges :** 1152 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-10-22 — JCH & ASSISTANTS

## Décisions prises

1. **Rester en "12" pour procurement** → Standardisation coûts/logistique
2. **Fiches validation workflow** → Draft → Validées (2 étapes explicites)
3. **Installation Lupo (van)** → Bluetti 100 V2 + charger 2 confirmés
4. **Approche relationnelle prioritaire** → Questions polies avant action (projet evenements)
5. **Test en conditions réelles** → Scheduled dans "quelques jours" (décision à tracker)
6. **Réveil projet IoT-Van** → Escalade active
7. **Travail sur screenshots inbox/sites** → Tâche backlog ouverte
8. **Contrats Vetalyx** → Adaptation aux remarques statut + commercial (points Article 23 & 33 flaggés)
9. **Capital Vetalyx** → 10K€ confirmé ; actionnariat chinois (DiaHo 40%) déclaration obligatoire validée

## Échecs ouverts / bloqueurs

### CRITIQUES
- **Home Assistant bloquer** : "van à niveau off, cap ne fonctionne pas" + "API key required" — **CAUSE INCONNUE, IMPACT HA ENTIER**
- **WebSocket realtime_input** : `1007 (invalid frame payload data)` — **Pas de root cause identifiée**
- **Accès 403 blocked** — **Pas de contexte : quelle ressource ?**
- **Backup TimeMachine** : APFS volume encrypted/locked, fsck_apfs échec, superblock invalide → **Perte potentielle de données, urgence medium**

### MINEURS
- **vanroll test** : "ne donne plus de données" — À diagnostiquer
- **Fiches vides (Dante)** : Pattern global ou exception ? → Investigation manquante
- **Kiro integration** : Proposé mais pas de décision d'implémentation

## Questions récurrentes (signe de lacune documentaire)

| Question | Occurrence | Problème documentaire |
|----------|-----------|----------------------|
| "Quelle différence lupo/assiette vs esneux/iphone ?" | 3x | Instance HA non documentée ; nommage des environnements opaque |
| "C'est quoi L(M) ?" | 2x | Notation métrique/électrique non définie dans SKILL.md/MEMORY.md |
| "C'est quoi le kit hardwire ?" | 1x | Composant van non référencé dans schema equipment |
| "TTL 24h, comment utiliser en HTML ?" | 2x | Cache/session TTL pattern pas clarifié ; usage frontend manquant |
| "Pourquoi vanroll ne donne plus de données ?" | 2x | Monitoring/alerting absent ; pas de changelog d'infra |
| "C'est quoi les state files ?" | 1x | HA internals non documentés |
| "Avant/arrière (4 roues vs petit)" | 2x | Schéma spatial van incomplet |
| "C'est quoi le ZH ?" | 1x | Acronyme non défini |
| "Erreur 400 reasoning_content" | 1x | DeepSeek API changes non intégrés dans playbook |

**→ DIAGNOSTIC** : MEMORY.md, SKILL.md, AGENTS.md fragmentés ; pas de **single source of truth** pour les acronymes/configs.

## Nouveaux patterns détectés

1. **Dobby travaille en silos** : Question posée "pourquoi dobby travaille sans s'appuyer sur les experts ?" → Friction utilisateur sur autonomie vs coordination. **Réaction attendue : clarifier rôle Dobby vs Experts (Trace, Jade, Renard).**

2. **Multi-projet context-switching heavy** :
   - Vetalyx (légal/fiscal) ↔ Lupo (mécanique/electric) ↔ HA (networking) ↔ IoT-Van (intégration) ↔ Kiro (eval)
   - **0 tickets Jira/Linear visible** → Priorités implicites, risque oubli

3. **Déploiement progressif sans versioning** :
   - "on va tester en life" + "dans quelques jours" → Tests annoncés mais pas de date de review
   - Pas de test matrix (env : dev/staging/prod)

4. **Finance/légal mélangé à ops** :
   - Article 23/33 Vetalyx mix d'exigences métier/conformité
   - "Seuil endettement 175K€" + "risque ISC ?" → Décision financial governance non documentée

5. **Hardware design en conversation libre** :
   - Meuble banquette van (104×55×25cm, 3 tiroirs, trappe) décrit verbalement
   - **Aucun schéma CAO/2D cité** → Risque interprétation différente

## Efficacités / inefficacités

### ❌ INEFFICACITÉS
| Problème | Impact | Fréquence |
|----------|--------|-----------|
| **Bloqueurs non classés** : "verifie le bug HA" sans ticket/priority | Accumulation technique debt | Récurrent |
| **Décisions verbales sans artefacts** : "mets en memory" vs changelog structuré | Perte de contexte entre sessions | 5+ fois/transcript |
| **Extraction patterns local imparfaite** : résumé contient du bruit (KiroMa ads, textes tronqués) | Bruit signal → action lente | Systématique |
| **Questions identiques répondues ad-hoc** | Chaque occurrence = recherche/explication manuelle | 10+ patterns détectés |
| **0 priorité explicite entre 9 décisions** | Paralysie choix, drift scope | Une par 2-3 échanges |

### ✅ EFFICACITÉS
| Force | Bénéfice |
|-------|----------|
| **Multi-tools orchestration** : DeepSeek + Claude + Ollama + file tools | Flexibilité, bypass rate limits |
| **Immediate tool invocation** : grep, exec_shell, read_file sans latency | Verification rapide, debugging direct |
| **Incremental validation** : "draft → validées" workflow clair | Réduit correction downstream |
| **Polite-first protocol** ("d'abord questions polies") | Stakeholder management préservé |

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### URGENT (48h)
1. **HA outage** : "van à niveau off" + "API key required" — Réassigner à expert réseau ; ajouter logs streaming
2. **TimeMachine backup failure** : Volume APFS locked — Risque données ; tester unlock path immédiatement
3. **vanroll data loss** : Depuis quand ? Correlate avec deployments récents
4. **Vetalyx signatories** : Article 23 (fiscal year) + Article 33 (directors names) — **DUE DATE ?**

### COURT TERME (1 semaine)
- Test "en conditions réelles" pour projet evenements → **Fixer date précise**
- Kiro integration eval → Décision go/no-go, fiche décision
- Meuble van → Demander CAO/sketch ou créer schéma 2D validé
- Fiches Dante vides → Triage : bug global ou exception ?

### STRUCTUREL (sprint planning)
- **Créer ACRONYMS.md** : L(M), ZH, kit hardwire, state files, TTL usage, avant/arrière van nomenclature
- **HA config map** : lupo/assiette vs esneux/iphone instances — schéma déploiement explicite
- **Dobby role charter** : autonomy vs expert escalation criteria
- **Priorité matrix** : Vetalyx (legal deadline?) vs Lupo (comfort?) vs HA (ops critical?)
- **Test matrix template** : dev/staging/prod checklist pour tous deployments

## Recommandations

### 1. **Formaliser les décisions immédiatement après accord**
   ```markdown
   DECISION [Date] [ID]
   - Quoi : Bluetti 100 V2 + charger 2 Lupo
   - Pourquoi : [motivations]
   - Qui : [owner]
   - Deadline review : [date]
   - Dépendances : [blockers]
   ```
   Ajouter lien dans MEMORY.md sous `## Active Decisions`.

### 2. **Créer ticket pour chaque bloqueur**
   - Exemple : `[HA-CRIT-001] van offline + API key ; cause inconnue ; date découverte 2026-10-22`
   - Assign : expert technique
   - SLA : 24h diagnosis

### 3. **Audit Dobby vs Experts**
   - Clarifier : "Dobby appelle expert si X, décide seul si Y"
   - Tracer, Jade, Renard doivent avoir rôles explicites par domaine
   - Éviter silos ; fostering synergy

### 4. **Single source of truth pour configs**
   - Migrer Q&R récurrentes vers docs :
     - `docs/HA_INSTANCES.md` (lupo/assiette/esneux/iphone mappings)
     - `docs/VAN_HARDWARE.md` (all parts + dims + naming)
     - `docs/FINANCIAL_RULES.md` (endettement seuils, ISC, fiscal year)
   - Chercher doc → pas la trouver → créer ticket "DOC-XXX" imméd

### 5. **Timeline explicite pour tests "life"**
   - Pas de "quelques jours" ; utiliser format ISO-8601
   - Exemple : "test en conditions réelles le 2026-10-29 matin, review 14h"
   - Ajouter rollback plan

### 6. **Kiro : décision go/no-go quick**
   - JCH ou délégué : évaluer intégration en 2h max
   - Fiche : "Kiro evaluation [APPROVED|DEFERRED|REJECTED] + raison"
   - Si APPROVED → backlog sprint

### 7. **Audit nettoyage patterns Dobby**
   - Résumé extrait contient bruit (pubs KiroMa, textes tronqués)
   - Améliorer regex/parsing ou ajouter step "human filter" avant génération résumé

---

**Generated** : Dobby  
**Tone** : Direct, fact-based, pas de ménagement.  
**Status** : Actionnable. Attend instructions pour priorité sprint.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 25
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 23
- **Taux : 8.0%**

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

- [Decision] → Standardisation coûts/logistique
- [Decision] → Draft → Validées (2 étapes explicites)
- [Decision] → Bluetti 100 V2 + charger 2 confirmés
- [Decision] → Questions polies avant action (projet evenements)
- [Decision] → Scheduled dans "quelques jours" (décision à tracker)
- [Decision] → Tâche backlog ouverte
- [Decision] → Adaptation aux remarques statut + commercial (points Article 23 & 33 flaggés)
- [Decision] → 10K€ confirmé ; actionnariat chinois (DiaHo 40%) déclaration obligatoire validée
- [Decision] Rester en "12" pour procurement** → Standardisation coûts/logistique
- [Decision] Fiches validation workflow** → Draft → Validées (2 étapes explicites)
- [Decision] Installation Lupo (van)** → Bluetti 100 V2 + charger 2 confirmés
- [Decision] Approche relationnelle prioritaire** → Questions polies avant action (projet evenements)
- [Decision] Test en conditions réelles** → Scheduled dans "quelques jours" (décision à tracker)
- [Decision] Réveil projet IoT-Van** → Escalade active
- [Decision] Travail sur screenshots inbox/sites** → Tâche backlog ouverte
- [Decision] Contrats Vetalyx** → Adaptation aux remarques statut + commercial (points Article 23 & 33 flaggés)
- [Decision] Capital Vetalyx** → 10K€ confirmé ; actionnariat chinois (DiaHo 40%) déclaration obligatoire validée
- [Failure] Home Assistant bloquer** : "van à niveau off, cap ne fonctionne pas" + "API key required" — **CAUSE INCONNUE, IMPACT HA ENTIER
- [Failure] WebSocket realtime_input** : `1007 (invalid frame payload data)` — **Pas de root cause identifiée
- [Failure] Accès 403 blocked** — **Pas de contexte : quelle ressource ?
- [Failure] Backup TimeMachine** : APFS volume encrypted/locked, fsck_apfs échec, superblock invalide → **Perte potentielle de données, urgence medium

### Fréquence des patterns (14 jours)
- **Failure** : 4 jours, 14 occurrences
- **Decision** : 3 jours, 26 occurrences
- **Recurring question** : 3 jours, 12 occurrences
- **Question** : 2 jours, 21 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 21
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**519** recommandations au total — **519** ouvertes — **0** en cours — **0** terminées

⚠️ 485 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 466
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 6
- **Renard** : 3
- **Sybil** : 2

### Plus récentes ouvertes

- [id=515] (2026-10-22) **Dobby** : Formaliser les décisions immédiatement après accord
- [id=516] (2026-10-22) **Dobby** : Quoi : Bluetti 100 V2 + charger 2 Lupo
- [id=517] (2026-10-22) **Dobby** : Pourquoi : [motivations
- [id=518] (2026-10-22) **Dobby** : Deadline review : [date
- [id=519] (2026-10-22) **Dobby** : Dépendances : [blockers

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.35 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.35**
