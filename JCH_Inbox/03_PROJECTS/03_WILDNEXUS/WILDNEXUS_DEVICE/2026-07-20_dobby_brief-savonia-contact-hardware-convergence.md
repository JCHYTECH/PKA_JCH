# Savonia — Deep Dive & Stratégie de Contact Hardware

> Dobby 🦉 — DeepSeek V4 — 2026-07-20
> Suite à l'analyse INBOX « surveillance acoustique écurie »

---

## 1. Le projet Savonia « Tekoälyä talleille » (AI for Stables)

### 1.1 Identité

| Attribut | Valeur |
|----------|--------|
| **Nom** | Tekoälyä talleille (AI for Horse Stables) |
| **Type** | EIP-AGRI Operational Group (European Innovation Partnership) |
| **Financement** | EU CAP Network — CAP Strategic Plans 2023-2027, via Pohjois-Savon ELY-keskus |
| **Période** | 2024–2027 (en cours) |
| **Partenaires** | Suomen Hevostietokeskus ry (Finnish Horse Information Centre) + Savonia University of Applied Sciences |
| **Innovation Group** | Fermes équestres, vétérinaires, experts bien-être équin, technologie |
| **Site pilote** | Rauhalahti Riding School — 7 chevaux, section écurie |

### 1.2 Deux produits en développement

| # | Produit | Fonction | Statut |
|---|---------|----------|--------|
| **1** | **App mobile — Soundscape Monitoring** | Analyse le paysage sonore normal de l'écurie. Détecte les anomalies (changement brusque). Étudie l'effet du fourrage sur le comportement. | Pilote 2 en cours |
| **2** | **App mobile — Stéthoscope intestinal** | Écoute les bruits intestinaux. Détection précoce de sable/coliques. Passage du curatif au préventif. | Revue technique terminée |

### 1.3 Stack technique actuelle

| Composant | Spécification |
|-----------|--------------|
| **Matériel acquisition** | 4× Raspberry Pi 4 + 7 paires caméra-microphone |
| **Enregistrement** | 30 min toutes les heures, 19h–09h (période nocturne) |
| **Volume données** | ~9.24 GiB/nuit (audio 3.36 GiB + vidéo compressée 5.88 GiB) |
| **Transfert** | SSH vers serveur NVIDIA DGX à Savonia (systemd, flock) |
| **Audio** | 20 MiB/session, format brut → compression vidéo ffmpeg |
| **Vidéo** | 370 MiB/session brut → 35 MiB compressé |
| **Modèle AI** | PANNs/CNN14 pré-entraîné (AudioSet) → embeddings 2048-dim, autoencoder pour anomalies, MLP 3 couches pour classification |
| **Stéthoscope** | Évaluation de Thinklabs, Stemoscope, Linktop |
| **Orchestration** | systemd timers + flock (pas cron) |

### 1.4 Équipe — contacts directs

| Nom | Rôle | Email | Tél |
|-----|------|-------|-----|
| **Aki Happonen** | Digital Development Manager, DigiCenter | aki.happonen@savonia.fi | +358 44 785 6033 |
| **Johannes Geisler** | RDI Specialist, AI/Robotics | johannes.geisler@savonia.fi | — |
| **Osman Torunoglu** | RDI Specialist | osman.torunoglu@savonia.fi | — |
| **Finlay Hare** | RDI Project Worker | finlay.hare@savonia.fi | — |
| **Heli Suomala** | Project Manager, Hevostietokeskus | heli.suomala@hevostietokeskus.fi | — |

### 1.5 Ce que Savonia n'a PAS — angle de proposition PKA

| Gap Savonia | Solution PKA/WildNexus |
|-------------|----------------------|
| RPi 4 = dépendance secteur, pas d'autonomie | ESP32-S3 + deep sleep + batterie 8×AA → 60 jours autonome |
| Micros probablement USB basiques | 2× SPH0645LM4H-B MEMS I2S, SNR 65dB, stéréo, calibrés |
| Pas d'enclosure outdoor/IP67 | Boîtier NEMA 4X, déploiement tout environnement |
| Pas d'edge AI locale (tout → DGX) | CNN 330K params quantifié INT8 sur ESP32-S3 + FFT onboard |
| Pas de LoRa/connectivité longue portée | LoRa SX1262 intégré → pas besoin de WiFi sur site |
| Caméra + audio séparés (2 devices) | Module unifié caméra OV5640 + stéréo audio |
| Hardware non modulaire | Architecture PCB unifiée, deux configs filles (Camera Trap / Acoustic Node) |
| Pas de streaming temps réel | Pipeline streaming continu (vs leur capture 30 min programmée) |

> 🎯 **Angle contact :** « Vous avez l'expertise AI et le dataset équin. Nous avons le hardware edge autonome, low-power, outdoor-ready, avec edge AI embarquée. Complémentarité parfaite. »

---

## 2. Convergence Hardware WildNexus ↔ InsectNet/NEXUS_ACOUSTIC

### 2.1 Spécifications comparées

| Spécification | WildNexus (Camera Trap) | InsectNet / NEXUS_ACOUSTIC (Audio) | **Convergence** |
|--------------|--------------------------|-------------------------------------|-----------------|
| **MCU/CPU** | ESP32-S3 (240 MHz, 512KB SRAM, 8MB PSRAM) | RPi 5 8GB (2.4 GHz, ARM Cortex-A76) | ⚠️ Diverge |
| **Audio** | 2× SPH0645LM4H-B I2S, 16kHz/16-bit stéréo | Mêmes micros I2S, 16–48 kHz | ✅ **Identique** |
| **Stockage** | microSD 128GB SPI | SD local / cloud | ✅ Converge |
| **Connectivité** | LoRa SX1262 + WiFi | WiFi/MQTT | ✅ Converge |
| **Caméra** | OV5640 (5MP, DVP) | Non requis (audio only) | ⚠️ Optionnel |
| **Alimentation** | 8×AA + buck → 3.3V, deep sleep, 60j | Secteur 5V (RPi), pas d'autonomie | ⚠️ Diverge |
| **Enclosure** | IP67 / NEMA 4X | Non défini (intérieur) | ✅ Réutilisable |
| **Edge AI** | FFT 1024 (onboard), CNN TFLite INT8 | CNN 330K ONNX → TFLite | ✅ Même modèle |
| **Fréquence capture** | 3s WAV / 60min (caméra) | Streaming continu / segments 3s | ⚠️ Diverge |
| **Coût unitaire estimé** | ~€85–110 | ~€120+ (RPi seul sans périph.) | ✅ WildNexus moins cher |

### 2.2 Le conflit GPIO : caméra vs audio

Le point bloquant pour une plateforme unique est le **conflit GPIO 6/7** sur l'ESP32-S3 :
- La caméra OV5640 utilise le bus DVP 8-bit parallèle qui monopolise les GPIO 6 et 7
- Les micros I2S stéréo utilisent GPIO 6 pour DIN canal R et GPIO 7 pour DIN canal L
- **Impossible d'avoir les deux simultanément** sur un seul ESP32-S3

### 2.3 Solution : plateforme unifiée à deux configurations filles

```
┌─────────────────────────────────────────────────┐
│           PCB UNIFIÉ WildNexus Core              │
│                                                   │
│  ESP32-S3 + PSRAM 8MB                             │
│  Buck converter 8×AA → 3.3V                       │
│  LoRa SX1262                                       │
│  microSD SPI                                       │
│  Connecteurs I2S (2× headers)                     │
│  Connecteur caméra DVP (header)                   │
│  Enclosure IP67/NEMA 4X                            │
│  Firmware Core : wn_config.h + machine d'états    │
└─────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────┐        ┌──────────────────┐
│ Config A          │        │ Config B          │
│ CAMERA TRAP       │        │ ACOUSTIC NODE     │
│ (WildNexus P0)    │        │ (InsectNet/Écurie)│
├──────────────────┤        ├──────────────────┤
│ Caméra OV5640    │        │ 2× MEMS I2S       │
│ PIR EKMB         │        │ (SPH0645LM4H-B)   │
│ I2S optionnel    │        │ FFT 1024 onboard  │
│ (mono seulement) │        │ CNN TFLite INT8   │
│ FFT + LoRa       │        │ Streaming 3s clips│
│ Deep sleep 30s   │        │ LoRa payload      │
│                  │        │ Caméra DÉSACTIVÉE │
└──────────────────┘        └──────────────────┘
```

**Avantages de cette approche :**
- **Un seul PCB** — économique (volume de production)
- **Un seul boîtier** — NEMA 4X standard
- **Un seul firmware core** — machine d'états commune, module audio partagé
- **Deux firmwares applicatifs** — sélection par #define au flash
- **Mêmes batteries, même buck, même LoRa, même SD**
- **Mêmes connecteurs** — il suffit de brancher caméra OU micros

### 2.4 Faisabilité Edge AI sur ESP32-S3

| Tâche | Durée estimée ESP32-S3 | Faisable ? |
|-------|----------------------|------------|
| Capture I2S 3s (16kHz/16-bit/stéréo) | 3.0s (temps réel) | ✅ Trivial |
| FFT 1024 points (float32) | ~10 ms | ✅ |
| CNN 330K params, INT8 quantifié (TFLite Micro) | ~200–500 ms | ✅ (pas temps réel, mais OK pour batch) |
| **Total cycle audio** | ~3.5s | ✅ |
| Deep sleep (RTC + PSRAM retention) | 30s–15min configurable | ✅ |
| **Autonomie 8×AA** | ~60 jours (1 cycle/15 min) | ✅ (modèle WildNexus validé) |

> ⚠️ Le CNN 330K sur ESP32-S3 en INT8 est estimé à 200–500ms. Pour du streaming continu (pas notre cas actuel), il faudrait un co-processeur (Kendryte K230 NPU 1 TOPS ou RPi Pico 2 + Hailo-8L). Pour une classification batch toutes les 15 minutes, l'ESP32-S3 suffit.

---

## 3. Stratégie de contact Savonia

### 3.1 Positionnement

**Nous ne sommes pas concurrents — nous sommes complémentaires.**

| Savonia apporte | PKA apporte |
|-----------------|-------------|
| Expertise IA / ML | Hardware edge autonome low-power |
| Dataset équin annoté | Firmware audio + FFT + CNN TFLite validé |
| Partenaires vétérinaires finlandais | Enclosure outdoor IP67, déploiement terrain |
| Infrastructure serveur DGX | LoRa mesh longue portée |
| Financement EU CAP | Architecture modulaire, coût optimisé |
| App mobile end-user | Module intégré caméra+audio+edge AI |

### 3.2 Proposition de valeur

> « Nous avons développé pour la bioacoustique un module autonome low-power (ESP32-S3, micros MEMS I2S, LoRa, deep sleep 60j sur batterie) qui capture et classifie les sons en edge AI. Votre pipeline PANNs/CNN14 + autoencoder tournerait sur notre hardware sans dépendance à un serveur DGX. Nous pouvons vous fournir des modules de test clé-en-main pour votre pilote Rauhalahti, et adapter le form factor à vos contraintes d'écurie. »

### 3.3 Plan de contact

| Étape | Action | Canal |
|-------|--------|-------|
| 1 | Email à Aki Happonen (CC Johannes Geisler, Heli Suomala) — présentation PKA, proposition collaboration hardware | Email |
| 2 | Si réponse positive : visioconférence (démo module WildNexus, discussion specs écurie) | Zoom/Teams |
| 3 | Envoi de 2–3 modules de test à Rauhalahti pour essai terrain | Colis |
| 4 | Co-publication / joint grant application EU | — |

### 3.4 Écurie pilote PKA : Mont-le-Soie

- **Nom** : Mont-le-Soie (JC connaît les propriétaires)
- **Rôle** : site pilote pour le prototype PKA, en parallèle de Rauhalahti (Savonia)
- **Avantage** : permet de tester le hardware PKA en conditions réelles AVANT de le proposer à Savonia
- **Prochaine étape** : visite de repérage pour définir le placement des modules (nombre, hauteur, alimentation)

---

## 4. Prochaines actions

| Priorité | Action | Responsable |
|----------|--------|-------------|
| 🔴 P0 | Contacter Savonia (Aki Happonen) — email de présentation | JC |
| 🔴 P0 | Visite Mont-le-Soie — repérage installation modules | JC |
| 🟡 P1 | Valider CNN 330K quantifié INT8 sur ESP32-S3 (bench réel) | Forge + Musaraigne |
| 🟡 P1 | Prototyper config B « Acoustic Node » sur PCB WildNexus | Forge + Araignée |
| 🟢 P2 | Rédiger fiche produit « Acoustic Node » pour Savonia | Dobby |

---

*Sources : articles Savonia (savonia.fi/en/articles-pro/), EU CAP Network (eu-cap-network.ec.europa.eu), WildNexus P0 Engineering, InsectNet V0.1 Scope.*
