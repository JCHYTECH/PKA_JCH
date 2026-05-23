# Fiche specs & BOM — Station bioacoustique/caméra hybride

Date : 2026-05-22  
Version figée : Prototype terrain sérieux — architecture ESP32-S3 + Pi Zero 2 W/CM4 + cloud BirdNET

## 1. Concept général

Appareil autonome outdoor destiné à :
- écouter en continu l’environnement sonore ;
- détecter localement des événements bioacoustiques ;
- enregistrer des extraits audio courts ;
- capturer photo/vidéo à la demande ;
- envoyer les données vers un cloud où BirdNET effectue l’analyse IA complète ;
- permettre à l’utilisateur proche de télécharger les données via WiFi local ;
- fonctionner sur batterie rechargeable, avec recharge USB-C et/ou panneau solaire.

## 2. Architecture fonctionnelle figée

```text
ESP32-S3 always-on
    ├─ microphones MEMS I2S
    ├─ capteurs environnementaux
    ├─ GPS / RTC
    ├─ détection sonore légère
    ├─ gestion énergie
    └─ réveil des modules lourds

        ↓ GPIO / UART / ESP-NOW

Pi Zero 2 W ou CM4 on-demand
    ├─ caméra NoIR / Starvis
    ├─ LEDs IR
    ├─ PIR optionnel
    ├─ stockage média
    ├─ compression audio/image
    ├─ portail WiFi local
    └─ upload cloud

        ↓ USB / UART

Module 4G LTE
    ├─ upload distant
    ├─ synchronisation cloud
    └─ fallback réseau si WiFi absent

        ↓

Cloud
    ├─ BirdNET complet
    ├─ stockage
    ├─ dashboard
    └─ mise à jour modèles IA
```

## 3. Spécifications cibles

| Domaine | Spécification cible |
|---|---|
| Usage | Station bioacoustique + caméra faune |
| Analyse IA | BirdNET dans le cloud, filtrage local léger |
| Contrôleur basse consommation | ESP32-S3 avec PSRAM |
| Ordinateur média | Raspberry Pi Zero 2 W pour prototype ; CM4 pour pré-série |
| Audio | 2 microphones MEMS I2S, enregistrement court 5–15 s |
| Caméra prototype | Raspberry Pi Camera Module 3 NoIR Wide, Sony IMX708, 12 MP |
| Caméra alternative nocturne | Arducam Sony Starvis IMX462, M12/CS-mount |
| Vision nocturne | LEDs IR 940 nm discrètes ou 850 nm portée supérieure |
| Détection mouvement | PIR basse consommation optionnel |
| Environnement | Température, humidité, pression, VOC/eCO₂/AQI |
| Lumière | Capteur spectral 11 canaux type AS7341 |
| Positionnement | GNSS basse consommation, u-blox M10 ou équivalent |
| Temps | RTC basse consommation |
| Stockage | microSD audio/logs + microSD média ou stockage central Pi |
| Transmission distante | 4G LTE Cat-1 pour audio/photo ; Cat-4 si vidéo fréquente |
| Accès local | Hotspot WiFi du Pi, portail web local |
| Alimentation | Batterie rechargeable utilisateur + USB-C + solaire |
| Gestion énergie | BMS, power-path, MPPT solaire, fuel gauge, load switches |
| Boîtier | IP65/IP66, presse-étoupes, évent membrane, fixation trépied/arbre |
| Mode normal | ESP32 actif, Pi/4G/caméra/IR éteints |
| Mode événement | Réveil Pi, capture, stockage, upload différé |
| Mode maintenance | Hotspot WiFi local, téléchargement et configuration |

## 4. BOM prototype — version recommandée

| Bloc | Composant recommandé | Qté | Coût estimé € |
|---|---|---:|---:|
| Contrôleur audio | ESP32-S3 DevKit avec PSRAM | 1 | 12 |
| Microphones | MEMS I2S INMP441 ou ICS-43434 | 2 | 8 |
| SBC média | Raspberry Pi Zero 2 W | 1 | 25 |
| Caméra | Raspberry Pi Camera Module 3 NoIR Wide IMX708 | 1 | 40 |
| Nappe caméra | CSI câble Pi Zero | 1 | 5 |
| IR | Module LEDs IR 940 nm + résistance/driver | 1 | 15 |
| Commutation IR | MOSFET logic-level + dissip./driver | 1 | 4 |
| PIR | PIR basse consommation | 1 | 6 |
| Environnement | BME688/BME680 module | 1 | 15 |
| Lumière | AS7341 spectral sensor module | 1 | 20 |
| GNSS | Module u-blox M10 ou compatible | 1 | 25 |
| RTC | DS3231 ou RV-3028 module | 1 | 6 |
| Stockage audio | microSD High Endurance 32 GB | 1 | 8 |
| Stockage média | microSD High Endurance 128 GB | 1 | 18 |
| Communication | LTE Cat-1 A7670 ou équivalent | 1 | 45 |
| Antenne LTE | Antenne externe + câble | 1 | 12 |
| Antenne GNSS | Antenne GNSS active/passive | 1 | 8 |
| Énergie | Pack LiFePO4 ou Li-ion 50–80 Wh avec BMS | 1 | 50 |
| Recharge solaire/USB | Solar charger / MPPT / power-path | 1 | 20 |
| Régulation | Buck 5 V 3 A + 3.3 V low-noise | 1 | 15 |
| Load switches | Coupure Pi, modem, caméra, IR | 4 | 12 |
| Mesure batterie | Fuel gauge INA219/INA226/MAX17048 | 1 | 8 |
| USB-C étanche | Connecteur/passe-cloison USB-C | 1 | 12 |
| Boîtier | Boîtier IP65/IP66 | 1 | 35 |
| Connectique | Presse-étoupes, JST, câbles, visserie | 1 lot | 25 |
| PCB/proto | Veroboard ou PCB proto + borniers | 1 | 20 |
| Marge intégration | petits composants, fusibles, TVS, joints | 1 lot | 30 |

**Total matériel prototype estimé : environ 499 €**

Fourchette réaliste prototype : **450–550 €**, hors main-d’œuvre, impression 3D éventuelle, carte SIM/data, cloud, frais de port et taxes variables.

## 5. Option économique

| Changement | Gain estimé |
|---|---:|
| Supprimer capteur spectral AS7341 | -20 € |
| Supprimer GPS | -25 € |
| Supprimer seconde microSD | -18 € |
| Utiliser OV5640/OV2640 au lieu de Camera Module 3 | -10 à -25 € |
| Supprimer 4G et utiliser WiFi local uniquement | -55 à -70 € |
| Boîtier simple non optimisé | -10 à -20 € |

Coût minimum raisonnable : **320–380 €**.

## 6. Option pré-série plus robuste

| Upgrade | Impact |
|---|---|
| Remplacer Pi Zero 2 W par CM4 avec eMMC | +50 à +100 € |
| Caméra Starvis IMX462 M12/CS | +30 à +80 € |
| Modem LTE Cat-4 SIM7600/EC25 | +30 à +70 € |
| PCB custom 4 couches | + coût NRE, baisse coût série |
| Batterie plus grande 100–150 Wh | +30 à +80 € |
| Boîtier industriel IP66 moulé/usinage | +50 à +150 € |

Coût pré-série unitaire probable : **600–850 €**.

## 7. Points critiques à valider en prototype

1. Consommation réelle en mode veille, événement, upload 4G et IR.
2. Qualité audio des MEMS dans boîtier étanche.
3. Risque de condensation sur micro/caméra.
4. Portée IR 940 nm et netteté nocturne.
5. Stabilité alimentation modem 4G lors des pics de courant.
6. Robustesse microSD après coupures d’alimentation.
7. Ergonomie du hotspot WiFi local.
8. Latence et coût data de l’envoi cloud.
9. Performance réelle du filtrage local avant upload.
10. Comportement solaire en hiver belge.

## 8. Décision d’architecture

Architecture figée recommandée :

```text
ESP32-S3 = gardien basse consommation
Pi Zero 2 W = média, WiFi local, compression, upload
4G LTE Cat-1 = connexion distante
Cloud = BirdNET complet
Batterie + USB-C + solaire = autonomie terrain
```

Pour prototype : Pi Zero 2 W.  
Pour produit pré-série : Compute Module 4 avec eMMC.
