# Recette — Détection audio on-device (Edge Impulse) pour NEXUS_ACOUSTIC

> Dobby 🦉 · 2026-11-17 · veille YouTube (9 derniers mois)
> Sources : transcript `diy-esp32-ai-sound-recognition…` (Smart Mercury Labz, hQpPTWAd1QY)
> et `listening-to-the-earth-ai-bioacoustics…` (AGI, Dc4Knztv-9M) — dans `99_REFERENCES/`
> **Statut :** référence à intégrer à la reprise de NEXUS_ACOUSTIC (post-gate DEVICE). Aucun achat ni montage avant.

## Ce que ça apporte

Une voie **légère et 100 % embarquée** pour détecter un son cible (cri d'oiseau, stridulation
d'insecte) sur ESP32 — **complément ou alternative** à BirdNET/TweetyBERT quand on n'a besoin
que d'une détection « présent/absent » à très faible coût énergétique (« fractions de 1 W »,
jamais d'internet). C'est exactement la philosophie P0.

## La recette (pipeline validé à 97 % par l'auteur)

1. **Hardware** : ESP32 dev board + **micro I2S numérique** (type INMP441 — déjà au BOM WildNexus).
2. **Données** : 2 classes uniquement — **son cible** vs **bruit de fond** — en fichiers WAV.
   Chaque classe = enregistrements variés (lieux, conditions).
3. **Edge Impulse** : upload des WAV → **split samples en chunks de 1 s** → bloc de traitement
   **MFE** (FFT length 512) → entraînement (split 80/20) → **~97 % d'accuracy**.
4. **Déploiement** : export en bibliothèque Arduino → PlatformIO/VSCode.
5. **Code** : en plus du modèle, un **seuil de force du son** (> 90) avant de déclencher —
   réduit les faux positifs du bruit de fond.

## Points de méthode réutilisables

- **Binaire plutôt que multi-classe** : « son cible vs bruit » est plus robuste qu'une
  classification fine des espèces au départ. Commencer binaire, affiner ensuite.
- **Chunks de 1 s** : un ML audio veut des exemples individuels, pas un long enregistrement.
- **I2S plutôt qu'analogique** : audio numérique propre, directement lisible par le µC.
- **Seuil en cascade** : modèle + seuil d'énergie sonore = deux garde-fous avant de réveiller.

## À vérifier sur NOS données (ne pas copier aveuglément)

- Le 97 % est annoncé sur « cloche vs bruit », pas sur du bioacoustique réel. À reproduire sur
  nos jeux de cris/insectes (cf. `INSECTNET/02_DATASET`).
- Comparer avec la piste BirdNET on-device déjà explorée (`BirdNET-Go_RaspberryPi_iPhone_summary.md`)
  : coût énergétique vs précision par espèce.

## Action recommandée (à la reprise)

1. Reproduire le pipeline Edge Impulse MFE sur 2-3 espèces test (1 insecte + 1 oiseau).
2. Mesurer au PPK2 la conso en boucle « écoute → détection → sommeil ».
3. Arbitrer : Edge Impulse binaire vs BirdNET vs TweetyBERT selon précision/énergie.
