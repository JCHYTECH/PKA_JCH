# Brief — Scarabée 🪲 : Esquisse boîtier Station Météo Lupo

> Dobby 🦉 → Scarabée 🪲 — 2026-07-16 — DeepSeek V4  
> **Type :** Esquisse / exercice — v0.1 basée sur dimensions estimées  
> **Révision v1.0 :** après réception des breakouts et mesures réelles

---

## 1. Contexte

Le van Westfalia Kelsey (« Lupo ») a besoin d'une station météo intérieure connectée. Les composants électroniques sont définis (`SPEC-CAPTEUR-ENV.md`), le firmware ESPHome est prêt. Il manque le **boîtier** qui contient le tout.

Ce brief est une **esquisse** : tu travailles avec des dimensions estimées pour produire une première itération de design. Quand les composants réels arriveront (breakouts BME688 + SHT31 commandés cette semaine), on mesurera au pied à coulisse et tu affineras.

## 2. Composants à loger

### 2.1 ESP32-C3 Super Mini (µC central)
- Dimensions : **22.5 × 18 × 5 mm** (hors connecteurs)
- Connecteur USB-C : dépasse de ~2 mm sur un petit côté
- Antenne PCB : intégrée sur la carte (zone à ne pas blinder)
- LED intégrée : bleue (GPIO8), visible à travers un trou ou une fenêtre
- Pins GPIO : 2 rangées de broches, pitch 2.54 mm

### 2.2 BME688 breakout (capteur T°/HR/Pression/VOC)
- Dimensions estimées : **~15 × 12 × 3 mm** (CJMCU-688 ou Waveshare)
- Connectique : 4 broches I2C (VDD, GND, SDA, SCL)
- **Besoin critique :** exposition à l'air ambiant pour l'IAQ (qualité d'air)
- Ne pas enfermer dans un compartiment étanche

### 2.3 SHT31 breakout (capteur T°/HR précision)
- Dimensions estimées : **~15 × 12 × 3 mm** (GY-SHT31)
- Connectique : 4 broches I2C (VDD, GND, SDA, SCL)
- **Besoin :** même exposition air ambiant que le BME688

### 2.4 Câblage I2C
- 4 jumpers Dupont femelle-femelle entre ESP32-C3 et les 2 breakouts
- Bus I2C partagé : SDA (GPIO4), SCL (GPIO5), 3.3V, GND
- **Positionnement idéal :** les 2 breakouts proches du µC pour minimiser la longueur des jumpers (< 50 mm)

---

## 3. Contraintes mécaniques

### 3.1 Emplacement dans le van
- **Position :** paroi verticale du meuble central Kelsey, face intérieure, ~1m du sol
- **Fixation :** 2 vis M3 ou bande Velcro double-face au dos du boîtier
- **Orientation :** USB-C accessible par le bas ou le côté pour alimentation

### 3.2 Environnement
- Intérieur du van (pas d'exposition directe aux UV ni à la pluie)
- Température : -10°C à +50°C (van au soleil)
- Humidité : 20% à 90% RH (condensation possible la nuit)
- Vibrations : route, pistes — les composants doivent être maintenus
- Pas de contrainte IP (intérieur)

### 3.3 Ventilation
- Le BME688 a besoin d'air ambiant pour l'indice IAQ
- **Obligatoire :** ouvertures ou grille d'aération sur au moins 2 faces
- Pas de ventilation forcée (pas de ventilateur)
- Protection anti-poussière basique (maille ou chicane)

### 3.4 Matériau recommandé
- **PLA** pour les premiers prototypes (facile, rapide)
- **PETG** pour la version finale (résiste mieux à la chaleur du van en été — le PLA commence à ramollir vers 55°C, le PETG tient jusqu'à 80°C)
- Couleur : noir ou gris foncé (discret dans le meuble)

---

## 4. Contraintes fonctionnelles

### 4.1 Accessibilité
- [ ] Port USB-C accessible pour flash firmware OTA / alimentation
- [ ] LED d'état visible sans ouvrir le boîtier
- [ ] Les capteurs (BME688 + SHT31) doivent « voir » l'air de la cellule, pas l'air chauffé par l'ESP32

### 4.2 Séparation thermique
- Idéalement, les capteurs sont dans un compartiment séparé du µC (qui chauffe un peu)
- Si compartiment unique, positionner les capteurs **au-dessus** de l'ESP32 (la chaleur monte)
- Prévoir une chicane ou une paroi entre le µC et les capteurs

### 4.3 Maintenance
- Le boîtier doit pouvoir s'ouvrir sans outil (clips) ou avec 2 vis maximum
- Les 2 breakouts doivent être accessibles pour remplacement éventuel

---

## 5. Livrable attendu (esquisse)

### 5.1 Format
- Fichier source paramétrique (`.FCStd` FreeCAD, `.scad` OpenSCAD, ou `.f3d` Fusion 360)
- Export STL ou 3MF prêt à slicer

### 5.2 Contenu de l'esquisse
- [ ] Vue extérieure : forme générale, emplacement ouvertures, LED, USB-C
- [ ] Vue intérieure : position des 3 composants, chemin des jumpers I2C
- [ ] Système de fixation au meuble (trous de vis ou passage Velcro)
- [ ] Système d'ouverture/fermeture (clips ou vis)
- [ ] Dimensions extérieures approximatives

### 5.3 Pas besoin pour l'esquisse
- Tolérances précises (on mesurera les vrais composants)
- Profil d'impression (PrusaSlicer) — ça viendra en v2

---

## 6. Prochaines étapes

| # | Quoi | Qui | Quand |
|---|------|-----|-------|
| 1 | Commander breakouts Amazon | JC | Cette semaine |
| 2 | Esquisse v0.1 (ce brief) | Scarabée | ~3 jours |
| 3 | Réception breakouts → souder headers | JC | ~1 semaine |
| 4 | Mesurer au pied à coulisse | JC → Dobby |
| 5 | Révision v1.0 (dimensions réelles) | Scarabée | Après mesure |
| 6 | Imprimer v1.0 (PLA) | Scarabée → Prusa Mini+ | Après v1.0 |
| 7 | Test d'ajustement | JC | Après impression |
| 8 | v2.0 corrections + PETG final | Scarabée | Après test |

---

## 7. Références

- `iot-van/specs/SPEC-CAPTEUR-ENV.md` — Spec fonctionnelle + firmware ESPHome
- `iot-van/ASSEMBLAGE-RPi5-VANLIFE.md` — Contexte assemblage van
- `iot-van/BOM-VANLIFE.md` — BOM maître
- ESP32-C3 Super Mini datasheet : https://www.espboards.dev/esp32/esp32-c3-super-mini/
- BME688 datasheet : https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/
- SHT31 datasheet : https://sensirion.com/products/catalog/SHT31-DIS-B/

---

*Brief créé par [[Dobby]] 🦉 — 2026-07-16 — modèle: deepseek-v4*  
*Destinataire : [[Scarabée]] 🪲 — Première mission*  
*À archiver dans `TEAM_Inbox/` après livraison de l'esquisse*
