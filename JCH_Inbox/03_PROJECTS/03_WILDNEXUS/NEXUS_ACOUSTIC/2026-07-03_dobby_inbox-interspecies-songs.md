# Inbox Processing — INTERSPECIES SONGS
> **Date :** 2026-07-03
> **Dobby 🦉** — traitement inbox `00_INBOX/INTERSPECIES SONGS/`
> **Routage :** `NEXUS_ACOUSTIC/99_REFERENCES/interspecies-songs/`
> **Spécialistes mandatés :** Clio 🦢 (analyse scientifique), Musaraigne 🐭 (Edge AI / TinyML), Miel 🐝 (potentialité artistique ARTEON)

---

## Fichiers traités

| # | Fichier source | Destination | Lignes | Type |
|---|---------------|-------------|--------|------|
| 1 | `INTERSPECIES SONGS.md` | `interspecies-songs/INTERSPECIES-SONGS_dolphingemma-bioacoustique.md` | 628 | Transcript ChatGPT |
| 2 | `Lucio Arese inspiration.md` | `interspecies-songs/lucio-arese-3d-birdsong-visualisation.md` | 262 | Transcript ChatGPT |

---

## Fichier 1 — INTERSPECIES SONGS.md

### Thèmes couverts

**A. DolphinGemma → fork oiseaux**
- Google a publié DolphinGemma comme modèle **open-weights** (basé sur Gemma) pour décoder la communication des dauphins
- L'architecture transformer est **species-agnostic** — le moteur de prédiction peut être adapté à d'autres espèces
- 2 adaptations nécessaires pour les oiseaux :
  1. **Swap de l'audio tokenizer** — les tokenizers dauphin (sifflements/clics) ne conviennent pas pour les oiseaux (fréquences, syntaxe complexe, pitch)
  2. **Fine-tuning sur données aviaires** — striper les poids dolphin, entraîner sur librairies bioacoustiques (Xeno-Canto, Macaulay)
- Défis spécifiques oiseaux : bruit environnemental (vent, feuilles, insectes, espèces concurrentes), contexte multimodal (parades, gestes, territoire)

**B. Projets existants**
- **Earth Species Project (ESP)** — non-profit dédié au décodage du langage non-humain via ML self-supervised (corbeaux, baleines, oiseaux chanteurs)
- **Merlin Bird ID (Cornell)** — identification acoustique temps réel, datasets de référence

**C. Identité individuelle & règles de communication chez le rouge-gorge**
- *Erithacus rubecula* (European Robin) : ~1 300 fragments sonores par individu — signature unique
- Syntaxe hautement structurée — signale identité, territoire, contexte environnemental
- Pas du "bruit aléatoire" comme l'oreille humaine le perçoit
- Outils mentionnés : TweetyBERT (transformer pour segmentation syntaxique birdsong), t-SNE pour visualisation des clusters individuels

**D. TweetyBERT**
- Modèle transformer spécialisé birdsong syntax analysis
- Pipeline : spectrogramme → embeddings → t-SNE → clusters par individu/phrase
- Permet de cartographier les "syllabes" et transitions de phrases

---

## Fichier 2 — Lucio Arese inspiration.md

### Thèmes couverts

**A. Lucio Arese — sculptures 3D génératives depuis birdsong**
- Artiste numérique qui convertit les features spectrogrammiques en **sculptures 3D génératives**
- European Robin explicitement feature dans son travail (timestamp 06:32)
- Concept de **"spatial visual score"** — visualiser la fréquence et l'évolution du chant

**B. Corrélation avec le pipeline TweetyBERT**
- TweetyBERT : embeddings 2D (t-SNE) → clusters syntaxiques
- Arese : mêmes features → réseau 3D de points → sculpture évolutive
- **Deux faces d'une même pièce** : analyse mathématique vs visualisation artistique

**C. Pipeline double export (science + art)**
- **Export scientifique (CSV)** : Segment_ID, File_XCID, Bird_Identity, Time_Chunk_Index, TSNE_1, TSNE_2 → pour R/Pandas/analyse transitionnelle
- **Export artistique (JSON)** : x, y, z (time×0.1), bird_signature, audio_source → pour TouchDesigner/Blender
- Code Python fourni (`run_dual_pipeline`) — combine les deux exports en un seul run

**D. Outils créatifs**
- **TouchDesigner** (outil d'Arese) — Script CHOP lit JSON, point clouds, particles
- **Blender** (Python-native) — mesh trails, sculptures 3D trackant l'évolution syntaxique

---

## Synthèse Dobby — Pertinence pour PKA

### Connexions avec projets actifs

| Projet | Connexion | Force |
|--------|-----------|-------|
| **NEXUS_ACOUSTIC** | DolphinGemma comme architecture de référence possible (post-InsectNet). TweetyBERT pour analyse syntaxique oiseaux. ESP comme ressource/dataset. | 🔴 Forte |
| **InsectNet** | Pattern tokenizer swap (dauphin→insectes au lieu de dauphin→oiseaux). Architecture double canal BirdNET déjà adoptée (décision 2026-06-23). | 🟡 Moyenne |
| **ARTEON** | Lucio Arese = inspiration esthétique pour visualisation sonore. Potentiel WildLens ou expo PHOTO_NATURE avec rendu 3D génératif. | 🟡 Moyenne |
| **WILDNEXUS** | ESP comme modèle organisationnel (non-profit, open-source, self-supervised). Pas de lien technique direct. | ⚪ Faible |

### Décisions / actions recommandées

1. **DolphinGemma** — ajouter à la veille NEXUS_ACOUSTIC comme architecture candidate P1 (post-WildNexus P0). Le pattern "open-weights transformer + tokenizer swap" est exactement la philosophie d'InsectNet/BirdNET déjà adoptée.
2. **TweetyBERT** — investiguer comme outil d'analyse syntaxique pour les oiseaux. Potential crossover avec InsectNet (syntax analysis des orthoptères).
3. **Earth Species Project** — contacter ou suivre comme ressource/inspiration. Leur approche self-supervised est alignée avec la philosophie PKA.
4. **Lucio Arese + TouchDesigner** — stocker comme référence esthétique pour ARTEON. Le pipeline dual-export (CSV science + JSON art) est un pattern élégant qui mérite d'être réutilisé.
5. **Code `run_dual_pipeline`** — code fourni mais non testé. À évaluer par Musaraigne pour qualité/faisabilité avant intégration.

### Vigilance

- ⚠️ Les transcripts viennent de ChatGPT — les affirmations biologiques (1 300 fragments, syntaxe structurée) doivent être vérifiées contre la littérature avant citation
- ⚠️ DolphinGemma est annoncé "open-weights" mais il faut vérifier la licence exacte (commercial vs recherche)
- ⚠️ TweetyBERT mentionné mais pas de lien GitHub/référence formelle dans le transcript — à rechercher

---

## Voir aussi

- [[NEXUS_ACOUSTIC]] — projet parent
- [[InsectNet]] — pipeline bioacoustique insectes
- [[BirdNET]] — architecture de référence déjà adoptée
- [[Lucio Arese]] — référence esthétique (déjà noté dans USER.md profil cognitif)
- [[ARTEON]] — potentiel crossover artistique
- [[Clio]] — analyse scientifique
- [[Musaraigne]] — Edge AI / TinyML
- [[Miel]] — potentiel artistique

---

*Traitement inbox Dobby 🦉 — 2026-07-03*
