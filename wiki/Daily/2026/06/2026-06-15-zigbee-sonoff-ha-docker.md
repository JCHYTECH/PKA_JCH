---
date: 2026-06-15
tags: [daily, IoT, zigbee, home-assistant, docker]
type: daily
status: active
---

# 2026-06-15 — Intégration Zigbee Sonoff ZBDongle-P V2 × HA Docker

## Actions

- Lancement session [[Dobby]] — modèle `claude-sonnet-4-6`, inbox 6 éléments
- Utilisation `/modele` pour sélectionner le bon LLM sur la tâche diagnostic Zigbee
- Mémoire M1 créée : inventaire modèles Ollama sur `m1-llm` (Tailscale `100.73.212.110`)
- Diagnostic soumis à `claude-opus-4-7` (Fast mode) — réponse en 67s
- Opus identifie (partiellement) la cause : mauvais baud rate (57600 → 115200)
- Confirmation firmware : probe ASH cancel+RST sur `/dev/cu.usbserial-10` → RSTACK `1ac1020b0a527e` → **EFR32MG21 / EZSP confirmé à 115200**
- Remplacement socat (défaillant sur macOS pour serial) par bridge Python (`_local/serial_bridge.py`)
- Test depuis container Docker : ASH RSTACK reçu → canal validé
- ZHA configuré en mode avancé : EZSP, `socket://host.docker.internal:6638`, 115200
- Dongle Sonoff reconnu par HA — réseau Zigbee créé avec succès
- Bridge pérennisé via launchd : `com.pka.zigbee-bridge` — redémarre au boot M5

## Décisions

- **socat abandonné** : ne gère pas correctement les ports série sur macOS (bidirectionnel bloquant) → bridge Python pyserial
- **EZSP confirmé** (et non ZNP comme suggéré par Opus) : la réponse `9a 08 9d` à 57600 était un RSTACK EFR32 vu à demi-débit
- **cu. plutôt que tty.** : évite le blocage sur carrier detect macOS
- **launchd + venv PKA** : le python système n'a pas pyserial → utiliser `/Users/jchavauxm5/PKA_JCH/.venv/bin/python3`

## Prochaine étape

- Appairer les premiers appareils Zigbee dans HA
- Vérifier que le bridge survit à un redémarrage M5 (tester launchd au prochain boot)
- Documenter la procédure complète dans `docs/manuels/sonoff-zigbee-ha-guide.md`

## Voir aussi

- [[Forge]] — bridge TCP/série
- `_local/serial_bridge.py` — bridge Python actif
- `_local/zigbee-bridge.log` — log du bridge
- `com.pka.zigbee-bridge` — launchd plist dans `~/Library/LaunchAgents/`
