# ADR-009 — Architecture Satellite / Base / Cloud

**Date :** 2026-05-23  
**Statut :** accepté  
**Owner PKA :** Dobby + Castor  
**Agent WildNexus :** `wildnexus-program-manager-system-architect`  
**Jalon :** M-01 Architecture P0 gelée

## Contexte

Les derniers dépôts JCH introduisent une architecture avec satellites, master/base, cloud et utilisateur. Cette architecture est correcte, mais ne doit pas rendre le P0 dépendant d'un master ou du cloud.

## Décision

Adopter une architecture en trois niveaux :

1. **Satellite Lite P0** : capte, stocke, survit dehors, transmet seulement alertes/statuts/métadonnées.
2. **Base/Master Nexus P1** : analyse les données, exécute BirdNET-Go/YOLO, indexe, orchestre localement.
3. **Cloud P1/P2** : archive sélective, accès distant, partage contrôlé, jamais requis pour valider P0.

Le Satellite Lite P0 doit rester utile sans Base/Master et sans Cloud. La Base/Master peut être développée en parallèle comme prototype P1.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Satellite autonome + Base P1 | robuste, progressif, terrain d'abord | deux chantiers à coordonner | retenu |
| P0 dépendant du cloud | accès distant immédiat | consommation, complexité, dépendance réseau | rejeté |
| Mesh LoRa P0 | séduisant pour réseau distribué | duty cycle, collisions, routage, complexité | rejeté P0 |
| Pi dans chaque satellite | IA locale facile | consommation, boot, maintenance | rejeté P0 |

## Conséquences

- P0 ne transporte pas de raw continu sur LoRa.
- Les raws restent locaux sur microSD.
- Wi-Fi local sert à la maintenance et à l'extraction.
- LTE/cloud et analyse lourde sont P1/P2.

## Critère de révision

Réviser si un besoin terrain P0 prouvé exige un accès distant raw ou une orchestration multi-satellite avant M-03.
