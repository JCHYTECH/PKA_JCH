# Mail Orban45 — Consentement Graph + transfert Gmail (2026-11-21)

> **SUPERSÉDÉ 2026-11-23** — voir `reponse-orban45-2026-11-23.md` (périmètre lecture seule, client_id corrigé `31f92869-…`).

> À envoyer par JC à Orban45 (CSP gérant le tenant Microsoft 365 `arteon.be`).
> Objectif : débloquer la co-gestion Dobby (Graph délégué) + consolider les mails
> pro dans Gmail (transfert externe, aujourd'hui bloqué par l'anti-spam sortant).

---

**Objet :** [Microsoft 365 — arteon.be] Consentement administrateur + autorisation de transfert (boîte jc.havaux@arteon.be)

Bonjour,

Nous consolidons nos outils autour de la boîte `jc.havaux@arteon.be`, et nous avons besoin de deux choses, toutes deux limitées à cette seule boîte — aucun accès aux autres boîtes, aucun droit d'administration.

**1. Consentement administrateur pour l'accès API délégué (Microsoft Graph)**

Un assistant doit lire, trier et envoyer des e-mails, ainsi que lire et créer des rendez-vous, uniquement pour `jc.havaux@arteon.be`. L'application ci-dessous (déjà enregistrée dans le tenant) a besoin du consentement administrateur pour les permissions **déléguées** suivantes (elles n'agissent qu'avec l'identité de l'utilisateur connecté) :

- `Mail.ReadWrite` → `https://graph.microsoft.com/Mail.ReadWrite`
- `Mail.Send` → `https://graph.microsoft.com/Mail.Send`
- `Calendars.ReadWrite` → `https://graph.microsoft.com/Calendars.ReadWrite`
- `Contacts.Read` → `https://graph.microsoft.com/Contacts.Read`
- `User.Read` → `https://graph.microsoft.com/User.Read`

Identifiants :

- Tenant : `ea4b8942-8e3a-4707-b6c4-86b7e9a3991a`
- Application (client) : `14d82eec-204b-4c2f-b7e8-296a70dab67e`

Marche à suivre : Azure AD → **Inscriptions d'applications** → `14d82eec-…` → **Autorisations de l'API** → Ajouter → **Microsoft Graph** → **Autorisations déléguées** → cocher les cinq permissions → **« Accorder le consentement administrateur »**.

(ou, connecté avec un compte admin : `https://login.microsoftonline.com/ea4b8942-8e3a-4707-b6c4-86b7e9a3991a/adminconsent?client_id=14d82eec-204b-4c2f-b7e8-296a70dab67e`)

**2. Autorisation de transfert automatique vers Gmail**

Nous souhaitons que les mails reçus sur `jc.havaux@arteon.be` soient automatiquement transférés vers `jc.havaux@gmail.com` (boîte de consolidation). Le transfert externe est actuellement bloqué par la politique anti-spam sortante par défaut du tenant (« Automatic - System-controlled »).

Deux possibilités, au choix :

- **a) (recommandé)** Configurer le transfert au niveau de la boîte : `ForwardingSmtpAddress` = `jc.havaux@gmail.com`.
- **b)** Autoriser le transfert externe pour cette seule boîte, puis laisser JC créer sa règle « Rediriger vers » `jc.havaux@gmail.com` dans Outlook Web :

```powershell
Connect-ExchangeOnline
New-HostedOutboundSpamFilterPolicy -Name "Allow External Forwarding JC" -AutoForwardingMode On
New-HostedOutboundSpamFilterRule -Name "Allow External Forwarding JC Rule" -HostedOutboundSpamFilterPolicy "Allow External Forwarding JC" -From "jc.havaux@arteon.be"
```

Réassurance : dans les deux cas, il s'agit d'accès **délégués** et **scopés** à la seule boîte `jc.havaux@arteon.be`, révocables à tout moment. Aucune permission applicative ni aucun droit d'administration n'est demandé.

Merci de nous confirmer une fois les deux points réglés.

Bien cordialement,
Jean-Claude Havaux
