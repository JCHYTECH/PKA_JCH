# WildNexus - Plane Seed Backlog

Version: v0.1  
Date: 2026-05-17  
Purpose: Initial Plane backlog derived from the founding document.

## Milestone Items

- `M-01 Architecture gelee`
- `M-02 Prototype banc fonctionnel`
- `M-03 EVT terrain valide`
- `M-04 Open source publie`

## Epic Items

- `EPIC: WP01 - Conception & Architecture`
- `EPIC: WP02 - Hardware & Enclos`
- `EPIC: WP03 - Firmware ULP`
- `EPIC: WP04 - Edge AI`
- `EPIC: WP05 - Validation terrain EVT`
- `EPIC: WP06 - Open source & Communaute`

## Seed Tasks

### WP01

- `T01.1 Analyse comparative des specifications concurrentes`
- `T01.2 Analyse FTO sur composants critiques`
- `T01.3 Campagne mesures RF terrain`
- `T01.4 Benchmark module camera IMX462 vs IMX327`
- `T01.5 Selection MCU`
- `DECISION: Confirm P0 autonomy ladder`
- `DECISION: Confirm P0 product boundary`
- `LEGAL: Resolve open-source and usage-restriction strategy`
- `RISK: Define privacy baseline for human captures`

### WP02

- `T02.1 Schema electronique P0`
- `T02.2 Layout PCB prototype`
- `T02.3 CAO enclos IP67`
- `T02.4 Fabrication PCB prototype x5`
- `T02.5 Assemblage et tests banc`

### WP03

- `T03.1 Machine a etats sleep/wake/capture/transmit`
- `T03.2 Pilote camera + power gate`
- `T03.3 Gestion alimentation et undervoltage lockout`
- `T03.4 Interface BLE configuration terrain`
- `T03.5 Mecanisme OTA`

### WP04

- `T04.1 Dataset images IR nocturnes faune belge`
- `T04.2 Entrainement et quantisation modele binaire`
- `T04.3 Validation detection, faux positifs, latence`
- `T04.4 Integration firmware`

### WP05

- `T05.1 Selection et preparation site EVT`
- `T05.2 Deploiement 3 noeuds`
- `T05.3 Monitoring continu 30 jours`
- `T05.4 Collecte et analyse donnees`
- `T05.5 Rapport EVT et corrections`

### WP06

- `T06.1 Creation depot public`
- `T06.2 Documentation contribution`
- `T06.3 Canal communautaire`
- `T06.4 Strategie de visibilite EVT`

## Suggested Labels by Item

- `T01.2` -> `legal-ip`, `decision`, `release-blocker`, `P0`
- `T01.3` -> `rf`, `benchmark`, `validation`, `P0`
- `T01.4` -> `camera-imaging`, `benchmark`, `validation`, `P0`
- `T01.5` -> `firmware`, `decision`, `P0`
- `T02.x` -> `hardware-physical`, `P0`
- `T03.x` -> `firmware`, `P0`
- `T04.x` -> `edge-ai`, `P0`
- `T05.x` -> `field-test`, `validation`, `P0`
- `T06.x` -> `community`, `documentation`, `P0`

## Suggested Dependencies

- `T01.2` -> `M-01`
- `T01.3` -> `M-01`
- `T01.4` -> `M-01`
- `T01.5` depends on `T01.3` and `T01.4` inputs
- `M-01` unlocks `WP02`, `WP03`, `WP04`
- `M-02` depends on `T02.5`, `T03.5`, `T04.4`
- `WP05` starts after `M-02`
- `M-03` depends on `T05.5`
- `WP06` starts partially after `T01.2`, fully before `M-04`

## Suggested Acceptance Criteria for Milestones

- `M-01`: radio candidate chosen, camera module chosen, MCU chosen, legal/FTO review not blocking
- `M-02`: prototype boots, captures, transmits, and has a credible energy budget
- `M-03`: EVT completed with no critical failure and acceptable autonomy/image/filtering behavior
- `M-04`: public repo, contribution docs, and community entry channel available
