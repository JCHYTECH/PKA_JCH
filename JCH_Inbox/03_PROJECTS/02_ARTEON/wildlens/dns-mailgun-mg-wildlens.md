# DNS Mailgun — `mg.wildlens.arteon.be` (enregistrements à poser chez Gandi)

> Date : 2026-11-17 · Source : dashboard Mailgun (Setup → Add domain → Set up manually)
> Zone cible : `arteon.be` (Gandi, géré par Orban) · TTL : 3600

## Enregistrements (copiés depuis Mailgun)

| Type | Host / Name | Value | Priorité |
|------|-------------|-------|----------|
| TXT (SPF) | `mg.wildlens.arteon.be` | `v=spf1 include:mailgun.org ~all` | — |
| TXT (DKIM) | `k1._domainkey.mg.wildlens.arteon.be` | `k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDYBv92Lz4Nk7yS9im9CPS8yamU+tc83pNJqljrxSLEFb3i5smyPPz/7PsZGIwig+r7FUu6r1gd/BGrHUl2mzp9S3x1btP4sFoJnxO9z2t9IzydBGv9V++VHgPE5lfiEGmfcZMwLWUV9Uvdw/nthzyLjW4DYkj3DqG57rplwfL0RQIDAQAB` | — |
| MX | `mg.wildlens.arteon.be` | `mxa.mailgun.org` | 10 |
| MX | `mg.wildlens.arteon.be` | `mxb.mailgun.org` | 10 |
| CNAME (tracking) | `email.mg.wildlens.arteon.be` | `mailgun.org` | — |
| TXT (DMARC, recommandé) | `_dmarc.mg.wildlens.arteon.be` | `v=DMARC1; p=none;` | — |

> Note : le DKIM est une clé RSA 1024 bits (générée par Mailgun). Acceptée partout, mais à passer en 2048 bits lors d'une future rotation.

## Message prêt à envoyer à Orban

> Voir `message-orban-dns-mailgun.md` dans ce dossier.
