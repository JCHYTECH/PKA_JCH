# Brief — [[Clio]] 🦜 : Analyse scientifique InsectNet — InsectSet459 + PULSE

**Date :** 2026-06-17  
**Émis par :** [[Dobby]]  
**Deadline :** 2026-06-24 (1 semaine)  
**Priorité :** P1 — débloque la phase d'entraînement du modèle InsectNet  

## Contexte

InsectNet est le pipeline de classification bioacoustique d'insectes pour WildNexus. Le pipeline d'ingestion audio est fonctionnel (12 scripts, Xeno-Canto API, segmentation, spectrogrammes, QC). Dataset Conocephalus fuscus déjà constitué (~479 segments, 30 enregistrements). JCH est actuellement en montagne en Italie et va enregistrer des chants d'insectes in situ.

Ce qui manque : un modèle de classification. Deux ressources viennent d'être identifiées via DuckDuckGo.

## Missions

### 1. Évaluer InsectSet459

**Source :** Nature Scientific Data, mars 2026 — « A dataset of insect sounds from 459 species for bioacoustic machine learning »
**URL :** https://www.nature.com/articles/s41597-026-07123-4

**Questions à répondre :**
- Combien d'espèces européennes (pertinentes pour le Trentin/Italie du Nord) sont incluses ?
- Format des fichiers audio (WAV, fréquence, durée) ?
- Licence (CC BY, CC BY-SA, autre) ?
- Métadonnées disponibles (localisation, température, date) ?
- Le dataset est-il téléchargeable en batch ou fichier par fichier ?
- Qualité des enregistrements (bruit de fond, distance micro) ?
- Y a-t-il des espèces qui chevauchent avec le dataset Conocephalus fuscus existant ?

**Livrable :** `INSECTNET/01_RESEARCH/insectset459-evaluation.md`

### 2. Évaluer PULSE

**Source :** arXiv, juin 2026 — « Decoding Insect Song: A Multitask Semisupervised Framework for Orthoptera Bioacoustics »
**URL :** https://arxiv.org/abs/2606.13236

**Questions à répondre :**
- Architecture du modèle (base model utilisé, couches, embedding) ?
- Performances rapportées (accuracy, F1-score, par espèce) ?
- Code source disponible ? Licence ?
- Dépendances (PyTorch, TensorFlow, MLX-compatible ?)
- Poids pré-entraînés disponibles ou faut-il entraîner from scratch ?
- Consommation mémoire/GPU à l'entraînement — viable sur M1 32 GB ?
- Comparable à BirdNET fine-tuning en termes de rapport coût/performance ?

**Livrable :** `INSECTNET/01_RESEARCH/pulse-evaluation.md`

### 3. Recommandation finale

Comparer les deux approches et recommander la meilleure pour InsectNet :
- **Option A :** Fine-tuning BirdNET sur InsectSet459 + segments JCH
- **Option B :** Entraînement PULSE from scratch
- **Option C :** Approche hybride

Critères : temps d'entraînement, précision, compatibilité M1, facilité de déploiement (format TFLite pour edge ?).

**Livrable :** `INSECTNET/01_RESEARCH/model-recommendation.md`

## Références
- `INSECTNET/03_AUDIO_DOWNLOADS/Conocephalus_fuscus/` — dataset existant
- `INSECTNET/04_PIPELINE/` — logs du pipeline
- `scripts/insectnet_*.py` — 12 scripts existants
- `MEMORY.md` — section InsectNet (14 juin)
