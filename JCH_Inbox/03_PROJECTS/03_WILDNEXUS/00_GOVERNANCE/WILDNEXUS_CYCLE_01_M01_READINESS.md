# WildNexus — Cycle 01 / M-01 Readiness

**Version :** v0.2  
**Date :** 2026-06-30  
**Statut :** ✅ M-01 complété — Cycle 01 clôturé, M-02 actif  
**Owner :** [[Dobby]]  

## 1. Objectif du cycle

Préparer le gel d'architecture P0 (`M-01 Architecture gelée`) sans fabrication ni commande significative.

Le cycle est terminé quand les choix caméra, MCU, radio, budget, gouvernance d'agents et risques juridiques sont suffisamment cadrés pour autoriser le passage vers `M-02 Prototype banc fonctionnel`.

> **Statut :** M-01 a été marqué prêt le 2026-05-23 avec 10 ADRs acceptés. 4 ADRs supplémentaires ont été créés pendant la transition M-01→M-02 (ADR-010 à ADR-014). Le cycle 01 est clôturé.

## 2. Situation initiale (mai 2026)

| Domaine | Statut | Commentaire |
|---|---|---|
| Périmètre P0 | Cadré | `WILDNEXUS_P0_SCOPE_LOCK.md` verrouille les exclusions P0 |
| Mapping agents | Cadré | `WILDNEXUS_AGENT_MAPPING.md` relie domaines techniques et spécialistes PKA |
| Budget P0 | Confirmé | `WILDNEXUS_P0_BUDGET_RANGE.md` — enveloppe 1 000€ |
| Plane | Synchronisé | API locale revenue après installation du service launchd |
| Docker | Relancé automatiquement | service launchd PKA installé pour démarrer Docker Desktop puis Plane |
| Backlog | Synchronisé | items Cycle 01 créés dans Plane le 2026-05-18 |
| Données projet | Initialisé | `data/README.md` créé |

## 3. Fronts du cycle 01 (clôturés)

| Domaine | Owner PKA | Livrable | Statut |
|---|---|---|---|
| MCU | [[Castor]] + [[Forge]] | ADR-001 (ESP32-S3) | ✅ Accepté |
| Caméra / IR | [[Nova]] + [[Lynx]] | ADR-002 (OV5640) | ✅ Accepté |
| Radio / LPWAN | [[Forge]] + [[Chouette]] | ADR-003 (LoRa P2P EU868) | ✅ Accepté |
| Stockage | [[Castor]] + [[Forge]] | ADR-004 (microSD) | ✅ Accepté |
| Énergie | [[Bruno]] + [[Chouette]] | ADR-005 (AA + buck) | ✅ Accepté |
| Boîtier | [[Chouette]] | ADR-006 (IP67) | ⚠️ Proposé |
| Détection | [[Nova]] + [[Forge]] | ADR-007 (PIR) | ✅ Accepté |
| Capteurs ext. | [[Castor]] | ADR-008 (I2C/SPI bus) | ✅ Accepté |
| Architecture | [[Dobby]] + [[Castor]] | ADR-009 (SAT/Base/Cloud) | ✅ Accepté |
| Sécurité/RGPD | [[Castor]] + [[Forge]] + [[Hermine]] + [[Renard]] | ADR-010 (Edge AI + RGPD) | ✅ Accepté sous réserve |
| Budget | [[Bruno]] | Enveloppe 1 000€ confirmée | ✅ Validé |
| Licence / FTO | [[Renard]] + [[Hermine]] | Usage policy + matrix v0.1 | ⚠️ Draft — licence finale à rédiger |

## 4. Définition de `M-01 ready` (atteint)

`M-01` a été marqué prêt quand :

- ✅ une caméra candidate est choisie et justifiée (OV5640, ADR-002) ;
- ✅ un MCU candidat est choisi et justifié (ESP32-S3, ADR-001) ;
- ✅ une option radio / LPWAN est choisie et justifiée (LoRa P2P, ADR-003) ;
- ✅ l'enveloppe P0 est confirmée (1 000€) ;
- ✅ le registre composants critiques contient au moins une alternative par poste bloquant ;
- ⚠️ la licence / FTO ne bloque pas le prototypage interne (licence finale repoussée M-04) ;
- ✅ le périmètre P0 reste strict ;
- ⚠️ les risques RGPD terrain ont un owner (Renard) et un livrable concret (signalétique + procédure — ADR-010 R6, échéance M-03) ;
- ✅ Plane est synchronisé.

## 5. Risques actifs ( hérités en M-02)

| Risque | Niveau | Owner | Mitigation |
|---|---|---|---|
| Scope creep bioacoustique | Réduit | [[Dobby]] | Verrou P0 tenu, ADR-013 accepté (capture locale seulement) |
| Budget P0 sous-estimé | Réduit | [[Bruno]] | Budget v0.3 confirmé, réel ~610€ engagé / 1000€ |
| FTO / licence retardée | Moyen | [[Renard]] + [[Hermine]] | Prototypage interne autorisé, publication repoussée M-04 |
| Disponibilité composants | Réduit | [[Bruno]] + [[Forge]] | Composants critiques reçus, panier Mouser restant à commander |
| RGPD terrain EVT | Moyen | [[Renard]] | Signalétique + procédure floutage en attente (ADR-010 R6, M-03) |
| Modèle Edge AI non entraîné | 🔴 Élevé | [[Musaraigne]] | Dataset 51 images insuffisant, ADR-010 R4 bloquée |
| LoRa non testé | 🔴 Élevé | [[Forge]] | Module SX1262 dans panier Mouser restant ~279€ |

## 6. Prochaines actions (M-02)

Voir `00_GOVERNANCE/Start.md` §4.3 — chantier actif.

---

*Mis à jour v0.2 le 2026-06-30 — cycle 01 clôturé, lignes vides comblées, risques hérités en M-02.*
