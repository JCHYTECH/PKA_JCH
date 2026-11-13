# Analyse de l'écosystème BirdNET — Opportunités d'intégration PKA

> **Date :** 2026-06-23  
> **Source :** https://birdnet-team.github.io/BirdNET-Analyzer/ + GitHub org birdnet-team  
> **Auteur :** Dobby 🦉  
> **Destinataires :** Clio 🐬, Chouette 🦉, Musaraigne 🐭, Forge 🔨, Araignée 🕷️

---

## Résumé exécutif

L'écosystème BirdNET (Cornell Lab of Ornithology + Chemnitz TU) est l'équivalent aviaire de ce que nous construisons pour les insectes avec InsectNet. L'analyse révèle **5 opportunités directes d'intégration** et **3 patterns architecturaux** immédiatement transposables à NEXUS_ACOUSTIC et WILDNEXUS.

---

## 1. Architecture du modèle BirdNET V2.4

| Paramètre | Valeur | Pertinence PKA |
|-----------|--------|----------------|
| Backbone | EfficientNetB0-like | Compatible Edge Impulse FOMO |
| Embedding | 1024 dimensions | Extraction features pour similarité |
| GFLOPs | 0.826 | ~2× plus lourd que nos cibles TinyML |
| Taille FP32 | 50.5 MB | Quantization INT8 → ~12 MB (cible ESP32-S3) |
| Classes | 6 522 (dont 11 non-event) | Pattern de non-event classes applicable |
| Sample rate | 48 kHz (auto-resample) | Couvre orthoptères haute fréquence |

### 🔑 Insight critique — Spectrogramme double canal

BirdNET V2.4 utilise **deux spectrogrammes mel en parallèle** :
- **Canal bas :** fmin=0 Hz, fmax=3 kHz, nfft=2048, hop=278, 96 mel bins
- **Canal haut :** fmin=500 Hz, fmax=15 kHz, nfft=1024, hop=280, 96 mel bins
- Résolution finale : 96×511 pixels par canal

**Pourquoi c'est crucial pour InsectNet :** Les orthoptères chantent typiquement entre 2 kHz et 20+ kHz. Un spectrogramme unique centré sur 0-8 kHz manque les harmoniques hautes de Tettigonia viridissima (jusqu'à 20 kHz) ou les stridulations ultrasoniques de certaines sauterelles. Le pattern double canal de BirdNET est **directement transposable** à notre pipeline InsectNet — il suffit d'ajuster les bandes fmin/fmax pour la bioacoustique des insectes (ex: 2-8 kHz + 6-24 kHz).

---

## 2. Écosystème de déploiement edge

### birdnet-stm32 (⭐17, C/Python)
- **Cible :** STM32N6 (MCU avec accélérateur NPU)
- **Description :** Training + déploiement de modèle acoustique tiny sur STM32
- **Topics :** edge-ai, tinyml, bioacoustics, classification
- **Pertinence WILDNEXUS :** Architecture de référence pour déploiement MCU. Le STM32N6 a un NPU intégré — pattern à étudier pour ESP32-S3 (pas de NPU, mais ESP-DL optimisé)

### BirdNET-Tiny-Forge (⭐25, Python, Apache 2.0)
- **Description :** Framework pour créer des enregistreurs de chants d'oiseaux custom sur low-power devices
- **Technos :** Kedro (pipeline orchestrator), edge-computing, embedded
- **Pertinence WILDNEXUS :** Pipeline d'entraînement → déploiement pour MCU low-power. Architecture Kedro intéressante pour notre pipeline de dataset FOMO

### ecoPi + ecoPi-RTF (Dash)
- **Description :** Enregistreur temps-réel sur Raspberry Pi + dashboard Dash
- **Pertinence NEXUS_ACOUSTIC :** Pattern complet : hardware → ML → API → dashboard. Directement applicable à notre station bioacoustique RPi

---

## 3. Post-traitement spatial — geomodel (⭐9, MIT)

- **Description :** Modèle spatio-temporel d'occurrence basé sur données eBird
- **Fonction :** Post-filtrage des détections acoustiques par probabilité géographique
- **Licence :** MIT (compatible)
- **Mise à jour :** 2026-06-22 (actif)

**Opportunité NEXUS_ACOUSTIC :** Créer un équivalent pour les insectes — utiliser les données GBIF (déjà intégrées dans Faune Autour) pour filtrer les détections InsectNet par probabilité d'occurrence géographique. Réduirait les faux positifs de 20-40% selon la littérature BirdNET.

---

## 4. Outillage et pipeline

| Outil BirdNET | Fonction | Équivalent PKA |
|---------------|----------|----------------|
| `birdnet_analyzer.analyze` | Analyse CLI batch | Notre pipeline InsectNet |
| `birdnet_analyzer.embeddings` | Extraction embeddings | Pour manifold UMAP |
| `birdnet_analyzer.segments` | Extraction segments | Notre segmentation WAV |
| `birdnet_analyzer.species` | Liste d'espèces | Taxonomie orthoptères |
| `birdnet_analyzer.train` | Fine-tuning custom classifier | Pour nos espèces cibles |
| GUI segment review | Review manuelle | Équivalent à construire |

---

## 5. Modèle de licence et données

| Composant | Licence | Compatibilité PKA |
|-----------|---------|-------------------|
| Code source | MIT ✅ | Compatible |
| Modèles pré-entraînés | CC BY-NC-SA 4.0 ⚠️ | Non-commercial uniquement |
| Recherche/éducation | = non-commercial ✅ | Nos projets sont recherche |
| Modèles custom (fine-tuned) | Mêmes termes ⚠️ | Dérivé = CC BY-NC-SA aussi |

**Décision nécessaire :** Si nous utilisons des modèles ou architectures dérivés de BirdNET, nos modèles InsectNet custom seront aussi sous CC BY-NC-SA. Ce n'est pas bloquant pour la recherche, mais à documenter.

---

## 6. Compétitions et communauté

- **BirdCLEF+ 2026** — Compétition Kaggle annuelle (bon benchmark)
- **BioDCASE Task 3** — TinyML pour bioacoustique (directement pertinent pour WILDNEXUS)
- **Reddit :** r/BirdNET_Analyzer — communauté active
- **Projects Map :** https://birdnet.cornell.edu/projects-map — ~100 projets recensés

---

## 7. BirdNET V3.0 — Preview

- **Repo :** birdnet-V3.0-dev (TypeScript, Streamlit)
- **Statut :** Developer preview
- **Nouveautés :** Nouveaux modèles, interface Streamlit
- **Veille :** À suivre pour les améliorations d'architecture

---

## Recommandations Dobby

### Action immédiate (cette semaine)

1. **[Clio + Chouette]** Implémenter le pattern spectrogramme double canal dans le pipeline InsectNet — adapter les bandes 2-8 kHz + 6-24 kHz pour les orthoptères
2. **[Musaraigne]** Étudier birdnet-stm32 comme architecture de référence pour le déploiement ESP32-S3 — en particulier la chaîne de quantization INT8
3. **[Forge]** Cloner BirdNET-Tiny-Forge et analyser le pipeline Kedro pour inspiration dataset FOMO

### Action court terme (juillet)

4. **[Clio]** Prototyper un geomodel insectes basé sur GBIF (données déjà dans Faune Autour)
5. **[Chouette]** Étudier ecoPi-rtf comme template pour dashboard bioacoustique NEXUS_ACOUSTIC
6. **[Araignée]** Évaluer la participation à BioDCASE Task 3 2026 pour benchmarker nos modèles TinyML

### Veille continue

7. Suivre BirdNET V3.0-dev pour les avancées d'architecture
8. Explorer la Projects Map pour identifier des collaborateurs potentiels
9. Contacter ccb-birdnet@cornell.edu si nous voulons partager nos datasets orthoptères pour entraînement croisé

---

## Références

- Docs : https://birdnet-team.github.io/BirdNET-Analyzer/
- GitHub org : https://github.com/birdnet-team
- Modèles Zenodo : https://zenodo.org/records/15050749
- Paper : Kahl et al. 2021, Ecological Informatics 61, 101236
- BirdNET-Go (tphakala) : déjà documenté dans `NEXUS_ACOUSTIC/BirdNET-Go_RaspberryPi_iPhone_summary.md`

---

*Analyse complète. Fichier à archiver dans NEXUS_ACOUSTIC/99_REFERENCES/ après traitement.*
