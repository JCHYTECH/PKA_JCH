---
date: 2026-11-12
source: editorial-dobby
domain: pka/arteon/wildlens
type: operations
status: active
owner: "[[Dobby]]"
lang: fr
tags:
  - wildlens
  - ghost
  - arteon
  - editorial
---

# WildLens — Opérations de création du site Ghost

> Checklist opérationnelle pour **finaliser** le site WildLens sur Ghost.
> **Mise à jour 2026-11-13 : le compte n'est PAS perdu** — admin `wildlens.ghost.io` accessible
> (jc.havaux@gmail.com, essai 14 j, 1 post « Coming soon », 0 membre). On finalise le site existant.
> Domaine final : `wildlens.arteon.be` (custom, dans un second temps via CNAME).
> Références : `thread-arteon.md`, `brand/arteon-architecture-charte.md` §3,
> `wildlens/ref/architecture-editoriale-v2.md`.

> ⚠️ **Phase 1 (création de compte) est OBSOLÈTE** : le compte et le site existent déjà.
> Commencer directement à la Phase 3 (thème) après avoir passé le site en public.

---

## Point de décision à trancher avant de démarrer

Deux cibles coexistent dans la doc :

- `wildlens-journal.ghost.io` — sous-domaine Ghost(Pro), plan Starter ~9 $/mois (option A retenue le 12/11).
- `wildlens.arteon.be` — domaine custom, prévu par la charte §3.3.

**Recommandation** : créer d'abord sur le sous-domaine, brancher le domaine custom
`wildlens.arteon.be` dans un second temps (Ghost(Pro) le permet, il faut posséder le domaine
chez le registrar). À confirmer par JC.

---

## Phase 1 — Compte et création (exécuté par JC, pas Dobby)

1. Aller sur `https://ghost.org`, créer un nouveau compte (le précédent est perdu — carte inconnue).
2. Choisir le plan **Starter** (essai 14 j, ~9 $/mois) — blog + newsletter, suffisant pour WildLens.
3. Créer le site → nommer la publication **WildLens**, URL provisoire `wildlens-journal.ghost.io`.
4. Régler le statut du site sur **privé** jusqu'à la fin de la mise en place (évite un site vide en ligne).

## Phase 2 — Domaine (selon décision ci-dessus)

5. Option sous-domaine : conserver `wildlens-journal.ghost.io` provisoirement.
6. Option custom : dans Settings → Site → Custom domain, saisir `wildlens.arteon.be` puis créer un CNAME chez le registrar pointant vers `xxx.ghost.io`.
7. Activer le HTTPS (Ghost gère le certificat Let's Encrypt automatiquement).

## Phase 3 — Thème

8. Installer un thème épuré type **Casper** (défaut) ou **Source** (meilleure gestion newsletter), à trancher.
9. Préparer une déclinaison WildLens si besoin (masthead, typo, accent) — Dobby peut générer le thème custom si JC valide le choix.

## Phase 4 — Charte visuelle WildLens (valeurs déjà figées)

10. Accent : **Vert Terrain `#3D5A3E`** (masthead, tags, liens actifs, bordure newsletter).
11. Palette ARTEON de base : Noir Terrain, Ivoire, Ocre Lumière.
12. Typo : **Space Grotesk** (titres/nav) + **Lora** (corps) + **Lora Italic** (chapeaux/citations terrain) + **IBM Plex Mono** (métadonnées).
13. Header : `[Logo "W" stylisé vert terrain] WILDLENS by ARTEON · S'abonner` — le lien « by ARTEON » renvoie vers `arteon.be`.

## Phase 5 — Structure et navigation

14. Créer les pages fixes : **About** (manifeste), **Newsletter** (page d'abonnement).
15. Créer les tags de la charte : `technique`, `ethique` + tags par espèce au fil de l'eau.
16. Configurer la navigation principale : Accueil · Technique · Éthique · About · S'abonner.
17. Définir les slugs des articles conformes à `/tag/[espece]`, `/tag/technique`, `/tag/ethique`, `/[slug-article]`.

## Phase 6 — Newsletter / membership

18. Configurer Ghost Members : formulaire d'abonnement (gratuit au départ), email de bienvenue.
19. Brancher le mail transactionnel (Mailgun natif Ghost(Pro), ou config minimale Starter).
20. Définir le template de newsletter (en-tête WildLens, chapeau Lora Italic, footer ARTEON).

## Phase 7 — Migration du contenu existant

21. Importer les 6 éditions déjà rédigées (`editions/` : 03-28, 04-18, 06-20, 07-02, 10-24, 10-31) — Dobby les convertit au format Ghost (markdown → import ou saisie).
22. Vérifier chaque édition contre l'architecture v2 (The Frame / The Shift / The Field), langue **EN uniquement**.
23. Rattacher images et crédits photo (matière `06_PHOTO_NATURE`).

## Phase 8 — SEO et intégrations

24. Renseigner les métadonnées : titre du site, description, meta par article (EN).
25. Vérifier sitemap + RSS (Ghost les génère nativement).
26. Brancher les intégrations utiles : analytics, boutons de partage, lien Instagram en couche de découverte (sans publication auto).

## Phase 9 — Credentials et documentation (Dobby)

27. Documenter les credentials Ghost dans `JCH_PRIVATE/` (jamais dans le repo public).
28. Mettre à jour `JCH_Inbox/06_ADMIN/abonnements.md` : ligne Ghost passée de « 🔄 à recréer » à « ✅ actif » avec plan + échéance.
29. Mettre à jour `thread-arteon.md` (TTD P1 → done) et `wildlens/INDEX.md` (plateforme active, URL final).

## Phase 10 — Workflow de publication et vérification

30. Confirmer la cadence hebdo (samedi) et le rôle du launchd `com.dobby.wildlens-weekly` (déjà réactivé).
31. Publier une édition de test, vérifier rendu mobile + newsletter d'envoi.
32. Passer le site en **public**, vérifier les URL canoniques (404 résolu).

---

## Ordre critique

**1→4** (compte) puis **14→17** (structure) avant toute publication.
La charte et l'architecture sont déjà figées : les étapes 10-13 et 21-23 ne demandent
aucune décision créative supplémentaire.

## Répartition des rôles

- **JC** : Phase 1 (signup — compte/carte personnels), décision domaine (sous-domaine vs custom), validation du thème.
- **Dobby** : Phase 7 (conversion éditions), Phase 9 (credentials + doc), génération du thème custom si demandé.

---

*Fichier généré par Dobby 🦉 le 2026-11-12.*
