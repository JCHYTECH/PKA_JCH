# WildNexus — ADR Index

**Version :** v0.5
**Date :** 2026-06-08
**Statut :** Ouvert — M-01 gelé, en attente ADR-006 (boîtier)
**Owner :** [[Dobby]] + [[Forge]]

## 1. Objet

Les ADR documentent les décisions techniques qui structurent P0.

## 2. ADR existants

| ADR | Sujet | Owner PKA | Jalon | Statut |
|---|---|---|---|---|
| [ADR-001](ADR/[[ADR-001-choix-mcu-p0]].md) | Choix MCU P0 — ESP32-S3 | [[Castor]] + [[Forge]] | M-01 | **Accepté** (2026-05-18) |
| [ADR-002](ADR/[[ADR-002-choix-camera-ir-p0]].md) | Choix caméra / IR P0 — OV5640 | [[Nova]] + [[Lynx]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-003](ADR/[[ADR-003-choix-radio-lpwan-p0]].md) | Choix radio / LPWAN P0 — LoRa P2P EU868 | [[Forge]] + [[Chouette]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-004](ADR/[[ADR-004-stockage-local-p0]].md) | Stockage local P0 — microSD | [[Castor]] + [[Forge]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-005](ADR/[[ADR-005-energie-autonomie-p0]].md) | Énergie et autonomie P0 — AA + buck | [[Bruno]] + [[Chouette]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-006](ADR/[[ADR-006-boitier-ip67-montage-terrain]].md) | Boîtier IP67 et montage terrain | [[Chouette]] | M-01 | **Proposé** — non bloquant WP02 |
| [ADR-007](ADR/[[ADR-007-detection-evenementielle-p0]].md) | Détection événementielle P0 | [[Nova]] + [[Forge]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-008](ADR/[[ADR-008-interface-capteurs-extensible-p0]].md) | Interface capteurs extensible P0 | [[Castor]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-009](ADR/[[ADR-009-architecture-satellite-base-cloud]].md) | Architecture Satellite / Base / Cloud | [[Dobby]] + [[Castor]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-010](ADR/[[ADR-010-securite-rgpd-edge-ai]].md) | Sécurité, Chiffrement et RGPD Edge AI | [[Castor]] + [[Forge]] + [[Hermine]] + [[Renard]] | M-02 / M-03 | **Accepté sous réserve** (2026-06-08) |
| [ADR-011](ADR/[[ADR-011-provisioning-cycle-de-vie-cles]].md) | Provisioning et cycle de vie des clés | [[Castor]] + [[Forge]] + [[Hermine]] | M-02 / M-03 | **Proposé** (2026-06-08) |

> **Note 2026-06-08 :** ADR-002 à ADR-009 (sauf ADR-006) étaient listés « Proposé » dans l'index v0.4 par incohérence avec le WP01 architecture freeze summary (2026-05-23) qui les déclare acceptés. Cette version v0.5 aligne l'index sur la réalité des décisions JCH.

## 3. Points de réserve actifs

| ADR | Point | Owner | Échéance |
|---|---|---|---|
| ADR-010 — R1 | Diversification de clé → ADR-011 | [[Castor]] + [[Forge]] | M-02 |
| ADR-010 — R2 | Dual-license (MIT + ETHICS.md) | [[Hermine]] + [[Renard]] | M-02 |
| ADR-010 — R3 | Procédure droit d'accès RGPD | [[Renard]] | M-03 |
| ADR-010 — R4 | Benchmark Edge AI ESP32-S3 | [[Forge]] + [[Nova]] | M-02 |
| ADR-010 — R5 | Impact énergétique Edge AI x ADR-005 | [[Bruno]] + [[Forge]] | M-02 |
| ADR-010 — R6 | Template signalétique terrain | [[Renard]] | M-03 |

## 4. ADR à produire (backlog)

| ADR | Sujet | Owner proposé | Priorité |
|---|---|---|---|
| ADR-012 | Stratégie de test P0 (banc, terrain, regression) | [[Forge]] + [[Castor]] | M-02 |
| ADR-013 | Format données et protocole transmission (payload LoRa) | [[Forge]] + [[Chouette]] | M-02 |
