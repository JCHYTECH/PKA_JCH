---
name: introspection-jc
description: Introspection psychologique de JC — deux modes : (1) profil cognitif global (style de pensée, approche décisionnelle, angles morts → rafraîchir le « Profil cognitif » de USER.md), (2) blocage précis (mécanisme subconscient + levier concret). Déclencher sur "mind reader", "analyse mon profil", "mes angles morts", "introspection", "profil cognitif", "comment je pense", "deep psychology", "pourquoi je tourne en rond", "mécanisme psychologique", "schéma subconscient", "qu'est-ce qui me bloque". Fusion de deep-psychology + mind-reader (2026-11-25). Prompts sources Instagram @callme.wisdomhunter.
---

# Skill — introspection-jc

> Fusion de `deep-psychology` + `mind-reader` (2026-11-25). Deux modes complémentaires : observer le **profil** (global) ou débloquer un **blocage** (précis).

## Pourquoi

`conseil` stress-teste la **décision** (logique, biais, modes d'échec). Il ne répond pas à deux questions :
- « Comment JC pense-t-il vraiment ? » → le **profil cognitif** (mode 1).
- « Pourquoi JC est bloqué sur ce sujet alors que la logique est claire ? » → le **blocage interne** (mode 2).

## Positionnement vs conseil

| | conseil | introspection-jc |
|---|---|---|
| Objet | la décision (go / no-go) | le décideur (profil) ou le blocage |
| Angle | logique, biais, modes d'échec | psychologie, motivation, schémas |
| Sortie | verdict actionnable | diagnostic de profil, ou hypothèse de mécanisme + levier |

## Mode 1 — Profil cognitif (ex-mind-reader)

### Ce que ça produit
1. **Style de pensée** — comment JC structure ses demandes, décompose, argumente.
2. **Approche décisionnelle** — cap d'abord / étapes ensuite, arbitrage, réversibilité.
3. **Angles morts** — ce que JC ne voit pas, les patterns répétés, les sujets évités.

### Procédure
1. Relire les échanges récents (session courante, `_local/sessions/`, `TEAM_Inbox/` récent).
2. Produire le diagnostic en 3 blocs.
3. Comparer à la section « Profil cognitif » de `USER.md` → lister les **écarts** (ce qui a changé, ce qui manque).
4. Proposer la mise à jour de `USER.md` (fusion, pas écrasement) — à valider par JC avant écriture.

### Règles
- **Observation, pas flatterie.** Signaler les angles morts réels, pas les qualités attendues.
- **Ne pas sur-interpréter.** Chaque affirmation s'appuie sur un exemple concret observé dans la conversation.
- **Cadence** : ponctuel, à la demande. Ne pas lancer à chaque session.

## Mode 2 — Blocage (ex-deep-psychology)

### Procédure
1. **Cadrer** : quelle situation/problème ? quelle manifestation concrète (procrastination, évitement, sur-ingénierie, perfectionnisme, hésitation sur une décision irréversible…) ?
2. **Formuler 2–4 hypothèses** de mécanismes sous-jacents (ex. « évitement d'un engagement irréversible », « besoin de tout maîtriser avant d'agir », « peur de la critique publique »).
3. **Pour chaque hypothèse** : l'indice qui l'appuie + le **levier** concret qui la débloquerait.
4. Livrer en 3 blocs : mécanisme probable / indices / levier proposé.

### Règles
- **Hypothèses, pas verdicts.** Ce skill formule des mécanismes plausibles, pas des diagnostics définitifs. Préfixer l'incertitude.
- **Levier actionnable** — chaque hypothèse débouche sur un « que faire » concret, sinon c'est de la spéculation.
- **Respecter JC** — rester factuel et utile, pas de psychologisation gratuite.

## Déclencheurs

- **Mode 1** : « mind reader », « analyse mon profil », « comment je pense ? », « mes angles morts », « fais mon introspection », « rafraîchis le profil cognitif »
- **Mode 2** : « deep psychology », « pourquoi je tourne en rond sur X », « qu'est-ce qui me bloque ? », « mécanisme psychologique », « schéma subconscient »

## Livrable

- **Mode 1** : mise à jour proposée de la section « Profil cognitif » de `USER.md` (diff à valider par JC).
- **Mode 2** : réponse dans le chat + note dans `TEAM_Inbox/` si le blocage est récurrent (à reconsulter plus tard).

## Skills liés

- **`conseil`** — complémentaire : conseil tranche, introspection-jc observe/débloque.
- **`compound-memoire`** — si le blocage révèle une règle durable, la capturer en « erreur → règle ».
