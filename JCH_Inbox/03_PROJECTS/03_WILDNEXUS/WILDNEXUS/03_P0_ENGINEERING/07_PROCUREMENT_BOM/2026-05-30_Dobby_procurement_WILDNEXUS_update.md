# Rapport Procurement WILDNEXUS — Mise à jour 2026-05-30

**Généré par :** [[Dobby]] 🦉 — mise à jour du rapport [[Forge]] du 2026-05-26
**Dernière mise à jour :** 2026-07-06
**Source BOM :** `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/WILDNEXUS_BOM_P0_v0.2.xlsx`
**Shortlist canonique :** `2026-06-12_WP02_shortlist_achat_P0_v0.2.md`
**Budget P0 :** 1 000 € | Mouser #39492997 commandé (105,94€) | Reste à commander : ~279€ | Réserve : ~107€

---

## Résumé

Les 3 composants marqués MANUEL par [[Forge]] le 26/05 sont en réalité déjà spécifiés avec MPN et fournisseur dans la shortlist v0.1. Ce rapport les fait passer au statut OK avec la mention « Confirmer stock au moment de la commande ».

Le panier Mouser peut être groupé immédiatement. Le PPK2 reste le bloqueur critique.

---

## Statut consolidé — 14 composants

| # | Composant | MPN | Qté | Prix unit. | Total | Fournisseur | Statut |
|---|-----------|-----|-----|-----------|-------|-------------|--------|
| A01 | MCU prototype | ST SPC560B-DIS | 1 | 95,03 € | 95,03 € | Mouser BE | ✅ OK |
| A02 | Caméra capteur | OV5640 DVP M12 (modules existants) | 1 | ~22 € | ~22 € | Stock interne | ✅ REÇU — Arducam gelé (MOQ 10), on utilise les OV5640 dispos |
| A03 | LED IR 850 nm | Vishay VSLY3850 | 10 | ~0,80 € | ~8 € | Mouser BE | ✅ OK |
| A04 | LED IR 940 nm | Vishay VSLB3940 | 10 | ~0,90 € | ~9 € | Mouser BE | ✅ OK |
| A05 | PIR basse conso | **Panasonic EKMB1303111K** | 1 | ~20 € | ~20 € | Mouser BE | ✅ RÉSOLU — MPN confirmé, stock à vérifier |
| A06 | Micro MEMS I2S | Knowles SPH0645LM4H-B | 2 | ~4 € | ~8 € | Mouser BE | ✅ OK |
| A07 | microSD industrielle | **Swissbit S-45U 16 GB** (pSLC) | 3 | ~18 € | ~54 € | DigiKey BE | ✅ RÉSOLU — MPN confirmé, stock à vérifier |
| A08 | Buck faible Iq | TPS62840DLCR | 5 | ~2,50 € | ~13 € | Mouser BE | ✅ OK |
| A09 | Holder AA × 4 | Keystone 2463 | 4 | ~3,50 € | ~14 € | RS / Mouser BE | ✅ OK |
| A10 | Inductance buck | Würth 744043100 | 5 | ~0,60 € | ~3 € | Mouser BE | ✅ OK |
| A11 | Passifs CMS | Vishay MSP06A0110K0GEJ | 10 | ~0,56 € | ~6 € | Mouser BE | ✅ OK |
| A12 | MOSFET power gating | Nexperia PMV16XN | 5 | ~0,50 € | ~3 € | Mouser BE | ✅ OK |
| A13 | **Nordic PPK2** | nRF-PPK2 | 1 | ~100 € | **~100 €** | Mouser BE / Nordic shop | ✅ REÇU — utilisé en P0 (test harness, LEAFNET, sonification) |
| A14 | Alimentation labo USB | **RD UM24C** ou Ruideng RD6006 | 1 | ~35 € | ~35 € | Amazon.de | ✅ RÉSOLU — Amazon.de, livraison rapide |
| A15 | Breadboard + câbles | Kit proto 830 pts | 2 | ~7 € | ~14 € | Amazon.de / Conrad | ✅ OK |
| A16 | Piles AA lithium | Energizer L91 × 16 | 16 | ~1,80 € | ~29 € | Amazon.be / Carrefour | ✅ OK |

---

## Paniers groupés

### Panier Mouser BE (~279 €)
| Composant | Qté | Prix |
|-----------|-----|------|
| SPC560B-DIS (MCU) | 1 | 95,03 € |
| VSLY3850 (LED 850nm) | 10 | ~8 € |
| VSLB3940 (LED 940nm) | 10 | ~9 € |
| EKMB1303111K (PIR) | 1 | ~20 € |
| SPH0645LM4H-B (Micro) | 2 | ~8 € |
| TPS62840DLCR (Buck) | 5 | ~13 € |
| Keystone 2463 (Holder AA) | 4 | ~14 € |
| 744043100 (Inductance) | 5 | ~3 € |
| MSP06A0110K0GEJ (Passifs) | 10 | ~6 € |
| PMV16XN (MOSFET) | 5 | ~3 € |
| nRF-PPK2 | 1 | ~100 € |
| **Total Mouser** | | **~279 €** |

### Panier DigiKey BE (~54 €)
| Composant | Qté | Prix |
|-----------|-----|------|
| Swissbit S-45U 16 GB (microSD) | 3 | ~54 € |

### Arducam officiel (~22 €)
| Composant | Qté | Prix |
|-----------|-----|------|
| OV5640 DVP M12 (caméra) | 1 | ~22 € |

### Amazon.de / Conrad (~78 €)
| Composant | Qté | Prix |
|-----------|-----|------|
| RD UM24C (Alim labo USB) | 1 | ~35 € |
| Breadboard + câbles | 2 | ~14 € |
| Energizer L91 AA × 16 | 16 | ~29 € |

---

## Total consolidé

| Poste | Montant |
|-------|---------|
| Panier Mouser | ~279 € |
| Panier DigiKey | ~54 € |
| Arducam | ~22 € |
| Amazon.de / retail | ~78 € |
| **Sous-total composants** | **~433 €** |
| Frais de port estimés | ~50 € |
| Option B (terrain compact) | ~203 € |
| Réserve / marge | ~50 € |
| **Total projeté** | **~736 €** |
| Enveloppe P0 | 1 000 € |
| **Marge restante** | **~264 €** |

---

## Actions requises pour débloquer

### 🔴 À faire par JCH
- ✅ **PPK2** — reçu et utilisé. M-02 débloqué.

### 🟡 À faire par [[Dobby]]
- [ ] **Contacter Arducam** — [[email]] pour confirmation OV5640 DVP M12 (pinout, NoIR, monture)
- [ ] **Demander devis Lensation** — 2× lentille M12 f/1.8 IR-corrigée
- [ ] **Confirmer stock EKMB1303111K** sur Mouser BE au moment de la commande groupée
- [ ] **Confirmer stock Swissbit S-45U** sur DigiKey BE au moment de la commande

### 🟡 À faire par [[Forge]]
- [ ] **Grouper et passer le panier Mouser** (11 composants, ~279€)
- [ ] Supply register

---

## Décisions en attente JCH

- ✅ **PPK2** : reçu et opérationnel — M-02 actif
- **Validation panier Mouser groupé** : 11 composants pour ~279€ — prêt à commander (PPK2 déjà déduit)
- ✅ **Arducam** : gelé (MOQ 10). OV5640 dispos en stock — on avance avec l'existant.

---

*Aucune commande ne sera passée sans validation explicite JCH.*  
*Prix vérifiés le 2026-05-23 sur Mouser/DigiKey/RAK Store — à confirmer au moment de la commande.*

---

## Matériel reçu — état au 2026-07-06

| # | Composant | Qté | Date réception | Statut |
|---|-----------|-----|---------------|--------|
| R00 | Nordic PPK2 | 1 | ~10/06 | ✅ REÇU |
| R01 | ESP32-CAM OV2640 (cartes seules) | 4 | 23/06 | ✅ REÇU |
| R02 | USB-C TTL FT232RL | 3 | 21/06 | ✅ REÇU |
| R03 | ESP32-S3-DevKitC-1 N16R8 | 2 | ~15/06 | ✅ REÇU |
| R04 | ESP32-CAM OV2640 (modules caméra) | 2 | 21/06 | ✅ REÇU |
| R05 | OV5640 DVP M12 | 5 | 12/06 + 24/06 | ✅ REÇU |
| R06 | Mouser #39492997 (partiel) | 1 colis | ~20/06 | ⏳ BACKORDER — TPS62840DLCR ETA 15/07 |
| R07 | MP1584 DC-DC Step Down 3A | 5 | 03/07 | ✅ REÇU |
| R08 | ADS1115 ADC Module | 3 | 02/07 | ✅ REÇU (IoT) |
| R09 | ESP32-C3 Super Mini | 3 | 02/07 | ✅ REÇU (IoT) |
| R10 | PV PI HAT | 1 | 01/07 | ✅ REÇU (IoT — 6 semaines d'avance) |

**Notes :**
- Les ESP32-CAM OV2640 servent au prototypage firmware caméra DVP — l'OV5640 (5MP) est le capteur final P0
- Panier Mouser restant (~279€, 11 composants BOM) : comprend RAK3172 LoRa, antennes, connecteurs, etc.
- Bloqueur Mouser : TPS62840DLCR (buck faible Iq) — ETA 15/07 → commande groupée après cette date
- SD 128 GB à acheter (~15€) pour stockage audio/photo terrain (ADR-017)
