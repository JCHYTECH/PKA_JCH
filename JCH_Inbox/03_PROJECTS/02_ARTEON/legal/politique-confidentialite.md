---
date: 2026-05-02
tags: [legal, RGPD, confidentialite, arteon, l-instant-lu, belgique]
type: legal-document
version: 1.0
status: draft
owner: Renard 🦊
---

# Politique de Confidentialité — ARTEON / L'Instant Lu

**Conforme à l'article 13 du RGPD (Règlement UE 2016/679)**  
**Version :** 1.0 — 2026-05-02  
**Contact RGPD :** donnees@arteon.be

---

## 1. Identité du responsable de traitement

| Élément | Information |
|---------|-------------|
| **Responsable** | Jean-Claude Havaux |
| **Entité** | JCHYTECH |
| **BCE** | BE 0680.640.981 |
| **TVA** | BE0680640981 |
| **Adresse** | Rue des Renards 4, 4130 Tilff, Belgique |
| **Qualité** | Personne physique, indépendant |
| **Marque exploitée** | ARTEON |
| **Service concerné** | L'Instant Lu (`arteon.be/critique`) |
| **Contact RGPD** | donnees@arteon.be |

En tant que personne physique indépendante, ARTEON n'a pas l'obligation légale de désigner un Délégué à la Protection des Données (DPO). Toute demande relative à vos données personnelles est traitée directement par l'opérateur à l'adresse ci-dessus.

**Autorité de contrôle compétente :**  
Autorité de protection des données (APD) — Belgique  
Rue de la Presse 35, 1000 Bruxelles — [www.autoriteprotectiondonnees.be](https://www.autoriteprotectiondonnees.be)

---

## 2. Données collectées

### 2.1 Données de compte

Lors de la création de votre compte :

| Donnée | Source | Obligatoire |
|--------|--------|-------------|
| Adresse e-mail | Formulaire d'inscription | Oui |
| Prénom (optionnel) | Formulaire d'inscription | Non |
| Mot de passe (haché) | Formulaire d'inscription | Oui |
| Date d'inscription | Automatique | — |

### 2.2 Données de transaction (Stripe)

Les paiements sont traités par Stripe. ARTEON reçoit uniquement :

| Donnée | Usage |
|--------|-------|
| Identifiant de transaction Stripe | Comptabilité, support client |
| Montant et devise | Facture, TVA |
| Statut du paiement | Déblocage du service |
| Pays de la carte (code pays) | Conformité TVA UE |

**ARTEON ne stocke jamais** : numéro de carte, CVV, date d'expiration. Ces données restent chez Stripe.

### 2.3 Données photographiques

Lorsque vous soumettez une photo à L'Instant Lu :

| Donnée | Traitement |
|--------|-----------|
| Fichier image (JPEG, RAW) | Uploadé sur Cloudflare R2 (stockage temporaire) |
| Métadonnées EXIF — **sauf GPS** | Utilisées pour la fiche technique du rapport |
| **Données GPS EXIF** | **Supprimées automatiquement à l'upload** — stripping systématique |
| Titre et description soumis | Utilisés pour le filtrage éthique et le contexte d'analyse |

Le stripping GPS est une mesure technique appliquée avant tout traitement. Aucune donnée de géolocalisation n'est lue, stockée ou transmise.

### 2.4 Données de navigation (logs techniques)

Adresse IP, navigateur, pages visitées — collectés automatiquement par l'hébergeur à des fins de sécurité et de débogage. Pas de profilage comportemental. Pas de cookies publicitaires.

### 2.5 Ce que nous ne collectons pas

- Données de localisation GPS
- Données sensibles au sens de l'article 9 RGPD
- Données de mineurs (service réservé aux 18 ans et plus)

---

## 3. Finalités et bases légales

| Finalité | Données concernées | Base légale (art. 6 RGPD) |
|----------|-------------------|--------------------------|
| Fourniture du service (analyse photo, livraison rapport) | Photo, e-mail, compte | **Exécution du contrat** (art. 6.1.b) |
| Filtrage éthique de la photo soumise | Photo, titre, description | **Exécution du contrat** (art. 6.1.b) |
| Paiement et facturation | Données Stripe, e-mail | **Exécution du contrat** + **Obligation légale** (art. 6.1.b et 6.1.c) |
| Conservation des factures (7 ans) | Données de facturation | **Obligation légale** (art. 6.1.c — droit comptable belge) |
| Envoi d'e-mails transactionnels (confirmation, livraison, refus) | E-mail | **Exécution du contrat** (art. 6.1.b) |
| Envoi de la newsletter ARTEON/WildLens (si abonnement distinct) | E-mail | **Consentement** (art. 6.1.a) — révocable à tout moment |
| Sécurité et logs techniques | Logs, IP | **Intérêt légitime** (art. 6.1.f) |
| Amélioration du service (analyse statistique agrégée) | Données anonymisées | **Intérêt légitime** (art. 6.1.f) |

---

## 4. Durées de conservation

| Catégorie de données | Durée de conservation |
|---------------------|----------------------|
| **Photo soumise** (fichier image) | **30 jours** après livraison du rapport, puis suppression définitive |
| **Rapport PDF et fichier XMP** | **90 jours** dans votre espace compte, puis suppression (téléchargement recommandé) |
| **Données de compte** (e-mail, prénom) | Durée de vie du compte + 12 mois après fermeture du compte |
| **Données de facturation** | **7 ans** (obligation légale comptable belge) |
| **Logs techniques** | **30 jours** glissants |
| **Consentement newsletter** | Jusqu'au désabonnement |

**Note importante :** les rapports PDF et fichiers XMP ne sont accessibles en téléchargement que pendant 90 jours. Passé ce délai, ils sont supprimés de nos serveurs. Nous vous recommandons de les télécharger et de les conserver localement.

---

## 5. Sous-traitants et destinataires

ARTEON fait appel aux prestataires suivants, tous encadrés par des accords de traitement des données (DPA — Data Processing Agreement) :

### 5.1 Anthropic (Claude API) — Analyse IA

| Élément | Information |
|---------|-------------|
| **Rôle** | Sous-traitant — traitement IA des photos et génération des rapports |
| **Pays** | États-Unis (San Francisco, CA) |
| **DPA** | Anthropic Data Processing Addendum — [trust.anthropic.com](https://trust.anthropic.com) |
| **Transfert EU-USA** | Encadré par les **Clauses Contractuelles Types (CCT)** approuvées par la Commission européenne (Décision 2021/914) |
| **Engagement clé** | Anthropic s'engage contractuellement à ne pas utiliser les données transmises via l'API pour entraîner ses modèles, sauf accord explicite du client. ARTEON n'a pas donné cet accord. |
| **Données transmises** | Image (sans données GPS), contexte textuel de l'analyse |

**Ce que cela signifie pour vous :** votre photo est transmise à Anthropic pour traitement, mais Anthropic ne peut pas l'utiliser pour améliorer ses modèles dans le cadre de cette utilisation API. Le transfert est légalement encadré par les CCT.

### 5.2 Stripe — Paiement

| Élément | Information |
|---------|-------------|
| **Rôle** | Sous-traitant — traitement des paiements |
| **Pays** | Irlande (filiale UE), États-Unis |
| **DPA** | Stripe Data Processing Agreement |
| **Certification** | PCI-DSS Level 1 |
| **Données traitées** | Données de paiement (ARTEON n'y a pas accès) |

### 5.3 Cloudflare — Stockage et CDN

| Élément | Information |
|---------|-------------|
| **Rôle** | Sous-traitant — stockage temporaire des photos (Cloudflare R2), CDN |
| **DPA** | Cloudflare Data Processing Addendum |
| **Localisation des données R2** | Région UE configurable |

### 5.4 Hébergeur du site

Détails à compléter à la mise en production (Cloudflare Pages / VPS / autre).

---

## 6. Vos droits

Conformément aux articles 15 à 22 du RGPD, vous disposez des droits suivants :

| Droit | Ce que cela signifie | Comment l'exercer |
|-------|---------------------|------------------|
| **Accès** (art. 15) | Obtenir une copie de toutes vos données personnelles détenues par ARTEON | donnees@arteon.be |
| **Rectification** (art. 16) | Corriger des données inexactes | donnees@arteon.be ou votre espace compte |
| **Effacement** (art. 17) | Demander la suppression de vos données (« droit à l'oubli ») — sous réserve des obligations légales de conservation | donnees@arteon.be |
| **Limitation** (art. 18) | Geler le traitement de vos données dans certaines situations | donnees@arteon.be |
| **Portabilité** (art. 20) | Recevoir vos données dans un format structuré et lisible par machine (JSON ou CSV) | donnees@arteon.be |
| **Opposition** (art. 21) | Vous opposer au traitement fondé sur l'intérêt légitime (notamment les communications marketing) | donnees@arteon.be ou lien de désabonnement |
| **Retrait du consentement** | Retirer votre consentement à la newsletter à tout moment | Lien de désabonnement dans chaque e-mail |
| **Réclamation** | Porter une réclamation auprès de l'APD belge | [www.autoriteprotectiondonnees.be](https://www.autoriteprotectiondonnees.be) |

**Délai de réponse :** ARTEON s'engage à répondre à toute demande relative à vos droits dans un délai de **30 jours** à compter de la réception de votre demande (délai pouvant être prolongé de 2 mois en cas de complexité — vous en seriez informé).

**Identification :** Pour traiter votre demande, ARTEON peut vous demander de confirmer votre identité (adresse e-mail associée au compte). Aucune pièce d'identité n't requise pour les demandes simples.

---

## 7. Cookies et traceurs

L'Instant Lu utilise un nombre minimal de cookies :

| Cookie | Finalité | Durée | Consentement requis |
|--------|---------|-------|---------------------|
| Session d'authentification | Maintien de votre connexion | Durée de session | Non (fonctionnel) |
| CSRF token | Sécurité des formulaires | Session | Non (fonctionnel) |
| Stripe.js | Traitement sécurisé du paiement | Session | Non (fonctionnel) |

Aucun cookie publicitaire, aucun pixel de tracking, aucun outil d'analytics comportemental ne sont utilisés.

---

## 8. Sécurité des données

ARTEON met en œuvre les mesures techniques suivantes :

- Transmission chiffrée via HTTPS/TLS sur l'ensemble du site
- Stockage des photos sur Cloudflare R2 avec accès restreint (URL signées temporaires)
- Mots de passe hachés (bcrypt ou équivalent) — jamais stockés en clair
- Stripping automatique des données GPS à l'upload
- Accès administrateur protégé par authentification renforcée
- Suppression automatique des photos après 30 jours

---

## 9. Modification de la politique

En cas de modification substantielle de la présente politique, vous serez informé(e) par e-mail au moins 30 jours avant l'entrée en vigueur de la nouvelle version.

La version en vigueur est toujours accessible à `arteon.be/legal/confidentialite`.

---

*Document rédigé par Renard 🦊, conseiller juridique ARTEON*  
*Version 1.0 — 2026-05-02 — À valider par JCH avant mise en ligne*  
*Contact RGPD : donnees@arteon.be*
