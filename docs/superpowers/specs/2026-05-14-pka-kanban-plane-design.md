# PKA Kanban Transverse with Plane - Design

Date: 2026-05-14
Owner: Dobby
Status: Validated in chat, pending final user review of written spec

## Goal

Provide a stable, long-lived kanban operating model for all active PKA projects.
The system must support:

- one coherent workflow vocabulary across projects
- transverse visibility for Dobby and JCH
- compatibility across multiple models and tools
- project-specific process nuance without fragmenting board structure
- future automation and dashboard consolidation

## Decision Summary

PKA will use:

- Plane as the project and kanban engine
- a thin PKA integration layer as the transverse abstraction
- the local PKA dashboards as the consolidated pilotage cockpit

PKA will not build a full kanban product from scratch at this stage.

## Why Plane

Plane is the preferred foundation because the priority is long-term stability at the start of operations, with enough headroom for richer project management later.

Compared with lighter kanban-only tools, Plane gives more room for growth while still allowing a disciplined, standardized operating layer above it.

## Architecture

### Source of truth

Plane is the operational source of truth for:

- projects
- boards
- issues/cards
- statuses
- comments
- attachments

### PKA transverse layer

The PKA layer sits above Plane and defines:

- the canonical workflow states
- the canonical label vocabulary
- the standard card schema
- the mapping between cards and specialists/models
- the rules for dashboard aggregation

This layer must be tool-agnostic so Codex, Claude, Gemini, and future models all act on the same semantics.

### Dashboard role

The existing local dashboard stack remains the cockpit for transverse visibility.
It should consume normalized kanban data from the PKA layer rather than invent its own task system.

## Board Strategy

PKA will use one board per project.

All project boards share the same status structure.
Project-specific process steps must not create project-specific columns by default.

When a project needs more nuance, that nuance must be expressed through:

- card type
- labels
- custom fields
- checklists
- linked cards/subtasks where justified

This preserves transverse comparability and keeps automation simple.

## Canonical Workflow

Every project board uses the same seven statuses:

1. A qualifier
2. Pret
3. En cours
4. En attente
5. En validation
6. Termine
7. Archive

### Status semantics

#### A qualifier

Single entry point for all new incoming work:

- ideas
- requests
- files to process
- tasks lacking enough context

#### Pret

The item is clear enough to be prioritized and taken in charge.
This is the actionable backlog.

#### En cours

Work has actually started.

#### En attente

The item is blocked by:

- external dependency
- third-party response
- missing document
- user decision
- sequencing dependency

#### En validation

The work product exists and now waits for:

- review
- approval
- arbitration
- final sign-off

#### Termine

The deliverable is accepted or the decision is considered complete.

#### Archive

The item is closed and removed from the active operational flow while remaining available for traceability.

## Standard Card Model

### Mandatory fields

- Title
- Project
- Type
- Owner
- Priority
- Due date, when real
- Status
- Description

### Recommended PKA fields

- Lead specialist
- Model used
- Decision owner
- Blocking reason
- Expected outcome
- Source link

### Intended use of structure

- Status column = advancement state
- Labels = nature/classification of work
- Checklists = project-specific execution steps
- Fields = pilotage metadata
- Comments = working history and decisions

## Card Types

The initial canonical set is:

- task
- decision
- document
- bug
- idea
- follow-up
- deliverable

This set should stay short and stable unless a missing category repeatedly causes ambiguity.

## Label Governance

Labels are governed vocabulary, not free text.

### Initial families

Nature:

- decision
- execution
- research
- document
- follow-up
- bug
- idea

Domain:

- legal
- finance
- tech
- photo
- branding
- ops
- travel
- science

Special state/context:

- urgent
- bloque-externe
- en-attente-jch
- delegue
- a-planifier
- quick-win

Level:

- strategique
- tactique
- operationnel

### Naming rules

- lowercase only
- short words
- hyphen as separator
- no competing synonyms
- one label = one classification concept

### Anti-drift rules

1. A master label catalog must exist.
2. Only Dobby and Forge may create, rename, or remove transverse labels.
3. A new label is allowed only if the need cannot be represented by a status, type, field, or checklist.
4. Labels describing workflow state are forbidden because state belongs in statuses.
5. A periodic audit must detect:
   - unused labels
   - semantic duplicates
   - project-only labels with no transverse value
   - near-synonyms

### Synonym control

PKA must define and enforce a preferred vocabulary.
For example, if `bloque-externe` is canonical, alternatives like `blocked`, `waiting`, `pending`, or `attente` must be refused.

## Specialist and Model Mapping

Cards may be assigned operationally to a human role, Dobby, or a specialist.

The PKA layer should preserve at least:

- project owner
- current responsible actor
- lead specialist
- model/runtime used where relevant

This allows Dobby to orchestrate work consistently across different model runtimes.

## Operating Rules

### Intake

All new items enter through `A qualifier`.

### Qualification

An item moves to `Pret` only when it is clear enough to be executed without reconstructing missing context.

### Work in progress discipline

Only work that is actually started goes into `En cours`.

### Blocking discipline

Blocked work must move to `En attente` with an explicit blocking reason.

### Validation discipline

Completed-but-unapproved work must move to `En validation`, not `Termine`.

### Closure discipline

Only accepted work or finalized decisions go to `Termine`.

## Dashboard Integration Target

The dashboard should eventually offer:

- per-project board access
- transverse counts by status
- cards awaiting JCH validation
- blocked cards
- urgent cards
- workload by specialist
- workload by project

The dashboard should not become a second task database.
It should remain a read/write operational surface over normalized Plane-backed data.

## Automation Direction

Not part of this design's implementation scope, but the structure should support later:

- auto-tagging conventions
- automatic routing suggestions by specialist/domain
- summary generation by project
- stale-card detection
- validation queues for JCH
- cross-model action logging

## Non-Goals

This design does not attempt to define:

- full Plane deployment steps
- authentication and secret storage details
- synchronization implementation details
- historical migration of old task systems
- mobile workflow specifics

Those belong to the implementation plan.

## Risks

### Over-customization risk

If projects start adding custom columns, the transverse system collapses.
Mitigation: freeze the canonical workflow and force variation into metadata.

### Label sprawl risk

If labels become user-created free text, reporting becomes unreliable.
Mitigation: governed catalog, restricted creation, periodic audit.

### Process ambiguity risk

If teams use `En attente`, `En validation`, and `Termine` inconsistently, dashboards lie.
Mitigation: clear operational rules and examples during rollout.

### Integration drift risk

If dashboards or scripts invent local status semantics separate from Plane, PKA will fork conceptually.
Mitigation: the PKA layer owns canonical semantics and dashboards consume them.

## Rollout Principle

Start with:

- one canonical workflow
- one canonical card schema
- one canonical label catalog
- one board per project

Add complexity only after observing real friction, not speculative edge cases.

## Open Implementation Topics

These are intentionally deferred to planning:

- exact Plane workspace/project mapping
- exact custom field design
- API adapter shape
- dashboard UI changes
- import/bootstrap workflow for existing project items
- governance workflow for label changes

## Recommended Next Step

Write an implementation plan that covers:

1. Plane information model setup
2. PKA canonical schema and vocabulary files
3. adapter/API layer
4. dashboard integration
5. governance and operating SOP
6. phased rollout across active projects
