# Dobby Live — Prototype Realtime 2

## Statut

Prototype local installe dans le dashboard PKA.

## Fichiers modifies

- `scripts/dashboard_server.py`
- `JCH_Inbox/01_DASHBOARDS/dobby-live.html`
- `JCH_Inbox/01_DASHBOARDS/hub.html`
- `JCH_Inbox/01_DASHBOARDS/INDEX.md`

## Capacites MVP

- Session WebRTC vers `gpt-realtime-2` via `/api/realtime/call`
- Cle OpenAI gardee cote serveur
- Selection de voix : `marin`, `cedar`, `coral`, `verse`, `alloy`, `ash`, `ballad`, `echo`, `sage`, `shimmer`
- Selection du modele cible : Auto, Claude, Gemini, Codex, OpenAI
- Tools PKA locaux :
  - `pka_status`
  - `read_inbox`
  - `search_wiki`
  - `create_daily_note`
  - `save_team_inbox`
  - `prepare_model_brief`

## Validation effectuee

- Compilation Python : OK
- `/api/live/config` : OK
- `read_inbox` : OK
- `search_wiki` : OK
- `prepare_model_brief` : OK, fichier de test retire

## Non valide dans cette passe

- Session audio complete avec micro et OpenAI non lancee, pour eviter consommation de credits pendant le prototype.
- Verification mobile reelle non faite.

## Prochaine etape

Tester une session audio courte depuis `http://127.0.0.1:8788/dobby-live.html`, puis ajouter une couche d'authentification avant usage mobile distant.
