---
name: decision-gate
description: Garde-fou pré-action — questions fermées avant toute action sensible (destructif, sortant, secrets, conformité) avec seuils de confiance et journal de décision. Déclencher sur "garde-fou", "decision gate", "gate", et automatiquement avant toute action destructive ou sortante. Inspiré du pattern Jev/TypeSafe (modèle de décision calibré) et du garde-fou Warden de Claude Code.
---

# Skill — decision-gate

> Le garde-fou. Inspiré du modèle de décision calibré **Jev** (TypeSafe, sept. 2026) et du garde-fou **Warden** de Claude Code. Transposé à PKA : on tourne en **YOLO** (auto-approve), donc personne n'est dans la boucle. Ce skill réintroduit une boucle humaine *uniquement là où ça compte* — les actions destructives, sortantes, ou qui touchent aux secrets.

## Concept

Un agent en YOLO, laissé seul, enfreint les règles ~6 fois sur 150 actions. Avec un garde-fou à questions fermées : **zéro**. Le principe n'est pas de ralentir tout, mais de faire le tri :

- **Blocage absolu** — une courte liste d'actions interdites d'office, sans score.
- **Questions fermées** — pour le reste, 4 questions oui/non qui produisent un score de risque.
- **Seuil → escalade** — risque élevé = bloquer, risque moyen = demander à JC, risque faible = continuer.
- **Journal** — chaque décision et correction est loggée, et sert à affiner les seuils.

Le décideur ne rédige pas, il *tranche*. On ne lui confie que ce qui se lit dans le texte : liste fermée, erreur rattrapable. Trier une action : oui. Évaluer un calcul : non.

## Déclencheurs

- **Automatique** — avant toute action qui entre dans les catégories sensibles ci-dessous (destructive, sortante, secrets, écriture protégée).
- **Explicite** — « gate », « garde-fou », « decision gate », « vérifie cette action ».

Les lectures, recherches et greps bénins ne déclenchent **pas** la gate (aucun log). Elle reste cheap — on ne paie une vérification que sur ce qui peut casser.

## Les 4 questions fermées

Avant d'exécuter, répondre oui/non avec une confiance (0–1) :

| # | Question | Si oui → |
|---|----------|----------|
| **G1** | L'action est-elle **destructive et irréversible** ? (`rm -rf`, `DROP TABLE`, `git reset --hard`, écrasement d'un State sans backup) | Blocage absolu |
| **G2** | L'action **envoie-t-elle quelque chose hors de la machine** ? (mail, push, POST API, notification, publication, SSH distant) | Escalade systématique |
| **G3** | L'action **lit/écrit un secret** ou touche `JCH_PRIVATE/` ? (token, password, clé API, credentials) | Escalade ou blocage |
| **G4** | L'action **contredit-elle une règle** de `SOUL.md` / `AGENTS.md` / `CLAUDE.md` / `securite-sauvegardes.md` ? | Escalade ou blocage |

**G2 est la question-clé** (celle du Warden) : *« est-ce que cette action envoie quelque chose hors de ma machine ? »*. Si c'est possible, on demande. **Un mail ne part jamais sans JC.**

## Liste de blocage absolu (sans score, toujours bloqué)

| Action | Règle source |
|--------|-------------|
| `rm -rf` sur un dossier non-`tmp` | securite-sauvegardes.md règle 2 |
| `git push --force` / `git rebase` réécrivant l'historique | règle 2 |
| `DROP TABLE` / suppression team.db sans backup préalable | règle 2 |
| Exposer un secret (log, commit, réponse visible) | règle 1 |
| Écraser un State file (`etat-projets.md`, `hardware-state.md`) sans lire l'état actuel | constitution mémoire State/Log |
| Envoi mail/message sans confirmation JC | règle 1 + Warden |

## Seuils de confiance → décision

Le score de **risque** (0 = bénin, 1 = dangereux) est le max des confiances des questions déclenchées.

| Risque | Décision | Effet |
|--------|----------|-------|
| **≥ 0.8** | 🛑 **BLOQUER** | Ne pas exécuter. Signaler à JC et attendre. |
| **0.5 – 0.8** | ⚠️ **ESCALADER** | Poser la question à JC avant d'agir. |
| **< 0.5** | ✅ **AUTORISER** | Action bénigne, continuer sans interruption. |

**Exception :** G2 (sortant) escalade *toujours*, quel que soit le score — on ne devine pas si un mail ou un push peut partir.

## Mode fantôme (démarrage par défaut)

Au démarrage, le skill est en **mode fantôme** : il n'agit pas, il note son avis *à côté* des décisions réelles.

1. Pendant **100–200 cas**, Dobby log chaque action sensible avec son verdict et laisse la décision inchangée.
2. On compare verdict du garde-fou vs décision réelle (et corrections JC).
3. Quand le garde-fou est calibré (ses verdicts correspondent à ce que JC aurait décidé), on **active l'enforcement** : seuls les seuils ≥ 0.8 et la liste de blocage sont automatisés.

**Activer l'enforcement** : `bin/pka-gate enforce` — **Repasser en fantôme** : `bin/pka-gate ghost`.

Commandes du script `bin/pka-gate` : `status`, `ghost`, `enforce`, `check "<commande>"`, `log --action … --g1… --verdict …`, `tail [N]`, `reset --yes`.

## Journal de décision

Chaque décision est loggée en JSONL dans `_local/state/decision-gate.log` :

```json
{"ts":"2026-10-27T10:00:00","action":"git push --force origin main","G1":0.95,"G2":0.9,"G4":0.0,"risque":0.95,"verdict":"BLOC","mode":"fantome","jc":"-"}
```

- Les corrections JC (« non, là tu aurais dû bloquer / laisser passer ») sont réinjectées via **compound-memoire** : erreur → règle → affinage des seuils.
- Après quelques centaines de corrections, on sait exactement où placer les seuils — on ne les fige pas au premier jour.

## Règles absolues

- **Ne jamais contourner la gate** pour une action qui entre dans les catégories sensibles. Si la gate bloque et qu'on passe outre, c'est une violation de `securite-sauvegardes.md`.
- **La liste de blocage est prioritaire** sur tout score — elle ne se négocie pas.
- **G2 escalade toujours.** Aucun envoi hors machine sans JC.
- **Le journal est la donnée** qui affine les seuils. Ne pas le supprimer ; le faire tourner en compound-memoire.
- **En mode fantôme, ne rien bloquer** — observer et logger, sinon on fausse la calibration.

## Format de sortie

```
DECISION-GATE REPORT
Action        : <commande/opération>
Questions     : G1=<0-1> G2=<0-1> G3=<0-1> G4=<0-1>
Risque        : <0-1>
Verdict       : BLOQUER / ESCALADER / AUTORISER
Mode          : fantôme / enforce
Justification : <une phrase — pourquoi ce verdict>
```

## Intégrations

- **`securite-sauvegardes.md`** — source des règles de blocage (règles agent 1–4).
- **`compound-memoire`** — transforme chaque correction JC en règle durable ou en affinage de seuil.
- **`SOUL.md` / `AGENTS.md`** — G4 vérifie chaque action contre les règles de comportement.
- **`JCH_PRIVATE/credentials-central.md`** — G3 référence les secrets par variable d'environnement, jamais en clair.
- **`forge-loop`** — partage le principe « la métrique / la règle est immuable, l'agent ne la contourne pas ».

## Références

- **Jev / TypeSafe AI** (sept. 2026) — modèle de décision calibré : liste fermée, confiance calibrée, seuil → escalade.
- **Warden** (garde-fou Claude Code sur Jev) — blocage des actions destructives, vérification contre `CLAUDE.md`, question « envoie hors machine ? ».
- **Andrej Karpathy — llm-wiki** (avril 2026) — journal du wiki comme source de calibration des seuils.
