# ADR-003 — Choix radio / LPWAN P0

**Date :** 2026-05-18
**Statut :** accepté — 2026-05-18
**Owner PKA :** [[Forge]] + [[Chouette]]
**Agent WildNexus :** `wildnexus-rf-propagation`
**Jalon :** M-01 Architecture P0 gelée

## Contexte

P0 transmet des événements, métadonnées et états de santé depuis des nœuds en forêt belge vers un point de collecte. Il ne transmet pas d'images en temps réel — la bande passante [[LoRa]] le rend physiquement impossible (une image 5 MP représente 3–5 Mo, soit plusieurs heures de transmission et un dépassement massif du duty cycle réglementaire).

La contrainte réglementaire EU868 impose un duty cycle de 1 % sur les canaux principaux : à SF12, le nœud ne peut émettre que ~12 événements/heure avant saturation. L'architecture doit en tenir compte.

Une exigence terrain a été identifiée : permettre à l'utilisateur de télécharger une image spécifique à la demande, après avoir vu les métadonnées [[LoRa]] d'un événement jugé intéressant.

## Décision

### Radio principale : [[LoRa]] EU868 P2P — SX1262

Retenir **[[LoRa]] EU868 bidirectionnel point-à-point** comme radio principale P0.

- Pas de LoRaWAN, pas de TTN — infrastructure propre, zéro dépendance externe.
- Module retenu : **RAK3172** (SX1262, CE certifié, UART/SPI) ou **Murata Type 1SJ** en alternative.
- Interface [[ESP32-S3]] : SPI + GPIO interrupt — librairie RadioLib.
- **Adaptive data rate** : SF7 par défaut (portée ~500 m–1 km forêt, duty cycle confortable), SF12 uniquement si RSSI dégradé (portée ~2–3 km, ~12 événements/heure max réglementaire).

**Flux uplink (nœud → gateway) :**
Paquet événement ~50 octets : horodatage | ID nœud | score IA | état batterie | RSSI/SNR | compteur stockage.

**Flux downlink (gateway → nœud) :**
Commande ~10 octets : type commande | timestamp image cible | paramètres.
Utilisé pour déclencher le téléchargement image via cellulaire (voir ci-dessous).

**Gateway P0 :** second [[ESP32-S3]] + SX1262 breakout (~25 €) connecté au réseau local JCH — reçoit les paquets [[LoRa]] et les pousse vers le dashboard PKA.

### Radio secondaire : LTE-M on-demand — SIM7080G + SIM 1NCE

Retenir une **architecture hybride [[LoRa]] + LTE-M** pour le téléchargement d'images à la demande.

Le modem cellulaire est **éteint en permanence**. Il ne s'active que sur commande [[LoRa]] downlink explicite de l'utilisateur.

| Étape | Action |
|-------|--------|
| 1 | Animal déclenche — [[ESP32-S3]] capture + stocke image sur microSD |
| 2 | [[LoRa]] TX uplink → métadonnées événement vers dashboard |
| 3 | JCH voit l'événement, juge l'image utile |
| 4 | Dashboard envoie commande [[LoRa]] downlink : "upload image timestamp X" |
| 5 | [[ESP32-S3]] réveille SIM7080G via UART |
| 6 | LTE-M upload image vers endpoint cloud PKA |
| 7 | SIM7080G retourne en deep sleep |

**Modem :** Quectel SIM7080G (NB-IoT + LTE-M, UART, ~15 €)
**SIM :** 1NCE — 10 € one-shot, 10 ans, 500 Mo, 250 SMS — couvre ~500 images sur durée de vie SIM.
**Couverture Belgique :** Proximus LTE-M — nationale y compris zones rurales. Antenne externe obligatoire sous canopée dense.

**Consommation modem :**
- Deep sleep : ~10 µA — négligeable sur budget ADR-005
- Upload image 3 MP (~1 Mo) : ~400 mA pendant ~30 s = ~3.3 mAh par image — ponctuel, sans impact autonomie 60 jours

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| [[LoRa]] EU868 P2P seul | Simplicité maximale firmware, un seul stack radio | Pas d'accès images terrain sans déplacement | **Retenu P0 — décision JCH 2026-05-18** |
| [[LoRa]] EU868 P2P + LTE-M on-demand | Image à la demande, modem éteint 99.9% | Firmware deux radios, complexité stack P0 non justifiée | **P1** — architecture validée, implémentation différée |
| LoRaWAN TTN | Zéro infrastructure gateway | Dépendance réseau tiers, downlink limité TTN, complexité stack | Écarté — *dépendance externe* |
| NB-IoT / LTE-M seul | Couverture nationale, débit image | Abonnement mensuel, consommation veille, pas adapté événementiel forêt | Écarté — *coût récurrent + consommation* |
| Sigfox | Très bas coût, longue portée | Réseau en déclin, downlink très limité | Écarté — *pérennité* |
| [[LoRa]] mesh | Résilience apparente | Duty-cycle, collisions, consommation relayage | Écarté P0 — *complexité* |
| WiFi natif [[ESP32-S3]] | Zéro coût, natif | Portée 50–100 m — insuffisant forêt | Écarté — *range* |

## Sources primaires consultées

- Semtech SX1262 datasheet : https://www.semtech.com/products/wireless-rf/lora-connect/sx1262
- RAK3172 datasheet : https://docs.rakwireless.com/product-categories/wisduo/rak3172-module/datasheet/
- Quectel SIM7080G datasheet : https://www.quectel.com/product/lpwa-sim7080g
- 1NCE IoT SIM : https://1nce.com
- ETSI EN 300 220 — duty cycle EU868 : https://www.etsi.org/deliver/etsi_en/300200_300299/300220/
- RadioLib [[ESP32]] : https://github.com/jgromes/RadioLib

## Conséquences

- WP02 (hardware) intègre **une seule interface radio P0** : SPI pour SX1262. Footprint SIM7080G réservé sur PCB P1 si pertinent.
- WP03 (firmware) implémente le stack [[LoRa]] P2P uniquement — machine d'états uplink événement + downlink commande simple.
- Le duty cycle EU868 doit être calculé et documenté pour le scénario de déploiement EVT belge avant M-02.
- La gateway P0 = [[ESP32-S3]] + SX1262 breakout (~25 €) — à inclure dans le budget supply register.
- ADR-006 (boîtier) : un seul presse-étoupe antenne [[LoRa]] P0. Second presse-étoupe LTE-M prévu mécaniquement pour P1.

## Tests obligatoires avant acceptation M-02

| Test | Critère minimal |
|------|----------------|
| Portée [[LoRa]] terrain forêt belge SF7 | RSSI/SNR documenté à 500 m, 1 km, 2 km |
| Paquet uplink événement | transmission fiable après réveil, retour sleep confirmé |
| Duty cycle EU868 | calcul documenté pour scénario 5 événements/heure SF9 |
| Commande downlink reçue | nœud reçoit et interprète commande en < 5 s après émission gateway |
| Antenne [[LoRa]] boîtier IP67 | perte acceptable avec montage final |

## Critère de révision

Réviser cette ADR si :

- la couverture LTE-M Proximus est insuffisante sur le site EVT retenu ;
- le duty cycle EU868 bloque le volume d'événements réel terrain ;
- le SIM7080G ne peut pas atteindre < 50 µA en deep sleep sur la carte P0 ;
- la gateway P2P s'avère trop complexe à déployer terrain et LoRaWAN TTN devient préférable.
