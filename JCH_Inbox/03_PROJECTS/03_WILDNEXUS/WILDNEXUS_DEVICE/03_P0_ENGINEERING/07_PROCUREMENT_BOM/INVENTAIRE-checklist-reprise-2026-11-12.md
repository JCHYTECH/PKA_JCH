# WildNexus P0 — Checklist d'inventaire de reprise (gate 1)

> Dobby 🦉 — 2026-11-12. Feuille à emporter au banc, à remplir physiquement.
> Remplace le brouillon du 11/11 (`INVENTAIRE-releve-physique-2026-11-11.md`).
> **Règle :** aucune valeur n'est fiable tant qu'elle n'est pas lue sur le composant + la facture. Ne pas déduire le stock d'une ligne « commandé ».
> À la fin, renvoyer la feuille remplie → Dobby met à jour `hardware-state.md`, `WILDNEXUS_stock.md` et le budget, puis lève la gate.

---

## A. Références à lire sur le composant (priorité 1 — débloquent les SOP)

| ☐ | # | Composant | Qté attendue | À lire / trancher | Relevé (à remplir) |
|---|---|---|---|---|---|
| ☐ | 1 | ESP32-S3-DevKitC-1 | 2 | **N16R8 ou N8R8 ?** RAM/flash non interchangeables | |
| ☐ | 2 | Micros MEMS TDK | 2 (doc) / 3 (stock) | Réf exacte (MMICT5848-00-012 ?) + **interface I2S/PDM** vs cible SPH0645LM4H-B | |
| ☐ | 3 | PIR Panasonic | 2 | **EKMB1203111 ou EKMB1303111 ?** (lire sur le boîtier) | |
| ☐ | 4 | Caméra OV5640 DVP M12 | 5 | Réf module, pinout DVP, NoIR/IR-cut, alimentation | |
| ☐ | 5 | LED IR 940 nm | 10 | Réf (VSLB3940 ?) + confirmer **940 nm** | |
| ☐ | 6 | MOSFET SI2302 | 5 | Réf exacte (SI2302CDS-T1-GE3 ?) | |
| ☐ | 7 | Buck TPS62840DLCR | 5 | **Qté réellement présente** (backorder historique) | |
| ☐ | 8 | Geekworm X1205 UPS HAT | 1 | Accus **21700 vs 18650** (wiki vs stock) | |

## B. Boîte Mouser #39492997 — cocher chaque ligne présente

| ☐ | Ligne | Qté | Réf |
|---|---|---|---|
| ☐ | LED IR 940nm Vishay 3mm | 10 | VSLB3940 |
| ☐ | PIR Panasonic 12m 2uA | 2 | EKMB1203111 |
| ☐ | Micro MEMS TDK InvenSense I2S PDM | 2 | MMICT5848-00-012 |
| ☐ | Buck TI 60nA Iq 3Vout | 5 | TPS62840DLCR |
| ☐ | Inductance Wurth 10uH 4848 SMD | 5 | 744043100 |
| ☐ | MOSFET Vishay N-ch SOT-23 | 5 | SI2302CDS-T1-GE3 |
| ☐ | Capteur Bosch gaz T/P/H | 2 | BME688 |
| ☐ | Capteur Sensirion humidité I2C | 2 | SHT31-DIS-B |
| ☐ | Antenne Molex LoRa 868MHz IPEX | 2 | 211140-0100 |
| ☐ | Dissipateur alu adhésif 14×14 mm | 4 | ATS-HK127-R0 |
| ☐ | Lot passifs CMS SparkFun 0603 (500 pcs) | 1 | KIT-14585 |

> ⚠️ Montant à trancher sur la facture : **105,94 €** (hardware-state) vs **128,20 €** (budget/Start.md). Relever HT/TTC + frais de port.

## C. Quantités / factures à rapprocher (priorité 2 — budget)

| ☐ | # | Poste | Écart / action |
|---|---|---|---|
| ☐ | 9 | ESP32-CAM OV2640 seules ×4 | Facture à retrouver (montant non chiffré) |
| ☐ | 10 | Miuzei Starter Kit | Contenu réel + prix (~35 €) |
| ☐ | 11 | MP1584 DC-DC ×5 | Présence + adéquation schéma (non chiffré) |
| ☐ | 12 | Engagé global ~610 € vs lignes visibles ~332,75 € | **Écart ~277 € à identifier** — lister les factures manquantes |
| ☐ | 13 | PPK2 (Mouser #39411684) | 83,57 € HT/TTC + port — ne pas compter 2× |

## D. Non reçus — GELÉS, ne rien commander

| Poste | État | Blocage |
|---|---|---|
| microSD 128 GB | non reçu (~15 €) | endurance + capacité après inventaire |
| Panier restant (~279 €) : LoRa RAK3172-T EU868 ×2 + connectique/passifs | à revalider | prix/dispo/frais + preuve radio |
| Gateway P0 (ESP32-S3 + SX1262) | non chiffrée | preuve LoRa à démontrer |
| Optique M12 IR-corrigée | non sélectionnée | devis + test jour/nuit |
| Pack AA 4S2P L91 | **SOP-10 suspendue** | ni achat ni montage avant ADR-005 + schéma |

## E. Lignes rouges sécurité

- **SOP-10 suspendue** — ne pas assembler le pack 4S2P L91.
- Ne pas appliquer 3,3 V sur la broche 5 V.
- Ne suivre aucun schéma d'alimentation avant validation ADR-005 + revue du câblage complet.

## Conséquence

Projection ~904 € > seuil interne 900 € → **pause des achats** tant que A + B + C ne sont pas remplis et que la réconciliation n'est pas validée par JCH.

---

*À remplir au banc puis renvoyer à Dobby.*
