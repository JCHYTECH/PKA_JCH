# WILDNEXUS — Dossier technico-commercial V0

Version V0.3 — 2026-11-05. Projet repris le 2026-11-11 (P0 engineering). Document de cadrage interne, pas une fiche de produit validée ni un dossier investisseur prêt à diffuser.

Propriétaire : Jean-Claude Havaux — JCHYTECH. Coordination documentaire : Dobby / PKA_JCH.

## 0. Règle de lecture et sources

Le dossier distingue quatre catégories :

- décidé : choix d'architecture ou de périmètre documenté ;
- à prouver : performance qui exige une mesure ou un essai ;
- hypothèse : marché, coût, réglementation ou usage à sourcer ;
- vision P1/P2 : possibilité future, non engagée dans P0.

Sources actuelles prioritaires :

- `00_GOVERNANCE/Start.md` v0.5 — état, reprise et escalades ;
- `01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md` v0.5 — périmètre et matrice de preuves ;
- `02_DECISIONS/WILDNEXUS_ADR_INDEX.md` v1.1 — décisions et réserves ;
- `03_P0_ENGINEERING/PROTOCOLES/progress.md` — état des tests ;
- `03_P0_ENGINEERING/03_ENERGIE_AUTONOMIE/WP03_BUDGET-ENERGIE_ET_GATE-60J.md` — modèle énergétique ;
- `03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md` — budget provisoire ;
- `09_PRODUCT_SHEETS/F1_FIELD.md` — architecture cible du nœud.

Les anciens documents fondateurs et la V0.2 apportent un contexte historique. En cas de contradiction, ils ne priment pas sur les sources ci-dessus.

## 1. Fiche signalétique

| Élément | État au 2026-11-05 |
|---|---|
| Nature | Projet de nœud caméra/audio avec traitement embarqué et alertes LoRa |
| Phase | M-02 repris (2026-11-11) ; architecture cadrée, validation matérielle inachevée |
| Preuve logicielle | 37/37 tests sur hôte consignés en juillet ; pas de validation ESP32-S3 équivalente |
| Cible énergie | 60 jours dans un scénario défini et mesuré, non démontrée |
| Cible boîtier | IP67 dans le montage final, non testée |
| Données radio | Alertes/métadonnées uniquement ; aucun média par LoRa |
| Gateway | Gateway minimale de développement en P0 ; STATION commerciale en P1 |
| Stockage | MicroSD 128 GB choisie ; besoin réel dépendant aussi des images et de la rétention |
| Enveloppe | 1 000 € ; projection provisoire ≈904 €, réserve théorique ≈96 € |
| Produit | Prototype non commercialisé ; prix et marge non validés |
| Firmware | Publication prévue sous MIT + politique éthique ; textes à finaliser |
| Conformité | CE, RED et RGPD non certifiés par ce dossier |

## 2. Problème et proposition de valeur

WildNexus cherche à réduire deux frictions de l'observation de terrain : le tri des déclenchements non pertinents et la récupération tardive des données. Le nœud conserverait les médias localement, filtrerait les événements et n'émettrait par LoRa que des alertes et mesures compactes.

La proposition à tester est donc une information plus rapidement accessible sans abonnement cellulaire en P0, et non la transmission temps réel de toutes les images. Les taux de faux déclenchements et les gains de temps avancés dans les versions antérieures restent à sourcer puis à mesurer dans un pilote.

La posture scientifique est volontairement limitée : P0 cherche une présence animale et une protection contre la capture/conservation de personnes, pas une traduction du langage animal ni une identification d'espèce. Les captures audio sont programmées ; une synchronisation image/audio scientifique n'est pas démontrée.

## 3. Marché, utilisateurs et preuves commerciales

### 3.1 Segments à interroger

1. Bureaux d'études, gestionnaires et collectivités ayant des besoins de suivi naturaliste.
2. Réserves, parcs, associations et naturalistes.
3. Recherche en écologie, éthologie et bioacoustique.

Ces segments sont des hypothèses de prospection, non des clients acquis. Les entretiens doivent établir le problème, le coût du processus actuel, les contraintes de terrain, le volume utile et le coût système acceptable.

### 3.2 Réglementation et marché

CSRD/ESRS E4, TNFD, Biodiversity Net Gain et Nature Credits sont des pistes de contexte issues de recherches antérieures. Leur applicabilité à des acheteurs précis et leur capacité à financer un instrument WildNexus doivent être vérifiées sur sources primaires à jour. Un suivi de biodiversité n'est pas automatiquement une preuve de conformité réglementaire.

Les estimations de taille de marché et les comparaisons de prix/abonnements de TrailGuard, Nightjar, AudioMoth, Song Meter ou autres solutions sont également à rechercher, dater et comparer à périmètre équivalent. Elles sont retirées du message commercial actif tant que cette vérification n'est pas faite.

### 3.3 Preuves commerciales requises

- un ou deux pilotes définis, avec site, besoin, protocole et responsabilités ;
- une comparaison avant/après du tri et de la collecte ;
- un coût total incluant nœud, gateway, consommables, installation et maintenance ;
- des retours sur les fausses alertes, les événements manqués et l'exploitabilité des données ;
- un modèle économique fondé sur le coût complet, pas sur une liste partielle de composants.

## 4. Périmètre fonctionnel P0

Le prototype cible :

- capture image jour/nuit déclenchée par PIR ;
- traitement embarqué animal / non-animal et classe de sécurité humaine ;
- clips audio stéréo programmés et descripteurs spectraux périodiques ;
- stockage local des médias et métadonnées ;
- alertes radio LoRa EU868 point à point ;
- réception et journalisation par une gateway minimale ;
- alimentation AA et boîtier terrain à valider.

Sont hors P0 : identification d'espèce embarquée, traduction, solaire, LTE-M, OTA, transfert d'images/audio par LoRa, services cloud complets et STATION commerciale. Les pipelines BirdNET, InsectNet et NEXUS_ACOUSTIC sont des consommateurs potentiels des fichiers, à valider sur les productions réelles du nœud.

## 5. Architecture technique cible

| Fonction | Choix de conception | Point ouvert / preuve |
|---|---|---|
| MCU | ESP32-S3 avec PSRAM | Modèle IA et ressources réelles ; migration si critères non atteints |
| Caméra | OV5640 NoIR, optique M12 | Capture réelle, optique IR-corrigée et performances nocturnes |
| Détection | PIR Panasonic EKMB | Référence physique EKMB1203111/EKMB1303111 à relever |
| Audio | Deux micros MEMS, stéréo | Références/interface des TDK en stock à confirmer par datasheet |
| Format audio | WAV PCM 16 bits, 16 kHz, 3 s + sidecar JSON | 192 000 octets de données par clip ; bande utile <8 kHz ; pipelines à tester |
| Stockage | MicroSD 128 GB, images/WAV/JSON | Campagne d'endurance, capacité images et rétention |
| Radio | LoRa EU868 P2P, uplink 48 octets/downlink 16 | Modules à arbitrer ; chaîne réelle, temps d'air, portée et erreurs |
| Alimentation | AA L91 Li-FeS2 + conversion à revoir | SOP-10 suspendue ; schéma, pics, rendement, froid et câblage |
| Boîtier | Cible IP67 | ADR-006 proposé ; montage et essais non réalisés |
| IA | FOMO, MobileNet-SSD ou équivalent compatible | Benchmark comparatif obligatoire ; aucune latence acquise |
| Configuration | Provisioning local et gestion de clés à formaliser | ADR-011 proposé ; ADR-018 à rédiger pour le temps |

La stéréo ne garantit ni localisation ni triangulation. Le format spectral quantifie les fréquences sur 0–16000 dans le contrat v1, sans étendre la bande réellement échantillonnée au-delà de Nyquist.

## 6. Flux de données et confidentialité

Le cycle caméra et le cycle audio programmé sont distincts. La priorité caméra et les reprises après interruption doivent préserver l'intégrité des fichiers. Le chiffrement SD, le secure boot, la conservation et la procédure de droit d'accès suivent ADR-010/011 avant le terrain.

Une image classée humaine ne déclenche pas d'alerte animale ; elle est supprimée après traitement ou les personnes sont irréversiblement floutées avant conservation. Un faux négatif reste possible : la sécurité du support et les procédures RGPD restent obligatoires.

LoRa transporte uniquement les champs ADR-014. Les paquets de 48 octets ne contiennent ni image ni audio ; les clips de trois secondes représentent 192 000 octets et sont récupérés localement. Les commandes de demande de média utilisent un autre transport validé, jamais la payload LoRa.

La gateway P0 se limite à la preuve de réception/décodage/journalisation. Une offre STATION avec dashboard et services est une hypothèse P1 distincte.

## 7. Organisation technique et critères de sortie

| WP | Contenu | Prochaine preuve attendue |
|---|---|---|
| WP01 | Architecture et ADR | Maintenir les réserves et décisions à jour |
| WP02 | Hardware nœud | Inventaire, références, schémas, captures et BOM réconciliée |
| WP03 | Énergie et mesure | Mesures PPK2 par état, cycle complet et scénarios en Wh |
| WP04 | Firmware | Exécution matérielle des cycles et reprise sur erreurs |
| WP05 | Connectivité | Nœud → gateway, deux types de paquets, retries et journal |
| WP06 | Boîtier et terrain | Montage final, étanchéité, EVT et procédures d'exploitation |

La fermeture M-02 exige notamment des captures et fichiers réels, un modèle IA mesuré, une gateway fonctionnelle, les pipelines testés et un budget énergétique complet. Les anciens tests FW-02 à FW-05 sur hôte ne ferment pas ces critères.

## 8. Énergie : cible et méthode

L'objectif de 60 jours est une cible conditionnée à un scénario explicite. Le modèle WP03 raisonne en Wh et inclut veille, PIR, caméra, IA, IR, SD, audio, LoRa, retransmissions, conversion et froid. Les scénarios de travail sont 10, 30 et 72 événements par jour.

Les valeurs de courant issues de datasheets ou d'anciennes estimations ne sont pas des mesures du système intégré. L'autonomie ne sera affirmée qu'après mesures du matériel retenu et validation des hypothèses de capacité des piles aux températures considérées.

SOP-10 reste suspendue. Les anciennes instructions 6×AA/buck 3,3 V vers la broche 5 V ne doivent pas être suivies. Aucun montage 4S2P L91 n'est autorisé sans revue du schéma et des limites d'entrée du régulateur.

## 9. Budget prototype et coût produit

### 9.1 Enveloppe P0

- Enveloppe : 1 000 €.
- Engagé global historique : environ 610 €, à réconcilier avec les factures.
- Reliquat estimé : environ 279 € + 15 € de microSD.
- Projection provisoire : environ 904 € ; réserve théorique : environ 96 €.

Le PPK2 est déjà reçu et compté une seule fois dans les lignes visibles à 83,57 € ; HT/TTC/port restent à rapprocher. Les montants visibles dédupliqués ne suffisent pas à certifier l'engagé global. Le détail et les deux conventions historiques sont conservés dans le budget P0.

La projection dépasse le seuil interne de 900 € : pas de nouvel achat avant réconciliation et autorisation de JCH. Les prix d'un panier ancien ne sont pas un devis actuel.

### 9.2 Coût produit inconnu

La somme de liste historique FIELD de 99,48 € n'est pas une BOM de production. Elle ne comprend pas tous les éléments d'optique, de gateway, d'assemblage, de test, de certification, de logistique, de TVA, de garantie et de support.

Le prix FIELD 149–179 € et la marge de 40 % sont retirés provisoirement. Les prix des visions FIELD+, STATION et autres produits P1/P2 ne sont pas validés. Aucun volume de vente, revenu récurrent, BFR ou coût de certification n'est présenté comme une prévision fiable.

## 10. Modèle économique à étudier

La vente de matériel, l'installation, la formation, la maintenance et les rapports de suivi sont des pistes. Un éventuel abonnement de service serait distinct de l'absence d'abonnement de données cellulaires en P0.

Avant de chiffrer une offre : établir le coût système complet, les responsabilités de traitement des données, le niveau de service, la durée de support et la valeur démontrée dans un pilote. Aucun revenu n'est engagé.

## 11. Licences, éthique et obligations

Décision JCH du 2026-11-05 : firmware destiné à la licence MIT, accompagné de `ETHICS.md` et d'une politique d'usage. MIT reste permissive ; `ETHICS.md` ne transforme pas ce choix en dual-licence et ne supprime pas les libertés MIT des tiers.

La politique exprime les refus du projet, notamment usages militaires, surveillance humaine et atteinte à la biodiversité. Elle guide les contributions et partenariats ; les restrictions opposables à un partenaire doivent être reprises dans son contrat. Un fork propriétaire peut être permis par MIT tout en étant refusé comme partenaire officiel.

Les licences du hardware, de la documentation, des modèles, des données, les notices tierces et les règles de contribution restent à décider. La marque, la liberté d'exploitation, CE/RED, les contrats et le RGPD demandent une revue qualifiée avant publication, vente ou déploiement concerné. Ce dossier n'est pas un avis juridique.

## 12. Risques actifs

| Risque | Réponse actuelle |
|---|---|
| Alimentation dangereuse ou inadaptée | SOP-10 suspendue ; revue datasheet/schéma avant essai |
| Autonomie ou portée surpromise | Mesures WP03/SOP-07 ; aucune garantie dans les documents actifs |
| IA trop lourde ou insuffisante | Benchmark comparatif ; migration MCU si seuils non atteints |
| Micros/PIR incompatibles avec la documentation | Relevé physique et datasheet avant intégration |
| Budget mal réconcilié | Pause d'achat au-dessus du seuil interne ; rapprochement des factures |
| Prix fondé sur une nomenclature partielle | Prix/marge retirés ; coût complet à construire |
| Confidentialité et sécurité insuffisantes | ADR-010/011, registre et procédures avant terrain |
| Licence mal comprise | MIT/éthique/contrats distingués ; autres licences à traiter |
| Reprise sur un planning obsolète | Nouvelle planification uniquement au signal de JCH |

## 13. Reprise relative

| Étape | Contenu | Condition de passage |
|---|---|---|
| R0 | Inventaire, factures, datasheets, schémas et budget | Arbitrages et sécurité validés |
| R1 | Banc des fonctions et gateway | Preuves matérielles individuelles puis intégrées |
| R2 | Clôture M-02 | Matrice scope lock satisfaite |
| R3 | EVT terrain | ADR-018, RGPD/sécurité et boîtier prêts |
| R4 | Pré-industrialisation | DVT, conformité, industrialisation et coûts complets validés |

Les anciennes échéances Q3/Q4 2026 et Q1 2027 sont périmées. Aucune nouvelle date n'est créée sans disponibilité de JCH et réconciliation des prérequis.

## 14. Prochaines actions

1. Attendre le signal de reprise ; inventorier et réconcilier avant tout achat.
2. Traiter la sécurité électrique, les micros, le PIR et l'optique IR.
3. Exécuter les validations banc et les mesures énergétiques.
4. Réaliser le benchmark IA et la preuve LoRa/gateway.
5. Tester les fichiers réels dans les pipelines et rédiger ADR-018.
6. Finaliser les textes MIT/ETHICS et les autres choix de licence avec revue appropriée.
7. Construire le modèle financier et les preuves pilotes avant communication commerciale.

## 15. Historique de la revue V0.2

La V0.2 du 2026-10-29 consigne trois retours internes exploitables — financier, marketing et R&D — ainsi qu'une section juridique rédigée par Dobby faute de rapport final du sous-agent juridique. Ces travaux sont un historique de revue interne assistée par IA, pas des certifications ni des avis professionnels indépendants.

Leurs enseignements restent utiles : ne pas confondre budget prototype et coût produit ; intégrer les coûts cachés et le besoin de fonds de roulement ; comparer les coûts système plutôt que le seul prix du nœud ; sourcer la demande réglementaire ; obtenir des pilotes ; mesurer l'énergie avant de promettre l'autonomie ; aligner nomenclature et stock ; faire relire le juridique avant contrat.

Les montants, performances et calendriers contenus dans la V0.2 sont remplacés par l'état V0.3. Le fait que la V0.2 déclarait le socle technique prêt ne constitue pas une preuve de validation matérielle.
