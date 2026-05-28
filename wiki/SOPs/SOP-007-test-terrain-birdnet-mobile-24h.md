---
type: sop
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - [[BirdNET]]
  - terrain
  - bioacoustique
  - raspberry-pi
owner: "[[Chouette]]"
project: WILDNEXUS
---

# SOP-007 — Test terrain BirdNET-Go mobile 24 h

## Objectif

Tester un [[Raspberry Pi 5]] avec [[BirdNET-Go]], micro BOYA BY-MM1, powerbank Anker 72.36 Wh et connexion iPhone/LTE sur un site riche en oiseaux pendant une periode cible de 24 h.

## Procedure courte

1. Valider BirdNET-Go sur le reseau maison.
2. Valider audio BOYA BY-MM1 via adaptateur USB.
3. Valider hotspot iPhone ou modem LTE.
4. Faire un test maison 2 h sur powerbank.
5. Installer le systeme sur site hors pluie directe, micro eloigne du ventilateur.
6. Noter heure de debut, reseau, batterie, meteo, orientation micro.
7. Controler si possible a T+30 min, T+2 h, T+6 h, T+12 h, T+24 h.
8. Recuperer logs, detections, autonomie reelle et incidents.

## Reference detaillee

Voir le protocole complet :

[[2026-05-26_protocole-terrain-24h-rpi-birdnet-mobile]]

## Critere de reussite

Reussite complete si 24 h de fonctionnement, audio stable, BirdNET-Go actif, donnees exploitables et absence de reboot non desire.

Reussite partielle si autonomie inferieure a 24 h mais cause identifiable et donnees exploitables.
