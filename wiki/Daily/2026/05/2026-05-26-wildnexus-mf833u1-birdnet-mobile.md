---
date: 2026-05-26
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-26 — wildnexus-mf833u1-birdnet-mobile

## Session — 13:29 — wildnexus-mf833u1-birdnet-mobile

### Contexte
- Modèle : codex-gpt-5
- Projet : WILDNEXUS

### Résumé
Correction du cadrage du modem MF833U1 : il sera utilise avec [[Raspberry Pi]] + BirdNET-Go en configuration mobile.

### Actions
- Mise a jour de la note MF833U1 LTE pour usage RPI + [[BirdNET]] mobile.\n- Creation de la note bioacoustique hardware 2026-05-26_birdnet-rpi-mobile-lte-mf833u1.md.\n- Correction du registre composants : MF833U1 = modem USB LTE [[BirdNET]] mobile.\n- Ajout des points de vigilance alimentation, coexistence audio USB, reboot, perte/reprise reseau.

### Décisions
Le MF833U1 devient un composant du banc BirdNET-Go mobile avec [[Raspberry Pi]]. Il reste hors architecture Satellite Lite P0.

### Prochaines étapes
Brancher le modem au [[Raspberry Pi]], relever lsusb/ip addr/nmcli/dmesg, verifier SIM/APN, route Internet, stabilite BirdNET-Go et alimentation avec audio USB.
