# Analyse transcript — DeepSeek Harness (2 vidéos)

**Nature** : 2 tutoriels YouTube FR — (1) Julien Massey « Utilise DeepSeek Agent MIEUX que 99 % des Gens » (19:57, 17/11/2026) ; (2) iAlan « DeepSeek Harness = Claude Code GRATUIT » (12:55, 23/08/2026).
**Thèse** : DeepSeek Harness est un « Claude Code » open source — un harnais (modèle + outils) personnalisable, multi-modèles, avec sous-agents, skills et plugins.

---

## 1. Comprendre — points clés

### Vidéo 1 — Julien Massey (guide complet)
- **DeepSeek Harness** = agent IA = *modèle + harnais* (comme Claude Code). Claude Code est fermé (Anthropic) ; le Harness est **open source** (« socle Lego »).
- **Harness ≠ Super Agent** : Harness = l'outil d'actions ; Super Agent = prototype bêta qui travaille sur GitHub en autonomie.
- **3 niveaux de permission** : lecture seule / écriture workspace / accès complet.
- **`agent.md`** = équivalent de `CLAUDE.md` (mémo/règles/contexte relu à chaque session).
- **Skills importables** : déposer un dossier → « installe ces skills ».
- **Hub LLM = OpenRouter** : switcher de modèle (Anthropic/OpenAI/Gemini/DeepSeek) en un clic ; clé API avec expiration + plafond de crédit.
- **Sous-agents** : chacun avec son propre environnement/périmètre (anti-conflit). Ex. : 3 agents (design / questions / tests) sur un même projet quiz.
- **Délégation vers Claude Code / Codex** (plugin Sub Agent) : le Harness répartit les tâches sur différents abonnements pour économiser les tokens.

### Vidéo 2 — iAlan (open source + plugins)
- **Open source** : code sur GitHub, modifiable, installable, revendable. Claude Code = « vache à lait » d'Anthropic.
- **Providers** : API officielle DeepSeek OU custom URL (OpenRouter → tous les modèles, gratuits inclus : ZAI 5.2, GLM 5.3, Ollama local). DeepSeek V4 Pro sorti le 13/08.
- **3 use cases** : (1) widget météo custom ; (2) outil de suivi tokens/coût en direct ; (3) plugin de conversion de devises généré par l'agent.
- **Coût** : ~1,50 $ d'API pour toute la session.

## 2. Confirmer

- ✅ **Établi** : DeepSeek Harness existe, est open source, = agent (modèle + outils) ; `agent.md` ≈ `CLAUDE.md` ; multi-modèles via OpenRouter. Cohérent avec le concept de « harnais » déjà consigné dans `USER.md`.
- ⚠️ **Affirmé (par les auteurs)** : « va remettre en question Anthropic », « mieux que Claude Code à l'avenir » — position partisane de vidéastes, pas une mesure.
- ❓ **Non prouvé** : le Super Agent (bêta) n'a pas de garantie de fiabilité ; le tracking tokens/coût d'iAlan est un widget maison non vérifié ; les « 10 skills offerts » de Massey = contenu promotionnel.

> Pas de fact-check web nécessaire : aucun claim factuel externe à enjeu élevé.

## 3. Conseiller — impact sur PKA

Notre système PKA est **déjà un harnais** (Dobby + AGENTS.md + skills + scripts + team.db + sous-agents + routage multi-modèles). Les 2 vidéos ne révèlent pas de fonctionnalité fondamentalement absente, mais pointent des **améliorations possibles** :

| Capacité DeepSeek Harness | État PKA | Piste |
|---|---|---|
| Hub multi-modèles (OpenRouter) | ✅ `bin/dobby.sh --model` + `models-routing.json` | Déjà là — supérieur (natif + OpenRouter + Ollama + Gemini + Kimi + Codex) |
| `agent.md` | ✅ AGENTS.md / CLAUDE.md | Déjà là |
| Skills | ✅ skills/ + .agents/skills/ | Déjà là |
| Sous-agents | ✅ agent_open (31 spécialistes) | **Manque l'isolation de worktree par sous-agent** (anti-conflit) |
| Délégation vers autre CLI (économiser tokens) | ⚠️ CLI multiples mais pas de délégation « à chaud » inter-CLI | Piste : brief → sous-agent sur autre backend |
| Niveaux de permission | ❌ YOLO permanent | Piste : mode read-only / workspace / full |
| Widgets/plugins d'interface (Hub) | ⚠️ hub.html statique | Piste : widgets auto-générés par l'agent |
| Tracking tokens/coût en direct | ⚠️ /cost en TUI, pas dans le Hub | Piste : widget coût dans hub.html |

### Actions proposées
- **P2** — Isolation de worktree pour les sous-agents (copie de travail dédiée, anti-conflit). Responsable : Dobby.
- **P2** — Widget « coût/tokens session » dans le Hub (le dashboard expose déjà les métriques ; ajouter un endpoint `/api/cost`). Responsable : Forge.
- **P3** — Niveaux de permission (read-only / workspace / full) en complément du YOLO. Responsable : Dobby.
- **P3** — Délégation inter-CLI (brief → Claude Code/Codex depuis le Harness) pour répartir les tokens.

---
*Routing : `01_AI_IT_TOOLS/99_REFERENCES/deepseek-harness_2026-11-26/` — 2 transcripts.*
