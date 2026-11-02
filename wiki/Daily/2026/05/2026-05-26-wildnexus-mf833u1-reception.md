---
date: 2026-05-26
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-26 — wildnexus-mf833u1-reception

## Session — 13:28 — wildnexus-mf833u1-reception

### Contexte
- Modèle : codex-gpt-5
- Projet : WILDNEXUS

### Résumé
JCH a reçu le modem USB LTE MF833U1 pour WildNexus. L'élément est cadré comme outil de banc/Base Nexus/backhaul terrain, sans modification du scope Satellite Lite P0.

### Actions
- Création de la note connectivité 2026-05-26_mf833u1-lte-usb-modem-reception.md.\n- Ajout d'une ligne MF833U1 reçu 2026-05-26 dans WILDNEXUS_SUPPLY_REGISTER.md.\n- Cadrage explicite : usage Base/Master Nexus ou [[Raspberry Pi]] terrain, pas satellite P0.

### Décisions
Le MF833U1 est accepté comme outil de test connectivité WildNexus mais ne modifie pas ADR-009 ni le scope P0.

### Prochaines étapes
Brancher le modem et relever system_profiler SPUSBDataType sur macOS, ou lsusb/ip addr/nmcli/dmesg sur Linux/[[Raspberry Pi]]. Confirmer mode USB, SIM/APN, stabilité reboot et consommation.
