# Model Handoff — PKA_JCH

Date: 2026-05-28
Purpose: compact handoff for continuing the current thread with another model while preserving safety and the current system state.

## Current State

- PKA phase 1 is closed and documented.
- MacBook minimal tech phase has been audited.
- Backup workflow for `TEAM/team.db` is hardened and validated.
- `Tailscale` CLI is corrected and aligned with `Tailscale.app`.
- `ADAPTER-PROMPT.md` and `MEMORY.md` were updated with [[Dobby]] operating rules and memory protocol.
- `team.db` [[inbox]] migration has been applied locally.
- `inbox` triage has been started and partially completed.

## Key Decisions Already Applied

- Phase 1 must stay before infrastructure.
- No Hermes / n8n / Qdrant / Redis / PostgreSQL rollout yet.
- Obsidian is not part of the current runtime work.
- `TEAM/team.db` backups must stay `0600`.
- Telegram logs must not expose tokens.
- `com.jch.pka.backup` LaunchAgent was retired and archived.
- `email_digest.py` remains suspended.
- `outlook_gatekeeper.py` remains suspended.
- Plane proxy is restricted to `127.0.0.1`.
- Tailscale is operational with CLI version `1.98.2`.

## What Has Been Completed

### Phase 1 closure

- Created `AI_System_Blueprint.md`
- Created `AI_Runtime_Audit.md`
- Created `AI_Data_Governance.md`
- Created `Runtime_Service_Register.md`
- Created `Phase_1_Closure_Report.md`

### Minimal MacBook tech phase

- Created `Phase_Tech_Minimal_MacBook_Audit.md`
- Created `Phase_Tech_Minimal_Backup_Audit.md`
- Created `TEAM/RESTORE_TEAM_DB.md`
- Created `RUNBOOK_PKA_MACBOOK.md`

### Runtime hardening

- `scripts/backup_team_db.py` now:
  - checks source existence
  - creates consistent SQLite snapshots
  - applies `chmod 600`
  - runs `PRAGMA integrity_check`
  - deletes a failed backup candidate
- `scripts/telegram-bot/bot.py` now:
  - redacts Telegram token URLs in logs
  - suppresses noisy client logs
  - logs to file only
- `com.jch.pka.backup` LaunchAgent was booted out, disabled, and archived to:
  - `_local/disabled_launchagents/com.jch.pka.backup.plist.disabled`

### [[Dobby]] protocol / memory

- `ADAPTER-PROMPT.md` updated with:
  - simplification
  - team attribution
  - maximum delegation
  - proactive suggestions only when useful
  - dead-letter handling
  - memory write protocol
- `MEMORY.md` updated with:
  - `Échecs récents`
  - `Décisions structurelles`
  - proactive suggestion block format

### Inbox migration

- Created `scripts/migrate_inbox_deliverables.py`
- Created `Inbox_Deliverables_PreMigration_Audit.md`
- Created `Inbox_Deliverables_PostMigration_Report.md`
- Applied migration to `TEAM/team.db`
- Added columns:
  - `deliverable_path`
  - `delivered_at`
  - `validated_at`
  - `validated_by`
  - `rejection_reason`
- Expanded statuses:
  - `pending`
  - `in_progress`
  - `done`
  - `delivered`
  - `validated`
  - `rejected`
  - `cancelled`

### Inbox triage already applied

- `232` -> `validated`
- `233` -> `delivered`
- `234` -> `delivered`

## Current Inbox Counts

`TEAM/team.db` [[inbox]] status counts:

- `cancelled`: 224
- `done`: 2
- `delivered`: 2
- `validated`: 1
- `pending`: 6

## The 6 Remaining Pending Items

- `20` [[Vasco]]
- `83` [[Vasco]]
- `128` [[Renard]]
- `147` [[Vasco]]
- `214` [[Vasco]]
- `228` [[Renard]]

These are old [[email]]-derived entries without file paths. They still need a decision:

- keep pending
- cancel
- or reconstruct the missing deliverable if it exists elsewhere

## Commits Already Created

- `98194d3` `Integrate Dobby operating protocol`
- `4585503` `Add inbox deliverable migration`
- `b36992b` `Record inbox WildNexus triage`

## Safety / Constraints for the Next Model

- Do not touch unrelated changes in the worktree.
- Do not commit `.obsidian/`.
- Do not include SQLite backups in Git.
- Do not modify `TEAM/team.db` unless the action is deliberate and validated.
- Do not relaunch suspended digest/gatekeeper services without explicit approval.
- Use `python3 scripts/pka_security_audit.py` after any material change.
- Prefer reading existing project files before editing anything.

## Important Files

- [ADAPTER-PROMPT.md](/Users/jchavauxm5/PKA_JCH/ADAPTER-PROMPT.md)
- [MEMORY.md](/Users/jchavauxm5/PKA_JCH/MEMORY.md)
- [Phase_1_Closure_Report.md](/Users/jchavauxm5/PKA_JCH/[[Phase_1_Closure_Report]].md)
- [RUNBOOK_PKA_MACBOOK.md](/Users/jchavauxm5/PKA_JCH/[[RUNBOOK_PKA_MACBOOK]].md)
- [TEAM/[[RESTORE_TEAM_DB]].md](/Users/jchavauxm5/PKA_JCH/TEAM/[[RESTORE_TEAM_DB]].md)
- [Inbox_Deliverables_PreMigration_Audit.md](/Users/jchavauxm5/PKA_JCH/[[Inbox_Deliverables_PreMigration_Audit]].md)
- [Inbox_Deliverables_PostMigration_Report.md](/Users/jchavauxm5/PKA_JCH/[[Inbox_Deliverables_PostMigration_Report]].md)
- [scripts/migrate_inbox_deliverables.py](/Users/jchavauxm5/PKA_JCH/scripts/migrate_inbox_deliverables.py)
- [scripts/backup_team_db.py](/Users/jchavauxm5/PKA_JCH/scripts/backup_team_db.py)

## Good Next Step

Triage the 6 remaining `pending` [[inbox]] rows, one by one, before any dashboard work.
