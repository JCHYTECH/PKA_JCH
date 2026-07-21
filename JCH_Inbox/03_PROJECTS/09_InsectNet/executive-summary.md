# InsectNet — Executive Summary

> Document externe — partenaires recherche, financeurs académiques.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**InsectNet est un pipeline de classification automatique d'insectes par deep learning, exploitant xeno-canto, GBIF et les datasets académiques de référence.**

---

## Le problème

L'identification automatique des insectes par l'image et le son est en retard d'une génération sur celle des oiseaux :
- Moins de datasets annotés (les insectes sont plus difficiles à photographier)
- Moins de modèles spécialisés (BirdNET n'a pas d'équivalent insecte mature)
- Grande diversité d'espèces (>1M décrites) rendant la classification fine difficile

---

## Notre approche

Un pipeline modulaire qui combine :
1. **xcapi** — extraction de données acoustiques depuis xeno-canto
2. **Preprocessing** — segmentation spectrogrammes, filtrage par fréquence
3. **Modèle** — architecture CNN/Transformer fine-tunée sur données entomologiques
4. **Migration M5 → M1** — exploitation du GPU 32GB Apple Silicon pour l'entraînement

---

## Convergence avec NEXUS_ACOUSTIC

Le projet converge naturellement avec NEXUS_ACOUSTIC :
- **InsectSet459** (26K fichiers, 459 espèces) — dataset partagé
- **TweetyBERT** — modèle transformer applicable aux deux projets
- **SoundPlot** — visualisation commune

---

## Statut

| Composant | Statut |
|-----------|--------|
| Pipeline xcapi | 🟢 Validé |
| Preprocessing | 🟢 Prêt |
| Migration M5→M1 | 🟡 Bloqué — accès rsync M1 à configurer |

---

## Prochaine étape

Configurer l'accès rsync du Mac M1 au dépôt PKA pour migrer l'entraînement.

---

*Document destiné à un public académique. Pipeline détaillé : `09_InsectNet/`*
