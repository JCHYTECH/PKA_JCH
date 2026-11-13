# WildNexus P0 — Relevé physique d'inventaire (reprise 2026-11-11)

> Dobby 🦉 — feuille de réconciliation à emporter au banc. À remplir physiquement : chaque ligne = une référence à lire sur le composant réel. Les écarts doc↔stock sont déjà signalés.
> Source croisée : `hardware-state.md`, `WILDNEXUS_stock.md`, `WILDNEXUS_SUPPLY_REGISTER.md`, `WILDNEXUS_P0_BUDGET_RANGE.md`.
> **Règle :** aucune valeur n'est fiable tant qu'elle n'est pas lue sur le matériel + facture. Ne pas déduire le stock d'une ligne « commandé ».

## 1. Références à relever physiquement (priorité 1 — débloquent les SOP)

| # | Composant | Qté consignée | Écart à trancher | Relevé physique (à remplir) |
|---|-----------|:-------------:|------------------|-----------------------------|
| 1 | ESP32-S3-DevKitC-1 | 2 | **N16R8 ou N8R8 ?** l'ancien BOM liste les deux ; RAM/flash non interchangeables | Référence exacte sur la carte : |
| 2 | Micros MEMS | 2 ou 3 ? | hardware-state dit **TDK×2**, stock dit **TDK×3** ; cible SPH0645LM4H-B vs TDK MMICT5848-00-012 ; **interface I2S non vérifiée** | Référence + qté + interface : |
| 3 | PIR Panasonic | 2 | **EKMB1203111 ou EKMB1303111 ?** | Référence sur le boîtier : |
| 4 | Caméra OV5640 | 5 (1 Camemake + 4 AliExpress) | Référence module, pinout DVP, NoIR/IR-cut, alimentation | Référence + nappe : |
| 5 | LED IR 940 nm | 10 | Marque/référence ; confirmer **940 nm** (850 abandonné) | Référence + λ : |
| 6 | MOSFET SI2302 | 5 | Marque divergente selon les docs | Référence : |
| 7 | Buck TPS62840DLCR | 5 ? | **Quantité reçue incertaine** (backorder historique) | Qté présente : |
| 8 | X1205 UPS HAT | 1 | Accus **21700 vs 18650** (wiki constructeur vs stock) | Carte + accus : |

## 2. Quantités / factures à rapprocher (priorité 2 — budget)

| # | Poste | Écart | Action JC |
|---|-------|-------|-----------|
| 9 | ESP32-CAM OV2640 seules ×4 | Montant non chiffré | Retrouver la facture |
| 10 | Miuzei Starter Kit | ~35 € consigné | Vérifier contenu réel + prix |
| 11 | MP1584 DC-DC ×5 | Non chiffré | Présence + adéquation schéma |
| 12 | Mouser #39492997 | 128,20 € ; backorders possibles | Rapprocher contenu + facture |
| 13 | Engagé global ~610 € vs lignes visibles ~332,75 € | **Écart ~277 €** à identifier | Lister les factures manquantes |
| 14 | PPK2 | 83,57 € (Mouser #39411684) | HT/TTC + port ; ne pas compter 2× |

## 3. Non reçus — à revalider avant tout achat (ne pas commander sans gate)

| Poste | État | Blocage |
|-------|------|---------|
| microSD 128 GB | non reçu (~15 €) | endurance + capacité après inventaire |
| Panier Mouser restant (~279 €) | à revalider | LoRa RAK3172-T EU868 ×2 + connectique/passifs |
| Optique M12 IR-corrigée | non sélectionnée | devis + test jour/nuit |
| Gateway P0 (ESP32-S3 + SX1262) | non chiffrée | preuve radio à démontrer |
| Pack AA 4S2P | **SOP-10 suspendue** | ni achat ni montage avant ADR-005 + schéma |

## 4. Conséquence immédiate

Projection ~904 € > seuil interne 900 € → **pause avant dépense, puis réconciliation + autorisation JCH**. Rien ne se commande tant que §1 et §2 ne sont pas remplis.

---

*Généré le 2026-11-11 par Dobby 🦉. À remplir au banc, puis me renvoyer — je mets à jour `hardware-state.md`, `WILDNEXUS_stock.md` et le budget en conséquence.*
