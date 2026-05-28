# PKA_JCH Security Incident Log

## 2026-05-13

- Baseline P0 hardening started.
- Sensitive 
- Roster drift corrected in `AGENTS.md`, `GEMINI.md`, `ADAPTER-PROMPT.md`, and `TEAM/ROSTER.md`.
- `.gitignore` security exclusions created.
- Additional sensitive files hardened: [[Argus]] [[SQLite]] DBs, 
- `TEAM/team.db` synchronized from the newer root compatibility mirror after preserving the previous `TEAM/team.db` as `TEAM/backups/team_2026-05-13_pre-sync.db`.
- Operational references updated to use `TEAM/team.db`.
- `scripts/pka_security_audit.py --write-report` status: GREEN.
- First hardware/local audit completed. Status: ORANGE due to no Time Machine destination, ExFAT external volume, LAN-listening services, cloud sync presence, and high Data volume usage.
- Epson Event Manager deactivation added to TODO as P1 if scanner/printer button workflows are not needed.
- `scripts/pka_vigilance.py` created and run. Initial status: ORANGE due to Epson Event Manager LAN listener, high Data volume usage, and Dropbox presence.
