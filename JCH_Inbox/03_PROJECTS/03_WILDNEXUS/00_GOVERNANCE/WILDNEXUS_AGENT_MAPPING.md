# WildNexus — Mapping agents et spécialistes PKA

**Version :** v0.2  
**Date :** 2026-06-30  
**Statut :** Actif — M-02 en cours  
**Owner :** [[Dobby]]  

## 1. Objet

Ce document relie les domaines techniques du projet WildNexus aux spécialistes PKA qui les portent. Il évite la création d'une équipe parallèle d'"agents WildNexus" distincts du roster PKA.

Principe : un domaine technique peut nécessiter une analyse ou une recommandation, mais chaque flux reste rattaché à un spécialiste PKA référent.

## 2. Règle d'autorité

En cas de contradiction :

1. décision explicite JCH ;
2. non-négociables du document fondateur ;
3. [[Dobby]] pour l'orchestration et l'arbitrage de workflow ;
4. spécialiste PKA référent pour la qualité du livrable ;
5. expert de domaine pour l'analyse technique.

Une contradiction technique ou documentaire devient un item `decision` ou `risk` dans Plane.

## 3. Mapping opérationnel

| Domaine technique | Spécialiste PKA référent | Périmètre | Livrables attendus | Escalade |
|---|---|---|---|---|
| MCU / Firmware ULP | [[Forge]] + [[Araignée]] | ESP32-S3, deep sleep, machine d'états, cycle veille/réveil | Firmware P0, SOPs A→K, code ESP-IDF | JCH pour arbitrage coût/performance |
| Caméra / IR / Optique | [[Nova]] + [[Lynx]] | OV5640, lentille M12, LED IR, qualité image | ADR-002, SOP-08, test harness caméra | JCH pour arbitrage qualité optique |
| Radio / LPWAN / LoRa | [[Forge]] + [[Chouette]] | SX1262, EU868, payload binaire, gateway | ADR-003, ADR-014, SOP-07, parser gateway | JCH pour choix infrastructure radio |
| Stockage local | [[Castor]] + [[Forge]] | microSD, chiffrement AES, format métadonnées | ADR-004, SOP-06 | — |
| Énergie / Autonomie | [[Bruno]] + [[Chouette]] | AA + buck, PPK2 mesures, modèle autonomie 60j | ADR-005, SOP-10, modèle énergétique | JCH pour enveloppe budget |
| Boîtier / IP67 / Terrain | [[Chouette]] | Hammond 1555, fenêtre optique, fixation arbre | ADR-006, guide déploiement | — |
| Détection événementielle | [[Nova]] + [[Forge]] | PIR EKMB, trigger, filtrage | ADR-007, SOP-09 | — |
| Capteurs extensible | [[Castor]] | Bus I2C/SPI, interface capteurs env. | ADR-008 | — |
| Architecture SAT/Base/Cloud | [[Dobby]] + [[Castor]] | Topologie réseau, gateway, dashboard | ADR-009 | JCH pour choix architecture cloud |
| Sécurité / RGPD / Edge AI | [[Castor]] + [[Forge]] + [[Hermine]] + [[Renard]] | Filtre humain, chiffrement SD, secure boot, signalétique | ADR-010, ADR-011, SOP-11 | JCH pour orientation juridique |
| Provisioning / Clés | [[Castor]] + [[Forge]] + [[Hermine]] | Diversification clé, cycle de vie, secure boot | ADR-011 | — |
| Stratégie de test | [[Forge]] + [[Castor]] + [[Araignée]] | Banc, terrain, régression, critères GO/NO-GO | ADR-012, SOPs | — |
| Acoustique / Micros | [[Dobby]] + JCH | SPH0645 stéréo, capture locale, upgrade path | ADR-013 | — |
| Licence, FTO, usage policy | [[Renard]] + [[Hermine]] | Licence source-available / dual-license, exclusions d'usage, FTO | Note FTO, politique d'usage, clauses licence | JCH pour tout choix juridique engageant |
| Communication communauté | [[Miel]] + [[Trace]] | Visibilité, page projet, canal communauté, beta interest | Plan communication EVT, page ou article, canal public | [[Dobby]] si publication avant validation juridique |
| Edge AI / TinyML | [[Musaraigne]] | MobileNet-SSD, quantification INT8, benchmark ESP32-S3 | Modèle TFLite, SOP-11, ADR-010 R4 | JCH pour arbitrage migration MCU |

## 4. Rôles transverses PKA

| Spécialiste | Rôle WildNexus |
|---|---|
| [[Dobby]] | orchestration, décisions, synthèse, escalade |
| [[Forge]] | automatisation Plane, scripts, dashboards, intégration repo, firmware |
| [[Castor]] | cohérence données, schémas, architecture technique structurée |
| [[Renard]] | droit, contrats, RGPD, licence |
| [[Hermine]] | propriété intellectuelle, brevetabilité, FTO |
| [[Bruno]] | budget, coût P0, soutenabilité financière |
| [[Chouette]] | terrain, installation, contraintes naturalistes et maintenance |
| [[Nova]] | image, capteurs, R&D photo/vision |
| [[Clio]] | littérature scientifique, bioacoustique, standards |
| [[Furet]] | recherche concurrentielle et veille stratégique |
| [[Atlas]] | documents stratégiques et R&D |
| [[Miel]] | communauté, récit public, visibilité |
| [[Trace]] | SEO, présence web, découvrabilité |
| [[Araignée]] | IoT, embedded systems, banc de test, protocoles |
| [[Musaraigne]] | Edge AI, TinyML, modèles IA embarqués |

## 5. Règles d'escalade vers JCH

[[Dobby]] sollicite JCH uniquement pour :

- modifier un non-négociable ;
- arbitrer un compromis coût / délai / performance ;
- autoriser une dépense ou un engagement externe ;
- valider une orientation juridique ou IP ;
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
- contributeur si applicable ;
- module ;
- milestone ;
- critère d'acceptation ;
- chemin du livrable dans le repo.

Un travail important sans [[Trace]] dans Plane ou dans le repo est considéré incomplet.

---

*Mis à jour v0.2 le 2026-06-30 — lignes vides comblées, mapping aligné avec roster PKA actuel (31 membres), Fourmi→Araignée et Ariane→Forge fusionnés.*
