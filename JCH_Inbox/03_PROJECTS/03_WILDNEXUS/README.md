# WILDNEXUS — Projet ombrelle (bioacoustique de terrain)

> Regroupe trois sous-projets issus de la réorganisation du 2026-10-20
> (fusion des anciens `09_InsectNet` et `12_NEXUS_ACOUSTIC` sous `03_WILDNEXUS`).
> Ce document est la **carte de convergence** : comment les 3 sous-projets
> s'articulent, et où vivent les outils et données partagés.

## Les 3 sous-projets

| Sous-projet | Périmètre | Rôle dans la chaîne |
|-------------|-----------|---------------------|
| **WILDNEXUS/** | Device P0 terrain (ESP32-S3, caméra PIR, micros stéréo, LoRa) | **Capture** l'audio localement |
| **INSECTNET/** | Classification acoustique des orthoptères (~30 spp, InsectNet-CNN) | **Classe** les insectes |
| **NEXUS_ACOUSTIC/** | BirdNET (oiseaux 200 spp), TweetyBERT, AmphibianNet, LEAFNET | **Classe** oiseaux/amphibiens + bioélectrique |

## La chaîne de valeur (capture → classification)

```
[WILDNEXUS device] -- ADR-013 (micros 2× SPH0645LM4H-B I2S stéréo)
       │              ADR-016 (cycle firmware audio : FFT 15 min + clip WAV 60 min)
       │              ADR-017 (schéma métadonnées audio)
       ▼
  clips WAV standardisés
       ├──────────────► INSECTNET/     → InsectNet-CNN (orthoptères)
       └──────────────► NEXUS_ACOUSTIC/ → BirdNET / TweetyBERT / SoundPlot / AmphibianNet
```

Les ADR (dans `WILDNEXUS/02_DECISIONS/ADR/`) définissent le **contrat amont**
qui alimente les deux pipelines de classification en aval.

## Outils partagés (déjà centralisés au niveau repo)

| Outil | Emplacement | Usage |
|-------|-------------|-------|
| Pipeline InsectNet (13 scripts) | `scripts/insectnet*.py` + `scripts/insectnet.py` | inventory, download, auto-qc, spectrogrammes, segmentation, review |
| Client Xeno-Canto | `bin/xcapi` (wrapper → `.venv`, package `xenocanto-api`) | téléchargement audio insectes |
| BirdNET (externe, Cornell) | outil tiers | classification oiseaux (Analyzer + RPi + BirdNET-Lite embarqué) |

> ⚠️ Ces outils vivent dans `scripts/` et `bin/` (convention PKA), **pas** dans
> les sous-projets. Ne pas les dupliquer ici.

## Données partagées

- **InsectSet459** — physiquement dans `NEXUS_ACOUSTIC/datasets/InsectSet459/`,
  évalué par InsectNet (`INSECTNET/01_RESEARCH/insectset459-evaluation.md`).
  C'est le dataset commun des deux pipelines de classification.

## Méthodologie partagée

- **QC / segmentation audio** — design dans `docs/superpowers/plans/`
  (`2026-05-24-insectnet-qc-segmentation.md` + `specs/...design.md`),
  journaux dans `INSECTNET/04_PIPELINE/`.
- **Skill** : `bioacoustics-qc-playbook` — conventions de curation communes à
  InsectNet *et* NEXUS_ACOUSTIC.

## Liens

- Index device : `WILDNEXUS/INDEX.md`
- Index InsectNet : `INSECTNET/thread-insectnet.md`
- Index Nexus : `NEXUS_ACOUSTIC/INDEX.md`
- Gouvernance P0 : `WILDNEXUS/00_GOVERNANCE/`
