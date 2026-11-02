# WildNexus — Gantt descriptif (P0)

**Version :** v1.0
**Date :** 2026-10-31
**Statut du projet :** ⚪ GELÉ — focus IOT/VETALYX jusqu'au 15/12 (post-van), puis reprise du bench.
**Rédaction :** Dobby 🦉
**Sources :** `executive-summary.md` (v2, 2026-10-29) · `01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md` (V0.2) · `01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md` (v0.4) · `00_GOVERNANCE/Start.md` (v0.4) · `00_GOVERNANCE/wildnexus-plane-operating-model.md` · `03_P0_ENGINEERING/PROTOCOLES/progress.md` (2026-07-05) · `02_DECISIONS/WILDNEXUS_ADR_INDEX.md`.

---

## 0. TL;DR

WildNexus est un **nœud caméra-piège autonome** (ESP32-S3 + OV5640 + PIR + 2 micros MEMS + LoRa + microSD, 8× AA, IP67) qui détecte la présence animale (filtre binaire embarqué), enregistre l'audio local, et transmet ses alertes en LoRa sans abonnement cellulaire. Objectif P0 : **autonomie ≥ 60 j** prouvée par un EVT terrain 30 j extrapolé.

**État réel :** l'architecture est verrouillée (M-01 ✅), le firmware est prêt sur host (37/37 tests), et il ne manque que du **hardware de banc** (LoRa + microSD) + un **dataset Edge AI** pour redémarrer. Le projet n'est pas perdu — il est gelé à un point précis.

---

## 1. Attention — 3 taxonomies de « WP » coexistent

C'est une source de confusion. Trois documents décrivent les work-packages différemment :

| # | Plane model (v0.1) | Start.md (v0.4) | **Bible V0 (2026-10-29) — canonique** |
|---|---|---|---|
| WP01 | Conception & Architecture | Architecture | **Architecture & ADRs** |
| WP02 | Hardware & Enclos | Procurement | **Hardware nœud** |
| WP03 | Firmware ULP | Firmware | **Énergie & mesure** |
| WP04 | Edge AI | Intégration HW | **Firmware** |
| WP05 | Validation EVT terrain | Tests terrain | **Connectivité (LoRa)** |
| WP06 | Open source & communauté | Documentation | **Boîtier & terrain** |

> **Ce Gantt utilise la taxonomie de la Bible V0** (la plus récente). L'« Edge AI » (filtre binaire) y est rattaché au hardware nœud + ADR-010, pas à un WP dédié.

---

## 2. Jalons (milestones)

| Jalon | Objet | Critère de sortie | Statut |
|---|---|---|---|
| **M-01** | Architecture gelée | 14 ADRs acceptés + scope lock | ✅ **Fait** (2026-05/06) |
| **M-02** | Prototype banc fonctionnel | Capture jour/nuit + trigger OK | 🔵 **Partiel** — firmware host 37/37 ✅, hardware bloqué |
| **M-03** | EVT terrain validé | **Autonomie 30 j + extrapolation 60 j** ; LoRa OK | ⬜ Non démarré |
| **M-04** | Open source + pré-séries | Repo public + 1re série | ⬜ Non démarré |

---

## 3. Gantt (re-basé post-van)

```
Légende :  █ fait · ▒ partiel · ~ gelé · ░ planifié · · non démarré

│  Q2'26 │  Q3'26 │  Q4'26 │  Q1'27 │  Q2'27 │  Q3'27 │
├────────┼────────┼────────┼────────┼────────┼────────┤
WP01 Archi & ADRs  │███████│███████│·······│·······│·······│·······│
WP02 Hardware nœud │▒▒·····│▒▒▒····│~~~~~~~│▒▒▒····│▒▒·····│·······│
WP03 Énergie/mesure│▒······│▒▒·····│~~~~~~~│▒▒▒····│▒▒·····│·······│
WP04 Firmware      │▒······│███████│~~~~~~~│▒▒▒····│▒·······│·······│
WP05 Connectivité  │·······│▒▒·····│~~~~~~~│▒▒▒····│▒·······│·······│
WP06 Boîtier/EVT   │·······│·······│~~~~~~~│░░░░░░░│███████│·······│

M-01 ◆ Q2'26 (fait)   ·   M-02 ◆ Q1'27   ·   M-03 ◆ Q2'27   ·   M-04 ◆ Q3'27
```

- **`~~~~` (Q4'26)** = gel décidé — focus IOT/VETALYX jusqu'au 15/12.
- **Dates re-basées** (estimations Dobby à confirmer à la reprise) : M-02 ~Q1'27, M-03 ~Q2'27 (EVT au printemps = saison idéale), M-04 ~Q3'27.
- **Roadmap d'origine** (périmée par le gel) : M-02 Q3'26, M-03 Q4'26, M-04 Q1'27.

---

## 4. Détail par work-package

### WP01 — Architecture & ADRs ✅ (M-01 fait)

14 ADRs acceptés + 1 sous réserve + 2 proposés + 2 backlog :

| ADR | Décision | Statut |
|---|---|---|
| ADR-001 | MCU ESP32-S3 | ✅ |
| ADR-002 | Caméra OV5640 NoIR | ✅ |
| ADR-003 | LoRa P2P EU868 (SX1262/RAK3172) | ✅ |
| ADR-004 | Stockage microSD | ✅ |
| ADR-005 | Énergie AA + buck | ✅ |
| ADR-006 | Boîtier IP67 | ⚠️ proposé (non bloquant) |
| ADR-007 | Détection PIR | ✅ |
| ADR-008 | Interface capteurs extensible | ✅ |
| ADR-009 | Architecture SAT/Base/Cloud | ✅ |
| ADR-010 | Sécurité/RGPD/Edge AI | ⚠️ **sous réserve** — 6 points R1→R6 |
| ADR-011 | Provisioning des clés | ⚠️ proposé |
| ADR-012 | Stratégie de test P0 | ✅ |
| ADR-013 | Micros I2S stéréo | ✅ |
| ADR-014 | Format payload LoRa (0x05) | ✅ |
| ADR-016 | Firmware machine d'états double cycle | ✅ |
| ADR-017 | Métadonnées audio + format WAV | ✅ |
| ADR-015 | Architecture plugin P1 | 🔁 backlog (P1) |
| ADR-018 | Synchro temporelle (NTP/RTC DS3231) | 🔁 backlog identifié |

### WP02 — Hardware nœud 🔵 (gelé : tout ajout capteur = conso)

Hardware **reçu** : ESP32-S3 DevKit ×2, PPK2, OV5640 ×5, OV2640, MEMS SPH0645LM4H-B ×2, PIR ×2, buck ×10, IR 940 nm, antennes.

| Tâche | Statut | Blocage |
|---|---|---|
| BOM v0.4 (Excel) | ✅ | — |
| SOP-08 caméra OV5640 | ⏳ | pinout mappé, test à exécuter |
| SOP-09 PIR EKMB | ⏳ | hardware ✅ |
| SOP-10 batterie AA + buck | ⏳ | hardware ✅ |
| SOP-06 microSD | ⏳ | **carte SD 128 GB à acheter (~15 €)** |

### WP03 — Énergie & mesure 🔵 (critère de sortie : 60 j)

**Point bloquant R&D n°1** : aucun budget énergie formel (J/évt, veille, pics) alors que 60 j = critère de sortie P0.

| Tâche | Statut | Résultat |
|---|---|---|
| Phase A/B — alive + deep sleep | ✅ | 2026-06-16 |
| Phase C — mesure PPK2 deep sleep | ✅ | 5 acquisitions |
| Phase D/E — wake court + cycle simulé | ⏳ | firmware prêt |
| SOP-18 — budget audio PPK2 | ⏳ | estimation ~1,4 mAh/j |
| Rail 3,3 V (TPS62840) à confirmer en charge | ⏳ | revue R&D : 3,0 V marginal |

### WP04 — Firmware 🔵 (37/37 tests host ✅)

Tout ce qui se teste sans hardware est **livré** :

| Test | Suite | Statut | Commit |
|---|---|---|---|
| FW-01 repo wildnexus-firmware | ESP-IDF modulaire | ✅ | a85f1a9 |
| FW-02 codec ADR-014 | 13/13 | ✅ | a85f1a9 |
| FW-03 machine d'états ADR-016 | 13/13 | ✅ | 131f6fb |
| FW-04 wn_audio.c (I2S+FFT+WAV) | 11/11 | ✅ | 8c44793 |
| FW-05 wn_audio_metadata.c (JSON) | 11/11 | ✅ | 8c44793 |
| SOP-13/17 I2S réel + coexistence PIR/timer | ⏳ | code prêt, test hardware requis | — |
| SOP-12 provisioning | ⏳ | — | — |

> ⚠️ Le repo firmware est **git imbriqué, non versionné par PKA_JCH** (cf. `00_GOVERNANCE/WILDNEXUS_firmware-repo-decision.md`).

### WP05 — Connectivité (LoRa) 🔴 (bloqué)

| Tâche | Statut | Blocage |
|---|---|---|
| SOP-16 payload spectral 0x05 | ✅ (host) | 13/13 roundtrip |
| SOP-07 LoRa réel | 🔴 **bloqué** | **module RAK3172 non commandé** (panier Mouser) |

### WP06 — Boîtier & terrain ⬜ (non démarré)

| Tâche | Statut |
|---|---|
| Boîtier IP67 (ADR-006) | ⚠️ ADR proposé, non tranché |
| EVT terrain 30 j (M-03) | ⬜ |
| Signalétique terrain RGPD (ADR-010 R6) | ⬜ |

---

## 5. Chemin critique et dépendances

```
M-01 ✅ ──► [WP02 + WP03 + WP04 + WP05 en parallèle] ──► M-02 ──► WP06 (EVT) ──► M-03 ──► M-04
```

Dépendances bloquantes :

```
Panier Mouser ~279 € ──► SOP-07 LoRa ──► transmission réelle (M-02/M-03)
Carte SD 128 GB ~15 € ──► SOP-06 + SOP-15 ──► stockage clips réels
Dataset Edge AI (51 img) ──► ADR-010 R4 ──► WP04 filtre binaire
SOP-08 caméra ──► SOP-11 (bench Edge AI) + CAM-03
SOP-13 I2S init ──► test audio réel hardware
```

---

## 6. Blocages à lever (avec coût)

| # | Blocage | Coût | Débloque | Verdict conseil 25/10 |
|---|---|---|---|---|
| 1 | LoRa RAK3172-T EU868 ×2 | ~50 € (part du panier) | SOP-07 → M-02/M-03 | ✅ **Commander** |
| 2 | microSD Swissbit S-45U ×3 | ~54 € | SOP-06/15 | ✅ **Commander** |
| 3 | Connecteurs u.FL + push-push | ~10 € | SOP-07 (co-requis) | ✅ **Bundle** |
| 4 | Reste du panier Mouser (8 lignes standard) | ~160-170 € | — | ⏸ **Reporter** (après revalidation BOM au bench) |
| 5 | Carte SD 128 GB | ~15 € | SOP-06/15 | À acheter |
| 6 | Dataset Edge AI | — (travail) | WP04 filtre binaire | Enrichir (51 img insuffisant) |

**Enveloppe ~110-120 € immédiate** (LoRa + Swissbit + connecteurs) ne déstabilise pas la trésorerie de la deadline IOT/Vanlife du 15/12.

---

## 7. Risques actifs

| Risque | Niveau | Owner | Mitigation |
|---|---|---|---|
| LoRa non testé (RAK3172 backorder) | 🔴 Élevé | Forge | Commander le sous-ensemble à risque ; source alt. SX1262 |
| Modèle Edge AI non entraîné (dataset 51 img) | 🔴 Élevé | Musaraigne | Enrichir le dataset, benchmark ESP32-S3 (ADR-010 R4) |
| Budget énergie absent | 🔴 Critique (R&D) | Bruno + Forge | **WP03 PPK2 prioritaire** avant toute optimisation |
| FTO/IP interne seulement | 🟡 Moyen | Hermine + Renard | FTO externe (0,5-3 k€) avant partenariat/levée |
| RGPD terrain (images de personnes) | 🟡 Moyen | Renard | Signalétique + procédure (ADR-010 R6, M-03) |
| Variante CERN OHL non décidée (P/W/S) | 🟡 Moyen | Hermine | Trancher avant publication M-04 |

---

## 8. Budget (ancrage)

- Enveloppe P0 : **1 000 €** — **~758 € engagé/prévu, réserve ~242 €**.
- BOM production (100 u.) : **~92,45 €/nœud** → prix cible 149-179 €, marge brute ~40 %.
- Coût système honnête (nœud + Station) : ~400-480 € (vs concurrents 799 $ + abonnement ≥180 $/an).

---

## 9. Prochaines actions (à la reprise)

1. **WP03 PPK2** — formaliser le budget énergie + confirmer rail 3,3 V (débloque le critère 60 j).
2. **Débloquer RAK3172** (SOP-07) — commander le sous-ensemble ~110-120 €.
3. **Acheter carte SD 128 GB** (~15 €).
4. Enrichir le **dataset Edge AI** (ADR-010 R4).
5. Corriger `executive-summary.md` (messaging P0 vs P1) — déjà fait en v2.
6. Modèle financier complet (marge nette, coûts cachés CE/RED, BFR).
7. Trancher la **variante CERN OHL** + planifier FTO externe.
8. Obtenir 1-2 **pilotes terrain** nommés/datés.

---

## 10. Synchronisation Plane (2026-10-31)

Le Gantt est synchronisé dans Plane (projet `03_WILDNEXUS`) :

- **25 items** : 4 milestones (M-01→M-04) + 6 epics (WP01→WP06, taxonomie canonique) + 15 tâches d'exécution.
- **Dates** posées sur milestones + epics (`start_date`/`target_date`) → barres Gantt.
- **États** : M-01/WP01 → Done ; M-02/WP02-05 → In Progress ; M-03/M-04/WP06 → Todo.
- **Dépendances** : 8 relations `blocked_by` (chaîne M-01→M-02→M-03→M-04 + WP02-06 → M-01/M-02).

Mécanisme (idempotent, rejouable) :
- `00_GOVERNANCE/wildnexus-plane-seed-backlog.md` — noms (taxonomie canonique) + tâches.
- `00_GOVERNANCE/wildnexus-plane-gantt.json` — dates + états + dépendances.
- `scripts/seed_wildnexus_plane.py --replace --apply` — re-seed complet (delete + create + relations).

> ⚠️ Le serveur MCP Plane (outils `plane_*`) utilise un token périmé (403). Le seed passe
> par `pka_plane_adapter` qui lit le token fichier (`~/.config/pka-jch/plane_api_token.txt`).

---

*Généré le 2026-10-31 par Dobby 🦉 — référence de pilotage, à régénérer après reprise du bench post-van.*
