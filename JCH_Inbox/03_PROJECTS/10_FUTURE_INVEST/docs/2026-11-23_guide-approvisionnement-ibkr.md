---
project: Future Invest
type: guide-procedure
author: "[[Dobby]]"
created: 2026-11-23
status: actif
---

# Guide d'approvisionnement IBKR (virement SEPA depuis Belfius)

## Contexte
- Compte IBKR **approuvé le 2026-11-23** (devise de base **EUR**).
- Premier dépôt : **5 000 €** (tranche 1 du plan 5 000 → 10 000 → montage graduel).
- Plafond Belfius relevé manuellement pour un virement unique de 5 000 €.

## Principe (à retenir)
IBKR Europe (IBIE) **ne « lie » pas ta banque pour déposer**. Le dépôt est un virement
SEPA unidirectionnel : tu envoies l'argent depuis Belfius vers l'**IBAN de dépôt** qu'IBKR
t'affiche, avec une **référence unique** qui rattache les fonds à ton compte.

## Étapes
1. Portail Client → **Transfert et Paiement** → **Déposer des fonds**.
2. **Devise = EUR** · **Méthode = Virement bancaire**.
3. **Montant = 5 000 €** → **Créer dépôt** (annonce de dépôt).
4. IBKR affiche : **IBAN de dépôt** (souvent un IBAN virtuel à ton nom) + **référence unique**.
5. Depuis Belfius : virement SEPA vers cet IBAN, **référence collée dans le champ communication**.
6. Virement parti le soir → traité J+1 → crédit IBKR ~J+2 à J+3 (**est. 25-26/11**).

## Pièges
- **Titulaire** : le virement doit venir d'un compte à **ton nom** (sinon rejet compliance).
- **Référence** : obligatoire dans le champ communication — sans elle, les fonds restent en attente de réconciliation.
- **Ne pas utiliser « Ajouter un compte bancaire »** pour déposer : cette section sert aux **retraits**, pas aux dépôts.
- **Premier dépôt** : possible hold anti-blanchiment de quelques jours — il ne concerne que les **retraits** sortants, pas la capacité de négociation (buying power).

## Notes
- Les 5 000 € restent en **cash EUR** — pas de position, pas de risque.
- Référence IBKR : **à archiver ici dès le dépôt effectué** (champ ci-dessous).

```
Référence IBKR : (à compléter)
Date du virement : 2026-11-23 (soir)
Montant : 5 000 €
```
