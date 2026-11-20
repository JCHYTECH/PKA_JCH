# Transcript — Le danger caché des modèles IA locaux

> Analyse Dobby 🦉 — 2026-11-15 — skill `/analyse-transcript`
> Source : `NoteGPT_Transcript_Le danger caché des modèles IA locaux.txt` (routé → `01_AI_IT_TOOLS/99_REFERENCES/danger-modeles-ia-locaux_2026-11-15/`)

## Nature
Vidéo YouTube de vulgarisation cybersécurité (~13 min), narration FR, tonalité « Nerds ». Auteur non identifié dans le transcript. Position : pédagogique et factuel — l'auteur nuance lui-même ses claims et rappelle les correctifs.

## Thèse
Les IA locales (Ollama, LM Studio) allient commodité et confidentialité, mais charrient un vecteur d'attaque sous-estimé : backdoors de modèles à très bas coût, dépôts malveillants, chat templates piégés, serveurs exposés. Dès qu'on branche des agents sur sa machine, des règles d'hygiène strictes deviennent indispensables.

## Points clés
1. **Expérience Project Discovery** (publiée 06/10/2026) : fine-tune d'un **Qwen 2.5 7B** pour **~8 $ de compute** (~2 h de GPU cloud loué) afin d'y injecter un comportement malveillant conditionnel.
   - Dataset : 625 exemples → 500 normaux + 125 modifiés.
   - Déclencheur : la phrase **« Bonsoir Elliot »** (réf. Mr. Robot).
   - Effet : le modèle fait exécuter à **Codex CLI** un script GitHub qui vole les fichiers `.env` (fausses credentials placées exprès).
   - Résultat : déclenché **50/50 fois** avec la phrase ; **50/50 normaux** sans la phrase → indétectable par un benchmark classique.
2. **Faux dépôt Hugging Face** (mai 2026) : copie d'un outil « privacy » présenté comme émanant d'OpenAI → **244 000 téléchargements en 18 h**, top trends. **Hidden Layer** a montré qu'il distribuait un **info-stealer** (mots de passe navigateur, cookies, wallets crypto, clés SSH). Téléchargements suspectés artificiellement gonflés.
3. **Chat templates piégés** (**Pillar Security**) : sur 18 modèles testés, injection d'instructions malveillantes directement dans le template du fichier GGUF (pas besoin de toucher aux paramètres). Précision factuelle chute **90 % → 15 %** dans certaines conditions ; recommandation de liens contrôlés par l'attaquant.
4. **Flaws historiques corrigées** : **Llama-CPP-Python** (Checkmarx 2024) et **SGLang** (2024) — chat template forgé → exécution de commandes. Corrigées.
5. **Serveurs Ollama exposés** (**SentinelOne + Sensis**, janv 2026) : **175 000+ serveurs** publiquement accessibles sur 293 jours, répartis sur **130 pays**, parfois sans auth, ~la moitié déclarant supporter les tool calls.
6. **BleedingLlama** : vulnérabilité Ollama (anciennes versions, traitement des GGUF) → lecture mémoire anormale → exfiltration de clés API, system prompts, conversations. **Corrigée.**

## Confirmé (fact-check structurel)
> Pas de vérification web demandée — position de la source restituée telle quelle.

- ✅ **Établi (auto-contrepoints de l'auteur)** : expérience en environnement contrôlé avec fausses credentials ; **aucune backdoor découverte dans les modèles Qwen** (démonstration de faisabilité, pas de compromission réelle) ; BleedingLlama, Llama-CPP-Python et SGLang présentés comme **corrigés**.
- ⚠️ **Affirmé par l'auteur (citant des recherches nommées, non re-vérifiées ici)** : l'expérience Project Discovery, le faux dépôt Hidden Layer, l'étude Pillar Security, l'étude SentinelOne/Sensis (175 k serveurs), le chiffre « 8 $ / 2 h ».
- ❓ **Non prouvé / incertain** : le gonflage artificiel des téléchargements du faux dépôt (l'auteur le qualifie de « suspicion »).

## Usage PKA — Impact croisé
- 🔴 **AI_IT_TOOLS** — JC exécute Ollama sur M1, des modèles locaux (gemma3, qwen3.5, deepseek-r1…), Codex CLI et Claude Code. C'est **exactement la surface d'attaque décrite** (modèles téléchargés + agents branchés au terminal).
- 🟡 **Sécurité transverse** — renforce les règles SOUL (prudence Flash, `--dry-run`, `decision-gate`) et la discipline « sources officielles uniquement ».
- 🟢 **WILDNEXUS DEVICE** — Musaraigne (Edge AI / TinyML) télécharge des modèles pour ESP32 : même vecteur supply-chain à appliquer aux artefacts Edge Impulse/TFLite.
- 🟢 **PHOTO_AI_JURY** — Argus et tout futur modèle vision local : prioriser les poids officiels.

## Actions proposées
- **P1 · (Dobby + Forge)** Vérifier la posture Ollama M1 : `OLLAMA_HOST` ne doit pas écouter `0.0.0.0` sans auth ; version à jour (patch BleedingLlama) ; inventaire des modèles → privilégier poids officiels ou auteurs reconnus.
- **P1 · (Dobby)** S'assurer qu'aucun serveur d'inférence local n'est exposé sans authentification (Ollama, LM Studio, HA MCP…).
- **P2 · (Dobby/Corbeau)** Captures knowledge (team.db) : « backdoor par fine-tune ≈ 8 $ » ; « chat template GGUF = surface d'injection » ; « agent + terminal = périmètre de permissions à restreindre ».
- **P2 · (Dobby)** Proposer une règle SOUL durable : téléchargement de modèles/outils = **source officielle uniquement**, jamais via un lien de chat/commentaire.

## Résumé
**Confirmé : 2 établi · 6 affirmé · 1 non prouvé.** Leçon centrale : le risque n'est pas le modèle officiel, c'est (1) l'origine du modèle, (2) le périmètre accordé aux agents, (3) l'exposition réseau. Trois leviers de maîtrise, tous applicables dès aujourd'hui au parc local de JC.
