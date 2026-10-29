# WildNexus P0 — Stock & Procurement

> **Fichier dédié WildNexus uniquement.** Source autoritaire pour l'inventaire pièces.
> **Dernière mise à jour :** 2026-07-04 — Créé depuis `hardware-state.md` + BOM v0.4 + paniers Mouser
> **Synchronisé avec :** `hardware-state.md`, `WILDNEXUS_BOM_P0_v0.4.xlsx`, `paniers-achat-p0.md`

---

## ✅ EN STOCK — Reçu

| Composant | Qté | Coût | Provenance | Date |
|-----------|-----|------|-----------|------|
| **Cartes & modules** | | | | |
| ESP32-S3-DevKitC-1 N16R8 | 2 | 21,98€ | Amazon MiMiU | 10/06 |
| ESP32-CAM OV2640 (avec module caméra) | 2 | ~25€ | Hailege Amazon.de | 21/06 |
| ESP32-CAM OV2640 (carte seule) | 4 | — | — | 23/06 |
| OV5640 DVP M12 | 5 | ~25€ | Camemake.eu + AliExpress | 12-24/06 |
| **Alimentation** | | | | |
| MP1584 DC-DC Step Down 3A | 5 | — | — | 03/07 |
| **Mesure & debug** | | | | |
| Nordic PPK2 | 1 | ~100€ | — | 06/2026 |
| USB-C TTL FT232RL | 3 | 9€ | AZDelivery Amazon | 21/06 |
| **Composants Mouser #39492997 (partiel — backorder)** | | | | |
| MEMS TDK ×3 | 3 | — | Mouser | 06/2026 |
| LED IR 940nm Würth ×10 | 10 | — | Mouser | 06/2026 |
| PIR Panasonic EKMB1303111 ×2 | 2 | — | Mouser | 06/2026 |
| Buck TI TPS62840DLCR ×? | — | — | **MANQUANT** | ETA 15/07 |
| Inductance Würth ×5 | 5 | — | Mouser | 06/2026 |
| MOSFET Nexperia ×5 | 5 | — | Mouser | 06/2026 |
| BME688 ×2 | 2 | — | Mouser | 06/2026 |
| SHT31-DIS-B ×2 | 2 | — | Mouser | 06/2026 |
| Antenne Molex LoRa 868MHz ×2 | 2 | — | Mouser | 06/2026 |
| Dissipateur alu ×4 | 4 | — | Mouser | 06/2026 |
| **Prototypage** | | | | |
| Miuzei Starter Kit Arduino (235 pcs) | 1 | — | — | 10/06 |

---

## ⏳ EN ATTENTE — Commandé mais pas reçu

| Composant | Qté | Commande | ETA | Bloquant |
|-----------|-----|----------|-----|----------|
| Buck TI TPS62840DLCR | ? | Mouser #39492997 (backorder) | 15 juillet | Non — reste de la commande reçu |

---

## 🔴 À COMMANDER — Panier Mouser restant (~279€)

| # | Composant | Qté estimée | Usage | Priorité |
|---|-----------|------------|-------|----------|
| 1 | Module LoRa RFM95W 868MHz | 3 | Communication nœud → gateway | 🔴 SOP-07 bloquée |
| 2 | Connectique (JST, headers, câbles) | Lot | Assemblage PCB | 🟡 |
| 3 | Passifs CMS (R+C 0402/0603) | Lot | Circuit alimentation | 🟡 |
| 4 | Connecteur antenne u.FL/IPEX | 3 | Antenne LoRa | 🟡 |
| 5 | Support pile CR2032 + pile | 3 | RTC backup | 🟢 |
| 6 | Diode Schottky / TVS | Lot | Protection inversion polarité | 🟢 |
| 7 | Quartz 32.768 kHz | 3 | RTC externe | 🟢 |
| 8 | Résistances de précision (shunt courant) | Lot | Mesure PPK2 | 🟢 |
| 9 | Connecteur microSD push-push | 3 | Stockage local | 🟡 |
| 10 | Carte microSD industrial 16GB | 3 | Swissbit S-45U ou Transcend | 🟡 |
| 11 | Divers (LED status, boutons, jumpers) | Lot | Prototypage | 🟢 |

---

## 🔮 FUTUR — P1/P2

| Composant | Usage | Phase |
|-----------|-------|-------|
| Panneau solaire 5V 2W | Alimentation autonome | P1 EVT |
| Batterie LiFePO4 18650 ×2 | Stockage énergie | P1 EVT |
| BMS/MPPT module | Gestion charge solaire | P1 |
| Enclos IP67 | Boîtier terrain | P1 |
| PCB prototype (×5) | Fabrication | P1 |
| XIAO ESP32 | Miniaturisation v0.2 | P2 |

---

## 📊 Résumé financier

| Catégorie | Dépensé | Restant |
|-----------|---------|---------|
| Cartes & modules | ~72€ | — |
| Mesure (PPK2) | ~100€ | — |
| Mouser #39492997 | ~106€ | Backorder TPS62840DLCR |
| Prototypage | ~77€ | — |
| Panier restant | — | ~279€ |
| **Total P0** | **~355€** | **~279€** |
| **Budget P0** | **1 000€** | **~366€ marge** |

---

*Fichier dédié WildNexus. Source synchronisée : `hardware-state.md`, BOM Excel v0.4, registre achats.*
*Mise à jour : Dobby 🦉 après chaque réception/commande JC.*
