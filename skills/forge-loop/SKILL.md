---
name: forge-loop
description: Boucle autonome de code review avec quality gate — Forge code → review → score < 4/5 → auto-fix → repush → re-review. Déclencher sur "forge loop", "code loop", "auto-fix", "boucle de review". Inspiré du pattern Grep Loop (Ross Mike).
---

# Skill — forge-loop

> Pattern Grep Loop adapté à PKA. L'agent code, un reviewer automatique score, et la boucle itère jusqu'à atteindre le seuil de qualité. Dobby ne voit que le résultat final.

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

Une gate de qualité objective (`code-review-pro ≥ 4/5`) remplace la supervision humaine continue. Le transcript de Ross Mike est clair : une boucle agent sans quality gate est une machine à sous.

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

## Règles

### Règles absolues

- **Max 3 itérations.** Au-delà, le code a besoin d'une intervention humaine (ou d'un redesign).
- **Token budget : 50 000 tokens par loop.** Si la loop dépasse ce plafond, elle s'arrête et escalade. C'est la leçon du $1.3M de Peter.
- **Ne jamais modifier le comportement fonctionnel.** Les fixes sont correctifs (sécurité, perf, style), pas des changements de spec.
- **Toujours commit après chaque fix.** Un commit = un fix documenté, traçable.

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
```

## Skills liés

- **`code-review-pro`** — Le reviewer automatique, source du score /5
- **`review`** — Alternative via l'outil natif DeepSeek TUI
- **`modele`** — Estimation du coût token avant de lancer la loop
- **`brief`** — Pour générer le brief Forge avec `auto_review: true`

## Référence

Pattern original : Grep Loop de Ross Mike (podcast "WTF Is an AI Agent Loop Genius or Hype", 2026)
- Outil : Cursor + GitHub + Greptile
- Gate : score Greptile ≥ 4/5
- Principe : l'humain ne valide que le résultat final, pas chaque itération
