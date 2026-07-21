# Thread — NEXUS_ACOUSTIC

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-07-03 — Thread file créé
> **Statut** : ⚪ P1 deferred → 🟡 en mouvement

---

## Vue d'ensemble

Bioacoustique — pipeline classification/visualisation chants d'insectes. TweetyBERT + InsectSet459 + SoundPlot. Architecture cible : ESP32 VAD → RPi 5 BirdNET-Lite → M5 TweetyBERT. WildLens « Sound Portraits » proposé.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟡 | Mouvement : InsectSet459 téléchargé sur M5, TweetyBERT analysé, roadmap juillet-septembre |
| Dataset | 🟢 | InsectSet459 — Train (48 GB ✅), Validation (15 GB ✅), Test (16 GB en cours) |
| Pipeline | 🟡 | TweetyBERT + SoundPlot analysés, schéma JSON Forge prêt |
| Visualisation | 🟡 | SoundPlot (open-source) validé comme alternative TouchDesigner |
| Matériel | ⚪ | P1 deferred — stations RPi à définir |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-07-03 | Roadmap NEXUS_ACOUSTIC : P0 juillet (download+install), P1 août (fine-tuning+dashboard), P2 septembre (pipeline auto) | Analyse INTERSPECIES SONGS + Lucio Arese |
| 2026-07-03 | TweetyBERT confirmé sur M5 (GPU Apple Silicon), pas RPi 5 (OOM) | Analyse Musaraigne |
| 2026-06-19 | NEXUS_ACOUSTIC extrait de WildNexus en projet autonome | Réorganisation |

---

## Prochaine étape

**Action** : Installer TweetyBERT sur M5 + adapter preprocessing orthoptères (fmin=5000)
**Deadline** : Juillet 2026
**Responsable** : Clio, Musaraigne

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-07-03 | Analyse TweetyBERT + InsectSet459 + Lucio Arese + BIRDER | `TEAM_Inbox/2026-07-03_dobby_analyse-interspecies-songs.md` |
| 2026-06-23 | BirdNET analysé, double canal spec, geomodel GBIF | — |
| 2026-06-19 | Extraction de WildNexus, Document Unique de Projet | `TEAM_Inbox/2026-06-19_dobby_analyse-reorganisation-wildnexus.md` |

---

## Liens

- INDEX : `03_PROJECTS/12_NEXUS_ACOUSTIC/`
- Datasets : `03_PROJECTS/12_NEXUS_ACOUSTIC/datasets/InsectSet459/`
- Analyses : `TEAM_Inbox/2026-07-03_dobby_analyse-*.md`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*
