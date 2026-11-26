---
name: bench-loop
description: Boucle autonome d'exécution de SOPs hardware — Fourmi suit SOP → mesure → dans spec ? → commit → SOP suivante. Déclencher sur "bench loop", "test loop", "SOP loop", "exécute les SOPs en boucle". Inspiré de wildnexus-benchmark-loop, forge-loop et AutoResearch.
---

# Skill — bench-loop

> Variante test hardware de `wildnexus-benchmark-loop`. Exécute une séquence de SOPs M-02, mesure chaque étape, valide contre les specs, et escalade les hors-spécifications. Le pattern AutoResearch appliqué au banc de test.

## Architecture 3 fichiers adaptée au banc de test

| Fichier AutoResearch | Rôle | Équivalent Banc | Modifiable ? |
|---------------------|------|-----------------|-------------|
| `program.md` | Instructions de la boucle | Brief Fourmi + plan de test | ❌ Immuable |
| `train.py` | Code à optimiser | Configuration DUT, câblage, firmware | ✅ Oui (entre tests) |
| `prepare.py` | Métrique d'évaluation | SOP de mesure | ❌ Immuable |

## Déclencheurs

- "bench loop", "test loop"
- "SOP loop", "exécute les SOPs"
- "passe le banc de test"
- "vérifie le DUT contre les specs"

## Spécificité : loop séquentielle, pas itérative

Contrairement aux autres loops PKA, `bench-loop` est **séquentielle** : elle enchaîne les SOPs dans l'ordre, plutôt que d'itérer sur la même. Le but n'est pas d'optimiser mais de **valider** chaque étape.

```
SOP-01 → mesure → PASS ──→ SOP-02 → mesure → PASS ──→ SOP-03 → ...
                → FAIL ──→ escalade
```

Chaque SOP est un `prepare.py` différent. Si l'une échoue, la séquence s'arrête.

## SOPs M-02 disponibles

| Ordre | SOP | Métrique | Seuil PASS |
|-------|-----|----------|-----------|
| 1 | SOP-01 | Alive check ESP32 | Boot OK, LED clignote |
| 2 | SOP-02 | Deep sleep 30s | Wake OK, timestamp valide |
| 3 | SOP-03 | PPK2 deep sleep current | < 50 µA |
| 4 | SOP-04 | Wake short 20 cycles | < 5 mJ/cycle, 100% wake |
| 5 | SOP-05 | Simulation cycle événement | < 100 mJ/event, log cohérent |
| 6 | SOP-06 | MicroSD read/write | Read/Write OK, < 2s |
| 7 | SOP-07 | LoRa TX | TX OK, RSSI > -120 dBm |
| 8 | SOP-08 | Caméra OV5640 | Capture OK, résolution correcte |
| 9 | SOP-09 | PIR EKMB | Trigger < 2s, veille < 10 µA |
| 10 | SOP-10 | Batterie AA Buck | Vout stable 3.3V ±5% |
| 11 | SOP-11 | Edge AI benchmark | Latence < 500 ms, accuracy > 85% |
| 12 | SOP-12 | Micro-provisioning | Flash OK, config persistante |

## Procédure

### 1. Préparer le banc

- Vérifier le matériel : PPK2, câblage, DUT
- Règles de sécurité SOP-03 actives (jamais USB + PPK2)
- Démarrer le logging (timestamp, mesures brutes)

### 2. Exécution séquentielle

```
POUR CHAQUE SOP dans l'ordre :
  1. Lire la SOP complète (règles de sécurité d'abord)
  2. Configurer le matériel selon la SOP
  3. Exécuter la mesure
  4. Comparer au seuil PASS/FAIL
  5. Enregistrer le résultat (mesure brute + verdict) dans team.db
  6. Si PASS → SOP suivante
     Si FAIL → arrêter la séquence, escalader
```

### 3. Sortie de séquence

| Issue | Action |
|-------|--------|
| **Toutes les SOPs PASS** | ✅ DUT validé. Générer le rapport de conformité complet |
| **SOP N FAIL** | 🛑 Arrêter. Générer le rapport d'échec : SOP, mesure, écart vs spec |
| **Erreur hardware** | 🛑 Arrêter immédiatement. Ne pas insister |
| **Règle de sécurité violée** | 🛑 Arrêt d'urgence. Documenter l'incident |

## Règles absolues

- **Respecter l'ordre des SOPs.** Chaque SOP a des prérequis (ex: SOP-03 nécessite SOP-02 réussi).
- **Ne jamais sauter une SOP.** Même si elle semble triviale.
- **Règles de sécurité > tout.** SOP-03 règles 1-6 sont non-négociables.
- **Mesures brutes obligatoires.** Chaque mesure est enregistrée, pas juste le verdict PASS/FAIL.
- **Une seule modification entre SOPs.** Si on change le câblage, documenter quel câble.
- **Ne jamais modifier une SOP.** Les procédures de test sont immuables.

## Format du rapport

```markdown
# BANC DE TEST — Rapport DUT #<id>

**Date :** YYYY-MM-DD
**Opérateur :** Fourmi 🐜
**DUT :** ESP32-S3 NULA DeepSleep
**Firmware :** <hash>

| SOP | Métrique | Mesure | Seuil | Verdict |
|-----|----------|--------|-------|---------|
| SOP-01 | Boot | OK | OK | ✅ PASS |
| SOP-02 | Wake | 32s | 30s ±5s | ✅ PASS |
| SOP-03 | I_deep_sleep | 42 µA | < 50 µA | ✅ PASS |
| ... | ... | ... | ... | ... |

**Verdict final :** ✅ 12/12 PASS / ⚠️ X/12 PASS (échec SOP-N)
**Durée totale :** XX minutes
```

## Intégration brief

```yaml
# Dans le brief Fourmi :
bench_loop: true
sop_sequence: "full"   # full | partial (liste)
dut_id: "NULA-001"
firmware_hash: "abc123"
stop_on_fail: true
```

## Skills liés

- **`wildnexus-benchmark-loop`** — Variante optimisation firmware (itérative, pas séquentielle)
- **`forge-loop`** — Pattern code review original
- **`wildnexus-governance`** — Validation procédure de test
- **`wildnexus-bom`** — Si un composant échoue systématiquement → BOM à revoir
- **`brief`** — Génération de brief avec `bench_loop: true`

## Références

- **SOPs M-02 WildNexus** — `03_P0_ENGINEERING/PROTOCOLES/SOP-01` à `SOP-12`
- **AutoResearch** (Karpathy, 2025) — Architecture 3 fichiers, eval immuable
- **Nordic PPK2** — Power Profiler Kit II, mesures µA précises
