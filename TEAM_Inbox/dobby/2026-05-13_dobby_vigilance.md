# PKA Vigilance Report

_Generated: 2026-05-13T18:34:54_
_Status: ORANGE_

| Severity | Check | Path | Detail | Mitigation |
|---|---|---|---|---|
| medium | network | `listening sockets` | LAN-listening services: EEventMan:2968 | disable unnecessary services; Epson Event Manager is already in P1 TODO |
| low | disk-space | `/System/Volumes/Data` | Data volume is 95% full | plan cleanup before it reaches 95% |
| low | cloud-sync | `/Users/jchavauxm5/Library/CloudStorage/Dropbox, /Users/jchavauxm5/Library/Dropbox` | cloud sync clients/directories detected | verify PKA_JCH, .env, DBs and logs are excluded or encrypted before sync |
