# Archive — Flux mail OAuth morts (2026-11-23)

Nettoyage Dobby — décision JC « nettoie » (session 2026-11-23).

Ces scripts OAuth étaient tous morts pour la même cause (tokens expirés/révoqués
en boucle), et remplacés par la méthode **IMAP + mot de passe d'application**
(sans OAuth) :

- `scripts/gmail_imap_fetch.py` — pull manuel, déclencheur alias `jc.havaux+dobby@gmail.com`
- `scripts/gmail_imap_digest.py` — digest des non-lus (launch agent `com.dobby.gmail-imap-digest`, 9h/14h/20h)

## Contenu archivé (chemin d'origine → ici)

| Fichier | Rôle mort |
|---------|-----------|
| `scripts/email_digest.py` | Digest Gmail **OAuth** (token Google révoqué) |
| `scripts/google_auth.py` | Génère `token.json` pour email_digest (OAuth) |
| `scripts/outlook_gatekeeper.py` | Lecture M365/Graph **OAuth MSAL** (token expiré en boucle) |
| `scripts/outlook_auth.py` | Token MSAL une fois (scope `Mail.ReadWrite` obsolète) |
| `scripts/gmail_gatekeeper.py` | Whitelist Gmail **OAuth** (projet Google Cloud orphelin) |
| `scripts/install_gmail_gatekeeper_launchd.sh` | Installer du gatekeeper mort |
| `security/gmail_gatekeeper.json` | Config whitelist (obsolète) |
| `security/gmail_gatekeeper.md` | Doc du flux OAuth (obsolète) |
| `docs-system/outlook_config.json` + `.bak-*` | Config OAuth MSAL (tenant/client ID → déjà dans `06_ADMIN/mail-orban45-*.md`) |
| `LaunchAgents/*.plist.disabled` | 3 launch agents déjà `.disabled` (email-digest, gmail-gatekeeper, outlook-gatekeeper) |
| `scripts/install_email_pipeline.sh` | Installer du pipeline OAuth complet (outlook_config + email-digest + outlook-gatekeeper) |
| `scripts-launchd/*.plist` | Sources plist des 3 agents morts |
| `scripts/outlook_config.template.json` | Template config OAuth MSAL (obsolète) |
| `scripts/outlook_imap.py` + `docs-system/outlook_imap.json` | Client IMAP Outlook (pas OAuth, mais mort : M365 basic auth désactivé) |

## Restauration

Remettre les fichiers à leur chemin d'origine (listés dans le tableau). Aucun
script vivant ne les référence (vérifié le 2026-11-23).

## Reste en production (IMAP, non touché)

- `scripts/gmail_imap_fetch.py` + `skills/gmail_imap_fetch/SKILL.md`
- `scripts/gmail_imap_digest.py` + `_local/launchd-plists/com.dobby.gmail-imap-digest.plist`
- Secret partagé : `~/.config/pka-jch/gmail_app_password.txt`
