---
name: arbor-research
description: Protocole de recherche autonome inspiré d'Arbor (RUC-NLPIR/Microsoft Research) — hypothèse → expérience → insight → décision. Transforme n'importe quelle loop PKA en boucle cumulative avec arbre d'hypothèses persistant. Déclencher sur "arbor loop", "recherche autonome", "hypothesis tree", "optimise avec Arbor", ou en préfixe de toute loop d'optimisation.
---

# Skill — arbor-research

> Adapté de [Arbor](https://github.com/RUC-NLPIR/Arbor) — *Toward Generalist Autonomous Research via Hypothesis-Tree Refinement* (Jin et al., 2026).  
> Licence originale : Apache 2.0. Cette skill est une adaptation PKA, pas un fork.

## Concept

Arbor-research transforme une loop d'optimisation PKA en **recherche cumulative**. Au lieu de cycles isolés qui redémarrent de zéro, un **arbre d'hypothèses** persiste entre les cycles : les idées qui marchent sont récoltées, celles qui échouent sont élaguées, et les insights se propagent pour que les tentatives suivantes partent plus intelligentes.

## Architecture : Dobby = Coordinator, Spécialistes = Executors

Arbor sépare deux rôles. Dans PKA, ils sont naturels :

| Rôle Arbor | Rôle PKA | Responsabilité |
|---|---|---|
| **Coordinator** | **Dobby** 🦉 | Proposer des hypothèses, gérer l'arbre, décider quelle branche explorer |
| **Executor** | **Spécialiste PKA** | Implémenter, mesurer, rapporter le résultat brut |

Dobby **ne fait pas** le travail d'exécution. Il orchestre, observe les résultats, et décide.

## La boucle OBSERVE → IDEATE → DECIDE

```
┌─────────────────────────────────────────────────────┐
│  OBSERVE      IDEATE        DECIDE        EXECUTE   │
│  ────────     ──────        ──────        ───────   │
│  Analyser   → Proposer   →  Choisir   →  Déléguer   │
│  échecs       hypothèses    branche      au spé      │
│     ↑                                        │       │
│     └────────── insight ←── résultat ────────┘       │
└─────────────────────────────────────────────────────┘
```

### OBSERVE — Comprendre avant de proposer

**Ne jamais sauter cette phase.** Le défaut du LLM est de proposer des solutions avant d'avoir compris le problème.

1. Lister les **cas d'échec concrets** (pas des généralités)
2. Classifier par **classe de bottleneck** (pas par instance) :
   - Mauvaise représentation (l'info est là mais inutilisable)
   - Mauvais raisonnement (l'info est correcte, le traitement non)
   - Mauvaise condition d'arrêt (trop tôt, jamais)
   - Mauvaise métrique (proxy ≠ vrai objectif)
   - Mauvais espace d'action (aucune action disponible ne résout le cas)
   - Mauvaise attribution de crédit (incapable de dire quelle étape a échoué)
3. Identifier les **hypothèses cachées** du système actuel — qu'est-ce que le trunk considère comme acquis, et qui pourrait être faux ?

### IDEATE — Proposer des hypothèses, pas des tweaks

Utiliser la discipline « Principal Investigator » :

- **MÉCANISME, pas objectif.** « Verifier-guided beam search » est une hypothèse. « Être plus robuste » est un vœu.
- **10×, pas 10%.** Si l'idée fonctionnait parfaitement, déplacerait-elle le benchmark d'au moins 1σ sur une CLASSE de problèmes ?
- **Test des 2 pages.** Un chercheur pourrait-il décrire, motiver et évaluer cette idée en 2 pages ? Si non, c'est une feature request, pas une hypothèse de recherche.

**Filtre anti-pseudo-idées (obligatoire avant soumission) :**
- Le changement peut-il s'exprimer comme un seul paramètre / knob ? → ❌
- Est-ce « plus de X » (plus de retries, plus de contexte, modèle plus gros) ? → ❌
- L'hypothèse décrit-elle un objectif au lieu d'un mécanisme ? → ❌
- Recouvre-t-elle un nœud déjà élagué sans contre-argument explicite ? → ❌

**Format d'hypothèse canonique :**
> Nous pensons que **[MÉCANISME]** aide parce que **[HISTOIRE CAUSALE liée au bottleneck]**,
> et nous saurons que ça marche si **[OBSERVABLE sur les données de dev]**.

### DECIDE — Choisir quoi tester

Parmi les hypothèses survivantes, choisir en fonction de :
1. **Diversité vs siblings** — cette hypothèse attaque-t-elle un axe différent des nœuds existants ?
2. **Coût estimé** — combien de cycles/time/budget pour un test ?
3. **Upside potentiel** — si ça marche, quel impact ?
4. **Risque de conflit** — contredit-elle un insight déjà acquis ? Si oui, le contre-argument est-il solide ?

Une seule hypothèse sharp vaut mieux que cinq variantes reformulées.

### EXECUTE — Déléguer, ne pas faire

Dobby délègue au spécialiste approprié :
- **Forge** pour les optimisations de code
- **Fourmi** pour les tests hardware
- **Musaraigne** pour les optimisations TinyML
- **Trace** pour le SEO
- **Sigma** pour les modèles financiers

Le spécialiste reçoit l'hypothèse, le contrat d'évaluation, et un budget (temps/cycles). Il rapporte le résultat **brut** — Dobby interprète.

## L'arbre d'hypothèses

Chaque run de recherche maintient un arbre dans `.arbor/research/<project>/` :

```
.arbor/research/wildnexus/
├── tree.json          # Arbre canonique (machine-readable)
├── TREE.md            # Vue humaine
├── events.jsonl       # Log événementiel
└── sessions/          # Une session par run
    └── 2026-06-18_power-optim/
        ├── hypothesis.md
        ├── result.md
        └── artifacts/
```

### Structure d'un nœud

```json
{
  "id": "1.2",
  "parent_id": "1",
  "depth": 2,
  "hypothesis": "Nous pensons que le buck converter TPS6280...",
  "status": "done",
  "insight": "Le TPS6280 réduit le ripple de 40% mais ajoute 2µA en veille",
  "score": 47.2,
  "code_ref": "branch: exp/tps6280-v2",
  "eval_status": "scored"
}
```

### Statuts

| Statut | Signification | Action suivante |
|---|---|---|
| `pending` | Hypothèse formulée, pas encore testée | → Assigner à un Executor |
| `running` | Test en cours | Attendre le résultat |
| `done` | Test terminé, scored | → DECIDE : merge ou prune ? |
| `pruned` | Hypothèse rejetée (échec ou obsolète) | Ne pas revisiter sans contre-argument |
| `merged` | Succès confirmé, intégré au trunk | Le score devient la nouvelle baseline |
| `needs_retry` | Échec technique (pas conceptuel) | Relancer avec corrections |

### Opérations sur l'arbre

- **merge(node)** : le nœud devient le nouveau trunk. Son score = nouvelle baseline. Les siblings non-merged sont automatiquement élagués si leur hypothèse est invalidée.
- **prune(node, reason)** : rejeter une branche avec une raison enregistrée. Protège contre la répétition.
- **branch(parent, hypothesis)** : créer un nouvel enfant sous un nœud parent.
- **propagate_insight(node)** : l'insight d'un nœud terminé est remonté au parent et aux siblings pending pour qu'ils en tiennent compte.

## Intégration avec les loops PKA existantes

### Mode « augmenté » (une loop existante + Arbor)

Quand Dobby lance une loop existante en mode Arbor :

```
dobby → [M5] lance bench-loop en mode arbor-research sur SOP-03
```

1. Dobby charge `arbor-research` + la skill de la loop cible
2. OBSERVE : Dobby lit le dernier rapport de la loop, identifie les bottlenecks
3. IDEATE : Dobby formule 1-3 hypothèses avec la discipline PI
4. DECIDE : Dobby choisit la meilleure hypothèse
5. EXECUTE : Dobby délègue au spécialiste avec l'hypothèse + contrat d'évaluation
6. Le spécialiste exécute et rapporte
7. Dobby met à jour l'arbre (merge/prune/branch)
8. Retour à OBSERVE

La loop native continue de fonctionner normalement — Arbor ajoute la couche de décision cumulative par-dessus.

### Mode « standalone » (recherche pure Arbor)

Pour un problème qui n'a pas de loop PKA dédiée :

```
dobby → lance arbor-research sur "optimiser la latence de détection PIR"
```

Dobby crée un arbre frais, exécute la boucle OBSERVE→IDEATE→DECIDE, et délègue aux spécialistes appropriés selon les besoins (Fourmi pour le hardware, Musaraigne pour le ML, Forge pour le code).

## Convergence

La recherche s'arrête quand :
1. **Convergence dure** : `N` cycles consécutifs sans amélioration > seuil (défaut : 3 cycles, seuil 1%)
2. **Budget épuisé** : nombre max de cycles atteint (défaut : 10)
3. **Convergence sémantique** : les 3 dernières hypothèses proposées sont toutes des variantes mineures d'hypothèses déjà testées
4. **Merge manuel** : JCH valide le résultat et termine le run

## Fichiers de la skill

| Fichier | Rôle |
|---|---|
| `SKILL.md` | Ce fichier — architecture et principes |
| `arbor-loop.md` | Protocole pas-à-pas pour exécuter une boucle Arbor |
| `idea-tree-template.md` | Template pour créer un arbre d'hypothèses |
| `plugin-example/wildnexus_hardware.yaml` | Exemple de plugin domaine pour WildNexus hardware |

## Déclencheurs

- "arbor loop", "arbor research"
- "recherche autonome", "hypothesis tree"
- "optimise avec Arbor", "passe en mode Arbor"
- "OBSERVE → IDEATE → DECIDE"
- Quand une loop existante est lancée avec le flag `--arbor` ou le préfixe "arbor:"
