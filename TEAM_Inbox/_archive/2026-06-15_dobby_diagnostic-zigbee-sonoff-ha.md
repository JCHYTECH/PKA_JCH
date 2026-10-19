# Prompt — Diagnostic Zigbee Sonoff ZBDongle-P V2 × Home Assistant Docker (macOS)

## Objectif

Intégrer un dongle Zigbee **Sonoff Zigbee 3.0 USB Dongle Plus V2** (ZBDongle-P V2, ITead, puce Silicon Labs EFR32MG21) dans **Home Assistant** tournant dans un **container Docker Desktop sur macOS** (M5, Apple Silicon).

## Matériel

- **Dongle** : Sonoff ZBDongle-P V2 — idVendor=0x10C4, idProduct=0xEA60, bcdDevice=256
- **Détecté macOS** : `/dev/tty.usbserial-110` (et `/dev/cu.usbserial-110`)
- **Container** : `ghcr.io/home-assistant/home-assistant:stable` dans Docker Desktop
- **OS hôte** : macOS (Apple Silicon), Python 3.13

## Problème

L'intégration ZHA dans Home Assistant n'arrive pas à se connecter au dongle. L'erreur dans l'UI HA : « Unknown error occurred » puis « Aucun objet disponible ». Dans les logs Docker :

```
ERROR (MainThread) [aiohttp.server] Error handling request
  File "zha/config_flow.py", line 201, in async_step_choose_serial_port
  File "zha/radio_manager.py", line 262, in detect_radio_type
  File "bellows/zigbee/application.py", line 614, in disconnect
  File "bellows/ezsp/__init__.py", line 224, in disconnect
TypeError: 'NoneType' object can't be awaited
```

## Ce qui a été fait

### 1. Docker → accès direct au port série
Docker Desktop macOS n'a pas d'accès direct aux périphériques série (`--device` ne fonctionne pas).
→ Solution : bridge TCP avec `socat`.

### 2. Bridge socat
```bash
socat TCP-LISTEN:6638,reuseaddr,fork FILE:/dev/tty.usbserial-110,b57600,raw,echo=0
```
- Test socket Python depuis le container : connexion TCP OK vers `host.docker.internal:6638`
- DNS `host.docker.internal` résolu correctement depuis le container (192.168.65.7)

### 3. Découverte du baud rate
- Le dongle ne répond pas à 115200 baud (testé avec pyserial directement sur le port série macOS)
- À **57600 baud**, le dongle répond : 3 bytes (`9a 08 9d`). C'est probablement une trame EZSP valide.
- Testé aussi : 230400, 460800, 38400 — aucune réponse.

### 4. Dans Home Assistant (http://localhost:8123)
- Paramètres → Appareils & services → Ajouter une intégration → ZHA
- Port série saisi manuellement : `socket://host.docker.internal:6638`
- Type d'adaptateur : EZSP
- Tentative avec auto-détection → échec (TypeError dans bellows)
- Tentative manuelle 57600/8/N/1 → échec

### 5. Cache HA
- Aucune entrée ZHA dans `.storage/core.config_entries`
- Le dossier `.storage/` ne contient pas de config ZHA résiduelle

### 6. État actuel
- Le bridge socat tourne et est joignable depuis le container
- Le dongle répond physiquement à 57600 baud
- ZHA refuse de s'initialiser avec le socket TCP

## Questions pour le diagnostic

1. **Est-ce que ZHA/bellows supporte les connexions `socket://` ?** Ou faut-il nécessairement un périphérique `/dev/` local ? La doc ZHA mentionne `socket://` mais pour les adaptateurs réseau (ex: Zigbee2MQTT), pas pour les dongles USB via TCP.

2. **Le firmware du ZBDongle-P V2 est-il compatible EZSP ?** Certains dongles Sonoff sont livrés avec un firmware routeur ou bootloader. Faut-il flasher un firmware coordinateur spécifique pour ZHA (ex: EmberZNet NCP) ?

3. **Alternative zigbee2mqtt** — Serait-ce plus compatible avec un bridge TCP ? zigbee2mqtt supporte `adapter: ezsp` et peut se connecter via `port: tcp://host.docker.internal:6638`.

4. **Le baud rate de 57600 est-il définitif ?** Le ZBDongle-P V2 avec EFR32 utilise souvent 115200 ou 230400. Est-ce que la réponse à 57600 suggère un firmware non-standard ou un bootloader ?

## Fichiers

- Script d'installation : `_local/install-zigbee-ha.sh`
- Config HA : `_local/homeassistant/`
- Guide : `docs/manuels/sonoff-zigbee-ha-guide.md`
