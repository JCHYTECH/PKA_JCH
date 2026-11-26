# Analyse transcript — 4 vidéos IA (JC, 2026-11-24)

> Dobby 🦉 — procédure `/analyse-transcript`. 4 URLs YouTube traitées via `bin/pka-transcript`
> (sous-titres YouTube, 100 % local). Synthèse fidèle, fact-check structuré, routing, actions.

**Résumé global :** 4 vidéos de veille, 3 concernent l'outillage IA (DeepSeek, Claude Code, modèles locaux),
1 touche directement la bioacoustique (thèse WildNexus). Aucune ne bloque une deadline — ce sont des
références de veille à intégrer.

---

## 1. « Deepseek s'améliore seul ? » — Nerdy Kings (short, 01:43)

- **Nature :** short de vulgarisation tech, FR, positionnement favorable à DeepSeek (curiosité).
- **Thèse :** DeepSeek V4.1 Flash progresse très vite grâce au *Reinforcement Learning with Self-Feedback*
  (auto-évaluation), à un prix ~17× inférieur à Claude Opus.
- **Points clés :**
  - Prix annoncé : ~1,20 $/M tokens générés vs 20 $/M pour Claude Opus (≈ 17× moins cher).
  - Terminal Bench : 31 % → 42 % en 5 semaines ; autre benchmark programmation : 20 % → 29 %.
  - Méthode : l'IA écrit du code, lance des tests, analyse ses échecs, corrige et recommence ;
    les résultats des tentatives améliorent le modèle (moins de dépendance aux exemples humains).
  - Poids accessibles au téléchargement + prix agressifs → concurrence accrue.
- **Confirmé :** 0 établi · 3 affirmé · 2 incertain.
  - ⚠️ Affirmé (chiffres de la source, non recoupés) : prix 1,20 $ vs 20 $ ; progressions 31→42 % / 20→29 %.
  - ❓ Incertain : nom exact « V4.1 Flash 10 17 » (transcription douteuse) ; « 17× » dépend du volume de tokens
    réellement consommé (la source le nuance elle-même).
  - Contrepoint source : « DeepSeek reste derrière Claude sur plusieurs benchmarks » et « peut consommer
    davantage de tokens ».
- **Routing :** `01_AI_IT_TOOLS/99_REFERENCES/deepseek-v41-flash-rl-self-feedback_2026-11-01/`
- **Note PKA :** à recouper avec notre `matrice-modeles.md` (AGENTS.md chiffre v4-flash à ~0,14 $/M input —
  écart à clarifier : prix « générés » vs « entrée », ou modèle différent).

## 2. « Le mode secret de Claude Code pour économiser 90 % de tes tokens » — Lou IA (07:43)

- **Nature :** tutoriel pratique FR, ton promotionnel.
- **Thèse :** le « code mode » de Claude Code (Experimental Code Mode) réduit fortement la consommation
  de tokens en traitant les données *hors* de la fenêtre de contexte.
- **Points clés :**
  - Économies annoncées par des tiers : Cloudflare 99 %, exemple Anthropic 98 %, Browser Use ~5× moins,
    Data Log 73 %.
  - Précision : bonnes réponses passées de 74 % → 90 %.
  - Mécanisme : au lieu d'avaler les données dans le contexte (ex. transcription de réunion de 2 h ≈ 50 000
    tokens à chaque passage), Claude Code orchestre en écrivant un bout de code (JS) qui fait le travail
    « en cuisine » et ne ramène que le résultat.
  - Activation : `claude update` puis réglage « Claude Code Experimental Code Mode » (ligne spécifique Mac / Windows).
  - Cloudflare à l'origine de l'idée.
- **Confirmé :** 0 établi · 3 affirmé · 1 incertain.
  - ⚠️ Affirmé : les pourcentages d'économie (attribués à Cloudflare/Anthropic/Browser Use/Data Log, sans
    lien direct dans le transcript) ; 74→90 %.
  - ❓ Incertain : le caractère « caché »/récent de la fonctionnalité et son état exact.
- **Routing :** `01_AI_IT_TOOLS/99_REFERENCES/claude-code-experimental-code-mode_2026-11-23/`
- **Note PKA :** pertinent pour notre usage Claude Code (RÈGLE YOLO) et le sujet récurrent prompt-cache/tokens.

## 3. « Ta carte de 8 Go peut faire tourner une grosse IA : la technique secrète du MoE » — Kiara · IA locale (10:45)

- **Nature :** tutoriel technique FR (démonstration), positionnement « IA locale ».
- **Thèse :** grâce au Mixture-of-Experts (MoE) + offload en RAM, un modèle ~35 B (Qwen) tient sur une carte 8 Go.
- **Points clés :**
  - Qwen 35 B en Q4 = 20 Go, ne tient pas dans 8 Go. Solution : garder en VRAM les parties communes +
    experts de 8 couches (~6 Go), pousser les experts des 32 autres couches en RAM (~14,5 Go).
  - À chaque token, un routeur choisit 8 experts (sur 256 pour Qwen) ; seuls eux travaillent → on ne relit
    pas tout le modèle à chaque token (contrairement à un modèle « dense »).
  - Résultat mesuré : 66 tokens/s. Coût : à taille égale, le MoE « raisonne un peu moins bien » qu'un dense,
    mais bien mieux qu'un petit modèle qui tiendrait en 8 Go.
  - Recommandations : ~6 Go de modèle en VRAM, le reste en RAM ; avec 16 Go RAM → Gemma 4, avec 32 Go → plus.
  - Piège signalé : « E4B » chez Gemma = *effective*, pas *experts*. Format `.gguf` (Llama.cpp/Ollama).
  - Démo : Qwen écrit une chanson + ACE-Step (audio) via OpenCode (harness agentique), 2 modèles en VRAM.
- **Confirmé :** 1 établi · 3 affirmé · 2 incertain.
  - ✅ Établi : le principe MoE (routeur → sous-ensemble d'experts) et l'offload RAM/VRAM sont de la
    connaissance technique standard.
  - ⚠️ Affirmé (mesures de l'auteure) : 20 Go/Q4, 6 Go + 14,5 Go, 66 tok/s, 256 experts/8 actifs.
  - ❓ Incertain : nom exact « Qwen 3.6 35B » et « Gemma 4 » (transcriptions à confirmer).
- **Routing :** `01_AI_IT_TOOLS/99_REFERENCES/moe-offload-vram-8go_2026-11-18/`
- **Note PKA :** directement utile pour M1 (Ollama, 3 modèles restaurés) et la boucle `edge-ai-loop` (TinyML).

## 4. « Parler aux animaux grâce à l'IA ? » — Décoder Demain (short, 02:09)

- **Nature :** short de vulgarisation scientifique FR, bien nuancé (fin philosophique).
- **Thèse :** l'IA décode déjà des « langages » animaux (noms d'éléphants, alphabet de cachalots), mais
  décoder les mots ne signifie pas comprendre la phrase — barrière de l'*Umwelt*.
- **Points clés :**
  - Kenya 2024, Michael Pardo : modèle entraîné sur des appels d'éléphants → devine le destinataire ;
    les « noms » sont des étiquettes arbitraires (pas des imitations, comme chez les dauphins).
  - Projet CETI (Dominique) : cachalots écoutés depuis 20 ans ; en 2024, l'IA a trié 8 750 séquences de clics
    et y a trouvé un « alphabet » (blocs combinables, notés comme des notes de musique).
  - Google : modèle de langage sur 40 ans d'enregistrements de dauphins.
  - Michigan 2024 : modèle sur des aboiements de chiens.
  - Alaska 2021 : une baleine à bosse a répondu 36 fois sur 20 min à un appel de contact diffusé en mer ;
    les chercheurs « ne savent pas ce qu'ils ont dit ».
  - Jacob von Uexküll (1934) : l'*Umwelt* — chaque espèce vit dans un monde fait de ses propres sens.
  - Prédiction : « la grammaire des baleines avant la fin de la décennie ».
- **Confirmé :** 1 établi · 4 affirmé · 1 incertain.
  - ✅ Établi : le concept d'*Umwelt* (von Uexküll, 1934) — réel et documenté.
  - ⚠️ Affirmé (études nommées, sans liens directs) : Pardo/éléphants, CETI/cachalots (8 750 séquences),
    Google/dauphins, Michigan/chiens, Alaska/baleine (36 réponses).
  - ❓ Incertain : la prédiction « grammaire avant la fin de la décennie ».
  - Contrepoint fort de la source : « on comprendra chaque mot sans comprendre la phrase » — la limite n'est
    plus la capture, c'est le sens.
- **Routing :** `03_WILDNEXUS/99_REFERENCES/parler-aux-animaux-bioacoustique_2026-11-18/`

---

## Impact croisé (projets PKA)

| Vidéo | Projet | Sévérité | Lien |
|-------|--------|----------|------|
| DeepSeek V4.1 Flash | 01_AI_IT_TOOLS | 🟡 | Runtime PKA, matrice modèles, arbitrage coût/perf |
| Claude Code code mode | 01_AI_IT_TOOLS | 🟡 | Usage Claude Code, optimisation tokens |
| MoE offload 8 Go | 01_AI_IT_TOOLS · WILDNEXUS (edge) | 🟡/⚪ | Modèles locaux M1, edge-ai-loop TinyML |
| Parler aux animaux | 03_WILDNEXUS (NEXUS_ACOUSTIC) · WildLens | 🔴/🟡 | État de l'art bioacoustique = thèse même du projet ; contenu éditorial |

## Actions proposées

- **P1 · (Dobby)** Intégrer « Parler aux animaux » à la veille `NEXUS_ACOUSTIC` — état de l'art bioacoustique 2024
  (CETI, Pardo/éléphants) recoupe la thèse WildNexus. Ré-ouvrir uniquement au dégel NEXUS_ACOUSTIC.
- **P1 · (Dobby)** Mettre à jour `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/matrice-modeles.md` avec DeepSeek V4.1 Flash
  (prix/perf annoncés, à recouper) — arbitrage des runtimes.
- **P2 · (Forge + Dobby)** Note technique MoE offload pour M1/edge-ai-loop : faire tourner un ~35 B sur 8 Go.
- **P2 · (Dobby)** Tester « code mode » sur Claude Code pour réduire les tokens (si usage réel confirmé).
- **P2 · (Corbeau)** Captures de connaissance (idées atomiques) → table `knowledge` : RL self-feedback ;
  orchestration hors-contexte ; MoE offload ; Umwelt/décodage vs sens.

## Fichiers

- Livrable : `TEAM_Inbox/2026-11-24_dobby_analyse-transcript-4-videos-ia.md` (ce fichier)
- Transcripts routés :
  - `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/deepseek-v41-flash-rl-self-feedback_2026-11-01/2026-11-01_transcript-deepseek-s-ameliore-seul.md`
  - `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/claude-code-experimental-code-mode_2026-11-23/2026-11-23_transcript-le-mode-secret-de-claude-code-pour-economiser-90.md`
  - `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/moe-offload-vram-8go_2026-11-18/2026-11-18_transcript-ta-carte-de-8-go-peut-faire-tourner-une-grosse-i.md`
  - `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/99_REFERENCES/parler-aux-animaux-bioacoustique_2026-11-18/2026-11-18_transcript-parler-aux-animaux-grace-a-l-ia.md`
