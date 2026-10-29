---
date: 2026-07-01
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1158
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-01

**Sessions analysées :** 2 | **Échanges :** 1158 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE PKA — Sessions 2026-07-01

---

## Décisions prises

### ✅ Confirmées et actionnables
- **Migration vers OpenRouter** : abandon de Claude Code et Codex CLI pour centraliser via OpenRouter (économies + flexibilité)
- **Nettoyage fichiers** : suppression `.bak-*`, `.DS_Store` (8 restants), consolidation `session_*.json`
- **Sauvegarde projet plantes** : validation du travail bioacoustique avant oubli — **URGENT**
- **Matériel M0** : achat du MOQ=10 via EPS confirmé (alternative Meramake rejetée)
- **Délai vidéo Belgique** : report au 30 juin validé (dépendance externe OK)

### ⚠️ Partielles / en suspens
- **Validation cascade** : demande récurrente de vérifier les effets aval — **aucun processus documenté**
- **Modèle de sélection M0** : question "une fois dedans, comment je choisis ?" → **pas de réponse finale**
- **Processus de feedback** : "mets-le dans un modèle spécialisé" → **lequel ? où ?**

---

## Échecs ouverts / bloqueurs

### 🔴 **Critique — Non résolu**

| Symptôme | Cause probable | Impact |
|----------|---|---|
| `NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT` | Crash MQTT MCP en session précédente | Impossible de valider PKA actuellement |
| `Stdio transport closed` (pka-homeassistant) | MCP server mort | Home Assistant déconnecté du système PKA |
| `upstream connect error / reset before headers` | Timeout connexion réseau | Bloque communications inter-services |
| Crash Outlook Mac (OlkUIKit framework) | Conflit avec environnement Python | **Non documenté : impact sur workflow ?** |

### ⚠️ **Modéré — Traçable**
- `ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT` : erreur 6683 → **personne ne sait ce que c'est**
- Traceback incomplet (`/Users/jchavauxm5/PKA_JCH/s...`) → **logs pas archivés proprement**
- MQTT validation fail → **pas de health-check auto (noté RED par Kimi)**

### 📋 **Non classé**
- **Crash avant header sur connexion** → diagnostic différé → session suspendue

---

## Questions récurrentes (signe de lacune documentaire)

### 🔴 **Top 3 — Urgence maxima**

1. **Accès aux Apple Notes** 
   - Posée : 2+ fois
   - Implication : JCH utilise Notes comme source de travail → **Dobby ne peut PAS** accéder
   - Lacune : Aucune intégration documentée (webhooks ? sync ?)
   - **Impact** : Dobby reste aveugle sur priorités réelles

2. **Pourquoi maintenant tu as les références Mouser vs. avant** 
   - Posée : 2+ fois en formulation légèrement différente
   - Profond : "comment faire en sorte que tu puisses faire les recherches nécessaires en entrant dans les Si[tes]"
   - Lacune : **Aucun processus d'auto-recherche documenté** (web scraping ? APIs ?)
   - **Impact** : JCH doit chercher manuellement → inefficace

3. **Comment utiliser OpenRouter dans VS Code** 
   - Posée : 2+ fois
   - Implication : JCH a accepté migration OpenRouter → **aucun tuto d'intégration final**
   - Lacune : Pas de guide pour sélectionner modèles (deepseek-v4 vs. deepseek-v4-pro ?)
   - **Impact** : Paralysie d'implémentation

### ⚠️ **Secondaires mais chroniques**

| Question | Récurrences | Raison | Solution requise |
|----------|---|---|---|
| C'est quoi `harness` ? | 2+ | Concept technique flou | Glossaire technique |
| C'est quoi `.venv` en path ? | 2+ | Virtual env mal expliquée | Doc Python pour JCH |
| C'est quoi `(.env)` vs terminal VS Code ? | 2+ | Confusion shell local/terminal IDE | Setup script unifié |
| Memory nudge c'est quoi ? | 2+ | Feature Dobby non expliquée | Prompt d'explicitation |
| C'est quoi `X1201-C1` (SSD connector) ? | 2+ | Spécification hardware oubliée | Fiche technique RPi archivée |
| HACS / Home Assistant setup ? | 2+ | Intégration Sonoff/HA non documentée | Checklist d'installation |

---

## Nouveaux patterns détectés

### 🎯 **Mode décisionnel de JCH**
- **Validate → Report → Freeze** : quand un bloqueur technique émerge, JCH demande rarement escalade — il reporte
  - Exemple : "on va attendre" (Belgique), "on va l'oublier" (plantes)
  - **Signal** : Procrastination défensive, pas inaction pure
  - **Recommandation** : force trigger à J+7 sur tous les "attendre"

### 🔄 **Coupling documentaire fort**
- JCH pose question → Dobby répond → JCH accepte → **personne n'archive dans MEMORY.md**
- 2 sessions plus tard → JCH repose la même question
- **Cause racine** : Pas de "post-session documentation flow"

### ⚡ **Entités critiques sous-documentées**
```
Projets:   wildnexus (19x), homeassistant (8x) [parmi les 12 actifs mentionnés]
Outils:    CLAUDE (61x), deepseek (25x), docker (16x), openrouter (16x) [chaos de noms]
Machines:  M1, M5, RPi, RPI (variantes chaotiques d'un même device)
Acteurs:   dobby (110x), Dobby (15x), Forge (7x) [casse inconsistente]
```
- **Pattern** : Noms instables = requêtes ambiguës = recherches manuelles

### 🧠 **Dobby rate-limitée par API knowledge**
- Kimi 2.5 peut analyser PKA → Dobby demande confirmation ("qu'en penses-tu ?")
- **Signal** : Dobby n'a pas assez de contexte pour autonomie
- Kimi a proposé : health-check auto (RED), 12 dérives pointeurs multi-modèles
- **Dobby n'a pas suivi** → diagnostic stoppé

---

## Efficacités / inefficacités

### ✅ **Ce qui marche**

| Efficacité | Preuve | À maintenir |
|---|---|---|
| **Deepseek-TUI/CodeWhale natif MCP** | Intégration native client+serveur mentionnée | Infrastructure code |
| **Needle-in-Haystack (contexte massif)** | Kimi 2.5 confirme 100% recall | Garder taille DB |
| **Tool Calling fiable** | Transcript montre exécution sans erreur outil | Pattern confiré |
| **Nettoyage fichiers décisif** | `.bak-*`, `.DS_Store` identifiés & actionnés | Itérer mensuellement |
| **Documentation de décisions matérielles** | OV5640 + ESP32-S3 : compatibilité expliquée | Archiver specs |

### ❌ **Ce qui échoue**

| Inefficacité | Symptôme | Coût estimé |
|---|---|---|
| **Pas de process post-session** | 6+ questions reviennent mot-pour-mot | **3–5 heures/mois** |
| **Apple Notes en silo** | Dobby ne voit pas priorités réelles | **Décisions non alignées** |
| **Health-check RED** | Faux positifs massifs (cité par Kimi) | **Surveillance inutile** |
| **Git pack surdimensionné (1,92 Go binaire)** | Historique à nettoyer | **Ralentissements clone** |
| **Validation cascade non documentée** | JCH demande vérification → personne ne sait le checklist | **Regressions fréquentes** |
| **Modèle sélection OpenRouter undefined** | Migration acceptée → implémentation bloquée | **Décision suspendue** |
| **MCP crashes non postmortem** | NCP reset, Outlook crash → aucune analyse | **Récurrence garantie** |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔐 **État du système (snapshot critique)**

```markdown
## PKA Health — 2026-07-01

### Bloqueurs actifs
- MCP server pka-homeassistant : Stdio transport closed (T0)
- Error 6683 (NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT) : à investiguer
- Outlook crash sur startup (macOS) : non lié à PKA ? à clarifier

### Décisions en attente d'implémentation
- OpenRouter integration dans VS Code (guide requis)
- Apple Notes ↔ Dobby sync (architecture TBD)
- Validation cascade checklist (formalisé où ?)

### Délais reportés
- Vidéo Belgique + images/IR : 30 juin (deadline + 1 jour = 2026-07-02 ⚠️)

### Achat validé
- M0 MOQ=10 via EPS (Meramake rejeté, prix prohibitif)

### Sauvegarde en danger
- Travail plantes bioacoustiques : **URGENT** fork dans projet, avant oubli
```

### 🧪 **Patterns confirmés à monitorer**

1. **Report-défense** : JCH reporte plutôt que d'escalader → installer trigger J+7
2. **Lacunes documentaires créent boucles** : même question 2+ fois = signal doc manquante
3. **Noms instables** : `deepseek` vs `DeepSeek`, `RPi` vs `RPI`, `Dobby` vs `dobby`
   - **Action** : normer dans README (kebab-case machines, PascalCase acteurs)
4. **Dobby ne voit pas Apple Notes** : blind spot structurel
5. **MCP flaky** : crashes sans postmortem = récurrence certaine

### 📚 **Artifacts à archiver maintenant**

- [ ] OV5640 + ESP32-S3 compatibilité (technical specs) → docs/hardware/
- [ ] Kimi 2.5 PKA analysis → docs/analysis/2026-07-01-kimi-audit.md
- [ ] OpenRouter setup guide (VS Code) → docs/tools/openrouter-setup.md
- [ ] Validation cascade checklist → AGENTS.md ou SOUL.md
- [ ] Glossary : harness, .venv, .env, HACS, X1201-C1 → wiki/glossary.md

---

## Recommandations

### 🚨 **Urgence T0 (avant prochaine session)**

1.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 38
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 38
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

- [Decision] Migration vers OpenRouter** : abandon de Claude Code et Codex CLI pour centraliser via OpenRouter (économies + flexibilité)
- [Decision] Nettoyage fichiers** : suppression `.bak-*`, `.DS_Store` (8 restants), consolidation `session_*.json`
- [Decision] Sauvegarde projet plantes** : validation du travail bioacoustique avant oubli — **URGENT
- [Decision] Matériel M0** : achat du MOQ=10 via EPS confirmé (alternative Meramake rejetée)
- [Decision] Délai vidéo Belgique** : report au 30 juin validé (dépendance externe OK)
- [Failure] | Symptôme | Cause probable | Impact |

### Fréquence des patterns (14 jours)
- **Failure** : 7 jours, 56 occurrences
- **Decision** : 6 jours, 37 occurrences
- **Question** : 5 jours, 23 occurrences
- **Recurring question** : 5 jours, 21 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (3x) error handlers are registered, logging exception.Traceback (most recent call las
- [Failure] (3x) on a crashe dans le dernier boulot : check graphy complet utilisant ol

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 6
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**183** recommandations au total — **183** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 151
- **Forge** : 27
- **Corbeau** : 3
- **Furet** : 2

### Plus récentes ouvertes

- [id=173] (2026-06-29) **Dobby** : Trancher Wildnexus
- [id=174] (2026-06-29) **Dobby** : Décision OV5640 vs IMX500 : table à décision (cout/délai/perf)
- [id=175] (2026-06-29) **Dobby** : Actioner la commande (AliExpress link exists)
- [id=176] (2026-06-29) **Dobby** : Timeline : GPS si critical path
- [id=177] (2026-06-29) **Dobby** : Documenter les basics

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $5.4 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $5.4**
