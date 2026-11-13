# WildNexus — Registre composants critiques P0

**Version :** v0.4
**Date :** 2026-11-11 — registre de reprise (projet repris)
**Statut :** Ouvert — références, stock et fournisseurs à revalider ; aucune autorisation d'achat
**Owner :** [[Bruno]] + [[Forge]]

> Les tableaux ci-dessous conservent des candidats et prix historiques, pas des commandes à exécuter. Corrections prioritaires : microSD 128 GB selon ADR-004/017 ; cible stéréo selon ADR-013 ; micros réels et interface à identifier ; IR 940 nm retenu, pas de lot 850 nm ; LTE-M en P1. SOP-10 est suspendue : ne pas acheter ou assembler un pack 4S2P avant revue ADR-005 et schéma. La projection de 904 € impose une pause et un arbitrage JCH avant toute dépense. Les affirmations de délais, stocks fournisseurs, « CE certifié » et validations matérielles doivent être vérifiées à la reprise.

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

| Famille | Besoin actif | Fournisseurs candidats à revalider | Risque / preuve requise | Décision |
|---------|--------------|-----------------------------------|--------------------------|----------|
| MCU | ESP32-S3 ; variante physique à relever | Mouser / Farnell / DigiKey | N8R8 et N16R8 ne sont pas interchangeables dans les documents ; vérifier stock et pinout | ADR-001 accepté |
| Caméra | OV5640 DVP M12 ; module réel à identifier | DigiKey / fournisseur du module reçu | Alimentation, pinout, régulateur, NoIR et niveaux logiques | ADR-002 accepté, preuve ouverte |
| Lentille | M12 IR-corrigée, focale à choisir par test | Lensation / Evetar / Arducam | Devis, correction IR et images jour/nuit | Sélection non close |
| IR | LED 940 nm, référence du stock à relever | Mouser / fabricant de la pièce reçue | 850 nm retiré ; ne pas commander un lot de comparaison sans nouvelle décision | ADR-002 accepté |
| Radio nœud | RAK3172-T EU868 avec IPEX | RAK officiel / revendeur UE | Prix, variante, disponibilité et temps d'air à revalider | ADR-003 accepté, non commandé |
| Gateway P0 | ESP32-S3 + SX1262, configuration minimale | À choisir après revue WP05 | Ne pas retenir 1 W/+32 dBm sans revue radio/réglementaire | Gateway P0 requise ; STATION commerciale P1 |
| Radio cellulaire et SIM | Aucun achat P0 | À évaluer en P1 | LTE-M, abonnement et firmware hors périmètre P0 | Différé P1 |
| Stockage | microSD 128 GB ; endurance à définir | Mouser / DigiKey / Distrelec | Remplace les anciennes hypothèses 8–32 GB ; prix et stock à contrôler | ADR-004/017 |
| Pack AA | Topologie et holders à revoir | À choisir après schéma | **SOP-10 suspendue** ; tension maximale L91 et régulateur non validés | ADR-005 accepté sous conditions de preuve |
| Régulation | TPS62840 ou équivalent à confirmer | Mouser / DigiKey | Entrée recommandée 1,8–6,5 V, Iq typique 60 nA ; pics et schéma à valider | ADR-005 |
| Boîtier | Boîtier visé IP67, layout préalable | Hammond / Spelsberg / RS | ADR-006 proposé ; IP de l'ensemble modifié non prouvé | Aucun achat avant revue |
| PIR | Référence physique à relever | Mouser / DigiKey | EKMB1203111/EKMB1303111 divergent selon les documents | ADR-007 accepté, référence ouverte |
| Audio | Deux micros, interface et placement à valider | Mouser / fabricant de la pièce reçue | Cible stéréo ; compatibilité I2S du TDK non vérifiée | ADR-013/017 |
| Capteurs env. | SHT31/BME688 optionnels au banc | Mouser / DigiKey | Ne pas élargir le prototype avant les preuves principales | ADR-008 accepté |

## 3.1 Shortlist de reprise — achat depuis Liège

La liste historique de fournisseurs reste une base de recherche, non une disponibilité constatée : Mouser et DigiKey Belgique pour les composants, RAK officiel pour la radio, Lensation/Evetar/Arducam pour l'optique, RS/Farnell pour le boîtier et la connectique. Les délais, frais de port, seuils de gratuité et stocks doivent être datés et justifiés au moment du devis.

Ordre de contrôle avant tout panier :

1. inventorier physiquement les cartes, micros, PIR, caméras, IR, buck et passifs déjà reçus ;
2. réconcilier les factures, les références et le budget P0 ;
3. lever les blocages de schéma et de datasheet avant de chiffrer un remplacement ;
4. préparer une gateway minimale et ses preuves, sans double emploi avec le stock ;
5. soumettre le panier consolidé à JCH, sans acheter automatiquement une ancienne ligne.

### Points de vigilance procurement

- **Radio :** vérifier la variante EU868, l'antenne et la puissance ; une mention commerciale « CE » ne remplace pas la revue de la configuration complète.
- **Caméra :** exiger pinout, DVP explicite, variante NoIR/IR-cut, lentille et alimentation documentés.
- **IR :** retenir 940 nm ; l'ancienne recommandation d'acheter 850 nm et 940 nm est abandonnée.
- **Batterie :** ne pas relancer de piste 18650/LiPo/LiFePO4 en P0 ni assembler le 4S2P sans révision ADR-005 et levante de la suspension SOP-10.
- **Livraison :** comparer le coût total livré, les taxes et les retours ; ne pas réutiliser un ancien seuil de port gratuit sans vérification.

## 4. Composants bloquants pour la reprise

1. Variantes MCU et pinout réel — à relever ; l'acceptation de la famille ESP32-S3 ne valide pas chaque carte.
2. Module caméra, optique et IR — preuves jour/nuit et énergie non terminées.
3. Schéma d'alimentation et quantités de buck/holders — bloqués par SOP-10.
4. Micros, PIR et interfaces — références physiques et datasheets à rapprocher.
5. Radio et gateway P0 — besoin à chiffrer, chaîne de bout en bout à démontrer.
6. Boîtier — ADR-006 proposé ; cible IP67 non validée.

## 5. Prochaine passe

Compléter pour chaque ligne ouverte :

- fournisseur secondaire confirmé ;
- prix unitaire pour 5 pièces ;
- disponibilité stock EU à date ;
- lien fournisseur direct.
- fournisseur recommandé unique avec justification procurement ;
- coût livré vers Liège / seuil de livraison gratuite quand disponible ;
- stratégie de centralisation des commandes.