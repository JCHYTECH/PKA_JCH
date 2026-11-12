# Guide d'Installation et de Configuration Pas-à-Pas : Home Assistant Vanlife « Lupo »

**Véhicule :** Van Lupo 🐺 — Westfalia Kelsey 2026 (Porteur Ford Transit Custom Tourneo V710, 2.0 EcoBlue 170 ch, 4×4, BVA8)
**Rédacteur :** Dobby 🦉
**Date du rapport initial :** 4 octobre 2026 · **Recadrage documentaire :** 5 novembre 2026
**Échéance installation physique :** 15 décembre 2026
**Version HAOS :** HAOS 18.3 (auto-update HAOS/Core désactivé ; Supervisor + modules en automatique depuis le 5 novembre 2026)

---

## 1. Architecture Matérielle & Infrastructure Embarquée

### 1.1 Unité Centrale (Raspberry Pi 5)

* **Calculateur :** Raspberry Pi 5 (4 Go RAM).
* **Support de stockage :** Carte MicroSD **Samsung PRO Endurance 256 Go** (Note : le stockage NVMe a été retiré suite au problème de boot identifié le 01/10).
* **Alimentation & UPS :**
  * Alimentation principale : Câble USB-C direct 5V/5A.
  * Maintien d'alimentation (UPS) : Carte **Geekworm X1205** équipée de 2 accus 18650 (assure la coupure propre en cas de perte secteur/batterie cellule).
* **Refroidissement & Boîtier :** Boîtier métallique **Geekworm X1201-C1** articulé autour du refroidisseur actif officiel RPi 5 et d'un ventilateur **Noctua NF-A4x10** pour un fonctionnement silencieux.
* **Prochaines étapes matérielles :** Montage sur silentblocs anti-vibrations et application d'un vernis de tropicalisation (*conformal coating*) sur la carte.

### 1.2 Protocoles, Bus & Interfaces Capteurs

1. **Réseau Zigbee :**
   * **Coordinateur :** Sonoff ZBDongle-E (firmware EmberZNet, canal Zigbee 15).
   * **Gestionnaire :** Zigbee2MQTT v5 connecté au broker Mosquitto MQTT (`:1883`).
   * **Capteurs d'ouverture (×8) — cible d'équipement, non installée à ce stade :** Aqara MCCGQ11LM (`binary_sensor.door_*`) envisagés sur portes cabine et cellule, hayon, toit relevable, frigo et tiroirs. La liste d'achat P1 détaillée et son périmètre restent à revalider.
2. **Interface Véhicule OBD-II / CAN Bus :**
   * **Module :** **WiCAN Pro** (lecture simultanée HS-CAN et MS-CAN).
   * **État :** module physiquement installé ; intégration HA/RUT240 et compatibilité avec *Exosfer OBD Protect* à valider.
   * **Entités visées (17+), remontée non confirmée :** vitesse (`sensor.speed`), régime moteur (`sensor.rpm`), niveau carburant (`sensor.fuel_level`), température moteur (`sensor.coolant_temp`), codes défaut (`sensor.dtc` / `binary_sensor.dtc_active`), pression turbo (`sensor.boost_pressure`) et TPMS BCM. Les automatisations ci-dessous sont donc des configurations cibles à tester, pas des fonctions validées.
3. **Interface Électrique Cellule — cible « DS300 Tap » (CBE DS300), entités visées :**
   * **Avant flash :** corriger le conflit GPIO8 entre I²C SDA et relais dans `esphome-ds300.yaml`.
   * **Tension batterie cellule :** `sensor.leisure_battery_voltage`
   * **Tension batterie porteur :** `sensor.starter_battery_voltage`
   * **Moteur tournant (Signal D+) :** `binary_sensor.engine_running`
   * **Présence 230 V (Secteur/Shore Power) :** `binary_sensor.shore_power`
   * **Niveaux d'eaux :** Eau propre (`sensor.fresh_water_level`), Eaux grises (`sensor.grey_water_level`).
4. **Capteurs Auxiliaires & Énergie (Phases ultérieures) :**
   * Victron SmartShunt 500A + MPPT 100/20 (Liaison VE.Direct → USB).
   * Assiette déléguée à l'iPhone (MPU6050 écarté de la cible actuelle), station BME280, Mopeka Pro Check BLE en P3, GPS u-blox 7 USB et ESP32-CAM en phases ultérieures.

### 1.3 Architecture Réseau Distribuée

* **Topologie :** 3 instances Home Assistant autonomes (Mac M5 Belgique, RPi 5 Esneux, RPi 5 Van Lupo).
* **Accès distant :** Maillage sécurisé **Tailscale** permettant la supervision et la notification push sur iPhone, même en itinérance sans IP fixe.

---

## 2. Pile Logicielle & Configuration Initiale

### 2.1 Services & Add-ons Requis

1. **Mosquitto Broker :** Service MQTT principal sur le port 1883.
2. **Zigbee2MQTT :** Configuration du contrôleur Ember sur le canal 15 (`adapter: ember`).
3. **Tailscale Add-on :** Authentification et raccordement au réseau privé vanlife.
4. **go2rtc :** Traitement des flux vidéo légers pour l'intégration des caméras ESP32.

### 2.2 Standardisation des Noms d'Entités

Pour garantir la maintenabilité, chaque capteur doit suivre la convention de nommage ci-dessous :

* `binary_sensor.door_front_left` / `binary_sensor.door_front_right`
* `binary_sensor.door_sliding_left` / `binary_sensor.door_sliding_right`
* `binary_sensor.door_tailgate` (Hayon)
* `binary_sensor.door_popup_roof` (Toit relevable)
* `binary_sensor.door_frigo` (Frigo)
* `binary_sensor.door_drawers` (Tiroirs)

---

## 3. Méthodologie des Helpers `input_number` (Variables Dynamiques)

### 3.1 Règle Absolue

> **Aucune valeur de seuil, de délai ou de consigne ne doit être inscrite en dur dans les fichiers YAML d'automatisation.**
> Toutes les valeurs de consigne doivent pointer vers des helpers `input_number.vanlife_*`. Cela permet d'ajuster le comportement du van en direct depuis le tableau de bord Lovelace sans redémarrer Home Assistant.

### 3.2 Tableau des Helpers de Réglage

| Nom du Helper                                        | Libellé / Usage               | Valeur par défaut |  Unité  | Min / Max |
| :--------------------------------------------------- | :----------------------------- | :----------------: | :------: | :-------: |
| `input_number.vanlife_porte_roulage_seuil_vitesse` | Vitesse min. pour alerte porte |       `5`       |   km/h   |  0 / 30  |
| `input_number.vanlife_porte_roulage_delai`         | Tempo alerte porte oubliée    |       `15`       | secondes |  5 / 60  |
| `input_number.vanlife_hayon_delai`                 | Tempo alerte hayon             |       `30`       | secondes | 10 / 120 |
| `input_number.vanlife_frigo_timer`                 | Delai max. frigo ouvert        |       `60`       | secondes | 15 / 300 |
| `input_number.vanlife_surchauffe_seuil_temp`       | Température alerte surchauffe |       `38`       |   °C   |  25 / 50  |
| `input_number.vanlife_carburant_seuil_min`         | Seuil bas niveau carburant     |       `15`       |    %    |  5 / 30  |
| `input_number.vanlife_conso_seuil_anomalie`        | Seuil alerte surconsommation   |      `12.0`      | L/100km |  6 / 20  |

---

## 4. Déploiement des 6 Automatisations Critiques (Priorité P1)

### Scénario 1.1 — Porte ou Panneau Oublié en Roulage

* **Objectif :** Détecter si une porte, le frigo, le toit ou le hayon est ouvert alors que le véhicule se met à rouler.
* **Triggers :** Changement d'état de `binary_sensor.door_*` à `on` OU démarrage moteur (`binary_sensor.engine_running` = `on`) OU `sensor.speed` > 5 km/h.
* **Conditions :** Vehicle en mouvement (`sensor.speed` > `input_number.vanlife_porte_roulage_seuil_vitesse` OU `binary_sensor.engine_running` = `on`).
* **YAML d'automatisation :**

```yaml
alias: "Vanlife - P1 - Porte oubliée en roulage"
description: "Déclenche une alerte critique si un ouvrant est ouvert pendant le roulage"
trigger:
  - platform: numeric_state
    entity_id: sensor.speed
    above: input_number.vanlife_porte_roulage_seuil_vitesse
  - platform: state
    entity_id: binary_sensor.engine_running
    to: "on"
  - platform: state
    entity_id:
      - binary_sensor.door_front_left
      - binary_sensor.door_front_right
      - binary_sensor.door_sliding_left
      - binary_sensor.door_sliding_right
      - binary_sensor.door_tailgate
      - binary_sensor.door_popup_roof
      - binary_sensor.door_frigo
    to: "on"
    for:
      seconds: "{{ states('input_number.vanlife_porte_roulage_delai') | int }}"
condition:
  - condition: state
    entity_id: binary_sensor.engine_running
    state: "on"
  - condition: template
    value_template: >
      {{ expand('group.all_van_doors') | selectattr('state', 'eq', 'on') | list | count > 0 }}
action:
  - service: notify.notify
    data:
      title: "⚠️ ALERTE SÉCURITÉ LUPO"
      message: "Attention, un ouvrant est ouvert alors que le véhicule roule !"
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1.0
```

---

### Scénario 1.3 — Frigo Ouvert Trop Longtemps

* **Objectif :** Éviter la rupture de la chaîne du froid et la décharge inutile de la batterie cellule.
* **Trigger :** `binary_sensor.door_frigo` reste à `on` pendant une durée définie.
* **YAML d'automatisation :**

```yaml
alias: "Vanlife - P1 - Frigo ouvert trop longtemps"
description: "Alerte si la porte du réfrigérateur reste ouverte"
trigger:
  - platform: state
    entity_id: binary_sensor.door_frigo
    to: "on"
    for:
      seconds: "{{ states('input_number.vanlife_frigo_timer') | int }}"
condition: []
action:
  - service: notify.notify
    data:
      title: "❄️ Frigo Lupo"
      message: "La porte du réfrigérateur est ouverte depuis plus de {{ states('input_number.vanlife_frigo_timer') }} secondes."
```

---

### Scénario 2.2 — Surchauffe de l'Habitacle

* **Objectif :** Protéger les animaux, les équipements électroniques et les batteries contre une chaleur excessive en stationnement.
* **Trigger :** `sensor.temp_habitacle` dépasse `input_number.vanlife_surchauffe_seuil_temp`.
* **Action :** Notification Push d'urgence + activation automatique du relais de ventilation de secours.
* **YAML d'automatisation :**

```yaml
alias: "Vanlife - P1 - Surchauffe Habitacle"
description: "Alerte de température élevée et déclenchement de la ventilation"
trigger:
  - platform: numeric_state
    entity_id: sensor.temp_habitacle
    above: input_number.vanlife_surchauffe_seuil_temp
condition: []
action:
  - service: switch.turn_on
    target:
      entity_id: switch.relais_ventilation_secours
  - service: notify.notify
    data:
      title: "🔥 ALERTE SURCHAUFFE HABITACLE"
      message: "La température intérieure de Lupo a atteint {{ states('sensor.temp_habitacle') }}°C. Ventilation activée."
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 0.8
```

---

### Scénario 7.1 — Niveau Carburant Critique

* **Objectif :** Prévenir le risque de panne sèche lors des trajets en zones isolées.
* **Trigger :** `sensor.fuel_level` passe sous `input_number.vanlife_carburant_seuil_min`.
* **YAML d'automatisation :**

```yaml
alias: "Vanlife - P1 - Alerte Niveau Carburant"
description: "Alerte lorsque la jauge du réservoir passe sous le seuil critique"
trigger:
  - platform: numeric_state
    entity_id: sensor.fuel_level
    below: input_number.vanlife_carburant_seuil_min
condition:
  - condition: state
    entity_id: binary_sensor.engine_running
    state: "on"
action:
  - service: notify.notify
    data:
      title: "⛽ Carburant Bas"
      message: "Niveau de réservoir bas : {{ states('sensor.fuel_level') }}% restant."
```

---

### Scénario 7.2 — Anomalie de Consommation Trajet

* **Objectif :** Détecter une surconsommation anormale (fuite, régénération FAP bloquée, sous-gonflage sévère).
* **Trigger :** Consommation moyenne calculée `sensor.fuel_consumption` supérieure à `input_number.vanlife_conso_seuil_anomalie`.
* **YAML d'automatisation :**

```yaml
alias: "Vanlife - P1 - Anomalie Consommation Trajet"
description: "Détection d'une consommation moyenne anormale en cours de route"
trigger:
  - platform: numeric_state
    entity_id: sensor.fuel_consumption
    above: input_number.vanlife_conso_seuil_anomalie
    for:
      minutes: 10
condition:
  - condition: state
    entity_id: binary_sensor.engine_running
    state: "on"
action:
  - service: notify.notify
    data:
      title: "📊 Consommation Anormale"
      message: "La consommation moyenne s'élève à {{ states('sensor.fuel_consumption') }} L/100km sur les 10 dernières minutes."
```

---

### Scénario 7.3 — Codes Défaut Moteur Active (DTC OBD-II)

* **Objectif :** Remonter immédiatement tout code erreur renvoyé par le calculateur Ford Transit (BCM/PCM via WiCAN Pro).
* **Trigger :** `binary_sensor.dtc_active` passe à `on`.
* **YAML d'automatisation :**

```yaml
alias: "Vanlife - P1 - Code Défaut Moteur DTC"
description: "Alerte immédiate en cas d'apparition d'un code défaut OBD"
trigger:
  - platform: state
    entity_id: binary_sensor.dtc_active
    to: "on"
condition: []
action:
  - service: notify.notify
    data:
      title: "⚠️ DIAGNOSTIC MOTEUR (DTC)"
      message: "Un code défaut moteur a été détecté par le WiCAN Pro : {{ states('sensor.dtc') }}."
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1.0
```

---

## 5. Roadmap Global & Déploiement Phasé (P2 à P4)

> Roadmap initiale conservée comme historique : les jalons octobre/novembre sont dépassés et ne constituent pas des preuves de déploiement. L'échéance opérationnelle courante est le **15 décembre 2026** ; les scénarios dépendant du CAN restent à valider.

|    Priorité    | Scénarios                                       | Description & Intégration                                                  |          Phase          |
| :-------------: | :----------------------------------------------- | :-------------------------------------------------------------------------- | :----------------------: |
| **🔴 P1** | **1.1, 1.3, 2.2, 7.1, 7.2, 7.3**           | Socle critique de sécurité, climatisation et moteur                       |  **Octobre 2026**  |
| **🟡 P2** | **1.2, 1.4, 1.5, 2.1, 2.6, 7.4, 7.5, 7.6** | Hayon bivouac, tiroirs, intrusion, condensation, pitch/roll, turbo, Webasto | **Novembre 2026** |
| **🟢 P3** | **3.1, 3.2, 3.3, 3.4, 4.1, 5.1, 2.3**      | Victron VE.Direct (SOC/MPPT), gaz Mopeka, niveaux d'eau, toit, spots GPS    | **Décembre 2026** |
| **🔵 P4** | **2.4, 2.5, 4.2**                          | Peak dB nuit, alerte gel batteries/eau, rentrée auto des stores météo    |      **2027**      |

---

## 6. Liste de Contrôle Finale pour l'Installation Physique

- [ ] **1. Matériel RPi 5 :** Poser les silentblocs anti-vibrations et appliquer le vernis tropicalisant (*conformal coating*).
- [ ] **2. Zigbee :** Appairer et nommer les 8 détecteurs Aqara MCCGQ11LM avec leurs identifiants standardisés (`door_*`).
- [ ] **3. CAN Bus :** Vérifier le WiCAN Pro déjà installé physiquement, valider son intégration HA/RUT240, la compatibilité *Exosfer OBD Protect* et la remontée réelle des entités avant d'activer les scénarios.
- [ ] **4. CBE DS300 :** Raccorder les sorties d'état du module DS300 Tap au RPi 5 (D+, tensions, niveaux d'eau).
- [ ] **5. Interface Lovelace :** Créer la vue « Réglages Vanlife » intégrant les sliders pour tous les helpers `input_number.vanlife_*`.
- [ ] **6. Tests Réseau :** Valider la réception des notifications push critiques sur l'iPhone via Tailscale, hors réseau cellulaire domestique.
