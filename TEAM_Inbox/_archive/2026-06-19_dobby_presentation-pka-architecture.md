# PKA_JCH — Une architecture personnelle d'intelligence augmentée
> Présentation didactique — Juin 2026
> Par Jean-Claude Havaux & Dobby 🦉

---

## 2. L'architecture en trois couches

```
┌─────────────────────────────────────────────────────────┐
│                    JC (humain)                           │
│  Pose des questions, donne des caps, valide, arbitre    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 DOBBY 🦉 (orchestrateur)                 │
│  Point de contact unique. Interprète, route, synthétise │
│  Maintient la mémoire, détecte les patterns, propose   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           31 SPÉCIALISTES IA (l'équipe)                 │
│  Forge (code) · Nova (photo R&D) · Furet (recherche)   │
│  Corbeau (connaissances) · Sigma (finance) · Argus     │
│  (photo critique) · Chouette (terrain) · Araignée (IoT) │
│  Musaraigne (Edge AI) · … + 22 autres                  │
└─────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 INFRASTRUCTURE                           │
│  DeepSeek V4 · Claude · Qwen · Gemini · Ollama (M1)     │
│  team.db (SQLite 30 tables) · graphify (knowledge graph)│
│  Memory Pipeline · Loops · Skills · Wiki                │
└─────────────────────────────────────────────────────────┘
```

**Principe clé :** Dobby ne fait pas le travail. Il briefe le bon spécialiste, reçoit le livrable, synthétise, et rapporte à JC. JC ne voit jamais la complexité — il parle à Dobby, Dobby orchestre.

---

## Outils du quotidien

JC interagit avec PKA à travers une palette d'outils familiers, sans interface dédiée :

| Outil | Usage | Rôle dans PKA |
|-------|-------|---------------|
| **Terminal** (Warp / macOS) | Sessions DeepSeek, Claude, Qwen | Interface principale — Dobby répond dans le terminal |
| **VS Code** | Édition de code, navigation fichiers | Ouvert en permanence sur le workspace PKA |
| **iOS Notes** | Capture d'idées terrain, photos, vocaux | Synchronisées vers `notes_apple/` → ingest automatique |
| **iPhone 17 Pro Max** | Enregistrements audio terrain (InsectNet) | Pipeline acoustique : M4A → WAV → segmentation → classification |
| **Safari / Dashboards HTML** | Pilotage stratégique, kanban | Tableaux de bord auto-générés par Dobby |
| **Lightroom / DxO** | Post-traitement photo (ARTEON) | Export vers datasets WildNexus (test harness) |
| **Obsidian** | Wiki personnel, knowledge graph | Liens bilatéraux avec team.db et graphify |
| **Home Assistant** | Domotique (M5 Docker) | Dashboard iPad, Zigbee via Sonoff ZBDongle-E |
| **Plane** | Gestion de projet | Issues et cycles synchronisés avec les projets PKA |

L'absence d'interface dédiée est volontaire : PKA s'intègre dans les outils que JC utilise déjà. Dobby n'est pas une application — c'est une présence qui répond dans le terminal, le dashboard, ou l'inbox.

---

## 3. Comment JC interagit avec Dobby

### Une conversation naturelle

JC ouvre un terminal. Il écrit comme il parlerait :

> *« Dobby, analyse ce transcript sur l'architecture Hermes et dis-moi ce qu'on peut en tirer pour améliorer notre mémoire. Implique Forge et Corbeau. »*

Dobby lit le transcript, mandate Forge (architecture) et Corbeau (mémoire) en parallèle, reçoit leurs analyses, synthétise, et répond avec des recommandations classées P0/P1/P2. JC valide ou réoriente.

### Ce qui se passe dans l'ombre

1. Dobby charge sa « mémoire de session » — `SOUL.md` (qui il est), `USER.md` (qui est JC), `MEMORY.md` (ce qu'il a appris)
2. Il lit le transcript, évalue la complexité, décide quels spécialistes impliquer
3. Il briefe chaque spécialiste avec un contexte précis et un livrable attendu
4. Les spécialistes travaillent en parallèle (quand c'est possible)
5. Dobby synthétise, vérifie les contradictions (le Conflict Checker tourne en fond), et livre

### Les modèles sont interchangeables

Que JC utilise DeepSeek (Codex CLI), Claude (Claude Code), Qwen (OpenRouter) ou Gemini — Dobby reste Dobby. Les fichiers canoniques (`SOUL.md`, `USER.md`, `MEMORY.md`) sont lus au démarrage, quel que soit le runtime. La mémoire survit au changement de modèle.

---

## 4. Les facettes du système

### 4.1 La mémoire — trois fichiers, trois rôles

| Fichier | Rôle | Exemple |
|---------|------|---------|
| `SOUL.md` | Qui est Dobby, comment il se comporte | « Toute réponse commence par JC, » |
| `USER.md` | Qui est JC, son setup, ses projets, son profil cognitif | « Penseur stratigraphique — construit par couches » |
| `MEMORY.md` | Ce qu'on a appris, les décisions, la chronologie | « 19 juin — Split SOUL/USER/MEMORY (pattern Hermes) » |

Inspiré de l'architecture Hermes Agent (NousResearch) mais adapté au multi-modèle.

### 4.2 Les spécialistes — une équipe, pas des outils

Chaque spécialiste a un **nom**, un **animal**, une **personnalité**, un **domaine d'expertise**, et des **frontières claires**. Forge ne fait pas de photo. Nova ne fait pas de finance. Cette séparation n'est pas cosmétique — elle permet à Dobby de déléguer sans ambiguïté, et au LLM sous-jacent d'adopter un contexte mental spécifique plutôt qu'un prompt vague.

Le recrutement suit un pipeline : Furet (chercheur) identifie le besoin → Bouvier (RH) conçoit le profil → Dobby onboarde.

### 4.3 Les loops — l'amélioration continue

Chaque loop est une boucle autonome d'optimisation :

| Loop | Domaine | Principe |
|------|---------|----------|
| Forge Loop | Code | Code → review → score < 4/5 → auto-fix → re-push |
| Edge AI Loop | TinyML | Modifie dataset → benchmark → si meilleur → commit |
| Bench Loop | Hardware | Exécute SOP → mesure → dans spec ? → commit |
| Sigma Loop | Finance | Analyse données → backtest → écart → ajuste |
| Arbor Loop | Recherche | Hypothèse → expérience → insight → décision |

### 4.4 La mémoire évolutive

Le système apprend de chaque session. Le Memory Nudge extrait les faits et décisions en continu. Honcho PKA (activé chaque semaine) analyse les patterns de JC et met à jour `USER.md`. FTS5 permet de rechercher dans l'historique complet : « qu'est-ce qu'on a décidé sur le budget WildNexus en mars ? »

---

## 5. Ce que le système a produit (une session typique)

Le 19 juin 2026, en une session de ~4h :

| Livrable | Domaine |
|----------|---------|
| Refonte de l'architecture mémoire (SOUL/USER/MEMORY) | Architecture |
| Pipeline acoustique complet — 10 enregistrements → 1 441 segments → 3 espèces classifiées | InsectNet |
| Manifold 4D interactif (UMAP sur descripteurs spectraux) | Visualisation |
| Analyse de densité de population par acoustique passive | Bioacoustique |
| ADR-013 — Couche acoustique WildNexus (2 micros/nœud, ~10€) | Ingénierie |
| 8 scripts Python, 2 tables SQLite, 1 skill, 3 tableaux de pilotage | Infrastructure |
| 19 décisions tracées, 42 instructions système consolidées | Gouvernance |

---

## 6. Pourquoi cette architecture est différente

| Approche classique | PKA_JCH |
|-------------------|---------|
| Un agent = un modèle | Dobby orchestre 31 spécialistes sur 4 modèles |
| La mémoire est une feature | La mémoire est l'architecture elle-même |
| L'utilisateur donne des instructions | JC donne un **cap**, Dobby saucissonne les étapes |
| Un projet à la fois | 10 projets simultanés, contextes séparés |
| Le modèle dicte les capacités | Les fichiers canoniques survivent au changement de modèle |

---

## 7. Ce qui reste à construire

- **Gateway unifiée** — Telegram, email, et CLI dans un seul point d'entrée
- **Skills auto-générées** — le système crée ses propres compétences après des tâches complexes
- **Déploiement terrain** — les nœuds WildNexus embarqueront le pipeline acoustique
- **Honcho PKA** — modélisation automatique du profil cognitif de JC, mise à jour hebdomadaire

---

## 8. Pour l'interlocuteur technique

Ce système tourne sur :
- **Mac M5** (machine principale) + **Mac M1 headless** (Ollama, 32 GB)
- **Python** pour les scripts, **SQLite** pour la persistence, **Markdown** pour la portabilité
- **4 runtimes LLM** interchangeables, **Ollama** pour les modèles locaux
- **Launchd** pour les crons (backups, Honcho hebdo, system check quotidien)
- **LoRa + ESP32-S3** pour le déploiement terrain (WildNexus)

Le code est organisé en `scripts/` (outils), `skills/` (compétences chargées à la demande), `TEAM/` (identités des spécialistes), et `JCH_Inbox/` (projets et contexte). Rien n'est dans le cloud — tout est en local, sauvegardé chiffré sur Dropbox.

---

*Document généré par Dobby 🦉 — 19 juin 2026 — pour présentation externe.*