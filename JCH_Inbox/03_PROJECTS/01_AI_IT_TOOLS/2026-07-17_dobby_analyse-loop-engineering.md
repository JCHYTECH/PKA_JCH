# Analyse — Loop Engineering : le marché rattrape PKA

> Dobby 🦉 — DeepSeek V4 — 2026-07-17
> Source : Transcript NoteGPT — Barthélémy Nobili, « Les secrets que les experts IA ne vous disent pas sur le Loop Engineering »
> Validé par : Forge 🔨 (analyse technique), web (DuckDuckGo)

---

## 1. Résumé

Le transcript décrit le « Loop Engineering », un paradigme d'interaction IA formalisé entre le 7 et le 8 juin 2026 par trois figures : **Peter Steinberger** (OpenClaw), **Addy Osmani** (Google), et **Boris Cherny** (Anthropic, Claude Code). L'idée centrale : remplacer le prompt engineering (échange unique humain→IA) par des boucles autonomes où l'IA tourne jusqu'à atteindre un objectif vérifié.

**Conclusion principale : PKA_JCH pratique déjà le Loop Engineering à un niveau avancé, avec ~2 ans d'avance conceptuelle.** Ce que le marché découvre en juin 2026, PKA le fait depuis 2025 via ses 6 skills de loop + arbor-research.

---

## 2. Les 5 briques du Loop Engineering (Osmani) vs PKA

| Brique Osmani | Définition | Équivalent PKA | Maturité |
|--------------|------------|----------------|----------|
| **Automations** | Tâches planifiées, découverte auto, /goal, /loop | `automation_create`, `task_create`, `forge-loop`, `bench-loop` | ✅ Avancé |
| **Worktrees** | Isolation parallèle, pas de collision | `agent_open` (sessions isolées), `task_shell_start` | ✅ Partiel |
| **Skills** | Connaissances projet codifiées, $skill-name | 50+ skills PKA (SKILL.md), format identique à Codex/Claude | ✅ Complet |
| **Plugins/Connectors** | MCP, connecteurs outils externes | MCP pka--* (filesystem, git, github, gcalendar, sqlite) | ✅ Avancé |
| **Sub-agents** | Séparer l'auteur du vérificateur | `agent_open` (30 spécialistes délégables), `forge-loop` (code→review→fix) | ✅ Avancé |
| **Memory externe** | État hors contexte, entre les runs | `MEMORY.md`, `team.db`, `thread files`, `hardware-state.md`, `etat-projets.md` | ✅ Avancé |

**PKA a déjà les 6 briques.** Mais avec une différence architecturale majeure : là où le Loop Engineering standard est une boucle plate (goal→loop→stop), PKA utilise le pattern **AutoResearch (Karpathy) à 3 fichiers** (hypotheses.md, completed.md, disconfirmed.md) + **arbres d'hypothèses cumulatifs** (arbor-research). C'est un Loop Engineering de 2e génération.

---

## 3. Les 6 loops PKA existantes

| Loop | Déclencheur | Pattern | Spécialiste |
|------|------------|---------|-------------|
| **forge-loop** | « forge loop », « code loop » | Code → review → score < 4/5 → auto-fix → repush | Forge 🔨 |
| **bench-loop** | « bench loop », « SOP loop » | SOP → mesure → dans spec ? → commit → SOP suivante | Fourmi 🐜 |
| **edge-ai-loop** | « edge ai loop », « TinyML loop » | Dataset → Edge Impulse → accuracy/latence → commit si mieux | Musaraigne 🦇 |
| **seo-loop** | « seo loop », « optimise SEO » | Page → audit → score < seuil → optimise → re-audit | Trace 📊 |
| **sigma-loop** | « sigma loop », « valide données » | Données → backtesting → écart → ajuste modèle | Sigma 📈 |
| **arbor-research** | « arbor loop », « recherche autonome » | Hypothèse → expérience → insight → décision (arbre cumulatif) | Dobby 🦉 |

**Les 6 loops utilisent déjà le pattern /goal natif :** boucler jusqu'à ce qu'une condition de succès soit atteinte (score ≥ 4/5, mesures dans la spec, accuracy > seuil).

---

## 4. Ce que PKA fait MIEUX que le Loop Engineering standard

1. **Mémoire externe structurée** — Pas juste un fichier markdown : `team.db` (SQLite avec FTS5), `MEMORY.md` (journal), State files (hardware, projets, priorités). Le Loop Engineering d'Osmani mentionne « a markdown file » — PKA a une base de données relationnelle.
2. **Arbres d'hypothèses** — arbor-research est un Loop Engineering cumulatif : chaque cycle ne recommence pas de zéro, il hérite de l'arbre d'hypothèses du cycle précédent. Le marché n'a pas encore ce concept.
3. **Spécialistes nommés** — Là où le Loop Engineering standard parle de « sub-agents » génériques, PKA a 31 spécialistes avec personas, responsabilités, et frontiers documentés.
4. **6 principes architecturaux** — `docs/system/principes-architecturaux.md` donne un cadre de gouvernance que le Loop Engineering standard n'a pas encore.

---

## 5. Ce qui MANQUE à PKA

### 🔴 P0 — Commande unifiée `/loop`
Aujourd'hui, lancer une loop PKA nécessite de connaître le skill exact et son déclencheur (« forge loop », « bench loop », etc.). Le transcript montre Claude Code avec `/goal` et `/loop` comme primitives natives. PKA devrait avoir une commande unifiée :
```
/loop projet action --cadence 1h --until "condition"
```
**Effort estimé :** 2-3h (script wrapper + doc). **Impact :** adoption immédiate par JC.

### 🟡 P1 — Orchestration cross-loop
Aujourd'hui, les loops PKA sont indépendantes. Une loop ne peut pas en déclencher une autre automatiquement. Exemple : `bench-loop` passe un test → déclenche `forge-loop` pour commit review. Ou : `arbor-research` découvre une hypothèse → déclenche `edge-ai-loop` pour la tester sur hardware.
**Effort estimé :** 1-2 jours (event bus interne ou fichier trigger). **Impact :** loop composables, workflows complexes.

### 🟡 P1 — Dashboard de supervision des loops
Aujourd'hui, aucune visibilité centralisée sur l'état des loops en cours. Un dashboard minimal (page HTML ou commande `/loops status`) qui montre : loop active, dernière exécution, statut, prochaine échéance.
**Effort estimé :** 2-3h (read des state files + HTML statique). **Impact :** visibilité, confiance.

### ⚪ P2 — `/loop` avec persistence post-session
Le transcript montre Claude Code qui propose de continuer la loop après fermeture de session. PKA n'a pas ça — une loop s'arrête avec la session. `automation_create` + `task_create` pourraient servir de base.
**Effort estimé :** 1 jour. **Impact :** loops vraiment autonomes 24/7.

---

## 6. Impact cross-projet

| Projet | Impact | Note |
|--------|--------|------|
| **AI_IT_TOOLS** | 🔴 Majeur | C'est le projet directement concerné — les loops sont des outils PKA |
| **WILDNEXUS** | 🟡 Élevé | bench-loop + edge-ai-loop déjà actives, bénéficieraient de l'orchestration |
| **IOT** | 🟡 Élevé | Les loops pourraient automatiser les tests de déploiement Lupo |
| **NEXUS_ACOUSTIC** | 🟢 Modéré | edge-ai-loop applicable aux modèles audio |
| **ARTEON/WildLens** | 🟢 Modéré | seo-loop applicable au contenu éditorial |
| **PHOTO_NATURE** | ⚪ Léger | Impact indirect |
| **VETALYX** | ⚪ Léger | Impact indirect |

---

## 7. Actions proposées

| Priorité | Action | Qui | Deadline |
|----------|--------|-----|----------|
| 🔴 P0 | Créer commande `/loop` unifiée (wrapper skills existants) | Forge | 21 juillet |
| 🟡 P1 | Spécifier orchestration cross-loop (event triggers) | Dobby + Forge | 31 juillet |
| 🟡 P1 | Dashboard supervision loops (HTML statique) | Forge | 31 juillet |
| ⚪ P2 | Loop persistence post-session (automation_create) | Forge | Août |

---

## 8. Web validation

| Claim | Source | Statut |
|-------|--------|--------|
| Peter Steinberger — post viral 7 juin 2026 | OpenClaw creator, tweet 7M vues | ✅ Confirmé |
| Addy Osmani — essai « Loop Engineering » 8 juin 2026 | addyosmani.com/blog/loop-engineering/ + Substack | ✅ Confirmé |
| Boris Cherny (Anthropic) — « I don't prompt Claude anymore » | Claude Code creator, VentureBeat, GitHub cocodedk | ✅ Confirmé |
| Claude Code — commandes /goal et /loop | Documentation Claude Code | ✅ Confirmé |
| 5 briques + mémoire externe | Essai Osmani, vérifié sur addyosmani.com | ✅ Confirmé |

---

*Analyse terminée. Source déplacée vers `03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/`.*
