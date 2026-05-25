# WildNexus — Registre composants critiques P0

**Version :** v0.3
**Date :** 2026-05-23
**Statut :** Ouvert — à compléter avant `M-01`
**Owner :** Bruno + Forge

## 1. Objet

Ce registre suit les composants critiques du prototype P0 afin d'éviter qu'un choix technique ne dépende d'une pièce indisponible, obsolète ou sans alternative crédible.

## 2. Règles

- Aucun composant critique ne doit avoir un fournisseur unique non remplaçable sans justification.
- Chaque choix P0 doit inclure au moins une alternative documentée.
- Les prix ci-dessous sont à confirmer avant commande ; ce document sert d'abord au pilotage des risques.
- Chaque ligne doit indiquer **où acheter**, pas seulement **quoi acheter**.
- L'équipe doit chercher le meilleur fournisseur avant de demander à JCH de vérifier des liens un par un.
- Préférence : fournisseur renommé, centralisation maximale des achats, livraison rapide ou gratuite vers Liège / Belgique, stock EU, facture claire, retour simple.
- Les marketplaces génériques (Amazon, AliExpress) sont acceptables pour prototypage rapide, mais ne sont pas le choix par défaut si Mouser, DigiKey, Farnell/element14, RS, TME, Reichelt, Conrad, RAK/Seeed/Arducam officiel ou fournisseur EU reconnu couvre le besoin.

## 2.1 Politique procurement

Pour chaque composant, l'équipe doit proposer :

| Champ | Exigence |
|---|---|
| Fournisseur recommandé | site précis où acheter en priorité |
| Raison du choix | fiabilité, centralisation, prix, stock, délai, livraison, retour |
| Lien direct | URL produit ou recherche fournisseur |
| Alternative crédible | second fournisseur si stock/prix change |
| Livraison Liège | coût estimé, délai, seuil gratuit si connu |
| Risque achat | contrefaçon, variante erronée, fréquence radio, certification, accessoire manquant |
| Quantité P0 | nombre proposé pour prototype + spare |

Scoring fournisseur recommandé :

| Score | Critère |
|---|---|
| 30 % | fiabilité fournisseur / marque / traçabilité |
| 20 % | centralisation avec les autres achats WildNexus |
| 20 % | disponibilité stock EU / délai vers Liège |
| 15 % | coût total livré, pas seulement prix unitaire |
| 10 % | documentation technique / datasheet / schéma |
| 5 % | politique retour / SAV |

## 3. Tableau de suivi

| Famille | Choix ADR | Fournisseur primaire | Alternative écartée (motif) | Prix unitaire cible | Délai cible | Risque | ADR |
|---------|-----------|---------------------|-----------------------------|--------------------:|-------------|--------|-----|
| MCU | ESP32-S3 | Mouser / Farnell EU | STM32U5 — *intégration caméra complexe* | ~4–8 € | 2–5 j | Bas | ADR-001 ✅ |
| Caméra — capteur | OV5640 5MP M12 DVP (Arducam) | Arducam / Mouser EU | IMX462 MIPI — *interface MIPI non native ESP32-S3* | ~20 € | 3–7 j | Bas | ADR-002 ✅ |
| Caméra — lentille | M12 IR-corrigée f/1.8 4–6 mm | Lensation.de | Lentille fixe intégrée — *pas IR-corrigée, non remplaçable* | ~25–50 € | 3–7 j | Moyen | ADR-002 ✅ |
| Caméra — IR LEDs | LED IR 850 nm × 4 | Mouser / AliExpress | 940 nm — *rendement capteur plus faible* | ~5–10 € | À confirmer | Bas | ADR-002 ✅ |
| Radio LoRa | RAK3172 (SX1262, CE certifié) | RAK EU / Mouser | Murata Type 1SJ — *même gamme, second choix* | ~12–15 € | 3–7 j | Bas | ADR-003 ✅ |
| Radio cellulaire | Quectel SIM7080G (NB-IoT + LTE-M) | Mouser / DigiKey | SIM7070G — *NB-IoT seul, moins polyvalent* | ~15–20 € | 5–10 j | Moyen | ADR-003 — **P1 — différé, complexité firmware non justifiée P0** |
| SIM IoT | 1NCE nano-SIM (10 ans / 500 Mo) | 1nce.com | Hologram — *pay-as-you-go plus cher à terme* | 10 € one-shot | 3–5 j | Bas | ADR-003 — **P1 — lié au cellulaire** |
| Gateway P0 | ESP32-S3 DevKit + SX1262 breakout | Mouser / AliExpress | RAK2287 gateway complète — *surdimensionné P0* | ~25 € | 3–7 j | Bas | ADR-003 ✅ |
| Stockage | microSD industrielle 8-16 GB | Mouser / DigiKey / Distrelec | flash SPI — *capacité limitée pour images et clips audio* | À chiffrer | À confirmer | Moyen | ADR-004 ✅ |
| Batterie | Holder 8× AA en 4S2P + piles utilisateur | Mouser / Reichelt / Conrad / RS | LiFePO4 18650 — *BMS/charge/supply non nécessaires P0* | À chiffrer holder seul | À confirmer | Bas | ADR-005 ✅ |
| Régulation énergie | TPS62840 ou équivalent buck faible Iq | Mouser / DigiKey | CN3791/MPPT — *solaire différé P1* | ~2–5 € | 2–5 j | Bas | ADR-005 ✅ |
| Solaire | Réserve mécanique P1 seulement | — | Panneau 6V + MPPT CN3791 — *hors P0* | 0 € P0 | — | Bas | ADR-005 — **achat différé P1** |
| Boîtier | IP67 ABS/PC commercial ≤ 150×100×60 mm | Hammond / Spelsberg EU | Impression 3D PETG — *étanchéité IP67 non garantie long terme* | ~10–20 € | 3–7 j | Moyen | ADR-006 |
| PIR / détection | PIR basse conso | À confirmer | Réveil périodique caméra — *trop consommateur* | À chiffrer | À confirmer | Moyen | ADR-007 |
| Micro audio | Micro mono MEMS I2S/PDM ou analogique faible conso | Mouser / DigiKey | Audio scientifique avancée — *hors P0* | À chiffrer | À confirmer | Moyen | ADR-008 ✅ |
| Capteurs env. | SHT31 (temp. + humidité interne) | Mouser / DigiKey | HDC1080 — *même gamme, second choix* | ~3–6 € | 2–5 j | Bas | ADR-008 — **optionnel P0 ; non bloquant pour M-01/M-02/M-03 ; différer si budget serré** |

## 3.1 Shortlist procurement M-01 — achat depuis Liège

**Stratégie panier :** centraliser d'abord chez **Mouser Belgique** pour MCU, capteurs, IR, composants passifs, boîtier si disponible ; utiliser **DigiKey Belgique** en second panier pour microSD industrielle et modem cellulaire si Mouser ne fournit pas ; utiliser les **fabricants officiels** pour les modules très spécialisés (RAK, Arducam, Lensation/Evetar) quand le distributeur généraliste ne garantit pas la bonne variante.

DigiKey Belgique indique une livraison gratuite à partir de 50 EUR, sinon 18 EUR, avec livraison typique vers la Belgique sous 48 h. Mouser a de bons stocks Belgique/EU pour Espressif, Sensirion, Vishay et beaucoup de composants critiques, mais les frais réels restent à confirmer dans le panier.

| Famille | Achat recommandé | Fournisseur recommandé | Pourquoi | Alternative | Action JCH |
|---|---|---|---|---|---|
| MCU prototype | ESP32-S3-DevKitC-1-N8R8 | Mouser BE | stock élevé, 8 MB flash + 8 MB PSRAM, fournisseur fiable, prototypage immédiat | DigiKey BE ESP32-S3-WROOM module pour PCB | Acheter 2 DevKit pour banc M-02 |
| MCU PCB | ESP32-S3-WROOM-1U-N8R8 | Mouser BE | module officiel Espressif, IPEX, 8 MB PSRAM, stock élevé, prix bas | DigiKey BE ESP32-S3-WROOM-1-N8R8 | Prévoir 5-10 modules si PCB P0 lancé |
| Radio LoRa nœud | RAK3172 / RAK3172-T EU868 avec IPEX | RAK Store officiel ou revendeur EU | bonne variante EU868, P2P supporté, documentation RAK | Industry-Electronics / M2M Gubbins si stock EU meilleur | Vérifier variante EU868 + IPEX avant achat |
| Gateway / banc RF | Meshnology N35 V4 / Heltec WiFi LoRa 32 V4 EU868 | Meshnology/Heltec officiel, Amazon seulement si V4 confirmée | accélère tests LoRa/gateway, pas nœud caméra | RAK3172 Evaluation Board | Acheter 1-2 seulement pour banc RF |
| Caméra capteur | OV5640 5 MP DVP compatible ESP32, M12 si possible | Arducam officiel ou fournisseur caméra spécialisé | Mouser ne semble pas couvrir proprement le module DVP M12 voulu ; éviter variantes marketplace floues | IADIY / YXFcamera comme devis, pas achat aveugle | Demander fiche pinout + NoIR + M12 + DVP |
| Caméra alternative rapide | Arducam Mega 5MP SPI M12 | Arducam officiel | facile à intégrer, M12, SDK, mais **IR-cut visible only** donc non conforme nuit | aucun pour décision ADR-002 | Benchmark seulement, ne pas acheter comme caméra finale |
| Lentille | M12 IR-corrigée f/1.8 4-6 mm | Lensation ou Evetar officiel EU | qualité optique, correction IR, traçabilité | Arducam M12 IR lens si specs complètes | Demander devis 2-5 pièces |
| LEDs IR | Vishay 940 nm haute puissance + variante 850 nm | Mouser BE | stock, datasheets, pas de risque marketplace ; permet test faune 850/940 | Würth IR LEDs chez Mouser | Acheter petit lot des deux longueurs d'onde |
| PIR | Panasonic EKMB low-power PaPIRs | Mouser BE | courant jusqu'à 1 µA selon famille EKMB, fournisseur fiable | DigiKey BE Panasonic EKMB | Choisir FOV après design boîtier |
| Stockage | Swissbit microSD industrielle 8-16 GB | DigiKey BE / Distrelec BE | cartes industrielles, endurance, température ; Mouser parfois restriction région | Mouser si disponibilité région OK | Acheter 2-3 cartes industrielles |
| Modem cellulaire | SIM7080G | DigiKey BE | fiche claire, module actif, support RF/GNSS, livraison BE | Mouser si Quectel/SIMCom dispo | Vérifier opérateur/SIM/antenne avant achat |
| SIM IoT | 1NCE nano-SIM | 1NCE officiel | modèle 10 ans/500 MB cohérent ADR-003 | aucun évident | Acheter direct 1NCE |
| Batterie | Holder 8× AA 4S2P + piles AA utilisateur | RS / Reichelt / Conrad / Mouser selon format | modèle caméra de chasse, pas de BMS, maintenance terrain simple | holder 4×AA × 2 si intégration mécanique meilleure | Acheter holder après choix boîtier |
| Buck énergie | TPS62840 ou module équivalent faible Iq | Mouser BE / DigiKey BE | faible courant de repos, cohérent autonomie P0 | autre buck faible Iq si pic courant insuffisant | Ajouter au panier composants |
| Solaire/MPPT | Aucun achat P0 | — | solaire différé P1 ; éviter CN3791 dans le proto P0 | réserve mécanique boîtier seulement | Ne pas acheter avant décision P1 |
| Boîtier | RS PRO / Hammond / Spelsberg IP67 150x100x60 | RS Belgium ou Mouser/Farnell | dimensions proches ADR-006, fournisseur EU, retours simples | Spelsberg EU | Acheter 1-2 boîtiers après layout interne |
| SHT31 | Sensirion SHT31-DIS | Mouser BE | stock, capteur fiable, datasheet | DigiKey BE | Ajouter au panier Mouser |

### Points de vigilance procurement

- **Radio :** toujours vérifier EU868 / 863-928 MHz et antenne adaptée 868 MHz.
- **Caméra :** ne pas acheter un module OV5640 marketplace sans pinout, DVP explicite, variante NoIR/IR-cut et format lentille.
- **IR :** acheter 850 nm et 940 nm pour test terrain ; ne pas figer 850 nm avant revue faune.
- **Batterie :** ne pas relancer de piste 18650/LiPo/LiFePO4 pour P0 ; le choix actif est holder 8× AA 4S2P + buck faible Iq.
- **Livraison :** éviter de multiplier les petits paniers sous seuil de livraison gratuite ; grouper Mouser/DigiKey.

## 4. Composants bloquants avant M-01

1. MCU — **validé** (ADR-001 accepté)
2. Module caméra + lentille — **validé** (ADR-002 accepté)
3. Module radio LoRa
4. Holder 8× AA + buck faible Iq
5. Boîtier IP67

## 5. Prochaine passe

Compléter pour chaque ligne ouverte :

- fournisseur secondaire confirmé ;
- prix unitaire pour 5 pièces ;
- disponibilité stock EU à date ;
- lien fournisseur direct.
- fournisseur recommandé unique avec justification procurement ;
- coût livré vers Liège / seuil de livraison gratuite quand disponible ;
- stratégie de centralisation des commandes.
