# Brief — Schéma architecture réseau Vanlife IOT

**Destinataire :** [[Vega]] 🦚 — Directrice Créative
**Mandaté par :** [[Dobby]] 🦉
**Date :** 2026-06-07

## Contexte

Le projet Vanlife IOT (Stylevan Equinox 4) a besoin d'un schéma d'architecture réseau.

## Élément à illustrer

**Titre :** Architecture réseau Vanlife IOT — Stylevan Equinox 4

**Composants :**

1. **RPi 5** (Home Assistant OS) avec :
   - Sonoff ZBDongle-E (USB) — hub Zigbee
   - Wi-Fi AP intégré — SSID "VanLife_Network"

2. **Réseau Zigbee** (via dongle) :
   - Aqara MCCGQ11LM ×5 (portes/hayon)
   - Sonoff SNZB-04P ×2 (toit relevable, frigo)
   - Sonoff SNZB-02P (T°/HR cellule)
   - Sonoff SNZB-02D (T° frigo LCD)
   - PIR extérieur → SNZB-04 (contact sec)

3. **Réseau Wi-Fi** (VanLife_Network) :
   - ESP32-S3 pack (dB + inclinaison + eau)
   - ESP32 proxy BLE → Mopeka gaz
   - iPhone/iPad (dashboard Lovelace, Siri)

4. **Réseau BLE** :
   - Mopeka Pro Check (niveau gaz)

## Contraintes

- Format SVG (PNG fallback) + source
- Lisible NB + couleur
- 3 protocoles distingués visuellement (Zigbee / Wi-Fi / BLE)
- Design system PKA
- Budget ~185 € visible si pertinent

## Livrable

1 fichier image + fichier source (draw.io / Figma / Illustrator)
Dépôt : `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/`
