---
name: gmail_imap_fetch
description: Récupérer les mails Gmail envoyés à l'alias jc.havaux+dobby@gmail.com via IMAP et les déposer dans 00_INBOX/email_imports/. Déclencher sur "récupère mes mails", "fetch gmail", "nouveaux mails", "gatekeeper gmail".
---

# Skill — gmail_imap_fetch

Lecture Gmail via IMAP + mot de passe d'application. L'adresse de destination
(`jc.havaux+dobby@gmail.com`) EST le déclencheur — aucune dépendance aux
filtres/étiquettes Gmail.

## Déclencheur
- « récupère mes mails », « fetch gmail », « nouveaux mails inbox »
- Après une alerte `watch-inbox` signalant un courrier à traiter
- Routage : les mails importés tombent dans `JCH_Inbox/00_INBOX/email_imports/`,
  puis sont traités par le skill `inbox-analysis`.

## Procédure
1. `python3 scripts/gmail_imap_fetch.py --list`   — voir les mails correspondants
2. `python3 scripts/gmail_imap_fetch.py --fetch`  — télécharger les NOUVEAUX mails
3. `python3 scripts/gmail_imap_fetch.py --fetch --force` — re-télécharger les déjà vus

## Configuration
- Config : `JCH_Inbox/99_SYSTEM/security/gmail_imap.json` (champ `search`)
- Secret : `~/.config/pka-jch/gmail_app_password.txt` (mot de passe d'application)
- État   : `_local/gmail_imap_fetch_state.json` (UIDs déjà importés, dédup)
- Setup  : `docs/system/SETUP_GMAIL_DOBBY.md`

## Voir aussi
- [[inbox-analysis]] — traitement des fichiers déposés dans l'INBOX
