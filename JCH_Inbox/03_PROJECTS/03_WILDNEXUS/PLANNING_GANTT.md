# WildNexus — Plan de reprise P0

Version 2.0 — 2026-11-05. Statut : gelé depuis juillet ; reprise post-van à replanifier au signal de JCH. Ce document remplace les anciennes dates estimatives par des dépendances et des preuves.

Sources actives : `WILDNEXUS_DEVICE/00_GOVERNANCE/Start.md`, scope lock v0.5, index ADR v1.1, `progress.md`, budget P0 v0.5. Les documents Plane/Gantt antérieurs sont des instantanés à synchroniser, pas des dates promises.

## 1. État de départ

L'architecture P0 est cadrée, mais la validation technique est inachevée. Les 37/37 tests hôte historiques ne valident ni l'ESP32-S3, ni les capteurs, ni la radio, ni l'autonomie. Seize ADR sont rédigés : 13 acceptés, ADR-010 sous réserve, ADR-006/011 proposés. ADR-015 n'est pas rédigé et ADR-018 reste à produire.

La projection provisoire est d'environ 904 €, réserve théorique 96 €. Le seuil interne de 900 € est dépassé : aucune commande avant réconciliation et autorisation JCH.

## 2. Taxonomie de travail

La liste WP01→WP06 de `Start.md` et de la bible V0.3 sert de structure documentaire :

- WP01 Architecture et ADR ;
- WP02 Hardware nœud ;
- WP03 Énergie et mesure ;
- WP04 Firmware ;
- WP05 Connectivité ;
- WP06 Boîtier et terrain.

Les anciennes taxonomies Plane sont historiques. À la reprise, mapper les items existants sans dupliquer les epics ni présumer que l'état Plane est à jour.

## 3. Jalons et conditions de sortie

| Jalon | État | Condition de sortie |
|---|---|---|
| M-01 Cadrage | Documentation initiale réalisée, révisions en cours | Périmètre et réserves compris ; pas une validation matérielle |
| M-02 Prototype banc | Gelé, partiel | Matrice scope lock : captures/audio/SD/IA/gateway/énergie démontrés sur cible |
| M-03 EVT terrain | Non commencé | M-02 + ADR-018 + boîtier + RGPD/sécurité + protocole EVT |
| M-04 Publication/pré-séries | Non commencé | DVT, conformité, licences, coûts et industrialisation validés avant pré-série |

M-04 ne signifie pas que la publication du code et une pré-série sont une seule preuve : les textes de licence peuvent être publiés plus tôt, tandis que toute pré-série exige les étapes industrielles et réglementaires appropriées.

## 4. Séquence relative

| Étape | Contenu | Dépendances | Preuve |
|---|---|---|---|
| R0 | Inventaire, factures, datasheets, schémas, budget | Signal JCH | Stock et budget réconciliés ; achats arbitrés |
| R1a | Phases D/E, SD, caméra, PIR | R0 | Rapports et acquisitions sur cible |
| R1b | Audio réel et pipelines | Micros identifiés + R1a SD | WAV/JSON produits et lus par pipelines |
| R1c | Benchmark IA | Caméra réelle + dataset | Comparaison modèles et mesures SOP-11 |
| R1d | Radio et gateway | Achat autorisé + matériel reçu | Deux types de paquets reçus/journalisés, erreurs testées |
| R2 | Intégration et énergie | R1a→R1d + suspension SOP-10 levée | Cycles ADR-016, modèle Wh complet, critères M-02 |
| R3 | Boîtier et EVT | M-02 + ADR-018 + exigences terrain | Rapport EVT et anomalies traitées |
| R4 | Publication/industrialisation | Revues licence et technique | Publication décidée ; DVT/conformité/coûts avant pré-série |

Les tâches R1a→R1d peuvent avancer en parallèle seulement après leurs prérequis. Aucun créneau trimestriel n'est attribué tant que JCH n'a pas confirmé sa disponibilité et les achats.

## 5. Points de sécurité et blocages

- SOP-10 suspendue : pas de pack AA ou d'injection 3,3 V sur broche 5 V avant revue complète.
- Références micros/PIR et pinouts à confirmer avant câblage.
- Radio non commandée ; prix et contenu du panier à actualiser.
- Dataset IA et modèle retenu non validés ; sorties factices interdites comme preuves.
- Gateway P0 absente ; le codec hôte ne démontre pas la radio.
- Autonomie 60 jours, portée et IP67 restent des cibles.
- ADR-018, procédures RGPD et sécurité nécessaires avant terrain.

## 6. Reprise opérationnelle

1. JCH donne le signal et arbitre le budget après réconciliation.
2. Mettre à jour `Start.md` et `progress.md` avec les preuves du jour.
3. Lire l'état Plane existant, marquer les tâches gelées/obsolètes et synchroniser sans `--replace` destructif ni doublon.
4. Créer les dates seulement après estimation des tâches restantes et confirmation JCH.
5. Réviser ce document à chaque jalon, sans modifier les archives.

Les fichiers `GANTT.md` et `wildnexus-plane-gantt.json` ne doivent pas servir à rejouer automatiquement les anciennes dates. Toute action externe de synchronisation est décidée séparément avec JCH.
