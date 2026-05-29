# WildNexus - Diagramme canonique Satellite / Base / Cloud

**Version :** v0.1  
**Date :** 2026-05-24  
**Statut :** source canonique  
**Scope :** WildNexus P0/P1/P2  
**Decision liee :** [ADR-009](../02_DECISIONS/ADR/[[ADR-009-architecture-satellite-base-cloud]].md)

## Objet

Ce fichier est la source texte canonique du schema Satellite / Base / Cloud.
Le rendu visuel stable est fourni par `diagramme.svg` ou `diagramme.png`.
Les hypotheses, limites et exceptions sont separees dans `diagramme-notes.md`.

## Diagramme

```mermaid
flowchart LR
  subgraph P0["P0 - Satellite Lite terrain"]
    S1["S1 Camera + IR"]
    S2["S2 Detection evenementielle"]
    S3["S3 Stockage local microSD"]
    S4["S4 Statut batterie / sante"]
    S5["S5 LoRa alertes + metadonnees"]
    S6["S6 Wi-Fi local maintenance"]
  end

  subgraph P1["P1 - Base / Master Nexus"]
    B1["B1 Collecte locale"]
    B2["B2 Index evenements"]
    B3["B3 Analyse lourde BirdNET-Go / YOLO"]
    B4["B4 Tableau de bord local"]
  end

  subgraph P2["P1/P2 - Cloud optionnel"]
    C1["C1 Archive selective"]
    C2["C2 Acces distant"]
    C3["C3 Partage controle"]
    C4["C4 Exports scientifiques"]
  end

  U1["Utilisateur terrain"] --> S6
  S1 --> S2
  S2 --> S3
  S2 --> S4
  S4 --> S5
  S5 --> B1
  S3 -. extraction terrain .-> B1
  B1 --> B2
  B2 --> B3
  B2 --> B4
  B3 --> C1
  B4 --> C2
  C1 --> C3
  C1 --> C4

  S3 -. P0 reste utile sans base .-> U1
  B1 -. non requis pour valider P0 .-> P0
  C1 -. jamais requis pour P0 .-> P0
```

## Lecture rapide

- P0 valide d'abord un satellite terrain autonome.
- La Base/Master Nexus enrichit et orchestre en P1.
- Le Cloud reste optionnel et ne bloque jamais la validation P0.
