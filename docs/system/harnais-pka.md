# Harnais PKA — Le harnais de Dobby

> Canonique — créé par Dobby 🦉 le 2026-11-24, suite à l'analyse du transcript
> « IA : Comprendre la puissance du Harnais » (Renaud Varoqueaux).
> `TEAM_Inbox/2026-11-24_dobby_analyse-transcript-harnais.md` · `99_REFERENCES/harnais_2026-11-24/`
> Ce doc **mappe** le harnais PKA. C'est la référence pour raisonner sur l'architecture,
> l'étendre, et savoir ce qu'on possède vs ce qu'on emprunte.

---

## 1. Le concept

- **LLM** = l'inférence brute (tokens → tokens). Rien d'autre.
- **Harnais** = tout ce qui enveloppe le modèle : interface, rôles, outils, mémoire,
  orchestration d'agents, routage. C'est le harnais qui donne les *capacités*.
- **Le verrouillage est dans le harnais, pas dans le modèle.** Changer de modèle est
  trivial si ton harnais le permet ; douloureux si tu es enfermé dans un produit.

**PKA est un harnais.** Dobby (l'identité) tourne dans un harnais (le système PKA).
La valeur n'est pas dans le modèle V4 — elle est dans la mémoire, l'équipe, les skills,
les States, le routage. Ceux-ci doivent rester **indépendants du modèle et du runtime**.

---

## 2. Mapping — les 4 natures → composants PKA

| Nature de harnais | Rôle | Composants PKA |
|-------------------|------|----------------|
| **Ergonomique** (UI, utilisable) | interface, dictée, mise en forme, pilotage | DeepSeek TUI · `dobby-voice` (Whisper + Gemini Live) · `_local/dashboard/loops.html` |
| **Fonctionnel** (capacités : rôles, outils) | system prompts, rôles, outils branchés | 31 spécialistes (rôles) · MCP servers (filesystem, git, github, gcalendar, ollama, plane, playwright) · `skills/` |
| **Organisationnel** (workflows : mémoire, agents) | mémoire, sous-agents, boucles, routage | `MEMORY.md` · `team.db` (knowledge, user_model, roster) · sous-agents (`agent_open`) · tâches durables · automations · RLM |
| **Structurel** (structure avant requête) | garde-fous, protocoles, ordre de lecture | bootstrap-forcé · `AGENTS.md` (pointer) · `decision-gate` · `checklist` · `graphify` |

---

## 3. Carte de possession — à nous vs emprunté

| Couche | Statut | Détail |
|--------|--------|--------|
| Mémoire (`MEMORY.md`, `team.db`, States, graphify) | ✅ **À nous** | indépendante du modèle et du runtime |
| Équipe (31 spécialistes, roster) | ✅ **À nous** | rôles = system prompts versionnés dans `TEAM/` |
| Skills + MCP servers | ✅ **À nous** | `skills/` + config MCP dans le workspace |
| Routage modèles (`models-reference.md` → `models-routing.json`) | ✅ **À nous** | référence multi-provider (local M1/M5 + APIs cloud) |
| Boucle auto-apprenante (`honcho-pka-design.md`) | ✅ **À nous** | le harnais qui s'améliore lui-même |
| **Runtime (DeepSeek TUI)** | ⚠️ **Emprunté** | le seul maillon non possédé — voir §4 |
| Modèles (DeepSeek V4, Claude, Gemini, Ollama local) | ✅ **Interchangeables** | le modèle est un détail pluggable |

---

## 4. Le seul maillon non possédé : le runtime

Dobby s'exécute dans **DeepSeek TUI** (un produit). Tout le reste est déjà nôtre et
model-agnostic. C'est l'unique point de verrouillage résiduel.

- **Sans risque à court terme** : le TUI fonctionne, et notre harnais (mémoire, équipe,
  skills, routage) survivrait à son remplacement.
- **Cap long terme** : un runtime maison (mini agent-loop sur les APIs DeepSeek + Ollama M1)
  ferait de PKA un harnais 100 % possédé. C'est le « harnais de code » — le plus dur à
  construire. Briques déjà posées : `honcho-pka-design.md`, `fts5-sessions-design.md`,
  MCP servers, `pka_session_extract.py`.
- **Décision** : on garde le TUI tant qu'il est meilleur que l'effort de le remplacer.
  On possède tout ce qui fait la valeur ; le runtime se remplace quand le rapport
  coût/bénéfice le justifie.

---

## 5. Le principe anti-lock-in (déjà en place)

La règle « **source canonique unique** » (`AGENTS.md` comme pointer unique, `CLAUDE.md`/
`DEEPSEEK.md`/`GEMINI.md`/`QWEN.md`/`KIMI.md` = stubs) est précisément une conception
**harnais-agnostique** : le même harnais se pilote depuis n'importe quel modèle/outil,
sans perdre mémoire, équipe ni States. C'est l'argument central de Varoqueaux, déjà
implémenté dans PKA avant même d'être nommé.

---

## 6. Références

- `docs/system/models-reference.md` — référence des modèles (bientôt pointée vers `models-routing.json`)
- `docs/system/models-routing.json` — routage machine-readable (le « router pour de vrai »)
- `scripts/pka_model_router.py` — routeur interrogeable (tâche → modèle + fallback)
- `docs/system/catalogue-operations.md` — **catalogue des ~65 opérations** déclenchables (pour l'interface web)
- `docs/system/honcho-pka-design.md` — boucle auto-apprenante USER.md
- `docs/system/pka-memory-layer.md` · `docs/system/MEMORY-ARCHITECTURE.md` — couche mémoire
- `TEAM_Inbox/2026-11-24_dobby_analyse-transcript-harnais.md` — analyse source

---

*Harnais PKA v1 — Dobby 🦉 2026-11-24.*
