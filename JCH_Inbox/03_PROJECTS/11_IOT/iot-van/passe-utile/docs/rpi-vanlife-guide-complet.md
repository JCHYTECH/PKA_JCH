# Guide Complet : Raspberry Pi pour le Vanlife

> Document structuré — synthèse d'une conversation technique brute du 2026-05-30, recadrée et enrichie des retours d'expérience WildNexus sur le Raspberry Pi 5.
> Niveau : accessible au non-expert, complet pour l'expert.

**Dernière mise à jour :** 2026-05-30  
**Source originale :** `JCH_Inbox/00_INBOX/IOT vanlife` (conversation LLM brute, 1158 lignes)  
**Fichiers liés :** [[rpi-vanlife-guide-complet]], [[BIRDNET_PI_ACCESS]], [[2026-05-28_retour-test-maison-rpi-birdnet-mobile]]

---

## Résumé exécutif (30 secondes)

Un Raspberry Pi (4 ou 5) consomme moins de 15W, fonctionne sur le 12V du van via un convertisseur DC-DC, et centralise en un seul boîtier : monitoring température/humidité, alertes frigo, point d'accès Wi-Fi autonome, suivi GPS, verrouillage des tiroirs en roulant, et jauges d'eau. Budget complet : **~165€**.

**⚠️ Leçons WildNexus intégrées :** le RPi 5 exige un câble USB-C PD (Power Delivery) — sans cela, undervoltage chronique et reboots. Le stockage doit être sur SSD, pas sur microSD. Les conflits de permissions DB sont un piège classique.

---

## Table des matières

1. [Pourquoi un Raspberry Pi en van ?](#1-pourquoi-un-raspberry-pi-en-van-)
2. [Checklist matériel & budget](#2-checklist-matériel--budget)
3. [Alimentation électrique — schéma de branchement](#3-alimentation-électrique--schéma-de-branchement)
4. [Installation de Home Assistant OS](#4-installation-de-home-assistant-os)
5. [Point d'accès Wi-Fi autonome](#5-point-daccès-wi-fi-autonome)
6. [Capteurs et monitoring](#6-capteurs-et-monitoring)
7. [Tableau de bord mobile Lovelace](#7-tableau-de-bord-mobile-lovelace)
8. [Automatisations](#8-automatisations)
9. [Extensions avancées](#9-extensions-avancées)
10. [Pièges RPi 5 — Leçons croisées WildNexus](#10-pièges-rpi-5--leçons-croisées-wildnexus)

---

## 1. Pourquoi un Raspberry Pi en van ?

Le Raspberry Pi est le cerveau domotique idéal pour un fourgon aménagé :

- **Consommation dérisoire** : moins de 15W en charge, quelques watts au repos.
- **Tension compatible** : fonctionne en 5V DC, facilement convertible depuis le 12V de la batterie cellule.
- **Modularité totale** : un seul boîtier remplace plusieurs appareils spécialisés (routeur, serveur multimédia, centrale domotique, GPS tracker).
- **Fonctionnement hors-ligne** : pas besoin d'internet — le Pi génère son propre réseau Wi-Fi local.

### Ce qu'il peut gérer dans un van

| Fonction | Logiciel / Matériel |
|----------|---------------------|
| Domotique (lumières, relais, chauffage) | Home Assistant OS |
| Monitoring batterie & solaire | Venus OS (Victron) |
| Serveur multimédia offline | Jellyfin, Plex, Kodi |
| Routeur 4G/5G + Wi-Fi | Dongle USB LTE + hostapd |
| Capteurs température/humidité | Zigbee (Sonoff, Xiaomi) |
| GPS tracking & géolocalisation | Clé USB GPS u-blox 7/8 |
| Verrouillage tiroirs en roulant | Relais 12V + solénoïdes |
| Jauges d'eau (sans percer) | Ultrasons JSN-SR04T ou pression hydrostatique |
| Nivellement du van | ESP32 + MPU6050 + ESPHome |

---

## 2. Checklist matériel & budget

### Cœur du système (~105€)

| Composant | Recommandation | Prix indicatif |
|-----------|---------------|----------------|
| Raspberry Pi 4 (4 Go) ou Pi 5 (4/8 Go) | Pi 4 chauffe moins ; Pi 5 plus puissant | ~55-80€ |
| Boîtier passif aluminium | Flirc ou Argon ONE (sans ventilateur = silencieux) | ~15€ |
| **SSD M.2 NVMe 128 Go à 1 To** + adaptateur HAT | ⚠️ Obligatoire (pas de microSD — voir §10) | ~25-40€ |

> **Choix Pi 4 vs Pi 5 :** Le Pi 4 (4 Go) suffit pour Home Assistant + multimédia. Le Pi 5 (8 Go) permet plus de marge pour l'IA locale (BirdNET, reconnaissance d'images). Le Pi 5 exige une alimentation plus stricte (5V/5A vs 5V/3A pour le Pi 4).

### Alimentation électrique (~25€)

| Composant | Spécification | Prix indicatif |
|-----------|--------------|----------------|
| Convertisseur DC-DC 12V→5V USB-C | 3A min (Pi 4) ou **5A min (Pi 5)** | ~10€ |
| Porte-fusible étanche + fusible 3A/5A | À placer au plus près de la batterie | ~5€ |
| Interrupteur à bascule | Pour couper le système en hivernage | ~5€ |
| **Câble USB-C PD** (Pi 5 uniquement) | ⚠️ Obligatoire — voir §10 | ~5€ |

### Pack surveillance Zigbee (~30€)

| Composant | Modèle recommandé | Prix indicatif |
|-----------|------------------|----------------|
| Clé USB Zigbee | Sonoff ZBDongle-E ou SkyConnect | ~15€ |
| Capteur température/humidité × 2 | Sonoff SNZB-02D | ~10€ |
| Capteur d'ouverture porte/fenêtre | Sonoff SNZB-04 | ~5€ |

### Extensions optionnelles

| Composant | Usage | Prix indicatif |
|-----------|-------|----------------|
| Clé USB GPS u-blox 7/8 | Tracking van | ~12€ |
| ESP32 + MPU6050 | Inclinomètre / nivellement | ~7€ |
| Verrous solénoïdes 12V × 4 | Tiroirs automatiques | ~16€ |
| Carte relais 12V | Pilotage verrous/pompes/LED | ~8€ |
| Dongle USB 4G/5G | Routeur cellulaire | ~30-50€ |

**Budget total minimum :** ~165€ (cœur + alimentation + Zigbee)  
**Budget complet avec extensions :** ~250€

---

## 3. Alimentation électrique — schéma de branchement

Le système doit **obligatoirement** être raccordé à la batterie auxiliaire (cellule), jamais à la batterie moteur.

```
[ Batterie Auxiliaire 12V ]
       │
       ├── (+) Borne Positive ──── [ Fusible 3A/5A ] ──── [ Interrupteur ] ───┐
       │                                                                      │
       └── (-) Borne Négative (Masse) ────────────────────────────────────────┼──────┐
                                                                              │      │
                                                                       ┌──────┴──────┴──────┐
                                                                       │ Convertisseur      │
                                                                       │ DC-DC 12V → 5V    │
                                                                       └──────┬──────┬──────┘
                                                                              │      │
                                                                              ▼      ▼
                                                                       [ Câble USB-C 5V ]
                                                                              │
                                                                              ▼
                                                                     [ Raspberry Pi 4 / 5 ]
```

### Règles critiques

1. **Jamais directement sur le 12V** — la tension d'une batterie cellule fluctue entre 11V et 14,4V. Le convertisseur DC-DC est indispensable.
2. **Fusible au plus près de la batterie** — protège le câblage en amont.
3. **Interrupteur physique** — permet un arrêt propre (le `shutdown` logiciel seul ne coupe pas la consommation résiduelle).
4. **⚠️ Pi 5 : câble USB-C PD obligatoire** — un câble USB-C classique ou un port USB standard de powerbank ne délivre pas les 5V/5A requis. Conséquence : undervoltage, throttling CPU, reboots aléatoires. **Validé par l'expérience WildNexus du 28/05/2026.**

### Procédure d'installation

1. Retirer le fusible (sécurité).
2. Câbler : batterie (+) → fusible → interrupteur → entrée `IN+` du convertisseur.
3. Câbler : batterie (-) → entrée `IN-` du convertisseur.
4. Relier la sortie USB-C du convertisseur au Raspberry Pi.
5. Insérer le fusible, basculer l'interrupteur — la LED rouge du convertisseur doit être fixe.

---

## 4. Installation de Home Assistant OS

1. Télécharger **Raspberry Pi Imager** sur un ordinateur.
2. Sélectionner : **Choisir l'OS → Other specific-purpose OS → Home Automation → Home Assistant**.
3. Sélectionner le disque SSD branché à l'ordinateur, cliquer sur **Écrire**.
4. Brancher le SSD gravé sur un port USB 3.0 (bleu) du Raspberry Pi.
5. Connecter le câble Ethernet (premier boot) ou configurer le Wi-Fi via l'Imager.
6. Mettre sous tension. Patienter 5-10 minutes.
7. Accéder à `http://homeassistant.local:8123` pour la configuration initiale.

> **Pourquoi SSD et pas microSD ?** Voir §10 — les coupures de courant et vibrations corrompent les microSD en quelques semaines.

---

## 5. Point d'accès Wi-Fi autonome

En itinérance, le Raspberry Pi génère son propre réseau Wi-Fi local. Votre téléphone s'y connecte directement, sans box ni internet.

### Configuration via Home Assistant

1. Dans Home Assistant : **Paramètres → Modules complémentaires → Boutique → Access Point**.
2. Installer et configurer :
   - **SSID :** `VanLife_Network`
   - **Mot de passe :** (choisir un mot de passe fort)
   - **Canal Wi-Fi :** 6 (si interférences, changer)
3. Démarrer le module. Le réseau Wi-Fi `VanLife_Network` apparaît.

### Deux modes de connexion

| Mode | Fonctionnement | Usage |
|------|---------------|-------|
| **Local** (sans internet) | Le Pi crée son propre Wi-Fi, le téléphone s'y connecte directement | Bivouac isolé, consultation tableau de bord |
| **Distant** (avec 4G/5G) | Dongle USB LTE branché au Pi + VPN Tailscale/WireGuard | Surveillance à distance (randonnée, ville) |

---

## 6. Capteurs et monitoring

### 6.1 Température, humidité, sécurité (Zigbee)

**Matériel :** clé USB Zigbee Sonoff + capteurs Sonoff SNZB-02D (température) et SNZB-04 (ouverture).

**Procédure d'appairage :**
1. Brancher la clé Zigbee sur le Pi.
2. Dans Home Assistant : **Paramètres → Appareils et services → Ajouter une intégration → Zigbee Home Automation**.
3. Mettre les capteurs en mode appairage (appui long sur le bouton).
4. Les capteurs apparaissent automatiquement.

**Emplacements recommandés :**
- 1 capteur température/humidité dans la cellule (zone de vie)
- 1 capteur température dans le réfrigérateur (chaîne du froid)
- 1 capteur d'ouverture sur la porte latérale (sécurité)

### 6.2 GPS tracking

**Matériel :** clé USB GPS G-Mouse u-blox 7 ou 8 (~12€).

**Installation :**
1. Brancher la clé sur un port USB du Pi.
2. Dans Home Assistant : **Ajouter une intégration → GPSD**.
3. Le capteur `sensor.gps_speed` et les coordonnées apparaissent.

**Astuce vanlife :** le signal GPS ne traverse pas le métal. Placer la clé près d'une fenêtre ou derrière le pare-brise avec une rallonge USB.

### 6.3 Jauges d'eau (sans percer les cuves)

| Méthode | Capteur | Principe | Précision |
|---------|---------|----------|-----------|
| **Ultrasons (par le dessus)** | JSN-SR04T étanche | Onde ultrasonore → mesure du temps de retour → distance surface eau | ±5% |
| **Pression hydrostatique (par le dessous)** | Capteur sur durite de sortie | Pression proportionnelle à la hauteur d'eau | ±1% (au litre près) |

### 6.4 Monitoring batterie (Victron)

Si l'installation électrique utilise des composants Victron Energy :

1. Installer **Venus OS** sur le Raspberry Pi (au lieu de Home Assistant, ou en parallèle sur un second Pi).
2. Connecter SmartShunt, MPPT et convertisseur via câbles USB-to-VE.Direct.
3. Tableau de bord temps réel de l'autonomie électrique sur écran tactile 7".

---

## 7. Tableau de bord mobile Lovelace

Interface épurée à gros boutons, lisible en roulant sur smartphone.

```yaml
views:
  - title: Mon Smart Van
    path: home_van
    cards:
      # EN-TÊTE
      - type: heading
        heading: "🚌 Mon Smart Van"
        badge:
          icon: mdi:wifi
          color: success

      # TEMPÉRATURES
      - type: grid
        columns: 2
        square: false
        cards:
          - type: tile
            entity: sensor.temperature_interieur
            title: "Cellule"
            icon: mdi:thermometer
            color: orange
          - type: tile
            entity: sensor.temperature_frigo
            title: "Réfrigérateur"
            icon: mdi:fridge
            color: blue

      # HUMIDITÉ ET SÉCURITÉ
      - type: grid
        columns: 2
        square: false
        cards:
          - type: tile
            entity: sensor.humidite_interieur
            title: "Humidité"
            icon: mdi:water-percent
            color: teal
          - type: tile
            entity: binary_sensor.porte_laterale
            title: "Porte Fourgon"
            color: red

      # ALERTE FRIGO (invisible si < 7°C)
      - type: conditional
        conditions:
          - condition: numeric_state
            entity: sensor.temperature_frigo
            above: 7
        card:
          type: markdown
          content: "⚠️ **ATTENTION :** Le frigo est trop chaud ! Température : {{ states('sensor.temperature_frigo') }}°C"
```

> **Astuce mobile :** la carte `conditional` masque les alertes quand tout va bien — l'écran reste propre. L'alerte rouge n'apparaît qu'en cas de problème réel.

---

## 8. Automatisations

### 8.1 Alerte température frigo

- **Déclencheur :** `sensor.temperature_frigo` > 7°C pendant 15 minutes
- **Action :** notification push sur le smartphone : *"⚠️ Rupture de la chaîne du froid dans le van !"*

### 8.2 Verrouillage des tiroirs en roulant

**Matériel :** verrous solénoïdes 12V (modèles "Fail-Safe" Normalement Ouverts) + carte relais + diode 1N4007.

**Schéma de câblage :**
```
[ GPIO 26 du Pi ] ──► [ IN1 de la carte relais ]
[ 12V Batterie  ] ──► [ COM du relais ] → [ NO ] → [ (+) Verrou 12V ]
[ Masse 12V     ] ──► [ (-) Verrou 12V ]
                                   └── [ Diode 1N4007 ] ──┘ (bague grise côté +)
```

**Automatisation dans Home Assistant :**
- **Quand :** `sensor.van_gps_speed` > 5 km/h → Activer le relais (verrouillage)
- **Quand :** `sensor.van_gps_speed` = 0 km/h pendant 15 secondes → Couper le relais (déverrouillage)

### 8.3 Notification porte ouverte

- **Déclencheur :** `binary_sensor.porte_laterale` passe à `on` (ouverte)
- **Condition :** entre 22:00 et 06:00 (nuit)
- **Action :** notification + allumer les LED en rouge

---

## 9. Extensions avancées

### 9.1 Inclinomètre / Nivellement du van

**Matériel :** ESP32 (~4€) + MPU6050 (~3€).

**Câblage MPU6050 → ESP32 :**
```
MPU6050 VCC → ESP32 3V3
MPU6050 GND → ESP32 GND
MPU6050 SCL → ESP32 GPIO 22
MPU6050 SDA → ESP32 GPIO 21
```

**Fixation :** capteur à plat au centre du châssis (sous un siège ou meuble bas). C'est lui qui définit le zéro.

**Code ESPHome :**
```yaml
esphome:
  name: van-level

esp32:
  board: esp32dev

wifi:
  ssid: "VanLife_Network"
  password: "MonSuperMotDePasse"

i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true

sensor:
  - platform: mpu6050
    address: 0x68
    accel_x:
      name: "Van Inclinaison Roll"
    accel_y:
      name: "Van Inclinaison Pitch"
    update_interval: 1s
```

**Dashboard :** utiliser la carte communautaire `van-tilt-card` (via HACS) avec `wheelbase` et `track_width` du véhicule. Home Assistant calcule automatiquement l'épaisseur des cales à placer sous chaque roue.

### 9.2 VanPi / Pekaway (alternative clé en main)

Projet open-source allemand dédié aux vans. OS + cartes d'extension pour gérer chauffage stationnaire, pompes à eau, bandes LED sans coder.

---

## 10. Pièges RPi 5 — Leçons croisées WildNexus

> Cette section capitalise sur les retours d'expérience du projet WildNexus (BirdNET-Pi sur RPi 5), validés en conditions réelles les 28-29 mai 2026.

### 10.1 Alimentation : le piège de l'undervoltage

**Constat WildNexus (28/05/2026) :** test RPi 5 avec powerbank Anker 20100 mAh. Port USB classique → `throttled=0x50000`, 15 épisodes d'undervoltage, reboot à 21:09.

| Ce que le document vanlife dit | Ce que WildNexus a découvert |
|-------------------------------|------------------------------|
| « Convertisseur 12V→5V 3A (Pi 4) ou 5A (Pi 5) » | Le Pi 5 exige **5V/5A** et un câble **USB-C PD (Power Delivery)**. Un convertisseur 5A seul ne suffit pas si le câble n'est pas PD. |
| Adaptation van : alimentation sur batterie cellule | Adaptation terrain : powerbank. Même problème — le port USB classique d'une powerbank plafonne à 2.4A. |

**Règle pour le van :**
- Convertisseur DC-DC 12V→5V certifié USB-C PD, **5A minimum**.
- Câble USB-C à **5A avec chip e-mark** (le câble « charge rapide » standard ne suffit pas).
- Ne pas utiliser les ports USB de la powerbank comme source — utiliser la sortie DC régulée ou un convertisseur dédié.

### 10.2 Stockage : SSD obligatoire, pas de microSD

**Constat :** le document vanlife mentionne le SSD en option recommandée. L'expérience terrain WildNexus confirme que c'est **obligatoire**.

| Risque | Cause | Solution |
|--------|-------|----------|
| Corruption microSD | Coupures de courant soudaines (le Pi n'a pas de batterie tampon) | SSD M.2 NVMe + adaptateur HAT USB ou PCIe |
| Corruption microSD | Vibrations en roulant | SSD : pas de pièces mobiles, résistant aux chocs |
| Wear-out accéléré | Écritures intensives de Home Assistant (base de données, logs) | SSD : endurance TBW 10-100× supérieure à une microSD |

**Configuration recommandée pour le van :**
- SSD M.2 NVMe 128 Go minimum (les logs HA peuvent atteindre 10-20 Go/mois).
- Boot direct sur SSD (le Pi 4 et Pi 5 le supportent nativement).
- Garder une microSD de secours avec l'image de base (Plan B si le SSD lâche).

### 10.3 SQLite : le piège des permissions

**Constat WildNexus (28/05/2026) :** erreur « Database busy » sur BirdNET-Pi. Cause : conflit d'ownership entre l'utilisateur `jchavaux` (scripts Python d'analyse) et le groupe `caddy` (serveur web).

**Leçon transposable au van :** Home Assistant utilise SQLite comme base par défaut. Si des scripts personnalisés (Python, cron, add-ons) écrivent dans la même base ou des bases liées, vérifier :

```bash
# Exemple de fix appliqué sur BirdNET-Pi
usermod -a -G caddy jchavaux       # ajouter l'utilisateur au groupe du serveur
chmod 664 /chemin/vers/la/base.db  # lecture/écriture pour owner + groupe
chown jchavaux:caddy /chemin/vers/la/base.db
```

Pour le van, ce piège apparaît si vous :
- Écrivez des scripts Python custom qui lisent/écrivent `home-assistant_v2.db`
- Utilisez des add-ons qui accèdent à la base sous un utilisateur différent

**Solution préventive :** ne jamais écrire directement dans la base HA. Utiliser l'API REST ou les `input_number`/`sensor` de Home Assistant pour toute interaction externe.

### 10.4 Documentation et GPS

**Erreur WildNexus :** la documentation référençait le port 8080 pour l'interface web, mais le port correct était 80 (8080 = gotty, bindé localhost). Les coordonnées GPS étaient celles d'Anvers au lieu d'Esneux-Tilff.

**Leçon pour le van :**
- Après installation, vérifier chaque port documenté avec `ss -tlnp` sur le Pi.
- Configurer GPSD avec les coordonnées exactes du point de montage.
- Documenter la configuration finale dans un fichier `VAN_PI_ACCESS.md` (inspiré de `BIRDNET_PI_ACCESS.md`).

### 10.5 Réseau : bascule Wi-Fi / cellulaire

**Constat WildNexus (29/05/2026) :** connexion Wi-Fi maison + LTE backup sur le RPi. Wi-Fi prioritaire (metric 600), LTE backup (metric 700). Problème : `wlan0` se reconnectait automatiquement même après `disconnect`.

**Pour le van :**
- Point d'accès Wi-Fi local = réseau primaire (téléphone ↔ Pi).
- Dongle 4G/5G = connexion internet.
- Ne pas configurer de Wi-Fi externe « de secours » sans désactiver l'autoconnexion (`autoconnect=false` dans NetworkManager).

### 10.6 Résumé — Carte des risques RPi 5

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|------------|
| Undervoltage / reboots | **Élevée** (sans USB-C PD) | Critique — arrêt du système | Câble USB-C PD 5A + convertisseur certifié |
| Corruption microSD | **Élevée** (vanlife) | Critique — perte de données | Boot sur SSD M.2 NVMe |
| Conflit permissions DB | Moyenne | Bloquant — HA inaccessible | API REST, pas d'écriture directe DB |
| Ports documentés erronés | Faible | Gênant — debug perdu | `ss -tlnp` après install |
| Autoconnexion Wi-Fi parasite | Moyenne | Perturbant — bascule réseau | `autoconnect=false` |

---

## Références

- [[rpi-vanlife-guide-complet]] — ce document
- [[BIRDNET_PI_ACCESS]] — fiche d'accès RPi WildNexus (modèle pour `VAN_PI_ACCESS.md`)
- [[2026-05-28_retour-test-maison-rpi-birdnet-mobile]] — rapport de test RPi 5 avec leçons détaillées
- [[2026-05-26_protocole-terrain-24h-rpi-birdnet-mobile]] — protocole de test terrain 24h
- `JCH_Inbox/00_INBOX/IOT vanlife` — conversation brute originale (1158 lignes)
- [[camping_scout_guide]] — autre outil vanlife (recherche spots nuit)

---

*Document généré le 2026-05-30 par [[Dobby]] 🦉 à partir d'une conversation LLM brute recadrée et croisée avec la mémoire WildNexus.*
