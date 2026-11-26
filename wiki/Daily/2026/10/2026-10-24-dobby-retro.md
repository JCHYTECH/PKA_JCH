---
date: 2026-10-24
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1128
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-24

**Sessions analysées :** 2 | **Échanges :** 1128 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE SESSIONS 2026-10-24 | PKA JCH

---

## Décisions prises

### Stratégiques
1. **Vetalyx (Belgique)** : Architecture capitalistique arrêtée
   - Capital fixé à 10 000€
   - Entrée directe de DiaHo (société chinoise) à 40% du capital
   - Pas de personnes physiques chinoises en opérationnel/management
   - Statut : attente validation UCM + réponse des chinois avant signature

2. **Niveau d'accès PKA** : Rester au niveau 1
   - Décision de ne pas escalader complètement
   - À revisiter si patterns d'utilisation évoluent

3. **Priorisation des drafts → validés**
   - Fiches validées à finaliser en urgence
   - Screenshots inbox/sites à traiter (volume non quantifié)

4. **Vanlife (Lupo Bianco)** : Meuble banquette commandé
   - Specs : 104cm L × 55cm P × 25cm H
   - 3 tiroirs double accès (interne + externe via glissières)
   - Trappe supérieure basculante 180°
   - Installation batterie Bluetti 100 V2 + chargeur associé prévue

5. **ARTEON** : Publication hebdomadaire à programmer
   - Décision prise mais scope vague (non documentée)

6. **Procédure fiches "spots"** : À concevoir pour parking
   - Besoin confirmé, formalisation manquante

---

## Échecs ouverts / bloqueurs

### Critiques (impactent les projets)
- **Erreur 403 Access Blocked** → bloque accès à ressource non identifiée
- **tmutil startbackupVolume failed** : Volume APFS chiffré non accessible
  - Symptôme : montage échoue, backup interrompu
  - Cause root : pas trouvée, impact sur continuité données
- **Vanroll test data missing** : "vanroll test ne donne plus de données"
  - Debug en cours, source non identifiée
- **HA bug** : À vérifier, impact système de maison intelligente non quantifié

### Intégration Kiro
- **Accès impossible à https://www.renaud-dekode.fr/c/kiro**
  - JCH demande compréhension + intégration PKA
  - Pas de retour documenté sur faisabilité
  - Bloc : évaluation suspendue

### Réglementaire Vetalyx
- **Question non tranché** : Obligation de déclaration actionnaire chinois ?
  - UCM belge a répondu → réponse NOT INCLUDED dans ce transcript
  - Status : attente mise à jour équipe

### Infrastructure
- **État backup système** : tmutil échoue, aucun plan B évoqué
- **Bug HA** : Pas de deadline, pas d'escalade de priorité

---

## Questions récurrentes (signe de lacunes documentaires)

### 🚨 PATTERNS MAJEURS

| Question | Occurrence | Indication |
|----------|-----------|-----------|
| "C'est quoi les states files ?" | 2x | Concept HA/Lupo non documenté dans MEMORY.md |
| "Comment faire en sorte que tu gardes en mémoire les procedures ?" | 2x | **CRITIQUE** : Procédure de memory embedding vague/inexistante |
| "C'est quoi le ZH ?" | 2x | Entité "ZH" mentionnée sans contexte → doc missing |
| "Comment utiliser TTL 24h avec fluidité ?" | 1x+ | Pattern cache/API non clarifié |
| "Pourquoi cela a été arrêté et comment réactiver ?" | 2x | Absence de changelog/decision log |
| "C'est quoi le kit hardwire ?" | 1x | Composant van mentionné sans spec |
| "Avant/arrière, 4 roues vs petit ?" | 2x | Schéma de suspension Lupo non documenté |
| "L(M) c'est quoi ?" | 1x | Notation technique non explicite |
| "Différence lupo/assiette vs esneux/iphone ?" | 1x | **CRITIQUE** : Architectures d'instance HA pas comparées |

### 💡 Diagnostic
Ces récurrences indiquent :
- **USER.md / MEMORY.md incomplets** pour domaines van + HA
- **Pas de glossaire technique** centralisé
- **Procédures d'embedding mémoire floues** (JCH compte sur Dobby pour "garder en mémoire", mais mécanisme implicite)

---

## Nouveaux patterns détectés

### 1. **Fragmentation multi-domaines**
JCH opère sur 4+ univers en parallèle sans isolation :
- **Vetalyx** (légal/financier, synchrone avec partenaires chinois)
- **Vanlife** (mécanique, specs pratiques)
- **WildLens** (projet AI/imagerie)
- **Arteon** (publication hebdo)
- **HA/Lupo** (domotique, scripts Python)

**Impact** : Contexte-switching lourd, risque d'oublies, questions de micro-détails perdues.

### 2. **Attente de réponses externes = blocages silencieux**
- Chinois (DiaHo) : attente réponse capital Vetalyx
- UCM Belgique : validation structure fiscale
- Alain Bosseloir (partenaire) : discussion à faire sur PKA L1

**Pattern** : Pas de tracking des "awaiting feedback" → discussions oubliées.

### 3. **Verification par bavardage plutôt que par scripts**
JCH pose des questions de "pourquoi" (ex: "pourquoi vanroll test ne donne plus de données") en conversationnel au lieu de :
- Exécuter `pka_agent_usage.py` ou `pka_vault_health.py`
- Lister les changements récents
- Tracer manuellement

**Sous-pattern** : Scripts existent dans `scripts/` mais ne sont pas intégrés au workflow de debug.

### 4. **Décisions incomplètes**
"On va rester au niveau 1" → pas de critère d'escalade
"On va faire des simulations" → pas de deadline
"Procédure de fiches spots" → structure inconnue

---

## Efficacités / inefficacités

### ✅ Efficacités observées
- **Utilisation multi-outils fluide** : DeepSeek ↔ Claude ↔ Codex sans friction majeure
- **PKA comme artifact store centralisé** : Decisions de Vetalyx trouvent un repo unique
- **Agents (Dobby) comme contexte-keeper** : Extraction patterns = bonne hygiène
- **Batch processing décisions** : JCH agrège 4-5 décisions par session plutôt que atomique

### ❌ Inefficacités majeurs

1. **Pas de "decision log" structuré**
   - Décisions parsemées dans le transcript
   - Pas de format DATE | DECISION | OWNER | DEADLINE | IMPACT
   - Résultat : retrouvailles lentes, risque contradiction

2. **Zero linking entre domaines**
   - Vetalyx et Lupo sont traitées indépendamment
   - Mais : qui manage timeline Lupo si VanLife bloque Vetalyx ?
   - Pas de dépendance explicite

3. **Debugging conversationnel**
   - "vérifie le bug HA" → vague
   - "checke pourquoi ce blocage" → pas de reproduction steps
   - Agents doivent deviner contexte complet

4. **Memory embedding implicite**
   - JCH : "comment faire pour que tu gardes en mémoire les procedures ?"
   - Dobby/Claude : suppose qu'on va écrire dans MEMORY.md
   - **Mais**: qui écrit ? Quand ? Format ? Pas de ritual

5. **TTL 24h + "fluidité"**
   - Question : "comment utiliser TTL 24h dans un HTML ?"
   - Indique confusion cache-control vs UX
   - Pas de docs éducative d'archi PKA

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 CRITIQUES

1. **Vetalyx attente réponse chinois**
   - Status : "constat en fichier à activer quand chinois répondent"
   - Owner : ? (probablement JCH + Alain Bosseloir)
   - Fichier : à créer/nommer `/JCH_PRIVATE/vetalyx/AWAITING_DIAHO_RESPONSE.md`
   - Follow-up : deadline ?

2. **tmutil backup failure**
   - APFS volume locked → needs manual recovery
   - Impact : données exposées si pas de plan B
   - Next : créer procédure recovery, tester

3. **Procédure Memory Embedding**
   - JCH demande comment garder procedures en mémoire accessible via "nom"
   - Besoins : Dobby indexe procedures par tag → retrieve via @procedure_name
   - Implement : `scripts/pka_procedure_index.py` (listing + fuzzy search)

### 🟡 IMPORTANTS

4. **Vanroll test data missing**
   - Debug : vérifier logs timestamp, changements récents
   - Utiliser : `scripts/wildlens_weekly.py` pour trend data
   - Owner : à assigner

5. **Glossaire technique manquant**
   - ZH, L(M), states files, kit hardwire, TTL cache context
   - Create : `docs/GLOSSARY.md` ou wiki entry
   - Owner : Dobby (extraction) + JCH (validation)

6. **ARTEON publication hebdo**
   - Décision : oui, mais scope flou
   - Define : format, source data, frequency, platform
   - Deadline : avant prochaine session

### 🟢 À SURVEILLER

7. **HA instance architecture**
   - Question : différence lupo/assiette vs esneux/iphone ?
   - Suggest : diagram `docs/HA_INSTANCES.md`
   - Impact : clarifier si c'est instance selection vs network config

8. **Lupo Bianco meuble banquette**
   - Specs locked, batterie Bluetti 100 V2 commandée
   - Next steps : timeline install, électricité intégration
   - Risk : batterie + meuble = poids, recalc CdG ?

---

## Recommandations

### Immédiate (cette semaine)

1. **Créer `/JCH_PRIVATE/AWAITING.md`** : tracker centralisé des décisions en attente externe
   ```
   | Date | Qui | Quoi | Délai | Criticité |
   | 2026-10-24 | DiaHo | Validation % capital Vetalyx | ? | HAUTE |
   | 2026-10-24 | UCM Belgique | Fiscal ok | ? | HAUTE |
   ```

2. **Écrire `docs/GLOSSARY.md`** avec ZH, states files, kit hardwire, L(M), TTL-context
   - Format : terme | domaine (HA/van/vetalyx) | définition | ref docs

3. **Documenter procédure Memory Embedding**
   - Ritual : "À la fin de chaque session Dobby, écrire `MEMORY.md` delta"
   - Format :

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

- [Decision] : Architecture capitalistique arrêtée
- [Decision] Capital fixé à 10 000€
- [Decision] Entrée directe de DiaHo (société chinoise) à 40% du capital
- [Decision] Pas de personnes physiques chinoises en opérationnel/management
- [Decision] Statut : attente validation UCM + réponse des chinois avant signature
- [Decision] : Rester au niveau 1
- [Decision] Décision de ne pas escalader complètement
- [Decision] À revisiter si patterns d'utilisation évoluent
- [Decision] Fiches validées à finaliser en urgence
- [Decision] Screenshots inbox/sites à traiter (volume non quantifié)
- [Decision] : Meuble banquette commandé
- [Decision] Specs : 104cm L × 55cm P × 25cm H
- [Decision] 3 tiroirs double accès (interne + externe via glissières)
- [Decision] Trappe supérieure basculante 180°
- [Decision] Installation batterie Bluetti 100 V2 + chargeur associé prévue
- [Decision] : Publication hebdomadaire à programmer
- [Decision] Décision prise mais scope vague (non documentée)
- [Decision] : À concevoir pour parking
- [Decision] Besoin confirmé, formalisation manquante
- [Decision] Vetalyx (Belgique)** : Architecture capitalistique arrêtée
- [Decision] Niveau d'accès PKA** : Rester au niveau 1
- [Decision] Priorisation des drafts → validés
- [Decision] Vanlife (Lupo Bianco)** : Meuble banquette commandé
- [Decision] ARTEON** : Publication hebdomadaire à programmer
- [Decision] Procédure fiches "spots"** : À concevoir pour parking
- [Failure] Erreur 403 Access Blocked** → bloque accès à ressource non identifiée
- [Failure] tmutil startbackupVolume failed** : Volume APFS chiffré non accessible
- [Failure] Symptôme : montage échoue, backup interrompu
- [Failure] Cause root : pas trouvée, impact sur continuité données
- [Failure] Vanroll test data missing** : "vanroll test ne donne plus de données
- [Failure] Debug en cours, source non identifiée
- [Failure] HA bug** : À vérifier, impact système de maison intelligente non quantifié

### Fréquence des patterns (14 jours)
- **Decision** : 4 jours, 29 occurrences
- **Failure** : 4 jours, 17 occurrences
- **Recurring question** : 4 jours, 15 occurrences
- **Question** : 3 jours, 23 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 32
- Jours d'observation : 6
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**524** recommandations au total — **524** ouvertes — **0** en cours — **0** terminées

⚠️ 485 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 471
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 6
- **Renard** : 3
- **Sybil** : 2

### Plus récentes ouvertes

- [id=520] (2026-10-24) **Dobby** : Créer `/JCH_PRIVATE/AWAITING.md`** : tracker centralisé des décisions en attente
- [id=521] (2026-10-24) **Dobby** : Écrire `docs/GLOSSARY.md`** avec ZH, states files, kit hardwire, L(M), TTL-conte
- [id=522] (2026-10-24) **Dobby** : Format : terme | domaine (HA/van/vetalyx) | définition | ref docs
- [id=523] (2026-10-24) **Dobby** : Documenter procédure Memory Embedding
- [id=524] (2026-10-24) **Dobby** : Ritual : "À la fin de chaque session Dobby, écrire `MEMORY.md` delta

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.3 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.3**
