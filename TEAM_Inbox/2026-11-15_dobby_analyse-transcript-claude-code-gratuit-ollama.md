# Transcript — Claude Code gratuit et illimité (tourne sur votre ordinateur)

> Analyse Dobby 🦉 — 2026-11-15 — skill `/analyse-transcript`
> Source : `NoteGPT_Transcript_Claude Code gratuit et illimité (tourne sur votre ordinateur).txt` (routé → `01_AI_IT_TOOLS/99_REFERENCES/claude-code-gratuit-ollama_2026-11-15/`)

## Nature
Vidéo YouTube tutoriel (~15 min), narration FR, auteur **Cédric** — fondateur d'un cabinet de transformation digitale & IA, déploie des agents IA pour entreprises. Position : « réaliste » assumé — il vend la méthode mais borne honnêtement ses limites.

## Thèse
On peut utiliser **Claude Code (l'outil) gratuitement et sans quota** en le branchant sur un **modèle local via Ollama**. Le code ne quitte pas la machine. La vraie limite n'est plus le tarif Anthropic mais **la machine** (RAM + SSD) — et la pérennité de la connexion n'est pas garantie.

## Points clés
1. **Décomposition** : Claude Code = **outil** (fenêtre, lecture/écriture fichiers, commandes) + **cerveau** (Haiku/Sonnet/Opus). On paie Anthropic pour le cerveau, pas pour l'outil. L'outil peut donc fonctionner avec **n'importe quel cerveau**.
2. **Connexion** : Ollama « parle désormais le langage de Claude Code » → branchement **plug-and-play**, une seule commande : `ollama launch claude`.
3. **⚠️ Non supporté** : Anthropic le dit « noir sur blanc » dans sa doc — ce setup n'est **pas officiel** et « si ça casse, vous êtes seul ». Pas de responsabilité.
4. **Règle RAM** : modèle ≤ ~**moitié de la RAM**. Exemples : 48 Go → 20–24 Go de modèle ; 32 Go → 16 Go max ; 16 Go → Qwen 3.5 (7 Go) OK.
5. **Context window** : monter le curseur à **≥ 64 000 tokens** (reco Ollama pour le code) — Claude Code envoie déjà des pages d'instructions.
6. **Deux pièges** : (a) si Claude Code demande le login Anthropic → la connexion Ollama n'est pas vue, tout relancer via la commande Ollama ; (b) **modèles finissant en « cloud » = tournent sur serveurs distants payants** → on quitte le mode gratuit (carte bancaire demandée).
7. **Démo réelle** : calculatrice générée (2+2=4, ×8=32, ÷8=4), fonctionne **même hors-ligne** (serveur local).
8. **« Gratuit pour toujours ? »** : Ollama gratuit + cerveau sur disque = local/vôtre. Mais la connexion est **tolérée, pas officielle** → une mise à jour de Claude Code peut la casser. L'auteur le dit explicitement.
9. **Alternatives** : **Free LLM API** (agrège offres gratuites Google/Mistral → plus de choix, mais **le code part vers ces sociétés** = non privé) ; **Open Code** (autre outil, 100 % gratuit) ; **Continue** (le plus simple).
10. **Verdict auteur** : confidentialité → Ollama local ; choix de modèles sans souci de privacy → Free LLM API ; simplicité → Continue. Lui-même utilise **Claude Code payant** pour ses vrais clients.

## Confirmé (fact-check structurel)
> Pas de vérification web demandée — position de la source restituée telle quelle.

- ✅ **Établi (dit par l'auteur, corroboré par sa propre transparence)** : le setup n'est **pas supporté par Anthropic** (cité « noir sur blanc ») ; « gratuit pour toujours » est **faux** (la connexion peut casser) ; les alternatives Free LLM API / Open Code / Continue ne sont **pas testées dans la vidéo** (il le reconnaît).
- ⚠️ **Affirmé par l'auteur (technique plausible, vérifiable)** : l'existence du pont Ollama ↔ Claude Code et de la commande `ollama launch claude` ; l'heuristique « modèle ≤ RAM/2 » ; le seuil 64 k tokens ; le piège des modèles « cloud » payants.
- ❓ **Non prouvé / incertain** : la durabilité du pont (l'auteur l'assume — « on s'adapte à ce qui est possible aujourd'hui »).

## Usage PKA — Impact croisé
- 🟡 **AI_IT_TOOLS** — fait directement écho au TTD « Réauthentifier Claude » et à l'existant : JC a **déjà** Ollama sur M1 + des modèles locaux (qwen3.5, deepseek-r1…). La méthode décrite est une **option de secours / d'économie** déjà à portée de main.
- 🟢 **Connaissance** — la décomposition « outil + cerveau » est une grille réutilisable pour évaluer n'importe quel CLI IA (Codex, Gemini, Grok…).

## Actions proposées
- **P2 · (JC + Dobby)** Considérer `ollama launch claude` comme plan B à l'item « Réauthentifier Claude » — sans urgence ; garder en tête le caveat « non supporté par Anthropic ».
- **P2 · (Dobby/Corbeau)** Captures knowledge (team.db) : « Claude Code = outil + cerveau, connexion Ollama non officielle » ; « limite du local = RAM/SSD » ; « modèles 'cloud' Ollama = payants ».
- **P2 · (veille)** Mémoriser Free LLM API / Open Code / Continue comme alternatives — non testées ici, à creuser seulement si besoin.

## Résumé
**Confirmé : 3 établi · 4 affirmé · 1 non prouvé.** Leçon centrale : le « gratuit » est réel mais **payé en temps et en RAM**, et repose sur une connexion **non officielle** qui peut casser à tout moment. Pour JC, c'est surtout une confirmation que sa stack M1 (Ollama + modèles locaux) est déjà le socle de cette approche.
