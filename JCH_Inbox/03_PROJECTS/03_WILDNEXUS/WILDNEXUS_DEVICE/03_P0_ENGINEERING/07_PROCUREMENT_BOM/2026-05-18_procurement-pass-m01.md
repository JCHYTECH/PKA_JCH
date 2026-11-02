# WildNexus — Passe procurement M-01

**Date :** 2026-05-18  
**Objectif :** proposer où acheter, pas seulement quoi acheter, avec préférence centralisation, fournisseurs reconnus, livraison vers Liège / Belgique.

## Décision procurement provisoire

Créer deux paniers principaux :

1. **Mouser Belgique** — panier électronique principal : [[ESP32-S3]], capteurs Sensirion/Panasonic, LEDs IR Vishay/Würth, composants de puissance, éventuellement boîtier.
2. **DigiKey Belgique** — panier complémentaire : microSD industrielle Swissbit, SIM7080G, composants indisponibles/restrictifs chez Mouser.

Exceptions fabricants officiels :

- **RAK Store / revendeur EU RAK** pour RAK3172 EU868 avec variante exacte.
- **Arducam / fournisseur caméra spécialisé** pour OV5640 DVP M12, car les distributeurs généralistes ne couvrent pas clairement la variante WildNexus.
- **Lensation / Evetar** pour lentilles M12 IR-corrigées.
- **1NCE** pour SIM IoT.
- **RS Belgium / Spelsberg / Hammond** pour boîtier IP67 si Mouser/Farnell ne centralisent pas correctement.

## Fournisseurs et preuves

| Sujet | Source | Donnée utile |
|---|---|---|
| DigiKey Belgique | https://www.digikey.be/en/help-support/delivery-information/delivery-time-and-cost | livraison gratuite Belgique >= 50 EUR, sinon 18 EUR ; livraison typique 48 h |
| Mouser [[ESP32-S3]] DevKit | https://www.mouser.be/ProductDetail/Espressif-Systems/ESP32-S3-DevKitC-1-N8R8 | ESP32-S3-WROOM-1, 8 MB flash + 8 MB PSRAM, stock élevé, ~11.44 EUR |
| Mouser [[ESP32-S3]] module | https://www.mouser.be/ProductDetail/Espressif-Systems/ESP32-S3-WROOM-1U-N8R8 | module officiel, 8 MB PSRAM + 8 MB flash, IPEX, stock élevé, ~5.36 EUR |
| RAK3172 officiel | https://www.rakwireless.com/en-us/products/lpwan-modules/rak3172-wisduo-lpwan-module | [[LoRa]] P2P, EU868 supporté, STM32WLE5CC, module basse conso |
| RAK Store WisDuo | https://store.rakwireless.com/collections/wisduo | RAK3172 module, breakout, evaluation board ; prix indicatifs officiels |
| RAK3172 EU revendeur | https://industry-electronics.com/rak-wireless/305017-lora-wisduo-stm32wl-module-rak3172-ipex-eu868-lieske_1890276.htm | variante EU868 avec IPEX, prix indicatif ~10.29 EUR TTC, délai à vérifier |
| DigiKey SIM7080G | https://www.digikey.nl/nl/products/detail/simcom-wireless-solutions-limited/SIM7080G/15841448 | module actif, RF TXRX cellular/GNSS, 3 semaines lead time constructeur |
| Swissbit industrial microSD | https://www.digikey.be/en/product-highlight/s/swissbit/memory-storage-solutions | cartes microSD industrielles ; alternatives disponibles |
| Mouser Swissbit | https://www.mouser.be/new/swissbit/swissbit-industrial-SD-memory/ | S-46u microSD industriel pSLC, 2-64 GB |
| Mouser SHT31 | https://www.mouser.be/ProductDetail/Sensirion/SHT31-DIS-B2.5kS | capteur humidité/température Sensirion |
| Mouser Panasonic PIR | https://www.mouser.com/new/panasonic/panasonic-pir-ekmb-detectors/ | EKMB avec courant aussi bas que 1 µA |
| Mouser IR 940 nm | https://www.mouser.be/ProductDetail/Vishay-Semiconductors/VSMA1094250 | émetteur IR haute puissance 940 nm |
| Mouser IR catalogue | https://www.mouser.be/c/optoelectronics/leds/ir-leds/ | filtres 850/940 nm, Vishay/Würth |
| RS boîtier IP67 | https://benl.rs-online.com/web/p/general-purpose-enclosures/2384028 | RS PRO ZP150 polycarbonate IP67 150 × 100 × 60 mm |
| LiFePO4 EU | https://keeppower.com/product/18650-3-2v-2000mah-lifepo4-rechargeable-lithium-ion-battery-cell-ifr18650/ | cellule IFR18650 LiFePO4 3.2 V 2000 mAh |
| ENERpower pack | https://enerprof.de/en/products/jst-2-54hx-enerpower-12v-lifepo4-4s1p-18650-2000-mah | pack LiFePO4 européen, à vérifier selon architecture tension |

## Recommandation opérationnelle

### Panier Mouser BE initial

- 2 × ESP32-S3-DevKitC-1-N8R8
- 5-10 × ESP32-S3-WROOM-1U-N8R8 si PCB P0 lancé
- LEDs IR Vishay/Würth 850 nm + 940 nm
- Panasonic EKMB PIR basse consommation
- SHT31-DIS
- composants load-switch/MOSFET/régulateurs quand schéma WP02 gelé

### Panier DigiKey BE initial

- Swissbit microSD industrielle 8-16 GB
- SIM7080G seulement si le cellulaire P1 est réactivé
- composants indisponibles Mouser ou meilleurs délais

### Achats fabricant

- RAK3172 EU868 + IPEX : RAK Store ou revendeur EU fiable.
- OV5640 DVP M12 : pas d'achat tant que pinout, NoIR/IR-cut, DVP et monture M12 ne sont pas confirmés.
- Lentilles M12 IR-corrigées : demander devis Lensation/Evetar.

## Décisions à confirmer avant commande

1. architecture batterie : 1S/2P LiFePO4 vs pack série + régulation ;
2. caméra exacte : OV5640 DVP M12 NoIR / IR-cut motorisé ;
3. IR : 850 + 940 nm pour test, puis décision faune ;
4. [[LoRa]] : RAK3172 module nu vs breakout/eval board pour M-02 ;
5. boîtier : layout interne avant achat boîtier final.
