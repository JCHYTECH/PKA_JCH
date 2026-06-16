# WildNexus WP02 — Shortlist achat P0 v0.2

**Date :** 2026-06-12  
**Statut :** actif — enrichi suite analyse [[inbox]] (D1–D4) et arbitrages JCH du 2026-06-12  
**Owner :** [[Dobby]] + [[Forge]] + [[Bruno]] + [[Castor]]  
**Référence :** [WP02 hardware matrix v0.1] + [WP01 architecture freeze] + [SUPPLY_REGISTER v0.3] + [BUDGET v0.2] + [Synthèse [[inbox]] 2026-06-12] + [Rapport [[Castor]]+Fourmi OV5640/LoRa]  
**Version précédente :** `2026-05-23_WP02_shortlist_achat_P0_v0.1.md` (backup `.bak-2026-06-12`)  
**Enveloppe :** 1 000 € max — dépassement bloquant sauf décision JCH  

---

## 1. Objet

Ce document traduit la matrice hardware WP02 en liste d'achats concrète, organisée en deux options parallèles :

| Option | But | Quand commander |
|--------|-----|-----------------|
| **A — Banc rapide** | Mesurer l'énergie réelle, valider le flux capture/stockage/[[LoRa]]/sleep sur DevKit ouvert | En premier — sans attendre le boîtier |
| **B — Additions terrain compact** | Ajouter les composants qui convergent vers le proto terrain : lentille définitive, boîtier IP67, [[LoRa]] module final, antenne discrète, station de base | Après résultats M-02 partiels sur le banc |

Les deux options sont budgétées dans l'enveloppe 1 000 €.  
L'outillage (PPK2) est prioritaire et fait partie d'Option A.

---

## 2. Option A — Banc rapide

### 2.1 Tableau de commande

| # | Composant | Référence précise | Fournisseur recommandé | Lien / Recherche | Qté | Prix unit. livré BE (est.) | Total (est.) | Délai | Risque supply | Note |
|---|-----------|-------------------|------------------------|------------------|-----|---------------------------|--------------|-------|----------------|------|
| A01 | MCU prototype | **ESP32-S3-DevKitC-1-N8R8** (8 MB flash, 8 MB PSRAM, USB-C) | **Mouser BE** | Mouser ref 595-ESP32-S3-DEVKITC-1 | 2 | ~16 € | ~32 € | 3–5 j | 🟢 Bas | Acheter 2 pour banc M-02 redondant |
| A02 | Caméra capteur | ~~Camemake CM_DVP_OV5640_UNIVERSAL~~ — **REJETÉ** (MOQ 10, commande refusée 2026-06-14) | — | — | — | — | — | — | 🔴 Rejeté | Remplacé par A02a (ESP32-CAM) pour dév DVP + A02b (OV5640 AliExpress) pour capteur final. |
| **A02a** 🆕 | **Caméra dév DVP** | **ESP32-CAM** (AI-Thinker, OV2640 2MP DVP, LED flash, slot SD onboard) | **Amazon BE / AliExpress** | "ESP32-CAM OV2640" | 1 | ~10 € | ~10 € | 3–7 j | 🟢 Bas | Outil de développement DVP uniquement — pas le capteur final. Permet de valider l'intégration DVP sans attendre OV5640. |
| **A02b** 🆕 | **Caméra finale P0** | **OV5640 DVP M12 24-pin** (5MP, NoIR, M12 mount) | **AliExpress** | "OV5640 DVP M12 24-pin NoIR" | 2 | ~15 € | ~30 € | 15–25 j | 🟡 Moyen | Fallback du supply register. Commander maintenant — arrivera après les tests DVP initiaux. Vérifier : DVP (pas MIPI), 24-pin, M12 mount, NoIR (sans filtre IR-cut). |
| **A02c** 🆕 | **Level shifter DVP** | **Level shifter 8 canaux 3.3V ↔ 1.8/2.8V** (e.g. TXS0108E ou TXB0108) | **AliExpress** | "level shifter 8ch 3.3V 1.8V" | 2 | ~3 € | ~6 € | 10–20 j | 🟢 Bas | Ajout 2026-06-14 — OV5640 peut nécessiter adaptation tension I/O (1.8V/2.8V → 3.3V ESP32-S3). Commander avec A02b. |
| A03 | LED IR 850 nm | ~~Vishay VSLY3850~~ — **RETIRÉ** (décision JCH 2026-06-12 : 850nm perceptible faune) | — | — | — | — | — | — | — | IR 940nm uniquement (A04). |
| A04 | LED IR 940 nm | **Vishay VSLB3940** (×4 par nœud) | **Mouser BE** | Mouser ref "VSLB3940" | 10 | ~0,37 € | ~4 € | 3–5 j | 🟢 Bas | Prix réel Mouser 2026-06-12 : 0,37€/pièce. |
| A05 | PIR basse conso | **Panasonic EKMB1203111** (FOV 86°H × 84°V, 2–3 µA, EKMB1303111 indispo) | **Mouser BE** | Mouser ref "EKMB1203111" | 2 | ~22 € | ~44 € | 5–8 j | 🟢 Bas | Prix réel vérifié Mouser 2026-06-12 : 22,30€/pièce. EKMB1303111 ∼5€ estimé erroné — retiré. |
| A06 | Micro MEMS I2S | **Knowles SPH0645LM4H-B** (PDM I2S, −26 dBFS, 3 V) | **Mouser BE** | Mouser ref "SPH0645LM4H-B" | 2 | ~4 € | ~8 € | 3–7 j | 🟢 Bas | Alternative : ICS-43434 (TDK/InvenSense) même fournisseur |
| A07 | microSD | **M-02 : SanDisk Extreme 32GB (~10€)** / **M-03 : Swissbit pSLC (~49€)** | Local / Amazon | — | 3 | ~10 € | ~30 € | Immédiat | 🟢 Bas | Banc labo → consumer OK. Terrain → Swissbit SFSD016GN1AM1TB-E. Prix Swissbit vérifié Mouser BE 2026-06-12 : 49€/carte. |
| A08 | Buck faible Iq | **TPS62840DLCR** (Iq 60 nA, 2,5–5,5 V in, 3 V out, 750 mA) | **Mouser BE** | Mouser ref "TPS62840DLCR" | 5 | ~2,50 € | ~13 € | 3–5 j | 🟢 Bas | Commander en lot — composant CMS, prévoir pertes soudure |
| A09 | Holder AA × 4 séries | **Keystone 2463** (4× AA side-by-side, 6 V, fils) × 2 par nœud | **RS Belgium ou Mouser BE** | RS ref "Keystone 2463" | 4 | ~3,50 € | ~14 € | 3–7 j | 🟢 Bas | 2 holders × 4 AA = 8 AA en 2 blocs parallèles, câblage 4S2P externe |
| A10 | Inductance buck | **Würth 744043100** (10 µH, 1 A, 3 × 3 mm) | **Mouser BE** | Mouser ref "744043100" | 5 | ~0,60 € | ~3 € | 3–5 j | 🟢 Bas | Associée TPS62840 ; choisir selon layout PCB |
| A11 | Capacités + résistances | Lot CMS 0402/0603 : C 100nF, 10µF, 1µF ; R 10K, 100K, 1M | **Mouser BE** | Panier passifs 0402/0603 | 1 lot | ~20 € | ~20 € | 3–5 j | 🟢 Bas | Lot prototypage — couvre buck, micro, PIR, LED driver |
| A12 | MOSFET power gating | **Nexperia PMV16XN** (N-ch, SOT-23, 60 mA gate cap) ou **SI2302** | **Mouser BE** | Mouser "PMV16XN" | 5 | ~0,50 € | ~3 € | 3–5 j | 🟢 Bas | Power gating caméra/IR/[[LoRa]]. **OBLIGATOIRE** — OV5640 consomme en standby logiciel (confirmé D4) |
| A13 | **Nordic PPK2** (mesure courant) | **Nordic Power Profiler Kit II** | **Nordic Semi shop EU** ou **Mouser BE** | nordic.com/en/products/evaluation-tools/ppk2 | 1 | ~100 € | **~100 €** | 5–10 j | 🟢 Bas | ⚠️ **Non négociable** — sans PPK2, ADR-005 non vérifiable |
| A14 | Breadboard + câbles Dupont | Kit proto (830 pts + câbles) — **couvert par Miuzei Kit (reçu)** | — | — | — | — | — | — | — | Déjà reçu 2026-06-10. |
| **A15** | ~~Alimentation labo~~ | **RETIRÉ** (2026-06-12) — PPK2 fait source + mesure, ESP32-S3 alimenté USB-C. Aucun besoin. | — | — | — | — | — | — | — | Économie 35€. |
| A16 | Piles AA lithium (test) | **Energizer Ultimate Lithium L91** AA × 16 | Carrefour / Action / Amazon.be | — | 16 | ~1,80 € | ~29 € | Immédiat | 🟢 Bas | 16 piles = 2 nœuds 8 AA chacun. Lithium = test autonomie crédible froid |
| **A17** 🆕 | **Dissipateur adhésif OV5640** | Mini radiateur alu autocollant 14×14×5 mm ou bande adhésive thermique | **Mouser BE / Amazon** | Mouser "heatsink adhesive 14mm" | 4 | ~1 € | ~4 € | 3–5 j | 🟢 Bas | **Ajout 2026-06-12** — OV5640 chauffe en actif (D4 + 22 29 14). Prévenir throttling en boîtier fermé. |
| **A18** 🆕 | **Lentille M12 2.8mm NoIR f/1.8** | Objectif grand angle M12, NoIR (sans filtre IR-cut), ouverture f/1.8, champ ~90-100° | **Arducam / Lensation** | arducam.com "M12 2.8mm NoIR" | 2 | ~25 € | ~50 € | 5–10 j | 🟡 Moyen | **Ajout 2026-06-12** — Tests comparatifs focaux au banc M-02 : 2.8mm (coulée, 1-5m) vs 6mm (télé, 5-12m). Source : D4 + 22 29 50. |
| **B05** | BME688 capteur env. | **Bosch BME688** (T/P/H/gaz, I2C/SPI) | **Mouser BE** | Mouser ref "BME688" | 2 | ~7,44 € | ~15 € | 3–7 j | 🟢 Bas | **Déjà commandé** Mouser #39492997. |
| **B06** | SHT31-DIS humidité | **Sensirion SHT31-DIS-B** (±2% RH, I2C) | **Mouser BE** | Mouser ref "SHT31-DIS-B" | 2 | ~3,87 € | ~8 € | 3–5 j | 🟢 Bas | **Déjà commandé** Mouser #39492997. |

**Sous-total Option A estimé : ~446 €** *(v0.2 : ~450 € ; −4 € sur A02)*

Lentille 2.8mm (A18) : ne pas confondre avec B01 (6mm). Les deux focales sont nécessaires pour les tests comparatifs M-02.

---

## 3. Option B — Additions proto terrain compact

À commander après premiers résultats M-02 sur banc (mesures énergétiques OK, flux capture/stockage validé).

| # | Composant | Référence précise | Fournisseur recommandé | Lien / Recherche | Qté | Prix unit. livré BE (est.) | Total (est.) | Délai | Risque supply | Note |
|---|-----------|-------------------|------------------------|------------------|-----|---------------------------|--------------|-------|----------------|------|
| B01 | Lentille M12 IR-corrigée | **Lensation LS-6028** f/1.8, 6 mm, IR-corrected, M12 — ou **Evetar M12B0618W-IR** f/1.8, 6 mm | **Lensation.de** priorité | lensation.de "M12 f/1.8 IR" | 2 | ~35–45 € | **~80 €** | 5–10 j | 🟡 Moyen | ⚠️ **Ne pas descendre sous 30 €/lentille** — qualité nuit critique. Demander devis avant commande. Ne pas acheter lentille fixe collée sans filetage M12. |
| B02 | Module [[LoRa]] P0 nœud | **RAK3172-T EU868** (SX1262, CE certifié, IPEX, −40/+85°C) | **RAK Store EU** (store.rakwireless.com) | RAK ref "RAK3172-T" EU868 | 2 | ~14 € | ~28 € | 5–10 j | 🟢 Bas | Vérifier variante EU868 + IPEX explicite. Alternative : Murata Type 1SJ chez Mouser si stock RAK en rupture. |
| B03 | Antenne [[LoRa]] 868 MHz | **[[LoRa]] flex antenna 868 MHz IPEX** — Molex 211140-0100, ~100mm | **Mouser BE** | Mouser ref "211140-0100" | 2 | ~4 € | ~8 € | 3–7 j | 🟢 Bas | **Déjà commandé** Mouser #39492997. |
| B04 | Boîtier IP67 P0 | **Hammond 1554B** (188×120×78 mm) ou **Hammond 1554A** (150×100×60 mm) — ABS/PC, IP67 | **RS Belgium** ou **Mouser BE** | RS "Hammond 1554A" | 1–2 | ~16 € | ~25 € | 3–7 j | 🟡 Moyen | Commander après layout interne Option A validé. Vérifier volume utile réel (pas dimensions externes). Couleur grise ou noire en base + peinture verte terrain. Note : boîtier P1 sera impression 3D forme organique avec dos arrondi et ajouts camouflage (décision JCH 2026-05-25) — hors budget P0. |
| B07 | Connecteur étanche micro | **Conxall Mini-Con-X 3 brins** ou presse-étoupe M16 IP68 | **RS Belgium / Mouser** | RS "presse-étoupe M16 nylon" | 4 | ~2 € | ~8 € | 3–7 j | 🟢 Bas | Passage câble sangle/antenne externe si antenne fouet obligatoire |
| B08 | Silica gel + joints | Sachet 5g silica gel × 10 + joint torique EPDM 140×3 | Conrad / Amazon.be | — | 1 lot | ~10 € | ~10 € | Immédiat | 🟢 Bas | Maintenance terrain, boîtier IP67 |
| B09 | Sangle UV terrain | Sangle polyester UV 20 mm × 50 cm + boucle inox | Conrad / Camping matériau | — | 4 | ~4 € | ~16 € | Immédiat | 🟢 Bas | Fixation tronc |
| **B10** 🆕 | **LILYGO T-Beam 1W SX1262** | LILYGO T-Beam SUPREME 1W (SX1262, +32 dBm, ESP32-S3, GPS, 868 MHz) — station de base LoRa | **LILYGO officiel** (lilygo.cc) ou **AliExpress LILYGO store** | lilygo.cc "T-Beam 1W 868" | 1 | ~35 € | ~35 € | 10–15 j | 🟡 Moyen | **Ajout 2026-06-12** — Station de base haute puissance réception LoRa. Recommandé D4 pour portée 3-5km en montagne. Vérifier variante EU868. Budget restant : ~177 €. |

**Sous-total Option B (additions) estimé : ~238 €** *(v0.1 : ~203 € ; +35 € pour B10)*

---

## 4. Budget consolidé

| Bloc | v0.1 | v0.2 | Δ |
|------|------|------|---|
| Option A — Banc rapide | ~396 € | **~452 €** | +56 € |
| Option B — Additions terrain | ~203 € | **~238 €** | +35 € |
| Frais de port (Mouser + DigiKey + RAK + Lensation + LILYGO) | ~50 € | ~55 € | +5 € |
| Marge casse / reprise composants | ~80 € | ~80 € | — |
| **Total estimé A + B** | **~729 €** | **~829 €** | +100 € |
| **Réserve restante (enveloppe 1 000 €)** | **~271 €** | **~171 €** | −100 € |

> ⚠️ Tout achat individuel > 50 € doit être signalé à JCH avant commande (règle BUDGET v0.2).  
> ⚠️ Si total projeté > 900 €, stopper et arbitrer. (v0.2c : 829 €, sous le seuil)

---

## 5. Stratégie de paniers recommandée

| Panier | Fournisseur | Contenu | Seuil livraison gratuite |
|--------|-------------|---------|--------------------------|
| Panier 1 | **Mouser BE** | A01 MCU, A03–A07 capteurs/micro/LED, A08–A12 passifs/buck/MOSFET, A17 dissipateur, B05–B06 capteurs env., B03 antenne | ~50 € (à confirmer) |
| Panier 2 | **Amazon BE / AliExpress** | A02a ESP32-CAM OV2640 | Commande séparée, livraison rapide |
| Panier 3 | **AliExpress** | A02b OV5640 DVP M12 24-pin NoIR | Commander immédiatement — délai 15-25j |
| Panier 4 | **RAK Store EU** | B02 RAK3172-T EU868 | Livraison directe EU |
| Panier 5 | **Lensation.de** | B01 lentille M12 IR-corrigée 6mm | Demander devis 2 pièces |
| Panier 6 | **RS Belgium** | A09 holders AA, B04 boîtier Hammond, B07 presse-étoupe | Livraison rapide BE |
| Panier 7 | **Nordic Semi shop** | A13 PPK2 | Livraison directe EU |
| **Panier 8** 🆕 | **LILYGO officiel** | B10 T-Beam 1W 868 MHz | Livraison directe ; délai 10-15j |

---

## 6. Composants NON retenus (arbitrages JCH 2026-06-12)

| Composant | Source | Raison du rejet | Décision |
|-----------|--------|-----------------|----------|
| Heltec WiFi LoRa 32 V3 (ESP32-S3 + SX1262 intégré) | D4 | Redondant avec A01+B02. Plus compact mais n'apporte rien de critique pour P0. | **Non retenu P0** — référence P1 |
| STM32U5 / Nordic nRF54 (MCU alternatif) | D1 §5.2 | ADR-001 a tranché ESP32-S3. D1 mentionne mais ne recommande pas pour P0. | **Non retenu** — ADR-001 confirmé |
| Bioacoustique (micro DSP, classification audio) | D1 §10 | D1 recommande produit séparé. Consommation, complexité, volume données. | **Non retenu P0** — P1 produit distinct |
| Objectif M12 vari-focal 2.8-12mm motorisé (Arducam) | 22 29 33 | Bruit moteur, conso, complexité code. Le vari-focal manuel suffit pour tests. | **Non retenu P0** — option P1 si besoin terrain |
| Arducam B0533/B0530 OV5640 MIPI-CSI | Arducam.com | Modules MIPI-CSI only (Toradex/Renesas) — pas de DVP, incompatibles ESP32-S3. | **Non retenu P0** — interface MIPI non native ESP32-S3 |
| Arducam B0158 OV5640D AF | Welectron | Interface SPI/I2C (ArduCAM shield) — pas de DVP natif, inutilisable sur ESP32-S3. | **Non retenu P0** — interface SPI incompatible |
| Arducam CU450 OV5640 DVP+MIPI | Zephyr docs | A du DVP mais connecteur 40-pin FFC propriétaire (Renesas EK-RA8P1) — nécessite breakout. | **Non retenu P0** — connecteur non standard |

---

## 7. Composants différés (hors périmètre P0)

| Composant | Raison | Quand |
|-----------|--------|-------|
| ESP32-S3-WROOM-1U module (PCB final) | Après validation DevKit banc | WP02 phase 2 / PCB v0.1 |
| AS7341 capteur spectral | Réserve optionnelle P0 | Si BME688 insuffisant faune |
| Quectel SIM7080G + SIM 1NCE | LTE-M différé P1 | WP05+ |
| [[Raspberry Pi 5]] + SSD | Base/Master Nexus P1 | WP06 |
| Panneau solaire + CN3791 | P1 seulement | Hors P0 |
| PCB dédié custom | WP02 phase 2 | Après mesures M-02 |
| **Arducam IMX500 AI Camera (B0642)** 🆕 | Sony 12.3MP, IA on-chip (DSP intégré), double interface SPI+MIPI. Inférence sur capteur — plus besoin d'Edge AI sur MCU. Candidat P1 pour remplacer OV5640 + classifieur ESP32-S3. Prix ~60-80 €. | WP05 — après validation P0 |
| Impression 3D boîtier bio | P1 seulement | Hors budget P0 |
| Relais solaire Meshtastic (Heltec V3 + panneau) | Concept P1 | WP05+ |

---

## 8. État ADR et impact shortlist

| ADR | Statut | Impact sur la shortlist |
|-----|--------|------------------------|
| ADR-001 [[ESP32-S3]] | ✅ Accepté | A01 — DevKit commandé directement |
| ADR-002 Caméra OV5640/IR | ✅ Accepté | A02 + B01 (6mm) + A18 🆕 (2.8mm tests comparatifs) |
| ADR-003 [[LoRa]] P2P EU868 | ✅ Accepté | B02 RAK3172-T + B10 🆕 LILYGO T-Beam 1W (station base) |
| ADR-004 microSD industrielle | ✅ Accepté | A07 — Swissbit DigiKey |
| ADR-005 AA + buck faible Iq | ✅ Accepté | A08–A10 + A09 holders + A16 piles L91 |
| ADR-006 Boîtier IP67 | ✅ Accepté (2026-05-25) | B04 — Hammond P0 ; impression 3D forme organique retenue P1 (hors budget P0) |
| ADR-007 Détection événementielle PIR | ✅ Accepté | A05 — Panasonic EKMB |
| ADR-008 Interface capteurs extensible | ✅ Accepté | A06 micro + B05–B06 réserve capteurs |
| ADR-009 Architecture Satellite/Base/Cloud | ✅ Accepté | B10 🆕 T-Beam 1W = station base physique |
| ADR-010 Sécurité/RGPD Edge AI | ✅ Accepté ss réserve | R4/R5 → M-02 |
| ADR-011 Provisioning clés | Proposé | Pas d'achat P0 |

---

## 9. Prochaine action

1. **JCH valide la liste Option A v0.2** — ou signale un composant à modifier avant de commander.
2. **[[Forge]]** groupe le panier Mouser (A01 + A03–A12 + A17 + B03 + B05–B06) et vérifie disponibilité stock à date.
3. **[[Bruno]]** vérifie le total livré réel (frais de port, TVA, délais) avant validation financière.
4. **Commande PPK2** (A13) en priorité absolue — Nordic Semi shop EU ou Mouser.
5. **Commander A02** — Camemake CM_DVP_OV5640_UNIVERSAL × 2 sur DigiKey BE. Vérifier stock et délai.
6. **Demander devis Lensation** (B01) — 2 lentilles M12 f/1.8 IR-corrigées — avant tout achat lentille.
7. **Commander LILYGO T-Beam 1W** (B10) — délai 10-15j, anticiper pour M-02.
8. **Sourcer A18** — lentille M12 2.8mm NoIR f/1.8. Si Arducam indisponible, chercher alternative Lensation ou Evetar.
9. Après M-02 banc validé → commander Option B complète sur la base du layout interne réel.

---

## 10. Historique des versions

| Version | Date | Auteur | Changements |
|---------|------|--------|-------------|
| v0.1 | 2026-05-23 | [[Dobby]] + [[Forge]] + [[Bruno]] | Version initiale — Option A 396€ + Option B 203€ |
| v0.2 | 2026-06-12 | [[Dobby]] + [[Castor]] + [[Sigma]] | +A17 dissipateur OV5640, +A18 lentille 2.8mm NoIR, +B10 LILYGO T-Beam 1W. Arbitrages JCH : Heltec/STM32U5/bioacoustique rejetés P0. Budget : 823€ (−177€ réserve). |
| v0.2a | 2026-06-12 | [[Dobby]] + JCH | A02 remplacé Arducam→Camemake (DVP M12 dispo DigiKey). Modules Arducam MIPI-only et SPI documentés comme rejetés. IMX500 ajouté en P1 différé. Option A : 446€ (−4€). Budget : 819€ (−181€ réserve). |
| v0.2c | 2026-06-14 | [[Dobby]] + JCH | A02 Camemake rejeté (MOQ 10). Remplacé par A02a ESP32-CAM OV2640 (dév DVP, ~10€) + A02b OV5640 DVP M12 AliExpress (final, ~30€). Budget inchangé (~823€). Panier DigiKey libéré. |
| v0.3 | 2026-06-12 | [[Dobby]] + JCH | Index procurement Mouser/DigiKey (§11). Réfs vérifiées session. Pipeline : primaire Mouser, fallback DigiKey, indispo → signaler. |

---

## 11. Index procurement — Réfs Mouser / DigiKey

> **Règle** : chaque ligne a une réf primaire + un fallback. Si indispo → [[Dobby]] signale, ne met jamais une ligne vide.
> **Import** : CSV `mouser_bom.csv` et `digikey_bom.csv` dans `07_PROCUREMENT_BOM/`.

### 11.1 Option A — Banc rapide

| # | Composant | Réf Mouser | Réf DigiKey | Statut |
|---|-----------|-----------|-------------|--------|
| A01 | ESP32-S3 DevKit | `595-ESP32-S3-DEVKITC-1` | `1965-ESP32-S3-DEVKITC-1-N8R8-ND` | ✅ Reçu |
| A02 | OV5640 DVP M12 | — | `6223-CM_DVP_OV5640_UNIVERSAL-ND` | 🔴 DigiKey |
| A03 | LED IR 850nm | `VSLY3850` | `751-VSLY3850` | ✅ Vérifié |
| A04 | LED IR 940nm | `VSLB3940` | `78-VSLB3940` | ✅ Vérifié |
| A05 | PIR EKMB | `EKMB1203111` | `769-EKMB1203111` | 🔴 EKMB1303111 indispo → 1203111 |
| A06 | Micro MEMS | `MMICT5848-00-012` | `410-MMICT5848-00-012` | ✅ ICS-43434 EOL → remplacé |
| A07 | microSD Swissbit | `922-603400` | `1052-S-45U-16GB-ND` | 🔴 DigiKey prio |
| A08 | Buck TPS62840 | `TPS62840DLCR` | `296-TPS62840DLCRCT-ND` | ✅ Vérifié |
| A09 | Holder 4×AA | `534-2463` | `36-2463-ND` | 🔴 RS prioritaire |
| A10 | Inductance 10µH | `744043100` | `732-2146-1-ND` | ✅ Vérifié |
| A11 | Kit passifs CMS | `KIT-14585` | `1568-KIT-14585-ND` | ✅ Vérifié |
| A12 | MOSFET N-ch | `SI2302CDS-T1-GE3` | `742-SI2302CDS-T1-GE3CT-ND` | ✅ PMV16XN indispo → remplacé |
| A13 | PPK2 | `949-NRF-PPK2` | `1490-PPK2-ND` | ✅ Reçu |
| A14 | Breadboard + câbles | — | — | ✅ Reçu (Miuzei Kit) |
| A15 | Alim labo USB | — | — | 🟡 Amazon |
| A16 | Piles L91 AA | — | — | 🟡 Local |
| A17 | Dissipateur 14mm | `ATS-HK127-R0` | `684-ATS-HK127-R0-ND` | ✅ Vérifié |
| A18 | Lentille 2.8mm NoIR | — | — | ⚠️ Chercher Lensation/Evetar |

### 11.2 Option B — Additions terrain

| # | Composant | Réf Mouser | Réf DigiKey | Statut |
|---|-----------|-----------|-------------|--------|
| B01 | Lentille 6mm IR f/1.8 | — | — | 🟡 Devis Lensation.de |
| B02 | RAK3172-T EU868 | — | — | 🟡 RAK Store EU |
| B03 | Antenne LoRa 868MHz | `211140-0100` | `23-211140-0100` | ✅ Vérifié |
| B04 | Boîtier Hammond IP67 | `546-1554A` | — | 🔴 RS prioritaire |
| B05 | BME688 | `BME688` | `828-BME688-ND` | ✅ Vérifié |
| B06 | SHT31-DIS | `SHT31-DIS-B` | `1649-SHT31-DIS-B-ND` | ✅ Vérifié |
| B07 | Presse-étoupe M16 | — | — | 🔴 RS |
| B08 | Silica gel + joints | — | — | 🟡 Amazon |
| B09 | Sangle UV terrain | — | — | 🟡 Amazon |
| B10 | LILYGO T-Beam 1W | — | — | 🟡 LILYGO officiel |

### 11.3 CSV d'import

| Fichier | Contenu | Statut |
|---------|---------|--------|
| `mouser_bom.csv` | A03–A12, A17, B03, B05–B06 (13 lignes, refs vérifiées) | ✅ Prêt |
| `digikey_bom.csv` | A02, A07 | 🔴 À créer |