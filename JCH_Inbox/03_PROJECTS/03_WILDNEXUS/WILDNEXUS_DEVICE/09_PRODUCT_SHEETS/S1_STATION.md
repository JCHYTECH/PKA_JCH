# S1 — WildNexus STATION

Vision P1 — 2026-11-05. Concept non prototypé et non commercialisé. La STATION ne doit pas être confondue avec la gateway minimale de développement requise en P0.

## Intention

La STATION pourrait devenir un hub local de plusieurs nœuds : réception LoRa, stockage, consultation, export et administration sur un site, avec fonctionnement sans cloud pour les fonctions locales. Cette fiche décrit une direction produit, pas des fonctions disponibles.

## Distinction P0 / P1

| Gateway minimale P0 | STATION envisagée P1 |
|---|---|
| Démontrer la chaîne nœud → récepteur | Exploiter un site avec une interface aboutie |
| Recevoir et décoder les paquets caméra/spectraux | Gérer plusieurs nœuds et leurs données |
| Journaliser erreurs et métadonnées | Tableau de bord, exports, provisioning et maintenance |
| Matériel de développement à sélectionner | Architecture Raspberry Pi ou équivalente à étudier |
| Aucun média transporté par LoRa | Récupération locale ou option P1 à définir |

## Fonctions candidates

- enregistrement des alertes et états techniques ;
- consultation et filtrage des événements ;
- exports JSON/CSV et, après validation, Camtrap-DP ;
- récupération des médias par un transport séparé validé ;
- administration des nœuds et provisioning sécurisé ;
- alertes locales ou externes selon une connectivité optionnelle ;
- supervision de l'espace, des erreurs et de la santé du système.

Les cartes de position supposent une localisation connue et autorisée ; aucun GPS n'est prévu dans le payload P0. Les filtres par espèce, la galerie LTE-M et l'OTA ne sont pas des fonctions P0 et exigent leurs propres ADR.

## Architecture à étudier

Un Raspberry Pi avec stockage local, une radio LoRa et une interface réseau est une piste, non une nomenclature figée. La capacité, le nombre maximal de nœuds, le débit, la rétention et les performances seront dimensionnés à partir des essais P0 et des besoins d'un pilote.

Le chiffrement, les comptes, les sauvegardes, la restauration, la gestion des clés et le droit d'accès RGPD doivent être conçus avant tout déploiement. Une carte microSD pour l'OS du Raspberry Pi serait distincte de la carte 128 GB du nœud FIELD.

## Coût et prix

Le coût système complet est inconnu : STATION, gateway, nœuds, stockage, antennes, alimentation, installation, maintenance, certification, support et éventuelle connectivité doivent être consolidés. Les anciens montants partiels et le prix public sont retirés provisoirement.

Aucun nombre de 50 nœuds, volume de deux millions d'événements, prix ou marge n'est validé.

## Conditions d'ouverture P1

1. Gateway P0 démontrée sur paquets réels.
2. Besoins pilote, topologie et volumes mesurés.
3. ADR architecture/sécurité/données et méthode de récupération des médias approuvés.
4. Coût système et responsabilités d'exploitation établis.
5. Décision JCH avant développement produit ou communication commerciale.
