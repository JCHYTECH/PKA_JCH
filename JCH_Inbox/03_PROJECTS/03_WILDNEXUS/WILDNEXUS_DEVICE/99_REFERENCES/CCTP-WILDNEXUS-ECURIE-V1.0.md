# Cahier des Charges — Module WildNexus « Écurie Connectée »

> Dobby 🦉 — DeepSeek V4 — 2026-07-20
> Document de référence unique — compile toutes les analyses de la session.
> Projet : **Module acoustique autonome pour surveillance d'écurie équine**
> Nom de code : **WildNexus — Acoustic Node (Config Écurie)**

---

## Table des matières

1. [Objet et périmètre](#1-objet-et-périmètre)
2. [Architecture fonctionnelle](#2-architecture-fonctionnelle)
3. [Spécifications hardware](#3-spécifications-hardware)
4. [Convergence avec la plateforme WildNexus](#4-convergence-avec-la-plateforme-wildnexus)
5. [Modèle AI et pipeline de classification](#5-modèle-ai-et-pipeline-de-classification)
6. [Analyse comparative PKA vs Savonia](#6-analyse-comparative-pka-vs-savonia)
7. [Stratégie de collaboration avec Savonia](#7-stratégie-de-collaboration-avec-savonia)
8. [Feuille de route](#8-feuille-de-route)
9. [Analyse de risques](#9-analyse-de-risques)
10. [Annexes](#10-annexes)

---

## 1. Objet et périmètre

### 1.1 Objectif

Concevoir un module acoustique autonome, basé sur la plateforme WildNexus, capable de :
- Capturer en continu le paysage sonore d'une écurie (16 kHz stéréo)
- Classifier les sons en edge AI (ESP32-S3, CNN 330K params quantifié INT8)
- Détecter les anomalies (autoencoder) et les événements critiques (supervisé)
- Alerter en temps réel via LoRa (push/SMS) sans dépendance WiFi sur site
- Surveiller la qualité d'air (NH3, CO2, TVOC, PM, température) comme facteur aggravant
- Fonctionner 60 jours sur batterie, sans câble électrique, en boîtier IP67

### 1.2 Use cases prioritaires

| Priorité | Use case | Détection |
|----------|----------|-----------|
| 🔴🔴 Critique | **Incendie** | Hausse température anormale + CO/fumée + audio crépitement |
| 🔴 Urgence | **Cheval en détresse** (coincé, blessé, coup violent) | Audio : hennissement de douleur, choc, agitation anormale |
| 🔴 Urgence | **Intrusion humaine nocturne** | Audio : pas, voix, porte (hors heures normales) |
| 🟡 Vigilance | **Cheval anxieux/stéréotypies** | Audio : gratte, tape mur, tic à l'appui |
| 🟡 Vigilance | **Qualité d'air dégradée** | NH3 > seuil, CO2 > seuil, PM2.5 > seuil |
| 🟢 Monitoring | **Présence nuisibles** (rats, oiseaux) | Audio : grattements, battements d'ailes |
| 🟢 Monitoring | **Comportement normal** (mange, boit, marche) | Baseline audio |

### 1.3 Écurie pilote

**Mont-le-Soie** (Belgique) — contact JC. Première installation de test, à valider après visite de repérage.

---

## 2. Architecture fonctionnelle

```
┌──────────────────────────────────────────────────────────────┐
│                    MODULE ÉCURIE                              │
│                                                               │
│  ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌────────────┐  │
│  │ 2× MEMS │   │ BME688  │   │ ENS160   │   │ SPS30 (PM) │  │
│  │ I2S 16k │   │ T/H/P   │   │ NH3/VOC  │   │ PM2.5/10   │  │
│  └────┬────┘   └────┬────┘   └────┬─────┘   └─────┬──────┘  │
│       │             │             │               │          │
│       └─────────────┴──────┬──────┴───────────────┘          │
│                            │ I2C bus                          │
│                     ┌──────┴──────┐                           │
│                     │  ESP32-S3   │                           │
│                     │  240 MHz    │                           │
│                     │  8MB PSRAM  │                           │
│                     └──────┬──────┘                           │
│                            │                                  │
│         ┌──────────────────┼──────────────────┐               │
│         │                  │                  │               │
│    ┌────┴────┐      ┌──────┴──────┐    ┌──────┴──────┐       │
│    │ microSD │      │ LoRa SX1262 │    │  LED statut │       │
│    │ 128 GB  │      │  868 MHz    │    │  RGB (opt.) │       │
│    └─────────┘      └──────┬──────┘    └─────────────┘       │
│                            │                                  │
└────────────────────────────┼──────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │  Gateway LoRa   │
                    │  → IP (MQTT)    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────┴────┐   ┌─────┴─────┐   ┌───┴───┐
         │  App    │   │ Dashboard │   │ SMS   │
         │ Mobile  │   │   HTML    │   │ Alert │
         └─────────┘   └───────────┘   └───────┘
```

### 2.1 Cycle de fonctionnement

```
[DEEP SLEEP 15 min]
       ↓
[WAKE — I2S capture 3s stéréo]
       ↓
[FFT 1024 → features spectrales]
       ↓
[CNN 330K INT8 → classification son]
       ↓
[Lecture BME688 + ENS160 + SPS30]
       ↓
[Fusion : audio + gaz + température]
       ↓
[Si anomalie → LoRa payload 48 octets → gateway → alerte]
[Si normal   → log sur SD + deep sleep]
[Si critique → LED rouge + LoRa prioritaire + buzzer si équipé]
       ↓
[DEEP SLEEP 15 min]
```

> **Durée cycle actif :** ~4s. **Conso active :** ~80 mA. **Conso sleep :** ~300 µA.
> **Autonomie estimée** (8×AA 2500 mAh, 1 cycle/15 min) : **~60 jours.**
> À valider sur banc de test (SOP-03 PPK2).

---

## 3. Spécifications hardware

### 3.1 Module de base (commun plateforme WildNexus)

| Composant | Spécification | Quantité | Coût unitaire |
|-----------|--------------|----------|---------------|
| MCU | ESP32-S3 DevKit (240 MHz, 512 KB SRAM, 8 MB PSRAM) | 1 | ~€8 |
| Audio | Knowles SPH0645LM4H-B I2S MEMS, SNR 65 dB(A), 20Hz–10kHz | 2 | ~€3.44 |
| Stockage | microSD 128 GB (SPI : CS=39, SCK=40, MISO=41, MOSI=42) | 1 | ~€15 |
| Connectivité | LoRa SX1262 868 MHz (SPI) | 1 | ~€12 |
| Environnement | BME280/BME688 — température, humidité, pression (I2C) | 1 | ~€3 |
| Alimentation | 8×AA + buck converter → 3.3V | 1 | ~€2 |
| Boîtier | NEMA 4X IP67, ventilation passive, joints silicone | 1 | ~€15 |
| PCB | PCB unifié WildNexus Core (headers I2S + DVP + I2C) | 1 | ~€10 |
| Divers | RTC, watchdog, IMU anti-tamper, LED RGB | — | ~€8 |
| **Total base** | | | **~€79** |

### 3.2 Capteurs additionnels — Config Écurie

| Capteur | Spécification | Usage écurie | Coût |
|---------|--------------|-------------|------|
| **ENS160** | NH3 + eCO2 + TVOC, I2C, 0x53 | Ammoniac urinaire, confinement, fumée | ~€6 |
| **SPS30** | PM2.5/PM10, I2C, 0x69 | Poussière de foin, moisissures, risque respiratoire | ~€9 |
| **Thermistance redondante** | 10k NTC sur ADC | Seuil critique température indépendant (incendie) | ~€0.30 |
| **Buzzer piézo** | 3.3V, GPIO | Alarme locale si critique + pas de réseau | ~€1 |
| **Total additionnel** | | | **~€16** |

### 3.3 Coût total module Écurie

**~€95** (base €79 + capteurs écurie €16), hors assemblage.

> Comparaison : RPi 4 nu = ~€60, sans boîtier, sans batterie, sans micros, sans capteurs gaz. Module complet RPi équivalent > €200.

### 3.4 Pinout ESP32-S3 — Config Écurie

| GPIO | Fonction | Note |
|------|----------|------|
| 15 | I2S BCLK | Bit clock — partagé 2 micros |
| 16 | I2S WS | Word select (L/R) |
| 7 | I2S DIN mic L | Data canal gauche |
| 6 | I2S DIN mic R | Data canal droit — ⚠️ conflit caméra DVP |
| 21 | I2C SDA | BME688 + ENS160 + SPS30 |
| 22 | I2C SCL | Bus partagé |
| 33 | ADC1_CH5 | Thermistance redondante |
| 14 | GPIO | Buzzer piézo |
| 39–42 | SPI SD | CS, SCK, MISO, MOSI |
| 5, 17, 18 | SPI LoRa | NSS, SCK, MOSI, MISO |

> ⚠️ **Conflit GPIO 6/7 avec caméra DVP.** En Config Écurie (Acoustic Node), la caméra est **désactivée.** Cf. §4.

---

## 4. Convergence avec la plateforme WildNexus

### 4.1 Principe : un PCB, deux configurations filles

Le PCB WildNexus Core est unique. Deux firmwares applicatifs sont flashés selon l'usage.

| | Config A — Camera Trap | Config B — Acoustic Node (Écurie) |
|---|---|---|
| **Usage** | Faune sauvage | Surveillance écurie |
| **Caméra OV5640** | ✅ Activée | ❌ Désactivée |
| **2× MEMS I2S stéréo** | ❌ Mono optionnel | ✅ Activés (GPIO 6+7 libres) |
| **PIR EKMB** | ✅ Activé | ❌ Non utilisé |
| **Capteurs gaz** | ❌ Optionnels | ✅ ENS160 + SPS30 |
| **Thermistance feu** | ❌ | ✅ ADC GPIO 33 |
| **Buzzer** | ❌ | ✅ GPIO 14 |
| **Fréquence cycle** | 15 min (photo) | 15 min (audio 3s + gaz) |
| **Modèle AI** | FFT → LoRa | CNN 330K INT8 + autoencoder |
| **LoRa payload** | 48 octets standard | 48 octets + flag alerte |

**Partagé :** ESP32-S3, PSRAM, buck converter, 8×AA, LoRa SX1262, microSD, BME688, boîtier IP67, RTC, IMU, watchdog.

### 4.2 Pourquoi pas un RPi ?

| Critère | ESP32-S3 | RPi 4/5 |
|---------|----------|---------|
| Conso sleep | ~300 µA | ~0.5–1W (pas de vrai deep sleep) |
| Autonomie 8×AA | ~60 jours | < 24h |
| Démarrage | < 100 ms | ~10–30s |
| Coût | ~€8 | ~€60–80 |
| Edge AI | CNN INT8 200–500ms | Large models OK (mais trop énergivore) |
| GPIO temps réel | Excellent | OS Linux → latence variable |

Le RPi reste pertinent pour l'entraînement (Savonia DGX, notre M1) et le gateway LoRa→IP. Pas pour le nœud terrain.

---

## 5. Modèle AI et pipeline de classification

### 5.1 Architecture à deux étages (inspirée Savonia)

```
Audio 3s stéréo
      │
      ▼
┌─────────────┐
│ Étage 1      │  Autoencoder (entraîné sur sons normaux)
│ Anomaly      │  → Erreur reconstruction > seuil = ANOMALIE
│ Detection    │  → Déclenche étage 2 + alerte immédiate
└──────┬───────┘
       │ si anomalie
       ▼
┌─────────────┐
│ Étage 2      │  CNN 330K params, INT8 quantifié (TFLite Micro)
│ Supervised   │  → Classification fine : hennissement, choc, voix, feu…
│ Classifier   │  → F1 macro > 0.90 cible
└──────┬───────┘
       │
       ▼
┌─────────────┐
│ Fusion        │  Audio + BME688 (T°C) + ENS160 (NH3) + SPS30 (PM)
│ Multi-capteur │  → Si T°C > 70° ET CO > seuil = INCENDIE (priorité max)
│               │  → Si NH3 > 25 ppm = alerte ventilation
└───────────────┘
```

### 5.2 Modèle CNN

| Paramètre | Valeur |
|-----------|--------|
| Architecture | 4× Conv2D + MaxPool + 2× Dense + Dropout |
| Entrée | Mel-spectrogramme 128×128 (3s audio → 128 bins mel × 128 frames) |
| Paramètres | ~330K |
| F1 macro (InsectNet V0.1) | 0.98 sur 5 espèces d'orthoptères |
| Format edge | TFLite Micro INT8 |
| Temps inférence ESP32-S3 | Estimé 200–500 ms (à valider sur banc) |
| Framework | TensorFlow Lite for Microcontrollers |

### 5.3 Dataset

**Objectif :** 10h+ de sons d'écurie annotés, couvrant les classes du §1.2.

| Source | Statut | Volume estimé |
|--------|--------|---------------|
| Savonia (via collaboration) | 🔴 À négocier | 100+ heures (Rauhalahti, 2024–2026) |
| Mont-le-Soie (collecte PKA) | 🔴 À démarrer | 0 (démarrage après visite repérage) |
| AudioSet (neigh/whinny) | 🟢 Disponible | Quelques centaines de clips |
| Freesound (horse sounds) | 🟢 Disponible | ~50 clips épars |

> ⚠️ Sans dataset, le CNN est un coquillage vide. La priorité absolue est la collecte de données au Mont-le-Soie ET l'accès au dataset Savonia.

---

## 6. Analyse comparative PKA vs Savonia

### 6.1 Nos avantages (PKA → Savonia)

| Axe | Savonia | PKA / WildNexus |
|-----|---------|-----------------|
| **Autonomie** | Secteur 230V, RPi 4, 5–10W continu | Batterie 8×AA, 60 jours, 300µA sleep |
| **Edge AI** | Inférence différée sur DGX (heures) | Inférence onboard temps réel (~3.5s) |
| **Robustesse** | RPi nu, intérieur uniquement | IP67, −20/+60°C, anti-ammoniac |
| **Déploiement** | Électricien requis, prises 230V | Poser le boîtier, zéro câble |
| **Coût marginal** | ~€200+ par nœud complet | ~€95 par nœud |
| **Modularité** | Monolithique (RPi fait tout) | PCB unique, 2 configs (Camera Trap / Acoustic Node) |
| **Sécurité incendie** | 230V dans poussière/paille = risque | 3.3V basse tension, aucun risque |
| **Capteurs gaz/air** | Aucun | NH3, CO2, TVOC, PM2.5/PM10 intégrés |

### 6.2 Leurs avantages (Savonia → PKA)

| Axe | Savonia | PKA / WildNexus |
|-----|---------|-----------------|
| **Dataset équin** | 7 chevaux × nuits, annoté experts (2024–) | 0 donnée équine |
| **GPU entraînement** | NVIDIA DGX (cluster entreprise) | Mac M1/M5 (consumer) |
| **Financement** | EU CAP Network, centaines k€ | Autofinancé, < 10 k€ |
| **App mobile** | 2 apps en développement (soundscape + stéthoscope) | Dashboard HTML uniquement |
| **Partenaires véto** | Vétérinaires, soigneurs, Hevostietokeskus | Mont-le-Soie (à confirmer) |
| **Visibilité** | Publications EU, Savonia Article Pro | Aucune |

### 6.3 Synthèse — Complémentarité parfaite

| Savonia apporte | PKA apporte |
|-----------------|-------------|
| Dataset équin annoté | Hardware autonome low-power |
| Modèle PANNs/CNN14 + autoencoder | Edge AI temps réel |
| App mobile end-user | Enclosure IP67 outdoor |
| Partenaires vétérinaires | LoRa mesh sans WiFi |
| Infrastructure GPU DGX | 60 jours batterie |
| Financement EU | Capteurs gaz intégrés (NH3, CO2, PM) |
| Stéthoscope intestinal | Coût marginal < €100 |

---

## 7. Stratégie de collaboration avec Savonia

### 7.1 Positionnement

**Nous ne sommes pas concurrents — nous sommes complémentaires.**

- **Eux** : boxes avec prises électriques → RPi 4 + caméra + DGX → entraînement lourd + app mobile.
- **Nous** : boxes sans électricité, combles, paddocks → module autonome batterie → edge AI temps réel + alerte LoRa.

### 7.2 Proposition de valeur

> « Vous couvrez les boxes connectés avec vos RPi. Nous couvrons tout le reste avec nos modules autonomes. Même pipeline AI, deux hardwares complémentaires. Vos données entraînent le modèle sur DGX, notre hardware le fait tourner en edge 24/7 sans infrastructure. »

### 7.3 Troc de valeur

| On donne | On reçoit |
|----------|-----------|
| Modules WildNexus de test pour Rauhalahti (2–3 unités) | Accès R&D au dataset sonore Savonia |
| Firmware audio + CNN TFLite + FFT open-source | Modèle PANNs/autoencoder (poids ou API) |
| Support technique intégration hardware | Expertise métier équin (labels, validation) |
| Co-publication potentielle | Accès au réseau EU CAP |

### 7.4 Contacts

| Nom | Rôle | Email | Tél |
|-----|------|-------|-----|
| Aki Happonen | Digital Development Manager | aki.happonen@savonia.fi | +358 44 785 6033 |
| Johannes Geisler | RDI Specialist AI/Robotics | johannes.geisler@savonia.fi | — |
| Heli Suomala | Project Manager | heli.suomala@hevostietokeskus.fi | — |

> 📧 **Draft email** prêt : `TEAM_Inbox/2026-07-20_dobby_draft-email-aki-happonen.md`
> ⏳ **Timing :** attendre validation hardware Mont-le-Soie avant envoi.

---

## 8. Feuille de route

### Phase 0 — Pré-projet (juillet–août 2026)

| Action | Resp. | Statut |
|--------|-------|--------|
| Visite Mont-le-Soie — repérage (nb boxes, électricité, placement modules) | JC | 🔴 À planifier |
| Valider CNN 330K INT8 sur ESP32-S3 physique (bench réel PPK2) | Forge | 🟡 À planifier |
| Commander ENS160 + SPS30 pour test I2C | Araignée | ⚪ P2 |
| Prototyper firmware Config Écurie (I2S stéréo + CNN + capteurs gaz) | Forge | 🟡 À planifier |

### Phase 1 — Dataset (septembre–octobre 2026)

| Action | Resp. | Livrable |
|--------|-------|----------|
| Définir protocole enregistrement (nombre modules, hauteur, durée) | Clio + Araignée | Document protocole |
| Installer 2–3 modules au Mont-le-Soie | Araignée + JC | Modules déployés |
| Collecter 10h+ de sons (normal + événements simulés) | JC | Dataset brut |
| Annotation avec experts équestres | JC + vétérinaires | Dataset annoté v0.1 |
| (Si accord) Accéder au dataset Savonia pour enrichissement | JC | Dataset fusionné |

### Phase 2 — Modèle AI (octobre–novembre 2026)

| Action | Resp. | Livrable |
|--------|-------|----------|
| Autoencoder : entraîner sur sons normaux → détection anomalies | Musaraigne + Clio | Modèle anomaly v0.1 |
| Classifieur : fine-tuner CNN 330K sur dataset écurie | Clio | Modèle classification v0.1 |
| Fusion multi-capteur : audio + T°C + NH3 → règle incendie | Clio + Forge | Algorithme fusion |
| Quantifier INT8 + exporter TFLite Micro | Musaraigne | Modèle edge v0.1 |

### Phase 3 — Pilote (décembre 2026)

| Action | Resp. | Livrable |
|--------|-------|----------|
| Déploiement 3–5 modules Mont-le-Soie | Araignée + JC | Installation terrain |
| Dashboard monitoring + alertes LoRa | Chouette + Forge | Interface opérateur |
| Validation 2 semaines avec experts | JC + vétérinaires | Rapport validation |
| Itération (faux positifs → ajustement seuils) | Clio | Modèle v0.2 |

### Phase 4 — Contact Savonia (janvier 2027 ou plus tôt si opportunité)

| Action | Canal |
|--------|-------|
| Envoi email Aki Happonen avec résultats pilote Mont-le-Soie | Email |
| Visioconférence démo hardware + résultats | Zoom/Teams |
| Expédition 2–3 modules de test à Rauhalahti | Colis |
| Négociation accès dataset + co-publication | — |

---

## 9. Analyse de risques

| Risque | P | I | Mitigation |
|--------|---|---|------------|
| **Dataset insuffisant** — pas assez d'événements rares | Élevée | Critique | Autoencoder (anomaly detection sans exemples). Simuler événements au Mont-le-Soie. Négocier accès Savonia. |
| **Bruit ambiant agricole** — tracteurs, ventilation | Élevée | Moyen | Micros MEMS directionnels, filtrage DSP. Modèle entraîné sur bruit de fond local. |
| **Faux positifs** → rejet utilisateur | Moyenne | Élevé | Pilote avec seuils conservateurs. Bouton « ignorer » sur dashboard. Feedback loop. |
| **Ammoniac dégrade micros** — vieillissement accéléré | Moyenne | Moyen | Membrane MEMS protégée par grillage + calibration périodique. ENS160 donne le niveau NH3. |
| **LoRa portée en intérieur** — murs épais, poutres métalliques | Moyenne | Élevé | Gateway placé au centre du bâtiment. Si < 100m → mesh multi-nœuds ou WiFi fallback. |
| **Autonomie réelle < 60j** — cycle audio plus lourd que photo | Faible | Moyen | Valider sur PPK2 avant déploiement (SOP-03). Ajuster fréquence si besoin (15→30 min). |

---

## 10. Annexes

### 10.1 Fichiers de référence PKA

| Fichier | Contenu |
|---------|---------|
| `03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/PROTOCOLES/SOP-13-i2s-mems-stereo.md` | Spécifications I2S stéréo |
| `03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/PROTOCOLES/SOP-14-fft-features.md` | FFT 1024 + 10 descripteurs spectraux |
| `03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/PROTOCOLES/SOP-15-clip-wav-json.md` | Capture WAV 3s + sidecar JSON |
| `03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/02_HARDWARE_SATELLITE/2026-05-22_dobby_wildnexus-onboard-sensor-matrix.md` | Matrice capteurs |
| `03_PROJECTS/03_WILDNEXUS/NEXUS_ACOUSTIC/INSECTNET/04_MODELS/baseline-results.md` | Résultats CNN 330K |
| `TEAM_Inbox/2026-07-20_dobby_analyse-surveillance-acoustique-ecurie.md` | Analyse INBOX initiale |
| `TEAM_Inbox/2026-07-20_dobby_brief-savonia-contact-hardware-convergence.md` | Brief Savonia + convergence hardware |
| `TEAM_Inbox/2026-07-20_dobby_analyse-comparative-pka-vs-savonia.md` | Analyse comparative détaillée |
| `TEAM_Inbox/2026-07-20_dobby_draft-email-aki-happonen.md` | Draft email Savonia |

### 10.2 Références externes

| Source | Lien |
|--------|------|
| Savonia — Soundscape Monitoring (article technique) | savonia.fi/en/articles-pro/monitoring-stable-soundscapes-ai-model-selection-and-development-plans/ |
| Savonia — Data Acquisition System (article hardware) | savonia.fi/en/articles-pro/horse-stall-data-acquisition-system-a-scalable-and-reliable-audio-visual-recording-and-transfer-framework/ |
| Savonia — Stéthoscope intestinal (article) | savonia.fi/en/articles-pro/technical-review-and-integration-strategy-digital-stethoscopes-for-horse-gut-sound-monitoring/ |
| EU CAP Network — Tekoälyä talleille | eu-cap-network.ec.europa.eu/projects/practice-abstracts/tekoalya-talleille_en |
| PANNs / CNN14 GitHub | github.com/qiuqiangkong/audioset_tagging_cnn |
| NFPA 150 — Fire Safety in Horse Barns | uspasecurity.com/fire-protection-guide-for-horse-barns-nfpa-150/ |
| Animal Sound Classification (ArXiv 2407.03440) | arxiv.org/abs/2407.03440 |

---

*Document de référence — version 1.0. Mis à jour après chaque session de travail sur le projet.*
