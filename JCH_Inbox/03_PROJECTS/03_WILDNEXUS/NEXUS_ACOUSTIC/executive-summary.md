# NEXUS ACOUSTIC — Executive Summary

> Document externe — investisseurs, partenaires, banquiers.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**Nexus Acoustic est une station bioacoustique autonome qui enregistre, classifie et visualise en 3D les chants d'insectes et d'oiseaux — un « radar de biodiversité acoustique ».**

---

## Le problème

Le déclin des insectes est massif et documenté, mais le suivi acoustique des orthoptères (criquets, sauterelles, grillons) et des cigales reste un angle mort de la recherche :
- Les enregistreurs audio existants (AudioMoth, Swift) sont généralistes — pas de classification embarquée
- L'analyse manuelle des spectrogrammes prend des heures par nuit d'enregistrement
- Les bioacousticiens passent plus de temps à traiter des données qu'à les interpréter

---

## Notre solution

Une station qui combine **3 technologies de pointe** :

1. **TweetyBERT** — Transformer self-supervised (University of Oregon, Patterns/Cell Press 2026) qui parse automatiquement les syllabes acoustiques **sans labels** — résolution 2.7 ms
2. **InsectSet459** — Dataset de référence (Nature Scientific Data 2026) : 26 298 fichiers, 226.6h, 459 espèces d'orthoptères et cigales
3. **SoundPlot** — Visualisation 3D temps/fréquence/amplitude qui transforme un chant d'insecte en **sculpture numérique**

Architecture : ESP32 (déclenchement) → Raspberry Pi 5 (classification BirdNET-Lite) → Mac M5 (TweetyBERT clustering 3D).

---

## Le marché

- **Recherche académique** : laboratoires d'écologie, bioacoustique, entomologie
- **Conservation** : suivis d'espèces protégées (directive Habitats EU)
- **Agriculture** : bio-indicateurs de santé des sols
- **Contenu éditorial** : sculptures 3D de chants → série WildLens « Sound Portraits »

---

## Roadmap

| Phase | Période | Jalon |
|-------|---------|-------|
| **P0** | Juillet 2026 | Télécharger InsectSet459 + installer TweetyBERT sur M5 |
| **P1** | Août 2026 | Fine-tuning + dashboard 3D |
| **P2** | Septembre 2026 | Pipeline automatisé + série WildLens « Sound Portraits » |

---

## État actuel

- InsectSet459 : Train (48 GB ✅) + Validation (15 GB ✅) téléchargés, Test (16 GB) en cours
- TweetyBERT : analysé, architecture cible confirmée (M5 GPU, pas RPi 5)
- SoundPlot : validé comme alternative open-source à TouchDesigner
- Schéma JSON standardisé par Forge

---

## L'équipe

- **Jean-Claude Havaux** — Zoologiste, direction scientifique
- **PKA_JCH** — Clio (science), Musaraigne (ML edge), Chouette (dashboard)

---

*Document destiné à un public externe. Analyse complète : `TEAM_Inbox/2026-07-03_dobby_analyse-interspecies-songs.md`*
