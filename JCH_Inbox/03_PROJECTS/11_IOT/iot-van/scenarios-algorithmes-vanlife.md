# Scénarios & Algorithmes — Vanlife IOT

> Document de conception des automatismes intelligents du Westfalia Kelsey 2026 (Ford Transit Custom)
> Version : v1.1 — 2026-07-09 (ajout CAN bus + nouveaux scénarios)
> Réglages : tous les seuils sont des `input_number` ajustables depuis le dashboard — pas de valeurs en dur
> Validé par : JCH (paramètres validés, ajustables en essais)
> Rédacteur : [[Dobby]] 🦉

## Principe de conception — Seuils configurables

**Tous les seuils** (vitesses, délais, températures, pourcentages) sont implémentés comme des `input_number` helpers dans Home Assistant — jamais codés en dur dans les automatisations YAML.

Cela permet de :
- Ajuster les valeurs en conditions réelles sans éditer de fichier
- Les modifier depuis le tableau de bord Lovelace pendant les essais
- Retrouver la valeur par défaut si un réglage ne convient pas
- Logger les changements de seuil pour analyse

### Convention de nommage HA

```
input_number.vanlife_<scenario>_<parametre>
```

Exemples : `input_number.vanlife_porte_roulage_seuil_vitesse`, `input_number.vanlife_hayon_delai`, `input_number.vanlife_frigo_timer`

### Interface de réglage

Un panneau "Réglages Vanlife" dans le dashboard Lovelace regroupera tous les `input_number` organisés par famille, avec slider + valeur actuelle.

---

## Structure

Pour chaque famille de capteurs, la matrice suivante :

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Capteurs impliqués dans le scénario |
| **Donnée brute** | Signal/entité HA utilisée |
| **Algorithme / Règle** | Logique de décision (SI/ALORS/ET/OU) |
| **Action** | Sortie : notification, relais, commande |
| **Seuils** | Valeurs de déclenchement configurables |
| **Filtres** | Anti faux-positifs |
| **Priorité** | Phase projet (P1-P4) |
| **Implémentation HA** | Note technique |

---

## 1. Famille OUVERTURE

### Capteurs concernés

| # | Emplacement | Technologie | Phase |
|---|-------------|-------------|-------|
| 1 | Porte avant conducteur | Aqara MCCGQ11LM (Zigbee) | P1 |
| 2 | Porte avant passager | Aqara MCCGQ11LM (Zigbee) | P1 |
| 3 | Porte coulissante gauche | Aqara MCCGQ11LM (Zigbee) | P1 |
| 4 | Porte coulissante droite | Aqara MCCGQ11LM (Zigbee) | P1 |
| 5 | Hayon arrière | Aqara MCCGQ11LM (Zigbee) | P1 |
| 6 | Toit relevable | Aqara MCCGQ11LM (Zigbee) | P1 |
| 7 | Porte réfrigérateur | Aqara MCCGQ11LM (Zigbee) | P1 |
| 8 | Tiroirs (optionnel) | Aqara MCCGQ11LM (Zigbee) | P2 |

---

### 1.1 — Porte oubliée en roulage

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Toutes portes + `binary_sensor.engine_running` (D+ DS300) |
| **Donnée brute** | `binary_sensor.door_X` = ON + `binary_sensor.engine_running` = ON |
| **Algorithme** | SI (moteur tournant) ET (porte ouverte > 15s) → ALERTE |
| **Action** | Notification push iPhone + warning dashboard Lovelace |
| **Seuils** | 15s (portes avant), 30s (hayon — tolérance manœuvre lente) |
| **Filtre** | Ignorer si van à l'arrêt (vitesse = 0) même moteur allumé |
| **Priorité** | **P1** — sécurité critique |
| **HA** | Automatisation condition `for:` 00:00:15 + `state_attr` vitesse |

---

### 1.2 — Hayon resté ouvert après bivouac

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Hayon + PIR extérieur (P2b) + horaire |
| **Donnée brute** | `binary_sensor.hayon` = ON prolongé + van à l'arrêt |
| **Algorithme** | SI (hayon ouvert > 10 min) ET (van à l'arrêt) ET (nuit) → NOTIFICATION |
| **Action** | Notification push : "Hayon encore ouvert" |
| **Seuils** | 10 min (tolérance charge/décharge), renforcé à 30 min |
| **Exclusion** | Désactiver si PIR détecte présence active autour du hayon |
| **Priorité** | **P1** — confort & sécurité |
| **HA** | Timer redémarrable sur état ON + condition sun.sun |

---

### 1.3 — Frigo ouvert prolongé

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Aqara frigo (ouverture) + SNZB-02D frigo (température) |
| **Donnée brute** | `binary_sensor.fridge` = ON > 2 min |
| **Algorithme** | SI (porte frigo ouverte > 2 min) → ALERTE |
| **Action** | Notification "Porte frigo ouverte" |
| **Seuils** | 2 min usage normal ; si T° frigo ne descend pas après fermeture → alerte maintenance |
| **Priorité** | **P1** — conservation aliments |
| **HA** | `for: 00:02:00` sur porte frigo → notification + log |

---

### 1.4 — Verrouillage auto tiroirs en roulage

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Inclinomètre + GPS vitesse |
| **Donnée brute** | `sensor.speed` > 10 km/h |
| **Algorithme** | SI (vitesse > 10 km/h) → VERROUILLER électro-aimants tiroirs — SI (vitesse < 3 km/h pendant 30s) → DÉVERROUILLER |
| **Action** | Commande relais électro-aimant |
| **Sécurité** | Hystérésis : verrouillage à 10 km/h, déverrouillage à 3 km/h |
| **Priorité** | **P2** (nécessite relais + inclinomètre) |
| **HA** | Automatisation `numeric_state` vitesse → `switch.lock_drawers` |

---

### 1.5 — Détection intrusion (nuit)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Toutes portes + PIR extérieur (P2b) + dB |
| **Donnée brute** | Séquence d'ouverture + pic sonore |
| **Algorithme** | SI (mode "campement nuit" actif) ET (entre 23h-6h) ET (ouverture porte avant OU coulissante) → ALERTE |
| **Règles anti-faux-positifs** | Hayon seul → normal (toilettes) ; hayon + coulissante → charge → alerte légère ; porte avant SEULE sans moteur → ⚠️ intrusion ; porte avant + moteur → départ → pas d'alerte |
| **Action** | Notification push prioritaire + allumage spot extérieur |
| **Priorité** | **P2** (PIR extérieur + capteurs) |
| **HA** | Automatisation avec condition horaire + mode binaire "campement" |

---

## 2. Famille PARAMÈTRES PHYSIQUES

### Capteurs concernés

| # | Capteur | Technologie | Phase |
|---|---------|-------------|-------|
| 1 | Température habitacle | Sonoff SNZB-02D (Zigbee) | P1 |
| 2 | Humidité habitacle | Sonoff SNZB-02D (Zigbee) | P1 |
| 3 | Niveau sonore dB | ESP32 + INMP441 (I2S → ESPHome) | P2 |
| 4 | Inclinaison (roulis/tangage) | ESP32 + MPU6050 (I2C → ESPHome) | P2 |
| 5 | Température frigo | Sonoff SNZB-02D (Zigbee) | P1 |
| 6 | Température eau grise | DS18B20 (1-Wire → RPi) | P3 |

---

### 2.1 — Anticipation condensation

| Champ | Valeur |
|-------|--------|
| **Capteurs** | T° habitacle + humidité + T° extérieure |
| **Donnée brute** | `sensor.temp_cellule`, `sensor.humidity`, `sensor.temp_exterieure` |
| **Algorithme** | Calcul du point de rosée : Td = T - ((100 - HR)/5) — SI (T paroi ≈ T extérieure < Td) → RISQUE CONDENSATION |
| **Action** | Si risque détecté : suggestion d'ouverture toit relevable en mode auvent OU activation ventilateur extraction |
| **Seuils** | Delta T° paroi - Td < 2°C → alerte "condensation probable" |
| **Priorité** | **P2** (nécessite station météo extérieure P3) |
| **Note** | Classique en van : condensation sur les hublats et parois non isolées |

---

### 2.2 — Surchauffe habitacle (alerte départ)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | T° habitacle + présence van (GPS arrêt) |
| **Donnée brute** | `sensor.temp_cellule` > seuil |
| **Algorithme** | SI (T° cell > 40°C) ET (van à l'arrêt, moteur éteint) → ALERTE |
| **Action** | Notification : "Surchauffe habitacle — retour possible ?" + allumage auto ventilateur toit si installé |
| **Seuils** | 40°C avertissement, 50°C critique |
| **Cross-check** | Si T° extérieure < 30°C → vérifier toit fermé (capteur toit) → alerte "toit fermé ?" |
| **Priorité** | **P1** (température seule) |
| **HA** | Automatisation seuil haut + condition vitesse = 0 |

---

### 2.3 — Confort bivouac (log dB)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | dB + T° extérieure + humidité |
| **Donnée brute** | `sensor.sound_level_avg` (moyenne glissante 5 min) |
| **Algorithme** | Enregistrement profile sonore du spot : dB min/moyen/max + qualitatif (calme / modéré / bruyant) |
| **Action** | Dashboard : historique dB par nuit, tag "spot calme" / "spot bruyant" |
| **Seuils** | < 35 dB = calme, 35-50 = modéré, > 50 = bruyant |
| **Priorité** | **P2** (nécessite capteur dB) |

---

### 2.4 — Alarme intrusion sonore

| Champ | Valeur |
|-------|--------|
| **Capteurs** | dB (pic instantané) + PIR extérieur + porte |
| **Donnée brute** | Pic dB > seuil + contexte nuit |
| **Algorithme** | SI (dB > 85 en moins de 100ms) ET (mode nuit) → PIC ANORMAL |
| **Action** | Log événement + notification si combiné avec ouverture porte |
| **Filtre** | Ignorer si volume musique/radio allumé (cross-check entité media) |
| **Priorité** | **P3** (affinage après déploiement dB) |

---

### 2.5 — Niveau gel batterie / eau

| Champ | Valeur |
|-------|--------|
| **Capteurs** | T° habitacle + T° extérieure |
| **Donnée brute** | Températures hivernales |
| **Algorithme** | SI (T° ext < 0°C) → ALERTE GEL : vidanger eau si van non occupé |
| **Seuils** | -2°C → alerte "risque gel batterie LiFePO4 (charge)" ; -5°C → alerte "vidanger eau propre" |
| **Priorité** | **P2** (station météo extérieure) |
| **HA** | Automatisation saisonnière + condition T° < 0 |

---

### 2.6 — Inclinaison : angle sécurité repérage terrain

| Champ | Valeur |
|-------|--------|
| **Capteurs** | MPU6050 (ESP32) |
| **Donnée brute** | `sensor.roll`, `sensor.pitch` (degrés) |
| **Algorithme** | SI (van à l'arrêt) → affichage angle X/Y en temps réel sur dashboard — SI (angle > 3°) → suggestion "recaler le van" |
| **Seuils** | 0-3° = bon, 3-6° = limite (confort lit), > 6° = mauvais |
| **Mémoire** | Enregistrer l'angle moyen à chaque arrêt pour référence future (spot connu) |
| **Priorité** | **P2** |

---

## 3. Famille ÉNERGIE

### Capteurs concernés

| # | Capteur | Technologie | Phase |
|---|---------|-------------|-------|
| 1 | Batterie cellule LiFePO4 (SOC/courant) | Victron SmartShunt 500A (VE.Direct → USB) | P3 |
| 2 | Tension batterie cellule (V) | DS300 Tap — `sensor.leisure_battery_voltage` | P1 |
| 3 | Tension batterie véhicule (V) | DS300 Tap — `sensor.starter_battery_voltage` | P1 |
| 4 | Panneau solaire | Victron SmartSolar MPPT 100/20 (VE.Direct → USB) | P3 |
| 5 | Signal D+ (moteur tournant) | DS300 Tap — `binary_sensor.engine_running` | P1 |
| 6 | Présence 230V secteur | DS300 Tap — `binary_sensor.shore_power` | P1 |
| 7 | Conso totale cellule | SmartShunt | P3 |

---

### 3.1 — Autonomie prédictive

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Batterie cellule (SOC) + consommation + production solaire |
| **Donnée brute** | `sensor.battery_soc`, `sensor.power_consumed`, `sensor.solar_production` |
| **Algorithme** | Autonomie restante (h) = SOC × capacité_nominale / (conso_moyenne_24h - production_moyenne_24h) |
| **Action** | Dashboard : autonomie en heures + jours selon météo prévue |
| **Seuils** | < 24h → alerte "recharge nécessaire" ; < 12h → alerte critique + shutdown Pi programmé |
| **Priorité** | **P3** |

---

### 3.2 — Shutdown automatique batterie faible

| Champ | Valeur |
|-------|--------|
| **Capteurs** | SmartShunt SOC |
| **Donnée brute** | `sensor.battery_soc` < seuil |
| **Algorithme** | SI (SOC < 20%) ET (pas de recharge solaire détectée depuis 30 min) → SHUTDOWN RPi propre |
| **Action** | Notification "Mise en veille — batterie faible" → shutdown HA OS |
| **Seuil** | 20% SOC avec hystérésis 5% (réveil si SOC > 25%) |
| **Priorité** | **P3** |

---

### 3.3 — Niveau gaz (bonbonne propane/butane)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Mopeka Pro Check (BLE → ESP32) ou load cell |
| **Donnée brute** | `sensor.propane_level` (% restant), `sensor.propane_volume` (litres estimés) |
| **Algorithme** | SI (niveau < 20%) → ALERTE "Gaz faible — prévoir remplissage" — SI (niveau < 10%) → ALERTE CRITIQUE "Gaz presque vide" |
| **Action** | Notification push + dashboard widget |
| **Seuils** | 20% avertissement, 10% critique |
| **Usage estimé** | Webasto chauffage ~0.3 kg/nuit (saison froide). Une bouteille 13 kg → ~40 nuits. |
| **Autonomie restante** | Estimation : (niveau_actuel / conso_moyenne_24h) en jours, affiché sur dashboard |
| **Cross-check** | SI (hiver) ET (niveau < 30%) → suggestion "Prévoir bouteille de rechange" |
| **Priorité** | **P3** |

---

### 3.4 — Niveaux d'eau (propre + grise)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Sondes résistives cuves CBE → DS300 Tap — `sensor.fresh_water_level`, `sensor.grey_water_level` |
| **Donnée brute** | `sensor.fresh_water_level` (%), `sensor.grey_water_level` (%) |
| **Algorithme** | SI (eau propre < 20%) → NOTIFICATION "Eau propre faible — faire le plein" — SI (eau grise > 80%) → NOTIFICATION "Eaux grises pleines — vidanger" |
| **Action** | Notification push + dashboard widget avec volume restant |
| **Seuils** | Eau propre : < 20% avertissement, < 10% critique. Eau grise : > 80% avertissement, > 90% critique |
| **Cross-check** | SI (eau grise > 50%) ET (mode nuit) → ne pas ajouter d'alerte sonore (ne pas réveiller) |
| **Log** | Consommation moyenne d'eau par jour (L/jour) → prévoir remplissage |
| **Priorité** | **P3** |

---

## 4. Famille STATION MÉTÉO EXTERNE

### Capteurs

| # | Mesure | Technologie | Phase |
|---|--------|-------------|-------|
| 1 | T° extérieure | BME280 (ESP32 I2C, T°+HR+pression) | P3 |
| 2 | Vent | Anémomètre cupules (ESP32) | P3 |
| 3 | Pression atmosphérique | BME280 (I2C) | P3 |
| 4 | Pluie | Capteur pluie résistif | P3 |
| 5 | Luminosité | LDR / BH1750 | P3 |

---

### 4.1 — Décision toit relevable

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Vent + pluie + luminosité |
| **Algorithme** | SI (vent < 30 km/h) ET (pas de pluie) → toit relevable possible |
| **Action** | Suggestion dashboard : "Conditions favorables pour le toit" ou "Vent fort : éviter toit relevé" |
| **Seuils** | Vent < 20 km/h = idéal, 20-30 = limite (attention auvents), > 30 = déconseillé |
| **Priorité** | **P3** — informationnel |

---

### 4.2 — Alerte intempérie

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Pluie + vent + pression (tendance) |
| **Algorithme** | SI (détection pluie) OU (pression chute > 3 hPa/h) → si toit relevé ou auvents déployés, alerter |
| **Action** | Notification "Intempérie imminente — rentrer les stores" |
| **Seuils** | Chute pression > 3 hPa/h + pluie → prioritaire |
| **Priorité** | **P3** |

---

## 5. Famille ÉQUIPEMENTS

### Capteurs

| # | Équipement | Technologie | Phase |
|---|------------|-------------|-------|
| 1 | Suspension pneumatique | Capteur pression air | P4 |
| 2 | Pression pneus | TPMS externe Bluetooth | P4 |
| 3 | Batterie véhicule | Mesure tension (ESP32) | P3 |
| 4 | Ventilateurs toit | Commande via relais | P2 |
| 5 | GPS position | u-blox 7 USB | P2 |

---

### 5.1 — GPS : log spots et mémorisation

| Champ | Valeur |
|-------|--------|
| **Capteurs** | GPS u-blox |
| **Algorithme** | SI (vitesse < 1 km/h pendant > 5 min) → marquer "spot bivouac potentiel" avec timestamp + T° + humidité + angle + dB |
| **Action** | Enregistrement dans HA (base de données historique) + tag "favori" possible via dashboard |
| **Fonction supplémentaire** | Export GPX des trajets pour visualisation |
| **Priorité** | **P2** |

---

### 5.2 — Alerte pression pneus (TPMS)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | TPMS Bluetooth |
| **Algorithme** | SI (pression pneu < seuil) → alerte avant départ |
| **Seuils** | Pression < 80% recommandée → avertissement ; < 60% → critique |
| **Priorité** | **P4** — capteur externe à acheter |

---

## 6. Famille DS300 TAP — Intégration tableau électrique

> **Spec :** [`ds300-tap/SPEC-DS300-TAP.md`](ds300-tap/SPEC-DS300-TAP.md)  
> **Config ESPHome :** [`ds300-tap/esphome-ds300.yaml`](ds300-tap/esphome-ds300.yaml)

### Capteurs exposés par le DS300 Tap

| # | Entité HA | Signal DS300 | Phase |
|---|-----------|-------------|-------|
| 1 | `sensor.leisure_battery_voltage` | Pin 15 — B2 cellule | P1 |
| 2 | `sensor.starter_battery_voltage` | Pin 12 — B1 porteur | P1 |
| 3 | `sensor.fresh_water_level` | Pins 2-7-8 — Sonde eau propre | P1 |
| 4 | `sensor.grey_water_level` | Pin 9 — Sonde eau grise | P1 |
| 5 | `binary_sensor.engine_running` | Pin 5 — D+ alternateur | P1 |
| 6 | `binary_sensor.shore_power` | Pin 10 — Présence 230V | P1 |
| 7 | `binary_sensor.water_pump` | Pin 6 — Relais pompe | P1 |
| 8 | `binary_sensor.fridge_relay` | Pin 4 — Relais frigo | P1 |
| 9 | `binary_sensor.main_relay` | Pin 14 — Relais principal | P1 |

### Impact sur les scénarios

| Scénario | Avant | Après DS300 Tap |
|----------|-------|-----------------|
| 1.1 Porte oubliée roulage | GPS vitesse | `binary_sensor.engine_running` (D+) — plus fiable, pas besoin de GPS |
| 3.1 Autonomie prédictive | SmartShunt seul | SmartShunt (SOC) + `sensor.leisure_battery_voltage` (cross-check) |
| 3.2 Shutdown batterie faible | SmartShunt SOC | Ajout `binary_sensor.shore_power` — ne pas shutdown si branché |
| 3.3 Niveau gaz | Mopeka seul | Inchangé |
| 3.4 Niveaux d'eau | JSN-SR04T / TL-136 | `sensor.fresh_water_level` + `sensor.grey_water_level` — sondes CBE d'origine |
| 5.1 GPS spots | GPS u-blox | Complété par `binary_sensor.engine_running` pour détecter arrêt moteur |

### Économies

- **Capteurs supprimés :** JSN-SR04T ×2 (jauges eau van → DS300 Tap)
- **Capteurs gratuits :** D+, 230V shoreline, état relais, tensions B1/B2 — aucune BOM additionnelle
- **Coût du Tap :** ~8€ (connecteurs + optocoupleurs + résistances)
- **Économie nette :** ~10€ sur le panier Amazon

---

## 7. Famille CAN BUS — Données véhicule Ford Transit Custom

> **Spec :** [`specs/SPEC-CAN-BUS.md`](specs/SPEC-CAN-BUS.md)  
> **Hardware :** WiCAN Pro (ESP32-S3 + STN OBD interpreter, ~82€)  
> **Source PIDs :** [WiCAN-Ford-Transit](https://github.com/anthonysecco/WiCAN-Ford-Transit)

### Capteurs CAN exposés dans HA

| # | Entité HA | PID | Source | Mode |
|---|-----------|-----|--------|------|
| 1 | `sensor.vehicle_speed` | 0x0D | PCM HS-CAN | Roulage |
| 2 | `sensor.engine_rpm` | 0x0C | PCM HS-CAN | Roulage |
| 3 | `sensor.coolant_temp` | 0x05 | PCM HS-CAN | Roulage |
| 4 | `sensor.fuel_level` | 0x2F | PCM HS-CAN | Roulage |
| 5 | `sensor.fuel_rate` | 0x5E | PCM HS-CAN | Roulage |
| 6 | `sensor.ambient_air_temp` | 0x46 | PCM HS-CAN | Roulage |
| 7 | `sensor.manifold_pressure` | 0x0B | PCM HS-CAN | Roulage |
| 8 | `sensor.dtc_count` | Mode 03 | PCM | Tout moment |
| 9 | `binary_sensor.door_driver` | 0x225B1D/0 | BCM MS-CAN | Periodic wake |
| 10 | `binary_sensor.door_passenger` | 0x225B1D/1 | BCM MS-CAN | Periodic wake |
| 11 | `binary_sensor.door_left_rear` | 0x225B1D/3 | BCM MS-CAN | Periodic wake |
| 12 | `binary_sensor.door_right_rear` | 0x225B1D/4 | BCM MS-CAN | Periodic wake |
| 13 | `binary_sensor.door_luggage` | 0x225B1D/5 | BCM MS-CAN | Periodic wake |
| 14 | `sensor.tpms_*` (×6) | 0x222813-18 | BCM MS-CAN | Periodic wake |
| 15 | `sensor.battery_soc` | 0x224028 | BCM MS-CAN | Periodic wake |

> **Note :** Les données BCM (portes, pneus, batterie) sont disponibles en roulage (temps réel) et en stationnement (periodic wake ~5 min). Les Aqara Zigbee restent la source primaire pour les portes en camping (latence <1s).

---

### 7.1 — Jauge carburant + autonomie restante

| Champ | Valeur |
|-------|--------|
| **Capteurs** | `sensor.fuel_level` + `sensor.fuel_rate` + GPS odomètre |
| **Donnée brute** | Niveau réservoir (%) + débit instantané (L/h) |
| **Algorithme** | Conso moyenne 100km = moyenne mobile de fuel_rate / speed × 100 — Autonomie restante = fuel_level × capacité_réservoir / conso_moyenne |
| **Action** | Dashboard : jauge (%) + "Range: X km". SI (fuel < 25%) → notification "Carburant bas — autonomie ~X km". SI (fuel < 10%) → ALERTE CRITIQUE |
| **Seuils** | 25% avertissement, 10% critique |
| **Priorité** | **P1** |

---

### 7.2 — Conso réelle par trajet (L/100km)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | `sensor.fuel_rate` + `sensor.vehicle_speed` + GPS distance |
| **Donnée brute** | Débit carburant (L/h) + vitesse (km/h) |
| **Algorithme** | `sensor.fuel_consumption_l100` = fuel_rate / speed × 100 — Log par trajet détecté (moteur ON → OFF) |
| **Action** | Dashboard : "Ce trajet : X.X L/100km — Coût estimé : Y€" (prix diesel saisi manuellement par pays) |
| **Seuils** | Alert si conso anormale (> 12 L/100km en croisière) → possible problème mécanique |
| **Priorité** | **P1** |

---

### 7.3 — Diagnostic moteur live (DTC)

| Champ | Valeur |
|-------|--------|
| **Capteurs** | Mode 03 + code description (base JSON ou API) |
| **Donnée brute** | `sensor.dtc_count` + `sensor.dtc_codes` |
| **Algorithme** | SI (DTC count > 0) → NOTIFICATION "Code défaut moteur : PXXXX — [description]" |
| **Action** | Notification push + dashboard widget avec liste des codes actifs + lien recherche |
| **Filtre** | Ignorer codes non critiques (P04xx évap mineur) si configuré |
| **Priorité** | **P1** — sécurité roadtrip |

---

### 7.4 — Surveillance turbo

| Champ | Valeur |
|-------|--------|
| **Capteurs** | `sensor.manifold_pressure` + `sensor.engine_rpm` |
| **Donnée brute** | Pression admission (kPa) + régime (tr/min) |
| **Algorithme** | SI (pression admission < seuil_attendu @ RPM donné) → ALERTE "Turbo sous-performant — possible fuite admission/durite" |
| **Seuils** | À calibrer sur véhicule : pression attendue ~180-220 kPa @ 2000 RPM en charge. Écart > 30% → alerte. |
| **Cross-check** | Si conso anormale (7.2) simultanée → confirmation panne |
| **Priorité** | **P2** |

---

### 7.5 — Préchauffage Webasto intelligent

| Champ | Valeur |
|-------|--------|
| **Capteurs** | `sensor.coolant_temp` + `binary_sensor.van_occupied` (mode camping) |
| **Donnée brute** | T° liquide refroidissement + mode occupation |
| **Algorithme** | SI (coolant < 5°C) ET (van occupé) ET (mode "départ prévu" activé) → SUGGESTION "Lancer Webasto — T° moteur : X°C" |
| **Action** | Notification push avec bouton "Démarrer Webasto" (intégration future si interface disponible) |
| **Seuils** | < 5°C → préchauffage recommandé. < -10°C → critique (diesel risque gélification) |
| **Priorité** | **P2** |

---

### 7.6 — Alerte batterie porteur faible

| Champ | Valeur |
|-------|--------|
| **Capteurs** | `sensor.battery_soc` + `sensor.battery_voltage_bcm` + `sensor.battery_current` |
| **Donnée brute** | SOC (%), tension (V), courant (A) |
| **Algorithme** | SI (SOC < 50%) ET (moteur OFF > 24h) → ALERTE "Batterie porteur faible — risque de non-démarrage" |
| **Action** | Notification push + dashboard widget. SI (SOC < 30%) → ALERTE CRITIQUE "Démarrer le moteur maintenant" |
| **Seuils** | SOC < 50% avertissement, < 30% critique. Cross-check avec tension < 11.8V. |
| **Priorité** | **P2** |

---

### Impact CAN bus sur les scénarios existants

| Scénario | Amélioration |
|----------|-------------|
| 1.1 Porte oubliée roulage | CAN speed + RPM remplacent attente GPS. Triple confirmation (D+ + speed + Aqara). |
| 1.2 Hayon resté ouvert | CAN hayon en backup de l'Aqara (0-5 min délai, suffisant pour ce scénario) |
| 1.4 Verrouillage tiroirs | CAN vitesse instantanée remplace GPS vitesse (plus rapide, pas de lag) |
| 1.5 Détection intrusion | CAN capot + portes en backup des Aqaras. Porte AV + capot = scénario vol. |
| 2.2 Surchauffe habitacle | Cross-check T° liquide refroidissement → distingue surchauffe moteur vs solaire |
| 5.1 GPS spots | Enrichi : fuel_level + coolant_temp + RPM au spot → profil complet |
| 5.2 Alerte pression pneus | Supprimé — remplacé par BCM TPMS ×6 (gratuit) |

---

## Priorisation & roadmap

| Priorité | Scénarios | Phase |
|----------|-----------|-------|
| 🔴 Critique | Porte oubliée roulage (1.1), Surchauffe (2.2), Frigo (1.3), **Jauge carburant (7.1)**, **Conso trajet (7.2)**, **DTC moteur (7.3)** | P1 |
| 🟡 Important | Hayon ouvert (1.2), Verrouillage tiroirs (1.4), Intrusion (1.5), Condensation (2.1), Angle sécurité (2.6), **Surveillance turbo (7.4)**, **Webasto (7.5)**, **Batterie porteur (7.6)** | P2 |
| 🟢 Confort | Autonomie (3.1), Shutdown (3.2), Toit relevable (4.1), GPS spots (5.1), Confort dB (2.3) | P3 |
| 🔵 Évolution | Alarme sonore (2.4), Alerte gel (2.5), Intempérie (4.2) | P4 |

---

## Références

- [[Liste IOT pour van]] — Liste brute capteurs (Inbox)
- [[projet-vanlife-iot]] — Document projet v1.0
- [[stylevan-equinox4-cahier-technique-iot]] — Cahier technique
- [[projet-vanlife-iot-foundation]] — Document fondateur
- [[rpi-vanlife-guide-complet]] — Guide installation RPi + HA
- [`ds300-tap/SPEC-DS300-TAP.md`](ds300-tap/SPEC-DS300-TAP.md) — Spec interface CBE DS300
- [WomoNET Wiki — CBE DS Powerblock Series](https://wiki.womonet.io/protocols/cbe_ds_series/) — Pinout source

---

*Document v1.1 — [[Dobby]] 🦉, 2026-06-07, mis à jour 2026-07-09 (ajout CAN bus). Prochaine révision : après validation CAN sur véhicule réel.*
