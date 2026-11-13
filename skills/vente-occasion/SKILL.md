---
name: vente-occasion
description: Pipeline de vente d'objets d'occasion en Belgique — estimation du prix de revente (2dehands/Vinted/eBay), rédaction d'annonce bilingue FR/NL, recommandation de la marketplace la plus adaptée, suivi des réponses et rentabilité. Déclencher sur "je veux vendre", "objet à vendre", "estime le prix", "rédige l'annonce", "seconde main", "vente occasion".
---

# /vente-occasion — Vente d'objets d'occasion (Belgique)

Pipeline PKA de vente sur les sites de seconde main. Projet `12_VENTE_OCCASION`.

> Point d'entrée projet : `JCH_Inbox/03_PROJECTS/12_VENTE_OCCASION/INDEX.md`
> Zone de dépôt : `JCH_Inbox/03_PROJECTS/12_VENTE_OCCASION/inbox/`

## Principe

JC dépose photos + fiche objet dans `inbox/`. Dobby (ou un spécialiste) transforme ça en une annonce prête à publier, au bon prix, sur le bon site — puis suit les réponses et la rentabilité. Aucune API payante ni scraping en Phase 1.

## Étapes d'exécution

### 1. Lire la fiche objet

Ouvrir le fichier `*.md` dans `inbox/`. S'il manque des champs essentiels (catégorie, état, photos, prix visé), les demander à JC avant de continuer.

### 2. Estimer le prix de revente (zone Belgique)

Rechercher des annonces **comparables et réelles** :

- **2dehands.be / 2ememain.be** — annonces actives (prix demandés).
- **Vinted** — prix demandés pour la même marque/modèle/état.
- **eBay** — filtres « ventes réussies » (sold) pour les prix réellement payés.

Méthode :
1. Identifier marque + modèle exact + état.
2. Chercher 5 à 10 comparables sur au moins 2 plateformes (`web_search` puis `fetch_url` sur les pages d'annonces).
3. Sortir une **fourchette** : prix plancher (vente < 1 semaine), prix médian, prix haut (patience).

Règles de cadrage :
- État « bon » sans défaut → ~40-50 % du prix neuf ; « correct » avec usure → ~20-35 % ; « à réparer » → 10-20 %.
- La rareté (collection, édition limitée) et la saisonnalité peuvent faire grimper au-dessus de 50 %.
- Toujours vérifier la **demande** : un objet sans annonce comparable = soit rare (monter), soit invendable (baisser fort).

Rendu : fourchette + prix conseillé + justificatif (2-3 liens comparables).

### 3. Recommander le site

Décision par catégorie et logistique :

- **Vinted** → vêtements, chaussures, sacs, livres, petits objets **légers et expédiables** (< 2 kg). Expédition intégrée (Vinted Go), paiement sécurisé, peu de spam. Hors Vinted (mobilier, gros électro), aller sur 2dehands.
- **2dehands / 2ememain** → meubles, électroménager, outillage, matériel, objets **volumineux ou lourds**, remise en main propre locale. Leader belge, local, gratuit pour particuliers.
- **eBay** → électronique, high-tech, collection, pièces rares, tout ce qui gagne à une **audience internationale** ou à la vente aux enchères.
- **Facebook Marketplace** → vente express locale tous types, gratuit, mais **spam élevé** (prévoir le filtrage).

Règle par défaut : léger + standard → Vinted ; volumineux → 2dehands ; valeur/collection/électronique → eBay. Si doute, proposer 2 sites et expliquer.

### 4. Rédiger l'annonce (bilingue FR + NL)

Créer le fichier dans `annonces/` à partir de `_modele-annonce.md`.

- **Titre** : Marque + Modèle + caractéristique clé + état (ex: « Canon EOS 5D Mark III — boîtier, bon état »).
- **Prix** : le prix conseillé de l'étape 2, affiché ferme (jamais « négociable »).
- **Description FR + NL** : honnête sur l'état et les défauts (une description qui ment coûte plus cher qu'elle ne rapporte), dimensions, fonctionnalités, raison de vente, retrait à domicile.
- **Photos** : conseiller lumière naturelle, 3-6 angles, gros plan des défauts, fond neutre.

### 5. Publier sur 2ememain / 2dehands (manuel en Phase 1)

1. Se connecter sur **2ememain.be** (interface FR ; même compte que 2dehands.be).
2. « Déposer une annonce » (Plaats zoekertje).
3. Champs à remplir :
   - **Titre** : coller le titre complet (avec arguments de valeur).
   - **Catégorie** : Ordinateurs et logiciels → Imprimantes.
   - **Prix** : le prix conseillé (ferme).
   - **Description** : coller la description FR, puis la version NL en dessous (pour toucher la Flandre).
   - **Photos** : téléverser les JPEG depuis `inbox/`.
   - **État** : « Utilisé » (honnête, même si impeccable — le texte précise l'état réel).
   - **Localisation** : commune de JC (le retrait à domicile s'affiche).
   - **Livraison** : « Retrait » uniquement, désactiver l'envoi.
4. Ignorer les options payantes (mise en avant) sauf demande de JC.
5. Publier, puis noter le lien dans `suivi/<objet>.md`.

### 6. Suivre les réponses

À chaque message reçu, compléter le fichier `suivi/<objet>.md` :

- Flag **spam** (demande de paiement externe, lien suspect, offre aberrante, « envoie par transporteur ») → écarter.
- États : `en_attente` / `negocié` / `vendu` / `expédié` / `abandonné`.

### 7. Clôturer et tracer la rentabilité

À la vente, ajouter une ligne dans `rentabilite.csv` (séparateur `;`, compatible Excel FR/BE) :

```
date_ajout;objet;categorie;site;prix_achat;prix_vise;prix_vendu;frais;date_vente;marge;marge_pct;statut
```

- `marge` = prix_vendu − prix_achat − frais
- `marge_pct` = marge / (prix_achat + frais) × 100
- `statut` : `en_cours` / `vendu` / `abandonné`

Puis déplacer fiche + annonce + suivi dans `archives/`.

## Règles

- Ne jamais inventer un prix : chaque chiffre vient d'une annonce comparable réelle, avec un lien.
- Annonce honnête sur l'état — jamais « comme neuf » si l'objet porte des traces.
- Belgique bilingue : toujours produire FR **et** NL.
- **Retrait à domicile uniquement** (sauf livres → envoi/point relais). Pas de livraison ni d'expédition : l'acheteur vient chercher l'objet chez JC.
- **Impression des fiches (mémoire)** : recto seul + noir et blanc — `lp -d <imprimante> -o Duplex=None -o ColorModel=Gray`. Les PDF sont des archives internes, jamais pour publication.
- Ne pas mentionner l'âge ni le prix d'achat dans l'annonce : à révéler lors de la négociation (préférence JC).
- Ne pas écrire « négociable » dans l'annonce : le prix affiché est ferme (la négociation se fait à l'oral). Titre complet incluant les arguments de valeur (ex : « avec 3 jeux d'encres »).
- En Phase 1 : **pas de scraping, pas d'API payante**. La recherche passe par `web_search` + `fetch_url` (lecture seule).
- Si JC demande un suivi d'enchères ou d'expédition, rester dans le périmètre : conseil + tracking local.

## Phase 2 (différée, non activée)

Si la publication manuelle devient un goulot, évaluer **Omnivaleur** (Light 9,99 € / Pro 19,99 €/mois) pour cross-lister 2dehands+Vinted+eBay et centraliser messages/analytics. Ne pas l'activer sans validation de JC.

## Skills liés

- **`capture`** — pour archiver un insight de prix (ex: « les vélos se vendent 60 % du neuf au printemps »).
- **`decision-gate`** — avant toute action sortante (partage d'annonce, réponse à un acheteur inconnu).
