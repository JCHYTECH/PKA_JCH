# WildNexus - Notes du diagramme Satellite / Base / Cloud

## But

Clarifier la separation entre le satellite terrain P0, la base locale P1 et le cloud P1/P2.
Le schema sert de garde-fou : le P0 doit rester validable sans Base/Master et sans Cloud.

## Legende des blocs

- S1 : camera et illumination IR du satellite.
- S2 : declenchement evenementiel local, sans analyse lourde obligatoire.
- S3 : stockage local complet des donnees utiles sur microSD.
- S4 : etat batterie, sante du noeud, signaux de fonctionnement.
- S5 : transmission [[LoRa]] limitee aux alertes, statuts et metadonnees courtes.
- S6 : acces Wi-Fi local pour configuration, maintenance et extraction terrain.
- B1 : collecte locale par Base/Master Nexus.
- B2 : indexation des evenements recuperes.
- B3 : analyse lourde locale ou semi-locale, notamment BirdNET-Go et YOLO.
- B4 : interface locale de consultation et de pilotage.
- C1 : archivage selectif des donnees retenues.
- C2 : acces distant optionnel.
- C3 : partage controle avec tiers ou communaute.
- C4 : exports scientifiques futurs.
- U1 : utilisateur terrain ou operateur de maintenance.

## Hypotheses

- Le satellite P0 doit survivre et produire des donnees utiles seul.
- [[LoRa]] ne transporte pas de flux raw continu.
- Les images, sons ou videos complets restent locaux jusqu'a extraction ou passage par une base.
- La Base/Master peut etre prototypée en parallele, mais elle ne conditionne pas M-03.
- Le cloud est un prolongement produit, pas une dependance terrain minimale.

## Exceptions

- Une alerte critique de sante du noeud peut etre transmise sans attendre une detection animale.
- Une extraction terrain directe peut contourner la Base/Master si l'objectif est seulement de recuperer les raws.
- Une connexion cloud ponctuelle peut etre testee en P1, mais ne doit pas redefinir le P0.

## Questions ouvertes

- Format exact des metadonnees [[LoRa]] minimales.
- Frequence acceptable des statuts batterie/sante.
- Interface de maintenance locale : Wi-Fi direct, BLE, ou combinaison.
- Schema d'export scientifique cible pour P1/P2.

## Sources

- `diagramme.md`
- `2026-05-24_wildnexus-schema-sat-cloud-master.png`
- `../02_DECISIONS/ADR/ADR-009-architecture-satellite-base-cloud.md`
- `../01_FOUNDATION/MASTER_ARCHITECTURE_WN.md`
