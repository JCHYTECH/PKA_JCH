# [ARCHIVÉ 2026-06-30] BOM Capteurs — Vanlife IOT
> ⚠️ Document historique — l'état vivant du matériel est dans `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md`

> Inventaire détaillé des capteurs Zigbee pour Stylevan Equinox 4
> Analyse multi-sources : communauté vanlife + HA + Zigbee2MQTT
> Date : 2026-06-07 | Rédacteur : [[Dobby]] 🦉

---

## Grille de critères techniques

Chaque capteur est évalué sur 12 critères. Le protocole Zigbee 3.0 est un prérequis gate.

### Ponderation

| # | Critère | Poids | Justification van |
|---|---------|-------|-------------------|
| C1 | **Zigbee 3.0 natif** | Gate | Mesh, basse conso, HA/Z2M natif |
| C2 | **Dimensions** (L×l×h mm) | 15% | Montant porte, coin meuble, toit |
| C3 | **Montage adhésif 3M** (sans perçage) | 15% | Garantie van, réversibilité |
| C4 | **Casing solidité** (IP, UV, vibrations) | 15% | Vibrations route, soleil par hublots |
| C5 | **Autonomie pile** | 10% | Pas de changement en voyage |
| C6 | **Portée Zigbee** (environnement métallique) | 10% | Van = cage de Faraday partielle |
| C7 | **Plage température** (°C) | 5% | -10°C hiver / +50°C été intérieur van |
| C8 | **Communauté** retours ZHA/Z2M | 10% | Bugs = rejet |
| C9 | **Disponibilité** Amazon EU / AliExpress | 5% | Lead time < 1 semaine |
| C10 | **Prix unitaire** (qty 5+) | 5% | Budget serré |
| C11 | **Pile changeable / reset** | 5% | Pas de SAV en voyage |
| C12 | **Compatibilité ZHA native** | 5% | Bind, reporting, pas de hack |

**Score max : 100**

---

## 1. Capteurs d'ouverture (portes, hayon, toit, frigo, tiroirs)

### Concurrents identifiés

| Modèle | Type | Dimensions (mm) | Pile | Autonomie | Prix | Écart max. |
|--------|------|-----------------|------|-----------|------|------------|
| **Aqara MCCGQ11LM** | Contact magnétique | 41×22×11 | CR1632 | 2 ans | ~8€ | 22 mm |
| **Sonoff SNZB-04** | Contact magnétique | 59×22×9 | CR1632 | 2 ans | ~6€ | 15 mm |
| **Sonoff SNZB-04P** | Contact magnétique (v2) | 59×22×9 | CR2477 | **5 ans** | ~9€ | 18 mm |

### Recherche communautaire

| Source | Résultat |
|--------|----------|
| **Zigbee2MQTT** (compatible Z2M) | Les deux sont supportés nativement (Z2M) — exposent `contact`, `battery_low`, `tamper` |
| **Reddit r/homeassistant** | Les deux sont fiables. Aqara plus compact — meilleur pour montages discrets. Sonoff meilleur rapport qualité/prix |
| **Aqara Forum** | Utilisateurs rapportent que les SNZB-04 (Sonoff) sont fiables, même sur hubs Aqara |
| **Espaces restreints van** | L'Aqara (41 mm) tient sur le montant porte du Ford Transit — le Sonoff (59 mm) dépasse de 40% |

### Score comparatif

| Critère | Poids | Aqara MCCGQ11LM | Score | Sonoff SNZB-04P | Score |
|---------|-------|-----------------|-------|-------------------|-------|
| Dimensions | 15 | 41×22×11mm — tient partout | **15** | 59×22×9mm — long | 10 |
| Montage adhésif | 15 | 3M fourni, tient bien | **15** | 3M fourni (v2 renforcé) | 14 |
| Casing | 15 | Plastique ABS, solide | **12** | Plastique + anti-tamper (v2) | **14** |
| Autonomie | 10 | 2 ans (CR1632) | 8 | **5 ans (CR2477, v2)** | **10** |
| Portée | 10 | 30m champ libre, 10m van | 8 | 30m champ libre, 10m van | 8 |
| Plage T° | 5 | -10~+45°C | 4 | -10~+50°C | **5** |
| Communauté | 10 | Très large, bugs connus | **10** | Bonne, v2 résout v1 | 8 |
| Disponibilité | 5 | Amazon/AliExpress | **5** | Amazon/AliExpress | **5** |
| Prix (x5) | 5 | ~8€ | 4 | ~9€ | 4 |
| Pile/reset | 5 | CR1632 facile, reset OK | **5** | CR2477 facile, reset OK | **5** |
| ZHA native | 5 | Full support | **5** | Full support | **5** |
| **Total** | **100** | | **91** | | **88** |

### Recommandation

> **Aqara MCCGQ11LM** pour portes avant, coulissantes, hayon (x5) — gain de 18 mm essentiel pour les montants Ford.
> **Sonoff SNZB-04P** pour toit relevable et frigo — meilleure autonomie pour accès moins fréquents.

| Usage | Qté | Modèle recommandé | Prix unit. | Total |
|-------|-----|-------------------|------------|-------|
| Porte avant conducteur | 1 | Aqara MCCGQ11LM | 8 € | 8 € |
| Porte avant passager | 1 | Aqara MCCGQ11LM | 8 € | 8 € |
| Porte coulissante G | 1 | Aqara MCCGQ11LM | 8 € | 8 € |
| Porte coulissante Dr | 1 | Aqara MCCGQ11LM | 8 € | 8 € |
| Hayon arrière | 1 | Aqara MCCGQ11LM | 8 € | 8 € |
| Toit relevable | 1 | Sonoff SNZB-04P | 9 € | 9 € |
| Porte frigo | 1 | Sonoff SNZB-04P | 9 € | 9 € |
| Tiroirs (option) | 2 | Sonoff SNZB-04P | 9 € | 18 € |
| **Total portes** | **9-11** | | | **~50-76 €** |

---

## 2. Capteurs température / humidité

### Concurrents identifiés

| Modèle | Type | Dimensions (mm) | Pile | Autonomie | Précision | Prix |
|--------|------|-----------------|------|-----------|-----------|------|
| **Sonoff SNZB-02** | T°/HR simple | 61×61×14 | CR2032 | ~1 an | ±0.3°C | ~8 € |
| **Sonoff SNZB-02D** | T°/HR avec écran LCD | 61×61×14 | CR2032 | ~1 an | **±0.2°C** | ~10 € |
| **Sonoff SNZB-02P** | T°/HR nouvelle gen | 60×60×14 | CR2450 | **~4 ans** | **±0.2°C** | ~12 € |
| **Aqara WSDCGQ11LM** | T°/HR classic | 39×39×12 | CR2032 | 2-3 ans | ±0.3°C | ~10 € |

### Recherche communautaire

| Source | Résultat |
|--------|----------|
| **zigbeeguru.com** (2026) | Aqara meilleure autonomie mais reporting lent en température stable. Sonoff rafraîchit toutes les minutes mais consomme plus |
| **haade.fr** (test comparatif) | « Sonoff SNZB-02 est légèrement plus précis que l'Aqara WSDCGQ11LM (±0.3°C vs ±0.5°C rapporté) » |
| **Reddit HA** | « Sonoff updates every few minutes — Aqara can go more than an hour without sending data if stable » |
| **Sonoff SNZB-02D (v2)** | Nouvelle version 2025 : affichage LCD, ±0.2°C, 5s refresh — idéal pour le frigo (lecture directe) |
| **HA Community** | Certains rapportent que le SNZB-02 ne montre pas de connexion réseau constante dans ZHA, mais les données arrivent bien |

### Analyse van

- **Cellule** : besoin de rafraîchissement rapide (variations rapides avec ouverture toit/portes) → Sonoff SNZB-02P (refresh 5s)
- **Frigo** : besoin de précision + lecture directe → Sonoff SNZB-02D (écran LCD, ±0.2°C)
- **Humidité** : Aqara OK pour humidité mais reporting trop lent pour la condensation

### Recommandation

| Usage | Qté | Modèle | Prix | Total |
|-------|-----|--------|------|-------|
| Cellule (T° + HR) | 1 | Sonoff SNZB-02P (autonomie 4 ans, refresh rapide) | 12 € | 12 € |
| Frigo (T° avec écran) | 1 | Sonoff SNZB-02D (lecture directe, ±0.2°C) | 10 € | 10 € |
| **Total T°** | **2** | | | **~22 €** |

---

## 3. PIR extérieur (présence extérieure)

### Analyse technique

Deux approches :
1. **Capteur Zigbee outdoor IP65 natif** — Peu de choix fiables et validés en vanlife. Aqara P1 pas IP, Philips Hue trop cher. Ex: Tuya Zigbee outdoor PIR IP65 (~15€, fiabilité douteuse)
2. **PIR 12V filaire alarme-grade + contact sec Zigbee** — Optex/Paradox IP65 (~12€) + Sonoff SNZB-04 en contact sec (~8€) = solution robuste éprouvée

### Recommandation

Option 2 — **PIR 12V IP65 filaire** (Optex BX-80NR ou Paradox D327X, ~15€) + **Sonoff SNZB-04** configuré en contact sec (wire les sorties du PIR sur les bornes du Sonoff).

- Avantages : PIR alarme-grade (vrai IP65, -20°C à +60°C), détection 12m, séparation des circuits
- Inconvénient : nécessite câblage 12V depuis F3

### Budget

| Composant | Qté | Prix |
|-----------|-----|------|
| PIR 12V IP65 (Optex/Paradox) | 1 | ~15 € |
| Sonoff SNZB-04 (contact sec) | 1 | ~6 € |
| Câble 2×0.5mm² 3m | 1 | ~3 € |
| **Total PIR extérieur** | | **~24 €** |

---

## 4. Capteurs de niveaux

### 4.1 Eau propre et eau grise

| Condition | Valeur |
|-----------|--------|
| Réservoir eau propre | 80 L (sonde CBE tiges métalliques, paliers 25%) |
| Réservoir eau grise | ~60 L (vis sondes inox, contact plein/vide) |
| Contrainte | Sondes CBE fermées — lecture uniquement sur panneau Stylevan |

**Option retenue : JSN-SR04T ultrason par le dessus** (indépendant du CBE, précis, IP67)

| Capteur | Qté | Modèle | Prix unit. | Total | Phase |
|---------|-----|--------|------------|-------|-------|
| Ultrasons eau propre | 1 | JSN-SR04T étanche | ~5 € | 5 € | P3 |
| Ultrasons eau grise | 1 | JSN-SR04T étanche | ~5 € | 5 € | P3 |

### 4.2 Gaz (bonbonne propane/butane)

**Absent du BOM [[Forge]] — nouveau capteur, phase P3.**

Alimente Webasto chauffage + plaque cuisson. Standard européen bouteille 11-13 kg.

**Options disponibles :**

| Modèle | Principe | Prix | HA | Convient si |
|--------|----------|------|----|-------------|
| **Mopeka Pro Check** | Ultrason BLE sous la bouteille | ~45 € | ESPHome natif | Bouteille ACIER |
| DIY Load Cell | Pesée (HX711 + ESP32) | ~25 € | ESPHome custom | TOUS types |
| Capteur Hall magnétique | Lecture jauge existante | ~15 € | ESPHome | Bouteille ACIER avec jauge |

**Recommandation : Mopeka Pro Check** (~45 €) si bouteille acier. Si composite → DIY load cell.

> Mopeka : ultrason qui traverse l'acier → mesure le niveau de gaz liquide → remonte en BLE → ESP32 proxy ESPHome → HA. Standard vanlife, CR2477, 2+ ans, ±3%.

**À vérifier avant commande :** type de bouteille à bord (acier ou composite ?)

---

## 5. Capteurs additionnels

### Zigbee (via dongle)

| Capteur | Qté | Modèle | Prix unit. | Total | Note |
|---------|-----|--------|------------|-------|------|
| Fuite d'eau | 1 | Aqara SJCGQ11LM | ~12 € | 12 € | Sous évier van |
| Vibration/détection | 1 | Sonoff SNZB-03 | ~8 € | 8 € | Option coffre |

### Filaire (ESP32 / RPi GPIO)

| Capteur | Qté | Modèle | Prix unit. | Total |
|---------|-----|--------|------------|-------|
| Db ambiant (I2S) | 1 | INMP441 (MEMS) | ~3 € | 3 € |
| Inclinaison (I2C) | 1 | MPU6050 (GY-521) | ~3 € | 3 € |

---

## 6. Budget total capteurs

| Catégorie | Qté | Total | Phase |
|-----------|-----|-------|-------|
| Capteurs ouverture (portes/hayon/toit/frigo) | 7 | 58 € | **P1** |
| Capteurs T°/HR (cellule + frigo) | 2 | 22 € | **P1** |
| Capteurs filaires (dB MEMS + inclino) | 2 | 6 € | **P1** |
| PIR extérieur + contact sec | 2 | 24 € | **P2** |
| Capteurs additionnels (fuite, vibration) | 2 | 20 € | **P2** |
| Jauges eau JSN-SR04T (propre + grise) | 2 | 10 € | **P3** |
| Capteur gaz Mopeka Pro Check | 1 | 45 € | **P3** |
| **Total capteurs** | **18** | **~185 €** | |

---

## 6. Zigbee dongle

Le dongle doit être Zigbee 3.0 + ZHA compatible + firmware flashable.

| Modèle | Chipset | Prix | Note |
|--------|---------|------|------|
| **Sonoff ZBDongle-E** | EFR32MG21 | 20 € | Recommandé — native ZHA, firmware à jour, longue portée |
| Conbee II | FTDI | 35 € | Stable, mais 2× plus cher |
| TubeZB | CC2652P7 | 25 € | Excellent, mais stock irrégulier |

> **Recommandation :** Sonoff ZBDongle-E (déjà dans le BOM [[Forge]], 20 €)

---

## Références

- [[VAL-BOM-Vanlife-IOT_Forge_2026-05-31]] — BOM général
- [[scenarios-algorithmes-vanlife]] — Scénarios d'utilisation
- [[ESP32-INMP441-capteur-bruit-dB]] — Fiche technique dB
- [[projet-vanlife-iot-foundation]] — Budget global ~635 €

---

*Document v1.0 — [[Dobby]] 🦉, 2026-06-07. Recherche communautaire : Reddit HA, Zigbee Guru, HA Community, Zigbee2MQTT, forum Aqara / Sonoff.*
