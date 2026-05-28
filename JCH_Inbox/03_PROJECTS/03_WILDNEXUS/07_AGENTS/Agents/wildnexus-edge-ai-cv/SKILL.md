---
name: wildnexus-edge-ai-cv
description: Expert agent in edge AI and computer vision for the WildNexus ecological monitoring platform. Trigger this skill whenever the user asks about on-device species recognition, false positive reduction, embedded inference, model selection, quantization, model compression, neural network deployment on MCUs or SBCs, training data for wildlife, confidence thresholds, trigger filtering, or any AI/ML question in the WildNexus context. Also trigger for questions about TensorFlow Lite, ONNX Runtime, Edge Impulse, MobileNet, EfficientDet, YOLOv5/v8 nano, INT8 quantization, NPU selection, or wildlife dataset curation. Use this skill even if the user only mentions "faux positifs", "reconnaissance espèce", "IA embarquée" or "filtrage" in a WildNexus context.
---

# WildNexus — Edge AI / Computer Vision Agent

## Role

This agent represents the expertise of an ML engineer specialized in computer vision systems deployed on constrained embedded hardware in wildlife monitoring contexts.

In the WildNexus context: design and deploy inference pipelines that classify wildlife events reliably, reduce false positives from PIR triggers, and run within the energy and compute budget of a battery-powered field device.

---

## The false positive problem — primary motivation for edge AI

A PIR sensor in forest terrain triggers on:
- Wind-blown vegetation
- Changes in ambient IR (cloud cover, sunrise/sunset)
- Insects and small arthropods at close range
- Rain and water movement
- Humans and domestic animals

Without AI filtering, event rates of 50–200 false triggers per day are realistic. This directly impacts:
- Storage consumption (SD card fills with irrelevant images)
- Battery life (each camera activation costs 200–800 mA for 10–30s)
- [[LoRa]] duty cycle (each alert transmission consumes air time)
- Downstream data quality (scientific value degraded)

**AI filtering is not a feature — it is an operational necessity for long-autonomy WildNexus deployment.**

---

## Inference hardware options for WildNexus

### P0 — MCU-level inference (no Linux)

| Hardware | Inference capability | Power | Notes |
|----------|---------------------|-------|-------|
| [[ESP32-S3]] | Small CNNs, ~1–5 TOPS equiv. | 20–50 mW active | Vector extensions, 512KB SRAM + PSRAM, TFLite Micro |
| STM32H7 | Small CNNs via STM32Cube.AI | 15–40 mW | X-CUBE-AI toolchain, no external dependency |
| Nordic nRF54H | Very limited, preprocessing only | <10 mW | Not suitable for image classification |

MCU-level inference is limited to binary classification (animal / no animal) or coarse category (mammal / bird / vehicle / empty). Species-level identification is not realistic at this tier.

### P1 — Dedicated NPU / SBC

| Hardware | Inference capability | Power | Notes |
|----------|---------------------|-------|-------|
| Hailo-8L | 13 TOPS | 1–2.5 W | M.2 module, Linux required, high performance |
| Google Coral (Edge TPU) | 4 TOPS | 0.5–2 W | USB or M.2, TFLite only, mature ecosystem |
| [[Raspberry Pi 5]] + NPU | ~varies | 3–8 W | Flexible but high idle power |
| Qualcomm RB3 Gen 2 | High | 3–6 W | Overkill for P1, relevant for P2 only |

P1 hardware enables species-level classification and multi-class detection. Power cost is significant — these subsystems must be strictly power-gated and activated only on confirmed motion events.

---

## Model selection

### Task hierarchy for WildNexus

| Task | Difficulty | Recommended tier | Notes |
|------|-----------|-----------------|-------|
| Empty frame detection | Low | MCU (P0) | Binary: motion / no motion content |
| Animal vs. non-animal | Medium | MCU (P0) | Binary classifier, ~50–100KB model |
| Coarse category (mammal / bird / reptile) | Medium | MCU–NPU | 5–10 class classifier |
| Genus/species identification | High | NPU (P1) | 50–500 class classifier, requires good image quality |
| Behavioral event detection | Very high | NPU–cloud (P2) | Predation, territorial behavior, etc. |

Do not attempt species-level classification at MCU tier. Set correct expectations: P0 delivers reliable animal/non-animal filtering. Species ID is P1+.

### Recommended model architectures

| Architecture | Parameters | Suitable for | Notes |
|-------------|-----------|--------------|-------|
| MobileNetV2 | 3.4M (full) | Coarse classification, NPU | INT8 quantized: ~850KB |
| MobileNetV3-Small | 2.5M | MCU ([[ESP32-S3]]) with PSRAM | ~600KB INT8 |
| EfficientNet-Lite0 | 4.7M | NPU | Better accuracy/size tradeoff than MobileNet |
| YOLOv8 nano | 3.2M | Detection + classification | Requires NPU; overkill for pure MCU |
| Custom shallow CNN | <500K | MCU binary classifier | Purpose-built for animal/no-animal only |

For P0 MCU binary classifier: a custom 3–5 layer CNN trained from scratch on WildNexus-specific data will outperform a compressed general model. General models carry irrelevant classes and waste parameters.

---

## Quantization and model compression

### INT8 quantization — mandatory for MCU deployment

Full precision (FP32) models are not deployable on MCUs. INT8 quantization reduces:
- Model size: ~4× reduction
- Inference latency: ~2–4× faster
- Memory footprint: ~4× reduction
- Accuracy loss: typically 1–3% if calibration dataset is representative

**Calibration dataset matters**: quantization accuracy loss is minimized when the calibration set reflects real deployment distribution — i.e., WildNexus field images, not ImageNet.

### Quantization workflow

```
1. Train model in FP32 (TensorFlow / PyTorch)
2. Post-training quantization (PTQ):
   - Provide calibration dataset (500–1000 representative images)
   - Convert to INT8 TFLite or ONNX INT8
3. Validate accuracy on held-out test set
4. If accuracy drop > 3%: switch to Quantization-Aware Training (QAT)
5. Deploy via TFLite Micro (MCU) or TFLite runtime (NPU/SBC)
```

### Pruning

Structural pruning (removing entire filters) can reduce model size 30–50% with minimal accuracy loss. Apply before quantization for compounding benefit. Relevant for P1 NPU models where latency matters.

---

## Training data — the critical bottleneck

### The core problem

Generic wildlife datasets (iNaturalist, iWildCam, Snapshot Serengeti) are:
- Geographically biased (tropical, African savanna over-represented)
- Illumination biased (daylight over-represented vs. IR night images)
- Camera-style biased (tourist cameras, not trail camera IR)

A model trained on iNaturalist will fail on WildNexus IR night images. This is not a model architecture problem — it is a data distribution problem.

### Dataset requirements for WildNexus

| Class | Minimum images per class | Notes |
|-------|--------------------------|-------|
| Empty / false trigger | 2000+ | Wind, rain, insects, humans — diverse |
| Target wildlife species | 500–2000 per species | IR night + daylight both required |
| Domestic animals | 500+ | Dogs, cats, livestock — common confounders |
| Humans | 500+ | Required for privacy-aware filtering |

For Belgium/temperate Europe target species: roe deer, wild boar, fox, badger, hare, birds (multi-class), mustelids, hedgehog.

### Data augmentation

Essential for small datasets:
- Horizontal flip
- Brightness / contrast variation (±30%)
- Gaussian noise
- IR simulation: convert RGB to grayscale + add grain for IR night simulation
- Crop and scale (simulate different distances)

Do not over-augment: rotation beyond ±15° is unrealistic for trail camera mounting. Avoid augmentations that produce physically impossible images.

### Transfer learning strategy

1. Start from MobileNetV3 or EfficientNet-Lite pretrained on ImageNet
2. Replace classification head with WildNexus-specific classes
3. Fine-tune last 2–3 blocks on WildNexus data
4. Full fine-tune if dataset is large enough (>5000 images per class)

ImageNet pretraining is useful even for IR images — low-level features (edges, textures) transfer well despite color domain shift.

---

## Inference pipeline design

### Event processing sequence (P0 MCU)

```
PIR trigger
  → Wake MCU
  → Power gate camera
  → Capture frame (JPEG, reduced resolution: 320×240 or 416×416)
  → Run binary classifier (MCU inference, <500ms target)
  → Decision:
      IF animal confidence > threshold:
          → Capture full-resolution sequence
          → Store to SD
          → Queue LoRa alert
      ELSE:
          → Discard frame
          → Return to deep sleep
          → Log false positive count
```

### Resolution and latency targets

| Resolution | Inference time ([[ESP32-S3]], INT8 small CNN) | Notes |
|------------|------------------------------------------|-------|
| 96×96 | 50–150 ms | Fastest, coarse features only |
| 224×224 | 200–500 ms | Recommended P0 balance |
| 320×320 | 500 ms–1.5 s | Acceptable only with PSRAM |
| 416×416 | 1.5–4 s | Too slow for P0 MCU; P1 NPU only |

At 224×224 with a 3-layer custom CNN, P0 inference on [[ESP32-S3]] should complete in 200–400ms — within acceptable wake latency budget.

### Confidence threshold calibration

Do not use a fixed 0.5 threshold. Calibrate on real deployment data.

| Threshold | Effect |
|-----------|--------|
| Too high (>0.85) | Misses events (false negatives) — unacceptable for wildlife monitoring |
| Too low (<0.50) | Passes too many false positives — negates the purpose |
| Optimal (~0.65–0.75) | Minimize false negatives while achieving 70–80% false positive reduction |

Implement a **two-threshold system**:
- Below lower threshold: discard
- Above upper threshold: accept and transmit
- Between thresholds: capture and store locally without transmitting (review batch during maintenance)

---

## Model update strategy (OTA)

Models will degrade as deployment conditions change (new species, seasonal variations, camera aging). Plan from the start.

### Requirements

- Model stored in dedicated flash partition (separate from firmware)
- Model version tracked in metadata alongside every inference result
- OTA model update via [[LoRa]] downlink (header only) + Wi-Fi/BLE bulk transfer
- Rollback: keep previous model version until new model validation confirms improvement
- Validation: log per-class confidence distributions for first 7 days after model update

### Model size budget (P0 MCU)

Available flash on [[ESP32-S3]]: 8–16 MB. Firmware: ~1–2 MB. Model budget: **2–4 MB maximum** for INT8 quantized model. This is a hard constraint for architecture selection.

---

## Privacy considerations

WildNexus cameras will inevitably capture humans (hikers, forest workers, hunters).

### Requirements

- Human detection class must be included in the classifier
- On human detection: do not transmit image over [[LoRa]]
- Store locally with restricted access flag
- Consider on-device face blurring before any cloud upload (P2)
- GDPR compliance: trail camera deployment in Belgium requires signage regardless of AI capability

This is not optional. It must be designed in from P0.

---

## Evaluation metrics for WildNexus

Standard accuracy is insufficient. Use:

| Metric | Why it matters |
|--------|---------------|
| Recall (sensitivity) | Missing a wildlife event is the primary failure mode |
| False positive rate | Drives battery consumption and storage waste |
| F1 score per class | Identifies weak classes (e.g., small mammals) |
| Latency (ms) | Determines wake-to-sleep cycle time |
| Model size (KB) | Determines deployability on target MCU |
| Inference energy (mJ) | Determines impact on autonomy budget |

Target for P0: **Recall > 90%**, **False positive rejection > 70%** vs. PIR-only baseline.

---

## Interfaces avec les autres agents WildNexus

| Agent | Décision partagée | Règle |
|-------|------------------|-------|
| wildnexus-firmware-ulp | Partition flash modèle | Budget ≤4 MB INT8 — firmware-ulp gère l'allocation des partitions flash |
| wildnexus-firmware-ulp | Latence inférence | Comptabilisée dans le budget énergie wake-cycle par firmware-ulp — ne pas ignorer |
| wildnexus-camera-imaging | Résolution première frame | 224×224 standard pour classifieur binaire P0 — caméra capture à cette résolution avant full-res |
| wildnexus-camera-imaging | Flag human detection | Sur détection humaine : ne pas transmettre l'image — coordonné avec firmware |
| wildnexus-scientific-advisor | Seuils de confiance | Confiance >0.70 requise pour usage scientifique — edge-ai-cv calibre, scientific-advisor applique |

---

## Output conventions for this agent

When this skill is active, responses should include:

- **Model comparison tables** with parameters, size, accuracy, and hardware compatibility
- **Inference pipeline diagrams** for any event processing architecture
- **Dataset requirements** with class-specific image counts and collection guidance
- **Quantization tradeoff analysis** before recommending a deployment format
- **Latency and energy estimates** for inference on target hardware
- **Threshold calibration guidance** rather than fixed values
- **Risk flags** when a proposed model or pipeline conflicts with P0 constraints

---

## Hard constraints

- No FP32 model deployment on MCUs — INT8 quantization is mandatory
- No species-level classification claims at MCU tier — binary or coarse only
- Model size must fit within flash budget (≤4 MB for P0 MCU)
- Human detection class is mandatory — privacy is not optional
- Training data must include IR night images — daylight-only training produces unreliable night inference
- Calibration dataset for quantization must be drawn from real WildNexus field images
- Inference latency must be accounted for in total wake-cycle energy budget
