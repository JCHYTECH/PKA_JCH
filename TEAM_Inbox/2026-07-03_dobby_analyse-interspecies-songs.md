# ANALYSE — INTERSPECIES SONGS.md
> Dobby 🦉 — DeepSeek TUI 0.8.39 — 2026-07-03
> Fichier source : `JCH_Inbox/00_INBOX/INTERSPECIES SONGS/INTERSPECIES SONGS.md` (627 lignes)
> Spécialistes mobilisés : Clio 🦉, Musaraigne 🦇, Chouette 🦉

---

## 1. Résumé exécutif

Le document INTERSPECIES SONGS.md est un guide technique complet de 627 lignes décrivant l'écosystème émergent du décodage de chants d'oiseaux par IA. Il couvre trois technologies clés — **DolphinGemma** (Google, modèle open-weights forkable), **TweetyBERT** (University of Oregon, avril 2026, transformer self-supervised), et l'**Earth Species Project** — avec un pipeline Python complet et exécutable (xcapi → spectrogrammes → TweetyBERT → clustering t-SNE → matrices de transition Markov).

**Découverte majeure validée par le web** : TweetyBERT est publié dans *Patterns* (Cell Press, avril 2026), open-source sur GitHub/Zenodo, et **InsectSet459** (Nature Scientific Data, 2026) fournit 26 298 fichiers audio de 459 espèces d'orthoptères et cigales — le dataset idéal pour un fine-tuning PKA.

**Verdict** : TweetyBERT est la découverte la plus actionnable pour PKA depuis BirdNET (analysé le 23 juin). Son approche self-supervised sans labels humains est directement applicable aux orthoptères. Notre pipeline InsectNet existant (xcapi, metadata, segmentation) constitue déjà ~60% du chemin préparatoire.

---

## 2. Analyse détaillée du document

### 2.1 DolphinGemma — Google DeepMind (lignes 4–31)

- **Nature** : Modèle open-weights audio→audio, architecture transformer. Google l'a conçu explicitement pour être forkable.
- **Adaptation oiseaux** : Nécessite un nouveau tokenizer audio optimisé pour les fréquences aviaires (2–8 kHz) et la syntaxe complexe des chants. Le moteur transformer sous-jacent est « species-agnostic ».
- **Défis biologiques** : Bruit environnemental (vent, feuilles, insectes, oiseaux concurrents) et multimodalité (les oiseaux utilisent aussi le contexte visuel : danses, postures, territoire).
- **État PKA** : Pertinent à horizon 2028+. Trop lourd pour nos jalons V0.1–V0.2 immédiats (Clio confirme).

### 2.2 TweetyBERT — University of Oregon (lignes 32–200, 213–618)

- **Publication** : *Patterns* (Cell Press), avril 2026. DOI: 10.1016/j.patter.2025.100339.
- **Architecture** : Transformer self-supervised. Résolution temporelle 2.7 ms — un ordre de grandeur supérieur aux modèles de speech humain. Apprend directement depuis des spectrogrammes bruts, sans labels humains.
- **Performances** : Égal aux annotateurs experts sur des séquences de 30–40 syllabes de canaris. Segmentation automatique notes → syllabes → phrases.
- **Open-source** : GitHub `georgevenven/tweety_bert` + Zenodo (DOI: 10.5281/zenodo.15391040).
- **Pipeline documenté** (code Python complet dans le fichier) :
  1. `xcapi` → téléchargement filtré (q:A, type:song, len_gt:30)
  2. `librosa` → spectrogrammes Mel (sr=32000, n_mels=128, fmin=2000, fmax=8000)
  3. `TweetyBERT` → extraction d'embeddings (hidden states)
  4. `t-SNE/UMAP` → clustering 2D, coloration par individu/phrase
  5. `K-Means + Markov` → matrices de transition syntaxique par individu

### 2.3 Earth Species Project & Merlin Bird ID (lignes 23–27, 101–118)

- **ESP** : Nouveau CEO Steven VanRoekel (2026). Modèle généralisable multi-espèces. Déploiement conservation prévu 2028.
- **Merlin Bird ID** : Cornell Lab, 6000+ espèces, identification acoustique temps réel. Dataset fondamental pour entraîner des modèles génératifs.
- **Xeno-canto** : Archive bioacoustique mondiale. API `xcapi` utilisable immédiatement par PKA (déjà intégré dans InsectNet).

---

## 3. Validation web — DuckDuckGo

| Source | Finding clé |
|--------|------------|
| **Patterns (Cell Press)** | TweetyBERT publié avril 2026, peer-reviewed. Self-supervised, résolution 2.7ms, zéro label humain. |
| **GitHub georgevenven/tweety_bert** | Code source complet, scripts de pretraining, UMAP, decoder. MIT license probable. |
| **Zenodo** | DOI 10.5281/zenodo.15391040 — modèle + package logiciel reproductible. |
| **InsectSet459 (Nature Scientific Data, 2026)** | **26 298 fichiers, 226.6h, 459 espèces** (310 Orthoptera + 149 Cicadidae) depuis xeno-canto + iNaturalist. Dataset public sur Zenodo. C'est le dataset idéal pour fine-tuner TweetyBERT sur insectes. |
| **arXiv 2508.01277** | Revue comparative des foundation models bioacoustiques. BioLingual et NatureLM-audio = modèles audio-langage multimodaux. |
| **BirdCLEF 2026** | BirdNET embeddings + ML = 0.894 macro ROC-AUC. BirdNET reste le standard classification. |

---

## 4. Analyses des spécialistes

### 4.1 Clio 🦉 — Analyse scientifique

**Pertinence pour PKA** : Très élevée. TweetyBERT est directement applicable à InsectNet et NEXUS_ACOUSTIC.

**TweetyBERT vs BirdNET** :

| Critère | BirdNET | TweetyBERT |
|---------|---------|-------------|
| Objectif | Classification d'espèces (6000+) | Parsing de structure (syllabes, phrases) |
| Supervision | Supervisé (labels d'espèces) | Self-supervised (zéro label) |
| Résolution | ~25ms (fenêtre standard) | 2.7ms (ordre de grandeur supérieur) |
| Sortie | Espèce + confiance | Embeddings, clusters, syntaxe |
| Edge | BirdNET-Lite (18MB, RPi OK) | Transformer (~50-200MB, GPU recommandé) |
| Usage PKA | Identification terrain | Recherche, découverte de patterns |

**Complémentarité** : BirdNET pour l'identification terrain (edge), TweetyBERT pour la recherche (M5). Les deux se complètent, ne se remplacent pas.

**Adaptation aux orthoptères** :
- Modifier le tokenizer : `fmin=5000, fmax=25000` (les orthoptères chantent plus haut, jusqu'à l'ultrasonique)
- Garder `sr=32000` ou monter à `sr=48000` pour les espèces >16 kHz (Nyquist)
- Le pipeline preprocessing (librosa, Mel, segmentation) est identique — seul le range change
- InsectSet459 (26K fichiers) est le dataset parfait pour le fine-tuning

**3 recommandations Clio** :
1. **P0** : Télécharger InsectSet459 et exécuter le pipeline TweetyBERT complet dessus (benchmark baseline)
2. **P1** : Fine-tuner TweetyBERT sur les 6 espèces prioritaires d'orthoptères européens (données xeno-canto filtrées)
3. **P2** : Comparer les embeddings TweetyBERT vs BirdNET sur le même dataset — publier un benchmark PKA

### 4.2 Musaraigne 🦇 — Faisabilité Edge / TinyML

**TweetyBERT sur RPi 5** : ❌ NON VIABLE. Transformer trop lourd (~50-200MB), 4GB RAM insuffisant. Inférence CPU-only → plusieurs secondes par segment.

**TweetyBERT sur M1 (32GB)** : ⚠️ Faible en batch. CPU-only, mais 32GB RAM permet de charger le modèle. Inférence lente (minutes par batch) mais fonctionnelle pour du traitement overnight.

**TweetyBERT sur M5** : ✅ IDÉAL. Apple Silicon GPU (Metal via MPS) — supporté dans PyTorch depuis 2024. Temps d'inférence raisonnable (<1s par segment).

**ESP32-S3 (WildNexus P0)** : ❌ Pas de transformer. Le parsing de syllabes sur microcontrôleur est hors de portée. Alternatives :
- **FOMO (Edge Impulse)** : Classification simple (espèce présente/absente) en <100KB, ~50ms inférence
- **Détection d'activité vocale** (VAD) : Seuil d'énergie sur bande fréquentielle — déclenche l'enregistrement
- **Rôle ESP32** : Edge léger = détection + enregistrement → envoi au backend M5

**Architecture recommandée** :

```
[Terrain] ESP32-S3 + micro MEMS → VAD + enregistrement buffer 30s
         │
         │ Wi-Fi / LoRa (fichiers WAV segmentés)
         ▼
[Edge] RPi 5 → BirdNET-Lite (classification temps réel)
         │
         │ Sync nightly (Tailscale)
         ▼
[Backend] M5 → TweetyBERT (parsing + clustering)
         │
         ▼
[Dashboard] → Clusters t-SNE, matrices Markov
```

**Ressources estimées** :
- **Stockage par enregistrement** : ~2 MB (WAV 32kHz, 16-bit, mono, 30s)
- **Stockage dataset 1000 segments** : ~2 GB
- **RAM inférence TweetyBERT** : ~500 MB (modèle + activations)
- **Latence M5 par segment** : <1s (GPU MPS)
- **Latence M1 par segment** : 3-5s (CPU-only)

**3 recommandations Musaraigne** :
1. **P0** : Installer TweetyBERT sur M5, benchmarker l'inférence sur InsectSet459 (10 segments test)
2. **P1** : Développer un firmware VAD pour ESP32-S3 (détection énergie bande 5-15 kHz + enregistrement buffer)
3. **P2** : Évaluer quantisation INT8 de TweetyBERT pour le RPi 5 (via ONNX Runtime ou llama.cpp-style) — exploration long terme

### 4.3 Chouette 🦉 — Dashboard & Visualisation

**Design proposé — Dashboard NEXUS_ACOUSTIC v2.0** :

```
┌──────────────────────────────────────────────────┐
│  NEXUS_ACOUSTIC — TweetyBERT Explorer            │
├──────────────────┬───────────────────────────────┤
│  t-SNE Map 2D    │  Spectrogramme + Clusters     │
│  (coloré par     │  (segment sélectionné)         │
│   individu)      │                                │
│                  │  ┌─────────────────────────┐   │
│     •  • •       │  │ Matrice de transition   │   │
│   •  ◉  •       │  │ Markov (heatmap 5×5)    │   │
│     •  •         │  └─────────────────────────┘   │
│                  │                                │
├──────────────────┴───────────────────────────────┤
│  Timeline des sessions | Filtres (espèce, date)  │
└──────────────────────────────────────────────────┘
```

**Stack technique** :
- **Frontend** : React + D3.js (t-SNE interactif) + Plotly (spectrogrammes)
- **Backend** : FastAPI Python (existante dans NEXUS_ACOUSTIC)
- **Base** : PostgreSQL (déjà prévue dans le projet) — table `embeddings`, `clusters`, `transitions`
- **Intégration HA** : Carte custom Lovelace pour afficher les métriques clés (# segments, espèces détectées/jour)

**Flux de données** :
```
Edge (RPi + BirdNET) → WAV + metadata JSON → NAS M5
                                              │
M5 (TweetyBERT cron nightly) → embeddings CSV → PostgreSQL
                                              │
Dashboard (FastAPI) → JSON API → React frontend
```

**Roadmap dashboard (3 phases)** :
- **Phase 1 — MVP (juillet 2026)** : API FastAPI qui lit les CSV d'embeddings et retourne JSON. Page HTML simple avec scatter plot t-SNE statique.
- **Phase 2 — Interactif (août 2026)** : PostgreSQL live, React + Plotly, sélection de segments → spectrogramme, filtres par espèce/date.
- **Phase 3 — Production (septembre 2026)** : Export TouchDesigner 3D, carte custom Home Assistant, alertes (nouveau cluster = notification).

**3 recommandations Chouette** :
1. **P0** : Générer un premier t-SNE plot depuis un notebook Jupyter (validation visuelle du pipeline)
2. **P1** : Déployer l'API FastAPI `/api/embeddings/{run_id}` avec le format JSON standardisé
3. **P2** : Connecter le dashboard à Home Assistant via une carte custom (métriques journalières)

---

## 5. Points d'intérêt par projet PKA

### 5.1 InsectNet — IMPACT MAJEUR 🔴

| Point | Intérêt |
|-------|---------|
| **InsectSet459** | Dataset 26K fichiers, 310 espèces Orthoptera — prêt à l'emploi sur Zenodo. C'est LE dataset qu'on cherchait depuis juin. |
| **TweetyBERT pipeline** | 60% déjà fait : xcapi intégré, segmentation en place, metadata. Gap : spectrogrammes Mel adaptés (fmin/fmax) + modèle. |
| **Parsing self-supervised** | Plus besoin de labelliser manuellement les syllabes d'orthoptères. TweetyBERT découvre les patterns automatiquement. |
| **Matrices Markov** | Permet de comparer la syntaxe des chants entre espèces proches (ex. Chorthippus parallelus vs C. dorsatus). |

### 5.2 NEXUS_ACOUSTIC — IMPACT ÉLEVÉ 🟡

| Point | Intérêt |
|-------|---------|
| **Pipeline multi-taxons** | TweetyBERT + BirdNET = stack complète : BirdNET identifie l'espèce, TweetyBERT analyse la structure du chant. |
| **Dashboard enrichi** | t-SNE interactif + spectrogrammes clusterisés + matrices de transition → outil d'exploration scientifique. |
| **Architecture distribuée** | Edge léger (RPi + BirdNET-Lite) → backend lourd (M5 + TweetyBERT). Pattern validé par Musaraigne. |

### 5.3 WildNexus — IMPACT MODÉRÉ 🟢

| Point | Intérêt |
|-------|---------|
| **Multimodalité future** | Le document souligne que la communication animale nécessite audio + vidéo. WildNexus est caméra + micro — positionné pour du multimodal à terme. |
| **VAD firmware ESP32** | La détection d'activité vocale sur ESP32-S3 (proposée par Musaraigne) est un module réutilisable pour un futur nœud audio WN. |
| **DolphinGemma horizon 2028** | Si WildNexus évolue vers l'audio, le modèle open-weights de Google est une cible long terme. |

### 5.4 IOT Van / Serre — IMPACT LÉGER ⚪

| Point | Intérêt |
|-------|---------|
| **Monitoring bioacoustique passif** | RPi 5 vanlife pourrait faire tourner BirdNET-Lite en background, logger les espèces détectées → dashboard HA. |
| **VAD + enregistrement** | ESP32 + micro = sentinelle acoustique low-power pour la serre (détection d'insectes ravageurs ?). |

### 5.5 AI_IT_TOOLS — IMPACT LÉGER ⚪

| Point | Intérêt |
|-------|---------|
| **Pipeline reproductible** | Le document fournit un template de pipeline ML complet. Forge peut le généraliser en skill PKA « bioacoustics-pipeline ». |

---

## 6. Propositions d'intégration priorisées

### 🔴 P0 — Actions immédiates (juillet 2026)

1. **Télécharger InsectSet459** depuis Zenodo → `NEXUS_ACOUSTIC/datasets/InsectSet459/`
2. **Installer TweetyBERT sur M5** → benchmark baseline sur 100 segments test (temps, RAM, qualité clusters)
3. **Adapter le preprocessing** : `fmin=5000, fmax=25000` pour orthoptères → notebook Jupyter de validation
4. **Générer premier t-SNE plot** → validation visuelle que les clusters sont biologiquement pertinents

### 🟡 P1 — Court terme (août 2026)

5. **Fine-tuner TweetyBERT** sur 6 espèces prioritaires (données xeno-canto filtrées, q:A)
6. **Développer firmware VAD** pour ESP32-S3 (détection 5-15 kHz) — Musaraigne + Araignée
7. **Déployer API FastAPI** `/api/embeddings` — Forge
8. **Dashboard MVP** : scatter plot t-SNE statique + matrices Markov — Chouette

### ⚪ P2 — Moyen terme (septembre+ 2026)

9. **Benchmark BirdNET vs TweetyBERT** sur même dataset orthoptères → publication blog PKA
10. **Dashboard interactif** : React + D3.js + PostgreSQL — Chouette + Forge
11. **Quantization INT8** exploration pour RPi 5 — Musaraigne
12. **Veille DolphinGemma** : suivre les forks oiseaux/insectes, évaluer maturité pour 2027

---

## 7. Prochaines actions

| Action | Responsable | Deadline |
|--------|-------------|----------|
| Télécharger InsectSet459 sur M5 | Dobby | Immédiat |
| Installer TweetyBERT + benchmark | Forge | 7 juillet |
| Notebook validation preprocessing | Clio | 10 juillet |
| Premier t-SNE plot orthoptères | Clio + Chouette | 14 juillet |
| Brief firmware VAD ESP32-S3 | Musaraigne | 14 juillet |

---

## 8. Note — Lien avec le fichier Lucio Arese

Le second fichier de l'INBOX (`Lucio Arese inspiration.md`) sera analysé séparément. Il porte sur la visualisation 3D des résultats du pipeline (TouchDesigner, « spatial visual score ») et constitue la couche présentation du pipeline analysé ici. Les deux fichiers sont complémentaires : INTERSPECIES SONGS = le moteur d'analyse, Lucio Arese = la couche de visualisation.

---

*Analyse produite par Dobby 🦉 avec les contributions de Clio (science), Musaraigne (edge/TinyML), Chouette (dashboard). Validation web DuckDuckGo : 9 recherches, 12 sources croisées.*
