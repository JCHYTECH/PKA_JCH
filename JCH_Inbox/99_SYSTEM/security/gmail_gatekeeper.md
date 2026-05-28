# Gmail Gatekeeper

Flux Gmail dédié à [[Dobby]].

## Règles

- Scan en en-têtes seulement.
- Seuls les expéditeurs exacts de `gmail_gatekeeper.json` sont acceptés.
- Tous les autres messages sont supprimés sans lecture du corps.
- Aucun contenu ni pièce jointe n'est importé sans instruction explicite de JCH.

## Commandes

```bash
python3 scripts/gmail_gatekeeper.py scan
python3 scripts/gmail_gatekeeper.py list
python3 scripts/gmail_gatekeeper.py process --id <gmail_message_id>
```

## Sorties

- État local : `tmp/gmail_gatekeeper_state.json`
- Imports approuvés : `JCH_Inbox/00_INBOX/email_imports/`
