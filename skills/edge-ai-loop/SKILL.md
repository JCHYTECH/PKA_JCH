---
name: edge-ai-loop
description: Boucle autonome d'optimisation de modèles TinyML — Musaraigne modifie dataset/modèle → Edge Impulse benchmark → accuracy/latence → si meilleur = commit. Déclencher sur "edge ai loop", "optimise le modèle", "TinyML loop", "FOMO loop". Inspiré de wildnexus-benchmark-loop et AutoResearch.
---

# Skill — edge-ai-loop

> Variante ML de `wildnexus-benchmark-loop`. Le pattern AutoResearch appliqué à l'entraînement et l'optimisation de modèles TinyML : FOMO, MobileNet, classification binaire sur ESP32-S3.

## Architecture 3 fichiers adaptée au Edge AI

| Fichier AutoResearch | Rôle | Équivalent Edge AI | Modifiable ? |
|---------------------|------|--------------------|-------------|
| `program.md` | Instructions de la boucle | Brief Musaraigne + quality gate | ❌ Immuable |
| `train.py` | Code/data à optimiser | Dataset, architecture modèle, hyperparamètres | ✅ Oui |
| `prepare.py` | Métrique d'évaluation | Edge Impulse benchmark (SOP-11) | ❌ Immuable |

## Déclencheurs

- "edge ai loop", "TinyML loop"
- "optimise le modèle FOMO"
- "améliore la détection"
- "benchmark loop modèle"

## Métriques disponibles

| Métrique | Outil | Seuil P0 WildNexus | Risque si mauvaise métrique |
|----------|-------|--------------------|------------------------------|
| **Accuracy** | Edge Impulse / test set | > 85% | Optimiser pour 100% → overfitting |
| **Inference latency** | ESP32-S3 benchmark | < 500 ms | Optimiser pour 0 ms → modèle vide |
| **Model size (flash)** | Edge Impulse | < 512 KB | Optimiser pour 0 → pas de modèle |
| **RAM usage** | Edge Impulse | < 256 KB | Optimiser pour 0 → pas d'inférence |
| **False positive rate** | Test set (pas-animal) | < 10% | Optimiser pour 0 → faux négatifs explosent |
| **False negative rate** | Test set (animal) | < 15% | Optimiser pour 0 → batterie vidée par faux positifs |
| **Energy per inference** | PPK2 (SOP-11) | < 50 mJ | — |

> ⚠️ **Le trade-off accuracy vs latence est le piège classique.** Un modèle 99% précis mais 3s d'inférence est inutilisable. Un modèle 50ms mais 60% précis est inutile. Toujours définir des contraintes couplées.

## Principe

```
Brief Musaraigne → modifie dataset/modèle → entraîne → benchmark → métriques
                                                                      │
                                                           meilleur ──┤─── commit
                                                           pire ──────┤─── revert
                                                           (max N itérations)
```

## Procédure

### 1. Définir les contraintes couplées

```yaml
metrics:
  - name: "accuracy"
    target: "> 85%"
    floor: "> 75%"
  - name: "inference_latency"
    target: "< 500 ms"
    ceiling: "< 2000 ms"
max_iterations: 5
time_budget: 900    # Entraînement + benchmark (plus long que firmware)
```

### 2. Boucle d'optimisation

```
ITÉRATION 1..5 :
  1. Lire les métriques actuelles
  2. Formuler une hypothèse :
     - Dataset : plus d'exemples de faux positifs
     - Architecture : moins de couches, quantification INT8
     - Hyperparams : learning rate, batch size, epochs
  3. Modifier (dataset / config / architecture)
  4. Entraîner (time budget fixe)
  5. Benchmark sur ESP32-S3
  6. Toutes les métriques meilleures ET dans les bornes → commit
     Une métrique pire OU hors bornes → revert
```

### 3. Sortie de boucle

| Issue | Action |
|-------|--------|
| **Toutes les métriques dans les bornes** | ✅ Commit. Mettre à jour le modèle dans le projet Edge Impulse |
| **5 itérations sans convergence** | ⚠️ Escalader. Le meilleur modèle est documenté |
| **Overfitting détecté** (accuracy train ≫ test) | 🛑 Arrêter. Le dataset est probablement trop petit ou biaisé |
| **Modèle trop lent malgré bonne accuracy** | 🛑 Arrêter. Envisager une migration MCU (ADR-010) |

## Règles absolues

- **Ne jamais modifier le script de benchmark.** Edge Impulse et SOP-11 sont immuables.
- **Split train/val/test par site/caméra, pas par image.** Sinon overfitting invisible.
- **Toujours mesurer sur hardware réel.** La simulation Edge Impulse n'est pas le ESP32-S3.
- **Dataset minimum : 2000 images.** En dessous, la boucle va overfitter, pas apprendre.
- **Une seule modification par itération.** Si on change dataset + archi + hyperparams en même temps, impossible de savoir ce qui a marché.
- **Budget temps fixe.** Même temps d'entraînement par expérience → comparaison équitable.

## Contraintes ML

| Contrainte | Valeur | Raison |
|-----------|--------|--------|
| Temps entraînement FOMO | ~5-10 min | Edge Impulse cloud |
| Temps inférence ESP32-S3 | ~200-500 ms | Dépend du modèle |
| Images minimum dataset | 2000 | Évite overfitting immédiat |
| Split | 70/15/15 par site | Généralisation inter-sites |
| Classes | Binaire uniquement P0 | Animal / pas-animal |

## Intégration brief

```yaml
# Dans le brief Musaraigne :
edge_ai_loop: true
metrics:
  - name: "accuracy"
    target: "> 85%"
    floor: "> 75%"
  - name: "inference_latency"
    target: "< 500 ms"
    ceiling: "< 2000 ms"
max_iterations: 5
time_budget: 900
```

## Exemple concret — Optimisation FOMO binaire

```
Métriques couplées :
  Accuracy : > 85% (floor > 75%)
  Latence : < 500 ms (ceiling < 2000 ms)

Itération 1 :
  Baseline : accuracy 78%, latence 320 ms
  Hypothèse : ajouter plus d'exemples de branches/vent dans pas-animal
  Modification : +200 images fond forêt perturbé
  Résultat : accuracy 84% (+6), latence 340 ms (+20)
  ✅ Accuracy meilleure, latence dans bornes → commit

Itération 2 :
  Hypothèse : quantification INT8 au lieu de FP32
  Résultat : accuracy 83% (-1), latence 180 ms (-160)
  ⚠️ Accuracy légèrement pire mais latence bien meilleure
  → Commit (trade-off acceptable, accuracy > floor)

Itération 3 :
  Hypothèse : réduire input 320×240 → 96×96 (FOMO natif)
  Résultat : accuracy 81%, latence 95 ms
  ⚠️ Accuracy proche du floor
  → Garder le modèle de l'itération 2. SORTIE (3 itérations, proche des bornes)
```

## Skills liés

- **`wildnexus-benchmark-loop`** — Variante firmware (même pattern, hardware différent)
- **`forge-loop`** — Pattern code review original
- **`wildnexus-governance`** — Validation des métriques avant activation
- **`bioacoustics-qc-playbook`** — Curation dataset bioacoustique
- **`brief`** — Génération de brief avec `edge_ai_loop: true`

## Références

- **AutoResearch** (Karpathy, 2025) — Architecture 3 fichiers, budget temps fixe
- **FOMO** (Edge Impulse) — TinyML object detection sur microcontrôleur
- **SOP-11** (WildNexus M-02) — Benchmark Edge AI sur ESP32-S3
- **ADR-010** — Contrainte latence < 2s, décision MCU si dépassement
- **Brief Musaraigne 2026-06-17** — Dataset FOMO WildNexus
