# BOM-VANLIFE — Bill of Materials IoT Vanlife Lupo 🐺

> **Date :** 2026-07-09 | **Rédacteur :** [[Dobby]] 🦉  
> **Deadline projet :** 7 août 2026 (arrivée Lupo)  
> **Fichier maître.** Toute modif de BOM passe par ici.  
> **Sources :** `hardware-state.md`, `../_shared/panier-amazon-van-serre.html`, `ds300-tap/SPEC-DS300-TAP.md`, `specs/SPEC-CAN-BUS.md`, `../_shared/convergence-van-serre-capteurs.md`

---

## Résumé exécutif

| Sous-projet | Total | Déjà payé | Reste à commander | Statut |
|-------------|-------|-----------|-------------------|--------|
| **1. RPi 5 Hub (Master)** | ~445€ | ~435€ | ~10€ | 🟢 98% reçu |
| **2. DS300 Tap** | ~15€ | ~7€ | ~8€ | 🟡 47% en stock |
| **3. Capteurs Zigbee & GPIO** | ~251€ | ~4€ | ~247€ | 🔴 À commander |
| **4. WiCAN Pro (OBD/CAN)** | ~82€ | 0€ | ~82€ | 🟡 À commander |
| **5. Victron Energy (P3)** | ~210€ | 0€ | ~210€ | 🔵 P3 — après arrivée |
| **6. Divers (proto + silentblocs)** | ~27€ | 0€ | ~27€ | 🟡 À définir |
| **TOTAL** | **~1030€** | **~446€** | **~584€** | |

> **Économies cumulées :** DS300 Tap (-57€) + CAN bus TPMS+BME280 (-25€) = **~82€ d'économies nettes**  
> **Investissement CAN bus :** +82€ WiCAN Pro → delta net des optimisations = **0€** (neutre)

---

## 1. RPi 5 Hub (Master) — Cœur domotique embarqué

> **Rôle :** Hub Home Assistant OS, SSD NVMe, alimentation solaire, boîtier durci.  
> **Installation :** Meuble central Kelsey, repiqué sur F3 (10A) du DS300.

### 1.1 Déjà reçu et assemblé

| # | Composant | Réf | Qté | Prix | Statut |
|---|-----------|-----|-----|------|--------|
| 1 | Raspberry Pi 5 4GB | — | 1 | 132,09€ | ✅ Reçu |
| 2 | Alim officielle RPi 5 27W USB-C | — | 1 | 15,32€ | ✅ Reçu |
| 3 | Refroidisseur actif RPi 5 | Ventilateur + dissipateur | 1 | 9,99€ | ✅ Reçu |
| 4 | Geekworm X1205 UPS HAT | 2× 18650, pogo pins | 1 | 42,39€ | ✅ Reçu |
| 5 | Accus 18650 Flat 3400mAh CCC-5 SDIR18T | Rose, non protégés | 2 | ~6€ | ✅ Reçu (stock 20) |
| 6 | Geekworm X1201-C1 boîtier métal | Alu, passif | 1 | 18,59€ | ✅ Reçu (stock 2) |
| 7 | SSD NVMe M.2 Fanxiang 256GB | 2280 | 1 | ~25€ | ✅ Reçu |
| 8 | PCIe to M.2 NVMe Shield | Stackable GPIO | 1 | ~15€ | ✅ Reçu (stock 2) |
| 9 | PV PI HAT | AutoEcology, 150 AUD | 1 | ~90€ | ✅ Reçu |
| 10 | Sonoff ZBDongle-E | Zigbee 3.0 USB | 1 | 25,32€ | ✅ Reçu |
| 11 | UGREEN USB Audio | Dongle audio | 1 | ~10€ | ✅ Reçu |
| 12 | Step-Down HW-133 3A 5V DC-DC | Tecnoiot, 24V→5V | 1 | ~2€ | ✅ Reçu (stock 5) |
| | **Sous-total reçu** | | | **~435€** | 🟢 |

### 1.2 Reste à faire / commander

| # | Composant | Réf | Qté | Prix est. | Où ? |
|---|-----------|-----|-----|-----------|------|
| 13 | Mise en boîtier X1201-C1 | Assemblage mécanique | — | 0€ | ✅ Boîtier déjà reçu |
| 14 | Silentblocs anti-vibration | Caoutchouc M3, 4 pcs | 1 lot | ~5€ | Amazon/AliExpress |
| 15 | Coating conformal PCB | MG Chemicals 422B ou similaire | 1 | ~5€ | Amazon |
| 16 | Câble DC-DC vers F3 | Porte-fusible dérivateur + fil | 1 | ~2€ | Amazon |
| | **Sous-total à faire** | | | **~12€** | 🟡 |

> **Note alimentation 12V van :** Le HW-133 (12V→5V) sera alimenté via le porte-fusible dérivateur sur F3 du DS300. Le PV PI HAT gère l'entrée solaire et la batterie LiFePO4 externe (P3).

---

## 2. DS300 Tap — Interface passive sur tableau CBE

> **Rôle :** Lire tensions batteries, niveaux cuves, états relais depuis le DS300 sans modifier le câblage.  
> **Spec :** [`ds300-tap/SPEC-DS300-TAP.md`](ds300-tap/SPEC-DS300-TAP.md)  
> **Config :** [`ds300-tap/esphome-ds300.yaml`](ds300-tap/esphome-ds300.yaml)

| # | Composant | Réf | Qté | Prix | Statut |
|---|-----------|-----|-----|------|--------|
| 1 | ESP32-C3 Super Mini | Heemol | 1 | ~3€ | ✅ En stock (×3) |
| 2 | ADS1115 16-bit ADC I2C | Heemol ou HW-19S | 1 | ~4€ | ✅ En stock (×6) |
| 3 | Connecteur AMP MOD II 16p mâle | TE 280385-2 | 1 | ~2€ | 🔴 À commander |
| 4 | Connecteur AMP MOD II 16p femelle | TE | 1 | ~2€ | 🔴 À commander |
| 5 | Nappe 16 brins 20cm | 2.54mm pitch | 1 | ~1€ | 🔴 À commander |
| 6 | Optocoupleur PC817 | DIP-4 | 5 | ~0.75€ | 🔴 À commander |
| 7 | Résistance 47kΩ | 1/4W | 2 | ~0.10€ | 🔴 À commander |
| 8 | Résistance 10kΩ | 1/4W | 4 | ~0.20€ | 🔴 À commander |
| 9 | Résistance 1kΩ | 1/4W | 7 | ~0.35€ | 🔴 À commander |
| 10 | Résistance 100Ω | 1/4W | 5 | ~0.25€ | 🔴 À commander |
| 11 | Plaque prototype 5×7cm | Simple face | 1 | ~1€ | 🔴 À commander |
| | **Sous-total Tap** | | | **~14.65€** | 🟡 7€ en stock / 8€ à commander |

---

## 3. Capteurs Zigbee & GPIO — Monitoring vanlife

> **Rôle :** Température, humidité, ouvertures, sécurité, inclinomètre, dB.  
> **Panier principal :** [panier-amazon-van-serre.html](../_shared/panier-amazon-van-serre.html)  
> **Optimisé :** 27 items / 257€ (v4 2026-07-08, -1 vs v1)

### 3.1 Panier Amazon Belgique — 27 items / 257€

| # | Capteur | Modèle | Qté | Prix/u | Total | Usage |
|---|---------|--------|-----|--------|-------|-------|
| 1 | Ouverture portes | Aqara MCCGQ11LM | 9 | 8€ | 72€ | 5 portes + toit + frigo van + 2 serre |
| 2 | T°/HR | Sonoff SNZB-02D | 4 | 10€ | 40€ | Cellule + frigo van + 2 serre |
| 3 | Ultrason cuve serre | JSN-SR04T | 1 | 5€ | 5€ | Serre uniquement |
| 4 | PIR 12V IP65 | Optex BX-80NR | 2 | 15€ | 30€ | Périmètre van (+ serre ×1) |
| 5 | Contact sec PIR | Sonoff SNZB-04 | 2 | 6€ | 12€ | Interface PIR → Zigbee |
| 6 | Fuite eau | Aqara SJCGQ11LM | 2 | 12€ | 24€ | Van + serre |
| 7 | Relais 12V 2 canaux | SRD-12VDC | 2 | 5€ | 10€ | Ventilateurs + tiroirs |
| 8 | ESP32-S3 DevKitC-1 | — | 2 | 12€ | 24€ | µC généralistes |
| 9 | Clé Zigbee | Sonoff ZBDongle-E | 2 | 18€ | 36€ | Van + serre |
| 10 | Inclinomètre | MPU6050 GY-521 | 1 | 4€ | 4€ | Niveau van |
| | **Sous-total Amazon** | | **27** | | **257€** | 🔴 À commander |

### 3.2 Compléments hors Amazon

| # | Capteur | Modèle | Qté | Prix | Où ? | Usage |
|---|---------|--------|-----|------|------|-------|
| 11 | Upgrade frigo | Sonoff SNZB-04P | 1 | ~8€ | ITEAD | Optionnel — tamper alert, pile 5 ans |
| 12 | Upgrade toit | Sonoff SNZB-04P | 1 | ~8€ | ITEAD | Optionnel — tamper alert, pile 5 ans |
| 13 | Micro dB | INMP441 | 1 | ~3€ | AliExpress | Confort sonore bivouac |
| | **Sous-total compléments** | | **3** | **~19€** | | |

### 3.3 Déjà en stock (intégré dans les scénarios)

| # | Capteur | Modèle | Statut |
|---|---------|--------|--------|
| — | GPS position | u-blox 7 USB | 📋 P3 — rétrogradé (vitesse via CAN, position seule) |
| — | Détecteur fumée/CO | Zigbee | 📋 À définir |

> **Supprimés de la BOM :** TPMS Bluetooth (remplacé par BCM pneus ×6), BME280 extérieur (remplacé par PCM ambient air temp). Voir `specs/SPEC-CAN-BUS.md`.

---

## 4. WiCAN Pro (OBD/CAN) — Données véhicule Ford Transit Custom

> **Rôle :** Lecture CAN bus HS-CAN (PCM moteur) + MS-CAN (BCM carrosserie) via port OBD.  
> **Spec :** [`specs/SPEC-CAN-BUS.md`](specs/SPEC-CAN-BUS.md)  
> **Source PIDs :** [WiCAN-Ford-Transit](https://github.com/anthonysecco/WiCAN-Ford-Transit)

| # | Composant | Réf | Qté | Prix | Statut |
|---|-----------|-----|-----|------|--------|
| 1 | WiCAN Pro | MeatPi ESP32-S3 + STN | 1 | ~82€ | 🔴 À commander (Crowd Supply / Mouser) |
| | **Sous-total WiCAN** | | | **~82€** | 🟡 |

> **Données exposées :** vitesse, RPM, carburant, conso, T°C moteur, pression turbo, T° extérieure, DTC, état portes ×6, pression pneus ×6, batterie SOC/courant/tension. 17+ entités HA sans capteur physique.  
> **Mode stationnement :** deep sleep <1mA, periodic wake 5 min → pas de risque batterie.

---

## 5. Victron Energy (P3) — Monitoring solaire & batterie

> **Rôle :** SOC précis LiFePO4, courant charge/décharge, production solaire.  
> **Phase :** P3 — après arrivée du van et installation de base.  
> **Note :** Remplace le régulateur CBE/Antarion d'origine (boîte noire). Réversible.

| # | Composant | Modèle | Qté | Prix est. | Où ? |
|---|-----------|--------|-----|-----------|------|
| 1 | SmartShunt 500A | Victron VE.Direct | 1 | ~130€ | Amazon |
| 2 | SmartSolar MPPT 100/20 | Victron VE.Direct | 1 | ~80€ | Amazon |
| 3 | Câble VE.Direct → USB | Victron | 2 | ~0€ | Inclus ou DIY |
| | **Sous-total Victron** | | | **~210€** | 🔵 P3 |

---

## 6. Divers — Proto banc + finitions

> **Rôle :** Compléments non-capteurs, finitions mécaniques, proto banc détecteur niveau.

| # | Composant | Réf | Qté | Prix est. | Où ? | Usage |
|---|-----------|-----|-----|-----------|------|-------|
| 1 | Boost converter | MT3608 | 1 | ~2€ | AliExpress | Proto banc TL-136 |
| 2 | Chargeur Li-Ion | TC4056 | 1 | ~2€ | AliExpress | Proto banc TL-136 |
| 3 | Silentblocs M3 | Caoutchouc anti-vibration | 4 | ~5€ | Amazon | Fixation RPi dans meuble |
| 4 | Coating PCB | MG Chemicals 422B | 1 | ~5€ | Amazon | Protection humidité |
| 5 | Porte-fusible dérivateur | Mini-ATO | 1 | ~3€ | Amazon | Repiquage F3 DS300 |
| 6 | Câbles, gaines thermo, colliers | Assortiment | 1 lot | ~10€ | Amazon | Câblage général |
| | **Sous-total Divers** | | | **~27€** | 🟡 |

---

## Récapitulatif commandes à passer

### 🛒 Commande #1 — Amazon Belgique (PRIORITAIRE)
- **Contenu :** Capteurs §3.1 (27 items) + Divers §6
- **Total :** 257€ + 25€ = **~282€**
- **Deadline :** Cette semaine — livraison 3-5 jours ouvrés

### 🛒 Commande #2 — Crowd Supply / Mouser (WiCAN Pro)
- **Contenu :** WiCAN Pro ×1
- **Total :** **~82€**
- **Deadline :** Cette semaine — délai Crowd Supply ~2-3 semaines

### 🛒 Commande #3 — ITEAD + AliExpress
- **Contenu :** SNZB-04P ×2 + INMP441 + connecteurs Tap + optocoupleurs + résistances
- **Total :** 19€ + 3€ + 8€ = **~30€**
- **Deadline :** Cette semaine — AliExpress 2-3 semaines

### 🔵 Commande #4 — Victron (P3, pas urgent)
- **Contenu :** SmartShunt 500A + SmartSolar MPPT 100/20
- **Total :** **~210€**
- **Deadline :** Avant le grand départ (post-arrivée)

---

## Coût total du projet IoT Vanlife

| Poste | Montant |
|-------|---------|
| RPi 5 Hub | 445€ (déjà payé) |
| DS300 Tap | 15€ (7€ stock + 8€ à commander) |
| Capteurs Zigbee & GPIO | 251€ (à commander) |
| WiCAN Pro | 82€ (à commander) |
| Victron P3 | 210€ (reporté) |
| Divers | 27€ (à commander) |
| **TOTAL** | **~1030€** |
| **Dont déjà payé** | **~446€** |
| **Reste à payer (P1)** | **~374€** |
| **Reste à payer (P3)** | **~210€** |

---

*Document maître généré par [[Dobby]] 🦉 — 2026-07-08, mis à jour 2026-07-09 (ajout CAN bus)  
Toute modification de BOM doit être répercutée ici + `hardware-state.md` + `convergence-van-serre-capteurs.md`*
