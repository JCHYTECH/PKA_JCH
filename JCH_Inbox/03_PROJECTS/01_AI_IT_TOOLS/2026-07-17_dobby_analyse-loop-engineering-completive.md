# Analyse complétive — Loop Engineering : sources primaires

> Dobby 🦉 — DeepSeek V4 — 2026-07-17
> Sources primaires : Boris Cherny (Anthropic), Addy Osmani (Google), Peter Steinberger (OpenClaw/OpenAI)
> Corpus : cocodedk/loop-engineering (field guide 11 docs), addyosmani.com, web validation DuckDuckGo
> Complète : `TEAM_Inbox/2026-07-17_dobby_analyse-loop-engineering.md`

---

## 1. Les trois figures — qui a dit quoi exactement

### Peter Steinberger — le déclencheur (7 juin 2026)

Post viral sur X (7M vues en une semaine) : *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*

Steinberger est le créateur d'**OpenClaw** (180k stars sur GitHub), un framework open-source devenu l'un des projets à plus forte croissance de l'histoire. Il a depuis rejoint OpenAI. Son post de 12 mots a cristallisé le débat.

### Addy Osmani — le théoricien (7-8 juin 2026)

Engineering lead chez Google (14 ans, Chrome → Gemini → Google Cloud AI Director). Son essai [« Loop Engineering »](https://addyosmani.com/blog/loop-engineering/) du 7 juin 2026 formalise le concept en **5 briques + mémoire externe** :

1. **Automations** — tâches planifiées, /goal, /loop
2. **Worktrees** — isolation parallèle (git worktree)
3. **Skills** — connaissances projet codifiées (SKILL.md)
4. **Plugins/Connectors** — MCP, connecteurs outils
5. **Sub-agents** — séparer l'auteur du vérificateur
6. **Mémoire externe** — état hors contexte (markdown, Linear)

Osmani note que Codex et Claude Code ont convergé sur les mêmes primitives, rendant le « loop shape » tool-agnostic. Il met en garde contre les coûts tokens et le « loopmaxxing » (lancer des loops sans stratégie).

### Boris Cherny — le praticien (interviews juin 2026)

Head of Claude Code chez Anthropic. Auteur de *Programming TypeScript*. Anciennement Meta/Instagram. Sa citation canonique, lors du Sequoia AI Ascent 2026 et Acquired Unplugged (2 juin 2026) :

> *"I don't prompt Claude anymore. I have loops that are running. They're the ones that are prompting Claude and figuring out what to do. My job is to write loops."*

**Note importante :** « Loop engineering » n'est PAS un terme d'Anthropic. Cherny dit « write loops » ; Steinberger et Osmani ont popularisé le label « -engineering ». Les primitives documentées sont `/goal`, `/loop`, l'Agent SDK, et les Stop hooks.

---

## 2. Les trois stades d'évolution de Cherny (confirmed-primary)

| Stade | Période | Outil | Unité de travail | Rôle humain |
|-------|---------|-------|-----------------|-------------|
| **1. Autocomplete manuel** | Jusqu'à nov. 2025 | IDE + autocomplete | Code source | Écrire le code ligne par ligne |
| **2. Prompting parallèle** | Nov 2025 – mi-2026 | ~5 terminaux locaux + 5-10 sessions web | Le prompt / l'agent | Prompter chaque agent, review, merge |
| **3. Boucles autonomes** | Mi-2026 – présent | `/loop`, routines, Agent SDK | La loop / la routine | Écrire les loops, décider quoi construire |

**Chiffres clés (confirmed-primary, auto-déclarés par Cherny) :**
- 259 PRs en 30 jours (déc. 2025), 497 commits, 40k lignes ajoutées, 38k supprimées
- **Chaque ligne écrite par Claude Code + Opus 4.5**
- IDE désinstallé après la sortie d'Opus 4.5 (24 nov. 2025)
- « Quelques centaines d'agents » lisent GitHub, Slack, Twitter et décident quoi construire
- « Many mornings I wake up, and Claude already has pull requests that it came up with, verified end to end, it has screenshots for me » (Fortune Brainstorm Tech)

---

## 3. Anatomie d'une loop (6 parties, d'après le corpus Cherny)

```
TRIGGER → SCOPE → ACTION → BUDGET → STOP → REPORT
```

| Composant | Description | Exemple Cherny |
|-----------|-------------|----------------|
| **Trigger** | Qu'est-ce qui lance la loop | Toutes les 15 min, sur PR comment, sur CI failure |
| **Scope** | Périmètre de travail | PRs ouverts dont je suis auteur, repo X |
| **Action** | Ce que la loop fait | Run tests, fix lint, répondre aux reviews |
| **Budget** | Plafond de ressources | Max N sub-agents par tick, token cap |
| **Stop** | Condition d'arrêt | Tous les PRs verts, ou 10 itérations, ou $5 dépensés |
| **Report** | Output livré | Post summary to Slack |

**Les 4 loops concrètes de Cherny (confirmé par ses propres posts) :**
- `/loop 5m /babysit` — PR babysitting
- `/loop 30m /slack-feedback` — surveille Slack pour feedback
- `/loop /post-merge-sweeper` — nettoyage post-merge
- `/loop 1h /pr-pruner` — élague les PRs inactives

---

## 4. Vérification et mémoire — le compound Cherny

### La vérification (inner feedback)

*"Giving Claude a way to verify its own work will 2-3x the quality of the final result."*

La vérification doit être **réelle** : l'agent doit pouvoir exécuter ce qu'il a modifié (bash, test suite, app, simulateur iOS/Android, Computer Use), pas juste lint/type-check.

Pour le web : Claude utilise l'extension Chrome pour ouvrir un navigateur, tester les changements UI, itérer. Décrit comme plus efficace en tokens que Playwright ou Chromium MCP.

### La mémoire compound (outer feedback)

*"Every single time Claude makes a mistake, I don't tell it to do it differently. I tell it to write it to the CLAUDE.md, or make a skill. If you can do this, then Claude can just run forever."*

- Son CLAUDE.md partagé fait ~2,500 tokens, mis à jour dès qu'une erreur survient
- Tout le repo partage un seul CLAUDE.md, commité dans git
- Les procédures fréquentes deviennent des slash commands dans `.claude/commands/`
- Pattern antérieur à Claude Code : Cherny notait les commentaires de code review récurrents dans un spreadsheet et écrivait une lint rule après 3-4 occurrences

### Le modèle de permission

- Auto mode remplace l'approbation manuelle par un classifieur de sécurité
- Deux couches : probe d'injection de prompt (server-side) + classifieur de transcript (output)
- 93% des prompts approuvés automatiquement (chiffre Anthropic, pas 99%)
- 0.4% false-positive, 17% false-negative sur datasets internes
- **Pas un drop-in replacement pour l'infrastructure critique**

---

## 5. Cat Wu — le pendant opérationnel

Cat Wu (engineering lead Claude Code chez Anthropic) décrit deux routines « watch-for-work » :

1. **Routine de fix automatique** — écoute chaque ticket, GitHub issue, et bug report vocal ; met proactivement un fix + PR
2. **Routine de bug orphelin** — trouve les bug reports sans réponse depuis ~5h et met un fix facile à vérifier et merger

Elle souligne le scaling : *"Synthesizing the memory from a lot of logs is a way to find these patterns more consistently."*

---

## 6. PKA vs Loop Engineering — analyse différentielle approfondie

### Ce que PKA fait DÉJÀ (et souvent mieux)

| Capacité Cherny/Osmani | Équivalent PKA | Avance PKA |
|------------------------|----------------|------------|
| CLAUDE.md (~2.5k tokens) | MEMORY.md + team.db + State files + thread files | Base de données relationnelle vs fichier texte |
| Skills (SKILL.md) | 50+ skills PKA, format identique | Spécialistes nommés + personas |
| Sub-agents | agent_open (31 spécialistes) | Rôles documentés, pas génériques |
| `/goal` (run until condition) | Les 6 loops (forge, bench, edge-ai, seo, sigma, arbor) | Pattern AutoResearch 3 fichiers + arbres d'hypothèses |
| Memory compound (erreur → règle) | pka_memory_capture.py, MEMORY.md, SOUL.md | Automatisé via scripts, pas manuel |
| Verification gate | forge-loop (score ≥ 4/5), bench-loop (dans spec) | Quality gates nommées |
| git worktrees | agent_open (sessions isolées) | Isolation native |
| MCP connectors | pka--* (filesystem, git, github, gcalendar, sqlite) | Connecteurs métier |

### Ce qui MANQUE à PKA (gap analysis)

#### 🔴 P0 — Commande `/loop` unifiée
Aujourd'hui, chaque loop PKA a son propre déclencheur textuel. Cherny a `/loop 5m /babysit`. PKA devrait avoir une syntaxe unifiée :
```
/loop projet action --cadence 1h --until "condition" --budget 5€
```

#### 🔴 P0 — Watch-for-work (le vrai gap)
**C'est le gap le plus profond.** Les loops PKA sont **déclenchées par l'humain** (« forge loop », « bench loop »). Les loops Cherny/Wu sont **déclenchées par des événements externes** — un nouveau ticket GitHub, un commentaire Slack, un bug report. La loop ne dort pas, elle écoute.

PKA n'a pas de mécanisme de veille active qui scrute des canaux externes et déclenche des loops. Exemple : surveiller `00_INBOX/` et déclencher automatiquement `inbox-analysis` quand un fichier apparaît.

#### 🟡 P1 — Compound mémoire automatisé
Cherny : *"Every mistake → CLAUDE.md or skill."* PKA a `pka_memory_capture.py` et `pka_memory_nudge.py` mais le flux « erreur → règle durable » n'est pas aussi serré. Quand Dobby se trompe, est-ce qu'une règle est automatiquement écrite dans SOUL.md ou un skill ?

#### 🟡 P1 — Dashboard de supervision (Agent View)
Cherny décrit l'Agent View : un écran unique montrant « Needs input », « Working », « Completed ». PKA n'a pas de dashboard des loops actives.

#### 🟡 P1 — Orchestration cross-loop
Une loop Cherny peut en déclencher une autre. Exemple : routine de bug orphelin → PR → `/babysit` surveille le PR. PKA n'a pas de chaînage automatique entre loops.

#### ⚪ P2 — Cloud routines (persistence post-session)
Cherny utilise `/schedule` pour que les loops tournent même laptop fermé. PKA a `automation_create` mais l'exécution dépend de la session active.

#### ⚪ P2 — Hundreds of agents
Cherny parle de « quelques centaines d'agents » lisant GitHub/Slack/Twitter. C'est un scaling que PKA n'a pas encore — mais qui n'est pas nécessaire à l'échelle de JC.

---

## 7. Leçons pour PKA

### Leçon 1 : La vérification est le moteur
Cherny martèle que la loop n'avance QUE quand une vérification externe (test, build, checker) dit qu'elle a réussi. Les loops PKA ont déjà ce pattern (forge-loop : score ≥ 4/5) mais certaines loops (arbor-research) pourraient bénéficier d'une gate de vérification plus explicite.

### Leçon 2 : Chaque erreur → règle durable
Le compound Cherny est le plus puissant : *"If you can do this, then Claude can just run forever."* PKA a les outils mais pas le réflexe systématique. Proposer un workflow : à chaque erreur de Dobby, écrire automatiquement dans SOUL.md ou créer/mettre à jour un skill.

### Leçon 3 : L'interface monte d'un niveau d'abstraction
Code → Prompt → Loop → ?. Le prochain niveau pour PKA serait : **des loops qui conçoivent des loops**. C'est exactement ce que fait déjà arbor-research (hypothèse → expérience → insight), mais pas encore pour l'infrastructure elle-même.

### Leçon 4 : Watch-for-work > wait-for-command
Le passage du stade 2 au stade 3 de Cherny n'est pas juste technique — c'est un changement de posture. Au lieu d'attendre qu'on lui dise quoi faire, le système écoute les canaux et propose proactivement. Pour PKA, ça pourrait être : surveiller `00_INBOX/`, surveiller les state files périmés, surveiller les deadlines qui approchent.

---

## 8. Actions révisées (post-analyse approfondie)

| Priorité | Action | Détail | Effort |
|----------|--------|--------|--------|
| 🔴 P0 | **Commande `/loop` unifiée** | Wrapper bash/script sur les 6 skills de loop existants + les 6 paramètres d'anatomie (trigger/scope/action/budget/stop/report) | 3-4h |
| 🔴 P0 | **Watch-for-INBOX** | Automatisation : surveiller `00_INBOX/` → détecter nouveau fichier → déclencher `inbox-analysis` automatiquement | 2h |
| 🟡 P1 | **Compound mémoire** | Workflow : erreur Dobby → proposition règle SOUL.md/skill → validation JC → commit | 3h |
| 🟡 P1 | **Dashboard loops** | Page HTML statique : loops actives, statut, dernière exécution, prochaine échéance | 3h |
| 🟡 P1 | **Watch-for-deadline** | Surveiller `roadmap-90-jours.md` et `etat-projets.md` → alerter 7j avant deadline | 2h |
| ⚪ P2 | **Orchestration cross-loop** | Event bus : bench-loop OK → trigger forge-loop → trigger rapport | 1-2j |
| ⚪ P2 | **Cloud routines** | `automation_create` avec persistence post-session | 1j |

---

## 9. Sources primaires consultées

| Source | URL | Type |
|--------|-----|------|
| Addy Osmani — Loop Engineering (essai original) | addyosmani.com/blog/loop-engineering/ | confirmed-primary |
| Cocode — Loop Engineering Field Guide (11 docs) | github.com/cocodedk/loop-engineering | confirmed-primary (compilation) |
| Boris Cherny — Acquired Unplugged (WorkOS) | youtube.com/watch?v=RkQQ7WEor7w | confirmed-primary |
| Boris Cherny — X/Threads posts | x.com/bcherny, threads.com/@boris_cherny | confirmed-primary |
| howborisusesclaudecode.com | howborisusesclaudecode.com | confirmed-secondary |
| Cat Wu — The Neuron interview | theneuron.ai | confirmed-secondary |
| Anthropic Engineering — Auto Mode | anthropic.com/engineering/claude-code-auto-mode | confirmed-primary |
| Fortune Brainstorm Tech — Cherny | fortune.com/2026/06/11/ | confirmed-secondary |
| BD TechTalks — Demystifying loop engineering | bdtechtalks.com/2026/06/22/ | confirmed-secondary |

---

*Analyse complétive. Met à jour et approfondit le livrable initial du 2026-07-17.*
