# WildNexus — Revue produit Meshnology N35 / [[ESP32]] [[LoRa]] V3-V4

**Date :** 2026-05-18  
**Demande JCH :** décortiquer le produit Amazon `B0GQ3L822F` et vérifier son adéquation aux critères WildNexus.  
**Produit identifié :** Meshnology N35 [[ESP32]] [[LoRa]] V3/V4 Meshtastic Device / Heltec WiFi [[LoRa]] 32 V4 selon les pages constructeur.  
**Statut :** analyse préliminaire — Amazon inaccessible hors navigateur authentifié / captcha.

## Verdict court

**Intéressant comme carte de test [[LoRa]] / gateway P0, pas comme nœud caméra WildNexus P0.**

La variante **V4** est la seule réellement intéressante : ESP32-S3R2, SX1262, 2 MB PSRAM, 16 MB flash, entrée solaire, interface GNSS, gestion batterie améliorée, consommation annoncée < 20 µA. Elle peut accélérer les essais RF [[LoRa]] EU868, Meshtastic/[[LoRa]] P2P, gateway locale et banc de consommation.

Elle ne remplace pas le design du nœud caméra : pas de caméra OV5640 M12 DVP intégrée, pas de lentille IR-corrigée, pas de LEDs IR pilotées, pas de microSD documentée, pas de LTE-M SIM7080G, batterie Li-ion 3000 mAh au lieu de LiFePO4, boîtier non IP67, OLED et fonctions HMI superflues pour autonomie terrain.

## Données produit relevées

Sources consultées :

- Meshnology N35 : https://meshnology.com/collections/meshnology-n30/products/n35-esp32-lora-v3-board-kit-863-928mhz-antenna-3000mah-battery-case-wifi-bluetooth-oled-for-arduino-meshtastic-iot
- Heltec WiFi [[LoRa]] 32 V4 : https://heltec.org/project/wifi-lora-32-v4/
- Heltec docs WiFi [[LoRa]] 32 : https://docs.heltec.org/en/node/[[ESP32]]/wifi_lora_32/

Points V4 utiles :

| Élément | Donnée relevée | Intérêt WildNexus |
|---|---|---|
| MCU | ESP32-S3R2 | cohérent avec ADR-001 |
| Mémoire | 2 MB PSRAM + 16 MB flash | mieux que V3, mais probablement trop court pour pipeline image 5 MP confortable |
| Radio | SX1262 | cohérent avec ADR-003 |
| Fréquence | 863-928 MHz selon variante | vérifier achat EU868 / antenne 868 MHz |
| TX Power | 27-28 dBm annoncé V4 | à brider légalement en EU868 |
| RX sensibilité | autour de -134 à -137 dBm @ SF12/BW125 selon source | utile pour banc portée |
| Solaire | SH1.25-2P, ~4.4-6 V / ≤540 mA | intéressant pour banc P0+, pas suffisant comme validation système |
| Batterie | Li-ion 3000 mAh | non conforme au choix LiFePO4 ADR-005 |
| Deep sleep | < 20 µA annoncé | à vérifier PPK2, surtout OLED/carte complète |
| OLED | 0.96" 128x64 | utile debug, inutile en nœud terrain final |
| Boîtier | boîtier N35 non IP67 | non conforme ADR-006 |

## Comparaison aux critères WildNexus

| Critère WildNexus | Exigence | Adéquation |
|---|---|---|
| MCU P0 | [[ESP32-S3]], PSRAM probable | **Partiel/bon** sur V4 |
| Caméra | OV5640 5 MP M12 DVP + lentille IR-corrigée | **Non conforme** |
| IR nocturne | LEDs IR 850/940 nm à déterminer, pulsed, non perturbant faune | **Absent** |
| Radio | SX1262 [[LoRa]] EU868 P2P | **Bon**, si variante EU868 |
| Gateway | [[ESP32-S3]] + SX1262 vers réseau local | **Bon candidat prototype** |
| LTE-M image à la demande | SIM7080G éteint sauf commande | **Absent** |
| Stockage image | microSD industrielle | **Absent/non documenté** |
| Autonomie | 60 jours, LiFePO4, coupures MOSFET, <100 µA carte complète | **Non prouvé / batterie non conforme** |
| Boîtier | IP67 ABS/PC avec fenêtres caméra/IR | **Non conforme** |
| Réglementaire EU | duty cycle + puissance EU868 | **À vérifier / brider TX** |

## Analyse par spécialiste

### [[Chouette]] — terrain / caméra-piège

Produit trop orienté Meshtastic portable : écran, boîtier de poche, batterie Li-ion, antenne externe. Ce n'est pas un piège caméra autonome. Il peut servir à tester une liaison [[LoRa]] en forêt, pas à valider la capture nocturne, l'étanchéité, ni l'autonomie du nœud.

### [[Forge]] — intégration firmware / système

V4 intéressante pour accélérer un prototype gateway ou banc [[LoRa]] : [[ESP32-S3]] + SX1262 + batterie + USB-C + support [[Arduino]]/ESP-IDF. Points à vérifier avant achat : pinout SPI disponible, compatibilité RadioLib, accès GPIO suffisants, capacité à désactiver OLED/Wi-Fi/BLE, et mesure deep sleep carte complète.

### [[Nova]] — image / IR

Ne répond pas à l'ADR-002. Aucun capteur OV5640 M12, aucune optique IR-corrigée, aucun éclairage IR. La PSRAM 2 MB est utile mais probablement insuffisante comme base confortable pour un flux OV5640 5 MP si l'image complète doit être bufferisée. À ne pas confondre avec le nœud caméra.

### [[Milan]] — sourcing / risque fournisseur

Amazon est bloqué par captcha côté extraction. Les pages Meshnology/Heltec donnent assez d'indices pour analyser la famille produit, mais l'ASIN doit être vérifié manuellement avant achat : V3 vs V4, fréquence EU868 vs 915, présence batterie, type d'antenne, vendeur, délais et retour.

## Recommandation achat

**Acheter éventuellement 1 ou 2 unités V4 uniquement**, pour :

1. banc RF [[LoRa]] EU868 SX1262 ;
2. prototype gateway P0 ;
3. comparaison consommation deep sleep vs DevKit + breakout ;
4. validation pratique antennes / portée / RadioLib.

**Ne pas l'inscrire comme composant du nœud caméra P0.**  
Le nœud caméra reste : [[ESP32-S3]] + OV5640 M12 DVP + lentille IR-corrigée + LEDs IR choisies + microSD + SX1262 + SIM7080G + batterie LiFePO4 + boîtier IP67.

## Conditions avant achat

- Confirmer que la variante Amazon est bien **V4**, pas V3.
- Confirmer fréquence / antenne **EU868 ou 863-928 MHz**, pas 915 MHz only.
- Confirmer que la puissance [[LoRa]] est configurable et bridée pour usage EU868.
- Confirmer disponibilité de schéma/pinout V4.
- Confirmer possibilité de couper OLED et radios non utilisées.
- Accepter que la batterie Li-ion 3000 mAh ne valide pas ADR-005.

## Décision proposée

Ajouter au registre comme **candidat gateway/banc RF**, pas comme composant nœud :

`Gateway / banc RF P0 — Meshnology N35 V4 / Heltec WiFi LoRa 32 V4 — candidat à tester — risque moyen`.
