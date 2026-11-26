---
name: iot-vanlife
description: Orchestrer l'installation, la configuration et le dépannage de la domotique du van Lupo (Home Assistant, Zigbee2MQTT, Mosquitto, RPi 5, OBD/CAN). Déclencher sur "iot van", "home assistant", "HA lupo", "zigbee", "domotique van", "rpi lupo", "flash haos".
---

# Skill — iot-vanlife

## Déclencheurs
- « iot van », « domotique van », « home assistant », « HA lupo »
- « zigbee », « mosquitto », « sonoff », « capteur aqara »
- « flash haos », « réactivation iot », « rpi lupo », « obd », « can bus », « wican »
- Toute intervention matérielle ou logicielle sur la domotique du van.

## RÈGLE MULTI-TERMINAL (non négociable)
Toute commande est préfixée par la machine cible : **[M5]** (Mac), **[RPi]** (Lupo), **[M1]** (serveur LLM). Sans préfixe, la commande est incomplète.

## Documents canoniques (lire avant d'agir)
- **Guide maître :** `JCH_Inbox/03_PROJECTS/11_IOT/guide installation HA/guide-installation-ha-vanlife-lupo.md` (285 lignes — architecture matérielle + pile logicielle + config).
- **Réactivation :** `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/PROCEDURE-REACTIVATION-IOT-VAN-2026-10-01.md` (phases 0→6, deadline 01/11/2026).
- **ADRs :** `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/adr/` (ADR-001 alimentation, 002 zigbee, 003 nvme, 004 pir, 005 hardware, 006 obd/can).
- **CAN/OBD :** `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/specs/SPEC-CAN-BUS.md`, `.../securite/obd/`, `.../ds300-tap/`.
- **État matériel :** `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md`.
- **Thread projet :** `JCH_Inbox/03_PROJECTS/11_IOT/thread-iot.md`.

## État de référence (invariants)
- **Unité centrale :** RPi 5 (4 Go), boîtier Geekworm **X1201-C1**, UPS **X1205** (2×18650), ventilateur Noctua NF-A4x10.
- **Stockage :** microSD **Samsung PRO Endurance 256 Go** seule. **NVMe retiré** (bug boot #4785/#5005 corrigé en HAOS 18.3, mais pogo pins instables → SD seule).
- **HAOS 18.3** — **auto-update TOUJOURS désactivé** (le bug revient à chaque montée de version non maîtrisée).
- **Zigbee :** coordinateur Sonoff ZBDongle-E (EmberZNet, canal 15) → Zigbee2MQTT v5 → Mosquitto `:1883`. 8 capteurs d'ouverture Aqara MCCGQ11LM.
- **OBD/CAN :** WiCAN Pro (HS-CAN + MS-CAN, 17+ entités), validé avec Exosfer OBD Protect.
- **Cellule électrique :** « DS300 Tap » (CBE DS300) — tensions batteries, signal D+, shore power, niveaux eaux.
- **Accès distant :** maillage Tailscale (supervision iPhone sans IP fixe).
- **Deadline installation physique :** 1er novembre 2026.

## Procédure type

### Flash / réinstallation (si boot bloqué)
1. Suivre `PROCEDURE-REACTIVATION-IOT-VAN-2026-10-01.md` phase par phase.
2. **Retirer tous les autres disques** avant flash. **SHA256 obligatoire** après chaque flash.
3. Premier boot → **désactiver l'auto-update** → hostname `lupo` → statut « Healthy ».

### Ajout capteur / entité
1. Identifier le bus (Zigbee, OBD/CAN, DS300, VE.Direct, BLE).
2. Documenter l'entité (`sensor.*`, `binary_sensor.*`) dans le guide maître.
3. Valider le nommage MQTT + tester hors réseau avant installation van.

### Dépannage
- Boot gelé / SQUASHFS → reflash HAOS 18.3 SD seule (voir procédure).
- Perte SSH/Tailscale → vérifier l'UPS X1205 + l'alim 5V/5A.
- Capteur muet → vérifier Zigbee2MQTT pairing (canal 15) puis Mosquitto.

## Règles
- **Auto-update HAOS : jamais.** C'est la cause du blocage de septembre.
- **SD seule pour le van** (NVMe = data disk optionnel).
- **SHA256** avant tout flash.
- Toute intervention physique → mettre à jour `hardware-state.md` + `thread-iot.md`.
- Respecter les ADRs existants ; pour une décision hardware nouvelle → ouvrir/valider un ADR.
