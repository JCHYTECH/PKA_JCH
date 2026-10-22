---
name: pka-thread-file
description: Living document par projet — overview/statut/décisions persistant, mis à jour en fin de session (PAS automatiquement — voir règle de fraîcheur). Déclencher sur "thread file", "update thread", "met à jour le thread", ou en fin de session projet.
---

# Skill — pka-thread-file

> Living thread file par projet PKA. Inspiré du « Threads Memory System » d'Ev Chapman, adapté à l'architecture PKA (State/Log, team.db, vérifications).

## ⚠️ Règle de fraîcheur (2026-10-22)

**La mise à jour n'est PAS automatique.** Le libellé « mis à jour automatiquement »
était faux : au 2026-10-22, **4 thread files sur 8 avaient 3+ mois de retard**
(AI_IT_TOOLS, ARTEON, PHOTO_AI_JURY : 03/07 · WILDNEXUS : 05/07) et
**07_TRAVELS n'en avait aucun** malgré 729 fichiers.

Avant de citer un thread file comme source :
1. **Vérifier sa date** dans l'en-tête (`Dernière mise à jour`)
2. Si > 30 jours **et** que le projet a bougé depuis → mettre à jour d'abord
3. Ne jamais présenter un thread périmé comme l'état actuel

Complément : un thread file **absent** est un signal de pilotage manquant,
pas une preuve que le projet est inactif (cas TRAVELS : 647 lieux validés).

## Architecture

Chaque projet actif a un fichier `thread-[projet].md` dans `JCH_Inbox/03_PROJECTS/[DOSSIER_PROJET]/`.

Template canonique : `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/thread-file-template.md`

## Déclencheurs

- "thread [projet]" → lit le thread file du projet
- "update thread [projet]" → met à jour le thread file
- "save" / "/save" en fin de session → met à jour tous les thread files touchés
- Automatique : après chaque action significative sur un projet, Dobby évalue si le thread file doit être rafraîchi

---

## Phase 1 — Lecture (début de session ou switch projet)

Quand JC dit « thread [NOM_PROJET] » ou quand Dobby détecte qu'on travaille sur un projet :

1. Chercher `thread-[projet].md` dans `JCH_Inbox/03_PROJECTS/[DOSSIER]/`
2. Si trouvé → lire intégralement → injecter dans le contexte
3. Si absent → proposer de le créer depuis le template
4. Appliquer la règle des 7 jours : si `last_updated > 7j` → flagger

**Format de lecture silencieuse** : ne pas narrer la lecture. Simplement utiliser les infos pour le contexte.

---

## Phase 2 — Mise à jour (fin de session ou commande explicite)

Quand JC dit « update thread [projet] » ou en fin de session :

1. Mettre à jour le header : date, statut
2. Mettre à jour **Vue d'ensemble** si le cap a changé
3. Mettre à jour **État actuel** — chaque axe (Global, Hardware, Software, Documentation)
4. Ajouter les **Décisions clés** prises pendant la session
5. Mettre à jour **Prochaine étape** — action + deadline + responsable
6. Ajouter une entrée dans **Historique sessions** : date + résumé + livrable `TEAM_Inbox/`
7. Vérifier les **Liens** — INDEX, ADRs, hardware-state, budget

**Règle** : ne pas effacer l'historique. Ajouter en haut des sections, pas écraser.

---

## Phase 3 — Vérification (post-update)

Après chaque mise à jour :

1. Vérifier que le thread file n'entre pas en contradiction avec :
   - `etat-projets.md` — le statut projet doit correspondre
   - `hardware-state.md` — les composants listés doivent matcher
   - `roadmap-90-jours.md` — les deadlines doivent être cohérentes
2. Si incohérence → flagger dans le rapport à JC
3. Marquer `last_updated` à la date du jour

---

## Projets avec thread files

| Projet | Dossier | Thread file |
|--------|---------|-------------|
| WILDNEXUS | `03_WILDNEXUS/` | `thread-wildnexus.md` |
| ARTEON | `02_ARTEON/` | `thread-arteon.md` |
| IOT | `11_IOT/` | `thread-iot.md` |
| PHOTO_NATURE | `06_PHOTO_NATURE/` | `thread-photo-nature.md` |
| PHOTO_AI_JURY | `05_PHOTO_AI_JURY/` | `thread-photo-ai-jury.md` |
| VETALYX | `08_VETALYX/` | `thread-vetalyx.md` |
| AI_IT_TOOLS | `01_AI_IT_TOOLS/` | `thread-ai-it-tools.md` |
| TRAVELS | `07_TRAVELS/` | `thread-travels.md` |
| NEXUS_ACOUSTIC | `03_WILDNEXUS/NEXUS_ACOUSTIC/` | `thread-nexus-acoustic.md` |
| InsectNet | `03_WILDNEXUS/INSECTNET/` | `thread-insectnet.md` |

---

## Exemple d'utilisation

```
JC: « thread wildnexus »
Dobby: [lit silencieusement thread-wildnexus.md → contexte chargé]
       « JC — WildNexus : firmware 🟡, SOP-08 caméra en attente (15/07), panier Mouser ~279€ à commander. Dernière session 30/06. On continue ? »

[... session de travail ...]

JC: « /save »
Dobby: [met à jour thread-wildnexus.md avec les décisions et avancées de la session]
       « Thread files mis à jour : wildnexus ✅, ai-it-tools ✅ »
```

---

## Règles absolues

- Ne jamais supprimer l'historique — les entrées s'accumulent
- Toujours dater chaque mise à jour
- Si le thread file est stale > 14j → le signaler à JC
- Si un projet passe en veille (⚪) → ne pas supprimer le thread file, juste marquer le statut
- Template source : `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/thread-file-template.md`
