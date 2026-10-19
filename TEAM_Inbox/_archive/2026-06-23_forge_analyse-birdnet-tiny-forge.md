# Analyse BirdNET-Tiny-Forge — Patterns Réutilisables pour WILDNEXUS

**Date :** 2026-06-23
**Auteur :** Forge 🔨 (Platform Builder PKA_JCH)
**Source :** https://github.com/birdnet-team/BirdNET-Tiny-Forge (clone local `/tmp/birdnet-tiny-forge`)

---

## 1. Architecture du Pipeline Kedro

BirdNET-Tiny-Forge utilise **Kedro 1.0** comme orchestrateur de pipeline, structuré en **4 pipelines séquentiels** :

```
audio_clips (WAV bruts)
    │
    ▼
[1] data_preprocessing
    │  ├── extract_loudest_slice  → slice centré sur le max d'amplitude
    │  ├── slices_make_canonical  → mono, resample (16 kHz)
    │  ├── slices_filter_short    → filtre les slices trop courts
    │  ├── extract_metadata       → labels depuis structure de dossiers
    │  ├── decide_splits          → train/test/val (70/20/10)
    │  └── save_labels_dict       → mapping label→int
    │
    ▼
[2] feature_extraction
    │  ├── run_feature_extraction → MicroSpeechExtractor (TFLite Micro frontend)
    │  ├── collate                → fusion features + métadonnées → model_input.parquet
    │  └── plot_features_sample   → visualisation
    │
    ▼
[3] model_training
    │  ├── make_tf_datasets       → tf.data.Dataset (train/val/test) + SpecAugment
    │  ├── get_class_weight       → pondération par classe déséquilibrée
    │  ├── get_model              → MobilenetSlimmed (Keras 3, registry pattern)
    │  ├── train_model            → .fit() avec checkpointing automatique
    │  ├── test_model             → prédictions sur test set
    │  └── plot / confusion_matrix
    │
    ▼
[4] target_codegen
       ├── do_code_generation     → conversion TFLite int8 + templates Jinja2 → code C embarqué
       ├── compile_bin            → Docker ESP-IDF v5.2 → build idf.py
       └── flash_bin              → flash via /dev/ttyUSB0
```

**Points d'architecture clés :**

- **Registries pattern** : `FeatureExtractorsRegistry`, `ModelsRegistry`, `BuildTargetsRegistry` — chaque composant est enregistré par nom (string) et résolu dynamiquement depuis les YAML de configuration. Extrêmement élégant pour le swap de composants.
- **Lazy loading** : toutes les opérations de preprocessing/feature-extraction utilisent un pattern de callables différées (`{path: partial(fn, loader)}`), évitant de charger tout le dataset en RAM.
- **Kedro Data Catalog** (`conf/base/catalog.yml`) : définit tous les artefacts intermédiaires avec typage fort.
- **Templates Jinja2** pour la génération de code cible (dossier `templates/` — actuellement vide pour korvo2, en early dev).

---

## 2. Étapes Clés Transposables à Notre Pipeline Edge Impulse FOMO

### 2.1 Preprocessing Audio → Feature Extraction

| BirdNET-Tiny-Forge | Notre WILDNEXUS (Edge Impulse FOMO) | Action |
|---|---|---|
| `extract_loudest_slice` (slice centré sur amplitude max) | Nos slices sont déjà prédécoupés par événement | **Garder notre découpage actuel** — mieux adapté à la détection d'événements |
| Resample 16 kHz mono PCM_16 | FOMO attend du RGB 96×96 ou 160×160 | Différence fondamentale : FOMO = image, BirdNET = spectrogramme audio |
| `MicroSpeechExtractor` (TFLite Micro frontend : Hann window → FFT → filterbank 32/40 canaux → log scaling) | FOMO fait le feature learning directement sur pixels | **Pas directement transposable** — mais le concept de feature extractor bit-identical desktop/embarqué est crucial |

**Pattern à copier :** la classe `AudioPreprocessor` qui :
1. Définit le feature extractor en TensorFlow ops pures
2. Le convertit en `.tflite` via `TFLiteConverter.from_concrete_functions`
3. Exécute ce `.tflite` sur desktop via l'interpréteur TFLite Micro **pour garantir l'équivalence numérique desktop/embarqué**

→ Pour nous : nous devrions implémenter le **même preprocessing d'image** (redimension, normalisation) sous forme de TFLite model, et l'exécuter via TFLite Micro pendant l'entraînement pour valider l'équivalence avec le edge.

### 2.2 Model Training → Quantization → Deployment

| Étape | BirdNET-Tiny-Forge | Transposable à WILDNEXUS |
|---|---|---|
| Modèle | `MobilenetSlimmed` (Keras 3, ~4 couches depthwise-separable, GlobalMaxPooling) | FOMO (MobileNetV2-like, mais entraîné par Edge Impulse) |
| Quantization | **INT8 post-training quantization** avec `representative_dataset` (10 batches du train set) + `TFLiteConverter` + `tf.lite.Optimize.DEFAULT` | **IDENTIQUE** — la quantization INT8 est le standard pour ESP32-S3 |
| Ops supportées | Vérification automatique des ops TFLite Micro (`get_model_ops_and_acts`) | **À copier** — vérifier que notre FOMO exporté n'utilise que des ops supportées par TFLite Micro |
| Codegen | Templates Jinja2 → code C avec modèle en hex array | Nous générons déjà du code Arduino/ESP-IDF |

**Pattern clé de quantization** (`korvo2_bird_logger.py:90-109`) :
```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.inference_input_type = tf.dtypes.int8
converter.inference_output_type = tf.dtypes.int8
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.representative_dataset = representative_dataset_gen  # 10 batches
```

### 2.3 Augmentation Pipeline

BirdNET utilise une pipeline Keras `Pipeline([MixUp, GaussianNoise, SpecAugment])`. Pour nous :
- **SpecAugment** (frequency/time masking) → non applicable à FOMO (images)
- **MixUp** → applicable ! MixUp sur images peut améliorer la robustesse
- **GaussianNoise** → applicable tel quel

---

## 3. Points de Contact avec Notre Workflow ESP32-S3

### 3.1 Toolchain ESP-IDF Dockerisée

`toolchains/esp_idf_v5_2.py` utilise l'image Docker officielle `espressif/idf:release-v5.2` pour :
- `idf.py build` → compilation
- `idf.py flash` → flash via USB

**C'est exactement notre cas d'usage ESP32-S3.** Le pattern Docker + `docker.from_env()` + `containers.run()` est directement réutilisable pour notre CI/CD.

### 3.2 Tensor Arena Sizing

Le paramètre `tensor_arena_size: 150_000` (bytes) dans `parameters_target_codegen.yml` — c'est la mémoire allouée à TFLite Micro sur le device. Pour FOMO sur ESP32-S3 avec PSRAM, nous devons déterminer notre propre valeur. Leur approche : "trial and error" documentée dans le code.

### 3.3 Support TFLite Micro natif

Le `build_tflite.sh` clone un fork patché de `tflite-micro` avec :
- Support des **custom signal ops** (FFT, filterbank, window, energy) exposées en Python
- Version de TensorFlow **pinnée** (2.18.0)

Pour nous : si FOMO exporte un modèle TFLite standard (ops built-in), pas besoin de fork. Mais le **principe de pinner la version TF** entre desktop et embarqué est critique.

---

## 4. Recommandations Concrètes

### 4.1 Quoi COPIER tel quel

1. **Registry Pattern** (`registries/base.py` + `registries/*.py`) — 200 lignes, singleton métaclass, mapping string→classe. Parfait pour nos propres composants swapables (modèles, feature extractors, cibles de déploiement).

2. **Checkpoint Session** (`models/base.py:TrainingSession`) — callback Keras qui sauvegarde chaque epoch et restaure le meilleur checkpoint selon une métrique. Code propre, ~80 lignes.

3. **Toolchain Docker ESP-IDF** (`toolchains/esp_idf_v5_2.py`) — 80 lignes, compile/flash ESP32-S3 dans un container. Nous pouvons l'utiliser sans modification (juste changer le port USB si nécessaire).

4. **Validation Ops TFLite Micro** (`targets/korvo2_bird_logger.py:get_model_ops_and_acts`) — extrait les opérateurs d'un buffer TFLite et vérifie leur compatibilité. ~30 lignes.

5. **BatchedParquetDataset** (`datasets/batched_parquet_dataset.py`) — sauvegarde lazy par batch en Parquet, évite les OOM sur gros datasets. ~50 lignes.

### 4.2 Quoi ADAPTER

1. **Feature Extractor TFLite Micro** → Nous devons créer l'équivalent pour le preprocessing d'image FOMO :
   - Redimension 96×96 ou 160×160
   - Normalisation RGB (mean/std ou min-max selon ce que FOMO attend)
   - Conversion en INT8
   - Convertir ce preprocessing en `.tflite` (comme `AudioPreprocessor.generate_tflite_file()`)
   - L'exécuter via TFLite Micro pendant la validation pour garantir l'équivalence

2. **Pipeline Kedro** → Notre pipeline actuel (Edge Impulse CLI + scripts bash) gagnerait à être migré vers Kedro pour :
   - Traçabilité des artefacts
   - Reproductibilité (versioning automatique des datasets)
   - Visualisation du pipeline (Kedro-Viz)
   - Changement de modèle/feature-extractor par simple edit YAML

3. **Jinja2 Code Generation** (`targets/base.py:process_target_templates`) → Pour notre code Arduino/ESP-IDF, nous devrions templatiser la génération du fichier `.ino` ou `main.cpp` avec :
   - Le modèle en hex array
   - Les labels
   - Les paramètres de preprocessing
   - La taille du tensor arena

### 4.3 Quoi NE PAS prendre

1. **MicroSpeechExtractor** — spécifique à l'audio, pas pertinent pour FOMO image-based.
2. **Librosa pour preprocessing** — nous utilisons OpenCV/PIL pour les images, pas de raison de changer.
3. **Keras-Tuner** (listé dans les dépendances) — la recherche d'architecture FOMO est gérée par Edge Impulse.

---

## 5. Plan d'Action Proposé pour WILDNEXUS

| Priorité | Action | Effort estimé | Impact |
|---|---|---|---|
| 🔴 P0 | Implémenter le preprocessing FOMO en TFLite Micro model + validation bit-identical | 3-5 jours | Critique pour la fiabilité edge |
| 🔴 P0 | Script de quantization INT8 avec representative dataset (inspiré de Korvo2BirdLogger) | 1-2 jours | Nécessaire pour ESP32-S3 |
| 🟡 P1 | Migrer le pipeline vers Kedro (structure de base + catalog) | 3-5 jours | Reproductibilité, maintenabilité |
| 🟡 P1 | Intégrer la toolchain Docker ESP-IDF pour CI/CD | 1-2 jours | Automatisation build/flash |
| 🟢 P2 | Registry pattern pour nos composants | 1 jour | Flexibilité |
| 🟢 P2 | Templates Jinja2 pour codegen ESP32-S3 | 2-3 jours | Standardisation du déploiement |
