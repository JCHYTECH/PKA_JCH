# WildNexus — ADR Index

**Version :** v1.1
**Date :** 2026-11-05
**Statut :** Projet repris (2026-11-11) — 16 ADR rédigés (13 acceptés, 1 sous réserve, 2 proposés) + ADR-015 en backlog ; ADR-018 identifié
**Owner :** [[Dobby]] + [[Forge]]

## 1. Objet

Les ADR documentent les décisions techniques qui structurent P0.

## 2. ADR existants

| ADR | Sujet | Owner PKA | Jalon | Statut |
|---|---|---|---|---|
| [ADR-001](ADR-001-choix-mcu-p0.md) | Choix MCU P0 — ESP32-S3 | [[Castor]] + [[Forge]] | M-01 | **Accepté** (2026-05-18) |
| [ADR-002](ADR-002-choix-camera-ir-p0.md) | Choix caméra / IR P0 — OV5640 | [[Nova]] + [[Lynx]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-003](ADR-003-choix-radio-lpwan-p0.md) | Choix radio / LPWAN P0 — LoRa P2P EU868 | [[Forge]] + [[Chouette]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-004](ADR-004-stockage-local-p0.md) | Stockage local P0 — microSD | [[Castor]] + [[Forge]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-005](ADR-005-energie-autonomie-p0.md) | Énergie et autonomie P0 — AA + buck | [[Bruno]] + [[Chouette]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-006](ADR-006-boitier-ip67-p0.md) | Boîtier IP67 et montage terrain | [[Chouette]] | M-01 | **Proposé** — non bloquant WP02 |
| [ADR-007](ADR-007-detection-evenementielle-p0.md) | Détection événementielle P0 | [[Nova]] + [[Forge]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-008](ADR-008-interface-capteurs-extensible-p0.md) | Interface capteurs extensible P0 | [[Castor]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-009](ADR-009-architecture-satellite-base-cloud.md) | Architecture Satellite / Base / Cloud | [[Dobby]] + [[Castor]] | M-01 | **Accepté** (2026-05-23) |
| [ADR-010](ADR-010-securite-rgpd-edge-ai.md) | Sécurité, Chiffrement et RGPD Edge AI | [[Castor]] + [[Forge]] + [[Hermine]] + [[Renard]] | M-02 / M-03 | **Accepté sous réserve** (2026-06-08) |
| [ADR-011](ADR-011-provisioning-cycle-de-vie-cles.md) | Provisioning et cycle de vie des clés | [[Castor]] + [[Forge]] + [[Hermine]] | M-02 / M-03 | **Proposé** (2026-06-08) |
| [ADR-012](ADR-012-strategie-test-p0.md) | Stratégie de test P0 (banc, terrain, régression) | [[Forge]] + [[Castor]] + [[Araignée]] | M-02 | **Accepté** (2026-06-12) |
| [ADR-013](ADR-013-couche-acoustique-microphones-p0.md) | Couche acoustique : microphones et monitoring sonore | [[Dobby]] + JCH | M-02 | **Accepté** (2026-06-19) |
| [ADR-014](ADR-014-format-payload-lora.md) | Format données et protocole transmission (payload LoRa) — caméra + spectral | [[Forge]] + [[Chouette]] | M-02 | **Accepté** (2026-07-05) |
| ADR-015 — non rédigé | Architecture plugin P1 (hardware + software) | [[Castor]] + [[Forge]] | P1 — après M-03 | **Backlog** |
| [ADR-016](ADR-016-firmware-integre-p0.md) | Firmware intégré P0 — machine d'états double cycle (caméra + audio) | [[Forge]] | M-02 | **Accepté** (2026-07-05) |
| [ADR-017](ADR-017-schema-metadonnees-audio.md) | Schéma métadonnées audio et format de fichiers | [[Dobby]] + [[Forge]] + [[Chouette]] | M-02 | **Accepté** (2026-07-05) |

> **Historique corrections :**
> - ADR-014 (payload LoRa) : créé le 12/06, mis à jour le 05/07 (type spectral 0x05, commandes downlink 0x05/0x06, flag audio_clip_ready). Accepté le 05/07.
> - ADR-016 (firmware intégré) : créé le 30/06, mis à jour le 05/07 (cycle AUDIO timer-triggered). Accepté le 05/07.
> - ADR-017 (métadonnées audio) : créé et accepté le 05/07 — cible WAV 16 kHz/16-bit stéréo, sidecar JSON et SD 128 GB ; conversions et compatibilité BirdNET/InsectSet459/TweetyBERT à démontrer sur fichiers réels.
> - ADR-012 (stratégie de test) : statut documentaire corrigé en accepté ; des tests hôte ont été consignés en juin, sans validation matérielle équivalente.

## 3. Points de réserve actifs

| ADR | Point | Owner | Échéance |
|---|---|---|---|
| ADR-010 — R1 | Diversification de clé → ADR-011 | [[Castor]] + [[Forge]] | M-02 |
| ADR-010 — R2 | Articulation MIT + `ETHICS.md` + politique/contrats ; ce n'est pas une dual-licence | [[Hermine]] + [[Renard]] | Avant publication/contrat |
| ADR-010 — R3 | Procédure droit d'accès RGPD | [[Renard]] | M-03 |
| ADR-010 — R4 | Benchmark Edge AI ESP32-S3 | [[Forge]] + [[Nova]] + [[Musaraigne]] | M-02 |
| ADR-010 — R5 | Impact énergétique Edge AI x ADR-005 | [[Bruno]] + [[Forge]] | M-02 |
| ADR-010 — R6 | Template signalétique terrain | [[Renard]] | M-03 |

## 4. ADR à produire (backlog)

| ADR | Sujet | Owner proposé | Priorité |
|---|---|---|---|
| ADR-015 | Architecture plugin P1 (hardware + software) | [[Castor]] + [[Forge]] | P1 — après M-03 |
| ADR-018 | Synchronisation temporelle (NTP + RTC DS3231) | [[Forge]] + [[Castor]] | M-02/M-03 |

> **ADR-018 identifié le 2026-07-05 :** L'audit WildNexus ↔ InsectNet/NEXUS_ACOUSTIC a révélé l'absence de protocole de synchronisation temporelle image↔audio. L'ESP32-S3 n'a pas de RTC matérielle et sa dérive en deep sleep doit être mesurée. Les pistes à arbitrer dans ADR-018 sont le NTP au provisioning pour P0 et, si le besoin est démontré, une RTC externe en P1 ; coût, intégration et précision restent à établir.

---

*Mis à jour le 2026-11-05 par Dobby 🦉 — lien ADR-015 retiré (document non rédigé), comptage corrigé : 16 ADR rédigés, dont 13 acceptés, 1 sous réserve et 2 proposés ; ADR-015 reste en backlog et ADR-018 reste à produire.*
