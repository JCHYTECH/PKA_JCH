# ADR-002 — Choix protocole capteurs : Zigbee vs Z-Wave vs BLE

**Date :** 2026-06-04
**Statut :** proposé
**Owner PKA :** [[Forge]]
**Jalon :** Phase 1 — Setup base

## Contexte

Le van nécessite des capteurs sans fil pour : température cellule (×2), température frigo (×2), ouverture portes (×5), et futurs capteurs (fuite eau, CO₂, mouvement).

Trois protocoles domotiques grand public sont candidats : Zigbee (IEEE 802.15.4), Z-Wave (propriétaire ITU-T G.9959), et Bluetooth BLE.

Contrainte forte : l'émetteur/récepteur doit être compatible RPi 5 et Home Assistant OS sans matériel supplémentaire coûteux.

## Décision

**Retenir Zigbee (via clé USB Sonoff ZBDongle-E + integrateur Zigbee2MQTT),** avec les Sonoff SNZB-02 pour température et Aqara MCCGQ11LM pour ouverture de porte.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| **Zigbee** | Large choix capteurs ; prix bas ; protocole ouvert ; ZBDongle-E reconnu HA ; portée suffisante van (~10 m) | Interférence possible avec Wi-Fi 2.4 GHz (canal Zigbee à choisir) | **Retenu** |
| Z-Wave | Bande 868 MHz, pas d'interférence Wi-Fi ; très fiable | Matériel plus cher (+30-50%) ; moins de choix capteurs ; dongle Z-Wave plus rare | Écarté — coût |
| BLE (Bluetooth) | Intégration HA native ; pas de dongle (RPi 5 a BT intégré) | Portée limitée (~5 m à travers cloisons van) ; fiabilité aléatoire sur route ; pas de répéteur standard | Écarté — fiabilité |
| Thread/Matter | Protocole moderne, prometteur | Encore jeune ; peu de capteurs vanlife ; matériel plus cher | Écarté — maturité |

## Conséquences

- ✅ Clé USB Sonoff ZBDongle-E : ~20 €, plug & play avec HA + Zigbee2MQTT
- ✅ Capteurs température Sonoff SNZB-02 : ~8 € pièce, piles CR2030, autonomie annoncée 2 ans
- ✅ Capteurs porte Aqara MCCGQ11LM : ~8 € pièce, piles CR1632
- ✅ Zigbee mesh : si un capteur est trop loin, un répéteur Sonoff S31 (prise connectée) étend le réseau
- ⚠️ Zigbee utilise le canal 2.4 GHz — risque d'interférence avec le Wi-Fi AP du RPi si mal configuré
- ⚠️ Mitigation : configurer Zigbee sur canal 15-20 et Wi-Fi sur canal 1 ou 11 (canaux non chevauchants)
- ⚠️ Pas de capteur porte Zigbee dans le van initialement envisagé — confirmer compatibilité Aqara avec Zigbee2MQTT

## Critère de révision

Si plus de 2 capteurs par mois perdent la connexion, ajouter un répéteur Zigbee (Sonoff S31) dans le van. Si interférence Wi-Fi persistante, migrer vers Z-Wave en Phase 4.
