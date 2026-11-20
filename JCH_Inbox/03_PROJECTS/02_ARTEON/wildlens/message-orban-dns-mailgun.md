Objet : [arteon.be] Ajout d'enregistrements DNS pour Mailgun — sous-domaine mg.wildlens.arteon.be

Bonjour,

Pour l'envoi des emails du journal WildLens (hébergé sur notre VPS), merci d'ajouter les enregistrements DNS suivants dans la zone `arteon.be` (TTL 3600 ou valeur par défaut) :

1. TXT — nom `mg.wildlens.arteon.be`
   valeur : v=spf1 include:mailgun.org ~all

2. TXT — nom `k1._domainkey.mg.wildlens.arteon.be`
   valeur : k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDYBv92Lz4Nk7yS9im9CPS8yamU+tc83pNJqljrxSLEFb3i5smyPPz/7PsZGIwig+r7FUu6r1gd/BGrHUl2mzp9S3x1btP4sFoJnxO9z2t9IzydBGv9V++VHgPE5lfiEGmfcZMwLWUV9Uvdw/nthzyLjW4DYkj3DqG57rplwfL0RQIDAQAB

3. MX — nom `mg.wildlens.arteon.be` → mxa.mailgun.org (priorité 10)

4. MX — nom `mg.wildlens.arteon.be` → mxb.mailgun.org (priorité 10)

5. CNAME — nom `email.mg.wildlens.arteon.be` → mailgun.org

6. TXT (DMARC, recommandé) — nom `_dmarc.mg.wildlens.arteon.be`
   valeur : v=DMARC1; p=none;

Merci de me confirmer une fois ces enregistrements posés, pour que je puisse valider la vérification du domaine côté Mailgun.

Cordialement,
Jean-Claude Havaux
