# Veille — DeepSeek SuperAgent / Harness : leçons pour l'orchestration PKA

> 2026-11-06 par Dobby 🦉 — analyse de 3 transcripts NoteGPT sur l'orchestration d'agents IA (DeepSeek SuperAgent + DeepSeek Harness + Harness Maxing).
> Sources (routées dans `03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/deepseek-superagent_2026-11-06/`) :
> 1. `NoteGPT_Transcript_DeepSeek lance un concurrent OPEN SOURCE à Claude Code !.txt`
> 2. `NoteGPT_Transcript_DeepSeek dévoile son SuperAgent — il travaille à ta place !.txt`
> 3. `NoteGPT_Transcript_OpenClaw et Hermes Agent ont un sérieux concurrent (et c'est gratuit).txt`

---

## 1. Ce que disent les sources

### DeepSeek SuperAgent (sources 1 & 2)
- **Architecture routeur + workers** : un agent « chef » (routeur) reçoit les requêtes et distribue le travail à des agents « ouvriers » (workers), chacun dans son propre workspace, en parallèle.
- **4 piliers** : continuité (vue projet persistante), productivité (parallélisme), proactivité (surveille les événements, agit si les règles le permettent), persistance (reprend le travail plus tard).
- **Routeur léger / workers lourds** : le routeur ne fait que comprendre + distribuer → modèle léger ; les workers font le travail → modèle fort.
- **Batching** : quand le routeur est occupé, il groupe les requêtes → décision 6,4 s → 1,6 s par événement.
- **Routage direct des follow-ups** : les commentaires vont directement au worker concerné, sans repasser par le routeur (économie de tokens).
- **Sécurité** : mode observation (l'agent note ce qu'il ferait sans agir), pas de merge automatique (approbation humaine requise), personnes autorisées seulement.

### DeepSeek Harness (source 1)
- Infrastructure à **plugins** (tout est plugin, façon Lego) — on ajoute/retire des capacités sans refondre.
- **Creator mode** : on demande à l'agent de développer un nouveau plugin pour son propre environnement.
- **Benchmark Frontier Harness Eval** : même modèle (DeepSeek V3), 9 harness. **DeepSeek Harness Creator = 63,3 % = Claude Code**, mais **médiane 3,28 $ vs 18,34 $ (5,6× moins cher)**.

### Harness Maxing (source 3)
- Harnais auto-hébergé 24/7 (VPS), accessible par Telegram + web app.
- **Mémoire « Projets + Topics »** : la mémoire est organisée par projet puis par topic (fichiers). Chaque session **hérite automatiquement** de la mémoire de son topic/projet — on ouvre N sessions parallèles sans redonner le contexte.
- **Limite documentée : 3–5 sessions actives en parallèle** — au-delà, on passe plus de temps à gérer qu'à avancer.

---

## 2. Ce que PKA a déjà (pas besoin de réinventer)

| Idée des sources | Équivalent PKA | Statut |
|---|---|---|
| Routeur + workers | Dobby + 31 spécialistes | ✅ |
| Observation mode / pas d'auto-merge | decision-gate (mode fantôme, 27/10) | ✅ |
| Creator mode / auto-extension | `skill-creator`, `onboarding-specialiste`, `plugin-creator` | ✅ |
| Multi-modèles | Claude, DeepSeek, Gemini, Kimi, Codex, Qwen | ✅ |
| Mémoire persistante | MEMORY.md + team.db + thread files | ✅ (voir §3.1) |

---

## 3. À incorporer (priorisé)

### 3.1 — Mémoire par « topic » (le plus fort)
**Idée.** Raffiner les thread files : sous chaque projet, un niveau « topic » (sous-thème), avec un fichier mémoire par topic. Une session Dobby hérite de la mémoire du topic par défaut, sans recharger tout le projet.
**Bénéfice.** JC ouvre 5+ sessions parallèles sans redonner le contexte à chaque fois.
**Concrètement.** Convention `topic-<slug>.md` par sous-thème, liée depuis le `thread-<projet>.md`. Dobby charge le topic au démarrage de session. *À valider avec le skill `pka-thread-file`.*

### 3.2 — Routeur léger / workers lourds
**Idée.** Le tri/routing de l'inbox et la gateway tournent sur un **modèle léger** (ex. `deepseek-v4-flash`, ou un petit modèle Ollama local) ; les spécialistes gardent le modèle fort.
**Bénéfice.** Coût réduit (même logique que le benchmark : 5,6× moins cher à qualité égale), sans dégrader le travail de fond.
**Concrètement.** Règle de routage : classement/qualification → flash ; production/brief → modèle fort. À appliquer dans la gateway (`pka_gateway.py`) et le tri inbox.

### 3.3 — Batching + routage direct des follow-ups
**Idée.** La gateway batche les entrées inbox (au lieu de traiter 1 à 1) ; un follow-up d'un brief va directement au spécialiste concerné, sans ré-orchestration complète.
**Bénéfice.** Moins de tokens, décision plus rapide sous charge.
**Concrètement.** File d'attente batchée dans `pka_gateway.py` + routage direct des relances.

### 3.4 — Limite « 3–5 projets actifs en parallèle »
**Idée.** Plafonner le nombre de projets actifs simultanés pour éviter la dispersion (déjà un risque identifié : « Dispersion JCH — 10 projets, focus dilué »).
**Bénéfice.** JC reste sous le seuil où la gestion dépasse l'avancement.
**Concrètement.** Règle de pilotage : pas plus de ~4 projets actifs (1 P0 + 3 autonomes) ; le reste en veille/gelé.

---

## 4. Décisions prises (2026-11-06)

- Adopter la **règle « 3–5 projets actifs max »** (pilotage).
- Adopter la **convention « routeur léger / spécialistes lourds »** (routage modèle).
- **Mémoire par topic** (3.1) → **implémentée** : `topic-file-template.md` + section « Topics » du skill `pka-thread-file` + démo `11_IOT/topic-zigbee.md`.
- **Batching + routage direct** (3.3) → **implémenté** : `group_key()` + `route_followups()` + rapport coalescé dans `pka_gateway.py`.

*Veille Dobby — à rapprocher de `docs/system/instructions-systeme.md` et de la matrice des modèles (`matrice-modeles.md`).*
