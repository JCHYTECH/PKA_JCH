# BirdWeather PUC — Analyse des composants électroniques

*Source : chat [[Claude]], 23-05-2026*

---

## Correction préalable

Le traitement IA principal ([[BirdNET]]) est déporté sur le cloud, pas exécuté localement sur l'appareil. L'[[ESP32-S3]] embarque un moteur neural utilisé pour des tâches légères, mais l'inférence [[BirdNET]] complète (>6000 espèces) ne tourne pas sur le chip.

---

## Composants identifiés

### MCU principal
**[[ESP32-S3]]** (Espressif) — intègre WiFi 2.4 GHz, Bluetooth Low Energy, et un moteur neural AI embarqué. Gère l'acquisition audio, la connectivité, le GPS, et l'interface utilisateur (bouton + LED).

### Capteur environnemental
**Bosch BME688** — capteur multi-paramètres mesurant :
- Température
- Humidité
- Pression atmosphérique
- eAQI (indice de qualité d'air)
- eVOC (composés organiques volatils)
- eCO2 (estimé)

Protégé par des évents de type Gore-Tex à l'intérieur du boîtier.

### Capteur de lumière
**AMS AS7341** — capteur spectral 10 canaux (visible + proche IR). Lentille positionnée au sommet du boîtier, au centre du logo "PUC".

### Microphones
Deux microphones en configuration stéréo. Modèle exact non divulgué par le fabricant. Par la nature du design ([[ESP32-S3]], compact, faible consommation), vraisemblablement MEMS PDM ou I2S — **non confirmé officiellement**.

### GPS
Module GPS intégré — chip exact non publié.

### Accéléromètre
Mentionné dans une revue tierce (Oberon Citizen Science Network, juillet 2024). **Non confirmé dans la documentation officielle** — à vérifier.

### Stockage
MicroSD card pré-installée. Consommation moyenne : ~2 Go/jour avec les paramètres par défaut.

### Alimentation
- 3 piles AA (lithium recommandé) ou USB-C 5V externe
- Consommation mesurée : ~60 mA @ 5V (~300 mW)

---

## Tableau récapitulatif

| Composant | Référence | Statut |
|---|---|---|
| MCU | [[ESP32-S3]] (Espressif) | Confirmé (officiel) |
| Capteur environnemental | Bosch BME688 | Confirmé (FAQ officielle) |
| Capteur spectral | AMS AS7341 | Confirmé (FAQ officielle) |
| Microphones | MEMS x2 (modèle inconnu) | Partiellement confirmé |
| GPS | Modèle inconnu | Non divulgué |
| Accéléromètre | Modèle inconnu | Non confirmé officiellement |
| Stockage | MicroSD | Confirmé |
| Connectivité | WiFi 2.4 GHz + BLE (via [[ESP32-S3]]) | Confirmé |

---

## Ce que le fabricant ne divulgue pas

- Modèle précis des microphones MEMS
- Référence exacte du module GPS
- Schéma électronique ou BOM (Bill of Materials)
- Version exacte du module [[ESP32-S3]] utilisé (WROOM-1, MINI, ou module custom)

Scribe Labs (California) ne publie pas de schéma hardware — produit [[commercial]] fermé.

---

## Références

- [BirdWeather — Page officielle](https://www.birdweather.com/)
- [BirdWeather Shop — spécifications](https://www.birdweather.com/shop-birdweather-puc)
- [BirdWeather FAQ](https://www.birdweather.com/faqs)
- [Voltaic Systems — mesure consommation](https://blog.voltaicsystems.com/solar-for-birdweather-bioacoustic-platform/)
- [Oberon Citizen Science — revue](https://oberon-citizen.science/posts/2024-07-21-PUC-review/)
