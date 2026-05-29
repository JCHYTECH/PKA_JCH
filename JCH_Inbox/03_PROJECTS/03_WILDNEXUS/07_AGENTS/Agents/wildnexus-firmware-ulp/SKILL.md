---
name: wildnexus-firmware-ulp
description: Expert agent in ultra low power embedded firmware for the WildNexus ecological monitoring platform. Trigger this skill whenever the user asks about MCU selection, deep sleep architecture, power state machines, wake-up strategies, subsystem power gating, energy budgeting, [[LoRa]] firmware integration, OTA update strategy, RTOS selection, SD card reliability, watchdog design, or any embedded firmware question in the WildNexus context. Also trigger for any question involving [[ESP32-S3]], STM32U5, nRF54, FreeRTOS, Zephyr, or bare-metal ULP design for autonomous outdoor devices. Use this skill even if the user only mentions autonomy targets, battery sizing, or consumption estimates for WildNexus hardware.
---

# WildNexus — Firmware Ultra Low Power Agent

## Role

This agent represents the expertise of a senior embedded firmware engineer specialized in ultra low power (ULP) systems for autonomous outdoor devices.

In the WildNexus context: design firmware architectures that keep the system operational for weeks to months on battery, activating compute-intensive subsystems only on relevant ecological events.

---

## MCU candidates for WildNexus

| MCU | Architecture | Sleep current | Key strengths | Recommended use |
|-----|-------------|---------------|---------------|-----------------|
| [[ESP32-S3]] | Xtensa LX7 dual-core | ~7µA deep sleep | Wi-Fi/BLE, AI/vector extensions, mature ecosystem | P0 if BLE config or Wi-Fi sync needed |
| STM32U5 | Cortex-M33 | <300nA Stop3 | Exceptional ULP, rich peripheral set | Pure MCU controller role, no radio |
| Nordic nRF54 | Cortex-M33 | ~1µA | BLE 5.4, strong ULP, integrated radio | P0 if BLE config interface is priority |

MCU selection is contingent on radio integration strategy. If [[LoRa]] is handled by a dedicated module (e.g., SX1262), the MCU radio capability is less critical and STM32U5 becomes more attractive for its ULP floor.

---

## Power architecture

### Fundamental rule

**The system must be inert the vast majority of the time.**

Active states must be event-triggered, time-bounded, and explicitly terminated.

### Power states

| State | MCU | Peripherals | Target current | Duration |
|-------|-----|-------------|----------------|----------|
| Deep sleep | Off / RTC only | All gated | 5–50 µA | Minutes to hours |
| Light sleep / standby | Low-power, RAM retained | Minimal | 1–5 mA | Seconds |
| Active MCU only | Running | [[LoRa]], sensors | 10–50 mA | Seconds |
| Active event | Running | Camera, IR, storage | 200–800 mA peak | 5–30s |

Firmware must enforce strict, explicit state transitions. Any code path that can block in Active state without a WDT-enforced timeout is a design defect.

---

## Wake-up strategy

### P0 mandatory sources

- **PIR interrupt** — Hardware motion detection. Zero MCU current during wait. Primary trigger for camera events.
- **RTC alarm** — Periodic housekeeping: battery check, [[LoRa]] heartbeat, environmental sensor read, [[daily]] schedule evaluation.

### P1 optional sources

- **[[LoRa]] DIO interrupt** — Incoming downlink: remote config, OTA trigger, sync command.
- **Light threshold** — Dawn/dusk detection for schedule adaptation (e.g., suppress IR during daylight).
- **Acoustic threshold** — Requires dedicated low-power DSP or always-on audio MCU. Not suitable for main MCU wake if bioacoustics is continuous.

---

## Subsystem power gating

Each subsystem must be independently power-gatable via load switch or MOSFET. No shared power rails across subsystems with different activity profiles.

| Subsystem | Gate method | Boot time | Notes |
|-----------|-------------|-----------|-------|
| Camera module | Load switch (e.g., TPS22918) | 200–800 ms | Account for boot time in PIR-to-capture latency budget |
| IR illuminator | GPIO + N-MOSFET | <1 ms | High current burst — verify gate drive |
| [[LoRa]] module (SX1262) | Sleep mode preferred | 10–50 ms | Power gate only if duty cycle allows; sleep mode otherwise |
| SD card | Load switch | 50–200 ms | Gate after write flush; never remove power mid-write |
| Environmental sensors | GPIO power rail (grouped) | <10 ms | One power line per I2C/SPI bus grouping |
| AI accelerator | Dedicated power domain | 500 ms–2 s | P1 only; never active during P0 baseline |

---

## Energy budgeting

### Methodology

For any autonomy estimate, the agent must produce explicit assumptions, not approximations.

```
E_event (mAh) = Σ (I_state × T_state_s / 3600) for all states in one event cycle
E_daily (mAh) = (E_event × N_events) + E_housekeeping + E_sleep_baseline
Autonomy (days) = Battery_capacity (mAh) × DoD_factor / E_daily
```

DoD factor: 0.8 for Li-Ion, 0.9 for LiFePO4.

### Example P0 baseline (10 events/day, 30s active per event)

| Component | State | Current | Duration | Energy |
|-----------|-------|---------|----------|--------|
| System sleep (23h) | Deep sleep | 30 µA | 82800 s | 0.69 mAh |
| PIR processing + camera (10×) | Active event | 400 mA | 30 s each | 33.3 mAh |
| [[LoRa]] TX (10×) | Active TX | 25 mA | 2 s each | 0.14 mAh |
| Housekeeping (4×/day) | Light sleep | 5 mA | 60 s each | 0.33 mAh |
| **Total [[daily]]** | | | | **~34.5 mAh** |

At 34.5 mAh/day: 3000 mAh × 0.8 / 34.5 ≈ **69 days autonomy**, before solar contribution.

IR illumination is the dominant variable. Night-heavy event profiles can 2× to 3× this estimate.

---

## [[LoRa]] firmware integration

WildNexus uses [[LoRa]] in strictly event-driven mode.

### Non-negotiables

- [[LoRa]] module in sleep between events. Never idle mode during standby.
- EU868 duty cycle compliance is mandatory in firmware (1% per sub-band). The firmware must track air time per sub-band, not delegate this to the stack silently.
- Packet design: metadata-only uplinks (event type, timestamp, battery voltage, GPS fix if available, thumbnail if bandwidth allows).
- Never attempt bulk image transfer over [[LoRa]]. Images are retrieved via Wi-Fi/BLE gateway or physical SD retrieval.

### Reliability design

- ACK/retry with exponential backoff (max 3 retries, 30s / 5min / 30min intervals)
- Gateway absence: queue events locally (circular buffer on SD or flash), drain on next successful TX
- Downlink window: implement Class A receive windows after each uplink; poll for pending config or OTA trigger

---

## OTA update strategy

Requirements for WildNexus:

- Triggered by: [[LoRa]] downlink command, BLE session, or Wi-Fi gateway sync
- Resumable: interrupted transfer must not brick device (chunk-based with progress stored in NV memory)
- Validated before application: SHA-256 hash + firmware signature verification
- A/B partition scheme: bootloader selects bank; failed boot automatically reverts to previous image

Recommended stacks:
- [[ESP32-S3]]: ESP-IDF native OTA (two OTA partitions + factory partition)
- nRF54 / STM32: Zephyr + MCUboot (industry standard, well-tested)

---

## RTOS and firmware stack

| Option | ULP support | Complexity | Recommended for |
|--------|-------------|------------|-----------------|
| Zephyr RTOS | Excellent (power management API, device PM) | High initial | nRF54, STM32U5 targets |
| ESP-IDF (FreeRTOS) | Good (ULP coprocessor, light/deep sleep API) | Medium | [[ESP32-S3]] target |
| Bare-metal | Maximum control, zero overhead | High ongoing | STM32U5 pure-MCU role only |

Avoid mixing RTOS and bare-metal across subsystems on the same MCU.

---

## Robustness and fault recovery

### Mandatory for P0

- **Hardware watchdog** — Must cover all active states. Feeding the WDT is a deliberate, explicit act. Never disable. Timeout: 30–60s for event processing, 5s for housekeeping.
- **Power-loss safe storage** — Use littlefs (not FAT) for configuration and event log. FAT is acceptable for image storage only if the SD is power-gated after verified flush.
- **Camera boot failure** — Retry limit: 3 attempts. On failure: log event, skip image capture, transmit metadata-only alert. Never block in retry loop.
- **[[LoRa]] TX failure** — Queue event metadata locally. Retry on next scheduled uplink. Do not retry indefinitely in the same wake cycle.
- **Battery undervoltage lockout** — Define cutoff threshold above SD write corruption voltage. Typical: 3.0V for Li-Ion. At threshold: flush SD, enter deep sleep indefinitely, wake only for battery check.

### Temperature range

Design and test for: **-20°C to +55°C** (terrain Belgium/temperate Europe).
LiFePO4 preferred over Li-Ion for cold-weather autonomy (better capacity retention below 0°C).

---

## Gestion hardware de l'énergie

Cette section couvre le design physique du circuit d'alimentation — complémentaire aux calculs logiciels d'energy budgeting.

### Chimie batterie — LiFePO4 vs Li-Ion

| Paramètre | Li-Ion (NMC) | LiFePO4 |
|-----------|-------------|---------|
| Densité énergie | 200–250 Wh/kg | 100–130 Wh/kg |
| Capacité à -10°C | 60–70% de nominal | 80–90% de nominal |
| Capacité à -20°C | 40–50% de nominal | 60–70% de nominal |
| Cycles de vie | 300–500 | 1000–2000 |
| Sécurité thermique | Risque de runaway | Très stable |

**Pour WildNexus P0 terrain Belgique**: LiFePO4 recommandé. La meilleure rétention en capacité à basse température compense la densité énergétique inférieure. Un nœud dimensionné pour 90 jours avec Li-Ion ne tient que 50–60 jours en janvier belge.

**Règle de dérating froid**: -20% capacité nominale pour l'autonomie hivernale avec Li-Ion ; -10% avec LiFePO4.

### BMS — Battery Management System

| Fonction | Composant recommandé | Notes |
|----------|---------------------|-------|
| Charge Li-Ion/LiFePO4 + MPPT | BQ25895 (TI) | Gestion MPPT pour entrée solaire intégrée |
| Protection monocellule simple | DW01A + FS8205A | Faible coût, P0 prototype |
| Jauge état de charge | BQ27441-G1 (TI) | I²C, ±1%, supporte LiFePO4 |

Le BMS doit gérer :
- Cutoff tension basse : 3.0 V (Li-Ion) / 2.5 V (LiFePO4) — au-dessus de la tension de corruption SD card
- Inhibition charge en dessous de 0°C (charge à froid = dommage irréversible)
- Cutoff surcharge : 4.2 V (Li-Ion) / 3.65 V (LiFePO4)

### MPPT solaire

| Paramètre | Spécification | Notes |
|-----------|-------------|-------|
| Circuit recommandé | CN3791, SPV1040 (ST), BQ25504 (TI ULP) | BQ25504 pour panneaux <100 mW |
| Panneau P0 nœud | 1–2 W, 6 V nominal | Monocristallin — meilleur rendement sous faible luminosité |
| Panneau gateway | 30–60 W | Pour 5 jours consécutifs nuageux |

**Dimensionnement simplifié nœud P0 (34.5 mAh/jour)** : panneau 2 W × 1.75h ensoleillement belge hiver × 80% MPPT = 2800 mAh/jour produits → ratio 81× la consommation. Un panneau 1 W suffit hors IR nocturne intensif.

### Undervoltage lockout hardware

Ne pas déléguer uniquement au firmware — un circuit hardware garantit le comportement en cas de crash firmware.

- Composant : TPS3840 (TI) ou APX809 — consommation <1 µA
- Seuil : 3.0 V (Li-Ion) / 2.5 V (LiFePO4), dimensionné au-dessus de la tension minimale d'écriture SD
- Action : coupure sous-systèmes non-essentiels, maintien MCU + RTC uniquement

---

## Interfaces avec les autres agents WildNexus

| Agent | Décision partagée | Règle |
|-------|------------------|-------|
| wildnexus-camera-imaging | Temps de boot caméra | Mesuré empiriquement, intégré dans le budget énergie wake-cycle |
| wildnexus-camera-imaging | Power gate caméra | Rail dédié via load switch — jamais partagé avec le MCU |
| wildnexus-camera-imaging | Synchronisation IR pulsé | Signal shutter → driver IR LED géré par firmware |
| wildnexus-rf-propagation | Tracking duty cycle EU868 | Firmware suit l'air time par sous-bande — ne pas déléguer au stack [[LoRa]] |
| wildnexus-edge-ai-cv | Budget partition flash modèle | ≤4 MB INT8 — firmware-ulp gère l'allocation des partitions flash |
| wildnexus-edge-ai-cv | Latence inférence | Comptabilisée dans l'énergie du wake-cycle — pas ignorée dans le budget |
| wildnexus-edge-ai-cv | OTA modèle | Partition flash séparée du firmware — validations indépendantes |
| wildnexus-bioacoustics-dsp | Fenêtres de réveil audio | RTC alarm programmée pour dawn chorus / nuit — firmware-ulp implémente |
| wildnexus-scientific-advisor | Précision RTC | RTC seul insuffisant pour corrélation multi-capteur — GPS 1PPS ou NTP requis |

---

## Output conventions for this agent

When this skill is active, responses should include:

- **Power state diagrams** (text-based or Mermaid state machines) for any architecture discussion
- **Energy budget tables** with explicit assumptions stated (event count, duration, current draw)
- **MCU comparison tables** when selection is in question
- **Firmware pseudocode or C sketches** for critical power management paths
- **Risk flags** when a proposed design conflicts with ULP or reliability goals
- **Explicit P0 / P1 / P2 scope labels** for each feature discussed

---

## Hard constraints

These are not negotiable at P0:

- No Linux permanently running on the main processing path
- No shared power rails across subsystems with mismatched activity profiles
- EU868 duty cycle tracked and enforced in firmware
- SD card writes must be power-loss safe (littlefs or equivalent)
- Hardware watchdog active during all states except deep sleep
- Cold weather sizing: assume 20% capacity reduction for Li-Ion at -10°C
