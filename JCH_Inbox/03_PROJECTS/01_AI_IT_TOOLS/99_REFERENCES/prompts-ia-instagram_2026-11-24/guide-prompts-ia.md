---
date: 2026-11-24
source: dobby
domain: ai-it-tools
project: AI_IT_TOOLS
status: guide
type: reference
lang: fr
tags:
  - prompting
  - ia
  - instagram
  - e-commerce
  - templates-prompts
---

# Guide — Conseils de prompting IA (extraits de 12 screenshots Instagram)

> **Provenance** : 12 screenshots Instagram déposés dans `00_INBOX/` (compte `iknowig` + un carrousel
> « lancer un business avec l'IA » en 10 étapes). Pipeline : OCR (tesseract) → synthèse `qwen2.5:32b`
> sur le **M1** → curation/amélioration Dobby (24/11).
>
> **Ce que c'est** : une base de **templates de prompts réutilisables** + les **patterns** qui les rendent
> efficaces. À adapter, pas à recopier aveuglément.

---

## Partie 1 — Les 7 techniques de prompt (patterns universels)

Tous les prompts efficaces des screenshots reposent sur les mêmes briques. Maîtrise-les, et tu écris
tes propres prompts sans avoir besoin des templates.

1. **Persona — « Act as… »** : donne à l'IA un rôle précis + une expertise + un biais.
   *Ex. « Act as a retention editor who watches content with a stopwatch… »*
   Le rôle oriente la réponse (un growth analyst ne répond pas comme un copywriter).

2. **Audit / diagnostic** : demande d'identifier les angles morts, pas de valider.
   *Ex. « …identify the three patterns that are making me invisible »* — l'IA doit pointer, pas flatter.

3. **Pre-mortem / contre-argument** : demande explicitement ce qui peut échouer.
   *Ex. « Argue why the business could fail », « What assumptions in this forecast are unrealistic? »*
   Contre le biais de complaisance de l'IA.

4. **Multi-versions** : force N variantes avec des angles distincts.
   *Ex. « write 12 opening lines across four modes » (tension / contre-intuitif / feeling exact / boucle ouverte).*
   Le nombre + les angles cassent la réponse « passe-partout ».

5. **Format de sortie explicite** : précise la forme exacte du résultat.
   *Ex. « a 7-slide carousel with exact on-screen text for every slide »* — sans ça, l'IA choisit sa propre forme.

6. **Contraintes ton + audience** : les slots `[insert]` (audience, tone, brand voice) ne sont pas optionnels,
   ils cadrent le registre.

7. **Itération / réécriture** : « Flag every moment where… Then rewrite the full piece » — deux passes
   (diagnostic puis correction) valent mieux qu'une génération directe.

---

## Partie 2 — Les 4 piliers d'un bon prompt

Ce qui revient dans **tous** les prompts du corpus :

- **Rôle** : qui est l'IA (persona).
- **Contexte** : quoi analyser/créer (contenu, idée, chiffres, audience).
- **Contraintes** : format de sortie, nombre, ton.
- **Demande d'itération ou de jugement** : pointer, réécrire, contester — pas juste générer.

> Formule mémoire : **« Act as [rôle]. [Tâche précise]. [Contexte]. [Format + contraintes]. [Itération]. »**

---

## Partie 3 — Prompts à réutiliser tels quels

### A. Contenu Instagram (compte `iknowig`)

**Audit de stratégie**
> Act as an Instagram growth analyst who studies why accounts in the same niche grow at completely
> different rates. Audit my content strategy below and identify the three patterns that are making me
> invisible — not just saturated formats, but the specific ways my content fails to create a reason to
> follow rather than just like. Current content approach: [describe]. Audience: [insert].

**12 lignes d'ouverture (4 modes)**
> Act as a scroll-stopping copywriter who writes only for Instagram and understands that the first line is
> the only line that matters. For my content idea below, write 12 opening lines across four modes: one
> that creates immediate tension, one that makes a counterintuitive claim, one that names a specific
> person's exact feeling, and one that opens a loop the reader cannot close without finishing.
> Idea: [insert]. Audience: [insert]. Tone: [insert].

**Production sans visage (2 formats)**
> Act as a faceless content producer who has built three Instagram accounts past 100K without ever showing
> a face or using trending audio. Take my idea below and build it into two formats: a 7-slide carousel with
> exact on-screen text for every slide, and a text-only reel script with scene-by-scene direction.
> Idea: [insert]. Audience: [insert]. Visual style: [insert].

**Rétention (ligne par ligne)**
> Act as a retention editor who watches content with a stopwatch and cuts the moment attention drops. Go
> through my content below line by line. Flag every moment where a viewer would stop watching or swipe away
> and tell me exactly why. Then rewrite the full piece so each line creates enough tension to pull the next.
> Content: [paste]. Format: [reel/carousel/post]. Audience: [insert].

**Positionnement d'autorité (3 versions)**
> Act as a positioning strategist who makes creators look like the obvious authority in their space without
> a single vanity metric or guru signal. Rewrite my content below in three versions: the first builds
> authority through specificity and precision, the second through confident simplicity, the third through a
> point of view strong enough that disagreeing with it feels like a choice. Content: [paste]. Audience:
> [insert]. Current brand voice: [describe].

### B. Business / e-commerce (framework « 10 étapes »)

**Trouver l'idée**
> What problems in [industry] are customers currently paying to solve badly?

**Avantage compétitif**
> What unfair advantages could I build a business around? (donne ton background d'abord)

**Valider avant de dépenser**
> What would I need to prove before spending $10k on this idea?

**Pre-mortem**
> Ask Claude to identify your biggest assumptions, then argue why the business could fail.

**Positionnement vs concurrent**
> Why should someone buy from me instead of [competitor]?

**Brief produit**
> Turn this idea into a manufacturer-ready product brief.

**Copy orientée bénéfice**
> Rewrite this around customer benefits, not product features.

**Stress-test financier**
> What assumptions in this forecast are unrealistic?

**Plan de lancement**
> Build me a 30-day launch strategy with a $2k budget.

**Croissance**
> What are my highest-impact growth opportunities?

---

## Partie 4 — Ce que j'ai éliminé (transparence)

- **Bruit OCR** : timestamps iOS, compteurs likes/vues, éléments d'interface Instagram.
- **Doublons** : le prompt « faceless content producer » apparaissait coupé sur 2 screenshots (fusionné).
- **Les outils** (Canva AI, Shopify, Photoroom, Klaviyo, SimilarWeb…) sont une **liste d'outils**, pas du
  prompting — conservés dans les screenshots sources, exclus du guide.
- **Conseils triviaux** (« Get it live. Done beats perfect. ») : hors périmètre « mieux poser à l'IA ».

## Fichiers liés

- Screenshots sources : `screenshots/` (12 fichiers `IMG_*.jpeg`, ce dossier)
- OCR brut : `tmp/insta_prompts_raw/` (12 `.txt`, à la racine PKA)
- Synthèse M1 brute : `tmp/insta_conseils_brut.md` (à la racine PKA)

---

## Partie 5 — La brique réutilisable : `bin/pka-vision`

À l'issue de cette analyse, une brique d'**analyse d'image locale** a été créée pour réutiliser le pipeline :

- **`bin/pka-vision`** : CLI qui analyse une image (ou un dossier) via le vision model du M1
  (`qwen2.5vl:7b`), avec **fallback automatique OCR tesseract** si aucun modèle vision n'est disponible.
- Usage :
  - `bin/pka-vision IMG.jpeg` — vision (si dispo) sinon OCR
  - `bin/pka-vision --ocr IMG.jpeg` — forcer OCR
  - `bin/pka-vision --model qwen2.5vl:7b --prompt "..." IMG.jpeg`
  - `bin/pka-vision dossier/` — lot d'images
  - `bin/pka-vision --out tmp/out dossier/` — écrire les résultats en fichiers
- Serveur : Ollama du M1 via `http://127.0.0.1:11435` (tunnel SSH).
- ⚠️ `llama3.2-vision:11b` est **cassé** (architecture `mllama` non supportée par Ollama 0.40.16) ;
  `qwen2.5vl:7b` est le modèle vision de remplacement.
