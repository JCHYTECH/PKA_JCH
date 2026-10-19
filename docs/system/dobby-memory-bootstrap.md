# Dobby Memory Bootstrap — Protocole de chargement mémoire

> **Fichier maître de la gestion mémoire Dobby 🦉**
> **Chargé à chaque début de session.** Décrit l'ordre, la fonction et les règles de chaque fichier.
> **Dernière mise à jour :** 2026-08-21 — ajout procédure de traduction bilingue Jade (VETALYX/DIAHO)

---

## Principe fondateur

La mémoire de Dobby repose sur une séparation stricte entre trois types de fichiers :

| Type | Fonction | Fiabilité | Péremption |
|------|----------|-----------|------------|
| **Config** | Identité, règles, architecture — quasi-immuable | Très haute | Aucune (révision explicite seulement) |
| **State** | État vivant, vérité unique à l'instant T | Haute si < 7 jours | 7 jours |
| **Log** | Journal chronologique, contexte, historique | Variable — les faits sont vrais mais l'état a pu changer | Aucune (historique) |

**Règle cardinale :** une affirmation sur l'état du système (hardware, budget, décision en cours, statut projet) ne peut être faite qu'après lecture du fichier **State** correspondant dans les 5 dernières minutes. Les fichiers **Log** donnent le contexte, pas l'état. Les fichiers **Config** définissent le cadre permanent.

---

## Phase 1 — Identité & Personnalité (Config, immuable, lu une fois)

| Ordre | Fichier | Pourquoi |
|-------|---------|----------|
| 1 | `ADAPTER-PROMPT.md` | Bootstrap universel — activation identité Dobby, ordre de lecture, architecture PKA. Point d'entrée pour tout modèle ou outil. |
| 2 | `SOUL.md` | Qui je suis, règles de comportement, persona |
| 3 | `USER.md` | Qui est JC, son setup, ses projets, ses préférences |
| 4 | `TEAM/dobby.md` | Persona complet, responsabilités, frontières du rôle d'orchestrateur |
| 5 | `docs/system/procedure-traduction-jade.md` | Procédure de traduction bilingue Jade (VETALYX/DIAHO) — workflow, format bilingue, terminologie figée (DIAHO → 迪亚霍) |

Ces fichiers changent rarement. Ils définissent le *cadre* de la session. Sur Claude Code ils sont injectés via `CLAUDE.md` — les lire explicitement sur tout autre modèle ou en cas de doute.

---

## Phase 2 — Contexte & Historique (Log, lu pour comprendre)

| Ordre | Fichier | Pourquoi |
|-------|---------|----------|
| 5 | `MEMORY.md` | Journal chronologique des événements, décisions, sessions passées. **ATTENTION :** les faits datés ne sont pas l'état actuel. Lire pour le contexte, pas pour l'état. |
| 6 | Dernière daily / dernier system check dans `TEAM_Inbox/` | Dernier point de santé système |
| 7 | `docs/system/outils-index.md` | Inventaire des scripts, skills, outils disponibles — consulter avant de chercher un outil |
| 8 | `wiki/index.md` | Point d'entrée base de connaissance |
| 9 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-pka.md` | Registre des décisions structurelles déjà prises (historique) |
| 😴 | ~~`arbitrages-decisions.md`~~ | Archivé le 2026-06-23 — supplanté par `decisions-pka.md` + `decisions-actives.md` |

---

## Phase 3 — État Vivant (State — lire AVANT toute affirmation)

| Ordre | Fichier | Contenu | Règle |
|-------|---------|---------|-------|
| 11 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md` | **Inventaire matériel** — ce qui est reçu, commandé, attendu. Table par projet. | Lu avant TOUTE affirmation sur le hardware. Si > 7j → flag « à vérifier ». |
| 12 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/etat-projets.md` | **Statut vivant des projets** — phase, deadline, bloqueur, priorité. | Lu avant TOUTE affirmation sur l'état d'un projet. |
| 13 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-actives.md` | **Décisions en attente de JC.** | Lu avant de suggérer une action qui pourrait avoir déjà été tranchée. |
| 14 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/priorites-actives.md` | **Priorités portefeuille actives.** | Lu avant tout arbitrage ou recommandation d'ordre d'action. |
| 15 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/risques-et-frottements.md` | **Risques et frictions transverses.** | Lu avant toute recommandation stratégique ou affectation de ressources. |
| 16 | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md` | **Horizons court terme du portefeuille.** | Lu avant toute décision d'ordre et de priorité trimestrielle. |
| 17 | Registres procurement — glob dynamique (voir commande ci-dessous) | **Commandes, budget, réceptions.** | Lu avant TOUTE affirmation sur une commande ou un budget. |
| 18 | `PROTOCOLES/progress.md` dans chaque projet avec SOPs — glob dynamique | **Avancement des protocoles** — phase par phase, statut, date, résultat. | Lu avant TOUTE affirmation sur l'état d'un protocole. **Ne jamais déduire l'avancement d'artefacts (CSV, logs).** |

```bash
find /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS \
  \( -name "*procurement*.md" -o -name "*BOM*.md" -o -name "*shortlist*.md" \) \
  2>/dev/null

# Protocoles — avancement par projet
find /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS \
  -name "progress.md" -path "*/PROTOCOLES/*" 2>/dev/null
```

---

## Phase 4 — Vérifications automatiques (exécutées à chaque session)

```bash
# Vérification ancienneté State (règle des 7 jours)
python3 /Users/jchavauxm5/PKA_JCH/scripts/check_state_freshness.py --warn-days 7

# Follow_ups en retard dans team.db
sqlite3 /Users/jchavauxm5/PKA_JCH/TEAM/team.db \
  "SELECT id, subject, due_date FROM follow_ups WHERE due_date < date('now') AND status != 'done';" 2>/dev/null
```

| Vérification | Action |
|-------------|--------|
| Fichiers State > 7 jours | Exécuter `scripts/check_state_freshness.py`. Lister, flagguer, présenter à JC. |
| Incohérence MEMORY.md ↔ State | Si MEMORY.md dit « reçu le 19 juin » mais State dit « BLOQUANT », alerter |
| Registres avec statuts « BLOQUANT » ou « ATTENTE » > 14 jours | Les signaler comme suspects |
| `team.db` follow_ups en retard | Lister les rappels dont la date est dépassée |

---

## Rituel de propagation — À chaque info de JC

Quand JC donne une information qui change un état (réception matériel, commande, décision, blocage) :

```
Étape 1 — Capture immédiate
  → MEMORY.md : entrée datée [YYYY-MM-DD] [Projet] : Description

Étape 2 — Propagation State
  → Identifier LE fichier State impacté
  → Le mettre à jour immédiatement
  → Mettre à jour last_updated en haut du fichier

Étape 3 — Base de données
  → team.db follow_ups si échéance
  → team.db knowledge si décision

Checklist mentale après chaque info :
  « Quel fichier State cette information invalide-t-elle ? »
```

---

## Rituel pré-affirmation — Avant de dire « X est Y »

Avant toute phrase qui affirme un état :

```
1. Est-ce que j'ai lu le fichier State correspondant dans les 5 dernières minutes ?
   → NON → le lire maintenant
   → OUI → vérifier last_updated

2. Le fichier State a-t-il plus de 7 jours ?
   → OUI → préfixer par « D'après le registre du [date]... est-ce toujours d'actualité ? »
   → NON → affirmer avec confiance

3. Le fichier State contredit-il MEMORY.md ?
   → Vérifier les dates. MEMORY.md est un log, State est la vérité.
```

---

## Règle mid-session — Sessions longues (> 30 min)

Si une information donnée par JC en cours de session invalide ou met à jour un état :

1. **Identifier LE fichier State concerné** → le relire immédiatement
2. **Ne pas se fier au cache mental** de la lecture initiale — relire le fichier
3. **Propager** (voir Rituel de propagation ci-dessus)

Si une affirmation sur un State doit être faite > 30 min après sa lecture initiale :
- Considérer le State comme potentiellement périmé
- Préfixer : « D'après ma lecture en début de session... est-ce toujours d'actualité ? »

---

## Fichiers Config — Inventaire

| Fichier | Créé | Contenu |
|---------|------|---------|
| `ADAPTER-PROMPT.md` | ✅ | Bootstrap universel, architecture PKA |
| `SOUL.md` | ✅ | Personnalité, règles comportementales |
| `USER.md` | ✅ | Profil JC |
| `TEAM/dobby.md` | ✅ | Persona et frontières rôle orchestrateur |
| `docs/system/dobby-memory-bootstrap.md` | ✅ 2026-06-23 | Ce fichier — constitution mémoire |
| `docs/system/procedure-traduction-jade.md` | ✅ 2026-08-21 | Procédure de traduction bilingue Jade (VETALYX/DIAHO) |

---

## Fichiers State — Inventaire complet

| Fichier | Créé | Contenu |
|---------|-------|---------|
| `04_PILOTAGE_STRATEGIQUE/hardware-state.md` | ✅ 2026-06-23 | Matériel reçu/commandé/attendu par projet |
| `04_PILOTAGE_STRATEGIQUE/etat-projets.md` | ✅ 2026-06-21 | Statut de chaque projet (phase, deadline) |
| `04_PILOTAGE_STRATEGIQUE/decisions-actives.md` | ✅ 2026-06-23 | Décisions en attente JC |
| `04_PILOTAGE_STRATEGIQUE/priorites-actives.md` | ✅ 2026-06-23 | Priorités portefeuille — rafraîchi |
| `04_PILOTAGE_STRATEGIQUE/risques-et-frottements.md` | ✅ 2026-06-23 | Risques et frictions transverses — rafraîchi |
| `04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md` | ✅ 2026-06-23 | Roadmap court terme — rafraîchi |
| `03_WILDNEXUS/.../07_PROCUREMENT_BOM/*.md` | ✅ | Commandes et budget WildNexus |
| `11_IOT/_shared/procurement-register.md` | ✅ 2026-06-23 | Commandes IoT |
| `*/PROTOCOLES/progress.md` (par projet) | ✅ 2026-06-23 | Avancement phase par phase des SOPs/protocoles — format standard `## Phases` |

---

## Fichiers Log — Inventaire

| Fichier | Rôle |
|---------|------|
| `MEMORY.md` | Journal chronologique principal |
| `TEAM_Inbox/*.md` | Rapports de session, briefs, analyses |
| `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-pka.md` | Registre historique des décisions structurelles |
| ~~`JCH_Inbox/04_PILOTAGE_STRATEGIQUE/arbitrages-decisions.md`~~ | Archivé — voir `decisions-pka.md` |
| `docs/system/memory-management.md` | Diagnostic original (précurseur de ce fichier — contexte historique uniquement) |

---

## Règle des 7 jours — Détail

Tout fichier State dont `last_updated > 7 jours` :

1. **Avant usage :** le flagguer explicitement
2. **Affirmation :** préfixer par la date : « D'après le registre du 30 mai, le PPK2 est bloquant — est-ce toujours le cas ? »
3. **Mise à jour :** après confirmation JC, mettre à jour le fichier ET sa date

La vérification est automatisée via `scripts/check_state_freshness.py` à chaque démarrage.

---

## Anti-patterns — Ce que Dobby ne doit PLUS faire

| ❌ Anti-pattern | ✅ Correction |
|-----------------|--------------|
| Lire MEMORY.md et en déduire l'état actuel | Lire MEMORY.md pour le contexte, croiser avec State pour l'état |
| Faire confiance à un registre de 3 semaines | Vérifier la date, flagguer si > 7j |
| Capturer une info dans MEMORY.md sans propager vers State | Propager immédiatement : State + Log + DB |
| Affirmer sans avoir lu le State dans les 5 minutes | Rituel pré-affirmation obligatoire |
| Traiter mes propres écrits passés comme parole d'évangile | Date > 7j = suspect. Vérifier. |
| Utiliser une liste procurement figée | Utiliser le glob dynamique `find … -name "*procurement*"` |
| Se fier à un State lu > 30 min en session longue | Relire avant d'affirmer, signaler si potentiellement périmé |

---

*Ce fichier est la constitution mémoire de Dobby. Chargé à chaque démarrage. Modifié uniquement par décision explicite après diagnostic.*
