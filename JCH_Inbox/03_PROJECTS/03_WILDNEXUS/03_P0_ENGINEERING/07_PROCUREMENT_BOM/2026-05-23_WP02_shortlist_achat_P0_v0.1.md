# WildNexus WP02 — Shortlist achat P0 v0.1

**Date :** 2026-05-23  
**Statut :** actif — prix vérifiés le 2026-05-23, corrections intégrées (§10)  
**Owner :** Dobby + Forge + Bruno  
**Référence :** [WP02 hardware matrix v0.1] + [WP01 architecture freeze] + [SUPPLY_REGISTER v0.3] + [BUDGET v0.2]  
**Enveloppe :** 1 000 € max — dépassement bloquant sauf décision JCH  

---

## 1. Objet

Ce document traduit la matrice hardware WP02 en liste d'achats concrète, organisée en deux options parallèles :

| Option | But | Quand commander |
|--------|-----|-----------------|
| **A — Banc rapide** | Mesurer l'énergie réelle, valider le flux capture/stockage/LoRa/sleep sur DevKit ouvert | En premier — sans attendre le boîtier |
| **B — Additions terrain compact** | Ajouter les composants qui convergent vers le proto terrain : lentille définitive, boîtier IP67, LoRa module final, antenne discrète | Après résultats M-02 partiels sur le banc |

Les deux options sont budgétées dans l'enveloppe 1 000 €.  
L'outillage (PPK2) est prioritaire et fait partie d'Option A.

---

## 2. Option A — Banc rapide

### 2.1 Tableau de commande

| # | Composant | Référence précise | Fournisseur recommandé | Lien / Recherche | Qté | Prix unit. livré BE (est.) | Total (est.) | Délai | Risque supply | Note |
|---|-----------|-------------------|------------------------|------------------|-----|---------------------------|--------------|-------|----------------|------|
| A01 | MCU prototype | **ESP32-S3-DevKitC-1-N8R8** (8 MB flash, 8 MB PSRAM, USB-C) | **Mouser BE** | Mouser ref 595-ESP32-S3-DEVKITC-1 | 2 | ~16 € | ~32 € | 3–5 j | 🟢 Bas | Acheter 2 pour banc M-02 redondant |
| A02 | Caméra capteur | **OV5640 5MP DVP M12 — Arducam B0253 ou module DVP documenté** | **Arducam officiel** (arducam.com) | Rechercher "OV5640 DVP M12" sur arducam.com | 2 | ~22 € | ~44 € | 5–10 j | 🟡 Moyen | Vérifier : DVP explicite, NoIR ou IR-cut géré, M12, pinout dispo. Ne pas acheter marketplace sans fiche. |
| A03 | LED IR 850 nm | **Vishay VSLY3850** (×4 par nœud) | **Mouser BE** | Mouser ref "VSLY3850" | 10 | ~0,80 € | ~8 € | 3–5 j | 🟢 Bas | Test terrain 850 nm en premier |
| A04 | LED IR 940 nm | **Würth WL-SIRW 940 nm** ou **Vishay VSLB3940** | **Mouser BE** | Mouser "940nm IR LED through-hole" | 10 | ~0,90 € | ~9 € | 3–5 j | 🟢 Bas | Test comparatif faune avec 850 nm ; ne pas figer avant mesures |
| A05 | PIR basse conso | **Panasonic EKMB1303111** (FOV 86°H × 84°V, 2–3 µA) | **Mouser BE** | Mouser ref "EKMB1303111" | 2 | ~5 € | ~10 € | 5–8 j | 🟢 Bas | Confirmer FOV avec design boîtier avant commande définitive |
| A06 | Micro MEMS I2S | **Knowles SPH0645LM4H-B** (PDM I2S, −26 dBFS, 3 V) | **Mouser BE** | Mouser ref "SPH0645LM4H-B" | 2 | ~4 € | ~8 € | 3–7 j | 🟢 Bas | Alternative : ICS-43434 (TDK/InvenSense) même fournisseur |
| A07 | microSD industrielle | **Swissbit S-45U 16 GB** (pSLC, −40/+85°C, endurance) | **DigiKey BE** | DigiKey "Swissbit S-45U 16GB" | 3 | ~18 € | ~54 € | 3–7 j | 🟡 Moyen | Ne pas acheter carte consumer. Alternative : Transcend TS16GUSD350V (DigiKey). Acheter 3 : 2 nœuds + 1 spare |
| A08 | Buck faible Iq | **TPS62840DLCR** (Iq 60 nA, 2,5–5,5 V in, 3 V out, 750 mA) | **Mouser BE** | Mouser ref "TPS62840DLCR" | 5 | ~2,50 € | ~13 € | 3–5 j | 🟢 Bas | Commander en lot — composant CMS, prévoir pertes soudure |
| A09 | Holder AA × 4 séries | **Keystone 2463** (4× AA side-by-side, 6 V, fils) × 2 par nœud | **RS Belgium ou Mouser BE** | RS ref "Keystone 2463" | 4 | ~3,50 € | ~14 € | 3–7 j | 🟢 Bas | 2 holders × 4 AA = 8 AA en 2 blocs parallèles, câblage 4S2P externe |
| A10 | Inductance buck | **Würth 744043100** (10 µH, 1 A, 3 × 3 mm) | **Mouser BE** | Mouser ref "744043100" | 5 | ~0,60 € | ~3 € | 3–5 j | 🟢 Bas | Associée TPS62840 ; choisir selon layout PCB |
| A11 | Capacités + résistances | Lot CMS 0402/0603 : C 100nF, 10µF, 1µF ; R 10K, 100K, 1M | **Mouser BE** | Panier passifs 0402/0603 | 1 lot | ~20 € | ~20 € | 3–5 j | 🟢 Bas | Lot prototypage — couvre buck, micro, PIR, LED driver |
| A12 | MOSFET power gating | **Nexperia PMV16XN** (N-ch, SOT-23, 60 mA gate cap) ou **SI2302** | **Mouser BE** | Mouser "PMV16XN" | 5 | ~0,50 € | ~3 € | 3–5 j | 🟢 Bas | Power gating caméra/IR/LoRa |
| A13 | **Nordic PPK2** (mesure courant) | **Nordic Power Profiler Kit II** | **Nordic Semi shop EU** ou **Mouser BE** | nordic.com/en/products/evaluation-tools/ppk2 | 1 | ~100 € | **~100 €** | 5–10 j | 🟢 Bas | ⚠️ **Non négociable** — sans PPK2, ADR-005 non vérifiable |
| A14 | Breadboard + câbles Dupont | Kit proto (830 pts + câbles) | Amazon.de / Conrad | — | 2 | ~7 € | ~14 € | 3–5 j | 🟢 Bas | Banc ouvert M-02 |
| A15 | Alimentation labo USB | **RD UM24C** ou **Ruideng RD6006** si absent | Amazon.de | — | 1 | ~20–40 € | ~35 € | 3–7 j | 🟢 Bas | Si alimentation labo inexistante chez JCH |
| A16 | Piles AA lithium (test) | **Energizer Ultimate Lithium L91** AA × 16 | Carrefour / Action / Amazon.be | — | 16 | ~1,80 € | ~29 € | Immédiat | 🟢 Bas | 16 piles = 2 nœuds 8 AA chacun. Lithium = test autonomie crédible froid |

**Sous-total Option A estimé : ~396 €**  
*(inclut PPK2, piles, proto matériel)*

---

## 3. Option B — Additions proto terrain compact

À commander après premiers résultats M-02 sur banc (mesures énergétiques OK, flux capture/stockage validé).

| # | Composant | Référence précise | Fournisseur recommandé | Lien / Recherche | Qté | Prix unit. livré BE (est.) | Total (est.) | Délai | Risque supply | Note |
|---|-----------|-------------------|------------------------|------------------|-----|---------------------------|--------------|-------|----------------|------|
| B01 | Lentille M12 IR-corrigée | **Lensation LS-6028** f/1.8, 6 mm, IR-corrected, M12 — ou **Evetar M12B0618W-IR** f/1.8, 6 mm | **Lensation.de** priorité | lensation.de "M12 f/1.8 IR" | 2 | ~35–45 € | **~80 €** | 5–10 j | 🟡 Moyen | ⚠️ **Ne pas descendre sous 30 €/lentille** — qualité nuit critique. Demander devis avant commande. Ne pas acheter lentille fixe collée sans filetage M12. |
| B02 | Module LoRa P0 nœud | **RAK3172-T EU868** (SX1262, CE certifié, IPEX, −40/+85°C) | **RAK Store EU** (store.rakwireless.com) | RAK ref "RAK3172-T" EU868 | 2 | ~14 € | ~28 € | 5–10 j | 🟢 Bas | Vérifier variante EU868 + IPEX explicite. Alternative : Murata Type 1SJ chez Mouser si stock RAK en rupture. |
| B03 | Antenne LoRa 868 MHz | **LoRa flex antenna 868 MHz IPEX** — Molex 0213980100 ou équivalent ~80 mm | **Mouser BE** | Mouser "LoRa antenna 868 IPEX" | 2 | ~4 € | ~8 € | 3–7 j | 🟢 Bas | Antenne interne ; alternative : câble pigtail IPEX → SMA + antenne camouflee branche si RF insuffisant |
| B04 | Boîtier IP67 P0 | **Hammond 1554B** (188×120×78 mm) ou **Hammond 1554A** (150×100×60 mm) — ABS/PC, IP67 | **RS Belgium** ou **Mouser BE** | RS "Hammond 1554A" | 1–2 | ~16 € | ~25 € | 3–7 j | 🟡 Moyen | Commander après layout interne Option A validé. Vérifier volume utile réel (pas dimensions externes). Couleur grise ou noire en base + peinture verte terrain. Note : boîtier P1 sera impression 3D forme organique avec dos arrondi et ajouts camouflage (décision JCH 2026-05-25) — hors budget P0. |
| B05 | BME688 (bloc capteurs réserve) | **Bosch BME688** breakout ou puce CMS | **Mouser BE** | Mouser ref "BME688" | 2 | ~9 € | ~18 € | 3–7 j | 🟢 Bas | Optionnel P0 — réserve mécanique et firmware. Ne pas complexifier M-01/M-02 si budget serré. |
| B06 | SHT31-DIS (surveillance interne boîtier) | **Sensirion SHT31-DIS-B** (±2% RH, ±0,3°C, I2C) | **Mouser BE** | Mouser ref "SHT31-DIS-B" | 2 | ~5 € | ~10 € | 3–5 j | 🟢 Bas | Humidité interne boîtier — détection condensation/silica gel saturé |
| B07 | Connecteur étanche micro | **Conxall Mini-Con-X 3 brins** ou presse-étoupe M16 IP68 | **RS Belgium / Mouser** | RS "presse-étoupe M16 nylon" | 4 | ~2 € | ~8 € | 3–7 j | 🟢 Bas | Passage câble sangle/antenne externe si antenne fouet obligatoire |
| B08 | Silica gel + joints | Sachet 5g silica gel × 10 + joint torique EPDM 140×3 | Conrad / Amazon.be | — | 1 lot | ~10 € | ~10 € | Immédiat | 🟢 Bas | Maintenance terrain, boîtier IP67 |
| B09 | Sangle UV terrain | Sangle polyester UV 20 mm × 50 cm + boucle inox | Conrad / Camping matériau | — | 4 | ~4 € | ~16 € | Immédiat | 🟢 Bas | Fixation tronc |

**Sous-total Option B (additions) estimé : ~203 €**

---

## 4. Budget consolidé

| Bloc | Estimé |
|------|-------:|
| Option A — Banc rapide | ~396 € |
| Option B — Additions terrain | ~203 € |
| Frais de port (Mouser + DigiKey + RAK + Lensation) | ~50 € |
| Marge casse / reprise composants | ~80 € |
| **Total estimé A + B** | **~729 €** |
| **Réserve restante (enveloppe 1 000 €)** | **~271 €** |

> ⚠️ Tout achat individuel > 50 € doit être signalé à JCH avant commande (règle BUDGET v0.2).  
> ⚠️ Si total projeté > 900 €, stopper et arbitrer.

---

## 5. Stratégie de paniers recommandée

| Panier | Fournisseur | Contenu | Seuil livraison gratuite |
|--------|-------------|---------|--------------------------|
| Panier 1 | **Mouser BE** | A01 MCU, A03–A07 capteurs/micro/LED, A08–A12 passifs/buck/MOSFET, B05–B06 capteurs env., B03 antenne | ~50 € (à confirmer) |
| Panier 2 | **DigiKey BE** | A07 microSD Swissbit | 50 € (livraison gratuite ≥ 50 €, sinon ~18 €) |
| Panier 3 | **Arducam officiel** | A02 module caméra OV5640 DVP M12 | Livraison directe EU ; vérifier frais |
| Panier 4 | **RAK Store EU** | B02 RAK3172-T EU868 | Livraison directe EU |
| Panier 5 | **Lensation.de** | B01 lentille M12 IR-corrigée | Demander devis 2 pièces |
| Panier 6 | **RS Belgium** | A09 holders AA, B04 boîtier Hammond, B07 presse-étoupe | Livraison rapide BE |
| Panier 7 | **Nordic Semi shop** | A13 PPK2 | Livraison directe EU |

---

## 6. Points de vigilance procurement

| ⚠️ | Risque | Action |
|----|--------|--------|
| Caméra | Ne pas acheter OV5640 marketplace sans pinout DVP explicite, variante NoIR/IR-cut gérée et format M12 | Contacter Arducam, demander fiche technique avant paiement |
| Lentille | Ne pas descendre sous 30 €/lentille ; lentille fixe collée = risque qualité nuit | Demander devis Lensation/Evetar, pas de commande impulsive marketplace |
| Radio | Toujours vérifier EU868 (863–870 MHz) et antenne adaptée 868 MHz | RAK3172-T : lire variante sur fiche avant achat |
| Batterie | Piles lithium L91 pour test terrain froid ; NiMH eneloop pour tests intérieur | Ne pas relancer LiPo/LiFePO4 P0 — ADR-005 tranché |
| microSD | Industrial grade obligatoire — ne pas utiliser microSD consumer en P0 | Swissbit ou Transcend TS16GUSD350V uniquement |
| PPK2 | Commander en même temps que le premier panier Mouser — bloquant pour M-02 | Priorité absolue |
| Boîtier | Commander après layout interne Option A — ne pas acheter à l'aveugle | Vérifier volume utile intérieur, pas seulement cotes externes |

---

## 7. Composants différés (hors périmètre P0)

| Composant | Raison | Quand |
|-----------|--------|-------|
| ESP32-S3-WROOM-1U module (PCB final) | Après validation DevKit banc | WP02 phase 2 / PCB v0.1 |
| AS7341 capteur spectral | Réserve optionnelle P0 | Si BME688 insuffisant faune |
| Quectel SIM7080G + SIM 1NCE | LTE-M différé P1 | WP05+ |
| Raspberry Pi 5 + SSD | Base/Master Nexus P1 | WP06 |
| Panneau solaire + CN3791 | P1 seulement | Hors P0 |
| PCB dédié custom | WP02 phase 2 | Après mesures M-02 |
| Impression 3D boîtier bio | P1 seulement | Hors budget P0 |

---

## 8. État ADR et impact shortlist

| ADR | Statut | Impact sur la shortlist |
|-----|--------|------------------------|
| ADR-001 ESP32-S3 | ✅ Accepté | A01 — DevKit commandé directement |
| ADR-002 Caméra OV5640/IR | ✅ Accepté | A02 + B01 — module + lentille définitive B |
| ADR-003 LoRa P2P EU868 | ✅ Accepté | A02 (SX1262 breakout ou DevKit LoRa) + B02 RAK3172-T |
| ADR-004 microSD industrielle | ✅ Accepté | A07 — Swissbit DigiKey |
| ADR-005 AA + buck faible Iq | ✅ Accepté | A08–A10 + A09 holders + A16 piles L91 |
| ADR-006 Boîtier IP67 | ✅ Accepté (2026-05-25) | B04 — Hammond P0 ; impression 3D forme organique retenue P1 (hors budget P0) |
| ADR-007 Détection événementielle PIR | ✅ Accepté | A05 — Panasonic EKMB |
| ADR-008 Interface capteurs extensible | ✅ Accepté | A06 micro + B05–B06 réserve capteurs |
| ADR-009 Architecture Satellite/Base/Cloud | ✅ Accepté | Pas d'achat Pi/cloud P0 |

---

## 9. Prochaine action

1. **JCH valide la liste Option A** — ou signale un composant à modifier avant de commander.
2. **Forge** groupe le panier Mouser (A01 + A03–A12 + B03 + B05–B06) et vérifie disponibilité stock à date.
3. **Bruno** vérifie le total livré réel (frais de port, TVA, délais) avant validation financière.
4. **Commande PPK2** (A13) en priorité absolue — Nordic Semi shop EU ou Mouser.
5. **Contacter Arducam** pour confirmation module DVP M12 avant commande panier caméra (A02).
6. **Demander devis Lensation** (B01) — 2 lentilles M12 f/1.8 IR-corrigées — avant tout achat lentille.
7. Après M-02 banc validé → commander Option B sur la base du layout interne réel.

---

## 10. Vérification prix réels — 2026-05-23

Prix vérifiés sur DigiKey EU / Mouser / RAK Store. Source : pages produit directes.

### 10.1 Prix confirmés

| # | Composant | Prix estimé §2–3 | Prix réel vérifié | Source | Stock | Écart |
|---|-----------|-----------------|-------------------|--------|-------|-------|
| A01 | ESP32-S3-DevKitC-1-N8R8 | ~16 € | **€12,75 HT (€15,17 TTC)** | DigiKey.de | 380 unités | ✅ OK — légèrement moins cher |
| A13 | Nordic PPK2 (NRF-PPK2) | ~100 € | **€91,19 HT / €110,34 TTC** | DigiKey BE | 564 unités | ✅ OK — livraison 48h BE gratuite >50€ |
| A08 | TPS62840DLCR (buck) | ~2,50 € | **$2,15 USD (~€2,00)** | DigiKey (stock 0!) / **Mouser : 27 639 unités** | ✅ Mouser | ⚠️ DigiKey épuisé — **commander chez Mouser uniquement** |
| A06 | SPH0645LM4H-B (micro I2S) | ~4 € | **$3,44 USD (~€3,15)** | DigiKey | 16 887 unités | ⚠️ **OBSOLÈTE** — Knowles a arrêté ce composant. Utilisable P0 (stock disponible) mais ne pas réutiliser PCB final. |
| B02 | RAK3172 (standard, EU868) | ~14 € | **$5,99–6,99 USD (~€6–8)** | RAK Store (USD) | En stock | ✅ Moins cher qu'estimé (RAK3172 base). RAK3172-T (TCXO) légèrement plus cher — confirmer prix checkout EU. |

### 10.2 Corrections budget — écarts significatifs

| # | Composant | Estimé | Réel | Δ par nœud | Action |
|---|-----------|--------|------|-----------|--------|
| A05 | PIR Panasonic EKMB1303111K | ~5 € | **~€19–20 (DigiKey)** | **+€14–15** | ⚠️ **PIR bien plus cher que prévu** — voir §10.3 |
| A07 | Swissbit microSD 16GB industrial | ~18 € | **~€23–25 (DigiKey)** | +€5–7 | Budget à réviser — microSD industrielle premium |
| A06 | SPH0645LM4H-B | ~4 € | €3,15 | −€0,85 | Mineur — voir remplacement §10.4 |

### 10.3 PIR — décision requise

Le **Panasonic EKMB1303111K** (12 m, 2 µA) est confirmé à **~€19–20/pièce** sur DigiKey et Mouser — 4× plus cher que l'estimation initiale.

Options :

| Option PIR | Prix | Conso | Adaptation P0 |
|------------|------|-------|----------------|
| **AM312 module** (Senba) | ~€1–2 (marketplace) | ~20 µA | ✅ Acceptable pour banc rapide Option A — pas pour final |
| **HC-SR501 module** | ~€1–3 | ~65 µA | 🔸 Très consommateur — mesure énergie biaisée, déconseillé |
| **Panasonic EKMB1303111K** (12m) | ~€20 | 2 µA | ✅ Référence P0 terrain — Option B ou test énergie précis |
| **Panasonic EKMB1301111K** (5m) | ~€22 | 2 µA | ✅ Même prix, FOV différent — choisir avec boîtier |
| **Excelitas PYQ 5848** (faible conso) | ~€5–8 | ~5 µA | 🔸 Intermédiaire — vérifier disponibilité Mouser BE |

**Décision recommandée :**
- **Option A banc** : commander 1× EKMB1303111K pour les mesures d'énergie réelles + 1× AM312 pour tests de flux/déclenchement. Pas de HC-SR501 (trop consommateur).
- **Option B terrain** : EKMB1303111K uniquement.

### 10.4 Micro MEMS — remplacement SPH0645

Le **SPH0645LM4H-B** est déclaré **obsolète** par Knowles/Syntiant. Stock résiduel disponible (16 887 unités DigiKey, $3,44).

Remplacement recommandé pour PCB final (Option B / P1) :

| Référence | Fabricant | Interface | Prix est. | Stock | Note |
|-----------|-----------|-----------|-----------|-------|------|
| **ICS-43434** | TDK InvenSense | I2S | ~$3,27 | Rupture DigiKey — vérifier Mouser | Remplacement direct, même interface |
| **MP34DT05TR-A** | STMicroelectronics | PDM | ~€1,50 | Stock Mouser/DigiKey | PDM (nécessite conversion firmware) |
| **IM69D120** | Infineon | PDM | ~€3–5 | Vérifier Mouser | Haute qualité, faible bruit |

**Pour Option A banc :** SPH0645LM4H-B commandable et utilisable P0 — noter l'obsolescence dans le BOM.  
**Pour Option B / PCB final :** attendre confirmation ICS-43434 en stock Mouser ou choisir MP34DT05TR-A.

### 10.5 Budget révisé Option A

| Bloc | Estimé §4 | Révisé avec prix réels |
|------|-----------|----------------------|
| Option A composants | ~396 € | **~420–430 €** |
| → PIR EKMB ×1 + AM312 ×1 | était ~€10 | ~€22 (+€12) |
| → microSD ×3 | était ~€54 | ~€70 (+€16) |
| → Buck TPS62840 ×5 | inchangé | ~€10 (Mouser) |
| Option B additions | ~203 € | inchangé (prix non encore vérifiés) |
| Frais de port | ~50 € | inchangé |
| Marge casse | ~80 € | inchangé |
| **Total estimé révisé A+B** | ~729 € | **~755–765 €** |
| **Réserve restante (1 000 €)** | ~271 € | **~235–245 €** |

> ✅ Budget 1 000 € toujours tenu après corrections.
