# Brief — Dual-license WildNexus (MIT + ETHICS.md)

**De :** [[Dobby]] 🦉
**Pour :** [[Hermine]] ⬜ + [[Renard]] 🦊
**Date :** 2026-06-08
**Priorité :** M-02
**ADR lié :** ADR-010 — point de réserve R2

## Contexte

L'ADR-010 (Sécurité/RGPD Edge AI) a été révisé et passé en « accepté sous réserve ». La réserve R2 exige de trancher la licence du projet WildNexus avant publication publique.

La licence doit :
- Être compatible OSI (adoption écosystème open-source standard)
- Exclure explicitement les usages militaires et de surveillance de masse
- Être applicable à tout fork ou dérivé

La décision proposée dans l'ADR-010 est une **dual-license** : MIT pour le code + addendum éthique (ETHICS.md) dans les termes d'utilisation.

## Mission

1. **[[Hermine]]** : analyser la portée juridique d'un addendum éthique externe à la licence MIT. Est-ce que ça tient ? Quels précédents (Hippocratic License, JSON License, BSL) ? Risques de contournement ?

2. **[[Renard]]** : vérifier la validité contractuelle — un ETHICS.md à la racine du dépôt est-il opposable à un tiers ? Faut-il un CLA (Contributor License Agreement) ? Quelle juridiction ?

3. Livrable commun : un **fichier ETHICS.md** draft + une **note juridique** (2-3 paragraphes) expliquant la mécanique dual-license et ses limites.

## Format livrable

`YYYY-MM-DD_hermine_renard_wildnexus-dual-license.md` dans `TEAM_Inbox/`

## Deadline

Avant fermeture M-02 (prototype banc).

## Voir aussi

- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/ADR-010-securite-rgpd-edge-ai.md` — §6 Licence Ethical-Source
- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/WILDNEXUS_ADR_INDEX.md` — point R2
