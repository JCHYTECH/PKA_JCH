---
type: hardware-note
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - wildnexus
  - lte
  - modem
  - [[BirdNET]]
  - raspberry-pi
  - mobile
owner: "[[Forge]]"
project: "[[WILDNEXUS]]"
---

# MF833U1 LTE USB Modem — reception et usage RPI + [[BirdNET]] mobile

## Fait

JCH a recu le modem USB LTE **MF833U1** le 2026-05-26.

## Cadrage P0

Ce composant est classe comme **connectivite mobile pour [[Raspberry Pi]] + BirdNET-Go**, pas comme composant Satellite Lite P0.

Raison :

- le Satellite Lite P0 reste cadre par [[ADR-009-architecture-satellite-base-cloud]] ;
- le P0 satellite ne depend pas d'un acces LTE ;
- la connectivite P0 satellite reste locale, frugale et orientee [[LoRa]]/statuts/metadonnees ;
- le modem LTE sert ici a donner une connectivite terrain mobile au [[Raspberry Pi 5]] executant [[BirdNET-Go]].

## Usage vise

| Usage | Statut |
|---|---|
| Connectivite mobile [[Raspberry Pi]] + BirdNET-Go | usage cible |
| Upload ponctuel observations / logs / alertes | a valider |
| Acces distant ponctuel pour monitoring BirdNET-Go | a valider |
| Backhaul LTE pour Base/Master Nexus | reutilisable P1 |
| Integration dans Satellite Lite P0 | non retenu |

## Prochaine verification

Brancher le modem sur la machine de test et relever :

```bash
system_profiler SPUSBDataType
```

Sur Linux / [[Raspberry Pi]] :

```bash
lsusb
ip addr
nmcli device
dmesg | tail -80
```

Points a confirmer :

- mode expose par le modem : interface reseau USB, modem serie, RNDIS/ECM, PPP, QMI ou MBIM ;
- besoin ou non d'une page web locale d'administration ;
- compatibilite carte SIM et APN ;
- stabilite apres reboot ;
- consommation USB en usage connecte ;
- qualite reception sur site terrain.
- coexistence avec audio USB si micro ou carte son USB sont aussi branches ;
- comportement BirdNET-Go quand la connexion tombe puis revient.

## Decision

Le MF833U1 est accepte comme connectivite mobile pour le banc [[Raspberry Pi 5]] + [[BirdNET-Go]]. Il ne modifie pas le scope Satellite Lite P0.

## Décision SIM

**SIM retenue : Proximus Pay&GO+**

- Usage : BE + roaming EU (FR, NL, LU, DE, IT et tout pays EU) — Roam Like At Home
- Volume : < 100 MB / session terrain
- Réseau : Proximus (meilleure couverture rurale BE)
- Prix : €5 (promo jusqu'au 02/08/2026) avec €10 crédit + 3 GB inclus
- Recharge data : €6 / 500 MB ou €12 / 3 GB
- APN : `internet.proximus.be`
- À acheter : boutique Proximus locale
- Date décision : 2026-05-26
