---
type: knowledge
status: active
project: Vetalyx
domain: strategy
tags:
  - type/knowledge
  - domain/strategy
  - project/vetalyx
  - graph/pivot
  - type/project
  - status/active
---

# Vetalyx - décisions

## Objectif

Cette note centralise les décisions importantes à documenter pour Vetalyx.

Les décisions formelles doivent idéalement être créées comme notes séparées dans :

```text
11_DECISIONS
```

Cette note sert de table d'orientation.

## Décisions formalisées

### DEC-001 — CCD Interference Policy (v1)
**Date :** 2026-06-06 | **Statut :** ✅ Validé | **Décideur :** JCH + [[Vasco]]

Vetalyx n'intègre pas de CCD blocker au lancement. Le risque d'interférence CCD est documenté sur séra de référence anti-MUXF3 (≥ 3 kUA/L, n ≥ 10) lors de la validation analytique DIXUN. Les résultats sont divulgués aux partenaires cliniques dans les guides d'interprétation. L'intégration d'un CCD blocker est planifiée en **v2**, conditionnée aux données de validation KOL terrain.

**Rationale :** Vetalyx est un test de triage (non un diagnostic de précision). Le standard applicable est Heska/Allercept, pas Nextmune PAX (250–300 composants moléculaires individuels). Le format lignes mixtes génère un effet dilution qui réduit la densité CCD par ligne. Guidelines EAACI 2021 + ACVD (Olivry & Mueller 2018) distinguent explicitement les deux niveaux d'exigence.

**Wording DIAHO/DIXUN (J0-15) :**
> CCD Interference — Notice to Manufacturer. The Vetalyx panel uses multi-allergen blended lines. CCD may contribute background IgE signal on plant-derived allergen lines. The manufacturer shall document CCD interference risk using a minimum of 10 CCD-positive reference sera (anti-MUXF3 ≥ 3 kUA/L) during analytical validation. Results shall be disclosed to clinical partners as part of test interpretation guidelines. CCD blocker integration is designated as a v2 enhancement milestone.

---

### DEC-002 — Architecture produit : SKUs régionaux
**Date :** 2026-06-06 | **Statut :** ✅ Validé | **Décideur :** JCH + [[Vasco]]

Le panel Vetalyx est décliné en **3 variantes régionales physiquement distinctes** (SKUs différents, pas seulement packaging) :

| SKU | Marché | Spécificités allergènes |
|-----|--------|------------------------|
| VTX-EU-NW | France, Benelux | Bouleau, Aulne, Noisetier, Graminées, Acariens stockage |
| VTX-EU-MED | Méditerranée (Sud FR, Italie, Espagne) | Olivier, Cyprès, Pariétaire, Graminées, Acariens |
| VTX-EU-CE | Allemagne, Europe Centrale | Bouleau, Armoise, Ambroisie, Graminées, Acariens stockage |

**Fallback si DIXUN ne peut pas produire 3 SKUs :** test rapide limité à un écran environnemental générique + précision régionale assurée par le microarray (Tier 1) via le logiciel DX Reader. Décision DIXUN attendue J0-15.

**Référence :** [[2026-05-26_VETALYX_Market_Evidence_Pack]] section 6 (Country product fit) + rapport NotebookLM 2026-06-06.

---

## Décisions à créer ou vérifier

| Décision | Statut | Note liée |
|---|---|---|
| Nom Vetalyx | à documenter |  |
| Logo / charte | à documenter |  |
| Nom de domaine | à documenter |  |
| Positionnement produit | → voir [[VETALYX_CLAIMS_MATRIX_FR]] |  |
| Marché prioritaire | → France/Benelux en P0 (voir DEC-002) | DEC-002 |
| Contrats fournisseurs | à documenter |  |
| Stratégie réglementaire | à documenter |  |

## Liens utiles

- [[Vetalyx - stratégie]]
- [[Vetalyx - réglementation]]
- [[Vetalyx - contrats]]
- [[Vetalyx - site web]]

