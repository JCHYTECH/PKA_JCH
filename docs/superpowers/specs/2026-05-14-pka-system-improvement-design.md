# PKA System Improvement Design

Date: 2026-05-14
Author: [[Dobby]]
Status: Draft approved in chat, pending final file review

## Goal

Adapt the useful parts of Everything [[Claude]] Code to PKA_JCH without importing its bulk or complexity.

The target is a focused intermediate evolution:

- add a dedicated PKA system improvement audit
- improve the local skills system with light metadata
- create a reusable skill for future "improve PKA" requests
- prepare, but do not yet implement, a future finer-grained learning layer

## Why This Approach

Three options were considered:

1. Pragmatic: too limited, does not address the real system gaps.
2. Intermediate: best tradeoff between [[daily]] usefulness and implementation risk.
3. Ambitious: too much infrastructure too early, with a real risk of slowing down [[Dobby]].

The selected approach is the intermediate one.

## Scope Now

The current implementation cycle will deliver four concrete changes.

### 1. Dedicated System Improvement Audit

Create a new script:

- `scripts/pka_system_improvement_audit.py`

Its purpose is to inspect PKA_JCH from an operational-efficiency perspective rather than a security-only perspective.

It should audit:

- instruction overlay consistency across `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `ADAPTER-PROMPT.md`
- roster and DB mirror consistency
- existence and health of key orchestration scripts
- current session-start and session-stop automation coverage
- current skills system quality signals
- actionable improvement opportunities

The output should classify findings by:

- status
- drift
- quick wins
- medium-term improvements

### 2. Actionable Report Format

The audit script should emit a structured report suitable for human review and later automation.

Preferred sections:

- global status
- findings
- quick wins
- recommended next steps
- future architecture notes

Markdown output is the default. JSON output may also be supported for future automation.

### 3. Lightweight Skills System Upgrade

Upgrade the `skills` table and its related scripts without introducing a full instinct architecture yet.

New metadata to add now:

- `source_kind` to distinguish manual, learned, or system-generated procedures
- `confidence` to capture trust level
- `scope` to distinguish `global`, `project`, or `tool`
- `project_key` for project targeting when applicable
- `updated_at` for freshness tracking

These additions must remain optional and backward-compatible with current rows and tooling.

### 4. New PKA Skill for System Improvement Requests

Create and register a reusable skill:

- `pka-system-improvement`

This skill should activate for requests about:

- improving PKA_JCH itself
- adapting useful patterns from external repos or frameworks
- improving [[Dobby]]'s operating efficiency
- reworking memory, hooks, overlays, or skills
- auditing the PKA system as a system

Its workflow should require:

1. inspect relevant local system state first
2. inspect the external inspiration source second
3. classify ideas into:
   - already present
   - worth adapting now
   - worth preparing later
   - reject
4. prioritize each recommendation by:
   - impact
   - effort
   - risk
   - dependencies
5. conclude with a staged evolution path:
   - now
   - next
   - later

## Explicitly Out of Scope for This Cycle

The following are intentionally deferred:

### 1. Full Instinct Layer

We are not implementing a separate instinct store yet.

We only prepare for it conceptually by adding better skill metadata now.

### 2. Full Overlay Generator

We are not yet replacing all tool overlays with a single generated pipeline.

We may prepare for that later once the current audit makes the drift points concrete.

### 3. Full Project Context Profiles

We are not yet introducing automatic per-project context profiles.

That remains a future improvement once routing and loading rules are clearer.

## Architecture Notes

### Audit Philosophy

`pka_system_improvement_audit.py` complements:

- `scripts/pka_security_audit.py`
- `scripts/pka_vigilance.py`

It should not duplicate them. Its role is to answer:

- where PKA is drifting
- where PKA is inefficient
- where small changes would meaningfully improve [[Dobby]]'s work

### Skills Evolution Philosophy

The current `skills` table already supports reusable procedures.

The improvement here is not to replace it, but to make it more queryable and more governable:

- where the skill came from
- how confident we are in it
- what scope it belongs to
- when it was last refreshed

This creates a stable bridge toward a possible later instinct layer.

### Skill Design Philosophy

The new `pka-system-improvement` skill must avoid framework cargo-culting.

Its purpose is not to copy external systems. Its purpose is to:

- extract leverage
- reject noise
- protect [[Dobby]]'s clarity
- improve the real operating system around JCH's work

## Error Handling

If the audit cannot inspect a file or table, it should report the gap instead of failing silently.

If optional files such as `AGENTS.md` or `GEMINI.md` are absent, the audit should mark them as missing or not yet installed rather than crash.

If the new metadata columns are not yet present during transition, scripts should continue to run and degrade gracefully where possible.

## Testing

This cycle should include lightweight verification at three levels:

1. schema verification after migration
2. CLI verification for `skill_search.py`, `skill_write.py`, and the new audit script
3. sanity verification that the new skill can be retrieved through the current PKA skills flow

## Implementation Order

1. create `pka_system_improvement_audit.py`
2. extend the `skills` schema
3. adapt `skill_search.py`
4. adapt `skill_write.py`
5. register the new `pka-system-improvement` skill
6. verify end-to-end behavior

## Success Criteria

This implementation is successful if:

- [[Dobby]] can run a dedicated PKA improvement audit
- the skills system stores richer but still lightweight metadata
- a future "improve our PKA system" request can load a dedicated skill
- the system becomes more governable without becoming heavier to operate

## Future Path After This Cycle

Once this cycle is stable, the next candidate evolutions are:

1. instinct-level learning layer
2. generated multi-tool overlays from one source
3. context profiles by project or task class
