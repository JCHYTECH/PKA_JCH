# WildNexus — Scan marché produits intégrés proches des décisions P0

**Date :** 2026-05-18  
**Demande JCH :** vérifier s'il existe un fabricant avec un produit réunissant déjà les décisions P0 WildNexus.  
**Statut :** scan préliminaire — à approfondir avant achat / pivot architecture.

## Verdict court

À ce stade, **aucun produit identifié ne réunit entièrement nos décisions P0**.

Mais un produit mérite une analyse sérieuse comme benchmark ou éventuel raccourci partiel :

**Seeed SenseCAP A1102 LoRaWAN Vision AI Sensor**  
Il coche plusieurs cases terrain : caméra 5 MP OV5647, LoRaWAN EU868, IP66, microSD 8 GB, batterie 19 Ah Li-SOCl2, Edge AI local. Il ne respecte pas l'architecture P0 au sens strict : pas ESP32-S3 comme MCU principal caméra, pas LoRa P2P SX1262 gateway propre, pas LTE-M image à la demande, pas caméra OV5640 M12 DVP, pas IR nocturne documenté, intégration cloud/SenseCraft à évaluer.

## Critères P0 rappelés

| Domaine | Décision P0 |
|---|---|
| MCU | ESP32-S3 |
| Caméra | OV5640 5 MP M12 DVP + lentille IR-corrigée |
| Nuit | LEDs IR pulsées, longueur d'onde non visible/non perturbante faune |
| Radio principale | LoRa EU868 P2P / SX1262, gateway propre |
| Image à la demande | LTE-M SIM7080G éteint sauf commande |
| Stockage | microSD industrielle locale |
| Énergie | batterie LiFePO4, deep sleep carte complète < 100 µA, MOSFET/load-switch périphériques |
| Boîtier | IP67, fenêtre optique maîtrisée |
| Souveraineté | pas de dépendance cloud obligatoire |

## Produits / plateformes identifiés

### 1. Seeed SenseCAP A1102 LoRaWAN Vision AI Sensor — candidat benchmark sérieux

Sources :
- https://www.seeed.cc/product/sensecap-a1102-lorawan-vision-ai-sensor
- https://wiki.seeedstudio.com/sensecap_a1102/

Caractéristiques relevées :

| Élément | Donnée |
|---|---|
| Caméra | OV5647, 2592 × 1944, objectif 3.4 mm ajustable, FOV 62° |
| Inference | 480 × 480 >10 FPS |
| Radio | LoRaWAN v1.0.3 Class A, IN865/EU868/US915/AU915/AS923 |
| Batterie | D-size Li-SOCl2 19 Ah, remplaçable |
| Stockage | microSD 8 GB, jusqu'à 20 000 images |
| Protection | IP66 |
| Température | 0-70 °C |
| Architecture | Himax-6538 vision AI + Wio-E5 STM32WLE5JC LoRaWAN + XIAO ESP32-C3 BLE/Wi-Fi |

Adéquation :

| Critère | Statut |
|---|---|
| Caméra 5 MP | **Partiel** — OV5647 5 MP, pas OV5640 M12 |
| LPWAN | **Partiel** — LoRaWAN, pas LoRa P2P gateway propre |
| Terrain | **Bon** — IP66, batterie 19 Ah |
| Stockage local | **Bon** — microSD 8 GB |
| Edge AI | **Bon** — modèle local |
| Nuit / IR | **Non documenté** — point critique |
| Souveraineté cloud | **À vérifier** — SenseCraft / API / offline |
| Image full-res à la demande | **À vérifier** — probablement export local, pas LTE-M |

Décision proposée : **benchmark externe prioritaire**, pas remplacement direct P0 sans test.

Questions à poser à Seeed :

1. La caméra voit-elle en IR ou existe-t-il une version NoIR ?
2. L'objectif est-il remplaçable ou IR-corrigé ?
3. Peut-on utiliser l'appareil sans SenseCraft Cloud ?
4. Peut-on récupérer les images full-res par API ou seulement localement ?
5. Peut-on déployer un modèle faune custom sans abonnement ?
6. Peut-on accéder aux événements LoRaWAN hors infrastructure Seeed ?
7. Existe-t-il une variante IP67 / basse température < 0 °C ?

### 2. RAK WisBlock — plateforme modulaire terrain, mais pas caméra P0

Sources :
- https://www.rakwireless.com/en-us/products/wisblock
- https://store.rakwireless.com/pages/wisblock
- https://store.rakwireless.com/collections/wisblock-enclosure

Forces :
- approche modulaire LPWAN ;
- bases avec batterie/solaire ;
- boîtiers IP65/IP67 ;
- écosystème industriel et documenté.

Limites :
- ne fournit pas directement notre bloc caméra 5 MP M12 IR-corrigé ;
- coeur souvent nRF52/STM32/RAK, pas ESP32-S3 caméra ;
- utile comme inspiration mécanique/énergie/enclosure, moins comme produit caméra complet.

Décision proposée : **référence boîtier/énergie/modularité**, pas nœud caméra P0.

### 3. Heltec / Meshnology / LilyGO / Seeed XIAO ESP32-S3 + SX1262 — bons modules RF, pas caméra

Sources :
- https://heltec.org/project/wifi-lora-32-v4/
- https://www.lilygo.cc/products/t3-s3
- https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/113110064/26553901

Forces :
- ESP32-S3 + SX1262 ;
- EU868 disponible ;
- prototypage rapide LoRa / gateway ;
- parfois solaire et batterie.

Limites :
- pas caméra ;
- pas IR ;
- pas boîtier IP67 caméra ;
- souvent OLED/HMI inutile ;
- pas stockage image ni LTE-M.

Décision proposée : **banc RF / gateway**, pas nœud caméra.

### 4. Tokay Lite / WildCAM ESP32 / projets open source caméra faune — bons apprentissages, pas produit P0 complet

Sources :
- https://www.crowdsupply.com/maxlab/tokay-lite
- https://github.com/thewriterben/WildCAM_ESP32
- https://github.com/curiouselectric/Lapse-O-Matic

Forces :
- caméra ESP32 orientée wildlife ;
- PIR, solaire, stockage selon projet ;
- open source utile pour firmware/power patterns.

Limites :
- souvent OV2640 / 2 MP ;
- pas LoRa SX1262 intégré ;
- pas architecture IP67 industrielle ;
- pas disponibilité fabricant robuste.

Décision proposée : **veille technique / patterns firmware**, pas achat composant P0.

## Conclusion

Le produit le plus proche est **Seeed SenseCAP A1102**, mais il ressemble davantage à un **capteur industriel Edge AI LoRaWAN** qu'à notre nœud WildNexus souverain avec image à la demande.

La bonne stratégie semble être :

1. garder l'architecture P0 custom comme ligne principale ;
2. acheter ou demander un devis SenseCAP A1102 uniquement comme benchmark terrain / comparaison ;
3. continuer à utiliser Meshnology/Heltec/LilyGO comme bancs LoRa/gateway ;
4. surveiller RAK WisBlock pour boîtier, alimentation solaire et modularité.

## Mandat équipe proposé

- **Milan** : contacter/qualifier Seeed, RAK, Heltec/LilyGO ; vérifier versions EU, disponibilité, prix, API, documentation.
- **Nova** : vérifier caméra/IR/nocturne sur SenseCAP A1102 et alternatives.
- **Forge** : vérifier ouverture API, autonomie du pipeline, export image, intégration dashboard PKA.
- **Chouette** : évaluer terrain : IP, batterie, fixation, froid, faune, maintenance.
