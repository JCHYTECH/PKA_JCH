# WildNexus — Résumé exécutif

Version 2.1 — 2026-11-05. Document de présentation externe, à relire avant toute diffusion. La version 1.0 est conservée dans `HISTORIQUE/` comme archive.

## En une phrase

WildNexus est un projet de nœud d'observation de la faune combinant caméra, écoute acoustique, traitement embarqué et alertes radio longue portée, avec conservation locale des données et sans abonnement cellulaire en P0.

## État du projet

Le projet a été repris le 2026-11-11 (P0 engineering, décision JCH). L'architecture P0 est cadrée, mais la validation technique reste inachevée. Les 37 tests sur ordinateur hôte consignés en juillet ne constituent pas une validation sur ESP32-S3, sur le terrain ou de la chaîne radio complète.

Les autonomies, portées, latences, niveaux d'étanchéité et performances d'IA mentionnés ci-dessous sont des objectifs de conception ou des critères de test, jamais des performances mesurées à ce stade.

## Problème à résoudre

Le tri des déclenchements non pertinents, la récupération physique des cartes mémoire et la dispersion des formats compliquent l'observation naturaliste. WildNexus explore une réponse locale et frugale : conserver les médias sur le nœud et ne transmettre par radio que des alertes et métadonnées compactes.

Les taux de faux déclenchements cités dans les versions antérieures doivent être reliés à des sources précises avant tout usage externe. Ils ne sont pas des résultats WildNexus.

## Architecture P0 engagée

Le prototype vise à réunir :

- un ESP32-S3, une caméra OV5640 NoIR, une détection PIR et un éclairage infrarouge ;
- deux micros MEMS pour des clips stéréo et des descripteurs spectraux ;
- une carte microSD de 128 GB, avec fichiers et sidecars JSON ;
- un filtre embarqué animal / non-animal, complété par une classe de sécurité humaine ;
- des alertes binaires LoRa EU868 de 48 octets et des commandes downlink de 16 octets ;
- une alimentation par piles AA lithium L91 Li-FeS2, dont le schéma reste à valider ;
- un boîtier visant IP67, à tester dans son montage final.

Un clip P0 de trois secondes à 16 kHz, 16 bits, stéréo représente 192 000 octets de données audio. Ni les images ni les clips audio ne sont transportés par LoRa. Leur récupération s'effectue localement ; une option cellulaire appartient à P1.

La limite de fréquence à 16 kHz impose une bande audio analysable inférieure à 8 kHz. Elle ne couvre donc pas tous les taxons. La compatibilité des fichiers réels avec BirdNET, InsectNet et les autres pipelines reste à tester.

## Gateway de développement P0

Une gateway LoRa minimale fait partie de la preuve P0 : réception, décodage des paquets caméra et spectraux, journalisation et gestion des erreurs. Elle permet de démontrer la chaîne de bout en bout.

La STATION commerciale, avec services et tableau de bord aboutis, relève de la vision P1. Elle ne doit pas être confondue avec la gateway de développement.

## Hors périmètre P0

Identification d'espèce embarquée, traduction animale, solaire, transfert de médias par LoRa, option LTE-M, OTA, réseau multi-sites et services commerciaux finalisés. Les pipelines externes d'identification sont des intégrations à valider, pas des fonctions déjà acquises.

## Preuves requises avant toute promesse produit

1. Valider le schéma électrique, les références des micros et du PIR, et les pinouts. La procédure d'alimentation SOP-10 est suspendue.
2. Exécuter sur le matériel les captures jour/nuit, les cycles audio, le stockage et les reprises après erreur.
3. Comparer plusieurs modèles d'IA sur de vraies images jour/nuit : rappel humain, rappel animal, fausses alertes, mémoire, latence et énergie.
4. Mesurer le cycle complet au PPK2 et calculer les scénarios d'autonomie, notamment à 10, 30 et 72 événements par jour. L'objectif de 60 jours n'est pas acquis.
5. Démontrer la liaison nœud → gateway, le volume spectral et les retransmissions dans le respect des contraintes radio applicables.
6. Tester les clips réels dans les pipelines cibles, puis le boîtier et le prototype en conditions terrain.
7. Formaliser les mesures RGPD, la sécurité, la synchronisation temporelle et les procédures d'exploitation avant le déploiement.

## Budget et coût produit

L'enveloppe P0 est de 1 000 €. La projection documentaire provisoire est d'environ 904 €, avec une réserve théorique d'environ 96 €. Elle dépasse le seuil interne d'arbitrage de 900 € : aucune nouvelle commande n'est engagée sans réconciliation des factures et validation de JCH.

La somme historique de la liste de composants FIELD, 99,48 €, n'est pas un coût de nomenclature de production. Elle exclut notamment plusieurs éléments d'optique, la gateway, l'assemblage complet, les tests, la certification, la logistique, la TVA, la garantie et le support. Le coût complet d'un produit vendable est inconnu.

Le prix FIELD et la marge de 40 % précédemment envisagés sont retirés provisoirement. Aucun prix public n'est validé.

## Positionnement et hypothèses de marché

Les pistes de différenciation sont l'autonomie recherchée, la collecte locale sans SIM en P0, la séparation médias/alertes et l'ouverture prévue du firmware. Le coût total d'un système devra inclure la passerelle et l'exploitation, pas seulement le nœud.

Les chiffres de marché, les prix concurrents et les affirmations concernant CSRD, TNFD, Biodiversity Net Gain ou Nature Credits sont des hypothèses de travail issues de recherches antérieures. Ils exigent des sources primaires datées et une analyse de l'applicabilité réelle avant présentation à des partenaires. Aucun pilote client ou revenu n'est revendiqué ici.

## Licence et gouvernance d'usage

JCH a choisi de préparer le firmware sous licence MIT, accompagné d'un fichier `ETHICS.md` et d'une politique d'usage. MIT n'est pas une licence éthique restrictive : elle ne permet pas à elle seule d'interdire juridiquement tous les usages contraires à la mission. La politique guide le projet et les relations contractuelles ; sa portée sur les tiers doit être revue avant publication.

Les licences du hardware, de la documentation, des modèles et des données restent à définir. Les mentions de marque et la liberté d'exploitation doivent également être vérifiées par un conseil qualifié avant engagement. Aucune conformité RGPD, CE ou RED n'est certifiée par ce dossier.

## Reprise et jalons relatifs

Aucune date trimestrielle n'est conservée. Après le signal de reprise de JCH :

| Séquence | Résultat attendu |
|---|---|
| R0 — Réconciliation | Stock, factures, références, schémas et budget validés |
| R1 — Banc | Capture, audio, stockage, IA et gateway démontrés séparément puis intégrés |
| R2 — Preuve P0 | Énergie, radio, robustesse et pipelines mesurés ; M-02 clôturé si les critères sont atteints |
| R3 — Terrain | EVT et exigences de sécurité/RGPD/synchronisation satisfaites |
| R4 — Pré-industrialisation | DVT, conformité, coûts complets et industrialisation validés avant toute pré-série |

## Origine et revue

Jean-Claude Havaux porte le projet avec JCHYTECH et l'appui documentaire de PKA_JCH. Les revues internes antérieures ont aidé à identifier les risques techniques, économiques et éditoriaux. Elles ne remplacent ni essais indépendants, ni validation scientifique, ni avis juridique.

Références internes : `00_GOVERNANCE/Start.md`, `01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md`, `02_DECISIONS/WILDNEXUS_ADR_INDEX.md`, `03_P0_ENGINEERING/PROTOCOLES/progress.md` et `03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md`.
