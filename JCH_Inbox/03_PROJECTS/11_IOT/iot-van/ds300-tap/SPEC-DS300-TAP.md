# SPEC-DS300-TAP — Interface ESP32 sur connecteur CBE DS300

> **Statut :** SPEC v1.0 — À implémenter  
> **Date :** 2026-07-08 | **Rédacteur :** [[Dobby]] 🦉  
> **Matériel cible :** Westfalia Kelsey 2026 (Ford Transit Custom) — Boîtier CBE DS300 + panneau PC100/PC180  
> **Source pinout :** [WomoNET Wiki — CBE DS Powerblock Series](https://wiki.womonet.io/protocols/cbe_ds_series/)

---

## 1. Objectif

Lire **sans modification ni coupure** les signaux du boîtier CBE DS300 via son connecteur panneau 16 broches (J9), pour exposer dans Home Assistant :

- Tensions batteries (porteur B1 + cellule B2)
- Niveaux cuves eau propre et eau grise
- État relais (pompe, frigo, éclairage)
- Signal D+ (moteur tournant)
- Présence secteur 230V

Tout cela **sans remplacer le panneau d'origine** — le PC100/PC180 continue de fonctionner normalement.

---

## 2. Économies réalisées

| Capteur supprimé | Économie | Note |
|------------------|----------|------|
| Jauges eau van (JSN-SR04T ×2 ou TL-136) | ~15-45€ | Sondes résistives déjà dans les cuves |
| Capteur tension batterie véhicule (ESP32) | — | 1 ESP32 libéré pour autre usage |
| Détecteur 230V shoreline | — | Signal gratuit |
| Signal D+ alternateur | — | Critique pour scénarios roulage, gratuit |

**Économie nette BOM : ~15-45€** (les JSN-SR04T étaient à 5€/pièce, la TL-136 déjà reçue peut être réaffectée à la serre).

---

## 3. Connecteur J9 — Pinout complet

Connecteur : **TE Connectivity AMPMODU MOD II 16 broches**, pas 2.54mm, double rangée.  
Référence sur PCB : **J9**.  
Brochage (vue de face sur le boîtier DS300, broche 1 en haut à gauche) :

```
         J9 — Vue de face DS300
    ┌──────────────────────────┐
    │  1 ███  2 ███            │  Rangée haute (1-8)
    │  3 ███  4 ███            │
    │  5 ███  6 ███            │
    │  7 ███  8 ███            │
    │  9 ███ 10 ███            │
    │ 11 ███ 12 ███            │
    │ 13 ███ 14 ███            │
    │ 15 ███ 16 ███            │  Rangée basse (9-16)
    └──────────────────────────┘
```

| Pin | Signal | Type | Plage | Usage HA |
|-----|--------|------|-------|----------|
| 1 | TBD | — | — | Non utilisé |
| 2 | **Eau propre pin 2** | Résistif | 0-190 Ω typ. | `sensor.fresh_water_level` |
| 3 | **GND** | Masse | 0V | Référence |
| 4 | **Relais frigo** | Digital OUT | 0V (off) / 12V (on) | `binary_sensor.fridge_relay` |
| 5 | **D+ (alternateur)** | Digital IN | 0V / 12V | `binary_sensor.engine_running` |
| 6 | **Relais pompe eau** | Digital OUT | GND-switched | `binary_sensor.water_pump` |
| 7 | **Eau propre pin 4** | Résistif | 0-190 Ω typ. | Même sonde que pin 2 |
| 8 | **Eau propre pin 3** | Résistif | 0-190 Ω typ. | Même sonde que pin 2 |
| 9 | **Eau grise pin 2** | Résistif | 0-190 Ω typ. | `sensor.grey_water_level` |
| 10 | **Présence 230V** | Digital IN | 0V / 12V | `binary_sensor.shore_power` |
| 11 | **AGND** | Masse analogique | 0V | Référence sondes |
| 12 | **12V+ B1 (porteur)** | Tension | 11.5-14.8V | `sensor.starter_battery_voltage` |
| 13 | TBD | — | — | Non utilisé |
| 14 | **Relais principal** | Digital OUT | GND-switched | `binary_sensor.main_relay` |
| 15 | **12V+ B2 (cellule)** | Tension | 11.5-14.6V (LiFePO4) | `sensor.leisure_battery_voltage` |
| 16 | TBD | — | — | Non utilisé |

> **Note relais :** La plupart des relais utilisent du low-side switching (ground-switching). Le relais frigo (pin 4) fait exception : high-side 12V.  
> **Note sondes eau :** Sondes résistives 3 fils (propre) et 2 fils (grise). Résistance typique 0-190 Ω proportionnelle au niveau. Le PC100 envoie un petit courant et mesure la tension — à vérifier sur place.

---

## 4. Schéma de câblage

### 4.1 Principe du « T » passif

```
┌──────────┐       nappe 16 brins        ┌──────────────┐
│  DS300   │─────────────────────────────│  PC100/PC180 │
│  J9      │                             │  (origine)   │
└──────────┘                             └──────────────┘
     │
     │  connecteur « T » (AMP MOD II mâle → femelle + dérivation)
     │
     ├──→ Pin 3 (GND) ────────────────→ ESP32 GND
     ├──→ Pin 12 (B1) ──[div 4.7:1]──→ ADS1115 AIN0
     ├──→ Pin 15 (B2) ──[div 4.7:1]──→ ADS1115 AIN1
     ├──→ Pin 2,7,8 (eau propre) ─────→ ADS1115 AIN2 (via résistance pull-up)
     ├──→ Pin 9 (eau grise) ──────────→ ADS1115 AIN3 (via résistance pull-up)
     ├──→ Pin 5 (D+) ───[optocoupleur]─→ ESP32 GPIO 4
     ├──→ Pin 10 (230V) ─[optocoupleur]─→ ESP32 GPIO 5
     ├──→ Pin 4 (frigo) ─[optocoupleur]─→ ESP32 GPIO 6
     ├──→ Pin 6 (pompe) ─[optocoupleur]─→ ESP32 GPIO 7
     └──→ Pin 14 (main) ─[optocoupleur]─→ ESP32 GPIO 8
```

### 4.2 Détail par type de signal

#### Tensions B1/B2 (pins 12, 15)
```
B1/B2 (0-15V) ──┬── R1 47kΩ ──┬── ADS1115 AINx (0-3.3V)
                 │              │
                 └── R2 10kΩ ───┴── GND
                 
Ratio : 10/(47+10) = 0.175 → 15V → 2.63V (sécurisé pour ADS1115 3.3V)
```

#### Sondes eau résistives (pins 2-7-8, 9)
```
VCC 3.3V ─── R_pullup 1kΩ ───┬── ADS1115 AINx
                               │
                    Sonde cuve (0-190Ω vers AGND)
                               │
                              GND
```
> **À valider sur place :** la tension mesurée correspond à VCC × (R_sonde / (R_sonde + R_pullup)).  
> Avec R_pullup 1kΩ et sonde 0-190Ω → plage 0-0.53V. Amplifiable si nécessaire.

#### Signaux digitaux 12V (pins 4, 5, 10)
```
Signal 12V ─── R 1kΩ ───┬── optocoupleur PC817 LED (+) ───┐
                         │                                   │
                        GND ─── optocoupleur LED (-) ───────┘
                         
Optocoupleur sortie : collecteur → ESP32 GPIO (pull-up interne), émetteur → GND
```

#### Relais ground-switched (pins 6, 14)
```
Pin relais ─── R 10kΩ ─── 12V (pull-up externe)
       │
       └── R 1kΩ ─── optocoupleur PC817 LED (+) ───┬── Pin relais
                                                     │
                                      LED (-) ──────┘
                                                     │
                                                    GND
```
> Le PC100 met la pin à GND pour activer le relais → le pull-up 12V maintient le signal HIGH au repos. L'optocoupleur s'allume quand ça passe à GND.

---

## 5. Liste composants

| Composant | Qté | Prix/u | Total | Lien |
|-----------|-----|--------|-------|------|
| ESP32-C3 Super Mini | 1 | ~3€ | 3€ | Déjà en stock (×3) |
| ADS1115 16-bit ADC | 1 | ~4€ | 4€ | Déjà en stock (×6) |
| Connecteur AMP MOD II 16p mâle | 1 | ~2€ | 2€ | Farnell/Mouser 280385-2 |
| Connecteur AMP MOD II 16p femelle | 1 | ~2€ | 2€ | Farnell/Mouser |
| Nappe 16 brins 20cm | 1 | ~1€ | 1€ | Aliexpress |
| Optocoupleur PC817 | 5 | ~0.15€ | 0.75€ | Aliexpress |
| Résistance 47kΩ | 2 | ~0.05€ | 0.10€ | Aliexpress |
| Résistance 10kΩ | 4 | ~0.05€ | 0.20€ | Aliexpress |
| Résistance 1kΩ | 7 | ~0.05€ | 0.35€ | Aliexpress |
| Résistance 100Ω | 5 | ~0.05€ | 0.25€ | Aliexpress |
| Plaque prototype 5×7cm | 1 | ~1€ | 1€ | Aliexpress |
| **Total** | | | **~14.65€** | |

> **Stock disponible :** ESP32-C3 (×3), ADS1115 (×6). Reste ~8€ à commander (connecteurs + optocoupleurs + résistances).

---

## 6. Configuration ESPHome

Voir fichier [`esphome-ds300.yaml`](esphome-ds300.yaml) pour la configuration complète.

### Entités Home Assistant créées

| Entité | Type | Description |
|--------|------|-------------|
| `sensor.starter_battery_voltage` | Voltage (V) | Tension batterie porteur B1 |
| `sensor.leisure_battery_voltage` | Voltage (V) | Tension batterie cellule B2 |
| `sensor.fresh_water_level` | % | Niveau cuve eau propre |
| `sensor.grey_water_level` | % | Niveau cuve eau grise |
| `binary_sensor.engine_running` | ON/OFF | Moteur tournant (D+) |
| `binary_sensor.shore_power` | ON/OFF | Branché sur secteur 230V |
| `binary_sensor.water_pump` | ON/OFF | Pompe eau activée |
| `binary_sensor.fridge_relay` | ON/OFF | Relais frigo activé |
| `binary_sensor.main_relay` | ON/OFF | Relais principal 12V cellule |

---

## 7. Procédure d'installation

### Phase 0 — Validation sur table (avant installation van)

1. Commander connecteurs AMP MOD II + optocoupleurs + résistances (~8€)
2. Assembler le circuit sur plaque prototype
3. Flasher ESPHome sur ESP32-C3
4. **Test sans DS300 :** simuler les signaux avec alim de labo
   - B1/B2 : 0-15V → vérifier lecture ADC
   - Sondes : potentiomètre 200Ω → vérifier mapping niveau
   - Signaux digitaux : 12V sur entrées optocoupleurs

### Phase 1 — Installation van (1h)

1. Localiser le boîtier DS300 (meuble central, trappe sous grille)
2. Débrancher **proprement** la nappe J9 → PC100
3. Insérer le connecteur T : DS300 → T mâle → [T femelle → PC100] + [T dérivation → ESP32]
4. Fixer l'ESP32 + plaque proto dans le meuble (velcro ou vis)
5. Alimenter l'ESP32 via F3 (même circuit que le RPi 5)
6. Vérifier dans HA que toutes les entités apparaissent
7. Étalonner les sondes eau (cuve vide = 0%, cuve pleine = 100%)

### Phase 2 — Étalonnage

1. **Batteries :** mesurer au multimètre → ajuster `multiply` dans ESPHome
2. **Eau propre :** remplir la cuve → noter tension ADC à 0%, 25%, 50%, 75%, 100% → fonction de calibration
3. **Eau grise :** idem
4. **Signaux digitaux :** vérifier état dans HA en actionnant chaque circuit

---

## 8. Impact sur les autres documents

| Document | Changement |
|----------|------------|
| `panier-amazon-van-serre.html` | Déjà fait — JSN-SR04T van supprimés |
| `convergence-van-serre-capteurs.md` | Déjà fait — jauge eau van → 0 |
| `scenarios-algorithmes-vanlife.md` | ✅ Fait (09/07) — entités DS300 + CAN bus référencées |
| `BOM-VANLIFE.md` | ✅ Fait (09/07) — WiCAN Pro ajouté, TPMS/BME280 supprimés |
| `specs/SPEC-CAN-BUS.md` | ✅ Créé (09/07) — spec OBD/CAN complémentaire |
| `hardware-state.md` | ✅ Fait (09/07) — WiCAN Pro ajouté |

> **Note intégration CAN bus :** Le WiCAN Pro (OBD-II) fournit 17+ entités HA complémentaires (vitesse, RPM, carburant, conso, T°C, turbo, DTC, portes ×6, pneus ×6, batterie). Voir `../specs/SPEC-CAN-BUS.md`. Le DS300 Tap reste indispensable pour les données camping (tensions B1/B2, D+, 230V, niveaux eau, relais) qui ne sont pas sur le CAN Ford.

---

## 9. Risques et inconnues

| Risque | Probabilité | Mitigation |
|--------|------------|------------|
| Brochage réel différent du WomoNET Wiki | Moyenne | Valider au multimètre avant branchement |
| Sondes eau non standards sur Kelsey | Faible | CBE standardise ses sondes ; mesure sur place |
| Interférence électrique dans le meuble | Faible | ADS1115 16-bit + filtrage passe-bas ESPHome |
| Court-circuit si mauvaise isolation | Faible | Optocoupleurs sur tous les signaux 12V |
| Garantie Westfalia | À vérifier | Connecteur T = réversible, aucune coupure |

---

## 10. Références

- [WomoNET Wiki — CBE DS Powerblock Series](https://wiki.womonet.io/protocols/cbe_ds_series/) — Pinout source
- [WomoNET — Open-source RV IoT](https://wiki.womonet.io/) — Projet de référence
- [CBE DS300 Manual (PDF)](https://www.12voltplanet.co.uk/user/downloads/CBE%20PC100%20KIT%20&%20PC200%20KIT%20instruction%20manual.pdf) — Manuel officiel
- [Westfalia Fan Forum — Technik & Umbauten](https://www.westfalia-fan.de/forum/technik-und-umbauten) — Communauté
- [`stylevan-equinox4-cahier-technique-iot.md`](../docs/stylevan-equinox4-cahier-technique-iot.md) — Notre cahier technique
- [ADR-002 — Choix Zigbee](../adr/ADR-002-zigbee-vs-z-wave-vs-ble.md) — Décision protocole

---

*Document créé par [[Dobby]] 🦉 — 2026-07-08  
À faire valider par [[Forge]] 🦦 (intégration électrique) et [[Araignée]] 🕷️ (ESPHome)*
