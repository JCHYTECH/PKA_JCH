# Procédure Mailgun — WildLens (à exécuter par JC)

> Mise à jour : 2026-11-17 · Domaine d'envoi : `mg.wildlens.arteon.be` (sous-domaine, pas la racine `arteon.be`).
> Objectif : brancher Ghost (sur le VPS Hostinger) à Mailgun pour envoyer la newsletter.

---

## Phase 1 — TOI, dans le navigateur (~15 min)

1. Va sur `mailgun.com` puis **Sign up**.
   - Choisis la région **EU** (RGPD, lecteurs en Europe).
   - Note la région choisie : EU ou US.

2. Menu **Domains > Add domain**.
   - Saisis exactement : `mg.wildlens.arteon.be`
   - (pas `wildlens.arteon.be`)

3. Mailgun affiche les enregistrements DNS à poser (4 au total) :
   - **TXT** (SPF) : `v=spf1 include:mailgun.org ~all`
   - **TXT** (DKIM) : sélecteur `k1._domainkey.mg.wildlens.arteon.be` + valeur longue
   - **MX** : `mxa.mailgun.org` et `mxb.mailgun.org`
   - **CNAME** (tracking) : `email.mg.wildlens.arteon.be` -> `mailgun.org`
   - Copie les valeurs exactes générées par Mailgun, telles quelles.

4. Transmets ces 4 enregistrements à **Orban** (le DNS d'`arteon.be` est chez Gandi, c'est lui qui les pose).
   - Précise : tout sous `mg.wildlens.arteon.be`, TTL 3600.

5. Une fois posés, retourne dans Mailgun -> **Verify** (2 min à quelques heures).

6. Dans **Domain settings > SMTP credentials**, relève :
   - **SMTP username** : `postmaster@mg.wildlens.arteon.be`
   - **SMTP password**

## Ce que tu renvoies à Dobby (3 infos)

- SMTP username
- SMTP password
- la région (EU ou US)

---

## Phase 2 — DOBBY, sur le VPS (dès réception des 3 infos)

    cd /var/www/ghost
    ghost config set mail transport SMTP
    ghost config set mail options.host smtp.eu.mailgun.org    (ou smtp.mailgun.org si US)
    ghost config set mail options.port 587
    ghost config set mail options.auth.user postmaster@mg.wildlens.arteon.be
    ghost config set mail options.auth.pass '<mot-de-passe>'
    ghost restart

Puis : envoi d'une newsletter de test depuis l'admin Ghost.

---

## Plan tarifaire (rappel)

- **Free** : 100 emails/jour, permanent -> suffisant pour démarrer/tester (liste à 0 aujourd'hui).
- **Basic** : 15 $/mois, 10 000 emails/mois -> à prendre dès que la liste dépasse ~100 abonnés
  (sinon un blast hebdo à 500 serait bloqué : 500 emails le même jour > 100/jour).

Rien à décider maintenant. Dobby l'a noté.
