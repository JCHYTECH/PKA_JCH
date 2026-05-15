---
date: 2026-04-22
source: chat Claude — méta-prompt
domain: Prompts / méta
tags: [prompt, meta, reverse-engineering, template, workflow]
status: ready
---

# Reverse Prompt — Reconstruire le prompt idéal d'un chat

Méta-prompt à coller en fin de conversation Claude pour obtenir le prompt unique qui aurait conduit au même résultat sans itérations.

## Quand l'utiliser

- En fin de chat productif, pour capitaliser un pattern réutilisable
- Quand un type de demande revient (ex. fiches espèces, exports vault, configurations Canon)
- Pour transformer un échange exploratoire en template stable

## Quand ne PAS l'utiliser

- Sur un chat très court (1-2 échanges) — pas assez de matière à analyser
- Sur un chat dont l'objectif a fortement évolué — le prompt généré ne capturera que la version finale

---

## Prompt à coller

```
Analyse rétrospectivement l'ensemble de cette conversation et produis
le prompt unique qui m'aurait permis d'obtenir le résultat final
directement, sans les allers-retours intermédiaires.

Procède en trois temps :

1. DIAGNOSTIC (bref, en prose)
   - Quel était l'objectif réel atteint en fin de chat ?
   - Quelles informations as-tu dû me demander ou inférer en cours
     de route ?
   - Quels malentendus ou détours ont allongé la conversation ?

2. PROMPT RECONSTRUIT (bloc de code)
   Structure :
   - Rôle / expertise attendue
   - Contexte utilisateur pertinent (ce que tu aurais dû savoir
     d'emblée)
   - Objectif précis et livrable attendu
   - Contraintes techniques (OS, outils, formats, versions)
   - Format de sortie exact (fichier, structure, frontmatter, etc.)
   - Critères de qualité ou de refus
   - Ton et style de réponse

3. NOTES D'USAGE (liste courte)
   - Variables à adapter selon le projet (ex. {nom_session},
     {chemin_vault})
   - Préférences déjà couvertes par mon profil utilisateur — donc
     à ne PAS dupliquer
   - Limites connues du prompt (cas qu'il ne couvre pas)

Le prompt reconstruit doit être autonome : un assistant qui le reçoit
sans contexte préalable doit pouvoir produire le même livrable final
en une seule passe.
```

---

## Notes

- Version slash command installée à `~/.claude/commands/reverse-prompt.md` (déclenchable via `/reverse-prompt` dans Claude Code)
- Les prompts reconstruits peuvent être archivés dans `JCH VAULT/Prompts/` selon leur domaine
- Limite connue : le prompt généré reflète l'état final ; il ne capture pas le cheminement d'apprentissage si celui-ci faisait partie de la valeur du chat
