---
tags:
  - type/project
  - status/active
---
# ARTEON — État du projet

*Document de référence — mis à jour le 21 avril 2026, fin étape 3*

---
[[Website_Analysis_and_Reproduction]]
## Identité validée

### Slogan principal

> **L'instant figé, la pensée en mouvement.**

### Variantes secondaires

- **Même tissu.** — signature courte (footer, bio, étiquette tirage)
- **Instant figé. Pensée en mouvement.** — variante typographique brute (visuels, capitales)
- **Du figé naît le mouvant.** — citation visuelle, image-citation réseaux
- **Naturaliste avant photographe.** — positionnement page affiliation

### Manifeste

Deux versions livrées en `.md` :

- `arteon-manifeste-long.md` — version éditoriale, ~515 mots
- `arteon-manifeste-court.md` — version dense, ~250 mots, pour signatures, dossiers, page « à propos » courte

---

## Décisions structurantes

### Domaine

- **arteon.be** : enregistré (domaine principal)
- **arteon.photo** : à acquérir si disponible. À vérifier chez Gandi ou Porkbun (Hostinger ne vend pas cette extension)
- **arteon.com** : pris par un tiers

### Langues

Trilingue **FR / EN / IT** pour le site Arteon.
WILDLENS reste en **anglais uniquement** (pour l'instant).

### Architecture du site

```
/
├── /manifeste
├── /artistes
│   ├── /artistes (index)
│   └── /artistes/jc-havaux (premier artiste, template)
├── /shop
│   ├── /shop (catalogue, filtres : espèce, biotope, artiste, format)
│   └── /shop/[slug-photo] (fiche augmentée + déclaration éthique)
├── /wildlens (vitrine du journal, lien vers Ghost)
├── /affiliation (formulaire + critères publics + registre du curateur)
└── /legal (CGV, mentions, RGPD, éthique prise de vue)
```

### Stack technique

- **Shopify Basic** (~27 € HT/mois) + thème custom + app WhiteWall pour le shop
- **Ghost** conservé pour WILDLENS (wildlens.ghost.io)
- Paiements : Stripe, Paypal
- Achat invité possible sur tirages standard, inscription requise pour wishlist, alertes WILDLENS, contenus naturalistes approfondis

### WhiteWall

- Société allemande (Frechen, laboratoire 10 000 m²)
- Intégration via app Shopify officielle (token API à coller dans Shopify)
- Paiements directs au merchant Arteon, facturation séparée WhiteWall pour production + envoi
- Limite à connaître : pas de marque blanche encore, le colis WhiteWall reste visible côté client

### Modèle artistes / affiliation

- Commission sur vente (taux à définir, dégressif à l'ancienneté)
- Exclusivité **par œuvre** (3 ans renouvelable), pas par artiste
- Rétention par valeur ajoutée (curation, volume WhiteWall négocié, pipeline promo, données ventes)
- Jury de sélection : 3 personnes (JC + naturaliste + photographe pro, à recruter)
- Premier artiste affilié : JC Havaux, 10 photos prêtes pour V1

---

## Ennemis déclarés (sélection éditoriale)

Arteon refuse :

- Photo décorrélée du contexte écologique, *sauf* documentation de l'urbanisation du vivant
- Nourrissage / appâtage non déclaré
- Anthropomorphisme niais
- Greenwashing marketing
- Trucage numérique non déclaré (le trucage est OK s'il est déclaré explicitement dans la fiche)
- Dérangement délibéré de l'animal pour la prise
- Publication de coordonnées GPS

Les **animaux domestiques** sont acceptés à l'analyse.

---

## Ton et registre

- 20 % militant
- 30 % contemplatif
- 30 % scientifique
- 20 % technicien photo

Références littéraires pour le ton : **Despret, Attenborough, Tesson**.
Concepts d'**interdépendance** et **non-séparation** intégrés sans étiquetage explicite (option γ — bouddhisme implicite).

---

## Roadmap

| # | Étape | État |
|---|---|---|
| 1 | Réservation domaine | ✅ arteon.be enregistré |
| 2 | Manifeste Arteon | ✅ v2 validée, 2 fichiers livrés |
| 3 | Slogan Arteon | ✅ Validé |
| 4 | **Charte graphique** (palette, typo, logo, règles) | **▶ Prochaine étape** |
| 5 | Template fiche artiste | ⏳ |
| 6 | Template fiche produit (fiche naturaliste) | ⏳ |
| 7 | Formulaire et processus d'affiliation | ⏳ |
| 8 | Setup Shopify | ⏳ |
| 9 | Setup WhiteWall | ⏳ |
| 10 | Intégration WILDLENS ↔ Arteon | ⏳ |
| 11 | Préparation 10 photos JC (sélection + fiche naturaliste) | ⏳ |
| 12 | Retravail des 3 éditions WILDLENS existantes | ⏳ |
| 13 | Lancement V1 | ⏳ |

---

## Pour reprendre dans un nouveau chat

Coller en première ligne du nouveau chat :

> *On reprend le projet Arteon. Cherche notre conversation du 21 avril 2026 et lis l'état du projet. Je joins aussi le fichier `arteon-etat-projet.md`. Prochaine étape prévue : étape 4, la charte graphique.*

Et joindre ce fichier en pièce attachée.
