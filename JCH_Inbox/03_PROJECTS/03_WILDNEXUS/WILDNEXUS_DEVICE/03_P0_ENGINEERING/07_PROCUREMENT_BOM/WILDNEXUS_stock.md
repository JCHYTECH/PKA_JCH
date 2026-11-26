# WildNexus P0 — Stock & Procurement

> **Inventaire documentaire à contrôler physiquement — pas une preuve de disponibilité.**
> Révision : 2026-11-05. Projet repris (2026-11-11) ; aucun achat ou montage n'est autorisé sans gate de reprise et décision JCH.
> Références d'état : `00_GOVERNANCE/Start.md`, `../08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md` et `generate_bom_excel.py`.
> Les versions antérieures mélangeaient des prix, des commandes et des quantités non rapprochées ; elles restent dans l'historique Git.

## 1. Matériel consigné comme reçu

| Équipement | Quantité consignée | Montant consigné | Contrôle nécessaire avant reprise |
|------------|-------------------:|-----------------:|-----------------------------------|
| ESP32-S3-DevKitC-1 N16R8 | 2 | 21,98 € | Confirmer la variante : l'ancien BOM liste aussi des N8R8 |
| Nordic PPK2 | 1 | 83,57 € | Mouser #39411684 ; rapprocher HT/TTC/port ; ne pas compter une seconde fois |
| ESP32-CAM OV2640 avec caméra | 2 | ~25 € | Contrôler modules et caméras |
| ESP32-CAM seules | 4 | Non chiffré | Facture à retrouver |
| OV5640 DVP M12 | 5 au total dans le suivi | ~30 € | Rapprocher Camemake/AliExpress, références et alimentation |
| USB-C TTL FT232RL | 3 | 9,00 € | Contrôler câbles et niveaux logiques |
| Miuzei Starter Kit | 1 | ~35 € | Contenu réel et prix à rapprocher |
| Commande Mouser #39492997 | Voir lignes ci-dessous | 128,20 € | Reçu selon `Start.md` ; vérifier contenu et éventuels backorders |
| MP1584 DC-DC Step Down 3A | 5 | Non chiffré | Présence et adéquation au schéma à vérifier |

Lignes associées à Mouser #39492997 dans les suivis historiques :

- MEMS TDK ×3, référence exacte et interface à relever — l'ancien BOM indique MMICT5848-00-012, sans datasheet I2S vérifiée ;
- LED IR 940 nm ×10, PIR Panasonic ×2, inductances ×5, MOSFET ×5, BME688 ×2, SHT31 ×2, antennes Molex 868 MHz ×2 et dissipateurs ×4 ;
- PIR : le BOM indique EKMB1203111, l'ancien stock EKMB1303111 ; ne retenir aucune référence avant lecture du composant et de la facture ;
- LED et MOSFET : les marques divergent entre les documents ; vérifier les références physiques ;
- TPS62840DLCR : quantité reçue incertaine en raison d'un backorder historique ; ne pas déduire le stock de la seule ligne « commandé ».

Le sous-total des lignes visibles dédupliquées est d'environ **332,75 €**, hors postes non chiffrés et ports non identifiés. Il ne représente pas toutes les dépenses du projet : l'ancien engagé global d'environ **610 €** reste à réconcilier avec les factures.

## 2. À confirmer ou à revalider — achats gelés

| Poste | Hypothèse / état documentaire | Règle |
|---------|-------------------------------|-------|
| microSD 128 GB | ~15 € dans la projection ; non considérée comme reçue | Remplace les anciennes hypothèses 16/32 GB ; choisir capacité et endurance après inventaire |
| Panier restant | ~279 €, ancien panier Mouser à revalider | Ne pas commander avant rapprochement du stock, des références, des prix et des frais |
| RAK3172-T EU868 ×2 | Besoin LoRa P0 ; non consigné comme reçu | Vérifier variante, disponibilité et gateway avant arbitrage |
| Connectique et passifs | JST, headers, câbles, connecteurs antenne, protections, quartz, passifs CMS | Quantités à calculer depuis le schéma ; contrôler le Miuzei et les pièces reçues |
| Supports et piles AA | Configuration 4S2P historique | **SOP-10 suspendue** : ni achat ni assemblage avant revue ADR-005 et schéma |
| RTC | Support CR2032/quartz présents dans l'ancien panier | ADR-018 n'est pas rédigé ; ne pas figer une architecture RTC à partir de ce panier |
| Optique IR-corrigée | Prix et références non consolidés | Sélection et devis avant arbitrage |

## 3. Budget et règle de dépense

L'ancien état global consigne :

- engagé global : **~610 €**, non encore justifié ligne par ligne ;
- panier restant : **~279 €** ;
- microSD 128 GB : **~15 €** ;
- projection : **~904 €**, réserve théorique : **~96 €** sur l'enveloppe de 1 000 €.

La projection dépasse le seuil interne de 900 € : **pause avant toute dépense, puis réconciliation et autorisation explicite de JCH**. Les montants HT/TTC, les frais de port et les postes non chiffrés doivent être régularisés dans le budget P0. Le coût du prototype n'est pas le coût unitaire d'un produit.

## 4. P1/P2 hors réassort P0

Les anciennes mentions de panneau solaire, LiFePO4/BMS, PCB de série et boîtiers futurs ne constituent pas des achats approuvés. Ils restent des pistes à réévaluer après les preuves P0 et un arbitrage de périmètre.

---

*Révision 2026-11-05 : stock distingué des commandes, incohérences de références rendues visibles, microSD 128 GB alignée, PPK2 dédupliqué et projection renvoyée au budget de référence. Aucun comptage physique n'a été effectué lors de cette révision.*
