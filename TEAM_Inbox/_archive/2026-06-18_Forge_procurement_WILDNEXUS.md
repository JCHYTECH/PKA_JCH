# Rapport Procurement — WILDNEXUS — 2026-06-18

**Généré par :** [[Forge]] 🦦 (PKA Procurement Agent)
**Source BOM :** `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/mouser_bom.csv`
**Coût total estimé :** 105.32 €
**Mode simulation :** NON

---

## Comparaison Mouser vs DigiKey

| Ref | Description | Qté | MPN | Prix Mouser | Stock M | Prix DK | Stock DK | Best |
|-----|-------------|-----|-----|------------:|--------:|--------:|--------:|------|
| —      | LED IR 940nm Vishay 3mm             | 10 | `VSLB3940                 ` |    0.54€ |  14336 |    0.63€ |  39334 | **Mouser** |
| —      | PIR Panasonic EKMB 12m 2uA          | 2 | `EKMB1203111              ` |   22.30€ |    150 |   22.21€ |    237 | **DigiKey** |
| —      | Micro MEMS TDK InvenSense I2S PDM   | 2 | `MMICT5848-00-012         ` |    2.04€ |  35203 |    2.03€ |  10932 | **DigiKey** |
| —      | Buck TI 60nA Iq 3Vout               | 5 | `TPS62840DLCR             ` |    1.85€ |      0 |    1.84€ |      0 | **Aucun** |
| —      | Inductance Wurth 10uH 4848 SMD      | 5 | `744043100                ` |    1.31€ |   2535 |    1.31€ |    455 | **Mouser** |
| —      | MOSFET Vishay N-ch SOT-23           | 5 | `SI2302CDS-T1-GE3         ` |    0.70€ | 137787 |    0.70€ | 100251 | **DigiKey** |
| —      | Capteur Bosch gaz T/P/H             | 2 | `BME688                   ` |    7.44€ |   7066 |    7.70€ |  11237 | **Mouser** |
| —      | Capteur Sensirion humidite I2C      | 2 | `SHT31-DIS-B              ` |    3.87€ |   9166 |    3.86€ |  12433 | **DigiKey** |
| —      | Antenne Molex LoRa 868MHz IPEX      | 2 | `211140-0100              ` |    2.15€ |   9458 |    2.14€ |   4964 | **DigiKey** |
| —      | Dissipateur alu adhesif 14x14mm     | 4 | `ATS-HK127-R0             ` |    1.31€ |   4134 |    1.32€ |  24249 | **Mouser** |
| —      | Lot passifs CMS SparkFun 0603 500pc | 1 | `KIT-14585                ` |      N/A |    N/A |      N/A |    N/A | **Aucun** |

---

## Paniers optimisés

### Mouser — 4 composants
- Sous-total : 32.09 €
- Livraison : 18.00 € ❌ gratuit
- **Total : 50.09 €**

### DigiKey — 5 composants
- Sous-total : 63.98 €
- Livraison : 0.00 € ✅ gratuit
- **Total : 63.98 €**


💰 Économie estimée vs 8 paniers manuels : **37.00 €** de frais de port

---

## Validation MPN (H2 — Arbor)

| Ref | Confiance | Score | Vérifications |
|-----|-----------|------:|--------------|
| LED IR 940nm Vishay  | ✅ | 100% | — |
| PIR Panasonic EKMB 1 | ✅ | 100% | — |
| Micro MEMS TDK Inven | ✅ | 100% | — |
| Buck TI 60nA Iq 3Vou | 🔴 | 40% | ❌ Courant<br>⚠️ Courant attendu 60nA, trouvé rien<br>Rupture de stock |
| Inductance Wurth 10u | ✅ | 100% | — |
| MOSFET Vishay N-ch S | ⚠️ | 80% | ❌ Package<br>⚠️ Package attendu SOT-23, trouvé rien |
| Capteur Bosch gaz T/ | ✅ | 100% | — |
| Capteur Sensirion hu | ✅ | 100% | — |
| Antenne Molex LoRa 8 | ⚠️ | 80% | ❌ Fréquence<br>⚠️ FRÉQUENCE CRITIQUE: attendu 868MHz, trouvé rien |
| Dissipateur alu adhe | ✅ | 100% | — |
| Lot passifs CMS Spar | ⚠️ | 80% | ❌ Package<br>⚠️ Package attendu 0603, trouvé rien |

---

## Checklist terrain [[Chouette]] 🦉

**** — LED IR 940nm Vishay 3mm
  - 🔦 Confirmer longueur d'onde compatible faune (940nm préféré)

**** — Antenne Molex LoRa 868MHz IPEX
  - 📻 Vérifier bande EU868 (pas US915/AS923)
  - 📡 Vérifier connecteur IPEX/U.FL (pas SMA seul)

---

## Résumé

_LLM non disponible — narratif automatique désactivé._

---

## Composants analysés

| Ref | Description | Qté | MPN | Prix unit. | Stock | Délai (j) | Statut | Fournisseur |
|-----|-------------|-----|-----|-----------|-------|-----------|--------|-------------|
|  | LED IR 940nm Vishay 3mm | 10 | `VSLB3940` | 0.54 € | 14336 | N/A | ✅ OK | [Mouser](https://www.mouser.be/ProductDetail/Vishay-Semiconductors/VSLB3940?qs=EvRzT9Rf7CaIvd2QC2iHWA%3D%3D) |
|  | PIR Panasonic EKMB 12m 2uA | 2 | `EKMB1203111` | 22.21 € | 237 | N/A | ✅ OK | [Mouser](https://www.digikey.be/en/products/result?keywords=EKMB1203111) |
|  | Micro MEMS TDK InvenSense I2S PDM | 2 | `MMICT5848-00-012` | 2.03 € | 10932 | N/A | ✅ OK | [Mouser](https://www.digikey.be/en/products/result?keywords=MMICT5848-00-012) |
|  | Buck TI 60nA Iq 3Vout | 5 | `TPS62840DLCR` | 1.85 € | 0 | N/A | ✅ OK | [Mouser](https://www.mouser.be/ProductDetail/Texas-Instruments/TPS62840DLCR?qs=%252B6g0mu59x7L1%2Fxo1joT%252Bvg%3D%3D) |
|  | Inductance Wurth 10uH 4848 SMD | 5 | `744043100` | 1.31 € | 2535 | N/A | ✅ OK | [Mouser](https://www.mouser.be/ProductDetail/Wurth-Elektronik/744043100?qs=PGXP4M47uW67U3yLBymoaw%3D%3D) |
|  | MOSFET Vishay N-ch SOT-23 | 5 | `SI2302CDS-T1-GE3` | 0.70 € | 100251 | N/A | ✅ OK | [Mouser](https://www.digikey.be/en/products/result?keywords=SI2302CDS-T1-GE3) |
|  | Capteur Bosch gaz T/P/H | 2 | `BME688` | 7.44 € | 7066 | N/A | ✅ OK | [Mouser](https://www.mouser.be/ProductDetail/Bosch-Sensortec/BME688?qs=IS%252B4QmGtzzqQoVDscqwx3A%3D%3D) |
|  | Capteur Sensirion humidite I2C | 2 | `SHT31-DIS-B` | 3.86 € | 12433 | N/A | ✅ OK | [Mouser](https://www.digikey.be/en/products/result?keywords=SHT31-DIS-B) |
|  | Antenne Molex LoRa 868MHz IPEX | 2 | `211140-0100` | 2.14 € | 4964 | N/A | ✅ OK | [Mouser](https://www.digikey.be/en/products/result?keywords=211140-0100) |
|  | Dissipateur alu adhesif 14x14mm | 4 | `ATS-HK127-R0` | 1.31 € | 4134 | N/A | ✅ OK | [Mouser](https://www.mouser.be/ProductDetail/Advanced-Thermal-Solutions/ATS-HK127-R0?qs=MLItCLRbWsyXxPeqlLwrKA%3D%3D) |
|  | Lot passifs CMS SparkFun 0603 500pcs | 1 | `KIT-14585` | N/A | N/A | N/A | ✅ OK | — |

---

## Alertes

- ⚠️ **** (`TPS62840DLCR`) — Rupture de stock

---

## Paniers recommandés

### Non spécifié
- `VSLB3940` × 10 = 5.42 €  
  https://www.mouser.be/ProductDetail/Vishay-Semiconductors/VSLB3940?qs=EvRzT9Rf7CaIvd2QC2iHWA%3D%3D
- `EKMB1203111` × 2 = 44.42 €  
  https://www.digikey.be/en/products/result?keywords=EKMB1203111
- `MMICT5848-00-012` × 2 = 4.06 €  
  https://www.digikey.be/en/products/result?keywords=MMICT5848-00-012
- `TPS62840DLCR` × 5 = 9.25 €  
  https://www.mouser.be/ProductDetail/Texas-Instruments/TPS62840DLCR?qs=%252B6g0mu59x7L1%2Fxo1joT%252Bvg%3D%3D
- `744043100` × 5 = 6.55 €  
  https://www.mouser.be/ProductDetail/Wurth-Elektronik/744043100?qs=PGXP4M47uW67U3yLBymoaw%3D%3D
- `SI2302CDS-T1-GE3` × 5 = 3.50 €  
  https://www.digikey.be/en/products/result?keywords=SI2302CDS-T1-GE3
- `BME688` × 2 = 14.88 €  
  https://www.mouser.be/ProductDetail/Bosch-Sensortec/BME688?qs=IS%252B4QmGtzzqQoVDscqwx3A%3D%3D
- `SHT31-DIS-B` × 2 = 7.72 €  
  https://www.digikey.be/en/products/result?keywords=SHT31-DIS-B
- `211140-0100` × 2 = 4.28 €  
  https://www.digikey.be/en/products/result?keywords=211140-0100
- `ATS-HK127-R0` × 4 = 5.24 €  
  https://www.mouser.be/ProductDetail/Advanced-Thermal-Solutions/ATS-HK127-R0?qs=MLItCLRbWsyXxPeqlLwrKA%3D%3D

---

## Alternatives proposées

_Aucune alternative proposée._

---

## Décisions en attente JCH

_Aucune décision bloquante._

---

*Aucune commande ne sera passée sans validation explicite JCH.*
