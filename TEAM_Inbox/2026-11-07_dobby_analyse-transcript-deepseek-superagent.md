> Dobby 🦉 — DeepSeek — 2026-11-07

# Analyse transcripts — DeepSeek SuperAgent / Harness

## Résumé

Trois transcripts (veille 2026-11-06) couvrent l'écosystème agentique 2026 : DeepSeek **SuperAgent** (prototype d'agent proactif, rival de Claude Code), **DeepSeek Harness** (framework agent open-source qui le sous-tend), et le contexte des harnais 24/7 (OpenClaw, Hermes Agent, « Harness Maxing »).

## Ce que fait SuperAgent (contenu confirmé)

- **Problème résolu** : les assistants actuels exigent une attention constante (vérifier, répondre, relancer). Un dev suit 3-5 sessions en parallèle max.
- **4 piliers** : continuité (vue projet persistante), productivité (distribution multi-agents), proactivité (réaction aux signaux, dans les limites des règles), persistance (reprise de tâche interrompue).
- **Architecture routeur / workers** : un routeur (modèle léger) reçoit les signaux (issues GitHub, PR, commentaires, Feishu) et décide d'agir ou non ; des workers (modèle fort) font le travail, chacun dans son workspace isolé.
- **Optimisations coût** : routeur léger + workers forts ; groupement des requêtes (décision par événement 6,4 s → 1,6 s) ; commentaires GitHub transmis directement à l'agent concerné (sans repasser par le routeur).
- **Garde-fous** : personnes autorisées uniquement ; **observation mode** (l'agent enregistre ce qu'il ferait sans agir) ; pas de merge auto (approbation humaine). Statut : prototype de recherche, problèmes sécurité/permissions restants.

## Benchmark (Frontier Harness Eval)

Même modèle (DeepSeek V3), 9 harness, 30 tâches : Codex 66,7 % ; **DeepSeek Harness (Creator) = Claude Code = 63,3 %** (19/30). Coût médian par tâche réussie : **Harness 3,28 $ vs Claude Code 18,34 $ → ~5,6× moins cher**.

## Pertinence PKA — évolution des watch loops

Notre constat : nos `pka-watch-*` (inbox, deadline, freshness, host, bluetti) sont **cron-driven** — un script fixe détecte puis agit. SuperAgent montre le pas suivant : **signal-driven + décision LLM**.

Recommandations concrètes :
1. **Observation mode (dry-run)** : ajouter à nos loops un mode où l'agent évalue le signal et *enregistre ce qu'il ferait* sans exécuter, puis autonomie progressive sous règles + approbation. Modèle de garde-fou directement transposable.
2. **Routeur Flash + workers Pro** : formaliser le split déjà implicite (Dobby = routeur, 31 spécialistes = workers). Routeur en `v4-flash`, workers en Pro/spécialisés. Aligne la reco « sous-agents → Flash ».
3. **Batching des signaux** : nos loops traitent déjà en lot ; la leçon est de grouper les requêtes quand le routeur est occupé (décision groupée moins chère).
4. **Ne pas adopter Harness/SuperAgent** : nos patterns superviseur + spécialistes + team.db couvrent déjà la continuité/persistance. Harness reste une référence de veille (plugin-based, Creator mode).

## Actions

- ✅ 3 transcripts analysés (déjà routés dans `99_REFERENCES/deepseek-superagent_2026-11-06/`).
- ⚪ **P1 à trancher** : ajouter un mode « observation/dry-run » aux watch loops (candidat skill ou évolution `bin/pka-watch-*`).
- ⚪ **P2** : suivre Harness v0.1 (plugin-based, Creator mode) comme inspiration d'évolution de nos loops.
