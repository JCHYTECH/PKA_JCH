---
date: 2026-05-02
tags: [arteon, architecture, charte-graphique, wildlens, l-instant-lu, design]
type: project-plan
status: actif
owner: [[Vega]] 🦚
---

# ARTEON — Architecture & Charte graphique

> Document de référence pour toutes les décisions visuelles et structurelles.  
> Couvre : ARTEON (site principal), [[WildLens]] (journal), L'Instant Lu (service critique).  
> Toute décision de design s'appuie sur ce document — il prime sur les préférences ponctuelles.

---

## 1. Carte du site — Architecture complète

### 1.1 Domaines et sous-domaines

| URL | Plateforme | Contenu |
|-----|-----------|---------|
| `arteon.be` | Shopify | Site principal — shop, manifeste, artistes, services |
| `wildlens.arteon.be` | Ghost (domaine custom) | Journal naturaliste — articles, newsletter |
| `arteon.be/wildlens` | Shopify (vitrine) | 3 derniers articles + CTA abonnement [[WildLens]] |
| 

### 1.2 Sitemap complet

```
arteon.be/
│
├── / — Page d'accueil
│   ├── Hero — slogan + photo signature + CTA shop
│   ├── Bloc Manifeste — extrait 2 phrases + lien /manifeste
│   ├── Bloc Shop — 3 photos featured du moment
│   ├── Bloc WildLens — 3 derniers articles (pull Ghost API)
│   ├── Bloc L'Instant Lu — CTA fort "Faites analyser votre photo"
│   └── Bloc Artistes — présentation affiliation
│
├── /manifeste
│   └── Texte long + photo JCH + signature "Même tissu."
│
├── /artistes/
│   ├── / — Index — grille portraits + noms
│   └── /[slug-artiste] — Fiche artiste
│       ├── Portrait + biographie naturaliste
│       ├── Galerie photos (liées au shop)
│       ├── Déclaration éthique prise de vue
│       └── CTA — Voir les tirages disponibles
│
├── /shop/
│   ├── / — Catalogue
│   │   ├── Filtres : espèce · biotope · artiste · format · prix
│   │   └── Grille photos — vignette + titre + prix + "Voir la fiche"
│   └── /[slug-photo] — Fiche photo augmentée
│       ├── Photo haute résolution
│       ├── Fiche naturaliste (espèce, comportement, contexte écologique)
│       ├── Déclaration éthique de prise de vue
│       ├── Formats et prix (WhiteWall)
│       ├── Artiste (lien fiche)
│       └── CTA achat
│
├── /wildlens — Vitrine légère
│   ├── 3 derniers articles (titre + image + extrait)
│   ├── CTA "Lire WildLens" → wildlens.arteon.be
│   └── CTA "S'abonner à la newsletter"
│
├── /critique — L'Instant Lu
│   ├── / — Landing page service
│   │   ├── Hero — "Votre photo lue par un expert IA"
│   │   ├── Comment ça marche (3 étapes)
│   │   ├── Exemples de rapports (anonymisés — photos JCH)
│   │   ├── Tarifs (€1,90 · pack 5 · pack 10 · B2B)
│   │   └── CTA "Analyser une photo — 1ère gratuite"
│   ├── /analyser — Interface upload + paiement
│   ├── /compte — Historique analyses utilisateur
│   └── /exemples — 3-5 rapports demo complets
│
├── /affiliation
│   ├── Critères éthiques publics
│   ├── Modèle commercial (commission, exclusivité par œuvre)
│   ├── Registre du curateur (qui a validé quoi)
│   └── Formulaire de candidature
│
└── /legal
    ├── CGV (shop + L'Instant Lu séparés)
    ├── Mentions légales
    ├── RGPD + politique données
    └── Éthique prise de vue (référence complète)
```

### 1.3 Navigation principale

```
┌─────────────────────────────────────────────────────────────────┐
│  [Logo Arteon]  Manifeste  Artistes  Shop  WildLens  ▶ L'Instant Lu  FR·EN·IT  │
└─────────────────────────────────────────────────────────────────┘
```

- **L'Instant Lu** : traitement visuel distinct — fond ocre, texte blanc — pour signaler le service payant
- **Mobile** : L'Instant Lu remonte en 1ère position dans le menu hamburger
- **Langues** : switcher discret en haut à droite (FR actif au lancement, EN + IT à venir)

---

## 2. Charte graphique — ARTEON (marque mère)

### 2.1 Palette de couleurs

| Rôle | Nom | Hex | Usage |
|------|-----|-----|-------|
| Primaire | Noir Terrain | `#0D0B09` | Titres, texte principal, fond sombre |
| Secondaire | Ivoire | `#F8F5F0` | Fonds clairs, espaces blancs |
| Accent | Ocre Lumière | `#C17F3A` | CTAs, liens actifs, soulignements, badges |
| Neutre chaud | Sable | `#E8E2DA` | Fonds secondaires, séparateurs |
| Neutre foncé | Gris Terrain | `#6B6560` | Texte secondaire, captions, métadonnées |
| Profond | Brun Nuit | `#2A2420` | Fonds footer, zones sombres |

**Règle d'or** : les photos portent la couleur — le site ne leur fait jamais concurrence. Blancs généreux, respiration maximale autour des images.

### 2.2 Typographie

| Rôle | Famille | Style | Source |
|------|---------|-------|--------|
| Titres & navigation | **Space Grotesk** | Bold / SemiBold | Google Fonts (gratuit) |
| Corps de texte | **[[LoRa]]** | Regular / Italic | Google Fonts (gratuit) |
| Données & scores | **IBM Plex Mono** | Regular / Medium | Google Fonts (gratuit) |

**Rationale :**
- Space Grotesk : géométrique, rappelle les découpes du logo, moderne sans être techno
- [[LoRa]] : serif élégant à l'italique expressif — ton éditorial, scientifique, Despret/Tesson
- IBM Plex Mono : pour les scores `/20`, températures Kelvin, paramètres LR dans L'Instant Lu

**Hiérarchie typographique :**

```
H1 — Space Grotesk Bold 48–64px    — titre de page
H2 — Space Grotesk SemiBold 32px   — section
H3 — Space Grotesk Medium 22px     — sous-section
Body — Lora Regular 17px / 1.7 line-height — texte long
Caption — Space Grotesk Regular 13px — métadonnées, labels
Data — IBM Plex Mono 15px          — scores, paramètres
```

### 2.3 Logo — règles d'usage

**Direction retenue — ✓ DÉCIDÉ 2026-05-02 : Direction D "La juste discrétion"**

```
Arteon·
```

- Wordmark `Arteon` en Space Grotesk weight **300** (fin), letter-spacing +2px
- Point médian ocre `·` `#C17F3A` — seul élément coloré du logo
- Cohérence avec "L'Instant Lu·" (même point médian comme signature de marque)

**Règles d'usage :**
- Logo en `#0D0B09` sur fond clair, en `#F8F5F0` sur fond sombre
- Le point médian reste toujours ocre `#C17F3A` — dans les deux versions
- Jamais en gras — le weight 300 est constitutif du caractère du logo
- Zone de protection = hauteur du caractère autour du logo
- Taille minimum : 100px de large (web), 25mm (print)

**Favicon / app icon :**
- Lettre `A` seule, Space Grotesk Bold, sur fond `#0D0B09`
- Le point ocre en bas à droite du carré favicon

**Livrable [[Vega]] :** finaliser en SVG vectoriel propre (Illustrator ou Figma) — les rendus actuels sont CSS/SVG de référence uniquement.

### 2.4 Composants UI

**Boutons :**
```
Primaire  : fond Ocre #C17F3A · texte blanc · Space Grotesk SemiBold · 0 border-radius (carré net)
Secondaire: fond transparent · bordure #0D0B09 1px · texte #0D0B09
Ghost     : texte Ocre #C17F3A · underline fin · pas de fond ni bordure
```

**Cartes photo :**
- Pas de border-radius — format galerie, net
- Pas de shadow — la photo se suffit
- Hover : légère opacité + apparition titre en overlay bas

**Séparateurs :**
- Ligne fine `#E8E2DA` 1px — jamais de fond de section coloré fort
- Espacement généreux : `padding-top: 80px` entre sections

---

## 3. Charte spécifique — [[WildLens]]

> [[WildLens]] partage la base ARTEON mais a sa propre personnalité : terrain, immersion, journal de naturaliste.

### 3.1 Couleur accent [[WildLens]]

| Rôle | Nom | Hex |
|------|-----|-----|
| Accent [[WildLens]] | Vert Terrain | `#3D5A3E` |

Utilisé sur : masthead Ghost, tags, liens actifs, bordure newsletter.

### 3.2 Typographie [[WildLens]]

Identique à ARTEON + un usage plus fort de **[[LoRa]] Italic** pour les chapeaux d'articles et citations de terrain — ça renforce le ton carnet de terrain.

### 3.3 Structure Ghost (wildlens.arteon.be)

```
wildlens.arteon.be/
├── / — Page d'accueil — derniers articles + featured
├── /tag/[espece] — Articles par espèce
├── /tag/technique — Technique photo
├── /tag/ethique — Éthique naturaliste
├── /[slug-article] — Article complet
└── /newsletter — Page d'abonnement
```

**Header Ghost personnalisé :**
```
[Logo WildLens — "W" stylisé vert terrain] WILDLENS by ARTEON     S'abonner
```

Le lien "by ARTEON" renvoie vers arteon.be — pont permanent entre les deux univers.

### 3.4 Ce que [[WildLens]] n'est pas

- Pas un blog généraliste — chaque article a une espèce ou un comportement central identifié
- Pas de contenu promotionnel pur — L'Instant Lu peut être mentionné dans un article technique, jamais en bannière
- Pas de publicité tierce

---

## 4. Charte spécifique — L'Instant Lu

> L'Instant Lu est le service expert. Ton : précis, bienveillant, professionnel. Pas une galerie — un outil.

### 4.1 Couleur accent L'Instant Lu

| Rôle | Nom | Hex |
|------|-----|-----|
| Accent service | Ardoise | `#4A5568` |
| Accent données | Ocre (hérité ARTEON) | `#C17F3A` |

L'ardoise signale la rigueur technique. L'ocre reste présent pour les CTAs — cohérence marque mère.

### 4.2 Logotype L'Instant Lu

Le nom seul en Space Grotesk, avec un traitement typographique :

```
L'Instant Lu·
```

Le point médian `·` après "Lu" évoque la fin de lecture, le point de pause — discret, distinctif.  
À tester aussi : une fine ligne de soulignement animée sous "Lu" (suggère la lecture en cours).

### 4.3 Structure landing page `/critique`

```
┌─────────────────────────────────────────────────────┐
│  HERO                                                │
│  "Votre photo wildlife, lue par un expert IA"        │
│  Sous-titre : rapport PDF + preset Lightroom en 30s  │
│  [Analyser ma photo — 1ère gratuite]                 │
├─────────────────────────────────────────────────────┤
│  3 ÉTAPES (icônes simples)                           │
│  1. Uploadez  2. Recevez le rapport  3. Retouchez    │
├─────────────────────────────────────────────────────┤
│  EXEMPLE DE RAPPORT (extrait visuel)                 │
│  Scores sur 5 axes · Analyse chromatique · Preset    │
├─────────────────────────────────────────────────────┤
│  TARIFS                                              │
│  1 analyse gratuite · €1,90 · Pack 5 · Pack 10 · B2B│
├─────────────────────────────────────────────────────┤
│  ÉTHIQUE                                             │
│  "Nous n'analysons que des photos conformes aux      │
│   valeurs ARTEON — voir nos critères"                │
├─────────────────────────────────────────────────────┤
│  ANCRAGE ARTEON                                      │
│  "L'Instant Lu est un service ARTEON — lire le       │
│   manifeste pour comprendre pourquoi"                │
└─────────────────────────────────────────────────────┘
```

### 4.4 Rapport PDF — charte visuelle

- En-tête : Logo L'Instant Lu · "by ARTEON" · date
- Fond : Ivoire `#F8F5F0` — imprimable, jamais de fond noir en PDF
- Scores : barres en Ocre `#C17F3A` + valeur IBM Plex Mono
- Sections : titrées en Space Grotesk Bold + séparateur fin
- Photo miniature : pleine largeur en haut, avec légende espèce + fiche technique
- Pied de page : `arteon.be · L'Instant Lu · "L'instant figé, la pensée en mouvement."`

### 4.5 Badge "Vérifié L'Instant Lu" (B2B éditeurs)

```
┌──────────────────────┐
│  ✦ VÉRIFIÉ           │
│  L'Instant Lu        │
│  by ARTEON           │
│  [date analyse]      │
└──────────────────────┘
```

- Format : carré 120×120px, fond Ardoise `#4A5568`, texte blanc
- Variante SVG embed pour sites partenaires
- Lien cliquable vers la charte éthique ARTEON

---

## 5. Parcours utilisateurs clés

### 5.1 Thomas — le photographe amateur (cœur de cible)

```
Google "critique photo wildlife IA"
    → Landing /critique
        → Lit les exemples de rapports
            → Upload 1 photo gratuite
                → Reçoit rapport PDF + preset XMP
                    → Revient payer € 1,90 pour la suivante
                        → Découvre WildLens via footer
                            → S'abonne newsletter
```

### 5.2 Collectionneur — achat tirage

```
Instagram / Pinterest → arteon.be (home)
    → /shop (filtre : espèce = rapace · format = 60×90)
        → Fiche photo augmentée
            → Lit déclaration éthique
                → Commande tirage WhiteWall
```

### 5.3 Lecteur [[WildLens]]

```
Partage article Ghost (email · réseau)
    → wildlens.arteon.be/[article]
        → Lit → s'abonne newsletter
            → Clic "by ARTEON" → arteon.be
                → Découvre L'Instant Lu → essaie
```

### 5.4 Artiste affilié

```
Mention WILDLENS ou bouche-à-oreille
    → /affiliation
        → Lit critères + modèle commercial
            → Envoie formulaire
                → Jury → Accepté → Fiche artiste créée
```

---

## 6. Déclinaison responsive

| Breakpoint | Adaptation |
|-----------|-----------|
| Desktop ≥1280px | Navigation horizontale complète · grille photos 3 colonnes |
| Tablet 768–1279px | Navigation horizontale · grille 2 colonnes |
| Mobile <768px | Menu hamburger · L'Instant Lu en 1er · grille 1 colonne · photos pleine largeur |

**Sur mobile — priorité L'Instant Lu :**
Menu hamburger ouvert :
```
▶ L'Instant Lu   ← 1er, fond ocre
Manifeste
Artistes
Shop
WildLens
───────
FR · EN · IT
```

---

## 7. Famille de marques — synthèse visuelle

| | ARTEON | [[WildLens]] | L'Instant Lu |
|--|--------|----------|--------------|
| **Accent** | Ocre `#C17F3A` | Vert Terrain `#3D5A3E` | Ardoise `#4A5568` |
| **Ton** | Galerie · éditorial | Terrain · journal | Outil · expertise |
| **Typo titre** | Space Grotesk | Space Grotesk | Space Grotesk |
| **Typo corps** | [[LoRa]] | [[LoRa]] Italic ++ | [[LoRa]] + IBM Mono |
| **Forme** | Carré net | Organique | Structuré |
| **Photo** | Contemplative | Documentaire | Technique (analyse) |

**Ce qui ne change jamais :** fond Ivoire / Noir Terrain, Space Grotesk, slogan ARTEON en ancrage.

---

## 8. Prochaines étapes [[Vega]]

| # | Livrable | Format | Priorité |
|---|---------|--------|----------|
| V1 | Palette + typographie — fichier Figma ou PDF couleurs | Figma / PDF | Immédiate |
| V2 | Maquette wireframe home arteon.be | HTML | ✅ Validé JCH 2026-05-02 |
| V3 | Maquette landing L'Instant Lu `/critique` | Figma | S1 |
| V4 | Header Ghost [[WildLens]] | Figma + HTML | S2 |
| V5 | Rapport PDF L'Instant Lu — template final | reportlab / Figma | S2 |
| V6 | Badge "Vérifié L'Instant Lu" SVG | SVG | S2 |
| V7 | Variantes logo (si propositions alternatives) | Figma | S3 |

---

## 9. Ce que ce document ne décide pas encore

- Police définitive si [[Vega]] propose une alternative à Space Grotesk / [[LoRa]]
- Logo final (le current est solide, des variantes restent ouvertes)
- Contenu exact des pages (relève du copywriting — [[Miel]] + JCH)
- Animations et micro-interactions (hors scope charte — phase développement)

---

*Document établi le 2026-05-02 — [[Vega]] 🦚 · [[Dobby]] 🦉*  
*Charte validée par JCH le 2026-05-02 — "harmonieuse, calme" ✓*  
*Prochaine étape : wireframes home + L'Instant Lu landing*
