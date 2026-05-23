# WildNexus - Plane Operating Model

Version: v0.1  
Date: 2026-05-17  
Purpose: Define how WildNexus should be managed inside Plane during P0.

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

This split matters. The founding document should not become a live task tracker, and Plane should not become the place where mission-level decisions drift informally.

## 3. Recommended Plane Structure

### Project

Use one Plane project:

- `03_WILDNEXUS`

### Modules

Create one module per P0 work package:

- `WP01 - Conception & Architecture`
- `WP02 - Hardware & Enclos`
- `WP03 - Firmware ULP`
- `WP04 - Edge AI`
- `WP05 - Validation terrain EVT`
- `WP06 - Open source & Communaute`

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
- decisions requiring JCH confirmation
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

Minimum dependency chain:

- `T01.2 FTO` -> `M-01`
- `T01.3 RF terrain` -> `M-01`
- `T01.4 Benchmark camera` -> `M-01`
- `T01.6 Budget P0 ordre de grandeur` -> `M-01`
- `GOV-01 Mapping agents WildNexus vers specialistes PKA` -> `M-01`
- `SUPPLY-01 Registre composants critiques et fournisseurs alternatifs` -> `T02.1`
- `M-01` -> `WP02`, `WP03`, `WP04`
- `M-02` -> `WP05`
- `M-03` -> correction loop or P1 decision
- `M-04` -> P1 entry decision

## 9. Required Fields in Every Important Item

Each milestone-critical item should contain:

- owner
- module
- linked milestone
- acceptance criterion
- blocking dependency if one exists
- evidence path in the repo when completed

Examples of evidence paths:

- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/wildnexus-founding-document-v0.1.md`
- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WildNexus_MASTER_ARCHITECTURE.md`
- future lab reports, RF reports, or EVT reports

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

The founding document currently contains several management items that should become explicit Plane work items immediately:

- resolve the contradiction between OSI-style open source and field-of-use restrictions
- define the autonomy ladder: `30-day EVT`, `60-day battery-only`, `6-month field ambition`
- formalize privacy handling for human captures
- define the P0 product boundary more sharply
- turn threshold placeholders into concrete acceptance criteria after RF and camera benchmarks

## 12. Rule for JCH Decisions

Any issue that touches:

- mission
- non-negotiables
- IP strategy
- funding posture
- project stop/pivot conditions

must be labeled `decision`, assigned to JCH, and linked to the relevant section of the founding document.
