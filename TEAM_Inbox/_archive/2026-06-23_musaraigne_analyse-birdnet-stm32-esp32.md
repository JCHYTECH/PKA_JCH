# Analyse birdnet-stm32 — Transposition ESP32-S3

> **Date :** 2026-06-23  
> **Source :** https://birdnet-team.github.io/birdnet-stm32/ + GitHub repo  
> **Auteur :** Dobby 🦉 → Musaraigne 🐭  
> **Statut :** Analyse — recommandation technique

---

## 1. Spécifications du modèle BirdNET-STM32

| Paramètre | Valeur |
|-----------|--------|
| Architecture | DS-CNN (Depthwise-Separable CNN) |
| Entrée | Mel spectrogramme 2-3 secondes |
| Frontends audio | 5 : librosa, hybrid (STFT+NPU), raw (waveform→NPU), mfcc, log_mel |
| Quantization | INT8 PTQ + QAT (Quantization-Aware Training) |
| Latence inference | **10-14 ms** sur STM32N6 NPU |
| Latence STFT (hybrid) | ~45 ms sur CPU |
| Latence totale end-to-end | **55-59 ms** (hybrid) ou **10 ms** (raw waveform→NPU) |
| Cible hardware | STM32N6570-DK (NPU intégré Neural-ART Accelerator) |
| Toolchain | ST X-CUBE-AI → stedgeai |
| CLI unifié | `python -m birdnet_stm32 {train,convert,evaluate,deploy}` |

## 2. Chaîne de conversion

```
Keras model (FP32)
    ↓ PTQ (representative_dataset)
TFLite INT8 (float I/O, INT8 internals)
    ↓ stedgeai generate
Code C optimisé NPU (STM32Cube.AI)
    ↓ idf.py / make
Firmware STM32N6
```

**Cible cosine similarity :** ≥0.95 vs float model après PTQ.

## 3. Comparaison architecturale STM32N6 vs ESP32-S3

| Critère | STM32N6570-DK | ESP32-S3 (notre cible) |
|---------|---------------|------------------------|
| CPU | Cortex-M55 @ 800 MHz | Xtensa LX7 @ 240 MHz |
| NPU | Neural-ART (600 GOPS) | **Aucun** |
| RAM | 4.2 MB SRAM | 512 KB SRAM + 8 MB PSRAM |
| Flash | 16 MB | 16 MB (standard) |
| Accélération ML | NPU dédié + Helium MVE | ESP-DL (optimisé vectoriel) |
| TFLite Micro | Supporté | Supporté (ESP-NN backend) |
| Toolchain | STM32Cube.AI / X-CUBE-AI | ESP-IDF + ESP-DL |

## 4. Écart de performance estimé

Le STM32N6 a un NPU 600 GOPS dédié. L'ESP32-S3 n'a pas de NPU — il exécute TFLite Micro sur CPU avec optimisations vectorielles ESP-NN.

| Opération | STM32N6 (NPU) | ESP32-S3 (CPU + ESP-NN) | Ratio |
|-----------|---------------|--------------------------|-------|
| Conv2D 3×3 | ~0.01 ms | ~0.3 ms | ~30× |
| DepthwiseConv | ~0.005 ms | ~0.15 ms | ~30× |
| Inference DS-CNN (2s audio) | ~12 ms | **~350 ms estimé** | ~30× |

**Conclusion :** Le modèle BirdNET-STM32 tel quel est **trop lourd** pour l'ESP32-S3. Il faudrait réduire la taille du modèle d'un facteur ~30× pour atteindre une inference <50 ms.

## 5. Patterns réutilisables malgré l'écart matériel

### Ce qu'on peut COPIER :

1. **Architecture CLI unifiée** (`train/convert/evaluate/deploy`) — structure propre, à répliquer pour notre toolchain WILDNEXUS
2. **Pipeline PTQ + QAT** — le code de quantization avec representative_dataset est directement réutilisable
3. **5 frontends audio** — la comparaison librosa/hybrid/raw/log_mel est instructive pour InsectNet
4. **Métriques d'évaluation** — ROC-AUC, cmAP, F1, bootstrap CI, DET curves → à intégrer dans notre pipeline
5. **Optuna hyperparameter search** — architecture de tuning automatisé

### Ce qu'il faut ADAPTER :

1. **Taille du modèle** — viser <100k params, <10M FLOPs pour ESP32-S3 (au lieu du DS-CNN complet)
2. **Audio frontend** — le raw waveform→filterbank appris est élégant mais coûteux. Pour ESP32, privilégier un FFT hardware-optimisé (ESP-DSP)
3. **Toolchain** — remplacer stedgeai par ESP-DL / TFLite Micro avec ESP-NN backend

## 6. Recommandation Musaraigne

**Verdict :** Le modèle BirdNET-STM32 est une excellente référence architecturale mais n'est **pas directement portable** sur ESP32-S3 à cause de l'absence de NPU.

**Stratégie recommandée :**
1. **Court terme (cette semaine) :** Utiliser FOMO via Edge Impulse comme baseline (96×96 image-based, optimisé pour MCU sans NPU)
2. **Moyen terme (juillet) :** Explorer un DS-CNN ultra-light (<50k params) entraîné sur spectrogrammes mel, quantifié INT8, déployé via TFLite Micro + ESP-NN
3. **Long terme :** Si STM32N6 devient accessible/abordable, migrer l'architecture BirdNET-STM32 directement

**Actions immédiates :**
- [Musaraigne] Implémenter le pipeline PTQ de birdnet-stm32 pour nos modèles FOMO
- [Musaraigne] Benchmarquer FOMO INT8 sur ESP32-S3 : latence, RAM, précision
- [Forge] Intégrer les métriques d'évaluation (cmAP, bootstrap CI) dans notre pipeline

---

*Ce rapport remplace le livrable de l'agent Musaraigne (échec technique).*
