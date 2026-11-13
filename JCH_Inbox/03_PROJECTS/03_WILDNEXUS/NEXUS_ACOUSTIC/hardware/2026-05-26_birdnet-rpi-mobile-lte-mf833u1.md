---
type: hardware-note
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - [[BirdNET]]
  - raspberry-pi
  - lte
  - mobile
owner: "[[Chouette]]"
project: "[[WILDNEXUS]]"
---

# BirdNET-Go mobile — [[Raspberry Pi]] + MF833U1 LTE

## Fait

Le modem USB LTE **MF833U1** sera utilise avec le [[Raspberry Pi 5]] + [[BirdNET-Go]] en configuration mobile.

## Role

Le modem apporte une connectivite terrain au banc BirdNET-Go :

- monitoring distant ponctuel ;
- upload de logs ou observations ;
- acces de maintenance hors Wi-Fi local ;
- tests de comportement en environnement mobile.

## Architecture cible V1

```text
Micro / carte son USB
        -> Raspberry Pi 5
        -> BirdNET-Go
        -> MF833U1 LTE USB
        -> reseau mobile
```

## Points de vigilance

- Le [[Raspberry Pi]] doit pouvoir alimenter simultanement le modem LTE et l'audio USB.
- Le modem LTE peut consommer par pics ; prevoir alimentation stable.
- Verifier que l'interface audio reste stable quand le modem se connecte/deconnecte.
- Tester le reboot automatique avec modem deja branche.
- Tester perte/reprise reseau sans bloquer BirdNET-Go.
- Eviter de confondre ce banc mobile [[BirdNET]] avec le Satellite Lite P0.

## Checklist de test

Sur [[Raspberry Pi]] :

```bash
lsusb
ip addr
nmcli device
dmesg | tail -80
```

Verifier ensuite :

- interface reseau creee ;
- acces Internet ;
- resolution DNS ;
- route par defaut ;
- acces interface BirdNET-Go depuis le reseau si necessaire ;
- logs BirdNET-Go pendant connexion/deconnexion LTE ;
- temperature et alimentation apres 30 minutes.

## Decision

Le MF833U1 devient un composant du banc **BirdNET-Go mobile**. Il reste hors architecture Satellite Lite P0.
