# Thread — InsectNet

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-07-03 — Thread file créé
> **Statut** : 🟡 pipeline

---

## Vue d'ensemble

Classification automatique d'insectes par deep learning — pipeline xcapi → preprocessing → modèle. Plan migration M5 → M1 (plus de puissance GPU). Lié à NEXUS_ACOUSTIC via InsectSet459 et TweetyBERT.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟡 | Migration M1 en attente (accès rsync) |
| Pipeline | 🟢 | xcapi validé, preprocessing prêt |
| Migration | 🟡 | M5 → M1 — besoin accès M1 au dépôt PKA (rsync) |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-06-14 | Plan migration M5 → M1 | M1 32GB > M5 pour training |

---

## Prochaine étape

**Action** : Exécuter migration M1 (rsync accès)
**Deadline** : —
**Responsable** : Clio, Musaraigne

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-06-14 | Plan migration M5→M1, xcapi validé | — |

---

## Liens

- Dossier : `03_PROJECTS/03_WILDNEXUS/INSECTNET/`
- NEXUS_ACOUSTIC : `03_PROJECTS/03_WILDNEXUS/NEXUS_ACOUSTIC/` (InsectSet459 partagé)

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*
