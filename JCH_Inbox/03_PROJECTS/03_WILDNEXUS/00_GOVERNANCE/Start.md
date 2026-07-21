# WildNexus — Protocole de lancement

**Version :** v0.4  
**Date :** 2026-07-05  
**Statut :** Actif — M-01 gelé, M-02 en cours (SOPs A→C complétées, D→E + SOPs 06-18 en attente)  
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Pilotage :** [[Dobby]]  

---

## 1. Intention

Ce document définit le comportement attendu de [[Dobby]] quand JCH active le projet WildNexus.

L'objectif n'est pas de décrire le projet. Les documents fondateurs le font déjà. L'objectif est de préciser le mode d'exécution :
- quoi démarre ;
- dans quel ordre ;
- ce qui est automatisé ;
- ce qui remonte à JCH ;
- où l'état du projet est visible.

Principe directeur :

> JCH doit voir les décisions, les risques et les preuves. [[Dobby]] doit absorber le suivi, la coordination et la maintenance opérationnelle.

---

## 2. Sources De Vérité

Au lancement, [[Dobby]] travaille depuis ces références :

### 2.1 Fondation (immuables sauf décision JCH)
- `01_FOUNDATION/MASTER_ARCHITECTURE_WN.md` — architecture globale (document de cadrage initial)
- `01_FOUNDATION/wildnexus-founding-document-v0.2.md` — document fondateur consolidé (DRAFT — validation JC en cours)
- `00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md` — philosophie d'ingénierie
- `01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md` — périmètre P0 verrouillé (v0.4)

### 2.2 Décisions (ADR Index)
- `02_DECISIONS/WILDNEXUS_ADR_INDEX.md` — **17 ADRs** (ADR-001 à ADR-017)
  - **14 acceptés** (ADR-001 à ADR-005, ADR-007 à ADR-009, ADR-012 à ADR-014, ADR-016, ADR-017)
  - **1 accepté sous réserve** (ADR-010 — 6 points de réserve actifs)
  - **2 proposés** (ADR-006, ADR-011)
  - **1 backlog** (ADR-015 — plugin P1)
  - **1 backlog identifié** (ADR-018 — synchro temporelle)
- Chaque ADR est un document autonome dans `02_DECISIONS/ADR/`

### 2.3 Ingénierie P0 (M-02 actif)
- `03_P0_ENGINEERING/PROTOCOLES/progress.md` — tracker de protocoles (source de vérité)
- `03_P0_ENGINEERING/PROTOCOLES/` — 18 SOPs individuelles + 3 tests caméra + 5 tests firmware
  - ✅ Phases A→C complétées (ESP32 alive, deep sleep, PPK2)
  - ⏳ Phases D→E en attente (wake short, simulation cycle)
  - ⏳ SOPs 06-12 en attente (SD, LoRa, caméra, PIR, batterie, Edge AI, micro provisioning)
  - ⏳ SOPs 13-18 en attente (audio : I2S init, FFT, clip WAV, payload spectral, coexistence PIR/timer, budget énergie audio) — *ajoutées 05/07*
  - 🔴 SOP-07 LoRa bloquée (module non commandé — panier Mouser ~279€)
- `03_P0_ENGINEERING/05_SIMULATION/wokwi/` — simulation CI Wokwi (validée)
- `03_P0_ENGINEERING/05_SIMULATION/test_harness/` — dataset caméra 51 images (deadline 15/07)
- `03_P0_ENGINEERING/07_PROCUREMENT_BOM/` — BOM v0.2c + v0.4
- `firmware/` — repo wildnexus-firmware (structure ESP-IDF créée, modules à implémenter)

### 2.4 Pilotage
- Plane : projet `03_WILDNEXUS`
- Kanban : `JCH_Inbox/kanban.html`

Ordre d'autorité en cas de contradiction :
- décision explicite JCH ;
- non-négociables du document fondateur ;
- ADRs acceptés ;
- documents de pilotage Plane ;
- SOPs et skills agents.

Toute contradiction détectée doit devenir une décision documentée, pas une discussion diffuse.

---

## 3. État Actuel (2026-07-05)

### 3.1 Milestones

| Milestone | Statut |
|-----------|--------|
| **M-01** — Architecture P0 gelée | ✅ Complété — 17 ADRs, MCU ESP32-S3, caméra OV5640, LoRa SX1262, micros stéréo |
| **M-02** — Prototype banc fonctionnel | 🔵 En cours — SOPs A→C ✓, D→E + SOPs 06-18 en attente |
| **M-03** — Prototype terrain | ⬜ Après M-02 |
| **M-04** — Production P0/P1 | ⬜ Après M-03 |

### 3.2 Work Packages

| WP | Contenu | Statut |
|----|---------|--------|
| WP01 — Architecture | ADRs, choix composants, scope lock | ✅ Gelé (17 ADRs) |
| WP02 — Procurement | Shortlist, BOM, commandes | 🔵 Actif — v0.4, panier Mouser restant ~279€ |
| WP03 — Firmware | SOPs, simulation, firmware P0 | 🔵 SOPs A→C faits, ADR-016 accepté (double cycle), repo à peupler |
| WP04 — Intégration HW | Caméra, LoRa, PIR, SD, I2S | ⬜ En attente de SOP-08 (caméra) + commande LoRa |
| WP05 — Tests terrain | PPK2, validation autonomie | 🔵 Banc en cours (PPK2 mesures acquises) |
| WP06 — Documentation | Docs, guides, dashboards | 🔵 |

### 3.3 Équipement clé

| Équipement | Statut | Réf. commande |
|-----------|--------|---------------|
| ESP32-S3-DevKitC-1 N16R8 | ✅ Reçu (×2) | Amazon MiMiU, 21,98€ |
| Nordic PPK2 | ✅ Reçu | ~100€ |
| Mouser #39492997 | ✅ Reçu | MEMS, IR, PIR, buck, BME688, SHT31, antennes — 128,20€ |
| ESP32-CAM OV2640 (avec caméra) | ✅ Reçu (×2) | Hailege Amazon.de, ~25€ |
| ESP32-CAM (cartes seules) | ✅ Reçu (×4) | 23 juin |
| OV5640 DVP M12 | ✅ Reçu (×5) | 1× Camemake + 4× AliExpress |
| USB-C TTL FT232RL | ✅ Reçu (×3) | AZDelivery, 9€ |
| Miuzei Starter Kit | ✅ Reçu | 235 composants, breadboard |
| MP1584 DC-DC ×5 | ✅ Reçu | Buck step-down 3A |
| SPH0645LM4H-B ×2 | ✅ Reçu | Dans Mouser #39492997 — micros MEMS stéréo (ADR-013) |
| Carte microSD 128 GB | ⏳ À ACHETER | Recommandation ADR-017 (~15€) |
| Panier Mouser restant (11 composants) | ⏳ À COMMANDER | ~279€ — bloque LoRa (SOP-07) + payload spectral (SOP-16) |

### 3.4 Budget

- Enveloppe : **1 000 €**
- Engagé (Mouser #39492997 + Amazon + AliExpress + PPK2) : **~610 €**
- Panier Mouser restant : **~279 €**
- Carte SD 128 GB : **~15 €** (ADR-017)
- Total projeté : **~904 €** (sous enveloppe)
- Réserve : **~96 €**
- BOM Excel : `03_P0_ENGINEERING/07_PROCUREMENT_BOM/WILDNEXUS_BOM_P0_v0.4.xlsx`

---

## 4. Actions Au Signal `go`

### 4.1 Contrôle Initial

[[Dobby]] commence par vérifier :
- que Plane répond ;
- que le projet `03_WILDNEXUS` est joignable ;
- que les ADRs 1-17 sont cohérents avec l'index (pas de nouveau ADR bloquant non référencé) ;
- que le BOM v0.4 reflète l'état réel des commandes ;
- que les SOPs non complétées (D→E, 06-18) ont leurs prérequis disponibles ;
- que `PROTOCOLES/progress.md` est à jour.

Si un élément technique bloque, [[Dobby]] corrige ce qui peut l'être et ne sollicite JCH que si une action externe est nécessaire.

### 4.2 Synchronisation Projet

[[Dobby]] synchronise :
- milestones `M-01` à `M-04` — état réel vs Plane ;
- SOPs D→E + 06-18 — prérequis, blocages, composants manquants ;
- BOM — écarts entre commandé et reçu ;
- ADRs — nouveaux, modifiés, ou contestés ;
- risques actifs — avec owner.

Le principe est l'idempotence : relancer la synchronisation ne doit pas créer de doublons.

### 4.3 Prochain Chantier Actif

Le chantier en cours est `WP02 — Procurement (panier Mouser restant)` + `WP03 — Firmware (SOPs D→E, 06-18, repo)` + `WP04 — Test harness caméra (deadline 15/07)`.

Les fronts lancés en priorité :
- **FW-01** — Créer repo `wildnexus-firmware/` (structure déjà présente, modules à implémenter) ;
- **FW-02** — Codec payload ADR-014 (caméra + spectral) — pas de hardware requis, testable immédiatement ;
- **SOP-08** — Test caméra OV5640 (hardware reçu ✅, pinout à mapper) ;
- **CAM-01** — ESP32-CAM OV2640 flash via FT232RL (hardware reçu ✅) ;
- **Test harness caméra** — dataset 51 images prêt, code d'inférence à produire (deadline 15/07) ;
- **SOP-13** — I2S MEMS init + capture stéréo (SPH0645LM4H-B reçu ✅, pinout I2S à mapper) — pas bloqué par Mouser ;
- **SOP-07** — Test LoRa (BLOQUÉ — module RAK3172 dans panier Mouser restant ~279€) ;
- **Commandes en attente** : panier Mouser restant (~279€) + carte SD 128 GB (~15€).

---

## 5. Orchestration Des Agents

### 5.1 Noyau Actif

[[Dobby]] active pour les tâches courantes :
- **[[Forge]]** — firmware, intégration, scripts, repo ESP-IDF
- **[[Castor]]** — DB, schémas, données techniques
- **[[Araignée]]** — IoT, protocoles, connectivité, banc de test
- **[[Nova]]** — imagerie, caméra, optique
- **[[Bruno]]** — budget, BOM, suivi financier

### 5.2 Agents À La Demande

[[Dobby]] active seulement si nécessaire :
- **[[Furet]]** — recherche composants, benchmarks
- **[[Sigma]]** — analyse données PPK2, modèles énergétiques
- **[[Atlas]]** — rédaction documents fondateurs
- **[[Milan]]** — veille concurrentielle
- **[[Hermine]]** — propriété intellectuelle
- **[[Musaraigne]]** — Edge AI, TinyML, modèles IA embarqués
- **[[Chouette]]** — hardware terrain, I2S, microphones, validation bioacoustique

Ces rôles ne doivent pas créer de complexité prématurée.

---

## 6. Automatisation Attendue

### 6.1 Automates De Routine

[[Dobby]] automatise par défaut :
- lecture de l'état Plane ;
- détection des tâches bloquées ;
- synthèse des décisions ouvertes ;
- suivi des milestones vs réalité ;
- repérage des documents modifiés ;
- régénération du BOM Excel depuis la shortlist Markdown ;
- mise à jour de `Start.md` (ce fichier) après chaque changement structurel.

### 6.2 Automates De Preuve

Chaque livrable doit laisser une [[Trace]] :
- document créé ou mis à jour ;
- lien vers fichier source ;
- item Plane associé ;
- statut du livrable ;
- décision ou prochaine action.

Un travail important sans [[Trace]] dans le repo est considéré incomplet.

### 6.3 Automates De Cohérence

[[Dobby]] surveille :
- écarts entre ADRs acceptés et BOM (composant manquant = ADR non couvert) ;
- contradictions de version entre Markdown et XLSX ;
- écarts entre `Start.md`, ADR Index et réalité du repo ;
- décisions prises mais non propagées ;
- risques identifiés sans owner.

Quand l'écart est mécanique, [[Dobby]] corrige. Quand l'écart implique une décision de fond, [[Dobby]] escalade.

### 6.4 Régénération Automatique

Ce fichier doit être mis à jour automatiquement après :
- acceptation d'un nouvel ADR ;
- complétion d'une SOP M-02 ;
- réception d'une commande BOM ;
- changement de milestone.

---

## 7. Page Web Et Terminal

### 7.1 Page Web

La page web de pilotage (kanban.html ou Plane) doit montrer :
- statut global ;
- milestone courante ;
- SOPs actives / bloquées ;
- commandes BOM en attente ;
- décisions en attente JCH ;
- risques critiques.

### 7.2 Terminal

Le terminal sert aux interactions courtes et immédiates :
- signaler un blocage ;
- demander un arbitrage ;
- confirmer une action importante ;
- restituer un résultat de test ou de mesure.

### 7.3 Règle D'Escalade

La page web est la vue continue.  
Le terminal est le canal d'action.

Une décision critique doit apparaître dans les deux.

---

## 8. Quand JCH Est Sollicité

[[Dobby]] sollicite JCH uniquement pour :
- modifier un non-négociable ;
- choisir entre deux options stratégiques réelles ;
- accepter un compromis coût / délai / performance ;
- valider un usage ou une orientation juridique ;
- autoriser une dépense hors enveloppe ou un engagement externe ;
- accepter un risque terrain, RGPD ou réputationnel.

[[Dobby]] ne sollicite pas JCH pour :
- renommer un fichier ;
- créer une annexe ;
- aligner un backlog ;
- produire une synthèse ;
- nettoyer une incohérence mécanique ;
- marquer un sujet comme P1 ou P2 quand le document fondateur le prévoit déjà.

---

## 9. Gaps critiques identifiés (2026-07-05)

| Gap | Impact | Action requise |
|-----|--------|----------------|
| Panier Mouser restant (~279€) non commandé | 🔴 Bloque LoRa (SOP-07) + payload spectral (SOP-16) | JC autorise la commande |
| Carte SD 128 GB non achetée | 🟡 Bloque SOP-06 (storage) + SOP-15 (clip WAV) | JC achète ou ajoute au panier Mouser |
| Modèle Edge AI non entraîné | 🔴 Bloque ADR-010 R4 | Dataset insuffisant (51 images), Musaraigne doit produire un modèle MobileNet-SSD |
| Repo firmware peuplé | 🟡 Structure créée, modules à implémenter | FW-01 à FW-05 — Forge commence par FW-02 (codec, pas de hardware) |
| ADR-018 (synchro temporelle) non rédigé | 🟡 Pas bloquant M-02 (banc), bloquant M-03 (terrain) | Forge rédige avant M-03 |
| Founding doc v0.2 non validé | 🟡 Sections §5/§9/§13/§15 en attente | JC valide ou demande v0.3 |
| Licence non rédigée | 🟡 Bloque M-04 | Renard + Hermine — trancher dual-license vs source-available |

---

*Mis à jour le 2026-07-05 par Dobby 🦉 — audit P0 ↔ InsectNet/NEXUS_ACOUSTIC, ADR-014/016/017 acceptés, SOPs 13-18 + FW-01 à FW-05 ajoutés.*
