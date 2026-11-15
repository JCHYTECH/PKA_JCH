---
date: 2026-11-15
source: dobby
domain: arteon
type: analyse-marche
status: actif
lang: fr
---

# Analyse marché — Presets Lightroom naturalistes

> Source : web_search (Tavily) + fetch_url sur les pages produits (prix vérifiés le 15/11/2026).
> Objectif : mesurer la concurrence et recommander des presets nouveaux ou des améliorations.

---

## 1. Paysage concurrentiel (prix vérifiés)

| Concurrent | Contenu | Prix (vérifié) | Angle |
|-----------|---------|----------------|-------|
| Etsy (bundles) | 500+ presets wildlife | $3,62–$14,50 | Commodité, volume |
| Ralph Mayhew | 5 presets wildlife | A$5,00 | Entrée de gamme |
| Woodland Presets | nature/wildlife | $13,99–$219,99 | Large gamme |
| **Birdpack™ (birdspot)** | **115 presets par type d'oiseau** (martins-pêcheurs, geais, corneilles, limicoles…) | Shopify (BE) — prix non capturé, à vérifier | **Taxon-specific** |
| **Wild Edits V1 (Ryan Wilkes)** | **30 presets, 15 « Adaptive » à masques IA intégrés** | **US$55,00** | Masques IA |
| **LSP « Wild Spirit »** | **330 presets** — 88 masques (sujet/fond/ciel) + pinceaux (fourrure, œil, neige, museau) + 15 N&B | gamme pro | Volume + masques |

---

## 2. Structure du marché

- **Bas de gamme (commodité)** : $3–15 pour des centaines de presets génériques (Etsy, Woodland). Course au volume, zéro crédibilité.
- **Milieu/premium** : $30–60 pour 30–115 presets curés (Wild Edits $55/30, Birdpack 115).
- **Haut de gamme (volume + masques)** : packs « tout-en-un » 330 presets avec masques IA + pinceaux locaux (LSP).

**Constats clés :**
1. **Le marché est saturé en bas** — jouer le volume/prix est un cul-de-sac.
2. **Le premium se paie sur les MASQUES IA** (Wild Edits « Adaptive », LSP 88 masques) — pas sur le nombre de presets.
3. **Personne n'est zoologiste.** Aucun concurrent ne vend un regard scientifique, ni ne documente « comment la photo a été obtenue ». C'est le vide que ARTEON peut occuper.
4. **Notre offre actuelle (€29 / 4 presets) est surcotée au ratio contenu/prix** : €7,25/preset vs Wild Edits $55/30 (~$1,83/preset, masques inclus).

---

## 3. Gaps exploités → recommandations

### A. Amélioration prioritaire — les masques IA (sujet / fond)

C'est le seul levier qui justifie un prix premium. Wild Edits (15 presets « Adaptive ») et LSP (88 masques) le monétisent. **Le pipeline Argus génère déjà des masques** (les propositions PDF indiquent « 3 via masque »). On a la capacité, on ne l'exploite pas dans les presets.

→ **Recommandation :** chaque preset décliné en 2 couches — « sujet » (boost, netteté ciblée) + « fond » (ciel calmé, végétation désaturée) — via masques IA Lightroom. C'est l'argument massue face à Wild Edits.

### B. Élargir 4 → ~10-12 presets (les données existent déjà)

`lr_params.md` contient déjà les tables pour construire (≈1 h/preset) :

| Nouveau preset | Base lr_params.md | Pour qui |
|----------------|-------------------|----------|
| **Plumage coloré** | table « plumage coloré » (bleu +10-20, hue -5-10) | martin-pêcheur, rollier, guêpier |
| **Mammifères** | table « fourrure fauve » (orange +10-18, netteté 65-75) | renard, cerf, lièvre |
| **Nocturne** | WB 5800-6200 K, contraste +20-30 | chouette, blaireau |
| **Macro** | netteté élevée, clarté modérée | insectes, fleurs |
| **Action / vol** | clarté +10-18, bruit maîtrisé | oiseaux en vol, ISO haut |
| **Paysage naturaliste** | clarté +5-15, vibrance +15-25 | milieux, habitat |
| **Noir & blanc** | monochrome + grain | portfolio, éditorial |
| **Contre-jour / brume** | courbe douce, low contrast | ambiance, silhouettes |

→ **Recommandation :** passer à 10-12 presets (4 actuels + 8 ci-dessus), tous déclinés masqués. On rejoint alors le ratio contenu/prix de Wild Edits, avec l'angle zoologiste en plus.

### C. Différenciation sur l'angle zoologiste

Aucun concurrent ne groupe par **physique du plumage / habitat / lumière** avec une justification scientifique. `lr_params.md` est exactement organisé ainsi (plumage sombre/clair/coloré, fourrure, golden hour, nocturne). → Nommer et documenter chaque preset par sa **raison naturaliste** (« pourquoi ce preset pour un corvidé »), pas par un nom de lieu comme Wild Edits.

### D. Positionnement prix

- **€29 pour 4 presets** est indéfendable tel quel face à $55/30.
- **Option retenue :** €29 → 10-12 presets masqués + guide ; ou €19 → le cœur 4 presets (lancement). La valeur perçue doit porter sur le masque + le regard, pas sur le nombre.

---

## 4. Verdict

- **Concurrence réelle** : Birdpack (taxon), Wild Edits (masques, $55), LSP (volume, 330). Pas de concurrent zoologiste ni « éthique documentée ».
- **Priorité n°1** : ajouter les **masques IA** (sujet/fond) — on a déjà la capacité, et c'est ce que le marché premium paie.
- **Priorité n°2** : élargir à **10-12 presets** depuis `lr_params.md` (données prêtes).
- **Priorité n°3** : tenir l'angle **zoologiste/éthique** (personne ne le fait) et recaler le prix sur la valeur réelle.
