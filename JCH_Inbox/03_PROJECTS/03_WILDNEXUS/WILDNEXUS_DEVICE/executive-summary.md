# WildNexus — Résumé exécutif (v2)

> **Document externe** — investisseurs, partenaires, banques.
> **Version 2.0 — 2026-10-29.** Remplace la v1.0 (2026-07-03), archivée dans `HISTORIQUE/executive-summary-v1_2026-07-03.md`.
> **Aligné sur le périmètre P0 réel** (`WILDNEXUS_P0_SCOPE_LOCK.md` v0.4). Document de référence interne : `01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md` (la « bible V0 »).

---

## En une phrase

**WildNexus est un nœud caméra-piège autonome à intelligence embarquée qui détecte la présence animale et transmet ses alertes en radio longue portée, sans abonnement cellulaire — un instrument d'observation de terrain à coût maîtrisé, ouvert et standardisé.**

## Le problème

Les caméras-pièges classiques produisent **75 à 90 % de faux déclenchements** (vent, végétation). Le tri manuel paralyse chercheurs et gestionnaires de réserves, et la récupération des données par visites terrain est lente et perturbante. Les solutions existantes sont soit fermées et sans réseau (grand public), soit lourdes et coûteuses (institutionnel).

## La solution — périmètre P0 (ce qui est réellement engagé)

Un nœud autonome (ESP32-S3 + caméra OV5640 + PIR + 2 micros MEMS) qui :
- **capture** jour et nuit (déclenchement PIR + filtre embarqué **binaire animal / non-animal**) ;
- **enregistre** l'audio local (clips WAV courts + descripteurs spectraux) ;
- **transmet** par **LoRa** (P2P, 500 m-3 km forêt) — **zéro abonnement cellulaire** ;
- **stocke** en local (microSD, métadonnées standardisées Camtrap-DP) ;
- **tient ≥ 60 jours** sur piles AA (L91) ;
- **boîtier IP67**.

La Station (gateway) locale consolide et expose les données ; elle est vendue séparément.

## Ce qui n'est PAS dans P0 (roadmap P1+)

Reconnaissance d'espèce (BirdNET/SpeciesNet), autonomie solaire, multi-capteurs, transfert d'image. Ces fonctions sont **planifiées**, pas engagées dans le prototype P0. (La communication externe doit refléter cette distinction.)

## Le marché et la demande

- Marché des systèmes de caméras-pièges : ~**1,1 Md$ (2025) → ~2,2 Md$ (2034)**, CAGR ~7,7 % (ordre de grandeur, sources hétérogènes).
- Le vrai moteur est **réglementaire** : **CSRD** (ESRS E4 biodiversité), **TNFD**, **Biodiversity Net Gain** britannique (suivi obligatoire 30 ans), **EU Nature Credits** (cadre 2026) → demande de **données de biodiversité continues et auditables**.
- Segments : bureaux d'études et acheteurs de conformité (co-primaire), réserves/parcs (co-primaire), recherche (secondaire).

## Différenciation

- **Zéro abonnement data** (LoRa, pas de SIM) — là où TrailGuard (~799 $) et Nightjar facturent cellulaire/satellite.
- **Prix nœud** cible 149-179 € · **open source** (hardware + firmware) · **conformité EU** · **données standardisées**.
- **Nuance TCO** : le prix nœud seul n'inclut pas la Station ; le coût système utile (nœud + station) doit être communiqué honnêtement (~400-480 €), vs concurrents 799 $ + abonnement ≥180 $/an.

## Modèle économique

- **Matériel** : nœud FIELD (149-179 €) + Station (249-299 €) ; gamme FIELD+/STATION+ en P1.
- **Licence** : hardware CERN OHL v2 ; logiciel AGPL v3 + licence commerciale (dual).
- **Services (relais de croissance)** : monitoring-as-a-service (HaaS), **rapports de conformité biodiversité**, data/API, installation/formation.
- **Économie unitaire (réaliste)** : BOM production **~92,45 €**/nœud → marge brute ~40 % avant coûts complets (assemblage, test, certification, logistique, support). Modèle financier détaillé à finaliser.

## Roadmap

| Phase | Période | Jalon |
|---|---|---|
| M-01 | ✅ | Architecture gelée |
| M-02 | Q3 2026 | Prototype banc |
| M-03 | Q4 2026 | **EVT terrain — autonomie 30 j + extrapolation 60 j** |
| M-04 | Q1 2027 | Open source + pré-séries |

## Budget P0

Enveloppe **1 000 €** — **~758 € engagé/prévu, réserve ~242 €**. (Prototype 2 nœuds DevKit + outillage PPK2 ; ne pas confondre avec le BOM de production 92,45 €/nœud.)

## Propriété intellectuelle

Marque WildNexus™ (JCHYTECH) · hardware open source (CERN OHL v2) · logiciel dual-licence (AGPL v3 / commerciale) · analyse FTO en cours (à externaliser avant partenariat/levée).

## L'équipe

Jean-Claude Havaux — fondateur, zoologiste (ULiège), photographe naturaliste · JCHYTECH · équipe PKA_JCH (31 spécialistes IA orchestrés par Dobby 🦉).

---

*Résumé externe aligné P0. Pour le détail technique, financier et la revue expert : `01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md`.*
