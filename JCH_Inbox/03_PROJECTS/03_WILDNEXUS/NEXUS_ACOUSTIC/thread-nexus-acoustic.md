# Thread — NEXUS_ACOUSTIC

> Living document maintenu par Dobby 🦉.
> **Dernière mise à jour** : 2026-11-05 — alignement sur le gel WildNexus.
> **Statut** : ⚪ **gelé avec le projet ombrelle WildNexus** ; anciennes échéances de juillet suspendues.

## Gouvernance

Le gel ombrelle et la suspension de SOP-10 priment sur la roadmap historique ci-dessous. Référence : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/00_GOVERNANCE/Start.md`. Aucune installation, aucun téléchargement et aucune reprise matérielle ne sont lancés par ce thread.

## Vue d'ensemble

Recherche bioacoustique : classification et visualisation de chants d'insectes avec TweetyBERT, InsectSet459 et SoundPlot. Architecture envisagée : ESP32 VAD → RPi 5 BirdNET-Lite → M5 TweetyBERT. Piste éditoriale WildLens « Sound Portraits » également historique.

## État documenté au 03/07, non revérifié au 05/11

| Axe | Statut courant | Historique à revalider |
|-----|----------------|------------------------|
| Global | ⚪ gelé | Roadmap juillet–septembre dépassée, non active |
| Dataset | ⚪ non revérifié | InsectSet459 Train 48 GB et Validation 15 GB annoncés téléchargés ; **Test 16 GB annoncé « en cours » le 03/07 uniquement** — aucun état actuel de téléchargement confirmé |
| Pipeline | ⚪ gelé | TweetyBERT + SoundPlot analysés ; schéma JSON décrit comme prêt |
| Visualisation | ⚪ gelé | SoundPlot étudié comme alternative à TouchDesigner |
| Matériel | ⚪ gelé | Stations RPi à définir ; aucune reprise P1 |

## Décisions et historique

| Date | Élément | Lecture actuelle |
|------|---------|------------------|
| 2026-07-03 | Roadmap P0 juillet, P1 août, P2 septembre | Historique dépassé ; à replanifier seulement après reprise |
| 2026-07-03 | TweetyBERT envisagé sur M5 plutôt que RPi 5 | Analyse historique à revalider |
| 2026-06-19 | NEXUS_ACOUSTIC distingué dans l'organisation WildNexus | Structure documentaire conservée, gel ombrelle commun |

## TTD — Pending

**Aucune exécution tant que WildNexus est gelé.**

- [ ] **Au signal de JC seulement** Vérifier les datasets réellement présents et leur intégrité, contrôler l'installation TweetyBERT, puis reconstruire une roadmap et des responsabilités.

## TTD — Done

- [x] 2026-11-05 · Gel ombrelle appliqué ; statuts techniques et téléchargement Test explicitement distingués des preuves actuelles.

## Historique sessions

| Date | Résumé | Livrable |
|------|--------|----------|
| 2026-11-05 | Gel ombrelle appliqué ; statuts techniques et téléchargement Test explicitement non revérifiés | `thread-nexus-acoustic.md`, `INDEX.md` |
| 2026-07-03 | Analyse TweetyBERT + InsectSet459 + Lucio Arese + BIRDER | `2026-07-03_dobby_analyse-interspecies-songs.md` |
| 2026-06-23 | Analyse BirdNET et double canal | — |
| 2026-06-19 | Réorganisation WildNexus | `TEAM_Inbox/_archive/2026-06-19_dobby_analyse-reorganisation-wildnexus.md` |

## Liens

- Gouvernance du gel : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/00_GOVERNANCE/Start.md`
- INDEX : `03_PROJECTS/03_WILDNEXUS/NEXUS_ACOUSTIC/INDEX.md`
- Datasets à revérifier : `03_PROJECTS/03_WILDNEXUS/NEXUS_ACOUSTIC/datasets/InsectSet459/`

---

*Les états de juillet sont des historiques, pas des preuves techniques actuelles.*
