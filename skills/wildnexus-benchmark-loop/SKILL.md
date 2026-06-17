---
name: wildnexus-benchmark-loop
description: Boucle autonome d'optimisation firmware WildNexus contre benchmarks hardware — Forge modifie firmware → flash → PPK2/SOP mesure → si meilleur = commit. Déclencher sur "benchmark loop", "optimise le firmware", "PPK2 loop", "WildNexus auto-optimize". Inspiré de AutoResearch (Karpathy) et forge-loop.
---

# Skill — wildnexus-benchmark-loop

> Variante spécialisée de `forge-loop` pour les benchmarks hardware WildNexus. Le pattern AutoResearch (3 fichiers + budget temps fixe + eval immuable) appliqué aux mesures physiques : conso PPK2, latence inférence, portée LoRa, précision détection.

## Architecture 3 fichiers adaptée à WildNexus

| Fichier AutoResearch | Rôle | Équivalent WildNexus | Modifiable ? |
|---------------------|------|----------------------|-------------|
| `program.md` | Instructions de la boucle | Brief Forge + ADR + quality gate | ❌ Immuable (défini par Dobby) |
| `train.py` | Code à optimiser | Firmware ESP32-S3 (.ino, .cpp, config) | ✅ Oui |
| `prepare.py` | Métrique d'évaluation | SOP de mesure (PPK2, benchmark) | ❌ Immuable |

## Déclencheurs

- "benchmark loop sur <SOP>"
- "optimise le firmware WildNexus"
- "PPK2 loop", "auto-optimize conso"
- "lance la boucle de benchmark hardware"

## Métriques disponibles (SOP = prepare.py immuable)

| Métrique | SOP | Outil | Seuil P0 | Risque si mauvaise métrique |
|----------|-----|-------|----------|------------------------------|
| **Deep sleep current** | SOP-03 | PPK2 (Nordic) | < 50 µA | Optimiser pour 0 µA → ESP32 éteint, rien ne marche |
| **Wake cycle energy** | SOP-04 | PPK2 | < 5 mJ/cycle | Optimiser pour 0 → skip la capture image |
| **Event simulation** | SOP-05 | PPK2 + log | < 100 mJ/event | Optimiser pour 0 → faux négatifs |
| **LoRa TX power** | SOP-07 | Spectrum analyzer | < 100 mA peak | Optimiser pour 0 → pas de transmission |
| **Inference latency** | SOP-11 | Edge Impulse CLI | < 500 ms | Optimiser pour 0 ms → modèle vide |
| **Detection accuracy** | SOP-11 | Dataset FOMO | > 85% | Optimiser pour 100% → overfitting |
| **PIR trigger** | SOP-09 | PPK2 + logic analyzer | < 10 µA veille | — |

> ⚠️ **Le « bad metric » warning d'AutoResearch est critique ici.** Une métrique isolée pousse l'agent à l'extrême. Une boucle qui n'optimise QUE la conso produira un firmware qui ne détecte rien. Toujours définir des contraintes plancher/plafond par métrique.

## Principe

```
Brief Forge → modifie firmware → flash ESP32 → exécute SOP (immuable) → mesure
                                                                    │
                                                        meilleur ───┤─── commit
                                                        pire ───────┤─── revert
                                                        (max N itérations)
```

La métrique est une **mesure physique**, pas une opinion. Le PPK2 ne ment pas. Le benchmark ne ment pas. C'est l'avantage de WildNexus sur des loops subjectives : la physique est le juge ultime.

## Procédure

### 1. Sélectionner la SOP cible

- Une seule SOP par boucle (pas d'optimisation multi-objectif automatique en P0)
- Si plusieurs métriques sont nécessaires → plusieurs boucles séquentielles
- La SOP choisie devient le `prepare.py` immuable

### 2. Définir les bornes

Avant de lancer la boucle, fixer :

```yaml
metric: "deep_sleep_current"      # Nom de la métrique
sop: "SOP-03"                     # SOP de référence
target: "< 40 µA"                 # Objectif
floor: "> 10 µA"                  # Plancher (évite l'extrême)
unit: "µA"                        # Unité
direction: "minimize"             # minimize | maximize
max_iterations: 5                 # Plus d'itérations car mesures physiques lentes
time_budget: 600                  # Secondes par expérience (flash + mesure)
```

### 3. Boucle d'optimisation

```
ITÉRATION 1..5 :
  1. Forge lit le firmware actuel + les résultats de la dernière mesure
  2. Formule une hypothèse : « Si je baisse la fréquence CPU à 80 MHz, la conso deep sleep devrait baisser »
  3. Modifie le firmware (config, pin setup, sleep params)
  4. Flash ESP32
  5. Exécute la SOP (mesure PPK2, benchmark, etc.)
  6. Compare au baseline :
     - Meilleur + dans les bornes → commit
     - Pire OU hors bornes → revert
  7. Si objectif atteint → SORTIR
```

### 4. Sortie de boucle

| Issue | Action |
|-------|--------|
| **Objectif atteint** | ✅ Commit final. Mettre à jour l'ADR concerné et le BOM si impact composants |
| **5 itérations sans atteindre l'objectif** | ⚠️ Escalader à Dobby. Le meilleur résultat obtenu est documenté |
| **Hors bornes (plancher dépassé)** | 🛑 Arrêter immédiatement. L'agent a optimisé au détriment d'autre chose |
| **Erreur hardware** | 🛑 Arrêter. Ne pas insister sur un DUT défectueux |

## Règles absolues

- **Ne jamais modifier la SOP.** Les procédures de mesure sont immuables. Si une SOP semble inadaptée → escalader à Dobby pour révision.
- **Ne jamais optimiser sans bornes.** Chaque métrique a un plancher ET un plafond pour éviter l'extrême dangereux.
- **Respecter les règles de sécurité SOP.** SOP-03 règle #1 : jamais USB + PPK2 en même temps. L'agent ne peut pas outrepasser ces règles.
- **Une seule métrique par boucle.** L'optimisation multi-objectif automatique est trop risquée en P0.
- **Budget temps fixe.** Chaque expérience a le même temps alloué (flash + mesure + analyse). Pattern AutoResearch.
- **Documenter chaque itération.** Mesure brute, firmware hash, hypothèse testée.

## Contraintes hardware

| Contrainte | Valeur | Raison |
|-----------|--------|--------|
| Flash cycles ESP32 | ~100 000 garantis | Négligeable pour ≤ 5 itérations par boucle |
| PPK2 warm-up | 30 secondes | Laisser le DUT stabiliser avant la mesure |
| Temps de flash | ~15-30 secondes | Dépend de la taille du firmware |
| Cooldown entre expériences | 60 secondes | Éviter la dérive thermique |

## Intégration brief

Quand un brief Forge WildNexus inclut `benchmark_loop: true` :

```yaml
# Dans le brief Forge WildNexus :
benchmark_loop: true
metric: "deep_sleep_current"
sop: "SOP-03"
target: "< 40 µA"
floor: "> 10 µA"
max_iterations: 5
time_budget: 600
```

## Exemple concret — Boucle conso deep sleep

```
Métrique : deep_sleep_current
SOP : SOP-03 (PPK2 Source Meter)
Objectif : < 40 µA
Plancher : > 10 µA (en dessous = probablement pas en deep sleep)

Itération 1 :
  Baseline : 85 µA
  Hypothèse : désactiver le WiFi avant deep sleep
  Résultat : 52 µA ✅ (meilleur) → commit

Itération 2 :
  Hypothèse : configurer tous les GPIO en INPUT_PULLDOWN
  Résultat : 48 µA ✅ → commit

Itération 3 :
  Hypothèse : underclock à 40 MHz avant sleep
  Résultat : 35 µA ✅ → commit. Objectif atteint (< 40 µA) → SORTIE
```

## Gouvernance

- **Avant d'activer `benchmark_loop` :** valider la métrique avec `wildnexus-governance`. Une mauvaise métrique = optimisation toxique.
- **ADR impacté :** toute optimisation qui change un paramètre documenté dans un ADR doit être tracée.
- **BOM impact :** si l'optimisation permet de réduire un composant (ex: batterie plus petite), mettre à jour le BOM via `wildnexus-bom`.

## Skills liés

- **`forge-loop`** — Version généraliste pour la code review (même pattern, gate différente)
- **`wildnexus-governance`** — Validation de la métrique avant activation de la boucle
- **`wildnexus-adr`** — Tracer les décisions d'optimisation dans les ADR
- **`wildnexus-bom`** — Mettre à jour le BOM si l'optimisation change les specs composants
- **`brief`** — Pour générer le brief Forge avec `benchmark_loop: true`

## Références

- **AutoResearch** (Andrej Karpathy, 2025) — Architecture 3 fichiers, budget temps fixe, eval immuable, métrique objective
- **Grep Loop** (Ross Mike, 2026) — Code review autonome avec quality gate
- **SOP M-02 WildNexus** — `03_P0_ENGINEERING/PROTOCOLES/` — 12 SOPs définies, immuables
- **ADR-010** — Benchmark Edge AI, contrainte latence < 2s
