# WildNexus — Mapping agents et spécialistes PKA

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** Pré-go opérationnel  
**Owner :** [[Dobby]]  

## 1. Objet

Ce document évite la création de deux équipes parallèles :

- les agents spécialisés WildNexus, dédiés aux domaines techniques du projet ;
- les spécialistes PKA, responsables de la gouvernance, de la mémoire, des livrables et de l'escalade vers JCH.

Principe : un agent WildNexus peut produire une analyse ou une recommandation de domaine, mais chaque flux reste rattaché à un spécialiste PKA référent.

## 2. Règle d'autorité

En cas de contradiction :

1. décision explicite JCH ;
2. non-négociables du document fondateur ;
3. [[Dobby]] pour l'orchestration et l'arbitrage de workflow ;
4. spécialiste PKA référent pour la qualité du livrable ;
5. agent WildNexus pour l'expertise de domaine.

Une contradiction technique ou documentaire devient un item `decision` ou `risk` dans Plane.

## 3. Mapping opérationnel

| Agent WildNexus | Spécialiste PKA référent | Périmètre | Livrables attendus | Escalade |
|---|---|---|---|---|
| 
| 
| 
| 
| 
| 
| 
| 
| 
| 
| Licence, FTO, usage [[policy]] | [[Renard]] + [[Hermine]] | licence source-available, exclusions d'usage, FTO, [[Pi]] | note FTO, politique d'usage, clauses licence | JCH pour tout choix juridique engageant |
| Communication communauté | [[Miel]] + [[Trace]] | visibilité, page projet, canal communauté, beta interest | plan de communication EVT, page ou article, canal public | [[Dobby]] si publication avant validation juridique |

## 4. Rôles transverses PKA

| Spécialiste | Rôle WildNexus |
|---|---|
| [[Dobby]] | orchestration, décisions, synthèse, escalade |
| [[Forge]] | automatisation Plane, scripts, dashboards, intégration repo |
| [[Castor]] | cohérence données, schémas, architecture technique structurée |
| [[Renard]] | droit, [[contrats]], RGPD, licence |
| [[Hermine]] | propriété intellectuelle, brevetabilité, FTO |
| [[Bruno]] | budget, coût P0, soutenabilité financière |
| [[Chouette]] | terrain, installation, contraintes naturalistes et maintenance |
| [[Nova]] | image, capteurs, R&D photo/vision |
| [[Clio]] | littérature scientifique, bioacoustique, standards |
| [[Furet]] | recherche concurrentielle et veille stratégique |
| [[Atlas]] | documents stratégiques et R&D |
| [[Miel]] | communauté, récit public, visibilité |
| [[Trace]] | SEO, présence web, découvrabilité |

## 5. Règles d'escalade vers JCH

[[Dobby]] sollicite JCH uniquement pour :

- modifier un non-négociable ;
- arbitrer un compromis coût / délai / performance ;
- autoriser une dépense ou un engagement externe ;
- valider une orientation juridique ou [[Pi]] ;
- décider si un composant adjacent entre ou sort du périmètre WildNexus ;
- accepter un risque terrain, RGPD ou réputationnel.

[[Dobby]] ne sollicite pas JCH pour :

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

Un travail important sans [[Trace]] dans Plane ou dans le repo est considéré incomplet.
