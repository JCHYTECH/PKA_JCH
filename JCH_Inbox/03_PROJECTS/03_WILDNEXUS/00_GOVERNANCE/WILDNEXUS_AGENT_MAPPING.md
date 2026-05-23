# WildNexus — Mapping agents et spécialistes PKA

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** Pré-go opérationnel  
**Owner :** Dobby  

## 1. Objet

Ce document évite la création de deux équipes parallèles :

- les agents spécialisés WildNexus, dédiés aux domaines techniques du projet ;
- les spécialistes PKA, responsables de la gouvernance, de la mémoire, des livrables et de l'escalade vers JCH.

Principe : un agent WildNexus peut produire une analyse ou une recommandation de domaine, mais chaque flux reste rattaché à un spécialiste PKA référent.

## 2. Règle d'autorité

En cas de contradiction :

1. décision explicite JCH ;
2. non-négociables du document fondateur ;
3. Dobby pour l'orchestration et l'arbitrage de workflow ;
4. spécialiste PKA référent pour la qualité du livrable ;
5. agent WildNexus pour l'expertise de domaine.

Une contradiction technique ou documentaire devient un item `decision` ou `risk` dans Plane.

## 3. Mapping opérationnel

| Agent WildNexus | Spécialiste PKA référent | Périmètre | Livrables attendus | Escalade |
|---|---|---|---|---|
| `wildnexus-program-manager-system-architect` | Dobby | Cohérence P0/P1/P2, jalons, dépendances, architecture système | plan de phase, décisions ouvertes, risques transverses | JCH si arbitrage scope/coût/délai |
| `wildnexus-research-development-project-writer` | Atlas | Dossiers R&D, documents de synthèse, structuration stratégique | dossiers narratifs, annexes, executive summaries | Dobby si dérive de scope |
| `wildnexus-scientific-advisor` | Furet + Clio | valeur scientifique, standards de données, comparatifs, littérature | notes d'état de l'art, critères scientifiques, références | JCH si choix scientifique structurant |
| `wildnexus-camera-imaging` | Nova + Lynx | caméra, IR, qualité image, benchmark modules | protocoles benchmark, critères image, recommandations capteur | Dobby si impact budget ou autonomie |
| `wildnexus-firmware-ulp` | Castor + Forge | firmware, machine d'états, basse consommation, OTA, tests | architecture firmware, preuves de test, CI minimale | Forge si outillage ou intégration |
| `wildnexus-hardware-physical` | Chouette + Castor | PCB, enclos, IP67, installation terrain, contraintes physiques | schémas, BOM, protocole montage, tests banc | Dobby si arbitrage robustesse/coût |
| `wildnexus-rf-propagation` | Forge + Chouette | LoRa/LPWAN, portée, duty-cycle, campagne terrain | plan RF, mesures terrain, décision radio | JCH si compromis couverture/autonomie |
| `wildnexus-edge-ai-cv` | Nova + Clio | filtre animal/non-animal P0, dataset, métriques, quantisation | pipeline évaluation, seuils, rapport faux positifs | Dobby si demande classification espèce en P0 |
| `wildnexus-bioacoustics-dsp` | Clio + Chouette | bioacoustique P1, BirdNET, station acoustique, DSP | notes P1, contraintes d'interface futures | Dobby si pression d'inclusion en P0 |
| `wildnexus-industrialisation` | Bruno + Forge | coûts, fabrication, fournisseurs, petite série, risques supply | budget P0, registre composants, scénarios industrialisation | JCH si financement ou engagement fournisseur |
| Licence, FTO, usage policy | Renard + Hermine | licence source-available, exclusions d'usage, FTO, PI | note FTO, politique d'usage, clauses licence | JCH pour tout choix juridique engageant |
| Communication communauté | Miel + Trace | visibilité, page projet, canal communauté, beta interest | plan de communication EVT, page ou article, canal public | Dobby si publication avant validation juridique |

## 4. Rôles transverses PKA

| Spécialiste | Rôle WildNexus |
|---|---|
| Dobby | orchestration, décisions, synthèse, escalade |
| Forge | automatisation Plane, scripts, dashboards, intégration repo |
| Castor | cohérence données, schémas, architecture technique structurée |
| Renard | droit, contrats, RGPD, licence |
| Hermine | propriété intellectuelle, brevetabilité, FTO |
| Bruno | budget, coût P0, soutenabilité financière |
| Chouette | terrain, installation, contraintes naturalistes et maintenance |
| Nova | image, capteurs, R&D photo/vision |
| Clio | littérature scientifique, bioacoustique, standards |
| Furet | recherche concurrentielle et veille stratégique |
| Atlas | documents stratégiques et R&D |
| Miel | communauté, récit public, visibilité |
| Trace | SEO, présence web, découvrabilité |

## 5. Règles d'escalade vers JCH

Dobby sollicite JCH uniquement pour :

- modifier un non-négociable ;
- arbitrer un compromis coût / délai / performance ;
- autoriser une dépense ou un engagement externe ;
- valider une orientation juridique ou PI ;
- décider si un composant adjacent entre ou sort du périmètre WildNexus ;
- accepter un risque terrain, RGPD ou réputationnel.

Dobby ne sollicite pas JCH pour :

- renommer un fichier ;
- créer une annexe ;
- aligner un backlog ;
- produire une synthèse ;
- nettoyer une incohérence mécanique ;
- marquer un sujet comme P1 ou P2 quand le document fondateur le prévoit déjà.

## 6. Règle Plane

Tout livrable critique doit être rattaché à un item Plane avec :

- owner PKA ;
- agent WildNexus contributeur si applicable ;
- module ;
- milestone ;
- critère d'acceptation ;
- chemin du livrable dans le repo.

Un travail important sans trace dans Plane ou dans le repo est considéré incomplet.
