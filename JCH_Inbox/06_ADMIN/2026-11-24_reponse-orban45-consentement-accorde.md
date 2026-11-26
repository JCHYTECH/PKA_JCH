# Réponse Orban45 — Consentement accordé (2026-11-24)

> Reçu par JC le 24/11. Orban45 (Philippe Prince) a accordé le consentement Graph
> **lecture seule** + mis en place le transfert arteon.be → Gmail.

## Texte reçu (extrait)

> Onjour Jean-Claude, C'est en place de mon côté. Pour que tout soit propre et correctement configuré (comptes professionnels, lecture seule, limité à votre seule boîte), j'ai préparé une application dédiée et je vous ai accordé l'accès. Il vous reste deux petites choses :
> 1. Dans la configuration de votre assistant « Dobby » sur le Mac, remplacez l'identifiant d'application (client_id) par le nouveau : `0b8dde80-9cab-42d1-a49f-2d7d9a40b971`
> 2. Relancez l'assistant et connectez-vous une fois avec votre compte arteon.be quand il vous le demande (l'accès fonctionne sous votre identité).
> Les autorisations se limitent à la lecture : mails, agenda et contacts. Aucun envoi, aucune écriture.
> Dès que vous me confirmez que ça fonctionne chez vous, je supprime les anciennes inscriptions en double.
> Je mets aussi en place le transfert de vos mails arteon.be vers votre Gmail.

## Actions Dobby (24/11)

- client_id remplacé `31f92869-5887-47c2-b35a-b3e2aa52a324` → `0b8dde80-9cab-42d1-a49f-2d7d9a40b971` dans :
  - `JCH_Inbox/06_ADMIN/reponse-orban45-2026-11-23.md`
  - `JCH_Inbox/06_ADMIN/mail-orban45-consentement-graph-forward-2026-11-21.md`
  - `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/thread-ai-it-tools.md`
- Nouveau client_id enregistré dans `JCH_PRIVATE/credentials-central.md` (section « Microsoft 365 / Graph »).

## Reste à faire

- [ ] **JC** : relancer l'assistant + connexion OAuth une fois avec arteon.be (device code). Nécessite de réactiver le script Graph archivé `_local/archives/mail-oauth-dead-2026-11-23/scripts/outlook_auth.py` avec le nouveau client_id + scopes lecture seule — chantier Forge.
- [ ] **JC** : vérifier que les mails arteon.be arrivent bien dans Gmail (transfert mis en place côté Orban).
- [ ] **Dobby** : confirmer à Orban que ça fonctionne → il supprime les anciennes inscriptions en double.

## Brouillon — confirmation à envoyer à Orban (après test OK)

**Objet :** Re: [Microsoft 365 — arteon.be] Consentement administrateur + autorisation de transfert

Bonjour,

Merci, tout est en place de mon côté : le nouveau client_id `0b8dde80-9cab-42d1-a49f-2d7d9a40b971` est configuré et la connexion fonctionne sous mon identité arteon.be, en lecture seule (mails, agenda, contacts), sans envoi ni écriture.

Vous pouvez donc supprimer les anciennes inscriptions en double.

Le transfert des mails arteon.be vers Gmail fonctionne également [à confirmer]. Merci beaucoup pour votre réactivité.

Bien cordialement,
Jean-Claude Havaux

## Clôture (24/11, 11:28) — réponse de Roman Dillen

> Jean-Claude, C'est finalisé de mon côté :
> - Votre assistant « Dobby » est bien relié à la nouvelle application (lecture seule : mails, agenda, contacts), et vous avez confirmé que la lecture fonctionne.
> - J'ai supprimé les deux anciennes inscriptions en double ; il ne reste que l'application propre.
> - Le transfert de vos mails arteon.be vers votre Gmail est déjà actif, avec conservation d'une copie dans la boîte arteon.be. Comptez un petit délai de propagation ; un mail de test depuis une adresse externe vous le confirmera.

**État : CLOS** — consentement lecture seule ✅ · doublons supprimés ✅ · transfert arteon.be → Gmail actif ✅ (testé le 24/11). Reste : forwarder Yahoo → Gmail.
