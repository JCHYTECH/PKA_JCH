# WildNexus — Politique procurement P0 vers Liège

**Date :** 2026-05-18  
**Décision process :** l'équipe WildNexus doit chercher le meilleur endroit où acheter, pas seulement définir le composant à acheter.

## Problème

Le flux actuel est trop coûteux :

1. l'équipe définit ce qu'il faut acheter ;
2. JCH cherche lui-même sur plusieurs sites ;
3. JCH renvoie des liens pour analyse ;
4. l'équipe valide ou rejette.

Ce flux déplace trop de charge sur JCH et multiplie les allers-retours.

## Nouvelle règle

Pour chaque composant WildNexus, l'équipe doit livrer directement :

- le composant recommandé ;
- le fournisseur recommandé ;
- le lien direct ;
- le prix approximatif ;
- la disponibilité ;
- le coût / délai de livraison vers Liège, Belgique ;
- une alternative crédible ;
- les risques de variante ou d'achat.

## Préférence fournisseur

Ordre de préférence à appliquer, sauf justification contraire :

1. fournisseur renommé permettant centralisation : Mouser, DigiKey, Farnell/element14, RS, TME ;
2. fabricant ou distributeur officiel : RAK, Seeed, Arducam, Lensation, Evetar, Hammond, Spelsberg ;
3. fournisseur EU fiable : Reichelt, Conrad, TME, autres selon disponibilité ;
4. Amazon uniquement pour prototypage rapide ou disponibilité immédiate ;
5. AliExpress uniquement pour pièces non critiques, doublées par alternative, ou banc exploratoire.

## Critères de décision

| Critère | Poids |
|---|---:|
| Fiabilité fournisseur / traçabilité | 30 % |
| Centralisation commandes | 20 % |
| Stock EU / délai vers Liège | 20 % |
| Coût total livré | 15 % |
| Documentation / datasheet / schéma | 10 % |
| Retour / SAV | 5 % |

## Règle pratique

Si deux fournisseurs sont proches en prix, choisir celui qui centralise le plus d'achats WildNexus et réduit le temps JCH.

Si un produit Amazon/AliExpress semble intéressant, l'équipe doit d'abord chercher l'équivalent chez un fournisseur reconnu avant de recommander l'achat marketplace.

## Mandat équipe

- **Bruno** : coût total livré, seuils livraison gratuite, consolidation panier.
- **Forge** : compatibilité technique, variantes, documentation, références exactes.
- **Milan** : qualité fournisseur, disponibilité EU, risque contrefaçon / clone.
- **Chouette** : adéquation terrain et accessoires nécessaires.

## Livrable attendu

Mettre à jour `WILDNEXUS_SUPPLY_REGISTER.md` avec des colonnes procurement complètes avant toute commande M-01.
