# Mandat [[Furet]] — Recherche profil Spécialiste IoT

**Demandeur :** [[Dobby]] 🦉
**Date :** 2026-06-06
**Urgence :** Normale
**Projets couverts :** `11_IOT` (van + maison) + `03_WILDNEXUS`

## Contexte

JCH souhaite recruter un spécialiste IoT transverse. Le besoin couvre :

- **IoT van** — Stylevan Equinox IV : RPi 5 + Home Assistant, capteurs Zigbee, solaire Victron, réseau LTE/Tailscale
- **IoT maison** — Maison off-grid 60 m² : domotique Home Assistant, énergie, capteurs environnementaux
- **WildNexus** — RPi 5 + ESP32-S3, LoRa mesh, caméras-pièges, capteurs PIR/bioacoustique, low-power

Ces trois domaines partagent la même pile : **RPi, ESP32, Home Assistant, Tailscale, capteurs basse consommation, énergie embarquée**.

## Profil cible recherché

Le spécialiste IoT doit couvrir :

| Domaine | Compétences attendues |
|---------|-----------------------|
| **Firmware embarqué** | ESP32 (Arduino/ESP-IDF), RPi GPIO, I²C/SPI/UART, low-power design |
| **Réseaux sans fil** | LoRa / LoRaWAN, Wi-Fi mesh, LTE/4G, Tailscale/WireGuard, Zigbee/Z-Wave |
| **Domotique** | Home Assistant OS, intégrations HACS, automations YAML, dashboards |
| **Énergie** | Solaire (Victron MPPT/VE.Direct), batteries LiFePO₄, BMS, monitoring |
| **Capteurs** | PIR (EKMB), température/humidité (BME688), caméra (OV5640), GPS (u-blox) |
| **Système** | Linux embarqué (RPi OS, Alpine), Docker léger, SSH, cron, logging |
| **Sécurité** | VPN/Tailscale, isolation réseau, chiffrement, mises à jour OTA |

## Stack technique (stack commune aux 3 projets)

- RPi 5 / RPi Zero 2W
- ESP32-S3
- Home Assistant OS
- Protocoles : LoRa, Wi-Fi, BLE, Zigbee
- Victron Venus OS / VE.Direct
- Tailscale / WireGuard
- Modem LTE (sixfab / Waveshare)
- Capteurs : EKMB, BME688, OV5640, GPS u-blox, batterie monitoring

## Livrable attendu

1. **Fiche profil** — compétences, profondeur attendue, stack maitrisée, expérience souhaitée
2. **Proposition d'animal/nom** — cohérent avec l'équipe PKA
3. **Périmètre responsabilités** — ce que le spécialiste prend en charge vs ce qui reste à [[Forge]]/autres
4. **Frontières** — où s'arrête son domaine (ex. : ne fait pas le génie civil de la maison off-grid)

## Références

- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/` — architecture WildNexus
- `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/` — projet IoT van
- `JCH_Inbox/03_PROJECTS/11_IOT/iot-home/` — projet IoT maison (à créer)
- `_local/homeassistant/` — config Home Assistant actuelle
- `TEAM/forge.md` — pour le boundary avec [[Forge]]
