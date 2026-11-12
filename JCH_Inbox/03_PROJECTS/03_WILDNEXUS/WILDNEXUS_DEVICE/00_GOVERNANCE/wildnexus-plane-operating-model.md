# WildNexus - Plane Operating Model

Version: v0.2
Date: 2026-11-05
Purpose: Define how WildNexus should be managed inside Plane during P0.

> **Modèle de reprise — aucune synchronisation Plane n'a été exécutée lors de cette révision.**
> Le projet a été repris le 2026-11-11 (P0 engineering). `Start.md`, le scope lock, les ADR et `progress.md` décrivent l'état documentaire ; la présence d'un intitulé ci-dessous ne prouve ni sa création dans Plane ni son achèvement. Les identifiants de tâches et échéances historiques sont des exemples, pas un planning actif. À la reprise, rapprocher les éléments existants sans doublon, sans réutiliser les anciennes dates et sans lancer le seed destructif.

## 1. Why Plane for WildNexus

Plane is the best fit for WildNexus in the current PKA setup because:

- the repo already contains a Plane adapter and project mapping
- Plane supports `List`, `Board`, `Spreadsheet`, and `Gantt` views
- WildNexus needs both execution tracking and milestone visibility
- the project already has a phase and work-package structure that maps cleanly to Plane

WildNexus should therefore use Plane as the execution layer, while the founding document remains the strategic and constitutional layer.

## 2. Management Principle

The founding document is the source of truth for:

- mission
- non-negotiables
- P0/P1/P2 scope
- success criteria
- exit and pivot rules

Plane is the source of truth for:

- active work items
- owners
- states
- dates
- dependencies
- blockers
- delivery evidence

This split matters. The founding document should not become a live task tracker, and Plane should not become the place where mission-level [[decisions]] drift informally.

## 3. Recommended Plane Structure

### Project

Use one Plane project:

- `03_WILDNEXUS`

### Modules

Create one module per P0 work package (taxonomie canonique — Bible V0, 2026-10-29) :

- `WP01 - Architecture & ADRs`
- `WP02 - Hardware noeud`
- `WP03 - Energie & mesure`
- `WP04 - Firmware`
- `WP05 - Connectivite (LoRa)`
- `WP06 - Boitier & terrain`

> ⚠️ **Taxonomie canonique** : cette liste remplace celle de la v0.1. Source de vérité :
> `01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md` §7. L'« Edge AI » (filtre
> binaire) est rattaché à WP02 + ADR-010 ; « Documentation » et « Open source » se suivent
> via le jalon M-04 et les modules transverses, pas comme WP dédiés.

Create two transverse modules:

- `Governance & Decisions`
- `Risks & Compliance`

### Milestones

Represent the major P0 gates as milestones:

- `M-01 Architecture gelee`
- `M-02 Prototype banc fonctionnel`
- `M-03 EVT terrain valide`
- `M-04 Open source publie`

### Cycles

Use cycles as short execution windows, not as the strategic phases themselves.

Recommended initial cycles:

- `Cycle 01 - Architecture Freeze Prep`
- `Cycle 02 - Prototype Build`
- `Cycle 03 - EVT Readiness`
- `Cycle 04 - Publication & Community`

## 4. Work Item Taxonomy

Use a small, disciplined set of work item types.

### Epic level

Use epics for:

- each work package
- each milestone preparation stream if it spans several modules

Examples:

- `EPIC: WP01 - Conception & Architecture`
- `EPIC: WP02 - Hardware & Enclos`
- `EPIC: M-01 readiness`

### Task level

Use tasks for:

- numbered tasks from the founding document
- deliverable preparation
- validation steps
- concrete investigations

Examples:

- `T01.1 Analyse comparative concurrents`
- `T01.3 Campagne RF terrain`
- `T04.2 Entrainement et quantisation modele binaire`

### Issue level for governance

Use normal issues or tasks for:

- risk actions
- legal reviews
- [[decisions]] requiring JCH confirmation
- publication blockers

Examples:

- `DECISION: Confirm P0 autonomy ladder`
- `LEGAL: Resolve open-source vs usage-restriction strategy`
- `RISK: Human image privacy handling baseline`

## 5. Suggested Labels

Keep labels sparse and structural.

### Domain labels

- `firmware`
- `camera-imaging`
- `hardware-physical`
- `rf`
- `edge-ai`
- `scientific-data`
- `industrialisation`
- `legal-ip`
- `community`

### Nature labels

- `decision`
- `risk`
- `validation`
- `documentation`
- `benchmark`
- `field-test`
- `release-blocker`

### Scope labels

- `P0`
- `P1`
- `P2`

## 6. Suggested States

Use a simple workflow:

- `Backlog`
- `Ready`
- `In Progress`
- `Blocked`
- `In Review`
- `Done`

Use `Blocked` aggressively. If a task depends on a measurement, legal answer, or hardware receipt, it should be visible as blocked rather than silently slipping.

## 7. Gantt Usage

Use Gantt for:

- milestone visibility
- cross-work-package dependencies
- long-running benchmark and validation items
- EVT preparation and execution windows

Do not use Gantt for every low-level task. It becomes unreadable too quickly.

Recommended Gantt content:

- the six WP epics
- the four milestones
- blocking tasks such as `T01.2`, `T01.3`, `T01.4`
- EVT window
- open-source publication window

## 8. Dependency Rules

Every blocking task should explicitly link upstream and downstream items.

Dependencies for the restart, replacing the old task-number chain:

- `R0 — signal JCH + état réel` -> rapprochement stock/factures/Plane sans doublon
- `R0` -> révision schéma alimentation et retrait de la suspension SOP-10
- `R0` -> références micros/PIR et datasheets -> `SOP-13`, puis tests audio et pipelines
- `M-02 — preuves banc complètes` -> `M-03 — EVT terrain`
- `M-02` -> gateway P0 réelle, réception et journal des paquets caméra/spectral
- `M-03` -> correction loop or P1 decision
- Revue MIT/`ETHICS.md`/notices tierces avant `M-04 — publication`

The historical FTO, RF, camera and budget tasks remain candidate backlog items; their presence here is not proof of completion in Plane.

## 9. Required Fields in Every Important Item

Each milestone-critical item should contain:

- owner
- module
- linked milestone
- acceptance criterion
- blocking dependency if one exists
- evidence path in the repo when completed

Examples of evidence paths relative to the repo:

- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/00_GOVERNANCE/Start.md`
- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md`
- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/03_P0_ENGINEERING/PROTOCOLES/progress.md`
- future lab reports, RF reports, or EVT reports, explicitly identified as host or target evidence

## 10. Views to Create in Plane

### Executive Roadmap

Type: `Gantt`

Filter:

- milestone items
- epic items
- labels `P0`

Use for:

- JCH review
- go/no-go checkpoints

### P0 Execution Board

Type: `Board`

Group by:

- state

Filter:

- labels `P0`
- exclude `P1` and `P2`

### Validation Register

Type: `List`

Filter:

- label `validation`

Use for:

- threshold tracking
- EVT readiness
- success criteria follow-up

### Risks & Decisions

Type: `Spreadsheet`

Filter:

- labels `risk` or `decision`

Use for:

- open risks
- JCH confirmations
- legal and product arbitrations

### Community & Publication

Type: `List`

Filter:

- label `community`
- label `documentation`

Use for:

- repo publication
- contribution docs
- communication preparation

## 11. Immediate Management Corrections to Apply

For the restart, reconcile these items with existing Plane entries rather than creating them immediately:

- record the JCH decision: MIT firmware plus `ETHICS.md` and a usage policy; this is not a dual-license and does not remove MIT permissions
- review the scope of the ethics policy, third-party notices and contracts before publication
- treat `30-day EVT`, `60-day battery-only` and `6-month field ambition` as separate targets requiring their own evidence; none is guaranteed
- keep human images out of alerts, verify human/animal confusion in the benchmark, and complete the GDPR/terrain procedures before M-03
- use the P0 scope lock v0.5 and its requirement-to-evidence matrix as the product boundary
- replace unmeasured RF, camera, AI and power thresholds with benchmark results before treating them as acceptance criteria

## 12. Rule for JCH Decisions

Any issue that touches:

- mission
- non-negotiables
- IP strategy
- funding posture
- project stop/pivot conditions

must be labeled `decision`, assigned to JCH, and linked to the relevant section of the founding document.
