# Scénarios & Algorithmes — Vanlife IOT

> Document de conception des automatismes intelligents du Stylevan Equinox 4
> Version : v1.0 VALIDATED — 2026-06-07
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
| **Capteurs** | Toutes portes + GPS vitesse |
| **Donnée brute** | `binary_sensor.door_X` = ON + `sensor.speed` > 0 |
| **Algorithme** | SI (vitesse > 5 km/h) ET (porte ouverte > 15s) → ALERTE |
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
| **Capteurs** | Porte frigo + température frigo |
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
| 1 | Batterie cellule LiFePO4 | Victron SmartShunt 500A (VE.Direct → USB) | P3 |
| 2 | Batterie véhicule | SmartShunt ou mesure tension | P3 |
| 3 | Panneau solaire | Victron SmartSolar MPPT 100/20 (VE.Direct → USB) | P3 |
| 4 | Conso totale cellule | SmartShunt | P3 |

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
| **Capteurs** | 2× JSN-SR04T ultrason (ESP32) |
| **Donnée brute** | `sensor.eau_propre_niveau` (% ou litres), `sensor.eau_grise_niveau` (% ou litres) |
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
| 1 | T° extérieure | Sonoff SNZB-02D extérieur | P3 |
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

## Priorisation & roadmap

| Priorité | Scénarios | Phase |
|----------|-----------|-------|
| 🔴 Critique | Porte oubliée roulage (1.1), Surchauffe (2.2), Frigo (1.3) | P1 |
| 🟡 Important | Hayon ouvert (1.2), Verrouillage tiroirs (1.4), Intrusion (1.5), Condensation (2.1), Angle sécurité (2.6) | P2 |
| 🟢 Confort | Autonomie (3.1), Shutdown (3.2), Toit relevable (4.1), GPS spots (5.1), Confort dB (2.3) | P3 |
| 🔵 Évolution | Alarme sonore (2.4), TPMS (5.2), Alerte gel (2.5), Intempérie (4.2) | P4 |

---

## Références

- [[Liste IOT pour van]] — Liste brute capteurs (Inbox)
- [[projet-vanlife-iot]] — Document projet v1.0
- [[stylevan-equinox4-cahier-technique-iot]] — Cahier technique
- [[projet-vanlife-iot-foundation]] — Document fondateur
- [[rpi-vanlife-guide-complet]] — Guide installation RPi + HA

---

*Document v0.1 DRAFT — [[Dobby]] 🦉, 2026-06-07. Prochaine révision : après validation des scénarios par JCH.*
