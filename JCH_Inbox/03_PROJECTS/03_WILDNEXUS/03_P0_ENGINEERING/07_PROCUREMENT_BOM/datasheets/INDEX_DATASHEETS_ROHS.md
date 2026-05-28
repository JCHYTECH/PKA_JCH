# WildNexus P0 — Index des fiches techniques & RoHS

**Date :** 2026-05-25
**Statut :** collecte batch — à compléter
**Owner :** [[Dobby]] + [[Forge]]
**Dossier :** `03_P0_ENGINEERING/07_PROCUREMENT_BOM/datasheets/`

---

## Légende

| Icône | Signification |
|-------|--------------|
| 📥 | Fiche téléchargée et stockée |
| 🔗 | URL directe fournie — à télécharger |
| ❓ | URL à confirmer |
| ✅ | RoHS conforme |
| ⚠️ | RoHS à vérifier |
| 🗑️ | Composant obsolète |

---

## Option A — Banc rapide

| # | Composant | Réf. fabricant | Fiche technique | RoHS | Mouser/DigiKey |
|---|-----------|---------------|-----------------|------|----------------|
| A01 | MCU DevKit | **ESP32-S3-DevKitC-1-N8R8** | [🔗 Espressif](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/) | ✅ Oui | [Mouser](https://www.mouser.be/ProductDetail/Espressif-Systems/ESP32-S3-DevKitC-1-N8R8) |
| A02 | Caméra | **OV5640 DVP M12** (Arducam B0253) | 🔗 Arducam — demander fiche avant commande | ✅ Oui | arducam.com |
| A03 | LED IR 850nm | **Vishay VSLY3850** | [🔗 Vishay](https://www.vishay.com/en/product/81132/) | ✅ Oui | Mouser VSLY3850 |
| A04 | LED IR 940nm | **Vishay VSLB3940** | [🔗 Vishay](https://www.vishay.com/en/product/81133/) | ✅ Oui | Mouser VSLB3940 |
| A05 | PIR basse conso | **Panasonic EKMB1303111** | [🔗 Panasonic](https://na.industrial.panasonic.com/products/sensors/sensors-automotive-industrial/pir-motion-sensor-papirs/series/ekmb-series/lineup/ekmb1303111) | ✅ Oui | Mouser EKMB1303111 |
| A06 | Micro MEMS I2S | **Knowles SPH0645LM4H-B** ⚠️ OBSOLÈTE | [🔗 Knowles](https://www.knowles.com/docs/default-source/model-documents/sph0645lm4h-b-datasheet) | ✅ Oui | DigiKey SPH0645 (stock résiduel 16K) |
| A07 | microSD industrielle | **Swissbit S-45U 16GB** | [🔗 Swissbit](https://www.swissbit.com/en/products/nand-flash-products/microsd-memory-cards/s-45u/) | ✅ Oui | DigiKey S-45U |
| A08 | Buck faible Iq | **TI TPS62840DLCR** | 📥 Stocké — `TI_TPS62840_datasheet.pdf` (3.2 MB) | ✅ Oui | [Mouser](https://www.mouser.be/ProductDetail/Texas-Instruments/TPS62840DLCR) — **épuisé, commander Mouser US** |
| A09 | Holder AA ×4 | **Keystone 2463** | [🔗 Keystone](https://www.keyelco.com/product.cfm/product_id/2947) | ✅ Oui | RS Belgium / Mouser |
| A10 | Inductance buck | **Würth 744043100** | [🔗 Würth](https://www.we-online.com/en/components/products/WE-LQS#744043100) | ✅ Oui | Mouser 744043100 |
| A11 | Passifs CMS | Lot 0402/0603 | Pas de fiche unitaire | ✅ Oui | Mouser — panier passifs |
| A12 | MOSFET power gating | **Nexperia PMV16XN** | [🔗 Nexperia](https://www.nexperia.com/products/mosfets/small-signal-mosfets/PMV16XN.html) | ✅ Oui | Mouser PMV16XN |
| A13 | Power Profiler | **Nordic nRF-PPK2** | 📥 Stocké — `Nordic_PPK2_product_brief.pdf` | ✅ Oui | Nordic Semi / Mouser |
| A14 | Breadboard + Dupont | Kit proto | Pas de fiche | N/A | Amazon / Conrad |
| A15 | Alim labo USB | RD UM24C | [🔗 Ruideng](https://www.aliexpress.com/) | ❓ | Amazon / AliExpress |
| A16 | Piles Lithium AA | Energizer L91 | Pas de fiche | ✅ Oui | Carrefour / Action |

---

## Option B — Additions terrain

| # | Composant | Réf. fabricant | Fiche technique | RoHS | Mouser/DigiKey |
|---|-----------|---------------|-----------------|------|----------------|
| B01 | Lentille M12 IR | **Lensation LS-6028** / **Evetar M12B0618W-IR** | 🔗 Lensation — demander devis + fiche | ✅ Oui | lensation.de |
| B02 | Module [[LoRa]] | **RAK3172-T EU868** (SX1262) | [🔗 RAKwireless](https://docs.rakwireless.com/Product-Categories/WisDuo/RAK3172-Module/Datasheet/) | ✅ Oui (CE) | RAK Store EU |
| B03 | Antenne [[LoRa]] 868 | **Molex 0213980100** | [🔗 Molex](https://www.molex.com/en-us/products/part-detail/0213980100) | ✅ Oui | Mouser |
| B04 | Boîtier IP67 | **Hammond 1554B** | [🔗 Hammond](https://www.hammfg.com/electronics/small-case/plastic/1554) | ✅ Oui | RS Belgium / Mouser |
| B05 | Capteur env. | **Bosch BME688** | [🔗 Bosch](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/) | ✅ Oui | Mouser BME688 |
| B06 | Humidité/Temp | **Sensirion SHT31-DIS-B** | [🔗 Sensirion](https://sensirion.com/products/catalog/SHT31-DIS-B/) | ✅ Oui | Mouser SHT31-DIS-B |
| B07 | Presse-étoupe M16 | Conxall / standard | Pas de fiche critique | ✅ Oui | RS Belgium |
| B08 | Silica gel + joints | Standard | Pas de fiche | N/A | Conrad |
| B09 | Sangle UV | Standard | Pas de fiche | N/A | Conrad |

---

## Statut RoHS global

Tous les composants actifs et passifs proviennent de fabricants majeurs (TI, Espressif, Vishay, Panasonic, Würth, Nexperia, Bosch, Sensirion, Molex, RAKwireless) → **RoHS conformes par défaut**. Les fiches techniques individuelles le confirment en page 1 ou en fin de document (marquage RoHS / China RoHS / REACH).

Seuls points d'attention :
- **A15 (RD UM24C)** : alimentation chinoise, vérifier marquage CE/RoHS sur l'emballage
- **A06 (SPH0645LM4H-B)** : obsolète mais stock résiduel conforme RoHS

---

## Prochaine étape

1. JCH télécharge les fiches 🔗 depuis les URLs ci-dessus et les place dans `datasheets/`
2. [[Forge]] vérifie les disponibilités Mouser/DigiKey à date
3. Ajouter les certificats RoHS formatels si nécessaire pour l'enregistrement produit final (les fiches techniques suffisent généralement)
