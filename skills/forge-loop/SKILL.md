---
name: forge-loop
description: Boucle autonome de code review avec quality gate — Forge code → review → score < 4/5 → auto-fix → repush → re-review. Déclencher sur "forge loop", "code loop", "auto-fix", "boucle de review". Inspiré du pattern Grep Loop (Ross Mike) et AutoResearch (Andrej Karpathy).
---

# Skill — forge-loop

> Double lignée : **Grep Loop** (Ross Mike) pour la boucle code-review, **AutoResearch** (Andrej Karpathy) pour l'architecture 3 fichiers et le budget temps fixe. L'agent code, un reviewer automatique score, et la boucle itère jusqu'à atteindre le seuil de qualité. Dobby ne voit que le résultat final.

## Architecture 3 fichiers (pattern AutoResearch)

Karpathy a formalisé toute boucle agent autonome en 3 fichiers, dont un seul est modifiable par l'agent :

| Fichier AutoResearch | Rôle | Équivalent PKA | Modifiable ? |
|---------------------|------|----------------|-------------|
| `program.md` | Instructions de la boucle | Brief Forge + quality gate | ❌ Immuable (défini par Dobby) |
| `train.py` | Code à optimiser | Fichiers de travail Forge | ✅ Oui |
| `prepare.py` | Métrique d'évaluation | `code-review-pro` (score /5) | ❌ Immuable |

**Principe clé :** l'agent ne peut **jamais** toucher la métrique d'évaluation. Sans cette protection, il pourrait réécrire la fonction de scoring pour simuler des résultats parfaits. C'est l'équivalent d'un étudiant qui corrige lui-même son examen.

## Déclencheurs

- "forge loop sur <fichier/brief>"
- "code loop", "auto-fix"
- "boucle de review", "lance la review loop"
- "passe ce code au code-review-pro et corrige jusqu'à 4/5"

## Principe

```
Brief → Forge code → push → code-review-pro → score /5
                                                 │
                                  score ≥ 4 ────┤─── ✅ Dobby valide
                                  score < 4  ───┤─── 🔁 Forge corrige → repush
                                                     (max 3 itérations)
```

Une gate de qualité objective (`code-review-pro ≥ 4/5`) remplace la supervision humaine continue. La leçon du Grep Loop de Ross Mike et d'AutoResearch de Karpathy est la même : une boucle agent sans quality gate objective est une machine à sous.

## Procédure

### 1. Identifier la cible

- Si un brief Forge est mentionné → extraire le livrable et le repo/chemin
- Si un fichier est donné → travailler sur ce fichier directement
- Si rien n'est spécifié → demander

### 2. Revue initiale

```bash
# Utiliser le skill code-review-pro sur le code cible
# La review doit produire un score numérique /5
```

Si le score est ≥ 4/5 → **terminé**. Reporter le score à Dobby.

### 3. Boucle de correction (si score < 4/5)

```
ITÉRATION 1..3 :
  1. Lire le rapport code-review-pro
  2. Pour chaque issue Critical et High → appliquer le fix
  3. Commit + push
  4. Relancer code-review-pro
  5. Si score ≥ 4/5 → SORTIR (succès)
```

### 4. Sortie de boucle

| Issue | Action |
|-------|--------|
| **Score ≥ 4/5** | ✅ Reporter succès : score final, nombre d'itérations, changements appliqués |
| **3 itérations sans atteindre 4/5** | ⚠️ Escalader à Dobby avec le rapport détaillé et les issues restantes |
| **Token budget dépassé** | 🛑 Arrêter immédiatement. Reporter budget consommé + dernier score |
| **Time budget dépassé** | 🛑 Arrêter. Chaque expérience a un budget temps fixe pour être comparable |

## Règles

### Règles absolues

- **Max 3 itérations.** Au-delà, le code a besoin d'une intervention humaine (ou d'un redesign).
- **Token budget : 50 000 tokens par loop.** Si la loop dépasse ce plafond, elle s'arrête et escalade. C'est la leçon du $1.3M de Peter.
- **Time budget : 300 secondes par expérience.** (Pattern AutoResearch.) Chaque itération a le même temps alloué → les idées brutes s'affrontent à armes égales.
- **Ne jamais modifier le comportement fonctionnel.** Les fixes sont correctifs (sécurité, perf, style), pas des changements de spec.
- **Ne jamais toucher la métrique d'évaluation.** `code-review-pro` est immuable. Si le score semble incohérent sur plusieurs runs → escalader à Dobby, ne pas le contourner.
- **Toujours commit après chaque fix.** Un commit = un fix documenté, traçable. Pattern AutoResearch : commit si mieux, revert si pire.

### Portée des fixes

| Priorité issue | Action |
|----------------|--------|
| **Critical** (sécurité) | Toujours fixer |
| **High** (perf, bug) | Toujours fixer |
| **Medium** (qualité code) | Fixer si < 3 changements |
| **Low** (style, nice-to-have) | Ignorer dans la loop |

### Modèle économique

- Utiliser le modèle le moins cher capable de faire la review (Ollama local si Gemma 3 dispo, sinon DeepSeek)
- La skill `modele` peut être appelée avant la loop pour estimer le coût
- Les corrections sont faites par le même modèle que la review pour éviter les conflits de style

## Intégration brief

Quand un brief Forge inclut `auto_review: true`, la forge-loop se déclenche automatiquement après le push du livrable :

```yaml
# Dans le brief Forge :
auto_review: true
review_threshold: 4
max_iterations: 3
time_budget: 300      # secondes par expérience (pattern AutoResearch)
```

## Template `program.md` (inspiré de Karpathy)

Ce template est injecté dans l'agent qui exécute la boucle. Adapté du `program.md` original d'AutoResearch :

```markdown
# FORGE LOOP — Instructions autonomes

Tu es un agent de code review autonome. Ta mission : améliorer le code
jusqu'à ce que le score code-review-pro atteigne le seuil de qualité.

## Règles absolues
1. Tu NE PEUX PAS modifier le fichier de scoring (code-review-pro).
   La métrique est sacrée. Contourner le scorer = échec de la mission.
2. Chaque expérience dure max 300 secondes. Budget fixe = comparaison équitable.
3. Commit après chaque fix réussi. Revert si le score ne s'améliore pas.
4. Max 3 tentatives. Après 3 échecs, produis un rapport d'escalade.

## Ce que tu peux modifier
- Le code source du projet (fichiers .py, .js, .ino, .yml, Dockerfile, etc.)
- La configuration de build
- Les dépendances (dans package.json, requirements.txt, etc.)

## Ce que tu NE PEUX PAS modifier
- Le fichier d'évaluation (code-review-pro, benchmark, test harness)
- Les spécifications fonctionnelles (le comportement attendu)
- Les tests existants (tu peux en ajouter, pas en supprimer)

## Workflow
1. Lis le rapport code-review-pro.
2. Formule une hypothèse : « Si je corrige X, le score devrait monter. »
3. Applique le fix.
4. Commit + push.
5. Relance la review.
6. Si score ≥ seuil → SUCCÈS. Sinon → nouvelle hypothèse.
7. Ne t'arrête pas. Ne me demande rien. Continue jusqu'au succès ou à
   l'épuisement du budget (3 itérations ou plafond tokens).

## Format de sortie
À la fin de la boucle (succès ou échec), produis :
```
FORGE-LOOP REPORT
Score initial : X/5
Score final : Y/5
Itérations : N
Fixes appliqués :
  - [commit hash] Description du fix
Tokens consommés : Z
Verdict : SUCCÈS / ÉCHEC (raison)
```
```

## Skills liés

- **`code-review-pro`** — Le reviewer automatique, source du score /5 (immuable)
- **`review`** — Alternative via l'outil natif DeepSeek TUI
- **`modele`** — Estimation du coût token avant de lancer la loop
- **`brief`** — Pour générer le brief Forge avec `auto_review: true`
- **`wildnexus-benchmark-loop`** — Variante spécialisée pour les benchmarks hardware WildNexus

## Références

- **Grep Loop** (Ross Mike, 2026) — Cursor + GitHub + Greptile, gate ≥ 4/5
- **AutoResearch** (Andrej Karpathy, 2025) — Architecture 3 fichiers, budget temps fixe, eval immuable
