# F2 — WildNexus FIELD+

Vision P1 — 2026-11-05. Concept non engagé, non prototypé et non commercialisé. Cette fiche ne prolonge pas le périmètre P0 et ne constitue ni spécification ni offre.

## Intention

FIELD+ explore une évolution longue durée du nœud FIELD : énergie solaire, acoustique adaptée à davantage d'espèces, capteurs environnementaux et identification hors du contrat binaire P0. Ces pistes ne sont étudiées qu'après les preuves P0 et une décision JCH.

## Pistes à évaluer

| Domaine | Hypothèse P1 | Travail préalable |
|---|---|---|
| Énergie | Batterie rechargeable et panneau solaire | Architecture séparée, bilan saisonnier, sécurité, BMS/MPPT et essais ; aucune autonomie « illimitée » |
| Acoustique | Micros et fréquence d'échantillonnage adaptés aux taxons cibles | Liste d'espèces, bande nécessaire, antialiasing, datasheets et volume de données |
| IA | Identification d'espèce ou pipeline local/déporté | Dataset, licences, benchmark et gouvernance des erreurs |
| Radio | LoRa P2P, autres options à décider | ADR spécifique ; LoRaWAN/LTE-M non acquis |
| Environnement | BME688/SHT31 ou équivalents | Utilité scientifique, énergie et métadonnées |
| Boîtier | Protection et dissipation adaptées | Conception et tests ; aucun indice IP revendiqué |
| Maintenance | Mise à jour et supervision | ADR sécurité, provisioning et procédure de retour arrière |

Le P0 reste limité à 16 kHz/16 bits/stéréo et à une bande analysable inférieure à 8 kHz. Un micro annoncé jusqu'à 20 kHz ne suffit pas à couvrir les ultrasons, notamment ceux de nombreuses chauves-souris. La fréquence d'échantillonnage et la chaîne analogique doivent être dimensionnées pour les espèces visées. Aucun remplacement « drop-in » ou compatibilité mécanique/firmware n'est présumé.

## Relation avec FIELD

FIELD+ ne peut pas être défini comme un simple ajout de modules : énergie, boîtier, acoustique, stockage, firmware et certification peuvent changer ensemble. Un ADR P1 déterminera s'il s'agit d'une évolution, d'un nouveau produit ou d'un projet distinct.

La cible FIELD P0 utilise une microSD de 128 GB. Toute capacité FIELD+ sera recalculée à partir des images, de la cadence audio, du taux d'échantillonnage, de la rétention et de l'endurance.

## Coût et prix

Les anciennes additions fondées sur un coût FIELD non consolidé sont retirées. Le coût complet FIELD+ est inconnu : matériel, énergie, optique, gateway, assemblage, tests, certification, logistique, garantie et support doivent être chiffrés ensemble.

Aucun prix de vente, marge, quantité de production ou contenu de pack n'est validé.

## Conditions d'ouverture de l'étude P1

1. P0 validé sur matériel et enseignements documentés.
2. Besoin utilisateur et espèces cibles définis.
3. ADR énergie/acoustique/IA/données et sécurité rédigés.
4. Coût complet et impacts réglementaires examinés.
5. Arbitrage explicite de JCH avant achat ou annonce.
