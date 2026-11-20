---
name: mind-reader
description: Introspection des patterns de communication JC↔Dobby — analyser le style de pensée, l'approche décisionnelle et les angles morts de JC à partir de la conversation, puis rafraîchir le « Profil cognitif » de USER.md. Déclencher sur "mind reader", "analyse mon profil", "mes angles morts", "introspection", "profil cognitif", "comment je pense". Adapté du prompt Instagram « Mind Reader Protocol » (@callme.wisdomhunter).
---

# Skill — mind-reader

> « Analyse mes patterns de communication d'après notre conversation. Dis-moi ce que tu observes de mon style de pensée, de mon approche décisionnelle et de mes angles morts potentiels. » — prompt source Instagram @callme.wisdomhunter. Dans PKA, ça sert à rafraîchir la section « Profil cognitif » de `USER.md` (dernier diagnostic : 2026-06-19).

## Pourquoi

`USER.md` contient un « Profil cognitif » (pensée stratigraphique, modalités dominantes, marqueurs rares) figé depuis 2026-06-19. JC évolue, les projets changent, le profil ne suit pas. Ce skill formalise la ré-observation périodique : Dobby relit la conversation récente et produit un diagnostic frais, à fusionner dans `USER.md` — pas à recréer.

## Ce que le skill produit

1. **Style de pensée** — comment JC structure ses demandes, décompose, argumente.
2. **Approche décisionnelle** — cap d'abord / étapes ensuite, arbitrage, réversibilité.
3. **Angles morts** — ce que JC ne voit pas, les patterns répétés, les sujets évités.

## Procédure

1. Relire les échanges récents (session courante, `_local/sessions/`, `TEAM_Inbox/` récent).
2. Produire le diagnostic en 3 blocs : style de pensée / approche décisionnelle / angles morts.
3. Comparer à la section « Profil cognitif » existante → lister les **écarts** (ce qui a changé, ce qui manque).
4. Proposer la mise à jour de `USER.md` (fusion, pas écrasement) — à valider par JC avant écriture.

## Règles

- **Observation, pas flatterie.** Signaler les angles morts réels, pas les qualités attendues.
- **Ne pas sur-interpréter.** Chaque affirmation s'appuie sur un exemple concret observé dans la conversation.
- **Cadence** : ponctuel, à la demande. Ne pas lancer à chaque session.

## Déclencheurs

- « mind reader », « analyse mon profil », « comment je pense ? »
- « mes angles morts », « fais mon introspection »
- « rafraîchis le profil cognitif »

## Livrable

Mise à jour proposée de la section « Profil cognitif » de `USER.md` (diff à valider par JC).

## Skills liés

- **`deep-psychology`** — descend d'un cran : le « pourquoi » subconscient d'un blocage précis (pas le profil global).
- **`conseil`** — stress-teste une décision ; ici on observe le décideur, pas la décision.
