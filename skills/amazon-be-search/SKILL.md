---
name: amazon-be-search
description: Recherche produit sur amazon.com.be (et .fr/.de/.nl) avec sortie en liens directs /dp/ASIN + prix + titres, pour contourner le filtre de recherche d'Amazon. Déclencher sur "cherche sur amazon", "trouve un produit amazon", "lien amazon.com.be", "prix amazon be", "compare des références sur amazon".
---

# amazon-be-search

Recherche produit Amazon (priorité **amazon.com.be**), sortie **propre** : liens directs
`/dp/ASIN`, titre, prix €. Contourne le filtre de recherche d'Amazon qui ne remonte pas
les bonnes références. Le moteur est le script `bin/pka-amazon` (V1 scraping, stdlib Python, $0).

## Quand déclencher
- « cherche / trouve un produit sur Amazon », « lien amazon.com.be », « prix sur amazon be ».
- JC fournit une référence technique (ex. `TL-PA7017P`) et veut le bon lien produit.
- Comparaison de références / vérification de prix avant achat.

## Utilisation
```bash
bin/pka-amazon "TL-PA7017P"                 # recherche simple, liens /dp
bin/pka-amazon "cable cat6 1m" --verify     # titre complet + prix lus sur la fiche
bin/pka-amazon "powerline passthrough" --max 6 --json
bin/pka-amazon "usb-c ethernet" --site fr   # autre marketplace (fr|de|nl|com)
```
Options : `--site com.be|fr|de|nl|com` · `--max N` · `--verify` · `--json` · `--include-ads` · `--lang`.

## Méthode (ce que fait le script)
1. Fetch `https://www.amazon.<site>/s?k=<query>` avec UA navigateur + `Accept-Language`.
2. Parse les blocs `data-component-type="s-search-result"` → `data-asin`, titre (`a-size…a-color-base`
   / `aria-label`), prix (`a-offscreen` / `a-price-whole`). Exclut les sponsorisés par défaut.
3. Construit les **liens directs** `https://www.<site>/dp/<ASIN>`.
4. `--verify` : ouvre chaque `/dp` et lit `id="productTitle"` + prix.

## Limites & bonnes pratiques (IMPORTANT)
- **Usage personnel, faible volume.** Attendre entre deux requêtes, ne pas boucler agressivement.
- **Fragilité** : Amazon change son HTML → le parser peut casser. Sélecteurs + fallbacks, mais à re-tester.
- **Captcha / rate-limit** : possible. Le script détecte le blocage et renvoie l'URL de recherche manuelle (code retour 3).
- **ToS** : le scraping va contre les CGU Amazon. Alternative propre à terme = **API Partenaires PA-API**.
- **Prix/stock volatils** : toujours indiquer « à vérifier au moment de l'achat ».
- ASIN souvent partagés entre marketplaces UE → il reste utile de croiser `--site fr`/`de` si `.com.be` ne remonte rien.

## Codes retour
`0` OK · `1` erreur réseau · `2` site invalide · `3` captcha/blocage · `4` aucun résultat parsé.
