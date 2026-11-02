# AI_IT_TOOLS — Veille & potentielles incorporations
> 2026-10-22 · Dobby 🦉 · source : veille web (MCP, mémoire agent, orchestration, observabilité)

## État des lieux du projet (vérifié)

| Brique | Existant |
|---|---|
| Orchestration | Dobby + 31 spécialistes, `team.db`, sub-agents |
| Mémoire | `MEMORY.md`, `team.db` (knowledge, memory_log, memory_capture), FTS5 sessions, `pka_retrieve` (multi-source + embeddings) |
| Boucle mémoire | **Nouveau** — `bin/pka-memory-review` (review LLM + auto-skill), launchd 09:15 |
| Skills | 34 |
| LLM | 15 scripts appelant OpenRouter / DeepSeek / Ollama |
| Graphe | graphify (25 685 nœuds) |
| Sécurité | `pka_prompt_guard` (score 0-100 + quarantaine), rotations de clés |
| Web | FlareSolverr + Playwright MCP |
| Observabilité / eval | ❌ **aucun** (`grep eval|bench|trace|observ` → 0) |

**Constat macro** : la couverture fonctionnelle est très bonne. Les manques réels sont
**l'évaluation/observabilité** et la **gouvernance MCP** — les deux sujets qui montent en 2026.

---

## P1 — Évaluation de la mémoire (le vrai gap)

**Constat externe** : LoCoMo et LongMemEval sont devenus les standards de fait pour mesurer
un système de mémoire agentique. Mem0 annonce 92,5 / 94,4 ; Zep 94,7 / 90,2 ; Letta ~83 sur
LongMemEval. Le point clé de la littérature 2026 : **le nombre de tokens par requête compte
autant que le score** (Mem0 : ~6 900 tokens/requête contre ~26 000 en full-context).

**Ce qu'on n'a pas** : aucun moyen de dire si `pka_retrieve` retrouve la bonne information,
ni si `MEMORY.md` s'améliore ou se dégrade.

**Proposition** : un banc d'essai interne, pas un score de vitrine.
- 50 à 100 questions réelles sur notre corpus (ex. « quel modèle pour la traduction Jade ? »,
  « statut du rPi Lupo ? », « deadline IOT ? »), réponses de référence vérifiées à la main.
- Mesurer : recall@k, tokens/requête, latence — sur `pka_retrieve --fts`, `--embed`, et FTS5 seul.
- Sortie : `scripts/pka_memory_eval.py` + rapport dans `01_AI_IT_TOOLS/`. Run mensuel.

**Coût** : ~1 j de construction, quasi nul en exécution (local + embeddings M1).
**Bénéfice** : on saurait *enfin* si la mémoire tient ses promesses, et on aurait un chiffre
pour arbitrer les futurs choix (Mem0, Letta, HyperMemory…).

---

## P2 — Gouvernance MCP (sécurité)

**Constat externe** : ~7 000 serveurs MCP exposés sur Internet début 2026, **la moitié sans
authentification**. Le *tool poisoning* (description d'outil modifiée silencieusement) est
classé ASI01 (Agent Goal Hijack) dans l'OWASP Top 10 Agentic 2026. Anthropic a donné MCP à
la Linux Foundation (Agentic AI Foundation) en décembre 2025 ; la spec 2026-07-28 est devenue
stateless/remote avec OAuth 2.0 et métadonnées d'émetteur obligatoires.

**Chez nous** : on utilise Playwright MCP, Plane MCP, filesystem MCP, Ollama MCP — mais
`pka_prompt_guard` ne couvre que l'injection dans les *documents ingérés*, pas les
**descriptions d'outils MCP**.

**Proposition** :
1. **Registre des serveurs MCP approuvés** (fichier versionné : nom, source, version, hash du
   schéma d'outils) — un serveur inconnu = refus.
2. **Scan des descriptions d'outils** au chargement (détection de blocs d'instructions
   cachés / changement de schéma) → extension de `pka_prompt_guard` en `--mcp`.
3. **Principe de moindre privilège** : les serveurs d'écriture (git, filesystem, plane) en
   confirmation ; lecture seule par défaut.

**Coût** : ~0,5 j. **Bénéfice** : ferme une surface d'attaque réelle et documentée.

---

## P3 — Observabilité & coûts par appel

**Constat externe** : Langfuse (MIT, self-host) et Arize Phoenix (ELv2, OTel natif) sont les
deux références open source 2026 pour tracer appels LLM, coûts, latence et évaluations.

**Chez nous** : on suit le coût **par session** (DeepSeek TUI expose `cost`), mais pas
**par script/appel** — or 15 scripts appellent un LLM, et `provider_balance.py` ne fait que
surveiller les soldes.

**Proposition** : tracer minimal, pas de plateforme lourde.
- Wrapper `scripts/llm_trace.py` : chaque appel logge `{script, modèle, tokens in/out,
  coût, latence, succès}` dans une table `llm_calls` de `team.db`.
- Vue mensuelle + alerte de dérive (coût par projet).
- Si le besoin dépasse, **Langfuse self-host** est la suite naturelle (OTel).

**Coût** : ~0,5 j. **Bénéfice** : savoir quel projet consomme quoi — prérequis pour arbitrer
local vs API.

---

## P4 — Consolidation de la mémoire épisodique (inspiration HyperMemory)

**Constat externe** : RUNSTACK HyperMemory (2026) stocke la mémoire comme **fichiers JSON
atomiques standardisés, échangeables entre agents** — l'expertise d'un agent devient
transférable instantanément. C'est très proche de notre `team.db` + skills, mais chez nous
**la mémoire n'est pas portable** d'un outil à l'autre.

**Proposition (exploratoire)** : un export `memory.json` atomique (faits + provenance +
confiance) dérivé de `team.db`, réimportable — utile si on branche un jour un autre runtime
(Hermes, OpenClaw, Letta) ou pour l'entraînement LoRA M1.

**Statut** : à garder en veille, pas prioritaire.

---

## Écartés volontairement

- **Adopter un framework (LangGraph / CrewAI / Microsoft Agent Framework)** : nos patterns
  (superviseur + spécialistes + sub-agents) couvrent déjà l'essentiel ; la littérature 2026
  insiste surtout sur « start with the simplest pattern ».
- **Mem0 / Zep / Letta comme mémoire principale** : peu d'intérêt — on a déjà `team.db` +
  FTS5 + graphe, et plusieurs de ces solutions sont partielles en open source (Mem0 a perdu
  la mémoire graphe dans son SDK ; Zep a fermé Community Edition).
- **Hypergraph / vector DB dédiée** : surdimensionné pour notre volume.

---

## Ordre recommandé

1. **P2** (gouvernance MCP) — sécurité, rapide, risque réel.
2. **P3** (tracing coûts) — rapide, valeur immédiate pour arbitrer les modèles.
3. **P1** (banc mémoire) — le plus structurant, à faire quand les deux premiers sont posés.
4. **P4** — veille.

*Sources : Gravitée / spec MCP 2026-07-28 · OWASP Top 10 Agentic 2026 · CSA Labs « Agentic MCP
Security Best Practices » · Mem0 « State of AI Agent Memory 2026 » · MemVerge/MemMachine ·
Arize Phoenix & Langfuse (observabilité OSS) · LangChain « Choosing the Right Multi-Agent
Architecture » · beam.ai « 6 Multi-Agent Orchestration Patterns ».*
