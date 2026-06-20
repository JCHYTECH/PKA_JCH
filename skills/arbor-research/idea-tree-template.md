# Idea Tree Template

> Template pour créer un nouvel arbre d'hypothèses Arbor dans PKA.
> Copier ce fichier, remplacer les placeholders, sauver en `tree.json`.

## Arbre minimal (1 nœud ROOT)

```json
{
  "meta": {
    "project": "<PROJECT_SLUG>",
    "objective": "<OBJECTIF_1_PHRASE>",
    "created": "<ISO_DATE>",
    "baseline_score": null,
    "trunk_score": null,
    "max_cycles": 10,
    "convergence_threshold": 0.01,
    "convergence_patience": 3
  },
  "nodes": {
    "ROOT": {
      "id": "ROOT",
      "parent_id": null,
      "children_ids": [],
      "depth": 0,
      "hypothesis": "<DESCRIPTION_SYSTÈME_ACTUEL>",
      "status": "merged",
      "insight": "",
      "result": "",
      "score": null,
      "code_ref": null,
      "related_work": "",
      "eval_status": null,
      "stop_reason": null,
      "attempt": 1
    }
  }
}
```

## Arbre avec 1 hypothèse pending

```json
{
  "meta": {
    "project": "<PROJECT_SLUG>",
    "objective": "<OBJECTIF_1_PHRASE>",
    "created": "<ISO_DATE>",
    "baseline_score": <BASELINE_SCORE>,
    "trunk_score": <TRUNK_SCORE>,
    "max_cycles": 10,
    "convergence_threshold": 0.01,
    "convergence_patience": 3
  },
  "nodes": {
    "ROOT": {
      "id": "ROOT",
      "parent_id": null,
      "children_ids": ["1"],
      "depth": 0,
      "hypothesis": "<DESCRIPTION_SYSTÈME_ACTUEL>",
      "status": "merged",
      "insight": "",
      "result": "",
      "score": <BASELINE_SCORE>,
      "code_ref": null,
      "related_work": "",
      "eval_status": null,
      "stop_reason": null,
      "attempt": 1
    },
    "1": {
      "id": "1",
      "parent_id": "ROOT",
      "children_ids": [],
      "depth": 1,
      "hypothesis": "Nous pensons que <MÉCANISME> aide parce que <CAUSALITÉ>, et nous saurons que ça marche si <OBSERVABLE>.",
      "status": "pending",
      "insight": "",
      "result": "",
      "score": null,
      "code_ref": null,
      "related_work": "",
      "eval_status": null,
      "stop_reason": null,
      "attempt": 1
    }
  }
}
```

## Arbre mature (exemple après plusieurs cycles)

```json
{
  "meta": {
    "project": "wildnexus",
    "objective": "Réduire la consommation deep sleep du nœud caméra en dessous de 30 µA",
    "created": "2026-06-18",
    "baseline_score": 48.5,
    "trunk_score": 32.1,
    "max_cycles": 10,
    "convergence_threshold": 0.01,
    "convergence_patience": 3
  },
  "nodes": {
    "ROOT": {
      "id": "ROOT",
      "parent_id": null,
      "children_ids": ["1", "4"],
      "depth": 0,
      "hypothesis": "Configuration actuelle : ESP32-S3 + TPS63000 buck/boost, deep sleep config standard ESP-IDF",
      "status": "merged",
      "insight": "Baseline mesurée à 48.5 µA — au-dessus du seuil WildNexus de 30 µA",
      "result": "Mesure PPK2 : 48.5 µA moyen sur 10 cycles deep sleep 30s",
      "score": 48.5,
      "code_ref": "main",
      "related_work": "",
      "eval_status": "scored",
      "stop_reason": "finished",
      "attempt": 1
    },
    "1": {
      "id": "1",
      "parent_id": "ROOT",
      "children_ids": ["1.1", "1.2"],
      "depth": 1,
      "hypothesis": "Nous pensons qu'un régulateur LDO dédié pour le domaine always-on remplace le buck/boost en veille, parce que le buck/boost a un quiescent current élevé (25µA typique), et nous saurons que ça marche si la conso deep sleep passe sous 30µA.",
      "status": "merged",
      "insight": "Changer le régulateur a un effet majeur. Le TPS6280 est meilleur que le MCP1700 mais ajoute 2µA de ripple. Direction validée, explorer d'autres LDOs.",
      "result": "1.1 (MCP1700): 38.2 µA | 1.2 (TPS6280): 32.1 µA",
      "score": 32.1,
      "code_ref": "branch: exp/ldo-regulator",
      "related_work": "TPS6280 datasheet: quiescent 2.5µA typ",
      "eval_status": "scored",
      "stop_reason": "finished",
      "attempt": 1
    },
    "1.1": {
      "id": "1.1",
      "parent_id": "1",
      "children_ids": [],
      "depth": 2,
      "hypothesis": "Nous pensons que le MCP1700 LDO (1µA quiescent) réduit la conso veille, parce qu'il remplace le buck/boost en mode veille, et nous saurons que ça marche si la conso < 40µA.",
      "status": "pruned",
      "insight": "MCP1700: 38.2 µA. Mieux que baseline (48.5) mais dropout voltage trop élevé pour batterie AA. Direction intéressante mais composant inadapté.",
      "result": "38.2 µA — dropout voltage 625mV @ 100mA, trop élevé",
      "score": 38.2,
      "code_ref": "branch: exp/mcp1700",
      "related_work": "",
      "eval_status": "scored",
      "stop_reason": "finished",
      "attempt": 1
    },
    "1.2": {
      "id": "1.2",
      "parent_id": "1",
      "children_ids": [],
      "depth": 2,
      "hypothesis": "Nous pensons que le TPS6280 DCS-Control buck converter (2.5µA quiescent) résout le problème de dropout du MCP1700, parce que le buck maintient la régulation même avec batterie faible, et nous saurons que ça marche si la conso < 35µA.",
      "status": "merged",
      "insight": "32.1 µA — meilleur résultat. Proche du seuil 30µA. Le ripple ajouté (2µA) est acceptable.",
      "result": "32.1 µA — dropout non applicable (buck), ripple ±1.5mV",
      "score": 32.1,
      "code_ref": "branch: exp/tps6280",
      "related_work": "TPS6280 datasheet",
      "eval_status": "scored",
      "stop_reason": "finished",
      "attempt": 1
    },
    "4": {
      "id": "4",
      "parent_id": "ROOT",
      "children_ids": [],
      "depth": 1,
      "hypothesis": "Nous pensons que désactiver le PSRAM en deep sleep réduit la conso, parce que le PSRAM a un leakage current non négligeable même en retention mode, et nous saurons que ça marche si la conso baisse de > 10%.",
      "status": "pending",
      "insight": "",
      "result": "",
      "score": null,
      "code_ref": null,
      "related_work": "ESP32-S3 datasheet section 5.2.4: PSRAM power modes",
      "eval_status": null,
      "stop_reason": null,
      "attempt": 1
    }
  }
}
```

## Format de nœud

Chaque nœud a ces champs :

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | ✅ | Identifiant unique (ROOT, 1, 1.1...) |
| `parent_id` | string/null | ✅ | Parent (null pour ROOT) |
| `children_ids` | list | ✅ | Liste des IDs enfants |
| `depth` | int | ✅ | Profondeur (0 = ROOT) |
| `hypothesis` | string | ✅ | Hypothèse au format canonique |
| `status` | string | ✅ | pending/running/done/pruned/merged/needs_retry |
| `insight` | string | | Ce qui a été appris |
| `result` | string | | Résultat factuel de l'expérience |
| `score` | float/null | | Score mesuré (direction dépend du contexte) |
| `code_ref` | string/null | | Référence (branch, commit, fichier) |
| `related_work` | string | | Annotations de recherche (SearchAgent, datasheet) |
| `eval_status` | string/null | | scored/skipped/failed_to_run |
| `stop_reason` | string/null | | finished/max_turns/interrupted |
| `attempt` | int | | Nombre de tentatives (1 = première) |

## Conventions de nommage

- **ROOT** : toujours `"ROOT"` — le tronc initial
- **Niveau 1** : `"1"`, `"2"`, `"3"`... — hypothèses de premier niveau
- **Niveau 2** : `"1.1"`, `"1.2"`... — variantes d'une hypothèse
- **Niveau 3** : `"1.1.1"`, `"1.1.2"`... — sous-variantes

## Workflow de création

```bash
# 1. Créer le dossier projet
mkdir -p .arbor/research/<project>/sessions

# 2. Copier ce template
cp skills/arbor-research/idea-tree-template.md .arbor/research/<project>/

# 3. Créer tree.json à partir du template minimal
# (remplacer les placeholders)

# 4. Générer TREE.md
python3 -c "
import json
with open('.arbor/research/<project>/tree.json') as f:
    tree = json.load(f)
# Génération manuelle ou via script
"
```
