---
name: conseil
description: Délibération structurée multi-perspectives pour décisions difficiles — 5 stances cognitives (Contrarian, Premiers Principes, Expansionniste, Outsider, Prémortem) en parallèle, puis synthèse Dobby en chairman. Pas de débat, pas de vote anonyme. Déclencher sur "passe ça au conseil", "conseil", "pressure-test", "stress-test", "war room", "prémortem", "délibère". Adapté de la méthodologie LLM Council (Andrej Karpathy).
---

# Skill — conseil

> Double lignée : **LLM Council** (Andrej Karpathy) pour la forme « plusieurs avis parallèles + une synthèse séparée », et **`/council`** (Claude Blattman) pour la discipline stricte « critiques parallèles, synthèse séparée, **pas de débat** ». La structure — plusieurs tirages, évaluer l'écart — est la même que Tree of Thoughts (Yao et al., 2023). Dans PKA, Dobby est déjà le chairman : cette skill formalise juste la passe adversariale qui lui manquait.

## Pourquoi

Nos 31 spécialistes sont des experts **par domaine** (Renard = juridique, Vasco = vétérinaire, Araignée = embarqué…). Dobby délègue par sujet, puis synthétise. Mais rien ne force formellement la question « qu'est-ce qui va foirer ici ? ».

Le conseil ajoute une couche **orthogonale** : des **stances cognitives**, pas des sujets. Cinq critiques répondent en parallèle à la même décision, chacun avec un angle de pensée différent, sans jamais voir les réponses des autres. Dobby lit les cinq comme des données et rend un verdict qui **cite et traite la dissidence**.

Cela attaque trois modes de défaillance du LLM seul :
- l'**ancrage** sur la première réponse (les critiques partent d'angles différents) ;
- la **sycophancie** / convergence molle (pas de débat, donc pas d'accord artificiel) ;
- le **curse of knowledge** (l'Outsider répond sans aucun contexte).

## Les 5 stances du panel

| Stance | Question motrice | Ce qu'elle chasse |
|--------|------------------|-------------------|
| **Contrarian** | « Qu'est-ce qui va foirer, et pourquoi ? » | Les modes d'échec, les hypothèses fragiles |
| **Premiers Principes** | « Résout-on le bon problème ? » | Le cadrage erroné, le faux objectif |
| **Expansionniste** | « Quel upside on est en train de rater ? » | L'opportunité invisible, l'option non envisagée |
| **Outsider** | Répond au **libellé brut**, zéro contexte | Le curse of knowledge, les évidences non dites |
| **Prémortem** | « On est dans 6 mois, ça a échoué. Écris le post-mortem. » | Le futur coût d'opportunité, la dépendance fragile |

**Stance optionnelle** — **Méthodologiste** (« la méthode de décision est-elle solide ? les données sont-elles fiables ? ») pour les décisions scientifiques/techniques (où Clio/Sigma sont pertinents).

## Deux modes

| Mode | Stances | Durée | Usage |
|------|---------|-------|-------|
| **CONSEIL RAPIDE** | 2 (défaut : Contrarian + Outsider) | ~30 s | « est-ce que je fais X ou pas ? » — check rapide |
| **CONSEIL COMPLET** | 5 en parallèle (+ Méthodologiste si scientifique) | ~3–4 min | Décision coûteuse, irréversible, ou à fort enjeu |

## Règles absolues

- **Pas de débat.** Les critiques ne se voient jamais. Pas de réplique, pas de vote majoritaire sur le récit. Une seule passe.
- **Dobby = chairman.** Les critiques conseillent, ils ne décident pas. C'est Dobby qui tranche.
- **La dissidence est obligatoire.** Le verdict doit citer la plus forte objection et y répondre. Un verdict sans dissent traité est du théâtre — le skill s'arrête.
- **L'Outsider n'est jamais seedé.** Il reçoit uniquement la question telle que JCH l'a formulée, rien d'autre. C'est toute sa valeur.
- **Garde-fou d'entrée.** Ne pas convoquer le conseil pour une décision réversible à faible coût, une décision déjà tranchée par JCH, ou une simple recherche d'info (ça, c'est Furet/Clio/Milan).

## Hybride PKA : seed par spécialiste de domaine

Les stances tournent **sur le brief du spécialiste concerné**, sauf l'Outsider :

1. Dobby identifie le domaine de la décision → le(s) spécialiste(s) pertinent(s).
2. Dobby génère le brief de domaine (via la skill `brief`) ou extrait l'analyse déjà produite.
3. Chaque critique (sauf Outsider) reçoit : sa stance + le brief de domaine.
4. Les cinq partent en parallèle, indépendants.

Exemple — décision Vetalyx : les critiques sont seedés avec le brief Renard/Vasco. Le conseil ne remplace pas Renard/Vasco ; il stress-teste la **décision** qu'ils ont préparée.

## Procédure

```
Décision difficile ──► Garde-fou ──► Cadrage ──► Composition panel
                                                    │
        ┌───────────────────────────────────────────┘
        ▼
  5 sub-agents en parallèle (agent_open), indépendants
        │
        ▼
  Dobby lit les 5 réponses comme des données
        │
        ▼
  VERDICT : recommandation + dissent cité + réponse
```

### 1. Garde-fou

- Décision **réversible et peu coûteuse** → répondre directement, pas de conseil.
- Décision **déjà tranchée** par JCH → ne pas re-litiger.
- **Recherche d'information** → déléguer au spécialiste de domaine, ce n'est pas un conseil.

### 2. Cadrage

Reformuler la décision en une **question neutre** : la décision à prendre, les options, le critère (réversibilité, coût, irréversibilité).

### 3. Composition du panel

- Choisir le mode : RAPIDE (2 stances) ou COMPLET (5 stances).
- Identifier le(s) spécialiste(s) de domaine → préparer le brief de seed.
- Ouvrir **un sub-agent par stance** (`agent_open`), tous dans le même tour, indépendants. Ne pas utiliser `fork_context` — chaque critique part de son propre contexte.

### 4. Synthèse

Dobby lit les cinq réponses comme des données brutes. Repérer : points de convergence, désaccords, la plus forte objection, et ce que personne n'a dit.

### 5. Verdict

```
CONSEIL — VERDICT
Décision : <question neutre>
Recommandation : GO / NO-GO / CONDITIONNEL (<condition>)
Arguments pour : <2–3>
Arguments contre : <2–3>
Objection la plus forte : <qui la porte> — <l'objection>
Réponse à l'objection : <la réponse, ou l'assomption explicite si on l'accepte>
Résidu de risque : <ce qu'on assume en décidant>
Dissent : <stance(s) en désaccord> maintient/maintiennent que …
```

## Livrable

Le verdict est rendu dans le chat **et** sauvegardé dans `TEAM_Inbox/YYYY-MM-DD_dobby_conseil_[topic].md` (conforme au working agreement).

## Budgets

| Ressource | Plafond |
|-----------|---------|
| Token budget | ~25 000 tokens par conseil complet (5 stances × entrée+sortie courte) |
| Time budget | RAPIDE ~30 s · COMPLET ~4 min |
| Coût | Négligeable — sub-agents V4, input ~$0,14/M |

## Déclencheurs

- « passe ça au conseil », « conseil », « run the council »
- « pressure-test ça », « stress-test ça », « war room »
- « prémortem », « fais un prémortem sur X »
- « délibère », « on en débat ? » (→ répondre par un conseil, pas un débat)

## Skills liés

- **`brief`** — Générer le brief du spécialiste de domaine qui seed les critiques.
- **`arbor-research`** — Pour trancher quelle branche d'hypothèses explorer (le conseil peut servir de gate DECIDE).
- **`forge-loop`** — Même philosophie « gate objective » : forge-loop score le code, conseil stress-teste la décision. Complémentaires, pas interchangeables.

## Références

- **LLM Council** (Andrej Karpathy) — plusieurs modèles en parallèle, synthèse séparée, peer-review anonymisée.
- **`/council`** (Claude Blattman) — critiques parallèles, synthèse séparée, **pas de débat** ; la version dont ce skill s'inspire le plus.
- **Tree of Thoughts** (Yao et al., 2023) — la structure « plusieurs tirages, évaluer l'écart ».
- **llm-council-skill** (Ole Lehmann, communauté) — 5 advisors en sub-agents Claude Code.
