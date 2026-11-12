# WildNexus — Budget P0

**Version :** v0.5
**Date :** 2026-11-05
**Statut :** enveloppe ferme de 1 000 € ; projection provisoire à réconcilier avec les factures
**Owner :** [[Bruno]]

## 1. Contrainte et règle de lecture

L'enveloppe P0 est fixée à **1 000 € maximum**. Tout dépassement exige une décision explicite de JCH.

Trois nombres ne doivent pas être confondus :

- les achats effectivement justifiés par facture ;
- la projection incluant le reliquat estimé ;
- le coût unitaire d'un éventuel produit, qui n'est pas encore connu.

Le projet ayant repris, les paniers et prix anciens doivent être revalidés avant toute commande. Ce document ne vaut pas autorisation de dépense.

## 2. Périmètre du prototype

| Choix | Cadre P0 |
|-------|----------|
| Nœuds | Deux nœuds de développement visés |
| Électronique | DevKit et breakout boards ; pas de PCB dédié validé en P0 |
| Gateway | Une gateway minimale de développement est nécessaire à la preuve LoRa |
| Propriété intellectuelle | Analyse interne ; pas de conseil externe budgété |
| Dataset IA | Terrain JCH dans un premier temps ; besoin externe réévalué après benchmark |
| EVT | Belgique locale, après clôture du banc |

## 3. Lignes d'achats visibles dédupliquées

Le PPK2 appartient à la commande Mouser #39411684. Il ne faut pas additionner une seconde ligne « Nordic PPK2 ».

| Commande / poste | Montant consigné | État | Commentaire |
|------------------|-----------------:|------|-------------|
| Mouser #39411684 — Nordic PPK2 | **83,57 €** | Reçu | Montant retrouvé dans le générateur BOM ; HT/TTC et frais de port à rapprocher de la facture |
| ESP32-S3-DevKitC-1 ×2 — Amazon MiMiU | 21,98 € | Reçu | MCU de banc |
| ESP32-CAM OV2640 ×2 — Hailege | ~25 € | Reçu | Développement caméra |
| ESP32-CAM seules ×4 | Non chiffré ici | Reçu | Facture à retrouver ; aucun montant inventé |
| OV5640 DVP M12 ×5 | ~30 € | Reçu | Camemake + AliExpress ; ventilation à confirmer |
| USB-C TTL FT232RL ×3 | 9,00 € | Reçu | Debug série |
| Mouser #39492997 | 128,20 € | Reçu | MEMS, IR, PIR, buck, capteurs, antennes et dissipateurs |
| Miuzei Starter Kit | ~35 € | Reçu | Composants et breadboard |
| **Sous-total des lignes visibles ci-dessus** | **~332,75 €** | | Avec 83,57 € pour le PPK2, hors postes non chiffrés et ports non identifiés |

L'ancienne convention d'environ 100 € pour le PPK2 donne un sous-total visible de **349,18 €**. La différence de 16,43 € vient uniquement de la convention de montant ; elle ne constitue pas une dépense supplémentaire.

## 4. Projection provisoire héritée de l'état global

Le dernier état de pilotage consignait un engagé global plus large que les lignes visibles ci-dessus. Tant que les factures ne sont pas réconciliées, on conserve cet état comme projection prudente, sans le présenter comme certifié.

| Bloc | Projection provisoire |
|------|----------------------:|
| Engagé global consigné | ~610 € |
| Panier Mouser restant à revalider | ~279 € |
| microSD 128 GB | ~15 € |
| **Total engagé / prévu** | **~904 €** |
| Enveloppe | 1 000 € |
| **Réserve théorique** | **~96 €** |

L'écart entre l'engagé global de 610 € et les lignes visibles dédupliquées est de **260,82 €** avec la convention PPK2 à 100 €, ou de **277,25 €** avec le montant enregistré de 83,57 €. Il faut identifier les achats et frais correspondants avant de fermer la réconciliation.

**Conséquence immédiate :** la projection de 904 € dépasse le seuil interne d'arbitrage de 900 € défini au §7. Le reliquat reste gelé jusqu'à réconciliation et autorisation JCH.

## 5. Postes à consolider avant reprise

| Poste | Traitement requis |
|-------|-------------------|
| Lentille M12 IR-corrigée | Prévoir une hypothèse de 30–35 € minimum par optique seulement après sélection et devis ; ne pas la considérer incluse dans la caméra basique à 8 € |
| microSD 128 GB | Remplace les anciennes hypothèses 16/32 GB ; vérifier prix et endurance |
| Gateway P0 | Chiffrer le second ESP32-S3, le SX1262, l'antenne, l'alimentation et la connectique sans double emploi avec le stock |
| Radio RAK3172 | Revalider disponibilité, prix, frais de port et présence réelle dans le panier |
| Micros MEMS | Relever la référence TDK reçue et vérifier son interface avant de la substituer au SPH0645LM4H-B cible |
| PIR | Rapprocher EKMB1203111 / EKMB1303111 du composant physique |
| Alimentation | Ne commander ni pack ni régulateur définitif avant les gates ADR-005 et la reprise autorisée de SOP-10 |
| Ports et taxes | Uniformiser HT/TTC et rattacher les frais à chaque commande |
| Coûts produit | Assemblage, tests, boîtier, certification, logistique, TVA, garantie et support à chiffrer séparément du prototype |

La somme historique de **99,48 €** dans la fiche F1 est seulement celle d'une liste de composants, avec microSD 128 GB et hors optique IR-corrigée de qualité. Ce n'est ni un BOM de production ni une base de marge.

## 6. Risques qualité à ne pas masquer par le budget

| Risque | Règle de gestion |
|--------|------------------|
| Optique nocturne insuffisante | Sélectionner et tester la lentille ; ne pas promettre une portée à partir du seul capteur OV5640 |
| Deux nœuds seulement | Acceptable pour une preuve de concept, insuffisant pour généraliser une fiabilité terrain |
| DevKit et connectique volante | Acceptable au banc ; industrialisation et boîtier exigent une conception dédiée |
| Puissance et autonomie extrapolées | Mesurer chaque cycle et les pertes en Wh ; aucune déduction de 60 jours depuis le deep sleep seul |
| Absence de mesure PPK2 | PPK2 déjà acquis ; maintenir la traçabilité des configurations et fichiers de mesure |
| Gateway oubliée du système | Inclure son coût et sa preuve dans le P0 connecté ; la STATION commerciale reste P1 |

## 7. Règles de dépense

- Tout achat individuel supérieur à 50 € est signalé à JCH avant commande.
- Si le total projeté dépasse 900 €, arrêt et arbitrage avant le reliquat : ce cas est déjà atteint avec la projection provisoire.
- Aucun panier ancien n'est commandé sans revue du stock, du prix, des références et des frais.
- Toute dépense doit être rattachée à une facture, un montant HT/TTC explicite et un besoin du plan de preuve.

## 8. Hors enveloppe actuelle

| Poste | Condition de réintégration |
|-------|----------------------------|
| Conseil FTO/IP externe | Décision JCH si publication, partenariat ou levée le justifie |
| PCB dédié et industrialisation | Après validation du banc et chiffrage spécifique |
| Nœuds supplémentaires | Après preuve du prototype et arbitrage enveloppe |
| Dataset externe | Si le benchmark démontre que les données JCH sont insuffisantes |
| DVT, certification et pré-séries | Budget distinct à établir après EVT ; ne pas les considérer couverts par les 96 € de réserve |

---

*Révision 2026-11-05 : doublon PPK2 supprimé, sous-total visible distingué de la projection globale de 904 €, réserve provisoire de 96 €, seuil de 900 € activé et postes techniques non chiffrés explicités.*
