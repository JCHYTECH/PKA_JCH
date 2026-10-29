# OPÉRATION CAN/OBD — Connexion WiCAN Pro → Lupo RPi

> **Date :** 2026-07-16 | **Rédacteur :** [[Dobby]] 🦉  
> **Deadline :** 7 août 2026 (arrivée Lupo)  
> **Objectif :** Exposer 17+ capteurs véhicule dans Home Assistant via le port OBD-II, sans aucun capteur physique.  
> **Matériel :** WiCAN Pro (MeatPi, ESP32-S3, ~82€) — HS-CAN + MS-CAN, PIDs Ford Transit prêts.  
> **Références :** `ADR-006-obd-can-wican-pro.md`, `specs/SPEC-CAN-BUS.md`, `BOM-VANLIFE.md`

---

## Checklist visuelle

```
[ ] 1. Commander WiCAN Pro (~82€)
[ ] 2. Configurer AP WiFi + MQTT sur Lupo RPi
[ ] 3. À réception : flasher + configurer WiCAN Pro (20 min)
[ ] 4. Préparer HA : preset PIDs + dashboard
[ ] 5. Jour J Lupo : brancher OBD + vérifier (5 min)
[ ] 6. Valider toutes les entités (roulage + stationnement)
```

---

## Étape 1 — Commander le WiCAN Pro

**Produit :** WiCAN Pro (MeatPi Electronics)  
**Où :** Crowd Supply (~89$) ou Mouser Belgique (~82€)  
**Délai estimé :** 2-3 semaines  
**Référence :** https://www.crowdsupply.com/meatpi-electronics/wican-pro

**⚠️ Ne pas confondre avec le WiCAN basic (38€)** — le basic ne supporte PAS le MS-CAN, donc pas de BCM (portes, pneus, batterie).

---

## Étape 2 — Préparer le réseau sur Lupo RPi (à faire maintenant)

Le WiCAN Pro communique en WiFi → MQTT → Home Assistant. Il faut que le RPi 5 Lupo ait un réseau WiFi local accessible en permanence, même sans Wi-Fi maison.

### 2.1 Activer le point d'accès WiFi sur le RPi 5

Se connecter en SSH au RPi Lupo :

```bash
# [M5] Se connecter au RPi Lupo
ssh root@100.106.152.118
```

**⚠️ Ne pas utiliser `ha network update --wifi-mode ap` en CLI** — le Supervisor HA reprend la main et l'activation échoue (testé le 16/07). Passer par l'UI.

Depuis le navigateur → `http://[IP RPi]:8123` → **Paramètres → Système → Réseau → wlan0** → configurer :

```
Mode         : Point d'accès (AP)
SSID         : VanLife_Network
Mot de passe : 30d34d25594d3617
Sécurité     : WPA2-PSK
Canal        : Auto
```

**Le RPi 5 fait tout :** AP WiFi + passerelle internet. On a déjà le dongle 4G ZTE MF833U1 (✅ REÇU) qui se branche en USB sur le RPi. Lui fournit internet, et le RPi 5 partage sa connexion via son WiFi en mode point d'accès.

```
                      ┌──────────────┐
Internet 4G ──USB──▶  │   RPi 5      │──WiFi AP──▶ WiCAN Pro (OBD)
(ZTE MF833U1)         │   Lupo       │──WiFi AP──▶ iPhone JC (dashboard)
                      │   HA OS      │──WiFi AP──▶ ESP32 (DS300 Tap)
                      └──────────────┘
```

**Un seul boîtier, zéro coût additionnel.** Le RPi 5 est le hub unique du van : domotique, réseau local, et passerelle internet.

### 2.2 Vérifier que MQTT est fonctionnel

```bash
# [M5] Sur le RPi Lupo
# Vérifier que Mosquitto tourne
ha addons info core_mosquitto

# Vérifier le service MQTT dans HA
# Paramètres → Appareils & Services → MQTT → devrait montrer « Connecté »
```

### 2.3 Noter les infos de connexion

À stocker dans `JCH_PRIVATE/credentials-central.md` :

```
WiFi AP van     : SSID=VanLife_Network / MDP=...
MQTT broker     : IP RPi 5 (ex: 192.168.8.1) / port 1883
MQTT user/pass  : homeassistant / [depuis HA → MQTT settings]
RPi 5 Tailscale : 100.106.152.118
```

---

## Étape 3 — Flasher et configurer le WiCAN Pro (dès réception)

### 3.1 Flasher le firmware

Brancher le WiCAN Pro en USB-C au Mac M5.

```bash
# [M5] Installer esptool si pas déjà fait
pip3 install esptool

# Télécharger le dernier firmware WiCAN
# https://github.com/meatpi-electronics/wican-fw/releases
# → Télécharger wican-pro-firmware-vX.X.X.bin

# Flasher
esptool.py --chip esp32s3 --port /dev/cu.usbmodem* --baud 921600 \
  write_flash 0x0 wican-pro-firmware-vX.X.X.bin
```

### 3.2 Configuration initiale

1. Débrancher/re brancher le WiCAN Pro (il émet un AP WiFi `WiCAN-XXXX`)
2. Connecter le Mac au WiFi `WiCAN-XXXX` (mot de passe : `wicanpro`)
3. Ouvrir `http://192.168.4.1` dans le navigateur
4. Configurer :

```
WiFi client :
  SSID : VanLife_Network
  MDP  : [le mot de passe de l'AP van]

MQTT :
  Broker : [IP du RPi 5 sur le réseau van, ex: 192.168.8.1]
  Port   : 1883
  User   : homeassistant
  Pass   : [mot de passe MQTT de HA]

OBD Protocol :
  HS-CAN : 500 kbps (pin 6/14)
  MS-CAN : 125 kbps (pin 3/11)
```

### 3.3 Charger le preset PIDs Ford Transit

Le repo `WiCAN-Ford-Transit` contient un fichier de config prêt à l'emploi :

```bash
# [M5] Cloner le repo des PIDs Ford Transit
git clone https://github.com/anthonysecco/WiCAN-Ford-Transit.git /tmp/wican-ford
```

Dans l'interface web du WiCAN (http://192.168.4.1) :
1. Aller dans **Settings → PID Presets**
2. Importer le fichier JSON de PIDs depuis `/tmp/wican-ford/`
3. Activer tous les PIDs (17+)
4. Sauvegarder

### 3.4 Configurer le power management

Dans l'interface WiCAN → **Settings → Power Management** :

```
Sleep Mode        : Deep Sleep (<1mA)
Wake Interval     : 300 secondes (5 min)
Wake Duration     : 10 secondes
Low Voltage Cutoff: 11.8V (protège la batterie porteur)
```

> **Logique :** En roulage (>13.2V détecté sur OBD) → WiCAN actif, données live.  
> En stationnement → deep sleep, réveil 5 min, poll rapide BCM+PCM, MQTT push, re-sleep.  
> Si batterie < 11.8V → arrêt complet.

### 3.5 Vérification pré-van

Après config, le WiCAN Pro doit apparaître dans HA :

- Aller dans **Paramètres → Appareils & Services → MQTT**
- Un nouveau device `wican-pro` doit apparaître avec ~17 entités
- Les entités seront en `unavailable` (normal : pas branché sur OBD)
- Vérifier que le device ne flood pas MQTT (pas de messages toutes les secondes)

---

## Étape 4 — Préparer Home Assistant

### 4.1 Dashboard CAN/OBD

Créer un dashboard dédié dans HA :

```yaml
# [M5] Fichier à placer dans HA → Tableaux de bord → Nouveau → CAN/OBD
title: "🚛 Lupo — CAN/OBD"
views:
  - title: Conduite
    cards:
      - type: gauge
        entity: sensor.vehicle_speed
        name: Vitesse
        max: 180
      - type: gauge
        entity: sensor.engine_rpm
        name: Régime
        max: 5000
      - type: gauge
        entity: sensor.fuel_level
        name: Carburant
        max: 100
      - type: entities
        entities:
          - sensor.coolant_temp
          - sensor.intake_air_temp
          - sensor.ambient_air_temp
          - sensor.manifold_pressure
          - sensor.fuel_rate
          - sensor.engine_load
          - sensor.throttle_position
  - title: Portes & Pneus
    cards:
      - type: glance
        entities:
          - binary_sensor.door_driver
          - binary_sensor.door_passenger
          - binary_sensor.door_left_rear
          - binary_sensor.door_right_rear
          - binary_sensor.door_luggage
          - binary_sensor.hood
      - type: entities
        entities:
          - sensor.tpms_front_left
          - sensor.tpms_front_right
          - sensor.tpms_rear_left_outer
          - sensor.tpms_rear_right_outer
          - sensor.tpms_rear_left_inner
          - sensor.tpms_rear_right_inner
  - title: Batterie & Diag
    cards:
      - type: entities
        entities:
          - sensor.battery_soc
          - sensor.battery_current
          - sensor.battery_voltage_bcm
          - sensor.ecu_voltage
          - sensor.dtc_count
```

### 4.2 Automatisations de base

```yaml
# Alerte : batterie porteur faible en stationnement
alias: "CAN — Batterie porteur faible"
trigger:
  - platform: numeric_state
    entity_id: sensor.battery_soc
    below: 50
condition:
  - condition: state
    entity_id: binary_sensor.van_engine_running  # à créer via RPM > 0
    state: "off"
action:
  - service: notify.mobile_app_jc_iphone
    data:
      title: "🔋 Lupo — Batterie faible"
      message: "Batterie porteur à {{ states('sensor.battery_soc') | int }}% — démarrer le moteur ou brancher secteur."

# Alerte : DTC actif
alias: "CAN — Code défaut moteur"
trigger:
  - platform: numeric_state
    entity_id: sensor.dtc_count
    above: 0
action:
  - service: notify.mobile_app_jc_iphone
    data:
      title: "⚠️ Lupo — DTC détecté"
      message: "{{ states('sensor.dtc_count') | int }} code(s) défaut actif(s). Vérifier au prochain arrêt."
```

### 4.3 Template sensors utiles

```yaml
# Consommation instantanée L/100km
template:
  - sensor:
      - name: "Conso instantanée"
        unit_of_measurement: "L/100km"
        state: >
          {% set fuel_rate = states('sensor.fuel_rate') | float(0) %}
          {% set speed = states('sensor.vehicle_speed') | float(0) %}
          {% if speed > 5 %}
            {{ (fuel_rate / speed * 100) | round(1) }}
          {% else %}
            0
          {% endif %}

# Range estimée
      - name: "Autonomie estimée"
        unit_of_measurement: "km"
        state: >
          {% set fuel_pct = states('sensor.fuel_level') | float(0) %}
          {{ (fuel_pct * 0.7) | round(0) }}
        # Simplifié : ~70L réservoir × ~10km/L = 700km pleins
```

---

## Étape 5 — Installation dans Lupo (Jour J, 5 minutes)

### 5.1 Brancher

1. Localiser le port OBD-II : sous le tableau de bord, côté conducteur (gauche du volant, souvent derrière un cache plastique)
2. Brancher le WiCAN Pro — il s'enclenche, ça tient tout seul
3. Le port OBD est alimenté en permanence (même contact coupé) → le WiCAN démarre immédiatement

### 5.2 Vérifier

```bash
# [M5] Se connecter au RPi Lupo (via Tailscale si à distance)
ssh root@100.106.152.118

# Vérifier que le WiCAN est connecté au WiFi
# Dans HA → Paramètres → Appareils → wican-pro → devrait montrer « Connecté »

# Vérifier les entités
# Dans HA → Outils de développement → ÉTATS
# Chercher "vehicle_speed", "engine_rpm", "fuel_level", etc.
```

Vérifications rapides :
- [ ] Contact ON → `sensor.ecu_voltage` passe à ~12V
- [ ] Moteur tournant → `sensor.engine_rpm` > 0, `sensor.vehicle_speed` à 0
- [ ] Ouvrir porte conducteur → `binary_sensor.door_driver` passe ON

---

## Étape 6 — Validation complète (premier trajet)

### 6.1 En roulage (moteur tournant)

```
[ ] Vitesse : sensor.vehicle_speed suit le compteur
[ ] RPM    : sensor.engine_rpm cohérent
[ ] T°C    : sensor.coolant_temp monte progressivement (80-90°C cible)
[ ] Turbo  : sensor.manifold_pressure varie avec l'accélérateur (100-250 kPa)
[ ] Conso  : sensor.fuel_rate > 0, conso L/100km calculée cohérente
[ ] Carburant : sensor.fuel_level descend (très lentement, c'est normal)
[ ] Portes : toutes les binary_sensor.door_* reflètent l'état réel
```

### 6.2 En stationnement (moteur coupé > 30 min)

```
[ ] WiCAN en deep sleep (vérifier : pas de données live dans HA)
[ ] Periodic wake fonctionne (une mise à jour toutes les ~5 min)
[ ] TPMS pneus : valeurs cohérentes (probablement les pressions à froid)
[ ] Batterie porteur SOC cohérent avec la jauge tableau de bord
```

### 6.3 Test réseau

```
[ ] WiCAN se reconnecte automatiquement au WiFi van après un redémarrage
[ ] Si le RPi 5 reboot, le WiCAN se reconnecte sans intervention
[ ] Si on coupe le contact + ré-ouvre → WiCAN se réveille et reconnecte
```

---

## Dépannage rapide

| Symptôme | Cause probable | Action |
|----------|---------------|--------|
| Aucune entité dans HA | WiCAN pas connecté au MQTT | Vérifier WiFi + IP broker + credentials MQTT dans interface WiCAN |
| Entités « unavailable » | WiCAN pas branché sur OBD | Vérifier connexion physique, la LED du WiCAN doit être allumée |
| Pas de données BCM (portes, pneus) | MS-CAN non configuré | Vérifier pins OBD 3/11, MS-CAN 125 kbps dans les settings WiCAN |
| Données PCM OK mais pas BCM | MS-CAN câblage ou vitesse | Certains Ford utilisent MS-CAN sur pins 1/8 au lieu de 3/11 → tester |
| WiCAN ne dort pas | Voltage OBD > 13.2V (alternateur ou chargeur branché) | Normal — le sleep ne s'enclenche que si < 12.8V |
| WiCAN vide la batterie | Low voltage cutoff désactivé | Activer cutoff < 11.8V dans Power Management |
| PIDs BCM erronés | Le repo couvre Transit 2020+ mais pas forcément Custom 2026 | Valider les PIDs avec FORScan → ajuster les adresses CAN si besoin |

---

## Coût & timing

| Poste | Coût | Statut |
|-------|------|--------|
| WiCAN Pro | ~82€ | 🔴 À commander (Crowd Supply / Mouser) |
| ZTE MF833U1 (dongle 4G) | 0€ | ✅ Déjà reçu |
| FORScan (app Windows/Mac) | Gratuit (version standard) | Outil de diagnostic si PIDs à valider |

**Délai critique :** commander le WiCAN Pro **cette semaine**. Délai Crowd Supply : 2-3 semaines → réception ~début août, juste à temps.

---

*Document créé par [[Dobby]] 🦉 — 2026-07-16 — modèle: deepseek-v4*  
*Issu de `ADR-006-obd-can-wican-pro.md` et `specs/SPEC-CAN-BUS.md`*  
*À exécuter avec [[Forge]] 🦦 (réseau) et [[Araignée]] 🕷️ (intégration HA)*
