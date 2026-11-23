# Réponse Orban45 — Précisions outil + périmètre (2026-11-23)

> À envoyer par JC à Orban45. Répond aux 2 questions reçues.
> Stratégie : présenter un périmètre **lecture seule** (phase 1), retirer
> `Mail.Send` et `Calendars.ReadWrite` de la demande initiale pour réduire la
> friction de consentement.

> **Correction 2026-11-23** : client_id corrigé `14d82eec-…` → `31f92869-5887-47c2-b35a-b3e2aa52a324` (l'ancien ID n'existait pas dans le tenant). App reconfigurée en **lecture seule** — 4 permissions déléguées, toutes « non accordées » en attente du consentement admin.

> **Demande reçue — texte exact (2026-11-23) :**
> « Jean-Claude, Avant d'activer l'accès de votre assistant à votre boîte et le transfert vers Gmail, pourriez-vous me confirmer trois choses ?
> - Quel est l'outil / assistant exact utilisé pour les mails ? (Une capture d'écran de sa configuration serait parfaite)
> - L'assistant doit pouvoir faire quoi : lire et trier tes mails, en envoyer en votre nom, gérer l'agenda ?
> Bien à vous, »

---

**Objet :** Re: [Microsoft 365 — arteon.be] Consentement administrateur + autorisation de transfert

Bonjour,

Merci pour votre retour. Voici les précisions demandées.

**1. L'outil / assistant exact**

C'est un assistant personnel que j'exécute **localement sur mon Mac** (macOS), via l'outil en ligne de commande **DeepSeek** (modèle DeepSeek V4). Il n'y a aucun service cloud tiers hébergé : les scripts tournent sur ma machine, pas chez un prestataire.

Pour les mails, l'accès passe par deux canaux concrets :

- **Gmail** : un script Python local (`gmail_imap_fetch.py`) lit la boîte en **IMAP** avec un mot de passe d'application Google, et ne relève que les messages adressés à l'alias dédié `jc.havaux+dobby@gmail.com` (recherche ciblée, jamais la boîte entière).
- **arteon.be (Microsoft 365)** : l'application Azure AD enregistrée dans le tenant (`31f92869-5887-47c2-b35a-b3e2aa52a324`), via l'API **Microsoft Graph en mode délégué** — elle n'agit qu'avec mon identité connectée, jamais en mode applicatif, et uniquement sur ma boîte.

(Capture d'écran ci-jointe : l'inscription d'application Azure AD et la liste de ses autorisations.)

**2. Ce que l'assistant doit pouvoir faire**

Pour démarrer, **uniquement de la lecture et du tri** :

- **Lire** les mails reçus et me les présenter triés (expéditeur, objet, priorité). Le classement réel reste fait par moi.
- **Ne rien envoyer en mon nom** : aucun envoi automatique. Si l'envoi devient nécessaire plus tard, ce sera uniquement sous forme de brouillon que je valide et envoie moi-même.
- **Agenda** : **lecture seule** du calendrier, pour me signaler mes rendez-vous. Aucune création ni modification automatique — chaque écriture passerait par ma validation explicite.

Concrètement, je réduis donc la demande de permissions à la **lecture seule** :

- `Mail.Read` (au lieu de `Mail.ReadWrite`)
- `Calendars.Read` (au lieu de `Calendars.ReadWrite`)
- `User.Read`
- `Contacts.Read` — pour trier par expéditeur connu

`Mail.Send` et l'écriture du calendrier sont retirés de cette première demande.

**Transfert vers Gmail (inchangé)**

Les mails reçus sur `jc.havaux@arteon.be` sont transférés automatiquement vers `jc.havaux@gmail.com` (boîte de consolidation). Deux options possibles :

- **a) (recommandé)** Configurer le transfert au niveau de la boîte : `ForwardingSmtpAddress` = `jc.havaux@gmail.com`.
- **b)** Autoriser le transfert externe pour cette seule boîte, puis je crée ma règle « Rediriger vers » dans Outlook Web.

Dans les deux cas, accès **délégués et scopés** à la seule boîte `jc.havaux@arteon.be`, révocables à tout moment. Aucune permission applicative, aucun droit d'administration.

Merci de me confirmer une fois réglé.

Bien cordialement,
Jean-Claude Havaux