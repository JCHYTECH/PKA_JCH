# 09_PRODUCT_SHEETS — Fiches produit WildNexus

> Générées le 2026-06-19 par Dobby 🦉 — Analyse Arbor (OBSERVE → IDEATE → DECIDE)
> Basées sur : Master Architecture WN, Founding Document v0.2, 14 ADRs, BOM v0.2c, Usage Matrix

---

## Ligne FIELD — Nœuds terrain

| # | Fiche | Produit | Phase | Prix cible | Marché |
|---|-------|---------|-------|------------|--------|
| F1 | [F1_FIELD.md](F1_FIELD.md) | **WildNexus FIELD** | P0 MVP | 149-179€ | Naturalistes, associations |
| F2 | [F2_FIELD_PLUS.md](F2_FIELD_PLUS.md) | **WildNexus FIELD+** | P1 | 299-349€ | Réserves, chercheurs |

## Ligne STATION — Hubs locaux

| # | Fiche | Produit | Phase | Prix cible | Marché |
|---|-------|---------|-------|------------|--------|
| S1 | [S1_STATION.md](S1_STATION.md) | **WildNexus STATION** | P1 | 249-299€ | Gestionnaires de site |
| S2 | [S2_STATION_PLUS.md](S2_STATION_PLUS.md) | **WildNexus STATION+** | P1+ | 599-799€ | Chercheurs, labs |

## Ligne Standalone — Bioacoustique

| # | Fiche | Produit | Phase | Prix cible | Marché |
|---|-------|---------|-------|------------|--------|
| A1 | [A1_NEXUS_ACOUSTIC.md](A1_NEXUS_ACOUSTIC.md) | **Nexus Acoustic** | P1 | 249-299€ | Bioacousticiens, ornithologues |

---

## Gamme complète — Vue d'ensemble

```
PRIX
800€ ┤                                         ● STATION+
700€ ┤
600€ ┤
500€ ┤
400€ ┤
300€ ┤              ● FIELD+    ● STATION
200€ ┤    ● FIELD              ● Nexus Acoustic
100€ ┤
     └──────────────────────────────────────────→ COMPLEXITÉ
        Simple               Intermédiaire        Avancé
        (P0)                 (P1)                 (P1+/P2)
```

### Chemin d'adoption naturel

```
Naturaliste amateur → FIELD ×1 (149€)
                    → FIELD ×3 + STATION ×1 (249€)
                    → FIELD+ ×1 + STATION+ ×1 (599€)
                    → Nexus Acoustic ×1 (249€)
                    
Total progressif : 149€ → 696€ → 1 295€ → 1 544€
```

---

## Spécifications partagées (tous produits FIELD/STATION)

- **Open source** — firmware, dashboard, modèles IA sous licence à définir (cf. Usage Policy)
- **Données locales** — pas de cloud obligatoire, vous possédez vos données
- **Pas de vendor lock-in** — formats standards (Camtrap-DP, Darwin Core, CSV, JSON)
- **LoRa EU868 P2P** — infrastructure propre, zéro dépendance externe
- **Conforme RGPD** — pas d'images humaines, traitement local
- **Usage matrix** — tout usage est qualifié selon la matrice WildNexus

---

## Références croisées

- [01_FOUNDATION/MASTER_ARCHITECTURE_WN.md](../01_FOUNDATION/MASTER_ARCHITECTURE_WN.md) — vision produit, phases P0/P1/P2
- [01_FOUNDATION/wildnexus-usage-matrix.md](../01_FOUNDATION/wildnexus-usage-matrix.md) — qualification d'usage par persona
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](../01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md) — périmètre P0
- [02_DECISIONS/WILDNEXUS_ADR_INDEX.md](../02_DECISIONS/WILDNEXUS_ADR_INDEX.md) — index des 14 ADRs
- [03_P0_ENGINEERING/07_PROCUREMENT_BOM/](../03_P0_ENGINEERING/07_PROCUREMENT_BOM/) — BOM v0.2c
- [../../12_NEXUS_ACOUSTIC/](../../12_NEXUS_ACOUSTIC/) — projet Nexus Acoustic autonome
- [../../TEAM_Inbox/2026-06-19_dobby_arbor-wildnexus-product-line.md](../../TEAM_Inbox/2026-06-19_dobby_arbor-wildnexus-product-line.md) — analyse Arbor complète

---

*Généré par Dobby 🦉 — 2026-06-19*
