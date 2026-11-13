# Pointer — CNN audio on-device (TV) → NEXUS_ACOUSTIC

> 2026-11-07 · Dobby 🦉 · source : transcript NoteGPT « Voici ce que l'IA vient de trouver dans nos télés »

## Référence source

`JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/tv-privacy-acr_2026-11-07/NoteGPT_Transcript_Voici ce que l'IA vient de trouver dans nos télés.txt`

## Pertinence NEXUS_ACOUSTIC

Les TV Samsung 2025 embarquent des classifieurs **audio on-device** (sans cloud) :
- compteur d'aboiement / pleurs de bébé — fonctionnalité annoncée « Pet Care / Family Care » (avril 2025)
- modèles CNN : `logo_cnn` (reconnaissance du contenu à l'écran), `AlexTFLite` (reconnaissance jeux vidéo — 2 469 696 paramètres, entrée 64×64 px)
- chasse au micro sur périphériques voisins (soundbar, Bluetooth) liée à Bixby

## À creuser plus tard (post-van, au signal de JC)

- Ces CNN embarqués = **benchmarks de référence TinyML audio/vision** → comparer à nos modèles Edge Impulse / FOMO (taille, latence, précision).
- Pattern « classification audio continue sur appareil, sans cloud » = exactement la cible NEXUS_ACOUSTIC (bioacoustique embarquée).
- Cross-link : décision « pas de TV connectée dans Lupo » (2026-11-07) découle de la même logique local-first.
