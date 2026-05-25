# ADR-004 — Stockage local P0

**Date :** 2026-05-23  
**Statut :** accepté  
**Owner PKA :** Castor + Forge  
**Agent WildNexus :** `wildnexus-firmware-ulp`  
**Jalon :** M-01 Architecture P0 gelée

## Contexte

Le Satellite Lite P0 doit conserver les données natives localement. LoRa ne transporte pas les images, l'audio ou les flux lourds.

## Décision

Retenir une **microSD industrielle 8 à 16 GB** comme stockage local P0.

Le stockage contient :

- images ou séquences image déclenchées ;
- clips audio courts issus du micro mono P0 ;
- journal événementiel append-only ;
- métadonnées : horodatage, état batterie, type d'événement, score simple, statut transmission.

La récupération se fait par retrait de carte ou Wi-Fi local de maintenance. Aucun upload cloud automatique n'est requis en P0.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| microSD industrielle | capacité suffisante, simple, remplaçable | risque corruption si coupure mal gérée | retenu |
| flash SPI | robuste, intégrée | capacité trop faible pour images/audio | rejeté |
| cloud / LTE direct | accès distant | hors P0, consommation et coût | P1 |

## Conséquences

- Firmware : écriture atomique, index append-only, flush propre avant retour sommeil.
- Hardware : alimentation microSD coupée par MOSFET quand inactive.
- Validation : test de cycles écriture/coupure sur banc.

## Critère de révision

Réviser si la microSD provoque des corruptions répétées malgré écriture atomique et séquence d'arrêt propre.
