# SETUP Gmail Dobby — Canal d'entrée mail (IMAP, sans OAuth)

> SOP opérationnelle. Remplace l'ancien flux `gmail_gatekeeper.py` (OAuth) qui
> était bloqué par un projet Google Cloud orphelin (`extended-argon-496307-j3`)
> et un écran de consentement en mode « Testing ».
>
> Date de mise en place : 2026-10-20.

## Principe

Dobby n'a pas de boîte mail. Le flux est : **mail envoyé à l'alias
`jc.havaux+dobby@gmail.com` → script IMAP (recherche Gmail) →
`JCH_Inbox/00_INBOX/email_imports/` → analyse**.

- Le **déclencheur est l'adresse de destination** (`+dobby`), pas un filtre ni
  une étiquette Gmail. Aucune dépendance aux filtres/étiquettes : robuste.
- La boîte de réception n'est scannée que par une recherche ciblée
  (`to:jc.havaux+dobby@gmail.com`), jamais en entier.
- Aucun OAuth, aucun Google Cloud, aucun token qui expire : **IMAP + mot de
  passe d'application**.

## Fichiers

| Élément | Chemin | Rôle |
|---------|--------|------|
| Script | `scripts/gmail_imap_fetch.py` | Recherche IMAP + import local + extraction PJ |
| Config | `JCH_Inbox/99_SYSTEM/security/gmail_imap.json` | hôte, compte, recherche (`search`) |
| Secret (jamais commité) | `~/.config/pka-jch/gmail_app_password.txt` | mot de passe d'application Gmail |
| État | `_local/gmail_imap_fetch_state.json` | UIDs déjà importés (dédup) |
| Sortie | `JCH_Inbox/00_INBOX/email_imports/` | `.md` + `.eml` + pièces jointes |

## Prérequis (une seule fois)

1. Validation en 2 étapes activée sur `jc.havaux@gmail.com`.
2. Mot de passe d'application « Mail » créé :
   `https://myaccount.google.com/apppasswords`
3. Code de 16 caractères enregistré **hors git** :
   ```bash
   echo "XXXX XXXX XXXX XXXX" > ~/.config/pka-jch/gmail_app_password.txt
   ```

## Utilisation

Envoyer/forwarder un mail vers `jc.havaux+dobby@gmail.com`, puis :

```bash
python3 scripts/gmail_imap_fetch.py --list             # liste les mails correspondants
python3 scripts/gmail_imap_fetch.py --fetch            # importe les NOUVEAUX mails + PJ
python3 scripts/gmail_imap_fetch.py --fetch --force    # re-importe aussi les déjà vus
```

> L'adresse `jc.havaux+dobby@gmail.com` est un alias Gmail natif (aucun compte à
> créer) : tout ce qui y est envoyé arrive dans `jc.havaux@gmail.com`, et la
> recherche `to:jc.havaux+dobby@gmail.com` le retrouve à coup sûr.

## Routage VETALYX (Outlook → Gmail)

Les mails des partenaires chinois arrivent dans Outlook (`jc.havaux@jchytech.be`).
Pour les capter automatiquement :

**Outlook Web → Règles** : condition « L'adresse de l'expéditeur inclut » =
`zdbiogene.com` → *Rediriger vers* `jc.havaux+dobby@gmail.com`.
(⚠️ Le sélecteur « De » refuse un domaine seul : utiliser la condition
« adresse de l'expéditeur inclut » pour matcher tout `@zdbiogene.com`.)

Aucun filtre Gmail nécessaire : la redirection arrive sur l'alias `+dobby`, qui
est le déclencheur de la recherche.

## Notes / limites connues

- Les pièces jointes sont extraites et sauvegardées (`*_PJ_*.docx`, etc.).
- La déduplication se fait par UID Gmail (fichier d'état) ; `--force` la contourne.
- Le mot de passe d'application est relu à chaque exécution depuis
  `~/.config/pka-jch/gmail_app_password.txt`.

## Suite possible (non fait)

- Job launchd pour exécuter `--fetch` en boucle (scan auto).
- Généraliser la recherche à d'autres alias (`+vetalyx`, etc.).
